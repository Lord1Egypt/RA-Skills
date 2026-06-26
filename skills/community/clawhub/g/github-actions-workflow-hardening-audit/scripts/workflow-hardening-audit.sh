#!/usr/bin/env bash
set -euo pipefail

WORKFLOW_GLOB="${WORKFLOW_GLOB:-.github/workflows/*.y*ml}"
TOP_N="${TOP_N:-20}"
OUTPUT_FORMAT="${OUTPUT_FORMAT:-text}"
WARN_SCORE="${WARN_SCORE:-3}"
CRITICAL_SCORE="${CRITICAL_SCORE:-7}"
REQUIRE_TIMEOUT="${REQUIRE_TIMEOUT:-1}"
REQUIRE_PERMISSIONS="${REQUIRE_PERMISSIONS:-1}"
REQUIRE_CONCURRENCY="${REQUIRE_CONCURRENCY:-0}"
FLAG_FLOATING_REFS="${FLAG_FLOATING_REFS:-1}"
ALLOW_REF_REGEX="${ALLOW_REF_REGEX:-}"
WORKFLOW_FILE_MATCH="${WORKFLOW_FILE_MATCH:-}"
WORKFLOW_FILE_EXCLUDE="${WORKFLOW_FILE_EXCLUDE:-}"
EVENT_MATCH="${EVENT_MATCH:-}"
EVENT_EXCLUDE="${EVENT_EXCLUDE:-}"
FAIL_ON_CRITICAL="${FAIL_ON_CRITICAL:-0}"

if [[ "$OUTPUT_FORMAT" != "text" && "$OUTPUT_FORMAT" != "json" ]]; then
  echo "ERROR: OUTPUT_FORMAT must be 'text' or 'json' (got: $OUTPUT_FORMAT)" >&2
  exit 1
fi

for value_name in TOP_N WARN_SCORE CRITICAL_SCORE REQUIRE_TIMEOUT REQUIRE_PERMISSIONS REQUIRE_CONCURRENCY FLAG_FLOATING_REFS FAIL_ON_CRITICAL; do
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

python3 - "$WORKFLOW_GLOB" "$TOP_N" "$OUTPUT_FORMAT" "$WARN_SCORE" "$CRITICAL_SCORE" "$REQUIRE_TIMEOUT" "$REQUIRE_PERMISSIONS" "$REQUIRE_CONCURRENCY" "$FLAG_FLOATING_REFS" "$ALLOW_REF_REGEX" "$WORKFLOW_FILE_MATCH" "$WORKFLOW_FILE_EXCLUDE" "$EVENT_MATCH" "$EVENT_EXCLUDE" "$FAIL_ON_CRITICAL" <<'PY'
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
    require_timeout_raw,
    require_permissions_raw,
    require_concurrency_raw,
    flag_floating_refs_raw,
    allow_ref_regex_raw,
    workflow_file_match_raw,
    workflow_file_exclude_raw,
    event_match_raw,
    event_exclude_raw,
    fail_on_critical_raw,
) = sys.argv[1:]

top_n = int(top_n_raw)
warn_score = int(warn_score_raw)
critical_score = int(critical_score_raw)
require_timeout = require_timeout_raw == '1'
require_permissions = require_permissions_raw == '1'
require_concurrency = require_concurrency_raw == '1'
flag_floating_refs = flag_floating_refs_raw == '1'
fail_on_critical = fail_on_critical_raw == '1'

allow_ref_regex = None
if allow_ref_regex_raw:
    try:
        allow_ref_regex = re.compile(allow_ref_regex_raw)
    except re.error as exc:
        print(f"ERROR: invalid ALLOW_REF_REGEX {allow_ref_regex_raw!r}: {exc}", file=sys.stderr)
        sys.exit(1)

workflow_file_match = None
if workflow_file_match_raw:
    try:
        workflow_file_match = re.compile(workflow_file_match_raw)
    except re.error as exc:
        print(f"ERROR: invalid WORKFLOW_FILE_MATCH {workflow_file_match_raw!r}: {exc}", file=sys.stderr)
        sys.exit(1)

