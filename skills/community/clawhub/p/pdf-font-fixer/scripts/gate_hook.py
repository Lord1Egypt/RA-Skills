#!/usr/bin/env python3
"""统一字体门禁钩子（gate hook）。

供其它 skill 在产出 PDF 后调用，把「记得手动跑门禁」变成「代码里强制跑」。

用法（调用方定位到本 skill 目录后）::

    python3 <pdf-font-fixer>/scripts/gate_hook.py 产物.pdf --min-version 1.0.1

退出码::

    0  门禁通过
    2  门禁不通过（字体有风险 / 逐字符审计失败）
    3  找不到 gate.py 或本模块不可用
    4  版本低于 --min-version（仅在 --strict-version 时返回，否则仅告警）

设计要点：
- 只做「定位 + 版本校验 + 透传」，诊断逻辑仍由 gate.py 负责，不重复实现。
- 不静默放过：找不到 gate.py 一律返回 3，调用方必须显式处理。
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


def fixer_root() -> Path:
    """本文件在 <root>/scripts/ 下，往上两级即 skill 根目录。"""
    return Path(__file__).resolve().parent.parent


def read_version(root: Path) -> str | None:
    skill_md = root / "SKILL.md"
    if not skill_md.exists():
        return None
    text = skill_md.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"^version:\s*([0-9][0-9.]*)", text, re.MULTILINE)
    return m.group(1) if m else None


def parse_version(v: str) -> tuple[int, ...]:
    parts = []
    for seg in v.strip().split("."):
        num = re.match(r"\d+", seg)
        parts.append(int(num.group()) if num else 0)
    return tuple(parts)


def main() -> int:
    ap = argparse.ArgumentParser(description="统一字体门禁钩子")
    ap.add_argument("pdf", nargs="+", help="待检查的 PDF")
    ap.add_argument("--min-version", default=None, help="要求的最低版本，如 1.0.1")
    ap.add_argument("--strict-version", action="store_true", help="版本不达标时直接失败（默认仅告警）")
    ap.add_argument("--quiet", action="store_true", help="透传给 gate.py 的 --quiet")
    ap.add_argument("--auto-fix", dest="auto_fix", action="store_true", default=True,
                    help="门禁不通过时自动产出「无损版 + 轮廓版」兜底（默认开启）")
    ap.add_argument("--no-auto-fix", dest="auto_fix", action="store_false",
                    help="只报告不修复（调用方要自己做降级处理时用）")
    args = ap.parse_args()

    root = fixer_root()
    gate = root / "scripts" / "gate.py"
    if not gate.exists():
        print(f"❌ 未找到 gate.py（预期位置：{gate}），无法执行字体门禁", file=sys.stderr)
        return 3

    if args.min_version:
        cur = read_version(root)
        if cur is None:
            print("⚠️ 无法读取 pdf-font-fixer 版本，跳过版本校验", file=sys.stderr)
        elif parse_version(cur) < parse_version(args.min_version):
            msg = f"⚠️ pdf-font-fixer 版本过低：当前 {cur}，要求 ≥ {args.min_version}"
            if args.strict_version:
                print(f"❌ {msg}", file=sys.stderr)
                return 4
            print(msg, file=sys.stderr)

    cmd = [sys.executable, str(gate), *args.pdf]
    if args.quiet:
        cmd.append("--quiet")
    if args.auto_fix:
        cmd.append("--auto-fix")
    return subprocess.call(cmd)


if __name__ == "__main__":
    sys.exit(main())
