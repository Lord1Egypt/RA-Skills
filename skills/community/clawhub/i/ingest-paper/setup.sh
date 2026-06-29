#!/usr/bin/env bash
# setup.sh — ingest_paper Skill 安装脚本（全类型版）
set -e
cd "$(dirname "$0")"

echo "[1/3] 安装 Python 依赖（含 pymupdf/python-docx/openpyxl，可能需要1-2分钟）..."
pip3 install -r requirements.txt --break-system-packages 2>/dev/null || pip3 install -r requirements.txt

echo "[2/3] 检查 .env 配置..."
if [ ! -f .env ]; then
  cp env-example.txt .env
  echo "  已生成 .env，请编辑填入真实的 GITEA_ADMIN_TOKEN！"
else
  echo "  .env 已存在，跳过。"
fi

echo "[3/3] 自检依赖..."
mkdir -p /tmp/paperkb
python3 -c "import fitz, docx, openpyxl; print('  pymupdf / python-docx / openpyxl 均 OK')" || echo "  依赖自检失败，请检查安装"

echo ""
echo "安装完成。测试命令："
echo '  python3 scripts/fetch_arxiv.py --url "https://arxiv.org/abs/1706.03762"'
