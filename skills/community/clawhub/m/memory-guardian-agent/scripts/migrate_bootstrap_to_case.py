#!/usr/bin/env python3
"""Migrate active bootstrap mem_* records into canonical case_* records."""

import argparse
import copy
import os
import sys
import uuid

from mg_utils import (
    _now_iso,
    classify_bootstrap_memory_type,
    is_bootstrap_memory_candidate,
    load_meta,
    save_meta,
    split_memory_heading,
)


DEFAULT_COST_FACTORS = {
    "write_cost": 0,
    "verify_cost": 0,
    "human_cost": 0,
    "transfer_cost": 0,
}

DEFAULT_QUALITY_GATE = {
    "confidence": 0.5,
    "gate_mode": "normal",
    "bypass_reason": None,
}


def _build_trigger_pattern(memory, heading):
    tags = set(memory.get("tags", []))
    if "bootstrapped" in tags and heading:
        return f"bootstrap: {heading}"
    if heading:
        return heading
    return "bootstrap"


def _build_context(memory, heading, body):
    context_parts = []
    if heading:
        context_parts.append(f"Original source: MEMORY.md section [{heading}]")
    if body:
        context_parts.append(f"Original body: {body[:300]}")
    if memory.get("failure_conditions"):
        context_parts.append(f"Known failures: {memory['failure_conditions']}")
    if memory.get("conflict_refs"):
        context_parts.append(f"Conflicts: {memory['conflict_refs']}")
    if memory.get("alternatives_considered"):
        context_parts.append(f"Alternatives: {memory['alternatives_considered']}")
    return "\n".join(context_parts)


def map_memory_to_case(memory, generated_id=None):
    """Map one bootstrapped mem_* record into a canonical case_* record."""
    now = _now_iso()
    heading, body = split_memory_heading(memory.get("content", ""))
    trigger_pattern = _build_trigger_pattern(memory, heading)
    case_id = generated_id or f"case_{uuid.uuid4().hex[:8]}"
    source = memory.get("source_case_id") or memory.get("provenance_source") or "bootstrap_migration"
    pinned = bool(memory.get("pinned") or memory.get("importance", 0) >= 0.9)

    case = {
        "id": case_id,
        "content": memory.get("content", ""),
        "importance": memory.get("importance", 0.5),
        "entities": memory.get("entities", []),
        "tags": list(dict.fromkeys(list(memory.get("tags", [])) + ["migrated", "v0.4.2"])),
        "created_at": memory.get("created_at", now),
        "last_accessed": memory.get("last_accessed", now),
        "access_count": memory.get("access_count", 0),
        "decay_score": memory.get("decay_score", memory.get("importance", 0.5)),
        "status": memory.get("status", "active"),
        "trigger": {
            "count": memory.get("trigger_count", 0),
            "last_triggered": memory.get("last_triggered"),
        },
        "trigger_pattern": trigger_pattern,
        "action": body,
        "context": _build_context(memory, heading, body),
        "confidence": memory.get("confidence", 0.5),
        "source": source,
        "case_type": memory.get("case_type", "case"),
        "reversibility": memory.get("reversibility", 1),
        "beta": memory.get("beta", 1.0),
        "trigger_count": memory.get("trigger_count", 0),
        "last_triggered": memory.get("last_triggered"),
        "cooling_threshold": memory.get("cooling_threshold", 5),
        "boundary_words": memory.get("boundary_words", []),
        "conflict_refs": memory.get("conflict_refs", []),
        "failure_conditions": memory.get("failure_conditions", []),
        "failure_count": memory.get("failure_count", 0),
        "last_failure_trigger": memory.get("last_failure_trigger"),
        "last_failure_fix": memory.get("last_failure_fix"),
        "source_case_id": memory.get("source_case_id"),
        "alternatives_considered": memory.get("alternatives_considered", []),
        "cost_factors": memory.get("cost_factors", DEFAULT_COST_FACTORS),
        "quality_gate": memory.get("quality_gate", DEFAULT_QUALITY_GATE),
        "importance_explain": memory.get("importance_explain"),
        "security_version": memory.get("security_version", 1),
        "cooldown_active": memory.get("cooldown_active", False),
        "cooldown_until": memory.get("cooldown_until"),
        "observing_since": memory.get("observing_since"),
        "suspended_pending_count": memory.get("suspended_pending_count", 0),
        "provenance_level": memory.get("provenance_level", "L1"),
        "provenance_source": memory.get("provenance_source", "bootstrap"),
        "memory_type": classify_bootstrap_memory_type(memory),
        "pinned": pinned,
        "migration_source": memory.get("id"),
        "schema_version": memory.get("schema_version", "v0.4.2"),
    }
    return case


def migrate_bootstrap_to_case(meta):
    """Return migrated meta plus summary without mutating the input."""
    migrated_meta = copy.deepcopy(meta)
    memories = migrated_meta.get("memories", [])
    migrated_memories = []
    migrated_cases = []
    skipped_count = 0
    conflicts = []
    seen_ids = {mem.get("id") for mem in memories if isinstance(mem, dict)}

    for memory in memories:
        if not is_bootstrap_memory_candidate(memory):
            migrated_memories.append(memory)
            skipped_count += 1
            continue

        case = map_memory_to_case(memory)
        while case["id"] in seen_ids:
            conflicts.append({"type": "duplicate_case_id", "id": case["id"], "source": memory.get("id")})
            case = map_memory_to_case(memory, generated_id=f"case_{uuid.uuid4().hex[:8]}")
        seen_ids.add(case["id"])
        migrated_memories.append(case)
        migrated_cases.append(case)

    migrated_meta["memories"] = migrated_memories
    return {
        "meta": migrated_meta,
        "cases": migrated_cases,
        "migrated_count": len(migrated_cases),
        "skipped_count": skipped_count,
        "conflicts": conflicts,
    }


def run(workspace, dry_run=False):
    meta_path = os.path.join(workspace, "memory", "meta.json")
    if not os.path.exists(meta_path):
        raise FileNotFoundError(f"meta.json not found: {meta_path}")

    meta = load_meta(meta_path)
    result = migrate_bootstrap_to_case(meta)
    if not dry_run and result["migrated_count"]:
        save_meta(meta_path, result["meta"])

    result["workspace"] = workspace
    result["meta_path"] = meta_path
    result["dry_run"] = dry_run
    return result


def build_parser():
    parser = argparse.ArgumentParser(description="Migrate active bootstrap memories into case records")
    parser.add_argument("--workspace", required=True, help="Workspace path")
    parser.add_argument("--dry-run", action="store_true", help="Preview without saving")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        result = run(args.workspace, dry_run=args.dry_run)
    except FileNotFoundError as exc:
        print(f"meta.json not found: {exc.filename or args.workspace}", file=sys.stderr)
        return 1

    print(f"Migrated: {result['migrated_count']}")
    print(f"Skipped: {result['skipped_count']}")
    print(f"Conflicts: {len(result['conflicts'])}")
    print(f"Dry run: {result['dry_run']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
