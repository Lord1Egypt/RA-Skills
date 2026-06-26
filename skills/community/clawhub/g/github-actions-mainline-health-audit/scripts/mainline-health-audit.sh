#!/usr/bin/env bash
set -euo pipefail

RUN_GLOB="${RUN_GLOB:-artifacts/github-actions/*.json}"
TOP_N="${TOP_N:-20}"
OUTPUT_FORMAT="${OUTPUT_FORMAT:-text}"
MIN_RUNS="${MIN_RUNS:-2}"
MAINLINE_BRANCH_MATCH="${MAINLINE_BRANCH_MATCH:-^(main|master|release.*)$}"
WORKFLOW_MATCH="${WORKFLOW_MATCH:-}"
WORKFLOW_EXCLUDE="${WORKFLOW_EXCLUDE:-}"
EVENT_MATCH="${EVENT_MATCH:-}"
EVENT_EXCLUDE="${EVENT_EXCLUDE:-}"
REPO_MATCH="${REPO_MATCH:-}"
REPO_EXCLUDE="${REPO_EXCLUDE:-}"
HEAD_SHA_MATCH="${HEAD_SHA_MATCH:-}"
HEAD_SHA_EXCLUDE="${HEAD_SHA_EXCLUDE:-}"
CONCLUSION_MATCH="${CONCLUSION_MATCH:-}"
CONCLUSION_EXCLUDE="${CONCLUSION_EXCLUDE:-}"
RUN_ID_MATCH="${RUN_ID_MATCH:-}"
RUN_ID_EXCLUDE="${RUN_ID_EXCLUDE:-}"
RUN_URL_MATCH="${RUN_URL_MATCH:-}"
RUN_URL_EXCLUDE="${RUN_URL_EXCLUDE:-}"
FAIL_WARN_PERCENT="${FAIL_WARN_PERCENT:-20}"
FAIL_CRITICAL_PERCENT="${FAIL_CRITICAL_PERCENT:-40}"
STALE_SUCCESS_DAYS="${STALE_SUCCESS_DAYS:-7}"
WARN_SCORE="${WARN_SCORE:-30}"
CRITICAL_SCORE="${CRITICAL_SCORE:-55}"
FAIL_ON_CRITICAL="${FAIL_ON_CRITICAL:-0}"

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

for value_name in FAIL_WARN_PERCENT FAIL_CRITICAL_PERCENT STALE_SUCCESS_DAYS WARN_SCORE CRITICAL_SCORE; do
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

python3 - "$RUN_GLOB" "$TOP_N" "$OUTPUT_FORMAT" "$MIN_RUNS" "$MAINLINE_BRANCH_MATCH" "$WORKFLOW_MATCH" "$WORKFLOW_EXCLUDE" "$EVENT_MATCH" "$EVENT_EXCLUDE" "$REPO_MATCH" "$REPO_EXCLUDE" "$HEAD_SHA_MATCH" "$HEAD_SHA_EXCLUDE" "$CONCLUSION_MATCH" "$CONCLUSION_EXCLUDE" "$RUN_ID_MATCH" "$RUN_ID_EXCLUDE" "$RUN_URL_MATCH" "$RUN_URL_EXCLUDE" "$FAIL_WARN_PERCENT" "$FAIL_CRITICAL_PERCENT" "$STALE_SUCCESS_DAYS" "$WARN_SCORE" "$CRITICAL_SCORE" "$FAIL_ON_CRITICAL" <<'PY'
import glob
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone

run_glob = sys.argv[1]
top_n = int(sys.argv[2])
output_format = sys.argv[3]
min_runs = int(sys.argv[4])
mainline_branch_match_raw = sys.argv[5]
workflow_match_raw = sys.argv[6]
workflow_exclude_raw = sys.argv[7]
event_match_raw = sys.argv[8]
event_exclude_raw = sys.argv[9]
repo_match_raw = sys.argv[10]
repo_exclude_raw = sys.argv[11]
head_sha_match_raw = sys.argv[12]
head_sha_exclude_raw = sys.argv[13]
conclusion_match_raw = sys.argv[14]
conclusion_exclude_raw = sys.argv[15]
run_id_match_raw = sys.argv[16]
run_id_exclude_raw = sys.argv[17]
run_url_match_raw = sys.argv[18]
run_url_exclude_raw = sys.argv[19]
warn_pct = float(sys.argv[20])
critical_pct = float(sys.argv[21])
stale_success_days = float(sys.argv[22])
warn_score = float(sys.argv[23])
critical_score = float(sys.argv[24])
fail_on_critical = sys.argv[25] == '1'

