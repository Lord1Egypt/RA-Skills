#!/usr/bin/env python3
import json

SEVERITY_LABELS = {
    "critical": "critical",
    "high": "high",
    "medium": "medium",
    "low": "low"
}

RULE_SUMMARY_LABELS = {
    "OPSEC-006": "explicit secret exposure guidance",
    "OPSEC-001": "shell execution signals",
    "OPSEC-002": "external-call or download signals",
    "OPSEC-003": "credential-related documentation",
    "OPSEC-004": "privilege or sensitive access signals",
    "OPSEC-005": "unsafe operational claims"
}

VERDICT_TEXT = {
    "do_not_install_until_reviewed": "Review the critical findings before installing.",
    "install_only_after_manual_review": "Review the high-risk findings before installing.",
    "review_recommended": "Review the flagged findings before installing.",
    "no_major_risk_found": "No major risky patterns found in reviewed files."
}

def print_human_report(report):
    print(f"Report ID: {report['report_id']}")
    print(f"Skill Path: {report['skill_path']}")
    print(f"Overall Risk: {report['overall_risk']}")
    print(f"Install Verdict: {report['install_verdict']}")
    print(f"Findings: {len(report['findings'])}")

    summary = report.get("summary", {})
    sev = summary.get("severity_counts", {})
    if summary:
        print(
            "Severity Summary: "
            f"critical={sev.get('critical', 0)}, "
            f"high={sev.get('high', 0)}, "
            f"medium={sev.get('medium', 0)}, "
            f"low={sev.get('low', 0)}"
        )

    note = report.get("note", "").strip()
    if note:
        print(f"Note: {note}")

    print("")

    if not report["findings"]:
        print("No risky patterns found.")
        return

    for idx, finding in enumerate(report["findings"], start=1):
        print(f"[{idx}] {finding['severity'].upper()} | {finding['rule_id']} | {finding['title']}")
        print(f"Matched File: {finding['matched_file']}")
        print(f"Matched Line: {finding['matched_line']}")
        print(f"Evidence: {finding['evidence']}")
        print(f"Why it matters: {finding['why_it_matters']}")
        print(f"Recommendation: {finding['recommendation']}")
        if finding.get("fix_command"):
            print(f"Fix command: {finding['fix_command']}")
        print("")

def build_summary_lines(report):
    summary = report.get("summary", {})
    sev = summary.get("severity_counts", {})
    rule_counts = summary.get("rule_counts", {})

    critical_labels = []
    high_labels = []
    medium_labels = []

    for rule_id, count in rule_counts.items():
        label = RULE_SUMMARY_LABELS.get(rule_id, rule_id)
        if count <= 0:
            continue

        # infer severity from findings
        matched_severity = None
        for finding in report.get("findings", []):
            if finding["rule_id"] == rule_id:
                matched_severity = finding["severity"]
                break

        if matched_severity == "critical":
            critical_labels.append(label)
        elif matched_severity == "high":
            high_labels.append(label)
        elif matched_severity == "medium":
            medium_labels.append(label)

    def uniq(items):
        seen = set()
        out = []
        for item in items:
            if item not in seen:
                seen.add(item)
                out.append(item)
        return out

    critical_labels = uniq(critical_labels)
    high_labels = uniq(high_labels)
    medium_labels = uniq(medium_labels)

    critical_text = ", ".join(critical_labels) if critical_labels else "none"
    high_text = ", ".join(high_labels) if high_labels else "none"
    medium_text = ", ".join(medium_labels) if medium_labels else "none"

    lines = [
        f"Overall Risk: {report['overall_risk']}",
        f"Critical: {sev.get('critical', 0)} ({critical_text})",
        f"High: {sev.get('high', 0)} ({high_text})",
        f"Medium: {sev.get('medium', 0)} ({medium_text} — review recommended, not a blocker)",
        f"Verdict: {VERDICT_TEXT.get(report['install_verdict'], report['install_verdict'])}"
    ]

    note = report.get("note", "").strip()
    if note:
        lines.append(f"Note: {note}")

    return lines

def print_summary_only(report):
    for line in build_summary_lines(report):
        print(line)

def print_json(report):
    print(json.dumps(report, indent=2, ensure_ascii=False))
