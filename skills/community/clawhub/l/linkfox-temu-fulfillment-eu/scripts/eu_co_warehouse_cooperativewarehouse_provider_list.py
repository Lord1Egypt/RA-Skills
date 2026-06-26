#!/usr/bin/env python3
"""bg.cooperativewarehouse.provider.list — 合作仓服务商列表."""
import _eu_fulfillment_script as m

if __name__ == "__main__":
    m.run_cli(
        "bg.cooperativewarehouse.provider.list",
        "eu_co_warehouse_cooperativewarehouse_provider_list.py '<JSON>'",
    )
