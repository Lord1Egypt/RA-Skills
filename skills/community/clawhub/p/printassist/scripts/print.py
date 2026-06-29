"""
Print dispatcher for PDF, Office, and image files.
Supports SumatraPDF for PDF/Office (via LibreOffice conversion) and win32print for images.

Natural language triggers that route here:
  "drucke", "print", "ausdruck", "drucken", "auf Drucker", "print to", "als Kopie", "Seiten drucken"
"""

import argparse
import os
import shutil
import socket
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

import yaml

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SUMATRA_SEARCH_PATHS = [
    r"C:\Program Files\SumatraPDF\SumatraPDF.exe",
    r"C:\Program Files (x86)\SumatraPDF\SumatraPDF.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\SumatraPDF\SumatraPDF.exe"),
    shutil.which("SumatraPDF") or "",
]

LIBREOFFICE_SEARCH_PATHS = [
    r"C:\Program Files\LibreOffice\program\soffice.exe",
    r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
    shutil.which("soffice") or "",
]

OFFICE_EXTENSIONS = {".docx", ".doc", ".xlsx", ".xls", ".pptx", ".ppt", ".odt", ".ods", ".odp"}
PDF_EXTENSIONS = {".pdf"}
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif", ".gif", ".webp"}

CONFIG_PATH = Path(__file__).parent.parent / "config" / "printers.yaml"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def find_executable(search_paths: list[str]) -> str | None:
    for p in search_paths:
        if p and Path(p).is_file():
            return p
    return None


def load_printer_config() -> dict[str, Any]:
    if not CONFIG_PATH.exists():
        example = CONFIG_PATH.parent / "printers.example.yaml"
        raise FileNotFoundError(
            f"Printer config not found: {CONFIG_PATH}\n"
            f"Run setup.ps1 to generate it automatically, or copy "
            f"{example} to {CONFIG_PATH} and fill in your printer name.\n"
            f"List available printers with: wmic printer get name"
        )
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f)


def resolve_printer(printer_override: str | None = None) -> str:
    """Return the printer name for this machine, or use the override."""
    if printer_override:
        return printer_override

    cfg = load_printer_config()
    hostname = socket.gethostname()

    hosts = cfg.get("hosts", {})
    if hostname in hosts:
        return hosts[hostname]["printer_name"]

    default = cfg.get("default", {}).get("printer_name")
    if not default or default.startswith("<"):
        raise ValueError(
            f"Kein Drucker für Hostname '{hostname}' konfiguriert und kein gültiger Standarddrucker "
            f"in {CONFIG_PATH}. Bitte echte Druckernamen eintragen (siehe README in CLAUDE.md)."
        )
    return default


def build_sumatra_print_settings(params: dict[str, Any]) -> str:
    """
    Build the -print-settings string for SumatraPDF from a parameter dict.

    Supported keys:
      paper        (str)  e.g. "A4", "Letter"
      orientation  (str)  "portrait" | "landscape"
      duplex       (str)  "duplex" | "duplexshort" | "simplex"
      color        (str)  "color" | "monochrome"
      scale        (str)  "fit" | "shrink" | "noscale"
      pages        (str)  e.g. "1-3,5" (SumatraPDF range syntax)
      copies       (int)  number of copies
    """
    parts: list[str] = []

    if params.get("paper"):
        parts.append(params["paper"])

    orientation = params.get("orientation", "").lower()
    if orientation == "landscape":
        parts.append("landscape")
    elif orientation == "portrait":
        parts.append("portrait")

    duplex = params.get("duplex", "").lower()
    if duplex in ("duplex", "duplexshort", "simplex"):
        parts.append(duplex)

    color = params.get("color", "").lower()
    if color == "monochrome":
        parts.append("monochrome")
    elif color == "color":
        parts.append("color")

    scale = params.get("scale", "").lower()
    if scale in ("fit", "shrink", "noscale"):
        parts.append(scale)

    pages = params.get("pages", "")
    if pages:
        parts.append(pages)

    copies = params.get("copies", 1)
    if copies and int(copies) > 1:
        parts.append(f"{copies}x")

    return ",".join(parts) if parts else ""


def convert_office_to_pdf(office_path: Path, output_dir: Path) -> Path:
    """Convert an Office file to PDF using LibreOffice headless."""
    soffice = find_executable(LIBREOFFICE_SEARCH_PATHS)
    if not soffice:
        raise FileNotFoundError(
            "LibreOffice nicht gefunden. Bitte installieren: https://www.libreoffice.org"
        )

    cmd = [
        soffice,
        "--headless",
        "--convert-to", "pdf",
        "--outdir", str(output_dir),
        str(office_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"LibreOffice Konvertierung fehlgeschlagen:\n{result.stderr}")

    pdf_name = office_path.stem + ".pdf"
    pdf_path = output_dir / pdf_name
    if not pdf_path.exists():
        raise FileNotFoundError(f"Konvertierte PDF nicht gefunden: {pdf_path}")
    return pdf_path


def print_pdf_with_sumatra(pdf_path: Path, printer: str, settings: str) -> None:
    sumatra = find_executable(SUMATRA_SEARCH_PATHS)
    if not sumatra:
        raise FileNotFoundError(
            "SumatraPDF nicht gefunden. Bitte installieren: https://www.sumatrapdfreader.org"
        )

    cmd = [sumatra, "-print-to", printer]
    if settings:
        cmd += ["-print-settings", settings]
    cmd.append(str(pdf_path))

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"SumatraPDF Druckfehler:\n{result.stderr}")


