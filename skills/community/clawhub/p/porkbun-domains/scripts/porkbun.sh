#!/usr/bin/env bash
# Porkbun API wrapper — all endpoints via curl + jq
# Usage: porkbun.sh <command> [args...]
#
# Env: PORKBUN_API_KEY, PORKBUN_SECRET_KEY (or reads from .env in workspace)
set -euo pipefail

API="https://api.porkbun.com/api/json/v3"

# Load keys from env or .env
if [ -z "${PORKBUN_API_KEY:-}" ]; then
  ENV_FILE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}/.env"
  if [ -f "$ENV_FILE" ]; then
    eval "$(grep '^PORKBUN_' "$ENV_FILE" | sed 's/^/export /')"
  fi
fi

: "${PORKBUN_API_KEY:?Set PORKBUN_API_KEY}"
: "${PORKBUN_SECRET_KEY:?Set PORKBUN_SECRET_KEY}"

AUTH="{\"apikey\":\"$PORKBUN_API_KEY\",\"secretapikey\":\"$PORKBUN_SECRET_KEY\"}"

post() {
  curl -s -X POST "$1" -H "Content-Type: application/json" -d "${2:-$AUTH}"
}

merge() {
  echo "$AUTH" | jq --argjson extra "$1" '. + $extra'
}

cmd="${1:-help}"
shift || true

case "$cmd" in
  ping)
    post "$API/ping" ;;
  list|domains)
    post "$API/domain/listAll" ;;
  check)
    post "$API/domain/check" "$(merge "{\"searchQuery\":\"${1:?Usage: check <domain>}\"}")" ;;
  dns-list|dns)
    post "$API/dns/retrieve/${1:?Usage: dns-list <domain>}" ;;
  dns-create)
    post "$API/dns/create/${1:?}" "$(merge "{\"type\":\"${2:?}\",\"name\":\"${3:-}\",\"content\":\"${4:?}\",\"ttl\":\"${5:-600}\"}")" ;;
  dns-delete)
    post "$API/dns/delete/${1:?}/${2:?}" ;;
  dns-delete-type)
    post "$API/dns/deleteByNameType/${1:?}/${2:?}/${3:-}" ;;
  nameservers|ns)
    post "$API/domain/getNs/${1:?Usage: ns <domain>}" ;;
  ns-update)
    d="${1:?}"; shift; nj=$(printf '"%s",' "$@" | sed 's/,$//');
    post "$API/domain/updateNs/$d" "$(merge "{\"ns\":[$nj]}")" ;;
  forward-add)
    post "$API/domain/addUrlForward/${1:?}" "$(merge "{\"subdomain\":\"${3:-}\",\"location\":\"${2:?}\",\"type\":\"${4:-temporary}\",\"includePath\":\"yes\",\"wildcard\":\"yes\"}")" ;;
  forward-list)
    post "$API/domain/getUrlForwarding/${1:?}" ;;
  forward-delete)
    post "$API/domain/deleteUrlForward/${1:?}/${2:?}" ;;
  ssl)
    post "$API/ssl/retrieve/${1:?}" ;;
  pricing)
    curl -s "$API/pricing/get" ;;
  auto-renew)
    post "$API/domain/updateAutoRenew/${1:?}" "$(merge "{\"status\":\"${2:?on or off}\"}")" ;;
  help|*)
    cat <<EOF
Porkbun API CLI — Domain & DNS Management

Usage: porkbun.sh <command> [args...]

DOMAINS
  ping                              Test API connection
  list                              List all domains
  check <domain>                    Check availability
  ns <domain>                       Get nameservers
  ns-update <domain> <ns1> <ns2>    Update nameservers
  auto-renew <domain> on|off        Toggle auto-renew
  pricing                           TLD pricing

DNS
  dns-list <domain>                 List all records
  dns-create <domain> <type> <name> <content> [ttl]
  dns-delete <domain> <id>
  dns-delete-type <domain> <type> [name]

URL FORWARDING
  forward-add <domain> <url> [subdomain] [permanent|temporary]
  forward-list <domain>
  forward-delete <domain> <id>

SSL
  ssl <domain>                      Get SSL cert bundle

Env: PORKBUN_API_KEY, PORKBUN_SECRET_KEY
EOF
    ;;
esac
