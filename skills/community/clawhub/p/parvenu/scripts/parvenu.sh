#!/usr/bin/env bash
# Call the Parvenu API: parvenu.sh <endpoint> [json-object-body]
# Adds PARVENU_API_KEY to the JSON body as "api_key". The key never appears on a
# command line and is never printed. Exits non-zero on HTTP errors.
set -euo pipefail

if [ -z "${PARVENU_API_KEY:-}" ]; then
  echo "PARVENU_API_KEY is not set. Add your Parvenu API key to the environment." >&2
  exit 1
fi

endpoint="${1:?usage: parvenu.sh <endpoint> [json-body]}"
case "$endpoint" in /*) ;; *) endpoint="/$endpoint" ;; esac

# Only the endpoints this skill documents.
case "$endpoint" in
  /credit_check|/all_list|/search_lead_locations|/lead_enrichment_list|/check_list_status|/download_list|/email_enrichment|/profile|/company_search) ;;
  *) echo "Unsupported endpoint: $endpoint" >&2; exit 2 ;;
esac

body="${2:-}"
[ -n "$body" ] || body='{}'

# Trim surrounding whitespace (including newlines) from the whole body.
body="${body#"${body%%[![:space:]]*}"}"
body="${body%"${body##*[![:space:]]}"}"
case "$body" in
  \{*\}) ;;
  *) echo "Body must be a JSON object, e.g. '{\"listname\": \"My list\"}'" >&2; exit 2 ;;
esac

# Escape the key for a JSON string (backslash and double quote; reject control chars).
case "$PARVENU_API_KEY" in
  *[[:cntrl:]]*) echo "PARVENU_API_KEY contains control characters." >&2; exit 1 ;;
esac
key="${PARVENU_API_KEY//\\/\\\\}"
key="${key//\"/\\\"}"

# Inner part of the object, without the outer braces.
inner="${body#\{}"
inner="${inner%\}}"
if [ -z "${inner//[[:space:]]/}" ]; then
  payload="{\"api_key\":\"${key}\"}"
else
  payload="{\"api_key\":\"${key}\",${inner}}"
fi

status=0
curl -sS --fail-with-body --connect-timeout 10 --max-time 120 \
  -X POST "https://api.parvenu.io${endpoint}" \
  -H "Content-Type: application/json" \
  -H "x-parvenu-source: openclaw" \
  --data-binary @- <<<"$payload" || status=$?
echo
exit $status
