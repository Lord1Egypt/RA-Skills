#!/usr/bin/env bash
set -euo pipefail

RUN_GLOB="${RUN_GLOB:-artifacts/github-actions/*.json}"
TOP_N="${TOP_N:-20}"
OUTPUT_FORMAT="${OUTPUT_FORMAT:-text}"
DUPLICATE_WINDOW_MINUTES="${DUPLICATE_WINDOW_MINUTES:-30}"
MIN_DUPLICATE_RUNS="${MIN_DUPLICATE_RUNS:-2}"
WARN_DUPLICATE_RUNS="${WARN_DUPLICATE_RUNS:-3}"
CRITICAL_DUPLICATE_RUNS="${CRITICAL_DUPLICATE_RUNS:-6}"
WARN_WASTED_MINUTES="${WARN_WASTED_MINUTES:-20}"
CRITICAL_WASTED_MINUTES="${CRITICAL_WASTED_MINUTES:-60}"
WORKFLOW_MATCH="${WORKFLOW_MATCH:-}"
WORKFLOW_EXCLUDE="${WORKFLOW_EXCLUDE:-}"
BRANCH_MATCH="${BRANCH_MATCH:-}"
BRANCH_EXCLUDE="${BRANCH_EXCLUDE:-}"
EVENT_MATCH="${EVENT_MATCH:-}"
EVENT_EXCLUDE="${EVENT_EXCLUDE:-}"
REPO_MATCH="${REPO_MATCH:-}"
REPO_EXCLUDE="${REPO_EXCLUDE:-}"
HEAD_SHA_MATCH="${HEAD_SHA_MATCH:-}"
HEAD_SHA_EXCLUDE="${HEAD_SHA_EXCLUDE:-}"
FAIL_ON_CRITICAL="${FAIL_ON_CRITICAL:-0}"

if [[ "$OUTPUT_FORMAT" != "text" && "$OUTPUT_FORMAT" != "json" ]]; then
  echo "ERROR: OUTPUT_FORMAT must be 'text' or 'json' (got: $OUTPUT_FORMAT)" >&2
  exit 1
fi

for value_name in TOP_N DUPLICATE_WINDOW_MINUTES MIN_DUPLICATE_RUNS WARN_DUPLICATE_RUNS CRITICAL_DUPLICATE_RUNS; do
  value="${!value_name}"
  if ! [[ "$value" =~ ^[0-9]+$ ]] || [[ "$value" -eq 0 ]]; then
    echo "ERROR: $value_name must be a positive integer (got: $value)" >&2
    exit 1
  fi
done

for value_name in WARN_WASTED_MINUTES CRITICAL_WASTED_MINUTES; do
  value="${!value_name}"
  if ! [[ "$value" =~ ^[0-9]+([.][0-9]+)?$ ]]; then
    echo "ERROR: $value_name must be numeric (got: $value)" >&2
    exit 1
  fi
done

if [[ "$FAIL_ON_CRITICAL" != "0" && "$FAIL_ON_CRITICAL" != "1" ]]; then
  echo "ERROR: FAIL_ON_CRITICAL must be 0 or 1 (got: $FAIL_ON_CRITICAL)" >&2
  exit 1
fi

python3 - "$RUN_GLOB" "$TOP_N" "$OUTPUT_FORMAT" "$DUPLICATE_WINDOW_MINUTES" "$MIN_DUPLICATE_RUNS" "$WARN_DUPLICATE_RUNS" "$CRITICAL_DUPLICATE_RUNS" "$WARN_WASTED_MINUTES" "$CRITICAL_WASTED_MINUTES" "$WORKFLOW_MATCH" "$WORKFLOW_EXCLUDE" "$BRANCH_MATCH" "$BRANCH_EXCLUDE" "$EVENT_MATCH" "$EVENT_EXCLUDE" "$REPO_MATCH" "$REPO_EXCLUDE" "$HEAD_SHA_MATCH" "$HEAD_SHA_EXCLUDE" "$FAIL_ON_CRITICAL" <<'PY'
import glob
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone

