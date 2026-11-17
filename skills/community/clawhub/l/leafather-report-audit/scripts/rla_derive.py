#!/usr/bin/env python3
"""rla_derive.py — 派生候选建议器（离线用，不参与审计判定）。

为什么单独一个工具：
    审计时必须确定性 —— 不能"猜"这个数字怎么来的。
    但帮 agent 补账可以带猜测 —— 猜出来的东西要人确认后才写进账本。

    一句话：**搜索只出现在"建议"阶段，永远不出现在"判定"阶段。**

用法：
    # 只看建议（不改账本）
    python3 scripts/rla_derive.py --ledger ledger.json --files report.md

    # 把建议写进账本（标 auto_suggested: true，仍需人过目）
    python3 scripts/rla_derive.py --ledger ledger.json --files report.md --apply
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rla_extract  # noqa: E402

PCT_HINT = ("%", "％", "率", "占比", "比例", "份额")
QUOT_HINT = ("倍", "均", "每", "单价", "客单", "人均", "店均")


def candidates(target: float, nums: list[dict], raw: str, ctx: str) -> list[dict]:
    """给一个不在账本里的数字，找可能的派生关系。不做减法（教训）。"""
    out = []
    vals = [(n["id"], float(n["value"]), str(n.get("label") or n["id"]))
            for n in nums if isinstance(n.get("value"), (int, float))]
    is_pct = any(k in ctx for k in PCT_HINT) or raw.rstrip().endswith(("%", "％"))
    want_quot = any(k in ctx for k in QUOT_HINT)

    if is_pct and 0 < abs(target) <= 100:
        for ia, va, la in vals:
            for ib, vb, lb in vals:
                if ia == ib or not vb or abs(va) > abs(vb):
                    continue
                if abs(va / vb * 100 - target) <= 0.05:
                    out.append({"label": f"{la} ÷ {lb}", "expr": f"{ia}/{ib}*100",
                                "num": ia, "den": ib, "how": "percent",
                                "confidence": "high" if out == [] else "medium"})
    if want_quot:
        for ia, va, la in vals:
            for ib, vb, lb in vals:
                if ia == ib or not vb:
                    continue
                if abs(va / vb - target) <= max(abs(target) * 0.005, 0.05):
                    out.append({"label": f"{la} ÷ {lb}", "expr": f"{ia}/{ib}",
                                "num": ia, "den": ib, "how": "quotient",
                                "confidence": "high"})
    return out[:3]


def main() -> int:
    ap = argparse.ArgumentParser(description="派生候选建议（离线）")
    ap.add_argument("--ledger", required=True)
    ap.add_argument("--files", nargs="+", required=True)
    ap.add_argument("--apply", action="store_true", help="把建议写进账本")
    ap.add_argument("--max-suggest", type=int, default=3)
    args = ap.parse_args()

    lp = Path(args.ledger)
    ledger = json.loads(lp.read_text(encoding="utf-8-sig"))
    nums = ledger["numbers"]
    known = {round(float(n["value"]), 6) for n in nums if isinstance(n.get("value"), (int, float))}

    # 收报告里"账本没有"的指标数字
    missing = []
    for f in args.files:
        for n in rla_extract.extract(Path(f)):
            if n["kind"] != "metric":
                continue
            if round(n["value"], 6) in known:
                continue
            missing.append(n)

    if not missing:
        print("✅ 报告里没有『账本之外』的指标数字，无需补声明")
        return 0

    if len(nums) > 100:
        print(f"⚠️  账本已有 {len(nums)} 条指标。候选组合空间很大，"
              "建议的置信度会明显下降，务必人工过目再 --apply。\n", file=sys.stderr)

    print(f"发现 {len(missing)} 个账本里没有的指标数字：\n")
    added = 0
    for i, m in enumerate(missing, 1):
        cands = candidates(m["value"], nums, m["raw"], m["context"])
        print(f"{i}. {m['raw']}  @{m['file']} {m['loc']}")
        print(f"   上下文：{m['context'][:64]}")
        if not cands:
            print("   ❌ 没找到候选 —— 这个数字需要人工说明来历\n")
            continue
        for c in cands[:args.max_suggest]:
            print(f"   → {c['label']}   [{c['expr']}]  置信度 {c['confidence']}")
        best = cands[0]
        print()
        if args.apply and best["confidence"] == "high":
            nid = f"d{len(nums) + added + 1}"
            nums.append({
                "id": nid, "label": f"{best['label']}（派生）", "value": m["value"],
                "unit": "", "caliber": f"由 {best['expr']} 计算",
                "derived_from": [best["num"], best["den"]], "expr": best["expr"],
                "verifiable": True, "auto_suggested": True,
                "origin": f"rla_derive 依据「{m['context'][:40]}」建议，待人工确认",
            })
            added += 1
            print(f"   ✅ 已写入账本 {nid}（auto_suggested: true）\n")

    if args.apply and added:
        lp.write_text(json.dumps(ledger, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"已写入 {added} 条派生到 {lp.name}")
        print("⚠️  这些条目标了 auto_suggested: true —— 请人工确认口径后再交付。")
    elif args.apply:
        print("没有置信度足够的候选，账本未改动。")
    else:
        print("（未改账本。确认后加 --apply 写入）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
