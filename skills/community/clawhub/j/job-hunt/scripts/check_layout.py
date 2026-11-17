#!/usr/bin/env python3
"""Require a current, page-by-page visual layout review for rendered CVs.

This validates the review record and its artifact hashes. It does not pretend
that a text parser has visually compared a template with the final document.
Exit 2 means there is no rendered CV to review; exit 1 means review findings.
"""
from __future__ import annotations

import argparse
import datetime
import json
import pathlib
import sys

import journal
import layout_requirements
from docx_content import docx_findings

GATE = "check_layout"
CHECKS = ("fonts", "font_sizes", "page_geometry", "headings_and_rules",
          "dates_and_alignment", "paragraph_spacing", "content_order",
          "pagination_and_clipping")


def inspect(ws: pathlib.Path, report=False):
    findings, hashes = [], {}
    reuse_cache = {}
    if not report and (ws / "cv.docx").is_file():
        findings.extend(docx_findings(ws / "cv.docx"))
    prefix = "report-" if report else ""
    path = ws / f"{prefix}layout-review.yaml"
    if not path.is_file():
        return findings + [f"NO_LAYOUT_REVIEW: render and inspect every page against the supplied template, then write {path.name}"], hashes
    hashes[path.name] = journal.sha256_file(path)
    try:
        review = journal.load_yaml(path, dict)
    except journal.YamlUnreadable as exc:
        return [f"BAD_LAYOUT_REVIEW: {exc.reason}"], hashes

    def bind(raw, expected, label, local=True):
        if not isinstance(raw, str) or not raw.strip():
            findings.append(f"BAD_LAYOUT_REVIEW: {label} has no path")
            return None
        target = pathlib.Path(raw)
        target = target.resolve() if target.is_absolute() else (ws / target).resolve()
        if local and not target.is_relative_to(ws.resolve()):
            findings.append(f"BAD_LAYOUT_REVIEW: {label} must be inside the workspace")
            return None
        if not target.is_file():
            findings.append(f"MISSING_LAYOUT_INPUT: {label}: {raw}")
            return None
        key = str(target.relative_to(ws.resolve())) if target.is_relative_to(ws.resolve()) else str(target)
        now = journal.sha256_file(target)
        hashes[key] = now
        if expected != now:
            findings.append(f"STALE_LAYOUT_REVIEW: {label} changed or was never fingerprinted; inspect the final version again")
        return target

    if not isinstance(review.get("reviewer"), str) or not review["reviewer"].strip():
        findings.append("BAD_LAYOUT_REVIEW: name the reviewer")
    try:
        # Python 3.10 fromisoformat does not accept a trailing "Z" (3.11+ does),
        # and the documented runtime floor is 3.10.
        raw = str(review.get("reviewed_at", ""))
        stamp = datetime.datetime.fromisoformat(raw[:-1] + "+00:00" if raw.endswith("Z") else raw)
        if stamp.tzinfo is None:
            raise ValueError("missing timezone")
    except (TypeError, ValueError):
        findings.append("BAD_LAYOUT_REVIEW: reviewed_at must be an ISO timestamp with timezone")
    if "reference" not in review:
        findings.append("BAD_LAYOUT_REVIEW: name the supplied template, or set reference: null when none was supplied")
    elif review["reference"] is not None:
        ref = journal.as_mapping(review["reference"])
        bind(ref.get("path"), ref.get("sha256"), "reference template", local=False)
    requirement_path = bind(f"{prefix}layout-requirements.yaml", review.get("requirements_sha256"), "format requirements")
    if requirement_path:
        try:
            requirements = journal.load_yaml(requirement_path, dict)
            if "reference" not in requirements or requirements["reference"] != review.get("reference"):
                findings.append("FORMAT_REFERENCE_CHANGED: requirements and review must name the same reference")
            expectations = journal.as_mapping(requirements.get("expectations"))
            for name in CHECKS:
                if not isinstance(expectations.get(name), str) or not expectations[name].strip():
                    findings.append(f"FORMAT_REQUIREMENT_MISSING: {name} needs concrete reference-derived expectations")
            findings.extend(layout_requirements.measure(ws, requirements, report=report))
        except journal.YamlUnreadable as exc:
            findings.append(f"BAD_LAYOUT_REQUIREMENTS: {exc.reason}")
    overrides = review.get("user_overrides")
    if not isinstance(overrides, list) or any(not isinstance(v, str) or not v.strip() for v in overrides):
        findings.append("BAD_LAYOUT_REVIEW: user_overrides must list the user's changes to the reference, or be []")
    checks = journal.as_mapping(review.get("checks"))
    for name in CHECKS:
        check = journal.as_mapping(checks.get(name))
        if check.get("status") != "pass" or not isinstance(check.get("detail"), str) or not check["detail"].strip():
            findings.append(f"LAYOUT_NOT_PASSED: {name} needs a passed comparison and a concrete observation")
    if review.get("unresolved_differences") != []:
        findings.append("LAYOUT_DIFFERENCES: resolve all unapproved layout differences before delivery")

    artifacts = journal.as_mapping(review.get("artifacts"))
    word_export_pdf = None  # the PDF the DOCX's pages are counted on, once bound
    if report:
        bind("report.md", review.get("source_sha256"), "report source")
        rendering = ws / "report-render.json"
        if not rendering.is_file():
            findings.append("NO_REPORT_RENDER: render the current source with render_report.py before review")
        else:
            hashes[rendering.name] = journal.sha256_file(rendering)
            try:
                pair = json.loads(rendering.read_text(encoding="utf-8"))
                if not isinstance(pair, dict) or any(
                        not (ws / name).is_file() or pair.get(key) != journal.sha256_file(ws / name)
                        for name, key in (("report.md", "source_sha256"), ("report.pdf", "pdf_sha256"))):
                    findings.append("STALE_REPORT_RENDER: report.md/report.pdf changed since rendering; render and review again")
            except (OSError, UnicodeError, ValueError):
                findings.append("BAD_REPORT_RENDER: unreadable render record; render and review again")
        if (ws / "report.md").is_file() and (ws / "report.pdf").is_file():
            try:
                import pymupdf
                with pymupdf.open(ws / "report.pdf") as doc:
                    pages = [page.get_text() for page in doc]
                missing = layout_requirements.report_text_problems(
                    (ws / "report.md").read_text(encoding="utf-8"), pages)
            except Exception as exc:  # an unreadable PDF cannot vouch for its source
                missing = [f"<unreadable report.pdf: {exc}>"]
            if missing:
                more = f" and {len(missing) - 3} more" if len(missing) > 3 else ""
                findings.append("REPORT_PDF_TEXT_MISMATCH: report.pdf does not carry the current "
                                "report.md text, in order: " + ", ".join(repr(m[:50]) for m in missing[:3]) + more
                                + "; re-render report.pdf from the current report.md and review it again")
    elif (ws / "cv.docx").is_file() and (ws / "cv.pdf").is_file():
        export = journal.as_mapping(review.get("word_export"))
        evidence = bind(export.get("path"), export.get("sha256"), "Word export PDF")
        if export.get("docx_sha256") != journal.sha256_file(ws / "cv.docx"):
            findings.append("STALE_WORD_EXPORT: export must bind the final DOCX")
        if evidence and journal.sha256_file(evidence) != journal.sha256_file(ws / "cv.pdf"):
            findings.append("PDF_NOT_WORD_EXPORT: deliver the reviewed Word export; do not replace it with a different PDF layout")
        word_export_pdf = evidence
    for name in (("report.pdf",) if report else ("cv.docx", "cv.pdf")):
        if not (ws / name).is_file():
            continue
        item = journal.as_mapping(artifacts.get(name))
        artifact = bind(name, item.get("sha256"), name)
        pages = item.get("pages")
        if type(pages) is not int or pages < 1:
            findings.append(f"BAD_LAYOUT_REVIEW: {name} needs its rendered page count")
            continue
        # A DOCX has no page count of its own; its pages are the bound Word
        # export's. Unchecked, a review could record cv.docx as 1 page beside a
        # 2-page export and pass with page 2 of the Word layout never inspected.
        counted = artifact if name.endswith(".pdf") else (word_export_pdf if name == "cv.docx" else None)
        if counted:
            try:
                import pymupdf
                with pymupdf.open(counted) as doc:
                    if len(doc) != pages:
                        what = name if counted is artifact else f"{name} (its Word export PDF)"
                        findings.append(f"LAYOUT_PAGE_COUNT: {what} has {len(doc)} pages, review recorded {pages}")
            except Exception as exc:
                findings.append(f"UNREADABLE_LAYOUT_PDF: {name}: {exc}")
        previews = item.get("previews")
        seen = []
        if not isinstance(previews, list):
            previews = []
        for i, raw in enumerate(previews):
            preview = journal.as_mapping(raw)
            seen.append(preview.get("page"))
            status = preview.get("review_status")
            if status is not None and status not in ("pass", "reused"):
                findings.append(f"UNREVIEWED_LAYOUT_PAGE: {name} page {preview.get('page')} still needs visual inspection")
            if status == "reused" or "reused_from" in preview:
                import layout_pages
                problem = layout_pages.validate_reuse(ws, review, name, preview, report, hashes, reuse_cache)
                if problem:
                    findings.append(problem)
            image = bind(preview.get("path"), preview.get("sha256"), f"{name} preview {i + 1}")
            if image:
                try:
                    import pymupdf
                    pix = pymupdf.Pixmap(image)
                    if pix.width < 1 or pix.height < 1:
                        raise ValueError("empty image")
                except Exception:
                    findings.append(f"UNREADABLE_LAYOUT_PREVIEW: {image.name}")
        if any(type(n) is not int for n in seen) or sorted(seen) != list(range(1, pages + 1)):
            findings.append(f"UNREVIEWED_LAYOUT_PAGE: {name} needs exactly one inspected preview for every rendered page")
    return findings, hashes


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", required=True, type=pathlib.Path)
    parser.add_argument("--report", action="store_true", help="review report.pdf against report-layout-requirements.yaml")
    args = parser.parse_args(argv)
    ws = args.workspace.resolve()
    if not ws.is_dir():
        print(f"cannot run {GATE}: workspace {ws} does not exist", file=sys.stderr)
        return 2
    gate = "check_report_layout" if args.report else GATE
    if not any((ws / name).is_file() for name in (("report.pdf",) if args.report else ("cv.docx", "cv.pdf"))):
        findings, hashes = ["NO_LAYOUT_ARTIFACT: no rendered document exists"], {}
        journal.receipt(ws, gate, hashes, "could_not_run", findings)
        print(findings[0], file=sys.stderr)
        return 2
    else:
        findings, hashes = inspect(ws, report=args.report)
    for finding in findings:
        print(finding)
    record = journal.receipt(ws, gate, hashes, "fail" if findings else "pass", findings)
    if not findings:
        import layout_pages
        try:
            layout_pages.remember(ws, args.report, record)
        except Exception as exc:  # the pass receipt is already written; an
            # optional cache must never turn it into a traceback. The review
            # still passed. Unsupported old previews simply get no reusable
            # baseline; the next round must inspect every page.
            print(f"NOTICE_LAYOUT_CACHE_UNAVAILABLE: {type(exc).__name__}: {exc}")
    return 1 if findings else 0


if __name__ == "__main__":
    from cli_io import configure_output
    configure_output()
    sys.exit(main())