if critical_pct < warn_pct:
    print('ERROR: FAIL_CRITICAL_PERCENT must be >= FAIL_WARN_PERCENT', file=sys.stderr)
    sys.exit(1)
if critical_score < warn_score:
    print('ERROR: CRITICAL_SCORE must be >= WARN_SCORE', file=sys.stderr)
    sys.exit(1)


def compile_regex(pattern, label, required=False):
    if not pattern and not required:
        return None
    if not pattern and required:
        print(f'ERROR: {label} is required', file=sys.stderr)
        sys.exit(1)
    try:
        return re.compile(pattern)
    except re.error as exc:
        print(f'ERROR: invalid {label} regex {pattern!r}: {exc}', file=sys.stderr)
        sys.exit(1)


mainline_branch_match = compile_regex(mainline_branch_match_raw, 'MAINLINE_BRANCH_MATCH', required=True)
workflow_match = compile_regex(workflow_match_raw, 'WORKFLOW_MATCH')
workflow_exclude = compile_regex(workflow_exclude_raw, 'WORKFLOW_EXCLUDE')
event_match = compile_regex(event_match_raw, 'EVENT_MATCH')
event_exclude = compile_regex(event_exclude_raw, 'EVENT_EXCLUDE')
repo_match = compile_regex(repo_match_raw, 'REPO_MATCH')
repo_exclude = compile_regex(repo_exclude_raw, 'REPO_EXCLUDE')
head_sha_match = compile_regex(head_sha_match_raw, 'HEAD_SHA_MATCH')
head_sha_exclude = compile_regex(head_sha_exclude_raw, 'HEAD_SHA_EXCLUDE')
conclusion_match = compile_regex(conclusion_match_raw, 'CONCLUSION_MATCH')
conclusion_exclude = compile_regex(conclusion_exclude_raw, 'CONCLUSION_EXCLUDE')
run_id_match = compile_regex(run_id_match_raw, 'RUN_ID_MATCH')
run_id_exclude = compile_regex(run_id_exclude_raw, 'RUN_ID_EXCLUDE')
run_url_match = compile_regex(run_url_match_raw, 'RUN_URL_MATCH')
run_url_exclude = compile_regex(run_url_exclude_raw, 'RUN_URL_EXCLUDE')


failure_outcomes = {'failure', 'cancelled', 'timed_out', 'startup_failure', 'stale', 'action_required'}


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


files = sorted(glob.glob(run_glob, recursive=True))
if not files:
    print(f'ERROR: no files matched RUN_GLOB={run_glob}', file=sys.stderr)
    sys.exit(1)

parse_errors = []
runs_scanned = 0
runs_filtered = 0
non_mainline_filtered = 0

