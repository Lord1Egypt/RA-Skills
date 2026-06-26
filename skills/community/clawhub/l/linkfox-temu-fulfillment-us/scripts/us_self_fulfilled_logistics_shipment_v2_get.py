#!/usr/bin/env python3
"""bg.logistics.shipment.v2.get — 查询自发货后的发货/物流信息 V2."""
import _us_fulfillment_script as m

if __name__ == "__main__":
    m.run_cli(
        "bg.logistics.shipment.v2.get",
        "us_self_fulfilled_logistics_shipment_v2_get.py '<JSON>'",
    )
