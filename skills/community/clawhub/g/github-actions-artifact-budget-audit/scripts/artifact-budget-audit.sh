#!/usr/bin/env bash
set -euo pipefail

ARTIFACT_GLOB="${ARTIFACT_GLOB:-artifacts/github-actions-artifacts/*.json}"
TOP_N="${TOP_N:-20}"
OUTPUT_FORMAT="${OUTPUT_FORMAT:-text}"
WARN_MB="${WARN_MB:-250}"
CRITICAL_MB="${CRITICAL_MB:-750}"
SOON_EXPIRES_DAYS="${SOON_EXPIRES_DAYS:-7}"
FAIL_ON_CRITICAL="${FAIL_ON_CRITICAL:-0}"
REPO_MATCH="${REPO_MATCH:-}"
REPO_EXCLUDE="${REPO_EXCLUDE:-}"
ARTIFACT_MATCH="${ARTIFACT_MATCH:-}"
ARTIFACT_EXCLUDE="${ARTIFACT_EXCLUDE:-}"

if [[ "$OUTPUT_FORMAT" != "text" && "$OUTPUT_FORMAT" != "json" ]]; then
  echo "ERROR: OUTPUT_FORMAT must be 'text' or 'json' (got: $OUTPUT_FORMAT)" >&2
  exit 1
fi

if ! [[ "$TOP_N" =~ ^[0-9]+$ ]] || [[ "$TOP_N" -eq 0 ]]; then
  echo "ERROR: TOP_N must be a positive integer (got: $TOP_N)" >&2
  exit 1
fi

if ! [[ "$WARN_MB" =~ ^[0-9]+([.][0-9]+)?$ ]]; then
  echo "ERROR: WARN_MB must be a non-negative number (got: $WARN_MB)" >&2
  exit 1
fi

if ! [[ "$CRITICAL_MB" =~ ^[0-9]+([.][0-9]+)?$ ]]; then
  echo "ERROR: CRITICAL_MB must be a non-negative number (got: $CRITICAL_MB)" >&2
  exit 1
fi

if ! [[ "$SOON_EXPIRES_DAYS" =~ ^[0-9]+$ ]]; then
  echo "ERROR: SOON_EXPIRES_DAYS must be a non-negative integer (got: $SOON_EXPIRES_DAYS)" >&2
  exit 1
fi

if [[ "$FAIL_ON_CRITICAL" != "0" && "$FAIL_ON_CRITICAL" != "1" ]]; then
  echo "ERROR: FAIL_ON_CRITICAL must be 0 or 1 (got: $FAIL_ON_CRITICAL)" >&2
  exit 1
fi

python3 - "$ARTIFACT_GLOB" "$TOP_N" "$OUTPUT_FORMAT" "$WARN_MB" "$CRITICAL_MB" "$SOON_EXPIRES_DAYS" "$FAIL_ON_CRITICAL" "$REPO_MATCH" "$REPO_EXCLUDE" "$ARTIFACT_MATCH" "$ARTIFACT_EXCLUDE" <<'PY'
import glob
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone

artifact_glob = sys.argv[1]
top_n = int(sys.argv[2])
output_format = sys.argv[3]
warn_mb = float(sys.argv[4])
critical_mb = float(sys.argv[5])
soon_days = int(sys.argv[6])
fail_on_critical = sys.argv[7] == '1'
repo_match_raw = sys.argv[8]
repo_exclude_raw = sys.argv[9]
artifact_match_raw = sys.argv[10]
artifact_exclude_raw = sys.argv[11]

if critical_mb < warn_mb:
    print('ERROR: CRITICAL_MB must be >= WARN_MB', file=sys.stderr)
    sys.exit(1)


def compile_optional_regex(pattern, label):
    if not pattern:
        return None
    try:
        return re.compile(pattern)
    except re.error as exc:
        print(f"ERROR: invalid {label} regex {pattern!r}: {exc}", file=sys.stderr)
        sys.exit(1)


