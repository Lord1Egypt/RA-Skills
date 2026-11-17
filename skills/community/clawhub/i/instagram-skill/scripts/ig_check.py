#!/usr/bin/env python3
"""Check every post in a plan against Instagram's current API limits, and fix what can be fixed.

    python3 scripts/ig_check.py plan.json          # report only
    python3 scripts/ig_check.py plan.json --fix    # write fixed copies to fixed/ and point the plan at them

Images: JPEG only, sRGB, 320 to 1440 px wide, aspect 4:5 to 1.91:1 for feed posts, at most 8 MB.
Videos: H.264 or HEVC in MP4/MOV, AAC audio, 23 to 60 fps, Reels 3 s to 15 min and 300 MB,
Stories 3 to 60 s. Captions: 2,200 characters, 5 hashtags, 20 mentions.
The limits live in LIMITS below, with the date they were checked; see references/instagram-specs.md.

Fixes never touch the originals. Anything that can't be fixed safely is reported as an error
with the reason, and the script exits with code 1 while errors remain.
Needs Python 3.8+, Pillow and (for video) ffmpeg/ffprobe.
"""
import argparse, json, os, re, shutil, subprocess, sys

from PIL import Image, ImageFilter, ImageOps

try:  # iPhone .heic photos, when pillow-heif is installed
    from pillow_heif import register_heif_opener
    register_heif_opener()
except ImportError:
    pass

# Checked 2026-11-04 against Meta's content publishing docs and Instagram's own announcements.
LIMITS = {
    "image_min_w": 320, "image_max_w": 1440, "image_bytes": 8 * 1024 * 1024,
    "feed_min_ratio": 0.8, "feed_max_ratio": 1.91,           # width / height
    "carousel_min": 2, "carousel_max": 20,
    "reel_min_s": 3, "reel_max_s": 15 * 60, "reel_bytes": 300 * 1024 * 1024,
    "story_min_s": 3, "story_max_s": 60, "story_bytes": 100 * 1024 * 1024,
    "carousel_video_max_s": 60,
    "fps_min": 23, "fps_max": 60,
    "caption_chars": 2200, "hashtags": 5, "mentions": 20, "fold_chars": 125,
}
VIDEO_EXT = {".mp4", ".mov", ".m4v", ".webm", ".mkv", ".avi"}
GRID_RATIO = 3 / 4  # the profile grid shows posts at 3:4

issues = []  # (level, post_id, item, message)


def report(level, post, item, msg):
    issues.append((level, post, item, msg))


def rel(path, base):
    try:
        return os.path.relpath(path, base)
    except ValueError:
        return path


# ---------- probing ----------

def probe_video(path):
    if not shutil.which("ffprobe"):
        sys.exit("ffprobe not found: install ffmpeg to check videos (see scripts/check_setup.py)")
    out = subprocess.run(["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", path],
                         capture_output=True, text=True)
    if out.returncode != 0:
        return None
    data = json.loads(out.stdout or "{}")
    v = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), None)
    a = next((s for s in data.get("streams", []) if s.get("codec_type") == "audio"), None)
    if not v:
        return None
    w, h = int(v.get("width", 0)), int(v.get("height", 0))
    rot = 0
    for sd in v.get("side_data_list", []) or []:
        if "rotation" in sd:
            rot = abs(int(float(sd["rotation"])))
    if str(v.get("tags", {}).get("rotate", "")).strip():
        rot = abs(int(v["tags"]["rotate"]))
    if rot in (90, 270):
        w, h = h, w

    def rate(r):
        try:
            n, d = r.split("/")
            return float(n) / float(d) if float(d) else 0.0
        except Exception:
            return 0.0

    fps = rate(v.get("avg_frame_rate", "0/0")) or rate(v.get("r_frame_rate", "0/0"))
    dur = float(data.get("format", {}).get("duration") or v.get("duration") or 0)
    return {
        "w": w, "h": h, "fps": fps, "duration": dur,
        "vcodec": v.get("codec_name", ""), "pix_fmt": v.get("pix_fmt", ""),
        "acodec": a.get("codec_name", "") if a else "",
        "format": data.get("format", {}).get("format_name", ""),
        "bytes": os.path.getsize(path),
        "vfr": abs(rate(v.get("r_frame_rate", "0/0")) - fps) > 0.5,
        "color_transfer": v.get("color_transfer", ""),
    }


