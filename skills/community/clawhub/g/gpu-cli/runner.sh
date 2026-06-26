#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# GPU CLI ClawHub Skill Runner
# - Whitelists `gpu` commands
# - Denies shell injections (pipes, chaining, redirection, subshells)
# - Preflight: gpu --version, gpu doctor --json (skipped for read-only cmds)
# - Optional caps: price/time (dry-run by default)
# - Exit-code remediation (daemon restart), cleanup on timeout/cancel
#
# Inputs (from ClawHub manifest settings or env overrides):
#   SKILL_DRY_RUN              (bool) default true
#   SKILL_REQUIRE_CONFIRM      (bool) default true
#   SKILL_MAX_PRICE_PER_HOUR   (float) default 0.50, 0 disables
#   SKILL_MAX_RUNTIME_MINUTES  (int)   default 30,   0 disables
#   SKILL_DEFAULT_GPU_TYPE     (str)   default "RTX 4090"
#   SKILL_PROVIDER             (str)   default "runpod"
#   SKILL_CONFIRM              ("yes" to bypass confirm gate)
#   SKILL_INPUT                (optional freeform text)
#
# Invocation:
#   runner.sh <gpu ...>                 # e.g., runner.sh gpu status --json
#   SKILL_INPUT="gpu run python train.py" runner.sh    # parses input
###############################################################################

echo_info()  { printf "[gpu-skill] %s\n" "$*" >&2; }
echo_warn()  { printf "[gpu-skill][warn] %s\n" "$*" >&2; }
echo_error() { printf "[gpu-skill][error] %s\n" "$*" >&2; }

# Exit code for "blocked by policy" (distinct from success)
EXIT_BLOCKED=4

# Load settings with defaults (ClawHub maps manifest settings to envs)
SKILL_DRY_RUN=${SKILL_DRY_RUN:-true}
SKILL_REQUIRE_CONFIRM=${SKILL_REQUIRE_CONFIRM:-true}
SKILL_MAX_PRICE_PER_HOUR=${SKILL_MAX_PRICE_PER_HOUR:-0.50}
SKILL_MAX_RUNTIME_MINUTES=${SKILL_MAX_RUNTIME_MINUTES:-30}
SKILL_DEFAULT_GPU_TYPE=${SKILL_DEFAULT_GPU_TYPE:-"RTX 4090"}
SKILL_PROVIDER=${SKILL_PROVIDER:-"runpod"}
SKILL_CONFIRM=${SKILL_CONFIRM:-""}

