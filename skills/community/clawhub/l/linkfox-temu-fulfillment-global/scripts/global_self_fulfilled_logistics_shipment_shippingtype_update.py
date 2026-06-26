#!/usr/bin/env python3
"""bg.logistics.shipment.shippingtype.update — 更新物流跟踪号/发货方式."""
import _global_fulfillment_script as m

if __name__ == "__main__":
    m.run_cli(
        "bg.logistics.shipment.shippingtype.update",
        "global_self_fulfilled_logistics_shipment_shippingtype_update.py '<JSON>'",
    )
