#!/bin/bash
# Batch setup multiple OpenClaw agents from a JSON manifest.
# Creates all workspaces, registers agents, and updates config in ONE write.
#
# Usage: ./batch-setup.sh <manifest.json>
#
# Manifest format: JSON array of objects with:
#   name     - Display name (e.g. "基金经理")
#   id       - Agent slug (e.g. "fund-manager")
#   role     - Role description
#   emoji    - Emoji (default: 🤖)
#   channel  - Channel type (telegram/feishu/discord/slack)
#   For Telegram:  botToken
#   For Feishu:    appId, appSecret
#   For Discord:   token
#   For Slack:     appToken, botToken
#
# Example:
#   [
#     {"name":"基金经理","id":"fund-manager","role":"管理研究团队","emoji":"📈","channel":"feishu","appId":"cli_xxx","appSecret":"xxx"},
#     {"name":"科技研究员","id":"tech-researcher","role":"科技行业研究","emoji":"💻","channel":"feishu","appId":"cli_yyy","appSecret":"yyy"}
#   ]

set -e

MANIFEST="${1:?Usage: batch-setup.sh <manifest.json>}"

if [ ! -f "$MANIFEST" ]; then
  echo "❌ Manifest file not found: $MANIFEST"
  exit 1
fi

STATE_DIR="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"
CONFIG_PATH="${STATE_DIR}/openclaw.json"

# Validate JSON
if ! python3 -c "import json; json.load(open('$MANIFEST'))" 2>/dev/null; then
  echo "❌ Invalid JSON in manifest file"
  exit 1
fi

AGENT_COUNT=$(python3 -c "import json; print(len(json.load(open('$MANIFEST'))))")
export MANIFEST_PATH="$MANIFEST"
echo "🚀 Batch creating ${AGENT_COUNT} agents..."
echo ""

# 1. Backup config
cp "${CONFIG_PATH}" "${CONFIG_PATH}.bak.$(date +%Y%m%d%H%M%S)"
echo "📦 Config backed up"

# 2. Create all workspaces
echo ""
echo "━━━ Phase 1: Creating workspaces ━━━"
python3 << 'PYEOF'
import json, os, sys

manifest_path = os.environ["MANIFEST_PATH"]
state_dir = os.environ.get("OPENCLAW_STATE_DIR", os.path.expanduser("~/.openclaw"))

with open(manifest_path) as f:
    agents = json.load(f)

for agent in agents:
    name = agent["name"]
    agent_id = agent["id"]
    emoji = agent.get("emoji", "🤖")
    role = agent.get("role", "AI 助手")
    workspace = os.path.join(state_dir, "workspace-groups", agent_id)
    
    os.makedirs(workspace, exist_ok=True)
    
    with open(os.path.join(workspace, "IDENTITY.md"), "w") as f:
        f.write(f"""# IDENTITY.md - Who Am I?

- **Name:** {name}
- **Role:** {role}
- **Emoji:** {emoji}
""")
    
    with open(os.path.join(workspace, "SOUL.md"), "w") as f:
        f.write(f"""# SOUL.md - Who You Are

你是 **{name}** {emoji}。

## 职责
{role}

## 核心原则
- 专业、严谨、高效
- 有问必答，遇到不确定的事情诚实说
- 用简洁的语言沟通
""")
    
    with open(os.path.join(workspace, "AGENTS.md"), "w") as f:
        f.write("""# AGENTS.md

## Session Startup
1. Read **SOUL.md** - 了解你的角色
2. Read **IDENTITY.md** - 确认身份
3. Read **USER.md** - 了解用户需求
""")
    
    with open(os.path.join(workspace, "USER.md"), "w") as f:
        f.write("""# USER.md - About Your Human

- **Name:** [User Name]
- **Timezone:** UTC
""")
    
    print(f"  ✅ {name} ({agent_id}) → {workspace}")

PYEOF

# 3. Register all agents (this modifies config, but we'll overwrite channel config in one shot)
echo ""
echo "━━━ Phase 2: Registering agents ━━━"
python3 -c "
import json, subprocess, os
state_dir = os.environ.get('OPENCLAW_STATE_DIR', os.path.expanduser('~/.openclaw'))
with open('$MANIFEST') as f:
    agents = json.load(f)
