#!/usr/bin/env bash
set -euo pipefail

BASELINE_GLOB="${BASELINE_GLOB:-}"
CURRENT_GLOB="${CURRENT_GLOB:-}"
TOP_N="${TOP_N:-20}"
OUTPUT_FORMAT="${OUTPUT_FORMAT:-text}"
WARN_DELTA_SECONDS="${WARN_DELTA_SECONDS:-30}"
CRITICAL_DELTA_SECONDS="${CRITICAL_DELTA_SECONDS:-90}"
WARN_DELTA_PERCENT="${WARN_DELTA_PERCENT:-15}"
CRITICAL_DELTA_PERCENT="${CRITICAL_DELTA_PERCENT:-35}"
FAIL_ON_CRITICAL="${FAIL_ON_CRITICAL:-0}"
WORKFLOW_MATCH="${WORKFLOW_MATCH:-}"
WORKFLOW_EXCLUDE="${WORKFLOW_EXCLUDE:-}"
JOB_MATCH="${JOB_MATCH:-}"
JOB_EXCLUDE="${JOB_EXCLUDE:-}"
REPO_MATCH="${REPO_MATCH:-}"
REPO_EXCLUDE="${REPO_EXCLUDE:-}"

if [[ -z "$BASELINE_GLOB" ]]; then
  echo "ERROR: BASELINE_GLOB is required" >&2
  exit 1
fi

if [[ -z "$CURRENT_GLOB" ]]; then
  echo "ERROR: CURRENT_GLOB is required" >&2
  exit 1
fi

if [[ "$OUTPUT_FORMAT" != "text" && "$OUTPUT_FORMAT" != "json" ]]; then
  echo "ERROR: OUTPUT_FORMAT must be 'text' or 'json' (got: $OUTPUT_FORMAT)" >&2
  exit 1
fi

if ! [[ "$TOP_N" =~ ^[0-9]+$ ]] || [[ "$TOP_N" -eq 0 ]]; then
  echo "ERROR: TOP_N must be a positive integer (got: $TOP_N)" >&2
  exit 1
fi

for value in "$WARN_DELTA_SECONDS" "$CRITICAL_DELTA_SECONDS" "$WARN_DELTA_PERCENT" "$CRITICAL_DELTA_PERCENT"; do
  if ! [[ "$value" =~ ^[0-9]+$ ]]; then
    echo "ERROR: threshold values must be non-negative integers (got: $value)" >&2
    exit 1
  fi
done

if (( CRITICAL_DELTA_SECONDS < WARN_DELTA_SECONDS )); then
  echo "ERROR: CRITICAL_DELTA_SECONDS must be >= WARN_DELTA_SECONDS" >&2
  exit 1
fi

if (( CRITICAL_DELTA_PERCENT < WARN_DELTA_PERCENT )); then
  echo "ERROR: CRITICAL_DELTA_PERCENT must be >= WARN_DELTA_PERCENT" >&2
  exit 1
fi

if [[ "$FAIL_ON_CRITICAL" != "0" && "$FAIL_ON_CRITICAL" != "1" ]]; then
  echo "ERROR: FAIL_ON_CRITICAL must be 0 or 1 (got: $FAIL_ON_CRITICAL)" >&2
  exit 1
fi

python3 - "$BASELINE_GLOB" "$CURRENT_GLOB" "$TOP_N" "$OUTPUT_FORMAT" "$WARN_DELTA_SECONDS" "$CRITICAL_DELTA_SECONDS" "$WARN_DELTA_PERCENT" "$CRITICAL_DELTA_PERCENT" "$FAIL_ON_CRITICAL" "$WORKFLOW_MATCH" "$WORKFLOW_EXCLUDE" "$JOB_MATCH" "$JOB_EXCLUDE" "$REPO_MATCH" "$REPO_EXCLUDE" <<'PY'
import glob
import json
import re
import sys
from collections import defaultdict
from datetime import datetime

(
    baseline_glob,
    current_glob,
    top_n_raw,
    output_format,
    warn_delta_seconds_raw,
    critical_delta_seconds_raw,
    warn_delta_percent_raw,
    critical_delta_percent_raw,
    fail_on_critical_raw,
    workflow_match_raw,
    workflow_exclude_raw,
    job_match_raw,
    job_exclude_raw,
    repo_match_raw,
    repo_exclude_raw,
) = sys.argv[1:]

top_n = int(top_n_raw)
warn_delta_seconds = int(warn_delta_seconds_raw)
critical_delta_seconds = int(critical_delta_seconds_raw)
warn_delta_percent = int(warn_delta_percent_raw)
critical_delta_percent = int(critical_delta_percent_raw)
fail_on_critical = fail_on_critical_raw == '1'


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


