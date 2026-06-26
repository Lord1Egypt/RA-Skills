#!/usr/bin/env bash
set -euo pipefail

RUN_GLOB="${RUN_GLOB:-artifacts/github-actions/*.json}"
TOP_N="${TOP_N:-20}"
OUTPUT_FORMAT="${OUTPUT_FORMAT:-text}"
JOB_TIMEOUT_SECONDS="${JOB_TIMEOUT_SECONDS:-3600}"
WARN_RATIO="${WARN_RATIO:-0.80}"
CRITICAL_RATIO="${CRITICAL_RATIO:-0.95}"
FAIL_ON_CRITICAL="${FAIL_ON_CRITICAL:-0}"
WORKFLOW_MATCH="${WORKFLOW_MATCH:-}"
WORKFLOW_EXCLUDE="${WORKFLOW_EXCLUDE:-}"
JOB_MATCH="${JOB_MATCH:-}"
JOB_EXCLUDE="${JOB_EXCLUDE:-}"
REPO_MATCH="${REPO_MATCH:-}"
REPO_EXCLUDE="${REPO_EXCLUDE:-}"
BRANCH_MATCH="${BRANCH_MATCH:-}"
BRANCH_EXCLUDE="${BRANCH_EXCLUDE:-}"

if [[ "$OUTPUT_FORMAT" != "text" && "$OUTPUT_FORMAT" != "json" ]]; then
  echo "ERROR: OUTPUT_FORMAT must be 'text' or 'json' (got: $OUTPUT_FORMAT)" >&2
  exit 1
fi

if ! [[ "$TOP_N" =~ ^[0-9]+$ ]] || [[ "$TOP_N" -eq 0 ]]; then
  echo "ERROR: TOP_N must be a positive integer (got: $TOP_N)" >&2
  exit 1
fi

if ! [[ "$JOB_TIMEOUT_SECONDS" =~ ^[0-9]+$ ]] || [[ "$JOB_TIMEOUT_SECONDS" -eq 0 ]]; then
  echo "ERROR: JOB_TIMEOUT_SECONDS must be a positive integer (got: $JOB_TIMEOUT_SECONDS)" >&2
  exit 1
fi

if [[ "$FAIL_ON_CRITICAL" != "0" && "$FAIL_ON_CRITICAL" != "1" ]]; then
  echo "ERROR: FAIL_ON_CRITICAL must be 0 or 1 (got: $FAIL_ON_CRITICAL)" >&2
  exit 1
fi

python3 - "$RUN_GLOB" "$TOP_N" "$OUTPUT_FORMAT" "$JOB_TIMEOUT_SECONDS" "$WARN_RATIO" "$CRITICAL_RATIO" "$FAIL_ON_CRITICAL" "$WORKFLOW_MATCH" "$WORKFLOW_EXCLUDE" "$JOB_MATCH" "$JOB_EXCLUDE" "$REPO_MATCH" "$REPO_EXCLUDE" "$BRANCH_MATCH" "$BRANCH_EXCLUDE" <<'PY'
import glob
import json
import re
import sys
from collections import defaultdict
from datetime import datetime

run_glob = sys.argv[1]
top_n = int(sys.argv[2])
output_format = sys.argv[3]
job_timeout_seconds = int(sys.argv[4])
warn_ratio_raw = sys.argv[5]
critical_ratio_raw = sys.argv[6]
fail_on_critical = sys.argv[7] == '1'
workflow_match_raw = sys.argv[8]
workflow_exclude_raw = sys.argv[9]
job_match_raw = sys.argv[10]
job_exclude_raw = sys.argv[11]
repo_match_raw = sys.argv[12]
repo_exclude_raw = sys.argv[13]
branch_match_raw = sys.argv[14]
branch_exclude_raw = sys.argv[15]


def parse_ratio(value, label):
    try:
        parsed = float(value)
    except ValueError:
        print(f"ERROR: {label} must be numeric (got {value!r})", file=sys.stderr)
        sys.exit(1)
    if parsed <= 0 or parsed > 1:
        print(f"ERROR: {label} must be > 0 and <= 1 (got {value!r})", file=sys.stderr)
        sys.exit(1)
    return parsed

warn_ratio = parse_ratio(warn_ratio_raw, 'WARN_RATIO')
critical_ratio = parse_ratio(critical_ratio_raw, 'CRITICAL_RATIO')
if critical_ratio < warn_ratio:
    print('ERROR: CRITICAL_RATIO must be >= WARN_RATIO', file=sys.stderr)
    sys.exit(1)

