#!/usr/bin/env python3
"""temu.local.goods.baseprice.recommend — 推荐基础价/供货价估算."""
import _us_price_script as m

if __name__ == "__main__":
    m.run_cli(
        "temu.local.goods.baseprice.recommend",
        "us_price_baseprice_recommend.py '<JSON>'",
    )
