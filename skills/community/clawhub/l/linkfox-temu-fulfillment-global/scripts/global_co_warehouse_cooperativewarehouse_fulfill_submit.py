#!/usr/bin/env python3
"""bg.cooperativewarehouse.fulfill.submit — 提交合作仓履约."""
import _global_fulfillment_script as m

if __name__ == "__main__":
    m.run_cli(
        "bg.cooperativewarehouse.fulfill.submit",
        "global_co_warehouse_cooperativewarehouse_fulfill_submit.py '<JSON>'",
    )
