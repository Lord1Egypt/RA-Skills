#!/usr/bin/env python3
"""Render the video with FFmpeg: shots -> scenes (transitions, Ken Burns, text) -> narration + music -> out/video.mp4.

Timing: every scene lasts exactly as long as its narration (rounded up to whole frames), so picture and voice
cannot drift. Transitions happen between shots inside a scene; scene boundaries are hard cuts.

Usage
  build_video.py PROJECT_DIR [--draft] [--only s01,s02] [--burn-subs] [--transition fade,dissolve]
                 [--transition-sec 0.5] [--no-text] [--no-music] [--font PATH] [--out PATH]
--draft renders 640x360 at low quality for a fast check. --only renders just those scenes (to out/preview.mp4).
"""
import argparse
import math
import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as c  # noqa: E402

KB_VARIANTS = ("zoom_in", "pan_right", "zoom_out", "pan_left")


def kb_filter(variant, n, w, h, fps):
    W, H = w * 2, h * 2
    if variant == "zoom_in":
        z, x, y = f"1+0.15*on/{n}", "(iw-iw/zoom)/2", "(ih-ih/zoom)/2"
    elif variant == "zoom_out":
        z, x, y = f"1.15-0.15*on/{n}", "(iw-iw/zoom)/2", "(ih-ih/zoom)/2"
    elif variant == "pan_right":
        z, x, y = "1.12", f"(iw-iw/zoom)*on/{n}", "(ih-ih/zoom)/2"
    else:
        z, x, y = "1.12", f"(iw-iw/zoom)*(1-on/{n})", "(ih-ih/zoom)/2"
    return (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
            f"zoompan=z='{z}':x='{x}':y='{y}':d={n}:s={w}x{h}:fps={fps},setsar=1,format=yuv420p")


def render_shot(d, m, frames, w, h, fps, idx, q):
    src = Path(d) / m["file"]
    if not src.exists():
        raise c.Fail(f"Missing media file {m['file']}.")
    st = src.stat()
    variant = KB_VARIANTS[idx % 4]
    key = c.sha([str(src), st.st_size, st.st_mtime_ns, frames, w, h, fps, variant if m["kind"] == "image" else "v", q])
    dest = Path(d) / "build" / "shots" / f"{key}.mp4"
    if dest.exists():
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    enc = ["-an", "-c:v", "libx264", "-crf", str(q["crf"]), "-preset", q["preset"], "-pix_fmt", "yuv420p",
           "-frames:v", str(frames)]
    tmp = dest.with_suffix(".tmp.mp4")
    if m["kind"] == "image":
        c.ffmpeg(["-i", src, "-vf", kb_filter(variant, frames, w, h, fps)] + enc + [tmp])
    else:
        vf = f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},setsar=1,fps={fps},format=yuv420p"
        c.ffmpeg(["-stream_loop", "-1", "-i", src, "-t", f"{frames / fps:.4f}", "-vf", vf] + enc + [tmp])
    tmp.replace(dest)
    return dest


def plan_shots(total_frames, n, tf, fps):
    """Frames per shot so that sum - (n-1)*tf == total_frames. Reduces n if shots would be too short."""
    while n > 1 and (total_frames + (n - 1) * tf) // n < max(2 * tf, 2 * fps):
        n -= 1
    total = total_frames + (n - 1) * tf
    base, rem = divmod(total, n)
    return n, [base + (1 if i < rem else 0) for i in range(n)]


