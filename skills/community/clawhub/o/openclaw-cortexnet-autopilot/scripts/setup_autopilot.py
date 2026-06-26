#!/usr/bin/env python3
"""One-command setup wrapper for OpenClaw autopilot workspaces."""

from __future__ import annotations

import argparse
import os
import shlex
import subprocess
from pathlib import Path
from typing import Dict


def repo_name_from_url(repo_url: str) -> str:
    name = repo_url.rstrip("/").split("/")[-1]
    return name[:-4] if name.endswith(".git") else name


def parse_env_file(path: Path) -> Dict[str, str]:
    env: Dict[str, str] = {}
    if not path.exists():
        return env
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip()
    return env


def run_cmd(cmd: list[str], cwd: Path | None = None, env: Dict[str, str] | None = None) -> int:
    print("$", " ".join(shlex.quote(x) for x in cmd))
    proc = subprocess.run(cmd, cwd=str(cwd) if cwd else None, env=env)
    return proc.returncode


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Setup a runnable OpenClaw autopilot workspace")
    p.add_argument("--output-dir", required=True, help="Workspace output directory")
    p.add_argument("--repo-url", required=True, help="Target GitHub repository URL")
    p.add_argument("--project-name", default=None, help="Project display name (default: derived from repo URL)")
    p.add_argument("--caller-name", default="自动化编排器", help="Caller identity shown in CLI prompts")
    p.add_argument("--task-requirement", default=None, help="Override task_requirement")
    p.add_argument("--branch", default="dev", help="Target branch")
    p.add_argument("--config-profile", choices=["default", "production"], default="production", help="Base profile")
    p.add_argument("--cli-order", default="codex,gemini,open-code,claude", help="CLI priority order")
    p.add_argument("--only-cli", default=None, help="Restrict enabled CLIs")
    p.add_argument("--token-env", default="GITHUB_TOKEN", help="Token env var name used by runtime")
    p.add_argument("--token", default=None, help="Optional GitHub token to write into .env")
    p.add_argument("--run-doctor", action="store_true", help="Run doctor after setup")
    p.add_argument("--run-once", action="store_true", help="Run one round after setup")
    p.add_argument("--force", action="store_true", help="Overwrite existing output files")
    p.add_argument("--min-non-doc-files", type=int, default=None, help="Override minimum_non_doc_files_changed")
    p.add_argument("--min-non-doc-lines", type=int, default=None, help="Override minimum_non_doc_lines_changed")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    output_dir = Path(args.output_dir).resolve()
    project_name = args.project_name or repo_name_from_url(args.repo_url)
    script_dir = Path(__file__).resolve().parent
    deploy_script = script_dir / "deploy_autopilot.py"

    deploy_cmd = [
        "python3",
        str(deploy_script),
        "--output-dir",
        str(output_dir),
        "--config-profile",
        args.config_profile,
        "--repo-url",
        args.repo_url,
        "--project-name",
        project_name,
        "--caller-name",
        args.caller_name,
        "--branch",
        args.branch,
        "--git-user-name",
        "ai",
        "--git-user-email",
        "ai@local",
        "--cli-order",
        args.cli_order,
        "--auto-disable-missing-clis",
        "--init-env",
    ]
    if args.task_requirement:
        deploy_cmd.extend(["--task-requirement", args.task_requirement])
    if args.only_cli:
        deploy_cmd.extend(["--only-cli", args.only_cli])
    if args.min_non_doc_files is not None:
        deploy_cmd.extend(["--min-non-doc-files", str(max(0, args.min_non_doc_files))])
    if args.min_non_doc_lines is not None:
        deploy_cmd.extend(["--min-non-doc-lines", str(max(0, args.min_non_doc_lines))])
    if args.force:
        deploy_cmd.append("--force")

    code = run_cmd(deploy_cmd)
    if code != 0:
        return code

    env_file = output_dir / ".env"
    if args.token:
        payload = f"{args.token_env}={args.token}\n"
        env_file.write_text(payload, encoding="utf-8")
        print(f"[setup] wrote token to {env_file} ({args.token_env})")
    elif not env_file.exists():
        print(f"[setup] no token written; create {env_file} and set {args.token_env}=<token>")

    run_env = os.environ.copy()
    run_env.update(parse_env_file(env_file))

    if args.run_doctor:
        doctor_cmd = [
            "python3",
            str(output_dir / "doctor_autopilot.py"),
            "--config",
            str(output_dir / "openclaw_config.json"),
        ]
        if args.token_env in run_env and run_env.get(args.token_env):
            doctor_cmd.append("--check-github-token")
        code = run_cmd(doctor_cmd, cwd=output_dir, env=run_env)
        if code != 0:
            return code

    if args.run_once:
        once_cmd = [
            "python3",
            str(output_dir / "openclaw_autopilot.py"),
            "--config",
            str(output_dir / "openclaw_config.json"),
            "--token-env",
            args.token_env,
            "--once",
        ]
        code = run_cmd(once_cmd, cwd=output_dir, env=run_env)
        if code != 0:
            return code

    print("[setup] workspace is ready.")
    print(f"[setup] next: cd {output_dir} && source .env && ./start_openclaw.sh")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
