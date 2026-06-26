from __future__ import annotations

import json
from typing import Any

from .bridge import BridgePage
from .browser_urls import build_search_url
from .errors import BrowserAutomationError

_EXTRACT_SEARCH_RESULTS_JS = """
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
    if (typeof value !== "string" || !normalizeText(value)) {
      fail(message);
    }
    return normalizeText(value);
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
  const toAbsoluteUrl = (value) => {
    const text = normalizeText(value);
    if (!text) {
      return "";
    }
    try {
      return new URL(text, window.location.origin).toString();
    } catch {
      return "";
    }
  };
  const extractListingIdFromUrl = (url) => {
    const match = url.match(/\\/(\\d+)(?:[/?#]|$)/);
    if (!match) {
      return null;
    }
    return match[1];
  };
  const parseLdJsonListings = () => {
    const nodes = Array.from(document.querySelectorAll('script[type="application/ld+json"]'));
    for (const node of nodes) {
      let parsed;
      try {
        parsed = JSON.parse(node.textContent || "");
      } catch {
        continue;
      }
      const entry = Array.isArray(parsed)
        ? parsed.find((item) => item?.["@type"] === "SearchResultsPage")
        : parsed;
      if (!entry || entry["@type"] !== "SearchResultsPage") {
        continue;
      }
      const mainEntity = expectObject(entry.mainEntity, "SearchResultsPage.mainEntity 缺失");
      const itemList = expectArray(mainEntity.itemListElement, "SearchResultsPage.itemListElement 缺失");
      const urlById = new Map();
      for (const item of itemList) {
        if (!item || typeof item !== "object" || Array.isArray(item)) {
          continue;
        }
        const url = toAbsoluteUrl(item.url);
        if (!url) {
          continue;
        }
        const listingId = extractListingIdFromUrl(url);
        if (!listingId) {
          continue;
        }
        urlById.set(listingId, url);
      }
      return urlById;
    }
    return new Map();
  };
  const parseDomDescriptions = () => {
    const descriptionById = new Map();
    const cards = Array.from(document.querySelectorAll('article[data-q="search-result"]'));
    for (const card of cards) {
      const anchor = card.querySelector('a[data-q="search-result-anchor"][href*="/p/"]');
      if (!anchor) {
        continue;
      }
      const href = toAbsoluteUrl(anchor.getAttribute("href"));
      if (!href) {
        continue;
      }
      const listingId = extractListingIdFromUrl(href);
      const descriptionNode = card.querySelector('[data-q="tile-description"] p');
      if (!descriptionNode) {
        continue;
      }
      const description = normalizeText(descriptionNode.textContent);
      if (!description) {
        continue;
      }
      descriptionById.set(listingId, description);
    }
    return descriptionById;
  };

  const dataLayerEntries = expectArray(window.dataLayer, "window.dataLayer 缺失");
  const initialDataLayer = dataLayerEntries.find(
    (entry) => entry && typeof entry === "object" && entry.name === "SrpViewEvent"
  );
  const srpViewEvent = expectObject(initialDataLayer, "未找到 SrpViewEvent 数据");
  const searchMeta = expectObject(srpViewEvent.s, "SrpViewEvent.s 缺失");
  const pageMeta = expectObject(srpViewEvent.p, "SrpViewEvent.p 缺失");

  const gumtreeDataLayer = expectArray(window.gumtreeDataLayer, "window.gumtreeDataLayer 缺失");
  const pageDeclaration = gumtreeDataLayer.find(
    (entry) => entry && typeof entry === "object" && entry.event === "pageDeclaration"
  );
  const pageDeclarationEvent = expectObject(pageDeclaration, "未找到 gumtreeDataLayer pageDeclaration 事件");
  const searchBar = expectObject(pageDeclarationEvent.searchBar, "pageDeclaration.searchBar 缺失");
  const rawListings = expectArray(pageDeclarationEvent.listListingDetails, "pageDeclaration.listListingDetails 缺失");
  const urlById = parseLdJsonListings();
  const descriptionById = parseDomDescriptions();

  const meta = {
    keyword: optionalString(searchMeta.kw),
    page_number: optionalFiniteNumber(searchMeta.pn),
    total_results: optionalFiniteNumber(searchMeta.tr),
    search_category_id: optionalFiniteNumber(searchMeta.dc),
    page_type: optionalString(pageMeta.t),
    platform: optionalString(pageMeta.pl),
    request_id: optionalString(pageDeclarationEvent.requestId),
    search_category_name: optionalString(searchBar.categoryName),
    search_bar_category_id: optionalFiniteNumber(searchBar.categoryId),
    search_location_name: optionalString(searchBar.locationName),
    page_size: optionalFiniteNumber(searchMeta.tp),
  };

  const items = rawListings.flatMap((listing, index) => {
    if (!listing || typeof listing !== "object" || Array.isArray(listing)) {
      return [];
    }
    const row = listing;
    const rawListingId = optionalFiniteNumber(row.id);
    const listingId = rawListingId == null ? extractListingIdFromUrl(toAbsoluteUrl(row.url || row.path)) : String(rawListingId);
    const url = urlById.get(listingId) || null;
    const description = descriptionById.get(listingId) || null;
    const title = optionalString(row.name);
    if (!title && !url && !listingId) {
      return [];
    }

    return [{
      listing_id: listingId,
      position: optionalFiniteNumber(row.position),
      title,
      description,
      price: optionalFiniteNumber(row.price),
      price_pennies: optionalFiniteNumber(row.pricePennies),
      location: optionalString(row.location),
      url,
      age: optionalString(row.age),
      number_of_images: optionalFiniteNumber(row.numberOfImages),
      number_words_description: optionalFiniteNumber(row.numberWordsDescription),
      category: optionalString(row.category),
      category_id: optionalFiniteNumber(row.categoryId),
      subcategory1: optionalFiniteNumber(row.subcategory1),
      subcategory2: optionalFiniteNumber(row.subcategory2),
      subcategory3: optionalFiniteNumber(row.subcategory3),
      subcategory4: optionalFiniteNumber(row.subcategory4),
      promotions: Array.isArray(row.promotions) ? row.promotions : [],
      is_trade: optionalBoolean(row.isTrade),
      video_link: optionalBoolean(row.videoLink),
      is_gbg_verified: optionalBoolean(row.isGBGVerified),
      is_delivery: optionalBoolean(row.isDelivery),
      source: optionalString(row.source),
      recall_source: optionalString(row.recallSource),
    }];
  });

  return JSON.stringify({
    source: "strict-structured-data",
    meta,
    items,
  });
})()
"""


