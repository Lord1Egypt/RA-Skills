#!/usr/bin/env python3
"""Batch PDF → clean markdown (wrapper around pdf_to_clean_md.py).

Each input PDF becomes one flat file under the output root:

    <output_root>/<title-slug>.md

The slug is derived from the paper's real title (see pdf_to_clean_md.py),
NOT the PDF filename, so renaming the input file later never breaks the
output or the figure names. Extracted figures (unless --no-figures) are
pooled into <output_root>/figures/. Figure filenames embed the same title
slug (e.g. `age-associated-resilience-...-fig_1.png`), so pooling cannot
collide, and the relative `figures/...` links inside each markdown file
resolve correctly from the output root.

Error-tolerant by design: a single bad PDF is logged and skipped; the rest of
the batch continues. Exit code is 0 only if every PDF succeeded, which makes
background runs easy to monitor.

Why this wrapper exists: pdf_to_clean_md.py always writes `fulltext.md` into
its output directory, so running it directly on a shared output root would
overwrite itself on every file. This wrapper gives each PDF its own temp
directory, then promotes the result to a uniquely named file.

Usage:
    python3 parse_many.py -o <output_root> [--no-figures] [--keep-names]
        [--skip-existing] [--figure-dpi 200] [--quiet] <pdf1> [pdf2 ...]

Options:
  --keep-names       Name each output after its PDF's filename instead of the
                     paper-title slug. Use when input filenames carry a
                     deliberate numbering scheme (e.g. numbered bibliography:
                     PDF #N <-> reference #N). Trade-off: renaming a PDF later
                     changes its output name, and duplicate filenames collide.
  --skip-existing    Skip a PDF whose output .md already exists (and is large
                     enough to be a real parse, not a near-empty stub), so
                     a re-run of a large batch only processes missing/new files.
                     This is a size check, NOT a version check — if the parser
                     was upgraded, delete or re-parse without this flag.
  --quiet            Suppress the per-file metadata block (FULLTEXT/TITLE/…/
                     figure crosscheck), leaving one status line per file plus
                     the final DONE: summary. Handy for large batches.
  --figure-dpi N     Figure render resolution (default 200).
  --keep-embedded    Also extract uncaptioned embedded images (logos/badges).

Notes:
  - A scanned/image-only PDF (no text layer) produces no real text and is
    reported as `EMPTY:` (a failure) with a hint to use the image-ocr skill —
    it is never silently reported `OK:`.
  - Two different PDFs of the SAME paper map to one file (title slug dedup) —
    a second parse simply overwrites the first. Genuinely different papers with
    identical titles are the only collision case; rename one input if needed.
  - For large batches (50+ PDFs) prefer running this as a background task and
    check the final `DONE:` line. Do NOT use `pkill`/`kill` patterns that could
    match the script's own command line when stopping such a task.
"""

import argparse
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path

try:  # PyMuPDF >= 1.24 ships the `pymupdf` module; `fitz` is a deprecated alias
    import pymupdf as fitz
except ImportError:  # older PyMuPDF builds
    import fitz  # PyMuPDF

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pdf_to_clean_md import AcademicPDFCleaner, derive_slug  # noqa: E402

# Below this many non-marker characters → treat as empty (e.g. a scanned PDF
# that yields only `<!-- page N -->` markers and no real text).
MIN_TEXT_CHARS = 50

# An existing output this small (or smaller) is NOT considered "already parsed"
# by --skip-existing: it's a version-stamp-only / near-empty file, so re-parse it.
SKIP_MIN_BYTES = 200

_MARKER_RE = re.compile(r"<!--.*?-->", flags=re.DOTALL)


def _is_empty(text: str, threshold: int = MIN_TEXT_CHARS) -> bool:
    """True if the parsed text has no real content (scanned PDF → markers only)."""
    cleaned = _MARKER_RE.sub("", text)
    return len(cleaned.strip()) < threshold


