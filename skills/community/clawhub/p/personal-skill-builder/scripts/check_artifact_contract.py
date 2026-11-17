#!/usr/bin/env python3
"""Check task-specific raw/final artifact constraints without invoking a model.

Only trusted, authored contracts may contain regexes. This tool checks declared
properties and file integrity; it cannot certify evidence provenance or semantics.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from pathlib import Path
from typing import Any


class ContractError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def reject_constant(value: str) -> None:
    raise ContractError("JSON contains a non-finite numeric constant")


def finite_number(value: Any) -> bool:
    return type(value) is int or (type(value) is float and math.isfinite(value))


def pointer_values(value: Any, pointer: str) -> list[Any]:
    """JSON Pointer plus * for every element of an array (not object keys)."""
    require(pointer == "" or pointer.startswith("/"), "invalid JSON pointer")
    values = [value]
    for raw_token in pointer.split("/")[1:]:
        require(re.search(r"~(?![01])", raw_token) is None, "invalid pointer escape")
        token = raw_token.replace("~1", "/").replace("~0", "~")
        selected = []
        for current in values:
            if token == "*":
                require(isinstance(current, list), "wildcard requires an array")
                selected.extend(current)
            elif isinstance(current, dict):
                require(token in current, "required JSON field missing")
                selected.append(current[token])
            elif isinstance(current, list):
                require(token.isdecimal() and int(token) < len(current), "array index missing")
                selected.append(current[int(token)])
            else:
                raise ContractError("JSON pointer cannot traverse scalar")
        values = selected
    return values


def check_one(check: dict[str, Any], text: str, data: Any) -> bool:
    kind = check.get("type")
    if kind in {"contains", "not_contains", "regex", "not_regex"}:
        value = check.get("value")
        require(isinstance(value, str) and bool(value), "text check value must be nonempty")
        if kind == "contains":
            return value in text
        if kind == "not_contains":
            return value not in text
        try:
            found = re.search(value, text, flags=re.MULTILINE) is not None
        except re.error as exc:
            raise ContractError("invalid authored regex") from exc
        return found if kind == "regex" else not found
    require(kind == "number_domain", "unknown check type")
    pointer = check.get("pointer")
    require(isinstance(pointer, str), "number_domain requires pointer")
    for option in ("allow_null", "allow_empty", "integer"):
        require(isinstance(check.get(option, False), bool), f"{option} must be boolean")
    bounds = {}
    for key in ("minimum", "maximum"):
        if key in check:
            bound = check[key]
            require(finite_number(bound), "invalid numeric bound")
            bounds[key] = bound
    require(not ("minimum" in bounds and "maximum" in bounds and bounds["minimum"] > bounds["maximum"]), "inverted numeric bounds")
    # An empty dataset does not make an invalid contract valid. Validate all
    # options and bounds before honoring the explicitly allowed empty case.
    values = pointer_values(data, pointer)
    if not values:
        return check.get("allow_empty", False)
    for value in values:
        if value is None and check.get("allow_null", False):
            continue
        if not finite_number(value):
            return False
        if check.get("integer", False) and value != int(value):
            return False
        if "minimum" in bounds and value < bounds["minimum"]:
            return False
        if "maximum" in bounds and value > bounds["maximum"]:
            return False
    return True


def evaluate(contract_path: Path) -> dict[str, Any]:
    contract = json.loads(contract_path.read_text(encoding="utf-8-sig"), parse_constant=reject_constant)
    require(isinstance(contract, dict) and contract.get("schema_version") == 1, "unsupported contract schema")
    stages = contract.get("required_stages")
    require(isinstance(stages, list) and bool(stages) and all(isinstance(x, str) and bool(x) for x in stages), "required_stages must be nonempty strings")
    require(len(set(stages)) == len(stages), "duplicate required stage")
    artifacts = contract.get("artifacts")
    require(isinstance(artifacts, list) and bool(artifacts), "artifacts must be nonempty")
    results = []
    ids: set[str] = set()
    paths: set[Path] = set()
    covered: set[str] = set()
    for artifact in artifacts:
        require(isinstance(artifact, dict), "artifact must be an object")
        artifact_id, stage = artifact.get("id"), artifact.get("stage")
        require(isinstance(artifact_id, str) and bool(artifact_id) and artifact_id not in ids, "artifact id missing or duplicated")
        require(stage in stages, "artifact stage not declared")
        ids.add(artifact_id)
        source = artifact.get("path")
        require(isinstance(source, str) and bool(source), "artifact path missing")
        path = (contract_path.parent / source).resolve()
        require(path not in paths, "different artifact stages require separately preserved files")
        paths.add(path)
        checks = artifact.get("checks")
        require(isinstance(checks, list) and bool(checks), "artifact checks must be nonempty")
        try:
            raw = path.read_bytes()
            text = raw.decode("utf-8-sig")
            require(bool(text.strip()), "artifact is empty")
            source_format = artifact.get("format", "text")
            require(source_format in {"text", "json"}, "unsupported artifact format")
            data = json.loads(text, parse_constant=reject_constant) if source_format == "json" else None
            outcomes = []
            check_ids: set[str] = set()
            for check in checks:
                require(isinstance(check, dict), "check must be an object")
                check_id = check.get("id")
                require(isinstance(check_id, str) and bool(check_id) and check_id not in check_ids, "check id missing or duplicated")
                check_ids.add(check_id)
                require(check.get("type") != "number_domain" or source_format == "json", "number_domain requires JSON artifact")
                outcomes.append({"id": check_id, "passed": check_one(check, text, data)})
            passed = all(item["passed"] for item in outcomes)
            results.append({"id": artifact_id, "stage": stage, "path": str(path), "sha256": hashlib.sha256(raw).hexdigest(), "passed": passed, "checks": outcomes})
            covered.add(stage)
        except (OSError, UnicodeError, ValueError, OverflowError, TypeError) as exc:
            # Do not echo document text, prohibited values or regex matches.
            results.append({"id": artifact_id, "stage": stage, "path": str(path), "passed": False, "error_type": type(exc).__name__})
    missing = sorted(set(stages) - covered)
    passed = not missing and all(item["passed"] for item in results)
    return {"schema_version": 1, "kind": "declared_artifact_contract", "passed": passed, "missing_stages": missing, "artifacts": results, "limits": "Checks only declared properties; independent semantic and provenance review still required."}


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("contract", type=Path)
    args = parser.parse_args()
    try:
        report = evaluate(args.contract.resolve())
    except (OSError, UnicodeError, ValueError, OverflowError, TypeError):
        # Fail closed without disclosing source contents in parser diagnostics.
        report = {"schema_version": 1, "passed": False, "error": "Invalid or unreadable artifact contract"}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
