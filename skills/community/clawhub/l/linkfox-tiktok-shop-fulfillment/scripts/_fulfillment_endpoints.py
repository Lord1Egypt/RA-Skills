"""Endpoint registry for linkfox-tiktok-shop-fulfillment (ERP /fulfillment APIs)."""

from __future__ import annotations

from typing import Any, Dict, List

RESERVED_PARAM_KEYS = {
    "api",
    "openId",
    "ttsAccessToken",
    "region",
    "contentType",
    "body",
    "requestBody",
    "queryString",
    "skipDepCheck",
    "skipShopCipherResolve",
    "shop_id",
    "shopId",
}

FULFILLMENT_ENDPOINTS: Dict[str, Dict[str, Any]] = {
    "get_authorized_shops": {
        "summary": "Get Authorized Shops — 获取已授权店铺与 shop_cipher",
        "method": "GET",
        "path": "authorization/202309/shops",
        "required": [],
        "query_fields": [],
        "body_fields": [],
        "needs_shop_cipher": False,
        "response_key": "data",
        "doc_url": "https://partner.tiktokshop.com/docv2/page/get-authorized-shops-202309",
    },
    "get_order_split_attributes": {
        "summary": "Get Order Split Attributes — 查询订单是否可拆单及拆单属性",
        "method": "GET",
        "path": "fulfillment/202309/orders/split_attributes",
        "required": ["order_ids"],
        "query_fields": ["order_ids"],
        "body_fields": [],
        "needs_shop_cipher": True,
        "response_key": "data",
        "doc_url": "https://partner.tiktokshop.com/docv2/page/get-order-split-attributes-202309",
    },
}


def list_api_names() -> List[str]:
    return sorted(FULFILLMENT_ENDPOINTS.keys())
