#!/usr/bin/env bash
set -euo pipefail

RUN_GLOB="${RUN_GLOB:-artifacts/github-actions/*.json}"
TOP_N="${TOP_N:-24}"
OUTPUT_FORMAT="${OUTPUT_FORMAT:-text}"
WARN_FAILURE_RUNS="${WARN_FAILURE_RUNS:-3}"
CRITICAL_FAILURE_RUNS="${CRITICAL_FAILURE_RUNS:-6}"
FAIL_ON_CRITICAL="${FAIL_ON_CRITICAL:-0}"
TZ_OFFSET_HOURS="${TZ_OFFSET_HOURS:-0}"
WORKFLOW_MATCH="${WORKFLOW_MATCH:-}"
WORKFLOW_EXCLUDE="${WORKFLOW_EXCLUDE:-}"
REPO_MATCH="${REPO_MATCH:-}"
REPO_EXCLUDE="${REPO_EXCLUDE:-}"
BRANCH_MATCH="${BRANCH_MATCH:-}"
BRANCH_EXCLUDE="${BRANCH_EXCLUDE:-}"

if [[ "$OUTPUT_FORMAT" != "text" && "$OUTPUT_FORMAT" != "json" ]]; then
  echo "ERROR: OUTPUT_FORMAT must be 'text' or 'json' (got: $OUTPUT_FORMAT)" >&2
  exit 1
fi

if ! [[ "$TOP_N" =~ ^[0-9]+$ ]] || [[ "$TOP_N" -eq 0 ]]; then
  echo "ERROR: TOP_N must be a positive integer (got: $TOP_N)" >&2
  exit 1
fi

if ! [[ "$WARN_FAILURE_RUNS" =~ ^[0-9]+$ ]] || ! [[ "$CRITICAL_FAILURE_RUNS" =~ ^[0-9]+$ ]]; then
  echo "ERROR: WARN_FAILURE_RUNS and CRITICAL_FAILURE_RUNS must be positive integers" >&2
  exit 1
fi

if [[ "$WARN_FAILURE_RUNS" -eq 0 || "$CRITICAL_FAILURE_RUNS" -eq 0 ]]; then
  echo "ERROR: WARN_FAILURE_RUNS and CRITICAL_FAILURE_RUNS must be > 0" >&2
  exit 1
fi

if [[ "$CRITICAL_FAILURE_RUNS" -lt "$WARN_FAILURE_RUNS" ]]; then
  echo "ERROR: CRITICAL_FAILURE_RUNS must be >= WARN_FAILURE_RUNS" >&2
  exit 1
fi

if [[ "$FAIL_ON_CRITICAL" != "0" && "$FAIL_ON_CRITICAL" != "1" ]]; then
  echo "ERROR: FAIL_ON_CRITICAL must be 0 or 1 (got: $FAIL_ON_CRITICAL)" >&2
  exit 1
fi

if ! [[ "$TZ_OFFSET_HOURS" =~ ^-?[0-9]+$ ]]; then
  echo "ERROR: TZ_OFFSET_HOURS must be an integer between -23 and 23 (got: $TZ_OFFSET_HOURS)" >&2
  exit 1
fi

if (( TZ_OFFSET_HOURS < -23 || TZ_OFFSET_HOURS > 23 )); then
  echo "ERROR: TZ_OFFSET_HOURS must be between -23 and 23 (got: $TZ_OFFSET_HOURS)" >&2
  exit 1
fi

python3 - "$RUN_GLOB" "$TOP_N" "$OUTPUT_FORMAT" "$WARN_FAILURE_RUNS" "$CRITICAL_FAILURE_RUNS" "$FAIL_ON_CRITICAL" "$TZ_OFFSET_HOURS" "$WORKFLOW_MATCH" "$WORKFLOW_EXCLUDE" "$REPO_MATCH" "$REPO_EXCLUDE" "$BRANCH_MATCH" "$BRANCH_EXCLUDE" <<'PY'
import glob
import json
import re
import sys
from datetime import datetime, timedelta

run_glob = sys.argv[1]
top_n = int(sys.argv[2])
output_format = sys.argv[3]
warn_failure_runs = int(sys.argv[4])
critical_failure_runs = int(sys.argv[5])
fail_on_critical = sys.argv[6] == '1'
tz_offset_hours = int(sys.argv[7])
workflow_match_raw = sys.argv[8]
workflow_exclude_raw = sys.argv[9]
repo_match_raw = sys.argv[10]
repo_exclude_raw = sys.argv[11]
branch_match_raw = sys.argv[12]
branch_exclude_raw = sys.argv[13]

