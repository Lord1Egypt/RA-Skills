#!/usr/bin/env bash
# switch-model.sh -- Deterministically switch OpenClaw agent model to a hudl/* model.
# Usage: bash scripts/switch-model.sh <model-id-with-or-without-hudl-prefix>

set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "ERROR: Missing target model. Usage: switch-model.sh <model-id-with-or-without-hudl-prefix>"
  exit 1
fi

trim() {
  local value="$1"
  value="${value#"${value%%[![:space:]]*}"}"
  value="${value%"${value##*[![:space:]]}"}"
  printf '%s' "$value"
}

resolve_config() {
  local candidate

  for candidate in "${OPENCLAW_CONFIG:-}" "$HOME/.openclaw/config.json" "$HOME/.openclaw/openclaw.json"; do
    if [ -n "$candidate" ] && [ -f "$candidate" ]; then
      printf '%s\n' "$candidate"
      return 0
    fi
  done

  return 1
}

TARGET_RAW="$(trim "$1")"
if [ -z "$TARGET_RAW" ]; then
  echo "ERROR: Missing target model after trimming whitespace."
  exit 1
fi

TARGET_MODEL="$TARGET_RAW"
if [[ "$TARGET_MODEL" != hudl/* ]]; then
  TARGET_MODEL="hudl/$TARGET_MODEL"
fi

if [[ ! "$TARGET_MODEL" =~ ^hudl/[A-Za-z0-9][A-Za-z0-9._/-]*$ ]]; then
  echo "ERROR: Invalid model id '$TARGET_MODEL'. Expected hudl/<model-id> with no spaces."
  exit 1
fi

if [[ "$TARGET_MODEL" == "hudl/" ]]; then
  echo "ERROR: Invalid model id 'hudl/'."
  exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "ERROR: jq is required but not installed. Install it with: sudo apt install jq"
  exit 1
fi

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
VALIDATE_LOG="$(mktemp)"
TMP_FILE="$(mktemp)"
cleanup() {
  rm -f "$VALIDATE_LOG" "$TMP_FILE"
}
trap cleanup EXIT

# Validate provider first (includes config-path compatibility checks).
if ! bash "$SCRIPT_DIR/validate.sh" >"$VALIDATE_LOG" 2>&1; then
  cat "$VALIDATE_LOG"
  exit 1
fi

CONFIG="$(resolve_config || true)"
if [ -z "$CONFIG" ]; then
  echo "ERROR: OpenClaw config not found."
  exit 1
fi

AGENT_COUNT="$(jq -r '(.agents.list // []) | length' "$CONFIG")"
if [ "${AGENT_COUNT:-0}" -eq 0 ]; then
  echo "ERROR: No agent entries found in config. This skill requires at least one agent in .agents.list to switch the active model."
  echo "config: $CONFIG"
  exit 1
fi

jq --arg model "$TARGET_MODEL" '
  .models.providers.hudl.models = (
    ((.models.providers.hudl.models // [])
      | map(
          .id = (
            (.id // "")
            | if startswith("hudl/") then . else "hudl/" + . end
          )
        )
      | map(select(.id != "hudl/"))
      | unique_by(.id))
    as $catalog
    | if any($catalog[]?; .id == $model) then
        $catalog
      else
        $catalog + [{"id": $model, "name": $model}]
      end
  ) |
  .agents.defaults.model.primary = $model |
  if (.agents.list // [] | length) > 0 then
    if any(.agents.list[]; .id == "main") then
      .agents.list |= map(if .id == "main" then .model.primary = $model else . end)
    else
      .agents.list[0].model.primary = $model
    end
  else
    .
  end
' "$CONFIG" > "$TMP_FILE"

mv "$TMP_FILE" "$CONFIG"
TMP_FILE=""

ACTIVE_MAIN="$(jq -r '(.agents.list // [] | map(select(.id=="main")) | .[0].model.primary) // empty' "$CONFIG")"
ACTIVE_FIRST="$(jq -r '(.agents.list // [])[0].model.primary // empty' "$CONFIG")"
DEFAULT_MODEL="$(jq -r '.agents.defaults.model.primary // empty' "$CONFIG")"
CATALOG_IDS="$(jq -r '(.models.providers.hudl.models // []) | map(.id // empty) | join(",")' "$CONFIG")"

ACTIVE_MODEL="$ACTIVE_MAIN"
if [ -z "$ACTIVE_MODEL" ]; then
  ACTIVE_MODEL="$ACTIVE_FIRST"
fi

if [ -z "$ACTIVE_MODEL" ] || [ -z "$DEFAULT_MODEL" ]; then
  echo "ERROR: Switch completed but active/default model is missing."
  echo "config: $CONFIG"
  echo "agent primary: ${ACTIVE_MODEL:-<not-set>}"
  echo "defaults primary: ${DEFAULT_MODEL:-<not-set>}"
  exit 1
fi

if [[ "$ACTIVE_MODEL" != hudl/* || "$DEFAULT_MODEL" != hudl/* ]]; then
  echo "ERROR: Switch completed but resulting model is not hudl-prefixed."
  echo "config: $CONFIG"
  echo "agent primary: $ACTIVE_MODEL"
  echo "defaults primary: $DEFAULT_MODEL"
  exit 1
fi

if [ "$ACTIVE_MODEL" != "$TARGET_MODEL" ] || [ "$DEFAULT_MODEL" != "$TARGET_MODEL" ]; then
  echo "ERROR: Switch completed but resulting model does not match target '$TARGET_MODEL'."
  echo "config: $CONFIG"
  echo "agent primary: $ACTIVE_MODEL"
  echo "defaults primary: $DEFAULT_MODEL"
  exit 1
fi

if ! jq -e --arg model "$TARGET_MODEL" 'any((.models.providers.hudl.models // [])[]?; (.id // empty) == $model)' "$CONFIG" >/dev/null; then
  echo "ERROR: Switch completed but provider model catalog does not contain target '$TARGET_MODEL'."
  echo "config: $CONFIG"
  echo "provider models: ${CATALOG_IDS:-<empty>}"
  exit 1
fi

if jq -e 'any((.models.providers.hudl.models // [])[]?; ((.id // "") | startswith("hudl/")) | not)' "$CONFIG" >/dev/null; then
  echo "ERROR: Switch completed but provider model catalog still contains non-hudl ids."
  echo "config: $CONFIG"
  echo "provider models: ${CATALOG_IDS:-<empty>}"
  exit 1
fi

echo "OK: model switched"
echo "config: $CONFIG"
echo "agent primary: $ACTIVE_MODEL"
echo "defaults primary: $DEFAULT_MODEL"
echo "provider models: ${CATALOG_IDS:-<empty>}"
