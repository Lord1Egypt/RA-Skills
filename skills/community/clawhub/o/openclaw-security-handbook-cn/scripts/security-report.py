#!/usr/bin/env python3
"""
OpenClaw Security Report Generator

Parses `openclaw security audit --json` output and produces a formatted
security report with severity grouping and fix guidance.

Usage:
    python3 security-report.py [--json INPUT_JSON] [--fix]

If --json is omitted, runs `openclaw security audit --json` directly.

Output: formatted markdown report to stdout.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

SEVERITY_ORDER = {"critical": 0, "warn": 1, "info": 2}
SEVERITY_SYMBOLS = {
    "critical": "🔴",
    "warn": "🟡",
    "info": "ℹ️",
}
SEVERITY_LABELS = {
    "critical": "CRITICAL — 必须立即处理",
    "warn": "WARN — 建议处理",
    "info": "INFO — 供参考",
}


def run_audit() -> dict:
    """Run `openclaw security audit --json` and return parsed JSON."""
    print("[*] Running openclaw security audit --json ...", file=sys.stderr)
    result = subprocess.run(
        ["openclaw", "security", "audit", "--json"],
        capture_output=True,
        text=True,
        timeout=60,
    )
    if result.returncode != 0:
        print(f"[!] audit returned code {result.returncode}", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        sys.exit(1)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as e:
        print(f"[!] Failed to parse JSON: {e}", file=sys.stderr)
        sys.exit(1)


def format_report(audit_data: dict, fix_mode: bool = False) -> str:
    """Format audit JSON into a markdown security report."""
    lines = []
    lines.append("# 🔒 OpenClaw 安全审计报告\n")

    # Summary
    summary = audit_data.get("summary", {})
    total = summary.get("totalFindings", "?")
    severity_counts = summary.get("severityCounts", {})

    lines.append(f"**总计发现**: {total} 项\n")

    # Severity breakdown
    for sev, label in SEVERITY_LABELS.items():
        count = severity_counts.get(sev, 0)
        symbol = SEVERITY_SYMBOLS.get(sev, "•")
        lines.append(f"- {symbol} {label.split('—')[0].strip()}: **{count}** 项\n")

    lines.append("---\n")

    # Findings
    findings = audit_data.get("findings", [])

    # Group by severity
    grouped = {}
    for f in findings:
        sev = f.get("severity", "info")
        grouped.setdefault(sev, []).append(f)

    # Sort groups by severity
    for sev in sorted(grouped.keys(), key=lambda s: SEVERITY_ORDER.get(s, 9)):
        symbol = SEVERITY_SYMBOLS.get(sev, "•")
        label = SEVERITY_LABELS.get(sev, sev)
        lines.append(f"## {symbol} {label}\n")
        lines.append(f"| checkId | 标题 | 当前状态 | 建议 |\n")
        lines.append(f"|---------|------|----------|------|\n")

        for finding in grouped[sev]:
            check_id = finding.get("checkId", "")
            title = finding.get("title", "")
            detail = finding.get("detail", "")
            remediation = finding.get("remediation", "")

            # Truncate detail to first line for the table
            detail_short = detail.split("\n")[0][:80]
            if len(detail) > 80:
                detail_short += "..."

            # Clean markdown pipes from text
            detail_short = detail_short.replace("|", "\\|")
            remediation_clean = remediation.replace("|", "\\|")

            lines.append(
                f"| `{check_id}` | {title} | {detail_short} | {remediation_clean} |\n"
            )

        lines.append("\n")

    # Secret diagnostics
    secret_diags = audit_data.get("secretDiagnostics", [])
    if secret_diags:
        lines.append("## 🔍 密钥泄露检测\n")
        lines.append(f"发现 **{len(secret_diags)}** 处可能的密钥泄露：\n\n")
        for diag in secret_diags:
            file_path = diag.get("file", "")
            line_num = diag.get("line", "")
            matched = diag.get("matched", "")
            lines.append(f"- `{file_path}:{line_num}` — 匹配 `{matched}`\n")
        lines.append(
            "\n⚠️ **建议**：在修复前先备份日志，然后用 `sed` 或编辑器清除明文密钥。\n"
        )
        lines.append("```bash\n")
        lines.append("# 备份后再清理（请确认范围）\n")
        lines.append("cp -r ~/.openclaw/sessions/ /tmp/sessions-backup/\n")
        lines.append(
            "# sed -i 's/sk-[A-Za-z0-9]\\{20,\\}/[REDACTED]/g' ~/.openclaw/sessions/*.jsonl\n"
        )
        lines.append("```\n")

    # Fix mode summary
    if fix_mode:
        lines.append("---\n")
        lines.append("## 🛠️ 自动修复建议\n")
        lines.append(
            "以下修复项可以安全地自动执行。复制命令到终端，或回复编号选择执行：\n\n"
        )
        fix_num = 1
        for sev in sorted(grouped.keys(), key=lambda s: SEVERITY_ORDER.get(s, 9)):
            for finding in grouped[sev]:
                remediation = finding.get("remediation", "")
                if remediation and "openclaw security audit --fix" not in remediation:
                    lines.append(f"{fix_num}. {remediation}\n")
                    fix_num += 1

    # Footer
    lines.append("---\n")
    lines.append("*由 openclaw-security skill 生成 | 基于 ZAST.AI Security Handbook*\n")

    return "".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Parse openclaw security audit JSON into a formatted report."
    )
    parser.add_argument(
        "--json",
        type=Path,
        default=None,
        help="Path to JSON file (reads from stdin if omitted)",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Include auto-fix guidance in the report",
    )
    args = parser.parse_args()

    if args.json:
        audit_data = json.loads(args.json.read_text())
    else:
        audit_data = run_audit()

    report = format_report(audit_data, fix_mode=args.fix)
    print(report)


if __name__ == "__main__":
    main()
