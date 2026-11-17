#!/usr/bin/env python3
"""curate.py — offline photo archive curator: exact + perceptual dedupe, blur flags,
burst keeper selection, EXIF-dated rename into YYYY/YYYY-MM tree. Stdlib only
(Pillow optional for better decoding). DRY-RUN by default; --apply to act.

Examples:
  python3 curate.py --root ~/Photos --scan
  python3 curate.py --root ~/Photos --organize            (plan only)
  python3 curate.py --root ~/Photos --organize --apply    (do it)
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import struct
import sys
import time
from pathlib import Path

PHOTO_EXT = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".heic", ".bmp", ".webp", ".gif"}
SIDECAR_EXT = {".mov", ".mp4", ".dng"}  # moved only alongside a renamed still
THUMB = 8


# ---------- exact hash ----------
def sha256_file(p: Path, limit=None) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while True:
            b = f.read(1 << 20)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


# ---------- minimal image decode ----------
def try_pillow():
    try:
        from PIL import Image  # type: ignore
        return Image
    except Exception:
        return None


def decode_gray(path: Path):
    """Return (w, h, bytes-graychannel-ish) via Pillow if available, else None."""
    Image = try_pillow()
    if Image is None:
        return None
    try:
        im = Image.open(path)
        im.draft("L", (256, 256))
        im = im.convert("L").resize((THUMB, THUMB))
        return list(im.getdata())
    except Exception:
        return None


def gray_from_header(path: Path):
    """Pure-stdlib fallback: no pixel data; only usable for size probing.
    Returns None (caller must handle gracefully)."""
    return None


# ---------- hashes ----------
def dhash(pixels) -> int:
    # 8x8 -> compare horizontal neighbors
    bits = 0
    for row in range(THUMB):
        for col in range(THUMB - 1):
            bits = (bits << 1) | (1 if pixels[row * THUMB + col] >
                                  pixels[row * THUMB + col + 1] else 0)
    return bits


def ahash(pixels) -> int:
    mean = sum(pixels) / len(pixels)
    bits = 0
    for v in pixels:
        bits = (bits << 1) | (1 if v > mean else 0)
    return bits


def hamming(x: int, y: int) -> int:
    return bin(x ^ y).count("1")


# ---------- EXIF ----------
def exif_datetime(path: Path):
    """Extract DateTimeOriginal from JPEG APP1 EXIF (stdlib, minimal parser)."""
    try:
        with open(path, "rb") as f:
            head = f.read(256 * 1024)
        if head[:2] != b"\xff\xd8":
            return None
        i = 2
        while i < len(head) - 4:
            if head[i] != 0xFF:
                i += 1
                continue
            marker = head[i + 1]
            if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
                i += 2
                continue
            size = struct.unpack(">H", head[i + 2:i + 4])[0]
            if marker == 0xE1 and head[i + 4:i + 10] == b"Exif\x00\x00":
                tiff = head[i + 10:i + 4 + size]
                return parse_exif_tiff(tiff)
            i += 2 + size
    except Exception:
        pass
    return None


def parse_exif_tiff(tiff: bytes):
    if len(tiff) < 8:
        return None
    endian = "<" if tiff[:2] == b"II" else (">" if tiff[:2] == b"MM" else None)
    if endian is None:
        return None
    ifd0_off = struct.unpack(endian + "I", tiff[4:8])[0]

    def read_ifd(off):
        if off + 2 > len(tiff):
            return {}
        n = struct.unpack(endian + "H", tiff[off:off + 2])[0]
        tags = {}
        for k in range(n):
            e = off + 2 + k * 12
            if e + 12 > len(tiff):
                break
            tag, typ, cnt = struct.unpack(endian + "HHI", tiff[e:e + 8])
            val = tiff[e + 8:e + 12]
            tags[tag] = (typ, cnt, val)
        return tags

    ifd0 = read_ifd(ifd0_off)

    def extract_dt(tags):
        # DateTimeOriginal 0x9003 (ASCII 20) — written into IFD0 by some tools
        if 0x9003 in tags:
            typ, cnt, raw = tags[0x9003]
            if typ == 2 and cnt >= 19:
                off = struct.unpack(endian + "I", raw[:4])[0] if cnt > 4 else None
                if off is not None and off + 20 <= len(tiff):
                    s = tiff[off:off + 20].decode("ascii", "replace").split("\x00")[0]
                    m = re.match(r"(\d{4}):(\d{2}):(\d{2}) (\d{2}):(\d{2}):(\d{2})", s)
                    if m:
                        y, mo, d, h, mi, sec = map(int, m.groups())
                        if 1990 <= y <= 2100:
                            return (y, mo, d, h, mi, sec)
        return None

    dt = extract_dt(ifd0)
    if dt:
        return dt
    # else follow Exif sub-IFD pointer (0x8769) — where cameras put it
    if 0x8769 in ifd0:
        typ, cnt, val = ifd0[0x8769]
        if typ == 4:
            ptr = struct.unpack(endian + "I", val[:4])[0]
            exif = read_ifd(ptr)
            return extract_dt(exif)
    return None


def stamp_of(p: Path):
    """(datetime_tuple, dated_by) — exif preferred, mtime fallback."""
    dt = exif_datetime(p)
    if dt:
        return dt, "exif"
    t = time.localtime(p.stat().st_mtime)
    return (t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec), "mtime"


def stamp_str(dt, dated_by):
    s = "%04d%02d%02d-%02d%02d%02d" % dt
    return s + "~" if dated_by == "mtime" else s


# ---------- scan ----------
def scan(root: Path):
    files = sorted(p for p in root.rglob("*")
                   if p.is_file() and p.suffix.lower() in PHOTO_EXT
                   and "_cull" not in p.parts)
    print(f"Photos: {len(files)}")

    by_sha = {}
    exact_dupes = []
    for p in files:
        d = sha256_file(p)
        if d in by_sha:
            exact_dupes.append((by_sha[d], p))
        else:
            by_sha[d] = p
    print(f"Exact duplicates: {len(exact_dupes)} "
          f"({sum(p.stat().st_size for _, p in exact_dupes) / 1e6:.1f} MB)")

    Image = try_pillow()
    hashes, blurvars, undated = {}, {}, 0
    if Image is not None:
        t0 = time.time()
        for idx, p in enumerate(files):
            px = decode_gray(p)
            if px is None:
                continue
            hashes[p] = (ahash(px), dhash(px))
            # blur proxy: variance of the 64 gray values (relative use only)
            mean = sum(px) / len(px)
            blurvars[p] = sum((v - mean) ** 2 for v in px) / len(px)
            if idx % 2000 == 0 and idx:
                print(f"  hashed {idx}/{len(files)} ({time.time()-t0:.0f}s)", file=sys.stderr)
        keys = list(hashes.keys())
        near = []
        for i in range(len(keys)):
            a = hashes[keys[i]]
            for j in range(i + 1, len(keys)):
                b = hashes[keys[j]]
                d = min(hamming(a[0], b[0]), hamming(a[1], b[1]))
                if d <= 6:
                    near.append((keys[i], keys[j], d))
        print(f"Near duplicates (dist<=6): {len(near)} pairs")
        med = sorted(blurvars.values())
        median_var = med[len(med) // 2] if med else 0.0
        blurry = [p for p, v in blurvars.items() if v < median_var * 0.10] if median_var else []
        print(f"Blur candidates (var < 10% of archive median): {len(blurry)}")
    else:
        print("Pillow not found — skipping perceptual/blur pass (pip install pillow to enable).")
        near, blurry = [], []

    for p in files:
        if stamp_of(p)[1] == "mtime":
            undated += 1
    print(f"Undated (no EXIF, mtime used): {undated}")

    # burst groups: consecutive EXIF times within 2s
    dated = sorted((stamp_of(p)[0], p) for p in files)
    bursts, cur = [], [dated[0][1]] if dated else []
    for (t0_, p0), (t1, p1) in zip(dated, dated[1:]):
        gap = (sum(x * f for x, f in zip(t1, (31536000, 2592000, 86400, 3600, 60, 1))) -
               sum(x * f for x, f in zip(t0_, (31536000, 2592000, 86400, 3600, 60, 1))))
        if gap <= 2:
            cur.append(p1)
        else:
            if len(cur) >= 3:
                bursts.append(cur)
            cur = [p1]
    if len(cur) >= 3:
        bursts.append(cur)
    keep_stats = []
    for g in bursts:
        keeper = max(g, key=lambda p: (blurvars.get(p, 0.0), p.stat().st_size))
        keep_stats.append((len(g), keeper.name, [x.name for x in g if x != keeper]))
    print(f"Burst groups (>=3 shots within 2s): {len(bursts)} "
          f"({sum(len(g) for g in bursts)} files, {sum(len(g) - 1 for g in bursts)} cull candidates)")
    return {"files": [str(p) for p in files], "exact_dupes": [(str(a), str(b)) for a, b in exact_dupes],
            "near": [(str(a), str(b), d) for a, b, d in near][:200],
            "blurry": [str(p) for p in blurry], "bursts": keep_stats[:50]}


# ---------- organize ----------
def organize(root: Path, apply_ops: bool):
    files = [p for p in root.rglob("*")
             if p.is_file() and (p.suffix.lower() in PHOTO_EXT or p.suffix.lower() in SIDECAR_EXT)
             and "_cull" not in p.parts]
    used = {}
    plan = []
    for p in sorted(files):
        dt, src = stamp_of(p)
        if p.suffix.lower() in SIDECAR_EXT and Path(str(p.with_suffix(".jpg"))) in files:
            continue  # sidecar moves with its still, handled below
        base = stamp_str(dt, src)
        key = base
        n = 1
        while key in used:
            n += 1
            key = f"{base}-{n}"
        used[key] = p
        dest = root / f"{dt[0]:04d}" / f"{dt[0]:04d}-{dt[1]:02d}" / f"{key}{p.suffix.lower()}"
        rel = os.path.relpath(dest, root)
        if dest == p:
            plan.append(("KEEP", str(p)))
            continue
        plan.append(("MOVE", f"{p} -> {rel}"))
        # sidecar twin
        for ext in SIDECAR_EXT:
            twin = p.with_suffix(ext)
            if twin.exists():
                tdest = dest.with_suffix(ext)
                plan.append(("MOVE", f"{twin} -> {os.path.relpath(tdest, root)}"))
    print(f"Plan: {sum(1 for k, _ in plan if k == 'MOVE')} moves, "
          f"{sum(1 for k, _ in plan if k == 'KEEP')} already correct")
    logf = root / "_curate_log.jsonl"
    if apply_ops:
        with open(logf, "a", encoding="utf-8") as lf:
            for kind, desc in plan:
                if kind == "MOVE":
                    src_, dst_ = desc.split(" -> ")
                    dst_p = root / dst_
                    dst_p.parent.mkdir(parents=True, exist_ok=True)
                    if dst_p.exists():
                        print(f"  SKIP (exists): {dst_}")
                        continue
                    shutil.move(src_, dst_p)
                lf.write(json.dumps({"ts": time.time(), "op": kind, "detail": desc}) + "\n")
        print(f"Applied. Log: {logf}")
    else:
        for kind, desc in plan[:20]:
            print(f"  [{kind}] {desc}")
        print("… dry run; pass --apply to execute")
    return plan


def main():
    p = argparse.ArgumentParser(description="Offline photo curator (dry-run default).")
    p.add_argument("--root", required=True)
    p.add_argument("--scan", action="store_true")
    p.add_argument("--organize", action="store_true")
    p.add_argument("--apply", action="store_true")
    a = p.parse_args()
    root = Path(a.root).expanduser().resolve()
    if not root.is_dir():
        sys.exit(f"not a dir: {root}")
    if a.scan:
        report = scan(root)
        (root / "_scan_report.json").write_text(json.dumps(report, indent=1)[:400000])
        print("Full report: _scan_report.json")
    if a.organize:
        organize(root, a.apply)
    if not (a.scan or a.organize):
        print("Nothing to do: pass --scan and/or --organize [--apply]")


if __name__ == "__main__":
    main()
