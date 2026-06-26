#!/usr/bin/env bash
set -euo pipefail

RUN_GLOB="${RUN_GLOB:-artifacts/github-actions-runs/*.json}"
TOP_N="${TOP_N:-20}"
OUTPUT_FORMAT="${OUTPUT_FORMAT:-text}"
WARN_WASTED_MINUTES="${WARN_WASTED_MINUTES:-15}"
CRITICAL_WASTED_MINUTES="${CRITICAL_WASTED_MINUTES:-45}"
FAIL_ON_CRITICAL="${FAIL_ON_CRITICAL:-0}"
REPO_MATCH="${REPO_MATCH:-}"
REPO_EXCLUDE="${REPO_EXCLUDE:-}"
WORKFLOW_MATCH="${WORKFLOW_MATCH:-}"
WORKFLOW_EXCLUDE="${WORKFLOW_EXCLUDE:-}"
BRANCH_MATCH="${BRANCH_MATCH:-}"
BRANCH_EXCLUDE="${BRANCH_EXCLUDE:-}"
ACTOR_MATCH="${ACTOR_MATCH:-}"
ACTOR_EXCLUDE="${ACTOR_EXCLUDE:-}"
CONCLUSION_MATCH="${CONCLUSION_MATCH:-}"
CONCLUSION_EXCLUDE="${CONCLUSION_EXCLUDE:-}"

if [[ "$OUTPUT_FORMAT" != "text" && "$OUTPUT_FORMAT" != "json" ]]; then
  echo "ERROR: OUTPUT_FORMAT must be 'text' or 'json' (got: $OUTPUT_FORMAT)" >&2
  exit 1
fi

if ! [[ "$TOP_N" =~ ^[0-9]+$ ]] || [[ "$TOP_N" -eq 0 ]]; then
  echo "ERROR: TOP_N must be a positive integer (got: $TOP_N)" >&2
  exit 1
fi

if ! [[ "$WARN_WASTED_MINUTES" =~ ^[0-9]+([.][0-9]+)?$ ]]; then
  echo "ERROR: WARN_WASTED_MINUTES must be a non-negative number (got: $WARN_WASTED_MINUTES)" >&2
  exit 1
fi

if ! [[ "$CRITICAL_WASTED_MINUTES" =~ ^[0-9]+([.][0-9]+)?$ ]]; then
  echo "ERROR: CRITICAL_WASTED_MINUTES must be a non-negative number (got: $CRITICAL_WASTED_MINUTES)" >&2
  exit 1
fi

if [[ "$FAIL_ON_CRITICAL" != "0" && "$FAIL_ON_CRITICAL" != "1" ]]; then
  echo "ERROR: FAIL_ON_CRITICAL must be 0 or 1 (got: $FAIL_ON_CRITICAL)" >&2
  exit 1
fi

python3 - "$RUN_GLOB" "$TOP_N" "$OUTPUT_FORMAT" "$WARN_WASTED_MINUTES" "$CRITICAL_WASTED_MINUTES" "$FAIL_ON_CRITICAL" "$REPO_MATCH" "$REPO_EXCLUDE" "$WORKFLOW_MATCH" "$WORKFLOW_EXCLUDE" "$BRANCH_MATCH" "$BRANCH_EXCLUDE" "$ACTOR_MATCH" "$ACTOR_EXCLUDE" "$CONCLUSION_MATCH" "$CONCLUSION_EXCLUDE" <<'PY'
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
repo_match_raw = sys.argv[7]
repo_exclude_raw = sys.argv[8]
workflow_match_raw = sys.argv[9]
workflow_exclude_raw = sys.argv[10]
branch_match_raw = sys.argv[11]
branch_exclude_raw = sys.argv[12]
actor_match_raw = sys.argv[13]
actor_exclude_raw = sys.argv[14]
conclusion_match_raw = sys.argv[15]
conclusion_exclude_raw = sys.argv[16]

if critical_minutes < warn_minutes:
    print('ERROR: CRITICAL_WASTED_MINUTES must be >= WARN_WASTED_MINUTES', file=sys.stderr)
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
    ts = str(value)
    if ts.endswith('Z'):
        ts = ts[:-1] + '+00:00'
    try:
        return datetime.fromisoformat(ts)
    except ValueError:
        return None


