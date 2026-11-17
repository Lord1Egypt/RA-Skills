#!/usr/bin/env python3
"""Deterministic HTML/PDF evidence checks for paged-report artifacts.

This is intentionally a small standard-library CLI.  ``pypdf`` is an optional
runtime dependency used only when a PDF is supplied; a missing dependency is
reported as WARN (or FAIL with ``--require-pdf``) rather than being hidden.
Static checks do not prove visual overflow.  The default overflow and logical /
physical page policy verdicts therefore remain explicit manual-review WARNs.
"""

from __future__ import annotations

import argparse
import html.parser
import importlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable, Mapping

SCHEMA_VERSION = "paged-report-qa/v1"
PASS = "PASS"
WARN = "WARN"
FAIL = "FAIL"
SKIP = "SKIP"

A4_WIDTH_PT = 595.27559055
A4_HEIGHT_PT = 841.88976378
A4_TOLERANCE_PT = 2.0
_LANGUAGE_RE = re.compile(r"^[A-Za-z]{2,3}(?:-[A-Za-z0-9]{2,8})*$")
_DOCTYPE_RE = re.compile(r"^<!doctype\s+html\s*>$", re.IGNORECASE)
_CSS_URL_RE = re.compile(r"url\(\s*(?:([\"'])(.*?)\1|([^)]*?))\s*\)", re.IGNORECASE)


def _check(status: str, message: str, **details: Any) -> dict[str, Any]:
    result: dict[str, Any] = {"status": status, "message": message}
    result.update(details)
    return result


def _status_of(checks: Iterable[Mapping[str, Any]], *, skip_is_warn: bool = False) -> str:
    statuses = [str(item.get("status", WARN)) for item in checks]
    if FAIL in statuses:
        return FAIL
    if WARN in statuses or (skip_is_warn and SKIP in statuses):
        return WARN
    return PASS


def _first_non_whitespace(text: str) -> str:
    return text.lstrip("\ufeff \t\r\n")


