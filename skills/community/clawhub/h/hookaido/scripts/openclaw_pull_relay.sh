#!/usr/bin/env bash
# Pull relay: Hookaido (public, pull mode) -> OpenClaw Gateway (local, no inbound).
# Requires: bash, curl, jq, base64.
#
# Long-polls a Hookaido pull endpoint, forwards each event to a local OpenClaw
# hook, and acks only after a 2xx. Retryable failures (network, 408, 429, 5xx)
# are nacked with a delay; any other status dead-letters the event in Hookaido
# with reason openclaw_http_<status>. Only talks to the two configured URLs.
set -euo pipefail

: "${HOOKAIDO_PULL_URL:?e.g. https://hooks.example.com/pull/github}"
: "${HOOKAIDO_PULL_TOKEN:?pull_api token}"
: "${OPENCLAW_HOOK_URL:=http://127.0.0.1:18789/hooks/github}"
: "${OPENCLAW_HOOKS_TOKEN:?OpenClaw hooks.token}"

# Both URLs carry a bearer token, so plain HTTP is only accepted for loopback.
# Set HOOKAIDO_RELAY_ALLOW_HTTP=1 only when the network layer already encrypts
# the hop (for example a Tailscale/WireGuard address).
curl_proto() {
  local url="$1" name="$2"
  if [[ "$url" =~ ^https:// ]]; then
    echo "=https"
  elif [[ "$url" =~ ^http://(127\.0\.0\.1|localhost|\[::1\])(:[0-9]+)?(/|$) ]]; then
    echo "=http"
  elif [[ "$url" =~ ^http:// && "${HOOKAIDO_RELAY_ALLOW_HTTP:-}" == "1" ]]; then
    echo "${name}: plain HTTP allowed by HOOKAIDO_RELAY_ALLOW_HTTP=1" >&2
    echo "=http"
  else
    echo "${name} must use https:// (plain http:// only for loopback, or with HOOKAIDO_RELAY_ALLOW_HTTP=1 on an encrypted network): ${url}" >&2
    return 1
  fi
}
pull_proto="$(curl_proto "$HOOKAIDO_PULL_URL" HOOKAIDO_PULL_URL)"
hook_proto="$(curl_proto "$OPENCLAW_HOOK_URL" OPENCLAW_HOOK_URL)"

payload_tmp="$(mktemp)"
trap 'rm -f "$payload_tmp"' EXIT

pull() {
  curl -sS --fail-with-body --proto "$pull_proto" -X POST "${HOOKAIDO_PULL_URL}/$1" \
    -H "Authorization: Bearer ${HOOKAIDO_PULL_TOKEN}" \
    -H "Content-Type: application/json" -d "$2"
}

# Header names are stored in canonical form (X-Github-Event), so look them up
# case-insensitively.
header() {
  jq -j --arg h "$2" '[.headers // {} | to_entries[] | select(.key | ascii_downcase == $h) | .value][0] // empty' <<<"$1"
}

while true; do
  batch="$(pull dequeue '{"batch":10,"lease_ttl":"60s","max_wait":"25s"}')" || { sleep 5; continue; }

  while IFS= read -r item; do
    item="${item%$'\r'}"
    [[ -z "$item" ]] && continue
    id="$(jq -j '.id' <<<"$item")"
    lease="$(jq -j '.lease_id' <<<"$item")"
    ctype="$(header "$item" content-type)"
    event="$(header "$item" x-github-event)"
    delivery="$(header "$item" x-github-delivery)"

    code=000
    if jq -j '.payload_b64' <<<"$item" | base64 -d >"$payload_tmp"; then
      # Idempotency-Key = Hookaido event id, so a redelivered event replays the
      # earlier OpenClaw run instead of starting a second one.
      code="$(curl -sS -o /dev/null -w '%{http_code}' --proto "$hook_proto" -X POST "$OPENCLAW_HOOK_URL" \
        -H "Authorization: Bearer ${OPENCLAW_HOOKS_TOKEN}" \
        -H "Content-Type: ${ctype:-application/json}" \
        -H "Idempotency-Key: ${id}" \
        ${event:+-H "X-GitHub-Event: ${event}"} \
        ${delivery:+-H "X-GitHub-Delivery: ${delivery}"} \
        --data-binary @"$payload_tmp")" || code=000
    fi

    case "$code" in
      2??) pull ack "$(jq -nc --arg l "$lease" '{lease_id:$l}')" >/dev/null ;;
      000|408|429|5??) pull nack "$(jq -nc --arg l "$lease" '{lease_id:$l,delay:"30s"}')" >/dev/null ;;
      *) pull nack "$(jq -nc --arg l "$lease" --arg r "openclaw_http_${code}" '{lease_id:$l,dead:true,reason:$r}')" >/dev/null ;;
    esac
    echo "event=${id} openclaw_status=${code}"
  done < <(jq -c '.items[]?' <<<"$batch")
done
