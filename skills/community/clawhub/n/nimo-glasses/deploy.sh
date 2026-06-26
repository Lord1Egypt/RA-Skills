#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# Nimo AI Glasses × OpenClaw 一键部署脚本
# 在 VPS 上执行此脚本完成全部配置
# ═══════════════════════════════════════════════════════════════

set -e

echo "🥽 Nimo AI Glasses × OpenClaw 部署脚本"
echo "═══════════════════════════════════════"

# ── 配置项（按需修改）──
GATEWAY_TOKEN="${GATEWAY_TOKEN:-nimo-demo-2026}"
GEMINI_API_KEY="${GEMINI_API_KEY:-}"
OPENAI_API_KEY="${OPENAI_API_KEY:-}"
MODEL="${MODEL:-google/gemini-2.5-flash}"
PLUGIN_DIR="$HOME/.openclaw/extensions/nimo-glasses"

# ── Step 1: 安装 OpenClaw ──
echo ""
echo "📦 Step 1: 安装 OpenClaw..."
if command -v openclaw &>/dev/null; then
  echo "OpenClaw 已安装: $(openclaw --version)"
  echo "正在更新..."
  npm update -g openclaw 2>/dev/null || npm install -g openclaw
else
  npm install -g openclaw
fi
echo "✅ OpenClaw $(openclaw --version)"

# ── Step 2: 清理旧配置（可选）──
if [ -f "$HOME/.openclaw/openclaw.json" ]; then
  echo ""
  read -p "⚠️  检测到旧配置，是否清除重新开始？(y/N) " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -rf "$HOME/.openclaw"
    echo "✅ 旧配置已清除"
  fi
fi

# ── Step 3: 初始化配置 ──
echo ""
echo "⚙️  Step 3: 配置 Gateway..."

# 确保配置目录存在
mkdir -p "$HOME/.openclaw"

# 开启 HTTP API
openclaw config set gateway.http.endpoints.chatCompletions.enabled true 2>/dev/null || true

# 绑定到公网
openclaw config set gateway.bind lan 2>/dev/null || true

# 设置 token
openclaw config set gateway.auth.token "$GATEWAY_TOKEN" 2>/dev/null || true

# 设置模型
if [ -n "$OPENAI_API_KEY" ]; then
  openclaw config set env.OPENAI_API_KEY "$OPENAI_API_KEY" 2>/dev/null || true
  openclaw config set agents.defaults.model.primary "openai/gpt-4o" 2>/dev/null || true
  echo "✅ 模型: OpenAI GPT-4o"
elif [ -n "$GEMINI_API_KEY" ]; then
  openclaw config set env.GEMINI_API_KEY "$GEMINI_API_KEY" 2>/dev/null || true
  openclaw config set agents.defaults.model.primary "$MODEL" 2>/dev/null || true
  echo "✅ 模型: $MODEL"
else
  echo "⚠️  未设置 API Key，请手动配置："
  echo "   openclaw config set env.GEMINI_API_KEY 'your-key'"
  echo "   openclaw config set agents.defaults.model.primary 'google/gemini-2.5-flash'"
fi

echo "✅ Token: $GATEWAY_TOKEN"

# ── Step 4: 安装 Nimo 眼镜插件 ──
echo ""
echo "🔌 Step 4: 安装 Nimo 眼镜插件..."

mkdir -p "$PLUGIN_DIR"

# 检查插件文件是否已存在
if [ -f "$PLUGIN_DIR/index.ts" ]; then
  echo "插件已存在，更新中..."
fi

# 复制当前目录的插件文件（假设脚本在插件目录内执行）
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
if [ -f "$SCRIPT_DIR/index.ts" ]; then
  cp "$SCRIPT_DIR/index.ts" "$PLUGIN_DIR/index.ts"
  cp "$SCRIPT_DIR/openclaw.plugin.json" "$PLUGIN_DIR/openclaw.plugin.json"
  cp "$SCRIPT_DIR/package.json" "$PLUGIN_DIR/package.json"
  [ -f "$SCRIPT_DIR/README.md" ] && cp "$SCRIPT_DIR/README.md" "$PLUGIN_DIR/README.md"
elif [ -f "$SCRIPT_DIR/src/index.ts" ]; then
  cp "$SCRIPT_DIR/src/index.ts" "$PLUGIN_DIR/index.ts"
  cp "$SCRIPT_DIR/openclaw.plugin.json" "$PLUGIN_DIR/openclaw.plugin.json"
  cp "$SCRIPT_DIR/package.json" "$PLUGIN_DIR/package.json"
  [ -f "$SCRIPT_DIR/README.md" ] && cp "$SCRIPT_DIR/README.md" "$PLUGIN_DIR/README.md"
else
  echo "❌ 找不到插件文件，请确保在插件目录中执行此脚本"
  exit 1
fi

# 启用插件
openclaw config set plugins.allow '["nimo-glasses"]' 2>/dev/null || true
openclaw config set plugins.entries.nimo-glasses.enabled true 2>/dev/null || true
openclaw config set plugins.entries.nimo-glasses.config.maxResponseLength 300 2>/dev/null || true
openclaw config set plugins.entries.nimo-glasses.config.systemPrompt '你是 Nimo 智能眼镜中的 AI 助手。回复简洁（300字内），不换行不列表，匹配用户语言，直接回答。' 2>/dev/null || true

echo "✅ 插件已安装到 $PLUGIN_DIR"

# ── Step 5: 启动 Gateway ──
echo ""
echo "🚀 Step 5: 启动 Gateway..."

# 停止已有的
openclaw gateway stop 2>/dev/null || true
sleep 2

# 启动
openclaw gateway start

echo ""
echo "═══════════════════════════════════════"
echo "✅ 部署完成！"
echo ""
echo "📍 Gateway 地址: http://$(hostname -I 2>/dev/null | awk '{print $1}' || echo 'YOUR_IP'):18789"
echo "🔑 Token: $GATEWAY_TOKEN"
echo ""
echo "📡 Demo API:"
echo "   POST http://YOUR_IP:18789/v1/chat/completions"
echo ""
echo "🔌 插件 API:"
echo "   GET  http://YOUR_IP:18789/nimo/health"
echo "   POST http://YOUR_IP:18789/nimo/pair"
echo "   POST http://YOUR_IP:18789/nimo/chat"
echo "   GET  http://YOUR_IP:18789/nimo/events"
echo ""
echo "查看 linkCode: curl http://localhost:18789/nimo/health"
echo "═══════════════════════════════════════"
