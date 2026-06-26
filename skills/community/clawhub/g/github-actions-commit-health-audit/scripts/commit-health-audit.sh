#!/usr/bin/env bash
set -euo pipefail

RUN_GLOB="${RUN_GLOB:-artifacts/github-actions/*.json}"
TOP_N="${TOP_N:-20}"
OUTPUT_FORMAT="${OUTPUT_FORMAT:-text}"
MIN_RUNS="${MIN_RUNS:-2}"
BRANCH_MATCH="${BRANCH_MATCH:-}"
BRANCH_EXCLUDE="${BRANCH_EXCLUDE:-}"
WORKFLOW_MATCH="${WORKFLOW_MATCH:-}"
WORKFLOW_EXCLUDE="${WORKFLOW_EXCLUDE:-}"
REPO_MATCH="${REPO_MATCH:-}"
REPO_EXCLUDE="${REPO_EXCLUDE:-}"
SHA_MATCH="${SHA_MATCH:-}"
SHA_EXCLUDE="${SHA_EXCLUDE:-}"
FAIL_WARN_PERCENT="${FAIL_WARN_PERCENT:-25}"
FAIL_CRITICAL_PERCENT="${FAIL_CRITICAL_PERCENT:-50}"
WARN_SCORE="${WARN_SCORE:-35}"
CRITICAL_SCORE="${CRITICAL_SCORE:-60}"
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

for value_name in FAIL_WARN_PERCENT FAIL_CRITICAL_PERCENT WARN_SCORE CRITICAL_SCORE; do
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

python3 - "$RUN_GLOB" "$TOP_N" "$OUTPUT_FORMAT" "$MIN_RUNS" "$BRANCH_MATCH" "$BRANCH_EXCLUDE" "$WORKFLOW_MATCH" "$WORKFLOW_EXCLUDE" "$REPO_MATCH" "$REPO_EXCLUDE" "$SHA_MATCH" "$SHA_EXCLUDE" "$FAIL_WARN_PERCENT" "$FAIL_CRITICAL_PERCENT" "$WARN_SCORE" "$CRITICAL_SCORE" "$FAIL_ON_CRITICAL" <<'PY'
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
branch_match_raw = sys.argv[5]
branch_exclude_raw = sys.argv[6]
workflow_match_raw = sys.argv[7]
workflow_exclude_raw = sys.argv[8]
repo_match_raw = sys.argv[9]
repo_exclude_raw = sys.argv[10]
sha_match_raw = sys.argv[11]
sha_exclude_raw = sys.argv[12]
warn_pct = float(sys.argv[13])
critical_pct = float(sys.argv[14])
warn_score = float(sys.argv[15])
critical_score = float(sys.argv[16])
fail_on_critical = sys.argv[17] == '1'

if critical_pct < warn_pct:
    print('ERROR: FAIL_CRITICAL_PERCENT must be >= FAIL_WARN_PERCENT', file=sys.stderr)
    sys.exit(1)
if critical_score < warn_score:
    print('ERROR: CRITICAL_SCORE must be >= WARN_SCORE', file=sys.stderr)
    sys.exit(1)


def compile_regex(pattern, label):
    if not pattern:
        return None
    try:
        return re.compile(pattern)
    except re.error as exc:
        print(f'ERROR: invalid {label} regex {pattern!r}: {exc}', file=sys.stderr)
        sys.exit(1)


branch_match = compile_regex(branch_match_raw, 'BRANCH_MATCH')
branch_exclude = compile_regex(branch_exclude_raw, 'BRANCH_EXCLUDE')
workflow_match = compile_regex(workflow_match_raw, 'WORKFLOW_MATCH')
workflow_exclude = compile_regex(workflow_exclude_raw, 'WORKFLOW_EXCLUDE')
repo_match = compile_regex(repo_match_raw, 'REPO_MATCH')
repo_exclude = compile_regex(repo_exclude_raw, 'REPO_EXCLUDE')
sha_match = compile_regex(sha_match_raw, 'SHA_MATCH')
sha_exclude = compile_regex(sha_exclude_raw, 'SHA_EXCLUDE')


failure_outcomes = {'failure', 'cancelled', 'timed_out', 'startup_failure', 'stale', 'action_required'}

