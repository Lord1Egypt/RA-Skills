#!/usr/bin/env bash
set -euo pipefail

RUN_GLOB="${RUN_GLOB:-artifacts/github-actions/*.json}"
TOP_N="${TOP_N:-20}"
OUTPUT_FORMAT="${OUTPUT_FORMAT:-text}"
INCIDENT_GAP_MINUTES="${INCIDENT_GAP_MINUTES:-45}"
WARN_FAILED_RUNS="${WARN_FAILED_RUNS:-2}"
CRITICAL_FAILED_RUNS="${CRITICAL_FAILED_RUNS:-4}"
WARN_DURATION_MINUTES="${WARN_DURATION_MINUTES:-20}"
CRITICAL_DURATION_MINUTES="${CRITICAL_DURATION_MINUTES:-60}"
FAIL_ON_CRITICAL="${FAIL_ON_CRITICAL:-0}"
WORKFLOW_MATCH="${WORKFLOW_MATCH:-}"
WORKFLOW_EXCLUDE="${WORKFLOW_EXCLUDE:-}"
REPO_MATCH="${REPO_MATCH:-}"
REPO_EXCLUDE="${REPO_EXCLUDE:-}"

if [[ "$OUTPUT_FORMAT" != "text" && "$OUTPUT_FORMAT" != "json" ]]; then
  echo "ERROR: OUTPUT_FORMAT must be 'text' or 'json' (got: $OUTPUT_FORMAT)" >&2
  exit 1
fi

for pair in \
  "TOP_N:$TOP_N" \
  "INCIDENT_GAP_MINUTES:$INCIDENT_GAP_MINUTES" \
  "WARN_FAILED_RUNS:$WARN_FAILED_RUNS" \
  "CRITICAL_FAILED_RUNS:$CRITICAL_FAILED_RUNS" \
  "WARN_DURATION_MINUTES:$WARN_DURATION_MINUTES" \
  "CRITICAL_DURATION_MINUTES:$CRITICAL_DURATION_MINUTES"; do
  key="${pair%%:*}"
  value="${pair#*:}"
  if ! [[ "$value" =~ ^[0-9]+$ ]] || [[ "$value" -eq 0 ]]; then
    echo "ERROR: $key must be a positive integer (got: $value)" >&2
    exit 1
  fi
done

if (( CRITICAL_FAILED_RUNS < WARN_FAILED_RUNS )); then
  echo "ERROR: CRITICAL_FAILED_RUNS must be >= WARN_FAILED_RUNS" >&2
  exit 1
fi

if (( CRITICAL_DURATION_MINUTES < WARN_DURATION_MINUTES )); then
  echo "ERROR: CRITICAL_DURATION_MINUTES must be >= WARN_DURATION_MINUTES" >&2
  exit 1
fi

if [[ "$FAIL_ON_CRITICAL" != "0" && "$FAIL_ON_CRITICAL" != "1" ]]; then
  echo "ERROR: FAIL_ON_CRITICAL must be 0 or 1 (got: $FAIL_ON_CRITICAL)" >&2
  exit 1
fi

python3 - "$RUN_GLOB" "$TOP_N" "$OUTPUT_FORMAT" "$INCIDENT_GAP_MINUTES" "$WARN_FAILED_RUNS" "$CRITICAL_FAILED_RUNS" "$WARN_DURATION_MINUTES" "$CRITICAL_DURATION_MINUTES" "$FAIL_ON_CRITICAL" "$WORKFLOW_MATCH" "$WORKFLOW_EXCLUDE" "$REPO_MATCH" "$REPO_EXCLUDE" <<'PY'
import glob
import json
import re
import sys
from collections import defaultdict
from datetime import datetime

run_glob = sys.argv[1]
top_n = int(sys.argv[2])
output_format = sys.argv[3]
incident_gap_minutes = int(sys.argv[4])
warn_failed_runs = int(sys.argv[5])
critical_failed_runs = int(sys.argv[6])
warn_duration_minutes = int(sys.argv[7])
critical_duration_minutes = int(sys.argv[8])
fail_on_critical = sys.argv[9] == '1'
workflow_match_raw = sys.argv[10]
workflow_exclude_raw = sys.argv[11]
repo_match_raw = sys.argv[12]
repo_exclude_raw = sys.argv[13]


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

failure_outcomes = {'failure', 'cancelled', 'timed_out', 'startup_failure', 'stale', 'action_required'}
parse_errors = []
runs_scanned = 0
runs_filtered = 0
non_failure_runs = 0

failures_by_repo = defaultdict(list)

for path in files:
    try:
        with open(path, 'r', encoding='utf-8') as fh:
            payload = json.load(fh)
    except Exception as exc:
        parse_errors.append(f"{path}: {exc}")
        continue

    runs_scanned += 1
    workflow = payload.get('workflowName') or payload.get('name') or '<unknown-workflow>'
    conclusion = (payload.get('conclusion') or payload.get('status') or 'unknown').lower()

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

    if conclusion not in failure_outcomes:
        non_failure_runs += 1
        continue

    started = parse_ts(payload.get('runStartedAt') or payload.get('startedAt') or payload.get('createdAt'))
    ended = parse_ts(payload.get('updatedAt') or payload.get('completedAt'))
    if not started:
        started = ended
    if not started:
        parse_errors.append(f"{path}: missing start timestamp")
        continue
    if not ended:
        ended = started

    if ended < started:
        ended = started

    run_id = str(payload.get('databaseId') or payload.get('id') or path)
    run_url = payload.get('url')
    branch = payload.get('headBranch') or '<unknown-branch>'

    failures_by_repo[repository].append(
        {
            'run_id': run_id,
            'workflow': workflow,
            'branch': branch,
            'conclusion': conclusion,
            'started': started,
            'ended': ended,
            'url': run_url,
        }
    )

