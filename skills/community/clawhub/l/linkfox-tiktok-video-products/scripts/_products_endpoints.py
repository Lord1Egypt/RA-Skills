"""Endpoint registry for linkfox-tiktok-video-products."""

from __future__ import annotations

from typing import Any, Dict, List

PRODUCTS_ENDPOINTS: Dict[str, Dict[str, Any]] = {
    "get_shop_products": {
        "summary": "Get Shop Products — 搜索达人绑定店铺的商品",
        "method": "GET",
        "path": "affiliate_creator/202509/shop_products",
        "required": ["page_size"],
        "defaults": {"page_size": 20},
        "query_fields": [
            "title_keyword",
            "sort_field",
            "sort_order",
            "page_size",
            "page_token",
        ],
        "body_fields": [],
        "response_key": "data",
        "doc_url": "https://partner.tiktokshop.com/docv2/page/get-shop-products-202509",
        "mrd_url": "https://bytedance.sg.larkoffice.com/docx/Os8tdPkaVo2QFBxhSRIlQwBAg9f",
    },
    "get_showcase_products": {
        "summary": "Get Showcase Products — 达人橱窗/直播袋商品列表",
        "method": "GET",
        "path": "affiliate_creator/202405/showcases/products",
        "required": ["page_size", "origin"],
        "defaults": {"page_size": 20, "origin": "SHOWCASE"},
        "query_fields": ["page_size", "page_token", "origin"],
        "body_fields": [],
        "response_key": "data",
        "doc_url": "https://partner.tiktokshop.com/docv2/page/get-showcase-products-202405",
        "mrd_url": "https://bytedance.sg.larkoffice.com/docx/Os8tdPkaVo2QFBxhSRIlQwBAg9f",
    },
}

LIST_QUERY_FIELDS: List[str] = []

RESERVED_PARAM_KEYS = frozenset({
    "api",
    "openId",
    "region",
    "contentType",
    "body",
    "requestBody",
    "skipDepCheck",
})


def list_api_names() -> List[str]:
    return sorted(PRODUCTS_ENDPOINTS.keys())
