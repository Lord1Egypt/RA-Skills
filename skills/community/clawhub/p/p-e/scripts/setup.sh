#!/bin/bash
# P-E skill dependency setup
# 安装图片提取→Excel所需的Python依赖
set -e

echo "Installing P-E dependencies..."
pip3 install --user openpyxl Pillow
echo "✓ Done. P-E skill is ready."
