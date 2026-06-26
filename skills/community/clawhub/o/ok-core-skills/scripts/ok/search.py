"""OK.com 搜索帖子"""

from __future__ import annotations

import logging
import re

from . import selectors as sel
from .client.base import BaseClient
from .errors import OKElementNotFound
from .human import medium_delay, short_delay
from .locale import build_locale
from .types import Listing, SearchResult
from .urls import build_base_url

logger = logging.getLogger("ok-search")


def _parse_price(price_str: str | None) -> float | None:
    """Extract numeric value from price string like '$2,250,000' or '¥30,000'."""
    if not price_str:
        return None
    digits = re.sub(r"[^\d.]", "", price_str)
    if not digits:
        return None
    try:
        return float(digits)
    except ValueError:
        return None


def _filter_by_price(
    listings: list[Listing],
    price_min: float | None,
    price_max: float | None,
) -> list[Listing]:
    """Filter listings by price range. Drops items with unparseable prices."""
    if price_min is None and price_max is None:
        return listings

    filtered = []
    for item in listings:
        val = _parse_price(item.price)
        if val is None:
            continue
        if price_min is not None and val < price_min:
            continue
        if price_max is not None and val > price_max:
            continue
        filtered.append(item)
    return filtered


def search_listings(
    bridge: BaseClient,
    keyword: str,
    country: str = "singapore",
    city: str = "singapore",
    lang: str = "en",
    max_results: int = 20,
    price_min: float | None = None,
    price_max: float | None = None,
) -> SearchResult:
    """搜索帖子

    Args:
        bridge: BridgeClient 实例
        keyword: 搜索关键词
        country: 国家
        city: 城市 code
        lang: 语言
        max_results: 最大返回结果数
        price_min: 最低价格（含），None 表示不限
        price_max: 最高价格（含），None 表示不限

    Returns:
        SearchResult 对象
    """
    locale = build_locale(country, city, lang)

    # 导航到搜索所在城市页面
    base_url = build_base_url(locale.subdomain, locale.lang, locale.city)
    bridge.navigate(base_url)
    bridge.wait_dom_stable()
    medium_delay()

    # 在搜索框输入关键词
    try:
        bridge.wait_for_selector(sel.SEARCH_INPUT, timeout=15000)
    except Exception:
        raise OKElementNotFound("搜索框未找到")

    bridge.click_element(sel.SEARCH_INPUT)
    short_delay()
    bridge.input_text(sel.SEARCH_INPUT, keyword)
    short_delay()

    # 按回车或点击搜索按钮
    bridge.send_command("press_key", {"key": "Enter"})
    medium_delay()

    # 等待搜索结果加载
    bridge.wait_dom_stable(timeout=15000)
    medium_delay()

    # 提取搜索结果（多取一些以应对价格过滤后数量减少）
    fetch_count = max_results * 3 if (price_min or price_max) else max_results
    listings = _extract_listings(bridge, fetch_count)
    listings = _filter_by_price(listings, price_min, price_max)
    listings = listings[:max_results]

    result = SearchResult(
        keyword=keyword,
        total_count=len(listings),
        listings=listings,
        locale=locale,
    )

    logger.info("搜索 '%s' 在 %s/%s: 找到 %d 条结果", keyword, country, city, len(listings))
    return result


def _extract_listings(bridge: BaseClient, max_results: int = 20) -> list[Listing]:
    """从当前页面提取帖子列表

    优先使用 LISTING_CARD 选择器（带样式类的卡片组件），
    如果找不到则降级到 JS 模式：遍历所有 <a> 链接，
    通过 URL 路径模式 /cate-xxx/slug/ 区分帖子和分类导航。
    """
    js = f"""
    (() => {{
        const maxResults = {max_results};
        let cards = [...document.querySelectorAll("{sel.LISTING_CARD}")];

        if (cards.length > 0) {{
            return cards.slice(0, maxResults).map(card => {{
                const link = card.querySelector('a') || card.closest('a');
                const titleEl = card.querySelector("{sel.CARD_TITLE}");
                const priceEl = card.querySelector("{sel.CARD_PRICE}");
                const locationEl = card.querySelector("{sel.CARD_LOCATION}");
                const imgEl = card.querySelector("{sel.CARD_IMAGE}");
                return {{
                    title: titleEl?.textContent?.trim() || card.textContent?.trim()?.substring(0, 200) || '',
                    price: priceEl?.textContent?.trim() || '',
                    location: locationEl?.textContent?.trim() || '',
                    url: link?.href || '',
                    image: imgEl?.src || '',
                }};
            }});
        }}

        // 降级：从页面链接中筛选帖子详情链接
        // 帖子 URL: /cate-xxx/slug/  分类 URL: /cate-xxx/
        const listingPattern = /\\/cate-[^/]+\\/[^/]+\\//;
        const catOnlyPattern = /\\/cate-[^/]+\\/$/;
        const seen = new Set();
        const results = [];
        for (const a of document.querySelectorAll('a[href*="/cate-"]')) {{
            const href = a.href;
            if (!href || catOnlyPattern.test(new URL(href).pathname)) continue;
            if (!listingPattern.test(new URL(href).pathname)) continue;
            if (seen.has(href)) continue;
            seen.add(href);
            const text = a.textContent?.trim()?.substring(0, 200) || '';
            if (!text) continue;
            const imgEl = a.querySelector('img');
            results.push({{
                title: text,
                price: '',
                location: '',
                url: href,
                image: imgEl?.src || '',
            }});
            if (results.length >= maxResults) break;
        }}
        return results;
    }})()
    """

    results = bridge.evaluate(js)
    if not results or not isinstance(results, list):
        logger.info("页面上找到 0 个帖子卡片")
        return []

    logger.info("页面上找到 %d 个帖子卡片", len(results))
    listings = []
    for r in results:
        if not r:
            continue
        listings.append(Listing(
            title=r.get("title", ""),
            price=r.get("price") or None,
            location=r.get("location") or None,
            url=r.get("url") or None,
            image_url=r.get("image") or None,
        ))
    return listings