# Build the command string
CMD_STR=""
if [[ $# -gt 0 ]]; then
  CMD_STR="$*"
elif [[ -n "${SKILL_INPUT:-}" ]]; then
  CMD_STR=$(echo "$SKILL_INPUT" | tr -s ' ')
else
  echo_error "No command provided. Example: 'gpu status --json' or set SKILL_INPUT."
  exit 2
fi

# Whitelist: must start with 'gpu '
if [[ ! "$CMD_STR" =~ ^gpu[[:space:]]+ ]]; then
  echo_error "Only 'gpu ...' commands are permitted by this skill."
  exit 2
fi

echo_info "Parsed command: $CMD_STR"

# Deny injection characters: ; & | ` ( ) > < $ { } and embedded newlines
if [[ "$CMD_STR" =~ [\;\&\|\`\(\)\>\<\$\{\}] ]] || [[ "$CMD_STR" == *$'\n'* ]]; then
  echo_error "Command contains disallowed shell operators. Please provide a single 'gpu ...' command without chaining, redirection, or variable expansion."
  exit 2
fi

# Extract subcommand
read -r _gpu SUBCMD _rest <<<"$CMD_STR"

# Subcommand allowlist
ALLOW_CMDS=(run status doctor logs attach stop inventory config auth daemon volume llm comfyui notebook)
is_allowed=false
for c in "${ALLOW_CMDS[@]}"; do
  if [[ "$SUBCMD" == "$c" ]]; then is_allowed=true; break; fi
done
if [[ "$is_allowed" != true ]]; then
  echo_error "Subcommand '$SUBCMD' not permitted by this skill."
  exit 2
fi
echo_info "Allowlist OK for subcommand: $SUBCMD"

# Append --json for known JSON-capable commands if not present
maybe_force_json() {
  local s="$1"
  case "$SUBCMD" in
    status|inventory|logs|config|daemon|volume|llm|comfyui)
      if [[ "$s" != *"--json"* ]]; then
        s+=" --json"
        echo_info "Appended --json flag"
      fi
      ;;
  esac
  printf "%s" "$s"
}

CMD_STR=$(maybe_force_json "$CMD_STR")

# Preflight checks
echo_info "Preflight: checking gpu --version"
if ! gpu --version >/dev/null 2>&1; then
  echo_error "'gpu' binary not found on PATH. Please install: curl -fsSL https://gpu-cli.sh/install.sh | sh"
  exit 2
fi

# Skip doctor preflight for read-only subcommands (they surface their own errors)
READ_ONLY_CMDS=(status logs config inventory doctor)
is_read_only=false
for c in "${READ_ONLY_CMDS[@]}"; do
  if [[ "$SUBCMD" == "$c" ]]; then is_read_only=true; break; fi
done

if [[ "$is_read_only" != true ]]; then
  echo_info "Preflight: running gpu doctor --json"
  if ! OUT=$(gpu doctor --json 2>&1); then
    echo_error "'gpu doctor' failed. Output:\n$OUT"
    exit 1
  fi
  if ! printf "%s" "$OUT" | tr -d '\n' | grep -q '"healthy"[[:space:]]*:[[:space:]]*true'; then
    echo_warn "Readiness check reported not healthy. Proceeding may fail."
  fi
fi

# Price check (best-effort). Only meaningful for 'run' subcommand.
PRICE_NOTE=""
if [[ "${SKILL_MAX_PRICE_PER_HOUR}" != "0" && "$SUBCMD" == "run" ]]; then
  TARGET_GPU="$SKILL_DEFAULT_GPU_TYPE"
  if echo "$CMD_STR" | grep -q -- "--gpu-type"; then
    # Extract quoted value after --gpu-type (supports "RTX 4090" style)
    TARGET_GPU=$(echo "$CMD_STR" | sed -E 's/.*--gpu-type[[:space:]]+"([^"]+)".*/\1/' )
    if [[ -z "$TARGET_GPU" || "$TARGET_GPU" == "$CMD_STR" ]]; then
      # Try unquoted single-word fallback
      TARGET_GPU=$(echo "$CMD_STR" | sed -E 's/.*--gpu-type[[:space:]]+([^[:space:]"-]+).*/\1/' )
    fi
    if [[ -z "$TARGET_GPU" || "$TARGET_GPU" == "$CMD_STR" ]]; then
      TARGET_GPU="$SKILL_DEFAULT_GPU_TYPE"
    fi
  fi
  if INV=$(gpu inventory --json --available 2>/dev/null); then
    # Use jq if available, fall back to grep/sed
    PRICE=""
    if command -v jq >/dev/null 2>&1; then
      PRICE=$(printf "%s" "$INV" | jq -r --arg g "$TARGET_GPU" \
        '.[] | select(.gpu_type == $g) | .cost_per_hour' 2>/dev/null | head -n1 || true)
    else
      # Best-effort: flatten JSON and match (may fail on nested objects)
      INV_FLAT=$(printf "%s" "$INV" | tr -d '\n')
      LINE=$(printf "%s" "$INV_FLAT" | grep -oi "{[^}]*\"gpu_type\"[[:space:]]*:[[:space:]]*\"$TARGET_GPU\"[^}]*}" | head -n1 || true)
      if [[ -n "$LINE" ]]; then
        PRICE=$(printf "%s" "$LINE" | sed -E 's/.*"cost_per_hour"[[:space:]]*:[[:space:]]*([0-9.]+).*/\1/' || true)
      fi
    fi
    if [[ -n "$PRICE" && "$PRICE" != "null" ]]; then
      PRICE_NOTE="GPU $TARGET_GPU at \$${PRICE}/hr"
      cmp=$(awk -v a="$PRICE" -v b="$SKILL_MAX_PRICE_PER_HOUR" 'BEGIN{if (a>b) print 1; else print 0}' || echo 0)
      if [[ "$cmp" == "1" ]]; then
        echo_warn "Estimated price ${PRICE_NOTE} exceeds cap \$${SKILL_MAX_PRICE_PER_HOUR}/hr."
        if [[ "$SKILL_REQUIRE_CONFIRM" == "true" && "$SKILL_CONFIRM" != "yes" ]]; then
          echo_info "Set SKILL_CONFIRM=yes to proceed despite cap, or lower GPU price."
          exit $EXIT_BLOCKED
        fi
      fi
    fi
  fi
fi

# Dry-run preview or confirmation gate
echo_info "Command preview: $CMD_STR"
if [[ -n "$PRICE_NOTE" ]]; then echo_info "Cost estimate: $PRICE_NOTE"; fi
if [[ "$SKILL_DRY_RUN" == "true" ]]; then
  echo_info "Dry-run enabled; not executing. Toggle SKILL_DRY_RUN=false to run."
  exit $EXIT_BLOCKED
fi
if [[ "$SKILL_REQUIRE_CONFIRM" == "true" && "$SKILL_CONFIRM" != "yes" ]]; then
  echo_info "Confirmation required. Set SKILL_CONFIRM=yes to proceed."
  exit $EXIT_BLOCKED
fi

# Build argument array from CMD_STR for direct execution (no shell re-evaluation)
read -ra CMD_ARGS <<<"$CMD_STR"
# Remove leading "gpu" — we invoke the gpu binary directly
CMD_ARGS=("${CMD_ARGS[@]:1}")

# Runtime timeout (best-effort). Prefer coreutils 'timeout' if present.
run_with_timeout() {
  local minutes="$1"; shift
  if [[ "$minutes" -gt 0 ]] && command -v timeout >/dev/null 2>&1; then
    timeout "$((minutes*60))" gpu "$@"
    return $?
  fi
  gpu "$@"
}

# Execute with basic remediation: if daemon error (13), start daemon and retry once
ATTEMPT=1
MAX_ATTEMPTS=2
EXIT=1
while [[ $ATTEMPT -le $MAX_ATTEMPTS ]]; do
  echo_info "Executing (attempt $ATTEMPT/$MAX_ATTEMPTS)..."
  set +e
  if [[ "$SKILL_MAX_RUNTIME_MINUTES" =~ ^[0-9]+$ ]]; then
    run_with_timeout "$SKILL_MAX_RUNTIME_MINUTES" "${CMD_ARGS[@]}"
    EXIT=$?
  else
    gpu "${CMD_ARGS[@]}"
    EXIT=$?
  fi
  set -e

  if [[ $EXIT -eq 0 ]]; then break; fi
  if [[ $EXIT -eq 13 && $ATTEMPT -lt $MAX_ATTEMPTS ]]; then
    echo_warn "Daemon connection error (13). Attempting 'gpu daemon start' then retry."
    gpu daemon start || true
    sleep 2
    ATTEMPT=$((ATTEMPT+1))
    continue
  fi
  break
done

# Cleanup on timeout/cancel
if [[ $EXIT -eq 124 || $EXIT -eq 130 ]]; then
  echo_warn "Command interrupted or timed out; attempting cleanup with 'gpu stop -y'"
  gpu stop -y || true
fi

case "$EXIT" in
  0) echo_info "Completed successfully." ;;
  10) echo_error "Auth required/failed (10). Remediation: run 'gpu auth login' from your environment." ;;
  11) echo_error "Quota exceeded (11). Consider 'gpu upgrade' or waiting for quota refresh." ;;
  12) echo_error "Resource not found (12). Verify IDs and context." ;;
  13) echo_error "Daemon connection error (13). Tried restart once; check 'gpu daemon status' and logs." ;;
  14) echo_error "Timeout (14). Increase caps or simplify the job." ;;
  15) echo_error "Cancelled (15)." ;;
  *) echo_error "Exited with code $EXIT." ;;
esac

exit "$EXIT"
