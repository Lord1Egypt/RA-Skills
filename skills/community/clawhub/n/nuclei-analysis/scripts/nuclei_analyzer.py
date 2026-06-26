#!/usr/bin/env python3
"""
nuclei-analysis - Parse, prioritize, and report on Nuclei scan findings.
Usage: python3 nuclei_analyzer.py <nuclei-output.txt> [--min-severity high] [--output report.md]
"""

import sys
import json
import re
import os
from datetime import datetime
from pathlib import Path

SEVERITY_ORDER = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3, 'info': 4, 'unknown': 5}

# Common false positives to filter
FALSE_POSITIVE_PATTERNS = [
    (re.compile(r'403 forbidden', re.IGNORECASE), '403 Forbidden (no further context)'),
    (re.compile(r'self-signed certificate', re.IGNORECASE), 'Self-signed certificate'),
    (re.compile(r'robots\.txt', re.IGNORECASE), 'Robots.txt access'),
    (re.compile(r'sitemap\.xml', re.IGNORECASE), 'Sitemap.xml access'),
    (re.compile(r'favicon\.ico', re.IGNORECASE), 'Favicon detection'),
    (re.compile(r'nginx.*version', re.IGNORECASE), 'Generic nginx version disclosure'),
    (re.compile(r'apache.*version', re.IGNORECASE), 'Generic apache version disclosure'),
    (re.compile(r'csrf.*token', re.IGNORECASE), 'CSRF token detection (info only)'),
    (re.compile(r'clickjacking', re.IGNORECASE), 'X-Frame-Options check (info)'),
]

# Severity override for known safe templates
SEVERITY_OVERRIDE = {
    'http/missing-security-headers/x-frame-options': 'low',
    'http/missing-security-headers/x-xss-protection': 'low',
    'http/missing-security-headers/content-security-policy': 'low',
    'http/technologies/trace-method': 'info',
    'http/technologies/options-method': 'info',
}


def is_false_positive(info):
    """Check if a finding is a known false positive."""
    for pattern, reason in FALSE_POSITIVE_PATTERNS:
        if pattern.search(info):
            return reason
    return None


def parse_nuclei_line(line):
    """Parse a nuclei output line (supports both JSON and text formats)."""
    line = line.strip()
    if not line:
        return None

    # Try JSON format (newline-delimited)
    try:
        obj = json.loads(line)
        return {
            'template': obj.get('template-id', obj.get('template', 'unknown')),
            'name': obj.get('info', {}).get('name', obj.get('name', 'unknown')),
            'severity': obj.get('info', {}).get('severity', obj.get('severity', 'unknown')).lower(),
            'host': obj.get('host', obj.get('matched-at', 'unknown')),
            'url': obj.get('url', obj.get('matched-at', 'unknown')),
            'matched_at': obj.get('matched-at', ''),
            'description': obj.get('info', {}).get('description', ''),
            'severity_override': SEVERITY_OVERRIDE.get(obj.get('template-id', ''), None),
        }
    except json.JSONDecodeError:
        pass

    # Try plain text format: [severity] template-name | info | host
    text_match = re.match(r'\[(\w+)\]\s+([^\|]+)\|(.+?)\|?\s*(https?://\S+)?', line)
    if text_match:
        sev, template, info, url = text_match.groups()
        fp_reason = is_false_positive(info)
        return {
            'template': template.strip(),
            'name': template.strip(),
            'severity': sev.lower().strip(),
            'host': url or '',
            'url': url or '',
            'matched_at': '',
            'description': info.strip(),
            'false_positive': fp_reason,
            'severity_override': SEVERITY_OVERRIDE.get(template.strip(), None),
        }

    return None


def analyze(file_path, min_severity='low'):
    """Read nuclei output and produce analysis."""
    if not os.path.exists(file_path):
        print(f'File not found: {file_path}', file=sys.stderr)
        sys.exit(1)

    with open(file_path) as f:
        lines = f.readlines()

    findings = []
    for line in lines:
        parsed = parse_nuclei_line(line)
        if parsed:
            # Apply severity override
            if parsed.get('severity_override'):
                parsed['severity'] = parsed['severity_override']
            # Skip false positives
            if parsed.get('false_positive'):
                parsed['filtered'] = parsed['false_positive']
            else:
                findings.append(parsed)

    # Filter by minimum severity
    min_idx = SEVERITY_ORDER.get(min_severity, 4)
    findings = [f for f in findings if SEVERITY_ORDER.get(f['severity'], 5) <= min_idx]

    # Sort by severity then by template
    findings.sort(key=lambda f: (SEVERITY_ORDER.get(f['severity'], 5), f['template']))

    return findings


