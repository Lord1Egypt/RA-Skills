"""成片拼接：concat + 混音 + 烧字幕."""
from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys


def pick_video_dir(project_dir: pathlib.Path) -> pathlib.Path:
    """优先用 lipsync/，fallback 到 videos/."""
    lipsync = project_dir / "lipsync"
    videos = project_dir / "videos"
    if lipsync.exists() and any(lipsync.glob("S*.mp4")):
        return lipsync
    return videos


def write_concat_list(videos: list[pathlib.Path], out: pathlib.Path) -> None:
    lines = [f"file '{v.resolve()}'" for v in videos]
    out.write_text("\n".join(lines))


def build_srt(script: dict, out: pathlib.Path) -> None:
    """按镜头 5s 均摊，每条对白占该镜时段."""
    entries = []
    idx = 1
    t = 0.0
    scene_dur = script.get("scene_duration", 5)
    for scene in script.get("scenes", []):
        dialogues = scene.get("dialogue", [])
        n = max(1, len(dialogues))
        slot = scene_dur / n
        for i, d in enumerate(dialogues):
            start = t + i * slot
            end = start + slot - 0.1
            entries.append(
                f"{idx}\n{fmt_ts(start)} --> {fmt_ts(end)}\n{d.get('text', '')}\n"
            )
            idx += 1
        t += scene_dur
    out.write_text("\n".join(entries))


def fmt_ts(s: float) -> str:
    h = int(s // 3600)
    m = int((s % 3600) // 60)
    sec = s % 60
    return f"{h:02d}:{m:02d}:{sec:06.3f}".replace(".", ",")


def run(cmd: list[str]) -> None:
    print(f"  $ {' '.join(cmd[:6])} ...")
    subprocess.run(cmd, check=True)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--project-dir", required=True)
    args = p.parse_args()

    project_dir = pathlib.Path(args.project_dir)
    script = json.loads((project_dir / "script.json").read_text())

    video_dir = pick_video_dir(project_dir)
    videos = sorted(video_dir.glob("S*.mp4"))
    if not videos:
        print(f"❌ 找不到视频片段: {video_dir}")
        return 1
    print(f"[edit] 从 {video_dir.name}/ 拼接 {len(videos)} 个镜头")

    # 1. concat
    concat_list = project_dir / "concat.txt"
    write_concat_list(videos, concat_list)
    concat_out = project_dir / "concat.mp4"
    run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy", str(concat_out),
    ])

    # 2. 字幕
    srt = project_dir / "subtitle.srt"
    build_srt(script, srt)

    # 3. 混 BGM + 烧字幕
    bgm = project_dir / "bgm.mp3"
    final = project_dir / "final.mp4"
    vf = f"subtitles={srt}:force_style='FontName=Source Han Serif SC,FontSize=48,PrimaryColour=&H00FFFFFF&,OutlineColour=&H00000000&,Outline=3,MarginV=120'"

    if bgm.exists():
        # 混入 BGM（压到 -20dB）
        run([
            "ffmpeg", "-y",
            "-i", str(concat_out),
            "-i", str(bgm),
            "-filter_complex",
            f"[0:a]volume=1.0[a0];[1:a]volume=0.1[a1];[a0][a1]amix=inputs=2:duration=first[aout]",
            "-map", "0:v", "-map", "[aout]",
            "-vf", vf,
            "-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-c:a", "aac", "-b:a", "192k",
            str(final),
        ])
    else:
        run([
            "ffmpeg", "-y",
            "-i", str(concat_out),
            "-vf", vf,
            "-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-c:a", "copy",
            str(final),
        ])

    size_mb = final.stat().st_size / 1024 / 1024
    print(f"✅ {final} ({size_mb:.1f} MB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