def normalize_repo(raw_repository):
    if isinstance(raw_repository, str) and raw_repository.strip():
        return raw_repository.strip()
    if isinstance(raw_repository, dict):
        return (
            raw_repository.get('nameWithOwner')
            or raw_repository.get('full_name')
            or raw_repository.get('fullName')
            or raw_repository.get('name')
            or '<unknown-repo>'
        )
    return '<unknown-repo>'


def collect_runtime_samples(file_glob):
    files = sorted(glob.glob(file_glob, recursive=True))
    if not files:
        print(f"ERROR: no files matched glob={file_glob}", file=sys.stderr)
        sys.exit(1)

    parse_errors = []
    runs_scanned = 0
    runs_filtered = 0
    jobs_scanned = 0
    jobs_filtered = 0
    jobs_missing_timestamps = 0

    buckets = defaultdict(lambda: {
        'repository': None,
        'workflow': None,
        'job_name': None,
        'runtime_seconds': [],
        'run_ids': set(),
        'branches': set(),
    })

    for path in files:
        try:
            with open(path, 'r', encoding='utf-8') as fh:
                payload = json.load(fh)
        except Exception as exc:
            parse_errors.append(f"{path}: {exc}")
            continue

        runs_scanned += 1
        repository = normalize_repo(payload.get('repository'))
        workflow = payload.get('workflowName') or payload.get('name') or '<unknown-workflow>'
        run_id = str(payload.get('databaseId') or payload.get('id') or path)
        branch = payload.get('headBranch') or '<unknown-branch>'

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

            started_at = parse_ts(job.get('startedAt') or job.get('started_at'))
            completed_at = parse_ts(job.get('completedAt') or job.get('completed_at'))

            if not started_at or not completed_at:
                jobs_missing_timestamps += 1
                continue

            runtime_seconds = (completed_at - started_at).total_seconds()
            if runtime_seconds < 0:
                jobs_missing_timestamps += 1
                continue

            key = (repository, workflow, job_name)
            bucket = buckets[key]
            bucket['repository'] = repository
            bucket['workflow'] = workflow
            bucket['job_name'] = job_name
            bucket['runtime_seconds'].append(runtime_seconds)
            bucket['run_ids'].add(run_id)
            bucket['branches'].add(branch)

    return {
        'files_scanned': len(files),
        'parse_errors': parse_errors,
        'runs_scanned': runs_scanned,
        'runs_filtered': runs_filtered,
        'jobs_scanned': jobs_scanned,
        'jobs_filtered': jobs_filtered,
        'jobs_missing_timestamps': jobs_missing_timestamps,
        'buckets': buckets,
    }


def percentile(values, q):
    ordered = sorted(values)
    if not ordered:
        return 0.0
    if len(ordered) == 1:
        return float(ordered[0])
    index = int(round((len(ordered) - 1) * q))
    index = max(0, min(len(ordered) - 1, index))
    return float(ordered[index])


def summarize_bucket(bucket):
    runtimes = bucket['runtime_seconds']
    avg_runtime = sum(runtimes) / len(runtimes)
    return {
        'repository': bucket['repository'],
        'workflow': bucket['workflow'],
        'job_name': bucket['job_name'],
        'instances': len(runtimes),
        'run_count': len(bucket['run_ids']),
        'branches': sorted(bucket['branches']),
        'avg_runtime_seconds': round(avg_runtime, 3),
        'p95_runtime_seconds': round(percentile(runtimes, 0.95), 3),
    }


baseline = collect_runtime_samples(baseline_glob)
current = collect_runtime_samples(current_glob)

baseline_summary = {key: summarize_bucket(bucket) for key, bucket in baseline['buckets'].items()}
current_summary = {key: summarize_bucket(bucket) for key, bucket in current['buckets'].items()}

regressions = []
new_jobs = []
critical_regressions = []

for key, current_row in current_summary.items():
    baseline_row = baseline_summary.get(key)
    if not baseline_row:
        new_jobs.append(current_row)
        continue

    baseline_avg = baseline_row['avg_runtime_seconds']
    current_avg = current_row['avg_runtime_seconds']
    delta_seconds = current_avg - baseline_avg
    delta_percent = 0.0 if baseline_avg == 0 else (delta_seconds / baseline_avg) * 100.0

    severity = 'ok'
    if delta_seconds >= critical_delta_seconds and delta_percent >= critical_delta_percent:
        severity = 'critical'
    elif delta_seconds >= warn_delta_seconds and delta_percent >= warn_delta_percent:
        severity = 'warn'

    row = {
        'repository': current_row['repository'],
        'workflow': current_row['workflow'],
        'job_name': current_row['job_name'],
        'severity': severity,
        'baseline_instances': baseline_row['instances'],
        'current_instances': current_row['instances'],
        'baseline_avg_runtime_seconds': baseline_avg,
        'current_avg_runtime_seconds': current_avg,
        'baseline_p95_runtime_seconds': baseline_row['p95_runtime_seconds'],
        'current_p95_runtime_seconds': current_row['p95_runtime_seconds'],
        'delta_runtime_seconds': round(delta_seconds, 3),
        'delta_runtime_percent': round(delta_percent, 3),
        'current_branches': current_row['branches'],
    }
    regressions.append(row)

    if severity == 'critical':
        critical_regressions.append(row)

