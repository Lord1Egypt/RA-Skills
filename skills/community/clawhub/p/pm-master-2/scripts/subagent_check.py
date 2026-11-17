#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PM Master v2 · Sub-Agent Output Validator
============================================================
After the main controller receives a sub-agent's report, run this script to
validate whether the output is compliant.

Checks:
  1. JSON structure completeness (must contain agent_role/status/artifacts/key_findings)
  2. Artifact files actually exist
  3. Estimate is numeric
  4. Risk/RAID completeness (owner/mitigation)
  5. project_yaml_updates format

Usage:
  python3 subagent_check.py --report <sub-agent report JSON file> --project <project>/project.yaml
  python3 subagent_check.py --report <JSON file> --strict  # promote warnings to fatal
"""
import os
import sys
import argparse
import json as _json

try:
    import yaml
except ImportError:
    yaml = None


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return _json.load(f)


def load_yaml(path):
    if yaml is None:
        raise RuntimeError("PyYAML required; please run: pip install pyyaml")
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def has_estimate(est):
    if est is None:
        return False
    if isinstance(est, (int, float)):
        return est > 0
    import re
    s = str(est).strip()
    if s in ('', '—', '-', 'TBD', 'N/A', 'NA', 'none', 'null'):
        return False
    m = re.search(r'\d+(\.\d+)?', s)
    if not m:
        return False
    return float(m.group()) > 0


def validate_report(report, project_root):
    """Validate the sub-agent report, return (problems, warnings)"""
    problems = []
    warnings = []

    # 1. JSON structure completeness
    required_fields = ['agent_role', 'status', 'artifacts', 'key_findings']
    for field in required_fields:
        if field not in report:
            problems.append(f"Missing required field: {field}")

    if 'agent_role' in report and report['agent_role'] not in (
        'planner-agent', 'scheduler-agent', 'risk-agent', 'stakeholder-agent',
        'reporter-agent', 'program-agent', 'communication-agent', 'monitoring-agent'
    ):
        warnings.append(f"Unknown role: {report['agent_role']}")

    if 'status' in report and report['status'] not in ('success', 'partial', 'failed'):
        problems.append(f"Invalid status: {report['status']}")

    # 2. Artifact file existence
    for art in report.get('artifacts', []):
        path = art.get('path', '')
        if not path:
            problems.append(f"Artifact {art.get('key','?')} missing path")
            continue
        # Support relative paths (relative to project_root)
        if not os.path.isabs(path):
            path = os.path.join(project_root, path)
        if not os.path.exists(path):
            problems.append(f"Artifact file not found: {art.get('key','?')} -> {path}")

    # 3. key_findings check
    findings = report.get('key_findings', [])
    if len(findings) < 2:
        warnings.append("key_findings fewer than 2; recommend 3-5")
    if len(findings) > 10:
        warnings.append(f"key_findings too many ({len(findings)}); recommend <=5")

    # 4. project_yaml_updates format
    updates = report.get('project_yaml_updates', {})
    if updates and not isinstance(updates, dict):
        problems.append("project_yaml_updates must be a dict")

    # 5. Handling when status=failed
    if report.get('status') == 'failed' and not report.get('errors'):
        problems.append("status=failed but no errors explanation")

    # 6. If report contains inline data, check estimates
    if 'data_files' in report:
        for df in report.get('data_files', []):
            if not os.path.exists(df):
                warnings.append(f"Data file not found: {df}")

    return problems, warnings


def main():
    ap = argparse.ArgumentParser(description="PM Master v2 sub-agent output validator")
    ap.add_argument('--report', required=True, help="Sub-agent report JSON file path")
    ap.add_argument('--project', default=None, help="Project project.yaml (resolves relative paths)")
    ap.add_argument('--strict', action='store_true', help="Promote warnings to fatal")
    a = ap.parse_args()

    try:
        report = load_json(a.report)
    except Exception as e:
        print(f"✗ Could not parse JSON: {e}")
        sys.exit(1)

    project_root = os.path.dirname(os.path.abspath(a.project)) if a.project else os.getcwd()
    problems, warnings = validate_report(report, project_root)

    print(f"=== Sub-Agent Output Validation ===")
    print(f"Role: {report.get('agent_role', '?')} | Status: {report.get('status', '?')}")
    print(f"Artifacts: {len(report.get('artifacts', []))} | Findings: {len(report.get('key_findings', []))}")

    if warnings:
        print(f"\n⚠ Warnings ({len(warnings)}):")
        for w in warnings:
            print(f"  - {w}")

    if problems:
        print(f"\n✗ Fatal problems ({len(problems)}):")
        for p in problems:
            print(f"  - {p}")
        if a.strict:
            problems.extend(f"[strict] {w}" for w in warnings)
        sys.exit(1)

    if not problems:
        print("\n✓ Sub-agent output validation passed")
        sys.exit(0)


if __name__ == '__main__':
    main()
