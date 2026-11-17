"""Endpoint registry for linkfox-tiktok-shop-order (ERP /order APIs)."""

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

ORDER_ENDPOINTS: Dict[str, Dict[str, Any]] = {
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
    "get_order_list": {
        "summary": "Get Order List — 搜索/列出订单",
        "method": "POST",
        "path": "order/202309/orders/search",
        "required": ["page_size"],
        "defaults": {"page_size": 20},
        "query_fields": ["page_size", "sort_order", "page_token", "sort_field"],
        "body_fields": [
            "order_status",
            "create_time_ge",
            "create_time_lt",
            "update_time_ge",
            "update_time_lt",
            "shipping_type",
            "buyer_user_id",
            "is_buyer_request_cancel",
            "warehouse_ids",
        ],
        "needs_shop_cipher": True,
        "response_key": "data",
        "doc_url": "https://partner.tiktokshop.com/docv2/page/get-order-list-202309",
        "allow_empty_body": True,
    },
    "get_order_detail": {
        "summary": "Get Order Detail — 获取订单详情（202507）",
        "method": "GET",
        "path": "order/202507/orders",
        "required": ["ids"],
        "query_fields": ["ids"],
        "body_fields": [],
        "needs_shop_cipher": True,
        "response_key": "data",
        "doc_url": "https://partner.tiktokshop.com/docv2/page/get-order-detail-202507",
    },
    "get_order_detail_202309": {
        "summary": "Get Order Detail — 获取订单详情（202309）",
        "method": "GET",
        "path": "order/202309/orders",
        "required": ["ids"],
        "query_fields": ["ids"],
        "body_fields": [],
        "needs_shop_cipher": True,
        "response_key": "data",
        "doc_url": "https://partner.tiktokshop.com/docv2/page/get-order-detail-202309",
    },
}


def list_api_names() -> List[str]:
    return sorted(ORDER_ENDPOINTS.keys())
