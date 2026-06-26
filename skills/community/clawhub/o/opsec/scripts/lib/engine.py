#!/usr/bin/env python3
import json
import os
import re
from datetime import datetime
from uuid import uuid4

SEVERITY_ORDER = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4
}

TEXT_EXTENSIONS = {".md", ".txt", ".py", ".json", ".yaml", ".yml", ".sh"}

EXCLUDED_DIRS = {
    ".git",
    "__pycache__",
    "rules",
    "references"
}

EXCLUDED_FILES = {
    "skill.json",
    "reports.json"
}

def load_rules(rules_path):
    with open(rules_path, "r", encoding="utf-8") as f:
        return json.load(f)["rules"]

def is_text_file(path):
    _, ext = os.path.splitext(path.lower())
    base = os.path.basename(path)
    return ext in TEXT_EXTENSIONS or base == "SKILL.md"

def collect_files(skill_path):
    files = []
    skill_path_abs = os.path.abspath(skill_path)

    for root, dirnames, filenames in os.walk(skill_path_abs):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDED_DIRS]

        for name in filenames:
            if name in EXCLUDED_FILES:
                continue
            full_path = os.path.abspath(os.path.join(root, name))
            if is_text_file(full_path):
                files.append(full_path)

    return files

def read_lines(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.readlines()
    except Exception:
        return []

def severity_max(findings):
    if not findings:
        return "low"
    return max(findings, key=lambda x: SEVERITY_ORDER.get(x["severity"], 0))["severity"]

def install_verdict(overall_risk):
    if overall_risk == "critical":
        return "do_not_install_until_reviewed"
    if overall_risk == "high":
        return "install_only_after_manual_review"
    if overall_risk == "medium":
        return "review_recommended"
    return "no_major_risk_found"

def compile_pattern(pattern_obj):
    value = pattern_obj["value"]
    match_type = pattern_obj.get("match_type", "substring")

    if match_type == "word":
        return {
            "kind": "regex",
            "pattern": re.compile(r"\b" + re.escape(value) + r"\b", re.IGNORECASE)
        }

    if match_type == "regex":
        return {
            "kind": "regex",
            "pattern": re.compile(value, re.IGNORECASE)
        }

    return {
        "kind": "substring",
        "pattern": value.lower()
    }

def compile_rule(rule):
    return {
        "rule_id": rule["rule_id"],
        "title": rule["title"],
        "severity": rule["severity"],
        "why_it_matters": rule["why_it_matters"],
        "recommendation": rule["recommendation"],
        "fix_command": rule.get("fix_command", ""),
        "patterns": [compile_pattern(p) for p in rule.get("patterns", [])],
        "exclude_patterns": [
            re.compile(p, re.IGNORECASE) for p in rule.get("exclude_patterns", [])
        ]
    }

def build_rule_index(rules):
    return [compile_rule(rule) for rule in rules]

def line_is_excluded(line, rule):
    for pattern in rule.get("exclude_patterns", []):
        if pattern.search(line):
            return True
    return False

def pattern_matches(line, compiled_pattern):
    if compiled_pattern["kind"] == "substring":
        return compiled_pattern["pattern"] in line.lower()
    return bool(compiled_pattern["pattern"].search(line))

def summarize_findings(findings):
    counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    by_rule = {}

    for finding in findings:
        sev = finding["severity"]
        counts[sev] = counts.get(sev, 0) + 1
        by_rule[finding["rule_id"]] = by_rule.get(finding["rule_id"], 0) + 1

    return {
        "severity_counts": counts,
        "rule_counts": by_rule
    }

def scan_skill(skill_path, rules):
    findings = []
    seen = set()
    indexed_rules = build_rule_index(rules)
    files = collect_files(skill_path)

    for path in files:
        lines = read_lines(path)
        rel_path = os.path.relpath(path, skill_path)

        for line_no, line in enumerate(lines, start=1):
            stripped = line.strip()
            if not stripped:
                continue

            for rule in indexed_rules:
                if line_is_excluded(stripped, rule):
                    continue

                matched = False
                for compiled_pattern in rule["patterns"]:
                    if pattern_matches(stripped, compiled_pattern):
                        matched = True
                        break

                if not matched:
                    continue

                dedupe_key = (
                    rule["rule_id"],
                    rel_path,
                    line_no,
                    stripped[:200]
                )
                if dedupe_key in seen:
                    continue
                seen.add(dedupe_key)

                findings.append({
                    "rule_id": rule["rule_id"],
                    "title": rule["title"],
                    "severity": rule["severity"],
                    "matched_file": rel_path,
                    "matched_line": line_no,
                    "evidence": stripped[:300],
                    "why_it_matters": rule["why_it_matters"],
                    "recommendation": rule["recommendation"],
                    "fix_command": rule["fix_command"]
                })

    findings.sort(
        key=lambda x: (
            -SEVERITY_ORDER.get(x["severity"], 0),
            x["matched_file"],
            x["matched_line"]
        )
    )

    overall = severity_max(findings)

    return {
        "report_id": f"OPSEC-{uuid4().hex[:8].upper()}",
        "created_at": datetime.utcnow().isoformat(),
        "skill_path": os.path.abspath(skill_path),
        "overall_risk": overall,
        "install_verdict": install_verdict(overall),
        "summary": summarize_findings(findings),
        "findings": findings
    }
