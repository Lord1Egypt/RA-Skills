#!/usr/bin/env python3
"""Video pins with ffmpeg: fit the user's clip to a pin shape, turn photos into a short video pin,
and look at the frames before choosing what opens the video.

    python3 scripts/video.py fit clip.mov --ratio 2:3 --x 0.5 --start 1.2 --end 9 --out video/pin.mp4
    python3 scripts/video.py fit clip.mov --ratio 9:16 --fit pad --out video/pin.mp4
    python3 scripts/video.py fit timelapse.mp4 --start 1.5 --end 25.5 --speed 2 --out video/pin.mp4
    python3 scripts/video.py stills a.jpg b.jpg c.jpg --seconds 1.2 --ratio 2:3 --out video/stills.mp4
    python3 scripts/video.py frames video/pin.mp4 --out video/        # frames-sheet.jpg to look at

fit:    crops to the ratio around --x (where the subject is, 0 = left, 1 = right), or pads (--fit pad)
        with a blurred copy or a plain colour (--bg black) when cropping would cut the subject. H.264, AAC, 30 fps, faststart.
        --start trims dead air: Pinterest plays videos muted in the feed and the first frame is what
        people see before it moves, so open on the most telling moment.
stills: each photo held --seconds with a short crossfade; for product or step photos the user owns.
frames: 8 evenly spaced frames on one sheet, with the 2:3 feed crop drawn on each.
Sizes: 2:3 = 1000x1500, 9:16 = 1080x1920, 1:1 = 1080x1080, 4:5 = 1080x1350.
"""
import argparse, json, os, shutil, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pinlib as P  # noqa: E402

SIZES = {"2:3": (1000, 1500), "9:16": (1080, 1920), "1:1": (1080, 1080), "4:5": (1080, 1350)}
ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-r", "30",
       "-movflags", "+faststart"]


def need_ffmpeg():
    if not (shutil.which("ffmpeg") and shutil.which("ffprobe")):
        sys.exit("ffmpeg is needed for video pins: run python3 scripts/check_setup.py for the install command")


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        sys.exit("ffmpeg failed:\n" + r.stderr[-1500:])


def has_audio(path):
    info = P.ffprobe(path) or {}
    return any(s.get("codec_type") == "audio" for s in info.get("streams", []))


def cmd_fit(a):
    w, h = SIZES[a.ratio]
    trim = []
    if a.start:
        trim += ["-ss", str(a.start)]
    if a.end:
        trim += ["-to", str(a.end)]
    if a.fit == "crop":
        vf = (f"scale={w}:{h}:force_original_aspect_ratio=increase,"
              f"crop={w}:{h}:(iw-{w})*{a.x}:(ih-{h})*{a.y},setsar=1")
        if a.speed != 1:
            vf += f",setpts=PTS/{a.speed}"
        fc = ["-vf", vf]
    else:
        bg = (f"color=c={a.bg}:s={w}x{h}[bg];" if a.bg != "blur" else
              f"[0:v]scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},boxblur=30:3,eq=brightness=-0.08[bg];")
        fc = ["-filter_complex", bg +
              f"[0:v]scale={w}:{h}:force_original_aspect_ratio=decrease[fg];"
              f"[bg][fg]overlay=(W-w)/2:(H-h)/2:shortest=1,setsar=1{f',setpts=PTS/{a.speed}' if a.speed != 1 else ''}[v]",
              "-map", "[v]"] + (["-map", "0:a?"] if a.speed == 1 else [])
    audio = ["-c:a", "aac", "-b:a", "160k"] if has_audio(a.input) and a.speed == 1 else ["-an"]
    if a.speed != 1 and has_audio(a.input):
        print("note: --speed drops the sound track")
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    run(["ffmpeg", "-y", "-v", "error"] + trim + ["-i", a.input] + fc + ENC + audio + [a.out])
    dur = P.duration(P.ffprobe(a.out))
    print(f"wrote {a.out} ({w}x{h}, {dur:.1f} s)")
    if dur < P.VIDEO_MIN_S:
        print(f"warning: {dur:.1f} s is under Pinterest's 4 s minimum")


