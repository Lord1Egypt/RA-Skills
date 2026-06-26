#!/usr/bin/env bash
set -euo pipefail

RUN_GLOB="${RUN_GLOB:-artifacts/github-actions/*.json}"
TOP_N="${TOP_N:-20}"
OUTPUT_FORMAT="${OUTPUT_FORMAT:-text}"
GROUP_BY="${GROUP_BY:-repo-workflow}"
NOW_ISO="${NOW_ISO:-}"
EVENTS="${EVENTS:-merge_group}"
WARN_FAILURE_RATE="${WARN_FAILURE_RATE:-0.2}"
CRITICAL_FAILURE_RATE="${CRITICAL_FAILURE_RATE:-0.4}"
WARN_P95_QUEUE_MINUTES="${WARN_P95_QUEUE_MINUTES:-8}"
CRITICAL_P95_QUEUE_MINUTES="${CRITICAL_P95_QUEUE_MINUTES:-20}"
WARN_STALE_SUCCESS_HOURS="${WARN_STALE_SUCCESS_HOURS:-18}"
CRITICAL_STALE_SUCCESS_HOURS="${CRITICAL_STALE_SUCCESS_HOURS:-48}"
MIN_RUNS="${MIN_RUNS:-3}"
WORKFLOW_MATCH="${WORKFLOW_MATCH:-}"
WORKFLOW_EXCLUDE="${WORKFLOW_EXCLUDE:-}"
BRANCH_MATCH="${BRANCH_MATCH:-}"
BRANCH_EXCLUDE="${BRANCH_EXCLUDE:-}"
REPO_MATCH="${REPO_MATCH:-}"
REPO_EXCLUDE="${REPO_EXCLUDE:-}"
EVENT_MATCH="${EVENT_MATCH:-}"
EVENT_EXCLUDE="${EVENT_EXCLUDE:-}"
FAIL_ON_CRITICAL="${FAIL_ON_CRITICAL:-0}"

if [[ "$OUTPUT_FORMAT" != "text" && "$OUTPUT_FORMAT" != "json" ]]; then
  echo "ERROR: OUTPUT_FORMAT must be 'text' or 'json' (got: $OUTPUT_FORMAT)" >&2
  exit 1
fi

if [[ "$GROUP_BY" != "repo-workflow" && "$GROUP_BY" != "repo-workflow-branch" ]]; then
  echo "ERROR: GROUP_BY must be repo-workflow or repo-workflow-branch (got: $GROUP_BY)" >&2
  exit 1
fi

for value_name in TOP_N WARN_P95_QUEUE_MINUTES CRITICAL_P95_QUEUE_MINUTES WARN_STALE_SUCCESS_HOURS CRITICAL_STALE_SUCCESS_HOURS MIN_RUNS; do
  value="${!value_name}"
  if ! [[ "$value" =~ ^[0-9]+$ ]]; then
    echo "ERROR: $value_name must be a non-negative integer (got: $value)" >&2
    exit 1
  fi
done

if [[ "$TOP_N" -eq 0 || "$MIN_RUNS" -eq 0 ]]; then
  echo "ERROR: TOP_N and MIN_RUNS must be >= 1" >&2
  exit 1
fi

for value_name in WARN_FAILURE_RATE CRITICAL_FAILURE_RATE; do
  value="${!value_name}"
  if ! [[ "$value" =~ ^0(\.[0-9]+)?$|^1(\.0+)?$ ]]; then
    echo "ERROR: $value_name must be between 0 and 1 (got: $value)" >&2
    exit 1
  fi
done

if [[ "$FAIL_ON_CRITICAL" != "0" && "$FAIL_ON_CRITICAL" != "1" ]]; then
  echo "ERROR: FAIL_ON_CRITICAL must be 0 or 1 (got: $FAIL_ON_CRITICAL)" >&2
  exit 1
fi

python3 - "$RUN_GLOB" "$TOP_N" "$OUTPUT_FORMAT" "$GROUP_BY" "$NOW_ISO" "$EVENTS" "$WARN_FAILURE_RATE" "$CRITICAL_FAILURE_RATE" "$WARN_P95_QUEUE_MINUTES" "$CRITICAL_P95_QUEUE_MINUTES" "$WARN_STALE_SUCCESS_HOURS" "$CRITICAL_STALE_SUCCESS_HOURS" "$MIN_RUNS" "$WORKFLOW_MATCH" "$WORKFLOW_EXCLUDE" "$BRANCH_MATCH" "$BRANCH_EXCLUDE" "$REPO_MATCH" "$REPO_EXCLUDE" "$EVENT_MATCH" "$EVENT_EXCLUDE" "$FAIL_ON_CRITICAL" <<'PY'
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
    group_by,
    now_iso_raw,
    events_raw,
    warn_failure_rate_raw,
    critical_failure_rate_raw,
    warn_p95_queue_minutes_raw,
    critical_p95_queue_minutes_raw,
    warn_stale_success_hours_raw,
    critical_stale_success_hours_raw,
    min_runs_raw,
    workflow_match_raw,
    workflow_exclude_raw,
    branch_match_raw,
    branch_exclude_raw,
    repo_match_raw,
    repo_exclude_raw,
    event_match_raw,
    event_exclude_raw,
    fail_on_critical_raw,
) = sys.argv[1:]

