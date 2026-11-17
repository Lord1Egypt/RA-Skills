#!/usr/bin/env python3
"""Validate rendered application artefacts and report CV page usage."""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from common import (
    PROFILE_DIR,
    ValidationError,
    load_application_content,
    load_json,
    public_location,
    validate_cv_selection,
)

DEFAULT_MIN_VERTICAL_FILL = 0.52
DEFAULT_MAX_VERTICAL_FILL = 0.98
USABLE_EDGE_RATIO = 0.01
PLACEHOLDER_PATTERN = re.compile(r"\{\{[^}\n]+\}\}|\bTODO\b|<[^>\n]{1,80}>", re.IGNORECASE)


class PdfInspectionError(RuntimeError):
    pass


@dataclass
class PdfInspection:
    path: Path
    pages: int
    text: str
    page_width: float
    page_height: float
    words: list[tuple[float, float, float, float, str]]


@dataclass
class ValidationReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    pages: int | None = None
    vertical_fill: float | None = None
    last_text_y: float | None = None

    @property
    def ok(self) -> bool:
        return not self.errors


def _run(command: list[str]) -> str:
    completed = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if completed.returncode:
        detail = (completed.stderr or completed.stdout).strip()
        raise PdfInspectionError(f"{' '.join(command[:2])} failed: {detail or 'unknown error'}")
    return completed.stdout


def inspect_pdf(path: Path) -> PdfInspection:
    if not path.is_file() or not path.stat().st_size:
        raise PdfInspectionError(f"Missing or empty PDF: {path.name}")
    pdfinfo, pdftotext = shutil.which("pdfinfo"), shutil.which("pdftotext")
    missing = [name for name, executable in (("pdfinfo", pdfinfo), ("pdftotext", pdftotext)) if not executable]
    if missing:
        raise PdfInspectionError(
            "PDF validation requires Poppler tools on PATH: " + ", ".join(missing)
        )
    info = _run([pdfinfo, str(path)])
    pages_match = re.search(r"^Pages:\s+(\d+)\s*$", info, re.MULTILINE)
    if not pages_match:
        raise PdfInspectionError(f"Could not determine page count for {path.name}")
    text = _run([pdftotext, str(path), "-"])
    bbox = _run([pdftotext, "-bbox", str(path), "-"])
    try:
        root = ET.fromstring(bbox)
    except ET.ParseError as error:
        raise PdfInspectionError(f"Could not parse text coordinates from {path.name}: {error}") from error
    pages = [element for element in root.iter() if element.tag.rsplit("}", 1)[-1] == "page"]
    if not pages:
        raise PdfInspectionError(f"No readable pages found in {path.name}")
    first_page = pages[0]
    try:
        width, height = float(first_page.attrib["width"]), float(first_page.attrib["height"])
    except (KeyError, ValueError) as error:
        raise PdfInspectionError(f"Missing page dimensions in {path.name}") from error
    words: list[tuple[float, float, float, float, str]] = []
    for word in first_page.iter():
        if word.tag.rsplit("}", 1)[-1] != "word":
            continue
        try:
            words.append((
                float(word.attrib["xMin"]), float(word.attrib["yMin"]),
                float(word.attrib["xMax"]), float(word.attrib["yMax"]), word.text or "",
            ))
        except (KeyError, ValueError) as error:
            raise PdfInspectionError(f"Invalid word coordinates in {path.name}") from error
    return PdfInspection(path, int(pages_match.group(1)), text, width, height, words)


def _check_pdf_text(inspection: PdfInspection, report: ValidationReport) -> None:
    if not inspection.text.strip():
        report.errors.append(f"{inspection.path.name} has no extractable text")
    placeholder = PLACEHOLDER_PATTERN.search(inspection.text)
    if placeholder:
        report.errors.append(
            f"{inspection.path.name} contains an open placeholder: {placeholder.group(0)!r}"
        )


def _check_bounds(inspection: PdfInspection, report: ValidationReport) -> None:
    tolerance = 0.5
    usable_left = inspection.page_width * USABLE_EDGE_RATIO
    usable_right = inspection.page_width * (1 - USABLE_EDGE_RATIO)
    usable_top = inspection.page_height * USABLE_EDGE_RATIO
    usable_bottom = inspection.page_height * (1 - USABLE_EDGE_RATIO)
    overflow = [word for word in inspection.words if (
        word[0] < usable_left - tolerance or word[1] < usable_top - tolerance or
        word[2] > usable_right + tolerance or word[3] > usable_bottom + tolerance
    )]
    if overflow:
        report.errors.append(
            f"{inspection.path.name} has text outside the page bounds or usable area (first: {overflow[0][4]!r})"
        )


def _check_cv_fill(inspection: PdfInspection, report: ValidationReport, strict_fill: bool,
                   min_vertical_fill: float, max_vertical_fill: float) -> None:
    report.pages = inspection.pages
    if inspection.pages != 1:
        report.errors.append(f"CV.pdf must have exactly one page; found {inspection.pages}")
        return
    if not inspection.words:
        report.errors.append("CV.pdf has no word coordinates for fill analysis")
        return
    usable_top = inspection.page_height * USABLE_EDGE_RATIO
    usable_bottom = inspection.page_height * (1 - USABLE_EDGE_RATIO)
    first_y = max(min(word[1] for word in inspection.words), usable_top)
    last_y = min(max(word[3] for word in inspection.words), usable_bottom)
    fill = (last_y - first_y) / (usable_bottom - usable_top)
    report.vertical_fill, report.last_text_y = fill, last_y
    if fill < min_vertical_fill:
        message = (
            f"CV vertical fill is {fill:.1%}, below the {min_vertical_fill:.1%} target. "
            "Add relevant, profile-backed content or refine the wording; do not blindly shrink spacing."
        )
        (report.errors if strict_fill else report.warnings).append(message)
    if fill > max_vertical_fill:
        report.errors.append(
            f"CV vertical fill is {fill:.1%}, above the {max_vertical_fill:.1%} maximum; reduce selected content."
        )