def generate_report(findings, target='unknown', output_file=None):
    """Generate a Markdown report from findings."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Group by severity
    groups = {}
    for f in findings:
        sev = f['severity']
        groups.setdefault(sev, []).append(f)

    lines = []
    lines.append(f'# Nuclei Scan Analysis Report')
    lines.append(f'')
    lines.append(f'**Target:** {target}')
    lines.append(f'**Analyzed:** {timestamp}')
    lines.append(f'**Total findings (post-filter):** {len(findings)}')
    lines.append(f'')
    lines.append(f'## Summary by Severity')
    lines.append(f'')
    lines.append(f'| Severity | Count |')
    lines.append(f'|----------|-------:|')

    total = 0
    for sev in ['critical', 'high', 'medium', 'low', 'info']:
        if sev in groups:
            count = len(groups[sev])
            total += count
            emoji = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🟢', 'info': '⚪'}.get(sev, '⚪')
            lines.append(f'| {emoji} {sev.upper()} | {count} |')

    lines.append(f'| **TOTAL** | **{total}** |')
    lines.append(f'')

    # High+ detailed findings
    for sev in ['critical', 'high']:
        if sev not in groups:
            continue
        lines.append(f'## {sev.upper()} Severity Findings')
        lines.append(f'')
        for f in groups[sev]:
            lines.append(f'### {f["name"]}')
            lines.append(f'')
            lines.append(f'- **Template:** `{f["template"]}`')
            lines.append(f'- **URL:** {f.get("url", "unknown")}')
            if f.get('description'):
                lines.append(f'- **Description:** {f["description"]}')
            if f.get('matched_at'):
                lines.append(f'- **Matched at:** {f["matched_at"]}')
            # Attack scenario
            lines.append(f'')
            lines.append(f'**Attack Scenario:**')
            lines.append(f'An attacker could exploit this finding to {f["description"].lower() if f.get("description") else "impact the target"}.')
            lines.append(f'')
            lines.append(f'**Suggested Steps to Reproduce:**')
            lines.append(f'1. Navigate to `{f.get("url", "<target>")}`')
            lines.append(f'2. Confirm the {f["name"].lower()} condition exists')
            lines.append(f'3. Craft a proof-of-concept payload based on the template')
            lines.append(f'4. Verify impact and document with screenshots/curl logs')
            lines.append(f'')

    # Medium/Low table
    for sev in ['medium', 'low', 'info']:
        if sev not in groups:
            continue
        lines.append(f'## {sev.upper()} Severity ({len(groups[sev])} findings)')
        lines.append(f'')
        lines.append(f'| Template | URL | Description |')
        lines.append(f'|----------|-----|-------------|')
        for f in groups[sev]:
            desc = (f.get('description') or '').replace('|', '/').strip()[:60]
            url = f.get('url', '')[:60]
            lines.append(f'| `{f["template"]}` | {url} | {desc} |')
        lines.append(f'')

    report = '\n'.join(lines)

    if output_file:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w') as f:
            f.write(report)
        print(f'Report saved to: {output_file}')

    return report


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Analyze Nuclei scan results')
    parser.add_argument('input', help='Nuclei output file (.txt or .jsonl)')
    parser.add_argument('--min-severity', default='low',
                        choices=['critical', 'high', 'medium', 'low', 'info'],
                        help='Minimum severity to include (default: low)')
    parser.add_argument('--output', '-o', help='Output file path (default: stdout)')
    parser.add_argument('--target', '-t', default='unknown',
                        help='Target name for report header')

    args = parser.parse_args()

    # Try to extract target from filename
    if args.target == 'unknown':
        basename = os.path.basename(args.input)
        target = re.sub(r'\.(txt|jsonl?|ndjson|log).*', '', basename)
        if target in ('nuclei', 'scan', 'output'):
            target = 'target'
        args.target = target

    # Default output path
    if not args.output:
        reports_dir = os.path.join(os.path.dirname(__file__), '..', 'reports', 'nuclei-analysis')
        args.output = os.path.join(reports_dir, f'{args.target}-{datetime.now().strftime("%Y%m%d-%H%M%S")}.md')
    else:
        args.output = os.path.expanduser(args.output)

    findings = analyze(args.input, args.min_severity)
    print(f'Parsed {len(findings)} findings (min severity: {args.min_severity})')
    report = generate_report(findings, args.target, args.output)
    print()
    print(report)


if __name__ == '__main__':
    main()