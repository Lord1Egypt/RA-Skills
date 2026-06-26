#!/usr/bin/env python3
"""
Convert Unicode block-character QR text to a clean scannable PNG.
Block chars encode 2 QR modules per row:
  ' ' = white/white  ▀ = black/white  ▄ = white/black  █ = black/black

Usage:
  qr_decode.py <infile> <outfile> [--raw] [--scale N] [--quiet N]

  --raw     Strip ANSI escape codes and filter to QR lines only.
            Use when infile is a raw terminal capture (script -q -c or pty output).
            Safe to pass even for clean input.
  --scale   Pixel scale per module (default: 10)
  --quiet   Quiet zone modules (default: 6)
"""
import sys
import re
import struct
import zlib
import argparse

BLOCK_CHARS = set('▄▀█ ')


def strip_and_filter(text: str) -> str:
    """Strip ANSI escape codes and filter to QR block-char lines only.

    QR lines are identified as: long (>30 chars after strip), start with █,
    and consist entirely of block characters (▄▀█ space).
    """
    # Strip ANSI escape codes
    text = re.sub(r'\x1b\[[0-9;]*[mGKHFJA-Za-z]', '', text)
    text = re.sub(r'\x1b\][^\x07]*\x07', '', text)  # OSC sequences

    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if (len(stripped) > 30
                and stripped[0] in BLOCK_CHARS
                and all(c in BLOCK_CHARS for c in stripped)):
            lines.append(stripped)
    return '\n'.join(lines)


def block_to_pixels(text: str, scale: int = 10, quiet: int = 6):
    """Decode block char QR text to pixel grid."""
    UPPER = {'▀', '█'}
    LOWER = {'▄', '█'}

    lines = [l for l in text.splitlines() if l.strip()]
    if not lines:
        sys.exit("No QR data found — no valid block-char lines in input")

    # Build binary matrix (0=white, 1=black)
    matrix = []
    for line in lines:
        top_row = []
        bot_row = []
        for ch in line:
            top_row.append(1 if ch in UPPER else 0)
            bot_row.append(1 if ch in LOWER else 0)
        matrix.append(top_row)
        matrix.append(bot_row)

    cols = max(len(r) for r in matrix)
    rows = len(matrix)

    # Block char encoding always produces even row counts (2 per char line).
    # If the QR has an odd number of modules (e.g. 59), the last char line
    # encodes a phantom bottom row. Drop it: if rows > cols, trim to cols.
    if rows > cols:
        matrix = matrix[:cols]
        rows = cols

    total_w = (cols + 2 * quiet) * scale
    total_h = (rows + 2 * quiet) * scale

    pixels = [[(255, 255, 255)] * total_w for _ in range(total_h)]

    for r, row in enumerate(matrix):
        for c, val in enumerate(row):
            color = (0, 0, 0) if val else (255, 255, 255)
            for pr in range(scale):
                for pc in range(scale):
                    y = (r + quiet) * scale + pr
                    x = (c + quiet) * scale + pc
                    pixels[y][x] = color

    return pixels, total_w, total_h


def encode_png_rgb(pixels, width, height):
    def chunk(name, data):
        c = name + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xFFFFFFFF)

    ihdr = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    raw = b''
    for row in pixels:
        raw += b'\x00' + bytes(v for px in row for v in px)
    idat = zlib.compress(raw, 9)
    return (b'\x89PNG\r\n\x1a\n' +
            chunk(b'IHDR', ihdr) +
            chunk(b'IDAT', idat) +
            chunk(b'IEND', b''))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert block-char QR terminal output to PNG')
    parser.add_argument('infile', help='Input file (terminal capture or clean block-char text)')
    parser.add_argument('outfile', help='Output PNG path')
    parser.add_argument('--raw', action='store_true',
                        help='Strip ANSI codes and filter to QR lines (use for terminal captures)')
    parser.add_argument('--scale', type=int, default=10, help='Pixel scale per module (default: 10)')
    parser.add_argument('--quiet', type=int, default=6, help='Quiet zone modules (default: 6)')
    args = parser.parse_args()

    text = open(args.infile, encoding='utf-8', errors='replace').read()

    if args.raw:
        text = strip_and_filter(text)
        if not text:
            sys.exit("ERROR: No QR block-char lines found after stripping. "
                     "Check that the WhatsApp QR was captured before filtering.")

    pixels, w, h = block_to_pixels(text, scale=args.scale, quiet=args.quiet)
    png = encode_png_rgb(pixels, w, h)
    open(args.outfile, 'wb').write(png)
    print(f"Written {w}x{h} PNG to {args.outfile} ({len(png)} bytes)")