def faststart(path):
    """True when the 'moov' atom comes before 'mdat' (the video can start before it fully loads)."""
    try:
        with open(path, "rb") as f:
            head = f.read(1 << 20)
        m, d = head.find(b"moov"), head.find(b"mdat")
        return m != -1 and (d == -1 or m < d)
    except OSError:
        return True


# ---------- image checks and fixes ----------

def image_target(fmt):
    """Aspect ratio range allowed for this post format: (min, max) as width/height."""
    if fmt == "story":
        return (0.5, 0.5625)  # anything taller than 9:16 is fine in Stories; we fit to 9:16
    return (LIMITS["feed_min_ratio"], LIMITS["feed_max_ratio"])


def check_image(path, fmt, post, label, first_ratio=None):
    problems, info = [], {}
    try:
        with Image.open(path) as im:
            info = {"w": im.width, "h": im.height, "format": im.format, "mode": im.mode,
                    "icc": bool(im.info.get("icc_profile")), "exif_rot": False}
            try:
                o = im.getexif().get(0x0112)
                info["exif_rot"] = o in (5, 6, 7, 8)
            except Exception:
                pass
    except Exception as e:
        hint = " (install pillow-heif to read iPhone .heic photos)" if path.lower().endswith((".heic", ".heif")) else ""
        report("error", post, label, f"can't open as an image{hint} ({e})")
        return None, ["unreadable"]
    w, h = (info["h"], info["w"]) if info["exif_rot"] else (info["w"], info["h"])
    ratio = w / h
    if info["format"] != "JPEG":
        problems.append("jpeg")
        report("fix", post, label, f"{info['format']} image: the Instagram API only takes JPEG")
    if info["mode"] not in ("RGB", "L"):
        problems.append("mode")
        report("fix", post, label, f"colour mode {info['mode']}: needs RGB (transparency becomes white)")
    if w > LIMITS["image_max_w"]:
        problems.append("big")
        report("fix", post, label, f"{w} px wide: the API takes at most {LIMITS['image_max_w']}; resize to 1080")
    if w < LIMITS["image_min_w"]:
        report("error", post, label, f"{w} px wide: below the API minimum of {LIMITS['image_min_w']}; use a larger original")
    elif w < 1080:
        report("warn", post, label, f"{w} px wide: Instagram shows 1080, so this will look soft")
    lo, hi = image_target(fmt)
    if fmt == "story":
        if abs(ratio - 9 / 16) > 0.01:
            problems.append("ratio")
            report("fix", post, label, f"aspect {w}x{h}: Stories are 9:16; fit to 1080x1920")
    elif ratio < lo - 0.005 or ratio > hi + 0.005:
        problems.append("ratio")
        if ratio < lo:
            report("fix", post, label, f"aspect {w}x{h} is taller than 4:5: the API rejects it; fit to 4:5 (1080x1350)")
        else:
            report("fix", post, label, f"aspect {w}x{h} is wider than 1.91:1: the API rejects it; fit to 1.91:1, "
                   "or to 4:5 with --ratio 4:5 (bigger in the feed and the grid)")
    if fmt == "carousel" and first_ratio and abs(ratio - first_ratio) > 0.01 and "ratio" not in problems:
        problems.append("match")
        report("fix", post, label, "a different shape from item 1: Instagram crops every item to the first one's shape")
    if os.path.getsize(path) > LIMITS["image_bytes"]:
        problems.append("bytes")
        report("fix", post, label, f"{os.path.getsize(path) / 1e6:.1f} MB: the API takes at most 8 MB")
    if fmt in ("image", "carousel") and " #1" in label or fmt == "image":
        if ratio > GRID_RATIO + 0.005:
            trim = 1 - GRID_RATIO / ratio
            if trim > 0.12:
                report("warn", post, label, f"the 3:4 profile grid will hide {trim:.0%} of the width of this cover; keep the subject and text in the middle")
    return ratio, problems


