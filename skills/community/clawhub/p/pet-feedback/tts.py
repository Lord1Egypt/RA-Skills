#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tts.py — 桌宠语音反馈模块（pet-feedback Skill）

职责：把大模型生成的文本回复转成语音并播放（通过主机喇叭）。
引擎按优先级自动回退：edge-tts（网络，音质最好）→ espeak-ng（本地离线）→ gtts（网络）。
播放：优先 pygame.mixer（本 Skill 本来就依赖 pygame），回退 ffplay/aplay/winsound。

用法示例：
  python3 tts.py --text "看到你笑我也很开心！" --play
  python3 tts.py --text "该起来活动一下啦" --engine espeak-ng --play   # 离线
  python3 tts.py --text "你好" --voice zh-CN-YunxiNeural --outdir audio --no-play
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone, timedelta

CST = timezone(timedelta(hours=8), "CST")
DEFAULT_VOICE = "zh-CN-XiaoxiaoNeural"  # 晓晓（女声，自然）


def now_str():
    return datetime.now(CST).strftime("%Y-%m-%dT%H:%M:%S%z")


def which(name):
    return shutil.which(name) is not None


# ---------- 合成 ----------

def synth_edge_tts(text, out_path, voice):
    if not which("edge-tts"):
        return None, "edge-tts CLI not found (pip install edge-tts)"
    cmd = ["edge-tts", "--voice", voice, "--text", text, "--write-media", out_path]
    rc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if rc.returncode != 0 or not os.path.exists(out_path):
        return None, (rc.stderr or "").strip()[:200]
    return "edge-tts", ""


def synth_espeak(text, out_path):
    if not which("espeak-ng"):
        return None, "espeak-ng not found (sudo apt install espeak-ng)"
    cmd = ["espeak-ng", "-v", "zh", "-w", out_path, text]
    rc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if rc.returncode != 0 or not os.path.exists(out_path):
        return None, (rc.stderr or "").strip()[:200]
    return "espeak-ng", ""


def synth_gtts(text, out_path):
    try:
        from gtts import gTTS
    except ImportError:
        return None, "gtts not installed (pip install gtts)"
    try:
        gTTS(text=text, lang="zh-CN").save(out_path)
    except Exception as e:
        return None, str(e)[:200]
    return "gtts", ""


def synth(text, out_path, engine="auto", voice=DEFAULT_VOICE):
    order = ["edge-tts", "espeak-ng", "gtts"] if engine == "auto" else [engine]
    errors = []
    for eng in order:
        if eng == "edge-tts":
            ok, err = synth_edge_tts(text, out_path, voice)
        elif eng == "espeak-ng":
            ok, err = synth_espeak(text, out_path)
        elif eng == "gtts":
            ok, err = synth_gtts(text, out_path)
        else:
            ok, err = None, "unknown engine: %s" % eng
        if ok:
            return ok, ""
        errors.append("%s: %s" % (eng, err))
    return None, " | ".join(errors)


# ---------- 播放 ----------

def play_pygame(path):
    try:
        import pygame
        pygame.mixer.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)
        return True, ""
    except Exception as e:
        return False, str(e)[:200]


def play_cmd(path):
    if path.endswith(".wav") and which("aplay"):
        rc = subprocess.run(["aplay", "-q", path], timeout=300)
        return rc.returncode == 0, ""
    if which("ffplay"):
        rc = subprocess.run(["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", path], timeout=300)
        return rc.returncode == 0, ""
    if which("mpv"):
        rc = subprocess.run(["mpv", "--no-terminal", "--really-quiet", path], timeout=300)
        return rc.returncode == 0, ""
    if os.name == "nt" and path.endswith(".wav"):
        import winsound
        winsound.PlaySound(path, winsound.SND_FILENAME)
        return True, ""
    return False, "no player available (aplay/ffplay/mpv/pygame)"


def play(path):
    ok, err = play_pygame(path)
    if ok:
        return True, "pygame.mixer"
    ok, err = play_cmd(path)
    if ok:
        return True, "cmd"
    return False, err


def main():
    ap = argparse.ArgumentParser(description="桌宠语音反馈（TTS 合成 + 播放）")
    ap.add_argument("--text", default=None, help="要合成的文本")
    ap.add_argument("--text-file", default=None, help="从文件读取文本（UTF-8）")
    ap.add_argument("--engine", default=os.environ.get("PET_TTS_ENGINE", "auto"),
                    choices=["auto", "edge-tts", "espeak-ng", "gtts"], help="合成引擎")
    ap.add_argument("--voice", default=os.environ.get("PET_TTS_VOICE", DEFAULT_VOICE),
                    help="edge-tts 音色，默认 %s" % DEFAULT_VOICE)
    ap.add_argument("--outdir", default="audio", help="音频输出目录")
    ap.add_argument("--filename", default=None, help="输出文件名（不含扩展名）")
    ap.add_argument("--play", dest="do_play", action="store_true", help="合成后播放")
    ap.add_argument("--no-play", dest="do_play", action="store_false", help="只合成不播放")
    ap.set_defaults(do_play=False)
    args = ap.parse_args()

    if args.text_file:
        with open(args.text_file, "r", encoding="utf-8-sig") as f:
            text = f.read().strip()
    else:
        text = (args.text or "").strip()
    if not text:
        print(json.dumps({"status": "error", "message": "文本为空"}, ensure_ascii=False))
        return 1

    os.makedirs(args.outdir, exist_ok=True)
    name = args.filename or datetime.now(CST).strftime("%Y%m%d_%H%M%S")
    out_path = os.path.join(args.outdir, name + ".mp3")

    engine, err = synth(text, out_path, engine=args.engine, voice=args.voice)
    if engine is None:
        print(json.dumps({"status": "error", "message": err}, ensure_ascii=False))
        return 1

    result = {"status": "ok", "engine": engine, "audio_path": out_path,
              "timestamp": now_str(), "played": False}
    if args.do_play:
        ok, method = play(out_path)
        if not ok:
            print(json.dumps({"status": "error", "message": "播放失败: %s" % method}, ensure_ascii=False))
            return 1
        result["played"] = True
        result["play_method"] = method
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