def compile_optional_regex(pattern, label):
    if not pattern:
        return None
    try:
        return re.compile(pattern)
    except re.error as exc:
        print(f"ERROR: invalid {label} regex {pattern!r}: {exc}", file=sys.stderr)
        sys.exit(1)


def parse_ts(value):
    if not value:
        return None
    ts = str(value)
    if ts.endswith('Z'):
        ts = ts[:-1] + '+00:00'
    try:
        return datetime.fromisoformat(ts)
    except ValueError:
        return None


def extract_repo_name(repository):
    if isinstance(repository, str) and repository.strip():
        return repository.strip()
    if isinstance(repository, dict):
        return (
            repository.get('nameWithOwner')
            or repository.get('full_name')
            or repository.get('fullName')
            or repository.get('name')
            or '<unknown-repo>'
        )
    return '<unknown-repo>'


def estimate_minutes(payload):
    started = parse_ts(payload.get('createdAt') or payload.get('runStartedAt') or payload.get('startedAt'))
    completed = parse_ts(payload.get('updatedAt') or payload.get('completedAt'))

    if started and completed:
        return max(0.0, (completed - started).total_seconds() / 60.0)

    total = 0.0
    for job in payload.get('jobs') or []:
        if not isinstance(job, dict):
            continue
        job_started = parse_ts(job.get('startedAt') or job.get('started_at') or job.get('createdAt'))
        job_completed = parse_ts(job.get('completedAt') or job.get('completed_at'))
        if job_started and job_completed:
            total += max(0.0, (job_completed - job_started).total_seconds() / 60.0)

    return total


workflow_match = compile_optional_regex(workflow_match_raw, 'WORKFLOW_MATCH')
workflow_exclude = compile_optional_regex(workflow_exclude_raw, 'WORKFLOW_EXCLUDE')
repo_match = compile_optional_regex(repo_match_raw, 'REPO_MATCH')
repo_exclude = compile_optional_regex(repo_exclude_raw, 'REPO_EXCLUDE')
branch_match = compile_optional_regex(branch_match_raw, 'BRANCH_MATCH')
branch_exclude = compile_optional_regex(branch_exclude_raw, 'BRANCH_EXCLUDE')

files = sorted(glob.glob(run_glob, recursive=True))
if not files:
    print(f"ERROR: no files matched RUN_GLOB={run_glob}", file=sys.stderr)
    sys.exit(1)

summary = {
    'files_scanned': len(files),
    'parse_errors': [],
    'runs_scanned': 0,
    'runs_filtered': 0,
    'failure_runs': 0,
    'failure_minutes_total': 0.0,
    'warn_windows': 0,
    'critical_windows': 0,
}

failure_conclusions = {'failure', 'cancelled', 'timed_out', 'action_required', 'startup_failure'}
windows = {}

for path in files:
    try:
        with open(path, 'r', encoding='utf-8') as fh:
            payload = json.load(fh)
    except Exception as exc:
        summary['parse_errors'].append(f"{path}: {exc}")
        continue

    summary['runs_scanned'] += 1

    conclusion = str(payload.get('conclusion') or '').lower()
    if conclusion not in failure_conclusions:
        summary['runs_filtered'] += 1
        continue

    repo = extract_repo_name(payload.get('repository'))
    workflow = payload.get('workflowName') or payload.get('name') or '<unknown-workflow>'
    branch = payload.get('headBranch') or '<unknown-branch>'

    if repo_match and not repo_match.search(repo):
        summary['runs_filtered'] += 1
        continue
    if repo_exclude and repo_exclude.search(repo):
        summary['runs_filtered'] += 1
        continue
    if workflow_match and not workflow_match.search(workflow):
        summary['runs_filtered'] += 1
        continue
    if workflow_exclude and workflow_exclude.search(workflow):
        summary['runs_filtered'] += 1
        continue
    if branch_match and not branch_match.search(branch):
        summary['runs_filtered'] += 1
        continue
    if branch_exclude and branch_exclude.search(branch):
        summary['runs_filtered'] += 1
        continue

    event_ts = parse_ts(
        payload.get('createdAt')
        or payload.get('runStartedAt')
        or payload.get('startedAt')
        or payload.get('updatedAt')
    )
    if not event_ts:
        summary['runs_filtered'] += 1
        continue

    local_ts = event_ts + timedelta(hours=tz_offset_hours)
    window_key = (local_ts.strftime('%a'), local_ts.hour)

    minutes = round(estimate_minutes(payload), 3)
    summary['failure_runs'] += 1
    summary['failure_minutes_total'] += minutes

    row = windows.setdefault(window_key, {
        'day': local_ts.strftime('%a'),
        'hour': local_ts.hour,
        'run_count': 0,
        'minutes': 0.0,
        'repos': set(),
        'workflows': set(),
        'branches': set(),
        'sample_runs': [],
    })

    row['run_count'] += 1
    row['minutes'] += minutes
    row['repos'].add(repo)
    row['workflows'].add(workflow)
    row['branches'].add(branch)

    run_id = str(payload.get('databaseId') or payload.get('id') or path)
    run_url = payload.get('url')
    if len(row['sample_runs']) < 3:
        row['sample_runs'].append({'run_id': run_id, 'url': run_url, 'repo': repo, 'workflow': workflow, 'branch': branch})