def _text_contains(text: str, expected: str) -> bool:
    """Compare PDF text robustly when a renderer inserted line breaks."""
    return " ".join(expected.split()) in " ".join(text.split())


def _leading_text(text: str, limit: int = 500) -> str:
    """Return only the cover-letter header area, not the closing/signature."""
    return text[:limit]


def _check_input_consistency(app_dir: Path, profile_dir: Path, inspections: dict[str, PdfInspection],
                             report: ValidationReport) -> None:
    profile = load_json(profile_dir / "master_profile.json")
    selection_path = app_dir / "cv_selection.json"
    if selection_path.is_file():
        selection = validate_cv_selection(load_json(selection_path), profile_dir)
        cv_text = inspections.get("CV.pdf", PdfInspection(Path("CV.pdf"), 0, "", 0, 0, [])).text
        for expected, label in ((profile.get("full_name", ""), "profile name"),
                                (selection["target_title"], "selected target title")):
            if expected and not _text_contains(cv_text, expected):
                report.errors.append(f"CV.pdf is missing {label}: {expected!r}")
    content_path = app_dir / "application_content.json"
    if content_path.is_file():
        content = load_application_content(content_path, profile)
        cover_text = inspections.get("cover_letter.pdf", PdfInspection(Path("cover_letter.pdf"), 0, "", 0, 0, [])).text
        cover_header = _leading_text(cover_text)
        for expected, label in (
            (profile.get("full_name", ""), "profile name in the cover-letter header"),
            (profile.get("email", ""), "profile email in the cover-letter header"),
            (profile.get("phone", ""), "profile phone in the cover-letter header"),
            (public_location(profile), "profile location in the cover-letter header"),
        ):
            if expected and not _text_contains(cover_header, expected):
                report.errors.append(f"cover_letter.pdf is missing {label}: {expected!r}")
        subject = content["cover_letter"]["subject"]
        if not _text_contains(cover_text, subject):
            report.errors.append(f"cover_letter.pdf is missing the content subject: {subject!r}")
        plain_path = app_dir / "indeed_text.txt"
        if not plain_path.is_file() or not plain_path.read_text(encoding="utf-8").strip():
            report.errors.append("Expected plain-text output is missing or empty: indeed_text.txt")


def validate_application(application_dir: Path, profile_dir: Path = PROFILE_DIR, *, strict_fill: bool = False,
                         min_vertical_fill: float = DEFAULT_MIN_VERTICAL_FILL,
                         max_vertical_fill: float = DEFAULT_MAX_VERTICAL_FILL,
                         inspector: Callable[[Path], PdfInspection] = inspect_pdf) -> ValidationReport:
    report = ValidationReport()
    app_dir = application_dir.expanduser().resolve()
    if not app_dir.is_dir():
        report.errors.append(f"Application directory not found: {app_dir}")
        return report
    if not (0 < min_vertical_fill <= max_vertical_fill <= 1):
        report.errors.append("Fill thresholds must satisfy 0 < min_vertical_fill <= max_vertical_fill <= 1")
        return report
    inspections: dict[str, PdfInspection] = {}
    for filename in ("CV.pdf", "cover_letter.pdf"):
        path = app_dir / filename
        if not path.is_file():
            report.errors.append(f"Expected PDF is missing: {filename}")
            continue
        try:
            inspection = inspector(path)
        except PdfInspectionError as error:
            report.errors.append(str(error))
            continue
        inspections[filename] = inspection
        _check_pdf_text(inspection, report)
        _check_bounds(inspection, report)
    cv = inspections.get("CV.pdf")
    if cv:
        _check_cv_fill(cv, report, strict_fill, min_vertical_fill, max_vertical_fill)
    try:
        _check_input_consistency(app_dir, profile_dir.expanduser().resolve(), inspections, report)
    except (OSError, ValidationError) as error:
        report.errors.append(f"Input validation failed: {error}")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate rendered application files and CV page usage.")
    parser.add_argument("application_directory", type=Path)
    parser.add_argument("--profile-dir", type=Path, default=PROFILE_DIR)
    parser.add_argument("--strict-fill", action="store_true", help="Treat a too-empty CV as an error")
    parser.add_argument("--min-vertical-fill", type=float, default=DEFAULT_MIN_VERTICAL_FILL)
    parser.add_argument("--max-vertical-fill", type=float, default=DEFAULT_MAX_VERTICAL_FILL)
    args = parser.parse_args()
    report = validate_application(
        args.application_directory,
        args.profile_dir,
        strict_fill=args.strict_fill,
        min_vertical_fill=args.min_vertical_fill,
        max_vertical_fill=args.max_vertical_fill,
    )
    if report.pages is not None:
        print(f"CV pages: {report.pages}")
    if report.vertical_fill is not None:
        print(f"CV vertical fill: {report.vertical_fill:.1%}")
    if report.last_text_y is not None:
        print(f"CV last text Y: {report.last_text_y:.2f}")
    for warning in report.warnings:
        print(f"WARNING: {warning}")
    for error in report.errors:
        print(f"ERROR: {error}")
    if report.ok:
        print("Application validation passed")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
