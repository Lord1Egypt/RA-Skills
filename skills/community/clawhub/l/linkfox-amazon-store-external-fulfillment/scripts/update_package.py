#!/usr/bin/env python3
"""
Amazon Store — updatePackage (External Fulfillment Shipping v2024-09-11)
=======================================================================

PUT `externalFulfillment/2024-09-11/shipments/{shipmentId}/packages/{packageId}`

官方参考: https://developer-docs.amazon.com/sp-api/reference/updatepackage
"""

from __future__ import annotations

import json
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
        "Usage: update_package.py '<JSON>'\n"
        "Required: sellerId, region, shipmentId, packageId, requestBody"
    )
    if not params.get("skipDepCheck"):
        ensure_auth_skill_available("update_package.py")
    require_fields(params, ["sellerId", "region", "shipmentId", "packageId", "requestBody"])

    rb = params["requestBody"]
    if not isinstance(rb, dict):
        print("requestBody must be a JSON object", file=sys.stderr)
        sys.exit(1)

    path = (
        f"{PATH_SHIPMENTS}/{enc_path_seg(params['shipmentId'])}"
        f"/packages/{enc_path_seg(params['packageId'])}"
    )
    body_str = json.dumps(rb, ensure_ascii=False)
    proxy = developer_proxy_call(
        str(params["region"]),
        path,
        "PUT",
        str(params["sellerId"]),
        body=body_str,
    )
    out = {"developerProxy": proxy, "resolvedPath": path, "requestBody": rb}
    merge_json_body(out, proxy, "updatePackage", ok_statuses=(200, 204))
    emit_result(out, inline=lf_inline_flag())


if __name__ == "__main__":
    main()
