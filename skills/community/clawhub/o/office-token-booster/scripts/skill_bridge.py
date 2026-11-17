#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""skill_bridge.py — office-token-booster 真实闭环 · 去品牌化

把已有的对话编排层 conversation.handle() 接进**宿主对话平台**的「任务完成事件」，
让「用户完成一次任务」能够**自动建议记账**——而且能带上宿主回报的**真实用量**
（token / 分钟），把「用户自报成本」升级为「实测成本」，形成真实提效闭环。

设计原则（延续三层解耦 + 粘合层 + 触发适配器）：
- 只消费 conversation 暴露的 handle()/classify()/_detect_type()/_parse_numbers()，
  以及 diagnose 的 load_ledger/diagnose；**不改 diagnose / qa / report_engine /
  ledger_agent / conversation 一行**。
- **去品牌化**：本模块不绑定任何具体平台（天禧 / OpenClaw 皆可），
  只认通用的「对话事件」契约，便于直接复用到比赛仓库。
- 纯标准库、无第三方依赖、无网络、无硬编码密钥（满足 OpenClaw/天禧 安全红线）。
- 安全默认：触发流只「建议」，绝不在用户确认前写回账本（沿用 run_long_chain(apply=False) 默认）。
- 触发判定与 conversation.classify 共享同一套完成信号语义，避免两套口径漂移。

宿主技能侧集成示例
----------------------
    from skill_bridge import on_conversation_event
    state = {}
    # 宿主在完成一次办公任务后，把真实用量随事件一并传来
    res = on_conversation_event("ledger.json", {
        "role": "user",
        "text": "我刚生成了周报",
        "cost": {"skill_tokens": 1800, "skill_minutes": 5},  # 宿主回报的真实用量
    }, state)
    if res.triggered:
        show_suggestion(res.suggestion)   # 渲染「建议记账：周报生成 … 确认？」

