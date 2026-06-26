#!/usr/bin/env python3
"""
PDF Text Replace v2.0 - Universal Entry Point
==============================================
Auto-selects the best replacement strategy based on PDF characteristics.

Usage:
    python3 pdf_text_replace.py input.pdf "old text" "new text" [output.pdf]
    python3 pdf_text_replace.py input.pdf "old" "new" --color 1,0,0 --size 14
    python3 pdf_text_replace.py input.pdf "old" "new" --password secret
    python3 pdf_text_replace.py input.pdf "old" "new" --force-ocr

Strategy pipeline (auto-selected):
    L6 → Decrypt encrypted PDFs (pikepdf)
    L5 → OCR pipeline for image-based PDFs (paddleocr / pytesseract)
    L1 → Direct byte-code swap (equal-length, chars in font)
    L2 → Tz scaling or reflow (variable-length replacement)
    L3 → Cross-Tj multi-operation replacement
    L4 → Style overlay (color, font-size, underline, bold)

Dependencies (core):
    pip3 install pypdf pdfplumber fonttools pdf2image Pillow

Optional (for full v2 capabilities):
    pip3 install pikepdf          # L6: encrypted PDFs
    pip3 install paddleocr        # L5: OCR (preferred)
    pip3 install pytesseract      # L5: OCR (fallback)
    pip3 install opencv-python    # L5: image preprocessing
    pip3 install pymupdf          # L4: style overlays
"""

import sys
import re
import io
import time
import argparse
import logging
from pathlib import Path
from typing import Optional, Tuple

# ── Core dependencies ──────────────────────────────────────────────────────────
from pypdf import PdfReader, PdfWriter
from pypdf.generic import (
    NameObject, NumberObject, ArrayObject,
    DictionaryObject, DecodedStreamObject,
)
from fontTools.ttLib import TTFont
from fontTools import subset as ft_subset
import pdfplumber

# ── Optional v2 feature modules (graceful degradation) ────────────────────────
try:
    from v2_l6_decrypt import decrypt_pdf, is_encrypted
    HAS_L6 = True
except ImportError:
    HAS_L6 = False

try:
    from v2_l5_ocr import is_image_based, replace_text_ocr
    HAS_L5 = True
except ImportError:
    HAS_L5 = False

try:
    from v2_l4_style import apply_style_overlay, StyleOptions
    HAS_L4 = True
except ImportError:
    HAS_L4 = False

try:
    from v2_l3_multitj import replace_multi_tj
    HAS_L3 = True
except ImportError:
    HAS_L3 = False

try:
    from v2_l2_varlen import replace_variable_length
    HAS_L2 = True
except ImportError:
    HAS_L2 = False

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)


# ── Font fallbacks ─────────────────────────────────────────────────────────────
FONT_FALLBACKS = {
    "serif": [
        "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
        "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf",
        "/System/Library/Fonts/Supplemental/Georgia.ttf",
        "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
    ],
    "sans": [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Supplemental/Verdana Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ],
}


def find_system_font(prefer_serif: bool = True) -> str:
    """Find first available system font."""
    key = "serif" if prefer_serif else "sans"
    for path in FONT_FALLBACKS[key]:
        if Path(path).exists():
            return path
    for p in Path("/usr/share/fonts").rglob("*.ttf"):
        if "bold" in p.name.lower():
            return str(p)
    raise FileNotFoundError("No suitable system font found")


def parse_cmap(cmap_data: str) -> dict:
    """Parse PDF ToUnicode CMap -> {byte_code: unicode_char}.

    Handles all common CMap formats:

    beginbfrange section — maps contiguous byte ranges:
      <20><20><0032>       single-char range (start == end)
      <20><25><4e2d>       multi-char range: codes 0x20–0x25 → U+4E2D, U+4E2E, …
      <20> <25> <4e2d>     same but space-separated (some PDF generators)

    beginbfchar section — maps individual bytes:
      <32> <0032>          byte 0x32 → U+0032
    """
    mapping = {}

    # ── beginbfrange sections ──────────────────────────────────────────────────
    # Parse only within beginbfrange...endbfrange to avoid false positives.
    # Each line: <start> <end> <base_unicode> (with or without spaces between hex tokens)
    hex_tok = r"<([0-9a-fA-F]+)>"
    range_pat = re.compile(
        hex_tok + r"\s*" + hex_tok + r"\s*" + hex_tok
    )
    for section in re.findall(r"beginbfrange(.*?)endbfrange", cmap_data, re.DOTALL):
        for m in range_pat.finditer(section):
            start = int(m.group(1), 16)
            end   = int(m.group(2), 16)
            base  = int(m.group(3), 16)
            # Expand the full range (start..end inclusive)
            for offset in range(end - start + 1):
                code = start + offset
                if code not in mapping:
                    mapping[code] = chr(base + offset)

    # ── beginbfchar sections ───────────────────────────────────────────────────
    # Parse only within beginbfchar...endbfchar to avoid mis-matching bfrange lines.
    pair_pat = re.compile(r"<([0-9a-fA-F]{2,4})>\s+<([0-9a-fA-F]{4})>")
    for section in re.findall(r"beginbfchar(.*?)endbfchar", cmap_data, re.DOTALL):
        for m in pair_pat.finditer(section):
            dst_hex = m.group(2)
            if dst_hex == "0000":
                continue
            code = int(m.group(1), 16)
            if code not in mapping:   # bfrange entries take precedence
                mapping[code] = chr(int(dst_hex, 16))

    return mapping


