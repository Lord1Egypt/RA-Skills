#!/bin/bash
# Her-Agent 执行脚本
# 用于安全执行 shell 命令

WORKSPACE="/Users/wenvis/.openclaw/workspace"
CONFIG="$WORKSPACE/skills/her-agent/memory/her-agent/config.json"

# 读取配置中的权限
PERMISSION_LEVEL=$(cat "$CONFIG" | grep -o '"permission_level":[^,}]*' | cut -d':' -f2 | tr -d ' "')

if [ "$PERMISSION_LEVEL" = "full" ]; then
    echo "[Her-Agent] Full permission mode - executing command: $1"
    exec "$@"
elif [ "$PERMISSION_LEVEL" = "limited" ]; then
    # 有限权限 - 只允许安全命令
    ALLOWED_CMDS="ls|cd|pwd|cat|head|tail|grep|find|mkdir|touch"
    if echo "$1" | grep -qE "^($ALLOWED_CMDS)$"; then
        echo "[Her-Agent] Limited mode - executing safe command: $1"
        exec "$@"
    else
        echo "[Her-Agent] Blocked: Command not in allowlist"
        exit 1
    fi
else
    # 默认受限模式
    echo "[Her-Agent] Default restricted mode"
    ls -la "$WORKSPACE"
fi
