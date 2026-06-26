#!/usr/bin/env python3
"""
maishou88.com data-layer client — derived from shopmind-price-compare v2.2.0
by xiaohaook (https://clawhub.ai/skills/shopmind-price-compare).

This file is a thin async client over the public maishou88.com API. The HTTP
endpoints, request shape, default headers, OPENID seed, and item-construction
logic are reused from the upstream `shopmind-price-compare` skill verbatim;
all credit to the original author. See README.md → Acknowledgements.

Reused under fair-use / community-standard practice for ClawHub skills (which
are publicly published as `public, open, and visible to everyone for sharing
and reuse` per ClawHub's own description). If the upstream author objects we
will switch to a clean-room reimplementation.

This file lives inside price-check so the skill no longer depends on having
shopmind-price-compare installed alongside it.
"""
from __future__ import annotations

import asyncio
import os
from typing import Any

import aiohttp


# ---------- API endpoints + authentication seeds ----------
INVITE_CODE = os.getenv("MAISHOU_INVITE_CODE") or "6110440"
OPENID = "564bdce0fa408fc9e1d5d42fd022ef0b"
API_BASE = "https://appapi.maishou88.com"
SHARE_API = "https://msapi.maishou88.com"

HEADERS = {
    "Accept": "application/json",
    "Referer": "https://hnbc018.kuaizhan.com/",
    "User-Agent": "Mozilla/5.0 AppleWebKit/537 Chrome/143 Safari/537",
}

PLATFORM_MAP: dict[str, str] = {
    "0": "全部", "1": "淘宝/天猫", "2": "京东", "3": "拼多多",
    "4": "苏宁", "5": "唯品会", "6": "考拉",
    "7": "抖音", "8": "快手", "10": "1688",
}


# ---------- helpers ----------
def calc_savings(item: dict[str, Any]) -> dict[str, Any]:
    """Compute final price after coupon, savings amount, and discount string."""
    price = float(item.get("actualPrice") or 0)
    original = float(item.get("originalPrice") or price)
    coupon = float(item.get("couponPrice") or 0)
    final = max(price - coupon, 0) if coupon > 0 else price
    saved = original - final
    discount = round((final / original) * 10, 1) if original > 0 else 10
    return {
        "finalPrice": round(final, 2),
        "saved": round(saved, 2),
        "discount": f"{discount}折" if discount < 10 else "无折扣",
        "hasCoupon": coupon > 0,
        "couponAmount": coupon,
    }


# ---------- search ----------
async def fetch_search_items(
    session: aiohttp.ClientSession,
    keyword: str,
    source: str = "0",
    page: int = 1,
    sort: str = "price",
    coupon: str = "0",
    min_price: float = 0,
    max_price: float = 999999,
) -> dict[str, Any]:
    """Multi-platform search; returns dict with items / stats / message keys.

    items[] has the raw shape produced by the upstream `_fetch_search_items`,
    so price_check.py's `_normalize_item` continues to work unchanged.
    """
    resp = await session.post(
        f"{API_BASE}/api/v1/homepage/searchList",
        headers={
            **HEADERS,
            "User-Agent": "MaiShouApp/3.7.7 (iPhone; iOS 26.3; Scale/3.00)",
            "openid": OPENID,
            "version": "3.7.7.2",
        },
        data={
            "isCoupon": 1 if coupon == "1" else 0,
            "keyword": str(keyword),
            "openid": OPENID,
            "order": "desc",
            "page": int(page),
            "pddListId": "",
            "sort": "",
            "sourceType": str(source),
            "user_id": "",
        },
    )
    data = await resp.json(encoding="utf-8-sig") or {}
    rows = data.get("data") or []
    if not rows:
        return {
            "items": [],
            "stats": {"count": 0, "lowestPrice": 0, "highestPrice": 0,
                      "avgPrice": 0, "couponCount": 0, "maxSaved": 0},
            "message": data.get("message") or "未找到相关商品",
        }

    items: list[dict[str, Any]] = []
    for v in rows:
        savings = calc_savings(v)
        items.append({
            "goodsId": v.get("goodsId"),
            "source": v.get("sourceType"),
            "sourceName": PLATFORM_MAP.get(str(v.get("sourceType")), "未知"),
            "title": v.get("title"),
            "shopName": v.get("shopName") or "",
            "originalPrice": float(v.get("originalPrice") or 0),
            "price": float(v.get("actualPrice") or 0),
            "finalPrice": savings["finalPrice"],
            "couponAmount": savings["couponAmount"],
            "saved": savings["saved"],
            "discount": savings["discount"],
            "hasCoupon": savings["hasCoupon"],
            "commission": v.get("commission") or "0",
            "monthSales": v.get("monthSales") or 0,
            "imageUrl": v.get("picUrl") or "",
        })

    min_p, max_p = float(min_price), float(max_price)
    items = [i for i in items if min_p <= i["finalPrice"] <= max_p]

    if sort == "price":
        items.sort(key=lambda x: x["finalPrice"])
    elif sort == "price_desc":
        items.sort(key=lambda x: x["finalPrice"], reverse=True)
    elif sort == "sales":
        def parse_sales(s: Any) -> float:
            s = str(s).replace("+", "").replace("万", "0000")
            try:
                return float(s)
            except ValueError:
                return 0.0
        items.sort(key=lambda x: parse_sales(x["monthSales"]), reverse=True)
    elif sort == "discount":
        items.sort(key=lambda x: x["saved"], reverse=True)
    elif sort == "commission":
        items.sort(key=lambda x: float(x["commission"]), reverse=True)

    for idx, item in enumerate(items):
        item["rank"] = idx + 1

    prices = [i["finalPrice"] for i in items if i["finalPrice"] > 0]
    stats = {
        "count": len(items),
        "lowestPrice": min(prices) if prices else 0,
        "highestPrice": max(prices) if prices else 0,
        "avgPrice": round(sum(prices) / len(prices), 2) if prices else 0,
        "couponCount": sum(1 for i in items if i["hasCoupon"]),
        "maxSaved": max((i["saved"] for i in items), default=0),
    }
    return {"items": items, "stats": stats, "message": None}


# ---------- goods detail (buy URL + Taobao share code) ----------
async def fetch_goods_detail(
    session: aiohttp.ClientSession,
    goods_id: str,
    source: str = "1",
) -> dict[str, Any]:
    """Fetch a single product's detail + share link in parallel.

    Returns {detail, link, buy_url, copy_cmd}.
    """
    params = {
        "goodsId": str(goods_id),
        "sourceType": str(source),
        "inviteCode": INVITE_CODE,
        "supplierCode": "",
        "activityId": "",
        "isShare": "1",
        "token": "",
    }

    detail_resp, link_resp = await asyncio.gather(
        session.post(f"{API_BASE}/api/v3/goods/detail",
                     json={**params, "keyword": "", "usageScene": 5}),
        session.post(f"{SHARE_API}/api/v1/share/getTargetUrl",
                     json={**params, "isDirectDetail": 0}),
    )
    detail_data = (await detail_resp.json(encoding="utf-8-sig") or {}).get("data") or {}
    link_data = (await link_resp.json(encoding="utf-8-sig") or {}).get("data") or {}
    buy_url = link_data.get("appUrl") or link_data.get("schemaUrl") or ""
    copy_cmd = link_data.get("kl") or ""

    return {
        "detail": detail_data,
        "link": link_data,
        "buy_url": buy_url,
        "copy_cmd": copy_cmd,
    }
