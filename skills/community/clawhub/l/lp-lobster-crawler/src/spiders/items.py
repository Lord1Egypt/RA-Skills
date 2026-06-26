"""Scrapy Item 定义。"""

import scrapy


class NovelItem(scrapy.Item):
    """小说/作品 Item。"""
    site = scrapy.Field()
    external_id = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    category = scrapy.Field()
    status = scrapy.Field()
    summary = scrapy.Field()
    cover_url = scrapy.Field()
    url = scrapy.Field()


class ChapterItem(scrapy.Item):
    """章节 Item。"""
    site = scrapy.Field()
    novel_external_id = scrapy.Field()
    external_id = scrapy.Field()
    index = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    word_count = scrapy.Field()
    publish_date = scrapy.Field()


class EpisodeItem(scrapy.Item):
    """剧集 Item（短剧类站点）。"""
    site = scrapy.Field()
    novel_external_id = scrapy.Field()
    external_id = scrapy.Field()
    index = scrapy.Field()
    title = scrapy.Field()
    media_url = scrapy.Field()
    duration = scrapy.Field()
    thumbnail_url = scrapy.Field()
    publish_date = scrapy.Field()