top_n = int(top_n_raw)
warn_failure_rate = float(warn_failure_rate_raw)
critical_failure_rate = float(critical_failure_rate_raw)
warn_p95_queue_minutes = int(warn_p95_queue_minutes_raw)
critical_p95_queue_minutes = int(critical_p95_queue_minutes_raw)
warn_stale_success_hours = int(warn_stale_success_hours_raw)
critical_stale_success_hours = int(critical_stale_success_hours_raw)
min_runs = int(min_runs_raw)
fail_on_critical = fail_on_critical_raw == '1'

if critical_failure_rate < warn_failure_rate:
    print('ERROR: CRITICAL_FAILURE_RATE must be >= WARN_FAILURE_RATE', file=sys.stderr)
    sys.exit(1)
if critical_p95_queue_minutes < warn_p95_queue_minutes:
    print('ERROR: CRITICAL_P95_QUEUE_MINUTES must be >= WARN_P95_QUEUE_MINUTES', file=sys.stderr)
    sys.exit(1)
if critical_stale_success_hours < warn_stale_success_hours:
    print('ERROR: CRITICAL_STALE_SUCCESS_HOURS must be >= WARN_STALE_SUCCESS_HOURS', file=sys.stderr)
    sys.exit(1)


def parse_ts(value, label):
    if value is None:
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
        return raw.get('nameWithOwner') or raw.get('full_name') or raw.get('name') or '<unknown-repo>'
    return '<unknown-repo>'


def percentile(values, q):
    if not values:
        return 0.0
    ordered = sorted(values)
    if len(ordered) == 1:
        return float(ordered[0])
    idx = q * (len(ordered) - 1)
    low = int(idx)
    high = min(low + 1, len(ordered) - 1)
    frac = idx - low
    return float(ordered[low] * (1 - frac) + ordered[high] * frac)


workflow_match = compile_regex(workflow_match_raw, 'WORKFLOW_MATCH')
workflow_exclude = compile_regex(workflow_exclude_raw, 'WORKFLOW_EXCLUDE')
branch_match = compile_regex(branch_match_raw, 'BRANCH_MATCH')
branch_exclude = compile_regex(branch_exclude_raw, 'BRANCH_EXCLUDE')
repo_match = compile_regex(repo_match_raw, 'REPO_MATCH')
repo_exclude = compile_regex(repo_exclude_raw, 'REPO_EXCLUDE')
event_match = compile_regex(event_match_raw, 'EVENT_MATCH')
event_exclude = compile_regex(event_exclude_raw, 'EVENT_EXCLUDE')

configured_events = {item.strip().lower() for item in events_raw.split(',') if item.strip()}
if not configured_events:
    print('ERROR: EVENTS must include at least one event', file=sys.stderr)
    sys.exit(1)

if now_iso_raw.strip():
    now = parse_ts(now_iso_raw, 'NOW_ISO')
else:
    now = datetime.now(timezone.utc)

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
        payload = json.load(open(path, 'r', encoding='utf-8'))
    except Exception as exc:
        parse_errors.append(f'{path}: {exc}')
        continue

    runs_scanned += 1
    workflow = payload.get('workflowName') or payload.get('name') or '<unknown-workflow>'
    branch = payload.get('headBranch') or '<unknown-branch>'
    event = str(payload.get('event') or '<unknown-event>').strip().lower()
    repo = normalize_repo(payload.get('repository'))

    if event not in configured_events:
        runs_filtered += 1
        continue
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
    if repo_match and not repo_match.search(repo):
        runs_filtered += 1
        continue
    if repo_exclude and repo_exclude.search(repo):
        runs_filtered += 1
        continue
    if event_match and not event_match.search(event):
        runs_filtered += 1
        continue
    if event_exclude and event_exclude.search(event):
        runs_filtered += 1
        continue

    run_id = payload.get('databaseId')
    if run_id is None:
        parse_errors.append(f'{path}: missing databaseId')
        continue

    created_at = parse_ts(payload.get('createdAt'), 'createdAt')
    started_at = parse_ts(payload.get('runStartedAt'), 'runStartedAt')
    updated_at = parse_ts(payload.get('updatedAt'), 'updatedAt')
    if created_at is None:
        parse_errors.append(f'{path}: missing createdAt')
        continue

    queue_minutes = 0.0
    if started_at is not None:
        queue_minutes = max(0.0, (started_at - created_at).total_seconds() / 60.0)

    conclusion = str(payload.get('conclusion') or '').strip().lower()
    is_failure = conclusion in {'failure', 'cancelled', 'timed_out', 'startup_failure'}
    is_success = conclusion == 'success'

    completed_at = updated_at or started_at or created_at

    if group_by == 'repo-workflow-branch':
        group_key = (repo, workflow, branch)
        group_label = f'{repo} / {workflow} / {branch}'
    else:
        group_key = (repo, workflow)
        group_label = f'{repo} / {workflow}'

    groups[group_key].append({
        'group': group_label,
        'repository': repo,
        'workflow': workflow,
        'branch': branch,
        'event': event,
        'run_id': run_id,
        'url': payload.get('url') or '',
        'queue_minutes': queue_minutes,
        'is_failure': is_failure,
        'is_success': is_success,
        'completed_at': completed_at,
        'conclusion': conclusion,
    })

