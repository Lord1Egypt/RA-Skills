#!/usr/bin/env bash
set -euo pipefail

RUN_GLOB="${RUN_GLOB:-artifacts/github-actions/*.json}"
TOP_N="${TOP_N:-20}"
OUTPUT_FORMAT="${OUTPUT_FORMAT:-text}"
MIN_OCCURRENCES="${MIN_OCCURRENCES:-3}"
WARN_FAILURE_RATE="${WARN_FAILURE_RATE:-0.20}"
CRITICAL_FAILURE_RATE="${CRITICAL_FAILURE_RATE:-0.40}"
FAIL_ON_CRITICAL="${FAIL_ON_CRITICAL:-0}"
REPO_MATCH="${REPO_MATCH:-}"
REPO_EXCLUDE="${REPO_EXCLUDE:-}"
WORKFLOW_MATCH="${WORKFLOW_MATCH:-}"
WORKFLOW_EXCLUDE="${WORKFLOW_EXCLUDE:-}"
JOB_MATCH="${JOB_MATCH:-}"
JOB_EXCLUDE="${JOB_EXCLUDE:-}"
STEP_MATCH="${STEP_MATCH:-}"
STEP_EXCLUDE="${STEP_EXCLUDE:-}"

if [[ "$OUTPUT_FORMAT" != "text" && "$OUTPUT_FORMAT" != "json" ]]; then
  echo "ERROR: OUTPUT_FORMAT must be 'text' or 'json' (got: $OUTPUT_FORMAT)" >&2
  exit 1
fi

if ! [[ "$TOP_N" =~ ^[0-9]+$ ]] || [[ "$TOP_N" -eq 0 ]]; then
  echo "ERROR: TOP_N must be a positive integer (got: $TOP_N)" >&2
  exit 1
fi

if ! [[ "$MIN_OCCURRENCES" =~ ^[0-9]+$ ]] || [[ "$MIN_OCCURRENCES" -eq 0 ]]; then
  echo "ERROR: MIN_OCCURRENCES must be a positive integer (got: $MIN_OCCURRENCES)" >&2
  exit 1
fi

if [[ "$FAIL_ON_CRITICAL" != "0" && "$FAIL_ON_CRITICAL" != "1" ]]; then
  echo "ERROR: FAIL_ON_CRITICAL must be 0 or 1 (got: $FAIL_ON_CRITICAL)" >&2
  exit 1
fi

python3 - "$RUN_GLOB" "$TOP_N" "$OUTPUT_FORMAT" "$MIN_OCCURRENCES" "$WARN_FAILURE_RATE" "$CRITICAL_FAILURE_RATE" "$FAIL_ON_CRITICAL" "$REPO_MATCH" "$REPO_EXCLUDE" "$WORKFLOW_MATCH" "$WORKFLOW_EXCLUDE" "$JOB_MATCH" "$JOB_EXCLUDE" "$STEP_MATCH" "$STEP_EXCLUDE" <<'PY'
import glob
import json
import re
import sys
from collections import defaultdict

(
    run_glob,
    top_n_raw,
    output_format,
    min_occurrences_raw,
    warn_failure_rate_raw,
    critical_failure_rate_raw,
    fail_on_critical_raw,
    repo_match_raw,
    repo_exclude_raw,
    workflow_match_raw,
    workflow_exclude_raw,
    job_match_raw,
    job_exclude_raw,
    step_match_raw,
    step_exclude_raw,
) = sys.argv[1:]

top_n = int(top_n_raw)
min_occurrences = int(min_occurrences_raw)
fail_on_critical = fail_on_critical_raw == '1'


def parse_rate(raw, label):
    try:
        value = float(raw)
    except ValueError:
        print(f"ERROR: {label} must be a decimal between 0 and 1 (got: {raw})", file=sys.stderr)
        sys.exit(1)
    if value < 0 or value > 1:
        print(f"ERROR: {label} must be between 0 and 1 (got: {value})", file=sys.stderr)
        sys.exit(1)
    return value


