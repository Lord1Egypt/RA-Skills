#!/usr/bin/env python3
"""
podcast-slideshow.py — render Ghost Signals podcast episodes as
1920x1080 slideshow MP4s using Kannaka's KAX artwork (the
"Kannaka: Our Journey" drop on kax.ninja-portal.com).

Layout per art slide: the 1024x1024 piece blur-filled to 1920x1080
behind a sharp 1080x1080 center panel, dip-to-black fades between
slides. Slide 0 is a generated cover card (hero art + episode title)
that doubles as the YouTube thumbnail.

Usage:
  python scripts/podcast-slideshow.py 8          # render episode 8
  python scripts/podcast-slideshow.py --all      # render all episodes
  python scripts/podcast-slideshow.py --covers   # regenerate covers only

Episode list comes from workspace/podcasts/episodes.json. Outputs to
workspace/podcasts/renders/GSP-0XX-slideshow.mp4 (+ cover PNG).
Idempotent: finished renders are skipped unless --force.
"""
import json
import math
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PODCASTS = os.path.join(ROOT, "workspace", "podcasts")
ART_DIR = os.path.join(PODCASTS, "art")
RENDERS = os.path.join(PODCASTS, "renders")
EPISODES_JSON = os.path.join(PODCASTS, "episodes.json")

COVER_SECONDS = 6.0
SLIDE_SECONDS = 45.0
FADE = 0.6
FPS = 24
SEG_WORKERS = 5
ART_STRIDE = 4  # art rotation offset between consecutive episodes

FONT_BOLD = "C:/Windows/Fonts/segoeuib.ttf"
FONT_REG = "C:/Windows/Fonts/segoeui.ttf"


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"cmd failed ({p.returncode}): {' '.join(cmd)}\n{p.stderr[-800:]}")
    return p.stdout


def audio_duration(path):
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
               "-of", "default=noprint_wrappers=1:nokey=1", path])
    return float(out.strip())


def load_manifest():
    with open(os.path.join(ART_DIR, "manifest.json"), encoding="utf-8") as f:
        return json.load(f)


def pick_art(manifest, ep_num, count):
    start = ((ep_num - 1) * ART_STRIDE) % len(manifest)
    return [manifest[(start + i) % len(manifest)] for i in range(count)]


def make_cover(ep, hero_path, out_path):
    from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

    W, H = 1920, 1080
    hero = Image.open(hero_path).convert("RGB")

    # background: hero blown up to cover, blurred and darkened
    scale = max(W / hero.width, H / hero.height)
    bg = hero.resize((int(hero.width * scale) + 1, int(hero.height * scale) + 1))
    bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2,
                  (bg.width - W) // 2 + W, (bg.height - H) // 2 + H))
    bg = bg.filter(ImageFilter.GaussianBlur(14))
    bg = ImageEnhance.Brightness(bg).enhance(0.38)
    canvas = bg

    # right panel: the art itself, sharp
    panel = hero.resize((880, 880))
    px, py = W - 880 - 110, (H - 880) // 2
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([px - 4, py - 4, px + 884, py + 884], outline=(185, 166, 238), width=3)
    canvas.paste(panel, (px, py))

    # left text block
    def text_shadow(xy, s, font, fill):
        x, y = xy
        draw.text((x + 3, y + 3), s, font=font, fill=(0, 0, 0))
        draw.text((x, y), s, font=font, fill=fill)

    f_kicker = ImageFont.truetype(FONT_BOLD, 42)
    f_title = ImageFont.truetype(FONT_BOLD, 96)
    f_footer = ImageFont.truetype(FONT_REG, 38)

    tx = 110
    kicker = f"GHOST SIGNALS · EPISODE {ep['num']}"
    text_shadow((tx, 240), kicker, f_kicker, (185, 166, 238))

    # wrap title to the text column (~760px)
    words, lines, cur = ep["title"].split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=f_title) > 760 and cur:
            lines.append(cur)
            cur = w
        else:
            cur = t
    lines.append(cur)
    y = 330
    for line in lines[:4]:
        text_shadow((tx, y), line, f_title, (240, 234, 255))
        y += 112

    text_shadow((tx, 930), "with KANNAKA — kannaka radio", f_footer, (138, 111, 208))

    canvas.save(out_path)
    return out_path


