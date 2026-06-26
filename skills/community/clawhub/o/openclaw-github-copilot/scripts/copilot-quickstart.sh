#!/usr/bin/env bash
set -euo pipefail

MODEL_ID="copilot-bridge/github-copilot"
MODEL_ALIAS="copilot-auto"
PROBE=0
DO_LOGIN=0
DO_ACTIVATE=0
ENSURE_ALIAS=0

usage() {
  cat <<'EOF'
Usage: bash scripts/copilot-quickstart.sh [--probe] [--login] [--ensure-alias] [--activate]

Guided GitHub Copilot bootstrap for OpenClaw.

Options:
  --probe         Run a live auth/provider probe via `openclaw models status --probe`
  --login         Run `openclaw models auth login-github-copilot` when needed
  --ensure-alias  Add/update `copilot-auto -> copilot-bridge/github-copilot`
  --activate      Switch the default model to GitHub Copilot when ready
  -h, --help
EOF
}

for arg in "$@"; do
  case "$arg" in
    --probe)
      PROBE=1
      ;;
    --login)
      DO_LOGIN=1
      ;;
    --ensure-alias)
      ENSURE_ALIAS=1
      ;;
    --activate)
      DO_ACTIVATE=1
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

collect_state() {
  list_output="$(openclaw models list --plain 2>&1 || true)"
  alias_output="$(openclaw models aliases list 2>&1 || true)"
  status_output="$(openclaw models status --plain 2>&1 || true)"
  probe_status="not-run"

  has_model=0
  has_alias=0

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

  is_default=0
  if [[ "$current_model" == "$MODEL_ID" ]]; then
    is_default=1
  fi

  if [[ "$PROBE" -eq 1 ]]; then
    probe_output="$(openclaw models status --probe 2>&1 || true)"
    probe_status="$(
      printf '%s\n' "$probe_output" \
        | awk -F '│' -v model="$MODEL_ID" '$2 ~ model {gsub(/^[[:space:]]+|[[:space:]]+$/, "", $4); print $4; exit}'
    )"
    if [[ -z "$probe_status" ]]; then
      probe_status="unknown"
    fi
  fi
}

print_summary() {
  echo "OpenClaw GitHub Copilot quickstart"
  echo "- Model id: $MODEL_ID"
  echo "- Alias: $MODEL_ALIAS"
  echo "- Model available: $([[ "$has_model" -eq 1 ]] && echo yes || echo no)"
  echo "- Alias available: $([[ "$has_alias" -eq 1 ]] && echo yes || echo no)"
  echo "- Current default: ${current_model:-unknown}"
  echo "- Copilot already default: $([[ "$is_default" -eq 1 ]] && echo yes || echo no)"
  if [[ "$PROBE" -eq 1 ]]; then
    echo "- Live probe: $probe_status"
  fi
}

collect_state
print_summary

if [[ "$has_model" -eq 0 && "$DO_LOGIN" -eq 1 ]]; then
  if [[ ! -t 0 || ! -t 1 ]]; then
    echo
    echo "Cannot run interactive GitHub Copilot login without a TTY." >&2
    exit 11
  fi

  echo
  echo "GitHub Copilot model not ready. Launching official login flow..."
  openclaw models auth login-github-copilot
  echo
  echo "Re-checking model availability after login..."
  collect_state
  print_summary
fi

if [[ "$has_model" -eq 0 ]]; then
  echo
  echo "Next step: run \`openclaw models auth login-github-copilot\` and then re-run this script." >&2
  exit 12
fi

if [[ "$PROBE" -eq 1 && "$probe_status" != "not-run" && "$probe_status" != ok* && "$DO_LOGIN" -eq 1 ]]; then
  if [[ ! -t 0 || ! -t 1 ]]; then
    echo
    echo "Cannot refresh GitHub Copilot auth without a TTY." >&2
    exit 13
  fi

  echo
  echo "Live probe did not report a healthy Copilot auth state. Launching official login flow..."
  openclaw models auth login-github-copilot
  echo
  echo "Re-checking after login..."
  collect_state
  print_summary
fi

if [[ "$has_alias" -eq 0 && "$ENSURE_ALIAS" -eq 1 ]]; then
  echo
  echo "Adding alias: $MODEL_ALIAS -> $MODEL_ID"
  openclaw models aliases add "$MODEL_ALIAS" "$MODEL_ID"
  collect_state
fi

if [[ "$has_alias" -eq 0 && "$ENSURE_ALIAS" -eq 0 ]]; then
  echo
  echo "Alias missing. Optional cleanup: \`openclaw models aliases add $MODEL_ALIAS $MODEL_ID\`"
fi

if [[ "$is_default" -eq 0 && "$DO_ACTIVATE" -eq 1 ]]; then
  echo
  echo "Switching OpenClaw default model to GitHub Copilot..."
  if [[ "$has_alias" -eq 1 ]]; then
    openclaw models set "$MODEL_ALIAS"
  else
    openclaw models set "$MODEL_ID"
  fi
  collect_state
fi

echo
print_summary

if [[ "$PROBE" -eq 1 && "$probe_status" != "not-run" && "$probe_status" != ok* ]]; then
  echo
  echo "Next step: run \`openclaw models auth login-github-copilot\` and then re-run this script with \`--probe\`."
  exit 14
fi

if [[ "$is_default" -eq 0 ]]; then
  echo
  echo "Next step: run \`bash scripts/copilot-activate.sh\` or re-run this script with \`--activate\`."
  exit 13
fi

echo
echo "GitHub Copilot is ready to use as the OpenClaw default model."
