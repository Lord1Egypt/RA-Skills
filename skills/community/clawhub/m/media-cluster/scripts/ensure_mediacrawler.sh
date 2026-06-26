#!/usr/bin/env bash
# 首次执行时从 GitHub 克隆 MediaCrawler 到技能目录下
# 执行时将 {baseDir} 换为技能根目录：bash {baseDir}/scripts/ensure_mediacrawler.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(dirname "$SCRIPT_DIR")"
MEDIACRAWLER_DIR="$SKILL_ROOT/MediaCrawler"
REPO_URL="https://github.com/NanmiCoder/MediaCrawler.git"

if [[ -d "$MEDIACRAWLER_DIR" ]]; then
  echo "MediaCrawler 已存在: $MEDIACRAWLER_DIR"
  exit 0
fi

echo "正在克隆 MediaCrawler 到 $MEDIACRAWLER_DIR ..."
git clone "$REPO_URL" "$MEDIACRAWLER_DIR"
echo "MediaCrawler 下载完成。"
