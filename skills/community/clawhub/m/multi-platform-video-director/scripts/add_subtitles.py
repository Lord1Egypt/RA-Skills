#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""给视频叠加字幕/标题（drawtext 烧录，中文字体自动探测）。

两种模式：
  1) 标题模式：--title "文字" 居中大字（海报/片头标题），可重复叠加多个
  2) 对白模式：--subs "开始-结束|文本" 底部字幕（对白/语气词/旁白），可重复多条

用法:
  # 标题：片头大字 + 底部小字
  python add_subtitles.py in.mp4 \
      --title "蛋糕店奇遇" --title-pos center --title-size 56 \
      --subs "1.5-4.0|哇——好漂亮的蛋糕店！" \
      --subs "4.8-8.5|嗯…要不要进去呢？" \
      --out out.mp4

  # 纯字幕
  python add_subtitles.py in.mp4 --subs "0.5-4.0|大家好，今天讲一个故事" --out out.mp4

参数:
  --title        标题文本，可重复；居中大字
  --title-size   标题字号（默认 48）
  --title-pos    标题位置：center（默认）/ top / bottom
  --subs         对白字幕 '开始秒-结束秒|文本'，可重复；底部小字带半透明黑底
  --sub-size     对白字号（默认 34）
  --color        文字颜色（默认 white；支持 white/yellow/red/0xRRGGBB）
  --font         字体文件路径（默认自动探测微软雅黑/黑体/宋体）
  --out          输出文件（默认 输入_带字幕.mp4）

依赖:
  imageio-ffmpeg（自带 ffmpeg，drawtext filter 依赖 libfreetype，官方构建已内置）
"""
import argparse
import os
import subprocess
import sys

import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

# Windows 常见中文字体（按优先级）
FONT_CANDIDATES = [
    r"C:/Windows/Fonts/msyh.ttc",    # 微软雅黑
    r"C:/Windows/Fonts/msyhbd.ttc",  # 微软雅黑 Bold
    r"C:/Windows/Fonts/simhei.ttf",  # 黑体
    r"C:/Windows/Fonts/simsun.ttc",  # 宋体
    r"C:/Windows/Fonts/Deng.ttf",    # 等线
]
# 非 Windows 兜底
FONT_CANDIDATES_LINUX = [
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",   # 文泉驿正黑
    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc", # 文泉驿微米黑
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
]


def find_font() -> str:
    cands = FONT_CANDIDATES + (FONT_CANDIDATES_LINUX if os.name != "nt" else [])
    for p in cands:
        if os.path.isfile(p):
            return p
    return FONT_CANDIDATES[0]  # 找不到也返回默认，让 ffmpeg 报错提示


def esc(value: str) -> str:
    """转义 filter 参数中的特殊字符。"""
    return value.replace("\\", "\\\\").replace("'", "\\'").replace(":", "\\:")


def parse_subs(arg: str):
    """解析 '开始-结束|文本' → (start, end, text)。"""
    if "|" not in arg or "-" not in arg.split("|", 1)[0]:
        sys.exit(f"--subs 格式应为 开始秒-结束秒|文本，收到: {arg}")
    time_part, text = arg.split("|", 1)
    try:
        start, end = time_part.split("-", 1)
        start, end = float(start), float(end)
    except ValueError:
        sys.exit(f"--subs 时间格式错误（应为 开始-结束 秒）: {time_part}")
    if end <= start:
        sys.exit(f"--subs 结束时间必须大于开始时间: {arg}")
    return start, end, text


def color_arg(color: str) -> str:
    if color.startswith("0x") or color.startswith("0X"):
        return color[2:]  # drawtext 用 RRGGBB 或 AARRGGBB
    return {"white": "white", "yellow": "yellow", "red": "red"}.get(color, color)


def build_filters(titles, subs, font, title_size, title_pos, sub_size, color):
    fc = []
    # 标题（居中大字，可多个纵向排列）
    ty = {"center": "h/2", "top": "h*0.12", "bottom": "h*0.85"}[title_pos]
    for i, t in enumerate(titles):
        yoff = i * (title_size + 12)
        fc.append(
            f"drawtext=fontfile='{esc(font)}':text='{esc(t)}':"
            f"fontsize={title_size}:fontcolor={color_arg(color)}:"
            f"x=(w-text_w)/2:y=({ty})+{yoff}:"
            f"shadowcolor=black@0.6:shadowx=2:shadowy=2"
        )
    # 对白（底部，半透明黑底，按时间轴显示）
    for start, end, text in subs:
        fc.append(
            f"drawtext=fontfile='{esc(font)}':text='{esc(text)}':"
            f"fontsize={sub_size}:fontcolor={color_arg(color)}:"
            f"box=1:boxcolor=black@0.45:boxborderw=12:"
            f"x=(w-text_w)/2:y=h-{sub_size + 60}:"
            f"enable='between(t,{start},{end})'"
        )
    return fc


def main() -> None:
    ap = argparse.ArgumentParser(description="burn subtitles/titles into video")
    ap.add_argument("video", help="输入视频")
    ap.add_argument("--title", action="append", default=[], help="标题文字（可重复）")
    ap.add_argument("--title-size", type=int, default=48)
    ap.add_argument("--title-pos", default="center", choices=["center", "top", "bottom"])
    ap.add_argument("--subs", action="append", default=[], help="对白 '开始-结束|文本'（可重复）")
    ap.add_argument("--sub-size", type=int, default=34)
    ap.add_argument("--color", default="white", help="white/yellow/red/0xRRGGBB")
    ap.add_argument("--font", default="")
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    if not os.path.isfile(args.video):
        sys.exit(f"视频文件不存在: {args.video}")
    if not args.title and not args.subs:
        sys.exit("至少需要 --title 或 --subs 之一")
    font = args.font or find_font()
    subs = [parse_subs(s) for s in args.subs]
    out = args.out or f"{os.path.splitext(args.video)[0]}_带字幕.mp4"

    filters = build_filters(args.title, subs, font,
                            args.title_size, args.title_pos, args.sub_size, args.color)
    if not filters:
        sys.exit("没有可叠加的字幕内容")

    cmd = [FFMPEG, "-y", "-i", args.video,
           "-vf", ",".join(filters),
           "-c:a", "copy",
           "-c:v", "libx264", "-preset", "medium", "-crf", "20",
           "-movflags", "+faststart",
           out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("FFMPEG_ERROR:\n", r.stderr[-2500:])
        sys.exit(1)
    print(f"OK subtitles burned: {out} ({len(args.title)} 标题, {len(subs)} 条对白)")


if __name__ == "__main__":
    main()
