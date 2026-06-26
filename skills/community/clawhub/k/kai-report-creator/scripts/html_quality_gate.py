#!/usr/bin/env python3
"""Validate final HTML report quality gates.

This complements guard_validate.py, which validates IR before rendering.
html_quality_gate.py validates the final HTML shell, theme fidelity, and KPI
rendering so direct HTML generation cannot bypass the guardrails.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import html as html_lib
import json
import re
import sys
from pathlib import Path


PLACEHOLDER_RE = re.compile(r"\[(?:INSERT VALUE|数据待填写)\]")

STANDARD_REQUIRED_IDS = [
    "report-summary",
    "toc-toggle-btn",
    "toc-sidebar",
    "card-mode-btn",
    "sc-overlay",
    "edit-hotzone",
    "edit-toggle",
    "export-btn",
    "export-menu",
    "export-print",
    "export-png-desktop",
    "export-png-mobile",
    "export-im-share",
]

THEME_MARKERS = {
    "corporate-blue": ["/* Theme: corporate-blue", "--font-sans:", "body { font-family: var(--font-sans)"],
    "minimal": ["/* Theme: minimal", "--font-sans:", "body { font-family: var(--font-sans)"],
    "dark-tech": ["/* Theme: dark-tech", "--font-mono:", "body { font-family: var(--font-sans)"],
    "dark-board": ["/* Theme: dark-board", "--font-mono:", "body { font-family: var(--font-sans)"],
    "data-story": ["/* Theme: data-story", "--font-sans:", "body { font-family: var(--font-sans)"],
    "newspaper": ["/* Theme: newspaper", "--font-sans:", "body { font-family: var(--font-sans)"],
    "regular-lumen": [
        "/* Theme: regular-lumen",
        "--bg: #F7F5F1",
        "--font-sans: 'Playfair Display'",
        "body { font-family: var(--font-sans)",
        ".report-wrapper { max-width: 920px",
        ".main-with-toc",
    ],
    "fangsong": [
        "/* Theme: fangsong",
        "--font-sans: 'FangSong'",
        "body { font-family: var(--font-sans-ui)",
        ".report-wrapper { max-width: 920px",
    ],
}


@dataclass(frozen=True)
class Finding:
    code: str
    message: str


def strip_tags(fragment: str) -> str:
    text = re.sub(r"<[^>]+>", "", fragment)
    return html_lib.unescape(text).strip()


def has_real_number(value: str) -> bool:
    return bool(re.search(r"\d", value)) and not PLACEHOLDER_RE.search(value)


def extract_theme(html: str) -> str | None:
    match = re.search(r'data-theme=["\']([^"\']+)["\']', html)
    return match.group(1) if match else None


def extract_summary_json(html: str) -> dict[str, object] | None:
    match = re.search(
        r'<script\b[^>]*id=["\']report-summary["\'][^>]*>\s*(.*?)\s*</script>',
        html,
        re.DOTALL,
    )
    if not match:
        return None
    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError:
        return None


def kpi_values_from_html(html: str) -> list[str]:
    pattern = re.compile(
        r'<div\b[^>]*class=["\'][^"\']*\bkpi-value\b[^"\']*["\'][^>]*>(.*?)</div>',
        re.DOTALL,
    )
    return [strip_tags(match.group(1)) for match in pattern.finditer(html)]


def validate_standard_shell(html: str) -> list[Finding]:
    findings: list[Finding] = []
    for element_id in STANDARD_REQUIRED_IDS:
        if f'id="{element_id}"' not in html and f"id='{element_id}'" not in html:
            findings.append(
                Finding("shell.missing_id", f"Missing standard shell element id={element_id!r}.")
            )
    if 'data-template="kai-report-creator"' not in html and "data-template='kai-report-creator'" not in html:
        findings.append(Finding("shell.missing_template_attr", "Missing data-template marker."))
    if 'data-version=' not in html:
        findings.append(Finding("shell.missing_version_attr", "Missing data-version marker."))
    if 'data-theme=' not in html:
        findings.append(Finding("shell.missing_theme_attr", "Missing data-theme marker."))
    return findings


def validate_theme_fidelity(html: str) -> list[Finding]:
    findings: list[Finding] = []
    theme = extract_theme(html)
    if not theme:
        return [Finding("theme.missing", "Missing data-theme attribute.")]

    markers = THEME_MARKERS.get(theme)
    if not markers:
        return findings

    for marker in markers:
        if marker not in html:
            findings.append(
                Finding("theme.fingerprint_mismatch", f"{theme} HTML missing theme marker: {marker}")
            )

    if theme == "regular-lumen":
        body_rule_match = re.search(r"body\s*\{[^}]*\}", html, re.DOTALL)
        body_rule = body_rule_match.group(0) if body_rule_match else ""
        if "max-width" in body_rule or re.search(r"padding\s*:\s*2rem", body_rule):
            findings.append(
                Finding(
                    "theme.regular_lumen_body_layout",
                    "regular-lumen must use .report-wrapper for width/padding, not body max-width/padding.",
                )
            )
        if "background-color: var(--bg)" in body_rule and "background: var(--bg)" not in body_rule:
            findings.append(
                Finding(
                    "theme.regular_lumen_background",
                    "regular-lumen body should preserve the theme background declaration.",
                )
            )
    return findings


def validate_kpi_values(html: str) -> list[Finding]:
    findings: list[Finding] = []
    for value in kpi_values_from_html(html):
        if not has_real_number(value):
            findings.append(Finding("kpi.invalid_value", f"Invalid KPI value: {value!r}."))

    summary = extract_summary_json(html)
    if not summary:
        findings.append(Finding("summary.invalid_json", "Missing or invalid report-summary JSON."))
        return findings

    kpis = summary.get("kpis", [])
    if not isinstance(kpis, list):
        findings.append(Finding("summary.invalid_kpis", "report-summary.kpis must be a list."))
        return findings

    for item in kpis:
        if not isinstance(item, dict):
            findings.append(Finding("summary.invalid_kpi_item", "Each summary KPI must be an object."))
            continue
        value = str(item.get("value", "")).strip()
        if value and not has_real_number(value):
            findings.append(Finding("summary.invalid_kpi_value", f"Invalid summary KPI value: {value!r}."))
    return findings


def validate_html_text(
    html: str,
    *,
    standard_shell: bool = True,
    theme_fidelity: bool = True,
    kpi_values: bool = True,
) -> dict[str, object]:
    findings: list[Finding] = []
    if standard_shell:
        findings.extend(validate_standard_shell(html))
    if theme_fidelity:
        findings.extend(validate_theme_fidelity(html))
    if kpi_values:
        findings.extend(validate_kpi_values(html))

    return {
        "status": "valid" if not findings else "invalid",
        "findings": [asdict(finding) for finding in findings],
        "exit_code": 0 if not findings else 1,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate final HTML report quality gates.")
    parser.add_argument("html_path", help="Path to generated HTML report")
    parser.add_argument("--no-standard-shell", action="store_true", help="Skip standard shell checks")
    parser.add_argument("--no-theme-fidelity", action="store_true", help="Skip theme fidelity checks")
    parser.add_argument("--no-kpi-values", action="store_true", help="Skip KPI value checks")
    args = parser.parse_args()

    html_text = Path(args.html_path).read_text(encoding="utf-8")
    report = validate_html_text(
        html_text,
        standard_shell=not args.no_standard_shell,
        theme_fidelity=not args.no_theme_fidelity,
        kpi_values=not args.no_kpi_values,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    sys.exit(int(report["exit_code"]))


if __name__ == "__main__":
    main()
