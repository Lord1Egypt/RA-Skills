#!/usr/bin/env bash
set -euo pipefail

JUNIT_GLOB="${JUNIT_GLOB:-test-results/**/*.xml}"
TOP_N="${TOP_N:-20}"
OUTPUT_FORMAT="${OUTPUT_FORMAT:-text}"
STACK_LINES="${STACK_LINES:-3}"
FAIL_ON_FAILURES="${FAIL_ON_FAILURES:-0}"

if [[ "$OUTPUT_FORMAT" != "text" && "$OUTPUT_FORMAT" != "json" ]]; then
  echo "ERROR: OUTPUT_FORMAT must be 'text' or 'json' (got: $OUTPUT_FORMAT)" >&2
  exit 1
fi

if ! [[ "$TOP_N" =~ ^[0-9]+$ ]] || [[ "$TOP_N" -eq 0 ]]; then
  echo "ERROR: TOP_N must be a positive integer (got: $TOP_N)" >&2
  exit 1
fi

if ! [[ "$STACK_LINES" =~ ^[0-9]+$ ]]; then
  echo "ERROR: STACK_LINES must be a non-negative integer (got: $STACK_LINES)" >&2
  exit 1
fi

if [[ "$FAIL_ON_FAILURES" != "0" && "$FAIL_ON_FAILURES" != "1" ]]; then
  echo "ERROR: FAIL_ON_FAILURES must be 0 or 1 (got: $FAIL_ON_FAILURES)" >&2
  exit 1
fi

python3 - "$JUNIT_GLOB" "$TOP_N" "$OUTPUT_FORMAT" "$STACK_LINES" "$FAIL_ON_FAILURES" <<'PY'
import glob
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict

junit_glob = sys.argv[1]
top_n = int(sys.argv[2])
output_format = sys.argv[3]
stack_lines = int(sys.argv[4])
fail_on_failures = sys.argv[5] == '1'

files = sorted(glob.glob(junit_glob, recursive=True))
if not files:
    print(f'ERROR: no JUnit files matched JUNIT_GLOB={junit_glob}', file=sys.stderr)
    sys.exit(1)


def normalize_text(text: str) -> str:
    if not text:
        return ''
    value = text.strip().lower()
    value = re.sub(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', '<uuid>', value)
    value = re.sub(r'0x[0-9a-f]+', '0x<hex>', value)
    value = re.sub(r'\b\d+\b', '<num>', value)
    value = re.sub(r':[0-9]+', ':<n>', value)
    value = re.sub(r'\s+', ' ', value)
    return value


def extract_failure_node(case):
    failure = case.find('failure')
    if failure is not None:
        return 'failure', failure
    error = case.find('error')
    if error is not None:
        return 'error', error
    return None, None


def normalized_stack_head(raw: str, max_lines: int) -> str:
    if max_lines == 0:
        return ''
    lines = [normalize_text(line) for line in (raw or '').splitlines()]
    lines = [line for line in lines if line]
    return '\n'.join(lines[:max_lines])


records = []
parse_errors = []
for path in files:
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        parse_errors.append(f'{path}: {exc}')
        continue

    for case in root.findall('.//testcase'):
        kind, node = extract_failure_node(case)
        if node is None:
            continue

        classname = case.attrib.get('classname', '<no-classname>')
        name = case.attrib.get('name', '<unnamed>')
        test_id = f'{classname}::{name}'

        failure_type = normalize_text(node.attrib.get('type', ''))
        message = normalize_text(node.attrib.get('message', '') or (node.text or '').strip().splitlines()[0] if (node.text or '').strip() else '')
        stack_head = normalized_stack_head(node.text or '', stack_lines)

        seed = f'{kind}|{failure_type}|{message}|{stack_head}'
        digest = hashlib.sha1(seed.encode('utf-8')).hexdigest()[:12]

        records.append({
            'fingerprint': digest,
            'kind': kind,
            'type': failure_type or '<none>',
            'message': message or '<none>',
            'stack_head': stack_head,
            'test_id': test_id,
            'file': path,
        })

summary = {
    'files_scanned': len(files),
    'parse_errors': parse_errors,
    'failure_rows': len(records),
    'unique_fingerprints': 0,
    'top_n': top_n,
}

if not records:
    summary['unique_fingerprints'] = 0
    if output_format == 'json':
        print(json.dumps({'summary': summary, 'fingerprints': [], 'records': []}, indent=2, sort_keys=True))
    else:
        print('JUNIT FAILURE FINGERPRINT REPORT')
        print('---')
        print(f"SUMMARY: files={summary['files_scanned']} failures=0 fingerprints=0")
        if parse_errors:
            print('PARSE_ERRORS:')
            for err in parse_errors:
                print(f'- {err}')
        print('No failing/error testcases found.')
    sys.exit(0)

clusters = defaultdict(lambda: {
    'occurrences': 0,
    'tests': set(),
    'files': set(),
    'kind': '',
    'type': '',
    'message': '',
    'stack_head': '',
})

for row in records:
    bucket = clusters[row['fingerprint']]
    bucket['occurrences'] += 1
    bucket['tests'].add(row['test_id'])
    bucket['files'].add(row['file'])
    bucket['kind'] = row['kind']
    bucket['type'] = row['type']
    bucket['message'] = row['message']
    bucket['stack_head'] = row['stack_head']

fingerprints = []
for fp, item in clusters.items():
    fingerprints.append({
        'fingerprint': fp,
        'occurrences': item['occurrences'],
        'unique_tests': len(item['tests']),
        'files_seen': len(item['files']),
        'kind': item['kind'],
        'type': item['type'],
        'message': item['message'],
        'stack_head': item['stack_head'],
        'sample_tests': sorted(item['tests'])[:5],
    })

fingerprints.sort(key=lambda x: (-x['occurrences'], -x['unique_tests'], x['fingerprint']))
summary['unique_fingerprints'] = len(fingerprints)

if output_format == 'json':
    print(json.dumps({'summary': summary, 'fingerprints': fingerprints[:top_n], 'records': records}, indent=2, sort_keys=True))
else:
    print('JUNIT FAILURE FINGERPRINT REPORT')
    print('---')
    print(
        'SUMMARY: '
        f"files={summary['files_scanned']} failures={summary['failure_rows']} "
        f"fingerprints={summary['unique_fingerprints']}"
    )
    if parse_errors:
        print('PARSE_ERRORS:')
        for err in parse_errors:
            print(f'- {err}')

    print('---')
    print(f"TOP FINGERPRINTS ({min(top_n, len(fingerprints))})")
    for row in fingerprints[:top_n]:
        print(
            f"- {row['fingerprint']} occurrences={row['occurrences']} "
            f"unique_tests={row['unique_tests']} kind={row['kind']}"
        )
        print(f"  type={row['type']}")
        print(f"  message={row['message']}")
        if row['stack_head']:
            print('  stack_head:')
            for line in row['stack_head'].splitlines():
                print(f'    {line}')
        print(f"  sample_tests={', '.join(row['sample_tests'])}")

if fail_on_failures and records:
    sys.exit(1)

sys.exit(0)
PY
