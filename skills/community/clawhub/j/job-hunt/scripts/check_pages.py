#!/usr/bin/env python3
"""Gate: the rendered PDF is as long as the market says it may be — and it still
says who the candidate is and where they worked.

Nothing else in the pipeline measures the artifact that is actually submitted.
The three judges read `cv.md`; `render_cv.py` reports success on any compile that
returns 0; and `references/cv-craft.md:224-228` states a hard length table that no
program has ever checked. A three-page CV for a five-year candidate renders
perfectly, passes every existing gate, and is a common silent screen-out.

The text-coverage half was added after a measured defect of the same shape: the
renderer emitted a pdfLaTeX preamble for a XeTeX engine, every character above
Latin-1 was dropped with an exit-0 warning, and `Łukasz Wójcik` reached recruiters
as `ukasz Wójcik`. `cv.md` was intact, so all three judges saw the right name. The
renderer now fails on those warnings, but this gate is the independent check on
the delivered bytes: a CV whose PDF does not contain the candidate's own name is
the one thing worth asserting mechanically.

Exit 0 = within budget and readable. Exit 1 = findings. Exit 2 = no PDF to measure.
"""
from __future__ import annotations

import argparse
import datetime
import pathlib
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
import zlib


sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import journal

GATE = "check_pages"
_PAGE = re.compile(rb"/Type\s*/Page(?![sA-Za-z])")
_PAGES_COUNT = re.compile(rb"/Type\s*/Pages\b[^>]{0,200}?/Count\s+(\d+)", re.S)
_YEAR = re.compile(r"(?<!\d)((?:19|20)\d{2})(?!\d)")
ACADEMIC = ("academic", "research")


def _streams(data: bytes) -> list:
    """Raw bytes plus every inflated FlateDecode stream.

    Measured: tectonic writes PDF 1.5 with compressed object streams, so the page
    objects are not in the raw bytes at all — a plain `/Type /Page` scan reports
    0 pages for a perfectly good one-page CV, which would make this gate fire on
    every single run.
    """
    parts = [data]
    for m in re.finditer(rb"stream\r?\n", data):
        start = m.end()
        end = data.find(b"endstream", start)
        if end < 0:
            continue
        try:
            parts.append(zlib.decompress(data[start:end]))
        except zlib.error:
            pass
    return parts


def _haystack(data: bytes) -> bytes:
    return b"\n".join(_streams(data))


def page_count(path):
    """Number of pages, or None when the file cannot be read as a PDF."""
    hay = _haystack(pathlib.Path(path).read_bytes())
    n = len(_PAGE.findall(hay))
    if n:
        return n
    counts = [int(c) for c in _PAGES_COUNT.findall(hay)]
    return max(counts) if counts else None


# ── PDF text extraction ───────────────────────────────────────────────────────
#
# Dependency-free on purpose: requirements.txt is PyYAML + python-docx, and a gate
# that only runs where poppler or pypdf happens to be installed is a gate that
# reports "clean" by being absent. `pdftotext` is used when it is there, but only
# as a rescue after the built-in reader — see `extract_text`.
#
# What does NOT work, measured: inflating the FlateDecode streams and reading the
# bytes. tectonic writes text as glyph indices into a subset font, so the content
# stream for "Łukasz" contains no letters at all. What works is the /ToUnicode
# CMap the same PDF carries to make itself copy-pasteable: it maps those indices
# back to Unicode. This reads every CMap in the file and decodes the text runs
# with each one in turn, rather than resolving which font each run belongs to —
# that resolution needs the page resource dictionary, which lives inside a
# compressed object stream. Decoding with the wrong CMap yields noise, and noise
# does not accidentally spell a candidate's name, so the union of the decodings is
# a sound thing to search: a needle found in any of them really is in the PDF.

_BFCHAR = re.compile(rb"beginbfchar(.*?)endbfchar", re.S)
_BFRANGE = re.compile(rb"beginbfrange(.*?)endbfrange", re.S)
_HEXTOK = re.compile(rb"<([0-9A-Fa-f\s]*)>")
_RANGE3 = re.compile(rb"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>")
# A PDF string is either <hex> or (literal); both appear in real output — tectonic
# writes hex for its fontspec/Identity-H fonts and literals for 8-bit T1 fonts.
_PDFSTR = re.compile(rb"<([0-9A-Fa-f\s]+)>|\(((?:\\.|[^\\()])*)\)", re.S)
_ESCAPES = {b"n": b"\n", b"r": b"\r", b"t": b"\t", b"b": b"\b", b"f": b"\f",
            b"(": b"(", b")": b")", b"\\": b"\\"}
