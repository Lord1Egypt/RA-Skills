#!/usr/bin/env python3
"""Self-test for the pdfparse skill (parse_many.py + pdf_to_clean_md.py).

Builds synthetic PDFs with PyMuPDF and exercises the batch wrapper end-to-end:
version stamp, --keep-names, empty/scanned detection, --skip-existing, --quiet,
and missing-file failure. Prints PASS/FAIL per check and exits non-zero on any
failure, so it can gate a release or run as a quick smoke test.

Usage:
    scripts/run.sh scripts/self_test.py
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

try:  # PyMuPDF >= 1.24 ships the `pymupdf` module; `fitz` is a deprecated alias
    import pymupdf as fitz
except ImportError:  # older PyMuPDF builds
    import fitz  # PyMuPDF

HERE = Path(__file__).resolve().parent
PARSE_MANY = HERE / "parse_many.py"

PASS = 0
FAIL = 0


def check(name: str, cond: bool, detail: str = "") -> None:
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"PASS: {name}")
    else:
        FAIL += 1
        print(f"FAIL: {name} {detail}")


def make_pdf(path: Path, body_lines: list[str], title: str | None = None) -> None:
    """Write a minimal single-column PDF with optional larger-font title."""
    doc = fitz.open()
    page = doc.new_page(width=595, height=842)
    y = 100
    if title:
        page.insert_text((72, y), title, fontsize=20)
        y += 40
    for line in body_lines:
        page.insert_text((72, y), line, fontsize=11)
        y += 20
    doc.save(str(path))
    doc.close()


def make_blank_pdf(path: Path) -> None:
    """A PDF with a page but no text (simulates a scan without OCR)."""
    doc = fitz.open()
    doc.new_page(width=595, height=842)
    doc.save(str(path))
    doc.close()


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(PARSE_MANY), *args],
        capture_output=True, text=True,
    )


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="pdfparse-selftest-"))

    # 1. Parse a normal PDF → version stamp + body text survive.
    p1 = tmp / "paper1.pdf"
    make_pdf(p1, ["This is the abstract body.", "More sentences follow here."], title="Title of Paper One")
    out1 = tmp / "out1"
    r1 = run("-o", str(out1), "--no-figures", "--quiet", str(p1))
    mds1 = list(out1.glob("*.md"))
    body_ok = len(mds1) == 1 and "pdfparse v" in mds1[0].read_text() and "abstract body" in mds1[0].read_text()
    check("parse + version stamp + body text", body_ok, f"r={r1.returncode} files={len(mds1)}")

    # 2. --keep-names → output named after the PDF filename.
    p2 = tmp / "02_Test_Paper.pdf"
    make_pdf(p2, [
        "Second paper body text with enough length to clear the minimum content threshold reliably.",
        "This is an additional sentence to make the parsed output comfortably exceed the skip size.",
        "Yet another line of body text so the generated markdown file is a few hundred bytes long.",
    ])
    out2 = tmp / "out2"
    run("-o", str(out2), "--no-figures", "--quiet", "--keep-names", str(p2))
    check("--keep-names preserves filename", (out2 / "02_Test_Paper.md").exists())

    # 3. Scanned/empty PDF → EMPTY failure, non-zero exit, not silently OK.
    p3 = tmp / "scanned.pdf"
    make_blank_pdf(p3)
    out3 = tmp / "out3"
    r3 = run("-o", str(out3), "--no-figures", "--quiet", str(p3))
    check("empty/scanned detected as failure", r3.returncode != 0 and "EMPTY" in r3.stderr,
          f"r={r3.returncode} stderr={r3.stderr!r}")

    # 4. --skip-existing → already-parsed file is skipped.
    out4 = tmp / "out4"
    run("-o", str(out4), "--no-figures", "--quiet", "--keep-names", str(p2))
    r4 = run("-o", str(out4), "--no-figures", "--quiet", "--keep-names", "--skip-existing", str(p2))
    check("--skip-existing skips existing output", r4.returncode == 0 and "SKIP" in r4.stdout,
          f"r={r4.returncode} out={r4.stdout!r}")

    # 5. Missing file → FAIL + non-zero exit.
    r5 = run("-o", str(tmp / "out5"), "--no-figures", "--quiet", str(tmp / "nope.pdf"))
    check("missing file → FAIL + exit != 0", r5.returncode != 0 and "not found" in r5.stderr,
          f"r={r5.returncode}")

    # 6. --keep-references → bibliography survives; default run prunes it.
    p6 = tmp / "with_refs.pdf"
    doc = fitz.open()
    page = doc.new_page(width=595, height=842)
    page.insert_text((72, 90), "A Study of Renal Ischemia", fontsize=18)
    y = 140
    for line in (
        "The body of the article discusses ischemia and reperfusion injury.",
        "This sentence is long enough to behave like real prose text.",
    ):
        page.insert_text((72, y), line, fontsize=11)
        y += 20
    y += 120
    page.insert_text((72, y), "References", fontsize=12)
    y += 40
    for ref in (
        "1. Smith J, Doe A. Renal ischemia in rats. Lab Anim. 2020;12:1-10.",
        "2. Jones B. Exercise physiology review. J Physiol. 2021;9:55-70.",
        "3. Brown C. Oxidative stress markers. Free Radic Biol Med. 2019;3:12-20.",
    ):
        page.insert_text((72, y), ref, fontsize=10)
        y += 20
    doc.save(str(p6))
    doc.close()

    out6a = tmp / "out6a"
    run("-o", str(out6a), "--no-figures", "--quiet", "--keep-names", str(p6))
    md6a = out6a / "with_refs.md"
    default_pruned = md6a.exists() and "References" not in md6a.read_text()
    check("default run prunes the reference section", default_pruned,
          f"exists={md6a.exists()}")

    out6b = tmp / "out6b"
    run("-o", str(out6b), "--no-figures", "--quiet", "--keep-names",
        "--keep-references", str(p6))
    md6b = out6b / "with_refs.md"
    kept = md6b.exists() and "References" in md6b.read_text() \
        and "Smith J" in md6b.read_text() and "Oxidative stress markers" in md6b.read_text()
    check("--keep-references keeps the bibliography", kept,
          f"exists={md6b.exists()}")

    # 7. --page-markers → page boundaries survive; off by default.
    p7 = tmp / "two_pages.pdf"
    doc = fitz.open()
    pg1 = doc.new_page(width=595, height=842)
    pg1.insert_text((72, 100), "First page body text ends with a full stop.", fontsize=11)
    pg2 = doc.new_page(width=595, height=842)
    pg2.insert_text((72, 100), "Second page body text continues the document.", fontsize=11)
    doc.save(str(p7))
    doc.close()

    out7a = tmp / "out7a"
    run("-o", str(out7a), "--no-figures", "--quiet", "--keep-names", str(p7))
    md7a = out7a / "two_pages.md"
    txt7a = md7a.read_text() if md7a.exists() else ""
    check("page markers off by default", md7a.exists() and "<!-- page" not in txt7a,
          f"exists={md7a.exists()}")

    out7b = tmp / "out7b"
    run("-o", str(out7b), "--no-figures", "--quiet", "--keep-names",
        "--page-markers", str(p7))
    md7b = out7b / "two_pages.md"
    txt7b = md7b.read_text() if md7b.exists() else ""
    ordered = ("<!-- page 1 -->" in txt7b and "<!-- page 2 -->" in txt7b
               and txt7b.index("<!-- page 1 -->") < txt7b.index("<!-- page 2 -->"))
    check("--page-markers keeps page boundaries in order", ordered,
          f"exists={md7b.exists()}")

    # 8. --json (single file) → valid JSON with the documented keys.
    out8 = tmp / "out8"
    r8 = subprocess.run(
        [sys.executable, str(HERE / "pdf_to_clean_md.py"), str(p1), str(out8),
         "--no-figures", "--json"],
        capture_output=True, text=True,
    )
    try:
        payload8 = json.loads(r8.stdout)
    except json.JSONDecodeError:
        payload8 = {}
    check("--json single-file summary parses",
          r8.returncode == 0
          and payload8.get("status") == "ok"
          and payload8.get("pages") == 1
          and str(payload8.get("output_path", "")).endswith("fulltext.md"),
          f"r={r8.returncode} stdout={r8.stdout[:120]!r}")

    # 9. --json (batch) → totals + per-file results.
    out9 = tmp / "out9"
    r9 = run("-o", str(out9), "--no-figures", "--json", str(p1), str(p2))
    try:
        batch9 = json.loads(r9.stdout)
    except json.JSONDecodeError:
        batch9 = {}
    check("--json batch summary parses",
          r9.returncode == 0
          and batch9.get("ok") == 2
          and len(batch9.get("results", [])) == 2,
          f"r={r9.returncode} stdout={r9.stdout[:120]!r}")

    print(f"\n{FAIL} failed, {PASS} passed")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