repo_match = compile_optional_regex(repo_match_raw, 'REPO_MATCH')
repo_exclude = compile_optional_regex(repo_exclude_raw, 'REPO_EXCLUDE')
workflow_match = compile_optional_regex(workflow_match_raw, 'WORKFLOW_MATCH')
workflow_exclude = compile_optional_regex(workflow_exclude_raw, 'WORKFLOW_EXCLUDE')
branch_match = compile_optional_regex(branch_match_raw, 'BRANCH_MATCH')
branch_exclude = compile_optional_regex(branch_exclude_raw, 'BRANCH_EXCLUDE')
actor_match = compile_optional_regex(actor_match_raw, 'ACTOR_MATCH')
actor_exclude = compile_optional_regex(actor_exclude_raw, 'ACTOR_EXCLUDE')
conclusion_match = compile_optional_regex(conclusion_match_raw, 'CONCLUSION_MATCH')
conclusion_exclude = compile_optional_regex(conclusion_exclude_raw, 'CONCLUSION_EXCLUDE')


DEFAULT_CONCLUSION_SET = {'cancelled', 'timed_out'}

files = sorted(glob.glob(run_glob, recursive=True))
if not files:
    print(f"ERROR: no files matched RUN_GLOB={run_glob}", file=sys.stderr)
    sys.exit(1)

parse_errors = []
files_scanned = 0
runs_scanned = 0
runs_filtered = 0
runs_missing_duration = 0
runs_considered = 0
critical_instances = []

agg = defaultdict(lambda: {
    'repository': None,
    'workflow': None,
    'conclusion': None,
    'minutes': [],
    'branches': set(),
    'actors': set(),
})

for path in files:
    try:
        with open(path, 'r', encoding='utf-8') as fh:
            payload = json.load(fh)
    except Exception as exc:
        parse_errors.append(f"{path}: {exc}")
        continue

    files_scanned += 1
    default_repo = path.rsplit('/', 1)[-1].rsplit('.', 1)[0]
    repository = default_repo
    runs = None

    if isinstance(payload, dict):
        repo_obj = payload.get('repository')
        if isinstance(repo_obj, dict):
            repo_name = repo_obj.get('full_name') or repo_obj.get('nameWithOwner') or repo_obj.get('name')
            if isinstance(repo_name, str) and repo_name.strip():
                repository = repo_name.strip()
        elif isinstance(repo_obj, str) and repo_obj.strip():
            repository = repo_obj.strip()

        runs = payload.get('workflow_runs') or payload.get('runs')
    elif isinstance(payload, list):
        runs = payload

    if not isinstance(runs, list):
        parse_errors.append(f"{path}: missing workflow_runs[]")
        continue

    for row in runs:
        if not isinstance(row, dict):
            continue

        runs_scanned += 1

        row_repo = row.get('repository')
        if isinstance(row_repo, dict):
            rr = row_repo.get('full_name') or row_repo.get('nameWithOwner') or row_repo.get('name')
            if isinstance(rr, str) and rr.strip():
                repository = rr.strip()

        workflow = row.get('name') or row.get('display_title') or '<unnamed-workflow>'
        workflow = str(workflow).strip() or '<unnamed-workflow>'

        branch = row.get('head_branch') or '<unknown-branch>'
        branch = str(branch).strip() or '<unknown-branch>'

        actor = '<unknown-actor>'
        actor_obj = row.get('actor')
        if isinstance(actor_obj, dict):
            actor = actor_obj.get('login') or actor_obj.get('name') or actor
        elif isinstance(actor_obj, str) and actor_obj.strip():
            actor = actor_obj.strip()

        conclusion = row.get('conclusion') or 'unknown'
        conclusion = str(conclusion).strip().lower() or 'unknown'

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
        if branch_match and not branch_match.search(branch):
            runs_filtered += 1
            continue
        if branch_exclude and branch_exclude.search(branch):
            runs_filtered += 1
            continue
        if actor_match and not actor_match.search(actor):
            runs_filtered += 1
            continue
        if actor_exclude and actor_exclude.search(actor):
            runs_filtered += 1
            continue

        if conclusion_match:
            if not conclusion_match.search(conclusion):
                runs_filtered += 1
                continue
        elif conclusion not in DEFAULT_CONCLUSION_SET:
            runs_filtered += 1
            continue

        if conclusion_exclude and conclusion_exclude.search(conclusion):
            runs_filtered += 1
            continue

        started_at = parse_ts(row.get('run_started_at') or row.get('created_at'))
        ended_at = parse_ts(row.get('updated_at') or row.get('completed_at'))
        if not started_at or not ended_at:
            runs_missing_duration += 1
            continue

        wasted_minutes = (ended_at - started_at).total_seconds() / 60.0
        if wasted_minutes < 0:
            runs_missing_duration += 1
            continue

        runs_considered += 1

        key = (repository, workflow, conclusion)
        bucket = agg[key]
        bucket['repository'] = repository
        bucket['workflow'] = workflow
        bucket['conclusion'] = conclusion
        bucket['minutes'].append(wasted_minutes)
        bucket['branches'].add(branch)
        bucket['actors'].add(actor)

        if wasted_minutes >= critical_minutes:
            critical_instances.append({
                'repository': repository,
                'workflow': workflow,
                'conclusion': conclusion,
                'run_id': row.get('id'),
                'run_number': row.get('run_number'),
                'branch': branch,
                'actor': actor,
                'wasted_minutes': round(wasted_minutes, 3),
                'html_url': row.get('html_url'),
                'created_at': row.get('created_at'),
                'run_started_at': row.get('run_started_at'),
                'updated_at': row.get('updated_at'),
            })

