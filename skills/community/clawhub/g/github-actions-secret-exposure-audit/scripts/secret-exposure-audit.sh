#!/usr/bin/env bash
set -euo pipefail

WORKFLOW_GLOB="${WORKFLOW_GLOB:-.github/workflows/*.y*ml}"
TOP_N="${TOP_N:-20}"
OUTPUT_FORMAT="${OUTPUT_FORMAT:-text}"
WARN_SCORE="${WARN_SCORE:-4}"
CRITICAL_SCORE="${CRITICAL_SCORE:-8}"
WORKFLOW_FILE_MATCH="${WORKFLOW_FILE_MATCH:-}"
WORKFLOW_FILE_EXCLUDE="${WORKFLOW_FILE_EXCLUDE:-}"
ALLOW_REF_REGEX="${ALLOW_REF_REGEX:-}"
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

if [[ "$FAIL_ON_CRITICAL" != "0" && "$FAIL_ON_CRITICAL" != "1" ]]; then
  echo "ERROR: FAIL_ON_CRITICAL must be 0 or 1 (got: $FAIL_ON_CRITICAL)" >&2
  exit 1
fi

python3 - "$WORKFLOW_GLOB" "$TOP_N" "$OUTPUT_FORMAT" "$WARN_SCORE" "$CRITICAL_SCORE" "$WORKFLOW_FILE_MATCH" "$WORKFLOW_FILE_EXCLUDE" "$ALLOW_REF_REGEX" "$FAIL_ON_CRITICAL" <<'PY'
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
    workflow_file_match_raw,
    workflow_file_exclude_raw,
    allow_ref_regex_raw,
    fail_on_critical_raw,
) = sys.argv[1:]

top_n = int(top_n_raw)
warn_score = int(warn_score_raw)
critical_score = int(critical_score_raw)
fail_on_critical = fail_on_critical_raw == '1'


def compile_regex(raw, label):
    if not raw:
        return None
    try:
        return re.compile(raw)
    except re.error as exc:
        print(f"ERROR: invalid {label} regex {raw!r}: {exc}", file=sys.stderr)
        sys.exit(1)


workflow_file_match = compile_regex(workflow_file_match_raw, 'WORKFLOW_FILE_MATCH')
workflow_file_exclude = compile_regex(workflow_file_exclude_raw, 'WORKFLOW_FILE_EXCLUDE')
allow_ref_regex = compile_regex(allow_ref_regex_raw, 'ALLOW_REF_REGEX')

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

