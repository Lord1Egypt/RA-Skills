#!/usr/bin/env python3
"""Show the batch the way Pinterest will: in the home feed at real size, and each pin's close-up
with its title, description, link and board, plus the schedule. One page to approve.

    python3 scripts/preview.py plan.json --out preview/

Writes preview/index.html (self-contained folder, open it in a browser) and preview/preview.png
(the feed at real size: look at it yourself before showing the user; if a headline can't be read
there, it can't be read on a phone). Video pins play muted, as they do in the feed.
"""
import argparse, html, json, os, shutil, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pinlib as P  # noqa: E402

FEED_W = 236       # Pinterest's column width
GAP = 16


def esc(s):
    return html.escape(str(s or ""))


def poster(path):
    from PIL import Image
    if path.lower().endswith(P.VIDEO_EXT):
        return P.frame_at(path, 0.0)      # the first frame is the cover
    return P.open_image(path)


def feed_title(d, title, f):
    """The title as the feed shows it: at most two lines of the column, cut with an ellipsis."""
    words, lines, cur = title.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= FEED_W - 8:
            cur = t
        else:
            lines.append(cur)
            cur = w
            if len(lines) == 2:
                break
    if len(lines) < 2 and cur:
        lines.append(cur)
    if len(lines) == 2 and " ".join(lines) != title:
        while d.textlength(lines[1] + "…", font=f) > FEED_W - 8 and " " in lines[1]:
            lines[1] = lines[1].rsplit(" ", 1)[0]
        lines[1] += "…"
    return lines[:2]