(
    run_glob,
    top_n_raw,
    output_format,
    duplicate_window_minutes_raw,
    min_duplicate_runs_raw,
    warn_duplicate_runs_raw,
    critical_duplicate_runs_raw,
    warn_wasted_minutes_raw,
    critical_wasted_minutes_raw,
    workflow_match_raw,
    workflow_exclude_raw,
    branch_match_raw,
    branch_exclude_raw,
    event_match_raw,
    event_exclude_raw,
    repo_match_raw,
    repo_exclude_raw,
    head_sha_match_raw,
    head_sha_exclude_raw,
    fail_on_critical_raw,
) = sys.argv[1:]

top_n = int(top_n_raw)
duplicate_window_minutes = int(duplicate_window_minutes_raw)
min_duplicate_runs = int(min_duplicate_runs_raw)
warn_duplicate_runs = int(warn_duplicate_runs_raw)
critical_duplicate_runs = int(critical_duplicate_runs_raw)
warn_wasted_minutes = float(warn_wasted_minutes_raw)
critical_wasted_minutes = float(critical_wasted_minutes_raw)
fail_on_critical = fail_on_critical_raw == '1'
window_seconds = duplicate_window_minutes * 60

if critical_duplicate_runs < warn_duplicate_runs:
    print('ERROR: CRITICAL_DUPLICATE_RUNS must be >= WARN_DUPLICATE_RUNS', file=sys.stderr)
    sys.exit(1)
if critical_wasted_minutes < warn_wasted_minutes:
    print('ERROR: CRITICAL_WASTED_MINUTES must be >= WARN_WASTED_MINUTES', file=sys.stderr)
    sys.exit(1)
if min_duplicate_runs < 2:
    print('ERROR: MIN_DUPLICATE_RUNS must be >= 2', file=sys.stderr)
    sys.exit(1)


def parse_ts(value, label='timestamp'):
    if not value:
        return None
    raw = str(value).strip()
    if not raw:
        return None
    if raw.endswith('Z'):
        raw = raw[:-1] + '+00:00'
    try:
        dt = datetime.fromisoformat(raw)
    except ValueError:
        print(f'ERROR: invalid {label}: {value!r}', file=sys.stderr)
        sys.exit(1)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def compile_regex(pattern, label):
    if not pattern:
        return None
    try:
        return re.compile(pattern)
    except re.error as exc:
        print(f'ERROR: invalid {label} regex {pattern!r}: {exc}', file=sys.stderr)
        sys.exit(1)


def normalize_repo(raw):
    if isinstance(raw, str) and raw.strip():
        return raw.strip()
    if isinstance(raw, dict):
        return (
            raw.get('nameWithOwner')
            or raw.get('full_name')
            or raw.get('fullName')
            or raw.get('name')
            or '<unknown-repo>'
        )
    return '<unknown-repo>'


def run_duration_minutes(row):
    started = parse_ts(row.get('startedAt') or row.get('runStartedAt'), 'startedAt')
    ended = parse_ts(row.get('updatedAt') or row.get('completedAt') or row.get('createdAt'), 'updatedAt')
    if not started or not ended:
        return 0.0
    delta = (ended - started).total_seconds() / 60.0
    return max(0.0, delta)


workflow_match = compile_regex(workflow_match_raw, 'WORKFLOW_MATCH')
workflow_exclude = compile_regex(workflow_exclude_raw, 'WORKFLOW_EXCLUDE')
branch_match = compile_regex(branch_match_raw, 'BRANCH_MATCH')
branch_exclude = compile_regex(branch_exclude_raw, 'BRANCH_EXCLUDE')
event_match = compile_regex(event_match_raw, 'EVENT_MATCH')
event_exclude = compile_regex(event_exclude_raw, 'EVENT_EXCLUDE')
repo_match = compile_regex(repo_match_raw, 'REPO_MATCH')
repo_exclude = compile_regex(repo_exclude_raw, 'REPO_EXCLUDE')
head_sha_match = compile_regex(head_sha_match_raw, 'HEAD_SHA_MATCH')
head_sha_exclude = compile_regex(head_sha_exclude_raw, 'HEAD_SHA_EXCLUDE')

