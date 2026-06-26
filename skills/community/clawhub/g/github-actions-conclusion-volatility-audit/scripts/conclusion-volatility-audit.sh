#!/usr/bin/env bash
set -euo pipefail

RUN_GLOB="${RUN_GLOB:-artifacts/github-actions/*.json}"
TOP_N="${TOP_N:-20}"
OUTPUT_FORMAT="${OUTPUT_FORMAT:-text}"
MIN_RUNS="${MIN_RUNS:-5}"
WARN_INSTABILITY_PCT="${WARN_INSTABILITY_PCT:-35}"
CRITICAL_INSTABILITY_PCT="${CRITICAL_INSTABILITY_PCT:-60}"
FAIL_ON_CRITICAL="${FAIL_ON_CRITICAL:-0}"
WORKFLOW_MATCH="${WORKFLOW_MATCH:-}"
WORKFLOW_EXCLUDE="${WORKFLOW_EXCLUDE:-}"
BRANCH_MATCH="${BRANCH_MATCH:-}"
BRANCH_EXCLUDE="${BRANCH_EXCLUDE:-}"
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

if ! [[ "$MIN_RUNS" =~ ^[0-9]+$ ]] || [[ "$MIN_RUNS" -eq 0 ]]; then
  echo "ERROR: MIN_RUNS must be a positive integer (got: $MIN_RUNS)" >&2
  exit 1
fi

if [[ "$FAIL_ON_CRITICAL" != "0" && "$FAIL_ON_CRITICAL" != "1" ]]; then
  echo "ERROR: FAIL_ON_CRITICAL must be 0 or 1 (got: $FAIL_ON_CRITICAL)" >&2
  exit 1
fi

python3 - "$RUN_GLOB" "$TOP_N" "$OUTPUT_FORMAT" "$MIN_RUNS" "$WARN_INSTABILITY_PCT" "$CRITICAL_INSTABILITY_PCT" "$FAIL_ON_CRITICAL" "$WORKFLOW_MATCH" "$WORKFLOW_EXCLUDE" "$BRANCH_MATCH" "$BRANCH_EXCLUDE" "$REPO_MATCH" "$REPO_EXCLUDE" <<'PY'
import glob
import json
import re
import sys
from collections import defaultdict
from datetime import datetime

run_glob = sys.argv[1]
top_n = int(sys.argv[2])
output_format = sys.argv[3]
min_runs = int(sys.argv[4])
warn_instability_raw = sys.argv[5]
critical_instability_raw = sys.argv[6]
fail_on_critical = sys.argv[7] == '1'
workflow_match_raw = sys.argv[8]
workflow_exclude_raw = sys.argv[9]
branch_match_raw = sys.argv[10]
branch_exclude_raw = sys.argv[11]
repo_match_raw = sys.argv[12]
repo_exclude_raw = sys.argv[13]


def parse_pct(value: str, label: str) -> float:
    try:
        parsed = float(value)
    except ValueError:
        print(f"ERROR: {label} must be numeric (got {value!r})", file=sys.stderr)
        sys.exit(1)
    if parsed < 0 or parsed > 100:
        print(f"ERROR: {label} must be between 0 and 100 (got {value!r})", file=sys.stderr)
        sys.exit(1)
    return parsed


warn_instability_pct = parse_pct(warn_instability_raw, 'WARN_INSTABILITY_PCT')
critical_instability_pct = parse_pct(critical_instability_raw, 'CRITICAL_INSTABILITY_PCT')
if critical_instability_pct < warn_instability_pct:
    print('ERROR: CRITICAL_INSTABILITY_PCT must be >= WARN_INSTABILITY_PCT', file=sys.stderr)
    sys.exit(1)


def compile_optional_regex(pattern: str, label: str):
    if not pattern:
        return None
    try:
        return re.compile(pattern)
    except re.error as exc:
        print(f"ERROR: invalid {label} regex {pattern!r}: {exc}", file=sys.stderr)
        sys.exit(1)


workflow_match = compile_optional_regex(workflow_match_raw, 'WORKFLOW_MATCH')
workflow_exclude = compile_optional_regex(workflow_exclude_raw, 'WORKFLOW_EXCLUDE')
branch_match = compile_optional_regex(branch_match_raw, 'BRANCH_MATCH')
branch_exclude = compile_optional_regex(branch_exclude_raw, 'BRANCH_EXCLUDE')
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


def normalize_conclusion(value):
    text = str(value or '').strip().lower()
    if not text:
        return 'unknown'
    return text


failure_like = {'failure', 'cancelled', 'timed_out', 'action_required', 'startup_failure'}

files = sorted(glob.glob(run_glob, recursive=True))
if not files:
    print(f"ERROR: no files matched RUN_GLOB={run_glob}", file=sys.stderr)
    sys.exit(1)

summary = {
    'files_scanned': len(files),
    'parse_errors': [],
    'runs_scanned': 0,
    'runs_filtered': 0,
    'groups': 0,
    'groups_below_min_runs': 0,
    'warn_groups': 0,
    'critical_groups': 0,
}

