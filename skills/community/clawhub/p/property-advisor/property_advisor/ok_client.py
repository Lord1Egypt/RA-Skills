from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any, Callable

from .models import PreflightCheck, PreflightReport, PublishPropertyRequest
from .publish import ok_publish_args


Runner = Callable[..., subprocess.CompletedProcess[str]]
Which = Callable[[str], str | None]


class OKCoreSkillError(RuntimeError):
    pass


def _candidate_roots(custom_root: str | Path | None, env: dict[str, str]) -> list[Path]:
    candidates: list[Path] = []
    for value in (
        custom_root,
        env.get("OK_CORE_SKILL_ROOT"),
        env.get("PROPERTY_OK_SKILL_ROOT"),
        "/Users/a58/Desktop/skills/ok-core-skill",
        str(Path.home() / "Desktop" / "skills" / "ok-core-skill"),
        "/Users/a58/Desktop/ok-core-skill/skills/ok-core-skill",
        str(Path.home() / "Desktop" / "ok-core-skill" / "skills" / "ok-core-skill"),
    ):
        if not value:
            continue
        candidate = Path(value).expanduser()
        if candidate not in candidates:
            candidates.append(candidate)
    return candidates


def resolve_ok_skill_root(custom_root: str | Path | None = None, env: dict[str, str] | None = None) -> Path:
    env = env or os.environ
    for candidate in _candidate_roots(custom_root, env):
        direct_cli = candidate / "scripts" / "cli.py"
        nested_cli = candidate / "skills" / "ok-core-skill" / "scripts" / "cli.py"
        if direct_cli.exists():
            return candidate
        if nested_cli.exists():
            return candidate / "skills" / "ok-core-skill"
    raise OKCoreSkillError("Unable to locate ok-core-skill. Set OK_CORE_SKILL_ROOT or PROPERTY_OK_SKILL_ROOT.")


