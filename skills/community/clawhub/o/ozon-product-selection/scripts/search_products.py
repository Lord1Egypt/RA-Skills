#!/usr/bin/env python3
"""
ozon-product-selection: Search 1688 products for Ozon product selection.
Based on AlphaShop AI Select Provider Search API.
Returns top matching products after filtering.
"""
import sys
import json
import os
import re
import argparse
import requests

import time
import jwt

API_URL = "https://api.alphashop.cn/ai.select.provider.search/1.0"
DETAIL_API_URL = "https://api.alphashop.cn/alphashop.openclaw.offer.detail.query/1.0"


def get_api_key():
    """Generate JWT token using ALPHASHOP_ACCESS_KEY and ALPHASHOP_SECRET_KEY env vars."""
    ak = os.environ.get("ALPHASHOP_ACCESS_KEY", "").strip()
    sk = os.environ.get("ALPHASHOP_SECRET_KEY", "").strip()
    if not ak or not sk:
        print("Error: ALPHASHOP_ACCESS_KEY / ALPHASHOP_SECRET_KEY not set.", file=sys.stderr)
        sys.exit(1)
    current_time = int(time.time())
    token = jwt.encode(
        {"iss": ak, "exp": current_time + 1800, "nbf": current_time - 5},
        sk, algorithm="HS256", headers={"alg": "HS256"}
    )
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token


def call_search_api(api_key, query):
    """Call the AlphaShop search API with SEARCH_OFFER intention."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "intention": "SEARCH_OFFER",
        "query": query
    }
    resp = requests.post(API_URL, json=payload, headers=headers, timeout=30)
    if resp.status_code != 200:
        return {"error": f"HTTP {resp.status_code}", "detail": resp.text[:500]}
    data = resp.json()
    if data.get("resultCode") != "SUCCESS":
        return {"error": "API_ERROR", "detail": json.dumps(data, ensure_ascii=False)[:500]}
    return data


def parse_price(price_str):
    """Extract numeric price from string."""
    if not price_str:
        return None
    match = re.search(r'[\d]+\.?\d*', str(price_str))
    return float(match.group()) if match else None


def parse_moq(infos):
    """Extract MOQ from purchaseInfos."""
    if not infos:
        return None
    for item in infos:
        if str(item.get("label", "")) == "起批量":
            match = re.search(r'(\d+)', str(item.get("value", "")))
            if match:
                return int(match.group(1))
    return None


def parse_ship_rate_48h(infos):
    """Extract 48H shipping rate from shipInfos."""
    if not infos:
        return None
    for item in infos:
        label = str(item.get("label", ""))
        if "48" in label and ("发货" in label or "揽收" in label):
            val = str(item.get("value", ""))
            match = re.search(r'([\d]+\.?\d*)', val)
            if match:
                return float(match.group(1))
    return None


def parse_sales(infos):
    """Extract yearly sales from salesInfos."""
    if not infos:
        return None
    for item in infos:
        label = str(item.get("label", ""))
        if "销量" in label:
            val = str(item.get("value", ""))
            # Handle formats like "1.9万+", "2456", "1608"
            match_wan = re.search(r'([\d]+\.?\d*)\s*万', val)
            if match_wan:
                return int(float(match_wan.group(1)) * 10000)
            match_num = re.search(r'([\d]+)', val.replace(",", ""))
            if match_num:
                return int(match_num.group(1))
    return None


def parse_location(infos):
    """Extract shipping location from shipInfos."""
    if not infos:
        return None
    for item in infos:
        if "发货地" in str(item.get("label", "")):
            return str(item.get("value", ""))
    return None


def filter_offers(offers, max_price=None, max_moq=None, min_ship_rate_48h=None, min_sales=None):
    """Filter offer list based on criteria."""
    filtered = []
    for offer in offers:
        if max_price is not None:
            price = parse_price(offer.get("itemPrice"))
            if price is not None and price > max_price:
                continue

        if max_moq is not None:
            moq = parse_moq(offer.get("purchaseInfos", []))
            if moq is not None and moq > max_moq:
                continue

        if min_ship_rate_48h is not None:
            rate = parse_ship_rate_48h(offer.get("shipInfos", []))
            if rate is None or rate < min_ship_rate_48h:
                continue

        if min_sales is not None:
            sales = parse_sales(offer.get("salesInfos", []))
            if sales is None or sales < min_sales:
                continue

        filtered.append(offer)
    return filtered


def fetch_sku_list(api_key, product_id):
    """Fetch SKU list from product detail API."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    try:
        resp = requests.post(DETAIL_API_URL, json={"productId": str(product_id)},
                             headers=headers, timeout=15)
        if resp.status_code != 200:
            return []
        data = resp.json()
        r = data.get("result", {}).get("result", {})
        sku_infos = r.get("productSkuInfos", [])
        skus = []
        for sku in sku_infos:
            # Build SKU name from attributes
            attrs = sku.get("skuAttributes", [])
            name_parts = [a.get("value", "") for a in attrs if a.get("value")]
            sku_name = " / ".join(name_parts) if name_parts else str(sku.get("skuId", ""))
            price = sku.get("price") or sku.get("consignPrice")
            price_float = float(price) if price else None
            skus.append({
                "skuId": sku.get("skuId"),
                "name": sku_name,
                "price": price_float,
                "suggestedPrice": round(price_float * 3, 2) if price_float else None,
                "stock": sku.get("amountOnSale"),
            })
        return skus
    except Exception:
        return []


