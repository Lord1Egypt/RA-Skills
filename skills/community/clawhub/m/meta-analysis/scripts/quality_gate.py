#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
quality_gate.py — human sign-off gate + R 计算红灯判定（升级项 ct-update A）

消费 R 侧 `run_quality_gate()` 产出的红灯 JSON，执行「人工签字门」：
  - status == "red"     → 默认阻断（exit 2），必须 --yes 人工签字后才放行（exit 0）
  - status == "yellow"  → 警告（exit 1），--yes 可放行
  - status == "green"   → 直接放行（exit 0）

设计意图（参照 O0000-code/meta-analysis-skill）：
  数值判断完全由 R 计算（不让 LLM 读数字判断），本脚本只负责门控 + 人工确认。

用法：
  python scripts/quality_gate.py gate.json              # 检查（红灯阻断）
  python scripts/quality_gate.py gate.json --yes        # 人工签字放行
  python scripts/quality_gate.py -                      # 从 stdin 读 JSON
  python scripts/quality_gate.py gate.json --json-out   # 打印判定 JSON

exit codes: 0=pass(绿/黄-yes/红-yes) 1=warn(黄未确认) 2=blocked(红未确认) 3=输入错误
纯标准库，无第三方依赖。
"""

import argparse
import json
import os
import sys


def is_chinese_os() -> bool:
    """轻量 locale 检测（无 i18n 依赖时的本地兜底）。"""
    env = "".join(os.environ.get(k, "") for k in ("LANG", "LC_ALL", "LANGUAGE"))
    return any(t in env.lower() for t in ("zh", "cn", "chs"))


_ZH = None


def t(en: str, zh: str) -> str:
    return zh if _ZH else en


def load_gate(path: str) -> dict:
    """读取 gate JSON：'-' = stdin；失败抛 ValueError。"""
    if path == "-":
        raw = sys.stdin.read()
    else:
        with open(path, encoding="utf-8") as f:
            raw = f.read()
    data = json.loads(raw)  # JSONDecodeError 冒泡
    if not isinstance(data, dict) or "status" not in data:
        raise ValueError(t("gate JSON missing 'status' field",
                           "gate JSON 缺少 'status' 字段"))
    return data


def render_checks(gate: dict) -> str:
    lines = []
    for c in gate.get("checks", []):
        lvl = c.get("level", "?")
        icon = {"green": "🟢", "yellow": "🟡", "red": "🔴"}.get(lvl, "⚪")
        lines.append(f"  {icon} [{c.get('item', '?')}] {c.get('message', '')}")
    return "\n".join(lines)


def main(argv=None) -> int:
    global _ZH
    ap = argparse.ArgumentParser(description="meta-analysis human sign-off gate (R red-light consumer)")
    ap.add_argument("input", help="gate JSON file, or '-' for stdin")
    ap.add_argument("--yes", action="store_true", help="human sign-off: override red/yellow block")
    ap.add_argument("--json-out", action="store_true", help="print machine-readable verdict JSON")
    args = ap.parse_args(argv)
    _ZH = is_chinese_os()

    try:
        gate = load_gate(args.input)
    except FileNotFoundError:
        sys.stderr.write(t(f"ERROR: input not found: {args.input}",
                           f"错误：找不到输入文件：{args.input}") + "\n")
        return 3
    except json.JSONDecodeError as e:
        sys.stderr.write(t(f"ERROR: invalid gate JSON: {e}",
                           f"错误：gate JSON 无效：{e}") + "\n")
        return 3
    except ValueError as e:
        sys.stderr.write(t(f"ERROR: {e}", f"错误：{e}") + "\n")
        return 3

    status = gate.get("status", "unknown")
    pooled = gate.get("pooled_presentable", False)
    k = gate.get("k")
    i2 = gate.get("I2")
    meta = (f"k={k}, I2={i2}%" if k is not None else "") if i2 is not None else (f"k={k}" if k is not None else "")

    summary = {
        "green": t("GATE PASS — all checks green.", "门禁通过——全部绿灯。"),
        "yellow": t("GATE WARN — yellow flags; confirm to proceed.",
                    "门禁警告——黄灯；确认后放行。"),
        "red": t("GATE BLOCKED — red light; pooled estimate NOT presented. "
                 "Human sign-off (--yes) required to override.",
                 "门禁阻断——红灯；不呈现合并效应。需人工签字（--yes）方可放行。"),
    }.get(status, t("GATE UNKNOWN", "门禁未知"))

    verdict = {
        "decision": "pass" if (status == "green" or args.yes) else
                    ("warn" if status == "yellow" else "blocked"),
        "status": status,
        "pooled_presentable": bool(pooled),
        "human_sign_off": bool(args.yes),
        "meta": meta,
    }
    exit_code = 0 if (status == "green" or args.yes) else (1 if status == "yellow" else 2)

    if args.json_out:
        print(json.dumps(verdict, ensure_ascii=False, indent=2))
    else:
        icon = {"green": "🟢", "yellow": "🟡", "red": "🔴"}.get(status, "⚪")
        print(f"{icon} {summary} ({meta.strip()})" if meta else f"{icon} {summary}")
        checks_txt = render_checks(gate)
        if checks_txt:
            print(checks_txt)
        if status == "red" and not args.yes:
            print(t("  -> blocked: run with --yes to record human sign-off",
                    "  -> 已阻断：加 --yes 记录人工签字"))
        elif status in ("red", "yellow") and args.yes:
            print(t("  -> human sign-off recorded; override allowed",
                    "  -> 已记录人工签字；放行"))

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
