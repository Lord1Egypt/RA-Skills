#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
企业应急响应指导 Skill - 复盘/候选经验生成器（防污染）

读取 WAL（memory/working/current_session.json），生成：
- episodic 情景快照（可追溯）
- candidates 候选经验（待审核）
- evolution report 草稿（便于审阅）

只生成候选，不自动合并到主库。
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


ROOT = Path(__file__).resolve().parents[1]
SESSION_PATH = ROOT / "memory" / "working" / "current_session.json"
EP_DIR = ROOT / "memory" / "episodic" / "2026"
CAND_PATH = ROOT / "memory" / "semantic" / "ir-patterns.candidates.json"
EVOL_DIR = ROOT / "memory" / "evolution-reports"


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def now_iso() -> str:
    return now_utc().isoformat()


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def take_text(arr: Any, key: str, n: int) -> List[str]:
    out: List[str] = []
    if not isinstance(arr, list):
        return out
    for x in arr[-n:]:
        if isinstance(x, dict):
            v = x.get(key) or x.get("path") or x.get("event") or ""
            if v:
                out.append(str(v))
        elif isinstance(x, str):
            out.append(x)
    return out


def build_candidates(cs: Dict[str, Any], limit: int = 5) -> List[Dict[str, Any]]:
    """
    候选经验的默认形态：把本次事件中“可复用的处置模式”模板化。

    启发式信号：
    - actions 中 verdict=pass 的 verify/contain/eradicate/recover/report
    - timeline / ioc 作为支撑证据
    """
    actions = cs.get("actions") or []
    if not isinstance(actions, list):
        actions = []

    signals: List[Dict[str, Any]] = []
    for a in actions:
        if not isinstance(a, dict):
            continue
        verdict = (a.get("verdict") or "").lower()
        phase = (a.get("phase") or "").lower()
        action = (a.get("action") or "").lower()
        if verdict == "pass" and (phase in ("triage", "contain", "eradicate", "recover", "report") or action in ("verify", "contain", "eradicate", "recover", "report")):
            signals.append(a)

    evidence_paths = [x for x in take_text(cs.get("evidence") or [], "path", 20) if x]
    ioc_snapshot = cs.get("iocs") or {}

    ts = now_utc().strftime("%Y%m%d_%H%M%S")
    out: List[Dict[str, Any]] = []

    def new_id(i: int) -> str:
        return f"cand-{ts}-{i:02d}"

    idx = 0
    for s in signals[:limit]:
        idx += 1
        out.append(
            {
                "id": new_id(idx),
                "created_at": now_iso(),
                "source": {
                    "incident_name": cs.get("incident_name"),
                    "scope": cs.get("scope"),
                    "rules": cs.get("rules"),
                },
                "title": f"（待命名）{s.get('phase')}/{s.get('action')} 的可复用处置模式",
                "one_liner": "（待补全）一句话模式：在什么信号下，做什么最小验证/处置，得到什么可复现证据。",
                "category": "IR-General",
                "pattern": {
                    "phase": s.get("phase"),
                    "signal_action": s.get("action"),
                    "signal_reason": s.get("reason"),
                    "target_hint": s.get("target"),
                },
                "vbr": {
                    "minimal_steps": [
                        "（待补全）最小验证步骤 1（日志/流量/主机取证）",
                        "（待补全）最小验证步骤 2（差异/证据锚点）"
                    ],
                    "expected_evidence": [
                        "（待补全）证据要求：日志片段/截图/pcap/导出文件"
                    ]
                },
                "containment_play": [
                    "（待补全）隔离/封禁/下线的最小影响做法（含回滚）"
                ],
                "counterexamples": [
                    "（待补全）反例/误判来源（时间漂移/日志缺失/噪声告警）"
                ],
                "fix_suggestion": [
                    "（待补全）加固/修复建议（最小改动优先）"
                ],
                "iocs_snapshot": ioc_snapshot,
                "evidence_paths": evidence_paths[:8],
                "review": {"status": "candidate", "reviewer": None, "reviewed_at": None, "decision": None}
            }
        )

    if not out:
        out.append(
            {
                "id": new_id(1),
                "created_at": now_iso(),
                "source": {
                    "incident_name": cs.get("incident_name"),
                    "scope": cs.get("scope"),
                    "rules": cs.get("rules"),
                },
                "title": "（待命名）本次事件通用经验模板",
                "one_liner": "（待补全）一句话经验：我如何从告警→证据→处置→复盘形成闭环。",
                "category": "IR-General",
                "pattern": {"phase": cs.get("phase"), "signal_action": None, "signal_reason": None, "target_hint": None},
                "vbr": {"minimal_steps": ["（待补全）步骤1", "（待补全）步骤2"], "expected_evidence": ["（待补全）证据要求"]},
                "containment_play": ["（待补全）最小影响隔离/封禁策略（含回滚）"],
                "counterexamples": ["（待补全）反例/不适用场景"],
                "fix_suggestion": ["（待补全）修复建议"],
                "iocs_snapshot": ioc_snapshot,
                "evidence_paths": evidence_paths[:8],
                "review": {"status": "candidate", "reviewer": None, "reviewed_at": None, "decision": None}
            }
        )

    return out


