#!/usr/bin/env python3
"""Run deterministic release checks for the MoSoCanvas skill package."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import py_compile
import re
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_SCHEMAS = {
    "artifact-review.example.json": "artifact-review.schema.json",
    "repair-run-state.example.json": "run-state.schema.json",
    "run-state.example.json": "run-state.schema.json",
    "series-plan.example.json": "series-plan.schema.json",
    "shot-plan.example.json": "shot-plan.schema.json",
    "visual-spec.example.json": "visual-spec.schema.json",
}


def load_json(path: Path, blockers: list[str]) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        blockers.append(f"invalid JSON {path.relative_to(ROOT)}: {exc}")
        return None


def validate_evals(blockers: list[str]) -> int:
    path = ROOT / "evals" / "evals.json"
    value = load_json(path, blockers)
    if not isinstance(value, dict):
        return 0
    cases = value.get("cases")
    if not isinstance(cases, list) or not cases:
        blockers.append("evals/evals.json requires a non-empty cases array")
        return 0
    ids: set[str] = set()
    for index, case in enumerate(cases, start=1):
        if not isinstance(case, dict):
            blockers.append(f"eval case {index} must be an object")
            continue
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id or case_id in ids:
            blockers.append(f"eval case {index} has a duplicate or empty id")
        else:
            ids.add(case_id)
        if not isinstance(case.get("input"), str) or not case["input"].strip():
            blockers.append(f"eval case {case_id or index} requires input")
        for field in ("expected", "forbidden"):
            items = case.get(field)
            if not isinstance(items, list) or not items:
                blockers.append(f"eval case {case_id or index} requires {field}")
            elif any(not isinstance(item, str) or not item.strip() for item in items):
                blockers.append(
                    f"eval case {case_id or index} has an invalid {field} item"
                )
    return len(ids)


def validate_version(blockers: list[str]) -> str:
    version_path = ROOT / "VERSION"
    try:
        version = version_path.read_text(encoding="utf-8").strip()
    except OSError as exc:
        blockers.append(f"VERSION cannot be loaded: {exc}")
        return ""
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", version):
        blockers.append("VERSION must contain one semantic version")
        return version

    skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    if f"# MoSoCanvas v{version}" not in skill_text:
        blockers.append("SKILL.md title does not match VERSION")
    evals = load_json(ROOT / "evals" / "evals.json", blockers)
    if isinstance(evals, dict) and evals.get("suite") != f"mosocanvas-v{version}":
        blockers.append("eval suite version does not match VERSION")
    return version


def validate_markdown_links(blockers: list[str]) -> int:
    count = 0
    pattern = re.compile(r"\[[^]]+\]\(([^)]+)\)")
    for markdown in ROOT.rglob("*.md"):
        for target in pattern.findall(markdown.read_text(encoding="utf-8")):
            if "://" in target or target.startswith("#"):
                continue
            count += 1
            path_part = target.split("#", 1)[0]
            if not (markdown.parent / path_part).resolve().exists():
                blockers.append(
                    f"broken markdown link in {markdown.relative_to(ROOT)}: {target}"
                )
    return count


def validate_schemas(
    blockers: list[str], warnings: list[str], strict: bool
) -> tuple[int, int]:
    schemas = sorted((ROOT / "schemas").glob("*.json"))
    loaded = [(path, load_json(path, blockers)) for path in schemas]
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        message = "jsonschema is unavailable; schema meta-validation was skipped"
        (blockers if strict else warnings).append(message)
        return len(schemas), 0

    for path, schema in loaded:
        if schema is None:
            continue
        try:
            Draft202012Validator.check_schema(schema)
        except Exception as exc:
            blockers.append(f"invalid JSON Schema {path.name}: {exc}")

    example_count = 0
    for example_name, schema_name in EXAMPLE_SCHEMAS.items():
        example = load_json(ROOT / "examples" / example_name, blockers)
        schema = load_json(ROOT / "schemas" / schema_name, blockers)
        if example is None or schema is None:
            continue
        example_count += 1
        errors = sorted(
            Draft202012Validator(schema).iter_errors(example),
            key=lambda error: list(error.path),
        )
        for error in errors:
            location = ".".join(map(str, error.path)) or "<root>"
            blockers.append(
                f"invalid example {example_name} at {location}: {error.message}"
            )
    return len(schemas), example_count


def main() -> int:
    parser = argparse.ArgumentParser(description="Run MoSoCanvas deterministic release checks.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail when optional schema-validation dependencies are unavailable.",
    )
    args = parser.parse_args()

    blockers: list[str] = []
    warnings: list[str] = []
    version = validate_version(blockers)

    compiled = 0
    for path in sorted((ROOT / "scripts").glob("*.py")) + sorted(
        (ROOT / "tests").glob("*.py")
    ):
        try:
            py_compile.compile(str(path), doraise=True)
            compiled += 1
        except py_compile.PyCompileError as exc:
            blockers.append(f"Python compile failed for {path.name}: {exc}")

    for path in sorted(ROOT.rglob("*.json")):
        load_json(path, blockers)

    tests = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "run_tests.py")],
        text=True,
        capture_output=True,
        check=False,
    )
    if tests.returncode:
        blockers.append("deterministic test suite failed")

    schema_count, example_count = validate_schemas(blockers, warnings, args.strict)
    eval_count = validate_evals(blockers)
    link_count = validate_markdown_links(blockers)

    report = {
        "schema": "moso.self-check/0.1",
        "version": version,
        "status": "block" if blockers else "pass",
        "root": str(ROOT),
        "checks": {
            "python_files_compiled": compiled,
            "deterministic_tests_passed": tests.returncode == 0,
            "json_schemas_found": schema_count,
            "schema_examples_validated": example_count,
            "behavioral_eval_cases_well_formed": eval_count,
            "local_markdown_links_checked": link_count,
        },
        "blockers": blockers,
        "warnings": warnings,
        "behavioral_eval_execution": (
            "not executed; evals require a clean-context model harness and rubric judge"
        ),
        "test_output": tests.stderr.strip() or tests.stdout.strip(),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if blockers else 0


if __name__ == "__main__":
    raise SystemExit(main())
