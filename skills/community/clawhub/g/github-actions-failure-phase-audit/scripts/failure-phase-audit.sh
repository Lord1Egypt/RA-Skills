#!/usr/bin/env bash
set -euo pipefail

RUN_GLOB="${RUN_GLOB:-artifacts/github-actions/*.json}"
TOP_N="${TOP_N:-20}"
OUTPUT_FORMAT="${OUTPUT_FORMAT:-text}"
WARN_MINUTES="${WARN_MINUTES:-20}"
CRITICAL_MINUTES="${CRITICAL_MINUTES:-45}"
FAIL_ON_CRITICAL="${FAIL_ON_CRITICAL:-0}"
WORKFLOW_MATCH="${WORKFLOW_MATCH:-}"
WORKFLOW_EXCLUDE="${WORKFLOW_EXCLUDE:-}"
REPO_MATCH="${REPO_MATCH:-}"
REPO_EXCLUDE="${REPO_EXCLUDE:-}"
BRANCH_MATCH="${BRANCH_MATCH:-}"
BRANCH_EXCLUDE="${BRANCH_EXCLUDE:-}"
PHASE_MATCH="${PHASE_MATCH:-}"
PHASE_EXCLUDE="${PHASE_EXCLUDE:-}"

if [[ "$OUTPUT_FORMAT" != "text" && "$OUTPUT_FORMAT" != "json" ]]; then
  echo "ERROR: OUTPUT_FORMAT must be 'text' or 'json' (got: $OUTPUT_FORMAT)" >&2
  exit 1
fi

if ! [[ "$TOP_N" =~ ^[0-9]+$ ]] || [[ "$TOP_N" -eq 0 ]]; then
  echo "ERROR: TOP_N must be a positive integer (got: $TOP_N)" >&2
  exit 1
fi

if ! [[ "$WARN_MINUTES" =~ ^[0-9]+([.][0-9]+)?$ ]] || ! [[ "$CRITICAL_MINUTES" =~ ^[0-9]+([.][0-9]+)?$ ]]; then
  echo "ERROR: WARN_MINUTES and CRITICAL_MINUTES must be numeric" >&2
  exit 1
fi

if [[ "$FAIL_ON_CRITICAL" != "0" && "$FAIL_ON_CRITICAL" != "1" ]]; then
  echo "ERROR: FAIL_ON_CRITICAL must be 0 or 1 (got: $FAIL_ON_CRITICAL)" >&2
  exit 1
fi

python3 - "$RUN_GLOB" "$TOP_N" "$OUTPUT_FORMAT" "$WARN_MINUTES" "$CRITICAL_MINUTES" "$FAIL_ON_CRITICAL" "$WORKFLOW_MATCH" "$WORKFLOW_EXCLUDE" "$REPO_MATCH" "$REPO_EXCLUDE" "$BRANCH_MATCH" "$BRANCH_EXCLUDE" "$PHASE_MATCH" "$PHASE_EXCLUDE" <<'PY'
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
repo_match_raw = sys.argv[9]
repo_exclude_raw = sys.argv[10]
branch_match_raw = sys.argv[11]
branch_exclude_raw = sys.argv[12]
phase_match_raw = sys.argv[13]
phase_exclude_raw = sys.argv[14]

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
repo_match = compile_optional_regex(repo_match_raw, 'REPO_MATCH')
repo_exclude = compile_optional_regex(repo_exclude_raw, 'REPO_EXCLUDE')
branch_match = compile_optional_regex(branch_match_raw, 'BRANCH_MATCH')
branch_exclude = compile_optional_regex(branch_exclude_raw, 'BRANCH_EXCLUDE')
phase_match = compile_optional_regex(phase_match_raw, 'PHASE_MATCH')
phase_exclude = compile_optional_regex(phase_exclude_raw, 'PHASE_EXCLUDE')

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


def classify_phase(step_name):
    text = (step_name or '').lower()
    phase_patterns = [
        ('setup', r'checkout|setup|install|dependency|cache|prepare|bootstrap'),
        ('build', r'build|compile|bundle|package|assemble'),
        ('test', r'test|pytest|jest|cypress|playwright|integration|unit|e2e'),
        ('lint', r'lint|eslint|ruff|format|prettier|typecheck|mypy|static'),
        ('deploy', r'deploy|release|publish|upload|docker\s+push|ship'),
        ('security', r'scan|security|sast|audit|trivy|codeql|vuln'),
    ]
    for phase, pattern in phase_patterns:
        if re.search(pattern, text):
            return phase
    return 'other'

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
    'jobs_failed': 0,
    'jobs_missing_timestamps': 0,
    'hotspots': 0,
    'warn_hotspots': 0,
    'critical_hotspots': 0,
    'failed_minutes_total': 0.0,
}