repo_match = compile_optional_regex(repo_match_raw, 'REPO_MATCH')
repo_exclude = compile_optional_regex(repo_exclude_raw, 'REPO_EXCLUDE')
artifact_match = compile_optional_regex(artifact_match_raw, 'ARTIFACT_MATCH')
artifact_exclude = compile_optional_regex(artifact_exclude_raw, 'ARTIFACT_EXCLUDE')


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


def repo_name(payload, fallback):
    raw_repo = payload.get('repository')
    if isinstance(raw_repo, str) and raw_repo.strip():
        return raw_repo.strip()
    if isinstance(raw_repo, dict):
        for key in ('nameWithOwner', 'full_name', 'fullName', 'name'):
            val = raw_repo.get(key)
            if isinstance(val, str) and val.strip():
                return val.strip()
    return fallback


files = sorted(glob.glob(artifact_glob, recursive=True))
if not files:
    print(f"ERROR: no files matched ARTIFACT_GLOB={artifact_glob}", file=sys.stderr)
    sys.exit(1)

now = datetime.now(timezone.utc)
soon_cutoff = now + timedelta(days=soon_days)

parse_errors = []
files_scanned = 0
records_scanned = 0
records_filtered = 0
records_missing_size = 0
critical_instances = []

agg = defaultdict(lambda: {
    'repository': None,
    'artifact_name': None,
    'size_bytes': [],
    'expired_count': 0,
    'soon_expire_count': 0,
    'run_ids': set(),
    'sample_urls': [],
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
    repository = repo_name(payload if isinstance(payload, dict) else {}, default_repo)

    artifacts = None
    if isinstance(payload, dict):
        artifacts = payload.get('artifacts')
    elif isinstance(payload, list):
        artifacts = payload

    if not isinstance(artifacts, list):
        parse_errors.append(f"{path}: missing artifacts[]")
        continue

    for row in artifacts:
        if not isinstance(row, dict):
            continue

        records_scanned += 1

        artifact_name_value = row.get('name')
        artifact_name = str(artifact_name_value).strip() if artifact_name_value is not None else ''
        if not artifact_name:
            artifact_name = '<unnamed-artifact>'

        if repo_match and not repo_match.search(repository):
            records_filtered += 1
            continue
        if repo_exclude and repo_exclude.search(repository):
            records_filtered += 1
            continue
        if artifact_match and not artifact_match.search(artifact_name):
            records_filtered += 1
            continue
        if artifact_exclude and artifact_exclude.search(artifact_name):
            records_filtered += 1
            continue

        size_bytes = row.get('size_in_bytes')
        try:
            size_bytes = int(size_bytes)
        except (TypeError, ValueError):
            records_missing_size += 1
            continue

        if size_bytes < 0:
            records_missing_size += 1
            continue

        expired = bool(row.get('expired', False))
        expires_at = parse_ts(row.get('expires_at') or row.get('expiresAt'))
        soon_expire = (expires_at is not None and expires_at <= soon_cutoff and not expired)

        run_data = row.get('workflow_run') or {}
        run_id = run_data.get('id') or row.get('workflow_run_id') or row.get('id') or '<unknown-run>'

        key = (repository, artifact_name)
        bucket = agg[key]
        bucket['repository'] = repository
        bucket['artifact_name'] = artifact_name
        bucket['size_bytes'].append(size_bytes)
        bucket['run_ids'].add(str(run_id))
        if expired:
            bucket['expired_count'] += 1
        if soon_expire:
            bucket['soon_expire_count'] += 1

        url = row.get('archive_download_url') or row.get('url')
        if url and len(bucket['sample_urls']) < 3 and url not in bucket['sample_urls']:
            bucket['sample_urls'].append(url)

        size_mb = size_bytes / (1024 * 1024)
        if size_mb >= critical_mb:
            critical_instances.append({
                'repository': repository,
                'artifact_name': artifact_name,
                'artifact_id': row.get('id'),
                'run_id': run_id,
                'size_mb': round(size_mb, 3),
                'expired': expired,
                'expires_at': row.get('expires_at') or row.get('expiresAt'),
                'url': url,
            })

groups = []
for bucket in agg.values():
    sizes = bucket['size_bytes']
    if not sizes:
        continue
    max_mb = max(sizes) / (1024 * 1024)
    avg_mb = (sum(sizes) / len(sizes)) / (1024 * 1024)
    total_mb = (sum(sizes)) / (1024 * 1024)

    severity = 'ok'
    if max_mb >= critical_mb:
        severity = 'critical'
    elif max_mb >= warn_mb:
        severity = 'warn'

    groups.append({
        'repository': bucket['repository'],
        'artifact_name': bucket['artifact_name'],
        'instances': len(sizes),
        'run_count': len(bucket['run_ids']),
        'max_mb': round(max_mb, 3),
        'avg_mb': round(avg_mb, 3),
        'total_mb': round(total_mb, 3),
        'expired_count': bucket['expired_count'],
        'soon_expire_count': bucket['soon_expire_count'],
        'severity': severity,
        'sample_urls': bucket['sample_urls'],
    })

groups.sort(key=lambda row: (-row['max_mb'], -row['total_mb'], row['repository'], row['artifact_name']))

summary = {
    'files_matched': len(files),
    'files_scanned': files_scanned,
    'parse_errors': parse_errors,
    'records_scanned': records_scanned,
    'records_filtered': records_filtered,
    'records_missing_size': records_missing_size,
    'groups': len(groups),
    'critical_instances': len(critical_instances),
    'warn_mb': warn_mb,
    'critical_mb': critical_mb,
    'soon_expires_days': soon_days,
    'top_n': top_n,
    'filters': {
        'repo_match': repo_match_raw or None,
        'repo_exclude': repo_exclude_raw or None,
        'artifact_match': artifact_match_raw or None,
        'artifact_exclude': artifact_exclude_raw or None,
    }
}

if output_format == 'json':
    print(json.dumps({'summary': summary, 'groups': groups[:top_n], 'all_groups': groups, 'critical_instances': critical_instances}, indent=2, sort_keys=True))
else:
    print('GITHUB ACTIONS ARTIFACT BUDGET AUDIT')
    print('---')
    print(
        'SUMMARY: '
        f"files={summary['files_scanned']}/{summary['files_matched']} artifacts={summary['records_scanned']} "
        f"filtered={summary['records_filtered']} missing_size={summary['records_missing_size']} "
        f"groups={summary['groups']} critical_instances={summary['critical_instances']}"
    )

    if parse_errors:
        print('PARSE_ERRORS:')
        for err in parse_errors:
            print(f"- {err}")

    active_filters = [
        f"repo={repo_match_raw}" if repo_match_raw else None,
        f"repo!={repo_exclude_raw}" if repo_exclude_raw else None,
        f"artifact={artifact_match_raw}" if artifact_match_raw else None,
        f"artifact!={artifact_exclude_raw}" if artifact_exclude_raw else None,
    ]
    active_filters = [f for f in active_filters if f]
    if active_filters:
        print('FILTERS: ' + ' '.join(active_filters))

    print('---')
    print(f"TOP ARTIFACT HOTSPOTS ({min(top_n, len(groups))})")
    if not groups:
        print('none')
    else:
        for row in groups[:top_n]:
            print(
                f"- [{row['severity']}] {row['repository']} :: {row['artifact_name']} "
                f"max_mb={row['max_mb']} avg_mb={row['avg_mb']} total_mb={row['total_mb']} "
                f"instances={row['instances']} runs={row['run_count']} "
                f"expired={row['expired_count']} soon_expire={row['soon_expire_count']}"
            )

sys.exit(1 if (fail_on_critical and critical_instances) else 0)
PY
