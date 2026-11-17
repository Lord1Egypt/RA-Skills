#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
企业应急响应指导 Skill - 卡住/打转检测器（Loop Detector）

输出：
- 降噪后的会话摘要（重复动作/重复尝试/无进展时长）
- 纠偏建议
- Advisor 纠偏提示词模板（用于重写计划）
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


ROOT = Path(__file__).resolve().parents[1]
SESSION_PATH = ROOT / "memory" / "working" / "current_session.json"


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def parse_iso(ts: Optional[str]) -> Optional[datetime]:
    if not ts:
        return None
    s = ts.strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(s)
    except Exception:
        return None


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def norm(s: str) -> str:
    s = (s or "").strip().lower()
    s = " ".join(s.split())
    return s[:180]


def pick_last_ts(cs: Dict[str, Any]) -> Optional[datetime]:
    candidates: List[datetime] = []
    for k in ("last_progress_time", "start_time"):
        t = parse_iso(cs.get(k))
        if t:
            candidates.append(t)
    for arr_key in ("notes", "attempts", "actions", "evidence", "timeline", "next_steps"):
        arr = cs.get(arr_key) or []
        if not isinstance(arr, list):
            continue
        for item in arr[-20:]:
            if isinstance(item, dict):
                t = parse_iso(item.get("ts") or item.get("timestamp"))
                if t:
                    candidates.append(t)
    return max(candidates) if candidates else None


def summarize_repeats(cs: Dict[str, Any]) -> Dict[str, Any]:
    attempts = cs.get("attempts") or []
    actions = cs.get("actions") or []

    att = []
    for a in attempts:
        if isinstance(a, dict):
            att.append(norm(a.get("text", "")))
        elif isinstance(a, str):
            att.append(norm(a))

    act = []
    for a in actions:
        if not isinstance(a, dict):
            continue
        key = f"{a.get('phase') or ''}|{a.get('action') or ''}|{a.get('verdict') or ''}|{a.get('reason') or ''}|{a.get('target') or ''}"
        key = norm(key)
        if key and key != "||||":
            act.append(key)

    att_c = Counter([x for x in att if x])
    act_c = Counter([x for x in act if x])

    return {
        "attempt_total": len(att),
        "attempt_unique": len(att_c),
        "attempt_top_repeats": att_c.most_common(5),
        "action_total": len(act),
        "action_unique": len(act_c),
        "action_top_repeats": act_c.most_common(5),
    }


def build_advisor_prompt(cs: Dict[str, Any], repeats: Dict[str, Any], idle_minutes: int) -> str:
    return (
        "你是企业应急响应的 Advisor（纠偏顾问）。\n"
        "目标：当处置出现打转/无进展时，基于现有证据重写计划（3-6步），并给出每步验证点（VBR）与风险提示。\n"
        "要求：\n"
        "- 先输出【卡住原因】（最多3条）\n"
        "- 再输出【信息缺口】（需要补什么证据/日志/取证）\n"
        "- 再输出【替代路线】（至少2条，优先低影响/先取证后处置）\n"
        "- 最后输出【新的TodoList】（3-6步，每步含验证点）\n"
        "\n"
        f"事件: {cs.get('incident_name')}\n"
        f"范围(scope): {cs.get('scope')}\n"
        f"规则(rules): {cs.get('rules')}\n"
        f"当前阶段: {cs.get('phase')}\n"
        f"最近无进展时长(分钟): {idle_minutes}\n"
        f"attempt_total={repeats.get('attempt_total')} unique={repeats.get('attempt_unique')}\n"
        f"action_total={repeats.get('action_total')} unique={repeats.get('action_unique')}\n"
        f"高频重复尝试Top3: {repeats.get('attempt_top_repeats', [])[:3]}\n"
        f"高频重复动作Top3: {repeats.get('action_top_repeats', [])[:3]}\n"
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="IR loop detector (stuck / repetition analyzer)")
    ap.add_argument("--session", default=str(SESSION_PATH), help="current_session.json 路径")
    ap.add_argument("--idle-minutes", type=int, default=30, help="超过多少分钟无新进展认为可能卡住（默认30）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args()

    session = load_json(Path(args.session), {"current_session": {}})
    cs: Dict[str, Any] = session.get("current_session") or {}

    last_ts = pick_last_ts(cs)
    idle: Optional[int] = None
    if last_ts:
        idle = int((now_utc() - last_ts).total_seconds() // 60)

    repeats = summarize_repeats(cs)

    stuck = False
    reasons: List[str] = []
    if idle is not None and idle >= args.idle_minutes:
        stuck = True
        reasons.append(f"最近 {idle} 分钟未记录到新进展（notes/attempts/actions/evidence/timeline）")
    if repeats["attempt_total"] >= 8 and repeats["attempt_unique"] <= max(2, repeats["attempt_total"] // 3):
        stuck = True
        reasons.append("尝试记录高度重复（unique/total 过低）")
    if repeats["action_total"] >= 6 and repeats["action_unique"] <= max(2, repeats["action_total"] // 3):
        stuck = True
        reasons.append("结构化动作高度重复（unique/total 过低）")

    suggestions = [
        "优先补齐可验证的新事实：关键日志片段、时间线锚点、进程/网络连接/文件落地证据（VBR）",
        "对处置动作设置“停止条件”：避免在未取证前破坏现场（先隔离/快照/导出）",
        "必要时触发 HITL：隔离主机/封禁账号/下线服务等会影响业务的动作必须先确认",
    ]

    advisor_prompt = build_advisor_prompt(cs, repeats, idle or 0)

    out_obj = {
        "stuck": stuck,
        "idle_minutes": idle,
        "phase": cs.get("phase"),
        "incident_name": cs.get("incident_name"),
        "scope": cs.get("scope"),
        "repeats": repeats,
        "reasons": reasons,
        "suggestions": suggestions,
        "advisor_prompt": advisor_prompt,
    }

    if args.json:
        print(json.dumps(out_obj, ensure_ascii=False, indent=2))
        return 0

    print("📌 Loop Detector（应急响应：卡住/打转检测）")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"- 事件: {out_obj['incident_name']}")
    print(f"- 范围: {out_obj['scope']}")
    print(f"- 阶段: {out_obj['phase']}")
    print(f"- idle_minutes: {out_obj['idle_minutes']}")
    print(f"- 是否疑似卡住: {'是' if stuck else '否'}")
    if reasons:
        print("\n【判定原因】")
        for r in reasons:
            print(f"- {r}")
    print("\n【建议动作】")
    for s in suggestions:
        print(f"- {s}")
    print("\n【Advisor 提示词模板】")
    print(advisor_prompt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

