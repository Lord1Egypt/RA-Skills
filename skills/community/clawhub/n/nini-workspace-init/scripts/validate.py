#!/usr/bin/env python3
"""Validate workspace initialization completeness.

Checks that all expected files and configurations are in place
after running workspace-init. Can be run standalone or called
by the skill at the end of Phase 5.

Usage:
    python3 validate.py [workspace_path]

    workspace_path: root of the workspace (default: current directory)

Exit codes:
    0: all checks passed
    1: errors found (init incomplete)
    2: warnings only (functional but incomplete)
"""

import json
import os
import re
import sys
from pathlib import Path


def check(label: str, passed: bool, evidence: str, level: str = "ERROR") -> dict:
    return {
        "label": label,
        "passed": passed,
        "evidence": evidence,
        "level": level,
    }


def validate_workspace(root: Path) -> list[dict]:
    results: list[dict] = []

    # --- repos.json ---
    repos_json = root / "repos.json"
    if not repos_json.exists():
        results.append(check("repos.json exists", False, "File not found"))
        return results  # Can't continue without repos.json

    try:
        data = json.loads(repos_json.read_text())
        repos = data.get("repos", [])
        results.append(check("repos.json is valid JSON", True, f"{len(repos)} repos defined"))
    except (json.JSONDecodeError, KeyError) as e:
        results.append(check("repos.json is valid JSON", False, str(e)))
        return results

    all_have_fields = all(
        all(k in r for k in ("name", "url", "path")) for r in repos
    )
    results.append(
        check(
            "repos.json entries have name/url/path",
            all_have_fields,
            "All fields present" if all_have_fields else "Missing fields in some entries",
        )
    )

    # --- CLAUDE.md ---
    claude_md = root / "CLAUDE.md"
    if claude_md.exists():
        content = claude_md.read_text()

        # Check for remaining placeholders
        placeholder_patterns = [
            r"\[ROLE:",
            r"\[LEVEL:",
            r"\[YOUR_LANGUAGE:",
            r"\[YOUR_FORMAT_COMMAND\]",
            r"\[YOUR_LINT_COMMAND\]",
            r"\[YOUR_TYPE_CHECK_COMMAND\]",
            r"\[YOUR_TEST_COMMAND\]",
            r"\[PROJECT_STYLE_GUIDE:",
            r"\[ADD YOUR",
        ]
        remaining = [p for p in placeholder_patterns if re.search(p, content)]
        results.append(
            check(
                "CLAUDE.md has no remaining placeholders",
                len(remaining) == 0,
                f"Remaining: {remaining}" if remaining else "All placeholders replaced",
            )
        )

        # Check repo table matches repos.json count
        table_rows = re.findall(r"^\|\s*`repos/", content, re.MULTILINE)
        results.append(
            check(
                "CLAUDE.md repo table matches repos.json",
                len(table_rows) == len(repos),
                f"Table has {len(table_rows)} rows, repos.json has {len(repos)} repos",
                "WARNING",
            )
        )
    else:
        results.append(check("CLAUDE.md exists", False, "File not found"))

    # --- Sub-repos ---
    for repo in repos:
        repo_path = root / repo["path"]
        name = repo["name"]
        is_git = (repo_path / ".git").exists()
        results.append(
            check(
                f"repo '{name}' cloned",
                repo_path.exists() and is_git,
                f"{'Git repo at ' + str(repo_path) if is_git else 'Not found or not a git repo'}",
            )
        )

    # --- OpenSpec ---
    openspec_dir = root / "openspec"
    results.append(
        check(
            "openspec/ directory exists",
            openspec_dir.exists(),
            str(openspec_dir) if openspec_dir.exists() else "Not found",
        )
    )

    config_yaml = openspec_dir / "config.yaml"
    if config_yaml.exists():
        try:
            # Basic YAML validity check without importing yaml
            content = config_yaml.read_text()
            has_context = "context:" in content
            has_rules = "rules:" in content
            results.append(
                check(
                    "openspec/config.yaml has context and rules",
                    has_context and has_rules,
                    f"context: {'found' if has_context else 'missing'}, rules: {'found' if has_rules else 'missing'}",
                    "WARNING",
                )
            )
        except Exception as e:
            results.append(check("openspec/config.yaml readable", False, str(e), "WARNING"))
    else:
        results.append(check("openspec/config.yaml exists", False, "Not found", "WARNING"))

    # --- Environments ---
    for repo in repos:
        repo_path = root / repo["path"]
        name = repo["name"]
        if not repo_path.exists():
            continue

        has_pyproject = (repo_path / "pyproject.toml").exists()
        has_setup_py = (repo_path / "setup.py").exists()
        has_package_json = (repo_path / "package.json").exists()

        if has_pyproject or has_setup_py:
            has_venv = (repo_path / "venv").exists()
            results.append(
                check(
                    f"repo '{name}' has Python venv",
                    has_venv,
                    "venv/ found" if has_venv else "venv/ missing",
                    "WARNING",
                )
            )

        if has_package_json:
            has_modules = (repo_path / "node_modules").exists()
            results.append(
                check(
                    f"repo '{name}' has node_modules",
                    has_modules,
                    "node_modules/ found" if has_modules else "node_modules/ missing",
                    "WARNING",
                )
            )

        has_precommit_config = (repo_path / ".pre-commit-config.yaml").exists()
        if has_precommit_config:
            hooks_dir = repo_path / ".git" / "hooks" / "pre-commit"
            has_hooks = hooks_dir.exists()
            results.append(
                check(
                    f"repo '{name}' pre-commit hooks installed",
                    has_hooks,
                    "Hooks installed" if has_hooks else "Run: cd {name} && pre-commit install",
                    "WARNING",
                )
            )

    # --- VSCode workspace ---
    workspace_files = list(root.glob("*.code-workspace"))
    if workspace_files:
        ws_file = workspace_files[0]
        try:
            ws_data = json.loads(ws_file.read_text())
            folders = ws_data.get("folders", [])
            expected = len(repos) + 1  # root + repos
            results.append(
                check(
                    f"{ws_file.name} folder count",
                    len(folders) == expected,
                    f"Has {len(folders)} folders, expected {expected}",
                    "WARNING",
                )
            )
        except json.JSONDecodeError as e:
            results.append(check(f"{ws_file.name} valid JSON", False, str(e), "WARNING"))
    else:
        results.append(
            check("VSCode workspace file exists", False, "No *.code-workspace found", "WARNING")
        )

    return results


def print_results(results: list[dict]) -> int:
    errors = 0
    warnings = 0

    for r in results:
        icon = "\u2713" if r["passed"] else ("\u2717" if r["level"] == "ERROR" else "\u26a0")
        prefix = "" if r["passed"] else f" [{r['level']}]"
        print(f"  {icon} {r['label']}{prefix}")
        if not r["passed"]:
            print(f"    {r['evidence']}")
            if r["level"] == "ERROR":
                errors += 1
            else:
                warnings += 1

    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    print()
    print(f"Result: {passed}/{total} checks passed", end="")
    if errors:
        print(f" ({errors} errors, {warnings} warnings)")
    elif warnings:
        print(f" ({warnings} warnings)")
    else:
        print()

    if errors:
        return 1
    elif warnings:
        return 2
    return 0


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    root = root.resolve()

    print(f"Validating workspace: {root}")
    print()

    results = validate_workspace(root)
    return print_results(results)


if __name__ == "__main__":
    sys.exit(main())
