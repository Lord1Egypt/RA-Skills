#!/usr/bin/env python3
"""bg.logistics.companies.get — 获取区域可用物流服务商列表."""
import _global_fulfillment_script as m

if __name__ == "__main__":
    m.run_cli(
        "bg.logistics.companies.get",
        "global_self_fulfilled_logistics_companies_get.py '<JSON>'",
    )
