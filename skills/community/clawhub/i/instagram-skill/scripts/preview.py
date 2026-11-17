#!/usr/bin/env python3
"""Show every post the way Instagram will, before anything is posted.

    python3 scripts/preview.py plan.json --out preview/ [--grid my-grid.png]

Writes preview/index.html (open it in a browser) and preview/preview.png (the same, as one image
the agent can look at). For each post: the feed view with the caption cut where Instagram adds
"... more", every slide in order, the Reel cover, the accounts and times, and the in-app
checklist. On top: the profile grid as it will look after the batch, newest first, with the 3:4
crop Instagram applies. --grid adds a screenshot of the current grid below the new posts.
Needs Python 3.8+ and Pillow; ffmpeg for video thumbnails.
"""
import argparse, html, json, os, shutil, subprocess, sys
from datetime import datetime

from PIL import Image, ImageDraw, ImageOps

try:  # iPhone .heic photos, when pillow-heif is installed
    from pillow_heif import register_heif_opener
    register_heif_opener()
except ImportError:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
FOLD = 125
VIDEO_EXT = {".mp4", ".mov", ".m4v", ".webm", ".mkv", ".avi"}


def font(size, weight="Regular"):
    from render_slides import font as rfont
    return rfont("sans", size, weight)


def is_video(p):
    return os.path.splitext(p)[1].lower() in VIDEO_EXT


def thumb(src, dst, box=(540, 960)):
    """A small JPEG of an image or of a video's first second."""
    if is_video(src):
        if not shutil.which("ffmpeg"):
            img = Image.new("RGB", (540, 960), "#222")
        else:
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "1", "-i", src, "-frames:v", "1",
                            "-vf", "scale=540:-2", dst], capture_output=True)
            img = Image.open(dst).convert("RGB") if os.path.exists(dst) else Image.new("RGB", (540, 960), "#222")
    else:
        with Image.open(src) as im:
            img = ImageOps.exif_transpose(im).convert("RGB")
    img.thumbnail(box, Image.LANCZOS)
    img.save(dst, "JPEG", quality=85)
    return img


def fold(caption):
    """(visible, hidden?) the way the feed shows a caption: about 125 characters or 2 lines."""
    text = (caption or "").strip()
    lines = text.split("\n")
    shown = "\n".join(lines[:2])
    cut = len(lines) > 2
    if len(shown) > FOLD:
        sp = shown.rfind(" ", 0, FOLD)
        shown = shown[: sp if sp > 60 else FOLD]
        cut = True
    return shown, cut


def when(at, tz):
    if not at:
        return "not scheduled"
    try:
        d = datetime.fromisoformat(at.replace("Z", "+00:00"))
        return d.strftime("%a %d %b, %H:%M") + (f" ({tz})" if tz and not at.endswith("Z") else "")
    except ValueError:
        return at


def grid_tile(img, size=300):
    """What the profile grid shows: the middle 3:4 of the post."""
    w, h = img.size
    tw = min(w, round(h * 3 / 4))
    th = min(h, round(w * 4 / 3))
    x, y = (w - tw) // 2, (h - th) // 2
    return img.crop((x, y, x + tw, y + th)).resize((size, round(size * 4 / 3)), Image.LANCZOS)


# ---------- PNG (for the agent) ----------

def draw_story_card(first, handle, width=540):
    """Stories are full screen: a progress bar and the handle on top, a reply bar at the bottom."""
    h = round(width * 16 / 9)
    card = ImageOps.fit(first.copy(), (width, h), Image.LANCZOS).convert("RGBA")
    shade = Image.new("RGBA", card.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shade)
    for i in range(110):
        sd.line([(0, i), (width, i)], fill=(0, 0, 0, round(120 * (1 - i / 110))))
    card = Image.alpha_composite(card, shade).convert("RGB")
    d = ImageDraw.Draw(card)
    d.rounded_rectangle([10, 10, width - 10, 13], radius=2, fill=(255, 255, 255))
    d.ellipse([14, 24, 46, 56], fill="#DDDDDD")
    d.text((56, 30), handle.lstrip("@"), fill="white", font=font(20, "SemiBold"))
    d.rounded_rectangle([14, h - 58, width - 70, h - 18], radius=20, outline="white", width=2)
    d.text((32, h - 49), "Send message", fill="white", font=font(18))
    return card


