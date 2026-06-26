"""Dify plugin adapter draft for One Person Company OS.

This file documents the command mapping used by the Dify tool YAML files.
The final marketplace package may need Dify's current plugin SDK base classes.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import List


ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = ROOT / "scripts"


def run_script(script: str, args: List[str]) -> str:
    completed = subprocess.run(
        [sys.executable, str(SCRIPTS / script)] + args,
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    output = "\n".join(part for part in (completed.stdout.strip(), completed.stderr.strip()) if part)
    if completed.returncode != 0:
        raise RuntimeError(output or f"{script} failed")
    return output


def init_business(company_name: str, workspace_path: str, product_name: str, target_user: str, core_problem: str, product_pitch: str, language: str = "zh-CN") -> str:
    return run_script(
        "init_business.py",
        [
            company_name,
            "--path",
            workspace_path,
            "--product-name",
            product_name,
            "--target-user",
            target_user,
            "--core-problem",
            core_problem,
            "--product-pitch",
            product_pitch,
            "--language",
            language,
            "--confirmed",
        ],
    )


def update_focus(company_dir: str, primary_goal: str, primary_bottleneck: str, primary_arena: str, today_action: str) -> str:
    return run_script(
        "update_focus.py",
        [
            company_dir,
            "--primary-goal",
            primary_goal,
            "--primary-bottleneck",
            primary_bottleneck,
            "--primary-arena",
            primary_arena,
            "--today-action",
            today_action,
        ],
    )


def generate_artifact_document(company_dir: str, title: str, category: str, summary: str, evidence: str = "") -> str:
    args = [company_dir, "--title", title, "--category", category, "--summary", summary]
    if evidence:
        args.extend(["--evidence", evidence])
    return run_script("generate_artifact_document.py", args)


def validate_release() -> str:
    return run_script("validate_release.py", [])
