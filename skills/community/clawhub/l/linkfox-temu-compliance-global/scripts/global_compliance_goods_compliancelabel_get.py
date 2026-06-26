#!/usr/bin/env python3
"""bg.goods.compliancelabel.get — 合规标签查询."""
import _global_compliance_script as m

if __name__ == "__main__":
    m.run_cli(
        "bg.goods.compliancelabel.get",
        "global_compliance_goods_compliancelabel_get.py \'<JSON>\'",
    )
