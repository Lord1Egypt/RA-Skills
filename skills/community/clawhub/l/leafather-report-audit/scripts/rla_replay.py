#!/usr/bin/env python3
"""rla_replay.py — 策略回放：同一批报告，换策略后判决怎么变。

为什么需要它：
    改 policy 之前，你必须知道"谁会从通过变成拦下"。
    不量就改 = 拿真实交付物做实验。

用法：
    # 对比两套策略
    python3 scripts/rla_replay.py --ledger ledger.json --files a.md b.md \
        --policy-a old.yaml --policy-b new.yaml --mount "data=/path/your.parquet"

    # 只给 --policy-b：与"当前策略"比（默认读技能根的 policy.yaml）
    python3 scripts/rla_replay.py --ledger ledger.json --files a.md --policy-b strict.yaml

    # 输出机器可读
    ... --json

退出码：0 无变化｜1 有报告判决变化｜2 未就绪
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE / "rla_audit.py"

LABEL = {0: "PASS", 3: "REVIEW", 1: "FAIL", 2: "未就绪"}
STRICTNESS = {"PASS": 0, "REVIEW": 1, "FAIL": 2, "未就绪": 3}


def run_one(ledger: str, report: str, policy: str | None, mounts: list[str]) -> tuple[int, str]:
    cmd = [sys.executable, str(AUDIT), "--ledger", ledger, "--files", report, "--no-write"]
    if policy:
        cmd += ["--policy", policy]
    for m in mounts:
        cmd += ["--mount", m]
    p = subprocess.run(cmd, capture_output=True, text=True)
    concl = ""
    for line in p.stdout.splitlines():
        if "结论" in line:
            concl = line.split("**")[1] if "**" in line else line.strip()
            break
    return p.returncode, concl


def main() -> int:
    ap = argparse.ArgumentParser(description="策略回放：换策略后判决怎么变")
    ap.add_argument("--ledger", required=True)
    ap.add_argument("--files", nargs="+", required=True)
    ap.add_argument("--policy-a", default=None, help="旧策略（不给则用技能根 policy.yaml）")
    ap.add_argument("--policy-b", default=None, help="新策略（必给其中之一）")
    ap.add_argument("--mount", action="append", default=[])
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if not args.policy_a and not args.policy_b:
        print("❌ 未就绪：至少给 --policy-a 或 --policy-b 之一", file=sys.stderr)
        return 2
    for p in (args.policy_a, args.policy_b):
        if p and not Path(p).exists():
            print(f"❌ 未就绪：策略文件不存在 {p}", file=sys.stderr)
            return 2

    rows, changed = [], 0
    for f in args.files:
        if not Path(f).exists():
            print(f"❌ 未就绪：报告不存在 {f}", file=sys.stderr)
            return 2
        ca, ta = run_one(args.ledger, f, args.policy_a, args.mount)
        cb, tb = run_one(args.ledger, f, args.policy_b, args.mount)
        if ca == 2 or cb == 2:
            print(f"⚠️  {Path(f).name}：未就绪，跳过", file=sys.stderr)
            continue
        la, lb = LABEL.get(ca, str(ca)), LABEL.get(cb, str(cb))
        if la != lb:
            changed += 1
            delta = STRICTNESS[lb] - STRICTNESS[la]
            arrow = "⬆ 变严" if delta > 0 else "⬇ 变松"
        else:
            arrow = "—"
        rows.append({"file": Path(f).name, "a": la, "b": lb, "change": arrow})

    if args.json:
        print(json.dumps({"rows": rows, "changed": changed}, ensure_ascii=False, indent=2))
    else:
        na = Path(args.policy_a).name if args.policy_a else "policy.yaml(当前)"
        nb = Path(args.policy_b).name if args.policy_b else "policy.yaml(当前)"
        print(f"策略对比：A={na}  →  B={nb}\n")
        print(f"{'报告':<28}{'A':>8}{'B':>8}   变化")
        for r in rows:
            print(f"{r['file']:<28}{r['a']:>8}{r['b']:>8}   {r['change']}")
        print(f"\n共 {len(rows)} 份，判决变化 {changed} 份")
        if changed:
            print("⚠️ 上线新策略前，请先看上面这些「会变」的报告，确认它们变得合理。")

    return 1 if changed else 0


if __name__ == "__main__":
    sys.exit(main())
