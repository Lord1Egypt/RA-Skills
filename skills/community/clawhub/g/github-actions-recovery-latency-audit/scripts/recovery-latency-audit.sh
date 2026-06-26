#!/usr/bin/env bash
set -euo pipefail

RUN_GLOB="${RUN_GLOB:-artifacts/github-actions/*.json}"
TOP_N="${TOP_N:-20}"
OUTPUT_FORMAT="${OUTPUT_FORMAT:-text}"
MIN_RUNS="${MIN_RUNS:-4}"
WARN_P95_HOURS="${WARN_P95_HOURS:-6}"
CRITICAL_P95_HOURS="${CRITICAL_P95_HOURS:-18}"
WARN_OPEN_HOURS="${WARN_OPEN_HOURS:-12}"
CRITICAL_OPEN_HOURS="${CRITICAL_OPEN_HOURS:-36}"
WARN_OPEN_INCIDENTS="${WARN_OPEN_INCIDENTS:-1}"
CRITICAL_OPEN_INCIDENTS="${CRITICAL_OPEN_INCIDENTS:-2}"
NOW_ISO="${NOW_ISO:-}"
WORKFLOW_MATCH="${WORKFLOW_MATCH:-}"
WORKFLOW_EXCLUDE="${WORKFLOW_EXCLUDE:-}"
BRANCH_MATCH="${BRANCH_MATCH:-}"
BRANCH_EXCLUDE="${BRANCH_EXCLUDE:-}"
EVENT_MATCH="${EVENT_MATCH:-}"
EVENT_EXCLUDE="${EVENT_EXCLUDE:-}"
REPO_MATCH="${REPO_MATCH:-}"
REPO_EXCLUDE="${REPO_EXCLUDE:-}"
FAIL_ON_CRITICAL="${FAIL_ON_CRITICAL:-0}"

if [[ "$OUTPUT_FORMAT" != "text" && "$OUTPUT_FORMAT" != "json" ]]; then
  echo "ERROR: OUTPUT_FORMAT must be 'text' or 'json' (got: $OUTPUT_FORMAT)" >&2
  exit 1
fi

for int_var in TOP_N MIN_RUNS WARN_OPEN_INCIDENTS CRITICAL_OPEN_INCIDENTS; do
  val="${!int_var}"
  if ! [[ "$val" =~ ^[0-9]+$ ]]; then
    echo "ERROR: $int_var must be a non-negative integer (got: $val)" >&2
    exit 1
  fi
done

if [[ "$TOP_N" -eq 0 ]]; then
  echo "ERROR: TOP_N must be a positive integer" >&2
  exit 1
fi

for num_var in WARN_P95_HOURS CRITICAL_P95_HOURS WARN_OPEN_HOURS CRITICAL_OPEN_HOURS; do
  val="${!num_var}"
  if ! [[ "$val" =~ ^[0-9]+([.][0-9]+)?$ ]]; then
    echo "ERROR: $num_var must be numeric (got: $val)" >&2
    exit 1
  fi
done

if [[ "$FAIL_ON_CRITICAL" != "0" && "$FAIL_ON_CRITICAL" != "1" ]]; then
  echo "ERROR: FAIL_ON_CRITICAL must be 0 or 1 (got: $FAIL_ON_CRITICAL)" >&2
  exit 1
fi

python3 - \
  "$RUN_GLOB" "$TOP_N" "$OUTPUT_FORMAT" "$MIN_RUNS" \
  "$WARN_P95_HOURS" "$CRITICAL_P95_HOURS" "$WARN_OPEN_HOURS" "$CRITICAL_OPEN_HOURS" \
  "$WARN_OPEN_INCIDENTS" "$CRITICAL_OPEN_INCIDENTS" "$NOW_ISO" \
  "$WORKFLOW_MATCH" "$WORKFLOW_EXCLUDE" "$BRANCH_MATCH" "$BRANCH_EXCLUDE" \
  "$EVENT_MATCH" "$EVENT_EXCLUDE" "$REPO_MATCH" "$REPO_EXCLUDE" "$FAIL_ON_CRITICAL" <<'PY'
import glob
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone

