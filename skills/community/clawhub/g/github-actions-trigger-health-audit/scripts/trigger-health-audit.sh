#!/usr/bin/env bash
set -euo pipefail

RUN_GLOB="${RUN_GLOB:-artifacts/github-actions/*.json}"
TOP_N="${TOP_N:-20}"
OUTPUT_FORMAT="${OUTPUT_FORMAT:-text}"
MIN_RUNS="${MIN_RUNS:-2}"
FAIL_WARN_PERCENT="${FAIL_WARN_PERCENT:-20}"
FAIL_CRITICAL_PERCENT="${FAIL_CRITICAL_PERCENT:-40}"
FAIL_ON_CRITICAL="${FAIL_ON_CRITICAL:-0}"
WORKFLOW_MATCH="${WORKFLOW_MATCH:-}"
WORKFLOW_EXCLUDE="${WORKFLOW_EXCLUDE:-}"
EVENT_MATCH="${EVENT_MATCH:-}"
EVENT_EXCLUDE="${EVENT_EXCLUDE:-}"
REPO_MATCH="${REPO_MATCH:-}"
REPO_EXCLUDE="${REPO_EXCLUDE:-}"

if [[ "$OUTPUT_FORMAT" != "text" && "$OUTPUT_FORMAT" != "json" ]]; then
  echo "ERROR: OUTPUT_FORMAT must be 'text' or 'json' (got: $OUTPUT_FORMAT)" >&2
  exit 1
fi

if ! [[ "$TOP_N" =~ ^[0-9]+$ ]] || [[ "$TOP_N" -eq 0 ]]; then
  echo "ERROR: TOP_N must be a positive integer (got: $TOP_N)" >&2
  exit 1
fi

if ! [[ "$MIN_RUNS" =~ ^[0-9]+$ ]] || [[ "$MIN_RUNS" -eq 0 ]]; then
  echo "ERROR: MIN_RUNS must be a positive integer (got: $MIN_RUNS)" >&2
  exit 1
fi

if ! [[ "$FAIL_WARN_PERCENT" =~ ^[0-9]+([.][0-9]+)?$ ]]; then
  echo "ERROR: FAIL_WARN_PERCENT must be numeric (got: $FAIL_WARN_PERCENT)" >&2
  exit 1
fi

if ! [[ "$FAIL_CRITICAL_PERCENT" =~ ^[0-9]+([.][0-9]+)?$ ]]; then
  echo "ERROR: FAIL_CRITICAL_PERCENT must be numeric (got: $FAIL_CRITICAL_PERCENT)" >&2
  exit 1
fi

if [[ "$FAIL_ON_CRITICAL" != "0" && "$FAIL_ON_CRITICAL" != "1" ]]; then
  echo "ERROR: FAIL_ON_CRITICAL must be 0 or 1 (got: $FAIL_ON_CRITICAL)" >&2
  exit 1
fi

python3 - "$RUN_GLOB" "$TOP_N" "$OUTPUT_FORMAT" "$MIN_RUNS" "$FAIL_WARN_PERCENT" "$FAIL_CRITICAL_PERCENT" "$FAIL_ON_CRITICAL" "$WORKFLOW_MATCH" "$WORKFLOW_EXCLUDE" "$EVENT_MATCH" "$EVENT_EXCLUDE" "$REPO_MATCH" "$REPO_EXCLUDE" <<'PY'
import glob
import json
import re
import sys
from collections import defaultdict
from datetime import datetime

run_glob = sys.argv[1]
top_n = int(sys.argv[2])
output_format = sys.argv[3]
min_runs = int(sys.argv[4])
warn_pct = float(sys.argv[5])
critical_pct = float(sys.argv[6])
fail_on_critical = sys.argv[7] == '1'
workflow_match_raw = sys.argv[8]
workflow_exclude_raw = sys.argv[9]
event_match_raw = sys.argv[10]
event_exclude_raw = sys.argv[11]
repo_match_raw = sys.argv[12]
repo_exclude_raw = sys.argv[13]

if critical_pct < warn_pct:
    print("ERROR: FAIL_CRITICAL_PERCENT must be >= FAIL_WARN_PERCENT", file=sys.stderr)
    sys.exit(1)


