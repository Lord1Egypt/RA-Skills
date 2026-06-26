#!/usr/bin/env bash
set -euo pipefail

WORKFLOW_GLOB="${WORKFLOW_GLOB:-.github/workflows/*.y*ml}"
TOP_N="${TOP_N:-20}"
OUTPUT_FORMAT="${OUTPUT_FORMAT:-text}"
WARN_SCORE="${WARN_SCORE:-2}"
CRITICAL_SCORE="${CRITICAL_SCORE:-5}"
FLAG_MISSING_PERMISSIONS="${FLAG_MISSING_PERMISSIONS:-1}"
FLAG_WRITE_ALL="${FLAG_WRITE_ALL:-1}"
FLAG_WRITE_SCOPES="${FLAG_WRITE_SCOPES:-1}"
WORKFLOW_FILE_MATCH="${WORKFLOW_FILE_MATCH:-}"
WORKFLOW_FILE_EXCLUDE="${WORKFLOW_FILE_EXCLUDE:-}"
EVENT_MATCH="${EVENT_MATCH:-}"
EVENT_EXCLUDE="${EVENT_EXCLUDE:-}"
PERMISSION_MATCH="${PERMISSION_MATCH:-}"
PERMISSION_EXCLUDE="${PERMISSION_EXCLUDE:-}"
FAIL_ON_CRITICAL="${FAIL_ON_CRITICAL:-0}"

if [[ "$OUTPUT_FORMAT" != "text" && "$OUTPUT_FORMAT" != "json" ]]; then
  echo "ERROR: OUTPUT_FORMAT must be 'text' or 'json' (got: $OUTPUT_FORMAT)" >&2
  exit 1
fi

for value_name in TOP_N WARN_SCORE CRITICAL_SCORE FLAG_MISSING_PERMISSIONS FLAG_WRITE_ALL FLAG_WRITE_SCOPES FAIL_ON_CRITICAL; do
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

python3 - "$WORKFLOW_GLOB" "$TOP_N" "$OUTPUT_FORMAT" "$WARN_SCORE" "$CRITICAL_SCORE" "$FLAG_MISSING_PERMISSIONS" "$FLAG_WRITE_ALL" "$FLAG_WRITE_SCOPES" "$WORKFLOW_FILE_MATCH" "$WORKFLOW_FILE_EXCLUDE" "$EVENT_MATCH" "$EVENT_EXCLUDE" "$PERMISSION_MATCH" "$PERMISSION_EXCLUDE" "$FAIL_ON_CRITICAL" <<'PY'
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
    flag_missing_permissions_raw,
    flag_write_all_raw,
    flag_write_scopes_raw,
    workflow_file_match_raw,
    workflow_file_exclude_raw,
    event_match_raw,
    event_exclude_raw,
    permission_match_raw,
    permission_exclude_raw,
    fail_on_critical_raw,
) = sys.argv[1:]

top_n = int(top_n_raw)
warn_score = int(warn_score_raw)
critical_score = int(critical_score_raw)
flag_missing_permissions = flag_missing_permissions_raw == '1'
flag_write_all = flag_write_all_raw == '1'
flag_write_scopes = flag_write_scopes_raw == '1'
fail_on_critical = fail_on_critical_raw == '1'


def compile_optional(name: str, pattern: str):
    if not pattern:
        return None
    try:
        return re.compile(pattern)
    except re.error as exc:
        print(f"ERROR: invalid {name} {pattern!r}: {exc}", file=sys.stderr)
        sys.exit(1)


workflow_file_match = compile_optional('WORKFLOW_FILE_MATCH', workflow_file_match_raw)
workflow_file_exclude = compile_optional('WORKFLOW_FILE_EXCLUDE', workflow_file_exclude_raw)
event_match = compile_optional('EVENT_MATCH', event_match_raw)
event_exclude = compile_optional('EVENT_EXCLUDE', event_exclude_raw)
permission_match = compile_optional('PERMISSION_MATCH', permission_match_raw)
permission_exclude = compile_optional('PERMISSION_EXCLUDE', permission_exclude_raw)

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

trigger_key_re = re.compile(r"^(push|pull_request|pull_request_target|workflow_dispatch|repository_dispatch|schedule|merge_group|workflow_run|release):")
write_scope_re = re.compile(r"^\s*([A-Za-z0-9_-]+)\s*:\s*write\s*(?:#.*)?$")


def extract_event_set(lines):
    events = set()
    in_on = False
    on_indent = -1
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue
        indent = len(line) - len(line.lstrip(' '))
        if re.match(r'^on\s*:\s*$', line):
            in_on = True
            on_indent = indent
            continue
        if in_on:
            if indent <= on_indent and stripped:
                in_on = False
            else:
                match = trigger_key_re.match(stripped)
                if match:
                    events.add(match.group(1))
    return sorted(events)


rows = []
parse_errors = []
skipped_by_filter = []

