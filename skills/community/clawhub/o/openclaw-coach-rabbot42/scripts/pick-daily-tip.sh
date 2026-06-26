#!/bin/bash
# OpenClaw 每日技巧选择脚本
# 晚上 21:05 让用户选择明日想了解的技巧

OBSIDIAN_PATH="$HOME/Obsidian/Docs/OpenClaw"
TIPS_DIR="$OBSIDIAN_PATH/tips"
TIPS_FILE="$OBSIDIAN_PATH/daily-tips.json"

# 获取可用技巧列表
TIPS=()
for f in "$TIPS_DIR"/*.md; do
    if [[ -f "$f" ]]; then
        TIPS+=("$(basename "$f" .md)")
    fi
done

# 随机选3个 (macOS 兼容)
SELECTED=()
for i in 1 2 3; do
    rand=$((RANDOM % ${#TIPS[@]}))
    SELECTED+=("${TIPS[$rand]}")
done

# 发送选择消息
MESSAGE="🌙 晚安！明天想了解哪个 OpenClaw 技巧？\n\n"
MESSAGE+="请回复数字选择：\n"
for i in "${!SELECTED[@]}"; do
    MESSAGE+="$((i+1)). ${SELECTED[$i]}\n"
done

echo "$MESSAGE"

# 记录选项（供明日发送）
TOMORROW=$(date -v+1d +%Y-%m-%d 2>/dev/null || date -d "+1 day" +%Y-%m-%d)
echo "{\"$TOMORROW\": \"${SELECTED[0]}\"}" > "$TIPS_FILE"

# 通过 openclaw 发送消息
openclaw message send --target "ou_6492d43062b301922db4bb3b91f2c22a" --message "$MESSAGE"
