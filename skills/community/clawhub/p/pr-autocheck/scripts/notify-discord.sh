#!/usr/bin/env bash
# notify-discord.sh — Post a combined PR-autocheck report to Discord via webhook.
# Reads a JSON report on stdin (or --file PATH). Honors $DISCORD_WEBHOOK_URL.
# If no webhook is configured, it does NOT fake success: it writes the payload
# to reports/ and exits 3 so the caller can surface "delivery pending".
set -uo pipefail

REPORT_FILE=""
if [ "${1:-}" = "--file" ]; then REPORT_FILE="${2:-}"; fi

if [ -n "$REPORT_FILE" ]; then
  REPORT=$(cat "$REPORT_FILE")
else
  REPORT=$(cat)
fi

# Build a Discord embed from the report JSON.
OVERALL=$(printf '%s' "$REPORT" | jq -r '.overall // "unknown"')
case "$OVERALL" in
  ok) COLOR=3066993 ;;        # green
  warn) COLOR=16776960 ;;     # yellow
  critical|error) COLOR=15158332 ;; # red
  *) COLOR=9807270 ;;          # grey
esac

REPO=$(printf '%s' "$REPORT" | jq -r '.repo // "repo"')
PR=$(printf '%s' "$REPORT" | jq -r '.pr // "PR"')
REVIEW_SUM=$(printf '%s' "$REPORT" | jq -r '.review.summary // "n/a"')
HEALTH_SUM=$(printf '%s' "$REPORT" | jq -r '.health.summary // "n/a"')
FINDINGS=$(printf '%s' "$REPORT" | jq -r '
  (.review.findings // [])
  | if length==0 then "None 🎉"
    else (.[:8] | map("• **\(.severity)** — \(.title)") | join("\n"))
    end')

PAYLOAD=$(jq -nc \
  --arg title "PR Autocheck — $REPO $PR" \
  --argjson color "$COLOR" \
  --arg overall "$OVERALL" \
  --arg review "$REVIEW_SUM" \
  --arg health "$HEALTH_SUM" \
  --arg findings "$FINDINGS" \
  '{
     username: "PR Autocheck",
     embeds: [{
       title: $title,
       color: $color,
       fields: [
         {name:"Overall", value:$overall, inline:true},
         {name:"Code Review", value:$review, inline:false},
         {name:"Service Health", value:$health, inline:false},
         {name:"Top Findings", value:$findings, inline:false}
       ],
       footer: {text:"openclaw · pr-autocheck"}
     }]
   }')

if [ -z "${DISCORD_WEBHOOK_URL:-}" ]; then
  mkdir -p reports
  OUT="reports/pr-autocheck-discord-payload-$(date +%Y%m%dT%H%M%S).json"
  printf '%s\n' "$PAYLOAD" > "$OUT"
  echo "DELIVERY_PENDING: no DISCORD_WEBHOOK_URL set; payload saved to $OUT" >&2
  exit 3
fi

HTTP=$(curl -sS -o /tmp/discord_resp.$$ -w '%{http_code}' \
  -H 'Content-Type: application/json' \
  -X POST "$DISCORD_WEBHOOK_URL" -d "$PAYLOAD")
RC=$?
BODY=$(cat /tmp/discord_resp.$$ 2>/dev/null); rm -f /tmp/discord_resp.$$
if [ $RC -ne 0 ]; then
  echo "DELIVERY_FAILED: curl error $RC" >&2; exit 1
fi
if [ "$HTTP" -ge 200 ] && [ "$HTTP" -lt 300 ]; then
  echo "DELIVERED: Discord HTTP $HTTP"
  exit 0
fi
echo "DELIVERY_FAILED: Discord HTTP $HTTP — $BODY" >&2
exit 1
