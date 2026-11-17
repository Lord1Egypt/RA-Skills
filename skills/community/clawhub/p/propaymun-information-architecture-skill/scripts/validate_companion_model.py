#!/usr/bin/env python3
"""Validate structural invariants in ProPaymun product-sitemap and user-flow JSON."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict, deque
from pathlib import Path
from typing import Any


EVIDENCE_STATES = {"Provided", "Observed", "Confirmed", "Inferred", "Proposed", "Unknown"}
MODEL_STATUSES = {"draft", "proposed", "reviewed", "approved"}
READINESS_STATES = {"not-ready", "provisional", "reviewable", "approved"}
SOURCE_TYPES = {"ia-reference-lock", "minimum-semantic-substrate"}
DESTINATION_KINDS = {"root", "hub", "collection", "detail", "workspace", "utility", "external"}


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def mapping(value: Any, name: str, errors: list[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        errors.append(f"{name} must be an object")
        return {}
    return value


def array(value: Any, name: str, errors: list[str]) -> list[Any]:
    if not isinstance(value, list):
        errors.append(f"{name} must be an array")
        return []
    return value


def records(value: Any, name: str, errors: list[str]) -> tuple[list[dict[str, Any]], set[str]]:
    result: list[dict[str, Any]] = []
    identifiers: set[str] = set()
    for index, raw in enumerate(array(value, name, errors)):
        record = mapping(raw, f"{name}[{index}]", errors)
        identifier = record.get("id")
        if not nonempty(identifier):
            errors.append(f"{name}[{index}].id must be a non-empty string")
            continue
        if identifier in identifiers:
            errors.append(f"duplicate {name} id: {identifier}")
        identifiers.add(identifier)
        result.append(record)
    return result, identifiers


def evidence(owner: str, value: Any, errors: list[str]) -> None:
    if value not in EVIDENCE_STATES:
        errors.append(f"{owner} has invalid evidence_status: {value!r}")


def validate_meta(root: dict[str, Any], artifact_type: str, errors: list[str]) -> dict[str, Any]:
    meta = mapping(root.get("meta"), "meta", errors)
    for field in ("title", "artifact_type", "artifact_version", "status", "language", "scope"):
        if not nonempty(meta.get(field)):
            errors.append(f"meta.{field} must be a non-empty string")
    if meta.get("artifact_type") != artifact_type:
        errors.append(f"meta.artifact_type must be {artifact_type!r}")
    if meta.get("artifact_version") != "1.0":
        errors.append("meta.artifact_version must be '1.0'")
    if meta.get("status") not in MODEL_STATUSES:
        errors.append(f"meta.status must be one of: {', '.join(sorted(MODEL_STATUSES))}")
    if meta.get("direction") not in {"ltr", "rtl", "vertical"}:
        errors.append("meta.direction must be 'ltr', 'rtl', or 'vertical'")
    source = mapping(meta.get("source"), "meta.source", errors)
    if source.get("type") not in SOURCE_TYPES:
        errors.append(f"meta.source.type must be one of: {', '.join(sorted(SOURCE_TYPES))}")
    for field in ("reference_id", "version"):
        if not nonempty(source.get(field)):
            errors.append(f"meta.source.{field} must be a non-empty string")
    if source.get("readiness") not in READINESS_STATES:
        errors.append(f"meta.source.readiness must be one of: {', '.join(sorted(READINESS_STATES))}")
    return meta


def validate_sitemap(root: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    validate_meta(root, "product-sitemap", errors)
    destinations, destination_ids = records(root.get("destinations"), "destinations", errors)
    links, _ = records(root.get("links", []), "links", errors)
    if not destinations:
        errors.append("product sitemap must contain at least one destination")

    parents: dict[str, str | None] = {}
    children: dict[str, list[str]] = defaultdict(list)
    for destination in destinations:
        identifier = destination["id"]
        for field in ("label", "purpose", "access_scope"):
            if not nonempty(destination.get(field)):
                errors.append(f"destination {identifier} {field} must be a non-empty string")
        if destination.get("destination_kind") not in DESTINATION_KINDS:
            errors.append(f"destination {identifier} has invalid destination_kind: {destination.get('destination_kind')!r}")
        refs = destination.get("semantic_refs")
        if not isinstance(refs, list) or not refs or any(not nonempty(value) for value in refs):
            errors.append(f"destination {identifier} semantic_refs must be a non-empty array of strings")
        parent = destination.get("parent_id")
        if parent is not None and not nonempty(parent):
            errors.append(f"destination {identifier} parent_id must be null or a non-empty string")
        parents[identifier] = parent
        if nonempty(parent):
            children[parent].append(identifier)
        evidence(f"destination {identifier}", destination.get("evidence_status"), errors)

    for identifier, parent in parents.items():
        if parent is not None and parent not in destination_ids:
            errors.append(f"destination {identifier} references missing parent: {parent}")
    for start in destination_ids:
        seen: set[str] = set()
        current: str | None = start
        while current is not None and current in parents:
            if current in seen:
                errors.append(f"sitemap hierarchy cycle detected at destination: {current}")
                break
            seen.add(current)
            current = parents[current]

    roots = [identifier for identifier, parent in parents.items() if parent is None]
    if not roots:
        errors.append("product sitemap must contain at least one root destination")
    if len(roots) > 1:
        warnings.append("product sitemap has multiple roots; confirm that this is intentional")

    for link in links:
        identifier = link["id"]
        for endpoint in ("from", "to"):
            if link.get(endpoint) not in destination_ids:
                errors.append(f"link {identifier} references missing {endpoint} destination: {link.get(endpoint)!r}")
        if link.get("type") not in {"cross-link", "contextual-entry", "external-boundary"}:
            errors.append(f"link {identifier} has invalid type: {link.get('type')!r}")
        evidence(f"link {identifier}", link.get("evidence_status"), errors)

    for collection_name in ("views", "states"):
        collection, _ = records(root.get(collection_name, []), collection_name, errors)
        for record in collection:
            identifier = record["id"]
            if not nonempty(record.get("label")):
                errors.append(f"{collection_name[:-1]} {identifier} label must be a non-empty string")
            if record.get("destination_id") not in destination_ids:
                errors.append(f"{collection_name[:-1]} {identifier} references missing destination: {record.get('destination_id')!r}")
            evidence(f"{collection_name[:-1]} {identifier}", record.get("evidence_status"), errors)

    capabilities, _ = records(root.get("capabilities", []), "capabilities", errors)
    for capability in capabilities:
        identifier = capability["id"]
        if not nonempty(capability.get("label")):
            errors.append(f"capability {identifier} label must be a non-empty string")
        destinations_for_capability = capability.get("destination_ids")
        if not isinstance(destinations_for_capability, list) or not destinations_for_capability:
            errors.append(f"capability {identifier} destination_ids must be a non-empty array")
        else:
            for destination_id in destinations_for_capability:
                if destination_id not in destination_ids:
                    errors.append(f"capability {identifier} references missing destination: {destination_id!r}")
        refs = capability.get("semantic_refs")
        if not isinstance(refs, list) or not refs or any(not nonempty(value) for value in refs):
            errors.append(f"capability {identifier} semantic_refs must be a non-empty array of strings")
        evidence(f"capability {identifier}", capability.get("evidence_status"), errors)
    return sorted(set(errors)), sorted(set(warnings))


def validate_user_flow(root: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    meta = validate_meta(root, "user-flow", errors)
    if not nonempty(meta.get("goal")):
        errors.append("meta.goal must be a non-empty string")
    actors, actor_ids = records(root.get("actors"), "actors", errors)
    steps, step_ids = records(root.get("steps"), "steps", errors)
    transitions, _ = records(root.get("transitions"), "transitions", errors)
    if not actors:
        errors.append("user flow must contain at least one actor")
    if len(steps) < 2:
        errors.append("user flow must contain at least two steps")

    step_types = {step["id"]: step.get("type") for step in steps}
    outgoing: dict[str, list[dict[str, Any]]] = defaultdict(list)
    adjacency: dict[str, list[str]] = defaultdict(list)
    allowed_step_types = {"action", "system-response", "decision", "state", "success", "failure", "recovery", "cancellation", "exit", "handoff"}
    for actor in actors:
        if not nonempty(actor.get("label")):
            errors.append(f"actor {actor['id']} label must be a non-empty string")
        evidence(f"actor {actor['id']}", actor.get("evidence_status"), errors)
    for step in steps:
        identifier = step["id"]
        if step.get("type") not in allowed_step_types:
            errors.append(f"step {identifier} has invalid type: {step.get('type')!r}")
        if not nonempty(step.get("label")):
            errors.append(f"step {identifier} label must be a non-empty string")
        actor_id = step.get("actor_id")
        if actor_id is not None and actor_id not in actor_ids:
            errors.append(f"step {identifier} references missing actor: {actor_id!r}")
        refs = step.get("semantic_refs")
        if not isinstance(refs, list) or any(not nonempty(value) for value in refs):
            errors.append(f"step {identifier} semantic_refs must be an array of strings")
        evidence(f"step {identifier}", step.get("evidence_status"), errors)

    allowed_transition_kinds = {"main", "alternative", "error", "recovery", "cancel"}
    for transition in transitions:
        identifier = transition["id"]
        start = transition.get("from")
        end = transition.get("to")
        if start not in step_ids:
            errors.append(f"transition {identifier} references missing from step: {start!r}")
        if end not in step_ids:
            errors.append(f"transition {identifier} references missing to step: {end!r}")
        if start in step_ids and end in step_ids:
            outgoing[start].append(transition)
            adjacency[start].append(end)
        if transition.get("kind") not in allowed_transition_kinds:
            errors.append(f"transition {identifier} has invalid kind: {transition.get('kind')!r}")
        evidence(f"transition {identifier}", transition.get("evidence_status"), errors)

    entry = root.get("entry_step_id")
    if entry not in step_ids:
        errors.append(f"entry_step_id references missing step: {entry!r}")
    successes = root.get("success_conditions")
    if not isinstance(successes, list) or not successes or any(not nonempty(value) for value in successes):
        errors.append("success_conditions must be a non-empty array of strings")
    if "success" not in step_types.values():
        errors.append("user flow must contain at least one success step")

    for identifier, step_type in step_types.items():
        if step_type in {"action", "handoff"}:
            step = next(record for record in steps if record["id"] == identifier)
            if step.get("actor_id") not in actor_ids:
                errors.append(f"{step_type} step {identifier} must reference an existing actor")
        if step_type == "decision":
            branches = outgoing[identifier]
            if len(branches) < 2:
                errors.append(f"decision step {identifier} must have at least two outgoing transitions")
            conditions = [branch.get("condition") for branch in branches]
            if any(not nonempty(condition) for condition in conditions):
                errors.append(f"decision step {identifier} must label every outgoing condition")
            normalized = [condition.strip().casefold() for condition in conditions if nonempty(condition)]
            if len(normalized) != len(set(normalized)):
                errors.append(f"decision step {identifier} must use distinct outgoing conditions")
        if step_type == "failure" and not any(t.get("kind") == "recovery" for t in outgoing[identifier]):
            step = next(record for record in steps if record["id"] == identifier)
            if step.get("terminal") is not True:
                errors.append(f"failure step {identifier} needs a recovery transition or terminal=true")
        if step_type not in {"success", "exit", "cancellation"} and not outgoing[identifier]:
            warnings.append(f"non-terminal step has no outgoing transition: {identifier}")

    if entry in step_ids:
        reached: set[str] = {entry}
        queue: deque[str] = deque([entry])
        while queue:
            current = queue.popleft()
            for target in adjacency[current]:
                if target not in reached:
                    reached.add(target)
                    queue.append(target)
        for identifier in sorted(step_ids - reached):
            errors.append(f"unreachable flow step: {identifier}")
    return sorted(set(errors)), sorted(set(warnings))


def validate(data: Any) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    root = mapping(data, "document", errors)
    meta = root.get("meta") if isinstance(root.get("meta"), dict) else {}
    artifact_type = meta.get("artifact_type")
    if artifact_type == "product-sitemap":
        nested_errors, warnings = validate_sitemap(root)
    elif artifact_type == "user-flow":
        nested_errors, warnings = validate_user_flow(root)
    else:
        nested_errors, warnings = ["meta.artifact_type must be 'product-sitemap' or 'user-flow'"], []
    return sorted(set(errors + nested_errors)), warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", type=Path, help="Path to a product-sitemap or user-flow JSON file")
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
    errors, warnings = validate(data)
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
