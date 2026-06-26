from __future__ import annotations

from pathlib import Path

from openclaw_sec.models import AuditContext, Finding
from openclaw_sec.utils import (
    discover_named_files,
    discover_suffix_files,
    find_secret_hits,
    is_group_readable,
    is_group_writable,
    is_world_readable,
    is_world_writable,
    path_outside_base,
    permission_bits,
    permission_string,
    read_text,
)


ENV_NAMES = {".env", ".env.local"}
LOG_SUFFIXES = (".jsonl", ".log")
WORKSPACE_DOCS = {"MEMORY.md", "AGENTS.md", "SOUL.md", "TOOLS.md", "IDENTITY.md", "USER.md", "HEARTBEAT.md"}


def scan_filesystem(context: AuditContext) -> list[Finding]:
    findings: list[Finding] = []
    config_dir = context.config_path.parent

    findings.extend(_check_directory_permissions(config_dir))
    findings.extend(_check_file_permissions(context.config_path, "FS-001", "OpenClaw config file permissions are too open", "high"))

    scan_roots = [context.current_dir, config_dir]
    if context.workspace_path:
        scan_roots.append(context.workspace_path)

    env_files = discover_named_files(scan_roots, ENV_NAMES)
    env_files.extend(path for path in discover_suffix_files(scan_roots, (".env",)) if path.name not in ENV_NAMES)
    findings.extend(_check_env_file_permissions(env_files))

    log_files = discover_suffix_files(scan_roots, LOG_SUFFIXES)
    findings.extend(_check_many_file_permissions(log_files, "FS-004", "Log or session transcript permissions are too open", "medium"))

    findings.extend(_check_symlink_escape(context, env_files, log_files))
    return findings


def _check_directory_permissions(path: Path) -> list[Finding]:
    if not path.exists():
        return []
    mode = permission_bits(path)
    if not any((is_world_readable(mode), is_world_writable(mode), is_group_writable(mode))):
        return []
    return [
        Finding(
            id="FS-002",
            title="OpenClaw config directory permissions are too open",
            category="filesystem",
            severity="medium",
            confidence="high",
            heuristic=False,
            evidence=[f"{path} {permission_string(path)}"],
            risk="Broad directory permissions make it easier for other local users to inspect or replace sensitive runtime files.",
            recommendation="Restrict the OpenClaw directory to the owning user, typically mode 700 or 750 depending on your threat model.",
            references=["Filesystem permissions"],
        )
    ]


def _check_file_permissions(path: Path, finding_id: str, title: str, severity: str) -> list[Finding]:
    if not path.exists():
        return []
    mode = permission_bits(path)
    if not any((is_world_readable(mode), is_world_writable(mode), is_group_writable(mode))):
        return []
    return [
        Finding(
            id=finding_id,
            title=title,
            category="filesystem",
            severity=severity,
            confidence="high",
            heuristic=False,
            evidence=[f"{path} {permission_string(path)}"],
            risk="Sensitive files with broad local permissions are easier to exfiltrate or tamper with.",
            recommendation="Reduce permissions to user-only access where feasible, especially for config, env, and log artifacts.",
            references=["Filesystem permissions"],
        )
    ]


def _check_many_file_permissions(paths: list[Path], finding_id: str, title: str, severity: str) -> list[Finding]:
    evidence: list[str] = []
    for path in sorted(set(paths)):
        if not path.exists():
            continue
        mode = permission_bits(path)
        if any((is_world_readable(mode), is_world_writable(mode), is_group_writable(mode))):
            evidence.append(f"{path} {permission_string(path)}")
    if not evidence:
        return []
    return [
        Finding(
            id=finding_id,
            title=title,
            category="filesystem",
            severity=severity,
            confidence="high",
            heuristic=False,
            evidence=evidence[:20],
            risk="Broad file permissions increase local disclosure and tampering risk for security-sensitive artifacts.",
            recommendation="Tighten permissions and keep logs or env files out of shared directories.",
            references=["Filesystem permissions"],
        )
    ]


def _check_env_file_permissions(paths: list[Path]) -> list[Finding]:
    evidence: list[str] = []
    for path in sorted(set(paths)):
        if not path.exists():
            continue
        if not find_secret_hits(read_text(path)):
            continue
        mode = permission_bits(path)
        if any((is_world_readable(mode), is_world_writable(mode), is_group_writable(mode), is_group_readable(mode))):
            evidence.append(f"{path} {permission_string(path)}")
    if not evidence:
        return []
    return [
        Finding(
            id="FS-003",
            title="Environment file permissions are too open",
            category="filesystem",
            severity="high",
            confidence="high",
            heuristic=False,
            evidence=evidence[:20],
            risk="Environment files that contain secrets should not be readable or writable by other local users.",
            recommendation="Restrict secret-bearing env files to owner-only permissions such as 600.",
            references=["Filesystem permissions"],
        )
    ]


def _check_symlink_escape(context: AuditContext, env_files: list[Path], log_files: list[Path]) -> list[Finding]:
    candidates = [context.config_path]
    if context.workspace_path:
        candidates.extend(context.workspace_path / name for name in WORKSPACE_DOCS)
    candidates.extend(env_files)
    candidates.extend(log_files[:20])

    evidence: list[str] = []
    for path in candidates:
        if not path.exists() or not path.is_symlink():
            continue
        anchor = _expected_base(context, path)
        target = path.resolve(strict=False)
        if anchor and path_outside_base(target, anchor):
            evidence.append(f"{path} -> {target} (outside {anchor})")
    if not evidence:
        return []
    return [
        Finding(
            id="FS-005",
            title="Sensitive file symlink escapes the expected directory tree",
            category="filesystem",
            severity="high",
            confidence="high",
            heuristic=False,
            evidence=evidence,
            risk="Symlink indirection can point security-sensitive paths at less protected or unexpected locations.",
            recommendation="Replace escaped symlinks with real files inside the expected tree or validate the target path explicitly.",
            references=["Symlink path resolution"],
        )
    ]


def _expected_base(context: AuditContext, path: Path) -> Path | None:
    config_dir = context.config_path.parent
    try:
        path.relative_to(config_dir)
        return config_dir
    except ValueError:
        pass
    if context.workspace_path:
        try:
            path.relative_to(context.workspace_path)
            return context.workspace_path
        except ValueError:
            pass
    try:
        path.relative_to(context.current_dir)
        return context.current_dir
    except ValueError:
        return None
