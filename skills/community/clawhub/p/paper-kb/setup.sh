#!/bin/bash
set -e
echo "=== paper-kb 安装 ==="

echo "[1/2] 安装 Python 依赖..."
pip install -r requirements.txt --quiet

echo "[2/2] 创建 .env 文件..."
if [ ! -f .env ]; then
  cp env-example.txt .env
  echo "  已创建 .env，三个变量已预填，可直接使用"
else
  echo "  .env 已存在，跳过"
fi

echo "=== 安装完成 ==="
