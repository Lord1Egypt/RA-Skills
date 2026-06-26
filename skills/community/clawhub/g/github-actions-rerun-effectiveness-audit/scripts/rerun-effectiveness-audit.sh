#!/usr/bin/env bash
set -euo pipefail

RUN_GLOB="${RUN_GLOB:-artifacts/github-actions/*.json}"
TOP_N="${TOP_N:-20}"
OUTPUT_FORMAT="${OUTPUT_FORMAT:-text}"
GROUP_BY="${GROUP_BY:-workflow}"
FAILURE_CONCLUSIONS="${FAILURE_CONCLUSIONS:-failure,cancelled,timed_out,startup_failure,action_required}"
SUCCESS_CONCLUSIONS="${SUCCESS_CONCLUSIONS:-success}"
MIN_RUNS="${MIN_RUNS:-4}"
WARN_RERUN_RATE="${WARN_RERUN_RATE:-0.2}"
CRITICAL_RERUN_RATE="${CRITICAL_RERUN_RATE:-0.35}"
WARN_RERUN_SUCCESS_RATE="${WARN_RERUN_SUCCESS_RATE:-0.5}"
CRITICAL_RERUN_SUCCESS_RATE="${CRITICAL_RERUN_SUCCESS_RATE:-0.25}"
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
ACTOR_MATCH="${ACTOR_MATCH:-}"
ACTOR_EXCLUDE="${ACTOR_EXCLUDE:-}"
FAIL_ON_CRITICAL="${FAIL_ON_CRITICAL:-0}"

if [[ "$OUTPUT_FORMAT" != "text" && "$OUTPUT_FORMAT" != "json" ]]; then
  echo "ERROR: OUTPUT_FORMAT must be 'text' or 'json' (got: $OUTPUT_FORMAT)" >&2
  exit 1
fi

if [[ "$GROUP_BY" != "workflow" && "$GROUP_BY" != "workflow-branch" ]]; then
  echo "ERROR: GROUP_BY must be 'workflow' or 'workflow-branch' (got: $GROUP_BY)" >&2
  exit 1
fi

for value_name in TOP_N MIN_RUNS WARN_WASTED_MINUTES CRITICAL_WASTED_MINUTES; do
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
if [[ "$MIN_RUNS" -eq 0 ]]; then
  echo "ERROR: MIN_RUNS must be >= 1" >&2
  exit 1
fi

for value_name in WARN_RERUN_RATE CRITICAL_RERUN_RATE WARN_RERUN_SUCCESS_RATE CRITICAL_RERUN_SUCCESS_RATE; do
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

python3 - "$RUN_GLOB" "$TOP_N" "$OUTPUT_FORMAT" "$GROUP_BY" "$FAILURE_CONCLUSIONS" "$SUCCESS_CONCLUSIONS" "$MIN_RUNS" "$WARN_RERUN_RATE" "$CRITICAL_RERUN_RATE" "$WARN_RERUN_SUCCESS_RATE" "$CRITICAL_RERUN_SUCCESS_RATE" "$WARN_WASTED_MINUTES" "$CRITICAL_WASTED_MINUTES" "$WORKFLOW_MATCH" "$WORKFLOW_EXCLUDE" "$BRANCH_MATCH" "$BRANCH_EXCLUDE" "$EVENT_MATCH" "$EVENT_EXCLUDE" "$REPO_MATCH" "$REPO_EXCLUDE" "$ACTOR_MATCH" "$ACTOR_EXCLUDE" "$FAIL_ON_CRITICAL" <<'PY'
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
    success_conclusions_raw,
    min_runs_raw,
    warn_rerun_rate_raw,
    critical_rerun_rate_raw,
    warn_rerun_success_rate_raw,
    critical_rerun_success_rate_raw,
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
    actor_match_raw,
    actor_exclude_raw,
    fail_on_critical_raw,
) = sys.argv[1:]

top_n = int(top_n_raw)
min_runs = int(min_runs_raw)
warn_rerun_rate = float(warn_rerun_rate_raw)
critical_rerun_rate = float(critical_rerun_rate_raw)
warn_rerun_success_rate = float(warn_rerun_success_rate_raw)
critical_rerun_success_rate = float(critical_rerun_success_rate_raw)
warn_wasted_minutes = int(warn_wasted_minutes_raw)
critical_wasted_minutes = int(critical_wasted_minutes_raw)
fail_on_critical = fail_on_critical_raw == '1'

failure_conclusions = {
    item.strip().lower()
    for item in failure_conclusions_raw.split(',')
    if item.strip()
}
success_conclusions = {
    item.strip().lower()
    for item in success_conclusions_raw.split(',')
    if item.strip()
}

if not failure_conclusions:
    print('ERROR: FAILURE_CONCLUSIONS must include at least one conclusion', file=sys.stderr)
    sys.exit(1)
if not success_conclusions:
    print('ERROR: SUCCESS_CONCLUSIONS must include at least one conclusion', file=sys.stderr)
    sys.exit(1)