_MAX_RANGE = 4096          # a bfrange spanning more than this is malformed input


def _utf16(hexdigits: bytes) -> str:
    clean = re.sub(rb"\s", b"", hexdigits)
    try:
        return bytes.fromhex(clean.decode("ascii")).decode("utf-16-be", "replace")
    except ValueError:
        return ""


def _tounicode_maps(blobs) -> list:
    """Every /ToUnicode CMap in the file, as {code: text} dicts."""
    maps = []
    for blob in blobs:
        if b"beginbfchar" not in blob and b"beginbfrange" not in blob:
            continue
        table: dict = {}
        for chunk in _BFCHAR.findall(blob):
            toks = _HEXTOK.findall(chunk)
            for i in range(0, len(toks) - 1, 2):
                src = re.sub(rb"\s", b"", toks[i])
                if src:
                    table[int(src, 16)] = _utf16(toks[i + 1])
        for chunk in _BFRANGE.findall(blob):
            for m in _RANGE3.finditer(chunk):
                lo, hi = int(m.group(1), 16), int(m.group(2), 16)
                base = _utf16(m.group(3))
                if not base or hi < lo or hi - lo > _MAX_RANGE:
                    continue
                for code in range(lo, hi + 1):
                    try:
                        table[code] = base[:-1] + chr(ord(base[-1]) + (code - lo))
                    except ValueError:
                        break      # ran past U+10FFFF; the rest of the range is junk
        if table:
            maps.append(table)
    return maps


def _unescape(raw: bytes) -> bytes:
    out, i = bytearray(), 0
    while i < len(raw):
        ch = raw[i:i + 1]
        if ch == b"\\" and i + 1 < len(raw):
            nxt = raw[i + 1:i + 2]
            if nxt in _ESCAPES:
                out += _ESCAPES[nxt]
                i += 2
                continue
            octal = re.match(rb"[0-7]{1,3}", raw[i + 1:i + 4])
            if octal:
                out.append(int(octal.group(0), 8) & 0xFF)
                i += 1 + len(octal.group(0))
                continue
            i += 2
            continue
        out += ch
        i += 1
    return bytes(out)


def _text_runs(blobs) -> list:
    """Every string literal from every content stream, in order."""
    runs = []
    for blob in blobs:
        if b"Tj" not in blob and b"TJ" not in blob:
            continue
        for m in _PDFSTR.finditer(blob):
            if m.group(1) is not None:
                hexdigits = re.sub(rb"\s", b"", m.group(1))
                if len(hexdigits) % 2:
                    hexdigits += b"0"
                runs.append(bytes.fromhex(hexdigits.decode("ascii")))
            else:
                runs.append(_unescape(m.group(2)))
    return runs


def _decode(run: bytes, table: dict, two_byte: bool) -> str:
    if two_byte:
        return "".join(table.get((run[i] << 8) | run[i + 1], "")
                       for i in range(0, len(run) - 1, 2))
    return "".join(table.get(b, "") for b in run)


def _pdftotext(path) -> str:
    """poppler's extractor, if this machine has it. Not a dependency, a rescue."""
    exe = shutil.which("pdftotext")
    if not exe:
        return ""
    try:
        proc = subprocess.run([exe, "-q", str(path), "-"], capture_output=True,
                              text=True, encoding="utf-8", errors="replace", timeout=60)
    except (OSError, subprocess.SubprocessError):
        return ""
    return proc.stdout if proc.returncode == 0 else ""


