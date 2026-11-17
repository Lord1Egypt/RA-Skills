#!/usr/bin/env python3
"""cut_audio.py —— 从原声切镜头音频，**只切不改速**。

铁律：音频速度 = 原文件速度（1.0）。
本脚本**不提供、也不接受任何变速参数**，代码里没有 atempo。
只做三件事：裁区间 → 补齐到精确长度 → 最后一段淡出（避免硬切爆音）。

用法
----
# 单镜：从 0.72 裁到 31.12
python3 scripts/cut_audio.py 00-输入/音频/原声.wav --start 0.72 --end 31.12 -o 00-输入/音频

# 多镜：同上，但在 15.54 处切成 S01 / S02（各镜 ≤30s）
python3 scripts/cut_audio.py 00-输入/音频/原声.wav --start 0.72 --end 31.12 \
    --split-at 15.54 -o 00-输入/音频

# 只看怎么切、不写文件
python3 scripts/cut_audio.py 00-输入/音频/原声.wav --start 0.72 --end 31.12 \
    --split-at 15.54 --dry-run

关键提醒
--------
`--end` 必须是**最后一个字的结束时间 + 0.5~0.8s**。
拿句子的「开始时间」当结尾 → 最后一个字被整段切掉，这就是"少几个字、突然结束"。
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

MAX_SHOT_SECONDS = 30.0


def run(cmd: list[str]) -> str:
    return subprocess.run(cmd, capture_output=True, text=True, check=True).stdout


def probe_duration(path: Path) -> float:
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
               "-of", "csv=p=0", str(path)]).strip()
    return float(out)


def md5_slice(path: Path, start: float, dur: float = 0.2) -> str:
    out = subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-ss", f"{start:.3f}", "-t", f"{dur:.3f}", "-i", str(path),
         "-ar", "44100", "-ac", "1", "-f", "md5", "-"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    return out


def cut(src: Path, start: float, end: float, out: Path, fade: float, is_last: bool) -> float:
    dur = round(end - start, 3)
    filters = [f"apad=whole_dur={dur:.3f}"]
    if is_last and fade > 0:
        f = min(fade, dur / 3)
        filters.append(f"afade=t=out:st={dur - f:.3f}:d={f:.3f}")
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
           "-ss", f"{start:.3f}", "-t", f"{dur:.3f}", "-i", str(src),
           "-af", ",".join(filters), "-t", f"{dur:.3f}",
           "-ar", "44100", "-ac", "1", "-c:a", "pcm_s16le", str(out)]
    subprocess.run(cmd, check=True)
    return probe_duration(out)


def main() -> int:
    ap = argparse.ArgumentParser(description="按区间切镜头音频（永不变速）")
    ap.add_argument("src", help="原声音频")
    ap.add_argument("--start", type=float, default=0.0, help="人声起点（默认 0）")
    ap.add_argument("--end", type=float, default=None,
                    help="人声终点 = 最后一个字的结束时间 + 0.5~0.8s（默认取文件末尾）")
    ap.add_argument("--split-at", default="",
                    help="镜头切点，逗号分隔（绝对秒，落句间）。例：15.54,31.0")
    ap.add_argument("-o", "--outdir", default=None, help="输出目录（默认与原声同目录）")
    ap.add_argument("--prefix", default="S", help="输出前缀（默认 S → S01.wav）")
    ap.add_argument("--fade", type=float, default=0.30, help="末段淡出秒数（默认 0.30，0=关闭）")
    ap.add_argument("--dry-run", action="store_true", help="只打印方案，不写文件")
    ap.add_argument("--json", action="store_true", help="额外输出 JSON 摘要到 stdout")
    args = ap.parse_args()

    src = Path(args.src)
    if not src.is_file():
        print(f"[错误] 找不到原声：{src}", file=sys.stderr)
        return 2

    total = probe_duration(src)
    start = max(0.0, args.start)
    end = total if args.end is None else args.end
    if end > total + 0.01:
        print(f"[错误] --end {end:.2f}s 超过原声长度 {total:.2f}s", file=sys.stderr)
        return 2
    if end - start <= 0.5:
        print(f"[错误] 区间太短：{start:.2f} → {end:.2f}", file=sys.stderr)
        return 2

    splits = sorted(float(x) for x in args.split_at.split(",") if x.strip())
    bounds = [start]
    for s in splits:
        if not (start < s < end):
            print(f"[错误] 切点 {s:.2f} 不在 ({start:.2f}, {end:.2f}) 内", file=sys.stderr)
            return 2
        bounds.append(s)
    bounds.append(end)

    segs = [(bounds[i], bounds[i + 1]) for i in range(len(bounds) - 1)]
    bad = [(a, b) for a, b in segs if b - a > MAX_SHOT_SECONDS + 1e-6]
    if bad:
        print(f"[错误] 有 {len(bad)} 个片段超过 {MAX_SHOT_SECONDS:g}s："
              + "、".join(f"{a:.2f}-{b:.2f}" for a, b in bad)
              + "\n       请增加 --split-at 切点（切在句与句之间）", file=sys.stderr)
        return 2

    outdir = Path(args.outdir) if args.outdir else src.parent
    outdir.mkdir(parents=True, exist_ok=True)

    print(f"[原声] {src.name} · {total:.3f}s")
    print(f"[区间] {start:.2f} → {end:.2f}（{end - start:.2f}s）· {len(segs)} 镜")
    print(f"[变速] 无（1.0 倍原速；本脚本不支持变速）")

    summary = []
    for i, (a, b) in enumerate(segs, 1):
        name = f"{args.prefix}{i:02d}.wav"
        out = outdir / name
        is_last = i == len(segs)
        if args.dry_run:
            got = round(b - a, 3)
        else:
            got = cut(src, a, b, out, args.fade, is_last)
            same = md5_slice(src, a) == md5_slice(out, 0.0)
            if not same:
                print(f"[错误] {name} 与原声切片不一致（可能被改速/改采样）", file=sys.stderr)
                return 3
        summary.append({"id": f"{args.prefix}{i:02d}", "file": name,
                        "start": round(a, 3), "end": round(b, 3), "seconds": round(got, 3)})
        print(f"  {name}  {a:6.2f} → {b:6.2f}  · {got:6.2f}s"
              + ("  (淡出 %.2fs)" % args.fade if is_last and args.fade else ""))

    print(f"[合计] {sum(s['seconds'] for s in summary):.2f}s")
    if args.json:
        print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
