#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""多镜头拼接一条龙：按顺序拼接 N 个视频，加转场（xfade），混入背景音乐与按时间轴定位的语气词配音。

用法:
  python stitch_videos.py shot2.mp4 shot1.mp4 shot3.mp4 shot4.mp4 \
      --transitions dissolve,fadeblack,dissolve --duration 0.5 \
      --bgm bgm_full_track.wav:0.42 \
      --voice 1800:voice_find.mp3:1.3 --voice 5900:voice_hesitate.mp3:1.3 \
      --out 完整版.mp4

参数:
  videos           位置参数，按播放顺序的视频文件（≥2）
  --transitions    逗号分隔的转场类型，数量 = 视频数-1（默认全 dissolve）
                   常用：dissolve 交叉溶解 / fadeblack 黑场 / fade 淡入淡出 / slideleft 左滑
  --duration       每个转场时长（秒，默认 0.5）
  --bgm            背景音乐 文件[:音量]，默认音量 0.42
  --voice          语气词 '延迟毫秒:音频文件[:音量]'，可重复多次，默认音量 1.3
  --out            输出文件路径
  --t              总时长截断（秒），默认按 各段时长之和 - 转场时长*个数 自动计算
  --crf            H.264 质量（默认 20）
"""
import argparse
import os
import re
import subprocess
import sys

import imageio_ffmpeg

try:
    # 复用 probe_video.py 的探测逻辑（同目录）
    from probe_video import probe as _probe
except ImportError:
    def _probe(ffmpeg, path):  # 兜底：不依赖 probe_video.py
        r = subprocess.run([ffmpeg, "-i", path], capture_output=True, text=True)
        m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", r.stderr)
        if not m:
            return {"duration": 10.0}
        h, mi, s = m.groups()
        return {"duration": int(h) * 3600 + int(mi) * 60 + float(s)}

# xfade 常用合法转场名（避免无效值导致 ffmpeg 报错）
VALID_TRANSITIONS = {
    "fade", "fadeblack", "fadewhite", "dissolve", "slideleft", "slideright",
    "slideup", "slidedown", "wipeleft", "wiperight", "circleopen", "circleclose",
    "smoothleft", "smoothright", "smoothup", "smoothdown", "zoompan", "radial",
    "pixelize", "hblur", "wblur", "distance", "squeezev", "squeezeh", "hlwind",
    "hlslice", "hrwind", "hrslice", "vuwind", "vuslice", "vdwind", "vdslice",
}


def probe_dur(ffmpeg: str, path: str) -> float:
    """返回视频时长（秒），探测失败时按 10 秒兜底。"""
    return float(_probe(ffmpeg, path).get("duration", 10.0))


def main() -> None:
    ap = argparse.ArgumentParser(description="stitch video shots with transitions and audio")
    ap.add_argument("videos", nargs="+")
    ap.add_argument("--transitions", default="")
    ap.add_argument("--duration", type=float, default=0.5)
    ap.add_argument("--bgm", default="")
    ap.add_argument("--voice", action="append", default=[])
    ap.add_argument("--out", default="stitched.mp4")
    ap.add_argument("--t", type=float, default=0.0)
    ap.add_argument("--crf", type=int, default=20)
    args = ap.parse_args()

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    n = len(args.videos)
    if n < 2:
        print("至少需要 2 个视频文件"); sys.exit(1)

    trans = (args.transitions.split(",") if args.transitions else ["dissolve"] * (n - 1))
    if len(trans) != n - 1:
        print(f"转场数量 {len(trans)} 必须等于视频数-1 = {n - 1}"); sys.exit(1)
    for t in trans:
        if t not in VALID_TRANSITIONS:
            print(f"无效转场类型: {t}（可选: {', '.join(sorted(VALID_TRANSITIONS))}）"); sys.exit(1)

    cmd = [ffmpeg, "-y"]
    for v in args.videos:
        if not os.path.isfile(v):
            print(f"视频文件不存在: {v}"); sys.exit(1)
        cmd += ["-i", v]

    # 音频输入：背景音乐 + 语气词（标签用 a1/a2/... 独立命名空间，避免与视频链 v0-vN 冲突）
    voices = []  # (标签, 延迟ms, 音量)
    if args.bgm:
        seg = args.bgm.rsplit(":", 1)
        f, vol = seg[0], (seg[1] if len(seg) > 1 else "0.42")
        if not os.path.isfile(f):
            print(f"背景音乐文件不存在: {f}"); sys.exit(1)
        cmd += ["-i", f]
        voices.append(("bgm", 0, vol))
    for v in args.voice:
        seg = v.split(":", 2)
        if len(seg) < 2:
            print(f"--voice 格式应为 延迟ms:文件[:音量]，收到: {v}"); sys.exit(1)
        delay, f = int(seg[0]), seg[1]
        vol = seg[2] if len(seg) > 2 else "1.3"
        if not os.path.isfile(f):
            print(f"语气词音频文件不存在: {f}"); sys.exit(1)
        cmd += ["-i", f]
        voices.append((f"a{len(voices)}", delay, vol))

    # 探测各视频时长，计算 xfade offset
    durs = [probe_dur(ffmpeg, v) for v in args.videos]
    D = args.duration
    offsets, cur = [], durs[0]
    for i in range(n - 1):
        off = cur - D
        offsets.append(round(off, 3))
        cur = cur + durs[i + 1] - D
    total = round(cur, 3)
    if args.t > 0:
        total = args.t

    # 视频链
    fc = []
    for i in range(n):
        fc.append(f"[{i}:v]format=yuv420p[v{i}]")
    prev = f"v0"
    for i in range(n - 1):
        out = f"x{i + 1}"
        fc.append(f"[{prev}][v{i + 1}]xfade=transition={trans[i]}:duration={D}:offset={offsets[i]}[{out}]")
        prev = out
    fc.append(f"[{prev}]format=yuv420p[vout]")

    # 音频链
    idx = n
    for label, delay, vol in voices:
        if label == "bgm":
            fc.append(f"[{idx}:a]aresample=44100,volume={vol}[bgm]")
        else:
            fc.append(f"[{idx}:a]aresample=44100,pan=stereo|c0=c0|c1=c0,"
                      f"adelay={delay}|{delay},volume={vol}[{label}]")
        idx += 1
    if voices:
        ins = "".join(f"[{l}]" for l, _, _ in voices)
        fc.append(f"{ins}amix=inputs={len(voices)}:duration=longest:normalize=0,"
                  f"alimiter=limit=0.95[aout]")

    cmd += ["-filter_complex", ";".join(fc)]
    cmd += ["-map", "[vout]"]
    if voices:
        cmd += ["-map", "[aout]"]
    cmd += ["-t", str(total), "-c:v", "libx264", "-preset", "medium", "-crf", str(args.crf),
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", args.out]

    print(">>> " + " ".join(cmd))
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-3000:]); sys.exit(r.returncode)
    print(f"OK {args.out}: {total}s")


if __name__ == "__main__":
    main()
