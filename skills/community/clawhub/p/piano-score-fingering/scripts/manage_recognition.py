#!/usr/bin/env python3
"""Review, patch, confirm, and lock extracted piano score facts."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path

from plan_io import load_plan, save_plan
from recognition_state import open_review_items, score_facts_hash, set_fact_lock, verify_fact_lock
from validate_recognition import VISUAL_GATES, validate_recognition


PATCHABLE_RECOGNITION_FIELDS = {
    "expected_note_count", "unresolved_note_count", "event_count_checks", "systems", "scope",
    "measure_regions", "measure_symbol_checks",
    "measure_scope",
}
SEMANTIC_FIELDS = {
    "pitch_midi", "pitch_step", "pitch_alter", "pitch_octave", "duration", "onset",
    "staff", "voice", "hand", "chord_id", "chord_row", "chord_size", "tie_group",
    "tie_start", "tie_stop", "page", "page_x", "page_y", "staff_geometry_id",
    "symbol_class", "notehead_shape_verified", "sparse_symbol_verified", "origin",
    "chord_member_verified", "recognition_passes",
}


def _note_in_scope(note: dict, scope: dict) -> bool:
    pages = {int(value) for value in scope.get("pages", [])}
    measures = {int(value) for value in scope.get("measures", [])}
    hands = {str(value).upper() for value in scope.get("hands", [])}
    return (
        (not pages or int(note.get("page", 0)) in pages)
        and (not measures or int(note.get("measure_index", 0)) in measures)
        and (not hands or str(note.get("hand", "")).upper() in hands)
    )


def _invalidate_gates(recognition: dict, changed_fields: set[str], structural: bool) -> None:
    verification = recognition.setdefault("verification", {})
    if structural:
        for gate in (
            "scope_complete", "pitch_spelling", "pitch_geometry", "rhythm", "ties", "chords", "anchors"
        ):
            if gate in verification:
                verification[gate] = False
    if changed_fields & {"pitch_midi", "pitch_step", "pitch_octave", "staff", "page_y", "staff_geometry_id"}:
        verification["pitch_geometry"] = False
        verification["pitch_spelling"] = False
    if "pitch_alter" in changed_fields:
        verification["accidentals"] = False
        verification["pitch_spelling"] = False
    if changed_fields & {"duration", "onset", "voice"}:
        verification["rhythm"] = False
    if changed_fields & {"tie_group", "tie_start", "tie_stop"}:
        verification["ties"] = False
    if changed_fields & {"chord_id", "chord_row", "chord_size", "hand"}:
        verification["chords"] = False
    if changed_fields & {"page", "page_x", "page_y", "staff_geometry_id"}:
        verification["anchors"] = False


def create_review_queue(plan: dict) -> list[dict]:
    queue: list[dict] = []
    seen: set[str] = set()
    recognition = plan.get("recognition", {})
    threshold = float(recognition.get("review_confidence_threshold", 0.8))
    policy = recognition.get("confidence_policy", {})
    required_passes = int(policy.get("require_independent_passes", 0) or 0)
    grouped: dict[tuple, dict] = {}
    for note in plan.get("notes", []):
        reasons: list[str] = []
        reason = str(note.get("review_reason", "")).strip()
        if reason:
            reasons.append(reason)
        confidence = note.get("confidence")
        low_confidence = confidence is not None and float(confidence) < threshold
        if low_confidence:
            reasons.append(f"confidence={confidence}")
        passes = int(note.get("recognition_passes", 0) or 0)
        if required_passes and passes < required_passes:
            reasons.append(f"independent recognition passes={passes}, require {required_passes}")
        if not reasons:
            continue
        note_id = str(note.get("note_id", "unknown"))
        key = (note.get("page"), note.get("measure_index"), note.get("hand"))
        item = grouped.setdefault(key, {
            "review_id": f"scope:p{key[0]}-m{key[1]}-{str(key[2]).lower()}",
            "status": "open",
            "page": key[0],
            "measure": key[1],
            "hand": key[2],
            "note_ids": [],
            "reasons": [],
        })
        item["note_ids"].append(note_id)
        item["reasons"].extend(reasons)
    for item in grouped.values():
        item["note_ids"] = sorted(set(item["note_ids"]))
        reasons = sorted(set(item.pop("reasons")))
        item["reason"] = "; ".join(reasons)
        seen.add(str(item["review_id"]))
        queue.append(item)
    validation_plan = copy.deepcopy(plan)
    validation_plan.setdefault("recognition", {}).pop("review_queue", None)
    errors, warnings = validate_recognition(validation_plan, strict=True, require_locked=False)
    for message in errors + warnings:
        message_digest = hashlib.sha256(message.encode("utf-8")).hexdigest()[:12]
        item_id = f"validation:{message_digest}"
        if item_id in seen:
            continue
        queue.append({
            "review_id": item_id,
            "status": "open",
            "note_ids": [],
            "reason": message,
        })
    return queue


def command_queue(args: argparse.Namespace) -> int:
    plan = load_plan(args.input)
    queue = create_review_queue(plan)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({"review_queue": queue}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.plan_output:
        recognition = plan.setdefault("recognition", {})
        recognition.pop("fact_lock", None)
        recognition["status"] = "review"
        recognition["review_queue"] = queue
        save_plan(args.plan_output, plan)
    print(f"Wrote {len(queue)} review item(s) to {args.output}.")
    if args.plan_output:
        print(f"Embedded the queue in review-state plan: {args.plan_output}")
    return 0


def command_patch(args: argparse.Namespace) -> int:
    plan = load_plan(args.input)
    patch = json.loads(args.patch.read_text(encoding="utf-8"))
    if not isinstance(patch, dict) or not str(patch.get("reason", "")).strip():
        raise ValueError("patch must be an object with a non-empty reason")
    scope = patch.get("scope")
    if not isinstance(scope, dict) or not any(scope.get(key) for key in ("pages", "measures", "hands")):
        raise ValueError("patch.scope must restrict at least one of pages, measures, or hands")
    before = score_facts_hash(plan)
    notes = plan.get("notes", [])
    by_id = {str(note.get("note_id")): note for note in notes}
    changed_fields: set[str] = set()
    structural = False
    for operation in patch.get("operations", []):
        if not isinstance(operation, dict):
            raise ValueError("every patch operation must be an object")
        kind = str(operation.get("op", ""))
        note_id = str(operation.get("note_id", ""))
        if kind == "replace":
            if note_id not in by_id:
                raise ValueError(f"unknown note_id: {note_id}")
            note = by_id[note_id]
            if not _note_in_scope(note, scope):
                raise ValueError(f"{note_id} is outside patch.scope")
            changes = operation.get("changes")
            if not isinstance(changes, dict) or not changes:
                raise ValueError(f"{note_id}: replace requires non-empty changes")
            if "note_id" in changes:
                raise ValueError("replace cannot change stable note_id")
            note.update(changes)
            if not _note_in_scope(note, scope):
                raise ValueError(f"{note_id}: replacement moves the note outside patch.scope")
            changed_fields.update(changes)
        elif kind == "delete":
            if note_id not in by_id:
                raise ValueError(f"unknown note_id: {note_id}")
            note = by_id[note_id]
            if not _note_in_scope(note, scope):
                raise ValueError(f"{note_id} is outside patch.scope")
            notes.remove(note)
            by_id.pop(note_id)
            structural = True
        elif kind == "add":
            note = operation.get("note")
            if not isinstance(note, dict) or not str(note.get("note_id", "")):
                raise ValueError("add requires a note with note_id")
            if str(note["note_id"]) in by_id:
                raise ValueError(f"duplicate note_id: {note['note_id']}")
            if not _note_in_scope(note, scope):
                raise ValueError(f"{note['note_id']} is outside patch.scope")
            notes.append(note)
            by_id[str(note["note_id"])] = note
            structural = True
        else:
            raise ValueError(f"unsupported patch operation: {kind!r}")
    recognition = plan.setdefault("recognition", {})
    recognition_changes = patch.get("recognition_changes", {})
    if not isinstance(recognition_changes, dict):
        raise ValueError("recognition_changes must be an object")
    unexpected = set(recognition_changes) - PATCHABLE_RECOGNITION_FIELDS
    if unexpected:
        raise ValueError(f"recognition_changes contains unsupported fields: {sorted(unexpected)}")
    recognition.update(recognition_changes)
    changed_fields.update(SEMANTIC_FIELDS if recognition_changes else set())
    recognition.pop("fact_lock", None)
    recognition["status"] = "review"
    _invalidate_gates(recognition, changed_fields, structural)
    history = recognition.setdefault("patch_history", [])
    history.append({
        "reason": str(patch["reason"]),
        "scope": copy.deepcopy(scope),
        "operations": len(patch.get("operations", [])),
        "before_digest": before,
        "after_digest": score_facts_hash(plan),
    })
    save_plan(args.output, plan)
    print(f"Applied scoped patch; recognition returned to review state: {args.output}")
    return 0


def command_confirm(args: argparse.Namespace) -> int:
    plan = load_plan(args.input)
    recognition = plan.setdefault("recognition", {})
    verification = recognition.setdefault("verification", {})
    allowed = set(VISUAL_GATES) | {"pitch_spelling"}
    for gate in args.gates:
        if gate not in allowed:
            raise ValueError(f"unsupported verification gate: {gate}")
        verification[gate] = True
    resolved = set(args.resolve)
    for item in recognition.get("review_queue", []):
        if isinstance(item, dict) and str(item.get("review_id")) in resolved:
            item["status"] = "resolved"
    recognition["status"] = "verified"
    save_plan(args.output, plan)
    print(f"Confirmed {len(args.gates)} gate(s); recognition is verified but not locked: {args.output}")
    return 0


def command_freeze(args: argparse.Namespace) -> int:
    plan = load_plan(args.input)
    recognition = plan.setdefault("recognition", {})
    if open_review_items(plan):
        raise ValueError("open recognition.review_queue items must be resolved before locking")
    errors, warnings = validate_recognition(plan, strict=True, require_locked=False)
    for warning in warnings:
        print(f"WARNING: {warning}", file=sys.stderr)
    if errors:
        for error in errors[:args.max_errors]:
            print(f"ERROR: {error}", file=sys.stderr)
        if len(errors) > args.max_errors:
            print(
                f"ERROR: {len(errors) - args.max_errors} additional issue(s) omitted; "
                "run `manage_recognition.py queue` and repair the listed local scopes first.",
                file=sys.stderr,
            )
        return 1
    recognition["status"] = "verified"
    set_fact_lock(plan)
    save_plan(args.output, plan)
    print(f"Locked {len(plan.get('notes', []))} verified score facts: {args.output}")
    return 0


def command_status(args: argparse.Namespace) -> int:
    plan = load_plan(args.input)
    recognition = plan.get("recognition", {})
    lock_errors = verify_fact_lock(plan) if recognition.get("status") == "locked" else []
    print(json.dumps({
        "status": recognition.get("status", "draft"),
        "notes": len(plan.get("notes", [])),
        "open_reviews": len(open_review_items(plan)),
        "lock_valid": recognition.get("status") == "locked" and not lock_errors,
        "lock_errors": lock_errors,
    }, ensure_ascii=False, indent=2))
    return 1 if lock_errors else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    queue = subparsers.add_parser("queue", help="write a compact review queue")
    queue.add_argument("input", type=Path)
    queue.add_argument("-o", "--output", type=Path, required=True)
    queue.add_argument("--plan-output", type=Path, help="also embed the queue in a review-state plan")
    queue.set_defaults(func=command_queue)
    patch = subparsers.add_parser("patch", help="apply a scoped score-fact correction")
    patch.add_argument("input", type=Path)
    patch.add_argument("patch", type=Path)
    patch.add_argument("-o", "--output", type=Path, required=True)
    patch.set_defaults(func=command_patch)
    confirm = subparsers.add_parser("confirm", help="confirm locally rechecked gates")
    confirm.add_argument("input", type=Path)
    confirm.add_argument("--gates", nargs="+", required=True)
    confirm.add_argument("--resolve", nargs="*", default=[])
    confirm.add_argument("-o", "--output", type=Path, required=True)
    confirm.set_defaults(func=command_confirm)
    freeze = subparsers.add_parser("freeze", help="lock verified score facts")
    freeze.add_argument("input", type=Path)
    freeze.add_argument("-o", "--output", type=Path, required=True)
    freeze.add_argument("--max-errors", type=int, default=30, help="cap printed gate errors (default: 30)")
    freeze.set_defaults(func=command_freeze)
    status = subparsers.add_parser("status", help="show lock and review state")
    status.add_argument("input", type=Path)
    status.set_defaults(func=command_status)
    args = parser.parse_args()
    if getattr(args, "max_errors", 1) < 1:
        parser.error("--max-errors must be at least 1")
    return args.func(args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
