"""Inspect painted glyph IDs: a valid ToUnicode map can hide missing glyphs."""
from pathlib import Path


def _is_missing(codepoint: int, glyph: int) -> bool:
    """Glyph 0 is .notdef — the box a font draws for a character it lacks.

    Decide on the glyph id alone. The codepoint the PDF reports for a .notdef
    cannot be trusted: XeTeX/Tectonic write U+FFFF (a noncharacter, category
    Cn) for every glyph they could not map, so a filter that skipped "C*"
    categories passed a report whose ✓ had become a box. Only whitespace and
    C0 controls are exempt, because those are never painted ink.
    """
    if glyph != 0:
        return False
    if 0 <= codepoint < 0x20:
        return False
    try:
        return not chr(codepoint).isspace()
    except (ValueError, OverflowError):
        return True


def glyph_findings(path) -> list[str]:
    try:
        import pymupdf
        missing = set()
        with pymupdf.open(path) as document:
            for page in document:
                for span in page.get_texttrace():
                    if span.get("type") == 3:  # invisible OCR/search layer
                        continue
                    for codepoint, glyph, *_ in span["chars"]:
                        if _is_missing(codepoint, glyph):
                            missing.add(codepoint)
        if missing:
            return [f"MISSING_PDF_GLYPHS: {Path(path).name}: " +
                    ", ".join(f"U+{c:04X}" for c in sorted(missing))]
        return []
    except Exception as exc:
        return [f"PDF_GLYPHS_UNVERIFIED: {Path(path).name}: {exc}"]
