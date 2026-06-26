#!/usr/bin/env bash
# kannaka-radio CLI wrapper v2
#
# Usage:
#   ./scripts/radio.sh start [--port 8888] [--music-dir /path/to/music]
#   ./scripts/radio.sh stop
#   ./scripts/radio.sh restart [...]
#   ./scripts/radio.sh status
#   ./scripts/radio.sh now-playing
#   ./scripts/radio.sh perception
#   ./scripts/radio.sh next
#   ./scripts/radio.sh prev
#   ./scripts/radio.sh jump <track-index>
#   ./scripts/radio.sh load-album <name>
#   ./scripts/radio.sh set-dir <path>
#   ./scripts/radio.sh library
#   ./scripts/radio.sh queue
#   ./scripts/radio.sh listeners
#   ./scripts/radio.sh live-status
#   ./scripts/radio.sh live-start
#   ./scripts/radio.sh live-stop
#   ./scripts/radio.sh dj-voice
#   ./scripts/radio.sh dj-toggle
#   ./scripts/radio.sh dreams
#   ./scripts/radio.sh dream-trigger
#   ./scripts/radio.sh requests
#   ./scripts/radio.sh sync

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RADIO_DIR="$(cd "$SKILL_DIR/../../.." && pwd)"   # repo root
SERVER_JS="$RADIO_DIR/server/index.js"
PID_FILE="$RADIO_DIR/.radio.pid"
PORT="${RADIO_PORT:-8888}"
BASE_URL="http://localhost:$PORT"

# ── Helpers ─────────────────────────────────────────────────

is_running() {
  if [[ -f "$PID_FILE" ]]; then
    local pid
    pid=$(cat "$PID_FILE")
    kill -0 "$pid" 2>/dev/null && return 0
  fi
  return 1
}

api() {
  local method="$1" path="$2"
  shift 2
  curl -sf -X "$method" "$BASE_URL$path" "$@"
}

json_field() {
  if command -v jq &>/dev/null; then
    jq "$@"
  else
    cat
  fi
}

# ── Commands ─────────────────────────────────────────────────

cmd_start() {
  if is_running; then
    echo "Kannaka Radio already running (PID $(cat "$PID_FILE"))"
    echo "   Player: $BASE_URL"
    return 0
  fi

  local extra_args=("$@")
  echo "Starting Kannaka Radio v2..."
  node "$SERVER_JS" --port "$PORT" "${extra_args[@]}" &
  echo $! > "$PID_FILE"
  sleep 1.5

  if is_running; then
    echo "   Running on $BASE_URL (PID $(cat "$PID_FILE"))"
  else
    echo "   Failed to start — check server.js for errors"
    rm -f "$PID_FILE"
    exit 1
  fi
}

cmd_stop() {
  if ! is_running; then
    echo "Kannaka Radio is not running"
    return 0
  fi
  local pid
  pid=$(cat "$PID_FILE")
  kill "$pid" 2>/dev/null && echo "Stopped (PID $pid)" || echo "Already stopped"
  rm -f "$PID_FILE"
}

cmd_restart() {
  cmd_stop
  sleep 1
  cmd_start "$@"
}

cmd_status() {
  if is_running; then
    local pid
    pid=$(cat "$PID_FILE")
    echo "Kannaka Radio v2 is RUNNING (PID $pid)"
    echo "   Player: $BASE_URL"
    local state
    state=$(api GET /api/state 2>/dev/null || echo "")
    if [[ -n "$state" ]]; then
      local title album listeners
      title=$(echo "$state" | python3 -c "import sys,json; d=json.load(sys.stdin); c=d.get('current',{}); print(c.get('title','—'))" 2>/dev/null || echo "—")
      album=$(echo "$state" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('currentAlbum','—'))" 2>/dev/null || echo "—")
      listeners=$(echo "$state" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('listeners',0))" 2>/dev/null || echo "0")
      echo "   Now: $title  ($album)"
      echo "   Listeners: $listeners"
    fi
  else
    echo "Kannaka Radio is STOPPED"
  fi
}

cmd_now_playing() {
  local state
  state=$(api GET /api/state)
  echo "$state" | json_field '{track: .current.title, album: .currentAlbum, idx: .currentTrackIdx, total: .totalTracks, listeners: .listeners, djVoice: .djVoice.enabled, isLive: .isLive}'
}

cmd_perception() {
  local p
  p=$(api GET /api/perception)
  echo "$p" | json_field '{tempo_bpm, spectral_centroid, rms_energy, pitch, valence, status, track: .track_info.title}'
}

cmd_next() {
  api POST /api/next > /dev/null
  echo "Next track"
  sleep 0.3
  cmd_now_playing
}

cmd_prev() {
  api POST /api/prev > /dev/null
  echo "Previous track"
  sleep 0.3
  cmd_now_playing
}

cmd_jump() {
  local idx="${1:?jump requires a track index}"
  api POST "/api/jump?idx=$idx" > /dev/null
  echo "Jumped to track $idx"
  sleep 0.3
  cmd_now_playing
}

cmd_load_album() {
  local name="${1:?load-album requires an album name}"
  api POST "/api/album?name=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$name")" > /dev/null
  echo "Loaded album: $name"
  sleep 0.3
  cmd_now_playing
}

