#!/usr/bin/env bash
set -euo pipefail

RUN_GLOB="${RUN_GLOB:-artifacts/github-actions-runs/*.json}"
TOP_N="${TOP_N:-20}"
OUTPUT_FORMAT="${OUTPUT_FORMAT:-text}"
GROUP_BY="${GROUP_BY:-actor}"
OWNER_MAP_FILE="${OWNER_MAP_FILE:-}"
WARN_FAILURE_RUNS="${WARN_FAILURE_RUNS:-3}"
CRITICAL_FAILURE_RUNS="${CRITICAL_FAILURE_RUNS:-6}"
WARN_FAILURE_MINUTES="${WARN_FAILURE_MINUTES:-30}"
CRITICAL_FAILURE_MINUTES="${CRITICAL_FAILURE_MINUTES:-90}"
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

if [[ "$GROUP_BY" != "actor" && "$GROUP_BY" != "actor-workflow" && "$GROUP_BY" != "owner" && "$GROUP_BY" != "owner-workflow" ]]; then
  echo "ERROR: GROUP_BY must be 'actor', 'actor-workflow', 'owner', or 'owner-workflow' (got: $GROUP_BY)" >&2
  exit 1
fi

if ! [[ "$TOP_N" =~ ^[0-9]+$ ]] || [[ "$TOP_N" -eq 0 ]]; then
  echo "ERROR: TOP_N must be a positive integer (got: $TOP_N)" >&2
  exit 1
fi

if ! [[ "$WARN_FAILURE_RUNS" =~ ^[0-9]+$ ]] || ! [[ "$CRITICAL_FAILURE_RUNS" =~ ^[0-9]+$ ]]; then
  echo "ERROR: WARN_FAILURE_RUNS and CRITICAL_FAILURE_RUNS must be positive integers" >&2
  exit 1
fi

if ! [[ "$WARN_FAILURE_MINUTES" =~ ^[0-9]+([.][0-9]+)?$ ]] || ! [[ "$CRITICAL_FAILURE_MINUTES" =~ ^[0-9]+([.][0-9]+)?$ ]]; then
  echo "ERROR: WARN_FAILURE_MINUTES and CRITICAL_FAILURE_MINUTES must be non-negative numbers" >&2
  exit 1
fi

if [[ "$CRITICAL_FAILURE_RUNS" -lt "$WARN_FAILURE_RUNS" ]]; then
  echo "ERROR: CRITICAL_FAILURE_RUNS must be >= WARN_FAILURE_RUNS" >&2
  exit 1
fi

if [[ "$FAIL_ON_CRITICAL" != "0" && "$FAIL_ON_CRITICAL" != "1" ]]; then
  echo "ERROR: FAIL_ON_CRITICAL must be 0 or 1 (got: $FAIL_ON_CRITICAL)" >&2
  exit 1
fi

python3 - "$RUN_GLOB" "$TOP_N" "$OUTPUT_FORMAT" "$GROUP_BY" "$OWNER_MAP_FILE" "$WARN_FAILURE_RUNS" "$CRITICAL_FAILURE_RUNS" "$WARN_FAILURE_MINUTES" "$CRITICAL_FAILURE_MINUTES" "$FAIL_ON_CRITICAL" "$REPO_MATCH" "$REPO_EXCLUDE" "$WORKFLOW_MATCH" "$WORKFLOW_EXCLUDE" "$BRANCH_MATCH" "$BRANCH_EXCLUDE" "$ACTOR_MATCH" "$ACTOR_EXCLUDE" "$CONCLUSION_MATCH" "$CONCLUSION_EXCLUDE" <<'PY'
import glob
import json
import re
import sys
from collections import defaultdict
from datetime import datetime

run_glob = sys.argv[1]
top_n = int(sys.argv[2])
output_format = sys.argv[3]
group_by = sys.argv[4]
owner_map_file = sys.argv[5]
warn_failure_runs = int(sys.argv[6])
critical_failure_runs = int(sys.argv[7])
warn_failure_minutes = float(sys.argv[8])
critical_failure_minutes = float(sys.argv[9])
fail_on_critical = sys.argv[10] == '1'
repo_match_raw = sys.argv[11]
repo_exclude_raw = sys.argv[12]
workflow_match_raw = sys.argv[13]
workflow_exclude_raw = sys.argv[14]
branch_match_raw = sys.argv[15]
branch_exclude_raw = sys.argv[16]
actor_match_raw = sys.argv[17]
actor_exclude_raw = sys.argv[18]
conclusion_match_raw = sys.argv[19]
conclusion_exclude_raw = sys.argv[20]

