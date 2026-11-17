#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""多模态生成提示词构造助手。

把简略需求扩写为结构化、可用于 ImageGen/VideoGen 的优化提示词。

用法:
  python prompt_build.py "一只在看书的小猫" --style 水彩 --aspect 1:1 [--mode image|video]
"""
import argparse
import json
import sys

STYLE_BANK = {
    "写实": "photorealistic, highly detailed, 8k, cinematic lighting",
    "水彩": "watercolor painting style, soft brush, paper texture, pastel",
    "卡通": "flat cartoon style, bold outlines, vibrant colors",
    "赛博朋克": "cyberpunk, neon lights, futuristic city, high contrast",
    "极简": "minimalist, clean lines, flat color, negative space",
}


def build(prompt, style, aspect, mode):
    s = STYLE_BANK.get(style, style or "")
    if mode == "video":
        base = (f"视频分镜：{prompt}。"
                f"运镜平滑自然，时长 5 秒，电影级画质。")
    else:
        base = f"{prompt}。"
    if s:
        base += f" 风格：{s}。"
    if aspect:
        base += f" 画面比例 {aspect}。"
    return base


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt", help="简略需求")
    ap.add_argument("--style", default="")
    ap.add_argument("--aspect", default="")
    ap.add_argument("--mode", default="image", choices=["image", "video"])
    args = ap.parse_args()

    out = build(args.prompt, args.style, args.aspect, args.mode)
    print("✅ 生成提示词：")
    print(out)
    print("__JSON__" + json.dumps({"mode": args.mode, "prompt": out},
                                   ensure_ascii=False))


if __name__ == "__main__":
    main()
