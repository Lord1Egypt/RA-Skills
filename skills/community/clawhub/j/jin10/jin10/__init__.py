"""
Jin10 金十数据 API 客户端
模块化设计，支持按需导入
"""

from .client import Jin10Client, Jin10Error, BaseClient
from .quotes import QuotesClient, COMMON_QUOTES, Quote, QuoteCode, Kline, KlineResult
from .flash import FlashClient, FlashItem
from .news import NewsClient, NewsItem, NewsDetail
from .calendar import CalendarClient, CalendarEvent, STAR_LABELS

__all__ = [
    'Jin10Client',
    'Jin10Error',
    'BaseClient',
    'QuotesClient',
    'COMMON_QUOTES',
    'Quote',
    'QuoteCode',
    'Kline',
    'KlineResult',
    'FlashClient',
    'FlashItem',
    'NewsClient',
    'NewsItem',
    'NewsDetail',
    'CalendarClient',
    'CalendarEvent',
    'STAR_LABELS',
]

__version__ = '2.0.0'