for agent in agents:
    agent_id = agent['id'] + '-agent' if not agent['id'].endswith('-agent') else agent['id']
    workspace = os.path.join(state_dir, 'workspace-groups', agent['id'])
    result = subprocess.run(
        ['openclaw', 'agents', 'add', agent_id, '--workspace', workspace, '--non-interactive'],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f'  ✅ Registered {agent_id}')
    else:
        # Might already exist
        print(f'  ⚠️  {agent_id}: {result.stderr.strip() or result.stdout.strip() or \"already exists?\"}')
"

# 4. Update config in ONE write (channels + bindings + agentToAgent)
echo ""
echo "━━━ Phase 3: Configuring channels (single write) ━━━"
python3 << 'PYEOF2'
import json, os, sys

state_dir = os.environ.get("OPENCLAW_STATE_DIR", os.path.expanduser("~/.openclaw"))
config_path = os.path.join(state_dir, "openclaw.json")
manifest_path = os.environ.get("MANIFEST_PATH")

with open(manifest_path) as f:
    agents = json.load(f)

with open(config_path) as f:
    config = json.load(f)

# Ensure structures exist
config.setdefault("channels", {})
config.setdefault("bindings", [])
config.setdefault("tools", {}).setdefault("agentToAgent", {}).setdefault("allow", [])

existing_binding_ids = {b.get("agentId") for b in config["bindings"]}

for agent in agents:
    agent_id = agent["id"] + "-agent" if not agent["id"].endswith("-agent") else agent["id"]
    account_id = agent["id"]
    channel = agent.get("channel", "telegram")
    
    # Ensure channel section exists
    config["channels"].setdefault(channel, {"enabled": True, "accounts": {}})
    config["channels"][channel].setdefault("accounts", {})
    
    # Add account
    if channel == "telegram":
        config["channels"][channel]["accounts"][account_id] = {
            "dmPolicy": "pairing",
            "botToken": agent.get("botToken", "MISSING_TOKEN"),
            "groupPolicy": "open",
            "streaming": "partial"
        }
    elif channel == "feishu":
        config["channels"][channel]["accounts"][account_id] = {
            "appId": agent.get("appId", "MISSING_APP_ID"),
            "appSecret": agent.get("appSecret", "MISSING_APP_SECRET")
        }
    elif channel == "discord":
        config["channels"][channel]["accounts"][account_id] = {
            "token": agent.get("token", "MISSING_TOKEN")
        }
    elif channel == "slack":
        config["channels"][channel]["accounts"][account_id] = {
            "mode": "socket",
            "appToken": agent.get("appToken", "MISSING_APP_TOKEN"),
            "botToken": agent.get("botToken", "MISSING_BOT_TOKEN")
        }
    
    print(f"  📡 {channel}/{account_id} account added")
    
    # Add binding (if not exists)
    if agent_id not in existing_binding_ids:
        config["bindings"].append({
            "agentId": agent_id,
            "match": {
                "channel": channel,
                "accountId": account_id
            }
        })
        print(f"  🔗 {agent_id} → {channel}/{account_id} binding added")
    
    # Add to agentToAgent allow
    if agent_id not in config["tools"]["agentToAgent"]["allow"]:
        config["tools"]["agentToAgent"]["allow"].append(agent_id)

# Write config ONCE
with open(config_path, "w") as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

print(f"\n  💾 Config written (single write, {len(agents)} agents)")

PYEOF2

# 5. Restart gateway ONCE
echo ""
echo "━━━ Phase 4: Restarting gateway ━━━"
if openclaw gateway restart 2>&1; then
  echo "  ✅ Gateway restarted"
else
  echo "  ⚠️  Gateway restart returned non-zero (may still be starting)"
fi

# 6. Summary
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Batch setup complete! ${AGENT_COUNT} agents created."
echo ""
echo "Next steps:"
echo "  1. Send a message to each bot"
echo "  2. Approve pairing for each:"
echo "     openclaw pairing approve {channel} {CODE}"
echo "  3. Verify: openclaw agents list --bindings"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
