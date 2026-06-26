#!/usr/bin/env python3
"""Deploy OpenClaw autopilot templates into a target directory."""

from __future__ import annotations

import argparse
import json
import shlex
import shutil
import stat
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

TEMPLATE_FILES = [
    "openclaw_autopilot.py",
    "openclaw_config.json",
    "openclaw_config.production.json",
    "start_openclaw.sh",
    ".env.example",
]

CLI_ALIAS_MAP: Dict[str, str] = {
    "codex": "Codex CLI",
    "gemini": "Gemini CLI",
    "open-code": "Open Code CLI",
    "opencode": "Open Code CLI",
    "open_code": "Open Code CLI",
    "claude": "Claude Code CLI",
    "claude-code": "Claude Code CLI",
    "claude_code": "Claude Code CLI",
}


@dataclass
class CLIDiscovery:
    name: str
    command: str
    binary: str
    available: bool


def repo_name_from_url(repo_url: str) -> str:
    name = repo_url.rstrip("/").split("/")[-1]
    return name[:-4] if name.endswith(".git") else name


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Deploy OpenClaw autopilot templates")
    p.add_argument("--output-dir", required=True, help="Target directory")
    p.add_argument(
        "--config-profile",
        choices=["default", "production"],
        default="default",
        help="Base config profile written to openclaw_config.json before overrides",
    )
    p.add_argument("--repo-url", default=None, help="Override repo_url in openclaw_config.json")
    p.add_argument("--project-name", default=None, help="Override project_name in openclaw_config.json")
    p.add_argument("--task-requirement", default=None, help="Override task_requirement in openclaw_config.json")
    p.add_argument("--caller-name", default=None, help="Override caller_name in openclaw_config.json")
    p.add_argument("--branch", default=None, help="Override branch in openclaw_config.json")
    p.add_argument("--cli-order", default=None, help="CLI priority order (comma-separated), e.g. codex,gemini,open-code,claude")
    p.add_argument("--only-cli", default=None, help="Enable only specific CLI(s), comma-separated, e.g. codex or gemini")
    p.add_argument("--interval", type=int, default=None, help="Override loop_interval_seconds")
    p.add_argument("--min-pass-rate", type=float, default=None, help="Override report_min_pass_rate")
    p.add_argument(
        "--require-non-doc-code-changes",
        action="store_true",
        help="Require approved rounds to include non-doc code changes (docs-only changes fail the gate)",
    )
    p.add_argument(
        "--min-non-doc-files",
        type=int,
        default=None,
        help="Minimum number of non-doc files changed for an approved round",
    )
    p.add_argument(
        "--min-non-doc-lines",
        type=int,
        default=None,
        help="Minimum total non-doc changed lines (add+del) for an approved round",
    )
    p.add_argument(
        "--require-code-changes",
        action="store_true",
        help="Require each approved round to include real code changes; otherwise it is treated as audit failure",
    )
    p.add_argument(
        "--disable-init-phase",
        action="store_true",
        help="Disable one-time CLI init phase before task execution",
    )
    p.add_argument(
        "--force-reinit",
        action="store_true",
        help="Force re-run CLI init phase even if marker already exists",
    )
    p.add_argument("--git-user-name", default=None, help="Override git_identity.name in openclaw_config.json")
    p.add_argument("--git-user-email", default=None, help="Override git_identity.email in openclaw_config.json")
    p.add_argument(
        "--auto-disable-missing-clis",
        action="store_true",
        help="Disable CLI entries whose binaries are not found in PATH",
    )
    p.add_argument(
        "--init-env",
        action="store_true",
        help="Create .env from .env.example when .env does not exist",
    )
    p.add_argument(
        "--enable-fallback-report",
        action="store_true",
        help="Force enable fallback report generation on missing report",
    )
    p.add_argument(
        "--disable-fallback-report",
        action="store_true",
        help="Force disable fallback report generation on missing report",
    )
    p.add_argument(
        "--fallback-run-tests",
        dest="fallback_run_tests",
        action="store_true",
        help="Fallback mode runs test commands when report is missing",
    )
    p.add_argument(
        "--no-fallback-run-tests",
        dest="fallback_run_tests",
        action="store_false",
        help="Fallback mode skips test commands when report is missing",
    )
    p.add_argument(
        "--fallback-test-command",
        action="append",
        default=[],
        help="Append fallback test command candidate (repeatable)",
    )
    p.add_argument(
        "--print-diagnose-cmd",
        action="store_true",
        help="Print doctor command for post-deploy environment validation",
    )
    p.add_argument(
        "--doctor-after-deploy",
        action="store_true",
        help="Run doctor_autopilot.py immediately after deploy and return its exit code if failed",
    )
    p.add_argument("--force", action="store_true", help="Overwrite existing files")
    p.set_defaults(fallback_run_tests=None)
    return p.parse_args()