def encode_string(text: str, char_to_code: dict) -> str:
    """Encode a text string using the font's reverse CMap."""
    return "".join(chr(char_to_code[c]) for c in text)


def create_font_subset(system_font_path: str, chars: str) -> bytes:
    """Create a minimal TrueType font subset containing only the given chars."""
    font = TTFont(system_font_path)
    subsetter = ft_subset.Subsetter()
    subsetter.populate(text=chars)
    subsetter.subset(font)
    buf = io.BytesIO()
    font.save(buf)
    return buf.getvalue()


def build_pdf_font(writer: PdfWriter, subset_data: bytes, chars: str):
    """Build PDF font objects for the replacement font. Returns IndirectObject."""
    fstream = DecodedStreamObject()
    fstream.set_data(subset_data)
    fstream[NameObject("/Length1")] = NumberObject(len(subset_data))

    fdesc = DictionaryObject()
    for k, v in [
        ("/Type", "/FontDescriptor"), ("/FontName", "/ZZZZZZ+ReplacementFont"),
        ("/Flags", 32), ("/ItalicAngle", 0), ("/Ascent", 917),
        ("/Descent", -230), ("/CapHeight", 692), ("/StemV", 139),
    ]:
        fdesc[NameObject(k)] = NumberObject(v) if isinstance(v, int) else NameObject(v)
    fdesc[NameObject("/FontBBox")] = ArrayObject(
        [NumberObject(x) for x in [-222, -218, 1389, 939]]
    )
    fdesc[NameObject("/FontFile2")] = writer._add_object(fstream)

    ranges = "\n".join(
        f"<{ord(c):02X}><{ord(c):02X}><{ord(c):04X}>" for c in chars
    )
    cmap_bytes = (
        "/CIDInit /ProcSet findresource begin\n"
        "12 dict begin begincmap\n"
        "/CIDSystemInfo << /Registry (Adobe) /Ordering (UCS) /Supplement 0 >> def\n"
        "/CMapName /Adobe-Identity-UCS def /CMapType 2 def\n"
        "1 begincodespacerange <00><FF> endcodespacerange\n"
        f"{len(chars)} beginbfrange\n{ranges}\n"
        "endbfrange\nendcmap\n"
        "CMapName currentdict /CMap defineresource pop end end\n"
    ).encode("latin-1")
    tu_stream = DecodedStreamObject()
    tu_stream.set_data(cmap_bytes)

    codes = sorted(ord(c) for c in chars)
    fdict = DictionaryObject()
    for k, v in [
        ("/Type", "/Font"), ("/Subtype", "/TrueType"),
        ("/BaseFont", "/ZZZZZZ+ReplacementFont"),
        ("/Encoding", "/WinAnsiEncoding"),
    ]:
        fdict[NameObject(k)] = NameObject(v)
    fdict[NameObject("/FirstChar")] = NumberObject(codes[0])
    fdict[NameObject("/LastChar")] = NumberObject(codes[-1])

    tt = TTFont(io.BytesIO(subset_data))
    hmtx = tt["hmtx"]
    upem = tt["head"].unitsPerEm
    best_cmap = tt.getBestCmap()
    widths = []
    for code in range(codes[0], codes[-1] + 1):
        gname = best_cmap.get(code)
        w = hmtx[gname][0] * 1000 // upem if gname else 0
        widths.append(NumberObject(w))
    fdict[NameObject("/Widths")] = ArrayObject(widths)
    fdict[NameObject("/FontDescriptor")] = writer._add_object(fdesc)
    fdict[NameObject("/ToUnicode")] = writer._add_object(tu_stream)

    return writer._add_object(fdict)


