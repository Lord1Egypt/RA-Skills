#!/bin/sh
# min-web-search: Bing web search — pure POSIX shell
# Usage: ./search.sh "query" [--max N] [--json]
#
# Dependencies: curl or wget + sed + grep -oP + awk
# Uses Bing China RSS — no API key, no proxy needed.

set -e

# ── arg parsing ──
QUERY=""
MAX=5
JSON=0

while [ $# -gt 0 ]; do
    case "$1" in
        --json) JSON=1; shift ;;
        --max) MAX="$2"; shift 2 ;;
        -*) echo "Unknown option: $1" >&2; exit 1 ;;
        *)  QUERY="$1"; shift ;;
    esac
done

if [ -z "$QUERY" ]; then
    echo "Usage: $0 \"query\" [--max N] [--json]" >&2
    exit 1
fi

# ── URL encode ──
urlencode() {
    printf '%s' "$1" | awk '{
        n = split($0, chars, "")
        for (i = 1; i <= n; i++) {
            c = chars[i]
            if (c ~ /^[a-zA-Z0-9_.~-]$/) printf "%s", c
            else printf "%%%02X", int(c)
        }
    }'
}

ENCODED=$(urlencode "$QUERY")
URL="https://www.bing.com/search?q=${ENCODED}&format=rss"

# ── fetch RSS ──
RSS=""
if command -v curl >/dev/null 2>&1; then
    RSS=$(curl -sS --connect-timeout 10 -A "Mozilla/5.0" "$URL" 2>/dev/null) || true
elif command -v wget >/dev/null 2>&1; then
    RSS=$(wget -q -O - --timeout=10 --header="User-Agent: Mozilla/5.0" "$URL" 2>/dev/null) || true
else
    echo "ERROR: neither curl or wget found" >&2
    exit 1
fi

if [ -z "$RSS" ]; then
    if [ "$JSON" = "1" ]; then
        echo '{"success":false,"error":"network request failed"}'
    else
        echo "ERROR: network request failed" >&2
    fi
    exit 1
fi

# ── parse: split <item> onto separate lines, extract fields ──
RESULTS=$(echo "$RSS" | sed 's/<item>/\n<item>/g' | grep '^<item>' | sed 's/<\/item>//g' | awk -v max="$MAX" '
/<item>/ {
    title=""; link=""; desc=""
    if (match($0, /<title>[^<]*<\/title>/)) {
        s=substr($0, RSTART, RLENGTH)
        gsub(/<\/?title>/, "", s); title=s
    }
    if (match($0, /<link>[^<]*<\/link>/)) {
        s=substr($0, RSTART, RLENGTH)
        gsub(/<\/?link>/, "", s); link=s
    }
    if (match($0, /<description>[^<]*<\/description>/)) {
        s=substr($0, RSTART, RLENGTH)
        gsub(/<\/?description>/, "", s)
        gsub(/<[^>]*>/, "", s); desc=s
    }
    if (title != "" && link != "") {
        n++
        if (n <= max) printf "%s\t%s\t%s\n", title, link, desc
    }
}')

COUNT=$(echo "$RESULTS" | grep -c . 2>/dev/null || echo 0)

if [ "$COUNT" = "0" ]; then
    if [ "$JSON" = "1" ]; then
        echo '{"success":false,"error":"no results"}'
    else
        echo "ERROR: no results" >&2
    fi
    exit 1
fi

# ── output ──
if [ "$JSON" = "1" ]; then
    echo "$RESULTS" | awk -F'\t' -v q="$QUERY" '
    BEGIN { printf "{\"success\":true,\"query\":\"%s\",\"results\":[", q; first=1 }
    {
        if (!first) printf ","; first=0
        title=$1; url=$2; snip=$3
        gsub(/\\/, "\\\\", title); gsub(/"/, "\\\"", title)
        gsub(/\\/, "\\\\", url); gsub(/"/, "\\\"", url)
        gsub(/\\/, "\\\\", snip); gsub(/"/, "\\\"", snip)
        printf "{\"title\":\"%s\",\"url\":\"%s\",\"snippet\":\"%s\"}", title, url, snip
    }
    END { printf "]}" }
    '
    echo
else
    echo "$RESULTS" | awk -F'\t' '
    { printf "%d. %s\n   %s\n", NR, $1, $2 }
    $3 != "" { printf "   %.200s\n", $3 }
    { print "" }
    '
fi
