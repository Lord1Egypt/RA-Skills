#!/bin/sh
# pan-downloader 下载后处理链模板（开箱即用骨架）
# 用法：在 config.json 的 http.on_complete_hook 填：
#   bash "<此文件绝对路径>" "{target}" "{drive}" "{engine}" "{report}"
# 占位符由 pan 自动展开；本脚本默认"干跑预览"（AUTO=0），确认无误后改 AUTO=1 生效。
# 目标：解压常见压缩包、媒体重命名入库 Jellyfin/Emby/Plex 的本地扫描命令占位。
AUTO=0
TARGET="$1"
DRIVE="$2"
ENGINE="$3"
REPORT="$4"

if [ -z "$TARGET" ] || [ ! -d "$TARGET" ]; then
  echo "[post] 用法: post_media.sh <target> [drive] [engine] [report]"; exit 2
fi
echo "[post] target=$TARGET drive=$DRIVE engine=$ENGINE report=$REPORT"

# 1) 自动解压常见归档（保留原文件）
if command -v unzip >/dev/null 2>&1; then
  for f in "$TARGET"/*.zip; do
    [ -e "$f" ] || continue
    echo "[post] 发现 ZIP: $(basename "$f")"
    [ "$AUTO" = 1 ] && unzip -o "$f" -d "$TARGET" || echo "        (AUTO=0 跳过)"
  done
fi
if command -v tar >/dev/null 2>&1; then
  for f in "$TARGET"/*.tar.gz "$TARGET"/*.tgz; do
    [ -e "$f" ] || continue
    echo "[post] 发现 TGZ: $(basename "$f")"
    [ "$AUTO" = 1 ] && tar -xzf "$f" -C "$TARGET" || echo "        (AUTO=0 跳过)"
  done
fi

# 2) Jellyfin/Emby/Plex 媒体库扫描占位（改成你的服务地址即可）
# JELLYFIN_URL="http://127.0.0.1:8096"
# JELLYFIN_KEY="你的APIKey"
# [ "$AUTO" = 1 ] && [ -n "$JELLYFIN_URL" ] && curl -s -X POST "$JELLYFIN_URL/Library/Refresh?api_key=$JELLYFIN_KEY" || true

# 3) 重命名/刮削占位：这里放 tinyMediaManager / filebot 命令
# [ "$AUTO" = 1 ] && filebot -rename "$TARGET" --db TheMovieDB --format "..." 

echo "[post] 结束（AUTO=$AUTO，实际入库请把脚本顶部 AUTO 改成 1）"
