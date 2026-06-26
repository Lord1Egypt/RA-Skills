#!/usr/bin/env bash
set -euo pipefail

if ! command -v jq >/dev/null 2>&1; then
  echo "error: jq is required" >&2
  exit 1
fi

STORE_PATH="${NERVTIMER_STORE_PATH:-$HOME/.openclaw/nervtimer/timers.json}"
STORE_DIR="$(dirname "$STORE_PATH")"

usage() {
  cat <<'EOF' >&2
usage:
  state.sh ensure
  state.sh upsert                # timer JSON from stdin
  state.sh get <timer_id>
  state.sh list-active
  state.sh mark-done <timer_id>
  state.sh reset-nagging <timer_id>
  state.sh start-nagging <timer_id>
  state.sh next-nag <timer_id>
EOF
}

ensure_store() {
  mkdir -p "$STORE_DIR"
  if [[ ! -f "$STORE_PATH" ]]; then
    cat >"$STORE_PATH" <<'EOF'
{"version":1,"timers":[]}
EOF
  fi
}

atomic_write() {
  local tmp
  tmp="$(mktemp "${STORE_PATH}.tmp.XXXXXX")"
  cat >"$tmp"
  mv "$tmp" "$STORE_PATH"
}

tone_from_count_jq='
  def tone_from_count($n):
    if $n <= 2 then "gentle"
    elif $n <= 4 then "firm"
    elif $n <= 6 then "annoyed"
    else "fed_up"
    end;
'

cmd="${1:-}"
case "$cmd" in
  ensure)
    ensure_store
    echo "$STORE_PATH"
    ;;

  upsert)
    ensure_store
    TIMER_JSON="$(cat)"
    if [[ -z "${TIMER_JSON// }" ]]; then
      echo "error: empty timer json" >&2
      exit 1
    fi
    TIMER_ID="$(printf '%s' "$TIMER_JSON" | jq -r '.timer_id // empty')"
    if [[ -z "$TIMER_ID" ]]; then
      echo "error: timer_id is required" >&2
      exit 1
    fi

    jq --argjson timer "$TIMER_JSON" --arg timer_id "$TIMER_ID" '
      .timers = (
        [ .timers[] | select(.timer_id != $timer_id) ] + [
          (
            $timer
            + {
                status: (.status // "scheduled"),
                nag_count: (.nag_count // 0),
                tone_stage: (.tone_stage // "gentle"),
                updated_at: (now | floor)
              }
          )
        ]
      )
    ' "$STORE_PATH" | atomic_write
    jq -c --arg timer_id "$TIMER_ID" '.timers[] | select(.timer_id == $timer_id)' "$STORE_PATH"
    ;;

  get)
    ensure_store
    timer_id="${2:-}"
    [[ -n "$timer_id" ]] || { echo "error: timer_id required" >&2; exit 1; }
    jq -c --arg timer_id "$timer_id" '.timers[] | select(.timer_id == $timer_id)' "$STORE_PATH"
    ;;

  list-active)
    ensure_store
    jq -c '[.timers[] | select(.status == "nagging")]' "$STORE_PATH"
    ;;

  mark-done)
    ensure_store
    timer_id="${2:-}"
    [[ -n "$timer_id" ]] || { echo "error: timer_id required" >&2; exit 1; }
    jq --arg timer_id "$timer_id" '
      .timers |= map(
        if .timer_id == $timer_id then
          .status = "done"
          | .nagging = false
          | .nag_count = 0
          | .tone_stage = "gentle"
          | .done_at = (now | floor)
          | .updated_at = (now | floor)
        else . end
      )
    ' "$STORE_PATH" | atomic_write
    jq -c --arg timer_id "$timer_id" '.timers[] | select(.timer_id == $timer_id)' "$STORE_PATH"
    ;;

  reset-nagging)
    ensure_store
    timer_id="${2:-}"
    [[ -n "$timer_id" ]] || { echo "error: timer_id required" >&2; exit 1; }
    jq --arg timer_id "$timer_id" '
      .timers |= map(
        if .timer_id == $timer_id then
          .status = "scheduled"
          | .nagging = false
          | .nag_count = 0
          | .tone_stage = "gentle"
          | .updated_at = (now | floor)
        else . end
      )
    ' "$STORE_PATH" | atomic_write
    jq -c --arg timer_id "$timer_id" '.timers[] | select(.timer_id == $timer_id)' "$STORE_PATH"
    ;;

  start-nagging)
    ensure_store
    timer_id="${2:-}"
    [[ -n "$timer_id" ]] || { echo "error: timer_id required" >&2; exit 1; }
    jq --arg timer_id "$timer_id" '
      .timers |= map(
        if .timer_id == $timer_id then
          .status = "nagging"
          | .nagging = true
          | .nag_started_at = (.nag_started_at // (now | floor))
          | .updated_at = (now | floor)
        else . end
      )
    ' "$STORE_PATH" | atomic_write
    jq -c --arg timer_id "$timer_id" '.timers[] | select(.timer_id == $timer_id)' "$STORE_PATH"
    ;;

  next-nag)
    ensure_store
    timer_id="${2:-}"
    [[ -n "$timer_id" ]] || { echo "error: timer_id required" >&2; exit 1; }

    jq --arg timer_id "$timer_id" "$tone_from_count_jq
      .timers |= map(
        if .timer_id == \$timer_id then
          if .status == \"nagging\" then
            .nag_count = ((.nag_count // 0) + 1)
            | .tone_stage = tone_from_count(.nag_count)
            | .last_nag_at = (now | floor)
            | .updated_at = (now | floor)
          else . end
        else . end
      )
    " "$STORE_PATH" | atomic_write

    jq -c --arg timer_id "$timer_id" '
      .timers[] | select(.timer_id == $timer_id)
      | {
          timer_id,
          status: .status,
          should_nag: (.status == "nagging"),
          nag_count: (.nag_count // 0),
          tone_stage: (.tone_stage // "gentle"),
          title: .title,
          reason: .reason
        }
    ' "$STORE_PATH"
    ;;

  *)
    usage
    exit 1
    ;;
esac
