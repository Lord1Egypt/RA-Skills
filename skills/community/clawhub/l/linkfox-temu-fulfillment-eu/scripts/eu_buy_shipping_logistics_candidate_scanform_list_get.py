#!/usr/bin/env python3
"""temu.logistics.candidate.scanform.list.get — 查询可生成 Scan Form 的候选包裹分组."""
import _eu_fulfillment_script as m

if __name__ == "__main__":
    m.run_cli(
        "temu.logistics.candidate.scanform.list.get",
        "eu_buy_shipping_logistics_candidate_scanform_list_get.py '<JSON>'",
    )
