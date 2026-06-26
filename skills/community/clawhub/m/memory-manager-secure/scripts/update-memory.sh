#!/bin/bash
# 智能更新 MEMORY.md - 通用模式 v1.0.12
# 自动读取 openclaw.json 中配置的任意服务商

set -e

WORKSPACE="$HOME/.openclaw/workspace"
MEMORY_FILE="$WORKSPACE/MEMORY.md"
MEMORY_DIR="$WORKSPACE/memory"
TODAY=$(date +%Y-%m-%d)
LAST_UPDATE_FILE="$WORKSPACE/.memory_last_update"
OPENCLAW_CONFIG="$HOME/.openclaw/openclaw.json"

echo "🧠 智能记忆更新 - 通用模式 v1.0.12"
echo "📅 日期：$TODAY"

# ========== 步骤 0：从 openclaw.json 读取配置 ==========
echo "⚙️ 读取 OpenClaw 配置..."

CONFIG_JSON=$(python3 - "$OPENCLAW_CONFIG" << 'PYTHON_CODE'
import json
import sys
import os

config_path = sys.argv[1]

# 读取配置
try:
    with open(config_path, 'r') as f:
        config = json.load(f)
except:
    print("ERROR:config_not_found")
    sys.exit(0)

# 读取 auth profiles（用于匹配 API Key）
auth_profiles = config.get('auth', {}).get('profiles', {})
profile_providers = set()
for profile_name, profile_data in auth_profiles.items():
    provider = profile_data.get('provider', '')
    if provider:
        profile_providers.add(provider)

# 遍历所有 providers，找到第一个有 baseUrl 的
providers = config.get('models', {}).get('providers', {})
selected = None

for provider_name, provider_config in providers.items():
    base_url = provider_config.get('baseUrl', '')
    if base_url:
        # 获取默认模型
        default_model = config.get('agents', {}).get('defaults', {}).get('model', {}).get('primary', '')
        
        # 如果默认模型是这个 provider 的，提取模型名
        model_name = 'qwen3.5-plus'  # 默认
        if default_model.startswith(f'{provider_name}/'):
            model_name = default_model.split('/')[-1]
        elif provider_name == 'modelstudio':
            # 百炼的默认模型
            model_name = 'qwen3.5-plus'
        elif provider_name == 'vllm':
            # vllm 通常用 deepseek
            model_name = 'deepseek-chat'
        
        selected = {
            'provider': provider_name,
            'api_url': base_url.rstrip('/') + '/chat/completions',
            'model': model_name,
            'is_auth_profile': provider_name in profile_providers
        }
        break

if not selected:
    print("ERROR:no_provider_found")
    sys.exit(0)

print(json.dumps(selected))
PYTHON_CODE
)

# 检查是否读取成功
if echo "$CONFIG_JSON" | grep -q "^ERROR:"; then
    ERROR_MSG=$(echo "$CONFIG_JSON" | sed 's/^ERROR://')
    echo "⚠️ 配置读取失败：$ERROR_MSG (使用规则模式)"
    USE_LLM=false
    API_URL=""
    API_KEY=""
    MODEL=""
