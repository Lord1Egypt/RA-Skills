#!/usr/bin/env bash
set -euo pipefail

RUN_GLOB="${RUN_GLOB:-artifacts/github-actions/*.json}"
TOP_N="${TOP_N:-20}"
OUTPUT_FORMAT="${OUTPUT_FORMAT:-text}"
GROUP_BY="${GROUP_BY:-workflow}"
MANUAL_EVENTS="${MANUAL_EVENTS:-workflow_dispatch,repository_dispatch}"
RECENT_WINDOW="${RECENT_WINDOW:-5}"
MIN_RUNS="${MIN_RUNS:-5}"
WARN_MANUAL_RATIO="${WARN_MANUAL_RATIO:-0.35}"
CRITICAL_MANUAL_RATIO="${CRITICAL_MANUAL_RATIO:-0.65}"
WARN_MANUAL_RUNS="${WARN_MANUAL_RUNS:-5}"
CRITICAL_MANUAL_RUNS="${CRITICAL_MANUAL_RUNS:-12}"
WARN_RECENT_MANUAL_STREAK="${WARN_RECENT_MANUAL_STREAK:-3}"
CRITICAL_RECENT_MANUAL_STREAK="${CRITICAL_RECENT_MANUAL_STREAK:-5}"
WORKFLOW_MATCH="${WORKFLOW_MATCH:-}"
WORKFLOW_EXCLUDE="${WORKFLOW_EXCLUDE:-}"
BRANCH_MATCH="${BRANCH_MATCH:-}"
BRANCH_EXCLUDE="${BRANCH_EXCLUDE:-}"
EVENT_MATCH="${EVENT_MATCH:-}"
EVENT_EXCLUDE="${EVENT_EXCLUDE:-}"
REPO_MATCH="${REPO_MATCH:-}"
REPO_EXCLUDE="${REPO_EXCLUDE:-}"
FAIL_ON_CRITICAL="${FAIL_ON_CRITICAL:-0}"

if [[ "$OUTPUT_FORMAT" != "text" && "$OUTPUT_FORMAT" != "json" ]]; then
  echo "ERROR: OUTPUT_FORMAT must be 'text' or 'json' (got: $OUTPUT_FORMAT)" >&2
  exit 1
fi

if [[ "$GROUP_BY" != "workflow" && "$GROUP_BY" != "workflow-branch" ]]; then
  echo "ERROR: GROUP_BY must be 'workflow' or 'workflow-branch' (got: $GROUP_BY)" >&2
  exit 1
fi

for value_name in TOP_N RECENT_WINDOW MIN_RUNS WARN_MANUAL_RUNS CRITICAL_MANUAL_RUNS WARN_RECENT_MANUAL_STREAK CRITICAL_RECENT_MANUAL_STREAK; do
  value="${!value_name}"
  if ! [[ "$value" =~ ^[0-9]+$ ]] || [[ "$value" -eq 0 ]]; then
    echo "ERROR: $value_name must be a positive integer (got: $value)" >&2
    exit 1
  fi
done

for value_name in WARN_MANUAL_RATIO CRITICAL_MANUAL_RATIO; do
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

python3 - "$RUN_GLOB" "$TOP_N" "$OUTPUT_FORMAT" "$GROUP_BY" "$MANUAL_EVENTS" "$RECENT_WINDOW" "$MIN_RUNS" "$WARN_MANUAL_RATIO" "$CRITICAL_MANUAL_RATIO" "$WARN_MANUAL_RUNS" "$CRITICAL_MANUAL_RUNS" "$WARN_RECENT_MANUAL_STREAK" "$CRITICAL_RECENT_MANUAL_STREAK" "$WORKFLOW_MATCH" "$WORKFLOW_EXCLUDE" "$BRANCH_MATCH" "$BRANCH_EXCLUDE" "$EVENT_MATCH" "$EVENT_EXCLUDE" "$REPO_MATCH" "$REPO_EXCLUDE" "$FAIL_ON_CRITICAL" <<'PY'
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
    manual_events_raw,
    recent_window_raw,
    min_runs_raw,
    warn_ratio_raw,
    critical_ratio_raw,
    warn_manual_runs_raw,
    critical_manual_runs_raw,
    warn_recent_streak_raw,
    critical_recent_streak_raw,
    workflow_match_raw,
    workflow_exclude_raw,
    branch_match_raw,
    branch_exclude_raw,
    event_match_raw,
    event_exclude_raw,
    repo_match_raw,
    repo_exclude_raw,
    fail_on_critical_raw,
) = sys.argv[1:]

top_n = int(top_n_raw)
recent_window = int(recent_window_raw)
min_runs = int(min_runs_raw)
warn_ratio = float(warn_ratio_raw)
critical_ratio = float(critical_ratio_raw)
warn_manual_runs = int(warn_manual_runs_raw)
critical_manual_runs = int(critical_manual_runs_raw)
warn_recent_streak = int(warn_recent_streak_raw)
critical_recent_streak = int(critical_recent_streak_raw)
fail_on_critical = fail_on_critical_raw == '1'
manual_events = {item.strip().lower() for item in manual_events_raw.split(',') if item.strip()}

if not manual_events:
    print('ERROR: MANUAL_EVENTS must include at least one event name', file=sys.stderr)
    sys.exit(1)
if critical_ratio < warn_ratio:
    print('ERROR: CRITICAL_MANUAL_RATIO must be >= WARN_MANUAL_RATIO', file=sys.stderr)
    sys.exit(1)
if critical_manual_runs < warn_manual_runs:
    print('ERROR: CRITICAL_MANUAL_RUNS must be >= WARN_MANUAL_RUNS', file=sys.stderr)
    sys.exit(1)
