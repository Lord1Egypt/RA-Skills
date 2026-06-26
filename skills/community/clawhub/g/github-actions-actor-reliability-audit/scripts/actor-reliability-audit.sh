#!/usr/bin/env bash
set -euo pipefail

RUN_GLOB="${RUN_GLOB:-artifacts/github-actions/*.json}"
TOP_N="${TOP_N:-20}"
OUTPUT_FORMAT="${OUTPUT_FORMAT:-text}"
GROUP_BY="${GROUP_BY:-actor}"
FAILURE_CONCLUSIONS="${FAILURE_CONCLUSIONS:-failure,cancelled,timed_out,startup_failure}"
MIN_RUNS="${MIN_RUNS:-5}"
WARN_FAILURE_RATE="${WARN_FAILURE_RATE:-0.25}"
CRITICAL_FAILURE_RATE="${CRITICAL_FAILURE_RATE:-0.5}"
WARN_FAILED_RUNS="${WARN_FAILED_RUNS:-4}"
CRITICAL_FAILED_RUNS="${CRITICAL_FAILED_RUNS:-8}"
WARN_FAILURE_STREAK="${WARN_FAILURE_STREAK:-2}"
CRITICAL_FAILURE_STREAK="${CRITICAL_FAILURE_STREAK:-4}"
ACTOR_MATCH="${ACTOR_MATCH:-}"
ACTOR_EXCLUDE="${ACTOR_EXCLUDE:-}"
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

if [[ "$GROUP_BY" != "actor" && "$GROUP_BY" != "actor-workflow" ]]; then
  echo "ERROR: GROUP_BY must be 'actor' or 'actor-workflow' (got: $GROUP_BY)" >&2
  exit 1
fi

for value_name in TOP_N MIN_RUNS WARN_FAILED_RUNS CRITICAL_FAILED_RUNS WARN_FAILURE_STREAK CRITICAL_FAILURE_STREAK; do
  value="${!value_name}"
  if ! [[ "$value" =~ ^[0-9]+$ ]] || [[ "$value" -eq 0 ]]; then
    echo "ERROR: $value_name must be a positive integer (got: $value)" >&2
    exit 1
  fi
done

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

python3 - "$RUN_GLOB" "$TOP_N" "$OUTPUT_FORMAT" "$GROUP_BY" "$FAILURE_CONCLUSIONS" "$MIN_RUNS" "$WARN_FAILURE_RATE" "$CRITICAL_FAILURE_RATE" "$WARN_FAILED_RUNS" "$CRITICAL_FAILED_RUNS" "$WARN_FAILURE_STREAK" "$CRITICAL_FAILURE_STREAK" "$ACTOR_MATCH" "$ACTOR_EXCLUDE" "$WORKFLOW_MATCH" "$WORKFLOW_EXCLUDE" "$BRANCH_MATCH" "$BRANCH_EXCLUDE" "$EVENT_MATCH" "$EVENT_EXCLUDE" "$REPO_MATCH" "$REPO_EXCLUDE" "$FAIL_ON_CRITICAL" <<'PY'
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
    failure_conclusions_raw,
    min_runs_raw,
    warn_failure_rate_raw,
    critical_failure_rate_raw,
    warn_failed_runs_raw,
    critical_failed_runs_raw,
    warn_failure_streak_raw,
    critical_failure_streak_raw,
    actor_match_raw,
    actor_exclude_raw,
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
min_runs = int(min_runs_raw)
warn_failure_rate = float(warn_failure_rate_raw)
critical_failure_rate = float(critical_failure_rate_raw)
warn_failed_runs = int(warn_failed_runs_raw)
critical_failed_runs = int(critical_failed_runs_raw)
warn_failure_streak = int(warn_failure_streak_raw)
critical_failure_streak = int(critical_failure_streak_raw)
fail_on_critical = fail_on_critical_raw == '1'

failure_conclusions = {
    item.strip().lower()
    for item in failure_conclusions_raw.split(',')
    if item.strip()
}

if not failure_conclusions:
    print('ERROR: FAILURE_CONCLUSIONS must include at least one conclusion', file=sys.stderr)
    sys.exit(1)
if critical_failure_rate < warn_failure_rate:
    print('ERROR: CRITICAL_FAILURE_RATE must be >= WARN_FAILURE_RATE', file=sys.stderr)
    sys.exit(1)
if critical_failed_runs < warn_failed_runs:
    print('ERROR: CRITICAL_FAILED_RUNS must be >= WARN_FAILED_RUNS', file=sys.stderr)
    sys.exit(1)
if critical_failure_streak < warn_failure_streak:
    print('ERROR: CRITICAL_FAILURE_STREAK must be >= WARN_FAILURE_STREAK', file=sys.stderr)
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