def _detect_strategy(
    input_path: str,
    old_text: str,
    page_num: int,
    password: str,
    force_ocr: bool,
) -> str:
    """
    Analyse the PDF and return the recommended replacement strategy.

    Returns one of: 'ocr', 'direct', 'varlen', 'multitj', 'unknown'
    """
    if force_ocr:
        return "ocr"

    # L6: encrypted?
    reader = PdfReader(input_path)
    if reader.is_encrypted:
        return "encrypted"  # caller handles decrypt first

    # L5: image-based?
    if HAS_L5 and is_image_based(input_path, page_num):
        return "ocr"

    # Try to find old_text in extracted text
    try:
        with pdfplumber.open(input_path) as pdf:
            page_text = pdf.pages[page_num].extract_text() or ""
    except Exception:
        page_text = ""

    if old_text not in page_text:
        # Might be image-based even without L5
        return "ocr"

    # Inspect content stream for multi-Tj patterns
    page = reader.pages[page_num]
    fonts = page.get("/Resources", {}).get("/Font", {})
    for _, fref in fonts.items():
        font = fref.get_object()
        if "/ToUnicode" not in font:
            continue
        cmap_str = font["/ToUnicode"].get_object().get_data().decode("latin-1")
        mapping = parse_cmap(cmap_str)
        reverse = {v: k for k, v in mapping.items()}
        if all(c in reverse for c in old_text):
            # Font found; check length delta
            if len(old_text) == len(new_text_placeholder):
                return "direct"
            return "varlen"

    # If no single font covers all chars, likely multi-Tj
    return "multitj"


# Sentinel used only inside _detect_strategy; replace() receives real values.
new_text_placeholder = ""


