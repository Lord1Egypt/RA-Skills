#!/usr/bin/env bash
# setup.sh — init_user Skill 安装脚本
# 用法：bash setup.sh
set -e

cd "$(dirname "$0")"

echo "[1/3] 安装 Python 依赖..."
pip3 install -r requirements.txt --break-system-packages 2>/dev/null || pip3 install -r requirements.txt

echo "[2/3] 检查 .env 配置..."
if [ ! -f .env ]; then
  cp env-example.txt .env
  echo "  已从 env-example.txt 生成 .env，请编辑填入真实的 GITEA_ADMIN_TOKEN！"
else
  echo "  .env 已存在，跳过。"
fi

echo "[3/3] 自检：验证脚本可运行..."
python3 scripts/init_user.py --check --open_id setup_selftest || true

echo ""
echo "安装完成。请确认 .env 中的 GITEA_URL 和 GITEA_ADMIN_TOKEN 正确。"
echo "测试命令："
echo "  python3 scripts/init_user.py --check --open_id webchat_test"
