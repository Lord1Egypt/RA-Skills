# -*- coding: utf-8 -*-
"""合成一段温暖治愈系背景音乐（钢琴琶音风格），输出 WAV。"""
import wave
import sys
import numpy as np

SR = 44100


def note(freq, dur, amp=0.5, attack=0.02):
    """单音符：正弦基频 + 2 次谐波，指数衰减包络，带轻微起音。"""
    n = int(SR * dur)
    t = np.arange(n) / SR
    # 钢琴感：基频 + 谐波，指数衰减
    env = np.exp(-t * 3.2)
    env[: int(attack * SR)] *= np.linspace(0, 1, int(attack * SR))
    wave_ = (np.sin(2 * np.pi * freq * t)
             + 0.35 * np.sin(2 * np.pi * freq * 2 * t)
             + 0.12 * np.sin(2 * np.pi * freq * 3 * t))
    return amp * env * wave_


def chord_arp(notes, dur_per_note, amp=0.5):
    """把一个和弦的音符依次琶音，返回单声道片段。"""
    seg = np.concatenate([note(f, dur_per_note, amp) for f in notes])
    return seg


def main():
    total_sec = float(sys.argv[1]) if len(sys.argv) > 1 else 5.5
    out_path = sys.argv[2] if len(sys.argv) > 2 else "bgm.wav"
    style = sys.argv[3] if len(sys.argv) > 3 else "gentle"

    # 三套和弦进行与节奏
    if style == "bright":  # 明快：C - G - Am - F，更快更亮
        chords = [
            [261.63, 329.63, 392.00, 523.25],  # C
            [196.00, 246.94, 293.66, 392.00],  # G
            [220.00, 261.63, 329.63, 440.00],  # Am
            [174.61, 220.00, 261.63, 349.23],  # F
        ]
        dur_per_note, amps = 0.34, [0.44, 0.42, 0.40, 0.40]
    elif style == "calm":  # 安静：Fmaj7 - Cmaj7 - Am7，更慢更轻
        chords = [
            [174.61, 220.00, 261.63, 349.23],  # Fmaj7
            [261.63, 329.63, 392.00, 523.25],  # Cmaj7
            [220.00, 261.63, 329.63, 440.00],  # Am7
        ]
        dur_per_note, amps = 0.58, [0.34, 0.32, 0.30]
    else:  # gentle（默认）：Cmaj7 - Am7 - Fmaj7
        chords = [
            [261.63, 329.63, 392.00, 523.25],  # Cmaj7
            [220.00, 261.63, 329.63, 440.00],  # Am7
            [174.61, 220.00, 261.63, 349.23],  # Fmaj7
        ]
        dur_per_note, amps = 0.46, [0.42, 0.38, 0.36]

    # 分配时间：和弦轮转铺满 total_sec
    rounds = max(1, int(total_sec / (4 * dur_per_note * len(chords))) + 1)
    parts = []
    for i in range(rounds):
        for j, ch in enumerate(chords):
            parts.append(chord_arp(ch, dur_per_note, amps[j % len(amps)]))
    mono = np.concatenate(parts)[: int(SR * total_sec)]

    # 立体声：右声道延迟 15ms 制造轻微空间感
    delay = int(SR * 0.015)
    right = np.concatenate([np.zeros(delay), mono])[: len(mono)]
    left = mono

    # 整体淡入淡出（1s 淡入 / 1.5s 淡出）
    n = len(mono)
    fade_in = int(SR * 1.0)
    fade_out = int(SR * 1.5)
    win = np.ones(n)
    win[:fade_in] = np.linspace(0, 1, fade_in)
    win[-fade_out:] = np.linspace(1, 0, fade_out)
    left *= win
    right *= win

    # 归一化防削波
    peak = max(np.abs(left).max(), np.abs(right).max())
    if peak > 0.98:
        left *= 0.98 / peak
        right *= 0.98 / peak

    stereo = np.stack([left, right], axis=1)
    pcm = (stereo * 32767).astype(np.int16)

    with wave.open(out_path, "wb") as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(SR)
        f.writeframes(pcm.tobytes())

    print(f"OK music: {out_path} ({total_sec}s, {n/SR:.2f}s actual)")


if __name__ == "__main__":
    main()
