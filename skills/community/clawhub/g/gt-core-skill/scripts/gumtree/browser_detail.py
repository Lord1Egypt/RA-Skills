from __future__ import annotations

import json
from typing import Any

from .bridge import BridgePage
from .errors import BrowserAutomationError

_EXTRACT_DETAIL_PAGE_JS = """
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
  const optionalFiniteNumber = (value) => {
    if (typeof value !== "number" || !Number.isFinite(value)) {
      return null;
    }
    return value;
  };
  const optionalBoolean = (value) => {
    if (typeof value !== "boolean") {
      return null;
    }
    return value;
  };
  const expectBoolean = (value, message) => {
    if (typeof value !== "boolean") {
      fail(message);
    }
    return value;
  };
  const toAbsoluteUrl = (value, message) => {
    const text = expectString(value, message);
    try {
      return new URL(text, window.location.origin).toString();
    } catch {
      fail(`URL 格式异常: ${text}`);
    }
  };
  const queryText = (selector, message) => {
    const node = document.querySelector(selector);
    if (!node) {
      fail(message);
    }
    return expectString(node.textContent, message);
  };
  const queryOptionalText = (selector) => {
    const node = document.querySelector(selector);
    if (!node) {
      return null;
    }
    return optionalString(node.textContent);
  };

  const dataLayerEntries = expectArray(window.dataLayer, "window.dataLayer 缺失");
  const vipViewEvent = dataLayerEntries.find(
    (entry) => entry && typeof entry === "object" && entry.name === "VipViewEvent"
  );
  const vipEvent = expectObject(vipViewEvent, "未找到 VipViewEvent 数据");
  const pageMeta = expectObject(vipEvent.p, "VipViewEvent.p 缺失");

  const gumtreeDataLayer = expectArray(window.gumtreeDataLayer, "window.gumtreeDataLayer 缺失");
  const pageDeclaration = gumtreeDataLayer.find(
    (entry) => entry && typeof entry === "object" && entry.event === "pageDeclaration"
  );
  const detailEvent = expectObject(pageDeclaration, "未找到 gumtreeDataLayer pageDeclaration 事件");
  const listingDetails = expectObject(detailEvent.listingDetails, "pageDeclaration.listingDetails 缺失");
  const sellerProfile = expectObject(detailEvent.sellerProfile, "pageDeclaration.sellerProfile 缺失");

  const attributes = {};
  const attributesContainer = document.querySelector('[data-q="attribute-container"]');
  if (attributesContainer) {
    const attributeRows = Array.from(attributesContainer.querySelectorAll('[data-q="attribute-row"]'));
    for (const row of attributeRows) {
      const keyNode = row.querySelector("dt");
      const valueNode = row.querySelector('[data-testid="attribute-value"]');
      const key = optionalString(keyNode?.textContent);
      const value = optionalString(valueNode?.textContent);
      if (key && value) {
        attributes[key] = value;
      }
    }
  }

  const imageUrls = Array.from(document.querySelectorAll('[data-q="image-carousel"] img'))
    .map((node) => {
      const src = optionalString(node.getAttribute("src"));
      if (!src) {
        return null;
      }
      try {
        return new URL(src, window.location.origin).toString();
      } catch {
        return null;
      }
    })
    .filter(Boolean);
  const uniqueImageUrls = Array.from(new Set(imageUrls));

  const item = {
    title: queryText('[data-q="vip-title"]', "详情页标题缺失"),
    description: queryOptionalText('p[itemProp="description"]'),
    price: queryOptionalText('[data-q="ad-price"]'),
    location: queryOptionalText('[data-q="ad-location"]') || optionalString(listingDetails.location),
    url: window.location.href,
    age: optionalString(listingDetails.age),
    number_of_images: optionalFiniteNumber(listingDetails.numberOfImages),
    category: optionalString(listingDetails.category),
    promotions: Array.isArray(listingDetails.promotions) ? listingDetails.promotions : [],
    seller_name:
      queryOptionalText('[data-q="seller-name"][data-testid="seller-name"], [data-q="seller-name-large-screen"]'),
    seller_last_active: optionalString(sellerProfile.lastActive),
    seller_posting_for: optionalString(sellerProfile.postingFor),
    seller_rating_count: optionalFiniteNumber(sellerProfile.ratingCount),
    seller_rating_source: optionalString(sellerProfile.ratingSource),
    contact_by_email: optionalBoolean(listingDetails.contactEmail),
    contact_by_phone: optionalBoolean(listingDetails.contactNumber),
    is_trade: optionalBoolean(listingDetails.isTrade),
    gbg_verified: optionalBoolean(listingDetails.isGBGVerified),
    delivery_available: optionalBoolean(listingDetails.isDelivery),
    video_link: optionalBoolean(listingDetails.videoLink),
    website_link: optionalBoolean(listingDetails.websiteLink),
    location_show_on_map: optionalBoolean(listingDetails.locationShowOnMap),
    number_words_description: optionalFiniteNumber(listingDetails.numberWordsDescription),
    image_urls: uniqueImageUrls,
    attributes,
  };

  return JSON.stringify({
    source: "strict-detail-page",
    meta: {
      page_type: optionalString(pageMeta.t),
      platform: optionalString(pageMeta.pl),
      request_id: optionalString(detailEvent.requestId),
    },
    item,
  });
})()
"""


def run_browser_detail(
    page: BridgePage,
    detail_url: str,
) -> dict[str, Any]:
    page.navigate(detail_url)
    page.wait_for_load()
    page.wait_dom_stable(timeout=15000)

    raw = page.evaluate(_EXTRACT_DETAIL_PAGE_JS)
    if not raw:
        raise BrowserAutomationError("未能从 Gumtree 详情页提取结果")

    payload = json.loads(raw)
    if not isinstance(payload, dict):
        raise BrowserAutomationError("详情页结果格式异常")

    meta = payload.get("meta")
    if not isinstance(meta, dict):
        raise BrowserAutomationError("详情页元信息格式异常")

    item = payload.get("item")
    if not isinstance(item, dict):
        raise BrowserAutomationError("详情页数据格式异常")

    display_item_fields = (
        "title",
        "description",
        "price",
        "location",
        "url",
        "age",
        "number_of_images",
        "category",
        "promotions",
        "seller_name",
        "seller_last_active",
        "seller_posting_for",
        "seller_rating_count",
        "seller_rating_source",
        "contact_by_email",
        "contact_by_phone",
        "is_trade",
        "gbg_verified",
        "delivery_available",
        "video_link",
        "website_link",
        "location_show_on_map",
        "image_urls",
        "attributes",
    )

    cleaned = {field: item.get(field) for field in display_item_fields}
    return {
        "ok": True,
        "mode": "browser",
        "source": payload.get("source"),
        "detail_url": detail_url,
        "page_type": meta.get("page_type"),
        "platform": meta.get("platform"),
        "request_id": meta.get("request_id"),
        "item": cleaned,
    }