else
    # 解析配置
    API_URL=$(echo "$CONFIG_JSON" | jq -r '.api_url // ""')
    MODEL=$(echo "$CONFIG_JSON" | jq -r '.model // "qwen3.5-plus"')
    PROVIDER=$(echo "$CONFIG_JSON" | jq -r '.provider // ""')
    IS_AUTH=$(echo "$CONFIG_JSON" | jq -r '.is_auth_profile // false')
    
    echo "📡 服务商：$PROVIDER"
    echo "🔗 API: $API_URL"
    echo "🤖 模型：$MODEL"
    
    # ========== 步骤 1：匹配 API Key ==========
    echo "🔑 匹配 API Key..."
    
    API_KEY=""
    
    # 定义服务商到环境变量名的映射
    declare -A KEY_MAP=(
        ["modelstudio"]="BAILIAN_API_KEY ALIYUN_API_KEY DASHSCOPE_API_KEY"
        ["vllm"]="VLLM_API_KEY DEEPSEEK_API_KEY"
        ["openai"]="OPENAI_API_KEY"
        ["deepseek"]="DEEPSEEK_API_KEY"
        ["anthropic"]="ANTHROPIC_API_KEY"
        ["google"]="GOOGLE_API_KEY GEMINI_API_KEY"
        ["azure"]="AZURE_OPENAI_API_KEY"
    )
    
    # 根据服务商名称查找对应的环境变量
    KEY_VARS="${KEY_MAP[$PROVIDER]:-OPENCLAW_API_KEY API_KEY}"
    
    for var_name in $KEY_VARS; do
        if [ -n "${!var_name:-}" ]; then
            API_KEY="${!var_name}"
            echo "✅ 从 ${var_name} 获取"
            break
        fi
    done
    
    # 如果还是没找到，检查是否是 auth profile（可能 key 在 openclaw 内部）
    if [ -z "$API_KEY" ] && [ "$IS_AUTH" = "true" ]; then
        echo "⚠️ 服务商已认证但 Key 不在环境变量"
        echo "💡 请配置对应的环境变量（见下文）"
    fi
    
    # 最终检查
    if [ -z "$API_KEY" ]; then
        echo "⚠️ 未找到 API Key (使用规则模式)"
        echo "💡 配置方法："
        if [ "$PROVIDER" = "modelstudio" ]; then
            echo "   export BAILIAN_API_KEY='sk-xxx'"
        elif [ "$PROVIDER" = "vllm" ]; then
            echo "   export DEEPSEEK_API_KEY='xxx'"
        elif [ "$PROVIDER" = "openai" ]; then
            echo "   export OPENAI_API_KEY='sk-xxx'"
        else
            echo "   export OPENCLAW_API_KEY='xxx'"
        fi
        USE_LLM=false
    else
        USE_LLM=true
        KEY_SHOW="${API_KEY:0:8}...${API_KEY: -4}"
        echo "🔑 Key: $KEY_SHOW"
    fi
fi

# ========== 步骤 2：检查当天会话 ==========
TODAY_FILE="$MEMORY_DIR/$TODAY.md"
if [ ! -f "$TODAY_FILE" ]; then
    echo "⏭️ 当天无会话记录"
    exit 0
fi

# ========== 步骤 3：检查是否已更新 ==========
if [ -f "$LAST_UPDATE_FILE" ] && [ "$(cat "$LAST_UPDATE_FILE")" = "$TODAY" ]; then
    echo "⏭️ 今日已更新"
    exit 0
fi

# ========== 步骤 4：规则预过滤 ==========
echo "🔍 规则预过滤..."
PATTERNS="配置 | 安装 | 发布|技能|Skill|clawhub|警告 | 错误 | 修复 | 更新 | 定时任务|cron|API|Token|TTS|频道 | 决定 | 切换 | 创建 | 测试 | 检测 | 存储 | 模型 | 智能 | 欠费 | 登录 | 安全 | 通用 | 服务商"

MATCHED_CONTENT=$(grep -iE "$PATTERNS" "$TODAY_FILE" 2>/dev/null | head -n 30 || true)
if [ -z "$MATCHED_CONTENT" ]; then
    echo "⏭️ 无匹配内容"
    exit 0
fi

MATCH_COUNT=$(echo "$MATCHED_CONTENT" | wc -l)
echo "📊 匹配：$MATCH_COUNT 行"

# ========== 步骤 5：保存临时文件 ==========
TMP_FILE=$(mktemp)
echo "$MATCHED_CONTENT" > "$TMP_FILE"
trap "rm -f $TMP_FILE" EXIT

