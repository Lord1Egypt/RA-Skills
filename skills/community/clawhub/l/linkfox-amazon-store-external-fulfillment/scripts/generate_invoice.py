#!/usr/bin/env python3
"""
Amazon Store — generateInvoice (External Fulfillment Shipping v2024-09-11)
=========================================================================

POST `externalFulfillment/2024-09-11/shipments/{shipmentId}/invoice`

官方参考: https://developer-docs.amazon.com/sp-api/reference/generateinvoice
"""

from __future__ import annotations

import sys

from _spapi_ef_common import (
    PATH_SHIPMENTS,
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
        "Usage: generate_invoice.py '<JSON>'\nRequired: sellerId, region, shipmentId"
    )
    if not params.get("skipDepCheck"):
        ensure_auth_skill_available("generate_invoice.py")
    require_fields(params, ["sellerId", "region", "shipmentId"])

    path = f"{PATH_SHIPMENTS}/{enc_path_seg(params['shipmentId'])}/invoice"
    proxy = developer_proxy_call(
        str(params["region"]), path, "POST", str(params["sellerId"])
    )
    out = {"developerProxy": proxy, "resolvedPath": path}
    merge_json_body(out, proxy, "invoice")
    emit_result(out, inline=lf_inline_flag())


if __name__ == "__main__":
    main()
