#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
daemon.py — 桌宠反馈守护进程（pet-feedback Skill 的核心）

后台持续运行，把"表情显示 + 语音反馈 + 触摸检测 + 亮屏控制"整合成一个进程：

  1. 表情显示：监控 OpenClaw 写入的状态 JSON 文件，按情绪/状态切换表情
  2. 语音反馈：状态里带 message 字段时，自动 TTS 合成并播放
  3. 触摸检测：触摸屏触摸/按键 → 唤醒屏幕、重置待机计时（循环结构后台持续监控）
  4. 亮屏控制：待机超时熄屏，触摸/状态更新自动亮屏（树莓派 vcgencmd 或软件黑屏）

状态文件 JSON 格式（OpenClaw 侧写入）：
  {"emotion": "happy", "phase": "talking", "message": "看到你笑我也很开心！"}

用法示例：
  python3 daemon.py --state-file /tmp/pet_state.json --fullscreen
  python3 daemon.py --state-file /tmp/pet_state.json --idle-timeout 120 \
                    --wake-cmd "vcgencmd display_power 1" --blank-cmd "vcgencmd display_power 0"

OpenClaw 侧更新状态（触发反馈）：
  echo '{"emotion":"happy","phase":"talking","message":"看到你笑我也很开心！"}' > /tmp/pet_state.json
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time

import pygame

from expressions import render
from tts import synth, play

DEFAULT_STATE = os.path.join(tempfile.gettempdir(), "pet_state.json")


def load_state(path):
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
        return {
            "emotion": str(data.get("emotion", "neutral")),
            "phase": str(data.get("phase", "idle")),
            "message": data.get("message"),
            "tts": bool(data.get("tts", True)),
        }
    except Exception:
        return {"emotion": "neutral", "phase": "idle", "message": None, "tts": True}


def run_cmd(cmd):
    if not cmd:
        return False
    try:
        rc = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        return rc.returncode == 0
    except Exception:
        return False


def do_voice(text):
    """合成并播放语音（子进程，避免阻塞显示循环）。"""
    outdir = os.path.join(tempfile.gettempdir(), "pet_audio")
    os.makedirs(outdir, exist_ok=True)
    out_path = os.path.join(outdir, "tts_%d.mp3" % int(time.time()))
    engine, err = synth(text, out_path, engine=os.environ.get("PET_TTS_ENGINE", "auto"))
    if engine is None:
        print("[pet-feedback] TTS 失败: %s" % err, flush=True)
        return
    ok, method = play(out_path)
    print("[pet-feedback] 语音: %s (%s, %s)" % (text[:30], engine, method if ok else "播放失败"), flush=True)


def main():
    ap = argparse.ArgumentParser(description="桌宠反馈守护进程")
    ap.add_argument("--state-file", default=os.environ.get("PET_STATE_FILE", DEFAULT_STATE),
                    help="状态 JSON 文件路径（OpenClaw 写入），默认 %s" % DEFAULT_STATE)
    ap.add_argument("--size", default=os.environ.get("PET_SCREEN_SIZE", "800x480"),
                    help="屏幕尺寸，默认 800x480")
    ap.add_argument("--fullscreen", action="store_true", help="全屏显示")
    ap.add_argument("--poll-interval", type=float, default=0.3, help="状态轮询间隔（秒）")
    ap.add_argument("--idle-timeout", type=int, default=0,
                    help="无触摸待机秒数（0=不熄屏）")
    ap.add_argument("--wake-cmd", default=os.environ.get("PET_WAKE_CMD", ""),
                    help="亮屏命令（树莓派: vcgencmd display_power 1）")
    ap.add_argument("--blank-cmd", default=os.environ.get("PET_BLANK_CMD", ""),
                    help="熄屏命令（树莓派: vcgencmd display_power 0）")
    ap.add_argument("--font", default=None, help="中文字体路径")
    ap.add_argument("--log", action="store_true", help="打印详细日志")
    args = ap.parse_args()

    try:
        w, h = (int(x) for x in args.size.lower().split("x"))
    except Exception:
        sys.stderr.write("尺寸格式错误：%s\n" % args.size)
        return 2

    pygame.init()
    if args.fullscreen:
        screen = pygame.display.set_mode((w, h), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((w, h))
    pygame.display.set_caption("Pet Feedback Daemon")

    state = load_state(args.state_file)
    last_mtime = None
    last_message = state["message"]
    screen_on = True
    last_interaction = time.time()

    print("[pet-feedback] 守护进程启动，监控 %s" % args.state_file, flush=True)
    running = True
    while running:
        # 1. 状态文件监控
        if os.path.exists(args.state_file):
            mtime = os.path.getmtime(args.state_file)
            if mtime != last_mtime:
                last_mtime = mtime
                state = load_state(args.state_file)
                if args.log:
                    print("[pet-feedback] 状态更新: %s" % json.dumps(state, ensure_ascii=False), flush=True)
                # 状态更新也算互动：亮屏
                if not screen_on:
                    if run_cmd(args.wake_cmd):
                        screen_on = True
                last_interaction = time.time()

                # 新消息 → 语音反馈
                if state.get("message") and state["message"] != last_message:
                    last_message = state["message"]
                    if state.get("tts", True):
                        do_voice(state["message"])

        # 2. 渲染
        render(screen, emotion=state["emotion"], phase=state["phase"],
               message=state["message"] if screen_on else None, font_path=args.font)
        pygame.display.flip()

        # 3. 触摸/按键检测 → 唤醒
        touched = False
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN, pygame.FINGERDOWN):
                touched = True
            elif ev.type == pygame.KEYDOWN and ev.key in (pygame.K_ESCAPE, pygame.K_q):
                running = False
        if touched:
            if not screen_on:
                if run_cmd(args.wake_cmd):
                    screen_on = True
                else:
                    screen_on = True  # 无命令时软件唤醒（重绘即可）
            last_interaction = time.time()

        # 4. 待机熄屏
        if args.idle_timeout > 0 and screen_on and \
                time.time() - last_interaction > args.idle_timeout:
            if run_cmd(args.blank_cmd):
                screen_on = False
            else:
                screen_on = False  # 软件黑屏（渲染 None 消息，仅剩深色背景）
            print("[pet-feedback] 待机熄屏", flush=True)

        time.sleep(args.poll_interval)

    pygame.quit()
    return 0


if __name__ == "__main__":
    sys.exit(main())
