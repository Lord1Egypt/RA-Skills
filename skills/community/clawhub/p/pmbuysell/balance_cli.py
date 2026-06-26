"""
Polymarket 余额查询 CLI，供模型/脚本快速调用。

用法:
  python -m pmbuysell.skills.balance_cli --account ACC1
  python -m pmbuysell.skills.balance_cli --account ACC1 --slug tc-updown-5m-1772452800
"""

from __future__ import annotations

import argparse
import json
import sys

from .multi_account import get_balance


def main() -> None:
    p = argparse.ArgumentParser(description="Polymarket 余额查询 CLI")
    p.add_argument("--account", required=True, help="账号 ID，如 ACC1")
    p.add_argument("--slug", default="", help="可选：市场 slug，用于同时查询该市场的 up/down 持仓")
    args = p.parse_args()

    slug = args.slug.strip() or None
    result = get_balance(account_id=args.account, slug=slug)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result.get("ok") else 1)


if __name__ == "__main__":
    main()