def render_segment(img, dur, out, fade_in, fade_out, is_cover):
    if os.path.exists(out) and os.path.getsize(out) > 10000:
        return out
    fades = []
    if fade_in:
        fades.append(f"fade=t=in:st=0:d={FADE}")
    if fade_out:
        fades.append(f"fade=t=out:st={max(0.0, dur - FADE):.3f}:d={FADE}")
    fade_str = ("," + ",".join(fades)) if fades else ""
    if is_cover:  # already 1920x1080
        vf = f"[0:v]scale=1920:1080,setsar=1{fade_str},format=yuv420p[v]"
    else:
        vf = (
            "[0:v]scale=1920:1080:force_original_aspect_ratio=increase,"
            "crop=1920:1080,boxblur=28:2,eq=brightness=-0.22[bg];"
            "[0:v]scale=-2:1080[fg];"
            f"[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1{fade_str},format=yuv420p[v]"
        )
    run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", str(FPS),
         "-t", f"{dur:.3f}", "-i", img, "-filter_complex", vf, "-map", "[v]",
         "-c:v", "libx264", "-preset", "medium", "-tune", "stillimage",
         "-crf", "20", "-r", str(FPS), out])
    return out


def render_episode(ep, manifest, force=False):
    num = ep["num"]
    tag = f"GSP-{num:03d}"
    final = os.path.join(RENDERS, f"{tag}-slideshow.mp4")
    if os.path.exists(final) and not force:
        print(f"[{tag}] exists, skipping (--force to re-render)")
        return final
    os.makedirs(RENDERS, exist_ok=True)
    workdir = os.path.join(RENDERS, f"{tag}-work")
    os.makedirs(workdir, exist_ok=True)

    total = audio_duration(ep["audio"])
    n_art = max(3, round((total - COVER_SECONDS) / SLIDE_SECONDS))
    art_dur = (total - COVER_SECONDS) / n_art
    arts = pick_art(manifest, num, n_art)
    print(f"[{tag}] {total:.0f}s audio -> cover + {n_art} art slides @ {art_dur:.1f}s")

    cover = os.path.join(RENDERS, f"{tag}-cover.png")
    if not os.path.exists(cover) or force:
        make_cover(ep, os.path.join(ART_DIR, arts[0]["file"]), cover)

    # slide plan: cover first, art slides, last one padded so video > audio
    jobs = [(cover, COVER_SECONDS, os.path.join(workdir, "seg-000.mp4"), False, True, True)]
    for i, a in enumerate(arts):
        dur = art_dur + (1.5 if i == n_art - 1 else 0.0)
        jobs.append((os.path.join(ART_DIR, a["file"]), dur,
                     os.path.join(workdir, f"seg-{i + 1:03d}.mp4"), True, i < n_art - 1, False))

    with ThreadPoolExecutor(max_workers=SEG_WORKERS) as pool:
        futs = [pool.submit(render_segment, img, dur, out, fi, fo, cov)
                for img, dur, out, fi, fo, cov in jobs]
        for f in futs:
            f.result()

    concat_list = os.path.join(workdir, "concat.txt")
    with open(concat_list, "w", encoding="utf-8") as f:
        for _, _, out, _, _, _ in jobs:
            f.write(f"file '{os.path.basename(out)}'\n")
    video_only = os.path.join(workdir, "video.mp4")
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
         "-i", concat_list, "-c", "copy", video_only])
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", video_only, "-i", ep["audio"],
         "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         "-ar", "48000", "-movflags", "+faststart", "-shortest", final])

    vdur = audio_duration(final)
    drift = abs(vdur - total)
    size_mb = os.path.getsize(final) / 1e6
    status = "OK" if drift < 2.5 else "DRIFT!"
    print(f"[{tag}] final {vdur:.1f}s (audio {total:.1f}s, drift {drift:.2f}s) "
          f"{size_mb:.0f} MB -> {final} [{status}]")
    return final


def main():
    with open(EPISODES_JSON, encoding="utf-8") as f:
        episodes = json.load(f)
    manifest = load_manifest()
    force = "--force" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]

    if "--covers" in sys.argv:
        os.makedirs(RENDERS, exist_ok=True)
        for ep in episodes:
            arts = pick_art(manifest, ep["num"], 1)
            cover = os.path.join(RENDERS, f"GSP-{ep['num']:03d}-cover.png")
            make_cover(ep, os.path.join(ART_DIR, arts[0]["file"]), cover)
            print(f"cover -> {cover}")
        return

    if "--all" in sys.argv:
        targets = episodes
    else:
        wanted = {int(a) for a in args}
        targets = [e for e in episodes if e["num"] in wanted]
        if not targets:
            print("usage: podcast-slideshow.py <num...> | --all [--force] | --covers")
            sys.exit(64)
    for ep in targets:
        render_episode(ep, manifest, force=force)


if __name__ == "__main__":
    main()
