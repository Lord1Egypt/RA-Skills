#!/usr/bin/env python3
"""GIF / 动图 -> 动画 WebP，专为网易云音乐动态头像准备。

用法:
    python make_animated_webp.py input.gif output.webp [--size 240] [--quality 75]
                                                      [--no-square] [--max-kb 4800]

依赖: Pillow (需带 webp 支持)
    python -m pip install --no-user --target ./pylibs pillow
    export PYTHONPATH=./pylibs

退出码:
    0  成功且校验通过
    1  参数/输入错误
    2  输出不是合法动画 WebP（帧数 <= 1 或缺少 ANIM/ANMF）
    3  体积超限
"""

import argparse
import os
import struct
import sys
from collections import Counter

try:
    from PIL import Image
except ImportError:
    sys.stderr.write("缺少 Pillow。安装: python -m pip install --no-user --target ./pylibs pillow\n")
    sys.exit(1)


def load_frames(path):
    im = Image.open(path)
    n = getattr(im, "n_frames", 1)
    frames, durations = [], []
    for i in range(n):
        im.seek(i)
        frames.append(im.convert("RGBA"))
        durations.append(im.info.get("duration", 100))
    return im.size, frames, durations


def to_square(frame, size):
    w, h = frame.size
    s = min(w, h)
    left = (w - s) // 2
    top = (h - s) // 2
    return frame.crop((left, top, left + s, top + s)).resize((size, size), Image.LANCZOS)


def webp_chunks(path):
    data = open(path, "rb").read()
    if data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        raise ValueError("not a RIFF/WEBP file, head=%r" % data[:12])
    i, out = 12, []
    while i + 8 <= len(data):
        cid = data[i:i + 4].decode("latin1")
        size = struct.unpack("<I", data[i + 4:i + 8])[0]
        out.append((cid, size))
        i += 8 + size + (size & 1)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--size", type=int, default=240, help="输出边长(正方形)，默认 240")
    ap.add_argument("--quality", type=int, default=75, help="WebP 质量，默认 75")
    ap.add_argument("--method", type=int, default=4, help="压缩方法 0-6，默认 4")
    ap.add_argument("--no-square", action="store_true", help="不做居中正方形裁切")
    ap.add_argument("--max-frames", type=int, default=0, help="抽帧上限，0 表示不抽帧")
    ap.add_argument("--max-kb", type=int, default=4800, help="体积上限 KB，默认 4800(<5MB)")
    args = ap.parse_args()

    if not os.path.exists(args.src):
        sys.stderr.write("源文件不存在: %s\n" % args.src)
        return 1

    size, frames, durations = load_frames(args.src)
    print("源图: %s  尺寸=%dx%d  帧数=%d  单帧时长=%sms  总时长=%sms"
          % (args.src, size[0], size[1], len(frames), durations[0], sum(durations)))

    if args.max_frames and len(frames) > args.max_frames:
        step = max(1, len(frames) // args.max_frames)
        keep = list(range(0, len(frames), step))[:args.max_frames]
        frames = [frames[i] for i in keep]
        durations = [durations[i] * step for i in keep]
        print("抽帧后: %d 帧" % len(frames))

    if args.no_square:
        out_frames = []
        for f in frames:
            w, h = f.size
            scale = args.size / max(w, h)
            out_frames.append(f.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.LANCZOS))
    else:
        out_frames = [to_square(f, args.size) for f in frames]

    out_frames[0].save(
        args.dst, "WEBP", save_all=True, append_images=out_frames[1:],
        duration=durations, loop=0, quality=args.quality, method=args.method,
    )

    kb = os.path.getsize(args.dst) / 1024.0
    print("输出: %s  %.1f KB" % (args.dst, kb))

    chunks = Counter(c[0] for c in webp_chunks(args.dst))
    nframes = chunks.get("ANMF", 0)
    print("块结构: %s" % dict(chunks))
    print("动画帧数(ANMF)=%d" % nframes)

    if nframes <= 1 or chunks.get("ANIM", 0) < 1:
        sys.stderr.write("输出不是动画 WebP（缺 ANIM/ANMF）。源文件可能只有 1 帧。\n")
        return 2

    if kb > args.max_kb:
        sys.stderr.write("体积超限 %.1f KB > %d KB，请降 --size / --quality / 加 --max-frames\n"
                         % (kb, args.max_kb))
        return 3

    print("OK: 可直接用于网易云动态头像")
    return 0


if __name__ == "__main__":
    sys.exit(main())
