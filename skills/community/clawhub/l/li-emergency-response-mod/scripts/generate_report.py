#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
企业应急响应指导 Skill - 报告生成器（Markdown）

从 memory/working/current_session.json 生成一份“可交付、可审计、可复盘”的应急响应报告草稿。
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parents[1]
SESSION_PATH = ROOT / "memory" / "working" / "current_session.json"
REPORT_TPL = ROOT / "templates" / "report_template.md"
TIMELINE_TPL = ROOT / "templates" / "timeline_template.md"


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def fmt_list(items: List[str]) -> str:
    if not items:
        return "-（无）"
    return "\n".join([f"- {x}" for x in items])


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


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate IR report (markdown)")
    ap.add_argument("--session", default=str(SESSION_PATH), help="current_session.json 路径")
    ap.add_argument("--out", default=str(ROOT / "reports" / "ir-report.md"), help="输出报告路径")
    args = ap.parse_args()

    session = load_json(Path(args.session), {"current_session": {}})
    cs: Dict[str, Any] = session.get("current_session") or {}

    tpl = REPORT_TPL.read_text(encoding="utf-8") if REPORT_TPL.exists() else ""
    timeline_tpl = TIMELINE_TPL.read_text(encoding="utf-8") if TIMELINE_TPL.exists() else ""

    # 降噪：只取最近 N 条
    notes = take_text(cs.get("notes") or [], "text", 12)
    evidence = take_text(cs.get("evidence") or [], "path", 20)
    artifacts = take_text(cs.get("artifacts") or [], "path", 20)
    actions = cs.get("actions") or []
    timeline = take_text(cs.get("timeline") or [], "event", 20)
    next_steps = take_text(cs.get("next_steps") or [], "text", 10)
    containment = take_text(cs.get("containment") or [], "text", 20)
    eradication = take_text(cs.get("eradication") or [], "text", 20)
    recovery = take_text(cs.get("recovery") or [], "text", 20)
    lessons = take_text(cs.get("lessons_learned") or [], "text", 20)

    def dump_actions(arr: Any, n: int = 12) -> List[str]:
        if not isinstance(arr, list):
            return []
        return [json.dumps(x, ensure_ascii=False) for x in arr[-n:] if isinstance(x, dict)]

    def dump_iocs(iocs: Any) -> str:
        if not isinstance(iocs, dict):
            return "-（无）"
        lines = []
        for k in ("ip", "domain", "url", "hash", "process", "file", "registry", "user"):
            vals = iocs.get(k) or []
            if not vals:
                continue
            items = []
            for v in vals[-10:]:
                if isinstance(v, dict):
                    items.append(v.get("value"))
                else:
                    items.append(str(v))
            items = [x for x in items if x]
            if items:
                lines.append(f"- {k}: " + ", ".join(items[:10]))
        return "\n".join(lines) if lines else "-（无）"

    report = tpl
    report = report.replace("{{INCIDENT_NAME}}", str(cs.get("incident_name") or "（未填写）"))
    report = report.replace("{{DATE}}", datetime.now().strftime("%Y-%m-%d"))
    report = report.replace("{{SCOPE}}", str(cs.get("scope") or "（未填写）"))
    report = report.replace("{{RULES}}", str(cs.get("rules") or "（未填写）"))
    report = report.replace("{{SEVERITY}}", str(cs.get("severity") or "（未填写）"))
    report = report.replace("{{MODE}}", str(cs.get("mode") or "production"))
    report = report.replace("{{TIMEZONE}}", str(cs.get("timezone") or "（未填写）"))
    report = report.replace("{{SOURCES}}", "、".join(cs.get("sources") or []) if cs.get("sources") else "（未填写）")
    report = report.replace("{{STAKEHOLDERS}}", "、".join(cs.get("stakeholders") or []) if cs.get("stakeholders") else "（未填写）")
    report = report.replace("{{ASSETS}}", "、".join(cs.get("assets") or []) if cs.get("assets") else "（未填写）")
    report = report.replace("{{SUMMARY_NOTES}}", fmt_list(notes))
    report = report.replace("{{IOCS}}", dump_iocs(cs.get("iocs")))
    report = report.replace("{{FLAGS}}", fmt_list(take_text(cs.get("flags") or [], "text", 20)))
    report = report.replace("{{EVIDENCE}}", fmt_list(evidence))
    report = report.replace("{{ARTIFACTS}}", fmt_list(artifacts))
    report = report.replace("{{ACTIONS}}", fmt_list(dump_actions(actions)))
    report = report.replace("{{CONTAINMENT}}", fmt_list(containment))
    report = report.replace("{{ERADICATION}}", fmt_list(eradication))
    report = report.replace("{{RECOVERY}}", fmt_list(recovery))
    report = report.replace("{{LESSONS}}", fmt_list(lessons))
    report = report.replace("{{NEXT_STEPS}}", fmt_list(next_steps))

    timeline_doc = timeline_tpl.replace("{{INCIDENT_NAME}}", str(cs.get("incident_name") or "（未填写）"))
    timeline_doc = timeline_doc.replace("{{TIMELINE}}", fmt_list(timeline))

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report, encoding="utf-8")
    (out_path.parent / "timeline.md").write_text(timeline_doc, encoding="utf-8")
    print(f"[ok] report written: {out_path}")
    print(f"[ok] timeline written: {out_path.parent / 'timeline.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
