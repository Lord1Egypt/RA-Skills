#!/usr/bin/env bash
set -euo pipefail

RUN_GLOB="${RUN_GLOB:-artifacts/github-actions/*.json}"
TOP_N="${TOP_N:-20}"
OUTPUT_FORMAT="${OUTPUT_FORMAT:-text}"
MIN_RUNS="${MIN_RUNS:-3}"
WARN_RERUN_RATE="${WARN_RERUN_RATE:-0.25}"
CRITICAL_RERUN_RATE="${CRITICAL_RERUN_RATE:-0.45}"
WARN_FAILED_RUNS="${WARN_FAILED_RUNS:-2}"
CRITICAL_FAILED_RUNS="${CRITICAL_FAILED_RUNS:-4}"
WARN_WASTED_MINUTES="${WARN_WASTED_MINUTES:-25}"
CRITICAL_WASTED_MINUTES="${CRITICAL_WASTED_MINUTES:-75}"
WARN_WORKFLOWS="${WARN_WORKFLOWS:-2}"
CRITICAL_WORKFLOWS="${CRITICAL_WORKFLOWS:-4}"
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
FAILURE_CONCLUSIONS="${FAILURE_CONCLUSIONS:-failure,cancelled,timed_out,startup_failure,action_required}"
FAIL_ON_CRITICAL="${FAIL_ON_CRITICAL:-0}"

if [[ "$OUTPUT_FORMAT" != "text" && "$OUTPUT_FORMAT" != "json" ]]; then
  echo "ERROR: OUTPUT_FORMAT must be 'text' or 'json' (got: $OUTPUT_FORMAT)" >&2
  exit 1
fi

for value_name in TOP_N MIN_RUNS WARN_FAILED_RUNS CRITICAL_FAILED_RUNS WARN_WASTED_MINUTES CRITICAL_WASTED_MINUTES WARN_WORKFLOWS CRITICAL_WORKFLOWS; do
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

for value_name in WARN_RERUN_RATE CRITICAL_RERUN_RATE; do
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

python3 - "$RUN_GLOB" "$TOP_N" "$OUTPUT_FORMAT" "$MIN_RUNS" "$WARN_RERUN_RATE" "$CRITICAL_RERUN_RATE" "$WARN_FAILED_RUNS" "$CRITICAL_FAILED_RUNS" "$WARN_WASTED_MINUTES" "$CRITICAL_WASTED_MINUTES" "$WARN_WORKFLOWS" "$CRITICAL_WORKFLOWS" "$WORKFLOW_MATCH" "$WORKFLOW_EXCLUDE" "$BRANCH_MATCH" "$BRANCH_EXCLUDE" "$EVENT_MATCH" "$EVENT_EXCLUDE" "$REPO_MATCH" "$REPO_EXCLUDE" "$HEAD_SHA_MATCH" "$HEAD_SHA_EXCLUDE" "$FAILURE_CONCLUSIONS" "$FAIL_ON_CRITICAL" <<'PY'
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
    min_runs_raw,
    warn_rerun_rate_raw,
    critical_rerun_rate_raw,
    warn_failed_runs_raw,
    critical_failed_runs_raw,
    warn_wasted_minutes_raw,
    critical_wasted_minutes_raw,
    warn_workflows_raw,
    critical_workflows_raw,
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
    failure_conclusions_raw,
    fail_on_critical_raw,
) = sys.argv[1:]

top_n = int(top_n_raw)
min_runs = int(min_runs_raw)
warn_rerun_rate = float(warn_rerun_rate_raw)
critical_rerun_rate = float(critical_rerun_rate_raw)
warn_failed_runs = int(warn_failed_runs_raw)
critical_failed_runs = int(critical_failed_runs_raw)
warn_wasted_minutes = int(warn_wasted_minutes_raw)
critical_wasted_minutes = int(critical_wasted_minutes_raw)
warn_workflows = int(warn_workflows_raw)
critical_workflows = int(critical_workflows_raw)
fail_on_critical = fail_on_critical_raw == '1'

if critical_rerun_rate < warn_rerun_rate:
    print('ERROR: CRITICAL_RERUN_RATE must be >= WARN_RERUN_RATE', file=sys.stderr)
    sys.exit(1)
