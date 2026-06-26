#!/usr/bin/env python3
"""bg.promotion.activity.goods.query — 活动已报名商品查询."""
import _us_promotion_script as m

if __name__ == "__main__":
    m.run_cli(
        "bg.promotion.activity.goods.query",
        "us_promotion_activity_goods_query.py '<JSON>'",
    )
