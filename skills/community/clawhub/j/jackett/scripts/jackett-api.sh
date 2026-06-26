#!/bin/bash
# Jackett Torznab API helper script
# Usage: jackett-api.sh <command> [args...]

set -euo pipefail

DEFAULT_CONFIG="$HOME/.openclaw/credentials/jackett/config.json"

CONFIG_FILE="${JACKETT_CONFIG:-$DEFAULT_CONFIG}"

JACKETT_URL="${JACKETT_URL:-}"
JACKETT_API_KEY="${JACKETT_API_KEY:-${JACKETT_APIKEY:-}}"
DEFAULT_OUTPUT_LIMIT="${JACKETT_DEFAULT_LIMIT:-20}"

load_config() {
    if [[ -n "$JACKETT_URL" && -n "$JACKETT_API_KEY" ]]; then
        return
    fi

    if [[ -f "$CONFIG_FILE" ]]; then
        local cfg_url cfg_api_key
        cfg_url=$(jq -r '.url // empty' "$CONFIG_FILE")
        cfg_api_key=$(jq -r '.apiKey // .apikey // empty' "$CONFIG_FILE")

        JACKETT_URL="${JACKETT_URL:-$cfg_url}"
        JACKETT_API_KEY="${JACKETT_API_KEY:-$cfg_api_key}"
    fi
}

require_config() {
    load_config

    if [[ -z "$JACKETT_URL" ]]; then
        echo "Error: JACKETT_URL must be set (via env or $CONFIG_FILE)" >&2
        exit 1
    fi

    if [[ -z "$JACKETT_API_KEY" ]]; then
        echo "Error: JACKETT_API_KEY must be set (via env or $CONFIG_FILE)" >&2
        exit 1
    fi

    JACKETT_URL="${JACKETT_URL%/}"
}

urlencode() {
    python3 -c 'import sys, urllib.parse; print(urllib.parse.quote_plus(sys.argv[1]))' "$1"
}

add_param() {
    local key="$1"
    local value="${2:-}"
    if [[ -n "$value" ]]; then
        PARAMS+=("${key}=$(urlencode "$value")")
    fi
}

