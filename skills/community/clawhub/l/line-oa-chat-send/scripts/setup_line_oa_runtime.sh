#!/usr/bin/env bash
# Provision a private, caller-chosen Python runtime for the LINE OA CLI.
# This never creates a browser profile or requests LINE credentials.
set -euo pipefail

runtime_dir=""
install_browser=1
while [[ $# -gt 0 ]]; do
  case "$1" in
    --runtime-dir)
      [[ $# -ge 2 ]] || { printf 'ERROR: --runtime-dir requires a value\n' >&2; exit 2; }
      runtime_dir="$2"
      shift 2
      ;;
    --skip-browser-install)
      install_browser=0
      shift
      ;;
    --help|-h)
      printf 'Usage: %s --runtime-dir <private-runtime-directory> [--skip-browser-install]\n' "${0##*/}"
      exit 0
      ;;
    *)
      printf 'ERROR: unknown argument: %s\n' "$1" >&2
      exit 2
      ;;
  esac
done

if [[ -z "$runtime_dir" ]]; then
  printf 'ERROR: choose a private runtime location with --runtime-dir; no default directory is assumed.\n' >&2
  exit 2
fi
if ! command -v uv >/dev/null 2>&1; then
  printf 'ERROR: uv is required for safe isolated setup. Install uv, then retry.\n' >&2
  exit 2
fi

mkdir -p "$runtime_dir"
chmod 700 "$runtime_dir"
uv venv "$runtime_dir/venv"
uv pip install --python "$runtime_dir/venv/bin/python" playwright
chmod 700 "$runtime_dir/venv"
browser_dir="$runtime_dir/ms-playwright"
if (( install_browser )); then
  mkdir -p "$browser_dir"
  chmod 700 "$browser_dir"
  PLAYWRIGHT_BROWSERS_PATH="$browser_dir" "$runtime_dir/venv/bin/python" -m playwright install chromium
fi
printf 'SETUP OK\n'
printf 'Next: export LINE_OA_PYTHON=%q\n' "$runtime_dir/venv/bin/python"
printf 'Next: export LINE_OA_SEND_CHAT_BROWSER_DIR=%q\n' "$browser_dir"
printf 'Then: bash scripts/start_line_oa_chromium.sh\n'
