#!/usr/bin/env python3
"""Génère src-tauri/icons/icon.png (1024×1024 RGBA).

Carré arrondi #14141F (fond de l'UI web) + « M » tracé en #3ECF8E (accent UI).
Aucune dépendance : le PNG est encodé à la main (zlib + struct, stdlib).
Usage : python3 scripts/gen-icon.py
"""

import math
import os
import struct
import zlib

S = 1024  # taille du canevas
BG = (0x14, 0x14, 0x1F)  # fond — identique à packages/web
FG = (0x3E, 0xCF, 0x8E)  # accent — vert Memoria de l'UI web
CORNER = 180.0  # rayon des coins (style icône macOS)
STROKE = 92.0  # épaisseur du trait du M

# Le « M » : 4 segments (x1, y1, x2, y2) dans l'espace 1024.
M_SEGMENTS = [
    (310, 700, 310, 330),
    (310, 330, 512, 565),
    (512, 565, 714, 330),
    (714, 330, 714, 700),
]


def dist_to_segment(px, py, x1, y1, x2, y2):
    """Distance euclidienne du point au segment (caps ronds gratuits)."""
    dx, dy = x2 - x1, y2 - y1
    if dx == 0 and dy == 0:
        return math.hypot(px - x1, py - y1)
    t = ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)
    t = max(0.0, min(1.0, t))
    return math.hypot(px - (x1 + t * dx), py - (y1 + t * dy))


def rounded_rect_alpha(px, py):
    """Alpha [0..1] du carré arrondi plein cadre (SDF + anti-aliasing 1px)."""
    half = S / 2.0
    qx = abs(px - half) - (half - CORNER)
    qy = abs(py - half) - (half - CORNER)
    d = math.hypot(max(qx, 0.0), max(qy, 0.0)) + min(max(qx, qy), 0.0) - CORNER
    return max(0.0, min(1.0, 0.5 - d))


def stroke_alpha(px, py):
    """Alpha [0..1] du M (distance au segment le plus proche, AA 1px)."""
    d = min(dist_to_segment(px, py, *seg) for seg in M_SEGMENTS)
    return max(0.0, min(1.0, 0.5 + (STROKE / 2.0 - d)))


def build_pixels():
    rows = []
    for y in range(S):
        row = bytearray()
        row.append(0)  # filtre PNG 0 (None) en tête de scanline
        for x in range(S):
            a_bg = rounded_rect_alpha(x + 0.5, y + 0.5)
            if a_bg <= 0.0:
                row.extend((0, 0, 0, 0))
                continue
            a_m = stroke_alpha(x + 0.5, y + 0.5)
            r = round(BG[0] + (FG[0] - BG[0]) * a_m)
            g = round(BG[1] + (FG[1] - BG[1]) * a_m)
            b = round(BG[2] + (FG[2] - BG[2]) * a_m)
            row.extend((r, g, b, round(255 * a_bg)))
        rows.append(bytes(row))
    return b"".join(rows)


def png_chunk(tag, data):
    return (
        struct.pack(">I", len(data))
        + tag
        + data
        + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    )


def main():
    out = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "src-tauri", "icons", "icon.png"
    )
    raw = build_pixels()
    ihdr = struct.pack(">IIBBBBB", S, S, 8, 6, 0, 0, 0)  # 8-bit RGBA
    png = (
        b"\x89PNG\r\n\x1a\n"
        + png_chunk(b"IHDR", ihdr)
        + png_chunk(b"IDAT", zlib.compress(raw, 9))
        + png_chunk(b"IEND", b"")
    )
    with open(out, "wb") as f:
        f.write(png)
    print(f"icône écrite : {os.path.normpath(out)} ({len(png)} octets)")


if __name__ == "__main__":
    main()