def _core_replace(
    input_path: str,
    old_text: str,
    new_text: str,
    output_path: str,
    page_num: int,
) -> bool:
    """
    Core L1/L2/L3 text replacement (the original battle-tested algorithm).
    Handles equal-length direct swap, variable-length overlay, and multi-Tj.
    """
    reader = PdfReader(input_path)
    page = reader.pages[page_num]

    fonts = page["/Resources"]["/Font"]
    target_font = None
    cmap = {}
    font_upem = 2048
    char_width = 1213

    for fname, fref in fonts.items():
        font = fref.get_object()
        if "/ToUnicode" not in font:
            continue
        cmap_str = font["/ToUnicode"].get_object().get_data().decode("latin-1")
        mapping = parse_cmap(cmap_str)
        reverse = {v: k for k, v in mapping.items()}
        if all(c in reverse for c in old_text):
            target_font = fname
            cmap = mapping
            fd = font["/FontDescriptor"].get_object()
            fdata = fd["/FontFile2"].get_object().get_data()
            tt = TTFont(io.BytesIO(fdata))
            font_upem = tt["head"].unitsPerEm
            hmtx = tt["hmtx"]
            # Build per-code width map using font's INTERNAL cmap (not PDF ToUnicode)
            code_to_width = {}
            font_cmap = None
            for cmap_table in tt["cmap"].tables:
                if cmap_table.cmap:
                    font_cmap = cmap_table.cmap
                    break
            if font_cmap:
                for code_val in mapping:
                    glyph_name = font_cmap.get(code_val)
                    if glyph_name and glyph_name in hmtx.metrics:
                        code_to_width[code_val] = hmtx[glyph_name][0]
            char_width = next(iter(code_to_width.values()), 1213)  # fallback
            break

    if target_font is None:
        log.error("Could not identify the font rendering '%s'", old_text)
        return False

    char_to_code = {v: k for k, v in cmap.items()}
    encoded_old = encode_string(old_text, char_to_code)

    missing_chars = [c for c in new_text if c not in char_to_code]
    common_prefix = ""
    for i, c in enumerate(new_text):
        if c in char_to_code and i < len(old_text):
            common_prefix += c
        else:
            break

    log.info("Font: %s | Missing chars: %s", target_font, missing_chars)

    writer = PdfWriter()
    writer.append_pages_from_reader(reader)
    out_page = writer.pages[page_num]

    new_font_name = None
    if missing_chars:
        sys_font = find_system_font(prefer_serif=True)
        overlay_chars = new_text[len(common_prefix):]
        subset_data = create_font_subset(sys_font, overlay_chars)
        font_ref = build_pdf_font(writer, subset_data, overlay_chars)

        existing = set(str(k) for k in out_page["/Resources"]["/Font"].keys())
        for i in range(9, 30):
            candidate = f"/TT{i}"
            if candidate not in existing:
                new_font_name = candidate
                break
        out_page["/Resources"]["/Font"][NameObject(new_font_name)] = font_ref
        log.info("Added replacement font as %s", new_font_name)

    contents = out_page["/Contents"]
    if not isinstance(contents, list):
        contents = [contents]

    modified = False
    for content_ref in contents:
        content_obj = content_ref.get_object()
        data = content_obj.get_data()
        decoded = data.decode("latin-1")

        old_pattern = f"({encoded_old})"
        if old_pattern not in decoded:
            continue

        idx = decoded.find(old_pattern)
        block = decoded[max(0, idx - 300):idx]

        cm_matches = list(re.finditer(r"1\s+0\s+0\s+1\s+([\d.]+)\s+([\d.]+)\s+cm", block))
        tm_matches = list(re.finditer(r"(\d+)\s+0\s+0\s+(\d+)\s+([\d.]+)\s+([\d.]+)\s+Tm", block))
        tc_matches = list(re.finditer(r"([\d.]+)\s+Tc", block))

        cm_x = float(cm_matches[-1].group(1)) if cm_matches else 0
        cm_y = float(cm_matches[-1].group(2)) if cm_matches else 0
        font_size = int(tm_matches[-1].group(1)) if tm_matches else 18
        tm_x = float(tm_matches[-1].group(3)) if tm_matches else 0
        tc = float(tc_matches[-1].group(1)) if tc_matches else 0

        if missing_chars:
            encoded_prefix = encode_string(common_prefix, char_to_code)
            # Sum actual per-character widths for precise positioning
            x_overlay = tm_x
            for c in common_prefix:
                c_code = char_to_code[c]
                c_width = code_to_width.get(c_code, char_width)
                x_overlay += c_width / font_upem * font_size + tc
            overlay_text = new_text[len(common_prefix):]

            new_op = (
                f"ET Q q 1 0 0 1 {cm_x} {cm_y} cm BT 0 Tc "
                f"{font_size} 0 0 {font_size} {x_overlay:.4f} 0 Tm "
                f"{new_font_name} 1 Tf ({overlay_text}) Tj"
            )
            decoded = decoded.replace(
                f"{old_pattern} Tj",
                f"({encoded_prefix}) Tj {new_op}",
            )
        else:
            encoded_new = encode_string(new_text, char_to_code)
            decoded = decoded.replace(old_pattern, f"({encoded_new})")

        content_obj.set_data(decoded.encode("latin-1"))
        modified = True
        log.info("Content stream modified")

    if not modified:
        log.warning("Pattern not found in any content stream")
        return False

    with open(output_path, "wb") as f:
        writer.write(f)

    return True


def _verify(output_path: str, old_text: str, new_text: str, page_num: int) -> bool:
    """Text-extraction and optional visual verification."""
    try:
        v = PdfReader(output_path)
        vtext = v.pages[page_num].extract_text() or ""
        ok = new_text in vtext and old_text not in vtext
        log.info("Text verification: %s", "PASS" if ok else "FAIL")
        log.info("  has '%s': %s", new_text, new_text in vtext)
        log.info("  no  '%s': %s", old_text, old_text not in vtext)
    except Exception as e:
        log.warning("Text verification error: %s", e)
        ok = False

    # Visual verification (non-blocking)
    try:
        from pdf2image import convert_from_path
        imgs = convert_from_path(output_path, dpi=300)
        s = 300 / 72
        with pdfplumber.open(output_path) as pdf:
            chars = pdf.pages[page_num].chars
            targets = [c for c in chars if c["text"] in list(new_text)]
            if targets:
                y_c = int(targets[0]["top"] * s)
                x_c = int(targets[0]["x0"] * s)
                region = imgs[page_num].crop((
                    max(0, x_c - int(50 * s)),
                    max(0, y_c - int(15 * s)),
                    min(imgs[page_num].width, x_c + int(150 * s)),
                    min(imgs[page_num].height, y_c + int(25 * s)),
                ))
                verify_path = "/tmp/pdf_replace_verify.png"
                region.save(verify_path)
                log.info("Visual verification saved: %s", verify_path)
    except Exception as e:
        log.info("Visual verification skipped: %s", e)

    return ok


