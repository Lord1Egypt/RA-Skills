#!/bin/bash
# li_summarize 自动配置脚本
# 读取环境变量并自动设置

set -e

CONFIG_FILE="$HOME/.summarize/config.json"

echo "🔧 正在配置 li_summarize..."

# 优先使用环境变量
BASE_URL="${OPENAI_BASE_URL:-}"
API_KEY="${OPENAI_API_KEY:-}"
MODEL="${SUMMARIZE_MODEL:-qwen/qwen2.5-72b-instruct}"

# 如果环境变量为空，提示用户
if [ -z "$BASE_URL" ]; then
    echo "⚠️  未检测到 OPENAI_BASE_URL 环境变量"
    echo "   使用默认地址: https://dashscope.aliyuncs.com/compatible-mode/v1"
    BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
fi

if [ -z "$API_KEY" ]; then
    echo "⚠️  未检测到 OPENAI_API_KEY 环境变量"
    echo "   请在配置文件中填入 API Key"
    HAS_KEY=false
else
    HAS_KEY=true
fi

# 确保目录存在
mkdir -p "$HOME/.summarize"

# 创建配置文件
cat > "$CONFIG_FILE" << EOF
{
  "model": "$MODEL",
  "openaiBaseUrl": "$BASE_URL",
  "openaiApiKey": "$API_KEY",
  "length": "medium",
  "language": "zh-CN",
  "timeout": "2m"
}
EOF

if [ "$HAS_KEY" = true ]; then
    echo "✅ 已创建配置文件: $CONFIG_FILE"
else
    # 用占位符替换空 key
    sed -i 's/"openaiApiKey": ""/"openaiApiKey": "YOUR-API-KEY-HERE"/g' "$CONFIG_FILE"
    echo "⚠️  已创建模板配置文件，请手动填入 API Key: $CONFIG_FILE"
fi

echo ""
echo "📝 使用方式:"
echo "   summarize \"https://example.com\" --model $MODEL"
echo ""
echo "📖 查看配置: cat $CONFIG_FILE"
echo ""
echo "💡 提示: 推荐使用环境变量配置:"
echo "   export OPENAI_BASE_URL='$BASE_URL'"
echo "   export OPENAI_API_KEY='your-key'"