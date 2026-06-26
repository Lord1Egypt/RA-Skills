#!/usr/bin/env bash
set -euo pipefail

RUN_GLOB="${RUN_GLOB:-artifacts/github-actions/*.json}"
TOP_N="${TOP_N:-20}"
OUTPUT_FORMAT="${OUTPUT_FORMAT:-text}"
FAIL_ON_FAILURES="${FAIL_ON_FAILURES:-0}"
MIN_OCCURRENCES="${MIN_OCCURRENCES:-1}"
WORKFLOW_MATCH="${WORKFLOW_MATCH:-}"
WORKFLOW_EXCLUDE="${WORKFLOW_EXCLUDE:-}"
JOB_MATCH="${JOB_MATCH:-}"
JOB_EXCLUDE="${JOB_EXCLUDE:-}"
AXIS_MATCH="${AXIS_MATCH:-}"
AXIS_EXCLUDE="${AXIS_EXCLUDE:-}"
BRANCH_MATCH="${BRANCH_MATCH:-}"
BRANCH_EXCLUDE="${BRANCH_EXCLUDE:-}"
CONCLUSION_MATCH="${CONCLUSION_MATCH:-}"
CONCLUSION_EXCLUDE="${CONCLUSION_EXCLUDE:-}"
FAILED_STEP_MATCH="${FAILED_STEP_MATCH:-}"
FAILED_STEP_EXCLUDE="${FAILED_STEP_EXCLUDE:-}"
RUN_ID_MATCH="${RUN_ID_MATCH:-}"
RUN_ID_EXCLUDE="${RUN_ID_EXCLUDE:-}"
RUN_URL_MATCH="${RUN_URL_MATCH:-}"
RUN_URL_EXCLUDE="${RUN_URL_EXCLUDE:-}"
HEAD_SHA_MATCH="${HEAD_SHA_MATCH:-}"
HEAD_SHA_EXCLUDE="${HEAD_SHA_EXCLUDE:-}"
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

if [[ "$FAIL_ON_FAILURES" != "0" && "$FAIL_ON_FAILURES" != "1" ]]; then
  echo "ERROR: FAIL_ON_FAILURES must be 0 or 1 (got: $FAIL_ON_FAILURES)" >&2
  exit 1
fi

if ! [[ "$MIN_OCCURRENCES" =~ ^[0-9]+$ ]] || [[ "$MIN_OCCURRENCES" -eq 0 ]]; then
  echo "ERROR: MIN_OCCURRENCES must be a positive integer (got: $MIN_OCCURRENCES)" >&2
  exit 1
fi

python3 - "$RUN_GLOB" "$TOP_N" "$OUTPUT_FORMAT" "$FAIL_ON_FAILURES" "$MIN_OCCURRENCES" "$WORKFLOW_MATCH" "$WORKFLOW_EXCLUDE" "$JOB_MATCH" "$JOB_EXCLUDE" "$AXIS_MATCH" "$AXIS_EXCLUDE" "$BRANCH_MATCH" "$BRANCH_EXCLUDE" "$CONCLUSION_MATCH" "$CONCLUSION_EXCLUDE" "$FAILED_STEP_MATCH" "$FAILED_STEP_EXCLUDE" "$RUN_ID_MATCH" "$RUN_ID_EXCLUDE" "$RUN_URL_MATCH" "$RUN_URL_EXCLUDE" "$HEAD_SHA_MATCH" "$HEAD_SHA_EXCLUDE" "$REPO_MATCH" "$REPO_EXCLUDE" <<'PY'
import glob
import json
import re
import sys
from collections import defaultdict
from datetime import datetime