def run_browser_search(
    page: BridgePage,
    keyword: str,
    limit: int = 10,
    search_location: str = "uk",
    search_category: str = "all",
    sort: str | None = None,
    distance: int | None = None,
    min_price: int | None = None,
    max_price: int | None = None,
    conditions: list[str] | None = None,
    seller_types: list[str] | None = None,
    mobile_storage_capacity: str | None = None,
    common_for_sale_colour: str | None = None,
    mobile_model_apple: str | None = None,
) -> dict[str, Any]:
    display_item_fields = (
        "title",
        "description",
        "price",
        "location",
        "url",
        "age",
        "number_of_images",
        "promotions",
    )
    search_url = build_search_url(
        keyword,
        search_location=search_location,
        search_category=search_category,
        sort=sort,
        distance=distance,
        min_price=min_price,
        max_price=max_price,
        conditions=conditions,
        seller_types=seller_types,
        mobile_storage_capacity=mobile_storage_capacity,
        common_for_sale_colour=common_for_sale_colour,
        mobile_model_apple=mobile_model_apple,
    )
    page.navigate(search_url)
    page.wait_for_load()
    page.wait_dom_stable(timeout=15000)

    raw = page.evaluate(_EXTRACT_SEARCH_RESULTS_JS)
    if not raw:
        raise BrowserAutomationError("未能从 Gumtree 搜索页提取结果")

    payload = json.loads(raw)
    if not isinstance(payload, dict):
        raise BrowserAutomationError("搜索结果格式异常")

    items = payload.get("items")
    if not isinstance(items, list):
        raise BrowserAutomationError("搜索结果格式异常")

    meta = payload.get("meta")
    if not isinstance(meta, dict):
        meta = {}

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
        "keyword": meta.get("keyword"),
        "page_number": meta.get("page_number"),
        "total_results": meta.get("total_results"),
        "request_id": meta.get("request_id"),
        "page_type": meta.get("page_type"),
        "platform": meta.get("platform"),
        "search_category_id": meta.get("search_category_id"),
        "search_category_name": meta.get("search_category_name"),
        "search_bar_category_id": meta.get("search_bar_category_id"),
        "search_location_name": meta.get("search_location_name"),
        "page_size": meta.get("page_size"),
        "search_url": search_url,
        "items": limited,
        "total": len(limited),
    }
