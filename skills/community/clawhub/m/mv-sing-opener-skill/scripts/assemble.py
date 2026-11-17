#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把逐镜片段整理成最终成片：拼接（多镜）+ 贴回参考音频 + 精确裁秒 + 可选字幕。

用法：
  python3 scripts/assemble.py <项目>
  python3 scripts/assemble.py <项目> --subtitle
  python3 scripts/assemble.py <项目> --subtitle --burn

输入：
  04-提示词/分镜JSON.json          # shots[]：seconds / ref_audio_urls / lyrics（相对秒）
  成片片段/S01.mp4 …（生成时已裁到精确秒）
  06-MV成片_无音轨.mp4             # 有就直接用（generate_video.py --merge 产物）
输出：
  06-MV成片.mp4                    # 贴回音轨的最终成片
  06-歌词字幕.srt                  # --subtitle 时（绝对秒）
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import CLIPS_ROOT, PLAN_DIRS, PLAN_NAME, resolve_project  # noqa: E402


def ffprobe_duration(path: Path) -> float:
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration",
           "-of", "default=noprint_wrappers=1:nokey=1", str(path)]
    out = subprocess.run(cmd, capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(out.stderr.strip()[:500])
    return float(out.stdout.strip())


def has_audio(path: Path) -> bool:
    cmd = ["ffprobe", "-v", "error", "-select_streams", "a",
           "-show_entries", "stream=index", "-of", "csv=p=0", str(path)]
    out = subprocess.run(cmd, capture_output=True, text=True)
    return bool(out.stdout.strip())


def srt_time(t: float) -> str:
    t = max(0.0, float(t))
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    ms = int(round((t - int(t)) * 1000))
    if ms == 1000:
        s += 1
        ms = 0
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def run(cmd: list[str]) -> None:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError((proc.stderr or proc.stdout).strip()[:1200])


def resolve_local(project: Path, value: str) -> Path | None:
    p = Path(value)
    for cand in (project / p, project / "00-输入" / "音频" / p.name,
                 project / "00-输入" / p.name):
        if cand.is_file():
            return cand
    return None


def concat_audio(parts: list[Path], out: Path) -> None:
    if len(parts) == 1:
        shutil.copy2(parts[0], out)
        return
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                     encoding="utf-8") as f:
        for p in parts:
            f.write(f"file '{p.resolve().as_posix()}'\n")
        listfile = f.name
    try:
        run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
             "-f", "concat", "-safe", "0", "-i", listfile,
             "-c:a", "pcm_s16le", str(out)])
    finally:
        Path(listfile).unlink(missing_ok=True)


def concat_video(clips: list[Path], out: Path) -> None:
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                     encoding="utf-8") as f:
        for p in clips:
            f.write(f"file '{p.resolve().as_posix()}'\n")
        listfile = f.name
    try:
        run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
             "-f", "concat", "-safe", "0", "-i", listfile,
             "-c", "copy", str(out)])
    finally:
        Path(listfile).unlink(missing_ok=True)


