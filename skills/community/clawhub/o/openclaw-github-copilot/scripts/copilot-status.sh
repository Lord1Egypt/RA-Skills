#!/usr/bin/env bash
set -euo pipefail

MODEL_ID="copilot-bridge/github-copilot"
MODEL_ALIAS="copilot-auto"
PROBE=0

usage() {
  cat <<'EOF'
Usage: bash scripts/copilot-status.sh [--probe]

Check whether OpenClaw can use GitHub Copilot.

Options:
  --probe   Run a live auth/provider probe via `openclaw models status --probe`
  -h, --help
EOF
}

for arg in "$@"; do
  case "$arg" in
    --probe)
      PROBE=1
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $arg" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if ! command -v openclaw >/dev/null 2>&1; then
  echo "openclaw CLI is not installed or not on PATH." >&2
  exit 10
fi

list_output="$(openclaw models list --plain 2>&1 || true)"
alias_output="$(openclaw models aliases list 2>&1 || true)"
status_output="$(openclaw models status --plain 2>&1 || true)"
probe_status="not-run"
probe_line=""

if [[ "$PROBE" -eq 1 ]]; then
  probe_output="$(openclaw models status --probe 2>&1 || true)"
  probe_line="$(
    printf '%s\n' "$probe_output" \
      | awk -F '│' -v model="$MODEL_ID" '$2 ~ model {gsub(/^[[:space:]]+|[[:space:]]+$/, "", $4); print $4; exit}'
  )"
  if [[ -n "$probe_line" ]]; then
    probe_status="$probe_line"
  else
    probe_status="unknown"
  fi
fi

has_model=0
has_alias=0
is_default=0

if printf '%s\n' "$list_output" | grep -Fx "$MODEL_ID" >/dev/null 2>&1; then
  has_model=1
fi

if printf '%s\n' "$alias_output" | grep -F "$MODEL_ALIAS -> $MODEL_ID" >/dev/null 2>&1; then
  has_alias=1
fi

current_model="$(
  printf '%s\n' "$status_output" \
    | grep -E '^[a-z0-9][a-z0-9.-]*/[a-z0-9][a-z0-9./-]*$' \
    | head -n 1 \
    || true
)"

if [[ "$current_model" == "$MODEL_ID" ]]; then
  is_default=1
fi

echo "OpenClaw GitHub Copilot status"
echo "- Model id: $MODEL_ID"
echo "- Alias: $MODEL_ALIAS"
echo "- Model available: $([[ "$has_model" -eq 1 ]] && echo yes || echo no)"
echo "- Alias available: $([[ "$has_alias" -eq 1 ]] && echo yes || echo no)"
echo "- Current default: ${current_model:-unknown}"
echo "- Copilot already default: $([[ "$is_default" -eq 1 ]] && echo yes || echo no)"
if [[ "$PROBE" -eq 1 ]]; then
  echo "- Live probe: $probe_status"
fi

if [[ "$has_model" -eq 0 ]]; then
  echo
  echo "Next step: run \`openclaw models list\` and verify the GitHub Copilot provider is configured." >&2
  exit 11
fi

if [[ "$PROBE" -eq 1 && "$probe_status" != "not-run" && "$probe_status" != ok* ]]; then
  echo
  echo "Next step: run \`openclaw models auth login-github-copilot\` and then re-run this script with \`--probe\`." >&2
  exit 13
fi

if [[ "$is_default" -eq 0 ]]; then
  echo
  if [[ "$has_alias" -eq 1 ]]; then
    echo "Next step: run \`openclaw models set $MODEL_ALIAS\` or \`bash scripts/copilot-activate.sh\`."
  else
    echo "Next step: run \`openclaw models set $MODEL_ID\` or \`bash scripts/copilot-activate.sh\`."
  fi
  exit 12
fi

echo
echo "GitHub Copilot is available and already selected as the default model."
exit 0
