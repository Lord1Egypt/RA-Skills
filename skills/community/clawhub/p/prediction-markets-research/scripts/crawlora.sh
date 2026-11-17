#!/usr/bin/env bash
# Crawlora REST helper — minimal, dependency-free (curl only).
# Calls https://api.crawlora.net/api/v1 with your Crawlora API key.
# Get a free key (2,000 credits/mo, no card) at https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills.
#
# Usage:
#   GET  :  crawlora.sh /amazon/search k=laptop s=relevanceblender
#   GET  :  crawlora.sh /youtube/transcript/dQw4w9WgXcQ
#   POST :  crawlora.sh -X POST /google/search '{"keyword":"web scraping api","language":"en","country":"us"}'
#   POST :  crawlora.sh -X POST /google/trends/explore/interest-over-time '{"keywords":["bitcoin"]}'
#
# GET key=value args become the query string. POST takes one JSON body argument
# (or pass it with -d '<json>'). Prints raw JSON to stdout — pipe into `jq`.
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
body=""
args=()
while [ $# -gt 0 ]; do
  case "$1" in
    -X)
      [ $# -ge 2 ] || { echo "-X requires an HTTP method" >&2; exit 2; }
      method="$2"; shift 2 ;;
    -d)
      [ $# -ge 2 ] || { echo "-d requires a request body" >&2; exit 2; }
      body="$2"; shift 2 ;;
    *)  args+=("$1"); shift ;;
  esac
done

[ "${#args[@]}" -ge 1 ] || { echo "usage: crawlora.sh [-X METHOD] /path [k=v ... | json-body]" >&2; exit 2; }
path="${args[0]}"
rest=("${args[@]:1}")

# This skill's helper is limited to its documented Crawlora route set. Keep
# caller-account surfaces and unrelated API routes out of the helper even if
# someone supplies an undocumented path directly.
case "$method" in
  GET|POST) ;;
  *)
    echo "only GET and POST are supported by the prediction-markets-research skill" >&2
    exit 2
    ;;
esac

# Reject path syntax that could smuggle a route through a shell glob check.
case "$path" in
  ""|*[?#%]*|*..*|*//* )
    echo "invalid path for the prediction-markets-research skill" >&2
    exit 2
    ;;
esac

# Static routes use escaped case patterns. Parameterized routes use anchored
# extended regular expressions so every {param} is exactly one non-empty path
# segment; unlike a case '*', [^/]+ cannot consume another slash.
route_allowed=false
case "$path" in
  /draftkings/predictions/availability) route_allowed=true ;;
  /draftkings/predictions/categories) route_allowed=true ;;
  /draftkings/predictions/rules) route_allowed=true ;;
  /kalshi/events) route_allowed=true ;;
  /kalshi/events/multivariate) route_allowed=true ;;
  /kalshi/exchange/schedule) route_allowed=true ;;
  /kalshi/exchange/status) route_allowed=true ;;
  /kalshi/historical/cutoff) route_allowed=true ;;
  /kalshi/historical/markets) route_allowed=true ;;
  /kalshi/historical/trades) route_allowed=true ;;
  /kalshi/markets) route_allowed=true ;;
  /kalshi/markets/history) route_allowed=true ;;
  /kalshi/markets/orderbooks) route_allowed=true ;;
  /kalshi/series) route_allowed=true ;;
  /kalshi/trades) route_allowed=true ;;
  /metaculus/comments-feed) route_allowed=true ;;
  /metaculus/questions) route_allowed=true ;;
  /metaculus/top-comments) route_allowed=true ;;
  /polymarket/activity/trades) route_allowed=true ;;
  /polymarket/dashboards/macro) route_allowed=true ;;
  /polymarket/events) route_allowed=true ;;
  /polymarket/events/similar) route_allowed=true ;;
  /polymarket/fee-types) route_allowed=true ;;
  /polymarket/homepage/feed) route_allowed=true ;;
  /polymarket/leaderboard) route_allowed=true ;;
  /polymarket/markets) route_allowed=true ;;
  /polymarket/predictions) route_allowed=true ;;
  /polymarket/rewards/markets) route_allowed=true ;;
  /polymarket/search) route_allowed=true ;;
  /polymarket/tags) route_allowed=true ;;
  /polymarket/tokens/midpoints) route_allowed=true ;;
  /polymarket/tokens/orderbooks) route_allowed=true ;;
  /polymarket/tokens/prices) route_allowed=true ;;
  /polymarket/tokens/spreads) route_allowed=true ;;
