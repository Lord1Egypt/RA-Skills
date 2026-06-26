#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="${1:-$HOME/ocmemog}"
REPO_URL="https://github.com/simbimbo/ocmemog.git"
PLUGIN_ID="memory-ocmemog"
ENDPOINT="http://127.0.0.1:17890"

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "Missing required command: $1" >&2
    exit 1
  }
}

need_cmd git
need_cmd python3

if [ -d "$REPO_DIR/.git" ]; then
  git -C "$REPO_DIR" pull --ff-only
else
  git clone "$REPO_URL" "$REPO_DIR"
fi

python3 -m venv "$REPO_DIR/.venv"
"$REPO_DIR/.venv/bin/pip" install --upgrade pip >/dev/null
"$REPO_DIR/.venv/bin/pip" install -r "$REPO_DIR/requirements.txt"

if [ "$(uname -s)" = "Darwin" ]; then
  "$REPO_DIR/scripts/ocmemog-install.sh"
else
  nohup "$REPO_DIR/scripts/ocmemog-sidecar.sh" >"$REPO_DIR/.ocmemog-sidecar.log" 2>&1 &
  echo "Started sidecar in background; log: $REPO_DIR/.ocmemog-sidecar.log"
fi

if command -v openclaw >/dev/null 2>&1; then
  openclaw plugins install -l "$REPO_DIR" || true
  openclaw plugins enable "$PLUGIN_ID" || true
else
  echo "openclaw CLI not found; skipping plugin install/enable"
fi

python3 - <<'PY'
import json, sys, urllib.request
url = 'http://127.0.0.1:17890/healthz'
try:
    with urllib.request.urlopen(url, timeout=5) as r:
        body = r.read().decode('utf-8', 'replace')
    print('healthz ok:', body)
except Exception as e:
    print(f'healthz check failed: {e}', file=sys.stderr)
    sys.exit(2)
PY

echo
echo "ocmemog bootstrap complete."
echo "Repo: $REPO_DIR"
echo "Plugin: $PLUGIN_ID"
echo "Endpoint: $ENDPOINT"
echo
echo "If OpenClaw config is not already patched, set the memory slot to $PLUGIN_ID and the endpoint to $ENDPOINT."
