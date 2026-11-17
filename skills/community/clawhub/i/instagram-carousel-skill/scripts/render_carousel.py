#!/usr/bin/env python3
"""Render an Instagram carousel from a JSON spec.

    python3 scripts/render_carousel.py carousel.json --out carousel/

Writes carousel/slide-01.jpg ... (1080x1350 sRGB JPEG, the size the Instagram API accepts),
contact-sheet.png, cover-grid.png (the cover as it shows in the profile grid) and manifest.json
(byte sizes, alt text and warnings per slide).

Spec:
{
  "theme": {
    "preset": "editorial" | "notes" | "tweet",   # look of the text slides
    "mode": "light" | "dark",
    "accent": "#C2410C",                         # *starred* words, numbers, labels
    "headline_font": "serif" | "sans",           # editorial only
    "name": "Plodd", "handle": "@plodd.app", "avatar": "avatar.png",
    "ratio": "4:5" | "3:4",                      # 3:4 is for manual upload only
    "arrow": true                                # small arrow on the cover
  },
  "slides": [
    {"type": "cover", "title": "...", "kicker": "...", "image": "photo.jpg" | "screenshot": "app.png"},
    {"type": "text", "title": "...", "body": "..."},
    {"type": "step", "number": "1", "title": "...", "body": "..."},
    {"type": "list", "title": "...", "items": ["...", "..."], "marker": "number" | "check"},
    {"type": "myth", "myth": "...", "fact": "...", "source": "optional"},
    {"type": "stat", "number": "62%", "body": "...", "source": "Source, 2026"},
    {"type": "tweet", "text": "..."},
    {"type": "photo", "image": "...", "text": "...", "position": "bottom" | "top"},
    {"type": "screenshot", "image": "...", "title": "...", "body": "..."},
    {"type": "beforeafter", "before": "a.png", "after": "b.png", "caption": "..."},
    {"type": "cta", "title": "..."}
  ]
}
Every slide takes "alt": one sentence describing it, for Instagram's alt text.

Markup in any text: *word* = accent colour, ~~words~~ = struck through, "\\n" = line break.
Needs Python 3.8+ and Pillow. OpenCV is optional (warns when text sits on a face).
"""
import argparse, json, os, re, shutil, subprocess, sys, urllib.request
from datetime import date

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

S = 2  # render at 2x, downscale at the end for crisp text
W = 1080
HEIGHTS = {"4:5": 1350, "3:4": 1440}
SIDE, TOP, BOTTOM = 88, 100, 120          # margins at 1x
ANCHOR = 300                               # every text slide starts here, so nothing jumps
MAX_ANCHORED = 870                         # taller blocks are centred instead

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "..", "fonts")
FONT_FILES = {
    "sans": ("Inter.ttf", "ofl/inter/Inter%5Bopsz,wght%5D.ttf"),
    "serif": ("InstrumentSerif-Regular.ttf", "ofl/instrumentserif/InstrumentSerif-Regular.ttf"),
}

PALETTES = {
    "editorial": {
        "light": {"bg": "#F4F0E8", "fg": "#151413", "muted": "#6B665F", "accent": "#C2410C"},
        "dark": {"bg": "#121212", "fg": "#F3EFE8", "muted": "#9C978F", "accent": "#FF7A45"},
    },
    "notes": {
        "light": {"bg": "#FFFFFF", "fg": "#1C1C1E", "muted": "#8E8E93", "accent": "#E5A00D"},
        "dark": {"bg": "#1C1C1E", "fg": "#F2F2F7", "muted": "#8E8E93", "accent": "#F5B700"},
    },
    "tweet": {
        "light": {"bg": "#FFFFFF", "fg": "#0F1419", "muted": "#536471", "accent": "#1D9BF0"},
        "dark": {"bg": "#0B0B0C", "fg": "#E7E9EA", "muted": "#71767B", "accent": "#1D9BF0"},
    },
}

WARNINGS = []


def warn(msg):
    WARNINGS.append(msg)
    print("warning: " + msg, file=sys.stderr)


# ---------- fonts ----------

def font_path(kind):
    name, remote = FONT_FILES[kind]
    path = os.path.join(FONTS, name)
    if os.path.exists(path):
        return path
    # Some skill registries strip binary files; fetch the open-licensed font once.
    os.makedirs(FONTS, exist_ok=True)
    url = "https://raw.githubusercontent.com/google/fonts/main/" + remote
    try:
        urllib.request.urlretrieve(url, path)
    except Exception:
        if shutil.which("curl"):
            subprocess.run(["curl", "-sfL", url, "-o", path], check=False)
    if not os.path.exists(path) or os.path.getsize(path) < 10000:
        sys.exit(f"Font {name} missing and could not be downloaded from {url}")
    return path


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


def hexcolor(value, fallback):
    if not value:
        return fallback
    v = value.strip().lstrip("#")
    if not re.fullmatch(r"[0-9a-fA-F]{3}|[0-9a-fA-F]{6}", v):
        warn(f"'{value}' is not a hex colour, using {fallback}")
        return fallback
    if len(v) == 3:
        v = "".join(c * 2 for c in v)
    return "#" + v.upper()


