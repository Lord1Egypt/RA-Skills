#!/usr/bin/env bash
set -euo pipefail

TASK_FILE="$1"
TASK_ID=$(jq -r '.task_id' "$TASK_FILE")
ARTROOT=${OPENCLAW_ARTIFACT_ROOT:-/var/lib/openclaw/artifacts}
mkdir -p "$ARTROOT"
OUT="$ARTROOT/${TASK_ID}-preflight.json"

require_bin() {
  local b="$1"
  command -v "$b" >/dev/null 2>&1
}

has_sha_tool=0
if require_bin sha256sum || require_bin shasum; then
  has_sha_tool=1
fi

jq -n \
  --arg task_id "$TASK_ID" \
  --arg artifact_root "$ARTROOT" \
  --arg caller_allowlist "${OPENCLAW_ALLOWED_CALLERS:-architect,chief-of-staff}" \
  --arg allow_high_risk "${OPENCLAW_ALLOW_HIGH_RISK:-0}" \
  --arg allow_run_cmd "${OPENCLAW_ALLOW_RUN_CMD:-0}" \
  --arg allow_deploy_skill "${OPENCLAW_ALLOW_DEPLOY_SKILL:-0}" \
  --arg run_cmd_allowlist "${OPENCLAW_RUN_CMD_ALLOWLIST:-}" \
  --argjson has_openclaw "$(require_bin openclaw && echo true || echo false)" \
  --argjson has_jq "$(require_bin jq && echo true || echo false)" \
  --argjson has_curl "$(require_bin curl && echo true || echo false)" \
  --argjson has_tar "$(require_bin tar && echo true || echo false)" \
  --argjson has_timeout "$(require_bin timeout && echo true || echo false)" \
  --argjson has_git "$(require_bin git && echo true || echo false)" \
  --argjson has_sha_tool "$has_sha_tool" \
  '{
    task_id: $task_id,
    status: "completed",
    bins: {
      openclaw: $has_openclaw,
      jq: $has_jq,
      curl: $has_curl,
      tar: $has_tar,
      sha256sum_or_shasum: $has_sha_tool,
      timeout: $has_timeout,
      git: $has_git
    },
    env: {
      OPENCLAW_ARTIFACT_ROOT: $artifact_root,
      OPENCLAW_ALLOWED_CALLERS: $caller_allowlist,
      OPENCLAW_ALLOW_HIGH_RISK: $allow_high_risk,
      OPENCLAW_ALLOW_RUN_CMD: $allow_run_cmd,
      OPENCLAW_ALLOW_DEPLOY_SKILL: $allow_deploy_skill,
      OPENCLAW_RUN_CMD_ALLOWLIST: $run_cmd_allowlist
    },
    notes: [
      "run-cmd and deploy-skill are disabled unless both global and per-action gates are enabled",
      "deploy-skill writes to /opt/openclaw/skills and requires suitable filesystem privileges"
    ]
  }' > "$OUT"

echo "preflight complete: $OUT"
