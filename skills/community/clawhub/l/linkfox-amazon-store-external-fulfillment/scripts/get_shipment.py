#!/usr/bin/env python3
"""
Amazon Store — getShipment (External Fulfillment Shipping v2024-09-11)
=====================================================================

GET `externalFulfillment/2024-09-11/shipments/{shipmentId}`

官方参考: https://developer-docs.amazon.com/sp-api/reference/getshipment-1
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
        "Usage: get_shipment.py '<JSON>'\nRequired: sellerId, region, shipmentId"
    )
    if not params.get("skipDepCheck"):
        ensure_auth_skill_available("get_shipment.py")
    require_fields(params, ["sellerId", "region", "shipmentId"])

    path = f"{PATH_SHIPMENTS}/{enc_path_seg(params['shipmentId'])}"
    proxy = developer_proxy_call(
        str(params["region"]), path, "GET", str(params["sellerId"])
    )
    out = {"developerProxy": proxy, "resolvedPath": path}
    merge_json_body(out, proxy, "shipment")
    emit_result(out, inline=lf_inline_flag())


if __name__ == "__main__":
    main()