(
    run_glob,
    top_n_raw,
    output_format,
    min_runs_raw,
    warn_p95_hours_raw,
    critical_p95_hours_raw,
    warn_open_hours_raw,
    critical_open_hours_raw,
    warn_open_incidents_raw,
    critical_open_incidents_raw,
    now_iso,
    workflow_match_raw,
    workflow_exclude_raw,
    branch_match_raw,
    branch_exclude_raw,
    event_match_raw,
    event_exclude_raw,
    repo_match_raw,
    repo_exclude_raw,
    fail_on_critical_raw,
) = sys.argv[1:]

top_n = int(top_n_raw)
min_runs = int(min_runs_raw)
warn_p95_hours = float(warn_p95_hours_raw)
critical_p95_hours = float(critical_p95_hours_raw)
warn_open_hours = float(warn_open_hours_raw)
critical_open_hours = float(critical_open_hours_raw)
warn_open_incidents = int(warn_open_incidents_raw)
critical_open_incidents = int(critical_open_incidents_raw)
fail_on_critical = fail_on_critical_raw == '1'

if critical_p95_hours < warn_p95_hours:
    print('ERROR: CRITICAL_P95_HOURS must be >= WARN_P95_HOURS', file=sys.stderr)
    sys.exit(1)
if critical_open_hours < warn_open_hours:
    print('ERROR: CRITICAL_OPEN_HOURS must be >= WARN_OPEN_HOURS', file=sys.stderr)
    sys.exit(1)
if critical_open_incidents < warn_open_incidents:
    print('ERROR: CRITICAL_OPEN_INCIDENTS must be >= WARN_OPEN_INCIDENTS', file=sys.stderr)
    sys.exit(1)


def parse_ts(value):
    if not value:
        return None
    text = str(value)
    if text.endswith('Z'):
        text = text[:-1] + '+00:00'
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


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
branch_match = compile_optional_regex(branch_match_raw, 'BRANCH_MATCH')
branch_exclude = compile_optional_regex(branch_exclude_raw, 'BRANCH_EXCLUDE')
event_match = compile_optional_regex(event_match_raw, 'EVENT_MATCH')
event_exclude = compile_optional_regex(event_exclude_raw, 'EVENT_EXCLUDE')
repo_match = compile_optional_regex(repo_match_raw, 'REPO_MATCH')
repo_exclude = compile_optional_regex(repo_exclude_raw, 'REPO_EXCLUDE')

now_dt = parse_ts(now_iso) if now_iso else datetime.now(timezone.utc)
if now_iso and not now_dt:
    print(f"ERROR: NOW_ISO is not valid ISO-8601 (got: {now_iso})", file=sys.stderr)
    sys.exit(1)

failure_conclusions = {
    'failure',
    'timed_out',
    'cancelled',
    'startup_failure',
    'action_required',
    'stale',
}
success_conclusions = {'success'}

files = sorted(glob.glob(run_glob, recursive=True))
if not files:
    print(f"ERROR: no files matched RUN_GLOB={run_glob}", file=sys.stderr)
    sys.exit(1)

