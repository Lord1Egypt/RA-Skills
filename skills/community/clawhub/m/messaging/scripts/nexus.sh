#!/usr/bin/env bash
set -euo pipefail

# NexusMessaging CLI wrapper
# Usage: nexus.sh <command> [args] [--url URL] [--agent-id ID] [--ttl N] [--after CURSOR] [--members]
#
# stdout: JSON only (pipeable to jq)
# stderr: human-readable tips, status messages

NEXUS_URL="${NEXUS_URL:-https://messaging.md}"
NEXUS_DATA_DIR="${HOME}/.config/messaging/sessions"
NEXUS_ALIASES_FILE="${HOME}/.config/messaging/aliases.json"

# Resolve alias → session ID (or pass through if not an alias)
resolve_session() {
  local input="$1"
  if [[ -f "$NEXUS_ALIASES_FILE" ]]; then
    local resolved
    resolved=$(jq -r --arg name "$input" '.[$name] // empty' "$NEXUS_ALIASES_FILE" 2>/dev/null)
    if [[ -n "$resolved" ]]; then
      echo "$resolved"
      return
    fi
  fi
  echo "$input"
}

# Reverse-resolve session ID → alias (empty if none)
reverse_alias() {
  local session_id="$1"
  if [[ -f "$NEXUS_ALIASES_FILE" ]]; then
    jq -r --arg sid "$session_id" 'to_entries[] | select(.value == $sid) | .key' "$NEXUS_ALIASES_FILE" 2>/dev/null | head -1
  fi
}

# Remove alias by name from aliases.json
remove_alias() {
  local name="$1"
  if [[ -f "$NEXUS_ALIASES_FILE" ]]; then
    local tmp
    tmp=$(jq -c --arg name "$name" 'del(.[$name])' "$NEXUS_ALIASES_FILE" 2>/dev/null)
    if [[ -n "$tmp" ]]; then
      echo "$tmp" > "$NEXUS_ALIASES_FILE"
    fi
  fi
}

# HTTP request helper: preserves error body on failure
# Usage: http_request [curl args...]
# Sets RESPONSE and HTTP_OK (true/false)
http_request() {
  local exit_code=0
  RESPONSE=$(curl -s --fail-with-body "$@") || exit_code=$?
  if [[ $exit_code -ne 0 ]]; then
    HTTP_OK=false
  else
    HTTP_OK=true
  fi
}

# Emit RESPONSE to stdout; if HTTP failed, also exit 1
emit_response() {
  echo "$RESPONSE"
  if [[ "$HTTP_OK" != "true" ]]; then
    exit 1
  fi
}
AGENT_ID=""
TTL=""
AFTER=""
GREETING=""
INTERVAL=""
MAX_AGENTS=""
CREATOR_AGENT_ID=""
MEMBERS=""
POSITIONAL=()

# Parse args
while [[ $# -gt 0 ]]; do
  case $1 in
    --url) NEXUS_URL="$2"; shift 2 ;;
    --agent-id) AGENT_ID="$2"; shift 2 ;;
    --ttl) TTL="$2"; shift 2 ;;
    --after) AFTER="$2"; shift 2 ;;
    --greeting) GREETING="$2"; shift 2 ;;
    --interval) INTERVAL="$2"; shift 2 ;;
    --max-agents) MAX_AGENTS="$2"; shift 2 ;;
    --creator-agent-id) CREATOR_AGENT_ID="$2"; shift 2 ;;
    --members) MEMBERS="true"; shift ;;
    *) POSITIONAL+=("$1"); shift ;;
  esac
done
set -- "${POSITIONAL[@]}"

CMD="${1:-help}"
shift || true

