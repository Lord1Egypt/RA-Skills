#!/usr/bin/env bash
set -euo pipefail

RUN_GLOB="${RUN_GLOB:-artifacts/github-actions/*.json}"
TOP_N="${TOP_N:-20}"
OUTPUT_FORMAT="${OUTPUT_FORMAT:-text}"
RECENT_RUNS="${RECENT_RUNS:-4}"
MIN_RECENT_RUNS="${MIN_RECENT_RUNS:-3}"
MIN_BASELINE_RUNS="${MIN_BASELINE_RUNS:-4}"
WARN_SPIKE_PCT="${WARN_SPIKE_PCT:-15}"
CRITICAL_SPIKE_PCT="${CRITICAL_SPIKE_PCT:-30}"
WARN_RECENT_FAILURE_RATE="${WARN_RECENT_FAILURE_RATE:-25}"
CRITICAL_RECENT_FAILURE_RATE="${CRITICAL_RECENT_FAILURE_RATE:-45}"
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

for value_name in TOP_N RECENT_RUNS MIN_RECENT_RUNS MIN_BASELINE_RUNS; do
  value="${!value_name}"
  if ! [[ "$value" =~ ^[0-9]+$ ]] || [[ "$value" -eq 0 ]]; then
    echo "ERROR: $value_name must be a positive integer (got: $value)" >&2
    exit 1
  fi
done

for value_name in WARN_SPIKE_PCT CRITICAL_SPIKE_PCT WARN_RECENT_FAILURE_RATE CRITICAL_RECENT_FAILURE_RATE; do
  value="${!value_name}"
  if ! [[ "$value" =~ ^[0-9]+([.][0-9]+)?$ ]]; then
    echo "ERROR: $value_name must be numeric (got: $value)" >&2
    exit 1
  fi
done

if [[ "$FAIL_ON_CRITICAL" != "0" && "$FAIL_ON_CRITICAL" != "1" ]]; then
  echo "ERROR: FAIL_ON_CRITICAL must be 0 or 1 (got: $FAIL_ON_CRITICAL)" >&2
  exit 1
fi

python3 - "$RUN_GLOB" "$TOP_N" "$OUTPUT_FORMAT" "$RECENT_RUNS" "$MIN_RECENT_RUNS" "$MIN_BASELINE_RUNS" "$WARN_SPIKE_PCT" "$CRITICAL_SPIKE_PCT" "$WARN_RECENT_FAILURE_RATE" "$CRITICAL_RECENT_FAILURE_RATE" "$WORKFLOW_MATCH" "$WORKFLOW_EXCLUDE" "$BRANCH_MATCH" "$BRANCH_EXCLUDE" "$EVENT_MATCH" "$EVENT_EXCLUDE" "$REPO_MATCH" "$REPO_EXCLUDE" "$FAIL_ON_CRITICAL" <<'PY'
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
    recent_runs_raw,
    min_recent_runs_raw,
    min_baseline_runs_raw,
    warn_spike_pct_raw,
    critical_spike_pct_raw,
    warn_recent_failure_rate_raw,
    critical_recent_failure_rate_raw,
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
recent_runs = int(recent_runs_raw)
min_recent_runs = int(min_recent_runs_raw)
min_baseline_runs = int(min_baseline_runs_raw)
warn_spike_pct = float(warn_spike_pct_raw)
critical_spike_pct = float(critical_spike_pct_raw)
warn_recent_failure_rate = float(warn_recent_failure_rate_raw)
critical_recent_failure_rate = float(critical_recent_failure_rate_raw)
fail_on_critical = fail_on_critical_raw == '1'

if critical_spike_pct < warn_spike_pct:
    print('ERROR: CRITICAL_SPIKE_PCT must be >= WARN_SPIKE_PCT', file=sys.stderr)
    sys.exit(1)
if critical_recent_failure_rate < warn_recent_failure_rate:
    print('ERROR: CRITICAL_RECENT_FAILURE_RATE must be >= WARN_RECENT_FAILURE_RATE', file=sys.stderr)
    sys.exit(1)
if recent_runs < min_recent_runs:
    print('ERROR: RECENT_RUNS must be >= MIN_RECENT_RUNS', file=sys.stderr)
    sys.exit(1)


