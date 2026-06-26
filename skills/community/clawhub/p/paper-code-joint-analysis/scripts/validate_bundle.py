#!/usr/bin/env python3
"""Validate analysis_bundle.json for paper-code-joint-analysis.

This deliberately uses only Python's standard library. It validates the stable
contract the skill depends on rather than the entire JSON Schema vocabulary.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "paper-code-joint-analysis.v1"
TOP_LEVEL_REQUIRED = [
    "schema_version",
    "intake",
    "paper_questions",
    "domain_critical_execution",
    "mechanisms",
    "experiments",
    "implementation_omissions",
    "diagrams",
    "modify_guide",
    "validation",
]
EXPERIMENT_STATUSES = {"direct", "manual-matrix", "approximate", "requires-code-edit", "unsupported"}
VALIDATION_STATUSES = {"pass", "fail", "unresolved"}
FINAL_STATUSES = {"pass", "pass_with_unresolved", "fail"}
QUESTION_STATUSES = {"answered_by_code", "partly_answered_by_code", "not_answered", "contradiction", "reasonable_inference"}


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def is_nonempty_list(value: Any) -> bool:
    return isinstance(value, list) and len(value) > 0


def validate_code_indices(mech: dict[str, Any], errors: list[str], prefix: str) -> None:
    indices = mech.get("code_indices")
    require(is_nonempty_list(indices), errors, f"{prefix}.code_indices must be a non-empty list")
    if not isinstance(indices, list):
        return
    for i, item in enumerate(indices):
        ip = f"{prefix}.code_indices[{i}]"
        require(is_nonempty_string(item.get("path")), errors, f"{ip}.path is required")
        require(is_nonempty_list(item.get("symbols")), errors, f"{ip}.symbols must be non-empty")
        require(is_nonempty_string(item.get("role")), errors, f"{ip}.role is required")


def validate_bundle(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    for key in TOP_LEVEL_REQUIRED:
        require(key in data, errors, f"missing top-level key: {key}")
    if errors:
        return errors

    require(data.get("schema_version") == SCHEMA_VERSION, errors, f"schema_version must be {SCHEMA_VERSION}")

    intake = data.get("intake", {})
    require(isinstance(intake, dict), errors, "intake must be an object")
    paper = intake.get("paper", {}) if isinstance(intake, dict) else {}
    repo = intake.get("repository", {}) if isinstance(intake, dict) else {}
    require(is_nonempty_string(paper.get("title")), errors, "intake.paper.title is required")
    require(is_nonempty_list(paper.get("sources")), errors, "intake.paper.sources must be non-empty")
    require(is_nonempty_string(repo.get("path_or_url")), errors, "intake.repository.path_or_url is required")
    require(is_nonempty_string(intake.get("scope")), errors, "intake.scope is required")
    require(is_nonempty_string(intake.get("execution_stance")), errors, "intake.execution_stance is required")

    questions = data.get("paper_questions")
    require(is_nonempty_list(questions), errors, "paper_questions must be non-empty")
    if isinstance(questions, list):
        for i, question in enumerate(questions):
            prefix = f"paper_questions[{i}]"
            for key in ("id", "question", "why_it_matters", "paper_evidence", "code_evidence", "status", "answer"):
                if key in {"paper_evidence", "code_evidence"}:
                    require(isinstance(question.get(key), list), errors, f"{prefix}.{key} must be a list")
                elif key == "status":
                    require(question.get(key) in QUESTION_STATUSES, errors, f"{prefix}.status is invalid")
                else:
                    require(is_nonempty_string(question.get(key)), errors, f"{prefix}.{key} is required")

    substrate = data.get("domain_critical_execution", {})
    require(is_nonempty_string(substrate.get("name")), errors, "domain_critical_execution.name is required")
    require(is_nonempty_string(substrate.get("description")), errors, "domain_critical_execution.description is required")
    require(is_nonempty_list(substrate.get("code_paths")), errors, "domain_critical_execution.code_paths must be non-empty")

    mechanisms = data.get("mechanisms")
    require(is_nonempty_list(mechanisms), errors, "mechanisms must be non-empty")
    formula_count = 0
    if isinstance(mechanisms, list):
        for i, mech in enumerate(mechanisms):
            prefix = f"mechanisms[{i}]"
            require(is_nonempty_string(mech.get("id")), errors, f"{prefix}.id is required")
            require(is_nonempty_string(mech.get("name")), errors, f"{prefix}.name is required")
            require(is_nonempty_string(mech.get("paper_claim")), errors, f"{prefix}.paper_claim is required")
            validate_code_indices(mech, errors, prefix)
            require(is_nonempty_string(mech.get("relationship")), errors, f"{prefix}.relationship is required")
            require(isinstance(mech.get("differences", []), list), errors, f"{prefix}.differences must be a list")
            formulas = mech.get("formulas", [])
            if isinstance(formulas, list):
                formula_count += len(formulas)
                for j, formula in enumerate(formulas):
                    fp = f"{prefix}.formulas[{j}]"
                    require(is_nonempty_string(formula.get("id")), errors, f"{fp}.id is required")
                    require(is_nonempty_string(formula.get("math")), errors, f"{fp}.math is required")
                    require(is_nonempty_string(formula.get("fallback")), errors, f"{fp}.fallback is required")
    require(formula_count > 0, errors, "at least one mechanism formula is required")

    experiments = data.get("experiments")
    require(is_nonempty_list(experiments), errors, "experiments must be non-empty")
    if isinstance(experiments, list):
        for i, exp in enumerate(experiments):
            prefix = f"experiments[{i}]"
            require(is_nonempty_string(exp.get("id")), errors, f"{prefix}.id is required")
            require(is_nonempty_string(exp.get("paper_ref")), errors, f"{prefix}.paper_ref is required")
            require(is_nonempty_string(exp.get("intent")), errors, f"{prefix}.intent is required")
            require(isinstance(exp.get("settings"), dict), errors, f"{prefix}.settings must be an object")
            require(is_nonempty_list(exp.get("code_paths")), errors, f"{prefix}.code_paths must be non-empty")
            require(exp.get("command_status") in EXPERIMENT_STATUSES, errors, f"{prefix}.command_status is invalid")
            require(is_nonempty_string(exp.get("result_extraction")), errors, f"{prefix}.result_extraction is required")
            require(isinstance(exp.get("code_disclosed_omissions"), list), errors, f"{prefix}.code_disclosed_omissions must be a list")

    omissions = data.get("implementation_omissions")
    require(is_nonempty_list(omissions), errors, "implementation_omissions must be non-empty")
    if isinstance(omissions, list):
        for i, item in enumerate(omissions):
            prefix = f"implementation_omissions[{i}]"
            for key in ("detail", "paper_says", "code_does", "impact"):
                require(is_nonempty_string(item.get(key)), errors, f"{prefix}.{key} is required")

    diagrams = data.get("diagrams")
    require(is_nonempty_list(diagrams), errors, "diagrams must be non-empty")
    diagram_ids: set[str] = set()
    if isinstance(diagrams, list):
        for i, item in enumerate(diagrams):
            prefix = f"diagrams[{i}]"
            require(is_nonempty_string(item.get("id")), errors, f"{prefix}.id is required")
            if is_nonempty_string(item.get("id")):
                diagram_ids.add(item["id"])
            for key in ("type", "title", "source", "legend"):
                require(is_nonempty_string(item.get(key)), errors, f"{prefix}.{key} is required")

    for diagram_id in substrate.get("diagram_ids", []) or []:
        require(diagram_id in diagram_ids, errors, f"domain_critical_execution.diagram_ids references missing diagram: {diagram_id}")

    modify = data.get("modify_guide")
    require(is_nonempty_list(modify), errors, "modify_guide must be non-empty")
    if isinstance(modify, list):
        for i, item in enumerate(modify):
            prefix = f"modify_guide[{i}]"
            require(is_nonempty_string(item.get("goal")), errors, f"{prefix}.goal is required")
            require(is_nonempty_list(item.get("files_methods")), errors, f"{prefix}.files_methods must be non-empty")
            require(is_nonempty_string(item.get("minimal_change")), errors, f"{prefix}.minimal_change is required")
            require(is_nonempty_list(item.get("invariants")), errors, f"{prefix}.invariants must be non-empty")
            require(is_nonempty_string(item.get("smoke_test")), errors, f"{prefix}.smoke_test is required")

    validation = data.get("validation", {})
    require(is_nonempty_list(validation.get("source_files_reopened")), errors, "validation.source_files_reopened must be non-empty")
    checks = validation.get("checks")
    require(is_nonempty_list(checks), errors, "validation.checks must be non-empty")
    if isinstance(checks, list):
        for i, check in enumerate(checks):
            prefix = f"validation.checks[{i}]"
            require(is_nonempty_string(check.get("name")), errors, f"{prefix}.name is required")
            require(check.get("status") in VALIDATION_STATUSES, errors, f"{prefix}.status is invalid")
    require(validation.get("final_status") in FINAL_STATUSES, errors, "validation.final_status is invalid")

    if validation.get("final_status") == "pass":
        unresolved = validation.get("unresolved", [])
        require(not unresolved, errors, "validation.final_status pass cannot have unresolved items")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("bundle", help="Path to analysis_bundle.json")
    parser.add_argument("--json", action="store_true", help="Emit JSON report")
    args = parser.parse_args()

    path = Path(args.bundle)
    data = json.loads(path.read_text(encoding="utf-8"))
    errors = validate_bundle(data)
    report = {"bundle": str(path), "valid": not errors, "errors": errors}
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        if errors:
            print(f"INVALID {path}")
            for err in errors:
                print(f"- {err}")
        else:
            print(f"VALID {path}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
