#!/usr/bin/env python3
"""bg.logistics.shipped.package.confirm — 批量确认已购标包裹为已发货."""
import _global_fulfillment_script as m

if __name__ == "__main__":
    m.run_cli(
        "bg.logistics.shipped.package.confirm",
        "global_buy_shipping_logistics_shipped_package_confirm.py '<JSON>'",
    )
