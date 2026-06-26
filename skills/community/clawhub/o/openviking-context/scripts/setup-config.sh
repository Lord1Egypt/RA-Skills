#!/usr/bin/env bash
set -euo pipefail

BOLD='\033[1m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m'

CONFIG_DIR="$HOME/.openviking"
WORKSPACE_DIR="${OPENVIKING_WORKSPACE:-$HOME/openviking_workspace}"

log_info()  { echo -e "${GREEN}[✓]${NC} $1"; }
log_step()  { echo -e "\n${BOLD}▸ $1${NC}"; }
prompt()    { echo -en "${CYAN}  $1${NC}"; }

mkdir -p "$CONFIG_DIR"

echo -e "${BOLD}═══════════════════════════════════════════${NC}"
echo -e "${BOLD}  OpenViking 交互式配置向导${NC}"
echo -e "${BOLD}═══════════════════════════════════════════${NC}"

# --- 选择提供商 ---
log_step "选择模型提供商"
echo "  1) openai       — OpenAI / 兼容 API"
echo "  2) volcengine   — 火山引擎豆包"
echo "  3) nvidia       — NVIDIA NIM (免费)"
echo "  4) litellm      — LiteLLM (Anthropic/DeepSeek/Gemini/Ollama...)"
echo ""
prompt "请选择 [1-4]: "
read -r PROVIDER_CHOICE

case "$PROVIDER_CHOICE" in
    1)
        VLM_PROVIDER="openai"
        EMB_PROVIDER="openai"
        DEFAULT_VLM_MODEL="gpt-4o"
        DEFAULT_EMB_MODEL="text-embedding-3-large"
        DEFAULT_EMB_DIM=3072
        DEFAULT_API_BASE="https://api.openai.com/v1"
        ;;
    2)
        VLM_PROVIDER="volcengine"
        EMB_PROVIDER="volcengine"
        DEFAULT_VLM_MODEL="doubao-seed-2-0-pro-260215"
        DEFAULT_EMB_MODEL="doubao-embedding-vision-250615"
        DEFAULT_EMB_DIM=1024
        DEFAULT_API_BASE="https://ark.cn-beijing.volces.com/api/v3"
        ;;
    3)
        VLM_PROVIDER="openai"
        EMB_PROVIDER="openai"
        DEFAULT_VLM_MODEL="meta/llama-3.3-70b-instruct"
        DEFAULT_EMB_MODEL="nvidia/nv-embed-v1"
        DEFAULT_EMB_DIM=4096
        DEFAULT_API_BASE="https://integrate.api.nvidia.com/v1"
        ;;
    4)
        VLM_PROVIDER="litellm"
        EMB_PROVIDER="openai"
        DEFAULT_VLM_MODEL="claude-3-5-sonnet-20240620"
        DEFAULT_EMB_MODEL="text-embedding-3-large"
        DEFAULT_EMB_DIM=3072
        DEFAULT_API_BASE=""
        ;;
    *)
        echo "无效选择，使用 openai 默认值"
        VLM_PROVIDER="openai"
        EMB_PROVIDER="openai"
        DEFAULT_VLM_MODEL="gpt-4o"
        DEFAULT_EMB_MODEL="text-embedding-3-large"
        DEFAULT_EMB_DIM=3072
        DEFAULT_API_BASE="https://api.openai.com/v1"
        ;;
esac

# --- API Key ---
log_step "配置 API Key"
prompt "API Key: "
read -rs API_KEY
echo ""

if [ -z "$API_KEY" ]; then
    echo -e "${YELLOW}[!] 未提供 API Key，你可以稍后在配置文件中设置${NC}"
    API_KEY="YOUR_API_KEY_HERE"
fi

# --- API Base ---
log_step "配置 API 端点"
prompt "API Base [$DEFAULT_API_BASE]: "
read -r API_BASE
API_BASE="${API_BASE:-$DEFAULT_API_BASE}"

# --- VLM Model ---
log_step "配置 VLM 模型（用于语义理解）"
prompt "VLM Model [$DEFAULT_VLM_MODEL]: "
read -r VLM_MODEL
VLM_MODEL="${VLM_MODEL:-$DEFAULT_VLM_MODEL}"

# --- Embedding Model ---
log_step "配置 Embedding 模型（用于向量检索）"
prompt "Embedding Model [$DEFAULT_EMB_MODEL]: "
read -r EMB_MODEL
EMB_MODEL="${EMB_MODEL:-$DEFAULT_EMB_MODEL}"

prompt "Embedding Dimension [$DEFAULT_EMB_DIM]: "
read -r EMB_DIM
EMB_DIM="${EMB_DIM:-$DEFAULT_EMB_DIM}"

# --- Workspace ---
log_step "配置工作目录"
prompt "Workspace [$WORKSPACE_DIR]: "
read -r WS
WS="${WS:-$WORKSPACE_DIR}"
mkdir -p "$WS"

# --- 生成 ov.conf ---
log_step "生成服务器配置"

cat > "$CONFIG_DIR/ov.conf" << OVEOF
{
  "storage": {
    "workspace": "$WS"
  },
  "log": {
    "level": "INFO",
    "output": "stdout"
  },
  "embedding": {
    "dense": {
      "api_base": "$API_BASE",
      "api_key": "$API_KEY",
      "provider": "$EMB_PROVIDER",
      "dimension": $EMB_DIM,
      "model": "$EMB_MODEL"
    },
    "max_concurrent": 10
  },
  "vlm": {
    "api_base": "$API_BASE",
    "api_key": "$API_KEY",
    "provider": "$VLM_PROVIDER",
    "model": "$VLM_MODEL",
    "max_concurrent": 100
  }
}
OVEOF

log_info "服务器配置已写入 $CONFIG_DIR/ov.conf"

# --- 生成 ovcli.conf ---
cat > "$CONFIG_DIR/ovcli.conf" << CLIEOF
{
  "url": "http://localhost:1933",
  "timeout": 60.0,
  "output": "table"
}
CLIEOF

log_info "CLI 配置已写入 $CONFIG_DIR/ovcli.conf"

# --- 设置环境变量 ---
export OPENVIKING_CONFIG_FILE="$CONFIG_DIR/ov.conf"
export OPENVIKING_CLI_CONFIG_FILE="$CONFIG_DIR/ovcli.conf"

echo ""
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo -e "${GREEN}  配置完成！${NC}"
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo ""
echo "  配置文件:  $CONFIG_DIR/ov.conf"
echo "  CLI 配置:  $CONFIG_DIR/ovcli.conf"
echo "  工作目录:  $WS"
echo "  VLM:       $VLM_PROVIDER / $VLM_MODEL"
echo "  Embedding: $EMB_PROVIDER / $EMB_MODEL (dim=$EMB_DIM)"
echo ""
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "下一步："
echo "  1. 启动服务器:  openviking-server"
echo "  2. 测试连接:    python3 $SCRIPT_DIR/viking.py info"
echo "  3. 添加资源:    python3 $SCRIPT_DIR/viking.py add ./your-docs/"
echo ""