def extract_text(path) -> list:
    """Candidate readings of the PDF's text. Empty list = could not read it.

    Empty is NOT "the PDF has no text": the two are indistinguishable from here,
    which is exactly why the caller turns it into an UNVERIFIED finding instead of
    a pass. A gate that cannot run must not look like a gate that passed.
    """
    try:
        blobs = _streams(pathlib.Path(path).read_bytes())
    except OSError:
        return []
    runs = _text_runs(blobs)
    readings = []
    for table in _tounicode_maps(blobs):
        for two_byte in (True, False):
            text = "".join(_decode(run, table, two_byte) for run in runs)
            if text.strip():
                readings.append(text)
    # The pdftotext rescue runs ALWAYS, not only when the built-in reader came
    # back empty. `if not readings` was the wrong condition: a CJK font embedded
    # as Identity-H carries no ToUnicode CMap, but the Latin Modern subset in the
    # same document does — so a Korean CV produced four garbage readings from the
    # Latin CMaps, the rescue never ran, and text that pdftotext reads perfectly
    # was reported TEXT_MISSING_FROM_PDF. Measured on macOS with AppleSDGothicNeo:
    # correct PDF, correct page, blocked by its own gate. Every Korean CV.
    #
    # This can only ever REMOVE a false finding: a reading is evidence the text is
    # in the PDF, and pdftotext reads what the PDF actually says.
    rescue = _pdftotext(path)
    if rescue.strip():
        readings.append(rescue)
    return readings


# Everything the typesetter is entitled to change between the YAML and the page.
# Whitespace, because word spacing in a PDF is usually a positioning move with no
# space glyph behind it. Hyphens and dashes, because LaTeX hyphenates across line
# breaks and render_cv rewrites "—" as "---". Quotes, because render_cv rewrites
# the curly ones as ASCII (`_LATEX_REPLACEMENTS`), so "Moody's" typed with U+2019
# is set with U+0027. NFKC on top, because "fi" is set as one ligature glyph and
# "…" as three periods.
#
# The soft hyphen is written as the regex escape rather than the literal
# character: an invisible codepoint inside a character class is unreviewable,
# and scripts/check_hidden_chars.py refuses it tree-wide.
#
# Deleting these cannot turn a missing name into a found one: the needles are
# whole names and employers, and "Zoë Nowak" does not fall out of noise because
# the apostrophes were dropped from both sides.
_IGNORED_IN_MATCH = re.compile(r"[\s\xad\-‐-―'\"‘’“”`´]+")


def _squash(text: str) -> str:
    return _IGNORED_IN_MATCH.sub("", unicodedata.normalize("NFKC", text))


def pdf_contains(readings, needle: str) -> bool:
    return any(_squash(needle) in _squash(text) for text in readings)


def text_findings(cv_pdf, profile) -> list:
    """The candidate's name and every employer must survive into the PDF."""
    name = str((profile.get("meta") or {}).get("name") or "").strip()
    orgs = [str((ex or {}).get("org") or "").strip()
            for ex in (profile.get("experience") or []) if isinstance(ex, dict)]
    wanted = [("meta.name", name)] + [("experience[].org", o) for o in orgs if o]
    wanted = [(where, what) for where, what in wanted if what]
    if not wanted:
        return []

    label = pathlib.Path(cv_pdf).name
    readings = extract_text(cv_pdf)
    if not readings:
        return [f"UNVERIFIED_PDF_TEXT: no text could be extracted from {label}, so "
                f"nothing here checked that the candidate's name and employers "
                f"actually appear in the file that gets sent. This is NOT a pass. "
                f"Open the PDF, confirm by eye, or install poppler "
                f"(`pdftotext`) and re-run"]
    out = []
    for where, what in wanted:
        if not pdf_contains(readings, what):
            out.append(
                f"TEXT_MISSING_FROM_PDF: {label} does not contain {where} "
                f"{what!r} — the compile reported success but the glyphs did not "
                f"survive into the delivered file (cv.md and cv.docx can look "
                f"perfect while this is true). Re-render; if it repeats, the font "
                f"does not cover these characters — set meta.main_font")
    return out


def unreadable_start_dates(profile) -> list:
    """Start dates that carry a date but no Gregorian year this module can read.

    `_YEAR` matches 19xx/20xx only, so `平成31年4月` and `令和元年4月` yielded
    nothing — and `years_of_experience` turned "cannot read" into 0, which is the
    strictest possible answer: a one-page budget, and a false CV_TOO_LONG for a
    seven-year candidate. Measured 2026-09-05.

    Deliberately NOT an era-conversion table. Japanese eras, the Republic of
    China calendar, the Thai Buddhist era and Hijri dates are all real inputs,
    and a hard-coded table would be a list of factual claims that goes stale and
    covers only the calendars someone thought of. Reporting what could not be
    read, and refusing to score it as zero, generalises to all of them.
    """
    out = []
    for ex in profile.get("experience") or []:
        if not isinstance(ex, dict):
            continue
        raw = str(ex.get("start") or "").strip()
        if raw and not _YEAR.search(raw):
            out.append(raw)
    return out