def compile_optional_regex(pattern, label):
    if not pattern:
        return None
    try:
        return re.compile(pattern)
    except re.error as exc:
        print(f"ERROR: invalid {label} regex {pattern!r}: {exc}", file=sys.stderr)
        sys.exit(1)


workflow_match = compile_optional_regex(workflow_match_raw, 'WORKFLOW_MATCH')
workflow_exclude = compile_optional_regex(workflow_exclude_raw, 'WORKFLOW_EXCLUDE')
event_match = compile_optional_regex(event_match_raw, 'EVENT_MATCH')
event_exclude = compile_optional_regex(event_exclude_raw, 'EVENT_EXCLUDE')
repo_match = compile_optional_regex(repo_match_raw, 'REPO_MATCH')
repo_exclude = compile_optional_regex(repo_exclude_raw, 'REPO_EXCLUDE')


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


files = sorted(glob.glob(run_glob, recursive=True))
if not files:
    print(f"ERROR: no files matched RUN_GLOB={run_glob}", file=sys.stderr)
    sys.exit(1)

parse_errors = []
runs_scanned = 0
runs_filtered = 0
runtime_missing = 0

agg = defaultdict(lambda: {
    'repository': None,
    'event': None,
    'workflow': None,
    'run_ids': set(),
    'branches': set(),
    'outcomes': defaultdict(int),
    'runtime_seconds': [],
    'sample_urls': [],
})

failure_outcomes = {'failure', 'cancelled', 'timed_out', 'startup_failure', 'stale', 'action_required'}

for path in files:
    try:
        with open(path, 'r', encoding='utf-8') as fh:
            payload = json.load(fh)
    except Exception as exc:
        parse_errors.append(f"{path}: {exc}")
        continue

    runs_scanned += 1

    workflow = payload.get('workflowName') or payload.get('name') or '<unknown-workflow>'
    event = payload.get('event') or '<unknown-event>'
    conclusion = (payload.get('conclusion') or payload.get('status') or 'unknown').lower()
    run_id = str(payload.get('databaseId') or payload.get('id') or path)
    branch = payload.get('headBranch') or '<unknown-branch>'

    raw_repository = payload.get('repository')
    repository = '<unknown-repo>'
    if isinstance(raw_repository, str) and raw_repository.strip():
        repository = raw_repository.strip()
    elif isinstance(raw_repository, dict):
        repository = (
            raw_repository.get('nameWithOwner')
            or raw_repository.get('full_name')
            or raw_repository.get('fullName')
            or raw_repository.get('name')
            or repository
        )

    if repo_match and not repo_match.search(repository):
        runs_filtered += 1
        continue
    if repo_exclude and repo_exclude.search(repository):
        runs_filtered += 1
        continue
    if workflow_match and not workflow_match.search(workflow):
        runs_filtered += 1
        continue
    if workflow_exclude and workflow_exclude.search(workflow):
        runs_filtered += 1
        continue
    if event_match and not event_match.search(event):
        runs_filtered += 1
        continue
    if event_exclude and event_exclude.search(event):
        runs_filtered += 1
        continue

    started = parse_ts(payload.get('runStartedAt') or payload.get('startedAt') or payload.get('createdAt'))
    ended = parse_ts(payload.get('updatedAt') or payload.get('completedAt'))
    runtime_seconds = None
    if started and ended:
        diff = (ended - started).total_seconds()
        if diff >= 0:
            runtime_seconds = diff
        else:
            runtime_missing += 1
    else:
        runtime_missing += 1

    key = (repository, event, workflow)
    bucket = agg[key]
    bucket['repository'] = repository
    bucket['event'] = event
    bucket['workflow'] = workflow
    bucket['run_ids'].add(run_id)
    bucket['branches'].add(branch)
    bucket['outcomes'][conclusion] += 1

    if runtime_seconds is not None:
        bucket['runtime_seconds'].append(runtime_seconds)

    run_url = payload.get('url')
    if run_url and len(bucket['sample_urls']) < 3 and run_url not in bucket['sample_urls']:
        bucket['sample_urls'].append(run_url)


