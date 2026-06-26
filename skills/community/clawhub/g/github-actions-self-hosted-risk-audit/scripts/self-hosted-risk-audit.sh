#!/usr/bin/env bash
set -euo pipefail

WORKFLOW_GLOB="${WORKFLOW_GLOB:-.github/workflows/*.y*ml}"
TOP_N="${TOP_N:-20}"
OUTPUT_FORMAT="${OUTPUT_FORMAT:-text}"
WARN_SCORE="${WARN_SCORE:-4}"
CRITICAL_SCORE="${CRITICAL_SCORE:-8}"
WORKFLOW_FILE_MATCH="${WORKFLOW_FILE_MATCH:-}"
WORKFLOW_FILE_EXCLUDE="${WORKFLOW_FILE_EXCLUDE:-}"
FAIL_ON_CRITICAL="${FAIL_ON_CRITICAL:-0}"

if [[ "$OUTPUT_FORMAT" != "text" && "$OUTPUT_FORMAT" != "json" ]]; then
  echo "ERROR: OUTPUT_FORMAT must be 'text' or 'json' (got: $OUTPUT_FORMAT)" >&2
  exit 1
fi

for value_name in TOP_N WARN_SCORE CRITICAL_SCORE FAIL_ON_CRITICAL; do
  value="${!value_name}"
  if ! [[ "$value" =~ ^[0-9]+$ ]]; then
    echo "ERROR: $value_name must be a non-negative integer (got: $value)" >&2
    exit 1
  fi
done

if [[ "$TOP_N" -eq 0 ]]; then
  echo "ERROR: TOP_N must be >= 1" >&2
  exit 1
fi

if [[ "$WARN_SCORE" -gt "$CRITICAL_SCORE" ]]; then
  echo "ERROR: WARN_SCORE must be <= CRITICAL_SCORE" >&2
  exit 1
fi

python3 - "$WORKFLOW_GLOB" "$TOP_N" "$OUTPUT_FORMAT" "$WARN_SCORE" "$CRITICAL_SCORE" "$WORKFLOW_FILE_MATCH" "$WORKFLOW_FILE_EXCLUDE" "$FAIL_ON_CRITICAL" <<'PY'
import glob
import json
import re
import sys
from pathlib import Path

(
    workflow_glob,
    top_n_raw,
    output_format,
    warn_score_raw,
    critical_score_raw,
    workflow_file_match_raw,
    workflow_file_exclude_raw,
    fail_on_critical_raw,
) = sys.argv[1:]

top_n = int(top_n_raw)
warn_score = int(warn_score_raw)
critical_score = int(critical_score_raw)
fail_on_critical = fail_on_critical_raw == '1'

def compile_regex(raw: str, label: str):
    if not raw:
        return None
    try:
        return re.compile(raw)
    except re.error as exc:
        print(f"ERROR: invalid {label} regex {raw!r}: {exc}", file=sys.stderr)
        sys.exit(1)

workflow_file_match = compile_regex(workflow_file_match_raw, 'WORKFLOW_FILE_MATCH')
workflow_file_exclude = compile_regex(workflow_file_exclude_raw, 'WORKFLOW_FILE_EXCLUDE')

files = sorted(glob.glob(workflow_glob, recursive=True))
if not files:
    print(f"ERROR: no files matched WORKFLOW_GLOB={workflow_glob}", file=sys.stderr)
    sys.exit(1)

if workflow_file_match:
    files = [path for path in files if workflow_file_match.search(path)]
if workflow_file_exclude:
    files = [path for path in files if not workflow_file_exclude.search(path)]
if not files:
    print(
        "ERROR: no files left after WORKFLOW_FILE_MATCH/WORKFLOW_FILE_EXCLUDE filtering "
        f"(match={workflow_file_match_raw or '<none>'}, exclude={workflow_file_exclude_raw or '<none>'})",
        file=sys.stderr,
    )
    sys.exit(1)

self_hosted_re = re.compile(r"\bself-hosted\b", re.IGNORECASE)
pr_target_re = re.compile(r"^\s*pull_request_target\s*:")
pr_re = re.compile(r"^\s*pull_request\s*:")
issue_comment_re = re.compile(r"^\s*issue_comment\s*:")
write_perm_re = re.compile(r"^\s*[a-zA-Z_-]+\s*:\s*write\s*(?:#.*)?$")
write_all_re = re.compile(r"^\s*permissions\s*:\s*write-all\s*(?:#.*)?$", re.IGNORECASE)
checkout_uses_re = re.compile(r"^\s*(?:-\s*)?uses:\s*actions/checkout(?:@[^\s#]+)?", re.IGNORECASE)
persist_creds_false_re = re.compile(r"^\s*persist-credentials\s*:\s*false\s*(?:#.*)?$", re.IGNORECASE)

rows = []
parse_errors = []
workflows_with_self_hosted = 0