aggregates = defaultdict(lambda: {
    'failure_count': 0,
    'failed_minutes': 0.0,
    'run_ids': set(),
    'job_names': set(),
    'sample_urls': [],
    'conclusions': set(),
})

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
        conclusion = str(job.get('conclusion') or '').lower()
        if conclusion not in {'failure', 'cancelled', 'timed_out'}:
            continue

        summary['jobs_failed'] += 1
        job_name = job.get('name') or '<unnamed-job>'
        started_at = parse_ts(job.get('startedAt') or job.get('started_at') or job.get('createdAt') or job.get('created_at'))
        completed_at = parse_ts(job.get('completedAt') or job.get('completed_at'))
        if not started_at or not completed_at:
            summary['jobs_missing_timestamps'] += 1
            duration_minutes = 0.0
        else:
            duration_minutes = max(0.0, (completed_at - started_at).total_seconds() / 60.0)

        failed_step = '<unknown-step>'
        for step in (job.get('steps') or []):
            if not isinstance(step, dict):
                continue
            step_conclusion = str(step.get('conclusion') or '').lower()
            if step_conclusion and step_conclusion not in {'success', 'skipped', 'neutral'}:
                failed_step = step.get('name') or failed_step
                break

        phase = classify_phase(failed_step)
        if phase_match and not phase_match.search(phase):
            continue
        if phase_exclude and phase_exclude.search(phase):
            continue

        key = (repository, workflow, branch, phase, failed_step)
        row = aggregates[key]
        row['failure_count'] += 1
        row['failed_minutes'] += duration_minutes
        row['run_ids'].add(run_id)
        row['job_names'].add(job_name)
        row['conclusions'].add(conclusion)
        url = job.get('url') or payload.get('url')
        if url and len(row['sample_urls']) < 3:
            row['sample_urls'].append(url)

ranked = []
for (repository, workflow, branch, phase, failed_step), row in aggregates.items():
    failed_minutes = round(row['failed_minutes'], 3)
    summary['failed_minutes_total'] += failed_minutes
    severity = 'ok'
    if failed_minutes >= critical_minutes:
        severity = 'critical'
        summary['critical_hotspots'] += 1
    elif failed_minutes >= warn_minutes:
        severity = 'warn'
        summary['warn_hotspots'] += 1

    ranked.append({
        'repository': repository,
        'workflow': workflow,
        'branch': branch,
        'phase': phase,
        'failed_step': failed_step,
        'failure_count': row['failure_count'],
        'failed_minutes': failed_minutes,
        'run_count': len(row['run_ids']),
        'job_count': len(row['job_names']),
        'conclusions': sorted(row['conclusions']),
        'sample_urls': row['sample_urls'],
        'severity': severity,
    })

summary['hotspots'] = len(ranked)
summary['failed_minutes_total'] = round(summary['failed_minutes_total'], 3)

severity_rank = {'critical': 2, 'warn': 1, 'ok': 0}
ranked.sort(
    key=lambda row: (
        -severity_rank[row['severity']],
        -row['failed_minutes'],
        -row['failure_count'],
        row['repository'],
        row['workflow'],
        row['phase'],
        row['failed_step'],
    )
)

critical_hotspots = [row for row in ranked if row['severity'] == 'critical']

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
            'branch_match': branch_match_raw or None,
            'branch_exclude': branch_exclude_raw or None,
            'phase_match': phase_match_raw or None,
            'phase_exclude': phase_exclude_raw or None,
        },
    },
    'hotspots': ranked[:top_n],
    'all_hotspots': ranked,
    'critical_hotspots': critical_hotspots,
}

if output_format == 'json':
    print(json.dumps(result, indent=2, sort_keys=True))
else:
    print('GITHUB ACTIONS FAILURE PHASE AUDIT')
    print('---')
    print(
        'SUMMARY: '
        f"files={summary['files_scanned']} runs={summary['runs_scanned']} runs_filtered={summary['runs_filtered']} "
        f"jobs={summary['jobs_scanned']} jobs_failed={summary['jobs_failed']} hotspots={summary['hotspots']} "
        f"warn_hotspots={summary['warn_hotspots']} critical_hotspots={summary['critical_hotspots']} "
        f"failed_minutes_total={summary['failed_minutes_total']}"
    )
    print(f"THRESHOLDS: warn_minutes={warn_minutes} critical_minutes={critical_minutes}")

    if summary['parse_errors']:
        print('PARSE_ERRORS:')
        for err in summary['parse_errors']:
            print(f"- {err}")

    print('---')
    print(f"TOP FAILURE HOTSPOTS ({min(top_n, len(ranked))})")
    if not ranked:
        print('none')
    else:
        for row in ranked[:top_n]:
            print(
                f"- [{row['severity']}] {row['repository']} :: {row['workflow']} :: phase={row['phase']} "
                f"step={row['failed_step']} branch={row['branch']} failures={row['failure_count']} "
                f"failed_minutes={row['failed_minutes']} conclusions={','.join(row['conclusions']) or 'n/a'}"
            )

sys.exit(1 if (fail_on_critical and critical_hotspots) else 0)
PY
