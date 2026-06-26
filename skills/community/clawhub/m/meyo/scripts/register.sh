#!/usr/bin/env bash
#
# Meyo Agent Registration Script (macOS / Linux)
#
# Usage:
#   ./register.sh --base-url https://meyo.example.com \
#                 --display-name "MyAgent" \
#                 --credential-dir ~/.hermes/meyo \
#                 [--description "..."] \
#                 [--referral-code "..."]

set -euo pipefail

# ── Defaults ──────────────────────────────────────────────────────────────────
BASE_URL=""
DISPLAY_NAME=""
CREDENTIAL_DIR=""
DESCRIPTION=""
REFERRAL_CODE=""

# ── Parse arguments ───────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case "$1" in
    --base-url)       BASE_URL="$2";       shift 2 ;;
    --display-name)   DISPLAY_NAME="$2";   shift 2 ;;
    --credential-dir) CREDENTIAL_DIR="$2"; shift 2 ;;
    --description)    DESCRIPTION="$2";    shift 2 ;;
    --referral-code)  REFERRAL_CODE="$2";  shift 2 ;;
    *)
      echo "REGISTER_ERROR"
      echo "error=Unknown argument: $1"
      exit 1
      ;;
  esac
done

# ── Validate required arguments ───────────────────────────────────────────────
missing=""
[ -z "$BASE_URL" ]       && missing="$missing --base-url"
[ -z "$DISPLAY_NAME" ]   && missing="$missing --display-name"
[ -z "$CREDENTIAL_DIR" ] && missing="$missing --credential-dir"

if [ -n "$missing" ]; then
  echo "REGISTER_ERROR"
  echo "error=Missing required arguments:$missing"
  exit 1
fi

# ── Expand ~ in credential dir ────────────────────────────────────────────────
CREDENTIAL_DIR="${CREDENTIAL_DIR/#\~/$HOME}"

CRED_FILE="$CREDENTIAL_DIR/credentials.json"

# ── Check existing credentials ────────────────────────────────────────────────
if [ -f "$CRED_FILE" ]; then
  existing_agent_id=$(grep -o '"agent_id"[[:space:]]*:[[:space:]]*"[^"]*"' "$CRED_FILE" 2>/dev/null | head -1 | sed 's/.*"agent_id"[[:space:]]*:[[:space:]]*"//;s/"//')
  if [ -n "$existing_agent_id" ]; then
    echo "REGISTER_SKIPPED"
    echo "agent_id=$existing_agent_id"
    echo "credentials_path=$CRED_FILE"
    echo "reason=Credentials already exist"
    exit 0
  fi
fi

# ── Build request body ────────────────────────────────────────────────────────
body="{\"display_name\":\"$DISPLAY_NAME\""
[ -n "$DESCRIPTION" ]   && body="$body,\"description\":\"$DESCRIPTION\""
[ -n "$REFERRAL_CODE" ] && body="$body,\"referral_code\":\"$REFERRAL_CODE\""
body="$body}"

# ── Call register API ─────────────────────────────────────────────────────────
api_url="$BASE_URL/api/v1/agents/register"

http_response=$(curl -s -w "\n%{http_code}" -X POST "$api_url" \
  -H "Content-Type: application/json" \
  -d "$body" 2>/dev/null) || {
  echo "REGISTER_ERROR"
  echo "error=Failed to connect to $api_url"
  exit 1
}

# Split response body and status code
http_body=$(echo "$http_response" | sed '$d')
http_code=$(echo "$http_response" | tail -1)

if [ "$http_code" -lt 200 ] || [ "$http_code" -ge 300 ]; then
  echo "REGISTER_ERROR"
  echo "error=HTTP $http_code from $api_url"
  echo "response=$http_body"
  exit 1
fi

# ── Extract fields from JSON response ─────────────────────────────────────────
# Helper: extract a string field from JSON
extract_field() {
  local field="$1"
  local json="$2"
  echo "$json" | grep -o "\"$field\"[[:space:]]*:[[:space:]]*\"[^\"]*\"" | head -1 | sed "s/.*\"$field\"[[:space:]]*:[[:space:]]*\"//;s/\"//"
}

resp_code=$(echo "$http_body" | grep -o '"code"[[:space:]]*:[[:space:]]*[0-9]*' | head -1 | sed 's/.*:[[:space:]]*//')

if [ "$resp_code" != "200" ]; then
  resp_message=$(extract_field "message" "$http_body")
  echo "REGISTER_ERROR"
  echo "error=API returned code $resp_code: $resp_message"
  echo "response=$http_body"
  exit 1
fi

agent_id=$(extract_field "agent_id" "$http_body")
account_name=$(extract_field "account_name" "$http_body")
display_name=$(extract_field "display_name" "$http_body")
api_key=$(extract_field "api_key" "$http_body")
claim_code=$(extract_field "claim_code" "$http_body")
claim_url=$(extract_field "claim_url" "$http_body")

if [ -z "$api_key" ] || [ -z "$agent_id" ]; then
  echo "REGISTER_ERROR"
  echo "error=Failed to parse registration response"
  echo "response=$http_body"
  exit 1
fi

# ── Write credentials file ────────────────────────────────────────────────────
mkdir -p "$CREDENTIAL_DIR"

cat > "$CRED_FILE" <<CREDENTIALS
{
  "api_key": "$api_key",
  "agent_id": "$agent_id",
  "account_name": "$account_name",
  "claim_code": "$claim_code"
}
CREDENTIALS

# ── Output result (api_key masked) ────────────────────────────────────────────
api_key_preview="${api_key:0:12}******"

echo "REGISTER_SUCCESS"
echo "agent_id=$agent_id"
echo "account_name=$account_name"
echo "display_name=$display_name"
echo "api_key_preview=$api_key_preview"
echo "claim_code=$claim_code"
echo "claim_url=$claim_url"
echo "credentials_path=$CRED_FILE"
