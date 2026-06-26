#!/usr/bin/env python3
"""Merge travel reimbursement folders, converting Excel and placing invoices/images two-up on A4."""

from __future__ import annotations

import argparse
import importlib
import json
import math
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from zipfile import BadZipFile, ZipFile
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Iterable


AUTO_INSTALL_DEPS = "--no-auto-install" not in sys.argv and os.environ.get("MERGE_TRAVEL_PDFS_NO_AUTO_INSTALL") != "1"


def ensure_python_package(module_name: str, package_name: str):
    try:
        return importlib.import_module(module_name)
    except ModuleNotFoundError:
        if not AUTO_INSTALL_DEPS:
            raise
        print(f"Installing missing Python package: {package_name}", file=sys.stderr)
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return importlib.import_module(module_name)


fitz = ensure_python_package("fitz", "PyMuPDF")
openpyxl_module = ensure_python_package("openpyxl", "openpyxl")
load_workbook = openpyxl_module.load_workbook
Image = ensure_python_package("PIL.Image", "Pillow")


A4_WIDTH = 595.275590551
A4_HEIGHT = 841.88976378
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp", ".webp"}
SPREADSHEET_EXTS = {".xlsx", ".xls", ".xlsm"}
GENERATED_MARKERS = (
    "合并结果",
    "合并报告",
    "合并检查",
    "merge_report",
    "merged_travel_pdfs",
)

INVOICE_KEYWORDS = [
    ("发票号码", 4),
    ("发票代码", 4),
    ("开票日期", 3),
    ("价税合计", 4),
    ("购买方", 3),
    ("销售方", 3),
    ("纳税人识别号", 3),
    ("统一社会信用代码", 3),
    ("增值税", 4),
    ("电子发票", 4),
    ("全电发票", 4),
    ("数电票", 4),
    ("数电", 2),
    ("税率", 2),
    ("税额", 2),
    ("校验码", 3),
    ("税务局", 2),
    ("国家税务总局", 3),
]

FILENAME_INVOICE_KEYWORDS = [
    ("电子发票", 4),
    ("增值税", 4),
    ("发票", 3),
    ("dzfp", 3),
    ("invoice", 3),
]


@dataclass
class Item:
    path: str
    rel_path: str
    kind: str
    classification: str
    pages: int
    invoice_score: int = 0
    matched_signals: list[str] = field(default_factory=list)
    spreadsheet_sheets: list[str] = field(default_factory=list)
    warning: str | None = None


def natural_key(value: str) -> list[object]:
    parts = re.split(r"(\d+)", value.casefold())
    return [int(part) if part.isdigit() else part for part in parts]


def iter_input_files(root: Path, output: Path | None, report: Path | None) -> list[Path]:
    excludes = {p.resolve() for p in (output, report) if p is not None}
    files: list[Path] = []
    for path in root.rglob("*"):
        rel_path = str(path.relative_to(root))
        if not path.is_file():
            continue
        if path.name.startswith(".") or path.name.startswith("~$") or path.name.startswith(".~"):
            continue
        if path.resolve() in excludes:
            continue
        if any(marker in rel_path for marker in GENERATED_MARKERS):
            continue
        if path.suffix.lower() == ".pdf" or path.suffix.lower() in IMAGE_EXTS or path.suffix.lower() in SPREADSHEET_EXTS:
            files.append(path)
    return sorted(files, key=lambda p: natural_key(str(p.relative_to(root))))


def text_from_pdf(path: Path, max_pages: int = 3) -> tuple[str, str | None]:
    try:
        with fitz.open(path) as doc:
            if doc.is_encrypted:
                return "", "encrypted PDF cannot be read without a password"
            chunks = []
            for page_index in range(min(max_pages, doc.page_count)):
                chunks.append(doc.load_page(page_index).get_text("text"))
            return "\n".join(chunks), None
    except Exception as exc:  # noqa: BLE001 - report bad source files without stopping scan
        return "", f"text extraction failed: {exc}"


def count_pdf_pages(path: Path) -> tuple[int, str | None]:
    try:
        with fitz.open(path) as doc:
            return doc.page_count, None
    except Exception as exc:  # noqa: BLE001
        return 0, f"page count failed: {exc}"


