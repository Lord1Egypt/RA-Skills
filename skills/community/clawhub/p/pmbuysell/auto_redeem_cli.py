"""
Polymarket 自动结算（redeem）CLI 入口。

免费版仅提供接口，实际执行需购买 Pro 版本（pmbuysell_redeem）。
"""

from __future__ import annotations

import argparse
import json
import sys

_PRO_MESSAGE = (
    "自动结算为 Pro 版本功能， 价格10usdc请购买后使用。联系tg：@taroers 购买"
)

_PRO_MESSAGE_EN = '''Automatic settlement is a Pro version feature. The price is 10 USDC. Please purchase before using.
Contact Telegram: @taroers to buy'''


def main() -> None:
    p = argparse.ArgumentParser(description="Polymarket 自动结算（redeem）CLI [Pro 版本]")
    p.add_argument("--account", required=True, help="账号 ID，如 ACC1")
    p.add_argument("--dry-run", action="store_true", help="只构造交易不发送")
    args = p.parse_args()

    result = {
        "ok": False,
        "message": _PRO_MESSAGE,
        "message_en": _PRO_MESSAGE_EN,
        "result": None,
        "upgrade": "",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(1)


if __name__ == "__main__":
    main()
