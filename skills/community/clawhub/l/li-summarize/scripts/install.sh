#!/bin/bash
# li_summarize 安装脚本

set -e

echo "📝 安装 li_summarize 依赖..."

# 安装 summarize CLI (如果未安装)
if ! command -v summarize &> /dev/null; then
    echo "Installing summarize CLI..."
    npm install -g @steipete/summarize
fi

# 创建配置文件目录
mkdir -p ~/.summarize

# 配置文件路径
CONFIG_FILE="$HOME/.summarize/config.json"

# 只有当配置文件不存在时，才创建默认配置
if [[ ! -f "$CONFIG_FILE" ]]; then
    # 使用环境变量或默认值
    SUMMARIZE_MODEL="${SUMMARIZE_MODEL:-qwen/qwen2.5-72b-instruct}"
    BASE_URL="${OPENAI_BASE_URL:-https://dashscope.aliyuncs.com/compatible-mode/v1}"
    
    echo "🔧 创建默认配置文件..."
    cat > "$CONFIG_FILE" << EOF
{
  "model": "$SUMMARIZE_MODEL",
  "openaiBaseUrl": "$BASE_URL",
  "openaiApiKey": "YOUR-API-KEY-HERE",
  "length": "medium",
  "language": "zh-CN",
  "timeout": "2m"
}
EOF
    echo "✅ 已生成默认配置文件: $CONFIG_FILE"
    echo "⚠️  请编辑配置文件填入你的 API Key"
else
    echo "📋 检测到已有配置文件，保持不变: $CONFIG_FILE"
    SUMMARIZE_MODEL=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE')).get('model',''))" 2>/dev/null || echo "未知")
    echo "   当前模型: $SUMMARIZE_MODEL"
fi

# 创建预设提供商配置
cat > ~/.summarize/providers.json << 'EOF'
{
  "baidu": {
    "name": "百度千帆",
    "baseUrl": "https://qianfan.baidubce.com/v2",
    "models": ["qianfan/ernie-4.0-8k", "qianfan/ernie-3.5-8k", "qianfan/codegeex-4"]
  },
  "aliyun": {
    "name": "阿里云通义千问",
    "baseUrl": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    "models": ["qwen/qwen2.5-72b-instruct", "qwen/qwen-max", "qwen/qwen-turbo"]
  },
  "tencent": {
    "name": "腾讯混元",
    "baseUrl": "https://hunyuancloud.tencent.com/api/v3",
    "models": ["hunyuan/hunyuan-pro", "hunyuan/hunyuan-standard"]
  },
  "bytedance": {
    "name": "字节跳动火山引擎",
    "baseUrl": "https://ark.cn-beijing.volces.com/api/v3",
    "models": ["doubao-pro-32k", "doubao-standard-32k"]
  },
  "moonshot": {
    "name": "Moonshot AI (月之暗面)",
    "baseUrl": "https://api.moonshot.cn/v1",
    "models": ["moonshot/kimi-k2-0711-preview", "moonshot/kimi-long"]
  },
  "deepseek": {
    "name": "DeepSeek",
    "baseUrl": "https://api.deepseek.com/v1",
    "models": ["deepseek-chat", "deepseek-coder"]
  },
  "zhipu": {
    "name": "智谱 AI",
    "baseUrl": "https://open.bigmodel.cn/api/paas/v4",
    "models": ["glm-4-plus", "glm-4-flash", "glm-4"]
  },
  "minimax": {
    "name": "MiniMax",
    "baseUrl": "https://api.minimax.chat/v1",
    "models": ["MiniMax-Text-01", "abab6.5s-chat"]
  },
  "stepfun": {
    "name": "阶跃星辰",
    "baseUrl": "https://api.stepfun.com/v1",
    "models": ["step-1v-8k", "step-1.5-chat"]
  },
  "ollama": {
    "name": "Ollama (本地)",
    "baseUrl": "http://localhost:11434/v1",
    "models": ["llama3", "qwen2.5:72b", "deepseek-coder"]
  },
  "oneapi": {
    "name": "OneAPI / All In One",
    "baseUrl": "http://localhost:3000/v1",
    "models": ["gpt-4", "gpt-3.5-turbo", "claude-3-sonnet"]
  }
}
EOF

echo "✅ li_summarize 安装完成!"
echo ""
echo "📋 当前配置:"
echo "   模型: $SUMMARIZE_MODEL"
echo "   配置文件: $CONFIG_FILE"
echo ""
echo "📝 配置方式（二选一）:"
echo "1. 编辑 $CONFIG_FILE 填入你的 API Key"
echo "2. 使用环境变量 (推荐):"
echo "   export OPENAI_BASE_URL='https://dashscope.aliyuncs.com/compatible-mode/v1'"
echo "   export OPENAI_API_KEY='your-key'"
echo ""
echo "📖 查看支持的提供商: cat ~/.summarize/providers.json"