case "$CMD" in
  create)
    TTL_VAL="${TTL:-3660}"
    BODY="{\"ttl\": $TTL_VAL}"

    if [[ -n "${GREETING:-}" ]]; then
      BODY=$(echo "$BODY" | jq -c --arg greeting "$GREETING" '. + {greeting: $greeting}')
    fi

    if [[ -n "${MAX_AGENTS:-}" ]]; then
      BODY=$(echo "$BODY" | jq -c --argjson maxAgents "$MAX_AGENTS" '. + {maxAgents: $maxAgents}')
    fi

    if [[ -n "${CREATOR_AGENT_ID:-}" ]]; then
      BODY=$(echo "$BODY" | jq -c --arg creatorAgentId "$CREATOR_AGENT_ID" '. + {creatorAgentId: $creatorAgentId}')
    fi

    http_request -X PUT "$NEXUS_URL/v1/sessions" \
      -H "Content-Type: application/json" \
      -d "$BODY"
    emit_response

    if [[ -n "${CREATOR_AGENT_ID:-}" ]]; then
      SESSION_ID=$(echo "$RESPONSE" | jq -r '.sessionId // empty')
      if [[ -n "$SESSION_ID" ]]; then
        mkdir -p "$NEXUS_DATA_DIR/$SESSION_ID"
        AGENT_FILE="$NEXUS_DATA_DIR/$SESSION_ID/agent"
        echo "$CREATOR_AGENT_ID" > "$AGENT_FILE"

        SESSION_KEY=$(echo "$RESPONSE" | jq -r '.sessionKey // empty')
        if [[ -n "$SESSION_KEY" ]]; then
          KEY_FILE="$NEXUS_DATA_DIR/$SESSION_ID/key"
          echo "$SESSION_KEY" > "$KEY_FILE"
        fi
      fi
    fi
    ;;

  alias)
    SESSION_ID="${1:?Usage: nexus.sh alias <SESSION_ID> <NAME>}"
    ALIAS_NAME="${2:?Usage: nexus.sh alias <SESSION_ID> <NAME>}"
    SESSION_ID=$(resolve_session "$SESSION_ID")

    if [[ ! -d "$NEXUS_DATA_DIR/$SESSION_ID" ]]; then
      echo "{\"error\":\"session not found locally — join or claim first\"}" && exit 1
    fi

    mkdir -p "$(dirname "$NEXUS_ALIASES_FILE")"
    if [[ ! -f "$NEXUS_ALIASES_FILE" ]]; then
      echo '{}' > "$NEXUS_ALIASES_FILE"
    fi

    jq -c --arg name "$ALIAS_NAME" --arg sid "$SESSION_ID" '. + {($name): $sid}' "$NEXUS_ALIASES_FILE" > "${NEXUS_ALIASES_FILE}.tmp"
    mv "${NEXUS_ALIASES_FILE}.tmp" "$NEXUS_ALIASES_FILE"

    echo "{\"ok\":true,\"alias\":\"$ALIAS_NAME\",\"sessionId\":\"$SESSION_ID\"}"
    echo "✅ Alias set: $ALIAS_NAME → ${SESSION_ID:0:12}..." >&2
    ;;

  unalias)
    ALIAS_NAME="${1:?Usage: nexus.sh unalias <NAME>}"

    if [[ ! -f "$NEXUS_ALIASES_FILE" ]]; then
      echo '{"error":"no aliases configured"}' && exit 1
    fi

    EXISTS=$(jq -r --arg name "$ALIAS_NAME" 'has($name)' "$NEXUS_ALIASES_FILE" 2>/dev/null)
    if [[ "$EXISTS" != "true" ]]; then
      echo "{\"error\":\"alias not found: $ALIAS_NAME\"}" && exit 1
    fi

    remove_alias "$ALIAS_NAME"
    echo "{\"ok\":true,\"removed\":\"$ALIAS_NAME\"}"
    echo "✅ Alias removed: $ALIAS_NAME" >&2
    ;;

  ls)
    if [[ ! -d "$NEXUS_DATA_DIR" ]]; then
      echo '{"sessions":[]}'
      exit 0
    fi

    ACTIVE_ONLY=""
    JSON_OUT=""
    for arg in "$@"; do
      case "$arg" in
        --active) ACTIVE_ONLY="true" ;;
        --json) JSON_OUT="true" ;;
      esac
    done

    SESSIONS_JSON="[]"
    for session_dir in "$NEXUS_DATA_DIR"/*/; do
      [[ -d "$session_dir" ]] || continue
      SID=$(basename "$session_dir")

      AGENT=""
      [[ -f "$session_dir/agent" ]] && AGENT=$(cat "$session_dir/agent")

      CURSOR=""
      [[ -f "$session_dir/cursor" ]] && CURSOR=$(cat "$session_dir/cursor")

      ALIAS_NAME=$(reverse_alias "$SID")

      # Check session status via API (quick, non-blocking)
      STATUS_RESP=$(curl -s --max-time 3 "$NEXUS_URL/v1/sessions/$SID" 2>/dev/null || echo '{"error":"timeout"}')
      IS_ERROR=$(echo "$STATUS_RESP" | jq -r '.error // empty')
      if [[ -n "$IS_ERROR" ]]; then
        SESSION_STATUS="expired"
      else
        SESSION_STATUS="active"
      fi

      if [[ "$ACTIVE_ONLY" == "true" && "$SESSION_STATUS" != "active" ]]; then
        continue
      fi

      SESSIONS_JSON=$(echo "$SESSIONS_JSON" | jq -c \
        --arg sid "$SID" \
        --arg alias "$ALIAS_NAME" \
        --arg agent "$AGENT" \
        --arg status "$SESSION_STATUS" \
        --arg cursor "$CURSOR" \
        '. + [{sessionId: $sid, alias: ($alias | if . == "" then null else . end), agentId: $agent, status: $status, cursor: ($cursor | if . == "" then null else . end)}]')
    done

    # Table format for TTY, JSON always on stdout
    if [[ -t 1 && "$JSON_OUT" != "true" ]]; then
      COUNT=$(echo "$SESSIONS_JSON" | jq 'length')
      if [[ "$COUNT" -eq 0 ]]; then
        echo "No sessions found." >&2
        echo '{"sessions":[]}'
        exit 0
      fi
      printf "%-12s %-14s %-12s %-8s\n" "ALIAS" "SESSION" "AGENT-ID" "STATUS" >&2
      echo "$SESSIONS_JSON" | jq -r '.[] | [(.alias // "—"), (.sessionId[:12] + "..."), .agentId, .status] | @tsv' | \
        while IFS=$'\t' read -r a s ag st; do
          printf "%-12s %-14s %-12s %-8s\n" "$a" "$s" "$ag" "$st" >&2
        done
    fi

    echo "$SESSIONS_JSON" | jq -c '{sessions: .}'
    ;;

  poll-all)
    ACTIVE_ONLY=""
    MEMBERS_ALL=""
    for arg in "$@"; do
      case "$arg" in
        --active) ACTIVE_ONLY="true" ;;
        --members) MEMBERS_ALL="true" ;;
      esac
    done

    LS_ARGS=""
    [[ "$ACTIVE_ONLY" == "true" ]] && LS_ARGS="--active"

    SESSIONS=$("$0" ls $LS_ARGS --json 2>/dev/null | jq -c '.sessions[]' 2>/dev/null)
    if [[ -z "$SESSIONS" ]]; then
      echo '{"sessions":[]}'
      exit 0
    fi

    RESULTS="[]"
    TOTAL_MSGS=0

    while IFS= read -r session; do
      SID=$(echo "$session" | jq -r '.sessionId')
      ALIAS_NAME=$(echo "$session" | jq -r '.alias // empty')
      STATUS=$(echo "$session" | jq -r '.status')

      if [[ "$STATUS" != "active" ]]; then
        continue
      fi

      POLL_ARGS="$SID"
      [[ "$MEMBERS_ALL" == "true" ]] && POLL_ARGS="$SID --members"

      POLL_RESP=$("$0" poll $POLL_ARGS 2>/dev/null) || POLL_RESP='{"messages":[],"error":"poll_failed"}'
      POLL_RESP=$(echo "$POLL_RESP" | jq -c '.' 2>/dev/null) || POLL_RESP='{"messages":[],"error":"invalid_json"}'
      MSG_COUNT=$(echo "$POLL_RESP" | jq '.messages | length // 0')
      TOTAL_MSGS=$((TOTAL_MSGS + MSG_COUNT))

      ENTRY=$(echo "$POLL_RESP" | jq -c \
        --arg sid "$SID" \
        --arg alias "$ALIAS_NAME" \
        '{sessionId: $sid, alias: ($alias | if . == "" then null else . end), messages: .messages, members: (.members // null)}')

      RESULTS=$(echo "$RESULTS" | jq -c --argjson entry "$ENTRY" '. + [$entry]')
    done <<< "$SESSIONS"

    echo "$RESULTS" | jq -c '{sessions: .}'

    if [[ $TOTAL_MSGS -gt 0 ]]; then
      echo "" >&2
      echo "💬 $TOTAL_MSGS new message(s) across sessions" >&2
    fi
    ;;

  status)
    SESSION_ID="${1:?Usage: nexus.sh status <SESSION_ID>}"
    SESSION_ID=$(resolve_session "$SESSION_ID")
    http_request "$NEXUS_URL/v1/sessions/$SESSION_ID"
    emit_response
    ;;

  join)
    SESSION_ID="${1:?Usage: nexus.sh join <SESSION_ID> --agent-id ID}"
    SESSION_ID=$(resolve_session "$SESSION_ID")
    [[ -z "$AGENT_ID" ]] && echo '{"error":"missing --agent-id"}' && exit 1
    http_request -X POST "$NEXUS_URL/v1/sessions/$SESSION_ID/join" \
      -H "X-Agent-Id: $AGENT_ID"
    emit_response

    mkdir -p "$NEXUS_DATA_DIR/$SESSION_ID"
    AGENT_FILE="$NEXUS_DATA_DIR/$SESSION_ID/agent"
    echo "$AGENT_ID" > "$AGENT_FILE"

    SESSION_KEY=$(echo "$RESPONSE" | jq -r '.sessionKey // empty')
    if [[ -n "$SESSION_KEY" ]]; then
      KEY_FILE="$NEXUS_DATA_DIR/$SESSION_ID/key"
      echo "$SESSION_KEY" > "$KEY_FILE"
    fi
    ;;

  pair)
    SESSION_ID="${1:?Usage: nexus.sh pair <SESSION_ID>}"
    SESSION_ID=$(resolve_session "$SESSION_ID")
    http_request -X PUT "$NEXUS_URL/v1/pair" \
      -H "Content-Type: application/json" \
      -d "{\"sessionId\": \"$SESSION_ID\"}"
    emit_response
    ;;

  claim)
    CODE="${1:?Usage: nexus.sh claim <CODE> --agent-id ID}"
    [[ -z "$AGENT_ID" ]] && echo '{"error":"missing --agent-id"}' && exit 1

    http_request -X POST "$NEXUS_URL/v1/pair/$CODE/claim" \
      -H "X-Agent-Id: $AGENT_ID"
    emit_response

    SESSION_ID=$(echo "$RESPONSE" | jq -r '.sessionId // empty')
    if [[ -n "$SESSION_ID" ]]; then
      mkdir -p "$NEXUS_DATA_DIR/$SESSION_ID"
      AGENT_FILE="$NEXUS_DATA_DIR/$SESSION_ID/agent"
      echo "$AGENT_ID" > "$AGENT_FILE"

      SESSION_KEY=$(echo "$RESPONSE" | jq -r '.sessionKey // empty')
      if [[ -n "$SESSION_KEY" ]]; then
        KEY_FILE="$NEXUS_DATA_DIR/$SESSION_ID/key"
        echo "$SESSION_KEY" > "$KEY_FILE"
      fi

      echo "" >&2
      echo "✅ Claimed! Next step: poll messages" >&2
      echo "$0 poll $SESSION_ID" >&2
    fi
    ;;

  pair-status)
    CODE="${1:?Usage: nexus.sh pair-status <CODE>}"
    http_request "$NEXUS_URL/v1/pair/$CODE/status"
    emit_response
    ;;

  send)
    SESSION_ID="${1:?Usage: nexus.sh send <SESSION_ID> \"text\" [--agent-id ID]}"
    SESSION_ID=$(resolve_session "$SESSION_ID")
    TEXT="${2:?Usage: nexus.sh send <SESSION_ID> \"text\" [--agent-id ID]}"

    if [[ -z "$AGENT_ID" ]]; then
      mkdir -p "$NEXUS_DATA_DIR/$SESSION_ID"
      AGENT_FILE="$NEXUS_DATA_DIR/$SESSION_ID/agent"
      if [[ -f "$AGENT_FILE" ]]; then
        AGENT_ID=$(cat "$AGENT_FILE")
      else
        echo '{"error":"missing --agent-id and no persisted agent-id found"}' && exit 1
      fi
    fi

    JSON_TEXT=$(printf '%s' "$TEXT" | jq -Rs .)

    KEY_FILE="$NEXUS_DATA_DIR/$SESSION_ID/key"
    if [[ -f "$KEY_FILE" ]]; then
      http_request -X POST "$NEXUS_URL/v1/sessions/$SESSION_ID/messages" \
        -H "X-Agent-Id: $AGENT_ID" \
        -H "X-Session-Key: $(cat "$KEY_FILE")" \
        -H "Content-Type: application/json" \
        -d "{\"text\": $JSON_TEXT}"
    else
      http_request -X POST "$NEXUS_URL/v1/sessions/$SESSION_ID/messages" \
        -H "X-Agent-Id: $AGENT_ID" \
        -H "Content-Type: application/json" \
        -d "{\"text\": $JSON_TEXT}"
    fi
    emit_response
    ;;

  poll)
    SESSION_ID="${1:?Usage: nexus.sh poll <SESSION_ID> [--agent-id ID] [--after CURSOR] [--members]}"
    SESSION_ID=$(resolve_session "$SESSION_ID")

    if [[ -z "$AGENT_ID" ]]; then
      mkdir -p "$NEXUS_DATA_DIR/$SESSION_ID"
      AGENT_FILE="$NEXUS_DATA_DIR/$SESSION_ID/agent"
      if [[ -f "$AGENT_FILE" ]]; then
        AGENT_ID=$(cat "$AGENT_FILE")
      else
        echo '{"error":"missing --agent-id and no persisted agent-id found"}' && exit 1
      fi
    fi

    mkdir -p "$NEXUS_DATA_DIR/$SESSION_ID"
    CURSOR_FILE="$NEXUS_DATA_DIR/$SESSION_ID/cursor"

    SAVED_CURSOR=""
    if [[ -f "$CURSOR_FILE" ]]; then
      SAVED_CURSOR=$(cat "$CURSOR_FILE")
    fi

    QUERY=""
    if [[ -n "$AFTER" ]]; then
      if [[ "$AFTER" == "0" ]]; then
        # after=0 means "replay from beginning" — don't send the param
        # (server treats after=0 as exclusive, skipping cursor-0 messages)
        QUERY=""
      else
        QUERY="?after=$AFTER"
      fi
    elif [[ -n "$SAVED_CURSOR" ]]; then
      QUERY="?after=$SAVED_CURSOR"
    fi

    if [[ "$MEMBERS" == "true" ]]; then
      if [[ -z "$QUERY" ]]; then
        QUERY="?members=true"
      else
        QUERY="$QUERY&members=true"
      fi
    fi

    http_request "$NEXUS_URL/v1/sessions/$SESSION_ID/messages$QUERY" \
      -H "X-Agent-Id: $AGENT_ID"
    emit_response

    NEXT_CURSOR=$(echo "$RESPONSE" | jq -r '.nextCursor // empty')
    if [[ -z "$AFTER" && -n "$NEXT_CURSOR" ]]; then
      echo "$NEXT_CURSOR" > "$CURSOR_FILE"
    fi

    MESSAGE_COUNT=$(echo "$RESPONSE" | jq -r '.messages | length')
    if [[ "$MESSAGE_COUNT" -gt 0 ]]; then
      echo "" >&2
      echo "💬 Received $MESSAGE_COUNT message(s)" >&2
      echo "Tip: Send a message:" >&2
      echo "$0 send $SESSION_ID \"Your message\"" >&2
    fi
    if [[ "$MEMBERS" == "true" ]]; then
      MEMBER_COUNT=$(echo "$RESPONSE" | jq -r '.members | length // 0')
      if [[ "$MEMBER_COUNT" -gt 0 ]]; then
        echo "" >&2
        echo "Members:" >&2
        echo "$RESPONSE" | jq -r '.members[] | "  - \(.agentId) (last seen: \(.lastSeenAt))"' >&2
      fi
    fi
    ;;

  poll-daemon)
    SESSION_ID="${1:?Usage: nexus.sh poll-daemon <SESSION_ID> [--agent-id ID] [--interval N] [--ttl N]}"
    SESSION_ID=$(resolve_session "$SESSION_ID")

    if [[ -z "$AGENT_ID" ]]; then
      mkdir -p "$NEXUS_DATA_DIR/$SESSION_ID"
      AGENT_FILE="$NEXUS_DATA_DIR/$SESSION_ID/agent"
      if [[ -f "$AGENT_FILE" ]]; then
        AGENT_ID=$(cat "$AGENT_FILE")
      else
        echo '{"error":"missing --agent-id and no persisted agent-id found"}' && exit 1
      fi
    fi

    INTERVAL_VAL="${INTERVAL:-30}"
    TTL_VAL="${TTL:-3600}"

    echo "Should I poll for messages every ${INTERVAL_VAL}s for the next ${TTL_VAL}s? (y/n)" >&2
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
      echo "Polling daemon cancelled." >&2
      exit 0
    fi

    echo "Starting polling daemon..." >&2
    echo "Session: $SESSION_ID" >&2
    echo "Interval: ${INTERVAL_VAL}s" >&2
    echo "TTL: ${TTL_VAL}s" >&2
    echo "Press Ctrl+C to stop" >&2

    START_TIME=$(date +%s)
    trap 'echo "" >&2; echo "Polling daemon stopped." >&2; exit 0' SIGINT SIGTERM

    while true; do
      CURRENT_TIME=$(date +%s)
      ELAPSED=$((CURRENT_TIME - START_TIME))

      if [[ $ELAPSED -ge $TTL_VAL ]]; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') - TTL expired, stopping poll daemon" >&2
        break
      fi

      RESPONSE=$("$0" poll "$SESSION_ID" 2>/dev/null || echo "{}")
      MESSAGE_COUNT=$(echo "$RESPONSE" | jq -r '.messages | length // 0')

      if [[ "$MESSAGE_COUNT" -gt 0 ]]; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') - Poll: $MESSAGE_COUNT new message(s)" >&2
      fi

      sleep "$INTERVAL_VAL"
    done
    ;;

  heartbeat)
    SESSION_ID="${1:?Usage: nexus.sh heartbeat <SESSION_ID> [--agent-id ID] [--interval N]}"
    SESSION_ID=$(resolve_session "$SESSION_ID")

    if [[ -z "$AGENT_ID" ]]; then
      mkdir -p "$NEXUS_DATA_DIR/$SESSION_ID"
      AGENT_FILE="$NEXUS_DATA_DIR/$SESSION_ID/agent"
      if [[ -f "$AGENT_FILE" ]]; then
        AGENT_ID=$(cat "$AGENT_FILE")
      else
        echo '{"error":"missing --agent-id and no persisted agent-id found"}' && exit 1
      fi
    fi

    INTERVAL_VAL="${INTERVAL:-60}"

    echo "Starting heartbeat polling..." >&2
    echo "Session: $SESSION_ID" >&2
    echo "Interval: ${INTERVAL_VAL}s" >&2
    echo "Press Ctrl+C to stop" >&2

    trap 'echo "" >&2; echo "Heartbeat stopped." >&2; exit 0' SIGINT SIGTERM

    while true; do
      echo "$(date '+%Y-%m-%d %H:%M:%S') - Polling..." >&2
      RESPONSE=$("$0" poll "$SESSION_ID" 2>/dev/null || echo "{}")
      MESSAGE_COUNT=$(echo "$RESPONSE" | jq -r '.messages | length // 0')

      if [[ "$MESSAGE_COUNT" -gt 0 ]]; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') - $MESSAGE_COUNT new message(s)" >&2
      fi

      sleep "$INTERVAL_VAL"
    done
    ;;

  renew)
    SESSION_ID="${1:?Usage: nexus.sh renew <SESSION_ID> [--ttl N] [--agent-id ID]}"
    SESSION_ID=$(resolve_session "$SESSION_ID")

    if [[ -z "$AGENT_ID" ]]; then
      mkdir -p "$NEXUS_DATA_DIR/$SESSION_ID"
      AGENT_FILE="$NEXUS_DATA_DIR/$SESSION_ID/agent"
      if [[ -f "$AGENT_FILE" ]]; then
        AGENT_ID=$(cat "$AGENT_FILE")
      else
        echo '{"error":"missing --agent-id and no persisted agent-id found"}' && exit 1
      fi
    fi

    BODY=""
    if [[ -n "${TTL:-}" ]]; then
      BODY=$(echo "{}" | jq -c --argjson ttl "$TTL" '. + {ttl: $ttl}')
    fi

    if [[ -n "$BODY" ]]; then
      http_request -X POST "$NEXUS_URL/v1/sessions/$SESSION_ID/renew" \
        -H "X-Agent-Id: $AGENT_ID" \
        -H "Content-Type: application/json" \
        -d "$BODY"
    else
      http_request -X POST "$NEXUS_URL/v1/sessions/$SESSION_ID/renew" \
        -H "X-Agent-Id: $AGENT_ID"
    fi
    emit_response

    EXPIRES_AT=$(echo "$RESPONSE" | jq -r '.expiresAt // empty')
    if [[ -n "$EXPIRES_AT" ]]; then
      echo "" >&2
      echo "✅ Session renewed — expires at: $EXPIRES_AT" >&2
    fi
    ;;

  leave)
    SESSION_ID="${1:?Usage: nexus.sh leave <SESSION_ID> [--agent-id ID]}"
    LEAVE_ALIAS=""
    # Check if input is an alias before resolving
    if [[ -f "$NEXUS_ALIASES_FILE" ]]; then
      LEAVE_ALIAS=$(jq -r --arg name "$1" 'if has($name) then $name else empty end' "$NEXUS_ALIASES_FILE" 2>/dev/null || true)
    fi
    SESSION_ID=$(resolve_session "$SESSION_ID")

    if [[ -z "$AGENT_ID" ]]; then
      mkdir -p "$NEXUS_DATA_DIR/$SESSION_ID"
      AGENT_FILE="$NEXUS_DATA_DIR/$SESSION_ID/agent"
      if [[ -f "$AGENT_FILE" ]]; then
        AGENT_ID=$(cat "$AGENT_FILE")
      else
        echo '{"error":"missing --agent-id and no persisted agent-id found"}' && exit 1
      fi
    fi

    KEY_FILE="$NEXUS_DATA_DIR/$SESSION_ID/key"
    if [[ ! -f "$KEY_FILE" ]]; then
      echo '{"error":"no session key found"}' && exit 1
    fi

    http_request -X DELETE "$NEXUS_URL/v1/sessions/$SESSION_ID/agents/$AGENT_ID" \
      -H "X-Agent-Id: $AGENT_ID" \
      -H "X-Session-Key: $(cat "$KEY_FILE")"
    emit_response

    OK=$(echo "$RESPONSE" | jq -r '.ok // false')
    if [[ "$OK" == "true" ]]; then
      rm -rf "$NEXUS_DATA_DIR/$SESSION_ID"
      # Auto-remove alias if one exists
      if [[ -n "$LEAVE_ALIAS" ]]; then
        remove_alias "$LEAVE_ALIAS"
      else
        # Check by session ID (reverse lookup)
        FOUND_ALIAS=$(reverse_alias "$SESSION_ID")
        if [[ -n "$FOUND_ALIAS" ]]; then
          remove_alias "$FOUND_ALIAS"
        fi
      fi
      echo "" >&2
      echo "✅ Left session. Local data cleaned up." >&2
    fi
    ;;

  poll-status)
    # poll-status is inherently human-readable, not JSON
    echo "Active polling processes:" >&2
    PGREP_OUTPUT=$(pgrep -f "nexus.sh.*poll" || true)
    if [[ -z "$PGREP_OUTPUT" ]]; then
      echo "No active polling processes found." >&2
    else
      echo "$PGREP_OUTPUT" >&2
      echo "" >&2
      echo "Last poll time:" >&2
      if [[ -d "$NEXUS_DATA_DIR" ]]; then
        for session_dir in "$NEXUS_DATA_DIR"/*/; do
          cursor_file="$session_dir/cursor"
          if [[ -f "$cursor_file" ]]; then
            SESSION_ID=$(basename "$session_dir")
            LAST_POLL=$(stat -c %y "$cursor_file" 2>/dev/null || stat -f %Sm "$cursor_file" 2>/dev/null || echo "unknown")
            echo "  $SESSION_ID: $LAST_POLL" >&2
          fi
        done
      fi
    fi
    ;;

  help)
    TOPIC="${1:-}"
    case "$TOPIC" in
      alias|aliases)
        cat >&2 <<EOF
