#!/usr/bin/env bash
set -euo pipefail

RUN_GLOB="${RUN_GLOB:-artifacts/github-actions/*.json}"
TOP_N="${TOP_N:-20}"
OUTPUT_FORMAT="${OUTPUT_FORMAT:-text}"
WARN_STREAK="${WARN_STREAK:-2}"
CRITICAL_STREAK="${CRITICAL_STREAK:-4}"
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

if ! [[ "$WARN_STREAK" =~ ^[0-9]+$ ]] || ! [[ "$CRITICAL_STREAK" =~ ^[0-9]+$ ]]; then
  echo "ERROR: WARN_STREAK and CRITICAL_STREAK must be positive integers" >&2
  exit 1
fi

if [[ "$WARN_STREAK" -eq 0 || "$CRITICAL_STREAK" -eq 0 ]]; then
  echo "ERROR: WARN_STREAK and CRITICAL_STREAK must be > 0" >&2
  exit 1
fi

if [[ "$CRITICAL_STREAK" -lt "$WARN_STREAK" ]]; then
  echo "ERROR: CRITICAL_STREAK must be >= WARN_STREAK" >&2
  exit 1
fi

if [[ "$FAIL_ON_CRITICAL" != "0" && "$FAIL_ON_CRITICAL" != "1" ]]; then
  echo "ERROR: FAIL_ON_CRITICAL must be 0 or 1 (got: $FAIL_ON_CRITICAL)" >&2
  exit 1
fi

python3 - "$RUN_GLOB" "$TOP_N" "$OUTPUT_FORMAT" "$WARN_STREAK" "$CRITICAL_STREAK" "$FAIL_ON_CRITICAL" "$WORKFLOW_MATCH" "$WORKFLOW_EXCLUDE" "$REPO_MATCH" "$REPO_EXCLUDE" "$BRANCH_MATCH" "$BRANCH_EXCLUDE" <<'PY'
import glob
import json
import re
import sys
from datetime import datetime

run_glob = sys.argv[1]
top_n = int(sys.argv[2])
output_format = sys.argv[3]
warn_streak = int(sys.argv[4])
critical_streak = int(sys.argv[5])
fail_on_critical = sys.argv[6] == '1'
workflow_match_raw = sys.argv[7]
workflow_exclude_raw = sys.argv[8]
repo_match_raw = sys.argv[9]
repo_exclude_raw = sys.argv[10]
branch_match_raw = sys.argv[11]
branch_exclude_raw = sys.argv[12]

failure_conclusions = {'failure', 'cancelled', 'timed_out'}
recovery_conclusions = {'success', 'neutral', 'skipped'}


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
    ts = str(value)
    if ts.endswith('Z'):
        ts = ts[:-1] + '+00:00'
    try:
        return datetime.fromisoformat(ts)
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
    'runs_considered': 0,
    'failure_runs': 0,
    'groups': 0,
    'streaks': 0,
    'warn_streaks': 0,
    'critical_streaks': 0,
    'failure_minutes_total': 0.0,
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

    conclusion = str(payload.get('conclusion') or '').lower()
    if not conclusion:
        jobs = payload.get('jobs')
        if isinstance(jobs, list):
            has_failure = any(str((job or {}).get('conclusion') or '').lower() in failure_conclusions for job in jobs if isinstance(job, dict))
            has_success = any(str((job or {}).get('conclusion') or '').lower() == 'success' for job in jobs if isinstance(job, dict))
            if has_failure:
                conclusion = 'failure'
            elif has_success:
                conclusion = 'success'

    if conclusion not in failure_conclusions and conclusion not in recovery_conclusions:
        summary['runs_filtered'] += 1
        continue

    repo = extract_repo_name(payload.get('repository'))
    workflow = payload.get('workflowName') or payload.get('name') or '<unknown-workflow>'
    branch = payload.get('headBranch') or '<unknown-branch>'

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

    run_id = str(payload.get('databaseId') or payload.get('id') or path)
    head_sha = payload.get('headSha') or payload.get('head_sha') or '<unknown-sha>'
    created_at = parse_ts(payload.get('createdAt') or payload.get('runStartedAt') or payload.get('startedAt'))
    updated_at = parse_ts(payload.get('updatedAt') or payload.get('completedAt'))
    minutes = round(estimate_minutes(payload), 3)

    summary['runs_considered'] += 1
    if conclusion in failure_conclusions:
        summary['failure_runs'] += 1
        summary['failure_minutes_total'] += minutes

    key = (repo, workflow, branch)
    groups.setdefault(key, []).append({
        'run_id': run_id,
        'conclusion': conclusion,
        'head_sha': head_sha,
        'created_at': created_at,
        'updated_at': updated_at,
        'minutes': minutes,
        'url': payload.get('url'),
    })

summary['failure_minutes_total'] = round(summary['failure_minutes_total'], 3)
summary['groups'] = len(groups)