def main() -> None:
    ap = argparse.ArgumentParser(description="说唱视频：拼接 + 贴音轨 + 裁秒 + 可选字幕")
    ap.add_argument("project", help="项目目录，或 assets/output 下的项目名")
    ap.add_argument("--out", default="", help="输出（默认 <项目>/06-MV成片.mp4）")
    ap.add_argument("--subtitle", action="store_true", help="生成 06-歌词字幕.srt")
    ap.add_argument("--burn", action="store_true", help="把字幕烧进画面（需 --subtitle）")
    ap.add_argument("--crf", type=int, default=18, help="x264 CRF（默认 18）")
    args = ap.parse_args()

    project = resolve_project(args.project)
    plan_path = next((project / d / PLAN_NAME for d in PLAN_DIRS
                      if (project / d / PLAN_NAME).is_file()), None)
    if plan_path is None:
        sys.exit(f"[FAIL] 找不到 {PLAN_DIRS[0]}/{PLAN_NAME}")

    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    shots = plan.get("shots") or []
    if not shots:
        sys.exit("[FAIL] 分镜JSON 没有 shots")

    # ---------- 逐镜参数
    segs = []
    for i, s in enumerate(shots, 1):
        sid = str(s.get("id") or f"S{i:02d}")
        try:
            sec = float(s.get("seconds"))
        except (TypeError, ValueError):
            sys.exit(f"[FAIL] {sid} 没有有效的 seconds")
        segs.append({"id": sid, "seconds": sec,
                     "audios": s.get("ref_audio_urls") or [],
                     "lyrics": s.get("lyrics") or []})
    total = sum(x["seconds"] for x in segs)

    # ---------- 视频源
    merged = project / "06-MV成片_无音轨.mp4"
    if merged.is_file():
        video_src = merged
        print(f"[输入] 用已合并的无音轨成片：{merged.name}")
    elif len(segs) == 1:
        single = project / CLIPS_ROOT / f"{segs[0]['id']}.mp4"
        if not single.is_file():
            sys.exit(f"[FAIL] 找不到片段：{single}")
        video_src = single
        print(f"[输入] 单镜片段：{single.name}")
    else:
        clips = [project / CLIPS_ROOT / f"{x['id']}.mp4" for x in segs]
        missing = [c for c in clips if not c.is_file()]
        if missing:
            sys.exit("[FAIL] 缺片段：" + "、".join(c.name for c in missing))
        video_src = project / "06-MV成片_无音轨.mp4"
        concat_video(clips, video_src)
        print(f"[拼接] {len(clips)} 段 → {video_src.name}")

    # ---------- 音轨（逐镜参考音频顺次拼接）
    tmp_audio = project / "06-成片音轨.wav"
    parts = []
    for x in segs:
        got = None
        for v in x["audios"]:
            v = str(v or "")
            if v.startswith(("http://", "https://")):
                continue
            hit = resolve_local(project, v)
            if hit:
                got = hit
                break
        if got is None:
            sys.exit(f"[FAIL] {x['id']} 找不到本地参考音频（先上传/回填，或本地保留一份）")
        parts.append(got)
    if has_audio(video_src):
        print("[音频] 片段自带音轨，仍以参考音频为准（保持与口型一致）")
    concat_audio(parts, tmp_audio)
    audio_dur = ffprobe_duration(tmp_audio)
    print(f"[音轨] {tmp_audio.name}：{audio_dur:.3f}s（目标 {total:.3f}s）")

    # ---------- 字幕（绝对秒）
    srt_path = project / "06-歌词字幕.srt"
    if args.subtitle:
        lines, n, offset = [], 0, 0.0
        for x in segs:
            for row in x["lyrics"]:
                text = str(row.get("text") or "").strip()
                if not text:
                    continue
                st = offset + float(row.get("start") or 0)
                en = offset + float(row.get("end") or (float(row.get("start") or 0) + 2))
                n += 1
                lines += [str(n), f"{srt_time(st)} --> {srt_time(en)}", text, ""]
            offset += x["seconds"]
        srt_path.write_text("\n".join(lines), encoding="utf-8")
        print(f"[字幕] {srt_path.name}（{n} 条，绝对秒）")

    # ---------- 合成
    out = Path(args.out).expanduser() if args.out else project / "06-MV成片.mp4"
    out.parent.mkdir(parents=True, exist_ok=True)

    actual = ffprobe_duration(video_src)
    print(f"[时长] 画面 {actual:.3f}s · 目标 {total:.3f}s")

    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
           "-i", str(video_src), "-i", str(tmp_audio)]
    vf = []
    if actual < total - 0.05:
        vf.append(f"tpad=stop_mode=clone:stop_duration={total - actual:.3f}")
    if args.burn:
        if not srt_path.is_file():
            sys.exit("[FAIL] --burn 需要先 --subtitle")
        esc = str(srt_path).replace("\\", "/").replace(":", "\\:").replace("'", "\\'")
        vf.append(f"subtitles='{esc}':force_style='FontSize=16,Outline=1,Shadow=0'")
    if vf:
        cmd += ["-vf", ",".join(vf)]
    cmd += ["-map", "0:v:0", "-map", "1:a:0", "-t", f"{total:.3f}",
            "-c:v", "libx264", "-preset", "medium", "-crf", str(args.crf),
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart", str(out)]

    print("[合成] " + " ".join(cmd))
    run(cmd)

    final = ffprobe_duration(out)
    print(f"[OK] 成片：{out}（{final:.3f}s，音轨={'有' if has_audio(out) else '无'}）")


if __name__ == "__main__":
    main()
