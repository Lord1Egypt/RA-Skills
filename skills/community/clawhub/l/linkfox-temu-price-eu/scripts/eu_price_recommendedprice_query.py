#!/usr/bin/env python3
"""temu.local.goods.recommendedprice.query — 推荐供货价查询."""
import _eu_price_script as m

if __name__ == "__main__":
    m.run_cli(
        "temu.local.goods.recommendedprice.query",
        "eu_price_recommendedprice_query.py '<JSON>'",
    )