def cmd_stills(a):
    from PIL import Image, ImageOps
    w, h = SIZES[a.ratio]
    tmp = os.path.join(os.path.dirname(os.path.abspath(a.out)), ".stills")
    os.makedirs(tmp, exist_ok=True)
    frames = []
    for i, f in enumerate(a.images):
        im = P.open_image(f)
        im = ImageOps.fit(im, (w, h), P.LANCZOS, centering=(a.x, a.y))
        p = os.path.join(tmp, f"{i:03d}.png")
        im.save(p)
        frames.append(p)
    if len(frames) < 2:
        sys.exit("stills needs at least 2 images")
    fade = max(0.0, min(a.fade, a.seconds / 3))
    if fade == 0:      # hard cuts: text changes cleanly, no ghosted double headlines
        listfile = os.path.join(tmp, "list.txt")
        with open(listfile, "w", encoding="utf-8") as f:
            for p in frames:
                f.write(f"file '{os.path.abspath(p).replace(chr(92), '/')}'\nduration {a.seconds:.3f}\n")
            f.write(f"file '{os.path.abspath(frames[-1]).replace(chr(92), '/')}'\n")
        os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
        run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", listfile, "-vf", "fps=30,format=yuv420p"]
            + ENC + ["-an", a.out])
        shutil.rmtree(tmp, ignore_errors=True)
        dur = P.duration(P.ffprobe(a.out))
        print(f"wrote {a.out} ({w}x{h}, {len(frames)} photos, hard cuts, {dur:.1f} s)")
        if dur < P.VIDEO_MIN_S:
            print(f"warning: {dur:.1f} s is under Pinterest's 4 s minimum; add photos or raise --seconds")
        return
    inputs, chain = [], ""
    for p in frames:
        inputs += ["-loop", "1", "-t", f"{a.seconds + fade:.3f}", "-i", p]
    prev = "[0:v]"
    for i in range(1, len(frames)):
        out = f"[x{i}]" if i < len(frames) - 1 else "[v]"
        # each input lasts seconds+fade; the i-th crossfade starts i*seconds in
        chain += f"{prev}[{i}:v]xfade=transition=fade:duration={fade:.3f}:offset={i * a.seconds:.3f}{out};"
        prev = out
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    run(["ffmpeg", "-y", "-v", "error"] + inputs + ["-filter_complex", chain.rstrip(";"),
         "-map", "[v]"] + ENC + ["-an", a.out])
    shutil.rmtree(tmp, ignore_errors=True)
    dur = P.duration(P.ffprobe(a.out))
    print(f"wrote {a.out} ({w}x{h}, {len(frames)} photos, {dur:.1f} s)")
    if dur < P.VIDEO_MIN_S:
        print(f"warning: {dur:.1f} s is under Pinterest's 4 s minimum; add photos or raise --seconds")


def cmd_frames(a):
    from PIL import Image, ImageDraw
    dur = P.duration(P.ffprobe(a.input))
    if not dur:
        sys.exit("couldn't read the video's length")
    os.makedirs(a.out, exist_ok=True)
    shots = []
    for i in range(a.n):
        t = dur * (i + 0.5) / a.n
        fr = P.frame_at(a.input, t)
        if fr:
            shots.append((t, fr))
    tw = 240
    sheet = None
    for i, (t, fr) in enumerate(shots):
        th = int(tw * fr.height / fr.width)
        if sheet is None:
            sheet = Image.new("RGB", (len(shots) * (tw + 10) + 10, th + 46), "#EEEEEE")
        im = fr.resize((tw, th), P.LANCZOS)
        d = ImageDraw.Draw(im)
        cw, ch = (tw, int(tw * 1.5)) if th > tw * 1.5 else (int(th / 1.5), th)
        x0, y0 = (tw - cw) // 2, (th - ch) // 2
        d.rectangle([x0, y0, x0 + cw - 1, y0 + ch - 1], outline="#E60023", width=3)
        sheet.paste(im, (10 + i * (tw + 10), 10))
        ImageDraw.Draw(sheet).text((10 + i * (tw + 10), th + 18), f"{t:.1f} s", fill="#333333")
    if sheet is None:
        sys.exit("couldn't read any frames from the video")
    path = os.path.join(a.out, "frames-sheet.jpg")
    sheet.save(path, quality=88)
    json.dump([{"t": round(t, 2)} for t, _ in shots], open(os.path.join(a.out, "frames.json"), "w"))
    print(f"wrote {path}: the red box is the 2:3 area the feed shows. Open on the frame that tells the story")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("fit")
    f.add_argument("input")
    f.add_argument("--ratio", choices=SIZES, default="2:3")
    f.add_argument("--fit", choices=["crop", "pad"], default="crop")
    f.add_argument("--bg", default="blur", help="pad background: blur (a blurred copy) or a colour like black or #0D1020")
    f.add_argument("--x", type=float, default=0.5)
    f.add_argument("--y", type=float, default=0.5)
    f.add_argument("--start", type=float)
    f.add_argument("--end", type=float)
    f.add_argument("--speed", type=float, default=1.0, help="play faster (2 = twice as fast; drops the sound)")
    f.add_argument("--out", required=True)
    s = sub.add_parser("stills")
    s.add_argument("images", nargs="+")
    s.add_argument("--seconds", type=float, default=1.2)
    s.add_argument("--fade", type=float, default=0.3, help="crossfade seconds; 0 = hard cuts (use when frames carry text)")
    s.add_argument("--ratio", choices=SIZES, default="2:3")
    s.add_argument("--x", type=float, default=0.5)
    s.add_argument("--y", type=float, default=0.5)
    s.add_argument("--out", required=True)
    fr = sub.add_parser("frames")
    fr.add_argument("input")
    fr.add_argument("--n", type=int, default=8)
    fr.add_argument("--out", required=True)
    a = ap.parse_args()
    if getattr(a, "speed", 1) <= 0:
        sys.exit("--speed must be above 0")
    for k in ("x", "y"):
        if hasattr(a, k) and not 0 <= getattr(a, k) <= 1:
            sys.exit(f"--{k} is a fraction of the frame, from 0 to 1")
    need_ffmpeg()
    {"fit": cmd_fit, "stills": cmd_stills, "frames": cmd_frames}[a.cmd](a)


if __name__ == "__main__":
    main()
