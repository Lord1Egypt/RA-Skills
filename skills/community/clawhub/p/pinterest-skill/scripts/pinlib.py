"""Shared helpers for the Pinterest skill scripts (standard library + Pillow)."""
import json, os, re, shutil, subprocess, sys, unicodedata
from datetime import datetime
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

# Agents read script output through a pipe; on Windows that defaults to a legacy code page, which
# can't print emoji or most non-Latin titles. Always write UTF-8 and never crash on a character.
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Pinterest's limits, from its API spec (v5.28.0) and product specs. See references/pinterest-specs.md.
TITLE_MAX = 100
TITLE_FEED = 40            # about this much of the title shows under a pin in the feed
DESC_MAX = 800
DESC_SOFT = 500            # older editors cut at 500; keep the point inside it
ALT_MAX = 500
LINK_MAX = 2048
IMAGE_MAX_MB = 20
IMAGE_TYPES = {"JPEG", "PNG"}
VIDEO_EXT = (".mp4", ".mov", ".m4v", ".webm", ".mkv", ".avi")
VIDEO_MIN_S, VIDEO_MAX_S = 4, 15 * 60
VIDEO_MAX_MB = 2048
VIDEO_RATIOS = {"1:1": 1.0, "2:3": 2 / 3, "4:5": 0.8, "9:16": 9 / 16}
SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly", "is.gd", "buff.ly", "rebrand.ly", "cutt.ly",
              "shorturl.at", "tiny.cc", "rb.gy", "t.ly", "bl.ink", "short.io", "s.id", "v.gd", "lnkd.in", "amzn.to",
              "shorte.st", "adf.ly", "ouo.io", "dub.sh", "linktr.ee"}
TRACKING = re.compile(r"^(utm_\w+|fbclid|gclid|msclkid|mc_cid|mc_eid|epik|ref)$", re.I)
STOP = set("a an and are as at be by for from how i in is it its of on or our that the this to was we what when "
           "where which who why will with you your vs into than then them they these those can do does not no".split())
ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,79}$")
LANCZOS = getattr(getattr(__import__("PIL.Image", fromlist=["Image"]), "Resampling", None), "LANCZOS", None) \
    or __import__("PIL.Image", fromlist=["Image"]).LANCZOS


def load_plan(path):
    try:
        with open(path, encoding="utf-8") as f:
            plan = json.load(f)
    except FileNotFoundError:
        sys.exit(f"{path} not found")
    except ValueError as e:
        sys.exit(f"{path} isn't valid JSON: {e}")
    if not isinstance(plan, dict):
        sys.exit(f"{path} must be a JSON object with accounts, links and pins")
    for key, kind in (("accounts", dict), ("links", dict), ("pins", list)):
        if plan.get(key) is None:
            plan[key] = kind()
        if not isinstance(plan[key], kind):
            sys.exit(f"plan.json: '{key}' must be a {'list' if kind is list else 'object'}")
    for i, p in enumerate(plan["pins"]):
        if not isinstance(p, dict):
            sys.exit(f"plan.json: pin {i + 1} must be an object")
        for k in ("title", "description", "alt", "board", "file", "account"):
            if p.get(k) is None:
                p.pop(k, None)
            elif not isinstance(p[k], str):
                p[k] = str(p[k])
    return plan


def save_plan(path, plan):
    shutil.copyfile(path, path + ".bak")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(plan, f, indent=1, ensure_ascii=False)


def resolve(base, rel):
    if not rel:
        return rel
    rel = rel.replace("\\", "/") if os.sep == "/" else rel
    return rel if os.path.isabs(rel) else os.path.join(base, rel)


def rel(path, base):
    """A path relative to base, with forward slashes (portable in plan.json); absolute across drives."""
    try:
        r = os.path.relpath(path, base)
    except ValueError:      # Windows: another drive
        r = os.path.abspath(path)
    return r.replace("\\", "/")


