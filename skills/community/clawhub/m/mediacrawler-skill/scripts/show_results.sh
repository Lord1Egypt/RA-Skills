#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${PROJECT_PATH:-$HOME/MediaCrawler}"
PROJECT_DIR="${PROJECT_DIR/#\~/$HOME}"
DATA_DIR="$PROJECT_DIR/data"

if [ ! -d "$DATA_DIR" ]; then
  echo "未找到结果目录: $DATA_DIR"
  echo "请先运行爬取任务。"
  exit 1
fi

echo "MediaCrawler 结果文件："
find "$DATA_DIR" -maxdepth 3 -type f | sort | sed -n '1,200p'
