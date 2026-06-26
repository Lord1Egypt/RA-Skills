#!/usr/bin/env python3
"""bg.logistics.shipment.update — 延后发货时限更新 / 购标失败包裹重试."""
import _global_fulfillment_script as m

if __name__ == "__main__":
    m.run_cli(
        "bg.logistics.shipment.update",
        "global_buy_shipping_logistics_shipment_update.py '<JSON>'",
    )
