#!/usr/bin/env python3
"""bg.logistics.companies.get — 获取区域可用物流服务商列表."""
import _eu_fulfillment_script as m

if __name__ == "__main__":
    m.run_cli(
        "bg.logistics.companies.get",
        "eu_self_fulfilled_logistics_companies_get.py '<JSON>'",
    )