def parse_ts(value, label='timestamp'):
    if not value:
        return None
    raw = str(value).strip()
    if not raw:
        return None
    if raw.endswith('Z'):
        raw = raw[:-1] + '+00:00'
    try:
        dt = datetime.fromisoformat(raw)
    except ValueError:
        print(f'ERROR: invalid {label}: {value!r}', file=sys.stderr)
        sys.exit(1)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def compile_regex(pattern, label):
    if not pattern:
        return None
    try:
        return re.compile(pattern)
    except re.error as exc:
        print(f'ERROR: invalid {label} regex {pattern!r}: {exc}', file=sys.stderr)
        sys.exit(1)


def normalize_repo(raw):
    if isinstance(raw, str) and raw.strip():
        return raw.strip()
    if isinstance(raw, dict):
        return (
            raw.get('nameWithOwner')
            or raw.get('full_name')
            or raw.get('fullName')
            or raw.get('name')
            or '<unknown-repo>'
        )
    return '<unknown-repo>'


def is_failure(conclusion):
    value = (conclusion or '').strip().lower()
    return value in {'failure', 'timed_out', 'cancelled', 'action_required', 'startup_failure'}


workflow_match = compile_regex(workflow_match_raw, 'WORKFLOW_MATCH')
workflow_exclude = compile_regex(workflow_exclude_raw, 'WORKFLOW_EXCLUDE')
branch_match = compile_regex(branch_match_raw, 'BRANCH_MATCH')
branch_exclude = compile_regex(branch_exclude_raw, 'BRANCH_EXCLUDE')
event_match = compile_regex(event_match_raw, 'EVENT_MATCH')
event_exclude = compile_regex(event_exclude_raw, 'EVENT_EXCLUDE')
repo_match = compile_regex(repo_match_raw, 'REPO_MATCH')
repo_exclude = compile_regex(repo_exclude_raw, 'REPO_EXCLUDE')

files = sorted(glob.glob(run_glob, recursive=True))
if not files:
    print(f'ERROR: no files matched RUN_GLOB={run_glob}', file=sys.stderr)
    sys.exit(1)

parse_errors = []
runs_scanned = 0
runs_filtered = 0

agg = defaultdict(list)

for path in files:
    try:
        with open(path, 'r', encoding='utf-8') as fh:
            payload = json.load(fh)
    except Exception as exc:
        parse_errors.append(f'{path}: {exc}')
        continue

    runs_scanned += 1

    workflow = payload.get('workflowName') or payload.get('name') or '<unknown-workflow>'
    branch = payload.get('headBranch') or '<unknown-branch>'
    event = payload.get('event') or '<unknown-event>'
    repository = normalize_repo(payload.get('repository'))

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
    if event_match and not event_match.search(event):
        runs_filtered += 1
        continue
    if event_exclude and event_exclude.search(event):
        runs_filtered += 1
        continue
    if repo_match and not repo_match.search(repository):
        runs_filtered += 1
        continue
    if repo_exclude and repo_exclude.search(repository):
        runs_filtered += 1
        continue

    created_at = parse_ts(payload.get('createdAt') or payload.get('runStartedAt') or payload.get('startedAt'), 'createdAt')
    if created_at is None:
        parse_errors.append(f'{path}: missing createdAt/runStartedAt/startedAt')
        continue

    agg[(repository, workflow, branch, event)].append(
        {
            'created_at': created_at,
            'conclusion': (payload.get('conclusion') or '').strip().lower(),
            'url': payload.get('url') or '',
        }
    )

rows = []
critical_rows = []

