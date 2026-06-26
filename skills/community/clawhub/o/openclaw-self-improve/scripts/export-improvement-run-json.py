#!/usr/bin/env python3
"""
Export machine-readable JSON files from an OpenClaw self-improvement run.

Reads the markdown artifacts in a run directory and writes:
  - run-info.json   : run metadata + artifact paths
  - summary.json    : status snapshot suitable for CI/automation

In strict mode, the script returns a non-zero exit code if statuses or
hypothesis fields are still empty / placeholder, so CI pipelines do not
silently accept incomplete runs.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import List


PLACEHOLDER_PREFIXES = ("_(", "TODO", "todo")
ALLOWED_STATUS = {"pass", "fail", "blocked", "inconclusive"}
ALLOWED_APPROVAL = {
    "pending", "approved", "approved and implemented", "rejected", "blocked",
}


def read_lines(path: Path) -> List[str]:
    if not path.is_file():
        raise FileNotFoundError(f"Missing required file: {path}")
    return path.read_text(encoding="utf-8").splitlines()


def require_prefixed_value(lines: List[str], prefix: str, label: str) -> str:
    for line in lines:
        if line.startswith(prefix):
            return line[len(prefix):].strip()
    if label in ("Commit", "Branch"):
        return "n/a"
    raise ValueError(f"Missing required field '{label}'")


def section_lines(lines: List[str], heading: str) -> List[str]:
    in_section = False
    collected: List[str] = []
    for line in lines:
        if line == heading:
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if in_section:
            collected.append(line)
    return collected


def first_bullet(section: List[str]) -> str:
    for line in section:
        stripped = line.lstrip()
        if stripped.startswith("- ") or stripped.startswith("* "):
            return stripped[2:].strip()
    for line in section:
        s = line.strip()
        if s:
            return s
    return ""


def normalize_section_text(section: List[str]) -> str:
    text = "\n".join(line.rstrip() for line in section).strip()
    return text


def looks_like_placeholder(value: str) -> bool:
    if not value:
        return True
    return value.startswith(PLACEHOLDER_PREFIXES)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Export machine-readable JSON files from an OpenClaw "
            "self-improvement run."
        )
    )
    parser.add_argument("--run-dir", required=True, help="Path to the run directory")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero if statuses or selected hypothesis are missing/placeholder.",
    )
    args = parser.parse_args()

    run_dir = Path(args.run_dir).resolve()
    if not run_dir.is_dir():
        print(f"Run directory does not exist: {run_dir}", file=sys.stderr)
        return 1

    try:
        run_info_lines  = read_lines(run_dir / "run-info.md")
        baseline_lines  = read_lines(run_dir / "baseline.md")
        proposal_lines  = read_lines(run_dir / "proposal.md")
        validation_lines = read_lines(run_dir / "validation.md")
        outcome_lines   = read_lines(run_dir / "outcome.md")

        timestamp_utc   = require_prefixed_value(run_info_lines, "- Timestamp (UTC):", "Timestamp (UTC)")
        mode            = require_prefixed_value(run_info_lines, "- Mode:", "Mode")
        repo            = require_prefixed_value(run_info_lines, "- Repo:", "Repo")
        objective       = require_prefixed_value(run_info_lines, "- Objective:", "Objective")
        scope           = require_prefixed_value(run_info_lines, "- Scope:", "Scope")
        validation_gate = require_prefixed_value(run_info_lines, "- Validation Gate:", "Validation Gate")

        repo_state = section_lines(baseline_lines, "## Repo State")
        git_commit = require_prefixed_value(repo_state, "- Commit:", "Commit")
        git_branch = require_prefixed_value(repo_state, "- Branch:", "Branch")

        baseline_status   = first_bullet(section_lines(baseline_lines, "## Status"))
        approval_status   = first_bullet(section_lines(proposal_lines, "## Approval Status"))
        validation_status = first_bullet(section_lines(validation_lines, "## Status"))
        outcome_status    = first_bullet(section_lines(outcome_lines, "## Status"))

        selected_hypothesis = normalize_section_text(
            section_lines(proposal_lines, "## Selected Hypothesis")
        )
        next_iteration = normalize_section_text(
            section_lines(outcome_lines, "## Next Iteration")
        )

        warnings: List[str] = []
        if baseline_status not in ALLOWED_STATUS:
            warnings.append(f"baseline_status is '{baseline_status}', not in {sorted(ALLOWED_STATUS)}")
        if validation_status not in ALLOWED_STATUS:
            warnings.append(f"validation_status is '{validation_status}', not in {sorted(ALLOWED_STATUS)}")
        if outcome_status not in ALLOWED_STATUS:
            warnings.append(f"outcome_status is '{outcome_status}', not in {sorted(ALLOWED_STATUS)}")
        if approval_status not in ALLOWED_APPROVAL:
            warnings.append(f"approval_status is '{approval_status}', not in {sorted(ALLOWED_APPROVAL)}")
        if looks_like_placeholder(selected_hypothesis):
            warnings.append("selected_hypothesis is empty or still a placeholder")
        if looks_like_placeholder(next_iteration):
            warnings.append("next_iteration is empty or still a placeholder")

        for w in warnings:
            print(f"warning: {w}", file=sys.stderr)

        generated_at_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

        run_info_json = {
            "timestamp_utc": timestamp_utc,
            "mode": mode,
            "repo": str(repo),
            "objective": objective,
            "scope": scope,
            "validation_gate": validation_gate,
            "git_commit": git_commit,
            "git_branch": git_branch,
            "generated_at_utc": generated_at_utc,
            "artifacts": {
                "markdown": {
                    "run_info":   str(run_dir / "run-info.md"),
                    "baseline":   str(run_dir / "baseline.md"),
                    "hypotheses": str(run_dir / "hypotheses.md"),
                    "proposal":   str(run_dir / "proposal.md"),
                    "validation": str(run_dir / "validation.md"),
                    "outcome":    str(run_dir / "outcome.md"),
                },
                "json": {
                    "run_info": str(run_dir / "run-info.json"),
                    "summary":  str(run_dir / "summary.json"),
                },
            },
        }

        summary_json = {
            "run_dir": str(run_dir),
            "timestamp_utc": timestamp_utc,
            "mode": mode,
            "objective": objective,
            "scope": scope,
            "approval_status":   approval_status,
            "baseline_status":   baseline_status,
            "validation_status": validation_status,
            "outcome_status":    outcome_status,
            "selected_hypothesis": selected_hypothesis,
            "next_iteration": next_iteration,
            "generated_at_utc": generated_at_utc,
        }

        (run_dir / "run-info.json").write_text(
            json.dumps(run_info_json, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        (run_dir / "summary.json").write_text(
            json.dumps(summary_json, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        if args.strict and warnings:
            print("strict mode: refusing to succeed with incomplete run", file=sys.stderr)
            return 2

    except (FileNotFoundError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(f"Exported JSON to {run_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
