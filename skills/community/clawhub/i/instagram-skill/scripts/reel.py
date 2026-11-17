#!/usr/bin/env python3
"""Finish a Reel: pick a cover, make the cover image, and check the video against Instagram's overlays.

    python3 scripts/reel.py frames video.mp4 --out reel/             # 8 cover candidates + a sheet
    python3 scripts/reel.py cover video.mp4 --at 4.2 --out reel/cover.jpg [--title "3 rules"] [--theme dark]
    python3 scripts/reel.py zones video.mp4 --out reel/zones.jpg      # frames with the app's overlays drawn on

frames: sharp, well-lit candidates spread over the video (never the first half second), with the
  3:4 grid crop and the Reels overlay zones drawn on a contact sheet (frames-sheet.jpg).
cover: a 1080x1920 JPEG from one frame, with an optional title set inside the part the profile
  grid shows (the middle 3:4). Also writes cover-grid.jpg: the cover as the grid shows it.
zones: 6 frames with the areas Instagram covers (caption, buttons, top bar) shaded, so you can
  see whether any text in the video sits under them.
Needs Python 3.8+, Pillow and ffmpeg.
"""
import argparse, json, os, shutil, subprocess, sys, tempfile

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageStat

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

W, H = 1080, 1920
# Areas the Reels interface covers on a 1080x1920 frame (Meta's Reels safe-zone guidance:
# keep the top 14%, the bottom 35% and 6% on each side clear of text).
TOP, BOTTOM, SIDE = round(H * 0.14), round(H * 0.35), round(W * 0.06)
GRID_H = round(W * 4 / 3)              # the 3:4 window the profile grid shows
GRID_Y = (H - GRID_H) // 2


def need_ffmpeg():
    if not (shutil.which("ffmpeg") and shutil.which("ffprobe")):
        sys.exit("ffmpeg not found: run scripts/check_setup.py for the install command")


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", path],
                         capture_output=True, text=True).stdout
    try:
        return float(json.loads(out)["format"]["duration"])
    except Exception:
        sys.exit(f"can't read {path} as a video")


def grab(path, t, out):
    """One frame at time t, scaled and cropped to fill 1080x1920 the way a 9:16 Reel shows."""
    vf = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"
    r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", path, "-frames:v", "1",
                        "-vf", vf, "-q:v", "2", out], capture_output=True, text=True)
    if r.returncode != 0 or not os.path.exists(out):
        return None
    return out


def score(img):
    """Sharpness (edge energy) and exposure, so blurry or black frames sink."""
    g = img.convert("L").resize((270, 480))
    edges = ImageStat.Stat(g.filter(ImageFilter.FIND_EDGES)).var[0]
    mean = ImageStat.Stat(g).mean[0]
    exposure = 1 - abs(mean - 120) / 120
    return edges * max(exposure, 0.05)


def font(size, bold=True):
    try:
        from render_slides import font as rfont
        return rfont("sans", size, "Bold" if bold else "Regular")
    except Exception:
        return ImageFont.load_default()


def outline_zones(img):
    """Outlines only, for the cover candidates sheet, so the frames keep their real colours."""
    d = ImageDraw.Draw(img)
    red = (255, 59, 48)
    d.rectangle([SIDE, TOP, W - SIDE, H - BOTTOM], outline=red, width=5)
    d.rectangle([0, GRID_Y, W - 1, GRID_Y + GRID_H], outline=(255, 214, 10), width=6)
    return img


def shade_zones(img, alpha=110):
    over = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(over)
    red = (255, 59, 48, alpha)
    d.rectangle([0, 0, W, TOP], fill=red)
    d.rectangle([0, H - BOTTOM, W, H], fill=red)
    d.rectangle([0, TOP, SIDE, H - BOTTOM], fill=red)
    d.rectangle([W - SIDE, TOP, W, H - BOTTOM], fill=red)
    # the right-hand button column reaches higher than the caption
    d.rectangle([W - 150, round(H * 0.45), W, H - BOTTOM], fill=red)
    d.rectangle([0, GRID_Y, W - 1, GRID_Y + GRID_H], outline=(255, 214, 10, 255), width=6)
    out = Image.alpha_composite(img.convert("RGBA"), over).convert("RGB")
    return out


