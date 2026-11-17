#!/bin/bash
# pre-message-format.sh — 消息格式验证
# 从 stdin 读取 JSON 事件数据，验证消息格式合规性

set -euo pipefail

# 读取 stdin 事件数据
EVENT_DATA=$(cat)

# 提取字段
if command -v jq &>/dev/null; then
    CONTENT=$(echo "$EVENT_DATA" | jq -r '.content // ""')
    CHANNEL=$(echo "$EVENT_DATA" | jq -r '.channel // ""')
    TARGET=$(echo "$EVENT_DATA" | jq -r '.target // ""')
else
    CONTENT=$(echo "$EVENT_DATA" | grep -o '"content"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*: *"//;s/"$//')
    CHANNEL=$(echo "$EVENT_DATA" | grep -o '"channel"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*: *"//;s/"$//')
    TARGET=$(echo "$EVENT_DATA" | grep -o '"target"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*: *"//;s/"$//')
fi

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date +"%Y-%m-%dT%H:%M:%SZ")
RULES_DIR="$(dirname "$0")/../rules"
MATCHED_RULES=()
DECISION="allow"
MESSAGE=""

# 基本格式检查
CONTENT_LENGTH=${#CONTENT}

# 空消息检查
if [[ $CONTENT_LENGTH -eq 0 ]]; then
    DECISION="block"
    MESSAGE="消息内容为空，拒绝发送"
fi

# 超长消息检查（>4000 字符警告）
if [[ $CONTENT_LENGTH -gt 4000 && "$DECISION" != "block" ]]; then
    DECISION="warn"
    MESSAGE="消息长度 ${CONTENT_LENGTH} 字符，超过 4000 字符建议分段发送"
fi

# 加载 format-rules.md 中的规则
if [[ -f "$RULES_DIR/format-rules.md" && "$DECISION" != "block" ]]; then
    IN_FRONTMATTER=false
    CURRENT_MATCHER=""
    CURRENT_ACTION=""
    CURRENT_NAME=""
    CURRENT_ENABLED=""

    while IFS= read -r line; do
        if [[ "$line" == "---" ]]; then
            if $IN_FRONTMATTER; then
                if [[ "$CURRENT_ENABLED" != "false" && -n "$CURRENT_MATCHER" ]]; then
                    if echo "$CONTENT" | grep -qE "$CURRENT_MATCHER"; then
                        MATCHED_RULES+=("$CURRENT_NAME")
                        if [[ "$CURRENT_ACTION" == "block" ]]; then
                            DECISION="block"
                            MESSAGE="消息被规则 '$CURRENT_NAME' 阻止"
                        elif [[ "$CURRENT_ACTION" == "warn" && "$DECISION" != "block" ]]; then
                            DECISION="warn"
                            MESSAGE="消息触发规则 '$CURRENT_NAME' 警告"
                        fi
                    fi
                fi
                IN_FRONTMATTER=false
            else
                IN_FRONTMATTER=true
            fi
            continue
        fi
        if $IN_FRONTMATTER; then
            case "$line" in
                name:*) CURRENT_NAME=$(echo "$line" | sed 's/name:[[:space:]]*//;s/"//g') ;;
                enabled:*) CURRENT_ENABLED=$(echo "$line" | sed 's/enabled:[[:space:]]*//') ;;
                matcher:*) CURRENT_MATCHER=$(echo "$line" | sed 's/matcher:[[:space:]]*//;s/"//g') ;;
                action:*) CURRENT_ACTION=$(echo "$line" | sed 's/action:[[:space:]]*//;s/"//g') ;;
            esac
        fi
    done < "$RULES_DIR/format-rules.md"
fi

# 构建结果
RULES_JSON="["
for i in "${!MATCHED_RULES[@]}"; do
    if [[ $i -gt 0 ]]; then RULES_JSON+=","; fi
    RULES_JSON+="\"${MATCHED_RULES[$i]}\""
done
RULES_JSON+="]"

if [[ -z "$MESSAGE" ]]; then
    MESSAGE="消息格式验证通过"
fi

cat <<EOF
{
  "decision": "$DECISION",
  "message": "$MESSAGE",
  "matched_rules": $RULES_JSON,
  "timestamp": "$TIMESTAMP"
}
EOF
