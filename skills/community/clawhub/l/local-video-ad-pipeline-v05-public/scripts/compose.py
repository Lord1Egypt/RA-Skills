"""
Compose final video from clips, burn Korean-safe subtitles, concat, and optionally mux BGM.

Supports either fixed per-clip duration or variable durations planned from
subtitle reading time by plan_subtitle_durations.py.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path


DEFAULT_FONT = r"C\:/Windows/Fonts/malgun.ttf"


def ffmpeg_textfile_path(path):
    return path.resolve().as_posix().replace(":", r"\:")


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def probe_duration(path):
    out = subprocess.check_output([
        "ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", str(path)
    ], text=True)
    v = next(s for s in json.loads(out)["streams"] if s["codec_type"] == "video")
    return float(v["duration"])


def sanitize_subtitle(text, max_chars):
    text = " ".join(str(text).replace("\\n", " ").replace("\r", " ").replace("\n", " ").split())
    if max_chars and len(text) > max_chars:
        return text[: max(0, max_chars - 3)].rstrip() + "..."
    return text


def wrap_subtitle(text, max_line_chars=16, max_lines=2):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        candidate = word if not current else current + " " + word
        if len(candidate) <= max_line_chars:
            current = candidate
            continue
        if current:
            lines.append(current)
        current = word
        if len(lines) >= max_lines - 1:
            break
    if current and len(lines) < max_lines:
        lines.append(current)

    consumed = " ".join(lines)
    if len(consumed) < len(text):
        # Fall back to character packing for Korean-heavy lines with few spaces.
        compact = text
        lines = [compact[i:i + max_line_chars] for i in range(0, len(compact), max_line_chars)][:max_lines]
    if len(lines) > max_lines:
        lines = lines[:max_lines]
    if lines and len("".join(lines)) < len(text.replace(" ", "")):
        lines[-1] = lines[-1].rstrip(" .") + "..."
    return lines or [text]


def subtitle_size(lines, hero):
    n = max(len(line) for line in lines)
    base = 38 if hero else 32
    if n > 14:
        base -= 3
    if n > 18:
        base -= 3
    return max(24, base)


def load_durations(path):
    if not path:
        return {}
    data = read_json(path)
    if "items" in data:
        data = data["items"]
    out = {}
    for sid, value in data.items():
        if isinstance(value, dict):
            out[sid] = float(value["duration_s"])
        else:
            out[sid] = float(value)
    return out


def target_for(sid, durations, per_clip):
    return float(durations.get(sid, per_clip))


def step1(project, subs, durations, per_clip, out_fps, font, hero, tmp, no_slow, max_subtitle_chars, allow_short_clip):
    actual = {}
    for sid in sorted(subs):
        src = project / "videos" / f"{sid}.mp4"
        if not src.exists():
            print(f"  {sid}: missing {src}, skip")
            continue
        src_dur = probe_duration(src)
        target = target_for(sid, durations, per_clip)
        is_hero = sid in hero
        subtitle = sanitize_subtitle(subs[sid], max_subtitle_chars)
        lines = wrap_subtitle(subtitle, max_line_chars=14, max_lines=2)
        size = subtitle_size(lines, is_hero)
        line_gap = max(4, size // 4)

        if no_slow:
            if src_dur + 0.05 < target and not allow_short_clip:
                raise RuntimeError(
                    f"{sid}: native clip {src_dur:.2f}s is shorter than subtitle target {target:.2f}s. "
                    "Render more frames for this shot."
                )
            prefix = f"fps={out_fps},trim=duration={target:.3f},setpts=PTS-STARTPTS,"
            printed = f"native trim {src_dur:.2f}s -> {target:.2f}s"
            actual[sid] = min(src_dur, target)
        else:
            prefix = f"setpts={target / src_dur:.4f}*PTS,fps={out_fps},"
            printed = f"retime {src_dur:.2f}s -> {target:.2f}s"
            actual[sid] = target

        filters = [prefix.rstrip(",")]
        block_h = len(lines) * size + (len(lines) - 1) * line_gap
        if is_hero:
            base_y = f"(h-{block_h})/2+110"
        else:
            base_y = f"h-{block_h}-42"
        for line_idx, line in enumerate(lines):
            textfile = tmp / f"{sid}_subtitle_{line_idx + 1}.txt"
            textfile.write_text(line, encoding="utf-8")
            textfile_arg = ffmpeg_textfile_path(textfile)
            y = f"{base_y}+{line_idx * (size + line_gap)}"
            filters.append(
                f"drawtext=fontfile='{font}':textfile='{textfile_arg}':"
                f"fontcolor=white:fontsize={size}:"
                f"borderw=3:bordercolor=black@0.85:"
                f"shadowx=2:shadowy=2:shadowcolor=black@0.6:"
                f"x=(w-text_w)/2:y={y}:enable='gte(t,0.25)'"
            )
        vf = ",".join(filters)
        dst = tmp / f"{sid}_sub.mp4"
        cmd = [
            "ffmpeg", "-y", "-i", str(src), "-vf", vf,
            "-c:v", "libx264", "-preset", "medium", "-crf", "16",
            "-pix_fmt", "yuv420p", "-an", str(dst),
        ]
        print(f"  {sid}: {printed} + sub")
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stderr[-1000:])
            sys.exit(1)
    return actual


def step2(subs, tmp, silent_out):
    listfile = tmp / "concat.txt"
    listfile.write_text("\n".join(
        f"file '{(tmp / f'{sid}_sub.mp4').as_posix()}'"
        for sid in sorted(subs) if (tmp / f"{sid}_sub.mp4").exists()
    ), encoding="utf-8")
    silent_out.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listfile), "-c", "copy", str(silent_out)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-1000:])
        sys.exit(1)
    print(f"silent -> {silent_out}")


def step3(silent, bgm, fade_in, fade_out, total, final):
    fade_out_st = max(0, total - fade_out)
    af = f"[1:a]afade=t=in:st=0:d={fade_in},afade=t=out:st={fade_out_st}:d={fade_out}[a]"
    cmd = [
        "ffmpeg", "-y", "-i", str(silent), "-i", str(bgm),
        "-filter_complex", af, "-map", "0:v", "-map", "[a]",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", str(final),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-1000:])
        sys.exit(1)
    print(f"final -> {final}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--subs", required=True, help="JSON file: {sid: text, ...}")
    ap.add_argument("--durations", help="durations.json from plan_subtitle_durations.py")
    ap.add_argument("--out", required=True, help="Final mp4 path")
    ap.add_argument("--bgm", help="Optional WAV BGM path; omit for silent")
    ap.add_argument("--per-clip", type=float, default=5.0)
    ap.add_argument("--no-slow", action="store_true",
                    help="Keep each clip at native speed; trim long clips to the subtitle duration.")
    ap.add_argument("--target-duration", type=float, help="Validate final silent duration.")
    ap.add_argument("--allow-short", action="store_true")
    ap.add_argument("--allow-short-clip", action="store_true")
    ap.add_argument("--max-subtitle-chars", type=int, default=34)
    ap.add_argument("--out-fps", type=int, default=30)
    ap.add_argument("--font", default=DEFAULT_FONT)
    ap.add_argument("--hero", nargs="*", default=["S03", "S06"])
    ap.add_argument("--fade-in", type=float, default=0.5)
    ap.add_argument("--fade-out", type=float, default=1.0)
    args = ap.parse_args()

    project = Path(args.project)
    subs = read_json(args.subs)
    durations = load_durations(args.durations)
    tmp = project / "tmp_clips"
    tmp.mkdir(exist_ok=True)
    final = Path(args.out)
    silent = final.with_name(final.stem + "_silent.mp4")

    actual = step1(
        project, subs, durations, args.per_clip, args.out_fps, args.font, set(args.hero),
        tmp, args.no_slow, args.max_subtitle_chars, args.allow_short_clip
    )
    step2(subs, tmp, silent)
    actual_total = probe_duration(silent)
    if args.target_duration:
        if actual_total + 0.05 < args.target_duration and not args.allow_short:
            print(
                f"duration {actual_total:.3f}s is shorter than target {args.target_duration:.3f}s. "
                "Render more native frames or add another clip."
            )
            print("clip durations:", json.dumps(actual, ensure_ascii=False))
            sys.exit(2)
        if actual_total > args.target_duration + 0.05:
            trimmed = silent.with_name(silent.stem + "_trimmed.mp4")
            r = subprocess.run([
                "ffmpeg", "-y", "-i", str(silent), "-t", f"{args.target_duration:.3f}",
                "-c", "copy", "-an", str(trimmed)
            ], capture_output=True, text=True)
            if r.returncode != 0:
                print(r.stderr[-1000:])
                sys.exit(1)
            trimmed.replace(silent)
            actual_total = args.target_duration
    if args.bgm:
        step3(silent, Path(args.bgm), args.fade_in, args.fade_out, actual_total, final)
    else:
        silent.replace(final)
        print(f"final (silent) -> {final}")


if __name__ == "__main__":
    main()
