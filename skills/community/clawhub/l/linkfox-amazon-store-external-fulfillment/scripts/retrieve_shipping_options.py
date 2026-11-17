#!/usr/bin/env python3
"""
Amazon Store — retrieveShippingOptions (External Fulfillment Shipping v2024-09-11)
==================================================================================

GET `externalFulfillment/2024-09-11/shipments/{shipmentId}/shippingOptions?packageId=...`

官方参考: https://developer-docs.amazon.com/sp-api/reference/retrieveshippingoptions
"""

from __future__ import annotations

import sys

from _spapi_ef_common import (
    PATH_SHIPMENTS,
    build_query,
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
        "Usage: retrieve_shipping_options.py '<JSON>'\n"
        "Required: sellerId, region, shipmentId, packageId"
    )
    if not params.get("skipDepCheck"):
        ensure_auth_skill_available("retrieve_shipping_options.py")
    require_fields(params, ["sellerId", "region", "shipmentId", "packageId"])

    path = f"{PATH_SHIPMENTS}/{enc_path_seg(params['shipmentId'])}/shippingOptions"
    qs = build_query([("packageId", params.get("packageId"))])
    proxy = developer_proxy_call(
        str(params["region"]),
        path,
        "GET",
        str(params["sellerId"]),
        query_string=qs,
    )
    out = {"developerProxy": proxy, "resolvedPath": path, "queryString": qs}
    merge_json_body(out, proxy, "shippingOptions")
    emit_result(out, inline=lf_inline_flag())


if __name__ == "__main__":
    main()
