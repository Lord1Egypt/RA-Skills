#!/usr/bin/env python3
"""temu.logistics.self.delivery.pod.audit.result.get — 自配送 POD 审核结果查询."""
import _eu_fulfillment_script as m

if __name__ == "__main__":
    m.run_cli(
        "temu.logistics.self.delivery.pod.audit.result.get",
        "eu_self_fulfilled_logistics_self_delivery_pod_audit_result_get.py \'<JSON>\'",
    )
