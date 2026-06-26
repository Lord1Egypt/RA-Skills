#!/bin/bash
# Generate openclaw.json configuration blocks for multi-bot Feishu setup
#
# Usage:
#   ./setup-feishu-bots.sh <agentId:appId:appSecret> [agentId:appId:appSecret] ...
#
# Example:
#   ./setup-feishu-bots.sh orchestrator:cli_abc123:secret1 writer:cli_def456:secret2 coder:cli_ghi789:secret3
#
# Output: Prints three JSON blocks (channels, bindings, agents) ready to merge into openclaw.json

set -e

if [ $# -lt 1 ]; then
  echo "Usage: ./setup-feishu-bots.sh <agentId:appId:appSecret> [agentId:appId:appSecret] ..."
  echo ""
  echo "Each argument is a colon-separated triple:"
  echo "  agentId   — The agent ID to use in openclaw.json"
  echo "  appId     — The Feishu app's AppID (cli_xxx)"
  echo "  appSecret — The Feishu app's AppSecret"
  echo ""
  echo "Example:"
  echo "  ./setup-feishu-bots.sh orchestrator:cli_abc:sec1 writer:cli_def:sec2"
  exit 1
fi

# Parse arguments
declare -a AGENTS=()
declare -a APP_IDS=()
declare -a APP_SECRETS=()

for arg in "$@"; do
  IFS=':' read -r agent_id app_id app_secret <<< "$arg"
  if [ -z "$agent_id" ] || [ -z "$app_id" ] || [ -z "$app_secret" ]; then
    echo "Error: Invalid format '$arg'. Expected agentId:appId:appSecret"
    exit 1
  fi
  AGENTS+=("$agent_id")
  APP_IDS+=("$app_id")
  APP_SECRETS+=("$app_secret")
done

FIRST_AGENT="${AGENTS[0]}"
FIRST_APP_ID="${APP_IDS[0]}"
FIRST_SECRET="${APP_SECRETS[0]}"

echo "================================================"
echo "  OpenClaw Feishu Multi-Bot Configuration"
echo "  Generating config for ${#AGENTS[@]} agents"
echo "================================================"
echo ""

# --- Block 1: channels.feishu ---
echo "=== Block 1: channels.feishu ==="
echo "(Merge into your existing channels config)"
echo ""
echo '{'
echo '  "channels": {'
echo '    "feishu": {'
echo '      "enabled": true,'
echo "      \"appId\": \"$FIRST_APP_ID\","
echo "      \"appSecret\": \"$FIRST_SECRET\","
echo '      "connectionMode": "websocket",'
echo '      "accounts": {'

for i in "${!AGENTS[@]}"; do
  account_id="${AGENTS[$i]}-bot"
  comma=""
  if [ $i -lt $((${#AGENTS[@]} - 1)) ]; then
    comma=","
  fi
  echo "        \"$account_id\": {"
  echo "          \"appId\": \"${APP_IDS[$i]}\","
  echo "          \"appSecret\": \"${APP_SECRETS[$i]}\","
  echo "          \"agent\": \"${AGENTS[$i]}\""
  echo "        }$comma"
done

echo '      }'
echo '    }'
echo '  }'
echo '}'
echo ""

# --- Block 2: bindings ---
echo "=== Block 2: bindings ==="
echo "(Add these entries to your bindings array)"
echo ""
echo '{'
echo '  "bindings": ['

for i in "${!AGENTS[@]}"; do
  account_id="${AGENTS[$i]}-bot"
  comma=""
  if [ $i -lt $((${#AGENTS[@]} - 1)) ]; then
    comma=","
  fi
  echo '    {'
  echo '      "type": "route",'
  echo "      \"agentId\": \"${AGENTS[$i]}\","
  echo '      "match": {'
  echo '        "channel": "feishu",'
  echo "        \"accountId\": \"$account_id\""
  echo '      }'
  echo "    }$comma"
done

echo '  ]'
echo '}'
echo ""

# --- Block 3: agents.list ---
echo "=== Block 3: agents.list ==="
echo "(Add these to your agents.list array)"
echo ""
echo '{'
echo '  "agents": {'
echo '    "list": ['

for i in "${!AGENTS[@]}"; do
  agent="${AGENTS[$i]}"
  default_line=""
  subagents_line=""
  
  if [ $i -eq 0 ]; then
    default_line="        \"default\": true,"
    # First agent is orchestrator — build allowAgents
    allow_list=""
    for j in "${!AGENTS[@]}"; do
      if [ $j -gt 0 ]; then
        if [ -n "$allow_list" ]; then
          allow_list="$allow_list, "
        fi
        allow_list="$allow_list\"${AGENTS[$j]}\""
      fi
    done
    if [ -n "$allow_list" ]; then
      subagents_line="        \"subagents\": { \"allowAgents\": [$allow_list] },"
    fi
  fi
  
  comma=""
  if [ $i -lt $((${#AGENTS[@]} - 1)) ]; then
    comma=","
  fi
  
  echo '      {'
  echo "        \"id\": \"$agent\","
  [ -n "$default_line" ] && echo "$default_line"
  [ -n "$subagents_line" ] && echo "$subagents_line"
  echo "        \"workspace\": \"~/.openclaw/workspace-$agent\""
  echo "      }$comma"
done

echo '    ]'
echo '  }'
echo '}'
echo ""

# --- Workspace creation commands ---
echo "=== Workspace Setup Commands ==="
echo "(Run these to create agent workspaces)"
echo ""

for agent in "${AGENTS[@]}"; do
  echo "mkdir -p ~/.openclaw/workspace-$agent"
done

echo ""
echo "=== Next Steps ==="
echo "1. Merge the three JSON blocks into ~/.openclaw/openclaw.json"
echo "2. Create AGENTS.md for each workspace"
echo "3. Run: openclaw doctor"
echo "4. Run: openclaw gateway restart"
echo "5. Test each bot in Feishu"
echo ""
echo "✓ Configuration generated for ${#AGENTS[@]} agents!"
