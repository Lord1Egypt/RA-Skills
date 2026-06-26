"""Juejin Skills - Juejin (juejin.cn) operation skill package."""

from juejin_skill.api import JuejinAPI
from juejin_skill.auth import JuejinAuth
from juejin_skill.hot_articles import HotArticles
from juejin_skill.publisher import ArticlePublisher
from juejin_skill.downloader import ArticleDownloader

__all__ = [
    "JuejinAPI",
    "JuejinAuth",
    "HotArticles",
    "ArticlePublisher",
    "ArticleDownloader",
]

__version__ = "1.0.8"