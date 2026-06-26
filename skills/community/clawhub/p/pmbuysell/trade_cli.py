"""
Polymarket 一键下单 CLI，供模型/脚本快速调用。
用法: python -m pmbuysell.skills.trade_cli --account ACC1 --action buy --slug <slug> --side down --amount 10
或自动 slug: python -m pmbuysell.skills.trade_cli --account ACC1 --action buy --slug-mode auto --symbol tc --timeframe 5m --side down --amount 10
"""
from __future__ import annotations

import argparse
import json
import sys
import time

from .multi_account import market_buy, market_sell


def _slug_auto(symbol: str, timeframe: str) -> str:
    if timeframe not in ("5m", "15m"):
        raise ValueError("timeframe 只能是 5m 或 15m")
    now_ts = int(time.time())
    bucket_seconds = 300 if timeframe == "5m" else 900
    bucket_ts = now_ts - (now_ts % bucket_seconds)
    return f"{symbol}-updown-{timeframe}-{bucket_ts}"


def main() -> None:
    p = argparse.ArgumentParser(description="Polymarket 市价买卖 CLI")
    p.add_argument("--account", required=True, help="账号 ID，如 ACC1")
    p.add_argument("--action", required=True, choices=("buy", "sell"), help="buy 或 sell")
    p.add_argument("--slug", default="", help="市场 slug，如 tc-updown-5m-1772452800")
    p.add_argument("--slug-mode", choices=("manual", "auto"), default="manual", help="manual=用 --slug；auto=按 symbol+timeframe 生成")
    p.add_argument("--symbol", default="tc", help="slug_mode=auto 时使用，如 tc / btc")
    p.add_argument("--timeframe", default="5m", help="slug_mode=auto 时使用，5m 或 15m")
    p.add_argument("--side", required=True, choices=("up", "down"), help="up 或 down")
    p.add_argument("--amount", type=float, required=True, help="买入: USDC 金额；卖出: token 数量")
    args = p.parse_args()

    slug = args.slug
    if args.slug_mode == "auto":
        slug = _slug_auto(args.symbol.strip().lower(), args.timeframe.strip().lower())

    if not slug:
        print(json.dumps({"ok": False, "message": "缺少 slug 或 slug_mode=auto 时 symbol/timeframe 无效"}, ensure_ascii=False))
        sys.exit(1)

    if args.action == "buy":
        result = market_buy(args.account, slug, args.side, args.amount)
    else:
        result = market_sell(args.account, slug, args.side, args.amount)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result.get("ok") else 1)


if __name__ == "__main__":
    main()