groups = []
for bucket in agg.values():
    minutes = bucket['minutes']
    if not minutes:
        continue

    max_minutes = max(minutes)
    avg_minutes = sum(minutes) / len(minutes)
    total_minutes = sum(minutes)

    severity = 'ok'
    if max_minutes >= critical_minutes:
        severity = 'critical'
    elif max_minutes >= warn_minutes:
        severity = 'warn'

    groups.append({
        'repository': bucket['repository'],
        'workflow': bucket['workflow'],
        'conclusion': bucket['conclusion'],
        'run_count': len(minutes),
        'max_wasted_minutes': round(max_minutes, 3),
        'avg_wasted_minutes': round(avg_minutes, 3),
        'total_wasted_minutes': round(total_minutes, 3),
        'branches': sorted(bucket['branches']),
        'actors': sorted(bucket['actors']),
        'severity': severity,
    })

groups.sort(key=lambda row: (-row['max_wasted_minutes'], -row['total_wasted_minutes'], row['repository'], row['workflow'], row['conclusion']))

summary = {
    'files_matched': len(files),
    'files_scanned': files_scanned,
    'parse_errors': parse_errors,
    'runs_scanned': runs_scanned,
    'runs_filtered': runs_filtered,
    'runs_missing_duration': runs_missing_duration,
    'runs_considered': runs_considered,
    'groups': len(groups),
    'critical_instances': len(critical_instances),
    'warn_wasted_minutes': warn_minutes,
    'critical_wasted_minutes': critical_minutes,
    'top_n': top_n,
    'filters': {
        'repo_match': repo_match_raw or None,
        'repo_exclude': repo_exclude_raw or None,
        'workflow_match': workflow_match_raw or None,
        'workflow_exclude': workflow_exclude_raw or None,
        'branch_match': branch_match_raw or None,
        'branch_exclude': branch_exclude_raw or None,
        'actor_match': actor_match_raw or None,
        'actor_exclude': actor_exclude_raw or None,
        'conclusion_match': conclusion_match_raw or None,
        'conclusion_exclude': conclusion_exclude_raw or None,
    },
}

if output_format == 'json':
    print(json.dumps({'summary': summary, 'groups': groups[:top_n], 'all_groups': groups, 'critical_instances': critical_instances}, indent=2, sort_keys=True))
else:
    print('GITHUB ACTIONS CANCEL WASTE AUDIT')
    print('---')
    print(
        'SUMMARY: '
        f"files={summary['files_scanned']}/{summary['files_matched']} runs={summary['runs_scanned']} "
        f"filtered={summary['runs_filtered']} missing_duration={summary['runs_missing_duration']} "
        f"considered={summary['runs_considered']} groups={summary['groups']} "
        f"critical_instances={summary['critical_instances']}"
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
        f"branch={branch_match_raw}" if branch_match_raw else None,
        f"branch!={branch_exclude_raw}" if branch_exclude_raw else None,
        f"actor={actor_match_raw}" if actor_match_raw else None,
        f"actor!={actor_exclude_raw}" if actor_exclude_raw else None,
        f"conclusion={conclusion_match_raw}" if conclusion_match_raw else 'conclusion=cancelled|timed_out',
        f"conclusion!={conclusion_exclude_raw}" if conclusion_exclude_raw else None,
    ]
    active_filters = [f for f in active_filters if f]
    if active_filters:
        print('FILTERS: ' + ' '.join(active_filters))

    print('---')
    print(f"TOP CANCEL/TIMEOUT WASTE HOTSPOTS ({min(top_n, len(groups))})")
    if not groups:
        print('none')
    else:
        for row in groups[:top_n]:
            print(
                f"- [{row['severity']}] {row['repository']} :: {row['workflow']} ({row['conclusion']}) "
                f"max_min={row['max_wasted_minutes']} avg_min={row['avg_wasted_minutes']} "
                f"total_min={row['total_wasted_minutes']} runs={row['run_count']} "
                f"branches={','.join(row['branches'][:3])} actors={','.join(row['actors'][:3])}"
            )

sys.exit(1 if (fail_on_critical and critical_instances) else 0)
PY