trigger_key_re = re.compile(r"^(push|pull_request|pull_request_target|workflow_dispatch|repository_dispatch|schedule|merge_group|workflow_run|release):")
secret_expr_re = re.compile(r"\$\{\{\s*secrets\.([A-Za-z0-9_]+)\s*\}\}")
uses_re = re.compile(r"^\s*(?:-\s*)?uses:\s*([^\s#]+)")
run_key_re = re.compile(r"^\s*run\s*:\s*(.*)$")
command_secret_leak_re = re.compile(r"\b(echo|printf|tee)\b|::set-output", re.IGNORECASE)
hardcoded_credential_re = re.compile(
    r"^\s*[A-Za-z0-9_.-]*(password|passwd|token|secret|api[_-]?key|access[_-]?key)[A-Za-z0-9_.-]*\s*:\s*['\"]?([A-Za-z0-9_./+=:@-]{12,})['\"]?\s*$",
    re.IGNORECASE,
)


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
    events = set()
    secret_names = set()

    in_on = False
    on_indent = -1
    in_run_block = False
    run_indent = -1

    current_uses = None
    uses_indent = -1
    uses_ref_reason = None

    secret_echo_lines = []
    hardcoded_credential_lines = []
    pull_request_target_secret_lines = []
    floating_ref_secret_lines = []

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue

        indent = len(line) - len(line.lstrip(' '))

        if re.match(r'^on\s*:\s*$', line):
            in_on = True
            on_indent = indent
            continue

        if in_on:
            if indent <= on_indent and stripped:
                in_on = False
            else:
                trigger_match = trigger_key_re.match(stripped)
                if trigger_match:
                    events.add(trigger_match.group(1))

        if in_run_block and indent <= run_indent and stripped:
            in_run_block = False

        uses_match = uses_re.match(line)
        if uses_match:
            current_uses = uses_match.group(1)
            uses_indent = indent
            uses_ref_reason = classify_ref(current_uses)
        elif current_uses is not None and (
            indent < uses_indent or (indent == uses_indent and stripped.startswith('- '))
        ) and stripped:
            current_uses = None
            uses_ref_reason = None
            uses_indent = -1

        run_match = run_key_re.match(line)
        if run_match:
            run_rhs = run_match.group(1).strip()
            run_indent = indent
            in_run_block = run_rhs in {'|', '>-', '>', '|-'}

        secret_hits = list(secret_expr_re.finditer(line))
        if secret_hits:
            for hit in secret_hits:
                secret_names.add(hit.group(1))

            if in_run_block or run_match:
                if command_secret_leak_re.search(line):
                    secret_echo_lines.append({'line': idx, 'text': stripped})

            if current_uses and uses_ref_reason and indent > uses_indent:
                floating_ref_secret_lines.append(
                    {
                        'line': idx,
                        'action': current_uses,
                        'reason': uses_ref_reason,
                        'text': stripped,
                    }
                )

        hardcoded_match = hardcoded_credential_re.match(line)
        if hardcoded_match and '${{' not in line and '$' not in line:
            hardcoded_credential_lines.append({'line': idx, 'text': stripped})

    if 'pull_request_target' in events and secret_names:
        for idx, line in enumerate(lines, start=1):
            if secret_expr_re.search(line):
                pull_request_target_secret_lines.append({'line': idx, 'text': line.strip()})

    score = 0
    score += 4 if pull_request_target_secret_lines else 0
    score += len(secret_echo_lines) * 3
    score += len(floating_ref_secret_lines) * 2
    score += len(hardcoded_credential_lines) * 3

    severity = 'ok'
    if score >= critical_score:
        severity = 'critical'
    elif score >= warn_score:
        severity = 'warn'

    row = {
        'workflow_file': file_path,
        'severity': severity,
        'score': score,
        'events': sorted(events),
        'secret_names': sorted(secret_names),
        'pull_request_target_secret_lines': pull_request_target_secret_lines,
        'secret_echo_lines': secret_echo_lines,
        'floating_ref_secret_lines': floating_ref_secret_lines,
        'hardcoded_credential_lines': hardcoded_credential_lines,
    }
    rows.append(row)

rows.sort(
    key=lambda row: (
        0 if row['severity'] == 'critical' else 1 if row['severity'] == 'warn' else 2,
        -row['score'],
        row['workflow_file'],
    )
)
critical_rows = [row for row in rows if row['severity'] == 'critical']

summary = {
    'files_scanned': len(files),
    'files_evaluated': len(rows),
    'parse_errors': parse_errors,
    'critical_workflows': len(critical_rows),
    'warn_workflows': len([row for row in rows if row['severity'] == 'warn']),
    'ok_workflows': len([row for row in rows if row['severity'] == 'ok']),
    'warn_score': warn_score,
    'critical_score': critical_score,
    'checks': {
        'workflow_file_match': workflow_file_match_raw or None,
        'workflow_file_exclude': workflow_file_exclude_raw or None,
        'allow_ref_regex': allow_ref_regex_raw or None,
    },
}

if output_format == 'json':
    print(json.dumps({'summary': summary, 'workflows': rows[:top_n], 'all_workflows': rows, 'critical_workflows': critical_rows}, indent=2, sort_keys=True))
else:
    print('GITHUB ACTIONS SECRET EXPOSURE AUDIT')
    print('---')
    print(
        'SUMMARY: '
        f"files={summary['files_scanned']} evaluated={summary['files_evaluated']} "
        f"critical={summary['critical_workflows']} warn={summary['warn_workflows']} ok={summary['ok_workflows']}"
    )
    if parse_errors:
        print('PARSE_ERRORS:')
        for err in parse_errors:
            print(f'- {err}')
    print('---')
    print(f"TOP WORKFLOWS ({min(top_n, len(rows))})")
    if not rows:
        print('none')
    else:
        for row in rows[:top_n]:
            print(
                f"- [{row['severity']}] file={row['workflow_file']} score={row['score']} "
                f"events={','.join(row['events']) if row['events'] else '<none>'} "
                f"secrets={len(row['secret_names'])} "
                f"pr_target_secret={len(row['pull_request_target_secret_lines'])} "
                f"echo_leaks={len(row['secret_echo_lines'])} "
                f"floating_ref_secret={len(row['floating_ref_secret_lines'])} "
                f"hardcoded_creds={len(row['hardcoded_credential_lines'])}"
            )

sys.exit(1 if (fail_on_critical and critical_rows) else 0)
PY
