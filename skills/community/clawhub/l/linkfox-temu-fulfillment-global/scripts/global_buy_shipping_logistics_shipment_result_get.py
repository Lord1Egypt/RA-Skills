#!/usr/bin/env python3
"""bg.logistics.shipment.result.get — 查询购标/在线下单结果（面单状态）."""
import _global_fulfillment_script as m

if __name__ == "__main__":
    m.run_cli(
        "bg.logistics.shipment.result.get",
        "global_buy_shipping_logistics_shipment_result_get.py '<JSON>'",
    )