def print_image_with_win32(image_path: Path, printer: str, params: dict[str, Any]) -> None:
    """Scale image to target paper size and print via win32print."""
    try:
        import win32print
        import win32ui
        from PIL import Image
    except ImportError:
        raise ImportError(
            "Für Bilddruck werden 'pywin32' und 'Pillow' benötigt. "
            "Installiere sie mit: pip install pywin32 Pillow"
        )

    paper_sizes = {
        "A4": (794, 1123),
        "A3": (1123, 1587),
        "Letter": (816, 1056),
        "Legal": (816, 1344),
    }
    paper = params.get("paper", "A4")
    target_w, target_h = paper_sizes.get(paper, (794, 1123))

    orientation = params.get("orientation", "portrait").lower()
    if orientation == "landscape":
        target_w, target_h = target_h, target_w

    img = Image.open(image_path)
    img.thumbnail((target_w, target_h), Image.LANCZOS)

    hprinter = win32print.OpenPrinter(printer)
    try:
        hdc = win32ui.CreateDC()
        hdc.CreatePrinterDC(printer)
        hdc.StartDoc(str(image_path))
        copies = int(params.get("copies", 1))
        for _ in range(copies):
            hdc.StartPage()
            dib = img.convert("RGB")
            hdc.StretchDIBits(
                (0, 0, target_w, target_h),
                (0, 0, dib.width, dib.height),
                dib.tobytes("raw", "BGRX"),
            )
            hdc.EndPage()
        hdc.EndDoc()
    finally:
        win32print.ClosePrinter(hprinter)


# ---------------------------------------------------------------------------
# Main dispatcher
# ---------------------------------------------------------------------------

def print_file(
    file_path: str | Path,
    printer: str | None = None,
    params: dict[str, Any] | None = None,
) -> str:
    """
    Print any supported file (PDF, Office, Image).

    Args:
        file_path: Path to the file to print.
        printer:   Printer name override. If None, resolved from printers.yaml.
        params:    Dict with optional keys: paper, orientation, duplex, color,
                   scale, pages, copies.

    Returns:
        A short status message.
    """
    params = params or {}
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Datei nicht gefunden: {path}")

    printer_name = resolve_printer(printer)
    ext = path.suffix.lower()

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)

        if ext in PDF_EXTENSIONS:
            settings = build_sumatra_print_settings(params)
            print_pdf_with_sumatra(path, printer_name, settings)

        elif ext in OFFICE_EXTENSIONS:
            pdf = convert_office_to_pdf(path, tmp)
            settings = build_sumatra_print_settings(params)
            print_pdf_with_sumatra(pdf, printer_name, settings)

        elif ext in IMAGE_EXTENSIONS:
            print_image_with_win32(path, printer_name, params)

        else:
            raise ValueError(
                f"Nicht unterstützter Dateityp: '{ext}'. "
                f"Unterstützt: PDF, {', '.join(sorted(OFFICE_EXTENSIONS | IMAGE_EXTENSIONS))}"
            )

    return f"Gedruckt: {path.name} -> {printer_name}"


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Datei drucken (PDF, Office, Bild) via SumatraPDF / win32print."
    )
    parser.add_argument("file", help="Pfad zur Druckdatei")
    parser.add_argument("--printer", "-p", help="Druckername (überschreibt printers.yaml)")
    parser.add_argument("--paper", default="", help="Papierformat, z.B. A4, Letter")
    parser.add_argument("--orientation", default="", choices=["portrait", "landscape", ""],
                        help="Ausrichtung")
    parser.add_argument("--duplex", default="", choices=["duplex", "duplexshort", "simplex", ""],
                        help="Duplex-Modus")
    parser.add_argument("--color", default="", choices=["color", "monochrome", ""],
                        help="Farb- oder Schwarzweißdruck")
    parser.add_argument("--scale", default="", choices=["fit", "shrink", "noscale", ""],
                        help="Skalierung")
    parser.add_argument("--pages", default="", help="Seitenbereich, z.B. '1-3,5'")
    parser.add_argument("--copies", type=int, default=1, help="Anzahl Kopien")

    args = parser.parse_args()

    params = {
        "paper": args.paper,
        "orientation": args.orientation,
        "duplex": args.duplex,
        "color": args.color,
        "scale": args.scale,
        "pages": args.pages,
        "copies": args.copies,
    }

    try:
        msg = print_file(args.file, printer=args.printer, params=params)
        print(msg)
    except Exception as e:
        print(f"Fehler: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