esac
if [ "$route_allowed" = false ]; then
  route_regexes=(
  '^/kalshi/event/[^/]+$'
  '^/kalshi/event/[^/]+/history$'
  '^/kalshi/event/[^/]+/metadata$'
  '^/kalshi/historical/market/[^/]+$'
  '^/kalshi/historical/market/[^/]+/history$'
  '^/kalshi/market/[^/]+$'
  '^/kalshi/market/[^/]+/history$'
  '^/kalshi/market/[^/]+/orderbook$'
  '^/kalshi/series/[^/]+$'
  '^/metaculus/category/[^/]+/questions$'
  '^/metaculus/project/[^/]+/questions$'
  '^/metaculus/question/[^/]+$'
  '^/metaculus/question/[^/]+/forecast-history$'
  '^/metaculus/question/[^/]+/forecasts$'
  '^/metaculus/question/[^/]+/metadata$'
  '^/metaculus/question/[^/]+/options$'
  '^/metaculus/tournament/[^/]+/questions$'
  '^/polymarket/clob/market/[^/]+$'
  '^/polymarket/event/[^/]+$'
  '^/polymarket/events/[^/]+/tags$'
  '^/polymarket/market/[^/]+$'
  '^/polymarket/market/[^/]+/liquidity$'
  '^/polymarket/market/[^/]+/tags$'
  '^/polymarket/rewards/market/[^/]+$'
  '^/polymarket/tag/[^/]+$'
  '^/polymarket/tag/[^/]+/related-tags$'
  '^/polymarket/token/[^/]+/midpoint$'
  '^/polymarket/token/[^/]+/orderbook$'
  '^/polymarket/token/[^/]+/price$'
  '^/polymarket/token/[^/]+/price-history$'
  '^/polymarket/token/[^/]+/spread$'
  )
  for route_regex in ${route_regexes[@]+"${route_regexes[@]}"}; do
    if [[ "$path" =~ $route_regex ]]; then
      route_allowed=true
      break
    fi
  done
fi
if [ "$route_allowed" = false ]; then
  echo "path is not in the prediction-markets-research skill catalog" >&2
  exit 2
fi

