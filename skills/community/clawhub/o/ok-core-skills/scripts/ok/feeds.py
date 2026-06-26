"""OK.com 首页推荐帖子获取"""

from __future__ import annotations

import logging

from .client.base import BaseClient
from .human import medium_delay
from .locale import build_locale
from .search import _extract_listings
from .types import Listing
from .urls import build_base_url

logger = logging.getLogger("ok-feeds")


def list_feeds(
    bridge: BaseClient,
    country: str = "singapore",
    city: str = "singapore",
    lang: str = "en",
    max_results: int = 20,
) -> list[Listing]:
    """获取首页推荐帖子

    Args:
        bridge: BridgeClient 实例
        country: 国家
        city: 城市 code
        lang: 语言
        max_results: 最大返回结果数

    Returns:
        帖子列表
    """
    locale = build_locale(country, city, lang)
    url = build_base_url(locale.subdomain, locale.lang, locale.city)

    bridge.navigate(url)
    bridge.wait_dom_stable(timeout=15000)
    medium_delay()

    listings = _extract_listings(bridge, max_results)
    logger.info(
        "首页推荐 %s/%s: 获取 %d 条帖子",
        country, city, len(listings),
    )
    return listings