for (repository, workflow, branch, event), runs in agg.items():
    runs_sorted = sorted(runs, key=lambda row: row['created_at'])
    if len(runs_sorted) < (min_recent_runs + min_baseline_runs):
        continue

    recent_slice = runs_sorted[-recent_runs:]
    baseline_slice = runs_sorted[:-len(recent_slice)]

    if len(recent_slice) < min_recent_runs or len(baseline_slice) < min_baseline_runs:
        continue

    recent_failures = sum(1 for run in recent_slice if is_failure(run['conclusion']))
    baseline_failures = sum(1 for run in baseline_slice if is_failure(run['conclusion']))

    recent_rate = (recent_failures / len(recent_slice)) * 100.0
    baseline_rate = (baseline_failures / len(baseline_slice)) * 100.0
    spike_pct = recent_rate - baseline_rate

    severity = 'ok'
    if spike_pct >= critical_spike_pct and recent_rate >= critical_recent_failure_rate:
        severity = 'critical'
    elif spike_pct >= warn_spike_pct and recent_rate >= warn_recent_failure_rate:
        severity = 'warn'

    risk_score = max(0.0, (spike_pct * 1.5) + (recent_rate * 0.8) + (recent_failures * 4.0) - (baseline_rate * 0.2))
    latest_run_at = recent_slice[-1]['created_at']

    row = {
        'repository': repository,
        'workflow': workflow,
        'branch': branch,
        'event': event,
        'severity': severity,
        'runs_total': len(runs_sorted),
        'recent_runs': len(recent_slice),
        'baseline_runs': len(baseline_slice),
        'recent_failures': recent_failures,
        'baseline_failures': baseline_failures,
        'recent_failure_rate': round(recent_rate, 3),
        'baseline_failure_rate': round(baseline_rate, 3),
        'failure_rate_spike_pct': round(spike_pct, 3),
        'risk_score': round(risk_score, 3),
        'latest_run_at': latest_run_at.isoformat(),
        'sample_recent_urls': [run['url'] for run in recent_slice if run['url']][:3],
    }

    rows.append(row)
    if severity == 'critical':
        critical_rows.append(row)

rows.sort(
    key=lambda row: (
        -row['risk_score'],
        -row['failure_rate_spike_pct'],
        -row['recent_failure_rate'],
        row['repository'],
        row['workflow'],
        row['branch'],
        row['event'],
    )
)

summary = {
    'files_scanned': len(files),
    'runs_scanned': runs_scanned,
    'runs_filtered': runs_filtered,
    'parse_errors': parse_errors,
    'groups': len(rows),
    'critical_groups': len(critical_rows),
    'top_n': top_n,
    'recent_runs': recent_runs,
    'min_recent_runs': min_recent_runs,
    'min_baseline_runs': min_baseline_runs,
    'warn_spike_pct': warn_spike_pct,
    'critical_spike_pct': critical_spike_pct,
    'warn_recent_failure_rate': warn_recent_failure_rate,
    'critical_recent_failure_rate': critical_recent_failure_rate,
    'evaluated_at': datetime.now(timezone.utc).isoformat(),
    'filters': {
        'workflow_match': workflow_match_raw or None,
        'workflow_exclude': workflow_exclude_raw or None,
        'branch_match': branch_match_raw or None,
        'branch_exclude': branch_exclude_raw or None,
        'event_match': event_match_raw or None,
        'event_exclude': event_exclude_raw or None,
        'repo_match': repo_match_raw or None,
        'repo_exclude': repo_exclude_raw or None,
    },
}

if output_format == 'json':
    print(json.dumps({'summary': summary, 'groups': rows[:top_n], 'all_groups': rows, 'critical_groups': critical_rows}, indent=2, sort_keys=True))
else:
    print('GITHUB ACTIONS FAILURE SPIKE AUDIT')
    print('---')
    print(
        'SUMMARY: '
        f"files={summary['files_scanned']} runs={summary['runs_scanned']} runs_filtered={summary['runs_filtered']} "
        f"groups={summary['groups']} critical_groups={summary['critical_groups']} evaluated_at={summary['evaluated_at']}"
    )

    if parse_errors:
        print('PARSE_ERRORS:')
        for err in parse_errors:
            print(f'- {err}')

    print('---')
    print(f"TOP FAILURE SPIKES ({min(top_n, len(rows))})")
    if not rows:
        print('none')
    else:
        for row in rows[:top_n]:
            print(
                f"- [{row['severity']}] {row['repository']} :: {row['workflow']} :: branch={row['branch']} event={row['event']} "
                f"recent_failure_rate={row['recent_failure_rate']}% baseline_failure_rate={row['baseline_failure_rate']}% "
                f"spike={row['failure_rate_spike_pct']}pp recent_failures={row['recent_failures']}/{row['recent_runs']} risk_score={row['risk_score']}"
            )

sys.exit(1 if (fail_on_critical and critical_rows) else 0)
PY
