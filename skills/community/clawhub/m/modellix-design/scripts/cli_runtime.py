#!/usr/bin/env python3
"""Resolve and safely refresh the globally installed Modellix CLI.

The resolver checks the public npm ``latest`` tag once per workflow.  When a
newer release exists (or the CLI is missing), it installs that exact version
before any paid task is submitted.  Registry or install failures never replace
a working CLI; callers can keep using the installed version or fall back to
REST when no CLI is available.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import os
from pathlib import Path
import re
import shutil
import subprocess
import time
from typing import Callable, Mapping, MutableMapping, Sequence


CLI_PACKAGE = "modellix-cli"
PUBLIC_REGISTRY = "https://registry.npmjs.org"
QUERY_TIMEOUT_SECONDS = 20
INSTALL_TIMEOUT_SECONDS = 120
LOCK_STALE_SECONDS = 5 * 60
SEMVER_RE = re.compile(
    r"(?<![0-9A-Za-z.-])"
    r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?![0-9A-Za-z.-])"
)


@dataclass(frozen=True)
class CliRuntime:
    path: str | None
    installed_version: str | None
    latest_version: str | None
    source: str
    updated: bool
    update_warning: str | None

    @property
    def available(self) -> bool:
        return self.path is not None

    def to_dict(self) -> dict[str, object]:
        return {**asdict(self), "available": self.available}


RunCommand = Callable[..., subprocess.CompletedProcess[str]]
WhichCommand = Callable[[str], str | None]


def auto_update_enabled(environment: Mapping[str, str] | None = None) -> bool:
    source = os.environ if environment is None else environment
    value = source.get("MODELLIX_CLI_AUTO_UPDATE", "").strip()
    return value.lower() not in {"0", "false", "off"}


def valid_version(value: object) -> str:
    text = str(value or "").strip()
    match = SEMVER_RE.fullmatch(text)
    if not match:
        raise ValueError("npm returned an invalid modellix-cli version")
    return text


def extract_version(output: str) -> str | None:
    match = SEMVER_RE.search(output or "")
    return match.group(0) if match else None


def is_newer(candidate: str, current: str) -> bool:
    return _compare_versions(valid_version(candidate), valid_version(current)) > 0


def resolve_cli_runtime(
    *,
    environment: Mapping[str, str] | None = None,
    run_command: RunCommand | None = None,
    which_command: WhichCommand | None = None,
    lock_root: Path | None = None,
) -> CliRuntime:
    """Return a usable CLI path, refreshing it from public npm when possible."""
    env = dict(os.environ if environment is None else environment)
    run = run_command or subprocess.run
    which = which_command or shutil.which
    cli_path = which(CLI_PACKAGE)
    installed_version = _cli_version(cli_path, run, env)

    if not auto_update_enabled(env):
        return CliRuntime(
            cli_path,
            installed_version,
            None,
            "installed-pinned" if cli_path else "missing",
            False,
            None,
        )

    npm_path = which("npm")
    if not npm_path:
        return _fallback(
            cli_path,
            installed_version,
            None,
            "npm is unavailable; could not check modellix-cli@latest.",
        )

    update_lock = lock_root or (_default_lock_root(env) / ".update.lock")
    if not _acquire_lock(update_lock):
        return _fallback(
            cli_path,
            installed_version,
            None,
            "Another Modellix CLI update check is already running.",
        )

    try:
        try:
            latest_version = _npm_latest_version(npm_path, run, env, update_lock.parent)
        except (OSError, subprocess.TimeoutExpired, RuntimeError, ValueError) as exc:
            return _fallback(
                cli_path,
                installed_version,
                None,
                f"Could not check modellix-cli@latest: {_safe_message(exc)}",
            )

        if installed_version and not is_newer(latest_version, installed_version):
            source = (
                "installed-current"
                if latest_version == installed_version
                else "installed-newer"
            )
            return CliRuntime(
                cli_path,
                installed_version,
                latest_version,
                source,
                False,
                None,
            )

        try:
            _npm_install_version(npm_path, latest_version, run, env, update_lock.parent)
            refreshed_path = which(CLI_PACKAGE) or _npm_global_cli_path(
                npm_path, run, env, update_lock.parent
            )
            refreshed_version = _cli_version(refreshed_path, run, env)
            if refreshed_version != latest_version:
                raise RuntimeError("the installed CLI did not report the requested version")
            return CliRuntime(
                refreshed_path,
                refreshed_version,
                latest_version,
                "auto-updated",
                True,
                None,
            )
        except (OSError, subprocess.TimeoutExpired, RuntimeError, ValueError) as exc:
            return _fallback(
                cli_path,
                installed_version,
                latest_version,
                f"Could not install modellix-cli@{latest_version}: {_safe_message(exc)}",
            )
    finally:
        _release_lock(update_lock)


def _fallback(
    path: str | None,
    installed_version: str | None,
    latest_version: str | None,
    warning: str,
) -> CliRuntime:
    return CliRuntime(
        path,
        installed_version,
        latest_version,
        "installed-fallback" if path else "missing",
        False,
        warning,
    )


def _cli_version(
    cli_path: str | None, run: RunCommand, environment: Mapping[str, str]
) -> str | None:
    if not cli_path:
        return None
    try:
        proc = run(
            [cli_path, "--version"],
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
            env=dict(environment),
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if proc.returncode != 0:
        return None
    return extract_version(f"{proc.stdout or ''}\n{proc.stderr or ''}")


def _npm_latest_version(
    npm_path: str,
    run: RunCommand,
    environment: Mapping[str, str],
    state_root: Path,
) -> str:
    proc = run(
        [
            npm_path,
            "view",
            f"{CLI_PACKAGE}@latest",
            "version",
            "--json",
            "--registry",
            PUBLIC_REGISTRY,
            "--prefer-online",
        ],
        check=False,
        capture_output=True,
        text=True,
        timeout=QUERY_TIMEOUT_SECONDS,
        env=_public_npm_environment(environment, state_root),
    )
    if proc.returncode != 0:
        raise RuntimeError(f"npm view failed with exit code {proc.returncode}")
    raw = (proc.stdout or "").strip().strip('"')
    return valid_version(raw)


def _npm_install_version(
    npm_path: str,
    version: str,
    run: RunCommand,
    environment: Mapping[str, str],
    state_root: Path,
) -> None:
    proc = run(
        [
            npm_path,
            "install",
            "--global",
            "--ignore-scripts",
            "--no-audit",
            "--no-fund",
            "--registry",
            PUBLIC_REGISTRY,
            f"{CLI_PACKAGE}@{valid_version(version)}",
        ],
        check=False,
        capture_output=True,
        text=True,
        timeout=INSTALL_TIMEOUT_SECONDS,
        env=_public_npm_environment(environment, state_root),
    )
    if proc.returncode != 0:
        raise RuntimeError(f"npm install failed with exit code {proc.returncode}")


def _npm_global_cli_path(
    npm_path: str,
    run: RunCommand,
    environment: Mapping[str, str],
    state_root: Path,
) -> str | None:
    proc = run(
        [npm_path, "prefix", "--global"],
        check=False,
        capture_output=True,
        text=True,
        timeout=15,
        env=_public_npm_environment(environment, state_root),
    )
    if proc.returncode != 0 or not (proc.stdout or "").strip():
        return None
    prefix = Path(proc.stdout.strip())
    candidates = (
        (prefix / "modellix-cli.cmd", prefix / "modellix-cli")
        if os.name == "nt"
        else (prefix / "bin" / "modellix-cli",)
    )
    return next((str(path) for path in candidates if path.is_file()), None)


def _public_npm_environment(
    environment: Mapping[str, str], state_root: Path
) -> MutableMapping[str, str]:
    safe: dict[str, str] = {}
    for name, value in environment.items():
        lowered = name.lower()
        if lowered in {"node_auth_token", "npm_token"}:
            continue
        if lowered.startswith("npm_config_") and any(
            secret in lowered for secret in ("auth", "token", "password")
        ):
            continue
        safe[name] = value
    state_root.mkdir(parents=True, exist_ok=True)
    safe.update(
        {
            "FORCE_COLOR": "0",
            "NO_COLOR": "1",
            "npm_config_audit": "false",
            "npm_config_cache": str(state_root / "npm"),
            "npm_config_fund": "false",
            "npm_config_registry": PUBLIC_REGISTRY,
            "npm_config_update_notifier": "false",
            "npm_config_userconfig": os.devnull,
        }
    )
    return safe


def _default_lock_root(environment: Mapping[str, str]) -> Path:
    override = environment.get("MODELLIX_CLI_UPDATE_STATE_DIR", "").strip()
    if override:
        return Path(override).expanduser().resolve()
    if os.name == "nt":
        base = Path(environment.get("LOCALAPPDATA") or Path.home() / "AppData" / "Local")
        return base / "Modellix" / "Plugin" / "cli"
    if sys_platform() == "darwin":
        return Path.home() / "Library" / "Caches" / "modellix-plugin" / "cli"
    return Path(environment.get("XDG_CACHE_HOME") or Path.home() / ".cache") / "modellix-plugin" / "cli"


def sys_platform() -> str:
    # Isolated for deterministic tests without mutating sys.platform.
    import sys

    return sys.platform


def _acquire_lock(lock_root: Path) -> bool:
    lock_root.parent.mkdir(parents=True, exist_ok=True)
    try:
        lock_root.mkdir()
        return True
    except FileExistsError:
        try:
            if time.time() - lock_root.stat().st_mtime <= LOCK_STALE_SECONDS:
                return False
            shutil.rmtree(lock_root)
            lock_root.mkdir()
            return True
        except (FileNotFoundError, FileExistsError, OSError):
            return False


def _release_lock(lock_root: Path) -> None:
    try:
        lock_root.rmdir()
    except (FileNotFoundError, OSError):
        pass


def _compare_versions(left: str, right: str) -> int:
    left_match = SEMVER_RE.fullmatch(left)
    right_match = SEMVER_RE.fullmatch(right)
    if not left_match or not right_match:
        raise ValueError("invalid semantic version")
    left_core = tuple(int(left_match.group(index)) for index in range(1, 4))
    right_core = tuple(int(right_match.group(index)) for index in range(1, 4))
    if left_core != right_core:
        return 1 if left_core > right_core else -1
    return _compare_prerelease(left_match.group(4), right_match.group(4))


def _compare_prerelease(left: str | None, right: str | None) -> int:
    if left is None and right is None:
        return 0
    if left is None:
        return 1
    if right is None:
        return -1
    left_parts: Sequence[str] = left.split(".")
    right_parts: Sequence[str] = right.split(".")
    for left_part, right_part in zip(left_parts, right_parts):
        if left_part == right_part:
            continue
        left_numeric = left_part.isdigit()
        right_numeric = right_part.isdigit()
        if left_numeric and right_numeric:
            return 1 if int(left_part) > int(right_part) else -1
        if left_numeric != right_numeric:
            return -1 if left_numeric else 1
        return 1 if left_part > right_part else -1
    if len(left_parts) == len(right_parts):
        return 0
    return 1 if len(left_parts) > len(right_parts) else -1


def _safe_message(error: BaseException) -> str:
    return re.sub(
        r"((?:_authToken|_auth|password|token)\s*[=:]\s*)\S+",
        r"\1[redacted]",
        str(error) or "update unavailable",
        flags=re.IGNORECASE,
    )[:300]
