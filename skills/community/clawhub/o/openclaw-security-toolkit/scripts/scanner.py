#!/usr/bin/env python3
"""
OpenClaw Security Guard - Secret Scanner
Scans for exposed API keys, tokens, passwords, and other sensitive information.
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional

from utils import (
    OPENCLAW_DIR, CONFIG_FILE, mask_secret,
    Colors, print_severity
)


# Secret detection patterns
SECRET_PATTERNS = [
    {
        "id": "SEC001",
        "name": "OpenAI API Key",
        "pattern": r"sk-[a-zA-Z0-9]{20,}",
        "severity": "critical",
        "description": "OpenAI API key detected"
    },
    {
        "id": "SEC002",
        "name": "Feishu App Secret",
        "pattern": r'"appSecret"\s*:\s*"([a-zA-Z0-9]{16,})"',
        "severity": "critical",
        "description": "Feishu app secret detected"
    },
    {
        "id": "SEC003",
        "name": "Feishu App ID",
        "pattern": r'"appId"\s*:\s*"(cli_[a-zA-Z0-9]+)"',
        "severity": "medium",
        "description": "Feishu app ID detected"
    },
    {
        "id": "SEC004",
        "name": "API Key (generic)",
        "pattern": r'[aA]pi[Kk]ey["\']?\s*[:=]\s*["\']?([a-zA-Z0-9_\-]{20,})',
        "severity": "high",
        "description": "Generic API key detected"
    },
    {
        "id": "SEC005",
        "name": "Token (generic)",
        "pattern": r'"token"\s*:\s*"([a-zA-Z0-9]{16,})"',
        "severity": "high",
        "description": "Token detected"
    },
    {
        "id": "SEC006",
        "name": "Password in config",
        "pattern": r'[pP]assword["\']?\s*[:=]\s*["\']?([^\s"\']{8,})',
        "severity": "high",
        "description": "Password detected in configuration"
    },
    {
        "id": "SEC007",
        "name": "Private Key",
        "pattern": r"-----BEGIN\s+[A-Z]+\s+PRIVATE\s+KEY-----",
        "severity": "critical",
        "description": "Private key detected"
    },
    {
        "id": "SEC008",
        "name": "AWS Access Key",
        "pattern": r"AKIA[0-9A-Z]{16}",
        "severity": "critical",
        "description": "AWS access key detected"
    },
    {
        "id": "SEC009",
        "name": "Generic Secret",
        "pattern": r'"secret"\s*:\s*"([a-zA-Z0-9_\-]{16,})"',
        "severity": "high",
        "description": "Secret value detected"
    },
    {
        "id": "SEC010",
        "name": "Tavily API Key",
        "pattern": r"tvly-dev-[a-zA-Z0-9]+",
        "severity": "high",
        "description": "Tavily API key detected"
    }
]


def scan_file(filepath: Path, custom_patterns: List[Dict] = None) -> List[Dict]:
    """Scan a single file for secrets."""
    findings = []

    if not filepath.exists():
        return findings

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except:
        return findings

    patterns = SECRET_PATTERNS.copy()
    if custom_patterns:
        patterns.extend(custom_patterns)

    for i, line in enumerate(content.split('\n'), 1):
        for pattern_info in patterns:
            pattern = pattern_info["pattern"]
            matches = re.finditer(pattern, line)

            for match in matches:
                # Get the matched value
                if match.groups():
                    matched_value = match.group(1) if len(match.groups()) > 0 else match.group(0)
                else:
                    matched_value = match.group(0)

                findings.append({
                    "id": pattern_info["id"],
                    "file": str(filepath),
                    "line": i,
                    "name": pattern_info["name"],
                    "severity": pattern_info["severity"],
                    "description": pattern_info["description"],
                    "matched": mask_secret(matched_value),
                    "full_match": matched_value[:50] + "..." if len(matched_value) > 50 else matched_value,
                    "auto_fixable": False
                })

    return findings


def scan_directory(dirpath: Path, ignore_patterns: List[str] = None) -> List[Dict]:
    """Scan a directory for secrets."""
    findings = []
    ignore_patterns = ignore_patterns or []

    if not dirpath.exists():
        return findings

    for root, dirs, files in os.walk(dirpath):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        for filename in files:
            # Skip ignored files
            skip = False
            for pattern in ignore_patterns:
                if re.match(pattern.replace('*', '.*'), filename):
                    skip = True
                    break
            if skip:
                continue

            # Only scan text files
            if filename.endswith(('.json', '.env', '.yaml', '.yml', '.conf', '.config', '.ini', '.txt', '.md')):
                filepath = Path(root) / filename
                findings.extend(scan_file(filepath))

    return findings


def scan_secrets(
    custom_patterns: List[Dict] = None,
    deep: bool = False,
    quiet: bool = False
) -> Dict:
    """
    Scan for exposed secrets.

    Args:
        custom_patterns: Additional patterns to scan for
        deep: Include deeper scan of all config files
        quiet: Suppress output

    Returns:
        Dict with scan results
    """
    all_findings = []
    scanned_files = []

    # Default scan paths
    scan_paths = [
        CONFIG_FILE,
        OPENCLAW_DIR / ".env",
    ]

    # Deep scan includes more paths
    if deep:
        scan_paths.extend([
            OPENCLAW_DIR / "credentials",
            OPENCLAW_DIR / "workspace",
        ])

    for path in scan_paths:
        if path.is_file():
            findings = scan_file(path, custom_patterns)
            all_findings.extend(findings)
            scanned_files.append(str(path))
        elif path.is_dir():
            findings = scan_directory(path)
            all_findings.extend(findings)
            scanned_files.append(str(path))

    # Deduplicate findings
    seen = set()
    unique_findings = []
    for f in all_findings:
        key = (f["file"], f["line"], f["id"])
        if key not in seen:
            seen.add(key)
            unique_findings.append(f)

    return {
        "findings": unique_findings,
        "scanned_files": scanned_files,
        "total": len(unique_findings),
        "summary": {
            "critical": sum(1 for f in unique_findings if f["severity"] == "critical"),
            "high": sum(1 for f in unique_findings if f["severity"] == "high"),
            "medium": sum(1 for f in unique_findings if f["severity"] == "medium"),
            "low": sum(1 for f in unique_findings if f["severity"] == "low"),
        }
    }


def print_scan_results(results: Dict, i18n: Dict, verbose: bool = False):
    """Print scan results in table format."""
    findings = results["findings"]
    summary = results["summary"]

    if not findings:
        print(f"{Colors.GREEN}✅ {i18n['messages']['no_issues']}{Colors.RESET}")
        return

    print(f"\n{Colors.BOLD}🔍 {i18n.get('scan_results', 'Scan Results')}{Colors.RESET}\n")

    # Group by severity
    for severity in ["critical", "high", "medium", "low"]:
        sev_findings = [f for f in findings if f["severity"] == severity]
        if not sev_findings:
            continue

        sev_label = print_severity(severity, i18n)
        print(f"\n{sev_label}\n")

        for f in sev_findings:
            print(f"  {Colors.YELLOW}•{Colors.RESET} {f['name']}")
            print(f"    {Colors.CYAN}File:{Colors.RESET} {f['file']}:{f['line']}")
            if verbose:
                print(f"    {Colors.CYAN}Match:{Colors.RESET} {f['matched']}")
            print(f"    {Colors.CYAN}ID:{Colors.RESET} {f['id']}")
            print()

    # Summary
    print(f"\n{Colors.BOLD}📊 Summary{Colors.RESET}")
    print(f"  Scanned files: {len(results['scanned_files'])}")
    print(f"  Critical: {summary['critical']}")
    print(f"  High: {summary['high']}")
    print(f"  Medium: {summary['medium']}")
    print(f"  Low: {summary['low']}")


if __name__ == "__main__":
    # Test scan
    results = scan_secrets(deep=True)
    print(json.dumps(results, indent=2, ensure_ascii=False))