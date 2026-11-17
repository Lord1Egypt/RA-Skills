#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""host_hook.py — office-token-booster 宿主钩子示例（平台无关）

演示宿主对话平台（天禧 / OpenClaw）如何把「任务完成」事件接进
skill_bridge.on_conversation_event，让提效记账形成**真实闭环**：

- 宿主在完成一次办公任务后，把真实用量（token / 分钟）随事件一起传来；
- skill_bridge 据此自动建议记账，用户「确认」即写回账本。

本文件是「平台无关」的示例适配器：

- 不 import 任何平台 SDK、不发网络请求、不硬编码密钥（满足 OpenClaw/天禧 安全红线）；
- 宿主-specific 的 glue 由平台侧实现，只需把完成事件归一化成
  build_completion_event(...) 返回的 dict 形态即可。

真实成本来自宿主平台的用量回报，本技能只负责「采集建议 + 量化」，
不伪造、不估算技能的消耗。
"""

import argparse
import json
import sys
import tempfile
from pathlib import Path

# 允许从任意目录运行（与 skill_bridge / conversation 保持一致的 sibling import）。
sys.path.insert(0, str(Path(__file__).resolve().parent))

from skill_bridge import on_conversation_event  # noqa: E402
from executor import resolve_exec_type, propose_ledger  # noqa: E402  # 方向 B 闭环


def build_completion_event(task_text, *, skill_tokens=None, skill_minutes=None,
                            completed=None):
    """把宿主的「任务完成」归一化成 skill_bridge 认得的通用事件 dict。

    参数
    ----
    task_text    : 用户/宿主侧的完成描述（如「我刚生成了周报」）
    skill_tokens : 宿主回报的本技能真实 token 消耗（可选）
    skill_minutes: 宿主回报的本技能真实耗时（可选）
    completed    : 宿主显式声明「已完成」的结构化标志（可选）

    返回
    ----
    dict，含 "role"/"text"，可选 "cost"/"completed"
    """
    ev = {"role": "user", "text": task_text}
    if skill_tokens is not None or skill_minutes is not None:
        ev["cost"] = {}
        if skill_tokens is not None:
            ev["cost"]["skill_tokens"] = int(skill_tokens)
        if skill_minutes is not None:
            ev["cost"]["skill_minutes"] = int(skill_minutes)
    if completed is not None:
        ev["completed"] = bool(completed)
    return ev


def on_task_completed(ledger_path, event, state):
    """宿主钩子主入口：任务完成后调用，返回 (TriggerResult, 建议文本)。

    宿主侧只需：任务完成 → 取真实用量 → build_completion_event → on_task_completed。
    本函数本身不碰磁盘；是否写回由用户「确认」触发（沿用 skill_bridge 安全默认）。
    """
    res = on_conversation_event(ledger_path, event, state)
    return res, (res.suggestion if res.triggered else "")


def on_executor_completed(ledger_path, task_type, event, *, apply=False):
    """方向 B 闭环：宿主用 executor 跑完一个办公任务后，把带真实用量的完成事件
    直接记回 ledger——复用 build_completion_event 的 cost 形态。

    参数
    ----
    ledger_path : 账本 JSON 路径
    task_type   : 任务类型（如「周报生成」，会先归一化）
    event       : 完成事件 dict，可含 "cost"（{"skill_tokens":N,"skill_minutes":M}）
                  与 "text"（用于备注）；与 executor.propose_ledger 同源护栏。
    apply       : True 才真正写回（默认 dry-run 预览，不污染账本）

    返回
    ----
    ledger_agent.run_long_chain 的结果 dict；ledger_agent 不可用时返回 None。
    """
    std_type = resolve_exec_type(task_type) or task_type
    return propose_ledger(
        ledger_path, std_type,
        cost=(event or {}).get("cost"),
        note=(event or {}).get("text") or f"执行引擎：{std_type}",
        apply=apply,
    )


def main():
    parser = argparse.ArgumentParser(
        description="办公室提效 · 宿主钩子示例（演示真实用量自动记账）")
    parser.add_argument("ledger", nargs="?", help="账本 JSON 路径")
    parser.add_argument("--ledger", dest="ledger", help="账本 JSON 路径（同位置参数）")
    parser.add_argument("--demo", action="store_true",
                        help="用内置样本账本演示宿主完成事件如何触发记账建议")
    parser.add_argument("--demo-exec", action="store_true",
                        help="方向 B 演示：executor 跑完周报 → 带真实用量事件自动记回账本（dry-run）")
    args = parser.parse_args()

    if args.demo_exec:
        return _demo_executor_completed()

    if args.demo:
        sample = {"tasks": [
            {"date": "2026-08-01", "type": "周报生成", "baseline_tokens": 5000,
             "skill_tokens": 1800, "baseline_minutes": 20, "skill_minutes": 5, "note": "周报"},
        ]}
        tmp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
        json.dump(sample, tmp, ensure_ascii=False)
        tmp.close()
        ledger = tmp.name
    else:
        ledger = args.ledger
        if not ledger:
            print("[错误] 请提供账本路径或加 --demo：python host_hook.py <ledger.json> --demo",
                  file=sys.stderr)
            return 2
        try:
            from diagnose import load_ledger
            load_ledger(ledger)
        except (FileNotFoundError, ValueError, json.JSONDecodeError) as e:
            print(f"[错误] {e}", file=sys.stderr)
            return 2

    events = [
        ("宿主完成『周报生成』并回报真实用量 1800 token / 5 分钟",
         build_completion_event("我刚生成了周报", skill_tokens=1800, skill_minutes=5,
                                 completed=True)),
        ("宿主完成『PPT制作』，仅声明 completed，用量由后续填充",
         build_completion_event("写完了那份PPT", completed=True)),
    ]
    state = {}
    print("=== 宿主钩子演示 ===")
    for title, ev in events:
        print("\n-- " + title)
        res, sug = on_task_completed(ledger, ev, state)
        if res.triggered:
            print(f"[触发] 类型={res.pending_type} 信心={res.confidence} "
                  f"成本来源={res.cost_source}")
            print("    建议: " + sug.replace("\n", "\n          "))
        else:
            print(f"[不触发] 信心={res.confidence}")

    if args.demo:
        import os
        os.unlink(ledger)
    return 0


def _demo_executor_completed() -> int:
    """方向 B 闭环演示：executor 跑周报 → 带真实用量事件自动记回（dry-run 不写盘）。"""
    from executor import execute

    sample_weekly = (
        "本周概览：方向 B 执行引擎落地\n"
        "完成 executor 骨架与 5 个模块\n"
        "风险：回归覆盖待补充\n"
        "下周计划：补 docx/xlsx 导出"
    )
    md, meta = execute("周报生成", sample_weekly)
    print("=== 方向 B：executor 生成周报交付物 ===")
    print(md)
    print(f"[元信息] 字符数={meta['chars']}")

    # 宿主回报的完成事件（含真实用量），复用 build_completion_event 形态
    event = build_completion_event(
        "我刚用执行引擎生成了周报", skill_tokens=1800, skill_minutes=5, completed=True)

    ledger = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
    json.dump({"tasks": []}, ledger, ensure_ascii=False)
    ledger.close()
    try:
        print("\n=== 方向 B：executor 完成 → 自动记回账本（dry-run）===")
        res = on_executor_completed(ledger.name, "周报生成", event, apply=False)
        if res is None:
            print("[记账] ledger_agent 不可用，跳过。")
        elif res.get("blocked"):
            print(f"[记账] 已拦截：{res.get('block_reason') or res.get('reason')}（请补填 baseline 后确认写回）")
        else:
            entry = res.get("entry", {})
            print(f"[记账] 预览：类型={res.get('pending_type') or entry.get('type')} "
                  f"skill_tokens={entry.get('skill_tokens')} "
                  f"skill_minutes={entry.get('skill_minutes')}（确认后加 --confirm 写回）")
    finally:
        import os
        os.unlink(ledger.name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
