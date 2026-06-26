#!/usr/bin/env bash
# MediaCrawler 环境配置：创建 conda 环境、安装依赖与 Playwright
# 首次执行时会自动克隆 MediaCrawler（若不存在）
# 执行时将 {baseDir} 换为技能根目录：bash {baseDir}/scripts/setup_env.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MEDIACRAWLER_DIR="$(dirname "$SCRIPT_DIR")/MediaCrawler"

if [[ ! -d "$MEDIACRAWLER_DIR" ]]; then
  echo "MediaCrawler 目录不存在，正在从 GitHub 克隆..."
  bash "$SCRIPT_DIR/ensure_mediacrawler.sh"
fi

if [[ ! -d "$MEDIACRAWLER_DIR" ]]; then
  echo "Error: MediaCrawler not found at $MEDIACRAWLER_DIR"
  exit 1
fi

echo "Creating conda env media-cluster (Python 3.11)..."
conda create -n media-cluster python=3.11 -y

echo "Activating media-cluster and installing dependencies..."
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate media-cluster

cd "$MEDIACRAWLER_DIR"
pip install -r requirements.txt
pip install requests

echo "Installing Playwright browsers..."
playwright install

echo "Done. Use: conda activate media-cluster, then cd to MediaCrawler and run main.py"