files = sorted(glob.glob(run_glob, recursive=True))
if not files:
    print(f'ERROR: no files matched RUN_GLOB={run_glob}', file=sys.stderr)
    sys.exit(1)

parse_errors = []
runs_scanned = 0
runs_filtered = 0

groups = defaultdict(list)

for path in files:
    try:
        with open(path, 'r', encoding='utf-8') as fh:
            payload = json.load(fh)
    except Exception as exc:
        parse_errors.append(f'{path}: {exc}')
        continue

    runs_scanned += 1

    workflow = payload.get('workflowName') or payload.get('name') or '<unknown-workflow>'
    branch = payload.get('headBranch') or '<unknown-branch>'
    event = payload.get('event') or '<unknown-event>'
    repository = normalize_repo(payload.get('repository'))
    head_sha = payload.get('headSha') or '<unknown-sha>'

    if workflow_match and not workflow_match.search(workflow):
        runs_filtered += 1
        continue
    if workflow_exclude and workflow_exclude.search(workflow):
        runs_filtered += 1
        continue
    if branch_match and not branch_match.search(branch):
        runs_filtered += 1
        continue
    if branch_exclude and branch_exclude.search(branch):
        runs_filtered += 1
        continue
    if event_match and not event_match.search(event):
        runs_filtered += 1
        continue
    if event_exclude and event_exclude.search(event):
        runs_filtered += 1
        continue
    if repo_match and not repo_match.search(repository):
        runs_filtered += 1
        continue
    if repo_exclude and repo_exclude.search(repository):
        runs_filtered += 1
        continue
    if head_sha_match and not head_sha_match.search(head_sha):
        runs_filtered += 1
        continue
    if head_sha_exclude and head_sha_exclude.search(head_sha):
        runs_filtered += 1
        continue

    created_at = parse_ts(payload.get('createdAt') or payload.get('runStartedAt') or payload.get('startedAt'), 'createdAt')
    if created_at is None:
        parse_errors.append(f'{path}: missing createdAt/runStartedAt/startedAt')
        continue

    groups[(repository, workflow, branch, event, head_sha)].append(
        {
            'database_id': payload.get('databaseId'),
            'created_at': created_at,
            'duration_minutes': run_duration_minutes(payload),
            'conclusion': (payload.get('conclusion') or '').strip().lower(),
            'url': payload.get('url') or '',
        }
    )

rows = []
critical_rows = []

for (repository, workflow, branch, event, head_sha), runs in groups.items():
    if len(runs) < min_duplicate_runs:
        continue

    sorted_runs = sorted(runs, key=lambda row: row['created_at'])
    bursts = []
    current = [sorted_runs[0]]

    for run in sorted_runs[1:]:
        gap_seconds = (run['created_at'] - current[-1]['created_at']).total_seconds()
        if gap_seconds <= window_seconds:
            current.append(run)
        else:
            bursts.append(current)
            current = [run]
    bursts.append(current)

    duplicate_runs_total = 0
    wasted_minutes_total = 0.0
    burst_summaries = []

    for burst in bursts:
        if len(burst) < min_duplicate_runs:
            continue

        burst_sorted = sorted(burst, key=lambda row: row['created_at'])
        canonical = burst_sorted[-1]
        duplicate_runs = len(burst_sorted) - 1
        wasted_minutes = sum(item['duration_minutes'] for item in burst_sorted[:-1])

        duplicate_runs_total += duplicate_runs
        wasted_minutes_total += wasted_minutes

        burst_summaries.append(
            {
                'burst_size': len(burst_sorted),
                'duplicate_runs': duplicate_runs,
                'wasted_minutes': round(wasted_minutes, 3),
                'start_at': burst_sorted[0]['created_at'].isoformat(),
                'end_at': burst_sorted[-1]['created_at'].isoformat(),
                'canonical_run_id': canonical['database_id'],
                'sample_run_urls': [item['url'] for item in burst_sorted if item['url']][:3],
            }
        )

    if duplicate_runs_total == 0:
        continue

    severity = 'ok'
    if duplicate_runs_total >= critical_duplicate_runs or wasted_minutes_total >= critical_wasted_minutes:
        severity = 'critical'
    elif duplicate_runs_total >= warn_duplicate_runs or wasted_minutes_total >= warn_wasted_minutes:
        severity = 'warn'

    risk_score = (duplicate_runs_total * 8.0) + (wasted_minutes_total * 1.2) + (len(burst_summaries) * 4.0)
    latest_run = sorted_runs[-1]

    row = {
        'repository': repository,
        'workflow': workflow,
        'branch': branch,
        'event': event,
        'head_sha': head_sha,
        'severity': severity,
        'runs_total': len(sorted_runs),
        'duplicate_runs': duplicate_runs_total,
        'burst_count': len(burst_summaries),
        'wasted_minutes': round(wasted_minutes_total, 3),
        'risk_score': round(risk_score, 3),
        'latest_run_at': latest_run['created_at'].isoformat(),
        'latest_conclusion': latest_run['conclusion'],
        'sample_latest_url': latest_run['url'],
        'bursts': burst_summaries,
    }

    rows.append(row)
    if severity == 'critical':
        critical_rows.append(row)