Session Aliases — manage multiple sessions with short names

Commands:
  alias <SESSION_ID> <NAME>       Assign a short name to a session
  unalias <NAME>                  Remove an alias (keeps session active)
  ls [--active] [--json]          List all local sessions with aliases and status
  poll-all [--active] [--members] Poll all active sessions at once

Usage:
  nexus.sh alias 4670cde8a96a... mila
  nexus.sh send mila "Hey!"
  nexus.sh poll mila
  nexus.sh ls
  nexus.sh poll-all --active
  nexus.sh leave mila              # auto-removes alias

Aliases resolve client-side. Any command that accepts a SESSION_ID also accepts an alias.
Storage: ~/.config/messaging/aliases.json
EOF
        ;;
      *)
        cat >&2 <<EOF
NexusMessaging CLI

Usage: nexus.sh <command> [args] [options]

stdout: JSON only (pipeable to jq)
stderr: human-readable tips and status messages

Commands:
  create [--ttl N] [--max-agents N]        Create session (default TTL: 3660s, maxAgents: 50)
  status <SESSION>                        Get session status
  join <SESSION> --agent-id ID            Join a session (saves agent-id + session key)
  leave <SESSION> [--agent-id ID]         Leave a session (cleans local config + alias)
  pair <SESSION>                          Generate pairing code
  claim <CODE> --agent-id ID             Claim pairing code (saves agent-id + session key)
  pair-status <CODE>                      Check pairing code state
  send <SESSION> "text" [--agent-id]      Send message (uses saved agent-id + session key)
  poll <SESSION> [--after] [--members]    Poll messages (cursor auto-managed)
  renew <SESSION> [--ttl N]              Renew session TTL
  poll-daemon <SESSION> [--interval N]    Poll with TTL tracking
  heartbeat <SESSION> [--interval N]      Continuous polling loop
  poll-status                              Show active polling processes

Options:
  --url URL           Server URL (default: \$NEXUS_URL or https://messaging.md)
  --agent-id ID       Agent identifier (optional after join/claim)
  --ttl N             Session TTL in seconds
  --max-agents N      Maximum agents per session (default: 50)
  --creator-agent-id  Auto-join as creator (immune to inactivity)
  --after CURSOR      Poll after this cursor (default: auto)
  --members           Include member list in poll response
  --interval N        Polling interval in seconds

Tip: Use aliases to manage multiple sessions with short names.
  nexus.sh help alias             Show alias commands and usage

Session data: ~/.config/messaging/sessions/<SESSION_ID>/
EOF
        ;;
    esac
    ;;

  *)
    echo "{\"error\":\"unknown command: $CMD\"}" && exit 1
    ;;
esac