def set_executable(path: Path) -> None:
    mode = path.stat().st_mode
    path.chmod(mode | stat.S_IXUSR)


def discover_clis(config: Dict[str, object]) -> List[CLIDiscovery]:
    rows: List[CLIDiscovery] = []
    cli_tools = config.get("cli_tools", [])
    if not isinstance(cli_tools, list):
        return rows
    for item in cli_tools:
        if not isinstance(item, dict):
            continue
        command = str(item.get("command", "")).strip()
        parts: List[str] = []
        try:
            parts = shlex.split(command)
        except ValueError:
            parts = []
        binary = parts[0] if parts else ""
        rows.append(
            CLIDiscovery(
                name=str(item.get("name", "Unnamed CLI")),
                command=command,
                binary=binary,
                available=bool(binary) and (shutil.which(binary) is not None),
            )
        )
    return rows


def split_csv(raw: str | None) -> List[str]:
    if not raw:
        return []
    return [x.strip() for x in raw.split(",") if x.strip()]


def resolve_cli_names(tokens: List[str], available_names: List[str]) -> tuple[List[str], List[str]]:
    by_lower = {name.lower(): name for name in available_names}
    resolved: List[str] = []
    unknown: List[str] = []
    seen: set[str] = set()
    for token in tokens:
        key = token.strip().lower()
        target = CLI_ALIAS_MAP.get(key) or by_lower.get(key)
        if not target:
            unknown.append(token)
            continue
        if target in seen:
            continue
        seen.add(target)
        resolved.append(target)
    return resolved, unknown


