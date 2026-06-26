#!/bin/bash

# =========================
# OpenClaw Gmail Sync Runner
# =========================

# 进入目录
cd "$(dirname "$0")"

# 安装依赖（只第一次需要）
pip install python-dateutil html2text >/dev/null 2>&1

# 启动（main.py 需在直接执行时调用 run()，见文件末尾 __main__）
echo "🚀 mail IMAP Sync 启动..."
python3 main.py