def draw_feed_card(first, caption, handle, fmt, count, width=540):
    if fmt == "story":
        return draw_story_card(first, handle, width)
    media = first.copy()
    if fmt == "story":
        mh = round(width * 16 / 9)
    elif fmt == "reel":
        mh = round(width * 5 / 4)  # the main feed shows Reels cropped to 4:5
    else:
        r = max(0.8, min(1.91, media.width / media.height))
        mh = round(width / r)
    media = ImageOps.fit(media, (width, mh), Image.LANCZOS)
    shown, cut = fold(caption)
    f, fb, fs = font(20), font(20, "SemiBold"), font(17)
    tmp = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    words = (handle + " " + shown.replace("\n", " \n ")).split(" ")
    lines, cur = [], ""
    for w in words:
        if w == "\n":
            lines.append(cur)
            cur = ""
            continue
        t = (cur + " " + w).strip()
        if tmp.textlength(t, font=f) <= width - 28:
            cur = t
        else:
            lines.append(cur)
            cur = w
    lines.append(cur + (" ... more" if cut else ""))
    head, icons = 56, 46
    hgt = head + mh + icons + 30 * len(lines) + 20
    card = Image.new("RGB", (width, hgt), "white")
    d = ImageDraw.Draw(card)
    d.ellipse([12, 12, 44, 44], fill="#DDDDDD")
    d.text((54, 18), handle.lstrip("@"), fill="#111", font=fb)
    card.paste(media, (0, head))
    y = head + mh + 10
    for i, cx in enumerate((20, 62, 104)):
        d.ellipse([cx, y + 2, cx + 24, y + 26], outline="#111", width=2)
    d.rectangle([width - 40, y + 2, width - 20, y + 26], outline="#111", width=2)
    if fmt == "carousel" and count > 1:
        dots = min(count, 9)
        sx = width // 2 - dots * 6
        for i in range(dots):
            d.ellipse([sx + i * 12, y + 10, sx + i * 12 + 6, y + 16], fill="#1D9BF0" if i == 0 else "#BBBBBB")
        label = f"1/{count}"
        lw = d.textlength(label, font=fs)
        d.rounded_rectangle([width - lw - 34, head + 12, width - 12, head + 42], radius=15, fill=(0, 0, 0))
        d.text((width - lw - 23, head + 15), label, fill="white", font=fs)
    if fmt == "reel":
        d.text((14, head + mh - 34), "Reel (feed shows the middle 4:5)", fill="white", font=fb)
    y += icons
    for i, ln in enumerate(lines):
        if i == 0 and ln.startswith(handle):
            d.text((14, y), handle, fill="#111", font=fb)
            d.text((14 + d.textlength(handle + " ", font=fb), y), ln[len(handle):].strip(), fill="#111", font=f)
        elif ln.endswith(" ... more"):
            body = ln[: -len(" ... more")]
            d.text((14, y), body, fill="#111", font=f)
            d.text((14 + d.textlength(body + " ", font=f), y), "... more", fill="#8E8E8E", font=f)
        else:
            d.text((14, y), ln, fill="#111", font=f)
        y += 30
    return card


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("plan")
    ap.add_argument("--out", default="preview")
    ap.add_argument("--grid", help="screenshot of the current profile grid (optional)")
    a = ap.parse_args()
    base = os.path.dirname(os.path.abspath(a.plan))
    with open(a.plan, encoding="utf-8") as f:
        plan = json.load(f)
    out = a.out if os.path.isabs(a.out) else os.path.join(base, a.out)
    tdir = os.path.join(out, "media")
    os.makedirs(tdir, exist_ok=True)
    accounts = plan.get("accounts", {})
    brand = plan.get("brand", {})
    tz = plan.get("timezone", "")
    checks = None
    cj = os.path.join(base, "check.json")
    if os.path.exists(cj):
        with open(cj, encoding="utf-8") as f:
            checks = json.load(f)

    def P(x):
        return x if os.path.isabs(x) else os.path.join(base, x)

    posts_html, cards, tiles = [], [], {}
    acc_order = list(accounts) or ["_"]

    def media_for(pid, key, files):
        thumbs, imgs = [], []
        for i, m in enumerate(files):
            dst = os.path.join(tdir, f"{pid}{key}-{i + 1:02d}.jpg")
            if os.path.exists(P(m)):
                imgs.append(thumb(P(m), dst))
                thumbs.append(os.path.relpath(dst, out))
        return thumbs, imgs

    for p in plan.get("posts", []):
        pid, fmt = p.get("id", "post"), p.get("format", "image")
        targets = p.get("targets", []) or [{"account": acc_order[0]}]
        base_thumbs, base_imgs = media_for(pid, "", p.get("media", []))
        cover_rel = cover_img = None
        if p.get("cover") and os.path.exists(P(p["cover"])):
            dst = os.path.join(tdir, f"{pid}-cover.jpg")
            cover_img, cover_rel = thumb(P(p["cover"]), dst), os.path.relpath(os.path.join(tdir, f"{pid}-cover.jpg"), out)
        phones, strips, rows = "", "", ""
        for t in targets:
            key = t.get("account") or "_"
            acc = accounts.get(key, {})
            handle = acc.get("handle") or brand.get("handle") or "@yourhandle"
            if t.get("media"):
                thumbs, imgs = media_for(pid, "-" + key, t["media"])
            else:
                thumbs, imgs = base_thumbs, base_imgs
            if not imgs:
                continue
            c_img, c_rel = cover_img, cover_rel
            if t.get("cover") and os.path.exists(P(t["cover"])):
                dst = os.path.join(tdir, f"{pid}-{key}-cover.jpg")
                c_img, c_rel = thumb(P(t["cover"]), dst), os.path.relpath(dst, out)
            cap = "" if fmt == "story" else (t.get("caption") or p.get("caption", ""))
            first = c_img if (fmt == "reel" and c_img is not None) else imgs[0]
            cards.append((f"{pid} {handle}", draw_feed_card(first, cap, handle, fmt, len(imgs))))
            if fmt != "story":
                tiles.setdefault(key, []).append((t.get("at") or "", grid_tile(c_img or imgs[0])))
            shown, cut = fold(cap)
            ratio = "9/16" if fmt == "story" else "4/5" if fmt == "reel" else f"{max(0.8, min(1.91, imgs[0].width / imgs[0].height)):.3f}"
            main_img = c_rel if (fmt == "reel" and c_rel) else thumbs[0]
            count = f'<span class="count">1/{len(imgs)}</span>' if fmt == "carousel" else ""
            capdiv = "" if fmt == "story" else (f'<div class="cap"><b>{html.escape(handle.lstrip("@"))}</b> '
                                                f'{html.escape(shown).replace(chr(10), "<br>")}{" <span class=more>... more</span>" if cut else ""}</div>')
            phones += (f'<div class="phone"><div class="hd"><span class="av"></span><b>{html.escape(handle.lstrip("@"))}</b>'
                       f'<span class="when">{html.escape(when(t.get("at"), acc.get("timezone") or tz))}</span></div>'
                       f'<div class="media" style="aspect-ratio:{ratio}"><img src="{html.escape(main_img)}">{count}</div>{capdiv}</div>')
            if t.get("media") or not strips:
                figs = "".join(f'<figure><img src="{html.escape(x)}" loading="lazy"><figcaption>{i + 1}</figcaption></figure>' for i, x in enumerate(thumbs))
                if c_rel:
                    figs = f'<figure><img src="{html.escape(c_rel)}"><figcaption>cover</figcaption></figure>' + figs
                strips += f'<p class="note">{html.escape(handle)}{" (own version)" if t.get("media") else ""}</p><div class="strip">{figs}</div>'
            if fmt != "story":
                rows += f'<h3>Caption on {html.escape(handle)}</h3><pre>{html.escape(cap)}</pre>'
        if not phones:
            continue
        issues = [c for c in (checks or []) if c.get("post") == pid and c.get("level") in ("error", "fix", "warn")]
        issue_html = "".join(f'<li class="{c["level"]}"><b>{c["level"]}</b> {html.escape(c["item"])}: {html.escape(c["message"])}</li>'
                             for c in issues) or ('<li class="ok">All checks pass.</li>' if checks is not None
                                                  else '<li class="warn"><b>not checked</b> run scripts/ig_check.py plan.json first</li>')
        todo = "".join(f"<li>{html.escape(x)}</li>" for x in p.get("checklist", [])) or "<li>Nothing to add in the app.</li>"
        posts_html.append(f"""
<section class="post">
 <h2>{html.escape(pid)} <span class="fmt">{fmt}</span></h2>
 <div class="row">{phones}</div>
 <div class="side">{rows}
  <h3>Checks</h3><ul class="checks">{issue_html}</ul>
  <h3>Add in the Instagram app after posting</h3><ul>{todo}</ul>
 </div>
 {strips}
</section>""")

    grid_html, grid_imgs = "", []
    old = None
    if a.grid and os.path.exists(a.grid):
        old = Image.open(a.grid).convert("RGB")
        shutil.copyfile(a.grid, os.path.join(tdir, "current-grid" + os.path.splitext(a.grid)[1]))
    for key in tiles:
        imgs = [g for _, g in sorted(tiles[key], key=lambda x: x[0], reverse=True)]
        if not grid_imgs:
            grid_imgs = imgs
        for i, g in enumerate(imgs):
            g.save(os.path.join(tdir, f"grid-{key}-{i + 1:02d}.jpg"), "JPEG", quality=88)
        handle = accounts.get(key, {}).get("handle") or brand.get("handle") or ""
        grid_html += (f'<div class="gridwrap"><p class="note">{html.escape(handle)}</p><div class="grid">'
                      + "".join(f'<img src="media/grid-{key}-{i + 1:02d}.jpg">' for i in range(len(imgs))) + "</div></div>")
    old_html = f'<p class="note">Your current grid continues below:</p><img class="old" src="media/current-grid{os.path.splitext(a.grid)[1]}">' if old else ""

    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Instagram preview</title><style>