for file_path in files:
    try:
        text = Path(file_path).read_text(encoding='utf-8')
    except Exception as exc:
        parse_errors.append(f"{file_path}: {exc}")
        continue

    lines = text.splitlines()
    events = extract_event_set(lines)

    if event_match and not any(event_match.search(event) for event in events):
        skipped_by_filter.append(file_path)
        continue
    if event_exclude and any(event_exclude.search(event) for event in events):
        skipped_by_filter.append(file_path)
        continue

    permission_entries = []
    permissions_blocks = 0

    in_permissions = False
    permission_indent = -1

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue

        indent = len(line) - len(line.lstrip(' '))

        if re.match(r'^\s*permissions\s*:\s*$', line):
            permissions_blocks += 1
            in_permissions = True
            permission_indent = indent
            continue

        if in_permissions and indent <= permission_indent and stripped:
            in_permissions = False

        if in_permissions:
            write_match = write_scope_re.match(line)
            if write_match:
                scope = write_match.group(1)
                permission_entries.append({'line': idx, 'scope': scope, 'value': 'write'})
                continue

        inline_match = re.match(r'^\s*permissions\s*:\s*([^#]+?)\s*(?:#.*)?$', line)
        if inline_match:
            value = inline_match.group(1).strip().strip('"\'')
            lowered = value.lower()
            if lowered in {'write-all', 'read-all'}:
                permission_entries.append({'line': idx, 'scope': lowered, 'value': lowered})

    has_permission_policy = permissions_blocks > 0 or any(entry['value'] in {'write-all', 'read-all'} for entry in permission_entries)

    broad_write_entries = []
    for entry in permission_entries:
        scope = entry['scope']
        value = entry['value']

        if permission_match and not permission_match.search(f"{scope}:{value}"):
            continue
        if permission_exclude and permission_exclude.search(f"{scope}:{value}"):
            continue

        if value == 'write-all':
            broad_write_entries.append({**entry, 'reason': 'write-all grants write access to all token scopes'})
        elif value == 'write':
            broad_write_entries.append({**entry, 'reason': f"{scope}: write expands token access beyond read-only"})

    pull_request_target_write_risk = False
    if 'pull_request_target' in events:
        pull_request_target_write_risk = any(
            entry['value'] == 'write-all' or entry['value'] == 'write'
            for entry in broad_write_entries
        )

    score = 0
    findings = []

    if flag_missing_permissions and not has_permission_policy:
        score += 2
        findings.append('missing explicit permissions policy')

    if flag_write_all:
        write_all_hits = [entry for entry in broad_write_entries if entry['value'] == 'write-all']
        if write_all_hits:
            score += len(write_all_hits) * 4
            findings.append(f"{len(write_all_hits)} write-all grant(s)")

    if flag_write_scopes:
        write_scope_hits = [entry for entry in broad_write_entries if entry['value'] == 'write']
        if write_scope_hits:
            score += len(write_scope_hits)
            findings.append(f"{len(write_scope_hits)} scope-specific write grant(s)")

    if pull_request_target_write_risk:
        score += 3
        findings.append('pull_request_target combined with write token permissions')

    severity = 'ok'
    if score >= critical_score:
        severity = 'critical'
    elif score >= warn_score:
        severity = 'warn'

    rows.append(
        {
            'workflow_file': file_path,
            'severity': severity,
            'score': score,
            'events': events,
            'has_explicit_permissions': has_permission_policy,
            'findings': findings,
            'broad_permission_entries': broad_write_entries,
            'pull_request_target_write_risk': pull_request_target_write_risk,
        }
    )

rows.sort(key=lambda row: (-row['score'], row['workflow_file']))
critical_rows = [row for row in rows if row['severity'] == 'critical']

summary = {
    'files_scanned': len(files),
    'files_evaluated': len(rows),
    'files_skipped_by_filter': len(skipped_by_filter),
    'parse_errors': parse_errors,
    'critical_workflows': len(critical_rows),
    'warn_workflows': len([row for row in rows if row['severity'] == 'warn']),
    'ok_workflows': len([row for row in rows if row['severity'] == 'ok']),
    'warn_score': warn_score,
    'critical_score': critical_score,
}

if output_format == 'json':
    print(json.dumps({'summary': summary, 'workflows': rows[:top_n], 'all_workflows': rows, 'critical_workflows': critical_rows}, indent=2, sort_keys=True))
else:
    print('GITHUB ACTIONS PERMISSION SCOPE AUDIT')
    print('---')
    print(
        'SUMMARY: '
        f"files={summary['files_scanned']} evaluated={summary['files_evaluated']} filtered={summary['files_skipped_by_filter']} "
        f"critical={summary['critical_workflows']} warn={summary['warn_workflows']} ok={summary['ok_workflows']}"
    )
    if parse_errors:
        print('PARSE_ERRORS:')
        for err in parse_errors:
            print(f'- {err}')
    print('---')
    print(f"TOP WORKFLOWS ({min(top_n, len(rows))})")
    if not rows:
        print('none')
    else:
        for row in rows[:top_n]:
            print(
                f"- [{row['severity']}] file={row['workflow_file']} score={row['score']} "
                f"events={','.join(row['events']) if row['events'] else '<none>'} "
                f"permissions={len(row['broad_permission_entries'])} "
                f"findings={'; '.join(row['findings']) if row['findings'] else 'none'}"
            )

sys.exit(1 if (fail_on_critical and critical_rows) else 0)
PY
