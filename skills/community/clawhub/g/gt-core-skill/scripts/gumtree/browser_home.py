from __future__ import annotations

import json
from typing import Any

from .bridge import BridgePage
from .browser_urls import build_home_url
from .errors import BrowserAutomationError

_EXTRACT_HOME_RECOMMENDATIONS_JS = """
(() => {
  const fail = (message) => {
    throw new Error(message);
  };
  const normalizeText = (value) => String(value ?? "").replace(/\\s+/g, " ").trim();
  const expectObject = (value, message) => {
    if (!value || typeof value !== "object" || Array.isArray(value)) {
      fail(message);
    }
    return value;
  };
  const expectArray = (value, message) => {
    if (!Array.isArray(value)) {
      fail(message);
    }
    return value;
  };
  const expectString = (value, message) => {
    const text = normalizeText(value);
    if (!text) {
      fail(message);
    }
    return text;
  };
  const expectBoolean = (value, message) => {
    if (typeof value !== "boolean") {
      fail(message);
    }
    return value;
  };
  const expectFiniteNumber = (value, message) => {
    if (typeof value !== "number" || !Number.isFinite(value)) {
      fail(message);
    }
    return value;
  };
  const optionalString = (value) => {
    const text = normalizeText(value);
    return text || null;
  };
  const optionalBoolean = (value) => {
    if (typeof value !== "boolean") {
      return null;
    }
    return value;
  };
  const optionalFiniteNumber = (value) => {
    if (typeof value !== "number" || !Number.isFinite(value)) {
      return null;
    }
    return value;
  };
  const toAbsoluteUrl = (value) => {
    const text = normalizeText(value);
    if (!text) {
      return null;
    }
    try {
      return new URL(text, window.location.origin).toString();
    } catch {
      return null;
    }
  };

  const rawClientData = window.clientData;
  if (rawClientData == null) {
    fail("window.clientData 缺失");
  }
  let clientData;
  if (typeof rawClientData === "string") {
    try {
      clientData = JSON.parse(decodeURIComponent(rawClientData));
    } catch (error) {
      fail(`window.clientData 解析失败: ${error.message}`);
    }
  } else if (typeof rawClientData === "object" && !Array.isArray(rawClientData)) {
    clientData = rawClientData;
  } else {
    fail("window.clientData 格式异常");
  }

  const root = expectObject(clientData, "clientData 格式异常");
  const page = expectObject(root.page, "clientData.page 缺失");
  const socialData = expectObject(root.socialData, "clientData.socialData 缺失");
  const userFeed = expectObject(root.userFeed, "clientData.userFeed 缺失");
  const recommendedAds = expectArray(userFeed.recommendedAds, "clientData.userFeed.recommendedAds 缺失");

  const items = recommendedAds.flatMap((item, index) => {
    if (!item || typeof item !== "object" || Array.isArray(item)) {
      return [];
    }
    const row = item;
    const price = row.price && typeof row.price === "object" && !Array.isArray(row.price) ? row.price : null;
    const priceAmount = optionalFiniteNumber(price?.amount);
    const listingId = optionalFiniteNumber(row.id);
    const title = optionalString(row.title);
    const url = toAbsoluteUrl(row.path);
    if (!title && !url && listingId == null) {
      return [];
    }
    return [{
      listing_id: listingId == null ? null : String(listingId),
      title,
      description: optionalString(row.shortDescription),
      price: priceAmount == null ? null : priceAmount / 100,
      price_pennies: priceAmount,
      price_currency: optionalString(price?.currency),
      location: optionalString(row.location),
      url,
      image_url: toAbsoluteUrl(row.imageUrl || row.pictureUrl),
      age: optionalString(row.timeSincePosted),
      number_of_images: optionalFiniteNumber(row.numberOfImages),
      category: optionalString(row.category),
      top_level_category: optionalString(row.l1Category),
      spotlight: optionalBoolean(row.spotlight),
      delivery_available: optionalBoolean(row.supportShipping),
    }];
  });

  return JSON.stringify({
    source: "clientData.userFeed.recommendedAds",
    meta: {
      page_type: optionalString(page.type),
      page_title: optionalString(page.title),
      location_name: optionalString(socialData.location),
      total_recommendations: recommendedAds.length,
    },
    items,
  });
})()
"""


def run_browser_home_recommendations(
    page: BridgePage,
    limit: int = 10,
) -> dict[str, Any]:
    home_url = build_home_url()
    page.navigate(home_url)
    page.wait_for_load()
    page.wait_dom_stable(timeout=15000)

    raw = page.evaluate(_EXTRACT_HOME_RECOMMENDATIONS_JS)
    if not raw:
        raise BrowserAutomationError("未能从 Gumtree 首页提取推荐结果")

    payload = json.loads(raw)
    if not isinstance(payload, dict):
        raise BrowserAutomationError("首页推荐结果格式异常")

    items = payload.get("items")
    if not isinstance(items, list):
        raise BrowserAutomationError("首页推荐结果格式异常")

    meta = payload.get("meta")
    if not isinstance(meta, dict):
        raise BrowserAutomationError("首页推荐元信息格式异常")

    display_item_fields = (
        "title",
        "description",
        "price",
        "price_currency",
        "location",
        "url",
        "image_url",
        "age",
        "number_of_images",
        "category",
        "top_level_category",
        "spotlight",
        "delivery_available",
    )

    cleaned = []
    for item in items:
        if not isinstance(item, dict):
            continue
        cleaned.append({field: item.get(field) for field in display_item_fields})

    limited = cleaned[:limit]
    return {
        "ok": True,
        "mode": "browser",
        "source": payload.get("source"),
        "page_type": meta.get("page_type"),
        "page_title": meta.get("page_title"),
        "location_name": meta.get("location_name"),
        "home_url": home_url,
        "items": limited,
        "total": len(limited),
        "total_recommendations": meta.get("total_recommendations"),
    }
