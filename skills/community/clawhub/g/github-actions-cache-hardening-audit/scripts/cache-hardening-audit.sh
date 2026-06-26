#!/usr/bin/env bash
set -euo pipefail

WORKFLOW_GLOB="${WORKFLOW_GLOB:-.github/workflows/*.y*ml}"
TOP_N="${TOP_N:-20}"
OUTPUT_FORMAT="${OUTPUT_FORMAT:-text}"
WARN_SCORE="${WARN_SCORE:-3}"
CRITICAL_SCORE="${CRITICAL_SCORE:-6}"
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

cache_uses_re = re.compile(r"^\s*(?:-\s*)?uses:\s*actions/cache(?:/(?:restore|save))?@([^\s#]+)", re.IGNORECASE)
pull_request_target_re = re.compile(r"^\s*pull_request_target\s*:")
key_re = re.compile(r"^\s*key\s*:\s*(.+?)\s*(?:#.*)?$")
restore_key_re = re.compile(r"^\s*-\s*(.+?)\s*$")
path_re = re.compile(r"^\s*path\s*:\s*(.+?)\s*(?:#.*)?$")
with_re = re.compile(r"^\s*with\s*:\s*$")

sensitive_path_tokens = [
    '.aws',
    '.ssh',
    '.npmrc',
    '.pypirc',
    '.git/',
]

rows = []
parse_errors = []
workflows_with_cache = 0

for file_path in files:
    try:
        text = Path(file_path).read_text(encoding='utf-8')
    except Exception as exc:
        parse_errors.append(f"{file_path}: {exc}")
        continue

    lines = text.splitlines()
    has_pr_target = any(pull_request_target_re.match(line) for line in lines)

    issues = []
    score = 0
    cache_steps = 0

    for idx, line in enumerate(lines, start=1):
        m = cache_uses_re.match(line)
        if not m:
            continue

        cache_steps += 1
        ref = (m.group(1) or '').strip()
        step_issues = []
        step_weight = 0

        if ref.lower() in {'main', 'master'}:
            step_weight += 2
            step_issues.append({
                'code': 'floating_cache_action_ref',
                'message': f'actions/cache uses floating ref @{ref}.',
                'lines': [idx],
                'weight': 2,
            })

        key_value = None
        restore_keys = []
        path_values = []

        base_indent = len(line) - len(line.lstrip(' '))
        saw_with_block = False

        for follow_idx in range(idx + 1, len(lines) + 1):
            follow = lines[follow_idx - 1]
            stripped = follow.strip()
            if not stripped:
                continue

            indent = len(follow) - len(follow.lstrip(' '))
            if indent <= base_indent and (stripped.startswith('- ') or stripped.startswith('uses:') or stripped.startswith('name:') or re.match(r'^\w', stripped)):
                break

            if with_re.match(follow):
                saw_with_block = True
                continue

            key_match = key_re.match(follow)
            if key_match:
                key_value = key_match.group(1).strip().strip('"\'')
                continue

            path_match = path_re.match(follow)
            if path_match:
                path_values.append(path_match.group(1).strip().strip('"\''))
                continue

            if saw_with_block and stripped.startswith('- '):
                rk = restore_key_re.match(follow)
                if rk:
                    restore_keys.append(rk.group(1).strip().strip('"\''))

        if has_pr_target:
            step_weight += 4
            step_issues.append({
                'code': 'cache_on_pull_request_target',
                'message': 'actions/cache is used in workflow triggered by pull_request_target (cache poisoning risk).',
                'lines': [idx],
                'weight': 4,
            })

        if key_value and 'hashFiles(' not in key_value:
            step_weight += 2
            step_issues.append({
                'code': 'cache_key_without_hashfiles',
                'message': 'Cache key does not include hashFiles(...), increasing stale-cache collisions.',
                'lines': [idx],
                'weight': 2,
            })

        broad_restore = [rk for rk in restore_keys if rk.endswith('-') and rk.count('-') <= 2]
        if broad_restore:
            step_weight += 1
            step_issues.append({
                'code': 'broad_restore_keys',
                'message': 'restore-keys appears broad and may over-share cache entries across contexts.',
                'lines': [idx],
                'weight': 1,
                'details': broad_restore[:5],
            })

        sensitive_hits = []
        for value in path_values:
            lowered = value.lower()
            for token in sensitive_path_tokens:
                if token in lowered:
                    sensitive_hits.append(value)
                    break

        if sensitive_hits:
            step_weight += 3
            step_issues.append({
                'code': 'sensitive_path_in_cache',
                'message': 'Cache path includes potentially sensitive files or directories.',
                'lines': [idx],
                'weight': 3,
                'details': sensitive_hits[:5],
            })

        if step_weight:
            score += step_weight
            issues.extend(step_issues)

    if cache_steps == 0:
        continue

    workflows_with_cache += 1
    if score == 0:
        continue

    severity = 'critical' if score >= critical_score else ('warn' if score >= warn_score else 'info')

    rows.append({
        'workflow': file_path,
        'severity': severity,
        'score': score,
        'cache_steps': cache_steps,
        'issues': issues,
    })

rows.sort(key=lambda item: (-item['score'], item['workflow']))
critical_rows = [row for row in rows if row['severity'] == 'critical']
warn_rows = [row for row in rows if row['severity'] == 'warn']

summary = {
    'workflows_scanned': len(files),
    'workflows_with_cache': workflows_with_cache,
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
    print('GitHub Actions Cache Hardening Audit')
    print('===================================')
    print(f"Workflows scanned      : {summary['workflows_scanned']}")
    print(f"With cache usage       : {summary['workflows_with_cache']}")
    print(f"Flagged workflows      : {summary['workflows_flagged']}")
    print(f"Critical               : {summary['critical_count']}")
    print(f"Warn                   : {summary['warn_count']}")
    print(f"Thresholds             : warn>={warn_score}, critical>={critical_score}")
    if parse_errors:
        print('Parse errors           :')
        for err in parse_errors:
            print(f"  - {err}")

    if rows:
        print('\nTop flagged workflows')
        for i, row in enumerate(rows[:top_n], start=1):
            print(f"{i}. {row['workflow']} | severity={row['severity']} | score={row['score']} | cache_steps={row['cache_steps']}")
            for issue in row['issues']:
                lines = issue.get('lines') or []
                line_note = f" (lines: {','.join(str(line) for line in lines)})" if lines else ''
                detail = ''
                if issue.get('details'):
                    detail = f" details={issue['details']}"
                print(f"   - [{issue['code']}] {issue['message']}{line_note}{detail}")
    else:
        print('\nNo cache hardening risks detected.')

if fail_on_critical and critical_rows:
    sys.exit(1)
PY