if critical_failure_minutes < warn_failure_minutes:
    print('ERROR: CRITICAL_FAILURE_MINUTES must be >= WARN_FAILURE_MINUTES', file=sys.stderr)
    sys.exit(1)


def compile_optional_regex(pattern, label):
    if not pattern:
        return None
    try:
        return re.compile(pattern)
    except re.error as exc:
        print(f"ERROR: invalid {label} regex {pattern!r}: {exc}", file=sys.stderr)
        sys.exit(1)


def load_owner_mappings(path):
    if not path:
        return []

    try:
        with open(path, 'r', encoding='utf-8') as fh:
            payload = json.load(fh)
    except FileNotFoundError:
        print(f"ERROR: OWNER_MAP_FILE not found: {path}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        print(f"ERROR: failed to read OWNER_MAP_FILE {path}: {exc}", file=sys.stderr)
        sys.exit(1)

    mappings = []

    if isinstance(payload, dict):
        items = payload.items()
        for regex, owner in items:
            if not isinstance(regex, str) or not regex.strip():
                print('ERROR: OWNER_MAP_FILE dict keys must be non-empty regex strings', file=sys.stderr)
                sys.exit(1)
            if not isinstance(owner, str) or not owner.strip():
                print('ERROR: OWNER_MAP_FILE dict values must be non-empty owner strings', file=sys.stderr)
                sys.exit(1)
            try:
                pattern = re.compile(regex)
            except re.error as exc:
                print(f"ERROR: invalid OWNER_MAP_FILE regex {regex!r}: {exc}", file=sys.stderr)
                sys.exit(1)
            mappings.append((pattern, owner.strip()))
        return mappings

    if not isinstance(payload, list):
        print('ERROR: OWNER_MAP_FILE must be a JSON object or list', file=sys.stderr)
        sys.exit(1)

    for idx, row in enumerate(payload, start=1):
        if not isinstance(row, dict):
            print(f'ERROR: OWNER_MAP_FILE list item {idx} must be an object', file=sys.stderr)
            sys.exit(1)
        regex = row.get('match') or row.get('regex')
        owner = row.get('owner')
        if not isinstance(regex, str) or not regex.strip():
            print(f"ERROR: OWNER_MAP_FILE list item {idx} needs 'match' (or 'regex')", file=sys.stderr)
            sys.exit(1)
        if not isinstance(owner, str) or not owner.strip():
            print(f"ERROR: OWNER_MAP_FILE list item {idx} needs non-empty 'owner'", file=sys.stderr)
            sys.exit(1)
        try:
            pattern = re.compile(regex)
        except re.error as exc:
            print(f"ERROR: invalid OWNER_MAP_FILE regex {regex!r}: {exc}", file=sys.stderr)
            sys.exit(1)
        mappings.append((pattern, owner.strip()))

    return mappings


def resolve_owner(actor, mappings):
    for pattern, owner in mappings:
        if pattern.search(actor):
            return owner
    return actor


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


def extract_repo(default_repo, payload):
    repository = default_repo
    repo_obj = payload.get('repository')
    if isinstance(repo_obj, dict):
        repository = (
            repo_obj.get('full_name')
            or repo_obj.get('nameWithOwner')
            or repo_obj.get('fullName')
            or repo_obj.get('name')
            or repository
        )
    elif isinstance(repo_obj, str) and repo_obj.strip():
        repository = repo_obj.strip()
    return str(repository).strip() or '<unknown-repo>'


def normalize_workflow(run):
    workflow = run.get('workflowName') or run.get('name') or run.get('display_title')
    return str(workflow).strip() or '<unknown-workflow>'


def normalize_branch(run):
    return str(run.get('head_branch') or run.get('headBranch') or '<unknown-branch>').strip() or '<unknown-branch>'


def normalize_actor(run):
    actor = '<unknown-actor>'
    actor_obj = run.get('actor')
    if isinstance(actor_obj, dict):
        actor = actor_obj.get('login') or actor_obj.get('name') or actor
    elif isinstance(actor_obj, str) and actor_obj.strip():
        actor = actor_obj.strip()
    return str(actor).strip() or '<unknown-actor>'


def normalize_conclusion(run):
    return str(run.get('conclusion') or '').strip().lower() or 'unknown'


def estimate_minutes(run):
    started = parse_ts(run.get('run_started_at') or run.get('runStartedAt') or run.get('created_at') or run.get('createdAt'))
    completed = parse_ts(run.get('updated_at') or run.get('updatedAt') or run.get('completed_at') or run.get('completedAt'))
    if started and completed:
        minutes = (completed - started).total_seconds() / 60.0
        return max(minutes, 0.0)

    total = 0.0
    jobs = run.get('jobs')
    if isinstance(jobs, list):
        for job in jobs:
            if not isinstance(job, dict):
                continue
            j_started = parse_ts(job.get('started_at') or job.get('startedAt') or job.get('created_at') or job.get('createdAt'))
            j_completed = parse_ts(job.get('completed_at') or job.get('completedAt') or job.get('updated_at') or job.get('updatedAt'))
            if j_started and j_completed:
                total += max((j_completed - j_started).total_seconds() / 60.0, 0.0)

    return total


def extract_runs(path, payload):
    if isinstance(payload, list):
        return payload
    if not isinstance(payload, dict):
        return []

    if isinstance(payload.get('workflow_runs'), list):
        return payload['workflow_runs']
    if isinstance(payload.get('runs'), list):
        return payload['runs']

    # Single run payload shape.
    if any(k in payload for k in ('conclusion', 'workflowName', 'head_branch', 'headBranch', 'run_started_at', 'runStartedAt', 'databaseId', 'id')):
        return [payload]

    return []


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
owner_mappings = load_owner_mappings(owner_map_file)

DEFAULT_CONCLUSIONS = {'failure', 'cancelled', 'timed_out', 'action_required', 'startup_failure'}

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

agg = defaultdict(lambda: {
    'repository': None,
    'actor': None,
    'owner': None,
    'workflow': None,
    'actors': set(),
    'run_count': 0,
    'minutes_total': 0.0,
    'minutes_max': 0.0,
    'branches': set(),
    'conclusions': defaultdict(int),
    'sample_runs': [],
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

    runs = extract_runs(path, payload)
    if not runs:
        parse_errors.append(f"{path}: missing run rows")
        continue

    for run in runs:
        if not isinstance(run, dict):
            continue

        runs_scanned += 1

        repository = extract_repo(default_repo, run)
        workflow = normalize_workflow(run)
        branch = normalize_branch(run)
        actor = normalize_actor(run)
        owner = resolve_owner(actor, owner_mappings)
        conclusion = normalize_conclusion(run)

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
        elif conclusion not in DEFAULT_CONCLUSIONS:
            runs_filtered += 1
            continue

        if conclusion_exclude and conclusion_exclude.search(conclusion):
            runs_filtered += 1
            continue

        minutes = estimate_minutes(run)
        if minutes <= 0:
            runs_missing_duration += 1
            continue

        runs_considered += 1

        if group_by == 'actor-workflow':
            key = (repository, actor, workflow)
        elif group_by == 'owner-workflow':
            key = (repository, owner, workflow)
        elif group_by == 'owner':
            key = (repository, owner)
        else:
            key = (repository, actor)

        bucket = agg[key]
        bucket['repository'] = repository
        bucket['actors'].add(actor)
        bucket['actor'] = actor if group_by in ('actor', 'actor-workflow') else ('<multiple>' if len(bucket['actors']) > 1 else actor)
        bucket['owner'] = owner
        bucket['workflow'] = workflow if group_by in ('actor-workflow', 'owner-workflow') else None
        bucket['run_count'] += 1
        bucket['minutes_total'] += minutes
        bucket['minutes_max'] = max(bucket['minutes_max'], minutes)
        bucket['branches'].add(branch)
        bucket['conclusions'][conclusion] += 1

        if len(bucket['sample_runs']) < 3:
            bucket['sample_runs'].append({
                'run_id': run.get('id') or run.get('databaseId'),
                'run_number': run.get('run_number') or run.get('runNumber'),
                'branch': branch,
                'conclusion': conclusion,
                'minutes': round(minutes, 3),
                'html_url': run.get('html_url') or run.get('url'),
            })

rows = []
critical_rows = []
for bucket in agg.values():
    severity = 'ok'
    if bucket['run_count'] >= critical_failure_runs or bucket['minutes_total'] >= critical_failure_minutes:
        severity = 'critical'
    elif bucket['run_count'] >= warn_failure_runs or bucket['minutes_total'] >= warn_failure_minutes:
        severity = 'warn'

    row = {
        'repository': bucket['repository'],
        'actor': bucket['actor'],
        'owner': bucket['owner'],
        'actor_count': len(bucket['actors']),
        'actors': sorted(bucket['actors']),
        'workflow': bucket['workflow'],
        'run_count': bucket['run_count'],
        'total_failure_minutes': round(bucket['minutes_total'], 3),
        'max_failure_minutes': round(bucket['minutes_max'], 3),
        'branch_count': len(bucket['branches']),
        'conclusions': dict(sorted(bucket['conclusions'].items(), key=lambda item: (-item[1], item[0]))),
        'sample_runs': bucket['sample_runs'],
        'severity': severity,
    }
    rows.append(row)
    if severity == 'critical':
        critical_rows.append(row)

severity_rank = {'critical': 2, 'warn': 1, 'ok': 0}
rows.sort(key=lambda row: (-severity_rank[row['severity']], -row['run_count'], -row['total_failure_minutes'], row['repository'], row.get('owner') or row['actor'], row['actor']))

summary = {
    'files_matched': len(files),
    'files_scanned': files_scanned,
    'parse_errors': parse_errors,
    'runs_scanned': runs_scanned,
    'runs_filtered': runs_filtered,
    'runs_missing_duration': runs_missing_duration,
    'runs_considered': runs_considered,
    'groups': len(rows),
    'critical_groups': len(critical_rows),
    'top_n': top_n,
    'group_by': group_by,
    'warn_failure_runs': warn_failure_runs,
    'critical_failure_runs': critical_failure_runs,
    'warn_failure_minutes': warn_failure_minutes,
    'critical_failure_minutes': critical_failure_minutes,
    'owner_map_file': owner_map_file or None,
    'owner_mappings': len(owner_mappings),
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

result = {
    'summary': summary,
    'groups': rows[:top_n],
    'all_groups': rows,
    'critical_groups': critical_rows,
}

if output_format == 'json':
    print(json.dumps(result, indent=2, sort_keys=True))
else:
    print('GITHUB ACTIONS FAILURE OWNER AUDIT')
    print('---')
    print(
        'SUMMARY: '
        f"files={summary['files_scanned']}/{summary['files_matched']} runs={summary['runs_scanned']} "
        f"filtered={summary['runs_filtered']} missing_duration={summary['runs_missing_duration']} "
        f"considered={summary['runs_considered']} groups={summary['groups']} critical_groups={summary['critical_groups']}"
    )
    print(
        'THRESHOLDS: '
        f"group_by={group_by} warn_runs={warn_failure_runs} critical_runs={critical_failure_runs} "
        f"warn_minutes={warn_failure_minutes} critical_minutes={critical_failure_minutes}"
    )

    if parse_errors:
        print('PARSE_ERRORS:')
        for err in parse_errors:
            print(f"- {err}")

    print('---')
    print(f"TOP FAILURE OWNERS ({min(top_n, len(rows))})")
    if not rows:
        print('none')
    else:
        for row in rows[:top_n]:
            workflow_label = row['workflow'] if row['workflow'] else '*'
            print(
                f"- [{row['severity']}] {row['repository']} :: owner={row.get('owner') or row['actor']} actor={row['actor']} workflow={workflow_label} "
                f"runs={row['run_count']} total_min={row['total_failure_minutes']} max_min={row['max_failure_minutes']} "
                f"branches={row['branch_count']} conclusions={row['conclusions']}"
            )

sys.exit(1 if (fail_on_critical and critical_rows) else 0)
PY
