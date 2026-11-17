#!/usr/bin/env python3
"""
TikTok Shop ERP helpers — force appType=erp for linkfox-tiktok-shop-auth.
"""

from __future__ import annotations

import sys
from typing import Any


ERP_APP_TYPE = "erp"


def enforce_erp_app_type(params: dict[str, Any] | None = None) -> dict[str, Any]:
    """
    Return a copy of params with appType fixed to erp.
    Reject explicit non-erp appType values.
    """
    out: dict[str, Any] = dict(params or {})
    raw = out.get("appType")
    if raw is not None and str(raw).strip() and str(raw).strip().lower() != ERP_APP_TYPE:
        print(
            f"Error: linkfox-tiktok-shop-auth is ERP-only; appType must be '{ERP_APP_TYPE}' "
            f"(got {raw!r}). Use linkfox-tiktok-video-auth for creator.",
            file=sys.stderr,
        )
        sys.exit(1)
    out["appType"] = ERP_APP_TYPE
    return out


def filter_erp_stores(result: dict[str, Any]) -> dict[str, Any]:
    """Keep only appType=erp stores; recompute total."""
    if "stores" not in result or not isinstance(result.get("stores"), list):
        return result
    out = dict(result)
    erp_stores = [
        s
        for s in out["stores"]
        if isinstance(s, dict) and str(s.get("appType", "")).lower() == ERP_APP_TYPE
    ]
    out["stores"] = erp_stores
    out["total"] = len(erp_stores)
    if "filteredOutNonErp" not in out:
        original = result.get("stores") or []
        dropped = len(original) - len(erp_stores)
        if dropped > 0:
            out["filteredOutNonErp"] = dropped
    return out