def feed_png(pins, base, out):
    from PIL import Image, ImageDraw, ImageFont
    cols = min(5, max(3, len(pins)))
    heights = [0] * cols
    tiles = []
    for p in pins:
        im = poster(P.resolve(base, p["file"]))
        if im is None:
            continue
        th = int(FEED_W * im.height / im.width)
        c = heights.index(min(heights))
        tiles.append((c, heights[c], im.resize((FEED_W, th)), p))
        heights[c] += th + 66
    W = cols * (FEED_W + GAP) + GAP
    H = max(heights) + GAP * 2
    sheet = Image.new("RGB", (W, H), "#FFFFFF")
    d = ImageDraw.Draw(sheet)
    try:
        f = ImageFont.truetype(os.path.join(os.path.dirname(__file__), "..", "fonts", "Inter.ttf"), 13)
        f.set_variation_by_name("SemiBold")
    except Exception:
        f = ImageFont.load_default()
    for c, y, im, p in tiles:
        x = GAP + c * (FEED_W + GAP)
        mask = Image.new("L", im.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=16, fill=255)
        sheet.paste(im, (x, y + GAP), mask)
        if p.get("format") == "video":
            secs = round(P.duration(P.ffprobe(P.resolve(base, p["file"]))))
            badge = f"{secs // 60}:{secs % 60:02d}"
            by = y + GAP + im.height - 34
            d.rounded_rectangle([x + 10, by, x + 18 + d.textlength(badge, font=f) + 8, by + 24], radius=12, fill="#000000")
            d.text((x + 18, by + 4), badge, font=f, fill="#FFFFFF")
        for i, ln in enumerate(feed_title(d, p.get("title", ""), f)):
            d.text((x + 4, y + GAP + im.height + 8 + i * 17), ln, font=f, fill="#111111")
    sheet.save(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("plan")
    ap.add_argument("--out", default="preview")
    a = ap.parse_args()
    base = os.path.dirname(os.path.abspath(a.plan))
    plan = P.load_plan(a.plan)
    out = a.out if os.path.isabs(a.out) else os.path.join(base, a.out)
    mdir = os.path.join(out, "media")
    os.makedirs(mdir, exist_ok=True)
    missing = [p.get("id") for p in plan["pins"] if not p.get("file") or not os.path.exists(P.resolve(base, p["file"]))]
    if missing:
        print("not in the preview (media file missing): " + ", ".join(map(str, missing)))
    pins = sorted([p for p in plan["pins"] if p.get("id") not in missing], key=lambda p: p.get("at") or "")
    for p in pins:
        p["format"] = P.fmt_of(p)
    feed_png(pins, base, os.path.join(out, "preview.png"))

    cards, closeups = [], []
    for p in pins:
        src = P.resolve(base, p["file"])
        name = p["id"] + os.path.splitext(src)[1].lower()
        shutil.copyfile(src, os.path.join(mdir, name))
        acc = plan["accounts"].get(p.get("account"), {})
        url = P.link_of(p, plan["links"])[0]
        url = url if P.is_url(url) else ""
        media = (f'<video src="media/{esc(name)}" autoplay muted loop playsinline></video>' if p["format"] == "video"
                 else f'<img src="media/{esc(name)}" alt="{esc(p.get("alt"))}">')
        title = p.get("title", "")
        cards.append(f'<a class="card" href="#{esc(p["id"])}">{media}<div class="t">{esc(title)}</div></a>')
        d = P.parse_local(p.get("at"))
        when = d.strftime("%a %d %b %Y, %H:%M") if d else "not scheduled yet"
        closeups.append(f'''<section class="close" id="{esc(p["id"])}">
<div class="m">{media}</div>
<div class="side">
 <div class="row"><span class="dom">{esc(P.domain(url)) or "no link"}</span><span class="save">Save</span></div>
 <h2>{esc(title)}</h2>
 <p>{esc(p.get("description")).replace(chr(10), "<br>")}</p>
 <dl>
  <dt>Account</dt><dd>{esc(acc.get("handle") or p.get("account"))}</dd>
  <dt>Board</dt><dd>{esc(p.get("board"))}</dd>
  <dt>Link</dt><dd>{f'<a href="{esc(url)}">{esc(url)}</a>' if url else "none"}</dd>
  <dt>Goes live</dt><dd>{esc(when)} ({esc((acc.get("timezone") or plan.get("timezone") or "").split("/")[-1].replace("_", " "))})</dd>
  <dt>Alt text</dt><dd>{esc(p.get("alt")) or "none"}{" (added in Pinterest after posting)" if p.get("alt") else ""}</dd>
  <dt>Format</dt><dd>{esc(p["format"])}</dd>
 </dl>
</div></section>''')

    doc = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Pin preview</title>
<style>
:root{{--bg:#fff;--fg:#111;--muted:#5f5f5f;--line:#e9e9e9;--red:#e60023}}
@media (prefers-color-scheme:dark){{:root{{--bg:#121212;--fg:#f1f1f1;--muted:#a5a5a5;--line:#2a2a2a}}}}
body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,sans-serif}}
main{{max-width:1180px;margin:0 auto;padding:24px 16px 64px}}
h1{{font-size:22px;margin:0 0 4px}} .lede{{color:var(--muted);margin:0 0 20px}}
.feed{{columns:{FEED_W}px;column-gap:{GAP}px}}
.card{{display:block;break-inside:avoid;margin:0 0 18px;color:inherit;text-decoration:none}}
.card img,.card video{{width:100%;border-radius:16px;display:block}}
.card .t{{font-weight:600;font-size:13px;padding:6px 4px 0;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}}
.close{{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:0;border:1px solid var(--line);
border-radius:32px;overflow:hidden;margin:40px auto 0;max-width:900px;box-shadow:0 1px 20px rgba(0,0,0,.08)}}
.close .m img,.close .m video{{width:100%;display:block}}
.side{{padding:24px 28px}} .row{{display:flex;justify-content:space-between;align-items:center}}
.dom{{color:var(--muted);text-decoration:underline}} .save{{background:var(--red);color:#fff;border-radius:24px;padding:10px 16px;font-weight:700}}
.side h2{{font-size:26px;line-height:1.2;margin:18px 0 10px}}
dl{{display:grid;grid-template-columns:auto 1fr;gap:6px 14px;margin:20px 0 0;font-size:14px}}
dt{{color:var(--muted)}} dd{{margin:0;overflow-wrap:anywhere}} a{{color:inherit}}
@media (max-width:720px){{.close{{grid-template-columns:1fr;border-radius:20px}}}}
</style></head><body><main>
<h1>{len(pins)} pins, ready for a yes</h1>
<p class="lede">The feed at real size first (titles are cut where Pinterest cuts them), then each pin as it opens.</p>
<div class="feed">{"".join(cards)}</div>
{"".join(closeups)}
</main></body></html>'''
    with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"wrote {P.rel(os.path.join(out, 'index.html'), os.getcwd())} and preview.png (look at preview.png first)")


if __name__ == "__main__":
    main()