rows = []
critical_rows = []
for _, items in groups.items():
    total_runs = len(items)
    if total_runs < min_runs:
        continue

    failures = [item for item in items if item['is_failure']]
    successes = [item for item in items if item['is_success']]

    failure_rate = len(failures) / total_runs if total_runs else 0.0
    p95_queue_minutes = percentile([item['queue_minutes'] for item in items], 0.95)

    last_success_completed_at = max((item['completed_at'] for item in successes), default=None)
    if last_success_completed_at is None:
        stale_success_hours = float('inf')
    else:
        stale_success_hours = max(0.0, (now - last_success_completed_at).total_seconds() / 3600.0)

    severity = 'ok'
    if (
        failure_rate >= critical_failure_rate
        or p95_queue_minutes >= critical_p95_queue_minutes
        or stale_success_hours >= critical_stale_success_hours
    ):
        severity = 'critical'
    elif (
        failure_rate >= warn_failure_rate
        or p95_queue_minutes >= warn_p95_queue_minutes
        or stale_success_hours >= warn_stale_success_hours
    ):
        severity = 'warn'

    risk_score = (
        (failure_rate * 100.0)
        + (p95_queue_minutes * 2.0)
        + (min(stale_success_hours, 240.0) * 0.8)
    )

    sample_failures = sorted(failures, key=lambda x: x['queue_minutes'], reverse=True)[:3]

    row = {
        'group': items[0]['group'],
        'repository': items[0]['repository'],
        'workflow': items[0]['workflow'],
        'branch': items[0]['branch'],
        'severity': severity,
        'total_runs': total_runs,
        'failure_runs': len(failures),
        'failure_rate': round(failure_rate, 4),
        'p95_queue_minutes': round(p95_queue_minutes, 2),
        'stale_success_hours': None if stale_success_hours == float('inf') else round(stale_success_hours, 2),
        'no_success_yet': stale_success_hours == float('inf'),
        'events': sorted({item['event'] for item in items}),
        'sample_failure_run_ids': [item['run_id'] for item in sample_failures],
        'sample_failure_urls': [item['url'] for item in sample_failures if item.get('url')],
        'risk_score': round(risk_score, 3),
    }
    rows.append(row)
    if severity == 'critical':
        critical_rows.append(row)

rows.sort(key=lambda row: (-row['risk_score'], -row['failure_rate'], -row['p95_queue_minutes'], row['group']))

summary = {
    'files_scanned': len(files),
    'runs_scanned': runs_scanned,
    'runs_filtered': runs_filtered,
    'parse_errors': parse_errors,
    'groups': len(rows),
    'critical_groups': len(critical_rows),
    'evaluated_at': now.isoformat(),
    'group_by': group_by,
    'events': sorted(configured_events),
    'warn_failure_rate': warn_failure_rate,
    'critical_failure_rate': critical_failure_rate,
    'warn_p95_queue_minutes': warn_p95_queue_minutes,
    'critical_p95_queue_minutes': critical_p95_queue_minutes,
    'warn_stale_success_hours': warn_stale_success_hours,
    'critical_stale_success_hours': critical_stale_success_hours,
    'min_runs': min_runs,
    'filters': {
        'workflow_match': workflow_match_raw or None,
        'workflow_exclude': workflow_exclude_raw or None,
        'branch_match': branch_match_raw or None,
        'branch_exclude': branch_exclude_raw or None,
        'repo_match': repo_match_raw or None,
        'repo_exclude': repo_exclude_raw or None,
        'event_match': event_match_raw or None,
        'event_exclude': event_exclude_raw or None,
    },
}

if output_format == 'json':
    print(json.dumps({'summary': summary, 'groups': rows[:top_n], 'all_groups': rows, 'critical_groups': critical_rows}, indent=2, sort_keys=True))
else:
    print('GITHUB ACTIONS MERGE QUEUE HEALTH AUDIT')
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
    print(f"TOP MERGE-QUEUE RISK GROUPS ({min(top_n, len(rows))})")
    if not rows:
        print('none')
    else:
        for row in rows[:top_n]:
            stale_display = 'none' if row['no_success_yet'] else f"{row['stale_success_hours']:.2f}"
            print(
                f"- [{row['severity']}] group={row['group']} "
                f"failures={row['failure_runs']}/{row['total_runs']} failure_rate={row['failure_rate']:.3f} "
                f"p95_queue_minutes={row['p95_queue_minutes']:.2f} stale_success_hours={stale_display} "
                f"risk_score={row['risk_score']}"
            )

sys.exit(1 if (fail_on_critical and critical_rows) else 0)
PY