build_url() {
    local indexer="$1"
    local query="apikey=$(urlencode "$JACKETT_API_KEY")"

    if [[ ${#PARAMS[@]} -gt 0 ]]; then
        query+="&$(IFS='&'; echo "${PARAMS[*]}")"
    fi

    echo "${JACKETT_URL}/api/v2.0/indexers/${indexer}/results/torznab/api?${query}"
}

call_api() {
    local indexer="$1"
    local url
    require_config
    url=$(build_url "$indexer")
    curl -fsSL "$url"
}

parse_feed_xml() {
    local limit="$1"
    local offset="$2"

    python3 -c '
import json
import sys
import xml.etree.ElementTree as ET

limit = int(sys.argv[1])
offset = int(sys.argv[2])
xml_input = sys.stdin.read()

if not xml_input.strip():
    json.dump(
        {
            "meta": {
                "total": 0,
                "offset": offset,
                "limit": limit,
                "returned": 0,
                "truncated": False,
                "warning": "Jackett returned an empty response body.",
            },
            "results": [],
        },
        sys.stdout,
        ensure_ascii=False,
        indent=2,
    )
    raise SystemExit(0)

ns = {"torznab": "http://torznab.com/schemas/2015/feed"}
root = ET.fromstring(xml_input)
channel = root.find("channel")
channel_title = channel.findtext("title") if channel is not None else None

results = []
for item in root.findall("./channel/item"):
    attrs = {}
    for attr in item.findall("torznab:attr", ns):
        name = attr.attrib.get("name")
        value = attr.attrib.get("value")
        if name:
            attrs[name] = value

    enclosure = item.find("enclosure")
    categories = []
    for category in item.findall("category"):
        if category.text:
            categories.append(category.text)

    result = {
        "title": item.findtext("title"),
        "guid": item.findtext("guid"),
        "link": item.findtext("link"),
        "details": item.findtext("comments"),
        "publish_date": item.findtext("pubDate"),
        "size": int(item.findtext("size")) if (item.findtext("size") or "").isdigit() else (int(attrs["size"]) if attrs.get("size", "").isdigit() else attrs.get("size")),
        "seeders": int(attrs["seeders"]) if attrs.get("seeders", "").isdigit() else attrs.get("seeders"),
        "peers": int(attrs["peers"]) if attrs.get("peers", "").isdigit() else attrs.get("peers"),
        "grabs": int(attrs["grabs"]) if attrs.get("grabs", "").isdigit() else attrs.get("grabs"),
        "category": categories or None,
        "indexer": attrs.get("jackettindexer") or channel_title,
        "download_url": enclosure.attrib.get("url") if enclosure is not None else None,
        "infohash": attrs.get("infohash"),
        "magneturl": attrs.get("magneturl"),
        "imdb": attrs.get("imdb"),
        "tmdb": attrs.get("tmdb"),
        "tvdb": attrs.get("tvdb"),
    }
    results.append(result)

total_results = len(results)
if offset:
    results = results[offset:]
if limit > 0:
    results = results[:limit]

json.dump(
    {
        "meta": {
            "total": total_results,
            "offset": offset,
            "limit": limit,
            "returned": len(results),
            "truncated": (limit > 0 and (offset + len(results)) < total_results),
        },
        "results": results,
    },
    sys.stdout,
    ensure_ascii=False,
    indent=2,
)
' "$limit" "$offset"
}

usage() {
    cat <<EOF
Jackett Torznab API CLI

Usage: $(basename "$0") <command> [options]

Commands:
  indexers [--configured true|false] [--raw]
  caps [--indexer NAME] [--raw]

  search <query> [--indexer NAME] [--cat CATS] [--limit N] [--offset N] [--raw] [--cache true|false]
  tvsearch [--query Q] [--season N] [--ep N] [--imdbid ID] [--tvdbid ID] [--tmdbid ID] [--year Y] [--genre G] [--indexer NAME] [--cat CATS] [--limit N] [--offset N] [--raw]
  movie [--query Q] [--imdbid ID] [--tmdbid ID] [--year Y] [--genre G] [--indexer NAME] [--cat CATS] [--limit N] [--offset N] [--raw]
  music [--query Q] [--album A] [--artist B] [--track T] [--label L] [--year Y] [--genre G] [--indexer NAME] [--cat CATS] [--limit N] [--offset N] [--raw]
  book [--query Q] [--title T] [--author A] [--publisher P] [--year Y] [--genre G] [--indexer NAME] [--cat CATS] [--limit N] [--offset N] [--raw]

Options:
  --indexer, -i     Jackett indexer name, "all", or a filter expression (default: all)
  --cat             Comma-separated category ids
  --limit           Client-side result limit after parsing XML (default: ${DEFAULT_OUTPUT_LIMIT})
  --offset          Client-side result offset after parsing XML
  --cache           Pass cache=true|false to Jackett
  --raw             Print raw XML instead of parsed JSON

Examples:
  $(basename "$0") indexers --configured true
  $(basename "$0") search "ubuntu 24.04"
  $(basename "$0") search "dune 2024" --indexer nyaasi
  $(basename "$0") search "linux iso" --indexer "tag:public,lang:en"
  $(basename "$0") tvsearch --query "Foundation" --season 2 --ep 1
  $(basename "$0") movie --imdbid tt1160419
EOF
}

cmd_indexers() {
    local configured="" raw="false"

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --configured) configured="$2"; shift 2 ;;
            --raw) raw="true"; shift ;;
            *) echo "Unknown option: $1" >&2; exit 1 ;;
        esac
    done

    PARAMS=()
    add_param "t" "indexers"
    add_param "configured" "$configured"

    if [[ "$raw" == "true" ]]; then
        call_api "all"
    else
        call_api "all"
    fi
}