groups = defaultdict(list)

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
    conclusion = normalize_conclusion(payload.get('conclusion'))
    run_id = str(payload.get('databaseId') or payload.get('id') or path)
    run_url = payload.get('url')

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

    timestamp = (
        parse_ts(payload.get('createdAt'))
        or parse_ts(payload.get('runStartedAt'))
        or parse_ts(payload.get('updatedAt'))
    )

    groups[(repository, workflow, branch)].append({
        'run_id': run_id,
        'conclusion': conclusion,
        'timestamp': timestamp,
        'run_url': run_url,
    })

ranked_groups = []
critical_groups = []

for (repository, workflow, branch), runs in groups.items():
    runs_sorted = sorted(
        runs,
        key=lambda r: (
            r['timestamp'] is None,
            r['timestamp'] or datetime.min,
            r['run_id'],
        ),
    )

    conclusions = [r['conclusion'] for r in runs_sorted]
    run_count = len(conclusions)
    transitions = 0
    for idx in range(1, run_count):
        if conclusions[idx] != conclusions[idx - 1]:
            transitions += 1

    instability_pct = 0.0
    if run_count > 1:
        instability_pct = (transitions / (run_count - 1)) * 100.0

    success_count = sum(1 for c in conclusions if c == 'success')
    failure_like_count = sum(1 for c in conclusions if c in failure_like)

    failure_rate_pct = 0.0
    if run_count > 0:
        failure_rate_pct = (failure_like_count / run_count) * 100.0

    streak = 0
    max_failure_streak = 0
    for c in conclusions:
        if c in failure_like:
            streak += 1
            if streak > max_failure_streak:
                max_failure_streak = streak
        else:
            streak = 0

    severity = 'ok'
    if run_count < min_runs:
        summary['groups_below_min_runs'] += 1
    else:
        if instability_pct >= critical_instability_pct:
            severity = 'critical'
            summary['critical_groups'] += 1
        elif instability_pct >= warn_instability_pct:
            severity = 'warn'
            summary['warn_groups'] += 1

    row = {
        'repository': repository,
        'workflow': workflow,
        'branch': branch,
        'run_count': run_count,
        'transitions': transitions,
        'instability_pct': round(instability_pct, 3),
        'success_count': success_count,
        'failure_like_count': failure_like_count,
        'failure_rate_pct': round(failure_rate_pct, 3),
        'max_failure_streak': max_failure_streak,
        'latest_conclusion': conclusions[-1] if conclusions else None,
        'severity': severity,
        'sample_run_urls': [r['run_url'] for r in runs_sorted if r.get('run_url')][:3],
    }

    ranked_groups.append(row)
    if severity == 'critical':
        critical_groups.append(row)

severity_rank = {'critical': 2, 'warn': 1, 'ok': 0}
ranked_groups.sort(
    key=lambda row: (
        -severity_rank[row['severity']],
        -row['instability_pct'],
        -row['failure_rate_pct'],
        -row['run_count'],
        row['repository'],
        row['workflow'],
        row['branch'],
    )
)

summary['groups'] = len(ranked_groups)

result = {
    'summary': {
        **summary,
        'top_n': top_n,
        'thresholds': {
            'min_runs': min_runs,
            'warn_instability_pct': warn_instability_pct,
            'critical_instability_pct': critical_instability_pct,
        },
        'filters': {
            'repo_match': repo_match_raw or None,
            'repo_exclude': repo_exclude_raw or None,
            'workflow_match': workflow_match_raw or None,
            'workflow_exclude': workflow_exclude_raw or None,
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
    print('GITHUB ACTIONS CONCLUSION VOLATILITY AUDIT')
    print('---')
    print(
        'SUMMARY: '
        f"files={summary['files_scanned']} runs={summary['runs_scanned']} runs_filtered={summary['runs_filtered']} "
        f"groups={summary['groups']} warn_groups={summary['warn_groups']} critical_groups={summary['critical_groups']} "
        f"below_min_runs={summary['groups_below_min_runs']}"
    )
    print(
        'THRESHOLDS: '
        f"min_runs={min_runs} warn_instability_pct={warn_instability_pct} critical_instability_pct={critical_instability_pct}"
    )

    if summary['parse_errors']:
        print('PARSE_ERRORS:')
        for err in summary['parse_errors']:
            print(f"- {err}")

    print('---')
    print(f"TOP VOLATILITY GROUPS ({min(top_n, len(ranked_groups))})")
    if not ranked_groups:
        print('none')
    else:
        for row in ranked_groups[:top_n]:
            print(
                f"- [{row['severity']}] {row['repository']} :: {row['workflow']} :: {row['branch']} "
                f"instability_pct={row['instability_pct']} failure_rate_pct={row['failure_rate_pct']} "
                f"runs={row['run_count']} transitions={row['transitions']} max_failure_streak={row['max_failure_streak']}"
            )

sys.exit(1 if (fail_on_critical and critical_groups) else 0)
PY
