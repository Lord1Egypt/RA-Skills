#!/usr/bin/env bash
# Crawlora REST helper — minimal, dependency-free (curl only).
# Calls https://api.crawlora.net/api/v1 with your Crawlora API key.
# Get a free key (2,000 credits/mo, no card) at https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills.
#
# Usage:
#   GET  :  crawlora.sh /path
#
# GET key=value args become the query string. Prints raw JSON to stdout — pipe into `jq`.
set -euo pipefail

: "${CRAWLORA_API_KEY:?Set CRAWLORA_API_KEY first — get a free key at https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills}"
# The key is written to a curl config file below. Restrict it to the key
# alphabet so a newline, quote, or config directive cannot alter that file.
case "$CRAWLORA_API_KEY" in
  *[!A-Za-z0-9._-]*) echo "invalid CRAWLORA_API_KEY format" >&2; exit 2 ;;
esac
# Fixed, non-overridable: an env-configurable base URL would let anything that
# can set CRAWLORA_API_BASE redirect this key to an attacker-controlled host.
base="https://api.crawlora.net/api/v1"

method="GET"
args=()
while [ $# -gt 0 ]; do
  case "$1" in
    -X|-d) echo "only GET are supported by the opensea-research skill" >&2; exit 2 ;;
    *) args+=("$1"); shift ;;
  esac
done

[ "${#args[@]}" -ge 1 ] || { echo "usage: crawlora.sh /<route> [k=v ...]" >&2; exit 2; }
path="${args[0]}"
rest=("${args[@]:1}")

# This skill's helper is limited to its documented Crawlora route set. Keep
# caller-account surfaces and unrelated API routes out of the helper even if
# someone supplies an undocumented path directly.
case "$method" in
  GET) ;;
  *)
    echo "only GET are supported by the opensea-research skill" >&2
    exit 2
    ;;
esac

# Reject path syntax that could smuggle a route through a shell glob check.
case "$path" in
  ""|*[?#%]*|*..*|*//* )
    echo "invalid path for the opensea-research skill" >&2
    exit 2
    ;;
esac

# Static routes use escaped case patterns. Parameterized routes use anchored
# extended regular expressions so every {param} is exactly one non-empty path
# segment; unlike a case '*', [^/]+ cannot consume another slash.
route_allowed=false
case "$path" in
  /opensea/activity) route_allowed=true ;;
  /opensea/categories) route_allowed=true ;;
  /opensea/chains) route_allowed=true ;;
  /opensea/collections) route_allowed=true ;;
  /opensea/drops) route_allowed=true ;;
  /opensea/most-watched) route_allowed=true ;;
  /opensea/rankings) route_allowed=true ;;
  /opensea/search/collections) route_allowed=true ;;
  /opensea/top-movers) route_allowed=true ;;
esac
if [ "$route_allowed" = false ]; then
  route_regexes=(
  '^/opensea/collection/[^/]+$'
  '^/opensea/collection/[^/]+/activity$'
  '^/opensea/collection/[^/]+/best-deals$'
  '^/opensea/collection/[^/]+/chart$'
  '^/opensea/collection/[^/]+/depth$'
  '^/opensea/collection/[^/]+/holders$'
  '^/opensea/collection/[^/]+/items$'
  '^/opensea/collection/[^/]+/offers$'
  '^/opensea/collection/[^/]+/rarest-items$'
  '^/opensea/collection/[^/]+/search-items$'
  '^/opensea/collection/[^/]+/social-proof$'
  '^/opensea/collection/[^/]+/top-sales$'
  '^/opensea/collection/[^/]+/trait-offers$'
  '^/opensea/collection/[^/]+/traits$'
  '^/opensea/item/[^/]+/[^/]+/[^/]+$'
  '^/opensea/item/[^/]+/[^/]+/[^/]+/activity$'
  '^/opensea/item/[^/]+/[^/]+/[^/]+/chart$'
  '^/opensea/item/[^/]+/[^/]+/[^/]+/depth$'
  '^/opensea/item/[^/]+/[^/]+/[^/]+/listings$'
  '^/opensea/item/[^/]+/[^/]+/[^/]+/offers$'
  '^/opensea/item/[^/]+/[^/]+/[^/]+/owners$'
  '^/opensea/profile/[^/]+$'
  '^/opensea/profile/[^/]+/activity$'
  '^/opensea/profile/[^/]+/collections$'
  '^/opensea/profile/[^/]+/created$'
  '^/opensea/profile/[^/]+/items$'
  '^/opensea/profile/[^/]+/search-items$'
  )
  for route_regex in ${route_regexes[@]+"${route_regexes[@]}"}; do
    if [[ "$path" =~ $route_regex ]]; then
      route_allowed=true
      break
    fi
  done
fi
if [ "$route_allowed" = false ]; then
  echo "path is not in the opensea-research skill catalog" >&2
  exit 2
fi



# Keep the API key out of the curl process command line. A private temporary
# config supplies the header and is removed automatically on exit.
umask 077
curl_config="$(mktemp "${TMPDIR:-/tmp}/crawlora-curl.XXXXXX")"
chmod 600 "$curl_config"
trap 'rm -f "$curl_config"' EXIT
printf 'header = "x-api-key: %s"\n' "$CRAWLORA_API_KEY" >"$curl_config"
auth=(--config "$curl_config")

# GET-only skill: no request body or alternate method is accepted.
# -G + --data-urlencode URL-encodes each value (so spaces etc. are safe).
qs=()
for kv in ${rest[@]+"${rest[@]}"}; do
  [ -n "$kv" ] || continue
  case "$kv" in
    *@*) echo "@ is not allowed in query arguments" >&2; exit 2 ;;
  esac
  qs+=(--data-urlencode "$kv")
done
curl -q -fsS -G "${auth[@]}" ${qs[@]+"${qs[@]}"} "${base}${path}"