触发后，用户回复「确认」即由普通对话流 handle("确认", state) 写回，
桥接层本身不碰磁盘。
"""

import argparse
import json
import os
import re
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

# 允许从任意目录运行（与 conversation / diagnose 保持一致的 sibling import）。
sys.path.insert(0, str(Path(__file__).resolve().parent))

from conversation import (                                          # noqa: E402
    classify, handle, _detect_type, _parse_numbers, _REGISTRY, COMPLETION_VERBS)
from diagnose import load_ledger, diagnose                         # noqa: E402


# ─────────────────────────────────────────────────────────────
# 完成信号识别
# ─────────────────────────────────────────────────────────────

# 完成动词复用 conversation.COMPLETION_VERBS（单一事实源，避免两套口径漂移，修复 L3）。
# 这里只判定「是否完成事件」，成本数字是否齐全由 is_completion_event 单独报出。
_COMPLETION_VERBS = COMPLETION_VERBS

# 成本信号：花了/用了/耗时 … token/分钟
_COST_RE = re.compile(r"(花了|用了|耗时|花费|消耗|占)\s*.{0,12}?\s*(token|分钟|分)", re.I)


def is_completion_event(text):
    """判断一句话是否为「任务完成」事件（值得自动建议记账）。

    返回 dict：{is_completion, has_cost, confidence}
      - is_completion : 是否含完成动词
      - has_cost      : 是否含 token/分钟 成本数字
      - confidence    : high（动词+成本）/ medium（仅动词）/ low（无动词）
    """
    t = (text or "").strip()
    has_verb = bool(re.search(_COMPLETION_VERBS, t))
    has_cost = bool(_COST_RE.search(t))
    if has_verb and has_cost:
        confidence = "high"
    elif has_verb:
        confidence = "medium"
    else:
        confidence = "low"
    return {
        "is_completion": has_verb,
        "has_cost": has_cost,
        "confidence": confidence,
    }


def _lenient_type(text, diag):
    """对话层 _detect_type 认不出类型时（如缺成本数字、或别名大小写不符），
    用类型字典做大小写不敏感兜底匹配，提高触发流的类型召回。

    返回 (type, is_new)，与 _detect_type 同语义。
    """
    tt, is_new = _detect_type(text, diag)
    if tt:
        return tt, is_new
    # 兜底：大小写不敏感地在账本已知类型 / 类型字典里找
    # 类型字典由 conversation._REGISTRY 统一加载（单一事实源，避免重复实现文件定位）。
    low = text.lower()
    for k in [d["task_type"] for d in diag.by_type]:
        if k and k.lower() in low:
            return k, False
    registry = _REGISTRY or {}
    for std, aliases in registry.items():
        if std and std.lower() in low:
            return std, False
        for a in (aliases or []):
            if a and a.lower() in low:
                return std, False
    return None, False


def _coerce_int(v):
    """把宿主回报的数值安全转 int（修复 H3）。

    宿主事件输入不可全信：若 skill_tokens/skill_minutes 是字符串或畸形值，
    统一降级为 None（视为『无成本』），绝不抛出 ValueError 导致整个触发流崩溃。
    """
    if v is None:
        return None
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return None


# ─────────────────────────────────────────────────────────────
# 触发结果（结构化，便于 Skill/UI 渲染）
# ─────────────────────────────────────────────────────────────

@dataclass
class TriggerResult:
    """on_conversation_event 的结构化返回。Skill/UI 据此渲染建议卡片。"""
    triggered: bool = False
    intent: str = "unknown"
    suggestion: str = ""
    pending_type: str = None
    confidence: str = "low"
    # 成本来源：event=宿主回报真实用量 / text=自然语言解析 / none=无成本
    # 用于 Skill/UI 标注「本技能实测消耗」还是「估算」，也便于测试断言真实闭环。
    cost_source: str = "none"
    # True=本事件已被触发流接管，普通对话可跳过；False=未触发，调用方应交普通对话处理
    passthrough: bool = True


# ─────────────────────────────────────────────────────────────
# 主入口：处理一个对话事件
# ─────────────────────────────────────────────────────────────

def on_conversation_event(ledger_path, event, state, cost_provider=None):
    """处理一个宿主对话事件，必要时自动建议记账。

    参数
    ----
    ledger_path : 账本 JSON 路径
    event       : dict，至少含 "text"（用户的自然语言）。可含：
                    - "role"（默认 "user"）
                    - "cost"（dict，宿主回报的真实用量：
                             {"skill_tokens": N, "skill_minutes": M}）
                    - "completed"（bool，宿主显式声明「任务已完成」的结构化事件，
                             优先级高于文本里的完成动词）
    state       : 调用方维护的 dict（与 handle 共用，含可选 "pending"）
    cost_provider : 可选 HostCostProvider。当 event 未带 cost 时，
                    用宿主真实用量补全（仅作兜底，不覆盖宿主显式回报的实测值）。
                    不传则保持既有行为，零改动。

    返回
    ----
    TriggerResult
      - 命中完成信号（high/medium）→ triggered=True，suggestion 由 conversation.handle() 生成，
        内部已把待记账条目暂存到 state["pending"]，等待用户「确认」。
        若 event 携带真实用量（cost），则采用实测成本而非文本解析，cost_source="event"。
      - 未命中（low，纯闲聊/问答）→ triggered=False，调用方可把这句话交给普通对话。
    """
    text = (event or {}).get("text", "")
    if not text.strip():
        return TriggerResult()

    # 成本来源：优先取宿主回报的真实用量（修复 H3：先强制校验类型，畸形值降级为 None）
    ev_cost = (event or {}).get("cost") or {}
    ev_tokens = _coerce_int(ev_cost.get("skill_tokens"))
    ev_minutes = _coerce_int(ev_cost.get("skill_minutes"))

    # 事件未带 cost 但提供了 cost_provider → 用宿主真实用量兜底补全。
    # 仅当事件自身没有成本数字时才回退，绝不覆盖宿主显式回报的实测值。
    if (ev_tokens is None and ev_minutes is None) and cost_provider is not None:
        try:
            _recent = cost_provider.fetch_recent(1)
        except Exception:
            _recent = []
        if _recent:
            _rec = _recent[0]
            ev_tokens = _rec.skill_tokens or None
            ev_minutes = _rec.skill_minutes or None

    sig = is_completion_event(text)
    # 宿主可显式声明已完成（结构化事件），优先级高于文本动词
    if (event or {}).get("completed") is True:
        sig = {
            "is_completion": True,
            "has_cost": bool(ev_tokens is not None or ev_minutes is not None),
            "confidence": "high" if (ev_tokens is not None or ev_minutes is not None) else "medium",
        }

    # 只在「明确的任务完成」信号下自动建议；纯闲聊/问答不触发，避免打扰
    if not sig["is_completion"]:
        return TriggerResult(confidence=sig["confidence"])

    # 完成信号命中：归一化为标准记账句，交给 record 分支得到标准建议
    tasks = load_ledger(ledger_path)
    diag = diagnose(tasks)
    ttype, _is_new = _lenient_type(text, diag)

    if not ttype:
        # 认不出类型：
        #  - 中信心（仅动词、无成本）：多半是普通对话里顺口提了句「写完了」，
        #    不应强行接管，交还给普通对话处理（passthrough=True，修复 M5）。
        #  - 高信心（动词+成本）：仍给一次对话兜底（追问类型），但用独立 state，
        #    不污染调用方的待确认状态（修复 M3 串味）。
        if sig["confidence"] == "medium":
            return TriggerResult(confidence=sig["confidence"], passthrough=True)
        intent = classify(text)
        suggestion = handle(ledger_path, text, {})
        return TriggerResult(
            triggered=True, intent=intent, suggestion=suggestion,
            pending_type=None, confidence=sig["confidence"], passthrough=False)

    # 成本：宿主真实用量 > 文本解析；记录来源便于 Skill/UI 标注「实测 vs 估算」
    text_tokens, text_minutes = _parse_numbers(text)
    tokens = ev_tokens if ev_tokens is not None else text_tokens
    minutes = ev_minutes if ev_minutes is not None else text_minutes
    tok_from_event = ev_tokens is not None
    min_from_event = ev_minutes is not None
    if tok_from_event and min_from_event:
        cost_source = "event"                       # 全部来自宿主实测
    elif tok_from_event or min_from_event:
        cost_source = "mixed"                       # 部分实测、部分文本估算（修复 M4 误标）
    elif text_tokens is not None or text_minutes is not None:
        cost_source = "text"
    else:
        cost_source = "none"

    norm = f"记一笔 {ttype}"
    if tokens is not None:
        norm += f" 花了{tokens} token"
    if minutes is not None:
        norm += f" {minutes}分钟"

    intent = classify(norm)            # 归一化后必为 record
    suggestion = handle(ledger_path, norm, state)
    # 直接用已识别的类型，不依赖 state 副作用读取（修复 M3 串味）
    pending_type = ttype
    return TriggerResult(
        triggered=True, intent=intent, suggestion=suggestion,
        pending_type=pending_type, confidence=sig["confidence"],
        cost_source=cost_source, passthrough=False)


# ─────────────────────────────────────────────────────────────
# CLI（--demo 跑通几个事件，便于人工验证触发流）
# ─────────────────────────────────────────────────────────────

def main():
    parser = argparse_init()
    args = parser.parse_args()

    # --demo：临时账本，不污染用户数据
    if args.demo:
        sample = {"tasks": [
            {"date": "2026-08-01", "type": "周报生成", "baseline_tokens": 5000,
             "skill_tokens": 1800, "baseline_minutes": 20, "skill_minutes": 5, "note": "周报"},
            {"date": "2026-08-02", "type": "文档撰写", "baseline_tokens": 8000,
             "skill_tokens": 3000, "baseline_minutes": 30, "skill_minutes": 12, "note": "方案"},
        ]}
        tmp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
        json.dump(sample, tmp, ensure_ascii=False)
        tmp.close()
        ledger = tmp.name
    else:
        ledger = args.ledger
        if not ledger:
            print("[错误] 请提供账本路径或加 --demo：python skill_bridge.py <ledger.json> --demo",
                  file=sys.stderr)
            return 2
        try:
            load_ledger(ledger)
        except (FileNotFoundError, ValueError, json.JSONDecodeError) as e:
            print(f"[错误] {e}", file=sys.stderr)
            return 2

    demos = [
        ("用户说：我刚生成了周报，花了1800 token 5分钟（高信心，文本成本，应触发）",
         {"role": "user", "text": "我刚生成了周报，花了1800 token 5分钟"}),
        ("宿主事件：任务完成 + 真实用量（无文本数字，应触发并采用实测成本）",
         {"role": "user", "text": "我刚生成了周报",
          "cost": {"skill_tokens": 1800, "skill_minutes": 5}, "completed": True}),
        ("用户说：写完了那份PPT（中信心，无成本，应触发并经字典兜底识别类型）",
         {"role": "user", "text": "写完了那份PPT"}),
        ("用户说：今天天气不错（非完成事件，不应触发）",
         {"role": "user", "text": "今天天气不错"}),
    ]
    state = {}
    print("=== 真实闭环演示（去品牌化）===")
    for title, ev in demos:
        print("\n-- " + title)
        res = on_conversation_event(ledger, ev, state)
        if res.triggered:
            print(f"[触发] intent={res.intent} pending={res.pending_type} "
                  f"信心={res.confidence} 成本来源={res.cost_source}")
            print("    建议: " + res.suggestion.replace("\n", "\n          "))
        else:
            print(f"[不触发] 信心={res.confidence}（交给普通对话处理）")

    if args.demo:
        os.unlink(ledger)
    return 0


def argparse_init():
    p = argparse.ArgumentParser(
        description="办公室提效 · 真实闭环（接宿主对话事件、携带真实用量自动建议记账）")
    p.add_argument("ledger", nargs="?", help="账本 JSON 路径")
    p.add_argument("--ledger", dest="ledger", help="账本 JSON 路径（同位置参数）")
    p.add_argument("--demo", action="store_true",
                  help="用内置样本账本跑几个事件，演示触发流（不改动你的文件）")
    return p


if __name__ == "__main__":
    sys.exit(main())
