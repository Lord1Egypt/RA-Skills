#!/usr/bin/env python3
"""Render Pinterest pins (1000x1500, 2:3) from the user's own photos and a pins.json spec.

    python3 scripts/render_pins.py pins.json --out pins/

Spec (paths relative to pins.json):

{
  "brand": {"name": "Night Sky Notes", "site": "nightskynotes.com", "logo": "media/logo.png",
            "font": "serif" | "sans",
            "colors": {"bg": "#0E1220", "fg": "#F5F1E8", "accent": "#F2C14E"}},
  "pins": [
    {"id": "full-moon", "layout": "photo", "image": "media/moon.jpg", "focus": [0.5, 0.4],
     "headline": "Why we only ever see one side of the Moon", "sub": "Tidal locking, explained"},
    {"id": "phases", "layout": "grid", "headline": "The 8 Moon phases, in order",
     "tiles": [{"image": "media/p1.jpg", "label": "New Moon"}, ...], "cols": 2},
    {"id": "month", "layout": "fact", "big": "29.5", "headline": "days from one new Moon to the next",
     "image": "media/crescent.jpg"},
    {"id": "list", "layout": "list", "headline": "Moon phases cheat sheet",
     "items": ["New Moon: dark side faces us", "..."], "image": "media/moon.jpg"},
    {"id": "split", "layout": "split", "image": "media/pad.jpg", "headline": "...", "sub": "..."},
    {"id": "clean", "layout": "plain", "image": "media/product.jpg"}
  ]
}

Layouts (the design rules Pinterest itself recommends: vertical 2:3, the headline at the top and
readable on a phone, the subject shown in a real setting, a small logo, nothing that looks like an ad):
- photo: the photo fills the pin, the headline sits in a band at the top ("band": "top" | "bottom").
- split: photo in the top 62%, headline and sub in a solid block under it.
- grid:  headline at the top, 2 to 8 labelled tiles (steps, phases, options, before/after).
- fact:  one big number or word over a darkened photo, the headline under it.
- list:  headline, then 3 to 7 short numbered lines; an optional photo strip at the bottom.
- plain: the photo alone, cropped to 2:3 (a product or lifestyle photo that needs no words).

Every pin gets the site name (or logo) small at the bottom; never a big logo.
`focus` is where the subject is, as fractions of the photo's width and height (crop keeps it in).
Writes pins/<id>.jpg (sRGB JPEG, no metadata), pins/contact-sheet.jpg and pins/manifest.json with
each pin's headline size at feed width, so pin_check.py can tell whether it reads on a phone.
"""
import argparse, json, os, re, shutil, subprocess, sys, urllib.request

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pinlib as P  # noqa: E402

LANCZOS = P.LANCZOS

W, H = 1000, 1500
S = 2                      # render at 2x and downscale: crisp text
FEED_W = 236               # a pin's width in the home feed on a phone and desktop grid
MARGIN = 64
HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "..", "fonts")
FONT_FILES = {
    "sans": ("Inter.ttf", "ofl/inter/Inter%5Bopsz,wght%5D.ttf"),
    "serif": ("InstrumentSerif-Regular.ttf", "ofl/instrumentserif/InstrumentSerif-Regular.ttf"),
}
DEFAULT_COLORS = {"bg": "#F6F1E7", "fg": "#1B1A17", "accent": "#B4441E"}
WARNINGS = []


def warn(msg):
    WARNINGS.append(msg)
    print("warning: " + msg, file=sys.stderr)


# ---------- fonts ----------

CUSTOM_FONT = {}        # kind -> a font file the user chose (brand.font_file), e.g. for CJK or Arabic


