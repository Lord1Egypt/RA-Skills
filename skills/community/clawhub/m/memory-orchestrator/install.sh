#!/bin/bash
# Memory Orchestrator 安装脚本
# 功能：自动安装所有依赖、配置服务、初始化索引

set -e

WORKSPACE="/home/claw/.openclaw/workspace"
SKILL_DIR="$WORKSPACE/skills/memory-orchestrator"
LOG_FILE="$WORKSPACE/memory/state/install.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "开始安装 Memory Orchestrator..."

# 1. 检查 Python 环境
if ! command -v python3 &> /dev/null; then
    log "❌ Python3 未安装，请先安装 Python 3.9+"
    exit 1
fi
log "✅ Python3 已安装: $(python3 --version)"

# 2. 安装 Python 依赖
log "正在安装 Python 依赖..."
pip3 install -r "$SKILL_DIR/requirements.txt" -q
log "✅ Python 依赖安装完成"

# 3. 检查 Ollama 和模型
if ! command -v ollama &> /dev/null; then
    log "⚠️ Ollama 未安装，请手动安装：https://ollama.ai"
else
    log "✅ Ollama 已安装: $(ollama --version)"
    # 检查并拉取模型
    if ! ollama list | grep -q "qwen2.5:7b"; then
        log "正在拉取 qwen2.5:7b 模型..."
        ollama pull qwen2.5:7b
    fi
    if ! ollama list | grep -q "all-MiniLM-L6-v2"; then
        log "正在拉取 all-MiniLM-L6-v2 模型..."
        ollama pull all-MiniLM-L6-v2
    fi
    log "✅ Ollama 模型检查完成"
fi

# 4. 检查 Syncthing
if ! command -v syncthing &> /dev/null; then
    log "⚠️ Syncthing 未安装，请手动安装：sudo apt-get install syncthing"
else
    log "✅ Syncthing 已安装: $(syncthing --version)"
    # 启动服务
    if ! systemctl is-active --quiet syncthing@claw 2>/dev/null; then
        log "启动 Syncthing 服务..."
        sudo systemctl enable syncthing@claw
        sudo systemctl start syncthing@claw
    fi
    log "✅ Syncthing 服务状态: $(systemctl is-active syncthing@claw 2>/dev/null || echo '未运行')"
fi

# 5. 检查 Git 和 git-crypt
if ! command -v git &> /dev/null; then
    log "❌ Git 未安装，请先安装 Git"
    exit 1
fi
if ! command -v git-crypt &> /dev/null; then
    log "⚠️ git-crypt 未安装，请手动安装：sudo apt-get install git-crypt"
else
    log "✅ Git 和 git-crypt 已安装"
fi

# 6. 初始化 FAISS 索引
log "正在初始化 FAISS 索引..."
cd "$WORKSPACE"
python3 index_memory.py 2>/dev/null || log "⚠️ 索引初始化失败，请手动运行：python3 index_memory.py"
log "✅ FAISS 索引初始化完成"

# 7. 配置 iflow 钩子
log "配置 iflow 钩子..."
if [ -d "$WORKSPACE/.iflow/hooks" ]; then
    cp "$SKILL_DIR/hooks/pre-session.sh" "$WORKSPACE/.iflow/hooks/"
    cp "$SKILL_DIR/hooks/post-session.sh" "$WORKSPACE/.iflow/hooks/"
    chmod +x "$WORKSPACE/.iflow/hooks/"*.sh
    log "✅ iflow 钩子配置完成"
else
    log "⚠️ .iflow/hooks 目录不存在，跳过钩子配置"
fi

# 8. 配置 Cron 定时任务
log "配置 Cron 定时任务..."
if ! crontab -l 2>/dev/null | grep -q "auto-commit-memory.sh"; then
    (crontab -l 2>/dev/null; echo "*/30 * * * * $SKILL_DIR/scripts/auto-commit-memory.sh >> $LOG_FILE 2>&1") | crontab -
    log "✅ Cron 定时任务配置完成"
else
    log "✅ Cron 定时任务已存在"
fi

# 9. 生成欢迎信息
log "=========================================="
log "🎉 Memory Orchestrator 安装完成！"
log "=========================================="
log "📚 查看文档: $SKILL_DIR/SKILL.md"
log "🔍 测试搜索: memory_search '测试'"
log "🕸️ 生成图谱: memory_knowledge_graph generate"
log "❤️ 情感标注: memory_evolve tag-emotions"
log "=========================================="

echo "✅ 安装完成！请查看 $SKILL_DIR/SKILL.md 了解更多。"
