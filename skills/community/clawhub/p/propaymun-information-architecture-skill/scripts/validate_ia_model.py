#!/usr/bin/env python3
"""Validate structural invariants in a ProPaymun Semantic IA 2.0 JSON file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


EVIDENCE_STATES = {"Provided", "Observed", "Confirmed", "Inferred", "Proposed", "Unknown"}
MODEL_STATUSES = {"draft", "proposed", "reviewed", "approved"}
READINESS_STATES = {"not-ready", "provisional", "reviewable", "approved"}
ITEM_KINDS = {"object", "content_type", "record", "concept", "classification", "retrieval_system"}
HANDOFF_PURPOSES = {"conversation", "workshop", "review", "implementation"}


def _mapping(value: Any, name: str, errors: list[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        errors.append(f"{name} must be an object")
        return {}
    return value


def _list(value: Any, name: str, errors: list[str]) -> list[Any]:
    if not isinstance(value, list):
        errors.append(f"{name} must be an array")
        return []
    return value


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _evidence(owner: str, value: Any, errors: list[str]) -> None:
    if value not in EVIDENCE_STATES:
        errors.append(f"{owner} has invalid evidence_status: {value!r}")


def _unique_records(records: list[Any], name: str, errors: list[str]) -> tuple[list[dict[str, Any]], set[str]]:
    clean: list[dict[str, Any]] = []
    identifiers: set[str] = set()
    for index, raw in enumerate(records):
        record = _mapping(raw, f"{name}[{index}]", errors)
        identifier = record.get("id")
        if not _nonempty(identifier):
            errors.append(f"{name}[{index}].id must be a non-empty string")
            continue
        if identifier in identifiers:
            errors.append(f"duplicate {name} id: {identifier}")
        identifiers.add(identifier)
        clean.append(record)
    return clean, identifiers


def validate_model(data: Any) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    root = _mapping(data, "document", errors)
    meta = _mapping(root.get("meta"), "meta", errors)

    for field in ("title", "model_version", "status", "language", "scope"):
        if not _nonempty(meta.get(field)):
            errors.append(f"meta.{field} must be a non-empty string")
    if meta.get("model_version") != "2.0":
        errors.append("meta.model_version must be '2.0'")
    if meta.get("status") not in MODEL_STATUSES:
        errors.append(f"meta.status must be one of: {', '.join(sorted(MODEL_STATUSES))}")
    if meta.get("direction") not in {"ltr", "rtl"}:
        errors.append("meta.direction must be 'ltr' or 'rtl'")
    if meta.get("problem_shape") is not None and meta.get("problem_shape") not in {"content-taxonomy", "object-operation", "hybrid"}:
        errors.append("meta.problem_shape must be content-taxonomy, object-operation, or hybrid")

    handoff = _mapping(meta.get("handoff"), "meta.handoff", errors)
    if handoff.get("readiness") not in READINESS_STATES:
        errors.append(f"meta.handoff.readiness must be one of: {', '.join(sorted(READINESS_STATES))}")
    if handoff.get("purpose") not in HANDOFF_PURPOSES:
        errors.append(f"meta.handoff.purpose must be one of: {', '.join(sorted(HANDOFF_PURPOSES))}")

    domains, domain_ids = _unique_records(_list(root.get("domains"), "domains", errors), "domains", errors)
    items, item_ids = _unique_records(_list(root.get("items"), "items", errors), "items", errors)
    relationships, _ = _unique_records(_list(root.get("relationships"), "relationships", errors), "relationships", errors)
    roles_raw = root.get("roles", [])
    roles, role_ids = _unique_records(_list(roles_raw, "roles", errors), "roles", errors)

    if not domains:
        errors.append("model must contain at least one information domain")
    if not items:
        errors.append("model must contain at least one item")

    for domain in domains:
        domain_id = domain["id"]
        if not _nonempty(domain.get("label")):
            errors.append(f"domain {domain_id} label must be a non-empty string")
        _evidence(f"domain {domain_id}", domain.get("evidence_status"), errors)

    parent_by_id: dict[str, str | None] = {}
    for item in items:
        item_id = item["id"]
        if item.get("domain_id") not in domain_ids:
            errors.append(f"item {item_id} references missing domain: {item.get('domain_id')!r}")
        for field in ("label", "kind"):
            if not _nonempty(item.get(field)):
                errors.append(f"item {item_id} {field} must be a non-empty string")
        if item.get("kind") not in ITEM_KINDS:
            errors.append(f"item {item_id} kind must be one of: {', '.join(sorted(ITEM_KINDS))}")
        parent = item.get("parent_id")
        if parent is not None and not isinstance(parent, str):
            errors.append(f"item {item_id} parent_id must be a string or null")
        parent_by_id[item_id] = parent
        alternatives = item.get("alternative_parent_ids", [])
        if not isinstance(alternatives, list) or any(not isinstance(value, str) for value in alternatives):
            errors.append(f"item {item_id} alternative_parent_ids must be an array of strings")
        _evidence(f"item {item_id}", item.get("evidence_status"), errors)

    for item_id, parent_id in parent_by_id.items():
        if parent_id is not None and parent_id not in item_ids:
            errors.append(f"item {item_id} references missing parent: {parent_id}")
    for item in items:
        for parent_id in item.get("alternative_parent_ids", []):
            if parent_id not in item_ids:
                errors.append(f"item {item['id']} references missing alternative parent: {parent_id}")

    for start in item_ids:
        seen: set[str] = set()
        current: str | None = start
        while current is not None and current in parent_by_id:
            if current in seen:
                errors.append(f"hierarchy cycle detected at item: {current}")
                break
            seen.add(current)
            current = parent_by_id[current]

    for relationship in relationships:
        relationship_id = relationship["id"]
        for endpoint in ("from", "to"):
            if relationship.get(endpoint) not in item_ids:
                errors.append(f"relationship {relationship_id} references missing {endpoint} item: {relationship.get(endpoint)!r}")
        for field in ("type", "label", "meaning"):
            if not _nonempty(relationship.get(field)):
                errors.append(f"relationship {relationship_id} {field} must be a non-empty string")
        if relationship.get("direction") not in {"directed", "bidirectional", "undirected"}:
            errors.append(f"relationship {relationship_id} direction must be directed, bidirectional, or undirected")
        _evidence(f"relationship {relationship_id}", relationship.get("evidence_status"), errors)

    for role in roles:
        role_id = role["id"]
        if not _nonempty(role.get("label")):
            errors.append(f"role {role_id} label must be a non-empty string")
        _evidence(f"role {role_id}", role.get("evidence_status"), errors)
        if "/" in str(role.get("label", "")):
            warnings.append(f"role {role_id} combines labels with '/'; confirm that permissions are genuinely equivalent")

    permissions = _list(root.get("permissions", []), "permissions", errors)
    for index, raw in enumerate(permissions):
        permission = _mapping(raw, f"permissions[{index}]", errors)
        if permission.get("role_id") not in role_ids:
            errors.append(f"permissions[{index}] references missing role: {permission.get('role_id')!r}")
        if permission.get("item_id") not in item_ids:
            errors.append(f"permissions[{index}] references missing item: {permission.get('item_id')!r}")
        if not _nonempty(permission.get("scope")):
            errors.append(f"permissions[{index}].scope must be a non-empty string")
        actions = permission.get("actions")
        if not isinstance(actions, list) or not actions or any(not _nonempty(action) for action in actions):
            errors.append(f"permissions[{index}].actions must be a non-empty array of strings")
        _evidence(f"permissions[{index}]", permission.get("evidence_status"), errors)

    information_needs, _ = _unique_records(_list(root.get("information_needs", []), "information_needs", errors), "information_needs", errors)
    for need in information_needs:
        need_id = need["id"]
        for field in ("audience_or_context", "information_sought", "access_scope", "recovery"):
            if not _nonempty(need.get(field)):
                errors.append(f"information need {need_id} {field} must be a non-empty string")
        for field in ("entry_points", "item_ids"):
            values = need.get(field)
            if not isinstance(values, list) or not values or any(not _nonempty(value) for value in values):
                errors.append(f"information need {need_id} {field} must be a non-empty array of strings")
        cues = need.get("organizing_cues", [])
        if not isinstance(cues, list) or any(not _nonempty(value) for value in cues):
            errors.append(f"information need {need_id} organizing_cues must be an array of non-empty strings")
        for item_id in need.get("item_ids", []) if isinstance(need.get("item_ids"), list) else []:
            if item_id not in item_ids:
                errors.append(f"information need {need_id} references missing item: {item_id!r}")
        _evidence(f"information need {need_id}", need.get("evidence_status"), errors)

    lifecycles = _list(root.get("lifecycles", []), "lifecycles", errors)
    for index, raw in enumerate(lifecycles):
        lifecycle = _mapping(raw, f"lifecycles[{index}]", errors)
        item_id = lifecycle.get("item_id")
        if item_id not in item_ids:
            errors.append(f"lifecycles[{index}] references missing item: {item_id!r}")
        states, state_ids = _unique_records(_list(lifecycle.get("states"), f"lifecycles[{index}].states", errors), f"lifecycles[{index}].states", errors)
        for state in states:
            if not _nonempty(state.get("label")):
                errors.append(f"lifecycle state {state['id']} label must be a non-empty string")
        transitions = _list(lifecycle.get("transitions"), f"lifecycles[{index}].transitions", errors)
        for transition_index, raw_transition in enumerate(transitions):
            transition = _mapping(raw_transition, f"lifecycles[{index}].transitions[{transition_index}]", errors)
            for endpoint in ("from", "to"):
                if transition.get(endpoint) not in state_ids:
                    errors.append(f"lifecycle {item_id} transition references missing {endpoint} state: {transition.get(endpoint)!r}")
            actors = transition.get("actor_role_ids")
            if not isinstance(actors, list):
                errors.append(f"lifecycle {item_id} transition actor_role_ids must be an array")
            else:
                for role_id in actors:
                    if role_id not in role_ids:
                        errors.append(f"lifecycle {item_id} transition references missing role: {role_id!r}")
            _evidence(f"lifecycle {item_id} transition", transition.get("evidence_status"), errors)

    unknowns = _list(root.get("unknowns", []), "unknowns", errors)
    if handoff.get("readiness") in {"provisional", "reviewable", "approved"}:
        for unknown in unknowns:
            if isinstance(unknown, dict) and unknown.get("blocks_handoff") is True:
                errors.append(f"handoff is {handoff.get('readiness')} but blocking unknown remains: {unknown.get('id', 'unnamed')}")

    if items and not any(parent is None for parent in parent_by_id.values()):
        warnings.append("hierarchy has no root item")

    return sorted(set(errors)), sorted(set(warnings))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", type=Path, help="Path to Semantic IA 2.0 JSON")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable results")
    args = parser.parse_args()

    try:
        data = json.loads(args.model.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"ERROR: file not found: {args.model}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid JSON: {exc}", file=sys.stderr)
        return 2

    errors, warnings = validate_model(data)
    if args.json:
        print(json.dumps({"valid": not errors, "errors": errors, "warnings": warnings}, indent=2))
    else:
        for warning in warnings:
            print(f"WARNING: {warning}")
        for error in errors:
            print(f"ERROR: {error}")
        print("VALID" if not errors else "INVALID")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
