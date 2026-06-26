#!/usr/bin/env python3
"""
mcpsec-skill: Scan MCP server configuration files using mcpsec.

Discovers MCP config files on the system, runs mcpsec against each one,
and reports findings grouped by severity. Exits non-zero only if findings
at or above the configured threshold are found.

mcpsec binary must be available on PATH. Read-only — does not modify any
config files. subprocess is used with shell=False exclusively; all paths
are validated before use.
"""

import argparse
import json
import os
import re
import subprocess
from pathlib import Path


# ---------------------------------------------------------------------------
# Known MCP config locations to check
# ---------------------------------------------------------------------------

_CANDIDATE_PATHS: list[str] = [
    # Claude Desktop (macOS)
    "~/Library/Application Support/Claude/claude_desktop_config.json",
    # Claude Desktop Extensions directory (macOS)
    "~/Library/Application Support/Claude/Claude Extensions/",
    # Cursor (macOS)
    "~/.cursor/mcp.json",
    # VS Code (common extension path)
    "~/.vscode/mcp.json",
    # OpenClaw workspace configs
    "~/.openclaw/workspace/mcp-config.json",
    # Custom project configs (current dir)
    "./mcp-config.json",
    "./claude_desktop_config.json",
]

# Regex for safe path characters (no shell metacharacters)
_SAFE_PATH = re.compile(r"^[a-zA-Z0-9_\-./~ ]+$")


def _sanitize_path(p: str) -> str | None:
    """Return the path if it looks safe, else None."""
    if _SAFE_PATH.match(p):
        return p
    return None


def _run(cmd: list[str], timeout: int = 60) -> tuple[int, str, str]:
    """
    Run cmd with shell=False and return (returncode, stdout, stderr).

    shell=False is required — arguments are passed as a list, never
    interpolated into a shell string, preventing injection. Errors are
    returned as non-zero exit codes rather than raised.
    """
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=False,  # explicit: never interpret cmd as a shell string
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return 1, "", "Timed out"
    except FileNotFoundError:
        return 1, "", f"Binary not found: {cmd[0]}"
    except OSError as e:
        return 1, "", str(e)


def check_mcpsec() -> bool:
    """Return True if mcpsec is available on PATH."""
    code, out, _ = _run(["mcpsec", "version"])
    if code == 0:
        print(f"✅ {out}")
        return True
    print("❌ mcpsec not found — install from https://github.com/pfrederiksen/mcpsec")
    return False


def discover_configs(extra_paths: list[str]) -> list[Path]:
    """Return a list of existing MCP config paths to scan."""
    candidates = list(_CANDIDATE_PATHS) + extra_paths
    found: list[Path] = []

    for raw in candidates:
        expanded = os.path.expanduser(raw)
        safe = _sanitize_path(expanded)
        if safe is None:
            continue
        p = Path(safe)
        if p.exists():
            found.append(p)

    return found


def scan_config(config_path: Path, severity_filter: str, fail_on: str) -> dict:
    """
    Run mcpsec scan on a single config path and return a result dict.

    Returns:
        {
            "path": str,
            "findings": int,
            "output": str,
            "failed_threshold": bool,
        }
    """
    cmd = ["mcpsec", "scan", "--format", "json"]
    if severity_filter:
        cmd += ["--severity", severity_filter]
    if fail_on:
        cmd += ["--fail-on", fail_on]
    cmd.append(str(config_path))

    code, stdout, stderr = _run(cmd)

    # mcpsec exits 1 when --fail-on threshold is met (not an error)
    failed_threshold = code != 0 and fail_on and not stderr

    try:
        data = json.loads(stdout) if stdout else []
    except json.JSONDecodeError:
        data = []

    return {
        "path": str(config_path),
        "findings": len(data) if isinstance(data, list) else 0,
        "output": stdout or stderr,
        "data": data if isinstance(data, list) else [],
        "failed_threshold": failed_threshold,
    }


def format_text_report(results: list[dict]) -> str:
    """Format scan results as a human-readable text report."""
    if not results:
        return "No MCP config files found to scan."

    lines: list[str] = []
    total_findings = sum(r["findings"] for r in results)
    threshold_hits = [r for r in results if r["failed_threshold"]]

    header = f"🔍 MCPSec — {len(results)} config(s) scanned, {total_findings} finding(s)"
    if threshold_hits:
        header += f" — ⚠️ {len(threshold_hits)} above threshold"
    lines.append(header)
    lines.append("")

    for r in results:
        lines.append(f"📄 {r['path']}")
        if r["findings"] == 0:
            lines.append("   ✅ No findings")
        else:
            for finding in r["data"]:
                sev = finding.get("severity", "?").upper()
                rule = finding.get("finding", {}).get("uid", "?")
                title = finding.get("finding", {}).get("title", "?")
                resource = ""
                resources = finding.get("resources", [])
                if resources:
                    resource = f" [{resources[0].get('name', '')}]"
                icon = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🟢"}.get(sev, "⚪")
                lines.append(f"   {icon} [{sev}] {rule}: {title}{resource}")
        lines.append("")

    return "\n".join(lines).strip()


def main() -> None:
    """Parse arguments, discover configs, run scans, print report."""
    parser = argparse.ArgumentParser(
        description="Scan MCP server configs using mcpsec.",
    )
    parser.add_argument(
        "configs",
        nargs="*",
        help="Config file(s) or directory(s) to scan (auto-discovers if omitted)",
    )
    parser.add_argument(
        "--severity",
        default="",
        help="Filter by severity: critical,high,medium,low (default: all)",
    )
    parser.add_argument(
        "--fail-on",
        default="critical",
        help="Exit 1 if findings at or above this severity (default: critical)",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Only print output if findings exist",
    )
    args = parser.parse_args()

    if not check_mcpsec():
        raise SystemExit(1)

    extra = [p for p in args.configs if _sanitize_path(os.path.expanduser(p))]
    configs = discover_configs(extra) if not args.configs else [
        Path(os.path.expanduser(p)) for p in extra if Path(os.path.expanduser(p)).exists()
    ]

    if not configs:
        if not args.quiet:
            print("ℹ️  No MCP config files found. Nothing to scan.")
        return

    results = [scan_config(c, args.severity, args.fail_on) for c in configs]
    total_findings = sum(r["findings"] for r in results)
    threshold_hit = any(r["failed_threshold"] for r in results)

    if args.quiet and total_findings == 0:
        return

    if args.format == "json":
        print(json.dumps(results, indent=2))
    else:
        print(format_text_report(results))

    if threshold_hit:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
