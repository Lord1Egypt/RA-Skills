from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from openclaw_sec.models import AuditContext, Finding
from openclaw_sec.utils import (
    discover_named_files,
    discover_suffix_files,
    find_secret_hits,
    read_text,
    unique_preserve,
)


WORKSPACE_DOCS = {
    "MEMORY.md",
    "AGENTS.md",
    "SOUL.md",
    "TOOLS.md",
    "IDENTITY.md",
    "USER.md",
    "HEARTBEAT.md",
}

LOG_SUFFIXES = (".jsonl", ".log")
BACKUP_SUFFIXES = (".bak", ".old", ".orig", "~")
ENV_NAMES = {".env", ".env.local"}


def scan_secrets(context: AuditContext) -> list[Finding]:
    findings: list[Finding] = []
    scan_roots = [context.current_dir, context.config_path.parent]
    if context.workspace_path:
        scan_roots.append(context.workspace_path)

    findings.extend(_scan_plaintext_config(context.config_path))
    findings.extend(_scan_env_files(scan_roots))
    findings.extend(_scan_backup_files(scan_roots))
    if context.workspace_path:
        findings.extend(_scan_workspace_docs(context.workspace_path))
    findings.extend(_scan_session_logs(scan_roots))
    return findings


def _scan_plaintext_config(config_path: Path) -> list[Finding]:
    if not config_path.exists():
        return []
    hits = find_secret_hits(read_text(config_path))
    if not hits:
        return []
    evidence = [f"{config_path}:{hit.line_no} ({hit.pattern_name})" for hit in hits[:10]]
    return [
        Finding(
            id="PRIV-001",
            title="Plaintext secrets detected in OpenClaw config",
            category="secrets",
            severity="critical",
            confidence="high",
            heuristic=False,
            evidence=evidence,
            risk="Config files are commonly copied into backups and support bundles, so embedded secrets expand exposure quickly.",
            recommendation="Move secrets to a dedicated secret store or protected environment variables, then rotate exposed values.",
            masked_examples=unique_preserve(hit.masked_value for hit in hits[:10]),
            references=["OpenClaw config", str(config_path)],
        )
    ]


def _scan_env_files(scan_roots: list[Path]) -> list[Finding]:
    env_files = discover_named_files(scan_roots, ENV_NAMES)
    env_files.extend(path for path in discover_suffix_files(scan_roots, (".env",)) if path.name not in ENV_NAMES)
    matches = _aggregate_secret_hits(env_files)
    if not matches:
        return []
    return [
        Finding(
            id="PRIV-002",
            title="Plaintext secrets detected in environment files",
            category="secrets",
            severity="critical",
            confidence="high",
            heuristic=False,
            evidence=matches["evidence"],
            risk="Environment files often end up in shells, backups, or repos and should not store high-value secrets in plaintext.",
            recommendation="Move secrets into a proper secret manager or protected host environment, and keep .env files out of version control.",
            masked_examples=matches["masked_examples"],
            references=[".env scanning"],
        )
    ]


def _scan_backup_files(scan_roots: list[Path]) -> list[Finding]:
    backup_files = discover_suffix_files(scan_roots, BACKUP_SUFFIXES)
    matches = _aggregate_secret_hits(backup_files)
    if not matches:
        return []
    severity = "critical" if len(matches["evidence"]) >= 3 else "high"
    return [
        Finding(
            id="PRIV-003",
            title="Secrets detected in backup or editor recovery files",
            category="secrets",
            severity=severity,
            confidence="high",
            heuristic=False,
            evidence=matches["evidence"],
            risk="Backups are easy to overlook and can preserve revoked or still-active secrets outside the main config path.",
            recommendation="Delete stale backup files, rotate exposed credentials, and ensure sensitive files are excluded from ad-hoc backups.",
            masked_examples=matches["masked_examples"],
            references=["Backup file scan"],
        )
    ]