def sheet(images, labels, out, cols=4, thumb=270):
    th = round(thumb * H / W)
    rows = (len(images) + cols - 1) // cols
    pad, lab = 16, 44
    canvas = Image.new("RGB", (cols * thumb + (cols + 1) * pad, rows * (th + lab) + (rows + 1) * pad), "#111111")
    d = ImageDraw.Draw(canvas)
    f = font(26, False)
    for i, (im, text) in enumerate(zip(images, labels)):
        x = pad + (i % cols) * (thumb + pad)
        y = pad + (i // cols) * (th + lab + pad)
        canvas.paste(im.resize((thumb, th)), (x, y))
        d.text((x, y + th + 8), text, fill="#EEEEEE", font=f)
    canvas.save(out, "JPEG", quality=88)
    return out


def cmd_frames(a):
    need_ffmpeg()
    os.makedirs(a.out, exist_ok=True)
    d = duration(a.video)
    start = min(0.5, d / 10)
    n_try = max(a.n * 3, 12)
    cands = []
    tmp = tempfile.mkdtemp()
    for i in range(n_try):
        t = start + (d - start - 0.2) * (i + 0.5) / n_try
        p = grab(a.video, t, os.path.join(tmp, f"{i:03d}.jpg"))
        if p:
            with Image.open(p) as im:
                cands.append((score(im), t, p))
    if not cands:
        sys.exit("no frames could be read")
    # best first, skipping frames that look like one already picked or sit too close in time
    def small(p):
        with Image.open(p) as im:
            return im.convert("L").resize((36, 64))
    thumbs = {c[2]: small(c[2]) for c in cands}

    def alike(p, q):
        from PIL import ImageChops
        return ImageStat.Stat(ImageChops.difference(thumbs[p], thumbs[q])).mean[0] < 2.5

    gap = (d - start) / (a.n * 2)
    picks = []
    for c in sorted(cands, reverse=True):
        if len(picks) >= a.n:
            break
        if any(abs(c[1] - p[1]) < gap or alike(c[2], p[2]) for p in picks):
            continue
        picks.append(c)
    picks.sort(key=lambda c: c[1])
    imgs, labels, meta = [], [], []
    for k, (s, t, p) in enumerate(picks):
        dst = os.path.join(a.out, f"frame-{k + 1:02d}-{t:.1f}s.jpg")
        shutil.copyfile(p, dst)
        with Image.open(dst) as im:
            imgs.append(outline_zones(im.convert("RGB").copy()))
        labels.append(f"{k + 1}: {t:.1f}s")
        meta.append({"file": os.path.basename(dst), "time": round(t, 2), "score": round(s, 1)})
    shutil.rmtree(tmp, ignore_errors=True)
    sheet(imgs, labels, os.path.join(a.out, "frames-sheet.jpg"))
    with open(os.path.join(a.out, "frames.json"), "w") as f:
        json.dump(meta, f, indent=1)
    print(f"wrote {len(picks)} candidates and frames-sheet.jpg to {a.out}")
    print("Yellow box = what the profile grid shows. Red box = the area clear of Instagram's caption, buttons and top bar.")


def wrap(draw, text, f, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textlength(test, font=f) <= max_w or not cur:
            cur = test
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def cmd_cover(a):
    need_ffmpeg()
    out = a.out if a.out.lower().endswith((".jpg", ".jpeg")) else os.path.join(a.out, "cover.jpg")
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    if a.image:
        with Image.open(a.image) as im:
            from PIL import ImageOps
            img = ImageOps.fit(ImageOps.exif_transpose(im).convert("RGB"), (W, H), Image.LANCZOS)
    else:
        tmp = os.path.join(tempfile.mkdtemp(), "f.jpg")
        if not grab(a.video, a.at, tmp):
            sys.exit(f"no frame at {a.at}s")
        img = Image.open(tmp).convert("RGB")
    if a.title:
        dark = a.theme != "light"
        # a soft scrim behind the title so it reads on any frame
        scrim = Image.new("L", (W, H), 0)
        sd = ImageDraw.Draw(scrim)
        cy = GRID_Y + GRID_H // 2
        sd.rectangle([0, cy - 300, W, cy + 300], fill=205 if dark else 190)
        scrim = scrim.filter(ImageFilter.GaussianBlur(70))
        base = Image.new("RGB", (W, H), (0, 0, 0) if dark else (255, 255, 255))
        img = Image.composite(base, img, scrim)
        d = ImageDraw.Draw(img)
        max_w = W - 2 * 120
        size = 128
        while size >= 64:
            f = font(size)
            lines = wrap(d, a.title, f, max_w)
            lh = round(size * 1.08)
            if len(lines) <= 4 and lh * len(lines) <= 600:
                break
            size -= 6
        y = cy - lh * len(lines) // 2
        fg = "#FFFFFF" if dark else "#111111"
        for ln in lines:
            d.text(((W - d.textlength(ln, font=f)) / 2, y), ln, fill=fg, font=f)
            y += lh
        if a.kicker:
            fk = font(44, False)
            d.text(((W - d.textlength(a.kicker, font=fk)) / 2, y + 24), a.kicker,
                   fill="#DDDDDD" if dark else "#444444", font=fk)
    img.save(out, "JPEG", quality=92, optimize=True)
    grid = img.crop((0, GRID_Y, W, GRID_Y + GRID_H)).resize((360, 480), Image.LANCZOS)
    gpath = os.path.join(os.path.dirname(os.path.abspath(out)), "cover-grid.jpg")
    grid.save(gpath, "JPEG", quality=90)
    print(f"wrote {out} (1080x1920) and {gpath} (how the profile grid shows it)")


def cmd_zones(a):
    need_ffmpeg()
    d = duration(a.video)
    tmp = tempfile.mkdtemp()
    imgs, labels = [], []
    for i in range(6):
        t = min(d - 0.1, 0.3 + (d - 0.4) * i / 5)
        p = grab(a.video, t, os.path.join(tmp, f"{i}.jpg"))
        if p:
            with Image.open(p) as im:
                imgs.append(shade_zones(im.copy()))
            labels.append(f"{t:.1f}s")
    out = a.out if a.out.lower().endswith((".jpg", ".jpeg")) else os.path.join(a.out, "zones.jpg")
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    sheet(imgs, labels, out, cols=3, thumb=300)
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"wrote {out}: any text inside a red area sits under Instagram's caption, buttons or top bar")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("frames")
    f.add_argument("video")
    f.add_argument("--out", default="reel")
    f.add_argument("--n", type=int, default=8)
    c = sub.add_parser("cover")
    c.add_argument("video", nargs="?")
    c.add_argument("--at", type=float, default=1.0, help="time of the frame in seconds")
    c.add_argument("--image", help="use this image instead of a frame (a photo or a rendered slide)")
    c.add_argument("--title", help="short cover title, 2 to 6 words")
    c.add_argument("--kicker", help="optional small line under the title")
    c.add_argument("--theme", choices=["dark", "light"], default="dark")
    c.add_argument("--out", default="reel/cover.jpg")
    z = sub.add_parser("zones")
    z.add_argument("video")
    z.add_argument("--out", default="reel/zones.jpg")
    a = ap.parse_args()
    if a.cmd == "cover" and not (a.video or a.image):
        sys.exit("give a video (and --at) or --image")
    {"frames": cmd_frames, "cover": cmd_cover, "zones": cmd_zones}[a.cmd](a)


if __name__ == "__main__":
    main()