groups = []
critical_groups = []
for item in agg.values():
    total_runs = sum(item['outcomes'].values())
    if total_runs < min_runs:
        continue

    failed_runs = sum(count for outcome, count in item['outcomes'].items() if outcome in failure_outcomes)
    success_runs = item['outcomes'].get('success', 0)
    skipped_runs = item['outcomes'].get('skipped', 0)
    neutral_runs = item['outcomes'].get('neutral', 0)

    failure_rate = (failed_runs / total_runs) * 100.0
    avg_runtime = (sum(item['runtime_seconds']) / len(item['runtime_seconds'])) if item['runtime_seconds'] else 0.0
    max_runtime = max(item['runtime_seconds']) if item['runtime_seconds'] else 0.0

    severity = 'ok'
    if failure_rate >= critical_pct:
        severity = 'critical'
    elif failure_rate >= warn_pct:
        severity = 'warn'

    row = {
        'repository': item['repository'],
        'event': item['event'],
        'workflow': item['workflow'],
        'total_runs': total_runs,
        'failed_runs': failed_runs,
        'success_runs': success_runs,
        'skipped_runs': skipped_runs,
        'neutral_runs': neutral_runs,
        'failure_rate_percent': round(failure_rate, 3),
        'avg_runtime_seconds': round(avg_runtime, 3),
        'max_runtime_seconds': round(max_runtime, 3),
        'branches': sorted(item['branches']),
        'run_count': len(item['run_ids']),
        'outcomes': dict(sorted(item['outcomes'].items())),
        'severity': severity,
        'sample_urls': item['sample_urls'],
    }
    groups.append(row)

    if severity == 'critical':
        critical_groups.append(row)

groups.sort(key=lambda row: (-row['failure_rate_percent'], -row['failed_runs'], -row['total_runs'], row['repository'], row['event'], row['workflow']))

summary = {
    'files_scanned': len(files),
    'parse_errors': parse_errors,
    'runs_scanned': runs_scanned,
    'runs_filtered': runs_filtered,
    'runtime_missing': runtime_missing,
    'groups': len(groups),
    'min_runs': min_runs,
    'warn_percent': warn_pct,
    'critical_percent': critical_pct,
    'critical_groups': len(critical_groups),
    'top_n': top_n,
    'filters': {
        'repo_match': repo_match_raw or None,
        'repo_exclude': repo_exclude_raw or None,
        'workflow_match': workflow_match_raw or None,
        'workflow_exclude': workflow_exclude_raw or None,
        'event_match': event_match_raw or None,
        'event_exclude': event_exclude_raw or None,
    },
}

if output_format == 'json':
    print(json.dumps({'summary': summary, 'groups': groups[:top_n], 'all_groups': groups, 'critical_groups': critical_groups}, indent=2, sort_keys=True))
else:
    print('GITHUB ACTIONS TRIGGER HEALTH AUDIT')
    print('---')
    print(
        'SUMMARY: '
        f"files={summary['files_scanned']} runs={summary['runs_scanned']} runs_filtered={summary['runs_filtered']} "
        f"groups={summary['groups']} runtime_missing={summary['runtime_missing']} critical_groups={summary['critical_groups']}"
    )

    if parse_errors:
        print('PARSE_ERRORS:')
        for err in parse_errors:
            print(f"- {err}")

    active_filters = [
        f"repo={repo_match_raw}" if repo_match_raw else None,
        f"repo!={repo_exclude_raw}" if repo_exclude_raw else None,
        f"workflow={workflow_match_raw}" if workflow_match_raw else None,
        f"workflow!={workflow_exclude_raw}" if workflow_exclude_raw else None,
        f"event={event_match_raw}" if event_match_raw else None,
        f"event!={event_exclude_raw}" if event_exclude_raw else None,
    ]
    active_filters = [f for f in active_filters if f]
    if active_filters:
        print('FILTERS: ' + ' '.join(active_filters))

    print('---')
    print(f"TOP TRIGGER HOTSPOTS ({min(top_n, len(groups))})")
    if not groups:
        print('none')
    else:
        for row in groups[:top_n]:
            print(
                f"- [{row['severity']}] {row['repository']} :: event={row['event']} :: {row['workflow']} "
                f"failure_rate={row['failure_rate_percent']}% failed={row['failed_runs']}/{row['total_runs']} "
                f"avg_runtime_s={row['avg_runtime_seconds']} max_runtime_s={row['max_runtime_seconds']}"
            )

sys.exit(1 if (fail_on_critical and critical_groups) else 0)
PY
