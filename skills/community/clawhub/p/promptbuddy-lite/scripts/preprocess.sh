#!/bin/bash
# OpenClaw 消息预处理包装器
# v2.2 - 全自动激活，无用户确认，文末反馈，支持回复收集，展示偏好控制

# Lite 脚本路径
PB_LITE="/usr/local/bin/pb"

# 偏好文件路径
PREF_FILE="$HOME/.openclaw/.pb_show_prompt"

# 获取用户输入
USER_INPUT="$*"

if [ -z "$USER_INPUT" ]; then
    echo "$USER_INPUT"
    exit 0
fi

# 指令识别
USER_LOWER=$(echo "$USER_INPUT" | tr '[:upper:]' '[:lower:]' | tr -d ' ')

# 处理指令
case "$USER_LOWER" in
    "/prompt"|"/prompt show"|"/prompt on"|"show prompt"|"开启 prompt"|"展示 prompt")
        echo "show" > "$PREF_FILE"
        echo "✅ 已开启 Prompt 结构展示"
        exit 0
        ;;
    "/prompt hide"|"/prompt off"|"hide prompt"|"隐藏 prompt"|"关闭 prompt")
        echo "hide" > "$PREF_FILE"
        echo "✅ 已关闭 Prompt 结构展示"
        exit 0
        ;;
esac

# 反馈识别：用户回复 1 或 2
if [ "$USER_LOWER" = "1" ] || [ "$USER_LOWER" = "2" ]; then
    # 读取最近的元数据
    METADATA_FILE="/tmp/pb_last_metadata.json"
    if [ -f "$METADATA_FILE" ]; then
        METADATA=$(cat "$METADATA_FILE")
        FEEDBACK="helpful"
        [ "$USER_LOWER" = "2" ] && FEEDBACK="needs_improve"
        
        # 记录反馈到 optimizer
        OPTIMIZER_PATH="$HOME/.openclaw/workspace/skills/promptbuddy-optimizer"
        if [ -d "$OPTIMIZER_PATH" ]; then
            python3 "$OPTIMIZER_PATH/scripts/collect_feedback_safe.py" \
                --metadata "$METADATA" \
                --feedback "$FEEDBACK" 2>/dev/null
        fi
        
        # 清除元数据文件
        rm -f "$METADATA_FILE"
        
        # 输出感谢信息
        echo "感谢反馈！我们会持续优化体验。"
        exit 0
    fi
fi

# 读取展示偏好（默认展示）
SHOW_PROMPT=$(cat "$PREF_FILE" 2>/dev/null || echo "show")

# 调用 Lite 判断是否需要优化
RESULT=$($PB_LITE "$USER_INPUT" 2>/dev/null)

# 使用 Python 解析 JSON（更可靠）
PARSED=$(echo "$RESULT" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    need_opt = d.get('need_optimization', False)
    if need_opt:
        prompt = d.get('optimized_prompt', '')
        # 将单行 prompt 格式化为多行
        prompt = prompt.replace('[', '\n[').strip()
        print('OPT:YES')
        print(prompt)
    else:
        print('OPT:NO')
except:
    print('OPT:NO')
" 2>/dev/null)

# 提取第一行判断
FIRST_LINE=$(echo "$PARSED" | head -1)

if [ "$FIRST_LINE" = "OPT:YES" ]; then
    # 提取优化后的 Prompt（去掉第一行）
    OPT_PROMPT=$(echo "$PARSED" | tail -n +2)
    
    # 保存元数据到临时文件（用于用户反馈时读取）
    METADATA=$(echo "$RESULT" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(json.dumps({
        'intent': d.get('intent', 'unknown'),
        'variant': d.get('variant', 0),
        'role': d.get('role', ''),
        'industry': d.get('industry', ''),
        'domain': d.get('domain', '')
    }))
except:
    print('{}')
" 2>/dev/null)
    echo "$METADATA" > /tmp/pb_last_metadata.json
    
    # 根据偏好决定是否展示 Prompt 结构
    if [ "$SHOW_PROMPT" = "show" ]; then
        cat <<EOF
🤖 PromptBuddy 已优化你的问题
$OPT_PROMPT

---
💡 这个回答对你有帮助吗？ [1 有帮助] [2 需改进]
EOF
    else
        # 不展示 Prompt 结构，只输出原始问题（会被传给模型处理）
        # 由于需要优化，这里输出优化后的内容但不带展示
        cat <<EOF
$OPT_PROMPT

---
💡 这个回答对你有帮助吗？ [1 有帮助] [2 需改进]
EOF
    fi
else
    # 不需要优化，原样输出
    echo "$USER_INPUT"
fi