if critical_failed_runs < warn_failed_runs:
    print('ERROR: CRITICAL_FAILED_RUNS must be >= WARN_FAILED_RUNS', file=sys.stderr)
    sys.exit(1)
if critical_wasted_minutes < warn_wasted_minutes:
    print('ERROR: CRITICAL_WASTED_MINUTES must be >= WARN_WASTED_MINUTES', file=sys.stderr)
    sys.exit(1)
if critical_workflows < warn_workflows:
    print('ERROR: CRITICAL_WORKFLOWS must be >= WARN_WORKFLOWS', file=sys.stderr)
    sys.exit(1)

failure_conclusions = {item.strip().lower() for item in failure_conclusions_raw.split(',') if item.strip()}
if not failure_conclusions:
    print('ERROR: FAILURE_CONCLUSIONS must include at least one conclusion', file=sys.stderr)
    sys.exit(1)


def compile_regex(pattern, label):
    if not pattern:
        return None
    try:
        return re.compile(pattern)
    except re.error as exc:
        print(f'ERROR: invalid {label} regex {pattern!r}: {exc}', file=sys.stderr)
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
    return max(0.0, seconds / 60.0)


def normalize_repo(raw):
    if isinstance(raw, str) and raw.strip():
        return raw.strip()
    if isinstance(raw, dict):
        return raw.get('nameWithOwner') or raw.get('full_name') or raw.get('name') or '<unknown-repo>'
    return '<unknown-repo>'


def parse_attempt(raw):
    try:
        value = int(str(raw).strip())
    except Exception:
        return 1
    return value if value > 0 else 1


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
attempts_by_run = defaultdict(list)

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
    head_sha = str(payload.get('headSha') or '<unknown-sha>').strip() or '<unknown-sha>'

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
    if repo_match and not repo_match.search(repo):
        runs_filtered += 1
        continue
    if repo_exclude and repo_exclude.search(repo):
        runs_filtered += 1
        continue
    if head_sha_match and not head_sha_match.search(head_sha):
        runs_filtered += 1
        continue
    if head_sha_exclude and head_sha_exclude.search(head_sha):
        runs_filtered += 1
        continue

    run_id = payload.get('databaseId')
    if run_id is None:
        parse_errors.append(f'{path}: missing databaseId')
        continue

    created_at = parse_ts(payload.get('createdAt') or payload.get('runStartedAt'), 'createdAt/runStartedAt')
    if created_at is None:
        parse_errors.append(f'{path}: missing createdAt/runStartedAt')
        continue

    conclusion = str(payload.get('conclusion') or '<unknown>').strip().lower()

    attempts_by_run[(repo, run_id)].append({
        'repo': repo,
        'run_id': run_id,
        'workflow': workflow,
        'branch': branch,
        'event': event,
        'head_sha': head_sha,
        'attempt': parse_attempt(payload.get('runAttempt')),
        'conclusion': conclusion,
        'is_failure': conclusion in failure_conclusions,
        'created_at': created_at,
        'updated_at': parse_ts(payload.get('updatedAt') or payload.get('completedAt'), 'updatedAt/completedAt'),
        'duration_minutes': duration_minutes(payload),
        'url': payload.get('url') or '',
    })

rows_by_sha = defaultdict(list)
for (_repo, _run_id), attempts in attempts_by_run.items():
    ordered = sorted(attempts, key=lambda item: (item['attempt'], item['created_at'], item['updated_at'] or item['created_at']))
    latest = ordered[-1]
    rerun_attempts = max(0, len(ordered) - 1)
    wasted_minutes = sum(item['duration_minutes'] for item in ordered[1:])
    rows_by_sha[(latest['repo'], latest['head_sha'])].append({
        'workflow': latest['workflow'],
        'branch': latest['branch'],
        'event': latest['event'],
        'run_id': latest['run_id'],
        'has_rerun': rerun_attempts > 0,
        'rerun_attempts': rerun_attempts,
        'wasted_minutes': wasted_minutes,
        'is_failure': latest['is_failure'],
        'latest_conclusion': latest['conclusion'],
        'latest_run_at': latest['created_at'],
        'url': latest['url'],
    })

