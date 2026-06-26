#!/usr/bin/env python3
"""Offline smoke test for skill deploy scripts and templates."""

from __future__ import annotations

import json
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict


def run_cmd(cmd: list[str], cwd: Path | None = None, allow_failure: bool = False) -> tuple[int, str]:
    print("$", " ".join(shlex.quote(x) for x in cmd))
    proc = subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    out = proc.stdout or ""
    if proc.returncode != 0 and not allow_failure:
        raise RuntimeError(f"command failed ({proc.returncode}): {' '.join(cmd)}\n{out}")
    return proc.returncode, out


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    skill_dir = script_dir.parent
    deploy_script = script_dir / "deploy_autopilot.py"
    doctor_script = script_dir / "doctor_autopilot.py"
    summary_script = script_dir / "log_summary.py"

    with tempfile.TemporaryDirectory(prefix="openclaw_skill_smoke_") as tmp:
        workspace = Path(tmp) / "workspace"
        run_cmd(
            [
                sys.executable,
                str(deploy_script),
                "--output-dir",
                str(workspace),
                "--config-profile",
                "production",
                "--repo-url",
                "https://github.com/example/demo-repo.git",
                "--project-name",
                "demo-repo",
                "--caller-name",
                "smoke-test",
                "--task-requirement",
                "Run a smoke test round.",
                "--cli-order",
                "gemini,codex,open-code,claude",
                "--only-cli",
                "codex,gemini",
                "--auto-disable-missing-clis",
                "--init-env",
                "--force",
            ],
            cwd=skill_dir,
        )

        required = [
            "openclaw_autopilot.py",
            "openclaw_config.json",
            "openclaw_config.production.json",
            "start_openclaw.sh",
            ".env",
            ".env.example",
            "doctor_autopilot.py",
        ]
        for name in required:
            assert_true((workspace / name).exists(), f"missing deployed file: {name}")

        cfg = load_json(workspace / "openclaw_config.json")
        assert_true(str(cfg.get("repo_url", "")).endswith("example/demo-repo.git"), "repo_url override missing")
        assert_true(cfg.get("project_name") == "demo-repo", "project_name mismatch")
        cli_tools = cfg.get("cli_tools", [])
        assert_true(isinstance(cli_tools, list) and len(cli_tools) >= 2, "cli_tools invalid")
        names = [str(item.get("name", "")) for item in cli_tools if isinstance(item, dict)]
        assert_true(names[:2] == ["Gemini CLI", "Codex CLI"], f"unexpected CLI order: {names[:4]}")

        code, doctor_out = run_cmd(
            [
                sys.executable,
                str(doctor_script),
                "--config",
                str(workspace / "openclaw_config.json"),
                "--json",
            ],
            cwd=skill_dir,
            allow_failure=True,
        )
        assert_true(code in (0, 3), f"unexpected doctor exit code: {code}")
        doctor_json = json.loads(doctor_out)
        assert_true("ok" in doctor_json and "items" in doctor_json, "doctor json schema mismatch")

        run_cmd([sys.executable, str(workspace / "openclaw_autopilot.py"), "--help"], cwd=workspace)

        _, summary_out = run_cmd(
            [
                sys.executable,
                str(summary_script),
                "--log-dir",
                str(workspace / "logs"),
                "--json",
            ],
            cwd=skill_dir,
        )
        summary_json = json.loads(summary_out)
        assert_true(summary_json.get("rounds_total") == 0, "expected empty rounds in fresh workspace")

    print("[OK] smoke test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
