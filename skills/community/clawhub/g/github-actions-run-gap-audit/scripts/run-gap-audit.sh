#!/usr/bin/env bash
set -euo pipefail

RUN_GLOB="${RUN_GLOB:-artifacts/github-actions/*.json}"
TOP_N="${TOP_N:-20}"
OUTPUT_FORMAT="${OUTPUT_FORMAT:-text}"
MIN_RUNS="${MIN_RUNS:-4}"
WARN_GAP_MULTIPLIER="${WARN_GAP_MULTIPLIER:-2.0}"
CRITICAL_GAP_MULTIPLIER="${CRITICAL_GAP_MULTIPLIER:-3.5}"
MIN_WARN_GAP_HOURS="${MIN_WARN_GAP_HOURS:-12}"
MIN_CRITICAL_GAP_HOURS="${MIN_CRITICAL_GAP_HOURS:-24}"
WORKFLOW_MATCH="${WORKFLOW_MATCH:-}"
WORKFLOW_EXCLUDE="${WORKFLOW_EXCLUDE:-}"
BRANCH_MATCH="${BRANCH_MATCH:-}"
BRANCH_EXCLUDE="${BRANCH_EXCLUDE:-}"
EVENT_MATCH="${EVENT_MATCH:-}"
EVENT_EXCLUDE="${EVENT_EXCLUDE:-}"
REPO_MATCH="${REPO_MATCH:-}"
REPO_EXCLUDE="${REPO_EXCLUDE:-}"
RUN_ID_MATCH="${RUN_ID_MATCH:-}"
RUN_ID_EXCLUDE="${RUN_ID_EXCLUDE:-}"
RUN_URL_MATCH="${RUN_URL_MATCH:-}"
RUN_URL_EXCLUDE="${RUN_URL_EXCLUDE:-}"
NOW_ISO="${NOW_ISO:-}"
FAIL_ON_CRITICAL="${FAIL_ON_CRITICAL:-0}"

if [[ "$OUTPUT_FORMAT" != "text" && "$OUTPUT_FORMAT" != "json" ]]; then
  echo "ERROR: OUTPUT_FORMAT must be 'text' or 'json' (got: $OUTPUT_FORMAT)" >&2
  exit 1
fi

if ! [[ "$TOP_N" =~ ^[0-9]+$ ]] || [[ "$TOP_N" -eq 0 ]]; then
  echo "ERROR: TOP_N must be a positive integer (got: $TOP_N)" >&2
  exit 1
fi

if ! [[ "$MIN_RUNS" =~ ^[0-9]+$ ]] || [[ "$MIN_RUNS" -lt 2 ]]; then
  echo "ERROR: MIN_RUNS must be an integer >= 2 (got: $MIN_RUNS)" >&2
  exit 1
fi

for value_name in WARN_GAP_MULTIPLIER CRITICAL_GAP_MULTIPLIER MIN_WARN_GAP_HOURS MIN_CRITICAL_GAP_HOURS; do
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

python3 - "$RUN_GLOB" "$TOP_N" "$OUTPUT_FORMAT" "$MIN_RUNS" "$WARN_GAP_MULTIPLIER" "$CRITICAL_GAP_MULTIPLIER" "$MIN_WARN_GAP_HOURS" "$MIN_CRITICAL_GAP_HOURS" "$WORKFLOW_MATCH" "$WORKFLOW_EXCLUDE" "$BRANCH_MATCH" "$BRANCH_EXCLUDE" "$EVENT_MATCH" "$EVENT_EXCLUDE" "$REPO_MATCH" "$REPO_EXCLUDE" "$RUN_ID_MATCH" "$RUN_ID_EXCLUDE" "$RUN_URL_MATCH" "$RUN_URL_EXCLUDE" "$NOW_ISO" "$FAIL_ON_CRITICAL" <<'PY'
import glob
import json
import re
import statistics
import sys
from collections import defaultdict
from datetime import datetime, timezone

