#!/usr/bin/env python3
"""Analysis depth gate for analyst handoffs (omni-ecom v1.5.13).

Enforces the L0-L4 individual analysis ladder so members cannot ship
description-level work with attribution-level conclusions:

  L0 inventory   what data exists, which caliber
  L1 describe    what happened, with comparison
  L2 decompose   which dimensions carry the change
  L3 attribute   why, with alternatives and counter conditions
  L4 decide      what to do, with acceptance and stop conditions

Hard requirements for every analyst (unless gate_status == BLOCKED):
  * baseline_ack bound to the issued baseline-pack SHA256
  * reached_level >= min_required_level (default L2)
  * level_evidence filled for every level up to reached_level
  * at least one decomposition dimension with >= 2 segments when reached >= L2
  * self_check seven questions answered
  * fact / judgment / hypothesis strictly layered

Outputs depth-guard.json with status depth_guard_passed | depth_guard_blocked.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from artifact_contract import (native_analysis_identity, validate_analysis_identity,
                               validate_baseline_identity)

HEX64 = re.compile(r"^[0-9a-f]{64}$")
LEVELS = ("L0", "L1", "L2", "L3", "L4")
SELF_CHECK_KEYS = (
    "caliber_consistent",
    "denominator_comparable",
    "counterexample_considered",
    "sample_sufficient",
    "recomputable",
    "outlier_screened",
    "layered_fact_judgment_hypothesis",
)
MIN_SET_MIN_ITEMS = 4


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"json_root_invalid:{path.name}")
    return value


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_ok(value: Any, min_len: int = 12) -> bool:
    text = str(value or "").strip()
    if len(text) < min_len:
        return False
    placeholders = ("待补", "TBD", "无", "同上", "-", "—", "n/a", "N/A")
    return text not in placeholders


def check_handoff(
    agent_id: str,
    path: Path,
    handoff: dict[str, Any],
    baseline_sha: str,
    min_level: str,
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    depth = handoff.get("analysis_depth")
    if not isinstance(depth, dict):
        return {
            "agent_id": agent_id,
            "file": path.name,
            "sha256": sha256_file(path),
            "status": "blocked",
            "errors": ["depth_declaration_missing"],
            "warnings": [],
        }
    try:
        validate_analysis_identity(depth,"depth_declaration",handoff.get("agent_version"))
    except ValueError as exc:
        errors.append(str(exc))

    gate_status = str(handoff.get("gate_status") or "").upper()
    blocked_data = gate_status == "BLOCKED"

    # 1. baseline acknowledgement
    ack = depth.get("baseline_ack")
    if not isinstance(ack, dict):
        errors.append("baseline_ack_missing")
    else:
        if not baseline_sha:
            warnings.append("baseline_sha_not_provided")
        elif str(ack.get("baseline_sha256") or "") != baseline_sha:
            errors.append("baseline_ack_sha_mismatch")
        if not isinstance(ack.get("accepted"), bool):
            errors.append("baseline_ack_accepted_missing")
        elif ack.get("accepted") is False:
            deviations = ack.get("deviations")
            if not isinstance(deviations, list) or not deviations:
                errors.append("baseline_deviation_without_reason")
            else:
                for dev in deviations:
                    if isinstance(dev, dict) and not text_ok(dev.get("reason"), 4):
                        errors.append("baseline_deviation_reason_too_weak")

    # 2. depth ladder
    ladder = depth.get("depth_ladder")
    if not isinstance(ladder, dict):
        errors.append("depth_ladder_missing")
        ladder = {}
    reached = str(ladder.get("reached_level") or "")
    if reached not in LEVELS:
        errors.append("reached_level_invalid")
        reached = "L0"
    required = str(ladder.get("min_required_level") or min_level)
    if required not in LEVELS:
        required = min_level

    if LEVELS.index(reached) < LEVELS.index(required):
        if blocked_data and text_ok(ladder.get("blocked_below"), 6):
            warnings.append(f"depth_level_downgraded_blocked_data:{reached}")
        else:
            errors.append(f"depth_level_insufficient:{reached}<{required}")

    # 3. level evidence filled up to reached level
    evidence = ladder.get("level_evidence")
    if not isinstance(evidence, dict):
        errors.append("level_evidence_missing")
    else:
        for level in ("L1", "L2", "L3", "L4"):
            if LEVELS.index(level) > LEVELS.index(reached):
                continue
            if not text_ok(evidence.get(level)):
                errors.append(f"level_evidence_{level}_empty")

    # 4. decomposition when reached >= L2
    if LEVELS.index(reached) >= LEVELS.index("L2") and not blocked_data:
        decomposition = depth.get("decomposition")
        if not isinstance(decomposition, list) or not decomposition:
            errors.append("decomposition_missing")
        else:
            valid = 0
            for item in decomposition:
                if not isinstance(item, dict):
                    continue
                segments = item.get("segments")
                ids = item.get("evidence_ids")
                if (
                    text_ok(item.get("dimension"), 2)
                    and isinstance(segments, list)
                    and len(segments) >= 2
                    and isinstance(ids, list)
                    and ids
                ):
                    valid += 1
            if valid < 1:
                errors.append("decomposition_insufficient")

    # 5. self check
    self_check = depth.get("self_check")
    if not isinstance(self_check, dict):
        errors.append("self_check_missing")
    else:
        missing = [key for key in SELF_CHECK_KEYS if not isinstance(self_check.get(key), bool)]
        if missing:
            errors.append("self_check_incomplete:" + ",".join(missing))
        else:
            false_hits = [key for key in SELF_CHECK_KEYS if self_check.get(key) is False]
            if len(false_hits) > 2:
                errors.append("self_check_false_over_limit:" + ",".join(false_hits))
            elif false_hits:
                warnings.append("self_check_false:" + ",".join(false_hits))

    # 6. minimum analysis set
    min_set = depth.get("minimum_analysis_set")
    if 'question_contract' in depth:
        if depth['question_contract'].get('mode')=='mechanism' and handoff.get('client_scope')!='runtime-acceptance-no-client-data':
            errors.append('mechanism_questions_for_business_forbidden')
        from role_analysis_contract import check_questions
        try:
            check_questions(agent_id, depth)
        except ValueError as exc:
            errors.append(str(exc))
    if isinstance(min_set, list) and min_set:
        if len(min_set) < MIN_SET_MIN_ITEMS:
            warnings.append(f"minimum_analysis_set_short:{len(min_set)}")
        unanswered = 0
        for item in min_set:
            if not isinstance(item, dict):
                continue
            status = str(item.get("status") or "")
            if 'question_contract' in depth:
                known={e.get('id') for e in handoff.get('evidence_ledger',[]) if isinstance(e,dict)}
                if not item.get('evidence_ids'):
                    errors.append('minimum_analysis_evidence_missing')
                elif set(item['evidence_ids'])-known:
                    errors.append('minimum_analysis_evidence_unknown')
            if status not in ("answered", "unanswerable", "not_applicable"):
                errors.append("minimum_analysis_set_status_invalid")
                continue
            if status in ("unanswerable", "not_applicable"):
                unanswered += 1
                if not text_ok(item.get("blocker"), 4):
                    errors.append("minimum_analysis_set_blocker_missing")
                if 'question_contract' in depth and not item.get('evidence_ids'):
                    errors.append('minimum_analysis_gap_evidence_missing')
                if 'question_contract' in depth:
                    known={e.get('id') for e in handoff.get('evidence_ledger',[]) if isinstance(e,dict)}
                    if set(item.get('evidence_ids',[]))-known:
                        errors.append('minimum_analysis_evidence_unknown')
            elif not text_ok(item.get("answer")):
                errors.append("minimum_analysis_set_answer_too_weak")
        if min_set and unanswered / len(min_set) > 0.7 and not blocked_data:
            errors.append("minimum_analysis_set_mostly_unanswerable")
    else:
        errors.append("minimum_analysis_set_missing")

    # 7. layer discipline in the handoff body
    facts = handoff.get("facts") or []
    judgments = handoff.get("judgments") or []
    if not isinstance(facts, list) or not facts:
        errors.append("facts_missing")
    for item in judgments:
        if not isinstance(item, dict):
            continue
        if not (item.get("counter_conditions") or []):
            errors.append("judgment_without_counter_condition")
            break
    if not blocked_data and (not isinstance(judgments, list) or not judgments):
        warnings.append("judgments_empty")

    return {
        "agent_id": agent_id,
        "file": path.name,
        "sha256": sha256_file(path),
        "reached_level": reached,
        "required_level": required,
        "gate_status": gate_status or "UNKNOWN",
        "status": "blocked" if errors else "passed",
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate individual analysis depth of analyst handoffs.")
    parser.add_argument("--handoff", action="append", default=[], help="agent_id=path pair, repeatable")
    parser.add_argument("--baseline", required=True, help="current native v2 baseline-pack.json path")
    parser.add_argument("--min-level", default="L2", choices=LEVELS)
    parser.add_argument("--expect-agents", default="", help="comma separated agent ids that must all be present")
    parser.add_argument("--output", default="depth-guard.json")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    if not args.handoff:
        print("depth_guard_failed:no_handoff_provided")
        return 2

    baseline_path = Path(args.baseline)
    if not baseline_path.exists():
        print("depth_guard_failed:baseline_missing")
        return 2
    baseline_sha = sha256_file(baseline_path)
    if not HEX64.fullmatch(baseline_sha):
        print("depth_guard_failed:baseline_sha_invalid")
        return 2
    try:
        baseline=load_json(baseline_path)
        validate_baseline_identity(baseline)
    except (ValueError, KeyError, TypeError, json.JSONDecodeError):
        print("depth_guard_failed:baseline_identity_invalid")
        return 2

    results: list[dict[str, Any]] = []
    seen: set[str] = set()
    for pair in args.handoff:
        if "=" not in pair:
            print(f"depth_guard_failed:handoff_pair_invalid:{pair}")
            return 2
        agent_id, raw_path = pair.split("=", 1)
        agent_id = agent_id.strip()
        path = Path(raw_path.strip())
        if not path.exists():
            print(f"depth_guard_failed:handoff_missing:{agent_id}")
            return 2
        if agent_id in seen:
            print(f"depth_guard_failed:handoff_duplicated:{agent_id}")
            return 2
        seen.add(agent_id)
        body=load_json(path)
        if (body.get('run_id')!=baseline.get('run_id') or body.get('client_scope')!=baseline.get('client_scope') or
                body.get('agent_version')!=baseline.get('team_version')):
            print("depth_guard_failed:baseline_binding_mismatch")
            return 2
        results.append(check_handoff(agent_id, path, body, baseline_sha, args.min_level))

    if args.expect_agents:
        expected = {item.strip() for item in args.expect_agents.split(",") if item.strip()}
        missing = sorted(expected - seen)
        if missing:
            print("depth_guard_failed:missing_agents:" + ",".join(missing))
            return 2

    blocked = [r for r in results if r["status"] == "blocked"]
    status = "depth_guard_blocked" if blocked else "depth_guard_passed"
    payload = {
        **native_analysis_identity("depth_guard",baseline["team_version"]),
        "run_id": baseline["run_id"],
        "client_scope": baseline["client_scope"],
        "team_version": baseline["team_version"],
        "baseline_sha256": baseline_sha,
        "min_required_level": args.min_level,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "results": results,
        "summary": {
            "checked": len(results),
            "passed": len(results) - len(blocked),
            "blocked": len(blocked),
            "blocked_agents": [r["agent_id"] for r in blocked],
        },
        "status": status,
    }

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2 if args.pretty else None),
        encoding="utf-8",
    )
    print(f"{status}:{out_path}")
    return 0 if not blocked else 1


if __name__ == "__main__":
    sys.exit(main())
