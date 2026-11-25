# -*- coding: utf-8 -*-
"""PolicyForge: render a .docx through Word to PDF and PNG for visual inspection.

Requires: pywin32 (win32com), PyMuPDF (fitz), and Microsoft Word on Windows.

Usage
    python verify_docx_render.py document.docx
    python verify_docx_render.py document.docx --outdir _preview --dpi 170
    python verify_docx_render.py document.docx --pages 1,5,9,-1
    python verify_docx_render.py document.docx --keep-pdf

What it prints
    Word's own page / paragraph / table counts, the PDF path and size, then one
    PNG path per page (or only the requested pages).

Which pages to inspect
    title page      title centred, subtitle indent, page number present
    table page      columns inside the margin, header shading, no clipped cells
    placeholder page  red placeholders legible, brackets intact
    appendix page   starts on a new page, header row repeats, last row visible
    final page      body complete, page numbers consecutive

Cleanup
    * A preview PDF can stay locked by an office preview process after the COM
      object exits. Do not block on it: retry later in a short loop and report
      honestly instead of claiming it was deleted.
    * Forcing an office process to quit leaves owner files whose names start with
      a tilde next to the document; remove those separately.
    * Always close the PyMuPDF document.
"""

from __future__ import annotations

import argparse
import os
import sys


def utf8_console() -> None:
    """Align stdout with a UTF-8 console code page so Chinese output is not mangled."""
    if os.name != "nt":
        return
    try:
        import ctypes

        if ctypes.windll.kernel32.GetConsoleOutputCP() == 65001:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def parse_pages(spec: str, total: int) -> list[int]:
    """Accept '1,5,-1' style lists; negative values count from the end."""
    if not spec:
        return list(range(1, total + 1))
    wanted = []
    for chunk in spec.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        number = int(chunk)
        wanted.append(number if number > 0 else max(1, total + 1 + number))
    return sorted({n for n in wanted if 1 <= n <= total})


def word_to_pdf(source: str, pdf_path: str) -> tuple[int, int, int]:
    """Save as PDF through Word COM; return (pages, paragraphs, tables)."""
    try:
        import win32com.client  # type: ignore
    except ImportError:
        raise SystemExit("pywin32 is required for this step:  pip install pywin32")

    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    try:
        document = word.Documents.Open(os.path.abspath(source))
        try:
            document.Fields.Update()  # resolve the PAGE field before exporting
        except Exception as exc:
            print("[warn] field update skipped: %s" % exc)
        document.SaveAs(os.path.abspath(pdf_path), FileFormat=17)  # 17 = wdFormatPDF
        pages = document.ComputeStatistics(2)                      # 2 = wdStatisticPages
        paragraphs = document.Paragraphs.Count
        tables = document.Tables.Count
        document.Close(False)
        return int(pages), int(paragraphs), int(tables)
    finally:
        word.Quit()


def pdf_to_png(pdf_path: str, outdir: str, pages: str, zoom: float) -> list[str]:
    try:
        import fitz  # type: ignore
    except ImportError:
        raise SystemExit("PyMuPDF is required for this step:  pip install pymupdf")

    document = fitz.open(pdf_path)
    written = []
    try:
        targets = parse_pages(pages, document.page_count)
        matrix = fitz.Matrix(zoom, zoom)
        for number in targets:
            pixmap = document[number - 1].get_pixmap(matrix=matrix)
            path = os.path.join(outdir, "p%02d.png" % number)
            pixmap.save(path)
            written.append(path)
        print("[pdf] page count: %d" % document.page_count)
    finally:
        document.close()
    return written


def main(argv: list[str]) -> int:
    utf8_console()
    parser = argparse.ArgumentParser(description="Render a .docx to PDF/PNG for page inspection")
    parser.add_argument("source", help="path to the .docx file")
    parser.add_argument("--outdir", default="", help="PNG folder (default: <name>_preview)")
    parser.add_argument("--pdf", default="", help="PDF path (default: <name>_preview.pdf)")
    parser.add_argument("--dpi", type=int, default=170, help="render zoom x100 (default 170)")
    parser.add_argument("--pages", default="", help="page list such as 1,5,9,-1")
    parser.add_argument("--keep-pdf", action="store_true", help="keep the preview PDF")
    args = parser.parse_args(argv)

    if not os.path.exists(args.source):
        print("[ERR] not found: %s" % args.source)
        return 1

    stem = os.path.splitext(os.path.abspath(args.source))[0]
    outdir = args.outdir or (stem + "_preview")
    pdf_path = args.pdf or (stem + "_preview.pdf")
    os.makedirs(outdir, exist_ok=True)

    try:
        pages, paragraphs, tables = word_to_pdf(args.source, pdf_path)
    except SystemExit:
        raise
    except Exception as exc:
        print("[ERR] Word export failed: %s" % exc)
        print("      Without Word, degrade to parameter-only self-check and say so in the record.")
        return 2

    print("[word] pages %d  paragraphs %d  tables %d" % (pages, paragraphs, tables))
    if not os.path.exists(pdf_path):
        print("[ERR] PDF was not produced: %s" % pdf_path)
        return 2
    print("[pdf] %s (%d bytes)" % (pdf_path, os.path.getsize(pdf_path)))

    images = pdf_to_png(pdf_path, outdir, args.pages, args.dpi / 100.0)
    for path in images:
        print("  %s (%d bytes)" % (path, os.path.getsize(path)))

    if not args.keep_pdf:
        try:
            os.remove(pdf_path)
            print("[clean] preview PDF removed")
        except OSError as exc:
            print("[clean] preview PDF still locked (%s); delete it after the viewer exits" % exc)

    print("\n[next] inspect the representative pages, then delete %s" % outdir)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
