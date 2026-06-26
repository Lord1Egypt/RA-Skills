#!/usr/bin/env python3
"""
Generate a user-integrations.md reference file based on scan results.

Version-aware: breaking changes are filtered relative to the
user's actual HA version (detected during scan).

  ⚠️ = breaking change that ALREADY affects you
  🔮 = change in a newer version (will apply when you upgrade)
  ✨ = active integration

Usage:
  python3 generate_integration_docs.py                  # uses default paths
  python3 generate_integration_docs.py --scan-result references/ha_scan.json
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime


def parse_ha_version(version_str: str) -> tuple:
    """Parse '2026.4.1' -> (2026, 4, 1)."""
    if not version_str:
        return (0, 0, 0)
    try:
        parts = version_str.split(".")
        result = [int(p) for p in parts[:3]]
        while len(result) < 3:
            result.append(0)
        return tuple(result)
    except (ValueError, TypeError):
        return (0, 0, 0)


def version_gte(user_version: tuple, target: str) -> bool:
    """Check if user_version >= target (e.g. '2026.4')."""
    target_v = parse_ha_version(target)
    for i in range(3):
        if user_version[i] > target_v[i]:
            return True
        if user_version[i] < target_v[i]:
            return False
    return True


def parse_breaking_changes(notes_path: str) -> dict:
    """
    Parse ha-release-notes.md and extract breaking changes mapped to domains.
    Returns: { domain: [ {"version": "2026.4.1", "text": "..." }, ... ] }
    """
    breaking_changes = {}
    if not os.path.exists(notes_path):
        return breaking_changes

    try:
        with open(notes_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Warning: Could not read release notes: {e}", file=sys.stderr)
        return breaking_changes

    # Split by version headers: ## 2026.4.1 or ## Home Assistant 2026.4
    # Captures the version number from headers like "## 2026.4.1" or "## Home Assistant 2026.4.0"
    sections = re.split(r'\n## (?:Home Assistant )?(\d+\.\d+(?:\.\d+)?)', content)
    
    for i in range(1, len(sections), 2):
        version = sections[i]
        body = sections[i+1]
        
        # Find lines with (breaking-change)
        # Format: - Text ([domain docs]) (breaking-change)
        lines = body.split("\n")
        for line in lines:
            if "(breaking-change)" in line:
                # Extract domain: look for ([domain docs])
                match = re.search(r'\[(\w+) docs\]', line)
                if match:
                    domain = match.group(1)
                    # Clean up the text: remove the docs link, tag, and references
                    clean_text = line.strip().lstrip("- ")
                    clean_text = re.sub(r'\(.*?\)', '', clean_text) # remove ([@user] - [#123]) and (breaking-change)
                    clean_text = re.sub(r'\[.*?\]', '', clean_text) # remove [domain docs]
                    clean_text = clean_text.strip()
                    
                    breaking_changes.setdefault(domain, []).append({
                        "version": version,
                        "text": clean_text
                    })
    return breaking_changes


def generate_docs(scan_data: dict, output_path: str, notes_path: str):
    """Generate user-integrations.md."""
    ha_version_str = scan_data.get("ha_version", "0.0.0")
    user_version = parse_ha_version(ha_version_str)
    
    breaking_data = parse_breaking_changes(notes_path)

    lines = []
    lines.append("# User Setup: Installed Integrations Reference")
    lines.append("")
    lines.append(f"*Auto-generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}*")
    lines.append("")
    lines.append(f"> **Your HA version: {ha_version_str}**")
    lines.append("> ⚠️ = breaking change affecting you NOW")
    lines.append("> 🔮 = applies in a newer version (when you upgrade)")
    lines.append("")
    lines.append("---")
    lines.append("")

    integrations = scan_data.get("integrations", [])
    breaking_now = []
    breaking_future = []

    # Sort: HACS first, then alphabetically
    integrations.sort(key=lambda x: (not x.get("is_custom", False), x["domain"]))

    if not integrations:
        lines.append("*No integrations detected. Run the scan to populate this file.*")
    else:
        for integ in integrations:
            domain = integ.get("domain", "")
            title = integ.get("title", domain)
            state = integ.get("state", "")
            is_custom = integ.get("is_custom", False)
            
            hacs_badge = " *(Custom/HACS)*" if is_custom else ""
            icon = "✅" if state == "loaded" else "⚠️" if state else "❓"
            
            lines.append(f"### {icon} {title}{hacs_badge}")
            lines.append(f"**Domain**: `{domain}` | **Entries**: {integ.get('entries', 1)} | **State**: `{state}`")
            lines.append("")
            
            # Breaking Changes for this domain
            if domain in breaking_data:
                for bc in breaking_data[domain]:
                    is_now = version_gte(user_version, bc["version"])
                    marker = "⚠️ **Breaking**" if is_now else "🔮 **Future Breaking**"
                    ver_info = f"(in {bc['version']})"
                    lines.append(f"- {marker} {ver_info}: {bc['text']}")
                    
                    full_bc_text = f"**{title}** (`{domain}`): {bc['text']}"
                    if is_now:
                        breaking_now.append(full_bc_text)
                    else:
                        breaking_future.append((bc["version"], full_bc_text))
            else:
                lines.append("- *No recent breaking changes found in fetched release notes.*")
            
            lines.append("")
            lines.append(f"Docs: [home-assistant.io/integrations/{domain}](https://www.home-assistant.io/integrations/{domain}/)")
            lines.append("")
            lines.append("---")
            lines.append("")

    # Breaking Changes Summary
    if breaking_now or breaking_future:
        lines.append("## ⚠️ Breaking Changes Summary")
        lines.append("")
        if breaking_now:
            lines.append(f"### Affecting you NOW ({ha_version_str}):")
            lines.append("")
            for bc in sorted(set(breaking_now)):
                lines.append(f"- {bc}")
            lines.append("")
        if breaking_future:
            lines.append("### Will affect you when you upgrade:")
            lines.append("")
            for ver, bc in sorted(breaking_future):
                lines.append(f"- **{ver}**: {bc}")
            lines.append("")
        lines.append("---")
        lines.append("")

    # Summary
    hacs_count = sum(1 for i in integrations if i.get("is_custom"))
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- **HA Version**: {ha_version_str}")
    lines.append(f"- **Integrations**: {len(integrations)}")
    lines.append(f"- **Entities**: {scan_data['summary'].get('total_entities', 0)}")
    if hacs_count:
        lines.append(f"- **Custom components**: {hacs_count}")
        lines.append("")
        lines.append("⚠️ Check HACS/Custom component compatibility before Home Assistant core updates.")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Docs written to {output_path} (HA {ha_version_str})", file=sys.stderr)
    if breaking_now or breaking_future:
        print(f"Found {len(breaking_now)} current and {len(breaking_future)} future breaking changes.", file=sys.stderr)


def main():
    # Default paths resolve relative to the project root (one level up from scripts/)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    default_scan = os.path.join(project_root, "references", "ha_scan.json")
    default_notes = os.path.join(project_root, "references", "ha-release-notes.md")
    default_output = os.path.join(project_root, "references", "user-integrations.md")

    parser = argparse.ArgumentParser()
    parser.add_argument("--scan-result", default=default_scan,
                        help="Path to scan JSON (default: references/ha_scan.json)")
    parser.add_argument("--notes", default=default_notes)
    parser.add_argument("--output", default=default_output)
    args = parser.parse_args()
    
    if not os.path.exists(args.scan_result):
        # Default to a mock or empty results if file missing
        print(f"Warning: Scan result file not found: {args.scan_result}", file=sys.stderr)
        scan_data = {"ha_version": "0.0.0", "integrations": [], "summary": {}}
    else:
        with open(args.scan_result, "r", encoding="utf-8") as f:
            scan_data = json.load(f)
        
    generate_docs(scan_data, args.output, args.notes)


if __name__ == "__main__":
    main()
