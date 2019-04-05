# -*- coding: utf-8 -*-
import scrapy
import json

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem


class CartaCapitalSpider(scrapy.Spider):
    name = 'carta_capital'
    allowed_domains = ['cartacapital.com.br']
    start_urls = []

    def __init__(self, *a, **kw):
        super(CartaCapitalSpider, self).__init__(*a, **kw)
        with open('frontier/carta_capital.json') as json_file:
                data = json.load(json_file)
        self.start_urls = list(data.values())

    def parse(self, response):

        for href in response.css("div.eltdf-wrapper-inner a::attr(href)"):
            print(href)
            yield response.follow(href, self.scrap_url, meta={'url', response.url}

        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
    

    def scrap_url(self, response):
        yield {
            'categoria' : response.css("div.eltdf-post-info-category > a::text").get(default='').strip(),
            'titulo': response.css("a.eltdf-pt-link::text").get(default='').strip(),
            'subtitulo': response.css("div.wpb_wrapper > h3::text").get(default='').strip(),
            'url': response.url,
            'autor': response.css("a.eltdf-post-info-author-link::text").get(default='').strip(),
            'data': response.css("div.eltdf-post-info-date > a::text").get(default='').strip(),
            'texto': response.css("div.eltdf-post-text-inner > a::text, div.eltdf-post-text-inner > p::text").getall()
        }