run_glob = sys.argv[1]
top_n = int(sys.argv[2])
output_format = sys.argv[3]
fail_on_failures = sys.argv[4] == '1'
min_occurrences = int(sys.argv[5])
workflow_match_raw = sys.argv[6]
workflow_exclude_raw = sys.argv[7]
job_match_raw = sys.argv[8]
job_exclude_raw = sys.argv[9]
axis_match_raw = sys.argv[10]
axis_exclude_raw = sys.argv[11]
branch_match_raw = sys.argv[12]
branch_exclude_raw = sys.argv[13]
conclusion_match_raw = sys.argv[14]
conclusion_exclude_raw = sys.argv[15]
failed_step_match_raw = sys.argv[16]
failed_step_exclude_raw = sys.argv[17]
run_id_match_raw = sys.argv[18]
run_id_exclude_raw = sys.argv[19]
run_url_match_raw = sys.argv[20]
run_url_exclude_raw = sys.argv[21]
head_sha_match_raw = sys.argv[22]
head_sha_exclude_raw = sys.argv[23]
repo_match_raw = sys.argv[24]
repo_exclude_raw = sys.argv[25]


def compile_optional_regex(pattern, label):
    if not pattern:
        return None
    try:
        return re.compile(pattern)
    except re.error as exc:
        print(f'ERROR: invalid {label} regex {pattern!r}: {exc}', file=sys.stderr)
        sys.exit(1)


workflow_match = compile_optional_regex(workflow_match_raw, 'WORKFLOW_MATCH')
workflow_exclude = compile_optional_regex(workflow_exclude_raw, 'WORKFLOW_EXCLUDE')
job_match = compile_optional_regex(job_match_raw, 'JOB_MATCH')
job_exclude = compile_optional_regex(job_exclude_raw, 'JOB_EXCLUDE')
axis_match = compile_optional_regex(axis_match_raw, 'AXIS_MATCH')
axis_exclude = compile_optional_regex(axis_exclude_raw, 'AXIS_EXCLUDE')
branch_match = compile_optional_regex(branch_match_raw, 'BRANCH_MATCH')
branch_exclude = compile_optional_regex(branch_exclude_raw, 'BRANCH_EXCLUDE')
conclusion_match = compile_optional_regex(conclusion_match_raw, 'CONCLUSION_MATCH')
conclusion_exclude = compile_optional_regex(conclusion_exclude_raw, 'CONCLUSION_EXCLUDE')
failed_step_match = compile_optional_regex(failed_step_match_raw, 'FAILED_STEP_MATCH')
failed_step_exclude = compile_optional_regex(failed_step_exclude_raw, 'FAILED_STEP_EXCLUDE')
run_id_match = compile_optional_regex(run_id_match_raw, 'RUN_ID_MATCH')
run_id_exclude = compile_optional_regex(run_id_exclude_raw, 'RUN_ID_EXCLUDE')
run_url_match = compile_optional_regex(run_url_match_raw, 'RUN_URL_MATCH')
run_url_exclude = compile_optional_regex(run_url_exclude_raw, 'RUN_URL_EXCLUDE')
head_sha_match = compile_optional_regex(head_sha_match_raw, 'HEAD_SHA_MATCH')
head_sha_exclude = compile_optional_regex(head_sha_exclude_raw, 'HEAD_SHA_EXCLUDE')
repo_match = compile_optional_regex(repo_match_raw, 'REPO_MATCH')
repo_exclude = compile_optional_regex(repo_exclude_raw, 'REPO_EXCLUDE')

FAIL_LIKE = {
    'failure',
    'failed',
    'timed_out',
    'cancelled',
    'action_required',
    'startup_failure',
    'stale',
}


def parse_ts(ts):
    if not ts:
        return None
    # gh JSON timestamps are RFC3339 (`...Z`)
    if ts.endswith('Z'):
        ts = ts[:-1] + '+00:00'
    try:
        return datetime.fromisoformat(ts)
    except ValueError:
        return None