cmd_caps() {
    local indexer="all" raw="false"

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --indexer|-i) indexer="$2"; shift 2 ;;
            --raw) raw="true"; shift ;;
            *) echo "Unknown option: $1" >&2; exit 1 ;;
        esac
    done

    PARAMS=()
    add_param "t" "caps"

    if [[ "$raw" == "true" ]]; then
        call_api "$indexer"
    else
        call_api "$indexer"
    fi
}

run_search_mode() {
    local mode="$1"
    shift

    local indexer="all" cat="" limit="$DEFAULT_OUTPUT_LIMIT" offset="0" raw="false" cache=""

    PARAMS=()
    add_param "t" "$mode"

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --indexer|-i) indexer="$2"; shift 2 ;;
            --cat|--category) cat="$2"; shift 2 ;;
            --limit) limit="$2"; shift 2 ;;
            --offset) offset="$2"; shift 2 ;;
            --cache) cache="$2"; shift 2 ;;
            --raw) raw="true"; shift ;;
            --query|-q) add_param "q" "$2"; shift 2 ;;
            --season) add_param "season" "$2"; shift 2 ;;
            --ep|--episode) add_param "ep" "$2"; shift 2 ;;
            --imdbid) add_param "imdbid" "$2"; shift 2 ;;
            --tvdbid) add_param "tvdbid" "$2"; shift 2 ;;
            --tmdbid) add_param "tmdbid" "$2"; shift 2 ;;
            --tvmazeid) add_param "tvmazeid" "$2"; shift 2 ;;
            --traktid) add_param "traktid" "$2"; shift 2 ;;
            --doubanid) add_param "doubanid" "$2"; shift 2 ;;
            --album) add_param "album" "$2"; shift 2 ;;
            --artist) add_param "artist" "$2"; shift 2 ;;
            --label) add_param "label" "$2"; shift 2 ;;
            --track) add_param "track" "$2"; shift 2 ;;
            --title) add_param "title" "$2"; shift 2 ;;
            --author) add_param "author" "$2"; shift 2 ;;
            --publisher) add_param "publisher" "$2"; shift 2 ;;
            --year) add_param "year" "$2"; shift 2 ;;
            --genre) add_param "genre" "$2"; shift 2 ;;
            --) shift; break ;;
            *)
                if [[ "$mode" == "search" && -z "${SEEN_POSITIONAL_QUERY:-}" ]]; then
                    add_param "q" "$1"
                    SEEN_POSITIONAL_QUERY=1
                    shift
                else
                    echo "Unknown option: $1" >&2
                    exit 1
                fi
                ;;
        esac
    done

    add_param "cat" "$cat"
    add_param "cache" "$cache"

    if [[ "$raw" == "true" ]]; then
        call_api "$indexer"
    else
        call_api "$indexer" | parse_feed_xml "$limit" "$offset"
    fi
}

main() {
    local cmd="${1:-}"
    [[ $# -gt 0 ]] && shift || true

    case "$cmd" in
        indexers) cmd_indexers "$@" ;;
        caps) cmd_caps "$@" ;;
        search) unset SEEN_POSITIONAL_QUERY || true; run_search_mode "search" "$@" ;;
        tvsearch) unset SEEN_POSITIONAL_QUERY || true; run_search_mode "tvsearch" "$@" ;;
        movie) unset SEEN_POSITIONAL_QUERY || true; run_search_mode "movie" "$@" ;;
        music) unset SEEN_POSITIONAL_QUERY || true; run_search_mode "music" "$@" ;;
        book) unset SEEN_POSITIONAL_QUERY || true; run_search_mode "book" "$@" ;;
        ""|-h|--help|help) usage ;;
        *) echo "Unknown command: $cmd" >&2; usage; exit 1 ;;
    esac
}

main "$@"
