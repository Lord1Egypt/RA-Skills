#!/usr/bin/env bash
set -euo pipefail

RUN_GLOB="${RUN_GLOB:-artifacts/github-actions/*.json}"
TOP_N="${TOP_N:-20}"
OUTPUT_FORMAT="${OUTPUT_FORMAT:-text}"
WARN_WASTE_MINUTES="${WARN_WASTE_MINUTES:-20}"
CRITICAL_WASTE_MINUTES="${CRITICAL_WASTE_MINUTES:-60}"
FAIL_ON_CRITICAL="${FAIL_ON_CRITICAL:-0}"
WORKFLOW_MATCH="${WORKFLOW_MATCH:-}"
WORKFLOW_EXCLUDE="${WORKFLOW_EXCLUDE:-}"
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

if ! [[ "$WARN_WASTE_MINUTES" =~ ^[0-9]+([.][0-9]+)?$ ]] || ! [[ "$CRITICAL_WASTE_MINUTES" =~ ^[0-9]+([.][0-9]+)?$ ]]; then
  echo "ERROR: WARN_WASTE_MINUTES and CRITICAL_WASTE_MINUTES must be positive numbers" >&2
  exit 1
fi

if [[ "$FAIL_ON_CRITICAL" != "0" && "$FAIL_ON_CRITICAL" != "1" ]]; then
  echo "ERROR: FAIL_ON_CRITICAL must be 0 or 1 (got: $FAIL_ON_CRITICAL)" >&2
  exit 1
fi

python3 - "$RUN_GLOB" "$TOP_N" "$OUTPUT_FORMAT" "$WARN_WASTE_MINUTES" "$CRITICAL_WASTE_MINUTES" "$FAIL_ON_CRITICAL" "$WORKFLOW_MATCH" "$WORKFLOW_EXCLUDE" "$REPO_MATCH" "$REPO_EXCLUDE" "$BRANCH_MATCH" "$BRANCH_EXCLUDE" <<'PY'
import glob
import json
import re
import sys
from datetime import datetime

run_glob = sys.argv[1]
top_n = int(sys.argv[2])
output_format = sys.argv[3]
warn_waste_minutes = float(sys.argv[4])
critical_waste_minutes = float(sys.argv[5])
fail_on_critical = sys.argv[6] == '1'
workflow_match_raw = sys.argv[7]
workflow_exclude_raw = sys.argv[8]
repo_match_raw = sys.argv[9]
repo_exclude_raw = sys.argv[10]
branch_match_raw = sys.argv[11]
branch_exclude_raw = sys.argv[12]

if critical_waste_minutes < warn_waste_minutes:
    print('ERROR: CRITICAL_WASTE_MINUTES must be >= WARN_WASTE_MINUTES', file=sys.stderr)
    sys.exit(1)


def compile_optional_regex(pattern, label):
    if not pattern:
        return None
    try:
        return re.compile(pattern)
    except re.error as exc:
        print(f"ERROR: invalid {label} regex {pattern!r}: {exc}", file=sys.stderr)
        sys.exit(1)


def parse_ts(value):
    if not value:
        return None
    raw = str(value)
    if raw.endswith('Z'):
        raw = raw[:-1] + '+00:00'
    try:
        return datetime.fromisoformat(raw)
    except ValueError:
        return None


def extract_repo_name(repository):
    if isinstance(repository, str) and repository.strip():
        return repository.strip()
    if isinstance(repository, dict):
        return (
            repository.get('nameWithOwner')
            or repository.get('full_name')
            or repository.get('fullName')
            or repository.get('name')
            or '<unknown-repo>'
        )
    return '<unknown-repo>'


def estimate_minutes(payload):
    started = parse_ts(payload.get('createdAt') or payload.get('runStartedAt') or payload.get('startedAt'))
    completed = parse_ts(payload.get('updatedAt') or payload.get('completedAt'))

    if started and completed:
        return max(0.0, (completed - started).total_seconds() / 60.0)

    total = 0.0
    for job in payload.get('jobs') or []:
        if not isinstance(job, dict):
            continue
        job_started = parse_ts(job.get('startedAt') or job.get('started_at') or job.get('createdAt'))
        job_completed = parse_ts(job.get('completedAt') or job.get('completed_at'))
        if job_started and job_completed:
            total += max(0.0, (job_completed - job_started).total_seconds() / 60.0)

    return total


failure_conclusions = {'failure', 'cancelled', 'timed_out', 'action_required', 'startup_failure'}

workflow_match = compile_optional_regex(workflow_match_raw, 'WORKFLOW_MATCH')
workflow_exclude = compile_optional_regex(workflow_exclude_raw, 'WORKFLOW_EXCLUDE')
repo_match = compile_optional_regex(repo_match_raw, 'REPO_MATCH')
repo_exclude = compile_optional_regex(repo_exclude_raw, 'REPO_EXCLUDE')
branch_match = compile_optional_regex(branch_match_raw, 'BRANCH_MATCH')
branch_exclude = compile_optional_regex(branch_exclude_raw, 'BRANCH_EXCLUDE')

files = sorted(glob.glob(run_glob, recursive=True))
if not files:
    print(f"ERROR: no files matched RUN_GLOB={run_glob}", file=sys.stderr)
    sys.exit(1)

summary = {
    'files_scanned': len(files),
    'parse_errors': [],
    'runs_scanned': 0,
    'runs_filtered': 0,
    'groups_scanned': 0,
    'recoveries_found': 0,
    'recoveries_warn': 0,
    'recoveries_critical': 0,
    'wasted_minutes_total': 0.0,
}