def format_offer(offer, api_key=None):
    """Format a single offer into a clean structure."""
    pi = offer.get("providerInfo", {})
    tags = [t.get("tagName") for t in pi.get("providerTags", []) if t.get("tagName")] if pi else []

    detail_url = offer.get("offerDetailUrl")
    item_id = offer.get("itemId")
    if not detail_url and item_id:
        detail_url = f"https://detail.1688.com/offer/{item_id}.html"

    result = {
        "itemId": item_id,
        "title": offer.get("title"),
        "price": offer.get("itemPrice"),
        "imageUrl": offer.get("imageUrl"),
        "detailUrl": detail_url,
        "moq": parse_moq(offer.get("purchaseInfos", [])),
        "shipRate48h": parse_ship_rate_48h(offer.get("shipInfos", [])),
        "sales": parse_sales(offer.get("salesInfos", [])),
        "location": parse_location(offer.get("shipInfos", [])),
        "supplier": {
            "companyName": pi.get("companyName") if pi else None,
            "tags": tags,
        },
    }

    # Fetch SKU details if api_key provided
    if api_key and item_id:
        result["skus"] = fetch_sku_list(api_key, item_id)

    return result


def main():
    parser = argparse.ArgumentParser(description="Search 1688 products for Ozon selection")
    parser.add_argument("query", help="Search keyword (Chinese)")
    parser.add_argument("--max-price", type=float, default=None, help="Max unit price (CNY)")
    parser.add_argument("--max-moq", type=int, default=None, help="Max minimum order quantity")
    parser.add_argument("--min-ship-rate-48h", type=float, default=None, help="Min 48H ship rate (%%)")
    parser.add_argument("--min-sales", type=int, default=None, help="Min yearly sales count")
    parser.add_argument("--top", type=int, default=3, help="Number of top results to return (default: 3)")

    args = parser.parse_args()
    api_key = get_api_key()

    data = call_search_api(api_key, args.query)
    if "error" in data:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        sys.exit(1)

    result = data.get("result", {}).get("result", {})
    offers = result.get("offerInfo", {}).get("offerList", [])
    total_raw = len(offers)

    # Apply filters
    has_filters = any(v is not None for v in [args.max_price, args.max_moq, args.min_ship_rate_48h, args.min_sales])
    if has_filters:
        offers = filter_offers(offers, args.max_price, args.max_moq, args.min_ship_rate_48h, args.min_sales)

    output = {
        "query": args.query,
        "filters": {
            "max_price": args.max_price,
            "max_moq": args.max_moq,
            "min_ship_rate_48h": args.min_ship_rate_48h,
            "min_sales": args.min_sales,
        },
        "total_raw": total_raw,
        "total_filtered": len(offers),
        "products": [format_offer(o, api_key=api_key) for o in offers[:args.top]],
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
