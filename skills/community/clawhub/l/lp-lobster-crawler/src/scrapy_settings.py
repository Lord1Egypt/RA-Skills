"""Scrapy settings for lobster-crawler-skill project."""

BOT_NAME = "lobster_crawler"

SPIDER_MODULES = ["src.spiders"]
NEWSPIDER_MODULE = "src.spiders"

# 部分站点的 robots.txt 会阻止合法抓取，按需在爬虫 custom_settings 中覆盖
ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 8
DOWNLOAD_DELAY = 1.5

DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8",
}

DOWNLOADER_MIDDLEWARES = {
    "src.spiders.middlewares.RandomUserAgentMiddleware": 400,
    "src.spiders.middlewares.TlsImpersonateMiddleware": 500,
    "src.spiders.middlewares.RetryOnErrorMiddleware": 550,
}

ITEM_PIPELINES = {
    "src.spiders.pipelines.SQLitePipeline": 300,
}

LOG_LEVEL = "INFO"
