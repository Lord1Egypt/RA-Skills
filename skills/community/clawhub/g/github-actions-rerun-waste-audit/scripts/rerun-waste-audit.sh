#!/usr/bin/env bash
set -euo pipefail

RUN_GLOB="${RUN_GLOB:-artifacts/github-actions/*.json}"
TOP_N="${TOP_N:-20}"
OUTPUT_FORMAT="${OUTPUT_FORMAT:-text}"
WARN_MINUTES="${WARN_MINUTES:-10}"
CRITICAL_MINUTES="${CRITICAL_MINUTES:-30}"
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

if ! [[ "$WARN_MINUTES" =~ ^[0-9]+([.][0-9]+)?$ ]]; then
  echo "ERROR: WARN_MINUTES must be numeric (got: $WARN_MINUTES)" >&2
  exit 1
fi

if ! [[ "$CRITICAL_MINUTES" =~ ^[0-9]+([.][0-9]+)?$ ]]; then
  echo "ERROR: CRITICAL_MINUTES must be numeric (got: $CRITICAL_MINUTES)" >&2
  exit 1
fi

if [[ "$FAIL_ON_CRITICAL" != "0" && "$FAIL_ON_CRITICAL" != "1" ]]; then
  echo "ERROR: FAIL_ON_CRITICAL must be 0 or 1 (got: $FAIL_ON_CRITICAL)" >&2
  exit 1
fi

python3 - "$RUN_GLOB" "$TOP_N" "$OUTPUT_FORMAT" "$WARN_MINUTES" "$CRITICAL_MINUTES" "$FAIL_ON_CRITICAL" "$WORKFLOW_MATCH" "$WORKFLOW_EXCLUDE" "$JOB_MATCH" "$JOB_EXCLUDE" "$REPO_MATCH" "$REPO_EXCLUDE" "$BRANCH_MATCH" "$BRANCH_EXCLUDE" <<'PY'
import glob
import json
import re
import sys
from collections import defaultdict
from datetime import datetime

run_glob = sys.argv[1]
top_n = int(sys.argv[2])
output_format = sys.argv[3]
warn_minutes = float(sys.argv[4])
critical_minutes = float(sys.argv[5])
fail_on_critical = sys.argv[6] == '1'
workflow_match_raw = sys.argv[7]
workflow_exclude_raw = sys.argv[8]
job_match_raw = sys.argv[9]
job_exclude_raw = sys.argv[10]
repo_match_raw = sys.argv[11]
repo_exclude_raw = sys.argv[12]
branch_match_raw = sys.argv[13]
branch_exclude_raw = sys.argv[14]

if warn_minutes <= 0 or critical_minutes <= 0:
    print('ERROR: WARN_MINUTES and CRITICAL_MINUTES must be > 0', file=sys.stderr)
    sys.exit(1)
if critical_minutes < warn_minutes:
    print('ERROR: CRITICAL_MINUTES must be >= WARN_MINUTES', file=sys.stderr)
    sys.exit(1)

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
    'jobs_without_attempt': 0,
    'groups': 0,
    'groups_with_reruns': 0,
    'critical_groups': 0,
    'warn_groups': 0,
    'waste_minutes_total': 0.0,
}

attempt_groups = defaultdict(list)

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
    sha = payload.get('headSha') or payload.get('head_sha') or '<unknown-sha>'
    run_id = str(payload.get('databaseId') or payload.get('id') or path)
    run_attempt_raw = payload.get('runAttempt') or payload.get('run_attempt')

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

        duration_minutes = (completed_at - started_at).total_seconds() / 60.0
        if duration_minutes < 0:
            summary['jobs_missing_timestamps'] += 1
            continue

        attempt_raw = job.get('attempt')
        if attempt_raw is None:
            attempt_raw = run_attempt_raw

        try:
            attempt = int(attempt_raw) if attempt_raw is not None else None
        except (TypeError, ValueError):
            attempt = None

        if attempt is None:
            summary['jobs_without_attempt'] += 1
            attempt = 1

        attempt_groups[(repository, workflow, branch, sha, job_name)].append({
            'attempt': attempt,
            'duration_minutes': duration_minutes,
            'run_id': run_id,
            'conclusion': str(job.get('conclusion') or '').lower() or None,
            'job_url': job.get('url') or payload.get('url'),
        })

