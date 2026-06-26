#!/usr/bin/env python3
"""bg.logistics.shipment.sub.confirm — 确认子包裹发货（拆包场景）."""
import _global_fulfillment_script as m

if __name__ == "__main__":
    m.run_cli(
        "bg.logistics.shipment.sub.confirm",
        "global_self_fulfilled_logistics_shipment_sub_confirm.py '<JSON>'",
    )
