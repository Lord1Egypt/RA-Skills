#!/usr/bin/env python3
"""
Amazon Store — getReturn (External Fulfillment Returns v2024-09-11)
==================================================================

GET `externalFulfillment/2024-09-11/returns/{returnId}`

官方参考: https://developer-docs.amazon.com/sp-api/reference/getreturn
"""

from __future__ import annotations

import sys

from _spapi_ef_common import (
    PATH_RETURNS,
    developer_proxy_call,
    emit_result,
    enc_path_seg,
    ensure_auth_skill_available,
    lf_inline_flag,
    load_params_or_exit,
    merge_json_body,
    require_fields,
)


def main() -> None:
    params = load_params_or_exit(
        "Usage: get_return.py '<JSON>'\nRequired: sellerId, region, returnId"
    )
    if not params.get("skipDepCheck"):
        ensure_auth_skill_available("get_return.py")
    require_fields(params, ["sellerId", "region", "returnId"])

    path = f"{PATH_RETURNS}/{enc_path_seg(params['returnId'])}"
    proxy = developer_proxy_call(
        str(params["region"]), path, "GET", str(params["sellerId"])
    )
    out = {"developerProxy": proxy, "resolvedPath": path}
    merge_json_body(out, proxy, "returnItem")
    emit_result(out, inline=lf_inline_flag())


if __name__ == "__main__":
    main()