# ========== 步骤 6：调用 LLM（如果配置了 API Key） ==========
if [ "$USE_LLM" = true ] && [ -n "$API_URL" ]; then
    echo "📡 调用 LLM (15s 超时)..."
    
    RESULT=$(timeout 15 python3 - "$API_KEY" "$API_URL" "$MODEL" "$TMP_FILE" << 'PYTHON_CODE'
import json
import socket
import urllib.request
import sys
import re

socket.setdefaulttimeout(10)

api_key = sys.argv[1]
api_url = sys.argv[2]
model = sys.argv[3]
file_path = sys.argv[4]

with open(file_path, 'r') as f:
    content = f.read().strip()

if not content:
    print("NO_CONTENT")
    sys.exit(0)

system_prompt = "你是 OpenClaw 记忆助手。从会话日志提取重要事件（配置变更/技能发布/系统修改/定时任务/重要决定）。跳过闲聊。检测敏感信息（API Key/Token/Secret）。返回纯 JSON（无 markdown）：{\"events\":[{\"title\":\"标题\",\"detail\":\"详情 (50 字)\",\"category\":\"配置 | 技能 | 系统 | 任务 | 决策\"}],\"sensitive_detected\":false,\"summary\":\"50 字总结\"}"

data = {
    "model": model,
    "messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": content}
    ],
    "temperature": 0.3,
    "max_tokens": 800
}

req = urllib.request.Request(
    api_url,
    data=json.dumps(data).encode('utf-8'),
    headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
    method="POST"
)

try:
    with urllib.request.urlopen(req, timeout=10) as response:
        raw = response.read().decode('utf-8')
        result = json.loads(raw)
        content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
        content = re.sub(r'```json\s*', '', content)
        content = re.sub(r'```', '', content)
        parsed = json.loads(content.strip())
        events = parsed.get("events", [])
        if not events:
            print("NO_EVENTS")
        else:
            print(f"EVENTS:{json.dumps(events)}")
            print(f"SENSITIVE:{parsed.get('sensitive_detected', False)}")
            print(f"SUMMARY:{parsed.get('summary', '更新')}")
except socket.timeout:
    print("TIMEOUT")
except Exception as e:
    print(f"ERROR:{str(e)}")
PYTHON_CODE
    ) || RESULT="TIMEOUT"
else
    RESULT="NO_API_KEY"
fi

# ========== 步骤 7：处理结果 ==========
case "$RESULT" in
    *TIMEOUT*|*ERROR*|NO_API_KEY)
        if [ "$RESULT" = "NO_API_KEY" ]; then
            echo "⚠️ 未配置 API Key (降级规则模式)"
        else
            echo "⚠️ 调用失败 (降级规则模式)"
        fi
        echo -e "\n### $TODAY - 规则匹配" >> "$MEMORY_FILE"
        echo "$MATCHED_CONTENT" | head -n 10 | while IFS= read -r line; do
            [ -n "$line" ] && echo "- $line" >> "$MEMORY_FILE"
        done
        echo "$TODAY" > "$LAST_UPDATE_FILE"
        exit 0
        ;;
    NO_CONTENT|NO_EVENTS)
        echo "⏭️ 无重要事件"
        exit 0
        ;;
esac

# 提取数据
EVENTS_JSON=$(echo "$RESULT" | grep "^EVENTS:" | sed 's/^EVENTS://')
SENSITIVE=$(echo "$RESULT" | grep "^SENSITIVE:" | sed 's/^SENSITIVE://')
SUMMARY=$(echo "$RESULT" | grep "^SUMMARY:" | sed 's/^SUMMARY://')
EVENT_COUNT=$(echo "$EVENTS_JSON" | jq -r 'length' 2>/dev/null)

if [ -z "$EVENTS_JSON" ] || [ "$EVENT_COUNT" = "0" ]; then
    echo "⏭️ 无事件"
    exit 0
fi

echo "✅ $EVENT_COUNT 个事件"

# ========== 步骤 8：更新 MEMORY.md ==========
echo "📝 更新 MEMORY.md..."

{
    echo ""
    if [ "$SENSITIVE" = "true" ]; then
        echo "### ⚠️ $TODAY - $SUMMARY"
        echo "**敏感信息已脱敏**"
    else
        echo "### ✅ $TODAY - $SUMMARY"
    fi
    echo ""
    echo "$EVENTS_JSON" | jq -r '.[] | "  - [\(.category)] \(.title): \(.detail)"'
    echo ""
} >> "$MEMORY_FILE"

echo "$TODAY" > "$LAST_UPDATE_FILE"
echo "✅ 完成 | 敏感：$SENSITIVE"
