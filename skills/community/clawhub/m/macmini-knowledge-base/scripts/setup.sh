#!/bin/bash
# knowledge-base-setup 一键安装脚本 v2.0
# 用法: bash setup.sh <feishu_user_id>

set -e

FEISHU_USER_ID="${1:-}"

echo "=========================================="
echo "  知识库 + RAG 搜索系统 安装脚本 v2.0"
echo "=========================================="

# 1. Create directories
echo "[1/8] 创建目录结构..."
mkdir -p ~/.openclaw/workspace/knowledge/.analysis/summaries/archives
mkdir -p ~/.openclaw/workspace/knowledge/temp_docs
mkdir -p ~/.openclaw/workspace/knowledge/"Macro Financials"
touch ~/.openclaw/workspace/knowledge/文章目录/文章目录.md
echo "  目录创建完成"

# 2. Install system dependencies
echo "[2/8] 安装系统依赖..."
if command -v antiword &>/dev/null; then
    echo "  antiword 已安装"
else
    brew install antiword
fi

if command -v tesseract &>/dev/null; then
    echo "  tesseract 已安装"
else
    brew install tesseract
fi

if command -v pandoc &>/dev/null; then
    echo "  pandoc 已安装: $(pandoc --version | head -1)"
else
    brew install pandoc
fi

echo "  系统依赖安装完成"

# 3. Install Python dependencies
echo "[3/8] 安装 Python 依赖..."
pip3 install kreuzberg pytesseract pymupdf docx openpyxl python-pptx --quiet 2>/dev/null || \
pip3 install kreuzberg pytesseract pymupdf docx openpyxl python-pptx
echo "  Python 依赖安装完成"

# 4. Install Ollama
echo "[4/8] 检查 Ollama..."
if command -v ollama &>/dev/null; then
    echo "  Ollama 已安装: $(ollama --version 2>/dev/null || echo 'unknown')"
else
    echo "  请手动安装 Ollama: https://ollama.com/download"
fi

# 5. Pull embedding model
echo "[5/8] 下载 embedding 模型..."
if ollama list 2>/dev/null | grep -q "nomic-embed-text"; then
    echo "  nomic-embed-text 已存在"
else
    ollama pull nomic-embed-text
fi

# 6. Copy scripts
echo "[6/8] 部署分析脚本..."
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cp "$SCRIPT_DIR/run_analysis.py" ~/.openclaw/workspace/knowledge/.analysis/
cp "$SCRIPT_DIR/generate_catalog.py" ~/.openclaw/workspace/knowledge/.analysis/
cp "$SCRIPT_DIR/utils.py" ~/.openclaw/workspace/knowledge/.analysis/
chmod +x ~/.openclaw/workspace/knowledge/.analysis/run_analysis.py
chmod +x ~/.openclaw/workspace/knowledge/.analysis/generate_catalog.py
chmod +x ~/.openclaw/workspace/knowledge/.analysis/utils.py
echo "  脚本已部署到 ~/.openclaw/workspace/knowledge/.analysis/"

# 7. Update OpenClaw config
echo "[7/8] 更新 OpenClaw 配置..."
CONFIG_FILE="$HOME/.openclaw/openclaw.json"
BACKUP_FILE="$CONFIG_FILE.bak.$(date +%Y%m%d%H%M%S)"

if [ -f "$CONFIG_FILE" ]; then
    cp "$CONFIG_FILE" "$BACKUP_FILE"
    echo "  配置已备份到: $BACKUP_FILE"
fi

# 8. Register cron tasks
echo "[8/8] 注册定时任务..."
if [ -z "$FEISHU_USER_ID" ]; then
    echo "  ⚠️  未提供飞书用户ID，跳过定时任务注册"
    echo "  如需注册，请运行：bash setup.sh <飞书用户ID>"
else
    # Check if tasks already exist
    openclaw cron list 2>/dev/null | grep -q "分析新文档" && \
        echo "  定时任务已存在，跳过" || \
        openclaw cron add \
            --name "23:00分析新文档" \
            --cron "0 23 * * *" \
            --tz "Asia/Shanghai" \
            --session isolated \
            --timeout-seconds 600 \
            --message "cd ~/.openclaw/workspace/knowledge/.analysis && python3 run_analysis.py && python3 generate_catalog.py" \
            --announce --channel feishu --to "user:$FEISHU_USER_ID" 2>/dev/null || \
        echo "  定时任务注册失败，请手动执行"
fi

echo ""
echo "=========================================="
echo "  安装完成！"
echo "=========================================="
echo "  知识库目录：~/.openclaw/workspace/knowledge/"
echo "  分析脚本：~/.openclaw/workspace/knowledge/.analysis/"
echo "  手动测试：python3 ~/.openclaw/workspace/knowledge/.analysis/run_analysis.py"
echo "=========================================="