def apply_config_overrides(config: Dict[str, object], args: argparse.Namespace) -> Dict[str, object]:
    repo_url_overridden = False
    if args.repo_url is not None:
        config["repo_url"] = args.repo_url
        repo_url_overridden = True
    if args.project_name is not None:
        config["project_name"] = args.project_name
    elif repo_url_overridden:
        config["project_name"] = repo_name_from_url(str(config["repo_url"]))
    if args.task_requirement is not None:
        config["task_requirement"] = args.task_requirement
    if args.caller_name is not None:
        config["caller_name"] = args.caller_name
    if args.branch is not None:
        config["branch"] = args.branch
    if args.interval is not None:
        config["loop_interval_seconds"] = int(args.interval)
    if args.min_pass_rate is not None:
        config["report_min_pass_rate"] = float(args.min_pass_rate)
    if args.require_code_changes:
        config["require_code_changes"] = True
    if args.require_non_doc_code_changes:
        config["require_non_doc_code_changes"] = True
    if args.min_non_doc_files is not None:
        config["minimum_non_doc_files_changed"] = max(0, int(args.min_non_doc_files))
    if args.min_non_doc_lines is not None:
        config["minimum_non_doc_lines_changed"] = max(0, int(args.min_non_doc_lines))

    init_phase = config.get("init_phase")
    if not isinstance(init_phase, dict):
        init_phase = {}
    if args.disable_init_phase:
        init_phase["enabled"] = False
    if args.force_reinit:
        init_phase["force_reinit"] = True
    config["init_phase"] = init_phase

    fallback = config.get("fallback_report")
    if not isinstance(fallback, dict):
        fallback = {}
    if args.enable_fallback_report:
        fallback["enabled"] = True
    if args.disable_fallback_report:
        fallback["enabled"] = False
    if args.fallback_run_tests is not None:
        fallback["run_tests_on_missing_report"] = bool(args.fallback_run_tests)
    if args.fallback_test_command:
        existing = fallback.get("test_command_candidates", [])
        if not isinstance(existing, list):
            existing = []
        fallback["test_command_candidates"] = existing + list(args.fallback_test_command)
    config["fallback_report"] = fallback

    git_identity = config.get("git_identity")
    if not isinstance(git_identity, dict):
        git_identity = {}
    if args.git_user_name is not None:
        git_identity["name"] = args.git_user_name
    if args.git_user_email is not None:
        git_identity["email"] = args.git_user_email
    config["git_identity"] = git_identity

    cli_tools = config.get("cli_tools", [])
    if isinstance(cli_tools, list):
        all_names = [str(item.get("name", "")) for item in cli_tools if isinstance(item, dict)]

        if args.only_cli:
            wanted, unknown = resolve_cli_names(split_csv(args.only_cli), all_names)
            if unknown:
                print(f"WARNING: unknown --only-cli value(s): {', '.join(unknown)}")
            if wanted:
                wanted_set = set(wanted)
                by_name = {str(item.get("name", "")): item for item in cli_tools if isinstance(item, dict)}
                enabled_front = [by_name[name] for name in wanted if name in by_name]
                rest = [item for item in cli_tools if isinstance(item, dict) and str(item.get("name", "")) not in wanted_set]
                for entry in enabled_front:
                    entry["enabled"] = True
                for entry in rest:
                    entry["enabled"] = False
                cli_tools = enabled_front + rest
                print(f"Applied --only-cli: {', '.join(wanted)}")
            else:
                for entry in cli_tools:
                    if isinstance(entry, dict):
                        entry["enabled"] = False
                print("WARNING: --only-cli had no valid CLI names; all CLI entries are disabled")

        if args.cli_order:
            current_names = [str(item.get("name", "")) for item in cli_tools if isinstance(item, dict)]
            ordered_names, unknown = resolve_cli_names(split_csv(args.cli_order), current_names)
            if unknown:
                print(f"WARNING: unknown --cli-order value(s): {', '.join(unknown)}")
            if ordered_names:
                ordered_set = set(ordered_names)
                by_name = {str(item.get("name", "")): item for item in cli_tools if isinstance(item, dict)}
                front = [by_name[name] for name in ordered_names if name in by_name]
                rest = [item for item in cli_tools if isinstance(item, dict) and str(item.get("name", "")) not in ordered_set]
                cli_tools = front + rest
                print(f"Applied --cli-order: {', '.join([str(item.get('name', '')) for item in cli_tools if isinstance(item, dict)])}")
        config["cli_tools"] = cli_tools

    if args.auto_disable_missing_clis:
        discovered = discover_clis(config)
        enabled = 0
        missing = 0
        cli_tools = config.get("cli_tools", [])
        if isinstance(cli_tools, list):
            for idx, entry in enumerate(cli_tools):
                if not isinstance(entry, dict):
                    continue
                if idx >= len(discovered):
                    continue
                if not discovered[idx].available:
                    entry["enabled"] = False
                    missing += 1
                elif bool(entry.get("enabled", True)):
                    enabled += 1
        config["cli_tools"] = cli_tools
        print(f"Auto-disabled missing CLIs: {missing}; enabled CLIs after patch: {enabled}")

    repo_url = str(config.get("repo_url", "")).strip()
    if ("<owner>" in repo_url) or ("<repo>" in repo_url):
        print("WARNING: repo_url is still a placeholder. Set --repo-url or edit openclaw_config.json before running.")

    return config