def pdf_is_a4_full_page(path: Path) -> bool:
    try:
        with fitz.open(path) as doc:
            if doc.page_count == 0:
                return False
            for page in doc:
                width = page.rect.width
                height = page.rect.height
                portrait_a4 = 540 <= width <= 640 and 760 <= height <= 900
                landscape_a4 = 760 <= width <= 900 and 540 <= height <= 640
                if not (portrait_a4 or landscape_a4):
                    return False
            return True
    except Exception:
        return False


def matches_any(rel_path: str, patterns: Iterable[str]) -> bool:
    normalized = rel_path.casefold()
    return any(pattern.casefold() in normalized for pattern in patterns)


def classify_pdf(path: Path, root: Path, force_invoice: list[str], force_normal: list[str]) -> Item:
    rel_path = str(path.relative_to(root))
    pages, count_warning = count_pdf_pages(path)
    if matches_any(rel_path, force_invoice):
        return Item(str(path), rel_path, "pdf", "invoice", pages, matched_signals=["manual:force-invoice"], warning=count_warning)
    if matches_any(rel_path, force_normal):
        return Item(str(path), rel_path, "pdf", "normal", pages, matched_signals=["manual:force-normal"], warning=count_warning)

    text, text_warning = text_from_pdf(path)
    haystack = f"{path.name}\n{text}"
    if "航旅纵横" in haystack or "行程校验单" in path.name:
        return Item(
            str(path),
            rel_path,
            "hanglv_pdf",
            "normal",
            pages,
            matched_signals=["航旅纵横/行程校验单"],
            warning=count_warning or text_warning,
        )

    score = 0
    signals: list[str] = []
    for keyword, weight in INVOICE_KEYWORDS:
        if keyword.casefold() in haystack.casefold():
            score += weight
            signals.append(keyword)
    for keyword, weight in FILENAME_INVOICE_KEYWORDS:
        if keyword.casefold() in path.name.casefold():
            score += weight
            signals.append(f"filename:{keyword}")

    has_text = len(text.strip()) >= 30
    threshold = 8 if has_text else 3
    classification = "invoice" if score >= threshold else "normal"
    warning = count_warning or text_warning
    if classification == "invoice" and pdf_is_a4_full_page(path):
        return Item(str(path), rel_path, "a4_invoice_pdf", "normal", pages, score, signals + ["A4/full-page invoice"], warning)
    if not has_text and classification == "normal":
        warning = warning or "little or no extractable text; use manual override if this scanned PDF is an invoice"
    return Item(str(path), rel_path, "pdf", classification, pages, score, signals, warning)


def classify_image(path: Path, root: Path, force_invoice: list[str], force_normal: list[str]) -> Item:
    rel_path = str(path.relative_to(root))
    if matches_any(rel_path, force_invoice):
        return Item(str(path), rel_path, "image", "invoice", 1, matched_signals=["manual:force-invoice"])
    if matches_any(rel_path, force_normal):
        return Item(str(path), rel_path, "image", "normal", 1, matched_signals=["manual:force-normal"])
    return Item(str(path), rel_path, "image", "normal", 1, warning="image included as normal A5 attachment; invoice detection for images requires manual override")


