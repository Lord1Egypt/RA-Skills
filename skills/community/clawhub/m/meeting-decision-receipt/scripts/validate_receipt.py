#!/usr/bin/env python3
"""Validate a meeting receipt against JSON Schema and semantic invariants."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any, Iterable

from redact_sensitive import redact_value


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = ROOT / "schemas" / "receipt.schema.json"

DECISION_TYPES = {"confirmed", "provisional", "conditional", "proposed", "deferred", "rejected", "superseded"}
COMMITMENT_TYPES = {
    "explicit_commitment",
    "accepted_assignment",
    "unacknowledged_assignment",
    "implied_assignment",
    "tentative_intent",
    "conditional_commitment",
    "unowned",
}
CORE_DECISIONS = {"confirmed", "provisional", "conditional", "rejected"}
MISSING_FIELDS = {"owner", "task", "due", "dependencies", "acceptance_criteria", "confirmation"}
OPEN_LOOP_MISSING = MISSING_FIELDS | {"dependency_owner", "dependency_due", "decision", "final_approver", "source_evidence"}
REDACTION_CATEGORIES = {"password", "token", "api_key", "phone", "email", "credential", "other"}


def _require(condition: bool, path: str, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(f"{path}: {message}")


def _reject_unknown_keys(value: Any, allowed: set[str], path: str, errors: list[str]) -> None:
    if not isinstance(value, dict):
        return
    unknown = sorted(set(value) - allowed)
    if unknown:
        errors.append(f"{path}: unknown properties {unknown}")


def _fallback_structure(data: Any) -> list[str]:
    """Dependency-free checks used when jsonschema is unavailable."""

    errors: list[str] = []
    _require(isinstance(data, dict), "$", "must be an object", errors)
    if not isinstance(data, dict):
        return errors

    required = ["meeting", "close_status", "summary", "decisions", "commitments", "open_loops", "confirmation_message", "safety"]
    for key in required:
        _require(key in data, "$", f"missing required property {key}", errors)
    _reject_unknown_keys(data, set(required), "$", errors)

    meeting = data.get("meeting")
    _require(isinstance(meeting, dict), "$.meeting", "must be an object", errors)
    if isinstance(meeting, dict):
        _reject_unknown_keys(meeting, {"title", "date", "source_type", "participants", "source_label"}, "$.meeting", errors)
        for key in ["title", "date", "source_type", "participants"]:
            _require(key in meeting, "$.meeting", f"missing {key}", errors)
        _require(isinstance(meeting.get("title"), str) and bool(meeting.get("title")), "$.meeting.title", "must be a non-empty string", errors)
        _require(meeting.get("source_type") in {"transcript", "smart_minutes", "notes", "discussion_thread", "local_file"}, "$.meeting.source_type", "invalid value", errors)
        _require(isinstance(meeting.get("participants"), list) and all(isinstance(item, str) and item for item in meeting.get("participants", [])), "$.meeting.participants", "must contain non-empty strings", errors)
        if meeting.get("date") is not None:
            try:
                date.fromisoformat(meeting.get("date"))
            except (TypeError, ValueError):
                errors.append("$.meeting.date: must be YYYY-MM-DD or null")

    _require(data.get("close_status") in {"closed", "needs_confirmation", "no_clear_decision", "insufficient_evidence"}, "$.close_status", "invalid value", errors)
    summary = data.get("summary")
    summary_keys = {
        "confirmed_decisions", "provisional_decisions", "conditional_decisions",
        "explicit_commitments", "unconfirmed_assignments", "tentative_intents", "open_loops",
    }
    _require(isinstance(summary, dict), "$.summary", "must be an object", errors)
    if isinstance(summary, dict):
        _reject_unknown_keys(summary, summary_keys, "$.summary", errors)
        for key in summary_keys:
            _require(key in summary, "$.summary", f"missing {key}", errors)
            _require(isinstance(summary.get(key), int) and not isinstance(summary.get(key), bool) and summary.get(key, -1) >= 0, f"$.summary.{key}", "must be a non-negative integer", errors)
    for key in ["decisions", "commitments", "open_loops"]:
        _require(isinstance(data.get(key), list), f"$.{key}", "must be an array", errors)
    _require(isinstance(data.get("confirmation_message"), str) and bool(data.get("confirmation_message")), "$.confirmation_message", "must be a non-empty string", errors)

    for index, item in enumerate(data.get("decisions", [])):
        path = f"$.decisions[{index}]"
        _require(isinstance(item, dict), path, "must be an object", errors)
        if not isinstance(item, dict):
            continue
        _reject_unknown_keys(item, {"id", "statement", "status", "scope", "condition", "confidence", "current", "replaced_by", "evidence"}, path, errors)
        for key in ["id", "statement", "status", "scope", "condition", "confidence", "current", "replaced_by", "evidence"]:
            _require(key in item, path, f"missing {key}", errors)
        _require(bool(re.fullmatch(r"D-[0-9]{2,3}", str(item.get("id", "")))), f"{path}.id", "invalid ID", errors)
        _require(isinstance(item.get("statement"), str) and bool(item.get("statement")), f"{path}.statement", "must be a non-empty string", errors)
        _require(item.get("status") in DECISION_TYPES, f"{path}.status", "invalid decision type", errors)
        _require(item.get("confidence") in {"high", "medium", "low"}, f"{path}.confidence", "invalid confidence", errors)
        _require(isinstance(item.get("current"), bool), f"{path}.current", "must be boolean", errors)
        _validate_evidence(item.get("evidence"), f"{path}.evidence", errors)

    for index, item in enumerate(data.get("commitments", [])):
        path = f"$.commitments[{index}]"
        _require(isinstance(item, dict), path, "must be an object", errors)
        if not isinstance(item, dict):
            continue
        _reject_unknown_keys(item, {"id", "task", "owner", "owner_kind", "type", "due_original", "due_resolved", "dependencies", "acceptance_criteria", "missing_fields", "confidence", "evidence"}, path, errors)
        for key in ["id", "task", "owner", "owner_kind", "type", "due_original", "due_resolved", "dependencies", "acceptance_criteria", "missing_fields", "confidence", "evidence"]:
            _require(key in item, path, f"missing {key}", errors)
        _require(bool(re.fullmatch(r"C-[0-9]{2,3}", str(item.get("id", "")))), f"{path}.id", "invalid ID", errors)
        _require(isinstance(item.get("task"), str) and bool(item.get("task")), f"{path}.task", "must be a non-empty string", errors)
        _require(item.get("type") in COMMITMENT_TYPES, f"{path}.type", "invalid commitment type", errors)
        _require(item.get("owner_kind") in {"person", "team", "unknown"}, f"{path}.owner_kind", "invalid owner kind", errors)
        _require(item.get("owner") is None or isinstance(item.get("owner"), str), f"{path}.owner", "must be string or null", errors)
        _require(isinstance(item.get("dependencies"), list) and all(isinstance(value, str) and value for value in item.get("dependencies", [])), f"{path}.dependencies", "must contain non-empty strings", errors)
        raw_missing_fields = item.get("missing_fields")
        _require(isinstance(raw_missing_fields, list), f"{path}.missing_fields", "must be an array", errors)
        missing_values = set(raw_missing_fields) if isinstance(raw_missing_fields, list) else set()
        _require(missing_values <= MISSING_FIELDS, f"{path}.missing_fields", "contains invalid value", errors)
        _require(item.get("confidence") in {"high", "medium", "low"}, f"{path}.confidence", "invalid confidence", errors)
        if item.get("due_resolved") is not None:
            try:
                date.fromisoformat(item.get("due_resolved"))
            except (TypeError, ValueError):
                errors.append(f"{path}.due_resolved: must be YYYY-MM-DD or null")
        _validate_evidence(item.get("evidence"), f"{path}.evidence", errors)

    for index, item in enumerate(data.get("open_loops", [])):
        path = f"$.open_loops[{index}]"
        _require(isinstance(item, dict), path, "must be an object", errors)
        if not isinstance(item, dict):
            continue
        _reject_unknown_keys(item, {"id", "topic", "missing", "risk", "related_items"}, path, errors)
        for key in ["id", "topic", "missing", "risk", "related_items"]:
            _require(key in item, path, f"missing {key}", errors)
        _require(bool(re.fullmatch(r"O-[0-9]{2,3}", str(item.get("id", "")))), f"{path}.id", "invalid ID", errors)
        _require(isinstance(item.get("topic"), str) and bool(item.get("topic")), f"{path}.topic", "must be a non-empty string", errors)
        _require(isinstance(item.get("risk"), str) and bool(item.get("risk")), f"{path}.risk", "must be a non-empty string", errors)
        _require(isinstance(item.get("missing"), list) and bool(item.get("missing")), f"{path}.missing", "must be a non-empty array", errors)
        raw_loop_missing = item.get("missing")
        loop_missing_values = set(raw_loop_missing) if isinstance(raw_loop_missing, list) else set()
        _require(loop_missing_values <= OPEN_LOOP_MISSING, f"{path}.missing", "contains invalid value", errors)
        _require(isinstance(item.get("related_items"), list), f"{path}.related_items", "must be an array", errors)

    safety = data.get("safety")
    _require(isinstance(safety, dict), "$.safety", "must be an object", errors)
    if isinstance(safety, dict):
        safety_keys = {"contains_sensitive_content", "redactions", "redaction_categories", "send_requires_confirmation", "raw_source_persisted", "neutral_language_mode"}
        _reject_unknown_keys(safety, safety_keys, "$.safety", errors)
        for key in safety_keys:
            _require(key in safety, "$.safety", f"missing {key}", errors)
        _require(isinstance(safety.get("contains_sensitive_content"), bool), "$.safety.contains_sensitive_content", "must be boolean", errors)
        _require(isinstance(safety.get("redactions"), int) and not isinstance(safety.get("redactions"), bool) and safety.get("redactions", -1) >= 0, "$.safety.redactions", "must be a non-negative integer", errors)
        raw_categories = safety.get("redaction_categories")
        _require(isinstance(raw_categories, list), "$.safety.redaction_categories", "must be an array", errors)
        categories = set(raw_categories) if isinstance(raw_categories, list) else set()
        _require(
            categories <= REDACTION_CATEGORIES,
            "$.safety.redaction_categories",
            "contains invalid value",
            errors,
        )
        _require(
            not isinstance(raw_categories, list) or len(raw_categories) == len(categories),
            "$.safety.redaction_categories",
            "must contain unique values",
            errors,
        )
        _require(isinstance(safety.get("neutral_language_mode"), bool), "$.safety.neutral_language_mode", "must be boolean", errors)
        _require(safety.get("send_requires_confirmation") is True, "$.safety.send_requires_confirmation", "must be true", errors)
        _require(safety.get("raw_source_persisted") is False, "$.safety.raw_source_persisted", "must be false", errors)
    return errors


def _validate_evidence(evidence: Any, path: str, errors: list[str]) -> None:
    _require(isinstance(evidence, list) and len(evidence) >= 1, path, "must contain at least one item", errors)
    if not isinstance(evidence, list):
        return
    for index, item in enumerate(evidence):
        item_path = f"{path}[{index}]"
        _require(isinstance(item, dict), item_path, "must be an object", errors)
        if not isinstance(item, dict):
            continue
        _reject_unknown_keys(item, {"speaker", "timestamp", "paragraph", "quote"}, item_path, errors)
        for key in ["speaker", "timestamp", "paragraph", "quote"]:
            _require(key in item, item_path, f"missing {key}", errors)
        _require(bool(item.get("speaker")), f"{item_path}.speaker", "required", errors)
        _require(bool(item.get("timestamp")) or bool(item.get("paragraph")), item_path, "timestamp or paragraph is required", errors)
        quote = item.get("quote")
        _require(isinstance(quote, str) and 0 < len(quote) <= 240, f"{item_path}.quote", "must contain 1-240 characters", errors)


def _jsonschema_errors(data: Any, schema: dict[str, Any]) -> tuple[list[str], bool]:
    try:
        import jsonschema
    except ImportError:
        return [], False

    validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
    errors = []
    for error in sorted(validator.iter_errors(data), key=lambda item: list(item.absolute_path)):
        path = "$" + "".join(f"[{part}]" if isinstance(part, int) else f".{part}" for part in error.absolute_path)
        errors.append(f"{path}: {error.message}")
    return errors, True


def _semantic_errors(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    decisions = data.get("decisions", []) if isinstance(data.get("decisions"), list) else []
    commitments = data.get("commitments", []) if isinstance(data.get("commitments"), list) else []
    open_loops = data.get("open_loops", []) if isinstance(data.get("open_loops"), list) else []

    all_ids = [item.get("id") for item in decisions + commitments + open_loops if isinstance(item, dict)]
    if len(all_ids) != len(set(all_ids)):
        errors.append("$: decision, commitment, and open-loop IDs must be unique")
    id_set = set(all_ids)
    decision_id_set = {item.get("id") for item in decisions if isinstance(item, dict)}

    for index, decision in enumerate(decisions):
        if not isinstance(decision, dict):
            continue
        path = f"$.decisions[{index}]"
        status = decision.get("status")
        if status == "conditional" and not decision.get("condition"):
            errors.append(f"{path}.condition: conditional decision requires a condition")
        if status == "superseded":
            if decision.get("current") is not False:
                errors.append(f"{path}.current: superseded decision must be false")
            if decision.get("replaced_by") not in decision_id_set or decision.get("replaced_by") == decision.get("id"):
                errors.append(f"{path}.replaced_by: must reference a different existing decision")
        elif decision.get("replaced_by") is not None:
            errors.append(f"{path}.replaced_by: only superseded decisions may reference a replacement")
        if status in CORE_DECISIONS and decision.get("current") and decision.get("confidence") == "low":
            errors.append(f"{path}.confidence: current core decision cannot be low confidence")

    for index, commitment in enumerate(commitments):
        if not isinstance(commitment, dict):
            continue
        path = f"$.commitments[{index}]"
        kind = commitment.get("type")
        raw_missing = commitment.get("missing_fields", [])
        missing = set(raw_missing) if isinstance(raw_missing, list) else set()
        if kind == "unowned":
            if commitment.get("owner") is not None or commitment.get("owner_kind") != "unknown":
                errors.append(f"{path}: unowned item must have null owner and unknown owner_kind")
            if "owner" not in missing:
                errors.append(f"{path}.missing_fields: unowned item must include owner")
        if kind in {"unacknowledged_assignment", "implied_assignment"} and "confirmation" not in missing:
            errors.append(f"{path}.missing_fields: unconfirmed assignment must include confirmation")
        if kind == "conditional_commitment" and not commitment.get("dependencies"):
            errors.append(f"{path}.dependencies: conditional commitment requires at least one dependency")
        present_fields = {
            "owner": commitment.get("owner") is not None,
            "task": bool(commitment.get("task")),
            "due": bool(commitment.get("due_original") or commitment.get("due_resolved")),
            "dependencies": bool(commitment.get("dependencies")),
            "acceptance_criteria": bool(commitment.get("acceptance_criteria")),
        }
        for field, present in present_fields.items():
            if present and field in missing:
                errors.append(f"{path}.missing_fields: {field} is present and cannot also be marked missing")
        if kind in {"explicit_commitment", "accepted_assignment"} and commitment.get("confidence") == "low":
            errors.append(f"{path}.confidence: explicit or accepted commitment cannot be low confidence")

    for index, loop in enumerate(open_loops):
        if not isinstance(loop, dict):
            continue
        related_items = loop.get("related_items", [])
        for related in related_items if isinstance(related_items, list) else []:
            if related not in id_set:
                errors.append(f"$.open_loops[{index}].related_items: unknown reference {related}")

    expected = {
        "confirmed_decisions": sum(1 for item in decisions if isinstance(item, dict) and item.get("current") and item.get("status") in {"confirmed", "rejected"} and item.get("confidence") != "low"),
        "provisional_decisions": sum(1 for item in decisions if isinstance(item, dict) and item.get("current") and item.get("status") == "provisional" and item.get("confidence") != "low"),
        "conditional_decisions": sum(1 for item in decisions if isinstance(item, dict) and item.get("current") and item.get("status") == "conditional" and item.get("confidence") != "low"),
        "explicit_commitments": sum(1 for item in commitments if isinstance(item, dict) and item.get("type") in {"explicit_commitment", "accepted_assignment"} and item.get("confidence") != "low"),
        "unconfirmed_assignments": sum(1 for item in commitments if isinstance(item, dict) and item.get("type") in {"unacknowledged_assignment", "implied_assignment"}),
        "tentative_intents": sum(1 for item in commitments if isinstance(item, dict) and item.get("type") == "tentative_intent"),
        "open_loops": len(open_loops),
    }
    summary = data.get("summary", {})
    for key, value in expected.items():
        if summary.get(key) != value:
            errors.append(f"$.summary.{key}: expected {value}, got {summary.get(key)!r}")

    core_count = expected["confirmed_decisions"] + expected["provisional_decisions"] + expected["conditional_decisions"]
    close_status = data.get("close_status")
    if core_count == 0 and close_status not in {"no_clear_decision", "insufficient_evidence"}:
        errors.append("$.close_status: meetings without a current core decision must use no_clear_decision or insufficient_evidence")
    if close_status == "closed" and (open_loops or expected["unconfirmed_assignments"]):
        errors.append("$.close_status: closed cannot contain open loops or unconfirmed assignments")

    safety = data.get("safety", {})
    if isinstance(safety, dict):
        redactions = safety.get("redactions", 0)
        categories = safety.get("redaction_categories")
        if redactions == 0 and categories:
            errors.append("$.safety: redaction categories require redactions > 0")
        if isinstance(redactions, int) and redactions > 0 and not categories:
            errors.append("$.safety: redactions > 0 requires at least one category")

    _, sensitive_counts = redact_value(data)
    if sensitive_counts:
        categories = ", ".join(sorted(sensitive_counts))
        errors.append(f"$: unredacted sensitive values detected ({categories})")

    return errors


def validate_data(data: Any, schema: dict[str, Any]) -> tuple[list[str], str]:
    schema_errors, used_jsonschema = _jsonschema_errors(data, schema)
    if used_jsonschema:
        structure_errors = schema_errors
        engine = "jsonschema+semantic"
    else:
        structure_errors = _fallback_structure(data)
        engine = "stdlib-fallback+semantic"
    semantic_errors = _semantic_errors(data) if isinstance(data, dict) else []
    return structure_errors + semantic_errors, engine


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a meeting decision receipt.")
    parser.add_argument("input", help="Receipt JSON path")
    parser.add_argument("--schema", default=str(DEFAULT_SCHEMA), help="JSON Schema path")
    parser.add_argument("--json-report", help="Write a machine-readable validation report")
    args = parser.parse_args()

    try:
        data = json.loads(Path(args.input).read_text(encoding="utf-8"))
        schema = json.loads(Path(args.schema).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"validation input error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc

    errors, engine = validate_data(data, schema)
    report = {"valid": not errors, "engine": engine, "error_count": len(errors), "errors": errors}
    if args.json_report:
        Path(args.json_report).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if errors:
        print(f"receipt validation failed with {len(errors)} error(s) [{engine}]", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        raise SystemExit(1)

    print(f"receipt validation passed [{engine}]")


if __name__ == "__main__":
    main()