def text_filter(scene, d, w, h, font):
    t = (scene.get("on_screen_text") or "").strip()
    if not t or not font:
        return ""
    tf = Path(d) / "build" / "text" / f"{scene['id']}.txt"
    tf.parent.mkdir(parents=True, exist_ok=True)
    tf.write_text("\n".join(textwrap.wrap(t, 32)), encoding="utf-8")
    size = max(16, h // 17)
    # expansion=none: with FFmpeg's default text expansion a '%' (e.g. "6%") makes drawtext drop the whole text
    # with only a warning, while the render still reports success.
    return (f"drawtext=fontfile='{c.esc_filter_path(font)}':textfile='{c.esc_filter_path(tf)}':expansion=none:"
            f"fontsize={size}:"
            f"fontcolor=white:box=1:boxcolor=black@0.55:boxborderw={size // 3}:x=(w-text_w)/2:y=h*0.78:"
            f"enable='between(t,0.4,4.5)'")


def build_scene(d, row, w, h, fps, q, trans, tsec, font, use_text):
    s = row["scene"]
    media = [m for m in s.get("media", []) if (Path(d) / m["file"]).exists()]
    if not media:
        raise c.Fail(f"Scene {s['id']} has no media. Run fetch_clips.py pick or add-local.")
    tf = max(1, round(tsec * fps)) if len(media) > 1 else 0
    n, frames = plan_shots(row["frames"], len(media), tf, fps)
    if n < len(media):
        print(f"  {s['id']}: scene is short; using {n} of {len(media)} media.")
    shots = [render_shot(d, media[i], frames[i], w, h, fps, i, q) for i in range(n)]
    longest = max(frames) / fps
    if longest > 14:
        print(f"  {s['id']}: shots are {longest:.0f}s long; add more media for this scene to keep it lively.")
    txt = text_filter(s, d, w, h, font) if use_text else ""
    # The filter only names the text file, so the text itself and the font must be in the key; otherwise a changed
    # on_screen_text silently reuses the old scene.
    key = c.sha([[str(p) for p in shots], frames, tf, trans, txt, (s.get("on_screen_text") or "").strip() if txt else "",
                 str(font) if txt else "", row["frames"], q])
    dest = Path(d) / "build" / "scenes" / f"{s['id']}_{key}.mp4"
    if dest.exists():
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    for old in dest.parent.glob(f"{s['id']}_*.mp4"):
        old.unlink()
    inputs = []
    for p in shots:
        inputs += ["-i", p]
    tail = ["-an", "-c:v", "libx264", "-crf", str(q["crf"]), "-preset", q["preset"], "-pix_fmt", "yuv420p",
            "-frames:v", str(row["frames"]), dest]
    if n == 1:
        if txt:
            c.ffmpeg(["-i", shots[0], "-vf", txt] + tail)
        else:
            c.ffmpeg(["-i", shots[0], "-c:v", "copy", "-an", dest])
        return dest
    parts, prev, acc = [], "0:v", frames[0]
    for k in range(1, n):
        off = (acc - k * tf) / fps
        tr = trans[(k - 1) % len(trans)]
        out = f"v{k}"
        parts.append(f"[{prev}][{k}:v]xfade=transition={tr}:duration={tf / fps:.4f}:offset={off:.4f}[{out}]")
        prev, acc = out, acc + frames[k]
    last = f"[{prev}]" + (txt + "," if txt else "") + "format=yuv420p[vout]"
    parts.append(last)
    c.ffmpeg(inputs + ["-filter_complex", ";".join(parts), "-map", "[vout]"] + tail)
    return dest


def concat_list(files, listfile):
    lines = []
    for f in files:
        p = str(Path(f).resolve()).replace("'", "'\\''")
        lines.append(f"file '{p}'")
    Path(listfile).write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_audio(d, rows, project, use_music):
    """Return (narration_wav, total_seconds, filter parts, extra inputs)."""
    adir = Path(d) / "build" / "audio"
    adir.mkdir(parents=True, exist_ok=True)
    files = []
    for r in rows:
        s = r["scene"]
        if not s.get("audio_file") or not (Path(d) / s["audio_file"]).exists():
            raise c.Fail(f"Scene {s['id']} has no audio file. Run voiceover.py.")
        out = adir / f"{s['id']}.wav"
        c.ffmpeg(["-i", Path(d) / s["audio_file"], "-af", f"apad=whole_dur={r['dur']:.5f}", "-t", f"{r['dur']:.5f}",
                  "-ar", c.SAMPLE_RATE, "-ac", "1", "-c:a", "pcm_s16le", out])
        files.append(out)
    lst = adir / "narration.txt"
    concat_list(files, lst)
    narr = Path(d) / "build" / "narration.wav"
    c.ffmpeg(["-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", narr])
    return narr


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dir")
    ap.add_argument("--draft", action="store_true")
    ap.add_argument("--only")
    ap.add_argument("--burn-subs", action="store_true")
    ap.add_argument("--transition", default="fade,dissolve")
    ap.add_argument("--transition-sec", type=float, default=0.5)
    ap.add_argument("--no-text", action="store_true")
    ap.add_argument("--no-music", action="store_true")
    ap.add_argument("--font")
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    try:
        d = Path(a.dir).resolve()
        project = c.load_project(d)
        fps = project["fps"]
        w, h = c.parse_resolution(project["resolution"])
        q = {"crf": 18, "preset": "veryfast"}
        if a.draft:
            w, h, q = 640, 360, {"crf": 30, "preset": "ultrafast"}
        trans = [t.strip() for t in a.transition.split(",") if t.strip()] or ["fade"]
        rows, total = c.timeline(project)
        if a.only:
            ids = {x.strip() for x in a.only.split(",")}
            rows = [r for r in rows if r["scene"]["id"] in ids]
            if not rows:
                raise c.Fail("--only matched no scenes.")
            t = 0.0
            for r in rows:
                r["start"] = t
                t += r["dur"]
            total = t
        font = c.find_font(a.font)
        if not font and any(r["scene"].get("on_screen_text") for r in rows) and not a.no_text:
            print("Warning: no font file found, on-screen text skipped (use --font PATH).")
        c.ensure_dirs(d)
        print(f"Rendering {len(rows)} scene(s), {c.fmt_clock(total)} at {w}x{h} {fps} fps"
              f"{' (draft)' if a.draft else ''}.")
        scene_files = []
        for i, r in enumerate(rows, 1):
            print(f"[{i}/{len(rows)}] {r['scene']['id']}")
            scene_files.append(build_scene(d, r, w, h, fps, q, trans, a.transition_sec, font, not a.no_text))
        lst = d / "build" / "scenes.txt"
        concat_list(scene_files, lst)
        vid = d / "build" / "video_noaudio.mp4"
        c.ffmpeg(["-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", vid])

        # ---- audio mix ----
        narr = build_audio(d, rows, project, not a.no_music)
        music = project.get("music") or {}
        mfile = d / music["file"] if music.get("file") and not a.no_music else None
        if mfile and not mfile.exists():
            raise c.Fail(f"Music file not found: {music['file']}")
        inputs = ["-i", vid, "-i", narr]
        fc, idx = [], 2
        fc.append("[1:a]aresample=48000,asplit=2[n1][n2]" if mfile and music.get("duck", True) else "[1:a]aresample=48000[n1]")
        mix_in = ["[n1]"]
        if mfile:
            inputs += ["-stream_loop", "-1", "-i", mfile]
            vol = float(music.get("volume", 0.15))
            fo = max(0.0, total - 3)
            fc.append(f"[{idx}:a]atrim=0:{total:.3f},asetpts=PTS-STARTPTS,aresample=48000,volume={vol},"
                      f"afade=t=in:d=2,afade=t=out:st={fo:.3f}:d=3[m0]")
            if music.get("duck", True):
                fc.append("[m0][n2]sidechaincompress=threshold=0.03:ratio=10:attack=20:release=500[m1]")
                mix_in.append("[m1]")
            else:
                mix_in.append("[m0]")
            idx += 1
        starts = {r["scene"]["id"]: r["start"] for r in rows}
        for j, fx in enumerate(project.get("sfx") or []):
            p = d / fx.get("file", "")
            if not fx.get("file") or not p.exists():
                print(f"Warning: sfx file missing: {fx.get('file')}")
                continue
            at = fx.get("at")
            if at is None:
                if fx.get("scene") not in starts:
                    continue
                at = starts[fx["scene"]] + float(fx.get("offset", 0))
            if at >= total:
                continue
            ms = int(round(float(at) * 1000))
            inputs += ["-i", p]
            fc.append(f"[{idx}:a]aresample=48000,aformat=channel_layouts=mono,adelay={ms}:all=1,"
                      f"volume={float(fx.get('volume', 0.8))}[x{j}]")
            mix_in.append(f"[x{j}]")
            idx += 1
        if len(mix_in) > 1:
            fc.append(f"{''.join(mix_in)}amix=inputs={len(mix_in)}:duration=first:normalize=0:dropout_transition=0[mix]")
            src = "[mix]"
        else:
            src = mix_in[0]
        fc.append(f"{src}loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000,atrim=0:{total:.3f}[aout]")

        vcodec = ["-c:v", "copy"]
        vmap = "0:v"
        if a.burn_subs:
            srt = d / "out" / "subtitles.srt"
            if not srt.exists():
                raise c.Fail("out/subtitles.srt not found. Run subtitles.py first.")
            fc.insert(0, "[0:v]subtitles=out/subtitles.srt:force_style='Fontsize=14,Outline=2,Shadow=0,MarginV=36'[vout]")
            vmap = "[vout]"
            vcodec = ["-c:v", "libx264", "-crf", str(q["crf"]), "-preset", q["preset"], "-pix_fmt", "yuv420p"]
        out = Path(a.out) if a.out else d / "out" / ("preview.mp4" if (a.only or a.draft) else "video.mp4")
        out.parent.mkdir(parents=True, exist_ok=True)
        c.ffmpeg(inputs + ["-filter_complex", ";".join(fc), "-map", vmap, "-map", "[aout]"] + vcodec +
                 ["-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-t", f"{total:.3f}", out], cwd=str(d))
        info = c.probe(str(out))
        diff = abs(info["duration"] - total)
        print(f"Done: {out} ({c.fmt_clock(info['duration'])}, {info['width']}x{info['height']}, "
              f"audio {'yes' if info['has_audio'] else 'NO'}); expected {c.fmt_clock(total)}, off by {diff:.2f}s.")
        if diff > 0.25:
            print("Warning: duration differs from the plan by more than 0.25 s; inspect the file.")
        return 0
    except c.Fail as e:
        print(f"error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