summary['failure_minutes_total'] = round(summary['failure_minutes_total'], 3)

rows = []
for key, row in windows.items():
    run_count = row['run_count']
    if run_count >= critical_failure_runs:
        severity = 'critical'
        summary['critical_windows'] += 1
    elif run_count >= warn_failure_runs:
        severity = 'warn'
        summary['warn_windows'] += 1
    else:
        severity = 'ok'

    rows.append({
        'day': row['day'],
        'hour': row['hour'],
        'window': f"{row['day']} {row['hour']:02d}:00",
        'severity': severity,
        'run_count': run_count,
        'minutes': round(row['minutes'], 3),
        'repo_count': len(row['repos']),
        'workflow_count': len(row['workflows']),
        'branch_count': len(row['branches']),
        'sample_runs': row['sample_runs'],
    })

severity_rank = {'critical': 2, 'warn': 1, 'ok': 0}
rows.sort(key=lambda r: (-severity_rank[r['severity']], -r['run_count'], -r['minutes'], r['day'], r['hour']))
critical_rows = [r for r in rows if r['severity'] == 'critical']

result = {
    'summary': {
        **summary,
        'windows': len(rows),
        'top_n': top_n,
        'warn_failure_runs': warn_failure_runs,
        'critical_failure_runs': critical_failure_runs,
        'tz_offset_hours': tz_offset_hours,
        'filters': {
            'repo_match': repo_match_raw or None,
            'repo_exclude': repo_exclude_raw or None,
            'workflow_match': workflow_match_raw or None,
            'workflow_exclude': workflow_exclude_raw or None,
            'branch_match': branch_match_raw or None,
            'branch_exclude': branch_exclude_raw or None,
        },
    },
    'windows': rows[:top_n],
    'all_windows': rows,
    'critical_windows': critical_rows,
}

if output_format == 'json':
    print(json.dumps(result, indent=2, sort_keys=True))
else:
    print('GITHUB ACTIONS FAILURE HOUR AUDIT')
    print('---')
    print(
        'SUMMARY: '
        f"files={summary['files_scanned']} runs={summary['runs_scanned']} runs_filtered={summary['runs_filtered']} "
        f"failure_runs={summary['failure_runs']} windows={len(rows)} warn_windows={summary['warn_windows']} "
        f"critical_windows={summary['critical_windows']} failure_minutes_total={summary['failure_minutes_total']}"
    )
    print(
        f"THRESHOLDS: warn_failure_runs={warn_failure_runs} critical_failure_runs={critical_failure_runs} tz_offset_hours={tz_offset_hours}"
    )

    if summary['parse_errors']:
        print('PARSE_ERRORS:')
        for err in summary['parse_errors']:
            print(f"- {err}")

    print('---')
    print(f"TOP FAILURE WINDOWS ({min(top_n, len(rows))})")
    if not rows:
        print('none')
    else:
        for row in rows[:top_n]:
            print(
                f"- [{row['severity']}] {row['window']} runs={row['run_count']} minutes={row['minutes']} "
                f"repos={row['repo_count']} workflows={row['workflow_count']} branches={row['branch_count']}"
            )

sys.exit(1 if (fail_on_critical and critical_rows) else 0)
PY
