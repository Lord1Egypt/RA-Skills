#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用 edge-tts（晓晓中文女声）生成语气词/台词配音，带情绪语速/音调调节。

用法:
  # 快捷模式：默认 4 句剧情台词（发现→犹豫→进店→满足）
  python gen_voice_lines.py <输出目录>

  # 自定义台词模式：可重复 --voice，格式 文件名:台词[:rate][:pitch]
  python gen_voice_lines.py <输出目录> \
      --voice "v1:哇——好漂亮的蛋糕店！:+20%:+8Hz" \
      --voice "v2:嗯…要不要进去呢？:-15%:-3Hz" \
      --voice "v3:草莓蛋糕到手啦！:+10%:+6Hz"

  # 只改台词不改语速/音调（省略 rate/pitch 用默认 0%/0Hz）
  python gen_voice_lines.py <输出目录> --voice "v1:今天天气真好"

参数:
  outdir            输出目录（脚本自动创建）
  --voice           自定义台词，格式 文件名:台词[:rate][:pitch]，可重复
  --rate / --pitch  全局默认语速/音调（自定义台词未指定时生效）
  --voice <name>    可用微软神经网络中文女声：zh-CN-XiaoxiaoNeural（晓晓，默认）
                    zh-CN-XiaoyiNeural（晓伊，更活泼）/ zh-CN-YunxiNeural（云希，男声）

依赖:
  pip install edge-tts   （需联网；Windows 本地 System.Speech TTS 可能被安全策略拦截）
"""
import argparse
import asyncio
import os
import sys

import edge_tts

VOICE = "zh-CN-XiaoxiaoNeural"  # 晓晓：年轻自然女声

# 默认 4 句剧情台词（发现→犹豫→进店→满足），带情绪语速/音调设计
DEFAULT_LINES = [
    ("voice_find", "哇——好漂亮的蛋糕店！", "+20%", "+8Hz"),
    ("voice_hesitate", "嗯…草莓蛋糕…要不要进去呢？", "-15%", "-3Hz"),
    ("voice_enter", "哇，好香啊——", "+8%", "+5Hz"),
    ("voice_happy", "嘿嘿，草莓蛋糕到手啦！", "+10%", "+6Hz"),
]


def parse_voice_arg(arg: str, def_rate: str, def_pitch: str):
    """解析 '文件名:台词[:rate][:pitch]' → (文件名, 台词, rate, pitch)。"""
    parts = arg.split(":", 3)
    if len(parts) < 2:
        sys.exit(f"--voice 格式应为 文件名:台词[:rate][:pitch]，收到: {arg}")
    name = parts[0].strip()
    if not name:
        sys.exit(f"--voice 文件名不能为空: {arg}")
    text = parts[1].strip()
    rate = parts[2] if len(parts) > 2 and parts[2] else def_rate
    pitch = parts[3] if len(parts) > 3 and parts[3] else def_pitch
    return (name, text, rate, pitch)


async def gen(outdir: str, lines, voice: str):
    os.makedirs(outdir, exist_ok=True)
    for name, text, rate, pitch in lines:
        out = os.path.join(outdir, f"{name}.mp3")
        tts = edge_tts.Communicate(text, voice=voice, rate=rate, pitch=pitch)
        await tts.save(out)
        print(f"OK {out}: {text} [{rate} {pitch}]")


def main() -> None:
    ap = argparse.ArgumentParser(description="generate TTS voice lines with edge-tts")
    ap.add_argument("outdir", nargs="?", default=".", help="输出目录")
    ap.add_argument("--voice", action="append", default=[], help="自定义台词 文件名:台词[:rate][:pitch]")
    ap.add_argument("--rate", default="0%", help="全局默认语速，如 +20% / -15%")
    ap.add_argument("--pitch", default="0Hz", help="全局默认音调，如 +8Hz / -3Hz")
    ap.add_argument("--tts-voice", default=VOICE, help="edge-tts 音色名（默认晓晓）")
    args = ap.parse_args()

    lines = [parse_voice_arg(v, args.rate, args.pitch) for v in args.voice] if args.voice else DEFAULT_LINES
    try:
        asyncio.run(gen(args.outdir, lines, args.tts_voice))
    except Exception as e:
        sys.exit(f"TTS 生成失败（需联网，可重试）: {e}")


if __name__ == "__main__":
    main()
