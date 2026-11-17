#!/usr/bin/env python3
"""
Amazon Store — listReturns (External Fulfillment Returns v2024-09-11)
====================================================================

GET `externalFulfillment/2024-09-11/returns`

官方参考: https://developer-docs.amazon.com/sp-api/reference/listreturns
"""

from __future__ import annotations

import sys

from _spapi_ef_common import (
    PATH_RETURNS,
    build_query,
    developer_proxy_call,
    emit_result,
    ensure_auth_skill_available,
    lf_inline_flag,
    load_params_or_exit,
    merge_json_body,
    require_fields,
)


def main() -> None:
    params = load_params_or_exit(
        "Usage: list_returns.py '<JSON>'\n"
        "Required: sellerId, region\n"
        "Optional: returnLocationId, rmaId, status, reverseTrackingId, "
        "createdSince, createdUntil, lastUpdatedSince, lastUpdatedUntil, "
        "maxResults, nextToken"
    )
    if not params.get("skipDepCheck"):
        ensure_auth_skill_available("list_returns.py")
    require_fields(params, ["sellerId", "region"])

    qs = build_query(
        [
            ("returnLocationId", params.get("returnLocationId")),
            ("rmaId", params.get("rmaId")),
            ("status", params.get("status")),
            ("reverseTrackingId", params.get("reverseTrackingId")),
            ("createdSince", params.get("createdSince")),
            ("createdUntil", params.get("createdUntil")),
            ("lastUpdatedSince", params.get("lastUpdatedSince")),
            ("lastUpdatedUntil", params.get("lastUpdatedUntil")),
            ("maxResults", params.get("maxResults")),
            ("nextToken", params.get("nextToken")),
        ]
    )
    proxy = developer_proxy_call(
        str(params["region"]),
        PATH_RETURNS,
        "GET",
        str(params["sellerId"]),
        query_string=qs,
    )
    out = {"developerProxy": proxy, "resolvedPath": PATH_RETURNS, "queryString": qs}
    merge_json_body(out, proxy, "returns")
    emit_result(out, inline=lf_inline_flag())


if __name__ == "__main__":
    main()
