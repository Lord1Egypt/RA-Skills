#!/usr/bin/env python3
"""Render a report and record the exact source/PDF pair, before visual review.

For a custom layout, call render_with(md, pdf, renderer). The callback receives
the source and a fresh PDF destination and returns (ok, reason). A no-op callback
cannot bless an old PDF. This record detects stale files, not malicious forgery.
"""
from __future__ import annotations

import argparse
import datetime
import json
import pathlib
import tempfile

import journal


def render_with(md, pdf, renderer):
    md, pdf = pathlib.Path(md), pathlib.Path(pdf)
    # Audit evidence stays beside the source, even when a legacy delivery call
    # renders directly into a client folder with a localized PDF filename.
    receipt = md.with_name(md.stem + "-render.json")
    try:
        receipt.unlink(missing_ok=True)
        source_hash = journal.sha256_file(md)
        with tempfile.TemporaryDirectory(prefix=".report-render-", dir=pdf.parent) as temporary:
            fresh = pathlib.Path(temporary) / pdf.name
            ok, reason = renderer(md, fresh)
            if not ok:
                return False, reason
            if not fresh.is_file() or not fresh.stat().st_size:
                return False, "REPORT_NOT_RENDERED: renderer produced no new PDF"
            if journal.sha256_file(md) != source_hash:
                return False, "REPORT_SOURCE_CHANGED: source changed during rendering; render again"
            import pymupdf
            with pymupdf.open(fresh) as document:
                if not document.page_count:
                    return False, "REPORT_NOT_RENDERED: PDF has no pages"
            data = {"source_sha256": source_hash, "pdf_sha256": journal.sha256_file(fresh),
                    "rendered_at": datetime.datetime.now().astimezone().isoformat()}
            fresh.replace(pdf)
            receipt.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return True, ""
    except (OSError, RuntimeError, ValueError) as exc:
        return False, f"REPORT_RENDER_FAILED: {exc}"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--font", help="Explicit report font; requires pandoc/TeX")
    args = parser.parse_args(argv)
    ws = pathlib.Path(args.workspace)
    if not (ws / "report.md").is_file():
        print("NO_REPORT_SOURCE: write report.md before rendering")
        return 2
    from deliver import render_pdf
    ok, reason = render_pdf(ws / "report.md", ws / "report.pdf", args.font)
    if not ok:
        print(reason)
        return 2
    print("REPORT_RENDERED: inspect every PDF page, then run check_layout.py --report")
    return 0


if __name__ == "__main__":
    from cli_io import configure_output

    configure_output()
    raise SystemExit(main())