workflow_file_exclude = None
if workflow_file_exclude_raw:
    try:
        workflow_file_exclude = re.compile(workflow_file_exclude_raw)
    except re.error as exc:
        print(f"ERROR: invalid WORKFLOW_FILE_EXCLUDE {workflow_file_exclude_raw!r}: {exc}", file=sys.stderr)
        sys.exit(1)

event_match = None
if event_match_raw:
    try:
        event_match = re.compile(event_match_raw)
    except re.error as exc:
        print(f"ERROR: invalid EVENT_MATCH {event_match_raw!r}: {exc}", file=sys.stderr)
        sys.exit(1)

event_exclude = None
if event_exclude_raw:
    try:
        event_exclude = re.compile(event_exclude_raw)
    except re.error as exc:
        print(f"ERROR: invalid EVENT_EXCLUDE {event_exclude_raw!r}: {exc}", file=sys.stderr)
        sys.exit(1)

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

job_key_re = re.compile(r"^[A-Za-z0-9_.-]+:\s*(#.*)?$")
uses_re = re.compile(r"^\s*(?:-\s*)?uses:\s*([^\s#]+)")
trigger_key_re = re.compile(r"^(push|pull_request|pull_request_target|workflow_dispatch|repository_dispatch|schedule|merge_group|workflow_run|release):")


def classify_ref(uses_value: str):
    if '@' not in uses_value:
        return None
    ref = uses_value.rsplit('@', 1)[1].strip()
    if allow_ref_regex and allow_ref_regex.search(ref):
        return None
    lowered = ref.lower()
    if lowered in {'main', 'master', 'head', 'latest', 'stable', 'trunk', 'dev', 'develop'}:
        return 'branch-like'
    if re.match(r'^v\d+$', lowered):
        return 'major-tag'
    return None


rows = []
parse_errors = []
skipped_by_event_filter = []

for file_path in files:
    try:
        text = Path(file_path).read_text(encoding='utf-8')
    except Exception as exc:
        parse_errors.append(f"{file_path}: {exc}")
        continue

    lines = text.splitlines()
    workflow_permissions = False
    workflow_concurrency = False
    events = set()

    in_on = False
    on_indent = -1

    in_jobs = False
    jobs_indent = -1
    current_job = None
    total_jobs = 0
    job_timeout = {}
    job_permissions = {}
    job_concurrency = {}

    floating_refs = []

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue

        indent = len(line) - len(line.lstrip(' '))

        if re.match(r'^permissions\s*:', line):
            workflow_permissions = True
        if re.match(r'^concurrency\s*:', line):
            workflow_concurrency = True

        if re.match(r'^on\s*:\s*$', line):
            in_on = True
            on_indent = indent
            continue

        if in_on:
            if indent <= on_indent and stripped:
                in_on = False
            else:
                trigger_match = trigger_key_re.match(stripped)
                if trigger_match:
                    events.add(trigger_match.group(1))

        use_match = uses_re.match(line)
        if use_match and flag_floating_refs:
            uses_value = use_match.group(1)
            reason = classify_ref(uses_value)
            if reason:
                floating_refs.append({'line': idx, 'uses': uses_value, 'reason': reason})

        if not in_jobs and re.match(r'^jobs\s*:\s*$', line):
            in_jobs = True
            jobs_indent = indent
            current_job = None
            continue

        if in_jobs:
            if indent <= jobs_indent and stripped:
                in_jobs = False
                current_job = None
                continue

            if indent == jobs_indent + 2 and job_key_re.match(stripped):
                current_job = stripped.split(':', 1)[0]
                total_jobs += 1
                job_timeout[current_job] = False
                job_permissions[current_job] = False
                job_concurrency[current_job] = False
                continue

            if current_job and indent > jobs_indent + 2:
                if re.match(r'^\s*timeout-minutes\s*:', line):
                    job_timeout[current_job] = True
                if re.match(r'^\s*permissions\s*:', line):
                    job_permissions[current_job] = True
                if re.match(r'^\s*concurrency\s*:', line):
                    job_concurrency[current_job] = True

    matched_events = sorted(events)
    if event_match and not any(event_match.search(event) for event in matched_events):
        skipped_by_event_filter.append(file_path)
        continue
    if event_exclude and any(event_exclude.search(event) for event in matched_events):
        skipped_by_event_filter.append(file_path)
        continue

    missing_timeout_jobs = []
    missing_permission_jobs = []
    missing_concurrency_jobs = []

    if require_timeout:
        missing_timeout_jobs = [job for job, has_timeout in job_timeout.items() if not has_timeout]

    if require_permissions:
        if workflow_permissions:
            missing_permission_jobs = []
        elif total_jobs:
            missing_permission_jobs = [job for job, has_permissions in job_permissions.items() if not has_permissions]
        else:
            missing_permission_jobs = ['<workflow>']

    if require_concurrency:
        if workflow_concurrency:
            missing_concurrency_jobs = []
        elif total_jobs:
            missing_concurrency_jobs = [job for job, has_concurrency in job_concurrency.items() if not has_concurrency]
        else:
            missing_concurrency_jobs = ['<workflow>']

    score = 0
    score += len(missing_timeout_jobs) * 2
    score += len(missing_permission_jobs) * 1
    score += len(missing_concurrency_jobs) * 1
    score += len(floating_refs) * 2
    if 'pull_request_target' in events:
        score += 2

    severity = 'ok'
    if score >= critical_score:
        severity = 'critical'
    elif score >= warn_score:
        severity = 'warn'

    row = {
        'workflow_file': file_path,
        'severity': severity,
        'score': score,
        'total_jobs': total_jobs,
        'missing_timeout_jobs': missing_timeout_jobs,
        'missing_permission_jobs': missing_permission_jobs,
        'missing_concurrency_jobs': missing_concurrency_jobs,
        'floating_refs': floating_refs,
        'events': matched_events,
    }
    rows.append(row)