class OKCoreSkillClient:
    source_name = "ok-core-skill"
    runtime_mode = "ok"
    detail_supported = True

    def __init__(
        self,
        *,
        skill_root: str | Path | None = None,
        runner: Runner | None = None,
        which: Which | None = None,
        env: dict[str, str] | None = None,
    ) -> None:
        self.env = env or os.environ
        self.skill_root = resolve_ok_skill_root(skill_root, self.env)
        self.runner = runner or subprocess.run
        self.which = which or shutil.which
        self._selected_runner: str | None = None
        self._selected_prefix: list[str] | None = None
        self._warnings: list[str] = []
        self.last_command: list[str] = []

    def doctor(self, *, run_browser_smoke: bool = True) -> PreflightReport:
        checks: list[PreflightCheck] = []
        root = self.skill_root
        checks.append(
            PreflightCheck(
                name="skill_root",
                ok=root.exists(),
                message=f"ok-core-skill root: {root}",
            )
        )
        cli_path = root / "scripts" / "cli.py"
        checks.append(
            PreflightCheck(
                name="cli_entry",
                ok=cli_path.exists(),
                message=f"CLI entry {'found' if cli_path.exists() else 'missing'} at {cli_path}",
            )
        )
        uv_path = self.which("uv")
        checks.append(
            PreflightCheck(
                name="uv",
                ok=bool(uv_path),
                message="uv available" if uv_path else "uv not available; will try project .venv",
                detail={"path": uv_path},
            )
        )
        venv_python = root / ".venv" / "bin" / "python"
        checks.append(
            PreflightCheck(
                name="venv_python",
                ok=venv_python.exists(),
                message=f"Fallback venv python {'found' if venv_python.exists() else 'missing'} at {venv_python}",
                detail={"path": str(venv_python)},
            )
        )
        runtime_prefix, runtime_name, runtime_check, runtime_warnings = self._select_runtime()
        checks.append(runtime_check)
        selected_runner = runtime_name if runtime_check.ok else None
        ok = all(check.ok for check in checks if check.name in {"skill_root", "cli_entry", "runtime_smoke"})
        warnings: list[str] = list(runtime_warnings)

        if runtime_check.ok and run_browser_smoke:
            browser_check = self._browser_smoke(runtime_prefix, runtime_name)
            checks.append(browser_check)
            ok = ok and browser_check.ok
        elif runtime_check.ok:
            checks.append(
                PreflightCheck(
                    name="browser_smoke",
                    ok=True,
                    message="Browser smoke skipped.",
                )
            )

        if not uv_path:
            warnings.append("uv unavailable; runtime will rely on ok-core-skill .venv fallback.")
        if runtime_check.ok:
            self._selected_runner = runtime_name
            self._selected_prefix = runtime_prefix
        else:
            self._selected_runner = None
            self._selected_prefix = None
        return PreflightReport(
            ok=ok,
            skill_root=str(root),
            selected_runner=selected_runner,
            checks=checks,
            warnings=warnings,
            source_name=self.source_name,
            runtime_mode=self.runtime_mode,
            detail_supported=self.detail_supported,
        )

    def search_property(
        self,
        *,
        keyword: str,
        country: str,
        city: str,
        lang: str,
        max_results: int,
        query_text: str = "",
        search_location: str = "",
    ) -> list[dict[str, Any]]:
        payload = self._run_json(
            [
                "search",
                "--keyword",
                keyword,
                "--country",
                country,
                "--city",
                city,
                "--lang",
                lang,
                "--max-results",
                str(max_results),
            ]
        )
        return list(payload.get("listings", []))

    def browse_property(
        self,
        *,
        country: str,
        city: str,
        lang: str,
        max_results: int,
        query_text: str = "",
        search_location: str = "",
    ) -> list[dict[str, Any]]:
        payload = self._run_json(
            [
                "browse-category",
                "--category",
                "property",
                "--country",
                country,
                "--city",
                city,
                "--lang",
                lang,
                "--max-results",
                str(max_results),
            ]
        )
        return list(payload.get("listings", []))

    def get_listing_detail(self, *, url: str) -> dict[str, Any]:
        return self._run_json(["get-listing", "--url", url])

    def publish_property(
        self,
        request: PublishPropertyRequest,
        *,
        submit: bool = False,
        save_draft: bool = False,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        args = ok_publish_args(request, submit=submit, save_draft=save_draft, dry_run=dry_run)
        return self._run_json(args, timeout=300)

    def drain_warnings(self) -> list[str]:
        warnings = list(self._warnings)
        self._warnings.clear()
        return warnings

    def _select_runtime(self) -> tuple[list[str], str, PreflightCheck, list[str]]:
        warnings: list[str] = []
        uv_path = self.which("uv")
        if uv_path:
            uv_prefix = ["uv", "run", "python", "scripts/cli.py"]
            check = self._smoke_runtime(uv_prefix, "uv")
            if check.ok:
                return uv_prefix, "uv", check, warnings
            warnings.append(f"uv runtime smoke failed; falling back to .venv. stderr={check.detail.get('stderr', '')}")
        venv_python = self.skill_root / ".venv" / "bin" / "python"
        if venv_python.exists():
            venv_prefix = [str(venv_python), "scripts/cli.py"]
            check = self._smoke_runtime(venv_prefix, "venv")
            if check.ok:
                return venv_prefix, "venv", check, warnings
        return [], "unavailable", PreflightCheck(
            name="runtime_smoke",
            ok=False,
            message="Neither uv nor .venv runtime passed list-countries smoke.",
        ), warnings

    def _smoke_runtime(self, prefix: list[str], runtime_name: str) -> PreflightCheck:
        completed = self._run(prefix + ["list-countries"], timeout=30, check=False)
        ok = completed.returncode == 0
        message = (
            f"{runtime_name} runtime passed list-countries smoke."
            if ok
            else f"{runtime_name} runtime failed list-countries smoke."
        )
        detail = {
            "stdout": completed.stdout.strip()[:300],
            "stderr": completed.stderr.strip()[:300],
        }
        return PreflightCheck(name="runtime_smoke", ok=ok, message=message, detail=detail)

    def _browser_smoke(self, prefix: list[str], runtime_name: str) -> PreflightCheck:
        completed = self._run(prefix + ["check-login"], timeout=60, check=False)
        ok = completed.returncode == 0
        message = (
            f"{runtime_name} runtime passed check-login smoke."
            if ok
            else f"{runtime_name} runtime failed check-login smoke."
        )
        detail = {
            "stdout": completed.stdout.strip()[:300],
            "stderr": completed.stderr.strip()[:300],
        }
        return PreflightCheck(name="browser_smoke", ok=ok, message=message, detail=detail)

    def _ensure_runtime(self) -> tuple[list[str], str]:
        if self._selected_prefix and self._selected_runner:
            return self._selected_prefix, self._selected_runner
        report = self.doctor(run_browser_smoke=False)
        if not report.ok and report.selected_runner is None:
            raise OKCoreSkillError("ok-core-skill runtime preflight failed.")
        if not self._selected_prefix or not self._selected_runner:
            raise OKCoreSkillError("ok-core-skill runtime unavailable after preflight.")
        return self._selected_prefix, self._selected_runner

    def _run_json(self, args: list[str], *, timeout: int = 120) -> dict[str, Any]:
        prefix, _runtime_name = self._ensure_runtime()
        self.last_command = prefix + args
        completed = self._run(self.last_command, timeout=timeout, check=False)
        if completed.returncode != 0:
            raise OKCoreSkillError(
                f"ok-core-skill command failed ({completed.returncode}): {' '.join(prefix + args)}\n"
                f"stdout: {completed.stdout}\nstderr: {completed.stderr}"
            )
        try:
            return json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
            raise OKCoreSkillError(f"ok-core-skill returned invalid JSON: {completed.stdout[:500]}") from exc

    def _run(self, command: list[str], *, timeout: int, check: bool) -> subprocess.CompletedProcess[str]:
        return self.runner(
            command,
            cwd=str(self.skill_root),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=check,
        )