def fold(text):
    """Lowercase, accents removed, hyphens and punctuation as spaces: for matching words."""
    t = unicodedata.normalize("NFKD", str(text or "")).encode("ascii", "ignore").decode().lower()
    return " " + re.sub(r"[^a-z0-9]+", " ", t).strip() + " "


def has_phrase(text, phrase):
    """Whole-word phrase match ('wall art' doesn't match 'artichoke'; 'Moon-phases' matches 'moon phases')."""
    p = fold(phrase).strip()
    return bool(p) and (" " + p + " ") in fold(text)


def words(text):
    return [w for w in fold(text).split() if w not in STOP and len(w) > 1]


def is_url(u):
    try:
        s = urlsplit(u or "")
    except ValueError:
        return False
    return s.scheme in ("http", "https") and bool(s.netloc) and "." in s.netloc and " " not in u


def domain(url):
    try:
        d = (urlsplit(url or "").hostname or "").lower()
    except ValueError:
        d = ""
    return d[4:] if d.startswith("www.") else d


def canonical(url):
    """The page a URL points to, for comparing links: no tracking parameters, no fragment,
    host lowercased without www, no trailing slash. Two links with the same canonical URL are the same page."""
    if not url:
        return ""
    try:
        s = urlsplit(url.strip())
    except ValueError:
        return url.strip()
    q = urlencode([(k, v) for k, v in parse_qsl(s.query, keep_blank_values=True) if not TRACKING.match(k)])
    path = s.path.rstrip("/") or ""
    return urlunsplit(("https" if s.scheme in ("http", "https") else s.scheme, domain(url), path, q, ""))


def link_of(pin, links):
    """(url, error) for a pin: its 'link' is a key in plan.links or a full URL."""
    ref = pin.get("link")
    if not ref:
        return "", None
    if isinstance(ref, str) and ref in links:
        url = (links[ref] or {}).get("url") or ""
        return (url, None) if is_url(url) else (url, f"links.{ref}.url isn't a web address: '{url}'")
    if isinstance(ref, str) and is_url(ref):
        return ref, None
    return "", f"link '{ref}' is neither a key in links nor a full https:// address"


def run_text(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r


def ffprobe(path):
    if not shutil.which("ffprobe"):
        return None
    r = run_text(["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", path])
    try:
        return json.loads(r.stdout)
    except ValueError:
        return None


def duration(info):
    try:
        return float((info or {}).get("format", {}).get("duration"))
    except (TypeError, ValueError):
        return 0.0


def frame_at(path, t=0.0):
    """One frame of a video as a Pillow image (for hashing and previews)."""
    from PIL import Image
    import io
    if not shutil.which("ffmpeg"):
        return None
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", path, "-frames:v", "1", "-f", "image2pipe",
                        "-vcodec", "png", "-"], capture_output=True)
    if not r.stdout:
        return None
    return Image.open(io.BytesIO(r.stdout)).convert("RGB")


def open_image(path):
    """Open any photo the user has, including iPhone HEIC (with pillow-heif), as RGB with the right
    orientation. 16-bit and transparent images are converted correctly."""
    from PIL import Image, ImageOps
    if path.lower().endswith((".heic", ".heif")):
        try:
            import pillow_heif
            pillow_heif.register_heif_opener()
        except ImportError:
            sys.exit(f"{path} is a HEIC photo: pip install pillow-heif, or export it as JPEG first")
    try:
        im = Image.open(path)
        im.load()
    except Image.DecompressionBombError:
        sys.exit(f"{path} is too large to open safely; resize it below 100 megapixels first")
    except Exception as e:
        sys.exit(f"{path} can't be opened as an image ({e.__class__.__name__})")
    im = ImageOps.exif_transpose(im)
    if im.mode in ("I;16", "I;16B", "I;16L", "I"):
        im = im.point(lambda v: v * (1 / 256)).convert("L")
    if im.mode in ("RGBA", "LA", "P", "PA"):
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[-1])
        return bg
    return im.convert("RGB")