def replace_text(
    input_path: str,
    old_text: str,
    new_text: str,
    output_path: str = None,
    page_num: int = 0,
    # Style options (L4)
    color: tuple = None,       # RGB tuple, e.g. (1, 0, 0) for red
    font_size: int = None,     # New font size in points
    underline: bool = False,   # Add underline
    bold: bool = None,         # Toggle bold
    # Advanced options
    password: str = "",        # For encrypted PDFs (L6)
    force_ocr: bool = False,   # Force image-based pipeline (L5)
) -> bool:
    """
    Universal PDF text replacement - auto-selects the best strategy:

    1. Checks encryption -> decrypts if needed (L6)
    2. Checks if image-based -> uses OCR pipeline (L5)
    3. Analyzes font encoding -> determines replacement strategy
    4. Equal length -> direct code swap (L1)
    5. Variable length -> Tz scaling or reflow (L2)
    6. Multi-Tj text -> cross-operation replacement (L3)
    7. Applies style changes if requested (L4)
    8. Verifies result (text + visual)

    Returns True if successful.
    """
    global new_text_placeholder
    new_text_placeholder = new_text  # used by _detect_strategy

    start = time.time()
    input_path = str(input_path)

    # Default output path
    if output_path is None:
        stem = Path(input_path).stem
        suffix = Path(input_path).suffix
        output_path = str(Path(input_path).parent / f"{stem}_modified{suffix}")

    log.info("PDF Text Replace v2.0")
    log.info("  Input:  %s", input_path)
    log.info("  Output: %s", output_path)
    log.info("  Replace '%s' -> '%s' (page %d)", old_text, new_text, page_num)

    work_path = input_path  # may change after decrypt

    # ── Step 1: Encryption (L6) ────────────────────────────────────────────────
    reader_check = PdfReader(input_path)
    if reader_check.is_encrypted:
        if HAS_L6:
            log.info("PDF is encrypted - attempting decrypt (L6)")
            decrypted_path = "/tmp/pdf_decrypted_work.pdf"
            if not decrypt_pdf(input_path, decrypted_path, password):
                log.error("Decryption failed. Wrong password?")
                return False
            work_path = decrypted_path
        else:
            log.warning(
                "PDF is encrypted but pikepdf is not installed. "
                "Install with: pip install pikepdf"
            )
            # Try pypdf's built-in decrypt
            if password:
                try:
                    reader_check.decrypt(password)
                    log.info("Decrypted with pypdf (basic RC4/AES)")
                except Exception as e:
                    log.error("pypdf decrypt failed: %s", e)
                    return False
            else:
                log.error("Encrypted PDF requires --password")
                return False

    # ── Step 2: Image-based detection (L5) ────────────────────────────────────
    if force_ocr or (HAS_L5 and is_image_based(work_path, page_num)):
        if HAS_L5:
            log.info("Image-based PDF detected - using OCR pipeline (L5)")
            ok = replace_text_ocr(
                work_path, old_text, new_text, output_path, page_num
            )
        else:
            log.error(
                "Image-based PDF requires OCR dependencies. "
                "Install: pip install paddleocr opencv-python"
            )
            return False
    else:
        # ── Step 3-6: Text-based strategies ───────────────────────────────────
        # First check text is actually present
        try:
            with pdfplumber.open(work_path) as pdf:
                page_text = pdf.pages[page_num].extract_text() or ""
        except Exception as e:
            log.error("pdfplumber extraction failed: %s", e)
            page_text = ""

        if old_text not in page_text:
            log.error("'%s' not found in page %d text", old_text, page_num)
            log.info("Extracted text (first 200 chars): %s", page_text[:200])
            return False

        # Try L3 (multi-Tj) first if module available and replacement seems complex
        used_strategy = None
        ok = False

        if HAS_L3 and len(old_text) > 4:
            log.info("Attempting multi-Tj strategy (L3)")
            ok = replace_multi_tj(work_path, old_text, new_text, output_path, page_num)
            if ok:
                used_strategy = "L3"

        if not ok:
            # L2: variable-length replacement
            if HAS_L2 and len(old_text) != len(new_text):
                log.info("Attempting variable-length strategy (L2)")
                ok = replace_variable_length(
                    work_path, old_text, new_text, output_path, page_num
                )
                if ok:
                    used_strategy = "L2"

        if not ok:
            # L1: direct byte-code swap (core algorithm)
            log.info("Using core replacement strategy (L1)")
            ok = _core_replace(work_path, old_text, new_text, output_path, page_num)
            if ok:
                used_strategy = "L1"

        if not ok:
            log.error("All replacement strategies failed")
            return False

        log.info("Strategy used: %s", used_strategy)

    # ── Step 7: Style overlay (L4) ────────────────────────────────────────────
    has_style = any([color, font_size, underline, bold is not None])
    if has_style:
        if HAS_L4:
            log.info("Applying style overlay (L4)")
            opts = StyleOptions(
                color=color,
                font_size=font_size,
                underline=underline,
                bold=bold,
            )
            style_ok = apply_style_overlay(output_path, new_text, opts, page_num)
            if not style_ok:
                log.warning("Style overlay failed; text was replaced but unstyled")
        else:
            log.warning(
                "Style options requested but pymupdf not installed. "
                "Install with: pip install pymupdf"
            )

    # ── Step 8: Verify ────────────────────────────────────────────────────────
    ok = _verify(output_path, old_text, new_text, page_num)

    elapsed = time.time() - start
    log.info("Done in %.2fs -> %s", elapsed, output_path)
    return ok


