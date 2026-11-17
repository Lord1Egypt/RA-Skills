"""Endpoint registry for linkfox-tiktok-shop-return-refund."""

from __future__ import annotations

from typing import Any, Dict, List

RESERVED_PARAM_KEYS = {
    "api", "openId", "ttsAccessToken", "region", "contentType", "body", "requestBody",
    "queryString", "skipDepCheck", "skipShopCipherResolve", "shop_id", "shopId",
}

RETURN_REFUND_ENDPOINTS: Dict[str, Dict[str, Any]] = {
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
    "get_reject_reasons": {
        "summary": "Get Reject Reasons — 获取拒单/拒退原因列表",
        "method": "GET",
        "path": "return_refund/202309/reject_reasons",
        "required": ["return_or_cancel_id"],
        "query_fields": ["return_or_cancel_id", "locale"],
        "body_fields": [],
        "needs_shop_cipher": True,
        "response_key": "data",
        "doc_url": "https://partner.tiktokshop.com/docv2/page/get-reject-reasons-202309",
    },
}


def list_api_names() -> List[str]:
    return sorted(RETURN_REFUND_ENDPOINTS.keys())
