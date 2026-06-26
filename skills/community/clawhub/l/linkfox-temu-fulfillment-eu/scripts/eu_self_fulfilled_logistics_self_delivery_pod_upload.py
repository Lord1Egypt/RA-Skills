#!/usr/bin/env python3
"""temu.logistics.self.delivery.pod.upload — 自配送 POD 上传."""
import _eu_fulfillment_script as m

if __name__ == "__main__":
    m.run_cli(
        "temu.logistics.self.delivery.pod.upload",
        "eu_self_fulfilled_logistics_self_delivery_pod_upload.py \'<JSON>\'",
    )