if critical_rerun_rate < warn_rerun_rate:
    print('ERROR: CRITICAL_RERUN_RATE must be >= WARN_RERUN_RATE', file=sys.stderr)
    sys.exit(1)
if critical_rerun_success_rate > warn_rerun_success_rate:
    print('ERROR: CRITICAL_RERUN_SUCCESS_RATE must be <= WARN_RERUN_SUCCESS_RATE', file=sys.stderr)
    sys.exit(1)
if critical_wasted_minutes < warn_wasted_minutes:
    print('ERROR: CRITICAL_WASTED_MINUTES must be >= WARN_WASTED_MINUTES', file=sys.stderr)
    sys.exit(1)


def parse_ts(value, label):
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


def duration_minutes(payload):
    started = parse_ts(payload.get('runStartedAt') or payload.get('createdAt'), 'runStartedAt/createdAt')
    finished = parse_ts(payload.get('updatedAt') or payload.get('completedAt'), 'updatedAt/completedAt')
    if started is None or finished is None:
        return 0.0
    seconds = (finished - started).total_seconds()
    if seconds < 0:
        return 0.0
    return seconds / 60.0


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


def parse_run_attempt(payload):
    raw = payload.get('runAttempt')
    if raw is None:
        return 1
    try:
        parsed = int(str(raw).strip())
    except ValueError:
        return 1
    return parsed if parsed > 0 else 1


workflow_match = compile_regex(workflow_match_raw, 'WORKFLOW_MATCH')
workflow_exclude = compile_regex(workflow_exclude_raw, 'WORKFLOW_EXCLUDE')
branch_match = compile_regex(branch_match_raw, 'BRANCH_MATCH')
branch_exclude = compile_regex(branch_exclude_raw, 'BRANCH_EXCLUDE')
event_match = compile_regex(event_match_raw, 'EVENT_MATCH')
event_exclude = compile_regex(event_exclude_raw, 'EVENT_EXCLUDE')
repo_match = compile_regex(repo_match_raw, 'REPO_MATCH')
repo_exclude = compile_regex(repo_exclude_raw, 'REPO_EXCLUDE')
actor_match = compile_regex(actor_match_raw, 'ACTOR_MATCH')
actor_exclude = compile_regex(actor_exclude_raw, 'ACTOR_EXCLUDE')

files = sorted(glob.glob(run_glob, recursive=True))
if not files:
    print(f'ERROR: no files matched RUN_GLOB={run_glob}', file=sys.stderr)
    sys.exit(1)

parse_errors = []
runs_scanned = 0
runs_filtered = 0
attempt_groups = defaultdict(list)

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
    conclusion = (payload.get('conclusion') or '<unknown>').strip().lower()
    repository = normalize_repo(payload.get('repository'))
    actor = normalize_actor(payload)

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
    if actor_match and not actor_match.search(actor):
        runs_filtered += 1
        continue
    if actor_exclude and actor_exclude.search(actor):
        runs_filtered += 1
        continue

    created_at = parse_ts(payload.get('createdAt') or payload.get('runStartedAt') or payload.get('startedAt'), 'createdAt')
    if created_at is None:
        parse_errors.append(f'{path}: missing createdAt/runStartedAt/startedAt')
        continue

    run_id = payload.get('databaseId')
    if run_id is None:
        parse_errors.append(f'{path}: missing databaseId (required to correlate rerun attempts)')
        continue

    attempt_groups[(repository, run_id)].append(
        {
            'workflow': workflow,
            'branch': branch,
            'event': event,
            'actor': actor,
            'run_id': run_id,
            'head_sha': payload.get('headSha') or '<unknown-sha>',
            'attempt': parse_run_attempt(payload),
            'conclusion': conclusion,
            'is_failure': conclusion in failure_conclusions,
            'is_success': conclusion in success_conclusions,
            'created_at': created_at,
            'updated_at': parse_ts(payload.get('updatedAt') or payload.get('completedAt'), 'updatedAt/completedAt'),
            'url': payload.get('url') or '',
            'duration_minutes': duration_minutes(payload),
        }
    )

rows_by_group = defaultdict(list)

for (repository, run_id), attempts in attempt_groups.items():
    attempts_sorted = sorted(
        attempts,
        key=lambda row: (row['attempt'], row['created_at'], row['updated_at'] or row['created_at']),
    )
    if not attempts_sorted:
        continue

    latest_attempt = attempts_sorted[-1]
    rerun_attempts = max(0, len(attempts_sorted) - 1)
    wasted_minutes = sum(item['duration_minutes'] for item in attempts_sorted[1:])
    rerun_failed = rerun_attempts > 0 and latest_attempt['is_failure']

    group_key = (
        latest_attempt['workflow'],
        latest_attempt['branch'] if group_by == 'workflow-branch' else None,
    )

    rows_by_group[group_key].append(
        {
            'repository': repository,
            'workflow': latest_attempt['workflow'],
            'branch': latest_attempt['branch'],
            'event': latest_attempt['event'],
            'actor': latest_attempt['actor'],
            'run_id': run_id,
            'head_sha': latest_attempt['head_sha'],
            'attempt_count': len(attempts_sorted),
            'rerun_attempts': rerun_attempts,
            'has_rerun': rerun_attempts > 0,
            'rerun_failed': rerun_failed,
            'final_success': latest_attempt['is_success'],
            'final_failure': latest_attempt['is_failure'],
            'wasted_minutes': wasted_minutes,
            'latest_conclusion': latest_attempt['conclusion'],
            'latest_run_at': latest_attempt['created_at'],
            'sample_url': latest_attempt['url'],
        }
    )

