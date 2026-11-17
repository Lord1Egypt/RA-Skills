#!/usr/bin/env python3
"""rla_health.py — 记账体检：跑完脚本，趁报告还没写完，告诉你哪几条会没出处

为什么需要它：
    录像跑完只给一行「N 条查询记录」，用户接着就去看最终审计结论了。
    等看到「覆盖率 60%」时报告已经写完，返工成本最高。
    这个体检把「哪几条数会没账本」提前到**报告还没写**的时候说。

用法：
    python3 scripts/rla_health.py --ledger ledger.json                  # 只看账本自洽性
    python3 scripts/rla_health.py --ledger ledger.json --defs metrics.yaml
    python3 scripts/rla_health.py --ledger ledger.json --defs indicators.yaml
    python3 scripts/rla_health.py --ledger ledger.json --quiet          # 只在一句话里报

判断依据：
    · 账本条目有 `metric_id` = 已被指标定义认领（label/caliber 来自定义，报告里能锚住）
    · 没有 `metric_id` = label 是机器从 SQL 猜的，报告里写「总行数」大概率锚不住
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))


def _short(sql: str, n: int = 70) -> str:
    s = " ".join(str(sql or "").split())
    return s if len(s) <= n else s[: n - 1] + "…"


def _norm(s: str) -> str:
    return " ".join(str(s or "").lower().split())


def main() -> int:
    ap = argparse.ArgumentParser(description="记账体检")
    ap.add_argument("--ledger", required=True)
    ap.add_argument("--defs", default=None, help="指标定义文件（metrics.yaml / indicators.yaml）")
    ap.add_argument("--quiet", action="store_true", help="只输出一行摘要")
    ap.add_argument("--top", type=int, default=8, help="未认领明细最多列几条（默认 8）")
    args = ap.parse_args()

    lp = Path(args.ledger)
    if not lp.exists():
        print(f"❌ 账本不存在：{lp}", file=sys.stderr)
        return 2
    d = json.loads(lp.read_text(encoding="utf-8-sig"))
    numbers = [n for n in (d.get("numbers") or []) if n.get("id") is not None]
    if not numbers:
        print("❌ 账本里没有任何指标（录像没抓到 SQL？）", file=sys.stderr)
        return 2

    claimed = [n for n in numbers if n.get("metric_id")]
    unclaimed = [n for n in numbers if not n.get("metric_id")]
    total = len(numbers)

    if args.quiet:
        print(f"记账体检：{total} 条｜已认领 {len(claimed)}｜未认领 {len(unclaimed)}")
        return 0

    print("─" * 64)
    print("② 记账体检（趁报告还没写完，现在补还来得及）")
    print("─" * 64)
    print(f"账本：{total} 条｜已认领 {len(claimed)} 条（对上了指标定义）"
          f"｜未认领 {len(unclaimed)} 条")

    if not args.defs:
        if unclaimed:
            print()
            print("⚠️ 这次没给指标定义（--defs），所有条目的 label 都是从 SQL 猜的。")
            print("   报告里写「总行数」「客户数」这类说法时，大概率锚不住 → 覆盖率会很低。")
            print("   补法：写一个 metrics.yaml，给关键 SQL 加 match_sql（详见 examples/metrics.yaml）")
    elif unclaimed:
        print()
        print(f"未认领的 {len(unclaimed)} 条 —— 这些 SQL 算出来的数，"
              f"写进报告会被判「来源不明」：")
        for n in unclaimed[: args.top]:
            loc = n.get("origin") or ""
            print(f"  {str(n.get('label'))[:18]:<20}{_short(n.get('sql'))}")
        if len(unclaimed) > args.top:
            print(f"  …另外 {len(unclaimed) - args.top} 条，用 --top 放宽")
        print()
        print(f"怎么补：在 {Path(args.defs).name} 里给这几条加 match_sql"
              f"（SQL 子串匹配，命中多条取最长的）")
        print("       或者确认它们不产出报告数字（纯中间计算可以不管）")
    else:
        print("✅ 全部条目都已认领，报告里写这些指标都能锚住")

    # 顺带提醒：账本过期（数据变了没重算）
    fp = (d.get("report") or {}).get("data_fingerprint")
    if fp:
        try:
            import rla_render as RR
            cur = RR._current_fingerprint(lp)
            if cur and str(cur) != str(fp):
                print()
                print("⚠️ 数据文件已变，账本是旧版本的 —— 先重跑生成账本再继续")
        except Exception:  # noqa: BLE001
            pass

    print("─" * 64)
    return 0


if __name__ == "__main__":
    sys.exit(main())
