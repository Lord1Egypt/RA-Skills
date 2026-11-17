#!/usr/bin/env python3
"""
Amazon Store — generateShipLabels (External Fulfillment Shipping v2024-09-11)
============================================================================

PUT `externalFulfillment/2024-09-11/shipments/{shipmentId}/shipLabels?operation=...`
可选 shippingOptionId；body 可用 requestBody 或 packageIds / courierSupportedAttributes。

官方参考: https://developer-docs.amazon.com/sp-api/reference/generateshiplabels
"""

from __future__ import annotations

import json
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
        "Usage: generate_ship_labels.py '<JSON>'\n"
        "Required: sellerId, region, shipmentId, operation (GENERATE|REGENERATE)\n"
        "Optional: shippingOptionId, requestBody | packageIds, courierSupportedAttributes"
    )
    if not params.get("skipDepCheck"):
        ensure_auth_skill_available("generate_ship_labels.py")
    require_fields(params, ["sellerId", "region", "shipmentId", "operation"])

    op = str(params["operation"]).strip().upper()
    if op not in ("GENERATE", "REGENERATE"):
        print("operation must be GENERATE or REGENERATE", file=sys.stderr)
        sys.exit(1)

    path = f"{PATH_SHIPMENTS}/{enc_path_seg(params['shipmentId'])}/shipLabels"
    qs = build_query(
        [
            ("operation", op),
            ("shippingOptionId", params.get("shippingOptionId")),
        ]
    )

    if params.get("requestBody") is not None:
        rb = params["requestBody"]
        if rb is not None and not isinstance(rb, dict):
            print("requestBody must be a JSON object or omitted", file=sys.stderr)
            sys.exit(1)
    else:
        rb = {}
        if params.get("packageIds") is not None:
            rb["packageIds"] = params["packageIds"]
        if params.get("courierSupportedAttributes") is not None:
            rb["courierSupportedAttributes"] = params["courierSupportedAttributes"]
        if not rb:
            rb = None

    body_str = json.dumps(rb, ensure_ascii=False) if rb is not None else None
    proxy = developer_proxy_call(
        str(params["region"]),
        path,
        "PUT",
        str(params["sellerId"]),
        query_string=qs,
        body=body_str,
    )
    out = {
        "developerProxy": proxy,
        "resolvedPath": path,
        "queryString": qs,
        "requestBody": rb,
    }
    merge_json_body(out, proxy, "shipLabels")
    emit_result(out, inline=lf_inline_flag())


if __name__ == "__main__":
    main()
