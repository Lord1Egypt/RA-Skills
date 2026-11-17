"""Endpoint registry for linkfox-tiktok-shop-analytics."""

from __future__ import annotations

from typing import Any, Dict, List

RESERVED_PARAM_KEYS = {
    "api", "openId", "ttsAccessToken", "region", "contentType", "body", "requestBody",
    "queryString", "skipDepCheck", "skipShopCipherResolve", "shop_id", "shopId",
}

ANALYTICS_ENDPOINTS: Dict[str, Dict[str, Any]] = {
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
    "get_video_performances": {
        "summary": "Get Video Performances — 查询店铺视频表现数据",
        "method": "GET",
        "path": "analytics/202403/shop_videos/performance",
        "required": ["start_date", "end_date"],
        "query_fields": [
            "start_date",
            "end_date",
            "page_size",
            "page_token",
            "currency",
            "sort_field",
            "sort_order",
            "granularity",
        ],
        "defaults": {"page_size": 20},
        "body_fields": [],
        "needs_shop_cipher": True,
        "response_key": "data",
        "doc_url": "https://partner.tiktokshop.com/docv2/page/get-video-performances-202403",
    },
}


def list_api_names() -> List[str]:
    return sorted(ANALYTICS_ENDPOINTS.keys())