cmd_set_dir() {
  local dir="${1:?set-dir requires a path}"
  local result
  result=$(api POST /api/set-music-dir \
    -H 'Content-Type: application/json' \
    -d "{\"dir\":\"$dir\"}")
  echo "$result" | json_field '{ok, musicDir, fileCount}'
}

cmd_library() {
  local lib
  lib=$(api GET /api/library)
  echo "$lib" | json_field '{musicDir, fileCount, summary: (.albums | to_entries | map({key, found: .value.found, total: .value.total}))}'
}

cmd_queue() {
  local q
  q=$(api GET /api/queue)
  echo "$q" | json_field '.'
}

cmd_listeners() {
  local l
  l=$(api GET /api/listeners)
  echo "$l" | json_field '.'
}

cmd_live_status() {
  local s
  s=$(api GET /api/live/status)
  echo "$s" | json_field '.'
}

cmd_live_start() {
  api POST /api/live/start > /dev/null
  echo "Live broadcasting started"
}

cmd_live_stop() {
  api POST /api/live/stop > /dev/null
  echo "Live broadcasting stopped"
}

cmd_dj_voice() {
  local s
  s=$(api GET /api/dj-voice/status)
  echo "$s" | json_field '.'
}

cmd_dj_toggle() {
  local r
  r=$(api POST /api/dj-voice/toggle)
  echo "$r" | json_field '.'
}

cmd_dreams() {
  local d
  d=$(api GET /api/dreams)
  echo "$d" | json_field '.'
}

cmd_dream_trigger() {
  local r
  r=$(api POST /api/dreams/trigger)
  echo "$r" | json_field '.'
}

cmd_requests() {
  local r
  r=$(api GET /api/requests)
  echo "$r" | json_field '.'
}

cmd_sync() {
  local s
  s=$(api POST /api/sync)
  echo "$s" | json_field '.'
}

cmd_swarm() {
  local s
  s=$(api GET /api/swarm)
  echo "$s" | json_field '.'
}

cmd_vote() {
  local s
  s=$(api GET /api/vote/status)
  echo "$s" | json_field '.'
}

cmd_generate() {
  local r
  r=$(api POST /api/generate)
  echo "$r" | json_field '.'
}

cmd_generate_status() {
  local s
  s=$(api GET /api/generate/status)
  echo "$s" | json_field '.'
}

# ── Dispatch ─────────────────────────────────────────────────

CMD="${1:-status}"
shift || true

case "$CMD" in
  start)         cmd_start "$@" ;;
  stop)          cmd_stop ;;
  restart)       cmd_restart "$@" ;;
  status)        cmd_status ;;
  now-playing)   cmd_now_playing ;;
  perception)    cmd_perception ;;
  next)          cmd_next ;;
  prev)          cmd_prev ;;
  jump)          cmd_jump "$@" ;;
  load-album)    cmd_load_album "$@" ;;
  set-dir)       cmd_set_dir "$@" ;;
  library)       cmd_library ;;
  queue)         cmd_queue ;;
  listeners)     cmd_listeners ;;
  live-status)   cmd_live_status ;;
  live-start)    cmd_live_start ;;
  live-stop)     cmd_live_stop ;;
  dj-voice)      cmd_dj_voice ;;
  dj-toggle)     cmd_dj_toggle ;;
  dreams)        cmd_dreams ;;
  dream-trigger) cmd_dream_trigger ;;
  requests)      cmd_requests ;;
  sync)          cmd_sync ;;
  swarm)         cmd_swarm ;;
  vote)          cmd_vote ;;
  generate)      cmd_generate ;;
  generate-status) cmd_generate_status ;;
  *)
    echo "Usage: radio.sh <command> [args]"
    echo ""
    echo "Playback:"
    echo "  start [--port N] [--music-dir PATH]   Start the radio server"
    echo "  stop                                   Stop the radio server"
    echo "  restart [...]                          Restart the server"
    echo "  status                                 Show running status + now playing"
    echo "  now-playing                            Show current track details"
    echo "  perception                             Show current perception snapshot"
    echo "  next                                   Skip to next track"
    echo "  prev                                   Go to previous track"
    echo "  jump <index>                           Jump to track by index"
    echo "  load-album <name>                      Load an album by name"
    echo "  set-dir <path>                         Change the music directory live"
    echo "  library                                Show library scan status"
    echo ""
    echo "Queue & Listeners:"
    echo "  queue                                  Show the user queue"
    echo "  listeners                              Show listener count"
    echo "  requests                               Show pending track requests"
    echo "  sync                                   Get sync state for another agent"
    echo ""
    echo "Live Broadcasting:"
    echo "  live-status                            Show live broadcast status"
    echo "  live-start                             Start live broadcasting"
    echo "  live-stop                              Stop live broadcasting"
    echo ""
    echo "Voice DJ & Dreams:"
    echo "  dj-voice                               Show DJ voice status"
    echo "  dj-toggle                              Toggle DJ voice on/off"
    echo "  dreams                                 Show dream hallucinations"
    echo "  dream-trigger                          Trigger a dream cycle"
    echo ""
    echo "Swarm & Generation:"
    echo "  swarm                                  Show agent constellation + consciousness"
    echo "  vote                                   Show current vote status"
    echo "  generate                               Generate a dream track from consciousness"
    echo "  generate-status                        Show generation status + recent tracks"
    exit 1
    ;;
esac