def parse_axis_tokens(name):
    name = (name or '').strip()

    paren = re.match(r'^(?P<base>.+?)\s*\((?P<axis>[^()]*)\)\s*$', name)
    if paren:
        base = paren.group('base').strip()
        axis = [p.strip() for p in paren.group('axis').split(',') if p.strip()]
        return base, axis

    bracket = re.match(r'^(?P<base>.+?)\s*\[(?P<axis>[^\[\]]*)\]\s*$', name)
    if bracket:
        base = bracket.group('base').strip()
        axis = [p.strip() for p in bracket.group('axis').split(',') if p.strip()]
        return base, axis

    if ' / ' in name:
        parts = [p.strip() for p in name.split(' / ') if p.strip()]
        if len(parts) > 1:
            return parts[0], parts[1:]

    return name, []


def normalize_axis(tokens):
    if not tokens:
        return '(no-axis)'
    return ' | '.join(tokens)


def last_failed_step(job):
    for step in reversed(job.get('steps') or []):
        conclusion = str(step.get('conclusion') or '').lower()
        if conclusion in FAIL_LIKE:
            return step.get('name') or '<unnamed-step>'
    return None


files = sorted(glob.glob(run_glob, recursive=True))
if not files:
    print(f'ERROR: no files matched RUN_GLOB={run_glob}', file=sys.stderr)
    sys.exit(1)

parse_errors = []
run_count = 0
job_rows = 0
failure_rows = 0
filtered_rows = 0
runs_filtered = 0

records = defaultdict(lambda: {
    'workflow': None,
    'job_name': None,
    'axis': None,
    'axis_tokens': None,
    'conclusions': defaultdict(int),
    'occurrences': 0,
    'runs': set(),
    'branches': set(),
    'failed_steps': defaultdict(int),
    'latest_failure_at': None,
    'sample_urls': [],
})

for path in files:
    try:
        with open(path, 'r', encoding='utf-8') as fh:
            payload = json.load(fh)
    except Exception as exc:
        parse_errors.append(f'{path}: {exc}')
        continue

    run_count += 1
    workflow = payload.get('workflowName') or payload.get('name') or '<unknown-workflow>'
    run_id = str(payload.get('databaseId') or payload.get('id') or path)
    branch = payload.get('headBranch') or '<unknown-branch>'
    run_head_sha = payload.get('headSha') or ''
    run_url = payload.get('url')
    repository = '<unknown-repo>'
    raw_repository = payload.get('repository')
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

    if run_id_match and not run_id_match.search(run_id):
        runs_filtered += 1
        continue
    if run_id_exclude and run_id_exclude.search(run_id):
        runs_filtered += 1
        continue
    if run_url_match and not run_url_match.search(run_url or ''):
        runs_filtered += 1
        continue
    if run_url_exclude and run_url_exclude.search(run_url or ''):
        runs_filtered += 1
        continue
    if head_sha_match and not head_sha_match.search(run_head_sha):
        runs_filtered += 1
        continue
    if head_sha_exclude and head_sha_exclude.search(run_head_sha):
        runs_filtered += 1
        continue

    jobs = payload.get('jobs')
    if not isinstance(jobs, list):
        parse_errors.append(f'{path}: missing jobs[]')
        continue

    for job in jobs:
        if not isinstance(job, dict):
            continue

        job_rows += 1
        conclusion = str(job.get('conclusion') or '').lower().strip() or 'unknown'
        if conclusion not in FAIL_LIKE:
            continue

        failure_rows += 1
        raw_name = job.get('name') or '<unnamed-job>'
        base_name, axis_tokens = parse_axis_tokens(raw_name)
        axis = normalize_axis(axis_tokens)

        if workflow_match and not workflow_match.search(workflow):
            filtered_rows += 1
            continue
        if workflow_exclude and workflow_exclude.search(workflow):
            filtered_rows += 1
            continue

        if branch_match and not branch_match.search(branch):
            filtered_rows += 1
            continue
        if branch_exclude and branch_exclude.search(branch):
            filtered_rows += 1
            continue

        if job_match and not job_match.search(base_name):
            filtered_rows += 1
            continue
        if job_exclude and job_exclude.search(base_name):
            filtered_rows += 1
            continue

        if axis_match and not axis_match.search(axis):
            filtered_rows += 1
            continue
        if axis_exclude and axis_exclude.search(axis):
            filtered_rows += 1
            continue

        if conclusion_match and not conclusion_match.search(conclusion):
            filtered_rows += 1
            continue
        if conclusion_exclude and conclusion_exclude.search(conclusion):
            filtered_rows += 1
            continue

        failed_step = last_failed_step(job)

        if failed_step_match and not failed_step_match.search(failed_step or ''):
            filtered_rows += 1
            continue
        if failed_step_exclude and failed_step_exclude.search(failed_step or ''):
            filtered_rows += 1
            continue

        failed_at = parse_ts(job.get('completedAt') or job.get('completed_at'))
        job_url = job.get('url') or run_url

        key = (repository, workflow, base_name, axis)
        bucket = records[key]
        bucket['repository'] = repository
        bucket['workflow'] = workflow
        bucket['job_name'] = base_name
        bucket['axis'] = axis
        bucket['axis_tokens'] = axis_tokens
        bucket['occurrences'] += 1
        bucket['conclusions'][conclusion] += 1
        bucket['runs'].add(run_id)
        bucket['branches'].add(branch)
        if failed_step:
            bucket['failed_steps'][failed_step] += 1

        if failed_at and (bucket['latest_failure_at'] is None or failed_at > bucket['latest_failure_at']):
            bucket['latest_failure_at'] = failed_at

        if job_url and len(bucket['sample_urls']) < 3 and job_url not in bucket['sample_urls']:
            bucket['sample_urls'].append(job_url)