warn_failure_rate = parse_rate(warn_failure_rate_raw, 'WARN_FAILURE_RATE')
critical_failure_rate = parse_rate(critical_failure_rate_raw, 'CRITICAL_FAILURE_RATE')

if critical_failure_rate < warn_failure_rate:
    print('ERROR: CRITICAL_FAILURE_RATE must be >= WARN_FAILURE_RATE', file=sys.stderr)
    sys.exit(1)


def compile_regex(raw, label):
    if not raw:
        return None
    try:
        return re.compile(raw)
    except re.error as exc:
        print(f"ERROR: invalid {label} regex {raw!r}: {exc}", file=sys.stderr)
        sys.exit(1)


repo_match = compile_regex(repo_match_raw, 'REPO_MATCH')
repo_exclude = compile_regex(repo_exclude_raw, 'REPO_EXCLUDE')
workflow_match = compile_regex(workflow_match_raw, 'WORKFLOW_MATCH')
workflow_exclude = compile_regex(workflow_exclude_raw, 'WORKFLOW_EXCLUDE')
job_match = compile_regex(job_match_raw, 'JOB_MATCH')
job_exclude = compile_regex(job_exclude_raw, 'JOB_EXCLUDE')
step_match = compile_regex(step_match_raw, 'STEP_MATCH')
step_exclude = compile_regex(step_exclude_raw, 'STEP_EXCLUDE')

files = sorted(glob.glob(run_glob, recursive=True))
if not files:
    print(f"ERROR: no files matched RUN_GLOB={run_glob}", file=sys.stderr)
    sys.exit(1)

parse_errors = []
runs_scanned = 0
runs_filtered = 0
jobs_scanned = 0
jobs_filtered = 0
steps_scanned = 0
steps_filtered = 0
steps_missing_name = 0

failure_outcomes = {'failure', 'timed_out', 'cancelled', 'startup_failure', 'action_required', 'stale'}
skip_outcomes = {'skipped', 'neutral'}
success_outcomes = {'success'}

