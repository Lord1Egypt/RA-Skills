#!/usr/bin/env python3
"""bg.logistics.shippingservices.get — 按包裹尺寸/重量查询可用物流渠道（Buy-Shipping 查价）."""
import _us_fulfillment_script as m

if __name__ == "__main__":
    m.run_cli(
        "bg.logistics.shippingservices.get",
        "us_buy_shipping_logistics_shippingservices_get.py '<JSON>'",
    )