(
    run_glob,
    top_n_raw,
    output_format,
    min_runs_raw,
    warn_gap_multiplier_raw,
    critical_gap_multiplier_raw,
    min_warn_gap_hours_raw,
    min_critical_gap_hours_raw,
    workflow_match_raw,
    workflow_exclude_raw,
    branch_match_raw,
    branch_exclude_raw,
    event_match_raw,
    event_exclude_raw,
    repo_match_raw,
    repo_exclude_raw,
    run_id_match_raw,
    run_id_exclude_raw,
    run_url_match_raw,
    run_url_exclude_raw,
    now_iso_raw,
    fail_on_critical_raw,
) = sys.argv[1:]

top_n = int(top_n_raw)
min_runs = int(min_runs_raw)
warn_gap_multiplier = float(warn_gap_multiplier_raw)
critical_gap_multiplier = float(critical_gap_multiplier_raw)
min_warn_gap_hours = float(min_warn_gap_hours_raw)
min_critical_gap_hours = float(min_critical_gap_hours_raw)
fail_on_critical = fail_on_critical_raw == '1'

if critical_gap_multiplier < warn_gap_multiplier:
    print('ERROR: CRITICAL_GAP_MULTIPLIER must be >= WARN_GAP_MULTIPLIER', file=sys.stderr)
    sys.exit(1)
if min_critical_gap_hours < min_warn_gap_hours:
    print('ERROR: MIN_CRITICAL_GAP_HOURS must be >= MIN_WARN_GAP_HOURS', file=sys.stderr)
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

workflow_match = compile_regex(workflow_match_raw, 'WORKFLOW_MATCH')
workflow_exclude = compile_regex(workflow_exclude_raw, 'WORKFLOW_EXCLUDE')
branch_match = compile_regex(branch_match_raw, 'BRANCH_MATCH')
branch_exclude = compile_regex(branch_exclude_raw, 'BRANCH_EXCLUDE')
event_match = compile_regex(event_match_raw, 'EVENT_MATCH')
event_exclude = compile_regex(event_exclude_raw, 'EVENT_EXCLUDE')
repo_match = compile_regex(repo_match_raw, 'REPO_MATCH')
repo_exclude = compile_regex(repo_exclude_raw, 'REPO_EXCLUDE')
run_id_match = compile_regex(run_id_match_raw, 'RUN_ID_MATCH')
run_id_exclude = compile_regex(run_id_exclude_raw, 'RUN_ID_EXCLUDE')
run_url_match = compile_regex(run_url_match_raw, 'RUN_URL_MATCH')
run_url_exclude = compile_regex(run_url_exclude_raw, 'RUN_URL_EXCLUDE')

now = parse_ts(now_iso_raw, 'NOW_ISO') if now_iso_raw else datetime.now(timezone.utc)

files = sorted(glob.glob(run_glob, recursive=True))
if not files:
    print(f'ERROR: no files matched RUN_GLOB={run_glob}', file=sys.stderr)
    sys.exit(1)

parse_errors = []
runs_scanned = 0
runs_filtered = 0

agg = defaultdict(lambda: {
    'repository': None,
    'workflow': None,
    'branch': None,
    'event': None,
    'timestamps': [],
    'sample_urls': [],
})

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

    run_id = str(payload.get('databaseId') or payload.get('id') or '')
    run_url = str(payload.get('url') or '')

    if run_id_match and not run_id_match.search(run_id):
        runs_filtered += 1
        continue
    if run_id_exclude and run_id_exclude.search(run_id):
        runs_filtered += 1
        continue
    if run_url_match and not run_url_match.search(run_url):
        runs_filtered += 1
        continue
    if run_url_exclude and run_url_exclude.search(run_url):
        runs_filtered += 1
        continue

    created_at = parse_ts(payload.get('createdAt') or payload.get('runStartedAt') or payload.get('startedAt'), 'createdAt')
    if created_at is None:
        parse_errors.append(f'{path}: missing createdAt/runStartedAt/startedAt')
        continue

    key = (repository, workflow, branch, event)
    bucket = agg[key]
    bucket['repository'] = repository
    bucket['workflow'] = workflow
    bucket['branch'] = branch
    bucket['event'] = event
    bucket['timestamps'].append(created_at)

    if run_url and run_url not in bucket['sample_urls'] and len(bucket['sample_urls']) < 3:
        bucket['sample_urls'].append(run_url)

groups = []
critical_groups = []