class _HTMLProbe(html.parser.HTMLParser):
    """Collect only structural facts needed by the deterministic gate."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.doctypes: list[str] = []
        self.html_attrs: list[dict[str, str]] = []
        self.report_page_count = 0
        self.style_blocks = 0
        self.script_tags = 0
        self.link_tags = 0
        self.resource_refs: list[dict[str, str]] = []
        self.css_chunks: list[str] = []
        self.inline_style_values: list[str] = []
        self._style_depth = 0

    def handle_decl(self, decl: str) -> None:
        if decl.strip().lower().startswith("doctype"):
            self.doctypes.append(decl.strip())

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {name.lower(): (value or "") for name, value in attrs}
        if tag == "html":
            self.html_attrs.append(attr_map)
        if "report-page" in set(attr_map.get("class", "").split()):
            self.report_page_count += 1
        if tag == "style":
            self.style_blocks += 1
            self._style_depth += 1
        elif tag == "script":
            self.script_tags += 1
        elif tag == "link":
            self.link_tags += 1

        if "style" in attr_map:
            self.inline_style_values.append(attr_map["style"])

        resource_attributes = {"src", "srcset", "poster"}
        if tag in {"object", "embed"}:
            resource_attributes.add("data")
        for attribute in sorted(resource_attributes):
            if attribute in attr_map and attr_map[attribute].strip():
                self.resource_refs.append(
                    {"tag": tag, "attribute": attribute, "value": attr_map[attribute]}
                )

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag: str) -> None:
        if tag == "style" and self._style_depth:
            self._style_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._style_depth:
            self.css_chunks.append(data)


def _css_violations(css_values: Iterable[str]) -> list[dict[str, str]]:
    violations: list[dict[str, str]] = []
    for css in css_values:
        if re.search(r"@import\b", css, re.IGNORECASE):
            violations.append({"kind": "css-import", "value": "@import"})
        for match in _CSS_URL_RE.finditer(css):
            value = (match.group(2) or match.group(3) or "").strip()
            if value and not value.lower().startswith("data:"):
                violations.append({"kind": "css-url", "value": value})
    return violations


def _html_evidence(path: Path) -> dict[str, Any]:
    source = path.read_text(encoding="utf-8")
    probe = _HTMLProbe()
    probe.feed(source)
    probe.close()

    first = _first_non_whitespace(source)
    doctype_ok = bool(re.match(r"<!doctype\s+html\s*>", first, re.IGNORECASE))
    doctype = _check(
        PASS if doctype_ok and len(probe.doctypes) == 1 else FAIL,
        "HTML5 doctype is the first declaration" if doctype_ok else "HTML5 doctype is missing or not first",
        observed=len(probe.doctypes),
    )

    html_attrs = probe.html_attrs[0] if probe.html_attrs else {}
    language = html_attrs.get("lang", "").strip()
    language_ok = bool(language and _LANGUAGE_RE.fullmatch(language)) and len(probe.html_attrs) == 1
    language_check = _check(
        PASS if language_ok else FAIL,
        f"html lang={language!r} is present" if language_ok else "html lang is missing or invalid",
        value=language or None,
        html_elements=len(probe.html_attrs),
    )

    css_values = [*probe.css_chunks, *probe.inline_style_values]
    css_violations = _css_violations(css_values)
    resource_violations = [
        ref
        for ref in probe.resource_refs
        if not ref["value"].strip().lower().startswith("data:")
    ]
    containment_violations: list[dict[str, Any]] = []
    if probe.style_blocks == 0:
        containment_violations.append(
            {"kind": "missing-inline-style", "message": "no inline style element found"}
        )
    if probe.link_tags:
        containment_violations.append(
            {"kind": "link-element", "message": "link elements are external document dependencies"}
        )
    if probe.script_tags:
        containment_violations.append(
            {"kind": "script-element", "message": "script elements are not part of a static report"}
        )
    containment_violations.extend(
        {"kind": "resource-reference", **ref} for ref in resource_violations
    )
    containment_violations.extend(css_violations)
    self_containment = _check(
        PASS if not containment_violations else FAIL,
        "inline CSS and no external runtime/resource dependencies"
        if not containment_violations
        else "self-containment violations detected",
        inline_style_blocks=probe.style_blocks,
        violations=containment_violations,
    )

    html_status = _status_of([doctype, language_check, self_containment])
    return {
        "path": str(path),
        "bytes": len(source.encode("utf-8")),
        "status": html_status,
        "checks": {
            "doctype": doctype,
            "language": language_check,
            "self_containment": self_containment,
        },
        "parser": "Python stdlib html.parser.HTMLParser",
    }


def _logical_page_evidence(
    html_evidence: Mapping[str, Any], expected_logical_pages: int | None
) -> dict[str, Any]:
    source = Path(str(html_evidence["path"])).read_text(encoding="utf-8")
    probe = _HTMLProbe()
    probe.feed(source)
    probe.close()
    count = probe.report_page_count
    checks: list[dict[str, Any]] = [
        _check(
            PASS if count > 0 else FAIL,
            f"found {count} logical .report-page container(s)" if count else "no .report-page containers found",
            count=count,
            selector=".report-page",
        )
    ]
    if expected_logical_pages is not None:
        checks.append(
            _check(
                PASS if count == expected_logical_pages else FAIL,
                f"logical page count matches expected {expected_logical_pages}"
                if count == expected_logical_pages
                else f"logical page count {count} does not match expected {expected_logical_pages}",
                expected=expected_logical_pages,
                observed=count,
            )
        )
    return {
        "status": _status_of(checks),
        "count": count,
        "selector": ".report-page",
        "expected": expected_logical_pages,
        "checks": {"count": checks[0], **({"expected": checks[1]} if len(checks) > 1 else {})},
    }


def _load_pypdf() -> tuple[Any | None, dict[str, Any]]:
    try:
        module = importlib.import_module("pypdf")
    except ImportError as exc:
        return None, {
            "name": "pypdf",
            "status": "UNAVAILABLE",
            "error": str(exc),
            "install_hint": "python3 -m pip install pypdf (optional; required only for PDF inspection)",
        }
    return module, {
        "name": "pypdf",
        "status": "AVAILABLE",
        "version": str(getattr(module, "__version__", "unknown")),
    }


def _page_content_bytes(page: Any) -> bytes:
    try:
        contents = page.get_contents()
        if contents is None:
            return b""
        data = contents.get_data()
        return data if isinstance(data, bytes) else str(data).encode("utf-8")
    except Exception:
        return b""


def _page_xobject_count(page: Any) -> int:
    try:
        resources = page.get("/Resources") or {}
        xobjects = resources.get("/XObject") or {}
        return len(xobjects)
    except Exception:
        return 0


def _page_annotation_count(page: Any) -> int:
    try:
        return len(page.get("/Annots") or [])
    except Exception:
        return 0


def _pdf_evidence(path: Path, *, require_pdf: bool) -> dict[str, Any]:
    if not path.exists():
        return {
            "path": str(path),
            "status": FAIL,
            "physical_page_count": None,
            "checks": {
                "readable": _check(FAIL, "PDF path does not exist"),
            },
            "dependency": None,
        }

    pypdf, dependency = _load_pypdf()
    if pypdf is None:
        status = FAIL if require_pdf else WARN
        return {
            "path": str(path),
            "status": status,
            "physical_page_count": None,
            "checks": {
                "dependency": _check(
                    status,
                    "pypdf is required to inspect this PDF" if require_pdf else "PDF inspection skipped because pypdf is unavailable",
                    dependency=dependency,
                )
            },
            "dependency": dependency,
            "manual_review": ["Install pypdf and rerun for deterministic PDF evidence."],
        }

    try:
        reader = pypdf.PdfReader(str(path), strict=False)
        if reader.is_encrypted:
            return {
                "path": str(path),
                "status": FAIL,
                "physical_page_count": None,
                "checks": {"readable": _check(FAIL, "encrypted PDF cannot be inspected without a password")},
                "dependency": dependency,
            }
        pages = list(reader.pages)
    except Exception as exc:
        return {
            "path": str(path),
            "status": FAIL,
            "physical_page_count": None,
            "checks": {"readable": _check(FAIL, f"unable to read PDF: {exc}")},
            "dependency": dependency,
        }

    page_count_check = _check(
        PASS if pages else FAIL,
        f"PDF contains {len(pages)} physical page(s)" if pages else "PDF contains no physical pages",
        count=len(pages),
    )
    mediaboxes: list[dict[str, Any]] = []
    non_a4_pages: list[int] = []
    for page_number, page in enumerate(pages, start=1):
        try:
            box = page.mediabox
            width = float(box.width)
            height = float(box.height)
            portrait = abs(width - A4_WIDTH_PT) <= A4_TOLERANCE_PT and abs(height - A4_HEIGHT_PT) <= A4_TOLERANCE_PT
            landscape = abs(width - A4_HEIGHT_PT) <= A4_TOLERANCE_PT and abs(height - A4_WIDTH_PT) <= A4_TOLERANCE_PT
            is_a4 = portrait or landscape
            orientation = "portrait" if portrait else "landscape" if landscape else "non-a4"
            mediaboxes.append(
                {
                    "page": page_number,
                    "width_pt": round(width, 4),
                    "height_pt": round(height, 4),
                    "orientation": orientation,
                    "within_tolerance": is_a4,
                }
            )
            if not is_a4:
                non_a4_pages.append(page_number)
        except Exception as exc:
            non_a4_pages.append(page_number)
            mediaboxes.append({"page": page_number, "error": str(exc), "within_tolerance": False})

    a4_check = _check(
        PASS if not non_a4_pages else FAIL,
        "all PDF mediaboxes are A4 within ±2pt"
        if not non_a4_pages
        else f"non-A4 mediabox on page(s): {', '.join(map(str, non_a4_pages))}",
        tolerance_pt=A4_TOLERANCE_PT,
        pages=mediaboxes,
        non_a4_pages=non_a4_pages,
    )

    blank_pages: list[int] = []
    textless_render_pages: list[int] = []
    extraction_errors: list[dict[str, Any]] = []
    for page_number, page in enumerate(pages, start=1):
        extraction_failed = False
        try:
            text = page.extract_text() or ""
        except Exception as exc:
            text = ""
            extraction_failed = True
            extraction_errors.append({"page": page_number, "error": str(exc)})
        content = _page_content_bytes(page)
        xobject_count = _page_xobject_count(page)
        annotation_count = _page_annotation_count(page)
        if not text.strip():
            if (
                not extraction_failed
                and not content.strip()
                and not xobject_count
                and not annotation_count
            ):
                blank_pages.append(page_number)
            else:
                textless_render_pages.append(page_number)

    blank_status = FAIL if blank_pages else WARN if textless_render_pages or extraction_errors else PASS
    blank_message = (
        f"blank physical page(s): {', '.join(map(str, blank_pages))}"
        if blank_pages
        else "no blank physical pages detected"
        if not textless_render_pages and not extraction_errors
        else "some pages have no extractable text; visual review is required"
    )
    blank_check = _check(
        blank_status,
        blank_message,
        pages=blank_pages,
        textless_render_pages=textless_render_pages,
        extraction_errors=extraction_errors,
        detection="no text, content stream, XObject, or annotation; textless rendered pages remain manual",
    )
    checks: dict[str, Any] = {
        "readable": _check(PASS, "PDF parsed by pypdf", dependency=dependency),
        "physical_page_count": page_count_check,
        "a4_mediabox": a4_check,
        "blank_pages": blank_check,
    }
    return {
        "path": str(path),
        "status": _status_of(checks.values()),
        "physical_page_count": len(pages),
        "checks": checks,
        "dependency": dependency,
        "blank_pages": blank_pages,
        "mediaboxes": mediaboxes,
    }


def _expected_physical_check(
    pdf_evidence: Mapping[str, Any], expected_physical_pages: int | None
) -> dict[str, Any] | None:
    if expected_physical_pages is None:
        return None
    observed = pdf_evidence.get("physical_page_count")
    if observed is None:
        return _check(
            FAIL,
            "expected physical page count cannot be checked without a readable PDF",
            expected=expected_physical_pages,
            observed=None,
        )
    return _check(
        PASS if observed == expected_physical_pages else FAIL,
        f"physical page count matches expected {expected_physical_pages}"
        if observed == expected_physical_pages
        else f"physical page count {observed} does not match expected {expected_physical_pages}",
        expected=expected_physical_pages,
        observed=observed,
    )


def _page_policy_evidence(
    logical_pages: int,
    physical_pages: int | None,
    policy: str,
    expected_physical_check: dict[str, Any] | None,
) -> dict[str, Any]:
    checks: dict[str, dict[str, Any]] = {}
    if expected_physical_check is not None:
        checks["expected_physical_pages"] = expected_physical_check

    if policy == "independent":
        checks["policy"] = _check(
            WARN,
            "logical .report-page count and physical PDF page count are intentionally not equated",
            verdict="INDEPENDENT",
        )
        verdict = "INDEPENDENT"
    elif physical_pages is None:
        checks["policy"] = _check(
            FAIL,
            f"page policy {policy!r} requires a readable PDF",
            logical_pages=logical_pages,
            physical_pages=None,
        )
        verdict = "NOT_EVALUATED"
    elif policy == "exact":
        passed = physical_pages == logical_pages
        checks["policy"] = _check(
            PASS if passed else FAIL,
            "physical and logical counts match under explicit exact policy"
            if passed
            else f"exact policy mismatch: logical={logical_pages}, physical={physical_pages}",
            logical_pages=logical_pages,
            physical_pages=physical_pages,
            verdict="EXACT_PASS" if passed else "EXACT_FAIL",
        )
        verdict = "EXACT_PASS" if passed else "EXACT_FAIL"
    elif policy == "at-least":
        passed = physical_pages >= logical_pages
        checks["policy"] = _check(
            PASS if passed else FAIL,
            "physical page count is at least the logical container count under explicit at-least policy"
            if passed
            else f"at-least policy mismatch: logical={logical_pages}, physical={physical_pages}",
            logical_pages=logical_pages,
            physical_pages=physical_pages,
            verdict="AT_LEAST_PASS" if passed else "AT_LEAST_FAIL",
        )
        verdict = "AT_LEAST_PASS" if passed else "AT_LEAST_FAIL"
    else:  # defensive guard for direct callers
        raise ValueError(f"unsupported page policy: {policy}")

    return {
        "status": _status_of(checks.values()),
        "policy": policy,
        "verdict": verdict,
        "logical_pages": logical_pages,
        "physical_pages": physical_pages,
        "checks": checks,
    }


def _overflow_evidence(status: str, evidence: str | None) -> dict[str, Any]:
    if status == "manual":
        return {
            "status": WARN,
            "verdict": "MANUAL_REVIEW_REQUIRED",
            "method": "static HTML/PDF gate",
            "message": "static inspection cannot prove browser layout overflow; inspect via Kimi WebBridge or formal Playwright E2E",
        }
    if status == "pass":
        if not evidence or not evidence.strip():
            return {
                "status": FAIL,
                "verdict": "INVALID_EXTERNAL_EVIDENCE",
                "message": "--overflow-status pass requires --overflow-evidence",
            }
        return {
            "status": PASS,
            "verdict": "PASS",
            "method": "caller-supplied browser evidence",
            "evidence": evidence,
            "message": "recorded external browser evidence; not inferred from static HTML",
        }
    return {
        "status": FAIL,
        "verdict": "FAIL",
        "method": "caller-supplied browser evidence",
        "evidence": evidence,
        "message": "caller reported overflow or clipping",
    }


def run_gate(
    html_path: str | Path,
    *,
    pdf_path: str | Path | None = None,
    expected_logical_pages: int | None = None,
    expected_physical_pages: int | None = None,
    page_policy: str = "independent",
    require_pdf: bool = False,
    overflow_status: str = "manual",
    overflow_evidence: str | None = None,
) -> dict[str, Any]:
    """Return machine-readable evidence for one HTML artifact and optional PDF."""
    html_file = Path(html_path)
    if not html_file.exists():
        raise FileNotFoundError(f"HTML path does not exist: {html_file}")
    if expected_logical_pages is not None and expected_logical_pages < 0:
        raise ValueError("expected logical page count must be non-negative")
    if expected_physical_pages is not None and expected_physical_pages < 0:
        raise ValueError("expected physical page count must be non-negative")
    if page_policy not in {"independent", "exact", "at-least"}:
        raise ValueError("page policy must be one of: independent, exact, at-least")
    if overflow_status not in {"manual", "pass", "fail"}:
        raise ValueError("overflow status must be one of: manual, pass, fail")

    html_evidence = _html_evidence(html_file)
    logical_evidence = _logical_page_evidence(html_evidence, expected_logical_pages)

    if pdf_path is None:
        provided_status = FAIL if require_pdf else SKIP
        provided_message = (
            "PDF is required but no PDF was supplied"
            if require_pdf
            else "no PDF supplied; physical-page checks were not run"
        )
        dependency_status = "REQUIRED" if require_pdf else "NOT_NEEDED"
        dependency_message = (
            "supply --pdf to satisfy --require-pdf"
            if require_pdf
            else "supply --pdf to enable PDF inspection"
        )
        pdf_evidence: dict[str, Any] = {
            "path": None,
            "status": provided_status,
            "physical_page_count": None,
            "checks": {
                "provided": _check(provided_status, provided_message),
            },
            "dependency": {
                "name": "pypdf",
                "status": dependency_status,
                "message": dependency_message,
            },
        }
    else:
        pdf_evidence = _pdf_evidence(Path(pdf_path), require_pdf=require_pdf)

    expected_physical_check = _expected_physical_check(pdf_evidence, expected_physical_pages)
    page_policy_evidence = _page_policy_evidence(
        int(logical_evidence["count"]),
        pdf_evidence.get("physical_page_count"),
        page_policy,
        expected_physical_check,
    )
    overflow_evidence_result = _overflow_evidence(overflow_status, overflow_evidence)

    statuses = [
        html_evidence["status"],
        logical_evidence["status"],
        pdf_evidence["status"],
        page_policy_evidence["status"],
        overflow_evidence_result["status"],
    ]
    overall = FAIL if FAIL in statuses else WARN if WARN in statuses else PASS
    manual_review: list[str] = []
    if overflow_evidence_result["status"] == WARN:
        manual_review.append("Review rendered browser output for overflow, clipping, and visual hierarchy.")
    if page_policy == "independent":
        manual_review.append("Do not equate logical .report-page containers with physical PDF pages.")
    if pdf_evidence.get("status") in {WARN, SKIP}:
        manual_review.append("PDF physical evidence is incomplete; rerun with an available pypdf dependency and/or a PDF artifact.")

    return {
        "schema_version": SCHEMA_VERSION,
        "status": overall,
        "inputs": {
            "html": str(html_file),
            "pdf": str(pdf_path) if pdf_path is not None else None,
        },
        "html": html_evidence,
        "logical_pages": logical_evidence,
        "pdf": pdf_evidence,
        "overflow": overflow_evidence_result,
        "page_policy": page_policy_evidence,
        "manual_review": manual_review,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", type=Path, help="self-contained report HTML")
    parser.add_argument("--pdf", type=Path, help="optional PDF rendered from the report")
    parser.add_argument("--expected-logical-pages", type=int)
    parser.add_argument("--expected-physical-pages", type=int)
    parser.add_argument(
        "--page-policy",
        choices=("independent", "exact", "at-least"),
        default="independent",
        help="comparison policy; independent is the safe default",
    )
    parser.add_argument(
        "--require-pdf",
        action="store_true",
        help="require --pdf and turn missing PDF inspection dependencies into deterministic failures",
    )
    parser.add_argument(
        "--overflow-status",
        choices=("manual", "pass", "fail"),
        default="manual",
        help="record external browser overflow evidence; default is manual review",
    )
    parser.add_argument("--overflow-evidence", help="short provenance note for --overflow-status pass/fail")
    parser.add_argument("--pretty", action="store_true", help="indent JSON output")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    try:
        evidence = run_gate(
            args.html,
            pdf_path=args.pdf,
            expected_logical_pages=args.expected_logical_pages,
            expected_physical_pages=args.expected_physical_pages,
            page_policy=args.page_policy,
            require_pdf=args.require_pdf,
            overflow_status=args.overflow_status,
            overflow_evidence=args.overflow_evidence,
        )
    except (OSError, ValueError) as exc:
        evidence = {
            "schema_version": SCHEMA_VERSION,
            "status": FAIL,
            "error": str(exc),
        }
    print(json.dumps(evidence, ensure_ascii=False, sort_keys=True, indent=2 if args.pretty else None))
    return 1 if evidence.get("status") == FAIL else 0


if __name__ == "__main__":
    raise SystemExit(main())
