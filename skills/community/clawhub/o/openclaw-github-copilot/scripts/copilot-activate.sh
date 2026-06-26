#!/usr/bin/env bash
set -euo pipefail

MODEL_ID="copilot-bridge/github-copilot"
MODEL_ALIAS="copilot-auto"

usage() {
  cat <<'EOF'
Usage: bash scripts/copilot-activate.sh

Set OpenClaw's default model to GitHub Copilot.
The script prefers the `copilot-auto` alias and falls back to the full model id.
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

if [[ "$#" -gt 0 ]]; then
  echo "This script does not accept positional arguments." >&2
  usage >&2
  exit 2
fi

if ! command -v openclaw >/dev/null 2>&1; then
  echo "openclaw CLI is not installed or not on PATH." >&2
  exit 10
fi

list_output="$(openclaw models list --plain 2>&1 || true)"
alias_output="$(openclaw models aliases list 2>&1 || true)"

if ! printf '%s\n' "$list_output" | grep -Fx "$MODEL_ID" >/dev/null 2>&1; then
  echo "GitHub Copilot model was not found in \`openclaw models list --plain\`." >&2
  echo "Run \`openclaw models list\` and authenticate Copilot before trying again." >&2
  exit 11
fi

target="$MODEL_ID"
if printf '%s\n' "$alias_output" | grep -F "$MODEL_ALIAS -> $MODEL_ID" >/dev/null 2>&1; then
  target="$MODEL_ALIAS"
fi

echo "Setting OpenClaw default model to $target..."
openclaw models set "$target"

status_output="$(openclaw models status --plain 2>&1 || true)"
current_model="$(
  printf '%s\n' "$status_output" \
    | grep -E '^[a-z0-9][a-z0-9.-]*/[a-z0-9][a-z0-9./-]*$' \
    | head -n 1 \
    || true
)"

if [[ "$current_model" != "$MODEL_ID" ]]; then
  echo "The default model did not switch to $MODEL_ID." >&2
  echo "Inspect with \`openclaw models status --plain\`." >&2
  exit 12
fi

echo "Done. OpenClaw now defaults to $MODEL_ID."
