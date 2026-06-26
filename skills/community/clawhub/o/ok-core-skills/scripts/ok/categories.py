"""OK.com 分类浏览"""

from __future__ import annotations

import logging

from .client.base import BaseClient
from .human import medium_delay
from .locale import build_locale
from .search import _extract_listings, _filter_by_price
from .types import Listing
from .urls import build_category_url

logger = logging.getLogger("ok-categories")


def browse_category(
    bridge: BaseClient,
    category_code: str,
    country: str = "singapore",
    city: str = "singapore",
    lang: str = "en",
    max_results: int = 20,
    price_min: float | None = None,
    price_max: float | None = None,
) -> list[Listing]:
    """按分类浏览帖子

    Args:
        bridge: BridgeClient 实例
        category_code: 分类 code（如 "marketplace", "jobs", "property"）
        country: 国家
        city: 城市 code
        lang: 语言
        max_results: 最大返回结果数
        price_min: 最低价格（含），None 表示不限
        price_max: 最高价格（含），None 表示不限

    Returns:
        帖子列表
    """
    locale = build_locale(country, city, lang)
    url = build_category_url(locale.subdomain, locale.lang, locale.city, category_code)

    bridge.navigate(url)
    bridge.wait_dom_stable(timeout=15000)
    medium_delay()

    fetch_count = max_results * 3 if (price_min or price_max) else max_results
    listings = _extract_listings(bridge, fetch_count)
    listings = _filter_by_price(listings, price_min, price_max)
    listings = listings[:max_results]

    logger.info(
        "浏览分类 '%s' 在 %s/%s: 找到 %d 条帖子",
        category_code, country, city, len(listings),
    )
    return listings
