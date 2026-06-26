#!/usr/bin/env python3
"""bg.local.goods.priceorder.query — 定价单列表查询（白名单）."""
import _eu_price_script as m

if __name__ == "__main__":
    m.run_cli(
        "bg.local.goods.priceorder.query",
        "eu_price_priceorder_query.py '<JSON>'",
    )
