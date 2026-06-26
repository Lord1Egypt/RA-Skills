#!/usr/bin/env python3
"""bg.logistics.shipment.create — Buy-Shipping 在线下单购标（创建包裹/面单）."""
import _eu_fulfillment_script as m

if __name__ == "__main__":
    m.run_cli(
        "bg.logistics.shipment.create",
        "eu_buy_shipping_logistics_shipment_create.py '<JSON>'",
    )
