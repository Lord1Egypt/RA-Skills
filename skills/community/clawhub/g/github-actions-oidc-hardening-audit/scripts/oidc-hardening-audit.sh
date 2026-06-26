#!/usr/bin/env bash
set -euo pipefail

WORKFLOW_GLOB="${WORKFLOW_GLOB:-.github/workflows/*.y*ml}"
TOP_N="${TOP_N:-20}"
OUTPUT_FORMAT="${OUTPUT_FORMAT:-text}"
WARN_SCORE="${WARN_SCORE:-3}"
CRITICAL_SCORE="${CRITICAL_SCORE:-7}"
ALLOW_REF_REGEX="${ALLOW_REF_REGEX:-}"
WORKFLOW_FILE_MATCH="${WORKFLOW_FILE_MATCH:-}"
WORKFLOW_FILE_EXCLUDE="${WORKFLOW_FILE_EXCLUDE:-}"
FAIL_ON_CRITICAL="${FAIL_ON_CRITICAL:-0}"

if [[ "$OUTPUT_FORMAT" != "text" && "$OUTPUT_FORMAT" != "json" ]]; then
  echo "ERROR: OUTPUT_FORMAT must be 'text' or 'json' (got: $OUTPUT_FORMAT)" >&2
  exit 1
fi

for value_name in TOP_N WARN_SCORE CRITICAL_SCORE FAIL_ON_CRITICAL; do
  value="${!value_name}"
  if ! [[ "$value" =~ ^[0-9]+$ ]]; then
    echo "ERROR: $value_name must be a non-negative integer (got: $value)" >&2
    exit 1
  fi
done

if [[ "$TOP_N" -eq 0 ]]; then
  echo "ERROR: TOP_N must be >= 1" >&2
  exit 1
fi

if [[ "$WARN_SCORE" -gt "$CRITICAL_SCORE" ]]; then
  echo "ERROR: WARN_SCORE must be <= CRITICAL_SCORE" >&2
  exit 1
fi

python3 - "$WORKFLOW_GLOB" "$TOP_N" "$OUTPUT_FORMAT" "$WARN_SCORE" "$CRITICAL_SCORE" "$ALLOW_REF_REGEX" "$WORKFLOW_FILE_MATCH" "$WORKFLOW_FILE_EXCLUDE" "$FAIL_ON_CRITICAL" <<'PY'
import glob
import json
import re
import sys
from pathlib import Path

(
    workflow_glob,
    top_n_raw,
    output_format,
    warn_score_raw,
    critical_score_raw,
    allow_ref_regex_raw,
    workflow_file_match_raw,
    workflow_file_exclude_raw,
    fail_on_critical_raw,
) = sys.argv[1:]

top_n = int(top_n_raw)
warn_score = int(warn_score_raw)
critical_score = int(critical_score_raw)
fail_on_critical = fail_on_critical_raw == '1'

allow_ref_regex = None
if allow_ref_regex_raw:
    try:
        allow_ref_regex = re.compile(allow_ref_regex_raw)
    except re.error as exc:
        print(f"ERROR: invalid ALLOW_REF_REGEX {allow_ref_regex_raw!r}: {exc}", file=sys.stderr)
        sys.exit(1)

workflow_file_match = None
if workflow_file_match_raw:
    try:
        workflow_file_match = re.compile(workflow_file_match_raw)
    except re.error as exc:
        print(f"ERROR: invalid WORKFLOW_FILE_MATCH {workflow_file_match_raw!r}: {exc}", file=sys.stderr)
        sys.exit(1)

workflow_file_exclude = None
if workflow_file_exclude_raw:
    try:
        workflow_file_exclude = re.compile(workflow_file_exclude_raw)
    except re.error as exc:
        print(f"ERROR: invalid WORKFLOW_FILE_EXCLUDE {workflow_file_exclude_raw!r}: {exc}", file=sys.stderr)
        sys.exit(1)

files = sorted(glob.glob(workflow_glob, recursive=True))
if not files:
    print(f"ERROR: no files matched WORKFLOW_GLOB={workflow_glob}", file=sys.stderr)
    sys.exit(1)

if workflow_file_match:
    files = [path for path in files if workflow_file_match.search(path)]
if workflow_file_exclude:
    files = [path for path in files if not workflow_file_exclude.search(path)]
if not files:
    print(
        "ERROR: no files left after WORKFLOW_FILE_MATCH/WORKFLOW_FILE_EXCLUDE filtering "
        f"(match={workflow_file_match_raw or '<none>'}, exclude={workflow_file_exclude_raw or '<none>'})",
        file=sys.stderr,
    )
    sys.exit(1)

uses_re = re.compile(r"^\s*(?:-\s*)?uses:\s*([^\s#]+)")
perm_id_token_write_re = re.compile(r"^\s*id-token\s*:\s*write\s*(?:#.*)?$", re.IGNORECASE | re.MULTILINE)
role_to_assume_re = re.compile(r"^\s*role-to-assume\s*:\s*[^\s#]+")
aws_static_cred_re = re.compile(r"^\s*(aws-access-key-id|aws-secret-access-key)\s*:\s*", re.IGNORECASE)
secret_cloud_key_re = re.compile(
    r"\$\{\{\s*secrets\.(AWS_ACCESS_KEY_ID|AWS_SECRET_ACCESS_KEY|AWS_SESSION_TOKEN|AZURE_CLIENT_SECRET|GCP_SERVICE_ACCOUNT_KEY|GOOGLE_CREDENTIALS)\s*\}\}",
    re.IGNORECASE,
)