regressions.sort(
    key=lambda row: (
        -row['delta_runtime_seconds'],
        -row['delta_runtime_percent'],
        row['repository'],
        row['workflow'],
        row['job_name'],
    )
)
new_jobs.sort(key=lambda row: (row['repository'], row['workflow'], row['job_name']))

summary = {
    'baseline_files_scanned': baseline['files_scanned'],
    'current_files_scanned': current['files_scanned'],
    'baseline_runs_scanned': baseline['runs_scanned'],
    'current_runs_scanned': current['runs_scanned'],
    'baseline_runs_filtered': baseline['runs_filtered'],
    'current_runs_filtered': current['runs_filtered'],
    'baseline_jobs_scanned': baseline['jobs_scanned'],
    'current_jobs_scanned': current['jobs_scanned'],
    'baseline_jobs_filtered': baseline['jobs_filtered'],
    'current_jobs_filtered': current['jobs_filtered'],
    'baseline_jobs_missing_timestamps': baseline['jobs_missing_timestamps'],
    'current_jobs_missing_timestamps': current['jobs_missing_timestamps'],
    'baseline_groups': len(baseline_summary),
    'current_groups': len(current_summary),
    'regression_groups': len(regressions),
    'new_job_groups': len(new_jobs),
    'critical_regressions': len(critical_regressions),
    'thresholds': {
        'warn_delta_seconds': warn_delta_seconds,
        'critical_delta_seconds': critical_delta_seconds,
        'warn_delta_percent': warn_delta_percent,
        'critical_delta_percent': critical_delta_percent,
    },
    'filters': {
        'repo_match': repo_match_raw or None,
        'repo_exclude': repo_exclude_raw or None,
        'workflow_match': workflow_match_raw or None,
        'workflow_exclude': workflow_exclude_raw or None,
        'job_match': job_match_raw or None,
        'job_exclude': job_exclude_raw or None,
    },
    'parse_errors': baseline['parse_errors'] + current['parse_errors'],
}

if output_format == 'json':
    print(json.dumps({
        'summary': summary,
        'regressions': regressions[:top_n],
        'all_regressions': regressions,
        'new_jobs': new_jobs,
        'critical_regressions': critical_regressions,
    }, indent=2, sort_keys=True))
else:
    print('GITHUB ACTIONS RUNTIME REGRESSION AUDIT')
    print('---')
    print(
        'SUMMARY: '
        f"baseline_files={summary['baseline_files_scanned']} current_files={summary['current_files_scanned']} "
        f"baseline_runs={summary['baseline_runs_scanned']} current_runs={summary['current_runs_scanned']} "
        f"baseline_jobs={summary['baseline_jobs_scanned']} current_jobs={summary['current_jobs_scanned']} "
        f"regressions={summary['regression_groups']} new_jobs={summary['new_job_groups']} "
        f"critical_regressions={summary['critical_regressions']}"
    )

    if summary['parse_errors']:
        print('PARSE_ERRORS:')
        for err in summary['parse_errors']:
            print(f"- {err}")

    active_filters = [
        f"repo={repo_match_raw}" if repo_match_raw else None,
        f"repo!={repo_exclude_raw}" if repo_exclude_raw else None,
        f"workflow={workflow_match_raw}" if workflow_match_raw else None,
        f"workflow!={workflow_exclude_raw}" if workflow_exclude_raw else None,
        f"job={job_match_raw}" if job_match_raw else None,
        f"job!={job_exclude_raw}" if job_exclude_raw else None,
    ]
    active_filters = [item for item in active_filters if item]
    if active_filters:
        print('FILTERS: ' + ' '.join(active_filters))

    print('---')
    print(f"TOP RUNTIME REGRESSIONS ({min(top_n, len(regressions))})")
    if not regressions:
        print('none')
    else:
        for row in regressions[:top_n]:
            print(
                f"- [{row['severity']}] {row['repository']} :: {row['workflow']} :: {row['job_name']} "
                f"baseline_avg_s={row['baseline_avg_runtime_seconds']} current_avg_s={row['current_avg_runtime_seconds']} "
                f"delta_s={row['delta_runtime_seconds']} delta_pct={row['delta_runtime_percent']}"
            )

    print('---')
    print('NEW JOBS WITHOUT BASELINE')
    if not new_jobs:
        print('none')
    else:
        for row in new_jobs[:top_n]:
            print(
                f"- {row['repository']} :: {row['workflow']} :: {row['job_name']} "
                f"avg_runtime_s={row['avg_runtime_seconds']} instances={row['instances']}"
            )

exit_code = 1 if (fail_on_critical and critical_regressions) else 0
sys.exit(exit_code)
PY