streak_rows = []
for (repo, workflow, branch), runs in groups.items():
    runs.sort(key=lambda row: ((row['updated_at'] or row['created_at'] or datetime.min), row['run_id']))

    active = None
    for row in runs:
        is_failure = row['conclusion'] in failure_conclusions

        if is_failure:
            if active is None:
                active = {
                    'repo': repo,
                    'workflow': workflow,
                    'branch': branch,
                    'start_run_id': row['run_id'],
                    'end_run_id': row['run_id'],
                    'start_at': row['created_at'] or row['updated_at'],
                    'end_at': row['updated_at'] or row['created_at'],
                    'run_count': 1,
                    'minutes': row['minutes'],
                    'head_shas': {row['head_sha']},
                    'urls': [row['url']] if row['url'] else [],
                    'recovered': False,
                    'recovery_run_id': None,
                    'recovery_at': None,
                }
            else:
                active['end_run_id'] = row['run_id']
                active['end_at'] = row['updated_at'] or row['created_at'] or active['end_at']
                active['run_count'] += 1
                active['minutes'] += row['minutes']
                active['head_shas'].add(row['head_sha'])
                if row['url'] and len(active['urls']) < 3:
                    active['urls'].append(row['url'])
        else:
            if active is not None:
                active['recovered'] = True
                active['recovery_run_id'] = row['run_id']
                active['recovery_at'] = row['updated_at'] or row['created_at']
                streak_rows.append(active)
                active = None

    if active is not None:
        streak_rows.append(active)

summary['streaks'] = len(streak_rows)

for row in streak_rows:
    row['minutes'] = round(row['minutes'], 3)
    row['unique_shas'] = len(row.pop('head_shas'))
    row['duration_minutes'] = 0.0
    if row['start_at'] and row['end_at']:
        row['duration_minutes'] = round(max(0.0, (row['end_at'] - row['start_at']).total_seconds() / 60.0), 3)

    if row['run_count'] >= critical_streak:
        row['severity'] = 'critical'
        summary['critical_streaks'] += 1
    elif row['run_count'] >= warn_streak:
        row['severity'] = 'warn'
        summary['warn_streaks'] += 1
    else:
        row['severity'] = 'ok'

    for key in ('start_at', 'end_at', 'recovery_at'):
        row[key] = row[key].isoformat() if isinstance(row[key], datetime) else None

severity_rank = {'critical': 2, 'warn': 1, 'ok': 0}
streak_rows.sort(
    key=lambda row: (
        -severity_rank[row['severity']],
        -row['run_count'],
        -row['minutes'],
        row['repo'],
        row['workflow'],
        row['branch'],
        row['start_run_id'],
    )
)

critical_rows = [row for row in streak_rows if row['severity'] == 'critical']

result = {
    'summary': {
        **summary,
        'top_n': top_n,
        'warn_streak': warn_streak,
        'critical_streak': critical_streak,
        'filters': {
            'repo_match': repo_match_raw or None,
            'repo_exclude': repo_exclude_raw or None,
            'workflow_match': workflow_match_raw or None,
            'workflow_exclude': workflow_exclude_raw or None,
            'branch_match': branch_match_raw or None,
            'branch_exclude': branch_exclude_raw or None,
        },
    },
    'streaks': streak_rows[:top_n],
    'all_streaks': streak_rows,
    'critical_streaks': critical_rows,
}

if output_format == 'json':
    print(json.dumps(result, indent=2, sort_keys=True))
else:
    print('GITHUB ACTIONS FAILURE STREAK AUDIT')
    print('---')
    print(
        'SUMMARY: '
        f"files={summary['files_scanned']} runs={summary['runs_scanned']} runs_filtered={summary['runs_filtered']} "
        f"runs_considered={summary['runs_considered']} failure_runs={summary['failure_runs']} groups={summary['groups']} "
        f"streaks={summary['streaks']} warn_streaks={summary['warn_streaks']} critical_streaks={summary['critical_streaks']} "
        f"failure_minutes_total={summary['failure_minutes_total']}"
    )
    print(f"THRESHOLDS: warn_streak={warn_streak} critical_streak={critical_streak}")

    if summary['parse_errors']:
        print('PARSE_ERRORS:')
        for err in summary['parse_errors']:
            print(f"- {err}")

    print('---')
    print(f"TOP FAILURE STREAKS ({min(top_n, len(streak_rows))})")
    if not streak_rows:
        print('none')
    else:
        for row in streak_rows[:top_n]:
            status = 'open' if not row['recovered'] else f"recovered_by={row['recovery_run_id']}"
            print(
                f"- [{row['severity']}] {row['repo']} :: {row['workflow']} :: branch={row['branch']} "
                f"runs={row['run_count']} minutes={row['minutes']} unique_shas={row['unique_shas']} "
                f"start_run={row['start_run_id']} end_run={row['end_run_id']} {status}"
            )

sys.exit(1 if (fail_on_critical and critical_rows) else 0)
PY
