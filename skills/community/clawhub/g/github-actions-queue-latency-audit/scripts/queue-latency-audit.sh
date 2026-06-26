#!/usr/bin/env bash
set -euo pipefail

RUN_GLOB="${RUN_GLOB:-artifacts/github-actions/*.json}"
TOP_N="${TOP_N:-20}"
OUTPUT_FORMAT="${OUTPUT_FORMAT:-text}"
QUEUE_WARN_SECONDS="${QUEUE_WARN_SECONDS:-120}"
QUEUE_CRITICAL_SECONDS="${QUEUE_CRITICAL_SECONDS:-300}"
FAIL_ON_CRITICAL="${FAIL_ON_CRITICAL:-0}"
WORKFLOW_MATCH="${WORKFLOW_MATCH:-}"
WORKFLOW_EXCLUDE="${WORKFLOW_EXCLUDE:-}"
JOB_MATCH="${JOB_MATCH:-}"
JOB_EXCLUDE="${JOB_EXCLUDE:-}"
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

if ! [[ "$QUEUE_WARN_SECONDS" =~ ^[0-9]+$ ]]; then
  echo "ERROR: QUEUE_WARN_SECONDS must be a non-negative integer (got: $QUEUE_WARN_SECONDS)" >&2
  exit 1
fi

if ! [[ "$QUEUE_CRITICAL_SECONDS" =~ ^[0-9]+$ ]]; then
  echo "ERROR: QUEUE_CRITICAL_SECONDS must be a non-negative integer (got: $QUEUE_CRITICAL_SECONDS)" >&2
  exit 1
fi

if (( QUEUE_CRITICAL_SECONDS < QUEUE_WARN_SECONDS )); then
  echo "ERROR: QUEUE_CRITICAL_SECONDS must be >= QUEUE_WARN_SECONDS" >&2
  exit 1
fi

if [[ "$FAIL_ON_CRITICAL" != "0" && "$FAIL_ON_CRITICAL" != "1" ]]; then
  echo "ERROR: FAIL_ON_CRITICAL must be 0 or 1 (got: $FAIL_ON_CRITICAL)" >&2
  exit 1
fi

python3 - "$RUN_GLOB" "$TOP_N" "$OUTPUT_FORMAT" "$QUEUE_WARN_SECONDS" "$QUEUE_CRITICAL_SECONDS" "$FAIL_ON_CRITICAL" "$WORKFLOW_MATCH" "$WORKFLOW_EXCLUDE" "$JOB_MATCH" "$JOB_EXCLUDE" "$REPO_MATCH" "$REPO_EXCLUDE" <<'PY'
import glob
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone

run_glob = sys.argv[1]
top_n = int(sys.argv[2])
output_format = sys.argv[3]
queue_warn = int(sys.argv[4])
queue_critical = int(sys.argv[5])
fail_on_critical = sys.argv[6] == '1'
workflow_match_raw = sys.argv[7]
workflow_exclude_raw = sys.argv[8]
job_match_raw = sys.argv[9]
job_exclude_raw = sys.argv[10]
repo_match_raw = sys.argv[11]
repo_exclude_raw = sys.argv[12]


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
job_match = compile_optional_regex(job_match_raw, 'JOB_MATCH')
job_exclude = compile_optional_regex(job_exclude_raw, 'JOB_EXCLUDE')
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
jobs_scanned = 0
jobs_filtered = 0
jobs_missing_timestamps = 0
jobs_with_queue = 0
critical_instances = []

agg = defaultdict(lambda: {
    'repository': None,
    'workflow': None,
    'job_name': None,
    'queue_seconds': [],
    'runtime_seconds': [],
    'total_seconds': [],
    'branches': set(),
    'run_ids': set(),
    'sample_urls': [],
})

for path in files:
    try:
        with open(path, 'r', encoding='utf-8') as fh:
            payload = json.load(fh)
    except Exception as exc:
        parse_errors.append(f"{path}: {exc}")
        continue

    runs_scanned += 1
    workflow = payload.get('workflowName') or payload.get('name') or '<unknown-workflow>'
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

    jobs = payload.get('jobs')
    if not isinstance(jobs, list):
        parse_errors.append(f"{path}: missing jobs[]")
        continue

    for job in jobs:
        if not isinstance(job, dict):
            continue

        jobs_scanned += 1
        job_name = job.get('name') or '<unnamed-job>'

        if job_match and not job_match.search(job_name):
            jobs_filtered += 1
            continue
        if job_exclude and job_exclude.search(job_name):
            jobs_filtered += 1
            continue

        created_at = parse_ts(job.get('createdAt') or job.get('created_at'))
        started_at = parse_ts(job.get('startedAt') or job.get('started_at'))
        completed_at = parse_ts(job.get('completedAt') or job.get('completed_at'))

        if not created_at or not started_at or not completed_at:
            jobs_missing_timestamps += 1
            continue

        queue_seconds = (started_at - created_at).total_seconds()
        runtime_seconds = (completed_at - started_at).total_seconds()
        total_seconds = (completed_at - created_at).total_seconds()

        if queue_seconds < 0 or runtime_seconds < 0 or total_seconds < 0:
            jobs_missing_timestamps += 1
            continue

        jobs_with_queue += 1

        key = (repository, workflow, job_name)
        bucket = agg[key]
        bucket['repository'] = repository
        bucket['workflow'] = workflow
        bucket['job_name'] = job_name
        bucket['queue_seconds'].append(queue_seconds)
        bucket['runtime_seconds'].append(runtime_seconds)
        bucket['total_seconds'].append(total_seconds)
        bucket['branches'].add(branch)
        bucket['run_ids'].add(run_id)
        job_url = job.get('url') or payload.get('url')
        if job_url and len(bucket['sample_urls']) < 3 and job_url not in bucket['sample_urls']:
            bucket['sample_urls'].append(job_url)

        if queue_seconds >= queue_critical:
            critical_instances.append({
                'repository': repository,
                'workflow': workflow,
                'job_name': job_name,
                'run_id': run_id,
                'branch': branch,
                'queue_seconds': round(queue_seconds, 3),
                'runtime_seconds': round(runtime_seconds, 3),
                'job_url': job_url,
            })