groups = {}

for path in files:
    try:
        with open(path, 'r', encoding='utf-8') as fh:
            payload = json.load(fh)
    except Exception as exc:
        summary['parse_errors'].append(f"{path}: {exc}")
        continue

    summary['runs_scanned'] += 1

    repo = extract_repo_name(payload.get('repository'))
    workflow = payload.get('workflowName') or payload.get('name') or '<unknown-workflow>'
    branch = payload.get('headBranch') or '<unknown-branch>'
    sha = payload.get('headSha') or '<unknown-sha>'

    if repo_match and not repo_match.search(repo):
        summary['runs_filtered'] += 1
        continue
    if repo_exclude and repo_exclude.search(repo):
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

    created = parse_ts(payload.get('createdAt') or payload.get('runStartedAt') or payload.get('startedAt') or payload.get('updatedAt'))
    if not created:
        summary['runs_filtered'] += 1
        continue

    run = {
        'database_id': str(payload.get('databaseId') or payload.get('id') or path),
        'url': payload.get('url'),
        'conclusion': str(payload.get('conclusion') or '').lower(),
        'created': created,
        'minutes': round(estimate_minutes(payload), 3),
        'repo': repo,
        'workflow': workflow,
        'branch': branch,
        'sha': sha,
    }

    key = (repo, workflow, branch, sha)
    groups.setdefault(key, []).append(run)

rows = []
for (repo, workflow, branch, sha), attempts in groups.items():
    summary['groups_scanned'] += 1
    attempts.sort(key=lambda r: (r['created'], r['database_id']))

    first_success_index = next((idx for idx, run in enumerate(attempts) if run['conclusion'] == 'success'), None)
    if first_success_index is None:
        continue

    failure_attempts = [
        run for run in attempts[:first_success_index]
        if run['conclusion'] in failure_conclusions
    ]
    if not failure_attempts:
        continue

    wasted_minutes = round(sum(run['minutes'] for run in failure_attempts), 3)
    attempts_before_success = len(failure_attempts)

    if wasted_minutes >= critical_waste_minutes:
        severity = 'critical'
        summary['recoveries_critical'] += 1
    elif wasted_minutes >= warn_waste_minutes:
        severity = 'warn'
        summary['recoveries_warn'] += 1
    else:
        severity = 'ok'

    summary['recoveries_found'] += 1
    summary['wasted_minutes_total'] += wasted_minutes

    rows.append({
        'severity': severity,
        'repo': repo,
        'workflow': workflow,
        'branch': branch,
        'head_sha': sha,
        'attempts_before_success': attempts_before_success,
        'wasted_minutes_before_success': wasted_minutes,
        'first_success_run_id': attempts[first_success_index]['database_id'],
        'first_success_url': attempts[first_success_index]['url'],
        'failure_runs': [
            {
                'run_id': run['database_id'],
                'url': run['url'],
                'conclusion': run['conclusion'],
                'minutes': run['minutes'],
            }
            for run in failure_attempts[:5]
        ],
    })

summary['wasted_minutes_total'] = round(summary['wasted_minutes_total'], 3)
severity_rank = {'critical': 2, 'warn': 1, 'ok': 0}
rows.sort(
    key=lambda row: (
        -severity_rank[row['severity']],
        -row['wasted_minutes_before_success'],
        -row['attempts_before_success'],
        row['repo'],
        row['workflow'],
        row['branch'],
        row['head_sha'],
    )
)

critical_rows = [row for row in rows if row['severity'] == 'critical']

result = {
    'summary': {
        **summary,
        'recoveries_ranked': len(rows),
        'top_n': top_n,
        'warn_waste_minutes': warn_waste_minutes,
        'critical_waste_minutes': critical_waste_minutes,
        'filters': {
            'repo_match': repo_match_raw or None,
            'repo_exclude': repo_exclude_raw or None,
            'workflow_match': workflow_match_raw or None,
            'workflow_exclude': workflow_exclude_raw or None,
            'branch_match': branch_match_raw or None,
            'branch_exclude': branch_exclude_raw or None,
        },
    },
    'recoveries': rows[:top_n],
    'all_recoveries': rows,
    'critical_recoveries': critical_rows,
}

if output_format == 'json':
    print(json.dumps(result, indent=2, sort_keys=True))
else:
    print('GITHUB ACTIONS RETRY RECOVERY AUDIT')
    print('---')
    print(
        'SUMMARY: '
        f"files={summary['files_scanned']} runs={summary['runs_scanned']} runs_filtered={summary['runs_filtered']} "
        f"groups={summary['groups_scanned']} recoveries={summary['recoveries_found']} "
        f"warn={summary['recoveries_warn']} critical={summary['recoveries_critical']} "
        f"wasted_minutes_total={summary['wasted_minutes_total']}"
    )
    print(
        f"THRESHOLDS: warn_waste_minutes={warn_waste_minutes} critical_waste_minutes={critical_waste_minutes}"
    )

    if summary['parse_errors']:
        print('PARSE_ERRORS:')
        for err in summary['parse_errors']:
            print(f"- {err}")

    print('---')
    print(f"TOP RECOVERIES ({min(top_n, len(rows))})")
    if not rows:
        print('none')
    else:
        for row in rows[:top_n]:
            print(
                f"- [{row['severity']}] repo={row['repo']} workflow={row['workflow']} branch={row['branch']} "
                f"sha={row['head_sha']} failures_before_success={row['attempts_before_success']} "
                f"wasted_minutes={row['wasted_minutes_before_success']}"
            )

sys.exit(1 if (fail_on_critical and critical_rows) else 0)
PY