rows.sort(key=lambda row: (-row['score'], row['workflow_file']))
critical_rows = [row for row in rows if row['severity'] == 'critical']

summary = {
    'files_scanned': len(files),
    'files_evaluated': len(rows),
    'files_skipped_by_event_filter': len(skipped_by_event_filter),
    'parse_errors': parse_errors,
    'critical_workflows': len(critical_rows),
    'warn_workflows': len([row for row in rows if row['severity'] == 'warn']),
    'ok_workflows': len([row for row in rows if row['severity'] == 'ok']),
    'warn_score': warn_score,
    'critical_score': critical_score,
    'checks': {
        'require_timeout': require_timeout,
        'require_permissions': require_permissions,
        'require_concurrency': require_concurrency,
        'flag_floating_refs': flag_floating_refs,
        'allow_ref_regex': allow_ref_regex_raw or None,
        'workflow_file_match': workflow_file_match_raw or None,
        'workflow_file_exclude': workflow_file_exclude_raw or None,
        'event_match': event_match_raw or None,
        'event_exclude': event_exclude_raw or None,
    },
}

if output_format == 'json':
    print(json.dumps({'summary': summary, 'workflows': rows[:top_n], 'all_workflows': rows, 'critical_workflows': critical_rows}, indent=2, sort_keys=True))
else:
    print('GITHUB ACTIONS WORKFLOW HARDENING AUDIT')
    print('---')
    print(
        'SUMMARY: '
        f"files={summary['files_scanned']} evaluated={summary['files_evaluated']} filtered={summary['files_skipped_by_event_filter']} "
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
                f"- [{row['severity']}] file={row['workflow_file']} score={row['score']} jobs={row['total_jobs']} "
                f"missing_timeout={len(row['missing_timeout_jobs'])} "
                f"missing_permissions={len(row['missing_permission_jobs'])} "
                f"missing_concurrency={len(row['missing_concurrency_jobs'])} "
                f"floating_refs={len(row['floating_refs'])} "
                f"events={','.join(row['events']) if row['events'] else '<none>'}"
            )

sys.exit(1 if (fail_on_critical and critical_rows) else 0)
PY
