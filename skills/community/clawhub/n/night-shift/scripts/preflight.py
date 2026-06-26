"""Night Shift preflight checks.

Preflight is intentionally conservative: it should catch missing binaries,
background environment gaps, and non-interactive runner auth problems before
Night Shift starts mutating plan state or running every queued plan through the
same broken backend.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

try:
    from .models import Plan
    from .queue import get_approved_plans
except ImportError:  # direct execution from scripts/
    from models import Plan
    from queue import get_approved_plans

_SKILL_DIR = Path(__file__).resolve().parent.parent
_WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", _SKILL_DIR.parent.parent))
_DATA_DIR = Path(os.environ.get("NIGHT_SHIFT_DATA_DIR", _WORKSPACE / "data" / "night-shift"))

AGENTIC_METHODS = {"cursor", "subagent", "claude-code"}


@dataclass
class PreflightIssue:
    severity: str  # "error" | "warning"
    code: str
    message: str
    fix: str = ""

    def to_dict(self) -> dict:
        return {
            "severity": self.severity,
            "code": self.code,
            "message": self.message,
            "fix": self.fix,
        }


@dataclass
class PreflightResult:
    ok: bool
    issues: list[PreflightIssue] = field(default_factory=list)
    available_backends: list[str] = field(default_factory=list)

    @property
    def errors(self) -> list[PreflightIssue]:
        return [issue for issue in self.issues if issue.severity == "error"]

    @property
    def warnings(self) -> list[PreflightIssue]:
        return [issue for issue in self.issues if issue.severity == "warning"]

    def to_dict(self) -> dict:
        return {
            "ok": self.ok,
            "available_backends": self.available_backends,
            "issues": [issue.to_dict() for issue in self.issues],
        }

    def format(self) -> str:
        status = "OK" if self.ok else "BLOCKED"
        lines = [f"Night Shift preflight: {status}"]
        if self.available_backends:
            lines.append(f"Available backends: {', '.join(self.available_backends)}")
        for issue in self.issues:
            prefix = "❌" if issue.severity == "error" else "⚠️"
            lines.append(f"{prefix} {issue.code}: {issue.message}")
            if issue.fix:
                lines.append(f"   Fix: {issue.fix}")
        return "\n".join(lines)


def _phase_methods(plans: Iterable[Plan]) -> set[str]:
    methods: set[str] = set()
    for plan in plans:
        for phase in plan.ordered_phases():
            methods.add(getattr(phase, "execution_method", "cursor") or "cursor")
    return methods


def _cursor_cli_path() -> str | None:
    configured = os.environ.get("CURSOR_CLI")
    candidates = [configured, shutil.which("agent"), shutil.which("cursor"), "/root/.local/bin/agent", "/usr/local/bin/agent"]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return str(candidate)
    return None


def _check_cursor_auth(cli: str) -> tuple[bool, str]:
    """Best-effort non-interactive Cursor auth check.

    Cursor/agent CLIs vary by version. Prefer lightweight version/help checks,
    then treat explicit auth errors as blockers. We intentionally do not run a
    paid/model task here.
    """
    env = {**os.environ, "HOME": os.environ.get("HOME", str(Path.home()))}
    probes = ([cli, "--version"], [cli, "--help"])
    last = ""
    for cmd in probes:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=20, env=env)
        except Exception as exc:  # pragma: no cover - defensive
            last = str(exc)
            continue
        combined = (result.stdout + "\n" + result.stderr).strip()
        last = combined[:500]
        lower = combined.lower()
        if "authentication required" in lower or "login" in lower and "first" in lower:
            return False, combined[:500]
        if result.returncode == 0:
            return True, combined[:500]
    return False, last or "Cursor CLI did not respond to --version/--help"


def run_preflight(plans: list[Plan] | None = None, live: bool = False) -> PreflightResult:
    issues: list[PreflightIssue] = []
    available: list[str] = []

    if plans is None:
        plans = get_approved_plans()

    if sys.version_info < (3, 11):
        issues.append(PreflightIssue("error", "python-version", "Python 3.11+ is required.", "Install/use Python 3.11 or newer."))

    if shutil.which("git"):
        available.append("git")
    else:
        issues.append(PreflightIssue("error", "missing-git", "git binary is required for worktree isolation.", "Install git and ensure it is on PATH."))

    try:
        _DATA_DIR.mkdir(parents=True, exist_ok=True)
        probe = _DATA_DIR / ".preflight-write-test"
        probe.write_text("ok")
        probe.unlink(missing_ok=True)
    except Exception as exc:
        issues.append(PreflightIssue("error", "data-dir-not-writable", f"Night Shift data dir is not writable: {_DATA_DIR} ({exc})", "Set NIGHT_SHIFT_DATA_DIR or OPENCLAW_WORKSPACE to a writable path."))

    methods = _phase_methods(plans)

    if "HOME" not in os.environ or not os.environ.get("HOME"):
        # This was a real production failure in detached systemd.
        severity = "error" if live and methods & AGENTIC_METHODS else "warning"
        issues.append(PreflightIssue(severity, "missing-home", "HOME is not set; detached CLI runners commonly fail without it.", "Set HOME in the service/timer environment."))

    if "shell" in methods:
        available.append("shell")

    if methods & {"cursor", "subagent"}:
        cli = _cursor_cli_path()
        if not cli:
            issues.append(PreflightIssue("error" if live else "warning", "missing-cursor-cli", "Cursor/agent CLI is required by cursor/subagent phases but was not found.", "Install Cursor CLI or set CURSOR_CLI."))
        else:
            ok, detail = _check_cursor_auth(cli)
            if ok:
                available.append("cursor")
            else:
                issues.append(PreflightIssue("error" if live else "warning", "cursor-auth", "Cursor CLI is not ready for non-interactive background execution.", "Run cursor/agent login as the same service user or set CURSOR_API_KEY. Detail: " + detail[:220]))

    if "claude-code" in methods:
        claude = shutil.which("claude")
        if claude:
            available.append("claude-code")
        else:
            issues.append(PreflightIssue("error" if live else "warning", "missing-claude", "Claude Code phase requested but claude binary was not found.", "Install/configure Claude Code or change the phase execution_method."))

    errors = [issue for issue in issues if issue.severity == "error"]
    return PreflightResult(ok=not errors, issues=issues, available_backends=sorted(set(available)))


def main() -> int:
    live = "--live" in sys.argv or "run" in sys.argv
    result = run_preflight(live=live)
    if "--json" in sys.argv:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print(result.format())
    return 0 if result.ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
