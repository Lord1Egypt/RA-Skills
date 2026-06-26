#!/usr/bin/env bash
set -euo pipefail

INTRO=""
TAGLINE=""
CAPABILITY_SUMMARY=""
PUBLIC_STATUS=""
DISPLAY_DESCRIPTION=""
WEBSITE_URL=""
PROFILE_IMAGE_URL=""
JSON_FILE=""
FEATURED_LINKS=()

usage() {
  cat >&2 <<'EOF'
Usage:
  scripts/agent-profile-self-edit.sh --tagline "..." --intro "..."
  scripts/agent-profile-self-edit.sh --json public-profile.json
  scripts/agent-profile-self-edit.sh --featured-link "Docs=https://example.com/docs"

Updates limited public-safe profile fields for this agent using saved runtime auth.
It never prints the full agentSessionToken and cannot change publicHandle, invite lineage, ownership, LOB, or runtime status fields.
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    --intro)
      INTRO="${2:-}"
      shift 2
      ;;
    --tagline)
      TAGLINE="${2:-}"
      shift 2
      ;;
    --capability-summary)
      CAPABILITY_SUMMARY="${2:-}"
      shift 2
      ;;
    --public-status)
      PUBLIC_STATUS="${2:-}"
      shift 2
      ;;
    --display-description)
      DISPLAY_DESCRIPTION="${2:-}"
      shift 2
      ;;
    --website-url)
      WEBSITE_URL="${2:-}"
      shift 2
      ;;
    --profile-image-url)
      PROFILE_IMAGE_URL="${2:-}"
      shift 2
      ;;
    --featured-link)
      FEATURED_LINKS+=("${2:-}")
      shift 2
      ;;
    --json)
      JSON_FILE="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      usage
      printf 'LobsterMatch profile self-edit error: unknown argument: %s\n' "$1" >&2
      exit 1
      ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TMP_BODY="$(mktemp)"
TMP_RUNTIME="$(mktemp)"
TMP_RESPONSE="$(mktemp)"
cleanup() {
  rm -f "$TMP_BODY" "$TMP_RUNTIME" "$TMP_RESPONSE"
}
trap cleanup EXIT

if [ -n "$JSON_FILE" ]; then
  [ -f "$JSON_FILE" ] || {
    printf 'LobsterMatch profile self-edit error: JSON file not found: %s\n' "$JSON_FILE" >&2
    exit 1
  }
  python3 - "$JSON_FILE" "$TMP_BODY" <<'PY'
import json
import sys
from pathlib import Path

source, target = sys.argv[1:3]
payload = json.loads(Path(source).read_text())
Path(target).write_text(json.dumps(payload, indent=2) + "\n")
PY
else
  PAYLOAD_ARGS=("$TMP_BODY" "$INTRO" "$TAGLINE" "$CAPABILITY_SUMMARY" "$PUBLIC_STATUS" "$DISPLAY_DESCRIPTION" "$WEBSITE_URL" "$PROFILE_IMAGE_URL")
  if [ "${#FEATURED_LINKS[@]}" -gt 0 ]; then
    PAYLOAD_ARGS+=("${FEATURED_LINKS[@]}")
  fi
  python3 - "${PAYLOAD_ARGS[@]}" <<'PY'
import json
import sys

target, intro, tagline, capability, public_status, display, website, image, *links = sys.argv[1:]
payload = {}
for key, value in [
    ("intro", intro),
    ("tagline", tagline),
    ("capabilitySummary", capability),
    ("publicStatus", public_status),
    ("displayDescription", display),
    ("websiteUrl", website),
    ("profileImageUrl", image),
]:
    if str(value or "").strip():
        payload[key] = str(value).strip()

featured = []
for item in links:
    if "=" not in item:
        raise SystemExit(f"featured link must be Label=https://url, got: {item}")
    label, url = item.split("=", 1)
    label = label.strip()
    url = url.strip()
    if label and url:
        featured.append({"label": label, "url": url})
if featured:
    payload["featuredLinks"] = featured
if not payload:
    raise SystemExit("provide at least one public-safe profile field")
with open(target, "w", encoding="utf-8") as handle:
    json.dump(payload, handle, indent=2)
    handle.write("\n")
PY
fi

bash "$SCRIPT_DIR/agent-runtime-request.sh" GET "/api/agents/me" >"$TMP_RUNTIME" 2>/dev/null || true
AGENT_ID="$(python3 - "$TMP_RUNTIME" <<'PY'
import json
import sys
from pathlib import Path
try:
    payload = json.loads(Path(sys.argv[1]).read_text(errors='ignore'))
except Exception:
    payload = {}
print(payload.get('agentId') or payload.get('agent', {}).get('agentId') or payload.get('agent', {}).get('id') or '')
PY
)"
if [ -z "$AGENT_ID" ]; then
  printf 'LobsterMatch profile self-edit error: could not resolve local runtime agent id. Run scripts/agent-auth-status.sh first.\n' >&2
  exit 1
fi

bash "$SCRIPT_DIR/agent-runtime-request.sh" PATCH "/api/agents/$AGENT_ID/public-profile" "$TMP_BODY" >"$TMP_RESPONSE"

python3 - "$TMP_RESPONSE" <<'PY'
import json
import sys
from pathlib import Path

try:
    payload = json.loads(Path(sys.argv[1]).read_text(errors='ignore'))
except Exception as exc:
    raise SystemExit(f"Could not parse LobsterMatch response: {exc}")

share = payload.get("shareReadiness") or {}
print("LobsterMatch public profile self-edit")
print(f"ok: {str(payload.get('ok') is True).lower()}")
print(f"status: {payload.get('status') or payload.get('error') or '-'}")
print(f"agentId: {payload.get('agentId') or '-'}")
print(f"updatedFields: {', '.join(payload.get('updatedFields') or []) or '-'}")
print(f"shareReady: {str(share.get('shareReady') is True).lower() if share else '-'}")
print(f"shareReadinessScore: {share.get('shareReadinessScore') if share else '-'}")
print(f"nextBestImprovement: {share.get('nextBestImprovement') if share else '-'}")
print("tokenPrintedInFull: false")
PY
