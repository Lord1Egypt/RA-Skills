#!/usr/bin/env python3
"""rla_report.py — 一条命令出报告：录像 → 全量记账 → 审计。

为什么需要它：
    手写账本是"选摘记账"（人工挑主指标），实测漏掉 40%（某 agent那份报告用了 300+ 个数，
    账本只有 195 条）。这不是执行不到位，是方法本身的缺陷。
    **只有"跑过的 SQL 全记"，覆盖面才从方法上保证。**

用法：
    python3 scripts/rla_report.py \
        --out report.md --ledger ledger.json \
        --mount "data=/path/your.parquet" \
        --report-name "感冒场景洞察" --data-as-of 2026-10-19 \
        -- python3 build_report.py

    它会：
      1. 包住业务脚本运行，录像所有 SQL（业务代码零改动）
      2. SQL → 账本（全量，不是选摘）
      3. 审计刚生成的报告
      4. 输出结论 + 待补清单

    加 --auto-derive：自动把"报告里有、账本没有"的比率补成派生声明（标 auto_suggested，需人确认）。
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

try:                      # 子进程输出与主流程提示会乱序，这里强制行缓冲
    sys.stdout.reconfigure(line_buffering=True)
    sys.stderr.reconfigure(line_buffering=True)
except Exception:
    pass


def call(args: list[str]) -> int:
    r = subprocess.run([sys.executable] + args)
    return r.returncode


def main() -> int:
    import deps_check as DC
    DC.banner(allow_degrade=True)   # 依赖体检：缺包时给人话，不给 traceback
    ap = argparse.ArgumentParser(description="一条命令出报告：录像→记账→审计")
    ap.add_argument("--out", required=True, help="报告文件（业务脚本会生成它）")
    ap.add_argument("--ledger", default="ledger.json")
    ap.add_argument("--mount", action="append", default=[])
    ap.add_argument("--report-name", default="未命名报告")
    ap.add_argument("--data-as-of", default="")
    ap.add_argument("--agent", default="")
    ap.add_argument("--auto-derive", action="store_true",
                    help="自动补派生声明（标 auto_suggested，仍建议人工过目）")
    ap.add_argument("--policy", default=None)
    ap.add_argument("--metrics", default=None, help="metrics.yaml（可选，给数字贴稳定身份）")
    ap.add_argument("--files", default="",
                    help="额外交付件（逗号分隔）。默认只审 --out 那一份；"
                         "多件（md+客户版+摘要+PPT）时全列上，才能查跨件一致")
    ap.add_argument("cmd", nargs=argparse.REMAINDER, help="-- 之后是生成报告的命令")
    args = ap.parse_args()

    cmd = [c for c in args.cmd if c != "--"]
    if not cmd:
        print("❌ 用法：rla_report.py --out report.md -- python3 build.py", file=sys.stderr)
        return 2

    ledger = str(Path(args.ledger).resolve())
    out = str(Path(args.out).resolve())

    # ── 第 1 步：录像并全量记账 ───────────────────────────────
    print("=" * 60)
    print("① 跑报告 + 录像 + 全量记账")
    print("=" * 60)
    track = [str(HERE / "rla_track.py"), "--ledger", ledger,
             "--report-name", args.report_name,
             "--report-files", (args.files or Path(out).name),
             "--data-as-of", args.data_as_of,
             "--agent", args.agent]
    for m in args.mount:
        track += ["--mount", m]
    if args.metrics:
        track += ["--metrics", args.metrics]
    rc = call(track + ["--"] + cmd)
    if rc != 0:
        print(f"❌ 录像或记账失败（退出码 {rc}）；报告可能已生成，但没有账本", file=sys.stderr)
        return rc
    if not Path(out).exists():
        print(f"❌ 业务命令没有生成 {args.out}，无处审计", file=sys.stderr)
        return 2

    # ── 第 1.5 步：记账体检（趁报告还没写完）─────────────────
    # 这一步是"做报告时就介入"的落点：不等交付前才发现覆盖率不够
    print("")
    call([str(HERE / "rla_health.py"), "--ledger", ledger]
         + (["--defs", args.metrics] if args.metrics else []))

    # ── 第 2 步：（可选）自动补派生声明 ───────────────────────
    if args.auto_derive:
        print("\n" + "=" * 60)
        print("② 自动补派生声明")
        print("=" * 60)
        call([str(HERE / "rla_derive.py"), "--ledger", ledger, "--files", out, "--apply"])

    # ── 第 3 步：审计 ───────────────────────────────────────
    print("\n" + "=" * 60)
    print("③ 审计")
    print("=" * 60)
    # 路径基准修正（2026-10-25 某 agent报的 bug）：
    # --out 做了 resolve()，--files 没有 → 相对路径被审计按"账本目录"再拼一次，
    # 变成 deliverables/deliverables/xxx.md。这里统一处理：先按 CWD，不存在再按账本目录。
    ledger_dir = Path(ledger).parent
    def _fix(fs: str) -> Path:
        p = Path(fs)
        if p.is_absolute():
            return p
        if p.exists():
            return p.resolve()
        cand = ledger_dir / fs
        return cand if cand.exists() else p.resolve()

    audit_files = ([str(_fix(f.strip())) for f in (args.files or "").split(",") if f.strip()]
                   or [out])
    audit = [str(HERE / "rla_audit.py"), "--ledger", ledger,
             "--files", *audit_files,
             "--export-missing", str(Path(ledger).with_name("ledger.missing.json"))]
    for m in args.mount:
        audit += ["--mount", m]
    if args.policy:
        audit += ["--policy", args.policy]
    rc = call(audit)

    print("\n" + "=" * 60)
    print({0: "✅ 通过：报告与账本一致，可交付",
           3: "⚠️ 需人工复核：有未能验证的部分，建议看结论后再决定",
           1: "❌ 不通过：有来源不明或算错的数字，先修",
           2: "⛔ 未就绪：配置或数据缺失（不算通过）"}.get(rc, f"退出码 {rc}"))
    print(f"账本：{ledger}\n报告：{out}")
    if Path(ledger).with_name("ledger.missing.json").exists():
        print(f"待补清单：{Path(ledger).with_name('ledger.missing.json')}")
    print("=" * 60)
    return rc


if __name__ == "__main__":
    sys.exit(main())