def mix(a, b, t):
    a, b = a.lstrip("#"), b.lstrip("#")
    ca = [int(a[i:i + 2], 16) for i in (0, 2, 4)]
    cb = [int(b[i:i + 2], 16) for i in (0, 2, 4)]
    return "#" + "".join(f"{round(x + (y - x) * t):02X}" for x, y in zip(ca, cb))


# ---------- rich text ----------

TOKEN = re.compile(r"(~~.+?~~|\*[^*]+?\*)")
EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿️‍]")


def runs(text):
    """Split markup into words. Each word is a list of (text, accent, strike) pieces, so
    punctuation right after *accent* stays attached ("*twice*." renders as "twice.").
    A "\\n" word marks a line break."""
    text = str(text or "")
    if EMOJI.search(text):
        warn("emoji removed from slide text (the bundled fonts have no emoji); put emoji in the caption")
        text = re.sub(r" {2,}", " ", EMOJI.sub("", text)).strip()
    text = smart_quotes(text)
    out = []
    prev_tail_space = True
    for part in TOKEN.split(text):
        if not part:
            continue
        accent = part.startswith("*") and part.endswith("*") and len(part) > 2
        strike = part.startswith("~~") and part.endswith("~~") and len(part) > 4
        inner = part[2:-2] if strike else part[1:-1] if accent else part
        for i, para in enumerate(inner.split("\n")):
            if i:
                out.append("\n")
            for j, w in enumerate(para.split()):
                glue = (j == 0 and i == 0 and not prev_tail_space and not para[:1].isspace()
                        and out and out[-1] != "\n")
                if glue:
                    out[-1] = out[-1] + [(w, accent, strike)]
                else:
                    out.append([(w, accent, strike)])
        prev_tail_space = inner[-1:].isspace() if inner else True
    return out


def smart_quotes(text):
    """Typewriter quotes to typographic ones: don't -> don’t, "x" -> “x”."""
    text = re.sub(r"(?<=\w)'", "’", text)
    text = re.sub(r"'(?=\w)", "‘", text)
    text = text.replace("'", "’")
    text = re.sub(r'(^|[\s(\[*~])"', "\\1“", text)
    return text.replace('"', "”")


def wtext(word):
    return "".join(t for t, _, _ in word)


def plain(text):
    return re.sub(r"~~|\*", "", str(text or ""))


def word_count(text):
    return len(plain(text).split())


def _greedy(draw, items, f, max_w):
    lines, line, width = [], [], 0
    space = draw.textlength(" ", font=f)
    for word in items:
        if word == "\n":
            lines.append(line)
            line, width = [], 0
            continue
        ww = draw.textlength(wtext(word), font=f)
        if line and width + space + ww > max_w:
            lines.append(line)
            line, width = [], 0
        line.append(word)
        width += (space if len(line) > 1 else 0) + ww
    lines.append(line)
    return lines


def _width(draw, line, f):
    space = draw.textlength(" ", font=f)
    return sum(draw.textlength(wtext(w), font=f) for w in line) + space * max(0, len(line) - 1)


def layout(draw, items, f, max_w, balance=False):
    """Wrap words into lines. Headlines are balanced (similar line lengths); body text avoids
    lines that end on a short word ("a", "the") and one-word last lines."""
    lines = _greedy(draw, items, f, max_w)
    if balance and len(lines) > 1 and "\n" not in items:
        lo, hi = max_w * 0.5, max_w
        for _ in range(14):
            mid = (lo + hi) / 2
            if len(_greedy(draw, items, f, mid)) > len(lines):
                lo = mid
            else:
                hi = mid
        lines = _greedy(draw, items, f, hi)
    # widow: a short single word alone on the last line pulls one word down
    if len(lines) >= 2 and len(lines[-1]) == 1 and len(wtext(lines[-1][0])) <= 5 and len(lines[-2]) > 3:
        lines[-1].insert(0, lines[-2].pop())
    # then move short trailing words ("a", "of", "the") down when the next line has room
    for i in range(len(lines) - 1):
        last = wtext(lines[i][-1]) if lines[i] else ""
        if len(lines[i]) > 2 and len(last) <= 3 and last[-1:].isalpha() and lines[i + 1]:
            cand = [lines[i][-1]] + lines[i + 1]
            if _width(draw, cand, f) <= max_w:
                lines[i + 1] = [lines[i].pop()] + lines[i + 1]
    while len(lines) > 1 and not lines[-1]:
        lines.pop()
    return lines  # empty lines in the middle are blank lines the author wrote


def fit(draw, text, kind, weight, max_w, max_h, start, floor, lh, label, balance=False):
    """Largest size from start down to floor that fits; warns if even the floor overflows."""
    items = runs(text)
    # headlines with author line breaks: shrink until each written line fits on one line
    want = items.count("\n") + 1 if (balance and "\n" in items) else None
    size = start
    while True:
        f = font(kind, size * S, weight)
        lines = layout(draw, items, f, max_w * S, balance)
        h = len(lines) * size * lh
        if want and len(lines) > want and size > floor:
            size -= 2
            continue
        if h <= max_h or size <= floor:
            if h > max_h:
                warn(f"{label}: text does not fit even at {floor}px; split it over two slides")
            return f, lines, size
        size -= 2


