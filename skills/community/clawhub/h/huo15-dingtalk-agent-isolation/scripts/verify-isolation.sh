#!/usr/bin/env bash
# ============================================================
# verify-isolation.sh
# 验证钉钉 Agent 级隔离是否正确配置
# ============================================================

set -euo pipefail

BOLD='\033[1m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m'

PASS=0
FAIL=0

ok()   { echo -e "  ${GREEN}✅ $1${NC}"; PASS=$((PASS+1)); }
fail() { echo -e "  ${RED}❌ $1${NC}"; FAIL=$((FAIL+1)); }
info() { echo -e "  ${YELLOW}ℹ️  $1${NC}"; }

CONFIG_FILE="$HOME/.openclaw/openclaw.json"

echo -e "${BOLD}🔍 钉钉 Agent 级隔离验证${NC}"
echo "================================"
echo ""

# ---- 1. 检查配置文件 ----
echo -e "${BOLD}[1] 检查 openclaw.json${NC}"
if [[ ! -f "$CONFIG_FILE" ]]; then
  fail "配置文件不存在: $CONFIG_FILE"
  echo ""
  echo "总计: $PASS 通过, $FAIL 失败"
  exit 1
fi
ok "配置文件存在"

# 检查是否有 dingtalk-connector 配置
if grep -q "dingtalk-connector" "$CONFIG_FILE"; then
  ok "钉钉连接器已配置"
else
  fail "未找到 dingtalk-connector 配置"
fi

# 检查 agents.list
AGENTS_COUNT=$(python3 -c "
import json, re
with open('$CONFIG_FILE') as f:
    raw = f.read()
cleaned = re.sub(r'//.*$', '', raw, flags=re.MULTILINE)
cleaned = re.sub(r'/\*[\s\S]*?\*/', '', cleaned)
cleaned = re.sub(r',\s*([}\]])', r'\1', cleaned)
data = json.loads(cleaned)
agents = data.get('agents', {}).get('list', [])
print(len(agents))
" 2>/dev/null || echo "0")

if [[ "$AGENTS_COUNT" -gt 1 ]]; then
  ok "agents.list 包含 $AGENTS_COUNT 个 Agent"
else
  info "agents.list 只有 $AGENTS_COUNT 个 Agent（可能未配置隔离）"
fi

# 检查 bindings
BINDINGS_COUNT=$(python3 -c "
import json, re
with open('$CONFIG_FILE') as f:
    raw = f.read()
cleaned = re.sub(r'//.*$', '', raw, flags=re.MULTILINE)
cleaned = re.sub(r'/\*[\s\S]*?\*/', '', cleaned)
cleaned = re.sub(r',\s*([}\]])', r'\1', cleaned)
data = json.loads(cleaned)
bindings = data.get('bindings', [])
print(len(bindings))
" 2>/dev/null || echo "0")

if [[ "$BINDINGS_COUNT" -gt 0 ]]; then
  ok "bindings 包含 $BINDINGS_COUNT 条规则"
else
  info "bindings 为空（如使用动态创建模式，首次对话后会自动添加）"
fi

# 检查动态创建配置
if grep -q "dynamicAgentCreation" "$CONFIG_FILE"; then
  ok "dynamicAgentCreation 配置已添加"
  if grep -q '"enabled": true' "$CONFIG_FILE" && grep -A5 "dynamicAgentCreation" "$CONFIG_FILE" | grep -q '"enabled": true'; then
    ok "dynamicAgentCreation.enabled = true"
  else
    info "dynamicAgentCreation.enabled 可能未设为 true"
  fi
else
  info "未配置 dynamicAgentCreation（手动模式不需要）"
fi

echo ""

# ---- 2. 检查工作空间目录 ----
echo -e "${BOLD}[2] 检查工作空间目录${NC}"
WORKSPACE_DIRS=$(ls -d "$HOME/.openclaw/workspace-dingtalk-"* 2>/dev/null || true)
if [[ -n "$WORKSPACE_DIRS" ]]; then
  for dir in $WORKSPACE_DIRS; do
    if [[ -d "$dir" ]]; then
      ok "工作空间: $(basename "$dir")"
    fi
  done
else
  info "未找到 workspace-dingtalk-* 目录（动态模式下首次对话后自动创建）"
fi

echo ""

# ---- 3. 检查 Agent 目录 ----
echo -e "${BOLD}[3] 检查 Agent 目录${NC}"
AGENT_DIRS=$(ls -d "$HOME/.openclaw/agents/dingtalk-"* 2>/dev/null || true)
if [[ -n "$AGENT_DIRS" ]]; then
  for dir in $AGENT_DIRS; do
    if [[ -d "$dir/agent" ]]; then
      ok "Agent 目录: $(basename "$dir")"
    fi
  done
else
  info "未找到 agents/dingtalk-* 目录（动态模式下首次对话后自动创建）"
fi

echo ""

# ---- 4. 检查连接器源码（动态模式） ----
echo -e "${BOLD}[4] 检查连接器源码（动态模式）${NC}"
CONNECTOR_SRC=""
for c in "$HOME/.openclaw/extensions/dingtalk/src" "$HOME/.openclaw/extensions/dingtalk-connector/src"; do
  if [[ -d "$c" ]]; then
    CONNECTOR_SRC="$c"
    break
  fi
done

if [[ -n "$CONNECTOR_SRC" ]]; then
  ok "连接器源码目录: $CONNECTOR_SRC"
  if [[ -f "$CONNECTOR_SRC/dynamic-agent.ts" ]]; then
    ok "dynamic-agent.ts 已存在（动态模式已启用）"
  else
    info "dynamic-agent.ts 不存在（如需动态模式，请运行 patch 脚本）"
  fi
else
  info "未找到连接器源码目录（可能通过 npm 全局安装）"
fi

echo ""

# ---- 5. 检查 OpenClaw 运行状态 ----
echo -e "${BOLD}[5] 检查 OpenClaw 运行状态${NC}"
if command -v openclaw &>/dev/null; then
  ok "openclaw 命令可用"
  if openclaw status 2>/dev/null | grep -q "running"; then
    ok "OpenClaw 正在运行"
  else
    info "OpenClaw 可能未运行"
  fi
else
  info "openclaw 命令不在 PATH 中"
fi

echo ""
echo "================================"
echo -e "${BOLD}总计: ${GREEN}$PASS 通过${NC}, ${RED}$FAIL 失败${NC}${NC}"
echo ""

if [[ $FAIL -gt 0 ]]; then
  exit 1
fi
