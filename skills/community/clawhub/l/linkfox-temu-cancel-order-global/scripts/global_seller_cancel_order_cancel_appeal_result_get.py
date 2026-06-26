#!/usr/bin/env python3
"""temu.order.cancel.appeal.result.get — 查询卖家取消申请结果."""
import _global_cancel_order_script as m

if __name__ == "__main__":
    m.run_cli(
        "temu.order.cancel.appeal.result.get",
        "global_seller_cancel_order_cancel_appeal_result_get.py '<JSON>'",
    )
