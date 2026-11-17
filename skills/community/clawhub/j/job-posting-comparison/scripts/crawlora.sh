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
    echo "only GET and POST are supported by the job-posting-comparison skill" >&2
    exit 2
    ;;
esac

# Reject path syntax that could smuggle a route through a shell glob check.
case "$path" in
  ""|*[?#%]*|*..*|*//* )
    echo "invalid path for the job-posting-comparison skill" >&2
    exit 2
    ;;
esac

# Static routes use escaped case patterns. Parameterized routes use anchored
# extended regular expressions so every {param} is exactly one non-empty path
# segment; unlike a case '*', [^/]+ cannot consume another slash.
route_allowed=false
case "$path" in
  /datasets/jobs/companies) route_allowed=true ;;
  /datasets/jobs/facets) route_allowed=true ;;
  /datasets/jobs/search) route_allowed=true ;;
  /indeed/job) route_allowed=true ;;
  /indeed/search) route_allowed=true ;;
  /jobs/ashby/board) route_allowed=true ;;
  /jobs/company-search) route_allowed=true ;;
  /jobs/eightfold/board) route_allowed=true ;;
  /jobs/eightfold/job) route_allowed=true ;;
  /jobs/gem/board) route_allowed=true ;;
  /jobs/greenhouse/board) route_allowed=true ;;
  /jobs/greenhouse/job) route_allowed=true ;;
  /jobs/icims/board) route_allowed=true ;;
  /jobs/icims/job) route_allowed=true ;;
  /jobs/lever/posting) route_allowed=true ;;
  /jobs/lever/postings) route_allowed=true ;;
  /jobs/oracle/board) route_allowed=true ;;
  /jobs/oracle/job) route_allowed=true ;;
  /jobs/personio/feed) route_allowed=true ;;
  /jobs/phenom/board) route_allowed=true ;;
  /jobs/phenom/job) route_allowed=true ;;
  /jobs/pinpoint/board) route_allowed=true ;;
  /jobs/recruitee/offer) route_allowed=true ;;
  /jobs/recruitee/offers) route_allowed=true ;;
  /jobs/rippling/board) route_allowed=true ;;
  /jobs/rippling/job) route_allowed=true ;;
  /jobs/smartrecruiters/posting) route_allowed=true ;;
  /jobs/smartrecruiters/postings) route_allowed=true ;;
  /jobs/teamtailor/jobs) route_allowed=true ;;
  /jobs/ukg/board) route_allowed=true ;;
  /jobs/workable/posting) route_allowed=true ;;
  /jobs/workable/postings) route_allowed=true ;;
  /jobs/workday/board) route_allowed=true ;;
  /jobs/workday/job) route_allowed=true ;;
  /web/scrape) route_allowed=true ;;
esac
if [ "$route_allowed" = false ]; then
  route_regexes=(
  '^/datasets/jobs/companies/[^/]+$'
  '^/datasets/jobs/items/[^/]+$'
  )
  for route_regex in ${route_regexes[@]+"${route_regexes[@]}"}; do
    if [[ "$path" =~ $route_regex ]]; then
      route_allowed=true
      break
    fi
  done
fi
if [ "$route_allowed" = false ]; then
  echo "path is not in the job-posting-comparison skill catalog" >&2
  exit 2
fi

# Enforce the documented HTTP method for each route, not just the global method set.
route_method_allowed=false
route_method_regexes=(
  '^GET:/datasets/jobs/companies$'
  '^GET:/datasets/jobs/companies/[^/]+$'
  '^GET:/datasets/jobs/facets$'
  '^GET:/datasets/jobs/items/[^/]+$'
  '^GET:/datasets/jobs/search$'
  '^GET:/indeed/job$'
  '^GET:/indeed/search$'
  '^GET:/jobs/ashby/board$'
  '^GET:/jobs/company-search$'
  '^GET:/jobs/eightfold/board$'
  '^GET:/jobs/eightfold/job$'
  '^GET:/jobs/gem/board$'
  '^GET:/jobs/greenhouse/board$'
  '^GET:/jobs/greenhouse/job$'
  '^GET:/jobs/icims/board$'
  '^GET:/jobs/icims/job$'
  '^GET:/jobs/lever/posting$'
  '^GET:/jobs/lever/postings$'
  '^GET:/jobs/oracle/board$'
  '^GET:/jobs/oracle/job$'
  '^GET:/jobs/personio/feed$'
  '^GET:/jobs/phenom/board$'
  '^GET:/jobs/phenom/job$'
  '^GET:/jobs/pinpoint/board$'
  '^GET:/jobs/recruitee/offer$'
  '^GET:/jobs/recruitee/offers$'
  '^GET:/jobs/rippling/board$'
  '^GET:/jobs/rippling/job$'
  '^GET:/jobs/smartrecruiters/posting$'
  '^GET:/jobs/smartrecruiters/postings$'
  '^GET:/jobs/teamtailor/jobs$'
  '^GET:/jobs/ukg/board$'
  '^GET:/jobs/workable/posting$'
  '^GET:/jobs/workable/postings$'
  '^GET:/jobs/workday/board$'
  '^GET:/jobs/workday/job$'
  '^POST:/web/scrape$'
)
for route_method_regex in ${route_method_regexes[@]+"${route_method_regexes[@]}"}; do
  if [[ "$method:$path" =~ $route_method_regex ]]; then
    route_method_allowed=true
    break
  fi
done
if [ "$route_method_allowed" = false ]; then
  echo "method is not allowed for this job-posting-comparison route" >&2
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