def spreadsheet_sheet_names(path: Path) -> tuple[list[str], str | None]:
    if path.suffix.lower() not in {".xlsx", ".xlsm"}:
        return [], "legacy .xls sheet names are not inspected before conversion"
    try:
        with ZipFile(path) as archive:
            root = ET.fromstring(archive.read("xl/workbook.xml"))
    except (KeyError, BadZipFile, ET.ParseError) as exc:
        return [], f"could not inspect workbook sheets: {exc}"

    namespace = {"a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    sheets_node = root.find("a:sheets", namespace)
    if sheets_node is None:
        return [], "could not find workbook sheets"
    names = []
    for sheet in sheets_node:
        state = sheet.attrib.get("state", "visible")
        if state == "visible":
            names.append(sheet.attrib.get("name", "Sheet"))
    return names, None


def classify_spreadsheet(path: Path, root: Path) -> Item:
    rel_path = str(path.relative_to(root))
    sheet_names, sheet_warning = spreadsheet_sheet_names(path)
    warning = "spreadsheet will be converted to PDF and included as normal attachment"
    if sheet_warning:
        warning = f"{warning}; {sheet_warning}"
    return Item(str(path), rel_path, "spreadsheet", "normal", 0, spreadsheet_sheets=sheet_names, warning=warning)


def classify_files(files: list[Path], root: Path, force_invoice: list[str], force_normal: list[str]) -> list[Item]:
    items: list[Item] = []
    for path in files:
        if path.suffix.lower() == ".pdf":
            items.append(classify_pdf(path, root, force_invoice, force_normal))
        elif path.suffix.lower() in IMAGE_EXTS:
            items.append(classify_image(path, root, force_invoice, force_normal))
        else:
            items.append(classify_spreadsheet(path, root))
    return items


def fit_rect(page_width: float, page_height: float, box: fitz.Rect) -> fitz.Rect:
    scale = min(box.width / page_width, box.height / page_height)
    width = page_width * scale
    height = page_height * scale
    x0 = box.x0 + (box.width - width) / 2
    y0 = box.y0 + (box.height - height) / 2
    return fitz.Rect(x0, y0, x0 + width, y0 + height)


def half_page_slots() -> list[fitz.Rect]:
    margin = 28
    gap = 16
    slot_height = (A4_HEIGHT - margin * 2 - gap) / 2
    return [
        fitz.Rect(margin, margin, A4_WIDTH - margin, margin + slot_height),
        fitz.Rect(margin, margin + slot_height + gap, A4_WIDTH - margin, A4_HEIGHT - margin),
    ]


def add_image_to_slot(page: fitz.Page, image_path: Path, slot: fitz.Rect, rotate_degrees: int) -> None:
    with Image.open(image_path) as img:
        width, height = img.size
    fit_width, fit_height = (height, width) if rotate_degrees in {90, 270} else (width, height)
    page.insert_image(
        fit_rect(fit_width, fit_height, slot),
        filename=str(image_path),
        keep_proportion=True,
        rotate=rotate_degrees,
    )


def add_half_sheet(out: fitz.Document, entries: list[tuple[str, Path, int | None]], image_rotate: int) -> None:
    page = out.new_page(width=A4_WIDTH, height=A4_HEIGHT)
    for slot, (kind, path, page_index) in zip(half_page_slots(), entries):
        if kind == "image":
            add_image_to_slot(page, path, slot, image_rotate)
        else:
            assert page_index is not None
            with fitz.open(path) as src:
                src_page = src.load_page(page_index)
                target = fit_rect(src_page.rect.width, src_page.rect.height, slot)
                page.show_pdf_page(target, src, page_index, keep_proportion=True)


def prepare_spreadsheet_for_pdf(path: Path, temp_dir: Path) -> Path:
    if path.suffix.lower() not in {".xlsx", ".xlsm"}:
        return path

    workbook = load_workbook(path, keep_vba=path.suffix.lower() == ".xlsm")
    for sheet in workbook.worksheets:
        if sheet.sheet_state != "visible":
            continue
        sheet.sheet_properties.pageSetUpPr.fitToPage = True
        sheet.page_setup.paperSize = sheet.PAPERSIZE_A4
        sheet.page_setup.orientation = sheet.ORIENTATION_PORTRAIT
        sheet.page_setup.fitToWidth = 1
        sheet.page_setup.fitToHeight = 0
        sheet.page_margins.left = 0.25
        sheet.page_margins.right = 0.25
        sheet.page_margins.top = 0.35
        sheet.page_margins.bottom = 0.35
        sheet.print_options.horizontalCentered = True
        used_range = sheet.calculate_dimension()
        if used_range and used_range != "A1:A1":
            sheet.print_area = used_range

    prepared = temp_dir / f"printfit_{path.name}"
    workbook.save(prepared)
    workbook.close()
    return prepared


def find_soffice() -> str | None:
    candidates = [shutil.which("soffice"), shutil.which("libreoffice")]
    system = platform.system()
    if system == "Darwin":
        candidates.extend(
            [
                "/Applications/LibreOffice.app/Contents/MacOS/soffice",
                str(Path.home() / "Applications/LibreOffice.app/Contents/MacOS/soffice"),
            ]
        )
    elif system == "Windows":
        program_files = [os.environ.get("PROGRAMFILES"), os.environ.get("PROGRAMFILES(X86)")]
        for base in program_files:
            if base:
                candidates.append(str(Path(base) / "LibreOffice" / "program" / "soffice.exe"))
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return candidate
    return None


def install_libreoffice() -> None:
    if not AUTO_INSTALL_DEPS:
        raise RuntimeError("LibreOffice/soffice not found and auto-install is disabled")

    system = platform.system()
    commands: list[list[str]] = []
    if system == "Darwin":
        brew = shutil.which("brew")
        if brew:
            commands.append([brew, "install", "--cask", "libreoffice"])
    elif system == "Windows":
        winget = shutil.which("winget")
        choco = shutil.which("choco")
        if winget:
            commands.append([winget, "install", "--id", "TheDocumentFoundation.LibreOffice", "-e", "--accept-package-agreements", "--accept-source-agreements"])
        if choco:
            commands.append([choco, "install", "libreoffice-fresh", "-y"])
    else:
        apt = shutil.which("apt-get")
        dnf = shutil.which("dnf")
        yum = shutil.which("yum")
        if apt:
            commands.append([apt, "update"])
            commands.append([apt, "install", "-y", "libreoffice"])
        if dnf:
            commands.append([dnf, "install", "-y", "libreoffice"])
        if yum:
            commands.append([yum, "install", "-y", "libreoffice"])

    if not commands:
        raise RuntimeError(
            "LibreOffice/soffice not found and no supported package manager was detected. "
            "Install LibreOffice manually, then rerun."
        )

    print("LibreOffice/soffice not found. Attempting automatic install...", file=sys.stderr)
    for command in commands:
        result = subprocess.run(command, check=False)
        if result.returncode != 0:
            raise RuntimeError(f"automatic LibreOffice install failed while running: {' '.join(command)}")


def ensure_soffice() -> str:
    soffice = find_soffice()
    if soffice:
        return soffice
    install_libreoffice()
    soffice = find_soffice()
    if soffice:
        return soffice
    raise RuntimeError("LibreOffice installation finished, but soffice still was not found. Restart the terminal or install LibreOffice manually.")


def convert_spreadsheet_to_pdf(path: Path, temp_dir: Path) -> Path:
    soffice = ensure_soffice()

    source = prepare_spreadsheet_for_pdf(path, temp_dir)
    before = {p.resolve() for p in temp_dir.glob("*.pdf")}
    result = subprocess.run(
        [soffice, "--headless", "--convert-to", "pdf", "--outdir", str(temp_dir), str(source)],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "").strip()
        raise RuntimeError(f"failed to convert spreadsheet {path}: {detail}")

    expected = temp_dir / f"{source.stem}.pdf"
    if expected.exists():
        return expected
    created = [p for p in temp_dir.glob("*.pdf") if p.resolve() not in before]
    if len(created) == 1:
        return created[0]
    raise RuntimeError(f"spreadsheet conversion did not produce a PDF for {path}")


def merge(items: list[Item], output: Path, image_rotate: int) -> dict[str, int]:
    out = fitz.open()
    normal_pdf_pages = 0
    a4_invoice_pages = 0
    spreadsheet_pages = 0
    hanglv_pages = 0
    normal_image_slots: list[tuple[str, Path, int | None]] = []
    invoice_slots: list[tuple[str, Path, int | None]] = []
    converted_spreadsheets: list[dict[str, object]] = []

    with tempfile.TemporaryDirectory(prefix="merge-travel-pdfs-") as temp_name:
        temp_dir = Path(temp_name)
        for item in [i for i in items if i.classification == "normal" and i.kind != "hanglv_pdf"]:
            path = Path(item.path)
            if item.kind in {"pdf", "a4_invoice_pdf"}:
                with fitz.open(path) as src:
                    out.insert_pdf(src)
                    if item.kind == "a4_invoice_pdf":
                        a4_invoice_pages += src.page_count
                    else:
                        normal_pdf_pages += src.page_count
            elif item.kind == "spreadsheet":
                converted = convert_spreadsheet_to_pdf(path, temp_dir)
                with fitz.open(converted) as src:
                    out.insert_pdf(src)
                    item.pages = src.page_count
                    visible_sheet_count = len(item.spreadsheet_sheets)
                    if visible_sheet_count and src.page_count < visible_sheet_count:
                        item.warning = (
                            f"{item.warning}; converted PDF has fewer pages ({src.page_count}) "
                            f"than visible sheets ({visible_sheet_count})"
                        )
                    spreadsheet_pages += src.page_count
                    converted_spreadsheets.append({"source": item.rel_path, "pages": src.page_count, "sheets": item.spreadsheet_sheets})
            else:
                normal_image_slots.append(("image", path, None))

        for item in [i for i in items if i.kind == "hanglv_pdf"]:
            path = Path(item.path)
            with fitz.open(path) as src:
                out.insert_pdf(src)
                hanglv_pages += src.page_count

        for start in range(0, len(normal_image_slots), 2):
            add_half_sheet(out, normal_image_slots[start : start + 2], image_rotate)

        for item in [i for i in items if i.classification == "invoice"]:
            path = Path(item.path)
            if item.kind == "pdf":
                with fitz.open(path) as src:
                    for page_index in range(src.page_count):
                        invoice_slots.append(("pdf", path, page_index))
            else:
                invoice_slots.append(("image", path, None))

        for start in range(0, len(invoice_slots), 2):
            add_half_sheet(out, invoice_slots[start : start + 2], image_rotate)

        output.parent.mkdir(parents=True, exist_ok=True)
        out.save(output, garbage=4, deflate=True)
        out.close()

    normal_image_sheets = math.ceil(len(normal_image_slots) / 2)
    invoice_sheets = math.ceil(len(invoice_slots) / 2)
    return {
        "normal_pdf_pages": normal_pdf_pages,
        "a4_invoice_pages": a4_invoice_pages,
        "spreadsheet_pages": spreadsheet_pages,
        "hanglv_pages": hanglv_pages,
        "converted_spreadsheets": converted_spreadsheets,
        "normal_image_pages": len(normal_image_slots),
        "normal_image_sheets": normal_image_sheets,
        "normal_pages": normal_pdf_pages + a4_invoice_pages + spreadsheet_pages + hanglv_pages + normal_image_sheets,
        "invoice_pages": len(invoice_slots),
        "invoice_sheets": invoice_sheets,
        "expected_output_pages": normal_pdf_pages + a4_invoice_pages + spreadsheet_pages + hanglv_pages + normal_image_sheets + invoice_sheets,
    }


def render_check(output: Path, check_dir: Path) -> list[str]:
    check_dir.mkdir(parents=True, exist_ok=True)
    for old_png in check_dir.glob("page-*.png"):
        old_png.unlink()
    rendered: list[str] = []
    with fitz.open(output) as doc:
        if doc.page_count == 0:
            return rendered
        indexes = {0, doc.page_count - 1}
        if doc.page_count > 2:
            indexes.add(doc.page_count // 2)
        for index in sorted(indexes):
            pix = doc.load_page(index).get_pixmap(matrix=fitz.Matrix(0.35, 0.35), alpha=False)
            target = check_dir / f"page-{index + 1:03d}.png"
            pix.save(target)
            rendered.append(str(target))
    return rendered


def verify(output: Path, expected_pages: int) -> tuple[int, bool, str | None]:
    try:
        with fitz.open(output) as doc:
            actual_pages = doc.page_count
    except Exception as exc:  # noqa: BLE001
        return 0, False, f"output verification failed: {exc}"
    return actual_pages, actual_pages == expected_pages, None


def write_report(path: Path, report: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")


def default_output_for(root: Path) -> Path:
    return root / f"{root.name}PDF合并结果.pdf"


def default_report_for(root: Path) -> Path:
    return root / f"{root.name}PDF合并报告.json"


def default_render_check_for(root: Path) -> Path:
    return root / "合并检查缩略图"


def process_folder(
    root: Path,
    output: Path,
    report_path: Path,
    render_check_dir: Path | None,
    args: argparse.Namespace,
) -> bool:
    if not args.overwrite:
        for candidate in [output, report_path]:
            if candidate.exists() and not args.dry_run:
                print(f"ERROR: exists, pass --overwrite to replace: {candidate}", file=sys.stderr)
                return False

    files = iter_input_files(root, output, report_path)
    items = classify_files(files, root, args.force_invoice, args.force_normal)
    warnings = [f"{item.rel_path}: {item.warning}" for item in items if item.warning]
    report = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "source_folder": str(root),
        "output": str(output),
        "dry_run": args.dry_run,
        "image_rotate": args.image_rotate,
        "input_count": len(items),
        "normal_count": sum(1 for item in items if item.classification == "normal"),
        "invoice_count": sum(1 for item in items if item.classification == "invoice"),
        "items": [asdict(item) for item in items],
        "warnings": warnings,
    }

    if args.dry_run:
        write_report(report_path, report)
        print(f"Dry run complete. Source: {root}")
        print(f"Report: {report_path}")
        print(f"Normal: {report['normal_count']}  Invoice: {report['invoice_count']}  Warnings: {len(warnings)}")
        return True

    counts = merge(items, output, args.image_rotate)
    actual_pages, ok, verify_warning = verify(output, counts["expected_output_pages"])
    rendered = render_check(output, render_check_dir) if render_check_dir else []
    report.update(counts)
    report["items"] = [asdict(item) for item in items]
    report["warnings"] = [f"{item.rel_path}: {item.warning}" for item in items if item.warning]
    report.update(
        {
            "actual_output_pages": actual_pages,
            "verification_ok": ok and verify_warning is None,
            "verification_warning": verify_warning,
            "rendered_check_images": rendered,
        }
    )
    if verify_warning:
        report["warnings"].append(verify_warning)
    write_report(report_path, report)

    print(f"Output: {output}")
    print(f"Report: {report_path}")
    if rendered:
        print(f"Rendered check images: {len(rendered)} in {render_check_dir}")
    print(
        "Pages: normal_pdf={normal_pdf_pages}, a4_invoice={a4_invoice_pages}, spreadsheet={spreadsheet_pages}, hanglv={hanglv_pages}, normal_image_sheets={normal_image_sheets}, invoice_pages={invoice_pages}, "
        "invoice_sheets={invoice_sheets}, output={actual_output_pages}, ok={verification_ok}".format(**report)
    )
    if report["warnings"]:
        print(f"Warnings: {len(report['warnings'])}; review report for details")
    return report["verification_ok"]


def folder_has_supported_inputs(root: Path) -> bool:
    if any(marker in str(root) for marker in GENERATED_MARKERS):
        return False
    return any(
        path.is_file()
        and not path.name.startswith(".")
        and not any(marker in str(path.relative_to(root)) for marker in GENERATED_MARKERS)
        and (path.suffix.lower() == ".pdf" or path.suffix.lower() in IMAGE_EXTS or path.suffix.lower() in SPREADSHEET_EXTS)
        for path in root.rglob("*")
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path, help="Folder containing PDFs/images/Excel files to merge")
    parser.add_argument("--output", type=Path, help="Output PDF path")
    parser.add_argument("--report", type=Path, help="JSON report path")
    parser.add_argument("--render-check", type=Path, help="Directory for rendered check PNGs")
    parser.add_argument("--split-subfolders", action="store_true", help="Create one merged PDF per immediate subfolder")
    parser.add_argument("--output-root", type=Path, help="Directory for split-subfolders outputs; default keeps each output inside its subfolder")
    parser.add_argument("--image-rotate", type=int, choices=[0, 90, 180, 270], default=90, help="Rotate image attachments before fitting A5 slots")
    parser.add_argument("--no-auto-install", action="store_true", help="Disable automatic dependency installation")
    parser.add_argument("--force-invoice", action="append", default=[], help="Path/name fragment to classify as invoice")
    parser.add_argument("--force-normal", action="append", default=[], help="Path/name fragment to classify as normal")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite output/report when present")
    parser.add_argument("--dry-run", action="store_true", help="Only classify files and write report")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.folder.expanduser().resolve()
    if not root.is_dir():
        print(f"ERROR: folder does not exist: {root}", file=sys.stderr)
        return 2

    if args.split_subfolders:
        if args.output or args.report or args.render_check:
            print("ERROR: with --split-subfolders, use --output-root or per-subfolder defaults instead of --output/--report/--render-check", file=sys.stderr)
            return 2
        output_root = args.output_root.expanduser().resolve() if args.output_root else None
        subfolders = [
            path
            for path in sorted(root.iterdir(), key=lambda p: natural_key(p.name))
            if path.is_dir() and not any(marker in path.name for marker in GENERATED_MARKERS) and folder_has_supported_inputs(path)
        ]
        if not subfolders:
            print(f"ERROR: no immediate subfolders with supported inputs under {root}", file=sys.stderr)
            return 2
        results = []
        for subfolder in subfolders:
            if output_root:
                target_dir = output_root / subfolder.name
                output = target_dir / f"{subfolder.name}PDF合并结果.pdf"
                report_path = target_dir / f"{subfolder.name}PDF合并报告.json"
                render_check_dir = target_dir / "合并检查缩略图"
            else:
                output = default_output_for(subfolder)
                report_path = default_report_for(subfolder)
                render_check_dir = default_render_check_for(subfolder)
            results.append(process_folder(subfolder, output, report_path, render_check_dir, args))
        return 0 if all(results) else 1

    output = (args.output or default_output_for(root)).expanduser().resolve()
    report_path = (args.report or default_report_for(root)).expanduser().resolve()
    render_check_dir = args.render_check.expanduser().resolve() if args.render_check else default_render_check_for(root).resolve()
    ok = process_folder(root, output, report_path, render_check_dir, args)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