def _scan_workspace_docs(workspace_path: Path) -> list[Finding]:
    files = [workspace_path / name for name in WORKSPACE_DOCS if (workspace_path / name).exists()]
    matches = _aggregate_secret_hits(files)
    if not matches:
        return []
    return [
        Finding(
            id="PRIV-004",
            title="Secrets detected in OpenClaw workspace memory/bootstrap documents",
            category="secrets",
            severity="high",
            confidence="high",
            heuristic=False,
            evidence=matches["evidence"],
            risk="Workspace memory files are often fed back into agents, copied across sessions, or inspected interactively.",
            recommendation="Remove secrets from long-lived workspace documents and replace them with redacted references or secret identifiers.",
            masked_examples=matches["masked_examples"],
            references=["OpenClaw workspace docs"],
        )
    ]


def _scan_session_logs(scan_roots: list[Path]) -> list[Finding]:
    log_files = discover_suffix_files(scan_roots, LOG_SUFFIXES)
    matches = _aggregate_secret_hits(log_files)
    findings: list[Finding] = []
    if matches:
        severity = "critical" if len(matches["masked_examples"]) >= 3 else "high"
        findings.append(
            Finding(
                id="PRIV-005",
                title="Secrets detected in logs or session transcripts",
                category="secrets",
                severity=severity,
                confidence="high",
                heuristic=False,
                evidence=matches["evidence"],
                risk="Logs and JSONL transcripts are easy to index, sync, or retain far longer than the original secret owner expects.",
                recommendation="Purge or restrict affected logs, rotate exposed secrets, and reduce future secret logging at the source.",
                masked_examples=matches["masked_examples"],
                references=["Log scan"],
            )
        )
        if matches["duplicate_count"] >= 2:
            findings.append(
                Finding(
                    id="LOG-001",
                    title="The same secret pattern appears across multiple files",
                    category="hygiene",
                    severity="medium",
                    confidence="medium",
                    heuristic=False,
                    evidence=matches["duplicate_evidence"][:10],
                    risk="Repeated secret exposure across multiple artifacts makes cleanup and incident scoping much harder.",
                    recommendation="Prioritize rotation of duplicated secrets and purge every referenced copy instead of only the first hit.",
                    masked_examples=matches["masked_examples"][:10],
                    references=["Secret duplication scan"],
                )
            )
        if len(matches["files"]) >= 5:
            findings.append(
                Finding(
                    id="LOG-002",
                    title="Log hygiene appears weak around sensitive material",
                    category="hygiene",
                    severity="medium",
                    confidence="medium",
                    heuristic=True,
                    evidence=[f"Sensitive material detected across {len(matches['files'])} log files"],
                    risk="Large volumes of retained sensitive logs increase accidental disclosure and make complete cleanup less likely.",
                    recommendation="Tighten log retention, rotation, and redaction rules for agent sessions and command logs.",
                    masked_examples=matches["masked_examples"][:5],
                    references=["Log hygiene heuristic"],
                )
            )
    return findings


def _aggregate_secret_hits(paths: list[Path]) -> dict[str, object]:
    evidence: list[str] = []
    masked_examples: list[str] = []
    files: set[str] = set()
    duplicate_map: dict[str, set[str]] = defaultdict(set)
    for path in sorted(set(paths)):
        hits = find_secret_hits(read_text(path))
        if not hits:
            continue
        files.add(str(path))
        for hit in hits[:20]:
            evidence.append(f"{path}:{hit.line_no} ({hit.pattern_name})")
            masked_examples.append(hit.masked_value)
            duplicate_map[hit.masked_value].add(str(path))
    duplicate_evidence = [
        f"{masked} seen in {len(path_set)} files"
        for masked, path_set in duplicate_map.items()
        if len(path_set) > 1
    ]
    if not evidence:
        return {}
    return {
        "evidence": evidence[:20],
        "masked_examples": unique_preserve(masked_examples)[:20],
        "files": files,
        "duplicate_count": len(duplicate_evidence),
        "duplicate_evidence": duplicate_evidence,
    }
