#!/usr/bin/env python3
"""Append-only champion/challenger registry; it never runs or tunes strategies."""

from __future__ import annotations

import argparse
import json
import os
from copy import deepcopy
from pathlib import Path
from typing import Any

try:
    from .policy_store import (
        _atomic_write,
        canonical_json,
        content_hash,
        default_state_root,
        locked,
        user_key,
        utc_now,
    )
except ImportError:
    from policy_store import (
        _atomic_write,
        canonical_json,
        content_hash,
        default_state_root,
        locked,
        user_key,
        utc_now,
    )


REGISTRY_SCHEMA = "strategy_registry.v1"
CHALLENGER_SCHEMA = "strategy_challenger.v1"
EVALUATION_SCHEMA = "strategy_evaluation.v1"


def paths(root: Path, key: str) -> tuple[Path, Path, Path]:
    directory = root / "users" / key
    return directory / "strategy-registry.json", directory / "strategy-events.jsonl", directory / ".strategy-lock"


def empty_registry() -> dict[str, Any]:
    return {
        "schemaVersion": REGISTRY_SCHEMA,
        "championVersion": None,
        "championHistory": [],
        "challengers": {},
        "updatedAt": None,
    }


def load_registry(root: Path, key: str) -> dict[str, Any]:
    current_path, _, _ = paths(root, key)
    if not current_path.exists():
        return empty_registry()
    value = json.loads(current_path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or value.get("schemaVersion") != REGISTRY_SCHEMA:
        raise ValueError("invalid stored strategy registry")
    return value


def read_object(path: str) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("input must contain a JSON object")
    return value


def validate_challenger(value: dict[str, Any], registry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if value.get("schemaVersion") != CHALLENGER_SCHEMA:
        errors.append("schemaVersion:must_equal_strategy_challenger.v1")
    challenger_id = str(value.get("id") or "").strip()
    if not challenger_id:
        errors.append("id:required")
    if challenger_id in (registry.get("challengers") or {}):
        errors.append("id:already_exists")
    if value.get("parentVersion") != registry.get("championVersion"):
        errors.append("parentVersion:must_equal_current_champion")
    if not str(value.get("candidateVersion") or "").strip():
        errors.append("candidateVersion:required")
    if not str(value.get("hypothesis") or "").strip():
        errors.append("hypothesis:required")
    changed = value.get("changedComponents")
    if not isinstance(changed, list) or len(changed) != 1:
        errors.append("changedComponents:exactly_one_required")
    registration = value.get("preRegistration") if isinstance(value.get("preRegistration"), dict) else {}
    for field in ("primaryMetric", "hardRiskMetrics", "minimumShadowObservations", "promotionThresholds"):
        if registration.get(field) in (None, "", []):
            errors.append(f"preRegistration.{field}:required")
    return errors


def validate_evaluation(value: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if value.get("schemaVersion") != EVALUATION_SCHEMA:
        errors.append("schemaVersion:must_equal_strategy_evaluation.v1")
    required_booleans = (
        "pointInTimeData",
        "walkForward",
        "allTrialsReported",
        "costStressPassed",
        "missingDataStressPassed",
        "primaryMetricImproved",
        "hardMetricsPassed",
    )
    for field in required_booleans:
        if not isinstance(value.get(field), bool):
            errors.append(f"{field}:required_boolean")
    try:
        if int(value.get("shadowObservations")) < 0:
            raise ValueError
    except (TypeError, ValueError):
        errors.append("shadowObservations:non_negative_integer_required")
    try:
        float(value.get("riskContractViolationsDelta"))
    except (TypeError, ValueError):
        errors.append("riskContractViolationsDelta:number_required")
    if not str(value.get("dataCutoffAt") or "").strip():
        errors.append("dataCutoffAt:required")
    return errors


def promotion_blockers(challenger: dict[str, Any]) -> list[str]:
    evaluation = challenger.get("evaluation") if isinstance(challenger.get("evaluation"), dict) else {}
    preregistration = challenger.get("preRegistration") if isinstance(challenger.get("preRegistration"), dict) else {}
    blockers = []
    for field in (
        "pointInTimeData",
        "walkForward",
        "allTrialsReported",
        "costStressPassed",
        "missingDataStressPassed",
        "primaryMetricImproved",
        "hardMetricsPassed",
    ):
        if evaluation.get(field) is not True:
            blockers.append(field)
    if float(evaluation.get("riskContractViolationsDelta") or 0) > 0:
        blockers.append("riskContractViolationsDelta")
    if int(evaluation.get("shadowObservations") or 0) < int(preregistration.get("minimumShadowObservations") or 0):
        blockers.append("minimumShadowObservations")
    return blockers


def persist(root: Path, key: str, registry: dict[str, Any], event_type: str, details: dict[str, Any]) -> None:
    current_path, events_path, lock_path = paths(root, key)
    with locked(lock_path):
        registry["updatedAt"] = utc_now()
        event = {
            "schemaVersion": "strategy_registry_event.v1",
            "eventType": event_type,
            "occurredAt": registry["updatedAt"],
            "userKey": key,
            "registryHash": content_hash(registry),
            "details": details,
        }
        events_path.parent.mkdir(parents=True, exist_ok=True)
        with events_path.open("a", encoding="utf-8") as handle:
            handle.write(canonical_json(event) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        _atomic_write(current_path, registry)


def bootstrap(root: Path, key: str, version: str) -> dict[str, Any]:
    registry = load_registry(root, key)
    if registry.get("championVersion"):
        raise ValueError("registry already has a champion")
    registry["championVersion"] = version
    registry["championHistory"] = [version]
    persist(root, key, registry, "CHAMPION_BOOTSTRAPPED", {"version": version})
    return registry


def register(root: Path, key: str, challenger: dict[str, Any]) -> dict[str, Any]:
    registry = load_registry(root, key)
    errors = validate_challenger(challenger, registry)
    if errors:
        raise ValueError(";".join(errors))
    value = deepcopy(challenger)
    value["status"] = "PROPOSED"
    value["registeredAt"] = utc_now()
    registry.setdefault("challengers", {})[str(value["id"])] = value
    persist(root, key, registry, "CHALLENGER_REGISTERED", {"id": value["id"]})
    return registry


def evaluate(root: Path, key: str, challenger_id: str, evaluation: dict[str, Any]) -> dict[str, Any]:
    registry = load_registry(root, key)
    challenger = (registry.get("challengers") or {}).get(challenger_id)
    if not challenger:
        raise ValueError("challenger not found")
    errors = validate_evaluation(evaluation)
    if errors:
        raise ValueError(";".join(errors))
    challenger["evaluation"] = deepcopy(evaluation)
    challenger["status"] = "EVALUATED"
    challenger["evaluatedAt"] = utc_now()
    persist(root, key, registry, "CHALLENGER_EVALUATED", {"id": challenger_id})
    return registry


def promote(root: Path, key: str, challenger_id: str, user_confirmed: bool) -> dict[str, Any]:
    if not user_confirmed:
        raise ValueError("promotion requires explicit user confirmation")
    registry = load_registry(root, key)
    challenger = (registry.get("challengers") or {}).get(challenger_id)
    if not challenger:
        raise ValueError("challenger not found")
    blockers = promotion_blockers(challenger)
    if blockers:
        raise ValueError("promotion blocked:" + ",".join(blockers))
    old_version = registry.get("championVersion")
    new_version = challenger["candidateVersion"]
    registry["championVersion"] = new_version
    history = list(registry.get("championHistory") or [])
    if new_version not in history:
        history.append(new_version)
    registry["championHistory"] = history
    challenger["status"] = "PROMOTED"
    challenger["promotedAt"] = utc_now()
    persist(
        root,
        key,
        registry,
        "CHALLENGER_PROMOTED",
        {"id": challenger_id, "oldVersion": old_version, "newVersion": new_version, "userConfirmed": True},
    )
    return registry


def reject(root: Path, key: str, challenger_id: str, reason: str) -> dict[str, Any]:
    registry = load_registry(root, key)
    challenger = (registry.get("challengers") or {}).get(challenger_id)
    if not challenger:
        raise ValueError("challenger not found")
    challenger["status"] = "REJECTED"
    challenger["rejectedAt"] = utc_now()
    challenger["rejectionReason"] = reason
    persist(root, key, registry, "CHALLENGER_REJECTED", {"id": challenger_id, "reason": reason})
    return registry


def rollback(root: Path, key: str, version: str, user_confirmed: bool) -> dict[str, Any]:
    if not user_confirmed:
        raise ValueError("rollback requires explicit user confirmation")
    registry = load_registry(root, key)
    if version not in (registry.get("championHistory") or []):
        raise ValueError("rollback version is not in champion history")
    old_version = registry.get("championVersion")
    registry["championVersion"] = version
    persist(
        root,
        key,
        registry,
        "CHAMPION_ROLLED_BACK",
        {"oldVersion": old_version, "newVersion": version, "userConfirmed": True},
    )
    return registry


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state-dir", default=None)
    subparsers = parser.add_subparsers(dest="command", required=True)
    status_parser = subparsers.add_parser("status")
    status_parser.add_argument("--user-id", required=True)
    bootstrap_parser = subparsers.add_parser("bootstrap")
    bootstrap_parser.add_argument("--user-id", required=True)
    bootstrap_parser.add_argument("--version", required=True)
    register_parser = subparsers.add_parser("register")
    register_parser.add_argument("--user-id", required=True)
    register_parser.add_argument("--input", required=True)
    evaluate_parser = subparsers.add_parser("evaluate")
    evaluate_parser.add_argument("--user-id", required=True)
    evaluate_parser.add_argument("--id", required=True)
    evaluate_parser.add_argument("--input", required=True)
    promote_parser = subparsers.add_parser("promote")
    promote_parser.add_argument("--user-id", required=True)
    promote_parser.add_argument("--id", required=True)
    promote_parser.add_argument("--user-confirmed", action="store_true")
    reject_parser = subparsers.add_parser("reject")
    reject_parser.add_argument("--user-id", required=True)
    reject_parser.add_argument("--id", required=True)
    reject_parser.add_argument("--reason", required=True)
    rollback_parser = subparsers.add_parser("rollback")
    rollback_parser.add_argument("--user-id", required=True)
    rollback_parser.add_argument("--version", required=True)
    rollback_parser.add_argument("--user-confirmed", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    root = Path(args.state_dir).expanduser().resolve() if args.state_dir else default_state_root()
    key = user_key(args.user_id)
    if args.command == "status":
        result = load_registry(root, key)
    elif args.command == "bootstrap":
        result = bootstrap(root, key, args.version)
    elif args.command == "register":
        result = register(root, key, read_object(args.input))
    elif args.command == "evaluate":
        result = evaluate(root, key, args.id, read_object(args.input))
    elif args.command == "promote":
        result = promote(root, key, args.id, args.user_confirmed)
    elif args.command == "reject":
        result = reject(root, key, args.id, args.reason)
    elif args.command == "rollback":
        result = rollback(root, key, args.version, args.user_confirmed)
    else:
        raise ValueError("unsupported command")
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
