#!/usr/bin/env bash
# Portable launcher for the LINE OA CDP client. It does not start or log into a browser.
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

if [[ -n "${LINE_OA_PYTHON:-}" ]]; then
  if [[ ! -x "$LINE_OA_PYTHON" ]]; then
    printf 'ERROR: LINE_OA_PYTHON is not executable: %s\n' "$LINE_OA_PYTHON" >&2
    exit 2
  fi
  if ! "$LINE_OA_PYTHON" -c 'import playwright' >/dev/null 2>&1; then
    printf 'ERROR: Playwright is unavailable in LINE_OA_PYTHON: %s\n' "$LINE_OA_PYTHON" >&2
    printf 'Run scripts/setup_line_oa_runtime.sh with an explicit --runtime-dir, then export LINE_OA_PYTHON.\n' >&2
    exit 2
  fi
  exec "$LINE_OA_PYTHON" "$script_dir/send_line_oa_chat.py" "$@"
fi

for candidate in "${PYTHON:-}" python3 python; do
  [[ -n "$candidate" ]] || continue
  if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -c 'import playwright' >/dev/null 2>&1; then
    exec "$candidate" "$script_dir/send_line_oa_chat.py" "$@"
  fi
done

if command -v uv >/dev/null 2>&1; then
  # Creates/reuses uv's managed cache only; does not create a browser profile or handle credentials.
  exec uv run --no-project --with playwright python "$script_dir/send_line_oa_chat.py" "$@"
fi

printf 'ERROR: No Python runtime with Playwright was found.\n' >&2
printf 'Install uv, then run: bash scripts/setup_line_oa_runtime.sh --runtime-dir <private-runtime-dir>\n' >&2
printf 'After setup: export LINE_OA_PYTHON=<private-runtime-dir>/venv/bin/python\n' >&2
exit 2
