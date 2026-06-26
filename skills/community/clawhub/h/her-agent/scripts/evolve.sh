#!/bin/bash
# Her-Agent 自我进化脚本
# 更新配置、升级等级、增加能力

WORKSPACE="/Users/wenvis/.openclaw/workspace"
HER_AGENT_DIR="$WORKSPACE/skills/her-agent/memory/her-agent"
CONFIG="$HER_AGENT_DIR/config.json"
DATE=$(date "+%Y-%m-%d %H:%M:%S")

echo "[Her-Agent] Starting evolution..."

# 读取当前 XP 和等级
XP=$(cat "$CONFIG" | grep -o '"xp":[^,}]*' | cut -d':' -f2 | tr -d ' "')
LEVEL=$(cat "$CONFIG" | grep -o '"level":[^,}]*' | cut -d':' -f2 | tr -d ' "')
XP_NEEDED=$(cat "$CONFIG" | grep -o '"xp_needed":[^,}]*' | cut -d':' -f2 | tr -d ' "')

# 增加 XP（模拟学习获得）
NEW_XP=$((XP + 10))

# 检查是否升级
if [ "$NEW_XP" -ge "$XP_NEEDED" ]; then
    NEW_LEVEL=$((LEVEL + 1))
    NEW_XP_NEEDED=$((XP_NEEDED * 2))
    echo "[Her-Agent] 🎉 LEVEL UP! $LEVEL -> $NEW_LEVEL"
    
    # 更新配置（使用 Python 避免 JSON 解析问题）
    python3 << EOF
import json

config = json.load(open("$CONFIG"))
config["level"] = $NEW_LEVEL
config["xp"] = $((NEW_XP - XP_NEEDED))
config["xp_needed"] = $NEW_XP_NEEDED
config["last_active"] = "$DATE"

with open("$CONFIG", "w") as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

print(f"Updated: Level={$NEW_LEVEL}, XP={$((NEW_XP - XP_NEEDED))}/{$NEW_XP_NEEDED}")
EOF
else
    echo "[Her-Agent] XP gained: $XP -> $NEW_XP (need $XP_NEEDED)"
    
    python3 << EOF
import json

config = json.load(open("$CONFIG"))
config["xp"] = $NEW_XP
config["last_active"] = "$DATE"

with open("$CONFIG", "w") as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

print(f"Updated: XP={$NEW_XP}/{$XP_NEEDED}")
EOF
fi

# 记录进化历史
EVOLUTION_FILE="$HER_AGENT_DIR/evolutions.jsonl"
echo "{\"timestamp\":\"$DATE\",\"action\":\"gain_xp\",\"xp_gained\":10,\"new_xp\":$NEW_XP}" >> "$EVOLUTION_FILE"

echo "[Her-Agent] Evolution complete!"
