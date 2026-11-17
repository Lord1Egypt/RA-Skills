#!/usr/bin/env bash
# 配置 Codex 接入聚星逸网关
# 用法:
#   交互式: bash configure.sh
#   非交互式: JUXINGYI_API_KEY="fsk-xxx" JUXINGYI_MODEL="deepseek-v4-flash" bash configure.sh
set -euo pipefail

CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
API_BASE="${JUXINGYI_API_BASE:-https://fireworks-simulator-api.huo15.com/v1}"
CONFIG_FILE="$CODEX_HOME/config.toml"

echo "=== Codex 接入聚星逸配置 ==="
echo ""

# --- 1. 确保 Codex 目录存在 ---
mkdir -p "$CODEX_HOME"

# --- 2. 获取 API Key ---
API_KEY="${JUXINGYI_API_KEY:-}"
if [ -z "$API_KEY" ]; then
  echo "请在聚星逸控制台创建 API Key:"
  echo "  https://fireworks-simulator.huo15.com/app/#/keys"
  echo ""
  read -p "输入 API Key (fsk-开头): " -s API_KEY
  echo ""
  if [ -z "$API_KEY" ]; then
    echo "错误: API Key 不能为空"
    exit 1
  fi
fi

# --- 3. 拉取可用模型列表 ---
echo "正在从聚星逸获取可用模型列表..."
MODELS_JSON=$(curl -s -H "Authorization: Bearer $API_KEY" "$API_BASE/models" 2>/dev/null || echo "")
if [ -z "$MODELS_JSON" ] || echo "$MODELS_JSON" | jq -e '.error' &>/dev/null; then
  echo "错误: 无法获取模型列表，请检查 API Key 和网络"
  echo "  API_BASE: $API_BASE"
  if [ -n "$MODELS_JSON" ]; then
    echo "  返回: $MODELS_JSON"
  fi
  exit 1
fi

MODELS=$(echo "$MODELS_JSON" | jq -r '.data[].id' 2>/dev/null || echo "")
MODEL_COUNT=$(echo "$MODELS" | wc -l | tr -d ' ')
echo "  获取到 $MODEL_COUNT 个可用模型"
echo ""

# --- 4. 选择模型 ---
MODEL="${JUXINGYI_MODEL:-}"
if [ -z "$MODEL" ]; then
  echo "可用模型（前 20 个）:"
  echo "$MODELS" | head -20 | nl -w2 -s'. '
  if [ "$MODEL_COUNT" -gt 20 ]; then
    echo "  ... 共 $MODEL_COUNT 个"
  fi
  echo ""
  echo "推荐模型:"
  echo "  deepseek-v4-flash    - 快速、便宜"
  echo "  deepseek-v4-pro      - 强力推理"
  echo "  claude-opus-4-8      - Claude 最强"
  echo "  gpt-5.4              - GPT 最新"
  echo ""
  read -p "选择模型 (输入名称): " MODEL
  if [ -z "$MODEL" ]; then
    MODEL="deepseek-v4-flash"
    echo "  使用默认: $MODEL"
  fi
fi

# 验证模型存在
if ! echo "$MODELS" | grep -qx "$MODEL"; then
  echo "警告: 模型 '$MODEL' 不在可用列表中（可能仍可用，继续配置）"
fi

# --- 5. 备份现有配置 ---
if [ -f "$CONFIG_FILE" ]; then
  BACKUP="$CONFIG_FILE.bak.$(date +%Y%m%d%H%M%S)"
  cp "$CONFIG_FILE" "$BACKUP"
  echo "已备份现有配置: $BACKUP"
fi

# --- 6. 写入配置 ---
# 策略：读取现有配置，删除聚星逸相关行，追加新配置段
# 保留用户原有的 plugins/mcp_servers/projects 等段
TEMP_FILE=$(mktemp)
if [ -f "$CONFIG_FILE" ]; then
  # 删除旧的聚星逸相关配置行（model_provider/openai_base_url/model/review_model/model_reasoning_effort）
  grep -vE '^model_provider|^openai_base_url|^model_reasoning_effort|^model |^review_model' "$CONFIG_FILE" > "$TEMP_FILE" || true
else
  echo "" > "$TEMP_FILE"
fi

# 在文件开头插入聚星逸配置
{
  echo "# Codex 接入聚星逸网关 (配置于 $(date '+%Y-%m-%d %H:%M:%S'))"
  echo 'model_provider = "juxingyi"'
  echo "openai_base_url = \"$API_BASE\""
  echo "model = \"$MODEL\""
  echo 'model_reasoning_effort = "medium"'
  echo ""
  cat "$TEMP_FILE"
} > "$CONFIG_FILE"

rm -f "$TEMP_FILE"

echo ""
echo "=== 配置完成 ==="
echo "  配置文件: $CONFIG_FILE"
echo "  网关地址: $API_BASE"
echo "  模型: $MODEL"
echo ""

# --- 7. 验证连通性 ---
echo "正在验证连通性..."
TEST_RESULT=$(curl -s -w "\n%{http_code}" -H "Authorization: Bearer $API_KEY" "$API_BASE/models" 2>/dev/null)
HTTP_CODE=$(echo "$TEST_RESULT" | tail -1)
if [ "$HTTP_CODE" = "200" ]; then
  echo "  连通性验证通过"
else
  echo "  警告: 连通性验证失败 (HTTP $HTTP_CODE)"
  echo "  请检查 API Key 是否有效"
fi

echo ""
echo "Codex 现在可以使用聚星逸网关调用 50+ 大模型了。"
echo ""
echo "下一步: bash scripts/codex-status.sh  # 查看 Codex 状态"