warn_threshold_seconds = job_timeout_seconds * warn_ratio
critical_threshold_seconds = job_timeout_seconds * critical_ratio


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
branch_match = compile_optional_regex(branch_match_raw, 'BRANCH_MATCH')
branch_exclude = compile_optional_regex(branch_exclude_raw, 'BRANCH_EXCLUDE')


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

summary = {
    'files_scanned': len(files),
    'parse_errors': [],
    'runs_scanned': 0,
    'runs_filtered': 0,
    'jobs_scanned': 0,
    'jobs_filtered': 0,
    'jobs_missing_timestamps': 0,
    'jobs_with_runtime': 0,
    'jobs_warn_or_critical': 0,
    'jobs_timed_out': 0,
    'groups': 0,
    'warn_threshold_seconds': round(warn_threshold_seconds, 3),
    'critical_threshold_seconds': round(critical_threshold_seconds, 3),
    'job_timeout_seconds': job_timeout_seconds,
}

groups = defaultdict(lambda: {
    'repository': None,
    'workflow': None,
    'job_name': None,
    'branch_samples': set(),
    'run_ids': set(),
    'sample_urls': [],
    'durations': [],
    'timed_out_count': 0,
    'critical_count': 0,
    'warn_count': 0,
})

critical_instances = []

for path in files:
    try:
        with open(path, 'r', encoding='utf-8') as fh:
            payload = json.load(fh)
    except Exception as exc:
        summary['parse_errors'].append(f"{path}: {exc}")
        continue

    summary['runs_scanned'] += 1

    workflow = payload.get('workflowName') or payload.get('name') or '<unknown-workflow>'
    branch = payload.get('headBranch') or '<unknown-branch>'
    run_id = str(payload.get('databaseId') or payload.get('id') or path)

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
        summary['runs_filtered'] += 1
        continue
    if repo_exclude and repo_exclude.search(repository):
        summary['runs_filtered'] += 1
        continue
    if workflow_match and not workflow_match.search(workflow):
        summary['runs_filtered'] += 1
        continue
    if workflow_exclude and workflow_exclude.search(workflow):
        summary['runs_filtered'] += 1
        continue
    if branch_match and not branch_match.search(branch):
        summary['runs_filtered'] += 1
        continue
    if branch_exclude and branch_exclude.search(branch):
        summary['runs_filtered'] += 1
        continue

    jobs = payload.get('jobs')
    if not isinstance(jobs, list):
        summary['parse_errors'].append(f"{path}: missing jobs[]")
        continue

    for job in jobs:
        if not isinstance(job, dict):
            continue

        summary['jobs_scanned'] += 1
        job_name = job.get('name') or '<unnamed-job>'

        if job_match and not job_match.search(job_name):
            summary['jobs_filtered'] += 1
            continue
        if job_exclude and job_exclude.search(job_name):
            summary['jobs_filtered'] += 1
            continue

        started_at = parse_ts(job.get('startedAt') or job.get('started_at'))
        completed_at = parse_ts(job.get('completedAt') or job.get('completed_at'))
        if not started_at or not completed_at:
            summary['jobs_missing_timestamps'] += 1
            continue

        duration_seconds = (completed_at - started_at).total_seconds()
        if duration_seconds < 0:
            summary['jobs_missing_timestamps'] += 1
            continue

        summary['jobs_with_runtime'] += 1

        conclusion = str(job.get('conclusion') or '').lower()
        timed_out = conclusion == 'timed_out'
        severity = 'ok'

        if timed_out:
            severity = 'critical'
        elif duration_seconds >= critical_threshold_seconds:
            severity = 'critical'
        elif duration_seconds >= warn_threshold_seconds:
            severity = 'warn'

        if severity in ('warn', 'critical'):
            summary['jobs_warn_or_critical'] += 1

        if timed_out:
            summary['jobs_timed_out'] += 1

        key = (repository, workflow, job_name)
        bucket = groups[key]
        bucket['repository'] = repository
        bucket['workflow'] = workflow
        bucket['job_name'] = job_name
        bucket['branch_samples'].add(branch)
        bucket['run_ids'].add(run_id)
        bucket['durations'].append(duration_seconds)
        if severity == 'warn':
            bucket['warn_count'] += 1
        if severity == 'critical':
            bucket['critical_count'] += 1
        if timed_out:
            bucket['timed_out_count'] += 1

        job_url = job.get('url') or payload.get('url')
        if job_url and len(bucket['sample_urls']) < 3 and job_url not in bucket['sample_urls']:
            bucket['sample_urls'].append(job_url)

        if severity == 'critical':
            critical_instances.append({
                'repository': repository,
                'workflow': workflow,
                'job_name': job_name,
                'run_id': run_id,
                'branch': branch,
                'duration_seconds': round(duration_seconds, 3),
                'timed_out': timed_out,
                'conclusion': conclusion or None,
                'job_url': job_url,
            })

