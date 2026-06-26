#!/usr/bin/env bash
set -euo pipefail

RUN_GLOB="${RUN_GLOB:-artifacts/github-actions/*.json}"
TOP_N="${TOP_N:-20}"
OUTPUT_FORMAT="${OUTPUT_FORMAT:-text}"
MIN_RUNS_PER_BRANCH="${MIN_RUNS_PER_BRANCH:-2}"
MIN_BRANCHES="${MIN_BRANCHES:-2}"
BASELINE_BRANCH_MATCH="${BASELINE_BRANCH_MATCH:-^(main|master)$}"
WORKFLOW_MATCH="${WORKFLOW_MATCH:-}"
WORKFLOW_EXCLUDE="${WORKFLOW_EXCLUDE:-}"
REPO_MATCH="${REPO_MATCH:-}"
REPO_EXCLUDE="${REPO_EXCLUDE:-}"
FAILURE_DRIFT_WARN_PP="${FAILURE_DRIFT_WARN_PP:-10}"
FAILURE_DRIFT_CRITICAL_PP="${FAILURE_DRIFT_CRITICAL_PP:-25}"
RUNTIME_DRIFT_WARN_RATIO="${RUNTIME_DRIFT_WARN_RATIO:-1.25}"
RUNTIME_DRIFT_CRITICAL_RATIO="${RUNTIME_DRIFT_CRITICAL_RATIO:-1.6}"
FAIL_ON_CRITICAL="${FAIL_ON_CRITICAL:-0}"

if [[ "$OUTPUT_FORMAT" != "text" && "$OUTPUT_FORMAT" != "json" ]]; then
  echo "ERROR: OUTPUT_FORMAT must be 'text' or 'json' (got: $OUTPUT_FORMAT)" >&2
  exit 1
fi

for value_name in TOP_N MIN_RUNS_PER_BRANCH MIN_BRANCHES; do
  value="${!value_name}"
  if ! [[ "$value" =~ ^[0-9]+$ ]] || [[ "$value" -eq 0 ]]; then
    echo "ERROR: $value_name must be a positive integer (got: $value)" >&2
    exit 1
  fi
done

for value_name in FAILURE_DRIFT_WARN_PP FAILURE_DRIFT_CRITICAL_PP RUNTIME_DRIFT_WARN_RATIO RUNTIME_DRIFT_CRITICAL_RATIO; do
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

python3 - "$RUN_GLOB" "$TOP_N" "$OUTPUT_FORMAT" "$MIN_RUNS_PER_BRANCH" "$MIN_BRANCHES" "$BASELINE_BRANCH_MATCH" "$WORKFLOW_MATCH" "$WORKFLOW_EXCLUDE" "$REPO_MATCH" "$REPO_EXCLUDE" "$FAILURE_DRIFT_WARN_PP" "$FAILURE_DRIFT_CRITICAL_PP" "$RUNTIME_DRIFT_WARN_RATIO" "$RUNTIME_DRIFT_CRITICAL_RATIO" "$FAIL_ON_CRITICAL" <<'PY'
import glob
import json
import re
import sys
from collections import defaultdict
from datetime import datetime

run_glob = sys.argv[1]
top_n = int(sys.argv[2])
output_format = sys.argv[3]
min_runs_per_branch = int(sys.argv[4])
min_branches = int(sys.argv[5])
baseline_branch_match_raw = sys.argv[6]
workflow_match_raw = sys.argv[7]
workflow_exclude_raw = sys.argv[8]
repo_match_raw = sys.argv[9]
repo_exclude_raw = sys.argv[10]
warn_drift_pp = float(sys.argv[11])
critical_drift_pp = float(sys.argv[12])
warn_runtime_ratio = float(sys.argv[13])
critical_runtime_ratio = float(sys.argv[14])
fail_on_critical = sys.argv[15] == '1'

if critical_drift_pp < warn_drift_pp:
    print('ERROR: FAILURE_DRIFT_CRITICAL_PP must be >= FAILURE_DRIFT_WARN_PP', file=sys.stderr)
    sys.exit(1)
if critical_runtime_ratio < warn_runtime_ratio:
    print('ERROR: RUNTIME_DRIFT_CRITICAL_RATIO must be >= RUNTIME_DRIFT_WARN_RATIO', file=sys.stderr)
    sys.exit(1)