def convert_one(pdf: Path, out_root: Path, no_figures: bool, keep_embedded: bool = False,
                keep_names: bool = False, figure_dpi: int = 200, quiet: bool = False,
                skip_existing: bool = False,
                keep_references: bool = False,
                page_markers: bool = False) -> tuple[str, str]:
    """Parse one PDF into <out_root>/<slug>.md (+ pooled figures).

    Returns (status, message) where status ∈ {"ok", "skip", "empty", "fail"}.
    """
    try:
        # Resolve the output name first so --skip-existing can short-circuit.
        if keep_names:
            slug = pdf.stem
        else:
            doc = fitz.open(pdf)
            slug = derive_slug(doc, pdf.stem)
            doc.close()

        md_path = out_root / f"{slug}.md"
        if skip_existing and md_path.exists() and md_path.stat().st_size > SKIP_MIN_BYTES:
            return "skip", str(md_path)

        with tempfile.TemporaryDirectory(prefix="pdfparse-") as tmp:
            tmp_dir = Path(tmp)
            cleaner = AcademicPDFCleaner(
                str(pdf),
                str(tmp_dir),
                slug=slug,
                render_figures=not no_figures,
                keep_embedded=keep_embedded,
                keep_references=keep_references,
                page_markers=page_markers,
                figure_dpi=figure_dpi,
                quiet=quiet,
            )
            text = cleaner.process()

            if _is_empty(text):
                return "empty", f"{pdf}: no text layer (scanned? use image-ocr)"

            md_path.write_text(text, encoding="utf-8")

            figs_dir = tmp_dir / "figures"
            if figs_dir.is_dir():
                target = out_root / "figures"
                target.mkdir(parents=True, exist_ok=True)
                for fig in figs_dir.iterdir():
                    if fig.is_file():
                        shutil.copy2(fig, target / fig.name)
            return "ok", str(md_path)
    except Exception as exc:  # noqa: BLE001 - keep the batch going
        return "fail", f"{pdf}: {exc}"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Batch PDF → clean markdown, one .md per PDF under -o"
    )
    parser.add_argument("pdfs", nargs="+", help="Input PDF paths (one or more)")
    parser.add_argument("-o", "--output-dir", required=True, help="Output root directory")
    parser.add_argument("--no-figures", action="store_true", help="Skip figure extraction (faster, text-only)")
    parser.add_argument("--figure-dpi", type=int, default=200, help="Figure render DPI (default 200)")
    parser.add_argument(
        "--keep-names",
        action="store_true",
        help="Name each output after its PDF's filename instead of the paper title slug.",
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Skip a PDF whose output .md already exists (and is a real parse, not a stub).",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress per-file metadata; one status line per file.",
    )
    parser.add_argument(
        "--keep-embedded",
        action="store_true",
        help="Also extract uncaptioned embedded images (logos/badges). Off by "
        "default so figure numbers stay aligned with the paper's real Figure N.",
    )
    parser.add_argument(
        "--keep-references",
        action="store_true",
        help="Keep the reference/bibliography section instead of pruning it "
        "(for citation extraction, not for clean reading text).",
    )
    parser.add_argument(
        "--page-markers",
        action="store_true",
        help="Keep <!-- page N --> markers between pages so output can be "
        "cited by page number.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print one JSON summary (per-file status + totals) instead of the "
        "human-readable OK:/SKIP:/DONE: lines.",
    )
    args = parser.parse_args()

    out_root = Path(args.output_dir)
    out_root.mkdir(parents=True, exist_ok=True)

    ok = 0
    skipped = 0
    empty = 0
    failed: list[str] = []
    results: list[dict] = []
    for pdf_arg in args.pdfs:
        pdf = Path(pdf_arg)
        if not pdf.is_file():
            msg = f"{pdf}: not found"
            failed.append(msg)
            results.append({"status": "fail", "pdf": str(pdf), "reason": "not found"})
            print(f"FAIL: {msg}", file=sys.stderr)
            continue
        status, msg = convert_one(
            pdf, out_root, args.no_figures, args.keep_embedded,
            args.keep_names, args.figure_dpi, args.quiet or args.json,
            args.skip_existing,
            keep_references=args.keep_references,
            page_markers=args.page_markers,
        )
        results.append({
            "status": status,
            "pdf": str(pdf),
            **({"output": msg} if status in ("ok", "skip") else {"reason": msg}),
        })
        if status == "ok":
            ok += 1
            if not args.json:
                print(f"OK: {msg}")
        elif status == "skip":
            skipped += 1
            if not args.json:
                print(f"SKIP: {msg}")
        elif status == "empty":
            empty += 1
            failed.append(msg)
            print(f"EMPTY: {msg}", file=sys.stderr)
        else:
            failed.append(msg)
            print(f"FAIL: {msg}", file=sys.stderr)

    if args.json:
        print(json.dumps({
            "ok": ok,
            "skipped": skipped,
            "empty": empty,
            "failed": len(failed),
            "results": results,
        }, ensure_ascii=False, indent=2))
    else:
        print(f"DONE: {ok} ok, {skipped} skipped, {empty} empty, {len(failed)} failed")
    if failed:
        print("FAILED FILES:", *failed, sep="\n  - ", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