def maybe_init_env(output_dir: Path) -> None:
    env = output_dir / ".env"
    env_example = output_dir / ".env.example"
    if env.exists():
        return
    if env_example.exists():
        shutil.copy2(env_example, env)
        print(f"Initialized env file: {env}")


def print_cli_discovery(config: Dict[str, object]) -> None:
    rows = discover_clis(config)
    if not rows:
        print("CLI discovery: no cli_tools found")
        return
    print("\nCLI discovery:")
    for row in rows:
        mark = "OK" if row.available else "MISSING"
        print(f"- {row.name}: {mark} ({row.binary or 'unknown-binary'})")


def run_doctor_after_deploy(output_dir: Path) -> int:
    doctor = output_dir / "doctor_autopilot.py"
    config = output_dir / "openclaw_config.json"
    if not doctor.exists():
        print("Doctor run skipped: doctor_autopilot.py not found")
        return 0
    if not config.exists():
        print("Doctor run skipped: openclaw_config.json not found")
        return 0

    cmd = [sys.executable, str(doctor), "--config", str(config)]
    print("\nRunning post-deploy doctor:")
    print(" ".join(shlex.quote(x) for x in cmd))
    proc = subprocess.run(
        cmd,
        cwd=str(output_dir),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    if proc.stdout:
        print(proc.stdout.rstrip())
    return proc.returncode


def main() -> int:
    args = parse_args()
    if args.enable_fallback_report and args.disable_fallback_report:
        raise ValueError("Cannot set both --enable-fallback-report and --disable-fallback-report")

    skill_dir = Path(__file__).resolve().parents[1]
    templates_dir = skill_dir / "assets" / "templates"
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    missing = [name for name in TEMPLATE_FILES if not (templates_dir / name).exists()]
    if missing:
        raise FileNotFoundError(f"Missing template files: {', '.join(missing)}")

    for name in TEMPLATE_FILES:
        src = templates_dir / name
        dst = output_dir / name
        if dst.exists() and not args.force:
            raise FileExistsError(f"File exists (use --force): {dst}")
        shutil.copy2(src, dst)

    doctor_src = skill_dir / "scripts" / "doctor_autopilot.py"
    doctor_dst = output_dir / "doctor_autopilot.py"
    if doctor_src.exists():
        if doctor_dst.exists() and not args.force:
            raise FileExistsError(f"File exists (use --force): {doctor_dst}")
        shutil.copy2(doctor_src, doctor_dst)

    config_path = output_dir / "openclaw_config.json"
    config_src = output_dir / "openclaw_config.json"
    if args.config_profile == "production":
        config_src = output_dir / "openclaw_config.production.json"
    config = json.loads(config_src.read_text(encoding="utf-8"))
    config = apply_config_overrides(config, args)
    config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    set_executable(output_dir / "openclaw_autopilot.py")
    set_executable(output_dir / "start_openclaw.sh")
    if doctor_dst.exists():
        set_executable(doctor_dst)
    if args.init_env:
        maybe_init_env(output_dir)

    print("Deployed files:")
    for name in TEMPLATE_FILES:
        print(f"- {output_dir / name}")
    if doctor_dst.exists():
        print(f"- {doctor_dst}")
    print_cli_discovery(config)
    print("\nNext steps:")
    print(f"0) Active config profile: {args.config_profile}")
    print("1) Edit openclaw_config.json -> task_requirement and cli_tools[].command")
    print("2) cp .env.example .env and set GITHUB_TOKEN")
    print("3) Run once: source .env && python3 openclaw_autopilot.py --config openclaw_config.json --once")
    print("4) Long run: ./start_openclaw.sh")
    if args.print_diagnose_cmd:
        print("5) Doctor: python3 doctor_autopilot.py --config openclaw_config.json")
    if args.doctor_after_deploy:
        code = run_doctor_after_deploy(output_dir)
        if code != 0:
            print(f"Post-deploy doctor failed with exit code {code}")
            return code
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
