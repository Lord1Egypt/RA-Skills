#!/usr/bin/env bash
# MemVault CLI — Memory operations for AI agents
set -e

MEMVAULT_URL="${MEMVAULT_URL:-http://localhost:8002}"

_json_escape() {
    python3 -c "import sys,json; print(json.dumps(sys.stdin.read().strip()))"
}

case "$1" in
  memorize)
    USER_ID="${2:-default}"; CONV_FILE="$3"
    [[ -z "$CONV_FILE" ]] && echo "Usage: memvault memorize <user_id> <conv.json>" && exit 1
    curl -s -X POST "$MEMVAULT_URL/memorize" -H "Content-Type: application/json" \
      -d "{\"conversation\": $(cat "$CONV_FILE"), \"user_id\": \"$USER_ID\"}"
    ;;
  memorize-text)
    USER_ID="${2:-default}"; USER_MSG="$3"; ASST_MSG="$4"
    [[ -z "$USER_MSG" ]] && echo "Usage: memvault memorize-text <user_id> <message> [reply]" && exit 1
    UMSG_JSON=$(echo "$USER_MSG" | _json_escape)
    if [[ -z "$ASST_MSG" ]]; then
      PAYLOAD="{\"conversation\":[{\"role\":\"user\",\"content\":$UMSG_JSON}],\"user_id\":\"$USER_ID\"}"
    else
      AMSG_JSON=$(echo "$ASST_MSG" | _json_escape)
      PAYLOAD="{\"conversation\":[{\"role\":\"user\",\"content\":$UMSG_JSON},{\"role\":\"assistant\",\"content\":$AMSG_JSON}],\"user_id\":\"$USER_ID\"}"
    fi
    curl -s -X POST "$MEMVAULT_URL/memorize" -H "Content-Type: application/json" -d "$PAYLOAD"
    ;;
  retrieve)
    USER_ID="${2:-default}"; QUERY="$3"
    [[ -z "$QUERY" ]] && echo "Usage: memvault retrieve <user_id> <query>" && exit 1
    QJSON=$(echo "$QUERY" | _json_escape)
    curl -s -X POST "$MEMVAULT_URL/retrieve" -H "Content-Type: application/json" \
      -d "{\"query\":$QJSON,\"user_id\":\"$USER_ID\"}"
    ;;
  decay)
    USER_ID="${2:-default}"
    curl -s -X POST "$MEMVAULT_URL/decay?user_id=$USER_ID"
    ;;
  stats)
    USER_ID="${2:-default}"
    curl -s "$MEMVAULT_URL/stats?user_id=$USER_ID"
    ;;
  categories)
    USER_ID="${2:-default}"
    curl -s "$MEMVAULT_URL/categories?user_id=$USER_ID"
    ;;
  health)
    curl -s "$MEMVAULT_URL/health"
    ;;
  *)
    cat << 'HELP'
🔐 MemVault — Long-term Memory for AI Agents

Commands:
  memorize-text <user_id> <msg> [reply]  Store a single exchange
  memorize <user_id> <conv.json>         Store conversation from JSON
  retrieve <user_id> <query>             Retrieve relevant memories
  decay [user_id]                        Run Ebbinghaus memory decay
  stats [user_id]                        Show memory statistics
  categories <user_id>                   List memory categories
  health                                 Check service health

Environment:
  MEMVAULT_URL  Server URL (default: http://localhost:8002)

Examples:
  memvault memorize-text alice "I love Python and dark mode" "Noted!"
  memvault retrieve alice "what does the user prefer?"
  memvault stats alice
  memvault decay alice
HELP
    ;;
esac
