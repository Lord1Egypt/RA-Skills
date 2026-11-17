# -*- coding: utf-8 -*-
"""把背景音乐混入视频（使用 imageio-ffmpeg 自带的 ffmpeg 二进制）。"""
import subprocess
import sys

import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


def main():
    video = sys.argv[1]
    music = sys.argv[2]
    out = sys.argv[3]
    # 音乐音量 0.9，带轻微淡入；视频轨道复制不重编码
    cmd = [
        FFMPEG, "-y",
        "-i", video,
        "-i", music,
        "-filter_complex", "[1:a]volume=0.9,afade=t=in:d=0.8[bg]",
        "-map", "0:v", "-map", "[bg]",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        out,
    ]
    print("ffmpeg:", " ".join(cmd[:8]), "...")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("FFMPEG_ERROR:\n", r.stderr[-2000:])
        sys.exit(1)
    print(f"OK muxed: {out}")


if __name__ == "__main__":
    main()