agg = defaultdict(lambda: {
    'repository': None,
    'workflow': None,
    'job_name': None,
    'step_name': None,
    'total': 0,
    'success': 0,
    'failed': 0,
    'skipped': 0,
    'other': 0,
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

        steps = job.get('steps')
        if not isinstance(steps, list):
            continue

        for step in steps:
            if not isinstance(step, dict):
                continue

            steps_scanned += 1
            step_name = (step.get('name') or '').strip()
            if not step_name:
                steps_missing_name += 1
                continue

            if step_match and not step_match.search(step_name):
                steps_filtered += 1
                continue
            if step_exclude and step_exclude.search(step_name):
                steps_filtered += 1
                continue

            conclusion = str(step.get('conclusion') or step.get('outcome') or 'unknown').strip().lower()

            key = (repository, workflow, job_name, step_name)
            bucket = agg[key]
            bucket['repository'] = repository
            bucket['workflow'] = workflow
            bucket['job_name'] = job_name
            bucket['step_name'] = step_name
            bucket['total'] += 1
            bucket['branches'].add(branch)
            bucket['run_ids'].add(run_id)
            sample_url = job.get('url') or payload.get('url')
            if sample_url and len(bucket['sample_urls']) < 3 and sample_url not in bucket['sample_urls']:
                bucket['sample_urls'].append(sample_url)

            if conclusion in success_outcomes:
                bucket['success'] += 1
            elif conclusion in failure_outcomes:
                bucket['failed'] += 1
            elif conclusion in skip_outcomes:
                bucket['skipped'] += 1
            else:
                bucket['other'] += 1


groups = []
critical_groups = []

for item in agg.values():
    observed = item['total']
    if observed < min_occurrences:
        continue

    evaluated = observed - item['skipped']
    if evaluated <= 0:
        continue

    failed = item['failed']
    success = item['success']
    is_flaky = failed > 0 and success > 0
    failure_rate = failed / evaluated

    severity = 'ok'
    if is_flaky:
        if failure_rate >= critical_failure_rate:
            severity = 'critical'
        elif failure_rate >= warn_failure_rate:
            severity = 'warn'

    row = {
        'repository': item['repository'],
        'workflow': item['workflow'],
        'job_name': item['job_name'],
        'step_name': item['step_name'],
        'severity': severity,
        'is_flaky': is_flaky,
        'occurrences': observed,
        'evaluated_occurrences': evaluated,
        'run_count': len(item['run_ids']),
        'success_count': success,
        'failure_count': failed,
        'skipped_count': item['skipped'],
        'other_count': item['other'],
        'failure_rate': round(failure_rate, 4),
        'branches': sorted(item['branches']),
        'sample_urls': item['sample_urls'],
    }
    groups.append(row)

    if severity == 'critical':
        critical_groups.append(row)

groups.sort(
    key=lambda row: (
        0 if row['severity'] == 'critical' else 1 if row['severity'] == 'warn' else 2,
        -row['failure_rate'],
        -row['failure_count'],
        -row['occurrences'],
        row['repository'],
        row['workflow'],
        row['job_name'],
        row['step_name'],
    )
)

summary = {
    'files_scanned': len(files),
    'parse_errors': parse_errors,
    'runs_scanned': runs_scanned,
    'runs_filtered': runs_filtered,
    'jobs_scanned': jobs_scanned,
    'jobs_filtered': jobs_filtered,
    'steps_scanned': steps_scanned,
    'steps_filtered': steps_filtered,
    'steps_missing_name': steps_missing_name,
    'groups_scored': len(groups),
    'flaky_groups': len([row for row in groups if row['is_flaky']]),
    'critical_groups': len(critical_groups),
    'warn_groups': len([row for row in groups if row['severity'] == 'warn']),
    'ok_groups': len([row for row in groups if row['severity'] == 'ok']),
    'min_occurrences': min_occurrences,
    'warn_failure_rate': warn_failure_rate,
    'critical_failure_rate': critical_failure_rate,
    'filters': {
        'repo_match': repo_match_raw or None,
        'repo_exclude': repo_exclude_raw or None,
        'workflow_match': workflow_match_raw or None,
        'workflow_exclude': workflow_exclude_raw or None,
        'job_match': job_match_raw or None,
        'job_exclude': job_exclude_raw or None,
        'step_match': step_match_raw or None,
        'step_exclude': step_exclude_raw or None,
    },
}

if output_format == 'json':
    print(json.dumps({'summary': summary, 'groups': groups[:top_n], 'all_groups': groups, 'critical_groups': critical_groups}, indent=2, sort_keys=True))
else:
    print('GITHUB ACTIONS STEP FLAKE AUDIT')
    print('---')
    print(
        'SUMMARY: '
        f"files={summary['files_scanned']} runs={summary['runs_scanned']} runs_filtered={summary['runs_filtered']} "
        f"jobs={summary['jobs_scanned']} jobs_filtered={summary['jobs_filtered']} "
        f"steps={summary['steps_scanned']} steps_filtered={summary['steps_filtered']} "
        f"groups={summary['groups_scored']} flaky={summary['flaky_groups']} "
        f"critical={summary['critical_groups']} warn={summary['warn_groups']} ok={summary['ok_groups']}"
    )
    if parse_errors:
        print('PARSE_ERRORS:')
        for err in parse_errors:
            print(f"- {err}")

    print('---')
    print(f"TOP STEP GROUPS ({min(top_n, len(groups))})")
    if not groups:
        print('none')
    else:
        for row in groups[:top_n]:
            print(
                f"- [{row['severity']}] {row['repository']} :: {row['workflow']} :: {row['job_name']} :: {row['step_name']} "
                f"flaky={row['is_flaky']} failure_rate={row['failure_rate']} "
                f"failures={row['failure_count']} successes={row['success_count']} "
                f"occurrences={row['occurrences']} runs={row['run_count']}"
            )

sys.exit(1 if (fail_on_critical and critical_groups) else 0)
PY