# Enforce the documented HTTP method for each route, not just the global method set.
route_method_allowed=false
route_method_regexes=(
  '^GET:/draftkings/predictions/availability$'
  '^GET:/draftkings/predictions/categories$'
  '^GET:/draftkings/predictions/rules$'
  '^GET:/kalshi/event/[^/]+$'
  '^GET:/kalshi/event/[^/]+/history$'
  '^GET:/kalshi/event/[^/]+/metadata$'
  '^GET:/kalshi/events$'
  '^GET:/kalshi/events/multivariate$'
  '^GET:/kalshi/exchange/schedule$'
  '^GET:/kalshi/exchange/status$'
  '^GET:/kalshi/historical/cutoff$'
  '^GET:/kalshi/historical/market/[^/]+$'
  '^GET:/kalshi/historical/market/[^/]+/history$'
  '^GET:/kalshi/historical/markets$'
  '^GET:/kalshi/historical/trades$'
  '^GET:/kalshi/market/[^/]+$'
  '^GET:/kalshi/market/[^/]+/history$'
  '^GET:/kalshi/market/[^/]+/orderbook$'
  '^GET:/kalshi/markets$'
  '^GET:/kalshi/markets/history$'
  '^GET:/kalshi/markets/orderbooks$'
  '^GET:/kalshi/series$'
  '^GET:/kalshi/series/[^/]+$'
  '^GET:/kalshi/trades$'
  '^GET:/metaculus/category/[^/]+/questions$'
  '^GET:/metaculus/comments-feed$'
  '^GET:/metaculus/project/[^/]+/questions$'
  '^GET:/metaculus/question/[^/]+$'
  '^GET:/metaculus/question/[^/]+/forecast-history$'
  '^GET:/metaculus/question/[^/]+/forecasts$'
  '^GET:/metaculus/question/[^/]+/metadata$'
  '^GET:/metaculus/question/[^/]+/options$'
  '^GET:/metaculus/questions$'
  '^GET:/metaculus/top-comments$'
  '^GET:/metaculus/tournament/[^/]+/questions$'
  '^GET:/polymarket/activity/trades$'
  '^GET:/polymarket/clob/market/[^/]+$'
  '^GET:/polymarket/dashboards/macro$'
  '^GET:/polymarket/event/[^/]+$'
  '^GET:/polymarket/events$'
  '^GET:/polymarket/events/[^/]+/tags$'
  '^GET:/polymarket/events/similar$'
  '^GET:/polymarket/fee-types$'
  '^GET:/polymarket/homepage/feed$'
  '^GET:/polymarket/leaderboard$'
  '^GET:/polymarket/market/[^/]+$'
  '^GET:/polymarket/market/[^/]+/liquidity$'
  '^GET:/polymarket/market/[^/]+/tags$'
  '^GET:/polymarket/markets$'
  '^GET:/polymarket/predictions$'
  '^GET:/polymarket/rewards/market/[^/]+$'
  '^GET:/polymarket/rewards/markets$'
  '^GET:/polymarket/search$'
  '^GET:/polymarket/tag/[^/]+$'
  '^GET:/polymarket/tag/[^/]+/related-tags$'
  '^GET:/polymarket/tags$'
  '^GET:/polymarket/token/[^/]+/midpoint$'
  '^GET:/polymarket/token/[^/]+/orderbook$'
  '^GET:/polymarket/token/[^/]+/price$'
  '^GET:/polymarket/token/[^/]+/price-history$'
  '^GET:/polymarket/token/[^/]+/spread$'
  '^POST:/polymarket/tokens/midpoints$'
  '^POST:/polymarket/tokens/orderbooks$'
  '^POST:/polymarket/tokens/prices$'
  '^POST:/polymarket/tokens/spreads$'
)
for route_method_regex in ${route_method_regexes[@]+"${route_method_regexes[@]}"}; do
  if [[ "$method:$path" =~ $route_method_regex ]]; then
    route_method_allowed=true
    break
  fi
done
if [ "$route_method_allowed" = false ]; then
  echo "method is not allowed for this prediction-markets-research route" >&2
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

if [ "$method" = "GET" ]; then
  # -G + --data-urlencode URL-encodes each value (so spaces etc. are safe).
  qs=()
  for kv in ${rest[@]+"${rest[@]}"}; do
    [ -n "$kv" ] || continue
    # curl treats both @file and name@file forms as local-file input for
    # --data-urlencode. Reject @ outright so query arguments cannot disclose
    # local files to the Crawlora API.
    case "$kv" in
      *@*) echo "@ is not allowed in query arguments" >&2; exit 2 ;;
    esac
    qs+=(--data-urlencode "$kv")
  done
  # -q must be the first curl option: ignore any user ~/.curlrc so inherited
  # config cannot redirect the request, add uploads, or alter credential use.
  curl -q -fsS -G "${auth[@]}" ${qs[@]+"${qs[@]}"} "${base}${path}"
else
  [ -n "$body" ] || body="${rest[0]:-}"
  [ -n "$body" ] || body='{}'
  # Stream the body on stdin so curl never interprets a user value as its
  # @file shorthand (and cannot read local files supplied in a request body).
  printf '%s' "$body" | curl -q -fsS -X "$method" "${auth[@]}" \
    -H "Content-Type: application/json" --data-binary @- "${base}${path}"
fi
