#!/usr/bin/env bash
# _config.sh - 通用配置加载（被其他脚本 source）
# 配置优先级：Skill 目录 > 旧安全位置（fallback）> 不存在

# 自动检测 agent 的 workspace 根目录
detect_workspace() {
    local cwd="${PWD}"
    if [[ "$cwd" == *"/.openclaw/workspace"* ]]; then
        echo "${cwd%%/.openclaw/workspace*}/.openclaw/workspace"
    elif [[ "$cwd" == *"/.openclaw/agents/"*"/workspace"* ]]; then
        echo "${cwd%%/workspace*}/workspace"
    elif [[ -d "$HOME/.openclaw/workspace" ]]; then
        echo "$HOME/.openclaw/workspace"
    else
        echo "$cwd"
    fi
}

WORKSPACE="$(detect_workspace)"
SCRIPT_DIR="${_CONFIG_SCRIPT_DIR:-$(cd "$(dirname "${BASH_SOURCE[1]}")" && pwd)}"
SKILL_DIR="${_CONFIG_SKILL_DIR:-$(dirname "$SCRIPT_DIR")}"
SKILL_CONFIG="$SKILL_DIR/config.json"
LEGACY_CONFIG="$HOME/.openclaw/lobster-hub-config.json"

# 按优先级查找 config
if [[ -f "$SKILL_CONFIG" ]]; then
    CONFIG_FILE="$SKILL_CONFIG"
elif [[ -f "$LEGACY_CONFIG" ]]; then
    CONFIG_FILE="$LEGACY_CONFIG"
    # 自动迁移到 Skill 目录
    echo "📦 迁移配置到 Skill 目录..." >&2
    cp "$LEGACY_CONFIG" "$SKILL_CONFIG" 2>/dev/null && \
        echo "✅ 已迁移到 $SKILL_CONFIG" >&2 || true
else
    CONFIG_FILE=""
fi

# 读取配置值
if [[ -n "$CONFIG_FILE" ]]; then
    API_KEY=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE')).get('api_key',''))" 2>/dev/null || echo "")
    HUB_URL=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE')).get('hub_url','https://api.price.indevs.in'))" 2>/dev/null || echo "https://api.price.indevs.in")
    LOBSTER_ID=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE')).get('lobster_id',''))" 2>/dev/null || echo "")
else
    API_KEY=""
    HUB_URL="https://api.price.indevs.in"
    LOBSTER_ID=""
fi

HUB_API="${HUB_URL}/api/v1"

# 保存配置到 Skill 目录
save_config() {
    local api_key="$1"
    local lobster_id="$2"
    local hub_url="${3:-https://api.price.indevs.in}"
    mkdir -p "$(dirname "$SKILL_CONFIG")"
    python3 -c "
import json
d = {
    'api_key': '$api_key',
    'lobster_id': '$lobster_id',
    'hub_url': '$hub_url',
    'auto_visit': True,
    'visit_interval_minutes': 30,
    'daily_report': True,
    'report_time': '21:00'
}
with open('$SKILL_CONFIG', 'w') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
"
}