summary = {
    'files_scanned': len(files),
    'parse_errors': [],
    'runs_scanned': 0,
    'runs_filtered': 0,
    'groups_total': 0,
    'groups_ranked': 0,
    'incidents_total': 0,
    'incidents_closed': 0,
    'incidents_open': 0,
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
    event = payload.get('event') or '<unknown-event>'
    conclusion = str(payload.get('conclusion') or 'unknown').lower()
    created_at = parse_ts(payload.get('createdAt') or payload.get('created_at') or payload.get('updatedAt') or payload.get('updated_at'))

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
    if event_match and not event_match.search(event):
        summary['runs_filtered'] += 1
        continue
    if event_exclude and event_exclude.search(event):
        summary['runs_filtered'] += 1
        continue

    if not created_at:
        summary['parse_errors'].append(f"{path}: missing/invalid createdAt")
        continue

    groups[(repository, workflow, branch, event)].append({
        'created_at': created_at,
        'conclusion': conclusion,
        'run_id': payload.get('databaseId') or payload.get('id') or path,
        'url': payload.get('url'),
    })

severity_rank = {'critical': 2, 'warn': 1, 'ok': 0}
ranked_groups = []
critical_groups = []

for key, runs in groups.items():
    summary['groups_total'] += 1
    if len(runs) < min_runs:
        continue

    repository, workflow, branch, event = key
    ordered = sorted(runs, key=lambda item: item['created_at'])

    open_incident = None
    incidents = []
    latest_run = ordered[-1]

    for run in ordered:
        conc = run['conclusion']
        ts = run['created_at']

        if conc in failure_conclusions:
            if open_incident is None:
                open_incident = {
                    'start_at': ts,
                    'start_run_id': run['run_id'],
                    'start_url': run['url'],
                    'failed_runs': 1,
                    'last_failure_at': ts,
                }
            else:
                open_incident['failed_runs'] += 1
                open_incident['last_failure_at'] = ts
            continue

        if conc in success_conclusions and open_incident is not None:
            recovery_hours = max((ts - open_incident['start_at']).total_seconds() / 3600.0, 0.0)
            incidents.append({
                'status': 'closed',
                'start_at': open_incident['start_at'],
                'end_at': ts,
                'recovery_hours': round(recovery_hours, 3),
                'failed_runs': open_incident['failed_runs'],
                'start_run_id': open_incident['start_run_id'],
                'end_run_id': run['run_id'],
                'start_url': open_incident['start_url'],
                'end_url': run['url'],
            })
            open_incident = None

    if open_incident is not None:
        oldest_open_hours = max((now_dt - open_incident['start_at']).total_seconds() / 3600.0, 0.0)
        incidents.append({
            'status': 'open',
            'start_at': open_incident['start_at'],
            'end_at': None,
            'recovery_hours': None,
            'open_hours': round(oldest_open_hours, 3),
            'failed_runs': open_incident['failed_runs'],
            'start_run_id': open_incident['start_run_id'],
            'start_url': open_incident['start_url'],
        })

    if not incidents:
        continue

    closed = [x for x in incidents if x['status'] == 'closed']
    open_rows = [x for x in incidents if x['status'] == 'open']

    recovery_values = sorted(x['recovery_hours'] for x in closed)
    p95_recovery = None
    median_recovery = None
    max_recovery = None
    if recovery_values:
        idx95 = int((len(recovery_values) - 1) * 0.95)
        p95_recovery = round(recovery_values[idx95], 3)
        mid = len(recovery_values) // 2
        if len(recovery_values) % 2 == 0:
            median_recovery = round((recovery_values[mid - 1] + recovery_values[mid]) / 2.0, 3)
        else:
            median_recovery = round(recovery_values[mid], 3)
        max_recovery = round(recovery_values[-1], 3)

    oldest_open_hours = max((x['open_hours'] for x in open_rows), default=0.0)

    severity = 'ok'
    if (
        len(open_rows) >= critical_open_incidents
        or oldest_open_hours >= critical_open_hours
        or (p95_recovery is not None and p95_recovery >= critical_p95_hours)
    ):
        severity = 'critical'
    elif (
        len(open_rows) >= warn_open_incidents
        or oldest_open_hours >= warn_open_hours
        or (p95_recovery is not None and p95_recovery >= warn_p95_hours)
    ):
        severity = 'warn'

    row = {
        'repository': repository,
        'workflow': workflow,
        'branch': branch,
        'event': event,
        'runs_considered': len(ordered),
        'latest_conclusion': latest_run['conclusion'],
        'latest_run_id': latest_run['run_id'],
        'incidents_total': len(incidents),
        'closed_incidents': len(closed),
        'open_incidents': len(open_rows),
        'median_recovery_hours': median_recovery,
        'p95_recovery_hours': p95_recovery,
        'max_recovery_hours': max_recovery,
        'oldest_open_hours': round(oldest_open_hours, 3),
        'recent_incidents': [
            {
                'status': incident['status'],
                'start_at': incident['start_at'].isoformat().replace('+00:00', 'Z'),
                'end_at': incident['end_at'].isoformat().replace('+00:00', 'Z') if incident['end_at'] else None,
                'recovery_hours': incident.get('recovery_hours'),
                'open_hours': incident.get('open_hours'),
                'failed_runs': incident['failed_runs'],
                'start_run_id': incident['start_run_id'],
                'end_run_id': incident.get('end_run_id'),
                'start_url': incident.get('start_url'),
                'end_url': incident.get('end_url'),
            }
            for incident in incidents[-3:]
        ],
        'severity': severity,
    }

    summary['incidents_total'] += len(incidents)
    summary['incidents_closed'] += len(closed)
    summary['incidents_open'] += len(open_rows)
    if severity == 'warn':
        summary['warn_groups'] += 1
    elif severity == 'critical':
        summary['critical_groups'] += 1

    ranked_groups.append(row)
    if severity == 'critical':
        critical_groups.append(row)

ranked_groups.sort(
    key=lambda row: (
        -severity_rank[row['severity']],
        -row['open_incidents'],
        -(row['oldest_open_hours'] or 0),
        -(row['p95_recovery_hours'] or 0),
        -(row['max_recovery_hours'] or 0),
        row['repository'],
        row['workflow'],
    )
)
summary['groups_ranked'] = len(ranked_groups)

result = {
    'summary': {
        **summary,
        'top_n': top_n,
        'min_runs': min_runs,
        'thresholds': {
            'warn_p95_hours': warn_p95_hours,
            'critical_p95_hours': critical_p95_hours,
            'warn_open_hours': warn_open_hours,
            'critical_open_hours': critical_open_hours,
            'warn_open_incidents': warn_open_incidents,
            'critical_open_incidents': critical_open_incidents,
        },
        'filters': {
            'repo_match': repo_match_raw or None,
            'repo_exclude': repo_exclude_raw or None,
            'workflow_match': workflow_match_raw or None,
            'workflow_exclude': workflow_exclude_raw or None,
            'branch_match': branch_match_raw or None,
            'branch_exclude': branch_exclude_raw or None,
            'event_match': event_match_raw or None,
            'event_exclude': event_exclude_raw or None,
        },
        'now_iso': now_dt.isoformat().replace('+00:00', 'Z'),
    },
    'groups': ranked_groups[:top_n],
    'all_groups': ranked_groups,
    'critical_groups': critical_groups,
}

if output_format == 'json':
    print(json.dumps(result, indent=2, sort_keys=True))
else:
    print('GITHUB ACTIONS RECOVERY LATENCY AUDIT')
    print('---')
    print(
        'SUMMARY: '
        f"files={summary['files_scanned']} runs={summary['runs_scanned']} runs_filtered={summary['runs_filtered']} "
        f"groups_total={summary['groups_total']} groups_ranked={summary['groups_ranked']} "
        f"incidents_total={summary['incidents_total']} closed={summary['incidents_closed']} open={summary['incidents_open']} "
        f"warn_groups={summary['warn_groups']} critical_groups={summary['critical_groups']}"
    )
    print(
        'THRESHOLDS: '
        f"warn_p95_hours={warn_p95_hours} critical_p95_hours={critical_p95_hours} "
        f"warn_open_hours={warn_open_hours} critical_open_hours={critical_open_hours} "
        f"warn_open_incidents={warn_open_incidents} critical_open_incidents={critical_open_incidents}"
    )

    if summary['parse_errors']:
        print('PARSE_ERRORS:')
        for err in summary['parse_errors']:
            print(f"- {err}")

    print('---')
    print(f"TOP RECOVERY-RISK GROUPS ({min(top_n, len(ranked_groups))})")
    if not ranked_groups:
        print('none')
    else:
        for row in ranked_groups[:top_n]:
            print(
                f"- [{row['severity']}] {row['repository']} :: {row['workflow']} :: branch={row['branch']} event={row['event']} "
                f"open_incidents={row['open_incidents']} oldest_open_hours={row['oldest_open_hours']} "
                f"p95_recovery_hours={row['p95_recovery_hours'] if row['p95_recovery_hours'] is not None else 'n/a'}"
            )

sys.exit(1 if (fail_on_critical and critical_groups) else 0)
PY
