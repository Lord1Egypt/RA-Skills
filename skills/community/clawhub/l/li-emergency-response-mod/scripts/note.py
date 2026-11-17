#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
企业应急响应指导 Skill - 低摩擦记录工具（WAL / 黑板）

目的：
- 把应急过程写入结构化文件，避免“全靠对话记忆”
- 支持结构化 actions / IOC / 时间线，便于复盘与审计
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Tuple


ROOT = Path(__file__).resolve().parents[1]
SESSION_PATH = ROOT / "memory" / "working" / "current_session.json"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_kv(s: str) -> Tuple[str, str]:
    if "=" not in s:
        raise ValueError("格式必须为 key=value")
    k, v = s.split("=", 1)
    return k.strip(), v.strip()


def ensure_list(cs: Dict[str, Any], key: str):
    if key not in cs or not isinstance(cs[key], list):
        cs[key] = []


def main() -> int:
    ap = argparse.ArgumentParser(description="IR note (record-only WAL)")
    ap.add_argument("text", nargs="?", default="", help="一句话记录（可为空，仅用于 --set 场景）")
    ap.add_argument("--tag", help="标签（可选）：triage/logs/pcap/host/iam/malware 等")
    ap.add_argument("--evidence", action="append", default=[], help="证据路径（可重复）：截图/pcap/日志片段")
    ap.add_argument("--artifact", action="append", default=[], help="产物路径（可重复）：脚本/导出/报告")
    ap.add_argument("--attempt", action="append", default=[], help="尝试记录（可重复）")
    ap.add_argument("--next", dest="next_steps", action="append", default=[], help="下一步（可重复）")
    ap.add_argument("--set", action="append", default=[], help="设置 current_session 字段：key=value（可重复）")

    # 阶段与结构化动作
    ap.add_argument("--phase", help="阶段（detect/triage/contain/eradicate/recover/postmortem/report）")
    ap.add_argument("--mode", choices=["production", "ctf"], help="模式：production（真实处置）/ ctf（应急题解题）")
    ap.add_argument("--flag-format", help="CTF flag 格式提示（如 flag{...}），可选")
    ap.add_argument("--severity", help="严重性（low/medium/high/critical）")
    ap.add_argument("--timezone", help="事件时区（如 Asia/Shanghai）")
    ap.add_argument("--source", action="append", default=[], help="告警/数据源（可重复）：edr/siem/waf/fw/cloud/...") 
    ap.add_argument("--stakeholder", action="append", default=[], help="干系人（可重复）：应急负责人/系统负责人/审批人/... ")
    ap.add_argument("--asset", action="append", default=[], help="受影响资产（可重复）：主机/IP/业务/账号/数据库/... ")
    ap.add_argument("--action", help="动作类型（collect/analyze/verify/contain/eradicate/recover/report）")
    ap.add_argument("--verdict", help="结论（pass/fail/unknown）")
    ap.add_argument("--reason", help="原因（ioc-hit/log-proof/noise/assumption/timeout/unknown）")
    ap.add_argument("--tool", action="append", default=[], help="工具（可重复）：edr/siem/ssh/volatility 等")
    ap.add_argument("--target", help="目标对象（主机/账号/URL/日志源等）")
    ap.add_argument("--payload", help="关键查询/命令摘要（建议摘要）")
    ap.add_argument("--impact", help="业务影响描述（如：仅影响单台主机CPU，无业务中断）")
    ap.add_argument("--hitl", choices=["required", "not_required"], help="是否属于需要人工确认的高风险动作")

    # IOC 与时间线
    ap.add_argument("--ioc-ip", action="append", default=[], help="IOC IP（可重复）")
    ap.add_argument("--ioc-domain", action="append", default=[], help="IOC 域名（可重复）")
    ap.add_argument("--ioc-url", action="append", default=[], help="IOC URL（可重复）")
    ap.add_argument("--ioc-hash", action="append", default=[], help="IOC hash（可重复）")
    ap.add_argument("--ioc-file", action="append", default=[], help="IOC 文件路径/名称（可重复）")
    ap.add_argument("--ioc-proc", action="append", default=[], help="IOC 进程名/命令行（可重复）")
    ap.add_argument("--ioc-user", action="append", default=[], help="IOC 用户/账号（可重复）")
    ap.add_argument("--ioc-registry", action="append", default=[], help="IOC 注册表项（可重复）")
    ap.add_argument("--timeline", action="append", default=[], help="时间线事件（可重复，建议带时间）")
    ap.add_argument("--flag", action="append", default=[], help="CTF 题目答案（可重复），格式建议：问题=flag{...} 或 题号=答案")
    ap.add_argument("--containment", action="append", default=[], help="遏制动作（可重复）")
    ap.add_argument("--eradication", action="append", default=[], help="清除/加固动作（可重复）")
    ap.add_argument("--recovery", action="append", default=[], help="恢复动作（可重复）")
    ap.add_argument("--lesson", action="append", default=[], help="经验教训/改进项（可重复）")
    args = ap.parse_args()

    session = load_json(SESSION_PATH, {"current_session": {}})
    cs: Dict[str, Any] = session.get("current_session") or {}

    if not cs.get("start_time"):
        cs["start_time"] = now_iso()

    if args.phase:
        cs["phase"] = args.phase
    if args.mode:
        cs["mode"] = args.mode
    if args.flag_format:
        cs["flag_format"] = args.flag_format
    if args.severity:
        cs["severity"] = args.severity
    if args.timezone:
        cs["timezone"] = args.timezone

    for item in args.set:
        k, v = parse_kv(item)
        cs[k] = v

    if args.source:
        ensure_list(cs, "sources")
        cs["sources"].extend(args.source)
    if args.stakeholder:
        ensure_list(cs, "stakeholders")
        cs["stakeholders"].extend(args.stakeholder)
    if args.asset:
        ensure_list(cs, "assets")
        cs["assets"].extend(args.asset)

    if args.text.strip():
        ensure_list(cs, "notes")
        cs["notes"].append({"ts": now_iso(), "tag": args.tag, "text": args.text.strip()})
        cs["last_progress_time"] = now_iso()

    if args.evidence:
        ensure_list(cs, "evidence")
        cs["evidence"].extend([{"ts": now_iso(), "path": p} for p in args.evidence])
        cs["last_progress_time"] = now_iso()

    if args.artifact:
        ensure_list(cs, "artifacts")
        cs["artifacts"].extend([{"ts": now_iso(), "path": p} for p in args.artifact])

    if args.attempt:
        ensure_list(cs, "attempts")
        cs["attempts"].extend([{"ts": now_iso(), "text": x} for x in args.attempt])

    if args.next_steps:
        ensure_list(cs, "next_steps")
        cs["next_steps"].extend([{"ts": now_iso(), "text": x} for x in args.next_steps])

    # IOC
    cs.setdefault("iocs", {})
    for k, vals in [
        ("ip", args.ioc_ip),
        ("domain", args.ioc_domain),
        ("url", args.ioc_url),
        ("hash", args.ioc_hash),
        ("file", args.ioc_file),
        ("process", args.ioc_proc),
        ("user", args.ioc_user),
        ("registry", args.ioc_registry),
    ]:
        cs["iocs"].setdefault(k, [])
        for v in vals:
            cs["iocs"][k].append({"ts": now_iso(), "value": v})

    # timeline
    if args.timeline:
        ensure_list(cs, "timeline")
        cs["timeline"].extend([{"ts": now_iso(), "event": x} for x in args.timeline])

    # flags (CTF 题解)
    if args.flag:
        ensure_list(cs, "flags")
        cs["flags"].extend([{"ts": now_iso(), "text": x} for x in args.flag])
        cs["last_progress_time"] = now_iso()

    if args.containment:
        ensure_list(cs, "containment")
        cs["containment"].extend([{"ts": now_iso(), "text": x} for x in args.containment])
    if args.eradication:
        ensure_list(cs, "eradication")
        cs["eradication"].extend([{"ts": now_iso(), "text": x} for x in args.eradication])
    if args.recovery:
        ensure_list(cs, "recovery")
        cs["recovery"].extend([{"ts": now_iso(), "text": x} for x in args.recovery])
    if args.lesson:
        ensure_list(cs, "lessons_learned")
        cs["lessons_learned"].extend([{"ts": now_iso(), "text": x} for x in args.lesson])

    # structured action
    if args.action or args.verdict or args.reason or args.tool or args.target or args.payload:
        ensure_list(cs, "actions")
        cs["actions"].append(
            {
                "ts": now_iso(),
                "phase": cs.get("phase"),
                "action": args.action,
                "verdict": args.verdict,
                "reason": args.reason,
                "tool": args.tool,
                "target": args.target,
                "payload": args.payload,
                "impact": args.impact,
                "hitl": args.hitl,
                "note": (args.text or "").strip() or None,
            }
        )
        cs["last_progress_time"] = now_iso()

    session["current_session"] = cs
    save_json(SESSION_PATH, session)
    print(f"[ok] updated: {SESSION_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
