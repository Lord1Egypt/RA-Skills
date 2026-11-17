#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""探测视频/音频文件的元信息（时长、分辨率、帧率、编码、音轨等），输出 JSON。

用法:
  python probe_video.py <文件...> [--json]

输出示例:
  python probe_video.py shot1.mp4 shot2.mp4
  → 每个文件一行摘要；--json 输出完整 JSON 结构

用途:
  - 拼接前确认各镜头参数一致（分辨率/帧率/时长）
  - 排查素材：检查是否带音轨、编码是否兼容
  - 被 stitch_videos.py 内部复用（时长探测）
"""
import argparse
import json
import re
import subprocess
import sys

import imageio_ffmpeg


def probe(ffmpeg: str, path: str) -> dict:
    """解析 ffmpeg -i 的 stderr 输出，返回结构化元信息。"""
    r = subprocess.run([ffmpeg, "-i", path], capture_output=True, text=True)
    info = r.stderr
    out = {"path": path}

    # Duration: 00:00:05.04
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", info)
    if m:
        h, mi, s = m.groups()
        out["duration"] = int(h) * 3600 + int(mi) * 60 + float(s)
        out["duration_str"] = f"{int(h)}:{mi}:{s}"

    # 流信息
    out["streams"] = []
    for line in info.splitlines():
        sm = re.search(r"Stream #\d+:\d+(?:\[[^\]]*\])?\(?(\w+)?\)?: (\w+): (.+)", line)
        if not sm:
            continue
        lang, stype, detail = sm.groups()
        s = {"type": stype, "detail": detail.strip()}
        if lang:
            s["lang"] = lang
        # 视频：分辨率 / 帧率
        vm = re.search(r"(\d{2,5})x(\d{2,5})", detail)
        if stype == "Video" and vm:
            s["width"], s["height"] = int(vm.group(1)), int(vm.group(2))
        fm = re.search(r"(\d+(?:\.\d+)?)\s*fps", detail)
        if stype == "Video" and fm:
            s["fps"] = float(fm.group(1))
        # 编码
        cm = re.search(r"Video:\s*([a-z0-9_]+)", detail)
        if stype == "Video" and cm:
            s["codec"] = cm.group(1)
        am = re.search(r"Audio:\s*([a-z0-9_]+)", detail)
        if stype == "Audio" and am:
            s["codec"] = am.group(1)
        out["streams"].append(s)

    # 常用快捷字段
    videos = [s for s in out["streams"] if s["type"] == "Video"]
    audios = [s for s in out["streams"] if s["type"] == "Audio"]
    if videos:
        out["video"] = {
            "codec": videos[0].get("codec"),
            "width": videos[0].get("width"),
            "height": videos[0].get("height"),
            "fps": videos[0].get("fps"),
        }
    out["has_audio"] = bool(audios)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="probe media file metadata")
    ap.add_argument("files", nargs="+")
    ap.add_argument("--json", action="store_true", help="输出完整 JSON")
    args = ap.parse_args()

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    results = [probe(ffmpeg, f) for f in args.files]

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return

    for r in results:
        dur = r.get("duration_str", "?")
        v = r.get("video", {})
        res = f"{v.get('width','?')}x{v.get('height','?')}" if v else "-"
        fps = f"{v.get('fps','?')}fps" if v else "-"
        audio = "有音轨" if r.get("has_audio") else "无音轨"
        print(f"{r['path']} | {dur} | {res} | {fps} | {audio}")


if __name__ == "__main__":
    main()