def pct(values, quantile):
    if not values:
        return 0.0
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    idx = int(round((len(ordered) - 1) * quantile))
    idx = max(0, min(len(ordered) - 1, idx))
    return ordered[idx]


groups = []
for item in agg.values():
    q_vals = item['queue_seconds']
    r_vals = item['runtime_seconds']
    t_vals = item['total_seconds']

    max_queue = max(q_vals)
    avg_queue = sum(q_vals) / len(q_vals)
    p95_queue = pct(q_vals, 0.95)

    severity = 'ok'
    if max_queue >= queue_critical:
        severity = 'critical'
    elif max_queue >= queue_warn:
        severity = 'warn'

    groups.append({
        'repository': item['repository'],
        'workflow': item['workflow'],
        'job_name': item['job_name'],
        'instances': len(q_vals),
        'run_count': len(item['run_ids']),
        'branches': sorted(item['branches']),
        'max_queue_seconds': round(max_queue, 3),
        'avg_queue_seconds': round(avg_queue, 3),
        'p95_queue_seconds': round(p95_queue, 3),
        'avg_runtime_seconds': round(sum(r_vals) / len(r_vals), 3),
        'avg_total_seconds': round(sum(t_vals) / len(t_vals), 3),
        'severity': severity,
        'sample_urls': item['sample_urls'],
    })

groups.sort(key=lambda row: (-row['max_queue_seconds'], -row['avg_queue_seconds'], row['repository'], row['workflow'], row['job_name']))

summary = {
    'files_scanned': len(files),
    'parse_errors': parse_errors,
    'runs_scanned': runs_scanned,
    'runs_filtered': runs_filtered,
    'jobs_scanned': jobs_scanned,
    'jobs_filtered': jobs_filtered,
    'jobs_missing_timestamps': jobs_missing_timestamps,
    'jobs_with_queue_metrics': jobs_with_queue,
    'queue_warn_seconds': queue_warn,
    'queue_critical_seconds': queue_critical,
    'critical_instances': len(critical_instances),
    'groups': len(groups),
    'top_n': top_n,
    'filters': {
        'repo_match': repo_match_raw or None,
        'repo_exclude': repo_exclude_raw or None,
        'workflow_match': workflow_match_raw or None,
        'workflow_exclude': workflow_exclude_raw or None,
        'job_match': job_match_raw or None,
        'job_exclude': job_exclude_raw or None,
    },
}

if output_format == 'json':
    print(json.dumps({'summary': summary, 'groups': groups[:top_n], 'all_groups': groups, 'critical_instances': critical_instances}, indent=2, sort_keys=True))
else:
    print('GITHUB ACTIONS QUEUE LATENCY AUDIT')
    print('---')
    print(
        'SUMMARY: '
        f"files={summary['files_scanned']} runs={summary['runs_scanned']} runs_filtered={summary['runs_filtered']} "
        f"jobs={summary['jobs_scanned']} jobs_filtered={summary['jobs_filtered']} "
        f"jobs_with_queue={summary['jobs_with_queue_metrics']} missing_timestamps={summary['jobs_missing_timestamps']} "
        f"critical_instances={summary['critical_instances']} groups={summary['groups']}"
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
        f"job={job_match_raw}" if job_match_raw else None,
        f"job!={job_exclude_raw}" if job_exclude_raw else None,
    ]
    active_filters = [f for f in active_filters if f]
    if active_filters:
        print('FILTERS: ' + ' '.join(active_filters))

    print('---')
    print(f"TOP QUEUE HOTSPOTS ({min(top_n, len(groups))})")
    if not groups:
        print('none')
    else:
        for row in groups[:top_n]:
            print(
                f"- [{row['severity']}] {row['repository']} :: {row['workflow']} :: {row['job_name']} "
                f"max_queue_s={row['max_queue_seconds']} avg_queue_s={row['avg_queue_seconds']} "
                f"p95_queue_s={row['p95_queue_seconds']} instances={row['instances']} runs={row['run_count']}"
            )

exit_code = 1 if (fail_on_critical and critical_instances) else 0
sys.exit(exit_code)
PY