:root{{--fg:#111;--muted:#737373;--line:#DBDBDB;--bg:#FAFAFA;--card:#fff;--blue:#0095F6}}
body{{margin:0;font:15px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;background:var(--bg);color:var(--fg)}}
main{{max-width:1100px;margin:0 auto;padding:24px 16px 80px}}
h1{{font-size:22px;margin:0 0 4px}} .lede{{color:var(--muted);margin:0 0 24px}}
.grids{{display:flex;gap:28px;flex-wrap:wrap}} .gridwrap{{flex:1;min-width:240px;max-width:420px}} .grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:3px}} .when{{margin-left:auto;color:var(--muted);font-size:12px}} .row .phone{{flex:0 1 360px}} .side{{margin-top:16px}} .grid img{{width:100%;display:block}}
.old{{max-width:420px;width:100%;margin-top:3px;opacity:.75}} .note{{color:var(--muted);font-size:13px}}
.post{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:20px;margin:28px 0}}
.post h2{{margin:0 0 14px;font-size:18px}} .fmt{{font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);border:1px solid var(--line);border-radius:99px;padding:2px 8px;margin-left:6px}}
.row{{display:flex;gap:28px;flex-wrap:wrap}} .phone{{width:360px;max-width:100%;border:1px solid var(--line);border-radius:10px;overflow:hidden;background:#fff}}
.hd{{display:flex;align-items:center;gap:10px;padding:10px 12px}} .av{{width:30px;height:30px;border-radius:50%;background:#ddd;display:inline-block}}
.media{{position:relative;background:#000}} .media img{{width:100%;height:100%;object-fit:cover;display:block}}
.count{{position:absolute;top:10px;right:10px;background:rgba(0,0,0,.6);color:#fff;font-size:12px;border-radius:99px;padding:2px 8px}}
.cap{{padding:10px 12px 14px;font-size:14px}} .more{{color:var(--muted)}}
.side{{flex:1;min-width:280px}} .side h3{{font-size:13px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);margin:18px 0 6px}} .side h3:first-child{{margin-top:0}}
table{{border-collapse:collapse;width:100%;font-size:14px}} td{{border-top:1px solid var(--line);padding:6px 8px 6px 0;vertical-align:top}}
pre{{white-space:pre-wrap;font:inherit;background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:10px;margin:0}}
.checks{{padding-left:18px}} .checks .error b{{color:#ED4956}} .checks .fix b{{color:#E5A00D}} .checks .warn b{{color:#8E8E8E}} .checks .ok{{color:#2E7D32}}
.strip{{display:flex;gap:8px;overflow-x:auto;margin-top:16px;padding-bottom:6px}} .strip figure{{margin:0;flex:0 0 auto}}
.strip img{{height:220px;border-radius:6px;display:block}} .strip figcaption{{font-size:12px;color:var(--muted);text-align:center}}
@media (prefers-color-scheme:dark){{:root{{--fg:#F5F5F5;--muted:#A8A8A8;--line:#363636;--bg:#000;--card:#121212}} .phone,.phone .cap{{background:#000;color:#F5F5F5}}}}
</style></head><body><main>
<h1>Instagram preview</h1><p class="lede">{len(posts_html)} post(s). Nothing has been posted. Check the grid, the feed view and the captions, then say yes, change something, or cancel.</p>
<h3>Profile grid after this batch (newest first, as the grid crops it)</h3><div class="grids">{grid_html}</div>{old_html}
{''.join(posts_html)}
</main></body></html>"""
    with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)

    # one PNG: grid on the left, feed cards on the right
    gw = 3 * 180 + 2 * 4
    grid_canvas = None
    if tiles:
        blocks = []
        for key in tiles:
            imgs = [g for _, g in sorted(tiles[key], key=lambda x: x[0], reverse=True)]
            rows = (len(imgs) + 2) // 3
            blk = Image.new("RGB", (gw, 34 + rows * 244), "#EFEFEF")
            ImageDraw.Draw(blk).text((0, 2), accounts.get(key, {}).get("handle") or key, fill="#555", font=font(20, "SemiBold"))
            for i, g in enumerate(imgs):
                blk.paste(g.resize((180, 240)), ((i % 3) * 184, 34 + (i // 3) * 244))
            blocks.append(blk)
        grid_canvas = Image.new("RGB", (gw, sum(b.height for b in blocks) + 24 * (len(blocks) - 1)), "#EFEFEF")
        y = 0
        for b in blocks:
            grid_canvas.paste(b, (0, y))
            y += b.height + 24
    pad = 24
    col_h = max([c.height for _, c in cards] + [grid_canvas.height if grid_canvas else 0])
    total_w = pad + (gw + pad if grid_canvas else 0) + len(cards) * (540 + pad)
    sheet = Image.new("RGB", (total_w, col_h + 2 * pad + 40), "#EFEFEF")
    d = ImageDraw.Draw(sheet)
    x = pad
    if grid_canvas:
        d.text((x, pad - 4), "Grid", fill="#333", font=font(22, "SemiBold"))
        sheet.paste(grid_canvas, (x, pad + 32))
        x += gw + pad
    for pid, c in cards:
        d.text((x, pad - 4), pid, fill="#333", font=font(22, "SemiBold"))
        sheet.paste(c, (x, pad + 32))
        x += 540 + pad
    if sheet.width > 4000:
        sheet = sheet.resize((4000, round(sheet.height * 4000 / sheet.width)), Image.LANCZOS)
    sheet.save(os.path.join(out, "preview.png"))
    print(f"wrote {os.path.join(out, 'index.html')} and preview.png ({len(cards)} posts)")


if __name__ == "__main__":
    main()