incidents = []
gap_seconds = incident_gap_minutes * 60
incident_sequence = [0]

for repository, runs in failures_by_repo.items():
    runs.sort(key=lambda row: (row['started'], row['ended'], row['workflow'], row['run_id']))
    cluster = []

    def flush_cluster(current_cluster):
        if not current_cluster:
            return
        incident_sequence[0] += 1
        start = current_cluster[0]['started']
        end = max(item['ended'] for item in current_cluster)
        duration_minutes = max(0.0, (end - start).total_seconds() / 60.0)
        workflows = sorted({item['workflow'] for item in current_cluster})
        branches = sorted({item['branch'] for item in current_cluster})
        conclusions = defaultdict(int)
        sample_urls = []
        for item in current_cluster:
            conclusions[item['conclusion']] += 1
            url = item['url']
            if url and len(sample_urls) < 3 and url not in sample_urls:
                sample_urls.append(url)

        failed_runs = len(current_cluster)
        severity = 'ok'
        if failed_runs >= critical_failed_runs or duration_minutes >= critical_duration_minutes:
            severity = 'critical'
        elif failed_runs >= warn_failed_runs or duration_minutes >= warn_duration_minutes:
            severity = 'warn'

        incidents.append(
            {
                'incident_id': f"INC-{incident_sequence[0]:04d}",
                'repository': repository,
                'failed_runs': failed_runs,
                'duration_minutes': round(duration_minutes, 3),
                'start_time': start.isoformat(),
                'end_time': end.isoformat(),
                'workflows': workflows,
                'branches': branches,
                'workflow_count': len(workflows),
                'branch_count': len(branches),
                'conclusions': dict(sorted(conclusions.items())),
                'severity': severity,
                'sample_urls': sample_urls,
            }
        )

    for row in runs:
        if not cluster:
            cluster = [row]
            continue

        gap = (row['started'] - cluster[-1]['started']).total_seconds()
        if gap <= gap_seconds:
            cluster.append(row)
            continue

        flush_cluster(cluster)
        cluster = [row]

    flush_cluster(cluster)

severity_rank = {'critical': 2, 'warn': 1, 'ok': 0}
incidents.sort(
    key=lambda row: (
        -severity_rank[row['severity']],
        -row['failed_runs'],
        -row['duration_minutes'],
        row['repository'],
        row['start_time'],
    )
)

critical_incidents = [row for row in incidents if row['severity'] == 'critical']
warn_incidents = [row for row in incidents if row['severity'] == 'warn']

summary = {
    'files_scanned': len(files),
    'parse_errors': parse_errors,
    'runs_scanned': runs_scanned,
    'runs_filtered': runs_filtered,
    'non_failure_runs': non_failure_runs,
    'incident_count': len(incidents),
    'critical_incident_count': len(critical_incidents),
    'warn_incident_count': len(warn_incidents),
    'top_n': top_n,
    'incident_gap_minutes': incident_gap_minutes,
    'warn_failed_runs': warn_failed_runs,
    'critical_failed_runs': critical_failed_runs,
    'warn_duration_minutes': warn_duration_minutes,
    'critical_duration_minutes': critical_duration_minutes,
    'filters': {
        'repo_match': repo_match_raw or None,
        'repo_exclude': repo_exclude_raw or None,
        'workflow_match': workflow_match_raw or None,
        'workflow_exclude': workflow_exclude_raw or None,
    },
}

if output_format == 'json':
    print(
        json.dumps(
            {
                'summary': summary,
                'incidents': incidents[:top_n],
                'all_incidents': incidents,
                'critical_incidents': critical_incidents,
            },
            indent=2,
            sort_keys=True,
        )
    )
else:
    print('GITHUB ACTIONS INCIDENT TIMELINE AUDIT')
    print('---')
    print(
        'SUMMARY: '
        f"files={summary['files_scanned']} runs={summary['runs_scanned']} runs_filtered={summary['runs_filtered']} "
        f"non_failure_runs={summary['non_failure_runs']} incidents={summary['incident_count']} "
        f"critical_incidents={summary['critical_incident_count']} warn_incidents={summary['warn_incident_count']}"
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
    ]
    active_filters = [f for f in active_filters if f]
    if active_filters:
        print('FILTERS: ' + ' '.join(active_filters))

    print('---')
    print(f"TOP INCIDENT WINDOWS ({min(top_n, len(incidents))})")
    if not incidents:
        print('none')
    else:
        for row in incidents[:top_n]:
            print(
                f"- [{row['severity']}] {row['incident_id']} {row['repository']} "
                f"failed_runs={row['failed_runs']} duration_min={row['duration_minutes']} "
                f"workflows={row['workflow_count']} branches={row['branch_count']} "
                f"window={row['start_time']} -> {row['end_time']}"
            )

sys.exit(1 if (fail_on_critical and critical_incidents) else 0)
PY
