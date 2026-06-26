#!/usr/bin/env python3
"""bg.order.unshipped.package.get — 查询 Temu 集成物流已履约但未发货包裹."""
import _us_fulfillment_script as m

if __name__ == "__main__":
    m.run_cli(
        "bg.order.unshipped.package.get",
        "us_buy_shipping_order_unshipped_package_get.py '<JSON>'",
    )
