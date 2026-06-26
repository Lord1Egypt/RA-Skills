#!/usr/bin/env bash
# Verify the skill is seeing current OpenClaw docs.
# Prints page count, sha256, server Last-Modified, and local fetch timestamp —
# proves this is live, not cached.
set -eu
url=https://docs.openclaw.ai/llms.txt
tmp=$(mktemp)
hdr=$(mktemp)
trap 'rm -f "$tmp" "$hdr"' EXIT
curl -sfL -D "$hdr" "$url" > "$tmp"
pages=$(grep -c "^- \[" "$tmp" || true)
if command -v shasum >/dev/null 2>&1; then
  sha=$(shasum -a 256 "$tmp" | awk '{print $1}')
elif command -v sha256sum >/dev/null 2>&1; then
  sha=$(sha256sum "$tmp" | awk '{print $1}')
else
  sha="(no sha256 tool)"
fi
last_mod=$(awk 'BEGIN{IGNORECASE=1} /^last-modified:/ {sub(/^[^:]+: */, ""); sub(/\r$/, ""); print; exit}' "$hdr")
[ -z "$last_mod" ] && last_mod="(not advertised by server)"
printf 'source:        %s\npages:         %s\nsha256:        %s\nserver_mtime:  %s\nfetched:       %s\n' \
  "$url" "$pages" "$sha" "$last_mod" "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
