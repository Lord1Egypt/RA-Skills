#!/usr/bin/env python3
"""bg.cooperativewarehouse.fulfill.cancel — 取消合作仓履约单."""
import _eu_fulfillment_script as m

if __name__ == "__main__":
    m.run_cli(
        "bg.cooperativewarehouse.fulfill.cancel",
        "eu_co_warehouse_cooperativewarehouse_fulfill_cancel.py '<JSON>'",
    )