rows = []
critical_rows = []

for (repo, head_sha), run_rows in rows_by_sha.items():
    total_runs = len(run_rows)
    if total_runs < min_runs:
        continue

    rerun_rows = [row for row in run_rows if row['has_rerun']]
    rerun_runs = len(rerun_rows)
    rerun_rate = rerun_runs / total_runs
    failed_runs = sum(1 for row in run_rows if row['is_failure'])
    workflows = sorted({row['workflow'] for row in run_rows})
    workflow_count = len(workflows)
    wasted_minutes = sum(row['wasted_minutes'] for row in rerun_rows)
    rerun_attempts_total = sum(row['rerun_attempts'] for row in rerun_rows)

    severity = 'ok'
    if (
        rerun_rate >= critical_rerun_rate
        or failed_runs >= critical_failed_runs
        or wasted_minutes >= critical_wasted_minutes
        or workflow_count >= critical_workflows
    ):
        severity = 'critical'
    elif (
        rerun_rate >= warn_rerun_rate
        or failed_runs >= warn_failed_runs
        or wasted_minutes >= warn_wasted_minutes
        or workflow_count >= warn_workflows
    ):
        severity = 'warn'

    risk_score = (
        (rerun_rate * 100.0)
        + (failed_runs * 12.0)
        + (workflow_count * 8.0)
        + (wasted_minutes / 4.0)
        + (rerun_attempts_total * 2.0)
    )

    latest = max(run_rows, key=lambda row: row['latest_run_at'])

    row = {
        'repository': repo,
        'head_sha': head_sha,
        'severity': severity,
        'total_runs': total_runs,
        'rerun_runs': rerun_runs,
        'rerun_rate': round(rerun_rate, 4),
        'failed_runs': failed_runs,
        'workflow_count': workflow_count,
        'workflows': workflows[:8],
        'wasted_minutes': round(wasted_minutes, 2),
        'rerun_attempts_total': rerun_attempts_total,
        'latest_run_at': latest['latest_run_at'].isoformat(),
        'latest_conclusion': latest['latest_conclusion'],
        'sample_run_ids': [row['run_id'] for row in run_rows[:3]],
        'sample_urls': [row['url'] for row in run_rows[:3] if row.get('url')],
        'risk_score': round(risk_score, 3),
    }

    rows.append(row)
    if severity == 'critical':
        critical_rows.append(row)

rows.sort(key=lambda row: (-row['risk_score'], -row['rerun_rate'], -row['failed_runs'], row['repository'], row['head_sha']))

summary = {
    'files_scanned': len(files),
    'runs_scanned': runs_scanned,
    'runs_filtered': runs_filtered,
    'parse_errors': parse_errors,
    'groups': len(rows),
    'critical_groups': len(critical_rows),
    'failure_conclusions': sorted(failure_conclusions),
    'min_runs': min_runs,
    'warn_rerun_rate': warn_rerun_rate,
    'critical_rerun_rate': critical_rerun_rate,
    'warn_failed_runs': warn_failed_runs,
    'critical_failed_runs': critical_failed_runs,
    'warn_wasted_minutes': warn_wasted_minutes,
    'critical_wasted_minutes': critical_wasted_minutes,
    'warn_workflows': warn_workflows,
    'critical_workflows': critical_workflows,
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
    print('GITHUB ACTIONS SHA RERUN DEBT AUDIT')
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
    print(f"TOP SHA RERUN DEBT GROUPS ({min(top_n, len(rows))})")
    if not rows:
        print('none')
    else:
        for row in rows[:top_n]:
            print(
                f"- [{row['severity']}] repo={row['repository']} sha={row['head_sha']} "
                f"rerun_runs={row['rerun_runs']}/{row['total_runs']} rerun_rate={row['rerun_rate']:.3f} "
                f"failed_runs={row['failed_runs']} workflows={row['workflow_count']} "
                f"wasted_minutes={row['wasted_minutes']:.2f} rerun_attempts_total={row['rerun_attempts_total']} "
                f"latest_conclusion={row['latest_conclusion']} risk_score={row['risk_score']}"
            )

sys.exit(1 if (fail_on_critical and critical_rows) else 0)
PY
