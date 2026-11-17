#!/usr/bin/env python3
"""Deterministic identity and lifecycle helpers for extracted score facts."""

from __future__ import annotations

import hashlib
import json
from typing import Any


LOCK_ALGORITHM = "sha256-score-facts"
RECOGNITION_STATES = {"draft", "review", "verified", "locked"}

# Fingering and label-layout fields are deliberately excluded.  The lock must
# survive fingering generation and placement changes while detecting any
# change to the score semantics or notehead anchors.
FACT_NOTE_FIELDS = (
    "note_id", "part", "measure", "measure_index", "staff", "voice",
    "onset", "duration", "pitch_midi", "pitch_step", "pitch_alter",
    "key_fifths", "key_mode", "key_signature_alter", "accidental_scope",
    "pitch_octave", "clef", "event_index", "chord_id", "chord_row", "chord_size",
    "hand", "keyboard_x_cm", "page", "page_x", "page_y",
    "staff_geometry_id", "anchor_verified", "anchor_method",
    "pitch_geometry_verified", "tie_group", "tie_start", "tie_stop",
    "symbol_class", "notehead_shape_verified", "sparse_symbol_verified",
    "origin", "chord_member_verified", "recognition_passes",
)


def _selected(record: dict[str, Any], fields: tuple[str, ...]) -> dict[str, Any]:
    return {field: record.get(field) for field in fields if field in record}


def score_fact_payload(plan: dict[str, Any]) -> dict[str, Any]:
    recognition = plan.get("recognition", {})
    notes = sorted(
        (_selected(note, FACT_NOTE_FIELDS) for note in plan.get("notes", []) if isinstance(note, dict)),
        key=lambda note: str(note.get("note_id", "")),
    )
    systems = sorted(
        (dict(system) for system in recognition.get("systems", []) if isinstance(system, dict)),
        key=lambda system: str(system.get("system_id", "")),
    )
    count_checks = sorted(
        (dict(check) for check in recognition.get("event_count_checks", []) if isinstance(check, dict)),
        key=lambda check: (
            int(check.get("page", 0)), int(check.get("measure", 0)), str(check.get("hand", ""))
        ),
    )
    measure_regions = sorted(
        (dict(region) for region in recognition.get("measure_regions", []) if isinstance(region, dict)),
        key=lambda region: str(region.get("region_id", "")),
    )
    measure_symbol_checks = sorted(
        (dict(check) for check in recognition.get("measure_symbol_checks", []) if isinstance(check, dict)),
        key=lambda check: str(check.get("region_id", "")),
    )
    rests = sorted(
        (dict(rest) for rest in plan.get("rests", []) if isinstance(rest, dict)),
        key=lambda rest: str(rest.get("rest_id", "")),
    )
    source = plan.get("source", {})
    return {
        "schema_version": plan.get("schema_version"),
        "source": {
            key: source.get(key)
            for key in ("type", "path", "member", "coordinate_unit")
            if key in source
        },
        "pages": plan.get("pages", []),
        "scope": recognition.get("scope"),
        "measure_scope": recognition.get("measure_scope", []),
        "expected_note_count": recognition.get("expected_note_count"),
        "unresolved_note_count": recognition.get("unresolved_note_count", 0),
        "source_assets": recognition.get("source_assets", []),
        "systems": systems,
        "event_count_checks": count_checks,
        "measure_regions": measure_regions,
        "measure_symbol_checks": measure_symbol_checks,
        "key_signatures": recognition.get("key_signatures", []),
        "rests": rests,
        "notes": notes,
    }


def score_facts_hash(plan: dict[str, Any]) -> str:
    encoded = json.dumps(
        score_fact_payload(plan), ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def open_review_items(plan: dict[str, Any]) -> list[dict[str, Any]]:
    items = plan.get("recognition", {}).get("review_queue", [])
    return [
        item for item in items
        if isinstance(item, dict) and str(item.get("status", "open")).lower() != "resolved"
    ]


def set_fact_lock(plan: dict[str, Any]) -> None:
    recognition = plan.setdefault("recognition", {})
    recognition["status"] = "locked"
    recognition["fact_lock"] = {
        "algorithm": LOCK_ALGORITHM,
        "digest": score_facts_hash(plan),
        "note_count": len(plan.get("notes", [])),
    }


def verify_fact_lock(plan: dict[str, Any]) -> list[str]:
    recognition = plan.get("recognition", {})
    errors: list[str] = []
    status = str(recognition.get("status", "draft")).lower()
    if status not in RECOGNITION_STATES:
        return [f"recognition.status must be one of {sorted(RECOGNITION_STATES)}"]
    if status != "locked":
        return ["recognition.status must be locked before fingering generation"]
    lock = recognition.get("fact_lock")
    if not isinstance(lock, dict):
        return ["recognition.fact_lock is required when status is locked"]
    if lock.get("algorithm") != LOCK_ALGORITHM:
        errors.append(f"recognition.fact_lock.algorithm must be {LOCK_ALGORITHM}")
    if int(lock.get("note_count", -1)) != len(plan.get("notes", [])):
        errors.append("recognition.fact_lock.note_count no longer matches notes")
    if str(lock.get("digest", "")) != score_facts_hash(plan):
        errors.append("score facts changed after locking; run a scoped review patch and lock again")
    return errors