def normalize_actor(payload):
    actor = payload.get('triggeringActor') or payload.get('actor')
    if isinstance(actor, str) and actor.strip():
        return actor.strip()
    if isinstance(actor, dict):
        return (
            actor.get('login')
            or actor.get('name')
            or actor.get('username')
            or '<unknown-actor>'
        )
    return '<unknown-actor>'


def failure_streak(sorted_runs):
    streak = 0
    for run in reversed(sorted_runs):
        if run['is_failure']:
            streak += 1
        else:
            break
    return streak


actor_match = compile_regex(actor_match_raw, 'ACTOR_MATCH')
actor_exclude = compile_regex(actor_exclude_raw, 'ACTOR_EXCLUDE')
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
    conclusion = (payload.get('conclusion') or '').strip().lower() or '<unknown>'
    repository = normalize_repo(payload.get('repository'))
    actor = normalize_actor(payload)

    if actor_match and not actor_match.search(actor):
        runs_filtered += 1
        continue
    if actor_exclude and actor_exclude.search(actor):
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

    key = (actor,) if group_by == 'actor' else (actor, workflow)
    groups[key].append(
        {
            'database_id': payload.get('databaseId'),
            'created_at': created_at,
            'repository': repository,
            'workflow': workflow,
            'branch': branch,
            'event': event,
            'conclusion': conclusion,
            'is_failure': conclusion in failure_conclusions,
            'url': payload.get('url') or '',
        }
    )

rows = []
critical_rows = []

for key, runs in groups.items():
    if len(runs) < min_runs:
        continue

    sorted_runs = sorted(runs, key=lambda row: row['created_at'])
    failed_runs = [row for row in sorted_runs if row['is_failure']]
    failed_count = len(failed_runs)
    failure_rate = failed_count / len(sorted_runs)
    latest = sorted_runs[-1]
    streak = failure_streak(sorted_runs)

    severity = 'ok'
    if failure_rate >= critical_failure_rate or failed_count >= critical_failed_runs or streak >= critical_failure_streak:
        severity = 'critical'
    elif failure_rate >= warn_failure_rate or failed_count >= warn_failed_runs or streak >= warn_failure_streak:
        severity = 'warn'

    risk_score = (failure_rate * 100.0) + (failed_count * 3.0) + (streak * 10.0)

    row = {
        'actor': key[0],
        'workflow': (key[1] if len(key) > 1 else None),
        'severity': severity,
        'total_runs': len(sorted_runs),
        'failed_runs': failed_count,
        'failure_rate': round(failure_rate, 4),
        'latest_failure_streak': streak,
        'latest_run_at': latest['created_at'].isoformat(),
        'latest_conclusion': latest['conclusion'],
        'latest_event': latest['event'],
        'sample_failed_run_ids': [item['database_id'] for item in failed_runs[-3:] if item.get('database_id') is not None],
        'sample_failed_run_urls': [item['url'] for item in failed_runs[-3:] if item.get('url')],
        'sample_repositories': sorted({item['repository'] for item in sorted_runs})[:5],
        'risk_score': round(risk_score, 3),
    }

    rows.append(row)
    if severity == 'critical':
        critical_rows.append(row)

rows.sort(
    key=lambda row: (
        -row['risk_score'],
        -row['failure_rate'],
        -row['failed_runs'],
        row['actor'],
        row['workflow'] or '',
    )
)

summary = {
    'files_scanned': len(files),
    'runs_scanned': runs_scanned,
    'runs_filtered': runs_filtered,
    'parse_errors': parse_errors,
    'groups': len(rows),
    'critical_groups': len(critical_rows),
    'group_by': group_by,
    'failure_conclusions': sorted(failure_conclusions),
    'min_runs': min_runs,
    'warn_failure_rate': warn_failure_rate,
    'critical_failure_rate': critical_failure_rate,
    'warn_failed_runs': warn_failed_runs,
    'critical_failed_runs': critical_failed_runs,
    'warn_failure_streak': warn_failure_streak,
    'critical_failure_streak': critical_failure_streak,
    'evaluated_at': datetime.now(timezone.utc).isoformat(),
    'filters': {
        'actor_match': actor_match_raw or None,
        'actor_exclude': actor_exclude_raw or None,
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
    print('GITHUB ACTIONS ACTOR RELIABILITY AUDIT')
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
    print(f"TOP ACTOR RISK GROUPS ({min(top_n, len(rows))})")
    if not rows:
        print('none')
    else:
        for row in rows[:top_n]:
            workflow_part = f" workflow={row['workflow']}" if row.get('workflow') else ''
            print(
                f"- [{row['severity']}] actor={row['actor']}{workflow_part} "
                f"failed_runs={row['failed_runs']}/{row['total_runs']} "
                f"failure_rate={row['failure_rate']:.3f} latest_failure_streak={row['latest_failure_streak']} "
                f"latest_conclusion={row['latest_conclusion']} risk_score={row['risk_score']}"
            )

sys.exit(1 if (fail_on_critical and critical_rows) else 0)
PY
