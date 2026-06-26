from __future__ import annotations

import json
from typing import Any

from .bridge import BridgePage
from .browser_urls import build_favourites_url
from .errors import BrowserAutomationError

_EXTRACT_FAVOURITES_JS = """
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
  const decodeClientData = () => {
    const rawClientData = window.clientData;
    if (rawClientData == null) {
      fail("window.clientData 缺失");
    }
    if (typeof rawClientData === "string") {
      try {
        return JSON.parse(decodeURIComponent(rawClientData));
      } catch (error) {
        fail(`window.clientData 解析失败: ${error.message}`);
      }
    }
    if (typeof rawClientData === "object" && !Array.isArray(rawClientData)) {
      return rawClientData;
    }
    fail("window.clientData 格式异常");
  };

  const clientData = expectObject(decodeClientData(), "clientData 格式异常");
  const page = expectObject(clientData.page, "clientData.page 缺失");
  const request = expectObject(clientData.request, "clientData.request 缺失");
  const favouriteAds = expectObject(clientData.favouriteAds, "clientData.favouriteAds 缺失");
  const adverts = expectArray(favouriteAds.adverts, "clientData.favouriteAds.adverts 缺失");
  const userData = clientData.userData && typeof clientData.userData === "object" && !Array.isArray(clientData.userData)
    ? clientData.userData
    : null;

  const items = adverts.flatMap((item) => {
    if (!item || typeof item !== "object" || Array.isArray(item)) {
      return [];
    }

    const attributes = Array.isArray(item.attributes)
      ? item.attributes.flatMap((attribute) => {
          if (!attribute || typeof attribute !== "object" || Array.isArray(attribute)) {
            return [];
          }
          const name = optionalString(attribute.name);
          const value = optionalString(attribute.value);
          if (!name || !value) {
            return [];
          }
          return [{
            name,
            value,
            key: optionalString(attribute.key),
            unit: optionalString(attribute.unit),
          }];
        })
      : [];

    const additionalImageUrls = Array.isArray(item.additionalImageUrls)
      ? item.additionalImageUrls.map((url) => toAbsoluteUrl(url)).filter(Boolean)
      : [];

    const url = toAbsoluteUrl(item.path);
    const title = optionalString(item.title);
    const listingId = optionalFiniteNumber(item.id);
    if (!title && !url && listingId == null) {
      return [];
    }

    return [{
      listing_id: listingId == null ? null : String(listingId),
      title,
      description: optionalString(item.shortDescription),
      price: optionalString(item.price),
      location: optionalString(item.location),
      url,
      image_url: toAbsoluteUrl(item.imageUrl),
      additional_image_urls: additionalImageUrls,
      age: optionalString(item.postedDate),
      posted_timestamp: optionalFiniteNumber(item.date),
      number_of_images: optionalFiniteNumber(item.numberOfImages),
      category_id: optionalFiniteNumber(item.categoryId),
      top_level_category_id: optionalFiniteNumber(item.l1CategoryId),
      subcategory_level_2_id: optionalFiniteNumber(item.l2CategoryId),
      status: optionalString(item.status),
      featured: optionalBoolean(item.featured),
      urgent: optionalBoolean(item.urgent),
      standout: optionalBoolean(item.standout),
      bumpup: optionalBoolean(item.bumpup),
      premium: optionalBoolean(item.premium),
      has_video: optionalBoolean(item.hasVideo),
      seller_id: optionalFiniteNumber(item.sellerId),
      account_id: optionalFiniteNumber(item.accountId),
      seller_is_trade: optionalBoolean(item.proAccount),
      attributes,
    }];
  });

  return JSON.stringify({
    source: "clientData.favouriteAds.adverts",
    meta: {
      page_type: optionalString(page.type),
      page_title: optionalString(page.title),
      current_path: optionalString(request.path),
      current_url: window.location.href,
      user_logged_in: optionalBoolean(userData?.userLoggedIn),
      user_id: optionalFiniteNumber(userData?.id),
      user_name: optionalString([userData?.firstName, userData?.lastName].filter(Boolean).join(" ")),
      total_favourites: optionalFiniteNumber(favouriteAds.totalAdverts),
      show_saved_ads: optionalBoolean(favouriteAds.showSavedAds),
    },
    items,
  });
})()
"""


def run_browser_favourites(
    page: BridgePage,
    limit: int = 10,
) -> dict[str, Any]:
    favourites_url = build_favourites_url()
    page.navigate(favourites_url)
    page.wait_for_load()
    page.wait_dom_stable(timeout=15000)

    raw = page.evaluate(_EXTRACT_FAVOURITES_JS)
    if not raw:
        raise BrowserAutomationError("未能从 Gumtree 收藏页提取结果")

    payload = json.loads(raw)
    if not isinstance(payload, dict):
        raise BrowserAutomationError("收藏页结果格式异常")

    meta = payload.get("meta")
    if not isinstance(meta, dict):
        raise BrowserAutomationError("收藏页元信息格式异常")

    items = payload.get("items")
    if not isinstance(items, list):
        raise BrowserAutomationError("收藏页数据格式异常")

    display_item_fields = (
        "title",
        "description",
        "price",
        "location",
        "url",
        "image_url",
        "additional_image_urls",
        "age",
        "posted_timestamp",
        "number_of_images",
        "status",
        "featured",
        "urgent",
        "standout",
        "bumpup",
        "premium",
        "has_video",
        "seller_is_trade",
        "attributes",
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
        "current_url": meta.get("current_url"),
        "user_logged_in": meta.get("user_logged_in"),
        "user_id": meta.get("user_id"),
        "user_name": meta.get("user_name"),
        "favourites_url": favourites_url,
        "items": limited,
        "total": len(limited),
        "total_favourites": meta.get("total_favourites"),
        "show_saved_ads": meta.get("show_saved_ads"),
    }