rows = []
critical_rows = []

for (workflow, branch), run_rows in rows_by_group.items():
    total_runs = len(run_rows)
    if total_runs < min_runs:
        continue

    rerun_rows = [row for row in run_rows if row['has_rerun']]
    rerun_runs = len(rerun_rows)
    rerun_rate = rerun_runs / total_runs

    successful_reruns = sum(1 for row in rerun_rows if row['final_success'])
    rerun_success_rate = (successful_reruns / rerun_runs) if rerun_runs else 1.0
    failed_reruns = rerun_runs - successful_reruns

    rerun_attempts_total = sum(row['rerun_attempts'] for row in rerun_rows)
    wasted_minutes = sum(row['wasted_minutes'] for row in rerun_rows)

    severity = 'ok'
    if (
        rerun_rate >= critical_rerun_rate
        or (rerun_runs > 0 and rerun_success_rate <= critical_rerun_success_rate)
        or wasted_minutes >= critical_wasted_minutes
    ):
        severity = 'critical'
    elif (
        rerun_rate >= warn_rerun_rate
        or (rerun_runs > 0 and rerun_success_rate <= warn_rerun_success_rate)
        or wasted_minutes >= warn_wasted_minutes
    ):
        severity = 'warn'

    risk_score = (
        (rerun_rate * 100.0)
        + ((1.0 - rerun_success_rate) * 50.0)
        + (wasted_minutes / 5.0)
        + (rerun_attempts_total * 2.0)
    )

    sample_rerun_ids = [row['run_id'] for row in rerun_rows[:3]]
    sample_rerun_urls = [row['sample_url'] for row in rerun_rows[:3] if row.get('sample_url')]

    row = {
        'workflow': workflow,
        'branch': branch,
        'severity': severity,
        'total_runs': total_runs,
        'rerun_runs': rerun_runs,
        'rerun_rate': round(rerun_rate, 4),
        'rerun_success_rate': round(rerun_success_rate, 4),
        'failed_reruns': failed_reruns,
        'rerun_attempts_total': rerun_attempts_total,
        'wasted_minutes': round(wasted_minutes, 2),
        'latest_run_at': max(row['latest_run_at'] for row in run_rows).isoformat(),
        'latest_conclusion': max(run_rows, key=lambda row: row['latest_run_at'])['latest_conclusion'],
        'sample_repositories': sorted({row['repository'] for row in run_rows})[:5],
        'sample_rerun_run_ids': sample_rerun_ids,
        'sample_rerun_urls': sample_rerun_urls,
        'risk_score': round(risk_score, 3),
    }

    rows.append(row)
    if severity == 'critical':
        critical_rows.append(row)

rows.sort(
    key=lambda row: (
        -row['risk_score'],
        -row['rerun_rate'],
        row['workflow'],
        row.get('branch') or '',
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
    'success_conclusions': sorted(success_conclusions),
    'min_runs': min_runs,
    'warn_rerun_rate': warn_rerun_rate,
    'critical_rerun_rate': critical_rerun_rate,
    'warn_rerun_success_rate': warn_rerun_success_rate,
    'critical_rerun_success_rate': critical_rerun_success_rate,
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
        'actor_match': actor_match_raw or None,
        'actor_exclude': actor_exclude_raw or None,
    },
}

if output_format == 'json':
    print(json.dumps({'summary': summary, 'groups': rows[:top_n], 'all_groups': rows, 'critical_groups': critical_rows}, indent=2, sort_keys=True))
else:
    print('GITHUB ACTIONS RERUN EFFECTIVENESS AUDIT')
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
    print(f"TOP RERUN RISK GROUPS ({min(top_n, len(rows))})")
    if not rows:
        print('none')
    else:
        for row in rows[:top_n]:
            branch_part = f" branch={row['branch']}" if row.get('branch') else ''
            print(
                f"- [{row['severity']}] workflow={row['workflow']}{branch_part} "
                f"rerun_runs={row['rerun_runs']}/{row['total_runs']} "
                f"rerun_rate={row['rerun_rate']:.3f} rerun_success_rate={row['rerun_success_rate']:.3f} "
                f"wasted_minutes={row['wasted_minutes']:.2f} rerun_attempts_total={row['rerun_attempts_total']} "
                f"latest_conclusion={row['latest_conclusion']} risk_score={row['risk_score']}"
            )

sys.exit(1 if (fail_on_critical and critical_rows) else 0)
PY