auth_action_signatures = {
    'aws-actions/configure-aws-credentials': 'aws',
    'google-github-actions/auth': 'gcp',
    'azure/login': 'azure',
}


def classify_ref(uses_value: str):
    if '@' not in uses_value:
        return None
    ref = uses_value.rsplit('@', 1)[1].strip()
    if allow_ref_regex and allow_ref_regex.search(ref):
        return None
    lowered = ref.lower()
    if lowered in {'main', 'master', 'head', 'latest', 'stable', 'trunk', 'dev', 'develop'}:
        return 'branch-like'
    if re.match(r'^v\d+$', lowered):
        return 'major-tag'
    return None

rows = []
parse_errors = []

for file_path in files:
    try:
        text = Path(file_path).read_text(encoding='utf-8')
    except Exception as exc:
        parse_errors.append(f"{file_path}: {exc}")
        continue

    lines = text.splitlines()
    has_id_token_write = bool(perm_id_token_write_re.search(text))
    auth_actions = []
    floating_refs = []
    aws_action_lines = set()
    aws_role_to_assume_present = False
    aws_static_input_present = False
    secret_cloud_key_lines = []

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue

        use_match = uses_re.match(line)
        if use_match:
            uses_value = use_match.group(1)
            uses_name = uses_value.split('@', 1)[0].lower()
            provider = auth_action_signatures.get(uses_name)
            if provider:
                auth_actions.append({'line': idx, 'uses': uses_value, 'provider': provider})
                if provider == 'aws':
                    aws_action_lines.add(idx)

            reason = classify_ref(uses_value)
            if reason and provider:
                floating_refs.append({'line': idx, 'uses': uses_value, 'reason': reason})

        if role_to_assume_re.match(line):
            aws_role_to_assume_present = True

        if aws_static_cred_re.match(line):
            aws_static_input_present = True

        if secret_cloud_key_re.search(line):
            secret_cloud_key_lines.append(idx)

    if not auth_actions:
        continue

    score = 0
    issues = []

    if not has_id_token_write:
        score += 4
        issues.append({
            'code': 'missing_id_token_write',
            'message': 'Workflow uses cloud auth action(s) but does not declare id-token: write permissions.',
            'weight': 4,
        })

    if any(action['provider'] == 'aws' for action in auth_actions):
        if not aws_role_to_assume_present:
            score += 2
            issues.append({
                'code': 'aws_role_to_assume_missing',
                'message': 'AWS auth action is present but role-to-assume is missing (OIDC federation likely incomplete).',
                'weight': 2,
            })
        if aws_static_input_present:
            score += 4
            issues.append({
                'code': 'aws_static_credentials_input',
                'message': 'AWS auth action appears to use static key inputs (aws-access-key-id/aws-secret-access-key).',
                'weight': 4,
            })

    if secret_cloud_key_lines:
        score += 3
        issues.append({
            'code': 'static_cloud_secret_reference',
            'message': 'Workflow references long-lived cloud credential secrets instead of pure OIDC federation.',
            'weight': 3,
            'lines': secret_cloud_key_lines[:10],
        })

    if floating_refs:
        score += min(3, len(floating_refs))
        issues.append({
            'code': 'floating_auth_action_ref',
            'message': 'Cloud auth actions use non-pinned refs (@main/@master/@v1).',
            'weight': min(3, len(floating_refs)),
            'refs': floating_refs,
        })

    if score == 0:
        continue

    severity = 'critical' if score >= critical_score else ('warn' if score >= warn_score else 'info')

    rows.append({
        'workflow': file_path,
        'score': score,
        'severity': severity,
        'auth_actions': auth_actions,
        'issues': issues,
    })

rows.sort(key=lambda item: (-item['score'], item['workflow']))
critical_rows = [row for row in rows if row['severity'] == 'critical']
warn_rows = [row for row in rows if row['severity'] == 'warn']

summary = {
    'workflows_scanned': len(files),
    'workflows_flagged': len(rows),
    'critical_count': len(critical_rows),
    'warn_count': len(warn_rows),
    'warn_score': warn_score,
    'critical_score': critical_score,
    'top_n': top_n,
    'parse_errors': parse_errors,
}

if output_format == 'json':
    payload = {
        'summary': summary,
        'flagged_workflows': rows[:top_n],
        'critical_workflows': critical_rows,
    }
    print(json.dumps(payload, indent=2))
else:
    print('GitHub Actions OIDC Hardening Audit')
    print('===================================')
    print(f"Workflows scanned : {summary['workflows_scanned']}")
    print(f"Flagged workflows : {summary['workflows_flagged']}")
    print(f"Critical           : {summary['critical_count']}")
    print(f"Warn               : {summary['warn_count']}")
    print(f"Thresholds         : warn>={warn_score}, critical>={critical_score}")
    if parse_errors:
        print('Parse errors       :')
        for err in parse_errors:
            print(f"  - {err}")

    if rows:
        print('\nTop flagged workflows')
        for idx, row in enumerate(rows[:top_n], start=1):
            providers = ','.join(sorted({entry['provider'] for entry in row['auth_actions']}))
            print(
                f"{idx}. {row['workflow']} | severity={row['severity']} | score={row['score']} | providers={providers}"
            )
            for issue in row['issues']:
                extra = ''
                if 'lines' in issue:
                    extra = f" (lines: {','.join(str(line) for line in issue['lines'])})"
                print(f"   - [{issue['code']}] {issue['message']}{extra}")
    else:
        print('\nNo OIDC hardening findings.')

if fail_on_critical and critical_rows:
    sys.exit(1)
PY