def years_of_experience(profile, today_year: int):
    """Years since the earliest readable start date, or None if none is readable.

    None means "nobody could work this out", not "zero". They were the same value
    before, and the caller had no way to tell them apart.
    """
    years, dated = [], 0
    for ex in profile.get("experience") or []:
        if not isinstance(ex, dict):
            continue
        raw = str(ex.get("start") or "").strip()
        if raw:
            dated += 1
        m = _YEAR.search(raw)
        if m:
            years.append(int(m.group(1)))
    if years:
        return max(0, today_year - min(years))
    # No entry carries a start date at all — a genuine new graduate. That is
    # zero years, not an unreadable one, and it keeps the strict one-page budget
    # the length table gives them. Only a date that IS there and cannot be read
    # is unknown.
    return None if dated else 0


def _max_pages_override(profile):
    """`meta.max_pages` when it is a usable page count, else None."""
    override = (profile.get("meta") or {}).get("max_pages")
    if isinstance(override, int) and not isinstance(override, bool) and override > 0:
        return override
    return None


def budget_uses_experience(profile) -> bool:
    """Whether years of experience decide the page budget at all.

    They do not for an academic CV (no limit) or under an explicit
    `meta.max_pages`, so an unreadable start date changes nothing there.
    START_DATE_UNREAD told the user "or set meta.max_pages" and then kept
    firing after they did — a finding whose own remedy could not clear it.
    """
    meta = profile.get("meta") or {}
    if str(meta.get("cv_type") or "").strip().lower() in ACADEMIC:
        return False
    return _max_pages_override(profile) is None


def max_pages(profile, today_year: int):
    """The page budget, or None when there is none.

    cv-craft.md:224-228 — 0-2 years: 1 page; 3-7: 1-2; 8-15: 2; 15+: 2, "3 only if
    roles are very distinct and all relevant"; academic/research CVs: no limit.
    The 15+/3-page case is an explicit judgement call, so it is an explicit opt-in
    (`meta.max_pages: 3`) rather than a band the gate guesses at.
    """
    meta = profile.get("meta") or {}
    if str(meta.get("cv_type") or "").strip().lower() in ACADEMIC:
        return None
    override = _max_pages_override(profile)
    if override is not None:
        return override
    years = years_of_experience(profile, today_year)
    if years is None:
        # No readable start date. The permissive budget, because the strict one
        # was being applied to a candidate whose experience this module simply
        # could not parse — a guaranteed false CV_TOO_LONG on every non-Gregorian
        # CV. `unreadable_start_dates` says so out loud alongside it.
        return 2
    # cv-craft.md:130 gives US/Canada their own résumé length — 1 page, a
    # second only at 10+ years — and it is stricter than the generic ladder
    # below. The gate took no market at all, so a 5-year US resume rendered to
    # two pages and passed, against the convention table the same skill wrote.
    # `meta.max_pages` above remains the escape hatch for the senior exception.
    from render_cv import north_america
    if north_america((profile.get("meta") or {}).get("target_market")):
        return 1 if years < 10 else 2
    return 1 if years < 3 else 2


