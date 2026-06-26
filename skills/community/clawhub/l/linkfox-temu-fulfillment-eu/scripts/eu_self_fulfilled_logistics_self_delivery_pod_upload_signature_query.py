#!/usr/bin/env python3
"""temu.logistics.self.delivery.pod.upload.signature.query — 自配送 POD 上传签名查询."""
import _eu_fulfillment_script as m

if __name__ == "__main__":
    m.run_cli(
        "temu.logistics.self.delivery.pod.upload.signature.query",
        "eu_self_fulfilled_logistics_self_delivery_pod_upload_signature_query.py \'<JSON>\'",
    )