def parse_ts(value):
    if not value:
        return None
    text = str(value)
    if text.endswith('Z'):
        text = text[:-1] + '+00:00'
    try:
        return datetime.fromisoformat(text)
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
agg = defaultdict(lambda: {
    'repository': None,
    'sha': None,
    'runs': [],
    'branches': set(),
    'workflows': set(),
    'outcomes': defaultdict(int),
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

    repository = normalize_repo(payload.get('repository'))
    workflow = payload.get('workflowName') or payload.get('name') or '<unknown-workflow>'
    branch = payload.get('headBranch') or '<unknown-branch>'
    sha = payload.get('headSha') or '<unknown-sha>'

    if branch_match and not branch_match.search(branch):
        runs_filtered += 1
        continue
    if branch_exclude and branch_exclude.search(branch):
        runs_filtered += 1
        continue
    if workflow_match and not workflow_match.search(workflow):
        runs_filtered += 1
        continue
    if workflow_exclude and workflow_exclude.search(workflow):
        runs_filtered += 1
        continue
    if repo_match and not repo_match.search(repository):
        runs_filtered += 1
        continue
    if repo_exclude and repo_exclude.search(repository):
        runs_filtered += 1
        continue
    if sha_match and not sha_match.search(sha):
        runs_filtered += 1
        continue
    if sha_exclude and sha_exclude.search(sha):
        runs_filtered += 1
        continue

    conclusion = (payload.get('conclusion') or payload.get('status') or 'unknown').lower()
    created_at = parse_ts(payload.get('createdAt') or payload.get('runStartedAt') or payload.get('startedAt'))
    updated_at = parse_ts(payload.get('updatedAt') or payload.get('completedAt'))
    run_url = payload.get('url')

    key = (repository, sha)
    bucket = agg[key]
    bucket['repository'] = repository
    bucket['sha'] = sha
    bucket['branches'].add(branch)
    bucket['workflows'].add(workflow)
    bucket['outcomes'][conclusion] += 1
    bucket['runs'].append({'created_at': created_at, 'updated_at': updated_at, 'conclusion': conclusion})
    if run_url and len(bucket['sample_urls']) < 3 and run_url not in bucket['sample_urls']:
        bucket['sample_urls'].append(run_url)

now = datetime.now(timezone.utc)
groups = []
critical_groups = []

for bucket in agg.values():
    total_runs = sum(bucket['outcomes'].values())
    if total_runs < min_runs:
        continue

    failed_runs = sum(c for outcome, c in bucket['outcomes'].items() if outcome in failure_outcomes)
    success_runs = bucket['outcomes'].get('success', 0)
    failure_rate = (failed_runs / total_runs) * 100.0

    runs_with_time = [r for r in bucket['runs'] if r['created_at'] is not None]
    runs_with_time.sort(key=lambda item: item['created_at'])

    latest_run = runs_with_time[-1] if runs_with_time else None
    latest_run_failed = bool(latest_run and latest_run['conclusion'] in failure_outcomes)
    latest_failure_at = None
    latest_success_at = None
    for run in reversed(runs_with_time):
        if latest_failure_at is None and run['conclusion'] in failure_outcomes:
            latest_failure_at = run['created_at']
        if latest_success_at is None and run['conclusion'] == 'success':
            latest_success_at = run['created_at']
        if latest_failure_at and latest_success_at:
            break

    runtime_seconds = []
    for run in bucket['runs']:
        if run['created_at'] and run['updated_at']:
            diff = (run['updated_at'] - run['created_at']).total_seconds()
            if diff >= 0:
                runtime_seconds.append(diff)

    days_since_latest_failure = None
    if latest_failure_at is not None:
        days_since_latest_failure = (now - latest_failure_at).total_seconds() / 86400.0

    workflow_spread = len(bucket['workflows'])
    branch_spread = len(bucket['branches'])

    score = (
        failure_rate
        + (failed_runs * 6.0)
        + (workflow_spread * 4.0)
        + (branch_spread * 2.0)
        + (12.0 if latest_run_failed else 0.0)
    )
    score = round(score, 3)

    severity = 'ok'
    if failure_rate >= critical_pct or score >= critical_score:
        severity = 'critical'
    elif failure_rate >= warn_pct or score >= warn_score:
        severity = 'warn'

    row = {
        'repository': bucket['repository'],
        'head_sha': bucket['sha'],
        'total_runs': total_runs,
        'failed_runs': failed_runs,
        'success_runs': success_runs,
        'failure_rate_percent': round(failure_rate, 3),
        'workflow_spread': workflow_spread,
        'branch_spread': branch_spread,
        'latest_run_failed': latest_run_failed,
        'latest_failure_at': latest_failure_at.isoformat() if latest_failure_at else None,
        'latest_success_at': latest_success_at.isoformat() if latest_success_at else None,
        'days_since_latest_failure': round(days_since_latest_failure, 3) if days_since_latest_failure is not None else None,
        'avg_runtime_seconds': round((sum(runtime_seconds) / len(runtime_seconds)), 3) if runtime_seconds else None,
        'max_runtime_seconds': round(max(runtime_seconds), 3) if runtime_seconds else None,
        'commit_health_score': score,
        'severity': severity,
        'branches': sorted(bucket['branches']),
        'workflows': sorted(bucket['workflows']),
        'outcomes': dict(sorted(bucket['outcomes'].items())),
        'sample_urls': bucket['sample_urls'],
    }
    groups.append(row)
    if severity == 'critical':
        critical_groups.append(row)

groups.sort(key=lambda row: (-row['commit_health_score'], -row['failure_rate_percent'], -row['failed_runs'], row['repository'], row['head_sha']))

summary = {
    'files_scanned': len(files),
    'parse_errors': parse_errors,
    'runs_scanned': runs_scanned,
    'runs_filtered': runs_filtered,
    'groups': len(groups),
    'min_runs': min_runs,
    'warn_percent': warn_pct,
    'critical_percent': critical_pct,
    'warn_score': warn_score,
    'critical_score': critical_score,
    'critical_groups': len(critical_groups),
    'top_n': top_n,
    'filters': {
        'branch_match': branch_match_raw or None,
        'branch_exclude': branch_exclude_raw or None,
        'workflow_match': workflow_match_raw or None,
        'workflow_exclude': workflow_exclude_raw or None,
        'repo_match': repo_match_raw or None,
        'repo_exclude': repo_exclude_raw or None,
        'sha_match': sha_match_raw or None,
        'sha_exclude': sha_exclude_raw or None,
    },
}

if output_format == 'json':
    print(json.dumps({'summary': summary, 'groups': groups[:top_n], 'all_groups': groups, 'critical_groups': critical_groups}, indent=2, sort_keys=True))
else:
    print('GITHUB ACTIONS COMMIT HEALTH AUDIT')
    print('---')
    print(
        'SUMMARY: '
        f"files={summary['files_scanned']} runs={summary['runs_scanned']} runs_filtered={summary['runs_filtered']} "
        f"groups={summary['groups']} critical_groups={summary['critical_groups']}"
    )

    if parse_errors:
        print('PARSE_ERRORS:')
        for err in parse_errors:
            print(f'- {err}')

    active_filters = [
        f"branch={branch_match_raw}" if branch_match_raw else None,
        f"branch!={branch_exclude_raw}" if branch_exclude_raw else None,
        f"workflow={workflow_match_raw}" if workflow_match_raw else None,
        f"workflow!={workflow_exclude_raw}" if workflow_exclude_raw else None,
        f"repo={repo_match_raw}" if repo_match_raw else None,
        f"repo!={repo_exclude_raw}" if repo_exclude_raw else None,
        f"sha={sha_match_raw}" if sha_match_raw else None,
        f"sha!={sha_exclude_raw}" if sha_exclude_raw else None,
    ]
    active_filters = [f for f in active_filters if f]
    if active_filters:
        print('FILTERS: ' + ' '.join(active_filters))

    print('---')
    print(f"TOP COMMIT RISK GROUPS ({min(top_n, len(groups))})")
    if not groups:
        print('none')
    else:
        for row in groups[:top_n]:
            print(
                f"- [{row['severity']}] {row['repository']} :: sha={row['head_sha']} "
                f"commit_health_score={row['commit_health_score']} failure_rate={row['failure_rate_percent']}% "
                f"failed={row['failed_runs']}/{row['total_runs']} workflow_spread={row['workflow_spread']} "
                f"branch_spread={row['branch_spread']} latest_run_failed={row['latest_run_failed']}"
            )

sys.exit(1 if (fail_on_critical and critical_groups) else 0)
PY
