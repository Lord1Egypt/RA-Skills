#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""多段落背景音乐：按情绪规划拼接（默认 明快→轻柔→安静→明快），段落间交叉淡变，输出立体声 WAV。

用法:
  python compose_full_track.py <输出.wav> [--total 秒] [--plan "bright:5.4,gentle:4.8,calm:5.4,bright:4.8"]

参数:
  --total   总时长（秒）。默认按 plan 各段之和（含交叉淡变，实际略短），
            指定后末尾截断到精确总时长，方便对齐视频
  --plan    段落方案，逗号分隔 风格:秒数。风格可选 bright / gentle / calm
            默认「明快→轻柔→安静→明快」，适合发现→犹豫→行动→满足的叙事节奏
  --crossfade  段落交叉淡变时长（秒，默认 0.4）

示例:
  # 4 镜头故事片：2 明快(发现) → 1 轻柔(犹豫) → 3 安静(进店) → 4 明快(满足)
  python compose_full_track.py bgm_full.wav \
      --plan "bright:5.4,gentle:4.8,calm:5.4,bright:4.8" --total 18.7

  # 2 镜头：悬念→激昂
  python compose_full_track.py bgm_2.wav --plan "calm:5.0,bright:5.0"
"""
import argparse
import sys
import wave
import numpy as np

SR = 44100


def note(freq, dur, amp=0.5, attack=0.02):
    n = int(SR * dur)
    t = np.arange(n) / SR
    env = np.exp(-t * 3.2)
    env[: int(attack * SR)] *= np.linspace(0, 1, int(attack * SR))
    wave_ = (np.sin(2 * np.pi * freq * t)
             + 0.35 * np.sin(2 * np.pi * freq * 2 * t)
             + 0.12 * np.sin(2 * np.pi * freq * 3 * t))
    return amp * env * wave_


def chord_arp(notes, dur, amp):
    return np.concatenate([note(f, dur, amp) for f in notes])


def segment(chords, dur_per_note, amps, sec):
    parts = []
    total = 0.0
    i = 0
    while total < sec:
        ch = chords[i % len(chords)]
        parts.append(chord_arp(ch, dur_per_note, amps[i % len(amps)]))
        total += dur_per_note * len(ch)
        i += 1
    return np.concatenate(parts)[: int(SR * sec)]


# 三套和弦进行（与技能内 compose_music.py 一致）
BRIGHT = [
    [261.63, 329.63, 392.00, 523.25],  # C
    [196.00, 246.94, 293.66, 392.00],  # G
    [220.00, 261.63, 329.63, 440.00],  # Am
    [174.61, 220.00, 261.63, 349.23],  # F
]
GENTLE = [
    [261.63, 329.63, 392.00, 523.25],  # Cmaj7
    [220.00, 261.63, 329.63, 440.00],  # Am7
    [174.61, 220.00, 261.63, 349.23],  # Fmaj7
]
CALM = [
    [174.61, 220.00, 261.63, 349.23],  # Fmaj7
    [261.63, 329.63, 392.00, 523.25],  # Cmaj7
    [220.00, 261.63, 329.63, 440.00],  # Am7
]
STYLES = {"bright": (BRIGHT, 0.34, [0.44, 0.42, 0.40, 0.40]),
          "gentle": (GENTLE, 0.46, [0.42, 0.38, 0.36]),
          "calm":   (CALM,   0.58, [0.34, 0.32, 0.30])}


def crossfade(a, b, dur):
    n = int(SR * dur)
    n = min(n, len(a), len(b))
    fade = np.linspace(0, 1, n)
    a[-n:] *= (1 - fade)
    b[:n] *= fade
    return np.concatenate([a, b[n:]])


def main() -> None:
    ap = argparse.ArgumentParser(description="compose multi-mood background music track")
    ap.add_argument("out", nargs="?", default="full_track.wav")
    ap.add_argument("--total", type=float, default=0.0, help="精确总时长（秒），默认按 plan 自动")
    ap.add_argument("--plan", default="bright:5.4,gentle:4.8,calm:5.4,bright:4.8",
                    help="段落方案 风格:秒数，逗号分隔")
    ap.add_argument("--crossfade", type=float, default=0.4, help="段落交叉淡变秒数")
    args = ap.parse_args()

    plan = []
    for item in args.plan.split(","):
        item = item.strip()
        if ":" not in item:
            sys.exit(f"--plan 格式应为 风格:秒数，收到: {item}")
        style, sec = item.rsplit(":", 1)
        style, sec = style.strip(), float(sec)
        if style not in STYLES:
            sys.exit(f"未知风格: {style}（可选: bright/gentle/calm）")
        plan.append((style, sec))

    segs = []
    for style, sec in plan:
        chords, dur, amps = STYLES[style]
        segs.append(segment(chords, dur, amps, sec))

    mono = segs[0]
    for s in segs[1:]:
        mono = crossfade(mono, s, args.crossfade)

    # 精确总时长截断（指定 --total 时）
    if args.total > 0:
        target = int(SR * args.total)
        mono = mono[:target]
        if len(mono) < target:  # 各段太短时补零到总时长
            mono = np.concatenate([mono, np.zeros(target - len(mono))])

    # 立体声：右声道延迟 15ms 营造空间感
    delay = int(SR * 0.015)
    right = np.concatenate([np.zeros(delay), mono])[: len(mono)]
    left = mono

    # 整体淡入淡出
    n = len(mono)
    win = np.ones(n)
    fi, fo = int(SR * 0.8), int(SR * 1.2)
    win[:fi] = np.linspace(0, 1, fi)
    win[-fo:] = np.linspace(1, 0, fo)
    left *= win
    right *= win

    peak = max(np.abs(left).max(), np.abs(right).max())
    if peak > 0.95:
        left *= 0.95 / peak
        right *= 0.95 / peak

    stereo = np.stack([left, right], axis=1)
    pcm = (stereo * 32767).astype(np.int16)
    with wave.open(args.out, "wb") as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(SR)
        f.writeframes(pcm.tobytes())
    print(f"OK full track: {args.out} ({n / SR:.2f}s, plan={args.plan})")


if __name__ == "__main__":
    main()
