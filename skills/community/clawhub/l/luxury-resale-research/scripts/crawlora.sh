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
    -X|-d) echo "only GET are supported by the luxury-resale-research skill" >&2; exit 2 ;;
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
    echo "only GET are supported by the luxury-resale-research skill" >&2
    exit 2
    ;;
esac

# Reject path syntax that could smuggle a route through a shell glob check.
case "$path" in
  ""|*[?#%]*|*..*|*//* )
    echo "invalid path for the luxury-resale-research skill" >&2
    exit 2
    ;;
esac

# Static routes use escaped case patterns. Parameterized routes use anchored
# extended regular expressions so every {param} is exactly one non-empty path
# segment; unlike a case '*', [^/]+ cannot consume another slash.
route_allowed=false
case "$path" in
  /1stdibs/categories) route_allowed=true ;;
  /1stdibs/designers) route_allowed=true ;;
  /1stdibs/product) route_allowed=true ;;
  /1stdibs/search) route_allowed=true ;;
  /balenciaga/categories) route_allowed=true ;;
  /balenciaga/category) route_allowed=true ;;
  /balenciaga/product) route_allowed=true ;;
  /balenciaga/product/variants) route_allowed=true ;;
  /balenciaga/search) route_allowed=true ;;
  /balenciaga/store-countries) route_allowed=true ;;
  /balenciaga/stores) route_allowed=true ;;
  /burberry/categories) route_allowed=true ;;
  /burberry/category) route_allowed=true ;;
  /burberry/product) route_allowed=true ;;
  /burberry/related) route_allowed=true ;;
  /burberry/search) route_allowed=true ;;
  /burberry/suggest) route_allowed=true ;;
  /chrono24/autocomplete) route_allowed=true ;;
  /chrono24/brands) route_allowed=true ;;
  /chrono24/dealer) route_allowed=true ;;
  /chrono24/dealer/reviews) route_allowed=true ;;
  /chrono24/facets) route_allowed=true ;;
  /chrono24/listing) route_allowed=true ;;
  /chrono24/models) route_allowed=true ;;
  /chrono24/search) route_allowed=true ;;
  /depop/brands) route_allowed=true ;;
  /depop/categories) route_allowed=true ;;
  /depop/search) route_allowed=true ;;
  /depop/search-sellers) route_allowed=true ;;
  /depop/search/facets) route_allowed=true ;;
  /depop/sizes) route_allowed=true ;;
  /depop/suggest) route_allowed=true ;;
  /farfetch/categories) route_allowed=true ;;
  /farfetch/designers) route_allowed=true ;;
  /farfetch/product) route_allowed=true ;;
  /farfetch/search) route_allowed=true ;;
  /fashionphile/collections) route_allowed=true ;;
  /fashionphile/pages) route_allowed=true ;;
  /fashionphile/products) route_allowed=true ;;
  /fashionphile/search) route_allowed=true ;;
  /fashionphile/search/suggest) route_allowed=true ;;
  /fashionphile/sitemap/urls) route_allowed=true ;;
  /fashionphile/sitemaps) route_allowed=true ;;
  /fashionphile/store) route_allowed=true ;;
  /goat/collection) route_allowed=true ;;
  /goat/countries) route_allowed=true ;;
  /goat/curated) route_allowed=true ;;
  /goat/listings/count) route_allowed=true ;;
  /goat/search) route_allowed=true ;;
  /goat/search/facets) route_allowed=true ;;
  /goat/searches/trending) route_allowed=true ;;
  /goat/suggest) route_allowed=true ;;
  /grailed/categories) route_allowed=true ;;
  /grailed/collection) route_allowed=true ;;
  /grailed/collections) route_allowed=true ;;
  /grailed/designers) route_allowed=true ;;
  /grailed/listing) route_allowed=true ;;
  /grailed/search) route_allowed=true ;;
  /grailed/seller) route_allowed=true ;;
  /grailed/seller-reviews) route_allowed=true ;;
  /grailed/similar-listings) route_allowed=true ;;
  /grailed/sold-listings) route_allowed=true ;;
  /grailed/suggest) route_allowed=true ;;
  /gucci/categories) route_allowed=true ;;
  /gucci/category) route_allowed=true ;;
  /gucci/product) route_allowed=true ;;
  /gucci/recommendations) route_allowed=true ;;
  /gucci/search) route_allowed=true ;;
  /gucci/size-guide) route_allowed=true ;;
  /gucci/store) route_allowed=true ;;
  /gucci/stores) route_allowed=true ;;
  /gucci/stores/search) route_allowed=true ;;
  /gucci/suggest) route_allowed=true ;;
  /hermes/categories) route_allowed=true ;;
  /hermes/category) route_allowed=true ;;
  /hermes/product) route_allowed=true ;;
  /hermes/product/recommendations) route_allowed=true ;;
  /hermes/products) route_allowed=true ;;
  /hermes/search) route_allowed=true ;;
  /hermes/stores) route_allowed=true ;;
  /hermes/suggest) route_allowed=true ;;
  /modaoperandi/categories) route_allowed=true ;;
  /modaoperandi/designers) route_allowed=true ;;
  /modaoperandi/product) route_allowed=true ;;
  /modaoperandi/search) route_allowed=true ;;
  /moncler/categories) route_allowed=true ;;
  /moncler/category) route_allowed=true ;;
  /moncler/product) route_allowed=true ;;
  /moncler/search) route_allowed=true ;;
  /moncler/stores) route_allowed=true ;;
  /moncler/suggest) route_allowed=true ;;
  /poshmark/brands) route_allowed=true ;;
  /poshmark/categories) route_allowed=true ;;
  /poshmark/search) route_allowed=true ;;
  /prada/categories) route_allowed=true ;;
  /prada/category) route_allowed=true ;;
  /prada/product) route_allowed=true ;;
  /prada/search) route_allowed=true ;;
  /prada/stores) route_allowed=true ;;
  /prada/suggest) route_allowed=true ;;
  /rebag/collections) route_allowed=true ;;
  /rebag/pages) route_allowed=true ;;
  /rebag/products) route_allowed=true ;;
  /rebag/search) route_allowed=true ;;
  /rebag/search/suggest) route_allowed=true ;;
  /rebag/sitemap/urls) route_allowed=true ;;
  /rebag/sitemaps) route_allowed=true ;;
  /rebag/store) route_allowed=true ;;
  /stockx/brands) route_allowed=true ;;
  /stockx/categories) route_allowed=true ;;
  /stockx/releases) route_allowed=true ;;
  /stockx/search) route_allowed=true ;;
  /therealreal/autocomplete) route_allowed=true ;;
  /therealreal/categories) route_allowed=true ;;
  /therealreal/category) route_allowed=true ;;
  /therealreal/collection) route_allowed=true ;;
  /therealreal/collections) route_allowed=true ;;
  /therealreal/conditions) route_allowed=true ;;
  /therealreal/designer) route_allowed=true ;;
  /therealreal/designers) route_allowed=true ;;
  /therealreal/listing) route_allowed=true ;;
  /therealreal/search) route_allowed=true ;;
  /therealreal/similar) route_allowed=true ;;
  /tiffany/categories) route_allowed=true ;;
  /tiffany/category) route_allowed=true ;;
  /tiffany/content-search) route_allowed=true ;;
  /tiffany/filters) route_allowed=true ;;
  /tiffany/product) route_allowed=true ;;
  /tiffany/search) route_allowed=true ;;
  /tiffany/stores) route_allowed=true ;;
  /tiffany/suggest) route_allowed=true ;;
  /vestiaire/brands) route_allowed=true ;;
  /vestiaire/categories) route_allowed=true ;;
  /vestiaire/conditions) route_allowed=true ;;
  /vestiaire/product) route_allowed=true ;;
  /vestiaire/search) route_allowed=true ;;
  /vestiaire/search-sellers) route_allowed=true ;;
  /vestiaire/seller) route_allowed=true ;;
  /vestiaire/suggest) route_allowed=true ;;
  /yoox/categories) route_allowed=true ;;
  /yoox/designers) route_allowed=true ;;
  /yoox/product) route_allowed=true ;;
  /yoox/search) route_allowed=true ;;
