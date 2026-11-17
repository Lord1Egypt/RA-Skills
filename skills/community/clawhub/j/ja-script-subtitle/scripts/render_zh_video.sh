#!/usr/bin/env bash
# Step 4 —— 把中文字幕烧录进竖屏视频（纯色背景 + 原声）
#
# 用法:
#   bash render_zh_video.sh <zh.srt> <audio> <out.mp4> [fontsize]
#
# 说明:
#   * 背景 720x1280 竖屏深色 0x141418，15fps，纯色故码率极低
#   * PlayResX/PlayResY 必须显式设置 —— 否则 libass 用默认 384x288 缩放，
#     字号会被放大、字幕换行错位（本项目踩过）
#   * 本环境 ffmpeg 无 libx264，H.264 只能用 libopenh264
#   * 字体 Noto Sans CJK SC（fc-list :lang=zh 可查）
#   * srt 路径避免冒号；相对路径最稳（先 cd 到 srt 所在目录）
set -euo pipefail

SRT="$1"; AUDIO="$2"; OUT="$3"; FS="${4:-36}"

ffmpeg -y -f lavfi -i "color=c=0x141418:s=720x1280:r=15" -i "$AUDIO" -shortest \
  -vf "subtitles=${SRT}:force_style='PlayResX=720,PlayResY=1280,Fontname=Noto Sans CJK SC,Fontsize=${FS},PrimaryColour=&H00FFFFFF,Outline=2,OutlineColour=&H00000000,Shadow=0,MarginV=60,Alignment=2',format=yuv420p" \
  -c:v libopenh264 -b:v 400k -c:a aac -b:a 192k "$OUT"

echo "OK -> $OUT"
ffprobe -v error -show_entries format=duration,size -show_entries stream=codec_name,width,height -of default=noprint_wrappers=1 "$OUT"