def fit_image(src, dst, ratio, mode, max_w=1080):
    """Fit to the target ratio: 'crop' keeps the centre, 'pad' adds a blurred copy behind it."""
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im)
        if im.mode in ("RGBA", "LA", "P"):
            im = im.convert("RGBA")
            bg = Image.new("RGB", im.size, "white")
            bg.paste(im, mask=im.split()[-1])
            im = bg
        else:
            im = im.convert("RGB")
        icc = im.info.get("icc_profile")
        if icc:
            try:
                from PIL import ImageCms
                import io
                src_prof = ImageCms.ImageCmsProfile(io.BytesIO(icc))
                im = ImageCms.profileToProfile(im, src_prof, ImageCms.createProfile("sRGB"), outputMode="RGB")
            except Exception:
                pass
        w, h = im.size
        cur = w / h
        if ratio and abs(cur - ratio) > 0.005:
            if mode == "crop":  # never upscale: the crop keeps the source's own pixels
                tw = min(max_w, w if cur <= ratio else round(h * ratio))
            else:               # padding keeps the full width and adds space around the picture
                tw = min(max_w, w)
            th = round(tw / ratio)
            if mode == "crop":
                im = ImageOps.fit(im, (tw, th), Image.LANCZOS, centering=(0.5, 0.45))
            else:
                bg = ImageOps.fit(im, (tw, th), Image.LANCZOS).filter(ImageFilter.GaussianBlur(40))
                bg = Image.blend(bg, Image.new("RGB", bg.size, (0, 0, 0)), 0.25)
                fg = ImageOps.contain(im, (tw, th), Image.LANCZOS)
                bg.paste(fg, ((tw - fg.width) // 2, (th - fg.height) // 2))
                im = bg
        if im.width > max_w:
            im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
        q = 92
        while True:
            im.save(dst, "JPEG", quality=q, optimize=True, progressive=True, subsampling=0 if q >= 90 else 2)
            if os.path.getsize(dst) <= LIMITS["image_bytes"] or q <= 70:
                break
            q -= 6
    return dst


# ---------- video checks and fixes ----------

def check_video(path, fmt, post, label):
    info = probe_video(path)
    if not info:
        report("error", post, label, "can't read this video (no video stream)")
        return None, ["unreadable"]
    problems = []
    ratio = info["w"] / info["h"] if info["h"] else 0
    ext = os.path.splitext(path)[1].lower()
    if ext not in (".mp4", ".mov"):
        problems.append("container")
        report("fix", post, label, f"{ext} file: Instagram takes MP4 or MOV")
    if info["vcodec"] not in ("h264", "hevc"):
        problems.append("codec")
        report("fix", post, label, f"video codec {info['vcodec']}: needs H.264 (or HEVC)")
    if info["pix_fmt"] not in ("yuv420p", "yuvj420p"):
        problems.append("pix")
        report("fix", post, label, f"pixel format {info['pix_fmt']} (10-bit or HDR shows washed out or fails): re-encode to 8-bit yuv420p")
    if info["color_transfer"] in ("smpte2084", "arib-std-b67"):
        problems.append("hdr")
        report("fix", post, label, "HDR video: Instagram's upload often turns it grey; convert to SDR")
    if info["acodec"] and info["acodec"] != "aac":
        problems.append("audio")
        report("fix", post, label, f"audio codec {info['acodec']}: needs AAC")
    if not info["acodec"]:
        report("warn", post, label, "no audio track: fine, but silent Reels can't be given music through the API; add sound before posting if it needs it")
    if info["fps"] and not LIMITS["fps_min"] - 0.5 <= info["fps"] <= LIMITS["fps_max"] + 0.5:
        problems.append("fps")
        report("fix", post, label, f"{info['fps']:.2f} fps: needs 23 to 60; re-encode at 30")
    if info["vfr"]:
        report("warn", post, label, "variable frame rate (typical for phone screen recordings): re-encoding to constant 30 fps avoids audio drift")
    d = info["duration"]
    if fmt == "reel":
        lo, hi, cap = LIMITS["reel_min_s"], LIMITS["reel_max_s"], LIMITS["reel_bytes"]
    elif fmt == "story":
        lo, hi, cap = LIMITS["story_min_s"], LIMITS["story_max_s"], LIMITS["story_bytes"]
    else:
        lo, hi, cap = LIMITS["reel_min_s"], LIMITS["carousel_video_max_s"], LIMITS["reel_bytes"]
    if d < lo:
        report("error", post, label, f"{d:.1f} s: shorter than the {lo} s minimum")
    if d > hi:
        report("error", post, label, f"{d:.0f} s: longer than the {hi} s maximum for this format; trim it")
    if fmt in ("reel", "story") and abs(ratio - 9 / 16) > 0.01:
        problems.append("ratio")
        report("fix", post, label, f"{info['w']}x{info['h']}: {fmt.title()}s fill the screen at 9:16; fit to 1080x1920")
    if fmt == "carousel" and not 0.8 - 0.005 <= ratio <= 1.91:
        problems.append("ratio")
        report("fix", post, label, f"{info['w']}x{info['h']}: carousel items are 4:5 to 1.91:1; fit to 4:5")
    if max(info["w"], info["h"]) > 1920:
        problems.append("big")
        report("fix", post, label, f"{info['w']}x{info['h']}: larger than Instagram keeps (1080x1920); scaling down saves upload time")
    if info["bytes"] > cap:
        problems.append("bytes")
        report("fix", post, label, f"{info['bytes'] / 1e6:.0f} MB: over the {cap / 1e6:.0f} MB limit")
    if not faststart(path) and "codec" not in problems:
        report("warn", post, label, "the 'moov' index is at the end of the file; a re-encode with --fix moves it to the front")
    return ratio, problems


def edge_colour(src):
    """The average colour of the video's top and bottom edges, so the plate blends into it."""
    tmp = src + ".edge.png"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "1", "-i", src, "-frames:v", "1", "-vf", "scale=64:-2", tmp],
                   capture_output=True)
    try:
        with Image.open(tmp) as im:
            im = im.convert("RGB")
            px = [im.getpixel((x, y)) for x in range(im.width) for y in (0, 1, im.height - 2, im.height - 1)]
        os.remove(tmp)
        return "#%02X%02X%02X" % tuple(sum(p[i] for p in px) // len(px) for i in range(3))
    except Exception:
        return "#101010"


def frame_plate(dst_png, title, bg="#0E1726", fg="#FFFFFF", video_h=608, video_y=520):
    """A 1080x1920 background with a headline above where the video will sit (Reels 'framed' format).
    The headline sits below the top bar (14%), the video above the caption area (bottom 35%)."""
    from PIL import ImageDraw
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from render_slides import font
    img = Image.new("RGB", (1080, 1920), bg)
    d = ImageDraw.Draw(img)
    if title:
        size = 76
        while size >= 48:
            f = font("sans", size, "Bold")
            words, lines, cur = title.split(), [], ""
            for w in words:
                t = (cur + " " + w).strip()
                if d.textlength(t, font=f) <= 1080 - 2 * 96 or not cur:
                    cur = t
                else:
                    lines.append(cur)
                    cur = w
            lines.append(cur)
            lh = round(size * 1.15)
            if len(lines) <= 3:
                break
            size -= 4
        y = max(300, video_y - 40 - lh * len(lines))
        for ln in lines:
            d.text(((1080 - d.textlength(ln, font=f)) / 2, y), ln, fill=fg, font=f)
            y += lh
    img.save(dst_png)
    return dst_png


def fit_video(src, dst, ratio, mode, frame=None):
    """Re-encode to Instagram's sweet spot: H.264 High, 8-bit, AAC 48 kHz, moov first.
    Keeps the source frame rate when it's within 23 to 60 fps (24 and 25 fps footage stays as it is)."""
    tw = 1080
    th = round(tw / ratio)
    th -= th % 2
    if mode == "frame":
        # landscape video full width on a plate with a headline: no blur, nothing cut off
        plate = dst + ".plate.png"
        info = probe_video(src) or {"w": 1920, "h": 1080}
        vh = round(tw * info["h"] / info["w"]) // 2 * 2
        # headline from y=300 (below the top bar), video under it, all above the caption area (bottom 35%)
        title = (frame or {}).get("title", "")
        lines_guess = 0 if not title else min(3, max(1, len(title) // 22 + 1))
        vy = max(520, 300 + lines_guess * 88 + 40) if vh <= 760 else max(270, (th - vh) // 2)
        vy = min(vy, 1248 - vh) // 2 * 2
        frame_plate(plate, title, (frame or {}).get("bg") or edge_colour(src), video_h=vh, video_y=vy)
        cmd = ["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", plate, "-i", src, "-filter_complex",
               f"[1:v]scale={tw}:{vh}[v];[0:v][v]overlay=0:{vy}:shortest=1,format=yuv420p",
               "-map", "1:a?", "-r", fps_arg(src), "-c:v", "libx264", "-profile:v", "high", "-preset", "medium",
               "-crf", "19", "-maxrate", "20M", "-bufsize", "40M", "-color_primaries", "bt709", "-color_trc", "bt709",
               "-colorspace", "bt709", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
               "-movflags", "+faststart", dst]
        r = subprocess.run(cmd, capture_output=True, text=True)
        os.remove(plate)
        if r.returncode != 0:
            raise RuntimeError(r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "ffmpeg failed")
        return dst
    if mode == "crop":
        vf = f"scale={tw}:{th}:force_original_aspect_ratio=increase,crop={tw}:{th}"
    else:
        # blur at a quarter of the size, then scale up: same look, about 10x faster
        sw, sh = (tw // 4) // 2 * 2, (th // 4) // 2 * 2
        vf = (f"split[a][b];[a]scale={sw}:{sh}:force_original_aspect_ratio=increase,crop={sw}:{sh},"
              f"boxblur=10:2,eq=brightness=-0.08,scale={tw}:{th}[bg];[b]scale={tw}:{th}:force_original_aspect_ratio=decrease[fg];"
              f"[bg][fg]overlay=(W-w)/2:(H-h)/2")
    vf += ",zscale=t=bt709:m=bt709:r=tv,format=yuv420p" if has_zscale() and is_hdr(src) else ",format=yuv420p"
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", src, "-filter_complex" if mode != "crop" else "-vf", vf,
           "-r", fps_arg(src), "-c:v", "libx264", "-profile:v", "high", "-preset", "medium", "-crf", "19",
           "-maxrate", "20M", "-bufsize", "40M", "-color_primaries", "bt709", "-color_trc", "bt709",
           "-colorspace", "bt709", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
           "-movflags", "+faststart", dst]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "ffmpeg failed")
    return dst


def fps_arg(src):
    info = probe_video(src) or {}
    f = info.get("fps") or 30
    if info.get("vfr") or not LIMITS["fps_min"] - 0.5 <= f <= LIMITS["fps_max"] + 0.5:
        return "30"
    return f"{f:.3f}".rstrip("0").rstrip(".")


_zs = None


def has_zscale():
    global _zs
    if _zs is None:
        out = subprocess.run(["ffmpeg", "-hide_banner", "-filters"], capture_output=True, text=True).stdout
        _zs = " zscale " in out
    return _zs


def is_hdr(path):
    info = probe_video(path)
    return bool(info and info["color_transfer"] in ("smpte2084", "arib-std-b67"))


# ---------- caption checks ----------

HASHTAG = re.compile(r"(?<![\w&])#(\w+)", re.UNICODE)
MENTION = re.compile(r"(?<![\w.])@([A-Za-z0-9._]{1,30})")


def check_caption(text, post, label):
    if text is None:
        return
    if not text.strip():
        report("warn", post, label, "empty caption: the caption is what Instagram search and Google read")
        return
    n = len(text)
    if n > LIMITS["caption_chars"]:
        report("error", post, label, f"{n} characters: the limit is {LIMITS['caption_chars']}")
    tags = HASHTAG.findall(text)
    if len(tags) > LIMITS["hashtags"]:
        report("error", post, label, f"{len(tags)} hashtags: Instagram allows {LIMITS['hashtags']}; keep the most specific ones")
    if len({t.lower() for t in tags}) < len(tags):
        report("warn", post, label, "the same hashtag appears twice")
    if len(MENTION.findall(text)) > LIMITS["mentions"]:
        report("error", post, label, f"more than {LIMITS['mentions']} @mentions")
    first = text.strip().split("\n")[0]
    if len(first) > LIMITS["fold_chars"]:
        report("warn", post, label, f"first line is {len(first)} characters: the feed shows about {LIMITS['fold_chars']} characters or 2 lines before '... more'; put the hook before that")
    if re.search(r"https?://\S+", text):
        report("warn", post, label, "links in captions aren't clickable on Instagram; say 'link in bio' or use a Story link instead")
    if "\u2014" in text or "\u2013" in text:
        report("warn", post, label, "long dash in the caption: many readers now see it as an AI tell")


# ---------- main ----------

def media_kind(path):
    return "video" if os.path.splitext(path)[1].lower() in VIDEO_EXT else "image"


NUM = re.compile(r"\d[\d.,]*\s?%?")


def check_media(media, fmt, pid, who, base, a, forced, frame=None):
    """Check one list of media (and fix it with --fix). Returns (new list, changed)."""
    changed = False
    if not media:
        report("error", pid, "media" + who, "no media files")
        return media, False
    if fmt == "carousel" and not LIMITS["carousel_min"] <= len(media) <= LIMITS["carousel_max"]:
        report("error", pid, "media" + who, f"{len(media)} items: a carousel takes {LIMITS['carousel_min']} to {LIMITS['carousel_max']}")
    if fmt in ("image", "reel", "story") and len(media) != 1:
        report("error", pid, "media" + who, f"a {fmt} takes exactly one file, found {len(media)}")
    if fmt == "reel" and media_kind(media[0]) != "video":
        report("error", pid, "media" + who, "a Reel needs a video; post a photo as format 'image'")
    fixed_dir = os.path.join(base, "fixed")
    first_ratio, new_media = None, []
    for i, m in enumerate(media):
        path = m if os.path.isabs(m) else os.path.join(base, m)
        label = f"{os.path.basename(m)} #{i + 1}{who}"
        if not os.path.exists(path):
            report("error", pid, label, "file not found")
            new_media.append(m)
            continue
        kind = media_kind(path)
        if kind == "video":
            ratio, probs = check_video(path, fmt, pid, label)
        else:
            ratio, probs = check_image(path, fmt, pid, label, first_ratio)
        if i == 0 and ratio:
            first_ratio = ratio
            if fmt == "carousel" and "ratio" in probs:
                first_ratio = forced or (1.91 if ratio > 1.91 else 0.8)
        target = None
        if fmt in ("reel", "story"):
            target = 9 / 16
        elif "ratio" in probs:
            target = forced or (1.91 if ratio and ratio > 1.91 else 0.8)
        elif forced and kind == "image" and fmt == "image" and ratio and abs(ratio - forced) > 0.01:
            target = forced
            probs.append("forced")
        elif "match" in probs:
            target = first_ratio
        if a.fix and probs and "unreadable" not in probs:
            loss = 1 - min(ratio, target) / max(ratio, target) if (ratio and target) else 0
            mode = a.fit if a.fit != "auto" else ("frame" if frame and kind == "video" and fmt in ("reel", "story") else "auto")
            if mode == "frame" and kind != "video":
                mode = "pad"
            if mode == "auto":
                if kind == "video" and fmt in ("reel", "story") and loss >= 0.12:
                    # landscape or square footage: blurred bars look like a repost, and a blind
                    # centre crop can cut the subject. The user decides.
                    report("error", pid, label, f"this video would lose {loss:.0%} of its width to fill 9:16. Check reel.py frames, then: "
                           "reframe it on the subject in an editor; or --fit crop when the subject stays in the middle; or give the "
                           "post a \"frame\": {\"title\": \"...\"} for a framed Reel (video full width under a headline)")
                    new_media.append(m)
                    continue
                # pictures: crop when it loses less than 12%, otherwise pad
                mode = "crop" if loss < 0.12 else "pad"
            os.makedirs(fixed_dir, exist_ok=True)
            stem = f"{pid}{'-' + who.strip(' ()') if who else ''}-{i + 1:02d}"
            try:
                if kind == "video":
                    out = fit_video(path, os.path.join(fixed_dir, stem + ".mp4"), target or ratio, mode, frame)
                else:
                    out = fit_image(path, os.path.join(fixed_dir, stem + ".jpg"), target, mode)
                new_media.append(rel(out, base))
                changed = True
                report("fixed", pid, label, f"wrote {rel(out, base)} ({mode})")
                continue
            except Exception as e:
                report("error", pid, label, f"fix failed: {e}")
        new_media.append(m)
    return new_media, changed


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("plan")
    ap.add_argument("--fix", action="store_true", help="write fixed copies and update the plan")
    ap.add_argument("--fit", choices=["auto", "crop", "pad", "frame"], default="auto",
                    help="how to change the shape: crop the edges, pad with a blurred copy, frame (landscape video "
                         "on a solid background with the post's frame.title above it), or auto")
    ap.add_argument("--ratio", choices=["4:5", "1:1", "1.91:1"], help="shape for images that need changing (default: the nearest allowed)")
    a = ap.parse_args()
    forced = {"4:5": 0.8, "1:1": 1.0, "1.91:1": 1.91}.get(a.ratio)

    base = os.path.dirname(os.path.abspath(a.plan))
    with open(a.plan, encoding="utf-8") as f:
        plan = json.load(f)
    posts = plan.get("posts", [])
    if not posts:
        sys.exit("plan.json has no posts")
    changed = False
    per_account = {}
    openers = {}

    for p in posts:
        pid = p.get("id", "?")
        fmt = p.get("format")
        if fmt not in ("image", "carousel", "reel", "story"):
            report("error", pid, "format", f"format '{fmt}': use image, carousel, reel or story")
            continue
        new, ch = check_media(p.get("media", []), fmt, pid, "", base, a, forced, p.get("frame"))
        if a.fix and ch:
            p["media"], changed = new, True
        targets = p.get("targets", [])
        for t in targets:
            if t.get("media"):
                new, ch = check_media(t["media"], fmt, pid, f" ({t.get('account')})", base, a, forced, t.get("frame") or p.get("frame"))
                if a.fix and ch:
                    t["media"], changed = new, True

        for who, cover in [("", p.get("cover"))] + [(f" ({t.get('account')})", t.get("cover")) for t in targets if t.get("cover")]:
            if not cover:
                continue
            cpath = cover if os.path.isabs(cover) else os.path.join(base, cover)
            if not os.path.exists(cpath):
                report("error", pid, "cover" + who, "cover file not found")
                continue
            with Image.open(cpath) as im:
                if im.format != "JPEG":
                    report("error", pid, "cover" + who, "the Reel cover must be a JPEG (make it with reel.py cover)")
                if abs(im.width / im.height - 9 / 16) > 0.01:
                    report("warn", pid, "cover" + who, "Reel covers are 9:16; the grid shows the middle 3:4 of it")
        if p.get("frame") and not p.get("own_footage"):
            report("warn", pid, "frame", "a framed Reel is only original with your own footage. Adding a headline or border to "
                   "someone else's clip still reads as a repost to Instagram. Set \"own_footage\": true if you filmed or made it")
        if fmt == "reel" and not p.get("cover"):
            report("warn", pid, "cover", "no cover: Instagram picks a frame; choose one with reel.py frames/cover")

        if fmt == "story":
            if p.get("caption") or any(t.get("caption") for t in targets):
                report("warn", pid, "caption", "Stories have no caption; this text is dropped. Put the words on the image")
            if not p.get("with") and not all(t.get("at") or t.get("now") for t in targets):
                report("warn", pid, "with", "a Story with no time: tie it to a feed post with \"with\" so schedule.py can place it")
        else:
            check_caption(p.get("caption"), pid, "caption")
        if not targets:
            report("warn", pid, "targets", "no accounts yet")
        firsts = {}
        for t in targets:
            cap = t.get("caption") or p.get("caption") or ""
            if t.get("caption") and fmt != "story":
                check_caption(t["caption"], pid, f"caption for {t.get('account')}")
            first = "" if fmt == "story" else cap.strip().split("\n")[0].strip().lower()
            if first and first in firsts and len(targets) > 1:
                report("warn", pid, "captions", f"{t.get('account')} and {firsts[first]} open with the same line; vary the first line per account")
            firsts.setdefault(first, t.get("account"))
            cover_text = ((t.get("alt") or p.get("alt") or [""])[0] or "").lower()
            if fmt != "story" and (first or cover_text):
                for n in {x.strip() for x in NUM.findall(first + " " + cover_text) if any(c.isdigit() for c in x) and len(x.strip()) > 1}:
                    other = openers.get((t.get("account"), n))
                    if other and other != pid:
                        report("warn", pid, "captions", f"opens with {n} on {t.get('account')}, like {other}: two posts in one batch should not lead with the same fact")
                    openers.setdefault((t.get("account"), n), pid)
            day = (t.get("at") or "")[:10]
            if day and fmt != "story":
                key = (t.get("account"), day)
                per_account[key] = per_account.get(key, 0) + 1
        if len(targets) > 1 and fmt != "story" and not any(t.get("media") for t in targets[1:]):
            report("warn", pid, "media", "the same media on several accounts: Instagram's 2026 originality rules cover photos and "
                   "carousels too, so a second upload is likely seen as a repost of the first. Give each account its own version (targets[].media)")
        if p.get("trial") and fmt != "reel":
            report("error", pid, "trial", "Trial posts exist for Reels only")

    for (acct, day), n in per_account.items():
        if n > 25:
            report("warn", "schedule", acct, f"{n} posts on {day}: the API allows at most 100 a day (some docs say 50); this many reads as spam")

    if a.fix and changed:
        shutil.copyfile(a.plan, a.plan + ".bak")
        with open(a.plan, "w", encoding="utf-8") as f:
            json.dump(plan, f, indent=1, ensure_ascii=False)

    order = {"error": 0, "fix": 1, "warn": 2, "fixed": 3}
    issues.sort(key=lambda x: (str(x[1]), order[x[0]]))
    if not issues:
        print("All posts pass.")
    for level, post, item, msg in issues:
        print(f"[{level}] {post} / {item}: {msg}")
    errors = sum(1 for x in issues if x[0] == "error")
    fixes = sum(1 for x in issues if x[0] == "fix") - sum(1 for x in issues if x[0] == "fixed")
    with open(os.path.join(base, "check.json"), "w", encoding="utf-8") as f:
        json.dump([dict(zip(("level", "post", "item", "message"), x)) for x in issues], f, indent=1, ensure_ascii=False)
    if fixes > 0 and not a.fix:
        print(f"\n{fixes} item(s) can be fixed: run again with --fix (originals stay untouched).")
    if errors:
        print(f"\n{errors} error(s) left. Fix them before posting.")
    sys.exit(1 if errors or (fixes > 0 and not a.fix) else 0)


if __name__ == "__main__":
    main()
