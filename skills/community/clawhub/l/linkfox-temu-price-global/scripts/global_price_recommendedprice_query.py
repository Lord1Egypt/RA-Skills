#!/usr/bin/env python3
"""temu.local.goods.recommendedprice.query — 推荐供货价查询."""
import _global_price_script as m

if __name__ == "__main__":
    m.run_cli(
        "temu.local.goods.recommendedprice.query",
        "global_price_recommendedprice_query.py '<JSON>'",
    )