# ── CLI ────────────────────────────────────────────────────────────────────────

def _parse_color(s: str) -> Optional[Tuple[float, float, float]]:
    """Parse '1,0,0' or '255,0,0' into a normalized (r,g,b) tuple."""
    parts = [float(x.strip()) for x in s.split(",")]
    if len(parts) != 3:
        raise argparse.ArgumentTypeError("Color must be R,G,B (e.g. 1,0,0 or 255,0,0)")
    # Auto-normalize: if any value > 1, assume 0-255 range
    if any(v > 1 for v in parts):
        parts = [v / 255.0 for v in parts]
    return tuple(parts)


def main():
    parser = argparse.ArgumentParser(
        description="PDF Text Replace v2.0 - replace text while preserving visual fidelity",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic replacement
  python3 pdf_text_replace.py cert.pdf "2025" "2026"

  # With output path
  python3 pdf_text_replace.py cert.pdf "2025" "2026" output.pdf

  # Change text color to red
  python3 pdf_text_replace.py cert.pdf "Draft" "Final" --color 1,0,0

  # Change font size
  python3 pdf_text_replace.py cert.pdf "Small" "Small" --size 18

  # Add underline + bold
  python3 pdf_text_replace.py cert.pdf "name" "name" --underline --bold

  # Encrypted PDF
  python3 pdf_text_replace.py secret.pdf "old" "new" --password mypassword

  # Force OCR (image-based PDF)
  python3 pdf_text_replace.py scan.pdf "old" "new" --force-ocr

  # Specific page (0-indexed)
  python3 pdf_text_replace.py multi.pdf "old" "new" --page 2
""",
    )

    parser.add_argument("input", help="Input PDF path")
    parser.add_argument("old_text", help="Text to find and replace")
    parser.add_argument("new_text", help="Replacement text")
    parser.add_argument("output", nargs="?", help="Output PDF path (default: input_modified.pdf)")

    # Style options (L4)
    style_group = parser.add_argument_group("Style options (requires pymupdf)")
    style_group.add_argument(
        "--color", type=_parse_color, metavar="R,G,B",
        help="Text color as R,G,B values (0-1 or 0-255), e.g. 1,0,0 for red"
    )
    style_group.add_argument(
        "--size", type=int, dest="font_size", metavar="N",
        help="Font size in points"
    )
    style_group.add_argument(
        "--underline", action="store_true",
        help="Add underline to replacement text"
    )
    style_group.add_argument(
        "--bold", action="store_true", default=None,
        help="Make replacement text bold"
    )

    # Advanced options
    adv_group = parser.add_argument_group("Advanced options")
    adv_group.add_argument(
        "--password", default="", metavar="PWD",
        help="Password for encrypted PDFs"
    )
    adv_group.add_argument(
        "--force-ocr", action="store_true",
        help="Force OCR pipeline (for image-based PDFs)"
    )
    adv_group.add_argument(
        "--page", type=int, default=0, metavar="N",
        help="0-based page number (default: 0)"
    )
    adv_group.add_argument(
        "--verbose", action="store_true",
        help="Enable verbose debug output"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    ok = replace_text(
        input_path=args.input,
        old_text=args.old_text,
        new_text=args.new_text,
        output_path=args.output,
        page_num=args.page,
        color=args.color,
        font_size=args.font_size,
        underline=args.underline,
        bold=args.bold if args.bold else None,
        password=args.password,
        force_ocr=args.force_ocr,
    )

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