ranked_groups = []
critical_groups = []

for key, rows in attempt_groups.items():
    repository, workflow, branch, sha, job_name = key
    rows_sorted = sorted(rows, key=lambda item: (item['attempt'], item['run_id']))
    summary['groups'] += 1

    attempts_total = len(rows_sorted)
    if attempts_total <= 1:
        continue

    latest_attempt = max(item['attempt'] for item in rows_sorted)
    latest_rows = [item for item in rows_sorted if item['attempt'] == latest_attempt]
    previous_rows = [item for item in rows_sorted if item['attempt'] != latest_attempt]

    if not previous_rows:
        continue

    wasted_minutes = round(sum(item['duration_minutes'] for item in previous_rows), 3)
    summary['waste_minutes_total'] += wasted_minutes
    summary['groups_with_reruns'] += 1

    severity = 'ok'
    if wasted_minutes >= critical_minutes:
        severity = 'critical'
        summary['critical_groups'] += 1
    elif wasted_minutes >= warn_minutes:
        severity = 'warn'
        summary['warn_groups'] += 1

    row = {
        'repository': repository,
        'workflow': workflow,
        'branch': branch,
        'head_sha': sha,
        'job_name': job_name,
        'attempts_total': attempts_total,
        'latest_attempt': latest_attempt,
        'wasted_minutes': wasted_minutes,
        'latest_conclusions': sorted({item['conclusion'] for item in latest_rows if item['conclusion']}),
        'previous_conclusions': sorted({item['conclusion'] for item in previous_rows if item['conclusion']}),
        'latest_run_ids': sorted({item['run_id'] for item in latest_rows}),
        'previous_run_ids': sorted({item['run_id'] for item in previous_rows}),
        'sample_urls': [item['job_url'] for item in rows_sorted if item.get('job_url')][:3],
        'severity': severity,
    }

    ranked_groups.append(row)
    if severity == 'critical':
        critical_groups.append(row)

severity_rank = {'critical': 2, 'warn': 1, 'ok': 0}
ranked_groups.sort(
    key=lambda row: (
        -severity_rank[row['severity']],
        -row['wasted_minutes'],
        -row['attempts_total'],
        row['repository'],
        row['workflow'],
        row['job_name'],
    )
)

summary['waste_minutes_total'] = round(summary['waste_minutes_total'], 3)

result = {
    'summary': {
        **summary,
        'top_n': top_n,
        'warn_minutes': warn_minutes,
        'critical_minutes': critical_minutes,
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
    'critical_groups': critical_groups,
}

if output_format == 'json':
    print(json.dumps(result, indent=2, sort_keys=True))
else:
    print('GITHUB ACTIONS RERUN WASTE AUDIT')
    print('---')
    print(
        'SUMMARY: '
        f"files={summary['files_scanned']} runs={summary['runs_scanned']} runs_filtered={summary['runs_filtered']} "
        f"jobs={summary['jobs_scanned']} jobs_filtered={summary['jobs_filtered']} "
        f"groups={summary['groups']} groups_with_reruns={summary['groups_with_reruns']} "
        f"warn_groups={summary['warn_groups']} critical_groups={summary['critical_groups']} "
        f"waste_minutes_total={summary['waste_minutes_total']}"
    )
    print(f"THRESHOLDS: warn_minutes={warn_minutes} critical_minutes={critical_minutes}")

    if summary['parse_errors']:
        print('PARSE_ERRORS:')
        for err in summary['parse_errors']:
            print(f"- {err}")

    print('---')
    print(f"TOP RERUN WASTE GROUPS ({min(top_n, len(ranked_groups))})")
    if not ranked_groups:
        print('none')
    else:
        for row in ranked_groups[:top_n]:
            print(
                f"- [{row['severity']}] {row['repository']} :: {row['workflow']} :: {row['job_name']} "
                f"branch={row['branch']} attempts={row['attempts_total']} latest_attempt={row['latest_attempt']} "
                f"wasted_minutes={row['wasted_minutes']} latest={','.join(row['latest_conclusions']) or 'n/a'}"
            )

sys.exit(1 if (fail_on_critical and critical_groups) else 0)
PY