def dhash(img, size=16):
    """256-bit difference hash: survives resizing and recompression, changes when the picture changes."""
    g = img.convert("L").resize((size + 1, size), LANCZOS)
    px = list(g.getdata())
    bits = 0
    for y in range(size):
        for x in range(size):
            bits = (bits << 1) | (px[y * (size + 1) + x] > px[y * (size + 1) + x + 1])
    return f"{bits:0{size * size // 4}x}"


def thumb(img):
    """12x18 colour thumbnail as hex: catches 'different' hashes of flat or dark images."""
    return img.convert("RGB").resize((12, 18), LANCZOS).tobytes().hex()


def fingerprint(img):
    return {"d": dhash(img), "t": thumb(img)}


def same_picture(a, b):
    """True when two fingerprints show the same picture: the hashes are close AND the colours match."""
    if not a or not b or not a.get("d") or not b.get("d") or len(a["d"]) != len(b["d"]):
        return False
    bits = len(a["d"]) * 4
    close = bin(int(a["d"], 16) ^ int(b["d"], 16)).count("1") <= bits * 0.12
    ta, tb = bytes.fromhex(a.get("t", "")), bytes.fromhex(b.get("t", ""))
    if not ta or len(ta) != len(tb):
        return close
    mad = sum(abs(x - y) for x, y in zip(ta, tb)) / len(ta)
    return close and mad <= 18


def media_fingerprint(path):
    if path.lower().endswith(VIDEO_EXT):
        fr = frame_at(path, 0.0)
        return fingerprint(fr) if fr else None
    try:
        from PIL import Image
        with Image.open(path) as im:
            return fingerprint(im)
    except Exception:
        return None


def read_log(path):
    out = []
    if path and os.path.exists(path):
        with open(path, encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except ValueError:
                    continue
                if isinstance(row, dict) and row.get("postId"):
                    out.append(row)
    return out


def parse_local(at, tz=None):
    """A plan time as a naive datetime in the account's local time. Plain times ('2026-11-16T20:30')
    are local already; times with 'Z' or an offset are converted to the account's time zone `tz`."""
    if not isinstance(at, str) or not at:
        return None
    try:
        d = datetime.fromisoformat(at.strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    if d.tzinfo is not None and tz:
        d = d.astimezone(zone(tz))
    return d.replace(tzinfo=None)


def to_utc(at, tz):
    """A plan time (local, or with 'Z'/offset) as UTC ISO 8601 with Z, for WoopSocial."""
    d = datetime.fromisoformat(at.strip().replace("Z", "+00:00"))
    if d.tzinfo is None:
        d = d.replace(tzinfo=zone(tz))
    return d.astimezone(zone("UTC")).strftime("%Y-%m-%dT%H:%M:%SZ")


PLACEHOLDER = re.compile(r"<(mediaId|socialAccountId|board id) for ")


def zone(name):
    if not name:
        sys.exit("no time zone set: add \"timezone\" (e.g. America/New_York) to plan.json or the account")
    try:
        from zoneinfo import ZoneInfo
        return ZoneInfo(name)
    except Exception:
        sys.exit(f"time zone '{name}' not found. On Windows run: pip install tzdata. "
                 "Use names like Europe/London or America/New_York.")


def fmt_of(pin):
    """'video' or 'image', from the file's extension."""
    return "video" if (pin.get("file") or "").lower().endswith(VIDEO_EXT) else "image"


def check_ids(pins):
    """Pin ids become file names: letters, digits, dot, dash, underscore only."""
    seen = set()
    for i, p in enumerate(pins):
        pid = p.get("id")
        if not isinstance(pid, str) or not ID_RE.match(pid):
            sys.exit(f"pin {i + 1}: id {pid!r} must be letters, digits, '-', '_' or '.' (it becomes a file name)")
        if pid in seen:
            sys.exit(f"two pins share the id '{pid}'")
        seen.add(pid)
