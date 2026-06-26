#!/usr/bin/env bash
set -euo pipefail
MOPIDY_URL="${MOPIDY_URL:-}"

if [ -z "$MOPIDY_URL" ]; then
  echo "MOPIDY_URL is not set. Example: export MOPIDY_URL='https://your-host.example.com/mopidy/rpc'" >&2
  exit 1
fi

rpc() {
  local payload="$1"
  curl -sS -H 'Content-Type: application/json' -d "$payload" "$MOPIDY_URL"
}

usage() {
  cat <<'EOF'
Usage:
  mopidy.sh state
  mopidy.sh current
  mopidy.sh queue
  mopidy.sh playlists
  mopidy.sh search <query>
  mopidy.sh add-track <track-uri>
  mopidy.sh add-album <album-uri>
  mopidy.sh add-playlist-to-queue <playlist-uri>
  mopidy.sh play
  mopidy.sh play-track <track-uri>
  mopidy.sh pause
  mopidy.sh next
  mopidy.sh previous
  mopidy.sh clear
EOF
}

cmd="${1:-}"
shift || true

case "$cmd" in
  state)
    rpc '{"jsonrpc":"2.0","id":1,"method":"core.playback.get_state"}'
    ;;
  current)
    rpc '{"jsonrpc":"2.0","id":1,"method":"core.playback.get_current_track"}'
    ;;
  queue)
    rpc '{"jsonrpc":"2.0","id":1,"method":"core.tracklist.get_tl_tracks"}'
    ;;
  playlists)
    rpc '{"jsonrpc":"2.0","id":1,"method":"core.playlists.as_list"}'
    ;;
  search)
    q="${*:-}"
    [ -n "$q" ] || { echo "search query required" >&2; exit 1; }
    jq -nc --arg q "$q" '{jsonrpc:"2.0",id:1,method:"core.library.search",params:{query:{any:[$q]},uris:null,exact:false}}' | curl -ksS -H 'Content-Type: application/json' -d @- "$MOPIDY_URL"
    ;;
  add-track)
    uri="${1:-}"
    [ -n "$uri" ] || { echo "track uri required" >&2; exit 1; }
    jq -nc --arg uri "$uri" '{jsonrpc:"2.0",id:1,method:"core.tracklist.add",params:{uris:[$uri]}}' | curl -ksS -H 'Content-Type: application/json' -d @- "$MOPIDY_URL"
    ;;
  add-album)
    uri="${1:-}"
    [ -n "$uri" ] || { echo "album uri required" >&2; exit 1; }
    jq -nc --arg uri "$uri" '{jsonrpc:"2.0",id:1,method:"core.tracklist.add",params:{uris:[$uri]}}' | curl -ksS -H 'Content-Type: application/json' -d @- "$MOPIDY_URL"
    ;;
  add-playlist-to-queue)
    uri="${1:-}"
    [ -n "$uri" ] || { echo "playlist uri required" >&2; exit 1; }
    lookup=$(jq -nc --arg uri "$uri" '{jsonrpc:"2.0",id:1,method:"core.playlists.lookup",params:{uri:$uri}}' | curl -ksS -H 'Content-Type: application/json' -d @- "$MOPIDY_URL")
    uris=$(printf '%s' "$lookup" | jq '[.result.tracks[].uri]')
    jq -nc --argjson uris "$uris" '{jsonrpc:"2.0",id:1,method:"core.tracklist.add",params:{uris:$uris}}' | curl -ksS -H 'Content-Type: application/json' -d @- "$MOPIDY_URL"
    ;;
  play)
    rpc '{"jsonrpc":"2.0","id":1,"method":"core.playback.play"}'
    ;;
  play-track)
    uri="${1:-}"
    [ -n "$uri" ] || { echo "track uri required" >&2; exit 1; }
    rpc '{"jsonrpc":"2.0","id":1,"method":"core.tracklist.clear"}' >/dev/null
    jq -nc --arg uri "$uri" '{jsonrpc:"2.0",id:1,method:"core.tracklist.add",params:{uris:[$uri]}}' | curl -ksS -H 'Content-Type: application/json' -d @- "$MOPIDY_URL" >/dev/null
    rpc '{"jsonrpc":"2.0","id":1,"method":"core.playback.play"}'
    ;;
  pause)
    rpc '{"jsonrpc":"2.0","id":1,"method":"core.playback.pause"}'
    ;;
  next)
    rpc '{"jsonrpc":"2.0","id":1,"method":"core.playback.next"}'
    ;;
  previous)
    rpc '{"jsonrpc":"2.0","id":1,"method":"core.playback.previous"}'
    ;;
  clear)
    rpc '{"jsonrpc":"2.0","id":1,"method":"core.tracklist.clear"}'
    ;;
  *)
    usage
    exit 1
    ;;
esac
