#!/usr/bin/env bash
# track.sh — Track pageviews and custom events to Plausible Analytics
# Usage: track.sh --url "https://example.com/page" [--referrer "https://ref.com"] [--domain "example.com"] [--base-url "https://plausible.io"]
#   or:  track.sh --event "Signup" [--props '{"plan":"pro"}'] [--domain "example.com"]

set -euo pipefail

DOMAIN="${PLAUSIBLE_SITE_DOMAIN:-}"
BASE_URL="${PLAUSIBLE_BASE_URL:-https://plausible.io}"
EVENT_NAME=""
URL=""
REFERRER=""
PROPS=""

usage() {
  cat <<EOF
Usage: track.sh [options]
Options:
  --domain    Site domain (env: PLAUSIBLE_SITE_DOMAIN)
  --url       Page URL for pageview events
  --referrer  Referring URL (optional)
  --event     Custom event name (e.g. Signup)
  --props     JSON object for event properties (optional)
  --base-url  Plausible base URL (default: https://plausible.io)
EOF
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --domain) DOMAIN="${2:-}"; shift 2 ;;
    --url) URL="${2:-}"; shift 2 ;;
    --referrer) REFERRER="${2:-}"; shift 2 ;;
    --event) EVENT_NAME="${2:-}"; shift 2 ;;
    --props) PROPS="${2:-}"; shift 2 ;;
    --base-url) BASE_URL="${2:-}"; shift 2 ;;
    -h|--help) usage ;;
    *) echo "Unknown option: $1"; usage ;;
  esac
done

if [[ -z "$DOMAIN" ]]; then
  echo "Error: --domain or PLAUSIBLE_SITE_DOMAIN is required" >&2
  exit 1
fi

# Pageview event
if [[ -n "$URL" ]]; then
  PAYLOAD=$(jq -n \
    --arg d "$DOMAIN" \
    --arg u "$URL" \
    --arg r "$REFERRER" \
    '{
      name: "pageview",
      url: $u,
      domain: $d,
      referrer: (if $r != "" then $r else null end)
    }')

  RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD" \
    "${BASE_URL}/api/event")

  HTTP_CODE=$(echo "$RESPONSE" | tail -1)
  BODY=$(echo "$RESPONSE" | sed '$d')

  if [[ "$HTTP_CODE" == "202" ]] || [[ "$HTTP_CODE" == "200" ]]; then
    echo "Pageview tracked: $URL"
  else
    echo "Error tracking pageview (HTTP $HTTP_CODE): $BODY" >&2
    exit 1
  fi

# Custom event
elif [[ -n "$EVENT_NAME" ]]; then
  if [[ -n "$PROPS" ]]; then
    PAYLOAD=$(jq -n \
      --arg d "$DOMAIN" \
      --arg e "$EVENT_NAME" \
      --json p "$PROPS" \
      '{
        name: $e,
        url: "https://" + $d + "/custom",
        domain: $d,
        props: $p
      }')
  else
    PAYLOAD=$(jq -n \
      --arg d "$DOMAIN" \
      --arg e "$EVENT_NAME" \
      '{
        name: $e,
        url: "https://" + $d + "/custom",
        domain: $d
      }')
  fi

  RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD" \
    "${BASE_URL}/api/event")

  HTTP_CODE=$(echo "$RESPONSE" | tail -1)
  BODY=$(echo "$RESPONSE" | sed '$d')

  if [[ "$HTTP_CODE" == "202" ]] || [[ "$HTTP_CODE" == "200" ]]; then
    echo "Custom event tracked: $EVENT_NAME"
  else
    echo "Error tracking event (HTTP $HTTP_CODE): $BODY" >&2
    exit 1
  fi
else
  echo "Error: --url or --event is required" >&2
  usage
fi