failure_groups = []
for bucket in records.values():
    if bucket['occurrences'] < min_occurrences:
        continue

    top_failed_step = None
    if bucket['failed_steps']:
        top_failed_step = sorted(bucket['failed_steps'].items(), key=lambda kv: (-kv[1], kv[0]))[0][0]

    latest_failure_at = bucket['latest_failure_at']
    failure_groups.append({
        'repository': bucket['repository'],
        'workflow': bucket['workflow'],
        'job_name': bucket['job_name'],
        'axis': bucket['axis'],
        'axis_tokens': bucket['axis_tokens'],
        'occurrences': bucket['occurrences'],
        'run_count': len(bucket['runs']),
        'branches': sorted(bucket['branches']),
        'conclusions': dict(sorted(bucket['conclusions'].items())),
        'top_failed_step': top_failed_step,
        'sample_urls': bucket['sample_urls'],
        'latest_failure_at': latest_failure_at.isoformat() if latest_failure_at else None,
    })

failure_groups.sort(
    key=lambda r: (
        -r['occurrences'],
        -r['run_count'],
        r['repository'],
        r['workflow'],
        r['job_name'],
        r['axis'],
    )
)

summary = {
    'files_scanned': len(files),
    'parse_errors': parse_errors,
    'runs_scanned': run_count,
    'job_rows_scanned': job_rows,
    'failure_rows': failure_rows,
    'filtered_rows': filtered_rows,
    'runs_filtered': runs_filtered,
    'failure_groups': len(failure_groups),
    'min_occurrences': min_occurrences,
    'top_n': top_n,
    'filters': {
        'workflow_match': workflow_match_raw or None,
        'workflow_exclude': workflow_exclude_raw or None,
        'branch_match': branch_match_raw or None,
        'branch_exclude': branch_exclude_raw or None,
        'job_match': job_match_raw or None,
        'job_exclude': job_exclude_raw or None,
        'axis_match': axis_match_raw or None,
        'axis_exclude': axis_exclude_raw or None,
        'conclusion_match': conclusion_match_raw or None,
        'conclusion_exclude': conclusion_exclude_raw or None,
        'failed_step_match': failed_step_match_raw or None,
        'failed_step_exclude': failed_step_exclude_raw or None,
        'run_id_match': run_id_match_raw or None,
        'run_id_exclude': run_id_exclude_raw or None,
        'run_url_match': run_url_match_raw or None,
        'run_url_exclude': run_url_exclude_raw or None,
        'head_sha_match': head_sha_match_raw or None,
        'head_sha_exclude': head_sha_exclude_raw or None,
        'repo_match': repo_match_raw or None,
        'repo_exclude': repo_exclude_raw or None,
    },
}