def write_evolution_report(cs: Dict[str, Any], ep_path: Path, candidates: List[Dict[str, Any]]) -> Path:
    date_str = now_utc().strftime("%Y-%m-%d")
    out_path = EVOL_DIR / f"{date_str}.md"
    EVOL_DIR.mkdir(parents=True, exist_ok=True)

    notes = take_text(cs.get("notes") or [], "text", 10)
    evidence = take_text(cs.get("evidence") or [], "path", 12)
    timeline = take_text(cs.get("timeline") or [], "event", 12)

    lines: List[str] = []
    lines.append(f"# 应急响应 - 进化报告草稿（{date_str}）\n\n")
    lines.append("## 1) 基本信息\n")
    lines.append(f"- 事件名称：{cs.get('incident_name')}\n")
    lines.append(f"- 范围(scope)：{cs.get('scope')}\n")
    lines.append(f"- 规则(rules)：{cs.get('rules')}\n")
    lines.append(f"- 情景快照：`{ep_path}`\n\n")

    lines.append("## 2) 降噪摘要（最近关键笔记）\n")
    lines.extend([f"- {x}\n" for x in notes] or ["-（无）\n"])
    lines.append("\n## 3) 时间线锚点（最近）\n")
    lines.extend([f"- {x}\n" for x in timeline] or ["-（无）\n"])
    lines.append("\n## 4) 关键证据（Evidence）\n")
    lines.extend([f"- {x}\n" for x in evidence] or ["-（无）\n"])

    lines.append("\n## 5) 候选经验（待审核，宁缺毋滥）\n")
    for c in candidates:
        lines.append(f"\n### {c.get('id')} - {c.get('title')}\n")
        lines.append(f"- 一句话：{c.get('one_liner')}\n")
        lines.append("- 最小验证（VBR）：\n")
        for s in (c.get("vbr") or {}).get("minimal_steps", [])[:6]:
            lines.append(f"  - {s}\n")
        lines.append("- 反例/不适用：\n")
        for s in c.get("counterexamples", [])[:4]:
            lines.append(f"  - {s}\n")
        lines.append("- 修复建议：\n")
        for s in c.get("fix_suggestion", [])[:4]:
            lines.append(f"  - {s}\n")
        lines.append("- 合并建议：未审核（需负责人确认后执行 apply_updates_ir.py）\n")

    out_path.write_text("".join(lines), encoding="utf-8")
    return out_path


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate IR evolution candidates (no auto-merge)")
    ap.add_argument("--session", default=str(SESSION_PATH), help="current_session.json 路径")
    ap.add_argument("--limit", type=int, default=5, help="候选经验最多条数（默认5）")
    args = ap.parse_args()

    session = load_json(Path(args.session), {"current_session": {}})
    cs: Dict[str, Any] = session.get("current_session") or {}

    # episodic 快照
    ts = now_utc().strftime("%Y%m%d_%H%M%S")
    EP_DIR.mkdir(parents=True, exist_ok=True)
    ep_path = EP_DIR / f"ep-ir-{ts}.json"
    save_json(ep_path, {"ts": now_iso(), "session": cs})

    candidates = build_candidates(cs, limit=max(1, args.limit))
    cand_obj = load_json(CAND_PATH, {"meta": {}, "candidates": []})
    cand_obj["meta"] = {"name": "ir-patterns.candidates", "generated_at": now_iso(), "source": "retrospect_ir.py"}
    cand_obj["candidates"] = candidates
    save_json(CAND_PATH, cand_obj)

    report_path = write_evolution_report(cs, ep_path, candidates)

    print(f"[ok] episodic: {ep_path}")
    print(f"[ok] candidates: {CAND_PATH}")
    print(f"[ok] evolution report: {report_path}")
    print("\n下一步（人工审核后合并）：")
    print("  python3 scripts/apply_updates_ir.py --list")
    print("  python3 scripts/apply_updates_ir.py --ids cand-... cand-... --reviewer \"负责人\"")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

