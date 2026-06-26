#!/usr/bin/env python3
"""bg.logistics.shipment.v2.confirm — 确认发货 V2（待发货 → 已发货）."""
import _global_fulfillment_script as m

if __name__ == "__main__":
    m.run_cli(
        "bg.logistics.shipment.v2.confirm",
        "global_self_fulfilled_logistics_shipment_v2_confirm.py '<JSON>'",
    )