agg = defaultdict(lambda: {
    'repository': None,
    'workflow': None,
    'branch': None,
    'event': None,
    'outcomes': defaultdict(int),
    'runs': [],
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

    branch = payload.get('headBranch') or '<unknown-branch>'
    if not mainline_branch_match.search(branch):
        non_mainline_filtered += 1
        continue

    workflow = payload.get('workflowName') or payload.get('name') or '<unknown-workflow>'
    event = payload.get('event') or '<unknown-event>'
    repository = normalize_repo(payload.get('repository'))
    head_sha = payload.get('headSha') or payload.get('head_sha') or '<unknown-sha>'
    run_id = str(payload.get('databaseId') or payload.get('id') or '<unknown-run-id>')
    run_url = str(payload.get('url') or '')

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

    conclusion = (payload.get('conclusion') or payload.get('status') or 'unknown').lower()
    if conclusion_match and not conclusion_match.search(conclusion):
        runs_filtered += 1
        continue
    if conclusion_exclude and conclusion_exclude.search(conclusion):
        runs_filtered += 1
        continue
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

    created_at = parse_ts(payload.get('createdAt') or payload.get('runStartedAt') or payload.get('startedAt'))
    updated_at = parse_ts(payload.get('updatedAt') or payload.get('completedAt'))

    key = (repository, workflow, branch, event)
    bucket = agg[key]
    bucket['repository'] = repository
    bucket['workflow'] = workflow
    bucket['branch'] = branch
    bucket['event'] = event
    bucket['outcomes'][conclusion] += 1
    bucket['runs'].append({
        'created_at': created_at,
        'updated_at': updated_at,
        'conclusion': conclusion,
    })
    if run_url and len(bucket['sample_urls']) < 3 and run_url not in bucket['sample_urls']:
        bucket['sample_urls'].append(run_url)


now = datetime.now(timezone.utc)
groups = []
critical_groups = []

for bucket in agg.values():
    total_runs = sum(bucket['outcomes'].values())
    if total_runs < min_runs:
        continue

    failed_runs = sum(count for outcome, count in bucket['outcomes'].items() if outcome in failure_outcomes)
    success_runs = bucket['outcomes'].get('success', 0)
    failure_rate = (failed_runs / total_runs) * 100.0

    runs_with_time = [r for r in bucket['runs'] if r['created_at'] is not None]
    runs_with_time.sort(key=lambda item: item['created_at'])

    consecutive_failures = 0
    for run in reversed(runs_with_time):
        if run['conclusion'] in failure_outcomes:
            consecutive_failures += 1
        elif run['conclusion'] == 'success':
            break
        else:
            break

    latest_success_at = None
    latest_failure_at = None
    for run in reversed(runs_with_time):
        if latest_success_at is None and run['conclusion'] == 'success':
            latest_success_at = run['created_at']
        if latest_failure_at is None and run['conclusion'] in failure_outcomes:
            latest_failure_at = run['created_at']
        if latest_success_at and latest_failure_at:
            break

    stale_days = stale_success_days
    days_since_success = None
    if latest_success_at is not None:
        days_since_success = (now - latest_success_at).total_seconds() / 86400.0
        stale_days = max(0.0, days_since_success - stale_success_days)

    days_since_failure = None
    if latest_failure_at is not None:
        days_since_failure = (now - latest_failure_at).total_seconds() / 86400.0

    runtime_seconds = []
    for run in bucket['runs']:
        if run['created_at'] and run['updated_at']:
            diff = (run['updated_at'] - run['created_at']).total_seconds()
            if diff >= 0:
                runtime_seconds.append(diff)

    score = failure_rate + (consecutive_failures * 10.0) + min(25.0, stale_days * 2.0)
    score = round(score, 3)

    severity = 'ok'
    if failure_rate >= critical_pct or score >= critical_score:
        severity = 'critical'
    elif failure_rate >= warn_pct or score >= warn_score:
        severity = 'warn'

    row = {
        'repository': bucket['repository'],
        'workflow': bucket['workflow'],
        'branch': bucket['branch'],
        'event': bucket['event'],
        'total_runs': total_runs,
        'failed_runs': failed_runs,
        'success_runs': success_runs,
        'failure_rate_percent': round(failure_rate, 3),
        'consecutive_failures': consecutive_failures,
        'latest_success_at': latest_success_at.isoformat() if latest_success_at else None,
        'latest_failure_at': latest_failure_at.isoformat() if latest_failure_at else None,
        'days_since_success': round(days_since_success, 3) if days_since_success is not None else None,
        'days_since_failure': round(days_since_failure, 3) if days_since_failure is not None else None,
        'avg_runtime_seconds': round((sum(runtime_seconds) / len(runtime_seconds)), 3) if runtime_seconds else None,
        'max_runtime_seconds': round(max(runtime_seconds), 3) if runtime_seconds else None,
        'health_score': score,
        'severity': severity,
        'outcomes': dict(sorted(bucket['outcomes'].items())),
        'sample_urls': bucket['sample_urls'],
    }
    groups.append(row)
    if severity == 'critical':
        critical_groups.append(row)

groups.sort(key=lambda row: (-row['health_score'], -row['failure_rate_percent'], -row['consecutive_failures'], row['repository'], row['workflow'], row['branch'], row['event']))

summary = {
    'files_scanned': len(files),
    'parse_errors': parse_errors,
    'runs_scanned': runs_scanned,
    'runs_filtered': runs_filtered,
    'non_mainline_filtered': non_mainline_filtered,
    'groups': len(groups),
    'min_runs': min_runs,
    'warn_percent': warn_pct,
    'critical_percent': critical_pct,
    'stale_success_days': stale_success_days,
    'warn_score': warn_score,
    'critical_score': critical_score,
    'critical_groups': len(critical_groups),
    'top_n': top_n,
    'filters': {
        'mainline_branch_match': mainline_branch_match_raw,
        'workflow_match': workflow_match_raw or None,
        'workflow_exclude': workflow_exclude_raw or None,
        'event_match': event_match_raw or None,
        'event_exclude': event_exclude_raw or None,
        'repo_match': repo_match_raw or None,
        'repo_exclude': repo_exclude_raw or None,
        'head_sha_match': head_sha_match_raw or None,
        'head_sha_exclude': head_sha_exclude_raw or None,
        'conclusion_match': conclusion_match_raw or None,
        'conclusion_exclude': conclusion_exclude_raw or None,
        'run_id_match': run_id_match_raw or None,
        'run_id_exclude': run_id_exclude_raw or None,
        'run_url_match': run_url_match_raw or None,
        'run_url_exclude': run_url_exclude_raw or None,
    },
}

if output_format == 'json':
    print(json.dumps({'summary': summary, 'groups': groups[:top_n], 'all_groups': groups, 'critical_groups': critical_groups}, indent=2, sort_keys=True))
else:
    print('GITHUB ACTIONS MAINLINE HEALTH AUDIT')
    print('---')
    print(
        'SUMMARY: '
        f"files={summary['files_scanned']} runs={summary['runs_scanned']} runs_filtered={summary['runs_filtered']} "
        f"non_mainline_filtered={summary['non_mainline_filtered']} groups={summary['groups']} critical_groups={summary['critical_groups']}"
    )

    if parse_errors:
        print('PARSE_ERRORS:')
        for err in parse_errors:
            print(f'- {err}')

    active_filters = [
        f"mainline={mainline_branch_match_raw}",
        f"workflow={workflow_match_raw}" if workflow_match_raw else None,
        f"workflow!={workflow_exclude_raw}" if workflow_exclude_raw else None,
        f"event={event_match_raw}" if event_match_raw else None,
        f"event!={event_exclude_raw}" if event_exclude_raw else None,
        f"repo={repo_match_raw}" if repo_match_raw else None,
        f"repo!={repo_exclude_raw}" if repo_exclude_raw else None,
        f"sha={head_sha_match_raw}" if head_sha_match_raw else None,
        f"sha!={head_sha_exclude_raw}" if head_sha_exclude_raw else None,
        f"conclusion={conclusion_match_raw}" if conclusion_match_raw else None,
        f"conclusion!={conclusion_exclude_raw}" if conclusion_exclude_raw else None,
        f"run_id={run_id_match_raw}" if run_id_match_raw else None,
        f"run_id!={run_id_exclude_raw}" if run_id_exclude_raw else None,
        f"run_url={run_url_match_raw}" if run_url_match_raw else None,
        f"run_url!={run_url_exclude_raw}" if run_url_exclude_raw else None,
    ]
    active_filters = [f for f in active_filters if f]
    if active_filters:
        print('FILTERS: ' + ' '.join(active_filters))

    print('---')
    print(f"TOP MAINLINE RISK GROUPS ({min(top_n, len(groups))})")
    if not groups:
        print('none')
    else:
        for row in groups[:top_n]:
            print(
                f"- [{row['severity']}] {row['repository']} :: {row['workflow']} :: branch={row['branch']} event={row['event']} "
                f"health_score={row['health_score']} failure_rate={row['failure_rate_percent']}% "
                f"failed={row['failed_runs']}/{row['total_runs']} consecutive_failures={row['consecutive_failures']} "
                f"days_since_success={row['days_since_success']}"
            )

sys.exit(1 if (fail_on_critical and critical_groups) else 0)
PY
