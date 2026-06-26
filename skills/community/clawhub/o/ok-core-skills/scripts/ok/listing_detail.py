"""OK.com 帖子详情获取"""

from __future__ import annotations

import logging

from . import selectors as sel
from .client.base import BaseClient
from .errors import OKElementNotFound
from .human import medium_delay
from .types import ListingDetail

logger = logging.getLogger("ok-listing-detail")

_EXTRACT_JS = f"""
(() => {{
    const title = document.querySelector("{sel.DETAIL_TITLE}")?.textContent?.trim() || '';
    const price = document.querySelector("{sel.DETAIL_PRICE}")?.textContent?.trim() || '';
    const desc = document.querySelector("{sel.DETAIL_DESCRIPTION}")?.textContent?.trim() || '';
    const seller = document.querySelector("{sel.DETAIL_SELLER}")?.textContent?.trim() || '';
    const location = document.querySelector("{sel.DETAIL_LOCATION}")?.textContent?.trim() || '';

    // Real post images: lazy-loaded imgs whose src points to ok.com/post/image
    const images = Array.from(document.querySelectorAll("{sel.DETAIL_IMAGES}"))
        .map(img => img.src)
        .filter(s => s && s.includes("ok.com/post/image"));

    const category = Array.from(document.querySelectorAll("{sel.DETAIL_CATEGORY}"))
        .map(a => a.textContent?.trim()).filter(Boolean).join(' > ');

    // Posted time: extracted from page text "ADDED ON DEC 02, 2025"
    const dateMatch = document.body.innerText.match(/ADDED ON\\s+([A-Za-z]+ \\d+,\\s*\\d+)/i);
    const postedTime = dateMatch ? dateMatch[1] : '';

    // Property features (bedrooms, bathrooms, etc.)
    const ICON_MAP = {{
        'Bedrooms': 'bedrooms', 'Bathrooms': 'bathrooms',
        'Parking': 'parking', 'Area': 'area', 'Size': 'size',
        'Floor': 'floor', 'Rooms': 'rooms',
    }};
    const features = {{}};
    document.querySelectorAll("{sel.DETAIL_FEATURE_ITEM}").forEach(item => {{
        const icon = item.querySelector("img");
        const valEl = item.querySelector("{sel.DETAIL_FEATURE_VALUE}");
        const val = valEl?.textContent?.trim() || '';
        if (!val) return;
        if (icon && icon.src) {{
            const filename = icon.src.split("/").pop().replace(".png", "").replace(".svg", "");
            const key = ICON_MAP[filename] || filename.toLowerCase();
            features[key] = val;
        }} else {{
            features['type'] = val;
        }}
    }});

    return {{ title, price, description: desc, seller, location,
             postedTime, images, category, features }};
}})()
"""


def _build_detail(result: dict, url: str) -> ListingDetail:
    return ListingDetail(
        title=result.get("title", ""),
        price=result.get("price") or None,
        description=result.get("description") or None,
        location=result.get("location") or None,
        seller_name=result.get("seller") or None,
        images=result.get("images", []),
        url=url,
        category=result.get("category") or None,
        posted_time=result.get("postedTime") or None,
        features=result.get("features") or {},
    )


def get_listing_detail(bridge: BaseClient, url: str) -> ListingDetail:
    """进入帖子详情页并提取信息"""
    bridge.navigate(url)
    bridge.wait_dom_stable(timeout=15000)
    medium_delay()

    result = bridge.evaluate(_EXTRACT_JS)
    if not result or not result.get("title"):
        raise OKElementNotFound("帖子详情提取失败，可能页面未正确加载")

    detail = _build_detail(result, url)
    logger.info("获取帖子详情: %s", detail.title[:50])
    return detail


def get_listing_detail_from_page(bridge: BaseClient) -> ListingDetail:
    """从当前页面提取帖子详情"""
    url = bridge.get_url()

    result = bridge.evaluate(_EXTRACT_JS)
    if not result:
        raise OKElementNotFound("帖子详情提取失败")

    return _build_detail(result, url)