if output_format == 'json':
    print(json.dumps({'summary': summary, 'groups': failure_groups[:top_n], 'all_groups': failure_groups}, indent=2, sort_keys=True))
else:
    print('GITHUB ACTIONS FAILURE MATRIX')
    print('---')
    print(
        'SUMMARY: '
        f"files={summary['files_scanned']} runs={summary['runs_scanned']} jobs={summary['job_rows_scanned']} "
        f"failure_rows={summary['failure_rows']} filtered_rows={summary['filtered_rows']} "
        f"runs_filtered={summary['runs_filtered']} "
        f"groups={summary['failure_groups']} min_occurrences={summary['min_occurrences']}"
    )

    if parse_errors:
        print('PARSE_ERRORS:')
        for err in parse_errors:
            print(f'- {err}')

    active_filters = [
        f"workflow={workflow_match_raw}" if workflow_match_raw else None,
        f"workflow!={workflow_exclude_raw}" if workflow_exclude_raw else None,
        f"branch={branch_match_raw}" if branch_match_raw else None,
        f"branch!={branch_exclude_raw}" if branch_exclude_raw else None,
        f"job={job_match_raw}" if job_match_raw else None,
        f"job!={job_exclude_raw}" if job_exclude_raw else None,
        f"axis={axis_match_raw}" if axis_match_raw else None,
        f"axis!={axis_exclude_raw}" if axis_exclude_raw else None,
        f"conclusion={conclusion_match_raw}" if conclusion_match_raw else None,
        f"conclusion!={conclusion_exclude_raw}" if conclusion_exclude_raw else None,
        f"failed_step={failed_step_match_raw}" if failed_step_match_raw else None,
        f"failed_step!={failed_step_exclude_raw}" if failed_step_exclude_raw else None,
        f"run_id={run_id_match_raw}" if run_id_match_raw else None,
        f"run_id!={run_id_exclude_raw}" if run_id_exclude_raw else None,
        f"run_url={run_url_match_raw}" if run_url_match_raw else None,
        f"run_url!={run_url_exclude_raw}" if run_url_exclude_raw else None,
        f"head_sha={head_sha_match_raw}" if head_sha_match_raw else None,
        f"head_sha!={head_sha_exclude_raw}" if head_sha_exclude_raw else None,
        f"repo={repo_match_raw}" if repo_match_raw else None,
        f"repo!={repo_exclude_raw}" if repo_exclude_raw else None,
    ]
    active_filters = [f for f in active_filters if f]
    if active_filters:
        print('FILTERS: ' + ' '.join(active_filters))

    print('---')
    print(f"TOP FAILURE GROUPS ({min(top_n, len(failure_groups))})")
    if not failure_groups:
        print('none')
    else:
        for row in failure_groups[:top_n]:
            conclusion_bits = ','.join(f"{k}:{v}" for k, v in sorted(row['conclusions'].items()))
            branches = ','.join(row['branches'])
            detail = (
                f"- {row['workflow']} :: {row['job_name']} :: {row['axis']} "
                f"repo={row['repository']} "
                f"occurrences={row['occurrences']} runs={row['run_count']} "
                f"conclusions={conclusion_bits} branches={branches}"
            )
            if row['top_failed_step']:
                detail += f" top_failed_step={row['top_failed_step']}"
            print(detail)

exit_code = 1 if (fail_on_failures and failure_groups) else 0
sys.exit(exit_code)
PY