def findings_for(cv_pdf, profile, today_year: int, letter_pdf=None) -> list:
    from pdf_glyphs import glyph_findings
    out = glyph_findings(cv_pdf)
    # Reported before anything is read off the PDF, because it is a fact about
    # the PROFILE: the page budget below was chosen without these dates, and a
    # reader who cannot see that will not know why a one-page CV got two. It
    # does not belong behind "is the PDF readable" — the two are unrelated.
    unread = unreadable_start_dates(profile) if budget_uses_experience(profile) else []
    if unread:
        out.append(f"START_DATE_UNREAD: {', '.join(repr(d) for d in unread)} "
                   f"carries no 19xx/20xx year, so years of experience could not "
                   f"be computed and the permissive page budget was used. Write "
                   f"the Gregorian year, or set meta.max_pages")
    pages = page_count(cv_pdf)
    if pages is None:
        out.append(f"UNREADABLE_PDF: {pathlib.Path(cv_pdf).name} has no readable page "
                   f"tree — the compile reported success but produced a file no "
                   f"reader can open; re-render before sending it")
    else:
        budget = max_pages(profile, today_year)
        if budget is not None and pages > budget and not budget_uses_experience(profile):
            out.append(f"CV_TOO_LONG: {pathlib.Path(cv_pdf).name} is {pages} pages; "
                       f"meta.max_pages allows {budget}. Cut, or raise meta.max_pages "
                       f"with a reason")
        elif budget is not None and pages > budget:
            years = years_of_experience(profile, today_year)
            basis = (f"{years} years of experience" if years is not None
                     else "an unread start date, so the permissive budget")
            out.append(f"CV_TOO_LONG: {pathlib.Path(cv_pdf).name} is {pages} pages; "
                       f"the length table in references/cv-craft.md allows {budget} "
                       f"for {basis}. Cut, or set meta.max_pages with a reason")
        # Only worth asking once the file is readable at all: an unreadable PDF
        # has already been reported and would produce a second, derivative finding.
        out += text_findings(cv_pdf, profile)
    if letter_pdf and pathlib.Path(letter_pdf).exists():
        out += glyph_findings(letter_pdf)
        lp = page_count(letter_pdf)
        if lp is None:
            out.append(f"UNREADABLE_PDF: {pathlib.Path(letter_pdf).name} has no "
                       f"readable page tree")
        elif lp > 1:
            out.append(f"LETTER_TOO_LONG: {pathlib.Path(letter_pdf).name} is {lp} "
                       f"pages; motivation-letter.md says one page, always")
    return out


def _macos_libreoffice_app():
    """The app bundle to launch on macOS, if this host has one.

    Recent LibreOffice builds can abort when their executable is started directly
    with ``--headless`` on macOS. LaunchServices starts the same app
    with the same private profile without that AppKit initialization crash.
    Keep the direct command as a fallback: a custom or older installation may
    not have an app bundle but can still export successfully.

    `open -a` activates the app it launches, and `--headless` does not stop that:
    LibreOffice would take the user's keyboard focus every time a Word file is
    measured. `-g` keeps it in the background and `-j` launches it hidden.
    """
    if platform.system() != "Darwin":
        return None
    for app in (pathlib.Path("/Applications/LibreOffice.app"),
                pathlib.Path.home() / "Applications" / "LibreOffice.app"):
        if app.is_dir():
            return app
    return None


def _office_export_commands(office, profile, folder, docx):
    """Ordered export commands, preferring the stable macOS app entry point."""
    args = ["-env:UserInstallation=" + pathlib.Path(profile).as_uri(),
            "--headless", "--convert-to", "pdf", "--outdir", str(folder),
            str(pathlib.Path(docx).resolve())]
    direct = [str(office), *args]
    app = _macos_libreoffice_app()
    if app and shutil.which("open"):
        return [["open", "-g", "-j", "-W", "-n", "-a", str(app), "--args", *args], direct]
    return [direct]


