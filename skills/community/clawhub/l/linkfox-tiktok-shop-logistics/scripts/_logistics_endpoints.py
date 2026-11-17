"""Endpoint registry for linkfox-tiktok-shop-logistics (ERP /logistics APIs)."""

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

LOGISTICS_ENDPOINTS: Dict[str, Dict[str, Any]] = {
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
    "get_warehouse_list": {
        "summary": "Get Warehouse List — 获取店铺仓库列表",
        "method": "GET",
        "path": "logistics/202309/warehouses",
        "required": [],
        "query_fields": [],
        "body_fields": [],
        "needs_shop_cipher": True,
        "response_key": "data",
        "doc_url": "https://partner.tiktokshop.com/docv2/page/get-warehouse-list-202309",
    },
}


def list_api_names() -> List[str]:
    return sorted(LOGISTICS_ENDPOINTS.keys())
