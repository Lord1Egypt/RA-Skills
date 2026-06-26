from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

from openclaw_sec.audit import run_audit
from openclaw_sec.models import AuditContext
from openclaw_sec.report import render_text, write_reports
from openclaw_sec.utils import expand_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="openclaw-sec", description="Local security audit for OpenClaw environments")
    subparsers = parser.add_subparsers(dest="command", required=True)

    audit_parser = subparsers.add_parser("audit", help="Run the local audit")
    audit_parser.add_argument("--config", default="~/.openclaw/openclaw.json", help="Path to the OpenClaw config")
    audit_parser.add_argument("--workspace", default=None, help="Path to the OpenClaw workspace")
    audit_parser.add_argument("--output-dir", default=None, help="Directory for generated reports")
    audit_parser.add_argument("--format", default="all", choices=["text", "json", "md", "all"], help="Output format")
    audit_parser.add_argument("--no-git", action="store_true", help="Skip git tracked file scan")
    audit_parser.add_argument("--no-host", action="store_true", help="Skip host and network checks")
    audit_parser.add_argument("--strict", action="store_true", help="Exit non-zero if high or critical findings exist")
    audit_parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command != "audit":
        parser.error("unsupported command")

    workspace = expand_path(args.workspace)
    if workspace is None:
        default_workspace = expand_path("~/.openclaw/workspace")
        workspace = default_workspace if default_workspace and default_workspace.exists() else None

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = expand_path(args.output_dir) if args.output_dir else Path.cwd() / f"openclaw-sec-report-{timestamp}"
    context = AuditContext(
        config_path=expand_path(args.config) or Path("~/.openclaw/openclaw.json").expanduser(),
        workspace_path=workspace,
        output_dir=output_dir,
        output_format=args.format,
        enable_git=not args.no_git,
        enable_host=not args.no_host,
        strict=args.strict,
        debug=args.debug,
        current_dir=Path.cwd(),
    )

    report = run_audit(context)
    paths = write_reports(report, context.output_dir, context.output_format)
    text_summary = render_text(report)
    print(text_summary)
    if paths:
        print("")
        print("Report files:")
        for kind, path in sorted(paths.items()):
            print(f"  {kind}: {path}")

    if args.strict and any(finding.severity in {"critical", "high"} for finding in report.findings):
        return 2
    return 0