def docx_findings(cv_docx, profile, today_year, letter_docx=None):
    """Measure an independent Office render, never infer DOCX pages from LaTeX.

    A private LibreOffice profile prevents a running GUI instance from swallowing
    the conversion request. Temporary PDFs and settings are deleted on exit.
    """
    documents = [(pathlib.Path(p), letter) for p, letter in
                 [(cv_docx, False), (letter_docx, True)] if p and pathlib.Path(p).exists()]
    if not documents:
        return []
    office = shutil.which("soffice") or shutil.which("libreoffice")
    if not office:
        return ["DOCX_NOT_MEASURED: install LibreOffice to check the delivered Word "
                "files; the LaTeX PDF page count does not validate DOCX"]
    out = []
    with tempfile.TemporaryDirectory(prefix="jobhunt-office-") as temp:
        root = pathlib.Path(temp)
        for index, (docx, is_letter) in enumerate(documents):
            folder = root / str(index)
            folder.mkdir()
            pdf = folder / (docx.stem + ".pdf")
            export_error = None
            try:
                converted = False
                for command in _office_export_commands(office, root / "profile", folder, docx):
                    # A failed converter may leave a partial PDF. Remove it before
                    # the next fallback so a later zero exit cannot validate stale
                    # bytes from the failed attempt.
                    try:
                        pdf.unlink()
                    except FileNotFoundError:
                        pass
                    try:
                        result = subprocess.run(command, capture_output=True, text=True,
                                                encoding="utf-8", timeout=60, check=False)
                    except (OSError, UnicodeError, subprocess.SubprocessError) as exc:
                        export_error = exc
                        continue
                    if result.returncode == 0 and pdf.is_file():
                        converted = True
                        break
                if not converted:
                    if export_error:
                        out.append(f"DOCX_NOT_MEASURED: {docx.name}: {export_error}")
                    else:
                        out.append(f"DOCX_NOT_MEASURED: {docx.name} could not be exported by LibreOffice")
                    continue
                if is_letter:
                    from pdf_glyphs import glyph_findings
                    out.extend(glyph_findings(pdf))
                    pages = page_count(pdf)
                    problems = (["UNREADABLE_PDF: no readable page tree"] if pages is None
                                else [f"LETTER_TOO_LONG: {pages} pages; maximum is 1"]
                                if pages > 1 else [])
                else:
                    problems = findings_for(pdf, profile, today_year)
                out.extend(f"{problem.split(':', 1)[0]}: Word file {docx.name}: "
                           f"{problem.split(':', 1)[-1].strip()}" for problem in problems)
            except (OSError, UnicodeError, subprocess.SubprocessError) as exc:
                out.append(f"DOCX_NOT_MEASURED: {docx.name}: {exc}")
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", required=True)
    ap.add_argument("--cv", default=None, help="default: <workspace>/cv.pdf")
    ap.add_argument("--letter", default=None, help="default: <workspace>/letter.pdf")
    ap.add_argument("--cv-docx", default=None, help="default: <workspace>/cv.docx, if present")
    ap.add_argument("--letter-docx", default=None, help="default: <workspace>/letter.docx, if present")
    ap.add_argument("--profile", default=None,
                    help="default: <workspace>/tailored-profile.yaml")
    ap.add_argument("--today", default=None, help="YYYY-MM-DD; default: today")
    args = ap.parse_args(argv)

    ws = pathlib.Path(args.workspace)
    if not ws.is_dir():
        # journal.receipt() would mkdir it, and a gate that creates the
        # workspace it is auditing has manufactured its own evidence.
        print(f"cannot run {GATE}: workspace {ws} does not exist", file=sys.stderr)
        return 2
    cv = pathlib.Path(args.cv) if args.cv else ws / "cv.pdf"
    letter = pathlib.Path(args.letter) if args.letter else ws / "letter.pdf"
    prof = pathlib.Path(args.profile) if args.profile else ws / "tailored-profile.yaml"
    for p in (cv, prof):
        if not p.exists():
            journal.receipt(ws, GATE, {}, "could_not_run", [f"MISSING_INPUT: {p}"])
            print(f"cannot run {GATE}: {p} does not exist", file=sys.stderr)
            return 2

    today_year = int((args.today or
                      datetime.date.today().isoformat())[:4])
    try:
        profile = journal.load_yaml(prof)
    except journal.YamlUnreadable as exc:
        journal.receipt(ws, GATE, {}, "could_not_run", [exc.finding])
        print(f"cannot run {GATE}: {exc}", file=sys.stderr)
        return 2
    findings = findings_for(cv, profile, today_year, letter)
    cv_docx = pathlib.Path(args.cv_docx) if args.cv_docx else ws / "cv.docx"
    letter_docx = pathlib.Path(args.letter_docx) if args.letter_docx else ws / "letter.docx"
    for requested in (args.cv_docx, args.letter_docx):
        if requested and not pathlib.Path(requested).is_file():
            findings.append(f"DOCX_NOT_MEASURED: explicitly requested file {requested} is missing")
    findings += docx_findings(cv_docx, profile, today_year, letter_docx)
    for f in findings:
        print(f)
    inputs = {p.name: journal.sha256_file(p) for p in
              (cv, letter, cv_docx, letter_docx, prof) if p.is_file()}
    journal.receipt(ws, GATE, inputs,
                    "fail" if findings else "pass", findings)
    return 1 if findings else 0


if __name__ == "__main__":
    from cli_io import configure_output

    configure_output()
    sys.exit(main())