esac
if [ "$route_allowed" = false ]; then
  route_regexes=(
  '^/depop/item/[^/]+$'
  '^/depop/item/[^/]+/similar$'
  '^/depop/shop/[^/]+$'
  '^/fashionphile/collections/[^/]+/products$'
  '^/fashionphile/pages/[^/]+$'
  '^/fashionphile/products/[^/]+$'
  '^/fashionphile/products/[^/]+/recommendations$'
  '^/goat/product/[^/]+$'
  '^/goat/product/[^/]+/recommended$'
  '^/poshmark/brand/[^/]+$'
  '^/poshmark/category/[^/]+$'
  '^/poshmark/closet/[^/]+$'
  '^/poshmark/listing/[^/]+$'
  '^/poshmark/trend/[^/]+$'
  '^/rebag/collections/[^/]+/products$'
  '^/rebag/pages/[^/]+$'
  '^/rebag/products/[^/]+$'
  '^/rebag/products/[^/]+/recommendations$'
  '^/stockx/product/[^/]+$'
  )
  for route_regex in ${route_regexes[@]+"${route_regexes[@]}"}; do
    if [[ "$path" =~ $route_regex ]]; then
      route_allowed=true
      break
    fi
  done
fi
if [ "$route_allowed" = false ]; then
  echo "path is not in the luxury-resale-research skill catalog" >&2
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