def draw_lines(draw, lines, f, x, y, size, lh, fg, accent, strike_col=None):
    space = draw.textlength(" ", font=f)
    step = size * lh * S
    for line in lines:
        cx = x
        for word in line:
            px = cx
            for t, a, s in word:
                col = accent if a else (strike_col or fg) if s else fg
                tw = draw.textlength(t, font=f)
                draw.text((px, y), t, font=f, fill=col)
                if s:
                    mid = y + size * S * 0.56
                    draw.line([(px - 4, mid), (px + tw + 4, mid)], fill=col, width=max(3, size * S // 13))
                px += tw
            cx += draw.textlength(wtext(word), font=f) + space
        y += step
    return y


def bh(lines, size, lh):
    return len(lines) * size * lh * S


# ---------- images ----------

def load_image(path, base):
    if not path:
        return None
    p = path if os.path.isabs(path) else os.path.join(base, path)
    if not os.path.exists(p):
        sys.exit(f"Image not found: {p}")
    return ImageOps.exif_transpose(Image.open(p)).convert("RGB")


def cover_crop(img, w, h, focus_y=0.5):
    scale = max(w / img.width, h / img.height)
    img = img.resize((max(w, round(img.width * scale)), max(h, round(img.height * scale))), Image.LANCZOS)
    left = (img.width - w) // 2
    top = int((img.height - h) * focus_y)
    return img.crop((left, top, left + w, top + h))


def faces(img):
    try:
        import cv2, numpy
        gray = cv2.cvtColor(numpy.array(img), cv2.COLOR_RGB2GRAY)
        casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        return list(casc.detectMultiScale(gray, 1.1, 6, minSize=(max(24, gray.shape[1] // 12),) * 2))
    except Exception:
        return []  # no or partial OpenCV install: skip the check


def rounded(img, radius):
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, img.width - 1, img.height - 1], radius, fill=255)
    out = Image.new("RGBA", img.size)
    out.paste(img, (0, 0), mask)
    return out


def paste_card(img, card, x, y, radius, dark):
    shadow = Image.new("RGBA", (card.width + 120 * S, card.height + 120 * S), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle([60 * S, 72 * S, 60 * S + card.width, 72 * S + card.height],
                                             radius, fill=(0, 0, 0, 140 if dark else 60))
    shadow = shadow.filter(ImageFilter.GaussianBlur(22 * S))
    img.paste(shadow, (x - 60 * S, y - 60 * S), shadow)
    img.paste(card, (x, y), card)


def disc(img_or_none, d, letter, fg, bg):
    if img_or_none is not None:
        av = cover_crop(img_or_none, d, d)
    else:
        av = Image.new("RGB", (d, d), fg)
        ImageDraw.Draw(av).text((d / 2, d / 2), letter, font=font("sans", int(d * 0.46), "Bold"),
                                fill=bg, anchor="mm")
    mask = Image.new("L", (d, d), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, d - 1, d - 1], fill=255)
    return av, mask


# ---------- context ----------

class Ctx:
    def __init__(self, theme, base, h):
        self.t, self.base, self.h = theme, base, h
        preset = theme.get("preset", "editorial")
        if preset not in PALETTES:
            warn(f"preset '{preset}' unknown, using editorial (choose editorial, notes or tweet)")
            preset = "editorial"
        mode = theme.get("mode", "light")
        if mode not in ("light", "dark"):
            warn(f"mode '{mode}' unknown, using light")
            mode = "light"
        pal = PALETTES[preset][mode]
        self.preset, self.mode, self.dark = preset, mode, mode == "dark"
        self.bg = hexcolor(theme.get("bg"), pal["bg"])
        self.fg = hexcolor(theme.get("fg"), pal["fg"])
        self.muted = hexcolor(theme.get("muted"), pal["muted"])
        self.accent = hexcolor(theme.get("accent"), pal["accent"])
        hf = theme.get("headline_font", "serif" if preset == "editorial" else "sans")
        self.serif = preset == "editorial" and hf == "serif"
        self.avatar = load_image(theme.get("avatar"), base) if theme.get("avatar") else None
        if self.avatar is None and preset == "tweet":
            warn("tweet cards look unfinished with a letter avatar; add \"avatar\" to the theme")

    @property
    def head_kind(self):
        return ("serif", "Regular") if self.serif else ("sans", "Bold")


def canvas(ctx):
    return Image.new("RGB", (W * S, ctx.h * S), ctx.bg)


def header(img, ctx, fg=None, muted=None):
    """Small creator header top-left: the one bit of chrome on every slide."""
    t = ctx.t
    name, handle = t.get("name", ""), t.get("handle", "")
    if not (name or handle):
        return
    fg, muted = fg or ctx.fg, muted or ctx.muted
    draw = ImageDraw.Draw(img)
    x, y = SIDE * S, 60 * S
    redundant = name and handle and handle.lstrip("@").split(".")[0].lower() == name.lower()
    if ctx.avatar is None and ctx.preset != "tweet":
        # no avatar: just the handle (or name), small and quiet
        col = mix(fg, ctx.bg, 0.3) if fg == ctx.fg else fg
        draw.text((x, y + 10 * S), handle or name, font=font("sans", 26 * S, "SemiBold"), fill=col)
        return
    d = 48 * S
    av, mask = disc(ctx.avatar, d, (name or handle).lstrip("@")[:1].upper(), fg, ctx.bg)
    img.paste(av, (x, y), mask)
    tx = x + d + 16 * S
    if name and handle and not redundant:
        draw.text((tx, y - 1 * S), name, font=font("sans", 26 * S, "SemiBold"), fill=fg)
        draw.text((tx, y + 26 * S), handle, font=font("sans", 22 * S), fill=muted)
    else:
        draw.text((tx, y + 9 * S), name or handle, font=font("sans", 26 * S, "SemiBold"), fill=fg)


def arrow(img, ctx, color=None):
    ImageDraw.Draw(img).text(((W - SIDE) * S, (ctx.h - 62) * S), "→",
                             font=font("sans", 50 * S), fill=color or ctx.muted, anchor="rs")


def notes_line(img, ctx):
    """The notes preset's small date line, like a phone notes app."""
    if ctx.preset != "notes":
        return
    d = ctx.t.get("date") or date.today().strftime("%B %d, %Y").replace(" 0", " ")
    ImageDraw.Draw(img).text((SIDE * S, 150 * S), d, font=font("sans", 26 * S, "Medium"), fill=ctx.accent)


def start_y(ctx, total_px):
    """Fixed anchor so text doesn't jump between slides; centre only very tall blocks."""
    if total_px / S <= MAX_ANCHORED:
        return ANCHOR * S
    return max(170 * S, ((ctx.h - BOTTOM) * S - total_px + 170 * S) / 2)


def stack(draw, parts, ctx, y=None):
    """Draw parts (font, lines, size, lh, colour, gap_after) top to bottom from the anchor."""
    total = sum(bh(p[1], p[2], p[3]) for p in parts) + sum(p[5] for p in parts[:-1]) * S
    y = start_y(ctx, total) if y is None else y
    for f, lines, size, lh, col, g in parts:
        y = draw_lines(draw, lines, f, SIDE * S, y, size, lh, col, ctx.accent, ctx.muted) + g * S
    return y


# ---------- slide types ----------

BW = W - 2 * SIDE


def head_parts(draw, ctx, title, label, start=None, floor=None, max_h=360):
    kind, weight = ctx.head_kind
    start = start or (128 if ctx.serif else 96)
    floor = floor or (72 if ctx.serif else 64)
    if word_count(title) > 10:
        warn(f"{label}: headline has {word_count(title)} words; 8 or fewer is easier to scan")
    if ctx.serif and re.search(r"(?<![\d.,])1(?![\d.,])", plain(title)):
        warn(f"{label}: a lone '1' in the serif headline can read as 'l'; spell it out or use the sans font")
    return fit(draw, title, kind, weight, BW, max_h, start, floor, 1.06, label, balance=True)


def body_parts(draw, ctx, body, label, max_h=520, start=54, floor=40):
    if word_count(body) > 45:
        warn(f"{label}: body has {word_count(body)} words; keep it under 30 (45 at most) or split")
    return fit(draw, body, "sans", "Regular", min(BW, 880), max_h, start, floor, 1.38, label)


def slide_cover(s, ctx, label):
    if s.get("image"):
        return slide_photo({**s, "text": s.get("title", "")}, ctx, label, cover=True)
    if ctx.preset == "tweet":
        img = slide_tweet({"text": s.get("title", "")}, ctx, label, start=84, floor=60, weight="SemiBold")
        if ctx.t.get("arrow", True):
            arrow(img, ctx)
        return img
    img = canvas(ctx)
    draw = ImageDraw.Draw(img)
    header(img, ctx)
    notes_line(img, ctx)
    title = s.get("title", "")
    if word_count(title) > 10:
        warn(f"{label}: cover title has {word_count(title)} words; 8 or fewer reads in a glance")
    shot = load_image(s.get("screenshot"), ctx.base)
    text_bottom = int(ctx.h * 0.55) if shot is not None else ctx.h - BOTTOM - 40
    kind, weight = ctx.head_kind
    if kind == "sans":
        weight = "Black"
    floor = 150 if ctx.serif else 130
    if shot is not None:
        floor = 110 if ctx.serif else 96
    kparts, kh = None, 0
    if s.get("kicker"):
        kf, kl, ks = fit(draw, s["kicker"], "sans", "SemiBold", BW, 120, 40, 34, 1.25, label)
        kh = bh(kl, ks, 1.25) / S + 34
        kparts = (kf, kl, ks)
    avail = text_bottom - 180 - kh
    f, lines, size = fit(draw, title, kind, weight, BW, avail, 200 if ctx.serif else 150, floor, 1.02,
                         label, balance=True)
    total = bh(lines, size, 1.02) + kh * S
    y = (180 * S + text_bottom * S - total) / 2 if shot is None else 190 * S
    y = draw_lines(draw, lines, f, SIDE * S, y, size, 1.02, ctx.fg, ctx.accent, ctx.muted)
    if kparts:
        draw_lines(draw, kparts[1], kparts[0], SIDE * S, y + 30 * S, kparts[2], 1.25, ctx.accent, ctx.accent)
    if shot is not None:
        area_h = ctx.h - text_bottom
        crop = cover_crop(shot, BW * S, (area_h + 40) * S, s.get("focus_y", 0.0))
        paste_card(img, rounded(crop, 32 * S), SIDE * S, text_bottom * S, 32 * S, ctx.dark)
    elif ctx.t.get("arrow", True):
        arrow(img, ctx)
    return img


def slide_text(s, ctx, label, number=None):
    img = canvas(ctx)
    draw = ImageDraw.Draw(img)
    header(img, ctx)
    notes_line(img, ctx)
    parts = []
    if number not in (None, ""):
        nsize = 164  # step numbers are always sans: serif "1" reads as "l", and steps must match
        nf = font("sans", nsize * S, "Bold")
        parts.append((nf, [[[(str(number), True, False)]]], nsize, 1.0, ctx.accent, 24))
    if s.get("title"):
        tf, tl, ts = head_parts(draw, ctx, s["title"], label)
        parts.append((tf, tl, ts, 1.06, ctx.fg, 58))
    if s.get("body"):
        used = sum(bh(p[1], p[2], p[3]) for p in parts) / S
        bf, bl, bs = body_parts(draw, ctx, s["body"], label, max_h=ctx.h - BOTTOM - ANCHOR - used - 80)
        parts.append((bf, bl, bs, 1.38, ctx.fg, 0))
    if parts:
        stack(draw, parts, ctx)
    return img


def slide_list(s, ctx, label):
    img = canvas(ctx)
    draw = ImageDraw.Draw(img)
    header(img, ctx)
    notes_line(img, ctx)
    items = s.get("items") or []
    if not items:
        sys.exit(f"{label}: list slide needs \"items\"")
    if len(items) > 7:
        warn(f"{label}: {len(items)} items; 7 or fewer reads at a glance")
    marker = s.get("marker", "number")
    title_part, title_h = None, 0
    if s.get("title"):
        tf, tl, ts = head_parts(draw, ctx, s["title"], label, max_h=260)
        title_part, title_h = (tf, tl, ts), bh(tl, ts, 1.06) + 48 * S
    size = 52
    while True:
        f = font("sans", size * S, "Medium")
        indent = int(size * 1.5) * S
        rows = [layout(draw, runs(it), f, BW * S - indent) for it in items]
        h = title_h + sum(bh(r, size, 1.3) for r in rows) + 28 * S * (len(rows) - 1)
        if h / S <= ctx.h - BOTTOM - ANCHOR - 20 or size <= 40:
            if h / S > ctx.h - BOTTOM - 180:
                warn(f"{label}: list does not fit; cut items or split the slide")
            break
        size -= 2
    y = start_y(ctx, h)
    if title_part:
        y = draw_lines(draw, title_part[1], title_part[0], SIDE * S, y, title_part[2], 1.06, ctx.fg, ctx.accent) + 48 * S
    mf = font("sans", size * S, "Bold")
    for i, r in enumerate(rows, 1):
        draw.text((SIDE * S, y), f"{i}." if marker == "number" else "✓", font=mf, fill=ctx.accent)
        y = draw_lines(draw, r, f, SIDE * S + indent, y, size, 1.3, ctx.fg, ctx.accent, ctx.muted) + 28 * S
    return img


def slide_myth(s, ctx, label):
    img = canvas(ctx)
    draw = ImageDraw.Draw(img)
    header(img, ctx)
    notes_line(img, ctx)
    lab = font("sans", 28 * S, "Bold")
    mf, ml, ms = fit(draw, f"~~{plain(s.get('myth', ''))}~~", "sans", "Medium", BW, 280, 64, 44, 1.2, label)
    ff, fl, fs = head_parts(draw, ctx, s.get("fact", ""), label, max_h=420)
    lab_h = int(28 * 1.4) * S + 14 * S
    total = lab_h + bh(ml, ms, 1.2) + 56 * S + lab_h + bh(fl, fs, 1.06)
    y = start_y(ctx, total)
    draw.text((SIDE * S, y), "MYTH", font=lab, fill=ctx.muted)
    y = draw_lines(draw, ml, mf, SIDE * S, y + lab_h, ms, 1.2, ctx.muted, ctx.accent, ctx.muted) + 56 * S
    draw.text((SIDE * S, y), "FACT", font=lab, fill=ctx.accent)
    draw_lines(draw, fl, ff, SIDE * S, y + lab_h, fs, 1.06, ctx.fg, ctx.accent, ctx.muted)
    if s.get("source"):
        source_line(draw, ctx, s["source"])
    return img


def source_line(draw, ctx, text):
    """Small source note near the bottom, wrapped to the text width."""
    f = font("sans", 26 * S)
    lines = layout(draw, runs(plain(text)), f, BW * S)
    y = (ctx.h - 150) * S - bh(lines, 26, 1.35)
    draw_lines(draw, lines, f, SIDE * S, y, 26, 1.35, ctx.muted, ctx.muted)


def slide_stat(s, ctx, label):
    img = canvas(ctx)
    draw = ImageDraw.Draw(img)
    header(img, ctx)
    notes_line(img, ctx)
    number = plain(s.get("number", ""))
    serif_ok = ctx.serif and "1" not in number
    kind, weight = ("serif", "Regular") if serif_ok else ("sans", "Bold")
    nf, nl, ns = fit(draw, number, kind, weight, BW, 380, 340 if serif_ok else 280, 160, 1.0, label)
    bf, bl, bs = fit(draw, s.get("body", ""), "sans", "Medium", min(BW, 860), 380, 54, 40, 1.3, label)
    stack(draw, [(nf, nl, ns, 1.0, ctx.accent, int(ns * 0.16)), (bf, bl, bs, 1.3, ctx.fg, 0)], ctx)
    if s.get("source"):
        source_line(draw, ctx, s["source"])
    elif re.search(r"\d", number):
        warn(f"{label}: a number with no \"source\"; say where it comes from, or cut it")
    return img


def slide_tweet(s, ctx, label, start=60, floor=44, weight="Regular"):
    img = canvas(ctx)
    draw = ImageDraw.Draw(img)
    t = ctx.t
    text = s.get("text", "")
    if len(plain(text)) > 280:
        warn(f"{label}: tweet card has {len(plain(text))} characters; 280 is what people expect")
    d = 92
    y0 = ANCHOR * S
    head, sep, rest = text.partition("\n\n")
    room = ctx.h - ANCHOR - d - 60 - BOTTOM
    if sep and weight == "Regular":
        # "Lie 1: ..." first paragraph in SemiBold, the rest Regular, same size
        size = start
        while True:
            hf, hl, _ = fit(draw, head, "sans", "SemiBold", BW, 9999, size, size, 1.34, label)
            rf, rl, _ = fit(draw, rest, "sans", "Regular", BW, 9999, size, size, 1.34, label)
            if (len(hl) + 1 + len(rl)) * size * 1.34 <= room or size <= floor:
                break
            size -= 2
        f, lines = None, None
    else:
        f, lines, size = fit(draw, text, "sans", weight, BW, room, start, floor, 1.34, label)
    name, handle = t.get("name", ""), t.get("handle", "")
    av, mask = disc(ctx.avatar, d * S, (name or handle or "?").lstrip("@")[:1].upper(), ctx.fg, ctx.bg)
    img.paste(av, (SIDE * S, int(y0)), mask)
    tx = (SIDE + d + 22) * S
    draw.text((tx, y0 + 12 * S), name or handle, font=font("sans", 34 * S, "Bold"), fill=ctx.fg)
    if name and handle:
        draw.text((tx, y0 + 54 * S), handle, font=font("sans", 30 * S), fill=ctx.muted)
    ty = y0 + (d + 40) * S
    if lines is None:
        ty = draw_lines(draw, hl, hf, SIDE * S, ty, size, 1.34, ctx.fg, ctx.accent, ctx.muted) + size * 1.34 * S
        draw_lines(draw, rl, rf, SIDE * S, ty, size, 1.34, ctx.fg, ctx.accent, ctx.muted)
    else:
        draw_lines(draw, lines, f, SIDE * S, ty, size, 1.34, ctx.fg, ctx.accent, ctx.muted)
    return img


def slide_photo(s, ctx, label, cover=False):
    photo = load_image(s.get("image"), ctx.base)
    if photo is None:
        sys.exit(f"{label}: photo slide needs an image")
    img = cover_crop(photo, W * S, ctx.h * S, s.get("focus_y", 0.5))
    text = s.get("text", "")
    pos = s.get("position", "bottom")
    if text:
        draw = ImageDraw.Draw(img)
        if word_count(text) > (10 if cover else 14):
            warn(f"{label}: text over a photo should be short ({word_count(text)} words)")
        start, floor = (128, 88) if cover else (64, 46)
        f, lines, size = fit(draw, text, "sans", "Black" if cover else "Bold", BW, 520, start, floor, 1.04,
                             label, balance=True)
        th = bh(lines, size, 1.04)
        kparts = None
        if s.get("kicker"):
            kf, kl, ks = fit(draw, s["kicker"], "sans", "SemiBold", BW, 120, 40, 34, 1.2, label)
            kparts = (kf, kl, ks)
            th += bh(kl, ks, 1.2) + 22 * S
        y = (TOP + 90) * S if pos == "top" else (ctx.h - BOTTOM - 30) * S - th
        grad_h = int(th + 420 * S)
        g = Image.new("L", (1, grad_h))
        for i in range(grad_h):
            frac = i / grad_h
            g.putpixel((0, i), int(200 * (frac if pos != "top" else 1 - frac) ** 1.5))
        img.paste(Image.new("RGB", (W * S, grad_h), "#000000"),
                  (0, ctx.h * S - grad_h if pos != "top" else 0), g.resize((W * S, grad_h)))
        band = img.resize((W, ctx.h)).crop((0, int(y / S), W, int((y + th) / S)))
        if faces(band):
            warn(f"{label}: text may sit on a face; try position '{'top' if pos != 'top' else 'bottom'}'")
        draw = ImageDraw.Draw(img)
        y = draw_lines(draw, lines, f, SIDE * S, y, size, 1.04, "#FFFFFF", ctx.accent)
        if kparts:
            draw_lines(draw, kparts[1], kparts[0], SIDE * S, y + 22 * S, kparts[2], 1.2, "#FFFFFF", ctx.accent)
    # a light shade at the top so the header reads on any photo
    gh = 220 * S
    g = Image.new("L", (1, gh))
    for i in range(gh):
        g.putpixel((0, i), int(110 * (1 - i / gh) ** 1.6))
    img.paste(Image.new("RGB", (W * S, gh), "#000000"), (0, 0), g.resize((W * S, gh)))
    header(img, ctx, fg="#FFFFFF", muted="#DDDDDD")
    if cover and ctx.t.get("arrow", True):
        arrow(img, ctx, color="#FFFFFF")
    return img


def slide_screenshot(s, ctx, label):
    img = canvas(ctx)
    draw = ImageDraw.Draw(img)
    header(img, ctx)
    parts = []
    if s.get("title"):
        tf, tl, ts = head_parts(draw, ctx, s["title"], label, max_h=240)
        parts.append((tf, tl, ts, 1.06, ctx.fg, 22))
    if s.get("body"):
        bf, bl, bs = fit(draw, s["body"], "sans", "Regular", BW, 140, 44, 38, 1.35, label)
        parts.append((bf, bl, bs, 1.35, ctx.fg, 0))
    shot = load_image(s.get("image"), ctx.base)
    if shot is None:
        sys.exit(f"{label}: screenshot slide needs an image")
    wide = shot.width >= shot.height
    y = stack(draw, parts, ctx, y=(ANCHOR if wide else 200) * S) if parts else ANCHOR * S
    top_y = y + 64 * S
    max_w, max_h = BW * S, (ctx.h - 70) * S - top_y
    scale = min(max_w / shot.width, max_h / shot.height)
    bleed = scale * shot.width < 620 * S
    if bleed:
        scale = min(max_w, 700 * S) / shot.width  # tall phone screenshot: wide, running off the bottom
    shot = shot.resize((int(shot.width * scale), int(shot.height * scale)), Image.LANCZOS)
    if wide:  # wide screenshots use the full text width
        scale = BW * S / shot.width
        shot = shot.resize((BW * S, int(shot.height * scale)), Image.LANCZOS)
    paste_card(img, rounded(shot, 28 * S), (W * S - shot.width) // 2, int(top_y), 28 * S, ctx.dark)
    return img


def slide_beforeafter(s, ctx, label):
    img = canvas(ctx)
    draw = ImageDraw.Draw(img)
    header(img, ctx)
    cap_h, cparts = 0, None
    if s.get("caption"):
        cf, cl, cs = fit(draw, s["caption"], "sans", "Medium", BW, 110, 44, 36, 1.3, label)
        cap_h, cparts = bh(cl, cs, 1.3) / S + 30, (cf, cl, cs)
    box_h = int((ctx.h - 170 - BOTTOM - cap_h - 28) / 2)
    y = 170
    lab = font("sans", 30 * S, "Bold")
    for key, name in (("before", "Before"), ("after", "After")):
        im = load_image(s.get(key), ctx.base)
        if im is None:
            sys.exit(f"{label}: before/after slide needs \"before\" and \"after\" images")
        card = rounded(cover_crop(im, BW * S, box_h * S, s.get("focus_y", 0.0)), 24 * S)
        paste_card(img, card, SIDE * S, y * S, 24 * S, ctx.dark)
        tw = draw.textlength(name, font=lab)
        pill = [(SIDE + 20) * S, (y + 20) * S, (SIDE + 20) * S + tw + 40 * S, (y + 72) * S]
        draw.rounded_rectangle(pill, 26 * S, fill=ctx.accent if key == "after" else "#000000")
        draw.text((pill[0] + 20 * S, pill[1] + 10 * S), name, font=lab, fill="#FFFFFF")
        y += box_h + 28
    if cparts:
        draw_lines(draw, cparts[1], cparts[0], SIDE * S, (y + 2) * S, cparts[2], 1.3, ctx.fg, ctx.accent)
    return img


def slide_cta(s, ctx, label):
    img = canvas(ctx)
    draw = ImageDraw.Draw(img)
    header(img, ctx)
    notes_line(img, ctx)
    kind, weight = ctx.head_kind
    f, lines, size = fit(draw, s.get("title", ""), kind, weight, BW, ctx.h - ANCHOR - BOTTOM - 120,
                         150 if ctx.serif else 112, 80, 1.04, label, balance=True)
    parts = [(f, lines, size, 1.04, ctx.fg, 40)]
    if s.get("body"):
        warn(f"{label}: the last slide has a body too; one ask per carousel works best")
        bf, bl, bs = body_parts(draw, ctx, s["body"], label, max_h=200, start=44)
        parts.append((bf, bl, bs, 1.38, ctx.muted, 0))
    stack(draw, parts, ctx)
    return img


TYPES = {"cover": slide_cover, "text": slide_text, "list": slide_list, "myth": slide_myth,
         "stat": slide_stat, "tweet": slide_tweet, "photo": slide_photo, "screenshot": slide_screenshot,
         "beforeafter": slide_beforeafter, "cta": slide_cta}


def render(spec, base, out):
    theme = spec.get("theme", {})
    ratio = theme.get("ratio", "4:5")
    if ratio not in HEIGHTS:
        warn(f"ratio '{ratio}' unknown, using 4:5")
        ratio = "4:5"
    if ratio == "3:4":
        warn("3:4 (1080x1440) is for manual upload in the app; the Instagram API only accepts 4:5 to 1.91:1")
    ctx = Ctx(theme, base, HEIGHTS[ratio])
    slides = spec.get("slides", [])
    if not slides:
        sys.exit("No slides in the spec")
    if len(slides) > 20:
        warn(f"{len(slides)} slides; Instagram allows 20 at most")
    if slides[0].get("type") != "cover":
        warn("slide 1 is not a cover; the first slide decides whether anyone swipes")
    os.makedirs(out, exist_ok=True)
    files = []
    for i, s in enumerate(slides, 1):
        label = f"slide {i}"
        kind = s.get("type", "text")
        if kind != "step" and kind not in TYPES:
            sys.exit(f"{label}: unknown type '{kind}'. Use one of: {', '.join(sorted(list(TYPES) + ['step']))}")
        img = slide_text(s, ctx, label, number=s.get("number", "")) if kind == "step" else TYPES[kind](s, ctx, label)
        img = img.resize((W, ctx.h), Image.LANCZOS)
        path = os.path.join(out, f"slide-{i:02d}.jpg")
        img.save(path, "JPEG", quality=92, optimize=True, progressive=False, subsampling=0)
        if not s.get("alt"):
            warn(f"{label}: no alt text; write one sentence on what the slide shows and says")
        text = " ".join(plain(s.get(k, "")) for k in ("kicker", "title", "number", "myth", "fact", "body", "text", "caption"))
        text = " ".join((text + " " + " ".join(plain(x) for x in s.get("items", []))).split())
        files.append({"path": os.path.abspath(path), "bytes": os.path.getsize(path), "type": kind,
                      "alt": s.get("alt", ""), "text": text})
    sheet = contact_sheet([f["path"] for f in files], os.path.join(out, "contact-sheet.png"))
    tile = cover_tile(files[0]["path"], os.path.join(out, "cover-grid.png"))
    manifest = {"slides": len(files), "size": f"{W}x{ctx.h}", "ratio": ratio, "files": files,
                "contactSheet": sheet, "coverGrid": tile, "warnings": WARNINGS}
    with open(os.path.join(out, "manifest.json"), "w") as fh:
        json.dump(manifest, fh, indent=2)
    return manifest


def contact_sheet(paths, out_path, thumb_w=360, gap=16):
    thumbs = [Image.open(p) for p in paths]
    th = int(thumbs[0].height * thumb_w / thumbs[0].width)
    cols = min(5, len(thumbs))
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * thumb_w + (cols + 1) * gap, rows * th + (rows + 1) * gap), "#DDDDDD")
    for i, im in enumerate(thumbs):
        sheet.paste(im.resize((thumb_w, th), Image.LANCZOS),
                    (gap + (i % cols) * (thumb_w + gap), gap + (i // cols) * (th + gap)))
    sheet.save(out_path)
    return os.path.abspath(out_path)


def cover_tile(path, out_path, w=270):
    """The cover as the profile grid shows it: cropped to 3:4, about 270 px wide on a phone."""
    im = Image.open(path)
    target_h = int(im.width * 4 / 3)
    if target_h <= im.height:
        top = (im.height - target_h) // 2
        im = im.crop((0, top, im.width, top + target_h))
    else:
        cw = int(im.height * 3 / 4)
        left = (im.width - cw) // 2
        im = im.crop((left, 0, left + cw, im.height))
    im.resize((w, int(w * 4 / 3)), Image.LANCZOS).save(out_path)
    return os.path.abspath(out_path)


def main():
    ap = argparse.ArgumentParser(description="Render an Instagram carousel from a JSON spec.")
    ap.add_argument("spec")
    ap.add_argument("--out", default="carousel")
    a = ap.parse_args()
    with open(a.spec) as fh:
        spec = json.load(fh)
    m = render(spec, os.path.dirname(os.path.abspath(a.spec)), a.out)
    print(f"Rendered {m['slides']} slides ({m['size']}) to {a.out}/")
    print(f"Contact sheet: {m['contactSheet']}\nCover in the grid: {m['coverGrid']}")
    if WARNINGS:
        print(f"{len(WARNINGS)} warning(s); fix them before posting.")


if __name__ == "__main__":
    main()