for bucket in agg.values():
    timestamps = sorted(bucket['timestamps'])
    if len(timestamps) < min_runs:
        continue

    intervals_hours = [
        (timestamps[idx] - timestamps[idx - 1]).total_seconds() / 3600.0
        for idx in range(1, len(timestamps))
        if (timestamps[idx] - timestamps[idx - 1]).total_seconds() > 0
    ]

    if not intervals_hours:
        continue

    median_interval = statistics.median(intervals_hours)
    quantiles = statistics.quantiles(intervals_hours, n=10, method='inclusive')
    p90_interval = quantiles[8] if quantiles else max(intervals_hours)

    latest_run_at = timestamps[-1]
    current_gap_hours = (now - latest_run_at).total_seconds() / 3600.0
    if current_gap_hours < 0:
        current_gap_hours = 0.0

    gap_ratio = current_gap_hours / median_interval if median_interval > 0 else 0.0

    severity = 'ok'
    if gap_ratio >= critical_gap_multiplier and current_gap_hours >= min_critical_gap_hours:
        severity = 'critical'
    elif gap_ratio >= warn_gap_multiplier and current_gap_hours >= min_warn_gap_hours:
        severity = 'warn'

    score = min(200.0, (gap_ratio * 20.0) + max(0.0, current_gap_hours - min_warn_gap_hours) * 0.35)

    row = {
        'repository': bucket['repository'],
        'workflow': bucket['workflow'],
        'branch': bucket['branch'],
        'event': bucket['event'],
        'runs': len(timestamps),
        'latest_run_at': latest_run_at.isoformat(),
        'oldest_run_at': timestamps[0].isoformat(),
        'median_interval_hours': round(median_interval, 3),
        'p90_interval_hours': round(p90_interval, 3),
        'current_gap_hours': round(current_gap_hours, 3),
        'gap_ratio': round(gap_ratio, 3),
        'severity': severity,
        'risk_score': round(score, 3),
        'sample_urls': bucket['sample_urls'],
    }
    groups.append(row)
    if severity == 'critical':
        critical_groups.append(row)

groups.sort(key=lambda row: (-row['risk_score'], -row['gap_ratio'], -row['current_gap_hours'], row['repository'], row['workflow'], row['branch'], row['event']))

summary = {
    'files_scanned': len(files),
    'parse_errors': parse_errors,
    'runs_scanned': runs_scanned,
    'runs_filtered': runs_filtered,
    'groups': len(groups),
    'critical_groups': len(critical_groups),
    'warn_gap_multiplier': warn_gap_multiplier,
    'critical_gap_multiplier': critical_gap_multiplier,
    'min_warn_gap_hours': min_warn_gap_hours,
    'min_critical_gap_hours': min_critical_gap_hours,
    'min_runs': min_runs,
    'top_n': top_n,
    'evaluated_at': now.isoformat(),
    'filters': {
        'workflow_match': workflow_match_raw or None,
        'workflow_exclude': workflow_exclude_raw or None,
        'branch_match': branch_match_raw or None,
        'branch_exclude': branch_exclude_raw or None,
        'event_match': event_match_raw or None,
        'event_exclude': event_exclude_raw or None,
        'repo_match': repo_match_raw or None,
        'repo_exclude': repo_exclude_raw or None,
        'run_id_match': run_id_match_raw or None,
        'run_id_exclude': run_id_exclude_raw or None,
        'run_url_match': run_url_match_raw or None,
        'run_url_exclude': run_url_exclude_raw or None,
    },
}

if output_format == 'json':
    print(json.dumps({'summary': summary, 'groups': groups[:top_n], 'all_groups': groups, 'critical_groups': critical_groups}, indent=2, sort_keys=True))
else:
    print('GITHUB ACTIONS RUN GAP AUDIT')
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
    print(f"TOP STALE WORKFLOW GROUPS ({min(top_n, len(groups))})")
    if not groups:
        print('none')
    else:
        for row in groups[:top_n]:
            print(
                f"- [{row['severity']}] {row['repository']} :: {row['workflow']} :: branch={row['branch']} event={row['event']} "
                f"runs={row['runs']} current_gap_hours={row['current_gap_hours']} median_interval_hours={row['median_interval_hours']} "
                f"gap_ratio={row['gap_ratio']} risk_score={row['risk_score']}"
            )

sys.exit(1 if (fail_on_critical and critical_groups) else 0)
PY