for file_path in files:
    try:
        text = Path(file_path).read_text(encoding='utf-8')
    except Exception as exc:
        parse_errors.append(f"{file_path}: {exc}")
        continue

    lines = text.splitlines()

    self_hosted_lines = []
    self_hosted_single_label_lines = []
    for idx, line in enumerate(lines, start=1):
        if self_hosted_re.search(line):
            self_hosted_lines.append(idx)
            normalized = re.sub(r"\s+", "", line.lower())
            if normalized in {
                "runs-on:self-hosted",
                "-self-hosted",
                "runs-on:[self-hosted]",
                "runs-on:[\"self-hosted\"]",
                "runs-on:['self-hosted']",
            }:
                self_hosted_single_label_lines.append(idx)

    if not self_hosted_lines:
        continue

    workflows_with_self_hosted += 1

    trigger_lines = {
        'pull_request_target': [],
        'pull_request': [],
        'issue_comment': [],
    }

    for idx, line in enumerate(lines, start=1):
        if pr_target_re.match(line):
            trigger_lines['pull_request_target'].append(idx)
        elif pr_re.match(line):
            trigger_lines['pull_request'].append(idx)
        elif issue_comment_re.match(line):
            trigger_lines['issue_comment'].append(idx)

    write_permission_lines = []
    for idx, line in enumerate(lines, start=1):
        if write_all_re.match(line) or write_perm_re.match(line):
            write_permission_lines.append(idx)

    checkout_without_persist_false = []
    for idx, line in enumerate(lines, start=1):
        if not checkout_uses_re.match(line):
            continue

        found_false = False
        base_indent = len(line) - len(line.lstrip(' '))
        for follow_idx in range(idx + 1, min(len(lines), idx + 8) + 1):
            follow = lines[follow_idx - 1]
            follow_strip = follow.strip()
            if not follow_strip:
                continue

            follow_indent = len(follow) - len(follow.lstrip(' '))
            if follow_indent <= base_indent and (follow_strip.startswith('- ') or follow_strip.startswith('uses:') or follow_strip.startswith('name:')):
                break

            if persist_creds_false_re.match(follow):
                found_false = True
                break

        if not found_false:
            checkout_without_persist_false.append(idx)

    score = 0
    issues = []

    if self_hosted_single_label_lines:
        score += 2
        issues.append({
            'code': 'self_hosted_single_label',
            'message': 'Self-hosted runner selection appears broad (`self-hosted` without extra routing labels).',
            'weight': 2,
            'lines': self_hosted_single_label_lines[:10],
        })

    if trigger_lines['pull_request_target']:
        score += 5
        issues.append({
            'code': 'pull_request_target_on_self_hosted',
            'message': 'Workflow uses pull_request_target with self-hosted runners.',
            'weight': 5,
            'lines': trigger_lines['pull_request_target'][:10],
        })

    if trigger_lines['pull_request']:
        score += 3
        issues.append({
            'code': 'pull_request_on_self_hosted',
            'message': 'Workflow uses pull_request with self-hosted runners.',
            'weight': 3,
            'lines': trigger_lines['pull_request'][:10],
        })

    if trigger_lines['issue_comment']:
        score += 2
        issues.append({
            'code': 'issue_comment_on_self_hosted',
            'message': 'Workflow can be triggered by issue comments while using self-hosted runners.',
            'weight': 2,
            'lines': trigger_lines['issue_comment'][:10],
        })

    if write_permission_lines:
        score += 3
        issues.append({
            'code': 'write_permissions_on_self_hosted',
            'message': 'Workflow includes write-capable token permissions in a self-hosted context.',
            'weight': 3,
            'lines': write_permission_lines[:10],
        })

    if checkout_without_persist_false:
        score += min(2, len(checkout_without_persist_false))
        issues.append({
            'code': 'checkout_persist_credentials_not_disabled',
            'message': 'actions/checkout is used without persist-credentials: false.',
            'weight': min(2, len(checkout_without_persist_false)),
            'lines': checkout_without_persist_false[:10],
        })

    if score == 0:
        continue

    severity = 'critical' if score >= critical_score else ('warn' if score >= warn_score else 'info')

    rows.append({
        'workflow': file_path,
        'severity': severity,
        'score': score,
        'self_hosted_lines': self_hosted_lines,
        'issues': issues,
    })

rows.sort(key=lambda item: (-item['score'], item['workflow']))
critical_rows = [row for row in rows if row['severity'] == 'critical']
warn_rows = [row for row in rows if row['severity'] == 'warn']

summary = {
    'workflows_scanned': len(files),
    'workflows_with_self_hosted': workflows_with_self_hosted,
    'workflows_flagged': len(rows),
    'critical_count': len(critical_rows),
    'warn_count': len(warn_rows),
    'warn_score': warn_score,
    'critical_score': critical_score,
    'top_n': top_n,
    'parse_errors': parse_errors,
}

if output_format == 'json':
    payload = {
        'summary': summary,
        'flagged_workflows': rows[:top_n],
        'critical_workflows': critical_rows,
    }
    print(json.dumps(payload, indent=2))
else:
    print('GitHub Actions Self-Hosted Risk Audit')
    print('=====================================')
    print(f"Workflows scanned          : {summary['workflows_scanned']}")
    print(f"With self-hosted runners   : {summary['workflows_with_self_hosted']}")
    print(f"Flagged workflows          : {summary['workflows_flagged']}")
    print(f"Critical           : {summary['critical_count']}")
    print(f"Warn               : {summary['warn_count']}")
    print(f"Thresholds         : warn>={warn_score}, critical>={critical_score}")
    if parse_errors:
        print('Parse errors       :')
        for err in parse_errors:
            print(f"  - {err}")

    if rows:
        print('\nTop flagged workflows')
        for idx, row in enumerate(rows[:top_n], start=1):
            print(f"{idx}. {row['workflow']} | severity={row['severity']} | score={row['score']}")
            for issue in row['issues']:
                lines = issue.get('lines') or []
                suffix = f" (lines: {','.join(str(line) for line in lines)})" if lines else ''
                print(f"   - [{issue['code']}] {issue['message']}{suffix}")
    else:
        print('\nNo self-hosted workflow risks detected.')

if fail_on_critical and critical_rows:
    sys.exit(1)
PY
