#!/usr/bin/env python3
"""Cross-member conflict scanner for sealed handoffs (omni-ecom v2.0 candidate).

Scans four analyst sealed handoffs and detects four conflict families:

  numeric     same metric + same period, values differ beyond tolerance
  caliber     same metric declared under different denominators / dedupe rules
  direction   opposite trend words on the same metric token
  attribution competing structured causal conclusions for the same outcome

Hard conflicts force a targeted challenge round before the lead may merge results.
Fail closed: missing, unreadable or duplicated handoffs abort the scan.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from artifact_contract import native_analysis_identity, validate_baseline_identity
from causal_evidence_guard import review_handoffs, causal_conflicts

HEX64 = re.compile(r"^[0-9a-f]{64}$")
CONFLICT_ID = re.compile(r"^X-[A-Za-z0-9_-]+$")

UP_WORDS = ("上升", "上涨", "提升", "改善", "好转", "增长", "变好", "走高", "恢复")
DOWN_WORDS = ("下降", "下滑", "崩塌", "恶化", "变差", "走低", "萎缩", "衰退", "减少")

# Metrics where an opposite direction claim is business critical.
CORE_METRICS = ("转化率", "客单价", "访客", "GMV", "退款率", "ROI", "ROAS", "UV价值", "净销售")

CALIBER_TRAPS = {
    "转化率": ("访客", "去重", "分母"),
    "访客数": ("去重", "SPU", "加总"),
    "UV价值": ("退款", "净"),
    "ROI": ("归因", "花费"),
    "ROAS": ("归因", "花费"),
}

def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"json_root_invalid:{path.name}")
    return value


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value))


def norm_metric(text: str) -> str:
    cleaned = re.sub(r"[\s（）()\[\]【】：:，,。.]", "", str(text or "")).strip()
    return cleaned


def norm_period(text: str) -> str:
    return re.sub(r"[\s/年\-—]", "", str(text or "")).strip()


def evidence_rows(handoff: dict[str, Any], agent_id: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in handoff.get("evidence_ledger") or []:
        if not isinstance(item, dict):
            continue
        metric = norm_metric(item.get("metric"))
        if not metric:
            continue
        rows.append(
            {
                "agent_id": agent_id,
                "metric": metric,
                "raw_metric": str(item.get("metric") or ""),
                "period": norm_period(item.get("period")),
                "value": item.get("value"),
                "formula": str(item.get("formula") or ""),
                "status": str(item.get("status") or ""),
                "evidence_id": str(item.get("id") or ""),
            }
        )
    return rows


def scan_numeric(rows: list[dict[str, Any]], tolerance: float) -> list[dict[str, Any]]:
    conflicts: list[dict[str, Any]] = []
    buckets: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for row in rows:
        if not is_number(row["value"]):
            continue
        buckets.setdefault((row["metric"], row["period"]), []).append(row)

    seq = 0
    for (metric, period), group in buckets.items():
        agents = {row["agent_id"] for row in group}
        if len(agents) < 2:
            continue
        values = [float(row["value"]) for row in group]
        spread = max(values)
        base = min(values)
        if base == 0:
            rel = 0.0 if spread == 0 else 1.0
        else:
            rel = abs(spread - base) / abs(base)
        if rel <= tolerance:
            continue
        seq += 1
        conflicts.append(
            {
                "conflict_id": f"X-NUM-{seq:03d}",
                "type": "numeric",
                "metric": metric,
                "period": period,
                "severity": "hard" if metric in CORE_METRICS else "soft",
                "topic": f"{metric}（期间 {period or '未标注'}）在成员间数值不一致，相对差异 {rel:.1%}",
                "positions": [
                    {
                        "agent_id": row["agent_id"],
                        "position": f"{metric} = {row['value']}",
                        "value": row["value"],
                        "evidence_ids": [row["evidence_id"]] if row["evidence_id"] else [],
                    }
                    for row in group
                ],
                "needs_challenge_round": True,
                "lead_recomputation_required": metric in CORE_METRICS,
            }
        )
    return conflicts


def scan_caliber(rows: list[dict[str, Any]], handoffs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    conflicts: list[dict[str, Any]] = []
    seq = 0
    by_metric: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_metric.setdefault(row["metric"], []).append(row)

    for metric, group in by_metric.items():
        trap_words = CALIBER_TRAPS.get(metric)
        if not trap_words:
            continue
        agents = {row["agent_id"] for row in group}
        if len(agents) < 2:
            continue
        formulas = {row["agent_id"]: row["formula"] for row in group if row["formula"]}
        deviations: dict[str, str] = {}
        for agent_id in sorted(agents):
            ack = (handoffs.get(agent_id, {}).get("analysis_depth") or {}).get("baseline_ack") or {}
            for dev in ack.get("deviations") or []:
                if isinstance(dev, dict) and str(dev.get("item") or ""):
                    deviations[agent_id] = str(dev.get("reason") or "未说明原因")
        if not deviations and len(set(formulas.values())) <= 1:
            continue
        seq += 1
        conflicts.append(
            {
                "conflict_id": f"X-CAL-{seq:03d}",
                "type": "caliber",
                "metric": metric,
                "severity": "hard",
                "topic": f"{metric} 在成员间存在同名不同口径："
                + ("；".join(f"{a}={r}" for a, r in deviations.items()) or "公式声明不一致"),
                "positions": [
                    {
                        "agent_id": agent_id,
                        "position": formulas.get(agent_id) or deviations.get(agent_id) or "未声明口径",
                        "evidence_ids": [],
                    }
                    for agent_id in sorted(agents)
                ],
                "needs_challenge_round": True,
                "lead_recomputation_required": True,
            }
        )
    return conflicts


def direction_of(text: str) -> str | None:
    up = any(word in text for word in UP_WORDS)
    down = any(word in text for word in DOWN_WORDS)
    if up and not down:
        return "up"
    if down and not up:
        return "down"
    return None


def scan_direction(handoffs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    conflicts: list[dict[str, Any]] = []
    claims: dict[str, list[dict[str, Any]]] = {}

    for agent_id, handoff in handoffs.items():
        texts: list[str] = []
        for item in handoff.get("judgments") or []:
            if isinstance(item, dict):
                texts.append(str(item.get("claim") or ""))
        for item in handoff.get("facts") or []:
            if isinstance(item, dict):
                texts.append(str(item.get("claim") or ""))
        summary = str(handoff.get("contribution_summary") or "")
        if summary:
            texts.append(summary)
        for text in texts:
            for metric in CORE_METRICS:
                if metric not in text:
                    continue
                direction = direction_of(text)
                if not direction:
                    continue
                claims.setdefault(metric, []).append(
                    {"agent_id": agent_id, "direction": direction, "text": text[:180]}
                )

    seq = 0
    for metric, group in claims.items():
        dirs = {item["direction"] for item in group}
        if dirs != {"up", "down"}:
            continue
        seq += 1
        conflicts.append(
            {
                "conflict_id": f"X-DIR-{seq:03d}",
                "type": "direction",
                "metric": metric,
                "severity": "hard",
                "topic": f"{metric} 的变化方向在成员间完全相反，属于决定主结论的核心冲突",
                "positions": [
                    {
                        "agent_id": item["agent_id"],
                        "position": ("判断为上升：" if item["direction"] == "up" else "判断为下降：") + item["text"],
                        "evidence_ids": [],
                    }
                    for item in group
                ],
                "needs_challenge_round": True,
                "lead_recomputation_required": True,
            }
        )
    return conflicts


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan sealed handoffs for cross-member conflicts.")
    parser.add_argument("--handoff", action="append", default=[], help="agent_id=path pair, repeatable")
    parser.add_argument("--baseline", required=True, help="current native v2 baseline-pack.json path")
    parser.add_argument("--run-id", help="run identifier")
    parser.add_argument("--tolerance", type=float, default=0.02, help="relative numeric tolerance, default 0.02")
    parser.add_argument("--output", default="conflict-scan.json")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    if not args.handoff:
        print("conflict_scan_failed:no_handoff_provided")
        return 2

    handoffs: dict[str, dict[str, Any]] = {}
    scanned: list[dict[str, Any]] = []
    for pair in args.handoff:
        if "=" not in pair:
            print(f"conflict_scan_failed:handoff_pair_invalid:{pair}")
            return 2
        agent_id, raw_path = pair.split("=", 1)
        agent_id = agent_id.strip()
        path = Path(raw_path.strip())
        if not path.exists():
            print(f"conflict_scan_failed:handoff_missing:{agent_id}")
            return 2
        if agent_id in handoffs:
            print(f"conflict_scan_failed:handoff_duplicated:{agent_id}")
            return 2
        handoffs[agent_id] = load_json(path)
        scanned.append({"agent_id": agent_id, "file": path.name, "sha256": sha256_file(path)})

    baseline_path = Path(args.baseline)
    if not baseline_path.exists():
        print("conflict_scan_failed:baseline_missing")
        return 2
    baseline_sha = sha256_file(baseline_path)
    try:
        baseline = load_json(baseline_path)
        validate_baseline_identity(baseline)
    except (ValueError, KeyError, TypeError, json.JSONDecodeError):
        print("conflict_scan_failed:baseline_identity_invalid")
        return 2

    run_ids = {str(h.get("run_id") or "").strip() for h in handoffs.values()}
    run_ids.discard("")
    if args.run_id and run_ids and args.run_id not in run_ids:
        print("conflict_scan_failed:run_id_mismatch")
        return 2
    if len(run_ids) > 1:
        print("conflict_scan_failed:run_id_conflict")
        return 2
    expected_run = args.run_id or (next(iter(run_ids)) if run_ids else None)
    versions = {str(h.get('agent_version') or '').strip() for h in handoffs.values()}; versions.discard('')
    clients = {str(h.get('client_scope') or '').strip() for h in handoffs.values()}; clients.discard('')
    try:
        validate_baseline_identity(baseline,
            expected_team_version=next(iter(versions)) if len(versions)==1 else None,
            run_id=expected_run,
            client_scope=next(iter(clients)) if len(clients)==1 else None)
    except ValueError:
        print("conflict_scan_failed:baseline_binding_mismatch")
        return 2

    scanned_at = datetime.now(timezone.utc).isoformat()
    try:
        causal_review = review_handoffs(
            handoffs,
            expected_run,
            baseline["client_scope"],
            baseline["team_version"],
            scanned_at,
        )
    except (ValueError, KeyError, TypeError) as exc:
        print("conflict_scan_failed:" + str(exc))
        return 2

    rows: list[dict[str, Any]] = []
    for agent_id, handoff in handoffs.items():
        rows.extend(evidence_rows(handoff, agent_id))

    conflicts: list[dict[str, Any]] = []
    conflicts.extend(scan_numeric(rows, args.tolerance))
    conflicts.extend(scan_caliber(rows, handoffs))
    conflicts.extend(scan_direction(handoffs))
    conflicts.extend(causal_conflicts(causal_review))

    for conflict in conflicts:
        if not CONFLICT_ID.fullmatch(str(conflict["conflict_id"])):
            print("conflict_scan_failed:conflict_id_invalid")
            return 2

    hard = [c for c in conflicts if c["severity"] == "hard"]
    soft = [c for c in conflicts if c["severity"] == "soft"]
    if hard:
        status = "conflict_scan_hard_blocked"
    elif soft:
        status = "conflict_scan_soft_only"
    else:
        status = "conflict_scan_clean"

    payload: dict[str, Any] = {
        **native_analysis_identity("conflict_scan",baseline["team_version"]),
        "run_id": args.run_id or (next(iter(run_ids)) if run_ids else ""),
        "client_scope": baseline["client_scope"],
        "team_version": baseline["team_version"],
        "baseline_sha256": baseline_sha,
        "scanned_handoffs": scanned,
        "conflicts": conflicts,
        "causal_review": causal_review,
        "summary": {
            "total": len(conflicts),
            "hard": len(hard),
            "soft": len(soft),
            "needs_challenge_round": any(bool(c.get("needs_challenge_round")) for c in conflicts),
            "lead_recomputation_required": any(bool(c.get("lead_recomputation_required")) for c in conflicts),
        },
        "status": status,
        "scanned_at": scanned_at,
    }

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2 if args.pretty else None),
        encoding="utf-8",
    )
    print(f"{status}:{out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
