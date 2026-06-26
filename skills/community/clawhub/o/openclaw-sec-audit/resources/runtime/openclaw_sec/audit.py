from __future__ import annotations

from datetime import datetime, timezone
from getpass import getuser
from pathlib import Path

from openclaw_sec import __version__
from openclaw_sec.detectors.config_scan import load_and_scan_config
from openclaw_sec.detectors.fs_scan import scan_filesystem
from openclaw_sec.detectors.git_scan import scan_git
from openclaw_sec.detectors.host_scan import scan_host
from openclaw_sec.detectors.network_scan import scan_network
from openclaw_sec.detectors.secret_scan import scan_secrets
from openclaw_sec.models import AuditContext, AuditReport
from openclaw_sec.report import sort_findings, summarize_findings


def run_audit(context: AuditContext) -> AuditReport:
    findings = []
    notes: list[str] = []
    config_findings, parsed_config = load_and_scan_config(context)
    findings.extend(config_findings)
    findings.extend(scan_secrets(context))
    findings.extend(scan_filesystem(context))

    git_findings, git_meta = scan_git(context)
    findings.extend(git_findings)

    host_info = {
        "user": getuser(),
    }
    if context.enable_host:
        network_findings, network_meta, network_notes = scan_network()
        findings.extend(network_findings)
        host_findings, system_meta, host_notes = scan_host()
        findings.extend(host_findings)
        notes.extend(network_notes)
        notes.extend(host_notes)
        host_info.update(system_meta)
        host_info.update(network_meta)

    findings = sort_findings(findings)
    generated_at = datetime.now(timezone.utc).isoformat()
    summary = summarize_findings(findings)
    target = {
        "config_path": str(context.config_path),
        "workspace_path": str(context.workspace_path) if context.workspace_path else None,
        "current_dir": str(context.current_dir),
        "git_root": git_meta.get("git_root"),
        "config_present": context.config_path.exists(),
        "config_parsed": parsed_config is not None,
    }
    return AuditReport(
        tool="openclaw-sec",
        version=__version__,
        mode="audit",
        generated_at=generated_at,
        host=host_info,
        target=target,
        summary=summary,
        findings=findings,
        notes=notes,
    )
