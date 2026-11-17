#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
show_expression.py — 桌宠表情单次显示脚本（pet-feedback Skill）

三种用法：
  1. 单次显示：python3 show_expression.py --emotion happy --phase talking --message "你好"
  2. 跟随状态文件：python3 show_expression.py --state-file /tmp/pet_state.json
     （监控 OpenClaw 写入的状态 JSON，自动切换表情，适合演示）
  3. 无头截图：python3 show_expression.py --emotion sad --snapshot preview.png
     （SDL dummy 驱动，不弹窗，用于测试/生成预览图）

状态文件 JSON 格式（与 daemon.py 一致）：
  {"emotion": "happy", "phase": "talking", "message": "看到你笑我也很开心！"}

按键：ESC / q 退出。
"""

import argparse
import json
import os
import sys
import tempfile
import time

os.environ.setdefault("SDL_VIDEODRIVER", os.environ.get("SDL_VIDEODRIVER", ""))  # 允许外部覆盖

import pygame

from expressions import render


def load_state(path):
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
        emotion = data.get("emotion", "neutral")
        phase = data.get("phase", "idle")
        message = data.get("message")
        return emotion, phase, message
    except Exception:
        return "neutral", "idle", None


def main():
    ap = argparse.ArgumentParser(description="桌宠表情显示（单次/跟随状态文件）")
    ap.add_argument("--emotion", default="happy", help="情绪（happy/sad/angry/...）")
    ap.add_argument("--phase", default="talking", help="状态（idle/listening/thinking/talking/sleeping）")
    ap.add_argument("--message", default=None, help="要显示的消息文字")
    ap.add_argument("--state-file", default=None, help="监控状态 JSON 文件（OpenClaw 写入）")
    ap.add_argument("--size", default=os.environ.get("PET_SCREEN_SIZE", "800x480"),
                    help="窗口/画布尺寸，默认 800x480（7 寸屏常用）")
    ap.add_argument("--fullscreen", action="store_true", help="全屏显示")
    ap.add_argument("--duration", type=float, default=0, help="显示时长秒数（0=持续直到退出）")
    ap.add_argument("--snapshot", default=None, help="渲染一帧保存为 PNG 后退出（无头测试）")
    ap.add_argument("--font", default=None, help="中文字体路径（默认自动查找）")
    ap.add_argument("--poll-interval", type=float, default=0.3, help="状态文件轮询间隔（秒）")
    args = ap.parse_args()

    try:
        w, h = (int(x) for x in args.size.lower().split("x"))
    except Exception:
        sys.stderr.write("尺寸格式错误：%s（应为 宽x高）\n" % args.size)
        return 2

    if args.snapshot:
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        pygame.init()
        screen = pygame.Surface((w, h))
        emotion, phase, message = load_state(args.state_file) if args.state_file else (
            args.emotion, args.phase, args.message)
        render(screen, emotion=emotion, phase=phase, message=message, font_path=args.font)
        pygame.image.save(screen, args.snapshot)
        print(json.dumps({"status": "ok", "snapshot": args.snapshot,
                          "emotion": emotion, "phase": phase}, ensure_ascii=False))
        return 0

    pygame.init()
    if args.fullscreen:
        screen = pygame.display.set_mode((w, h), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((w, h))
    pygame.display.set_caption("Pet Feedback")

    emotion, phase, message = args.emotion, args.phase, args.message
    last_mtime = None
    start = time.time()
    running = True
    while running:
        # 状态文件监控
        if args.state_file and os.path.exists(args.state_file):
            mtime = os.path.getmtime(args.state_file)
            if mtime != last_mtime:
                last_mtime = mtime
                emotion, phase, message = load_state(args.state_file)

        render(screen, emotion=emotion, phase=phase, message=message, font_path=args.font)
        pygame.display.flip()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.KEYDOWN and ev.key in (pygame.K_ESCAPE, pygame.K_q):
                running = False

        if args.duration > 0 and time.time() - start > args.duration:
            running = False
        time.sleep(args.poll_interval)

    pygame.quit()
    return 0


if __name__ == "__main__":
    sys.exit(main())