ranked_groups = []
for bucket in groups.values():
    durations = bucket['durations']
    max_duration = max(durations)
    avg_duration = sum(durations) / len(durations)

    severity = 'ok'
    if bucket['critical_count'] > 0:
        severity = 'critical'
    elif bucket['warn_count'] > 0:
        severity = 'warn'

    ranked_groups.append({
        'repository': bucket['repository'],
        'workflow': bucket['workflow'],
        'job_name': bucket['job_name'],
        'instances': len(durations),
        'run_count': len(bucket['run_ids']),
        'branch_samples': sorted(bucket['branch_samples']),
        'max_duration_seconds': round(max_duration, 3),
        'avg_duration_seconds': round(avg_duration, 3),
        'warn_count': bucket['warn_count'],
        'critical_count': bucket['critical_count'],
        'timed_out_count': bucket['timed_out_count'],
        'severity': severity,
        'sample_urls': bucket['sample_urls'],
    })

severity_rank = {'critical': 2, 'warn': 1, 'ok': 0}
ranked_groups.sort(
    key=lambda row: (
        -severity_rank[row['severity']],
        -row['critical_count'],
        -row['max_duration_seconds'],
        row['repository'],
        row['workflow'],
        row['job_name'],
    )
)

summary['groups'] = len(ranked_groups)

result = {
    'summary': {
        **summary,
        'top_n': top_n,
        'filters': {
            'repo_match': repo_match_raw or None,
            'repo_exclude': repo_exclude_raw or None,
            'workflow_match': workflow_match_raw or None,
            'workflow_exclude': workflow_exclude_raw or None,
            'job_match': job_match_raw or None,
            'job_exclude': job_exclude_raw or None,
            'branch_match': branch_match_raw or None,
            'branch_exclude': branch_exclude_raw or None,
        },
    },
    'groups': ranked_groups[:top_n],
    'all_groups': ranked_groups,
    'critical_instances': critical_instances,
}

if output_format == 'json':
    print(json.dumps(result, indent=2, sort_keys=True))
else:
    print('GITHUB ACTIONS TIMEOUT RISK AUDIT')
    print('---')
    print(
        'SUMMARY: '
        f"files={summary['files_scanned']} runs={summary['runs_scanned']} runs_filtered={summary['runs_filtered']} "
        f"jobs={summary['jobs_scanned']} jobs_filtered={summary['jobs_filtered']} "
        f"jobs_with_runtime={summary['jobs_with_runtime']} warn_or_critical={summary['jobs_warn_or_critical']} "
        f"timed_out={summary['jobs_timed_out']} groups={summary['groups']}"
    )
    print(
        f"THRESHOLDS: timeout_s={job_timeout_seconds} warn_at_s={round(warn_threshold_seconds, 3)} critical_at_s={round(critical_threshold_seconds, 3)}"
    )

    if summary['parse_errors']:
        print('PARSE_ERRORS:')
        for err in summary['parse_errors']:
            print(f"- {err}")

    print('---')
    print(f"TOP TIMEOUT RISKS ({min(top_n, len(ranked_groups))})")
    if not ranked_groups:
        print('none')
    else:
        for row in ranked_groups[:top_n]:
            print(
                f"- [{row['severity']}] {row['repository']} :: {row['workflow']} :: {row['job_name']} "
                f"max_duration_s={row['max_duration_seconds']} avg_duration_s={row['avg_duration_seconds']} "
                f"critical={row['critical_count']} warn={row['warn_count']} timed_out={row['timed_out_count']} "
                f"instances={row['instances']}"
            )

sys.exit(1 if (fail_on_critical and critical_instances) else 0)
PY