rows.sort(
    key=lambda row: (
        -row['risk_score'],
        -row['duplicate_runs'],
        -row['wasted_minutes'],
        row['repository'],
        row['workflow'],
        row['branch'],
        row['event'],
        row['head_sha'],
    )
)

summary = {
    'files_scanned': len(files),
    'runs_scanned': runs_scanned,
    'runs_filtered': runs_filtered,
    'parse_errors': parse_errors,
    'groups': len(rows),
    'critical_groups': len(critical_rows),
    'top_n': top_n,
    'duplicate_window_minutes': duplicate_window_minutes,
    'min_duplicate_runs': min_duplicate_runs,
    'warn_duplicate_runs': warn_duplicate_runs,
    'critical_duplicate_runs': critical_duplicate_runs,
    'warn_wasted_minutes': warn_wasted_minutes,
    'critical_wasted_minutes': critical_wasted_minutes,
    'evaluated_at': datetime.now(timezone.utc).isoformat(),
    'filters': {
        'workflow_match': workflow_match_raw or None,
        'workflow_exclude': workflow_exclude_raw or None,
        'branch_match': branch_match_raw or None,
        'branch_exclude': branch_exclude_raw or None,
        'event_match': event_match_raw or None,
        'event_exclude': event_exclude_raw or None,
        'repo_match': repo_match_raw or None,
        'repo_exclude': repo_exclude_raw or None,
        'head_sha_match': head_sha_match_raw or None,
        'head_sha_exclude': head_sha_exclude_raw or None,
    },
}

if output_format == 'json':
    print(json.dumps({'summary': summary, 'groups': rows[:top_n], 'all_groups': rows, 'critical_groups': critical_rows}, indent=2, sort_keys=True))
else:
    print('GITHUB ACTIONS DUPLICATE RUN AUDIT')
    print('---')
    print(
        'SUMMARY: '
        f"files={summary['files_scanned']} runs={summary['runs_scanned']} runs_filtered={summary['runs_filtered']} "
        f"groups={summary['groups']} critical_groups={summary['critical_groups']} evaluated_at={summary['evaluated_at']}"
    )

    if parse_errors:
        print('PARSE_ERRORS:')
        for err in parse_errors:
            print(f'- {err}')

    print('---')
    print(f"TOP DUPLICATE RUN GROUPS ({min(top_n, len(rows))})")
    if not rows:
        print('none')
    else:
        for row in rows[:top_n]:
            print(
                f"- [{row['severity']}] {row['repository']} :: {row['workflow']} :: branch={row['branch']} event={row['event']} sha={row['head_sha']} "
                f"duplicates={row['duplicate_runs']} bursts={row['burst_count']} wasted_minutes={row['wasted_minutes']} risk_score={row['risk_score']}"
            )

sys.exit(1 if (fail_on_critical and critical_rows) else 0)
PY
