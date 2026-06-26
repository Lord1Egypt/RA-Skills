#!/bin/bash
# Memory Orchestrator 启动脚本
# 功能：启动所有服务并验证状态

set -e

WORKSPACE="/home/claw/.openclaw/workspace"
SKILL_DIR="$WORKSPACE/skills/memory-orchestrator"

echo "🚀 启动 Memory Orchestrator..."

# 1. 启动 Syncthing
if systemctl is-active --quiet syncthing@claw 2>/dev/null; then
    echo "✅ Syncthing 已运行"
else
    echo "启动 Syncthing..."
    sudo systemctl start syncthing@claw
    sleep 2
fi

# 2. 启动 Ollama
if ! pgrep -x "ollama" > /dev/null; then
    echo "启动 Ollama..."
    ollama serve &
    sleep 3
fi
echo "✅ Ollama 已运行"

# 3. 验证 FAISS 索引
if [ -f "$WORKSPACE/index/memory_index.faiss" ]; then
    echo "✅ FAISS 索引已存在"
else
    echo "⚠️ FAISS 索引不存在，正在生成..."
    python3 "$WORKSPACE/index_memory.py"
fi

# 4. 验证钩子脚本
if [ -x "$WORKSPACE/.iflow/hooks/pre-session.sh" ]; then
    echo "✅ Pre-session 钩子就绪"
else
    echo "⚠️ Pre-session 钩子未配置"
fi

if [ -x "$WORKSPACE/.iflow/hooks/post-session.sh" ]; then
    echo "✅ Post-session 钩子就绪"
else
    echo "⚠️ Post-session 钩子未配置"
fi

echo ""
echo "🎉 Memory Orchestrator 已就绪！"
echo "📚 使用示例:"
echo "  memory_search '关键词'"
echo "  memory_multimodal process image.jpg"
echo "  memory_knowledge_graph generate"
echo "  memory_evolve run"
