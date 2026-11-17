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
    -X|-d) echo "only GET are supported by the music-podcast-research skill" >&2; exit 2 ;;
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
    echo "only GET are supported by the music-podcast-research skill" >&2
    exit 2
    ;;
esac

# Reject path syntax that could smuggle a route through a shell glob check.
case "$path" in
  ""|*[?#%]*|*..*|*//* )
    echo "invalid path for the music-podcast-research skill" >&2
    exit 2
    ;;
esac

# Static routes use escaped case patterns. Parameterized routes use anchored
# extended regular expressions so every {param} is exactly one non-empty path
# segment; unlike a case '*', [^/]+ cannot consume another slash.
route_allowed=false
case "$path" in
  /apple-podcasts/charts) route_allowed=true ;;
  /apple-podcasts/charts/rankings) route_allowed=true ;;
  /apple-podcasts/episodes/search) route_allowed=true ;;
  /apple-podcasts/new) route_allowed=true ;;
  /apple-podcasts/search) route_allowed=true ;;
  /discogs/search) route_allowed=true ;;
  /soundcloud/playlist) route_allowed=true ;;
  /soundcloud/profile) route_allowed=true ;;
  /soundcloud/search) route_allowed=true ;;
  /soundcloud/track) route_allowed=true ;;
  /soundcloud/user-tracks) route_allowed=true ;;
  /spotify-podcasts/categories) route_allowed=true ;;
  /spotify-podcasts/charts) route_allowed=true ;;
  /spotify-podcasts/episode) route_allowed=true ;;
  /spotify-podcasts/home) route_allowed=true ;;
  /spotify-podcasts/search) route_allowed=true ;;
  /spotify-podcasts/show) route_allowed=true ;;
  /spotify-podcasts/show/episodes) route_allowed=true ;;
  /spotify-podcasts/show/recommendations) route_allowed=true ;;
  /spotify/album) route_allowed=true ;;
  /spotify/album/tracks) route_allowed=true ;;
  /spotify/albums/search) route_allowed=true ;;
  /spotify/artist) route_allowed=true ;;
  /spotify/artist/albums) route_allowed=true ;;
  /spotify/artist/playlists) route_allowed=true ;;
  /spotify/artist/related) route_allowed=true ;;
  /spotify/artists/search) route_allowed=true ;;
  /spotify/audiobook) route_allowed=true ;;
  /spotify/audiobook/chapters) route_allowed=true ;;
  /spotify/audiobooks/search) route_allowed=true ;;
  /spotify/chapter) route_allowed=true ;;
  /spotify/episodes/search) route_allowed=true ;;
  /spotify/featured-charts-by-country) route_allowed=true ;;
  /spotify/genre) route_allowed=true ;;
  /spotify/home) route_allowed=true ;;
  /spotify/playlist) route_allowed=true ;;
  /spotify/playlists/search) route_allowed=true ;;
  /spotify/popular-by-country) route_allowed=true ;;
  /spotify/profile) route_allowed=true ;;
  /spotify/profile/followers) route_allowed=true ;;
  /spotify/profile/playlists) route_allowed=true ;;
  /spotify/profiles/search) route_allowed=true ;;
  /spotify/search) route_allowed=true ;;
  /spotify/section) route_allowed=true ;;
  /spotify/shows/search) route_allowed=true ;;
  /spotify/track) route_allowed=true ;;
  /spotify/track/recommended) route_allowed=true ;;
  /spotify/track/similar-albums) route_allowed=true ;;
  /spotify/tracks/search) route_allowed=true ;;
esac
if [ "$route_allowed" = false ]; then
  route_regexes=(
  '^/apple-podcasts/show/[^/]+$'
  '^/apple-podcasts/show/[^/]+/episodes$'
  '^/apple-podcasts/show/[^/]+/related$'
  '^/discogs/artist/[^/]+$'
  '^/discogs/artist/[^/]+/releases$'
  '^/discogs/label/[^/]+$'
  '^/discogs/label/[^/]+/releases$'
  '^/discogs/master/[^/]+$'
  '^/discogs/release/[^/]+$'
  )
  for route_regex in ${route_regexes[@]+"${route_regexes[@]}"}; do
    if [[ "$path" =~ $route_regex ]]; then
      route_allowed=true
      break
    fi
  done
fi
if [ "$route_allowed" = false ]; then
  echo "path is not in the music-podcast-research skill catalog" >&2
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