def compile_regex(pattern, label, required=False):
    if not pattern and not required:
        return None
    if required and not pattern:
        print(f'ERROR: {label} is required', file=sys.stderr)
        sys.exit(1)
    try:
        return re.compile(pattern)
    except re.error as exc:
        print(f'ERROR: invalid {label} regex {pattern!r}: {exc}', file=sys.stderr)
        sys.exit(1)


baseline_branch_match = compile_regex(baseline_branch_match_raw, 'BASELINE_BRANCH_MATCH', required=True)
workflow_match = compile_regex(workflow_match_raw, 'WORKFLOW_MATCH')
workflow_exclude = compile_regex(workflow_exclude_raw, 'WORKFLOW_EXCLUDE')
repo_match = compile_regex(repo_match_raw, 'REPO_MATCH')
repo_exclude = compile_regex(repo_exclude_raw, 'REPO_EXCLUDE')

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

agg = defaultdict(lambda: {
    'repository': None,
    'workflow': None,
    'branches': defaultdict(lambda: {
        'runs': 0,
        'failed': 0,
        'success': 0,
        'runtime_seconds': [],
        'sample_urls': [],
    }),
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
    repository = normalize_repo(payload.get('repository'))

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

    branch = payload.get('headBranch') or '<unknown-branch>'
    conclusion = (payload.get('conclusion') or payload.get('status') or 'unknown').lower()
    started_at = parse_ts(payload.get('runStartedAt') or payload.get('startedAt') or payload.get('createdAt'))
    ended_at = parse_ts(payload.get('updatedAt') or payload.get('completedAt'))
    runtime_seconds = None
    if started_at and ended_at:
        diff = (ended_at - started_at).total_seconds()
        if diff >= 0:
            runtime_seconds = diff

    key = (repository, workflow)
    bucket = agg[key]
    bucket['repository'] = repository
    bucket['workflow'] = workflow

    branch_bucket = bucket['branches'][branch]
    branch_bucket['runs'] += 1
    if conclusion in failure_outcomes:
        branch_bucket['failed'] += 1
    if conclusion == 'success':
        branch_bucket['success'] += 1
    if runtime_seconds is not None:
        branch_bucket['runtime_seconds'].append(runtime_seconds)

    run_url = payload.get('url')
    if run_url and len(branch_bucket['sample_urls']) < 2 and run_url not in branch_bucket['sample_urls']:
        branch_bucket['sample_urls'].append(run_url)

rows = []
critical_rows = []
insufficient_baseline = 0
insufficient_branches = 0

for bucket in agg.values():
    branch_stats = []
    for branch, stats in bucket['branches'].items():
        if stats['runs'] < min_runs_per_branch:
            continue
        failure_rate = (stats['failed'] / stats['runs']) * 100.0 if stats['runs'] else 0.0
        avg_runtime = (sum(stats['runtime_seconds']) / len(stats['runtime_seconds'])) if stats['runtime_seconds'] else None
        branch_stats.append({
            'branch': branch,
            'runs': stats['runs'],
            'failed': stats['failed'],
            'success': stats['success'],
            'failure_rate_percent': failure_rate,
            'avg_runtime_seconds': avg_runtime,
            'sample_urls': stats['sample_urls'],
        })

    if len(branch_stats) < min_branches:
        insufficient_branches += 1
        continue

    baseline_candidates = [s for s in branch_stats if baseline_branch_match.search(s['branch'])]
    if not baseline_candidates:
        insufficient_baseline += 1
        continue

    baseline = sorted(baseline_candidates, key=lambda s: (-s['runs'], s['branch']))[0]
    baseline_failure = baseline['failure_rate_percent']
    baseline_runtime = baseline['avg_runtime_seconds']

    for stat in branch_stats:
        if stat['branch'] == baseline['branch']:
            continue

        failure_drift_pp = stat['failure_rate_percent'] - baseline_failure

        runtime_ratio = None
        if baseline_runtime and baseline_runtime > 0 and stat['avg_runtime_seconds'] is not None:
            runtime_ratio = stat['avg_runtime_seconds'] / baseline_runtime

        severity = 'ok'
        if failure_drift_pp >= critical_drift_pp or (runtime_ratio is not None and runtime_ratio >= critical_runtime_ratio):
            severity = 'critical'
        elif failure_drift_pp >= warn_drift_pp or (runtime_ratio is not None and runtime_ratio >= warn_runtime_ratio):
            severity = 'warn'

        row = {
            'repository': bucket['repository'],
            'workflow': bucket['workflow'],
            'baseline_branch': baseline['branch'],
            'baseline_runs': baseline['runs'],
            'baseline_failure_rate_percent': round(baseline_failure, 3),
            'baseline_avg_runtime_seconds': round(baseline_runtime, 3) if baseline_runtime is not None else None,
            'branch': stat['branch'],
            'branch_runs': stat['runs'],
            'branch_failure_rate_percent': round(stat['failure_rate_percent'], 3),
            'branch_avg_runtime_seconds': round(stat['avg_runtime_seconds'], 3) if stat['avg_runtime_seconds'] is not None else None,
            'failure_drift_pp': round(failure_drift_pp, 3),
            'runtime_drift_ratio': round(runtime_ratio, 3) if runtime_ratio is not None else None,
            'severity': severity,
            'sample_urls': stat['sample_urls'],
        }
        rows.append(row)
        if severity == 'critical':
            critical_rows.append(row)

rows.sort(key=lambda r: (
    {'critical': 0, 'warn': 1, 'ok': 2}[r['severity']],
    -r['failure_drift_pp'],
    -(r['runtime_drift_ratio'] if r['runtime_drift_ratio'] is not None else 0),
    r['repository'],
    r['workflow'],
    r['branch'],
))

summary = {
    'files_scanned': len(files),
    'parse_errors': parse_errors,
    'runs_scanned': runs_scanned,
    'runs_filtered': runs_filtered,
    'rows': len(rows),
    'critical_rows': len(critical_rows),
    'insufficient_baseline_groups': insufficient_baseline,
    'insufficient_branch_groups': insufficient_branches,
    'min_runs_per_branch': min_runs_per_branch,
    'min_branches': min_branches,
    'top_n': top_n,
    'thresholds': {
        'failure_drift_warn_pp': warn_drift_pp,
        'failure_drift_critical_pp': critical_drift_pp,
        'runtime_drift_warn_ratio': warn_runtime_ratio,
        'runtime_drift_critical_ratio': critical_runtime_ratio,
    },
    'filters': {
        'baseline_branch_match': baseline_branch_match_raw,
        'workflow_match': workflow_match_raw or None,
        'workflow_exclude': workflow_exclude_raw or None,
        'repo_match': repo_match_raw or None,
        'repo_exclude': repo_exclude_raw or None,
    },
}

if output_format == 'json':
    print(json.dumps({'summary': summary, 'rows': rows[:top_n], 'all_rows': rows, 'critical_rows': critical_rows}, indent=2, sort_keys=True))
else:
    print('GITHUB ACTIONS BRANCH DRIFT AUDIT')
    print('---')
    print(
        'SUMMARY: '
        f"files={summary['files_scanned']} runs={summary['runs_scanned']} runs_filtered={summary['runs_filtered']} "
        f"rows={summary['rows']} critical_rows={summary['critical_rows']} "
        f"insufficient_baseline_groups={summary['insufficient_baseline_groups']} "
        f"insufficient_branch_groups={summary['insufficient_branch_groups']}"
    )

    if parse_errors:
        print('PARSE_ERRORS:')
        for err in parse_errors:
            print(f'- {err}')

    print('---')
    print(f"TOP BRANCH DRIFT ROWS ({min(top_n, len(rows))})")
    if not rows:
        print('none')
    else:
        for row in rows[:top_n]:
            print(
                f"- [{row['severity']}] {row['repository']} :: {row['workflow']} :: {row['branch']} vs {row['baseline_branch']} "
                f"failure_drift_pp={row['failure_drift_pp']} runtime_ratio={row['runtime_drift_ratio']} "
                f"branch_fail={row['branch_failure_rate_percent']}% baseline_fail={row['baseline_failure_rate_percent']}% "
                f"branch_runs={row['branch_runs']} baseline_runs={row['baseline_runs']}"
            )

sys.exit(1 if (fail_on_critical and critical_rows) else 0)
PY