def font_path(kind):
    if kind in CUSTOM_FONT:
        return CUSTOM_FONT[kind]
    name, remote = FONT_FILES[kind]
    path = os.path.join(FONTS, name)
    if os.path.exists(path) and os.path.getsize(path) > 10000:
        return path
    os.makedirs(FONTS, exist_ok=True)   # some registries strip binary files: fetch the open font once
    url = "https://raw.githubusercontent.com/google/fonts/main/" + remote
    part = path + ".part"
    try:
        urllib.request.urlretrieve(url, part)
    except Exception:
        if shutil.which("curl"):
            subprocess.run(["curl", "-sfL", url, "-o", part], check=False)
    if not os.path.exists(part) or os.path.getsize(part) < 10000:
        if os.path.exists(part):
            os.remove(part)
        sys.exit(f"Font {name} missing and could not be downloaded from {url}")
    os.replace(part, path)
    return path


def missing_glyphs(text, f):
    """Characters the font can't draw (they'd show as empty boxes): emoji, CJK in a Latin font...
    A character renders exactly like the font's 'missing' box when the font has no glyph for it."""
    def ink(ch):
        size = max(8, int(getattr(f, "size", 40) * 2))
        im = Image.new("L", (size * 2, size * 2))
        ImageDraw.Draw(im).text((size // 2, size // 2), ch, font=f, fill=255)
        return im.tobytes()
    try:
        notdef = ink("\uffff")
    except Exception:
        return []
    out = []
    for ch in sorted(set(str(text))):
        if ch.isspace() or unicodedata_category(ch).startswith(("C", "Z")):
            continue
        try:
            if ink(ch) == notdef:
                out.append(ch)
        except Exception:
            out.append(ch)
    return out


def unicodedata_category(ch):
    import unicodedata
    return unicodedata.category(ch)


_cache = {}


def font(kind, size, weight="Regular"):
    key = (kind, size, weight)
    if key not in _cache:
        f = ImageFont.truetype(font_path(kind), size)
        if kind == "sans":
            try:
                f.set_variation_by_name(weight)
            except Exception:
                pass
        _cache[key] = f
    return _cache[key]


def hexcolor(v, fallback):
    v = (v or "").strip().lstrip("#")
    if re.fullmatch(r"[0-9a-fA-F]{6}", v):
        return "#" + v.upper()
    if re.fullmatch(r"[0-9a-fA-F]{3}", v):
        return "#" + "".join(c * 2 for c in v).upper()
    return fallback


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def luminance(h):
    def ch(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(c) for c in rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


# ---------- images ----------

def load(base, rel, label="pin"):
    if not isinstance(rel, str) or not rel:
        sys.exit(f"{label}: an image path is missing")
    path = P.resolve(base, rel)
    if not os.path.exists(path):
        sys.exit(f"{label}: image not found: {rel}")
    return P.open_image(path)


def load_logo(base, rel):
    path = P.resolve(base, rel)
    if not os.path.exists(path):
        sys.exit(f"logo not found: {rel}")
    im = ImageOps.exif_transpose(Image.open(path))
    return im.convert("RGBA")     # keeps transparency: pasted with its own alpha


def cover(im, w, h, focus=(0.5, 0.5), label=""):
    """Crop-to-fill around the subject. Warns when the photo is upscaled a lot (it will look soft)."""
    scale = max(w / im.width, h / im.height)
    if scale > 1.6 * S:
        warn(f"{label}: the photo is small for this space ({im.width}x{im.height}); it will look soft. Use a larger original.")
    nw, nh = max(w, round(im.width * scale)), max(h, round(im.height * scale))
    im = im.resize((nw, nh), LANCZOS)
    fx, fy = focus
    left = min(max(0, round(fx * nw - w / 2)), nw - w)
    top = min(max(0, round(fy * nh - h / 2)), nh - h)
    return im.crop((left, top, left + w, top + h))


# ---------- text ----------

def wrap(draw, text, f, width):
    lines = []
    for para in str(text).split("\n"):
        line = ""
        for word in para.split():
            trial = (line + " " + word).strip()
            if draw.textlength(trial, font=f) <= width or not line:
                line = trial
            else:
                lines.append(line)
                line = word
        lines.append(line)
    return lines


def balanced(draw, text, f, width):
    """Wrap, then even out the line lengths (no lone word on the last line) by narrowing the box
    while the number of lines stays the same."""
    lines = wrap(draw, text, f, width)
    if len(lines) < 2:
        return lines
    spread = lambda ls: max(draw.textlength(x, font=f) for x in ls) - draw.textlength(ls[-1], font=f)
    best, w = lines, width
    while w > width * 0.6:
        w -= width * 0.03
        trial = wrap(draw, text, f, w)
        if len(trial) != len(lines):
            break
        if spread(trial) < spread(best):
            best = trial
    return best


def fit(draw, text, kind, weight, width, max_h, start, minimum, max_lines, label):
    """Largest size (down to `minimum`) at which the text fits the box in at most max_lines."""
    size = start
    while True:
        f = font(kind, size * S, weight)
        lines = balanced(draw, text, f, width * S)
        lh = round(size * S * (1.08 if kind == "serif" else 1.14))
        if (len(lines) <= max_lines and lh * len(lines) <= max_h * S) or size <= minimum:
            if size <= minimum and (len(lines) > max_lines or lh * len(lines) > max_h * S):
                warn(f"{label}: '{text[:40]}...' is too long to stay readable; cut it to a few words")
            too_wide = [ln for ln in lines if draw.textlength(ln, font=f) > width * S]
            if too_wide and size > minimum // 2:
                size -= 2          # one long word: keep shrinking rather than cut it off
                continue
            if too_wide:
                warn(f"{label}: the word '{too_wide[0].split()[0]}' is wider than the pin; shorten it")
            gone = missing_glyphs(text, f)
            if gone:
                warn(f"{label}: the font can't draw {' '.join(gone[:6])} (they'd show as empty boxes); "
                     "remove them or set brand.font_file to a font that has them")
            return f, lines, lh, size
        size -= 2


def draw_lines(draw, lines, f, lh, x, y, fill, align="left", width=None):
    for i, ln in enumerate(lines):
        lx = x
        if align == "center" and width:
            lx = x + (width * S - draw.textlength(ln, font=f)) / 2
        draw.text((lx, y + i * lh), ln, font=f, fill=fill)
    return y + lh * len(lines)


# ---------- layouts ----------

class Pin:
    def __init__(self, spec, brand, base):
        self.spec, self.brand, self.base = spec, brand, base
        c = brand.get("colors") or {}
        self.bg = hexcolor(spec.get("bg") or c.get("bg"), DEFAULT_COLORS["bg"])
        self.fg = hexcolor(spec.get("fg") or c.get("fg"), DEFAULT_COLORS["fg"])
        self.accent = hexcolor(spec.get("accent") or c.get("accent"), DEFAULT_COLORS["accent"])
        self.kind = str(spec.get("font") or brand.get("font") or "serif").lower()
        if self.kind not in FONT_FILES:
            warn(f"{spec.get('id')}: font '{self.kind}' isn't serif or sans; using serif")
            self.kind = "serif"
        self.weight = "Bold" if self.kind == "sans" else "Regular"
        self.img = Image.new("RGB", (W * S, H * S), self.bg)
        self.d = ImageDraw.Draw(self.img)
        self.label = spec.get("id", "pin")
        self.headline_px = None
        if contrast(self.bg, self.fg) < 4.5:
            warn(f"{self.label}: text and background colours are too close (contrast {contrast(self.bg, self.fg):.1f}:1, needs 4.5)")

    def photo(self, rel, w, h, focus=None):
        f = focus or self.spec.get("focus") or (0.5, 0.5)
        try:
            fx, fy = (min(1.0, max(0.0, float(v))) for v in f)
        except (TypeError, ValueError):
            warn(f"{self.label}: focus {f!r} must be two numbers from 0 to 1, like [0.5, 0.4]; using the centre")
            fx, fy = 0.5, 0.5
        return cover(load(self.base, rel, self.label), w * S, h * S, (fx, fy), self.label)

    def headline(self, x, y, width, max_h, start=96, minimum=56, max_lines=4, fill=None, align="left"):
        text = self.spec.get("headline", "")
        if not text:
            return y
        f, lines, lh, size = fit(self.d, text, self.kind, self.weight, width, max_h, start, minimum, max_lines, self.label)
        self.headline_px = size
        return draw_lines(self.d, lines, f, lh, x * S, y * S, fill or self.fg, align, width) / S

    def sub(self, x, y, width, fill=None, size=38, align="left"):
        text = self.spec.get("sub")
        if not text:
            return y
        f, lines, lh, _ = fit(self.d, text, "sans", "Medium", width, 160, size, 30, 3, self.label)
        return draw_lines(self.d, lines, f, lh, x * S, y * S, fill or self.fg, align, width) / S

    def footer(self, fill=None, on_photo=False):
        """The site (or logo) small, bottom centre: findable, never an ad."""
        b = self.brand
        y = H - 58
        logo = b.get("logo")
        if logo:
            lg = load_logo(self.base, logo)
            lg.thumbnail((260 * S, 44 * S))
            self.img.paste(lg, ((W * S - lg.width) // 2, (y - 6) * S), lg)
            return
        text = b.get("site") or b.get("name")
        if not text:
            return
        f = font("sans", 26 * S, "Medium")
        gone = missing_glyphs(text, f)
        if gone:
            warn(f"{self.label}: the font can't draw {' '.join(gone[:6])} in the footer (they'd show as empty boxes)")
        tw = self.d.textlength(text, font=f)
        if on_photo:
            pad = 16 * S
            box = [(W * S - tw) / 2 - pad, (y - 8) * S, (W * S + tw) / 2 + pad, (y + 34) * S]
            self.d.rounded_rectangle(box, radius=21 * S, fill=(0, 0, 0))
            fill = "#FFFFFF"
        self.d.text(((W * S - tw) / 2, y * S), text, font=f, fill=fill or self.fg)

    # --- the six layouts ---

    def layout_photo(self):
        top = (self.spec.get("band") or "top") == "top"
        band_h = 470 if self.spec.get("sub") else 400
        pic_h = H - band_h
        self.img.paste(self.photo(self.spec["image"], W, pic_h), (0, (band_h if top else 0) * S))
        y0 = 70 if top else pic_h + 56
        y = self.headline(MARGIN, y0, W - 2 * MARGIN, band_h - 150, start=92)
        self.sub(MARGIN, y + 18, W - 2 * MARGIN, fill=self.accent)
        self.footer(on_photo=top)

    def layout_split(self):
        pic_h = 930
        self.img.paste(self.photo(self.spec["image"], W, pic_h), (0, 0))
        self.d.rectangle([0, (pic_h - 6) * S, W * S, pic_h * S], fill=self.accent)
        y = self.headline(MARGIN, pic_h + 60, W - 2 * MARGIN, 330, start=86)
        self.sub(MARGIN, y + 16, W - 2 * MARGIN, fill=self.accent)
        self.footer()

    def layout_grid(self):
        tiles = self.spec.get("tiles") or []
        if not 2 <= len(tiles) <= 8:
            sys.exit(f"{self.label}: a grid pin takes 2 to 8 tiles, got {len(tiles)}")
        cols = self.spec.get("cols") or (2 if len(tiles) in (2, 4, 6, 8) else 3)
        rows = -(-len(tiles) // cols)
        for t in tiles:
            if not isinstance(t, dict) or not t.get("image"):
                sys.exit(f"{self.label}: every grid tile needs an image, like {{\"image\": \"media/a.jpg\", \"label\": \"Step 1\"}}")
        y = self.headline(MARGIN, 64, W - 2 * MARGIN, 300, start=84, max_lines=3, align="center")
        if self.spec.get("sub"):
            y = self.sub(MARGIN, y + 10, W - 2 * MARGIN, fill=self.accent, size=34, align="center")
        top, bottom, gap = y + 34, H - 110, 18
        lab_h = 62
        tw = (W - 2 * MARGIN - gap * (cols - 1)) / cols
        th = (bottom - top - gap * (rows - 1)) / rows - lab_h
        if th < 120:
            warn(f"{self.label}: tiles are very small ({int(tw)}x{int(th)} px); use fewer tiles or a shorter headline")
        lf = font("sans", 40 * S, "SemiBold")
        for i, t in enumerate(tiles):
            r, c = divmod(i, cols)
            x = MARGIN + c * (tw + gap)
            ty = top + r * (th + lab_h + gap)
            ph = self.photo(t["image"], int(tw), int(th), t.get("focus"))
            self.img.paste(ph, (int(x * S), int(ty * S)))
            lab = t.get("label", "")
            gone = missing_glyphs(lab, lf) if lab else []
            if gone:
                warn(f"{self.label}: the font can't draw {' '.join(gone[:6])} in a tile label (they'd show as empty boxes)")
            if lab:
                lw = self.d.textlength(lab, font=lf)
                if lw > tw * S:
                    warn(f"{self.label}: tile label '{lab}' is wider than its tile; shorten it")
                self.d.text(((x + tw / 2) * S - lw / 2, (ty + th + 10) * S), lab, font=lf, fill=self.fg)
        self.footer()

    def layout_fact(self):
        if self.spec.get("image"):
            ph = self.photo(self.spec["image"], W, H)
            if self.spec.get("blur"):
                ph = ph.filter(ImageFilter.GaussianBlur(float(self.spec["blur"]) * S))
            self.img.paste(Image.blend(ph, Image.new("RGB", ph.size, (0, 0, 0)), float(self.spec.get("darken", 0.4))), (0, 0))
            fg = "#FFFFFF"
        else:
            fg = self.fg
        big = str(self.spec.get("big", ""))
        bf, lines, lh, _ = fit(self.d, big, self.kind, self.weight, W - 2 * MARGIN, 420, 360, 140, 1, self.label)
        y = 330
        draw_lines(self.d, lines, bf, lh, MARGIN * S, y * S, self.accent, "center", W - 2 * MARGIN)
        y = y + lh * len(lines) / S + 30
        y = self.headline(MARGIN, y, W - 2 * MARGIN, 360, start=80, align="center", fill=fg)
        self.sub(MARGIN, y + 20, W - 2 * MARGIN, fill=fg, align="center")
        self.footer(fill=fg)

    def layout_list(self):
        items = self.spec.get("items") or []
        if not 3 <= len(items) <= 8:
            warn(f"{self.label}: a list pin reads best with 3 to 8 lines, got {len(items)}")
        strip = int(self.spec.get("strip") or 380) if self.spec.get("image") else 0
        if strip:
            self.img.paste(self.photo(self.spec["image"], W, strip), (0, (H - strip) * S))
        y = self.headline(MARGIN, 70, W - 2 * MARGIN, 300, start=84, max_lines=3)
        y += 34
        space = H - strip - 60 - y
        each = min(space / max(1, len(items)), 165)
        nf = font("sans", 34 * S, "Bold")
        size = min(46, int(each * 0.42))
        for i, it in enumerate(items, 1):
            iy = y + (i - 1) * each
            r = 26
            self.d.ellipse([MARGIN * S, (iy + 2) * S, (MARGIN + 2 * r) * S, (iy + 2 + 2 * r) * S], fill=self.accent)
            n = str(i)
            self.d.text(((MARGIN + r) * S - self.d.textlength(n, font=nf) / 2, (iy + 9) * S), n, font=nf, fill=self.bg)
            f, lines, lh, _ = fit(self.d, it, "sans", "Medium", W - 2 * MARGIN - 80, each - 8, size, 26, 2, self.label)
            draw_lines(self.d, lines, f, lh, (MARGIN + 80) * S, (iy + 6) * S, self.fg)
        self.footer(on_photo=bool(strip))

    def layout_plain(self):
        self.img.paste(self.photo(self.spec["image"], W, H), (0, 0))
        if self.spec.get("headline"):
            warn(f"{self.label}: plain pins carry no text; the headline goes in the pin title instead")

    def render(self):
        layout = self.spec.get("layout", "photo")
        fn = getattr(self, "layout_" + layout, None)
        if not fn:
            sys.exit(f"{self.label}: unknown layout '{layout}' (photo, split, grid, fact, list, plain)")
        if layout != "grid" and layout != "fact" and layout != "list" and not self.spec.get("image"):
            sys.exit(f"{self.label}: the '{layout}' layout needs an image")
        fn()
        return self.img.resize((W, H), LANCZOS)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("spec")
    ap.add_argument("--out", default="pins")
    ap.add_argument("--only", help="render just these pin ids, comma-separated (the manifest keeps the others)")
    a = ap.parse_args()
    base = os.path.dirname(os.path.abspath(a.spec))
    try:
        with open(a.spec, encoding="utf-8") as f:
            spec = json.load(f)
    except (OSError, ValueError) as e:
        sys.exit(f"can't read {a.spec}: {e}")
    if not isinstance(spec, dict) or not isinstance(spec.get("pins"), list):
        sys.exit(f"{a.spec} needs a \"pins\" list (see the top of this script)")
    out = a.out if os.path.isabs(a.out) else os.path.join(base, a.out)
    os.makedirs(out, exist_ok=True)
    brand = spec.get("brand") or {}
    if brand.get("font_file"):
        ff = P.resolve(base, brand["font_file"])
        if not os.path.exists(ff):
            sys.exit(f"brand.font_file not found: {brand['font_file']}")
        CUSTOM_FONT["serif"] = CUSTOM_FONT["sans"] = ff
    P.check_ids(spec["pins"])
    only = set(a.only.split(",")) if a.only else None
    mpath = os.path.join(out, "manifest.json")
    old = {}
    if only and os.path.exists(mpath):
        try:
            old = {m["id"]: m for m in json.load(open(mpath, encoding="utf-8")).get("pins", [])}
        except Exception:
            old = {}
    manifest, thumbs = [], []
    for p in spec["pins"]:
        if only and p["id"] not in only:
            if p["id"] in old:
                manifest.append(old[p["id"]])
            continue
        before = len(WARNINGS)
        pin = Pin(p, brand, base)
        img = pin.render()
        path = os.path.join(out, p["id"] + ".jpg")
        img.save(path, "JPEG", quality=90, optimize=True, progressive=True)
        hp = pin.headline_px
        srcs = [p["image"]] if p.get("image") else [t["image"] for t in p.get("tiles", []) if isinstance(t, dict)]
        manifest.append({"id": p["id"], "file": P.rel(path, base), "layout": p.get("layout", "photo"),
                         "headline": p.get("headline", ""), "headline_px": hp,
                         "headline_px_in_feed": round(hp * FEED_W / W, 1) if hp else None,
                         "spec_dir": P.rel(base, out), "images": srcs,
                         "warnings": WARNINGS[before:]})
        thumbs.append(img)
        print(f"wrote {P.rel(path, base)}" + (f"  (headline {hp}px, {round(hp * FEED_W / W, 1)}px in the feed)" if hp else ""))
    with open(mpath, "w", encoding="utf-8") as f:
        json.dump({"pins": manifest}, f, indent=1, ensure_ascii=False)
    if thumbs:
        tw, gap = 300, 16
        th = int(tw * H / W)
        sheet = Image.new("RGB", (len(thumbs) * (tw + gap) + gap, th + 2 * gap), "#E9E9E9")
        for i, t in enumerate(thumbs):
            sheet.paste(t.resize((tw, th), LANCZOS), (gap + i * (tw + gap), gap))
        sheet.save(os.path.join(out, "contact-sheet.jpg"), quality=88)
        print(f"wrote {P.rel(os.path.join(out, 'contact-sheet.jpg'), base)}: look at it before going on")
    if WARNINGS:
        print(f"{len(WARNINGS)} warning(s) above: fix them before checking", file=sys.stderr)


if __name__ == "__main__":
    main()
