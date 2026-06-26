#!/usr/bin/env bash
# Lookup a Spotify URL on MusicBrainz to find linked entities.
# Usage: mb_lookup.sh <spotify-url>
# Example: mb_lookup.sh https://open.spotify.com/artist/3AnRJXttxRO7191Fxwkaxz

set -euo pipefail

URL="${1:?Usage: mb_lookup.sh <spotify-url>}"
# Load MB username from credentials file if not already set
if [ -z "${MB_USERNAME:-}" ]; then
  SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
  MB_USERNAME=$(jq -r '.username // empty' "$SKILL_DIR/.credentials.json" 2>/dev/null || true)
fi
CONTACT="${MB_USERNAME:-anonymous}@users.noreply.musicbrainz.org"
UA="${OPENCLAW_BOT_NAME:-OpenClawBot}/1.0 ($CONTACT)"
BASE="https://musicbrainz.org/ws/2"

echo "Looking up: $URL"

# Step 1: Find URL entity
RESULT=$(curl -s -A "$UA" "$BASE/url/?resource=$URL&fmt=json")
URL_MBID=$(echo "$RESULT" | jq -r '.id // empty')

if [ -z "$URL_MBID" ]; then
  echo "NOT FOUND on MusicBrainz"
  exit 1
fi

echo "URL MBID: $URL_MBID"

# Step 2: Get linked entities
RELS=$(curl -s -A "$UA" "$BASE/url/$URL_MBID?inc=artist-rels+release-rels+release-group-rels&fmt=json")
echo "$RELS" | jq '{
  url_id: .id,
  resource: .resource,
  relations: [.relations[] | {
    type: .type,
    direction: .direction,
    target_type: ."target-type",
    entity: (
      if ."target-type" == "artist" then .artist
      elif ."target-type" == "release" then .release
      elif ."target-type" == "release_group" then ."release-group"
      else null end
    ) | {id, name, disambiguation, type, country}
  }]
}'