if critical_recent_streak < warn_recent_streak:
    print('ERROR: CRITICAL_RECENT_MANUAL_STREAK must be >= WARN_RECENT_MANUAL_STREAK', file=sys.stderr)
    sys.exit(1)
if recent_window < warn_recent_streak:
    print('ERROR: RECENT_WINDOW must be >= WARN_RECENT_MANUAL_STREAK', file=sys.stderr)
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


def recent_manual_streak(sorted_runs):
    streak = 0
    for run in reversed(sorted_runs[-recent_window:]):
        if run['is_manual']:
            streak += 1
        else:
            break
    return streak


workflow_match = compile_regex(workflow_match_raw, 'WORKFLOW_MATCH')
workflow_exclude = compile_regex(workflow_exclude_raw, 'WORKFLOW_EXCLUDE')
branch_match = compile_regex(branch_match_raw, 'BRANCH_MATCH')
branch_exclude = compile_regex(branch_exclude_raw, 'BRANCH_EXCLUDE')
event_match = compile_regex(event_match_raw, 'EVENT_MATCH')
event_exclude = compile_regex(event_exclude_raw, 'EVENT_EXCLUDE')
repo_match = compile_regex(repo_match_raw, 'REPO_MATCH')
repo_exclude = compile_regex(repo_exclude_raw, 'REPO_EXCLUDE')

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
    event = (payload.get('event') or '<unknown-event>').strip().lower()
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

    created_at = parse_ts(payload.get('createdAt') or payload.get('runStartedAt') or payload.get('startedAt'), 'createdAt')
    if created_at is None:
        parse_errors.append(f'{path}: missing createdAt/runStartedAt/startedAt')
        continue

    key = (repository, workflow) if group_by == 'workflow' else (repository, workflow, branch)
    groups[key].append(
        {
            'database_id': payload.get('databaseId'),
            'created_at': created_at,
            'event': event,
            'is_manual': event in manual_events,
            'conclusion': (payload.get('conclusion') or '').strip().lower(),
            'url': payload.get('url') or '',
            'branch': branch,
        }
    )

rows = []
critical_rows = []

for key, runs in groups.items():
    if len(runs) < min_runs:
        continue

    sorted_runs = sorted(runs, key=lambda row: row['created_at'])
    manual_runs = [row for row in sorted_runs if row['is_manual']]
    manual_count = len(manual_runs)
    manual_ratio = manual_count / len(sorted_runs)
    streak = recent_manual_streak(sorted_runs)
    latest = sorted_runs[-1]

    severity = 'ok'
    if manual_ratio >= critical_ratio or manual_count >= critical_manual_runs or streak >= critical_recent_streak:
        severity = 'critical'
    elif manual_ratio >= warn_ratio or manual_count >= warn_manual_runs or streak >= warn_recent_streak:
        severity = 'warn'

    risk_score = (manual_ratio * 100.0) + (manual_count * 2.0) + (streak * 8.0)

    row = {
        'repository': key[0],
        'workflow': key[1],
        'branch': (key[2] if len(key) > 2 else None),
        'severity': severity,
        'total_runs': len(sorted_runs),
        'manual_runs': manual_count,
        'manual_ratio': round(manual_ratio, 4),
        'recent_manual_streak': streak,
        'latest_run_at': latest['created_at'].isoformat(),
        'latest_event': latest['event'],
        'latest_conclusion': latest['conclusion'],
        'sample_manual_run_ids': [item['database_id'] for item in manual_runs[-3:] if item.get('database_id') is not None],
        'sample_manual_urls': [item['url'] for item in manual_runs[-3:] if item.get('url')],
        'risk_score': round(risk_score, 3),
    }

    rows.append(row)
    if severity == 'critical':
        critical_rows.append(row)

rows.sort(
    key=lambda row: (
        -row['risk_score'],
        -row['manual_ratio'],
        -row['manual_runs'],
        row['repository'],
        row['workflow'],
        row['branch'] or '',
    )
)

summary = {
    'files_scanned': len(files),
    'runs_scanned': runs_scanned,
    'runs_filtered': runs_filtered,
    'parse_errors': parse_errors,
    'groups': len(rows),
    'critical_groups': len(critical_rows),
    'manual_events': sorted(manual_events),
    'group_by': group_by,
    'recent_window': recent_window,
    'min_runs': min_runs,
    'warn_manual_ratio': warn_ratio,
    'critical_manual_ratio': critical_ratio,
    'warn_manual_runs': warn_manual_runs,
    'critical_manual_runs': critical_manual_runs,
    'warn_recent_manual_streak': warn_recent_streak,
    'critical_recent_manual_streak': critical_recent_streak,
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
    },
}

if output_format == 'json':
    print(json.dumps({'summary': summary, 'groups': rows[:top_n], 'all_groups': rows, 'critical_groups': critical_rows}, indent=2, sort_keys=True))
else:
    print('GITHUB ACTIONS MANUAL TRIGGER AUDIT')
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
    print(f"TOP MANUAL-TRIGGER DEPENDENCE GROUPS ({min(top_n, len(rows))})")
    if not rows:
        print('none')
    else:
        for row in rows[:top_n]:
            branch_part = f" branch={row['branch']}" if row.get('branch') else ''
            print(
                f"- [{row['severity']}] {row['repository']} :: {row['workflow']}{branch_part} "
                f"manual_runs={row['manual_runs']}/{row['total_runs']} "
                f"manual_ratio={row['manual_ratio']:.3f} recent_manual_streak={row['recent_manual_streak']} "
                f"latest_event={row['latest_event']} risk_score={row['risk_score']}"
            )

sys.exit(1 if (fail_on_critical and critical_rows) else 0)
PY
