#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
markitdown-file-converter: Convert Word/PDF/Excel/PPT/Image to Markdown or JSON.

Modules:
- backends: pandoc, markitdown, mammoth
- ocr: RapidOCR + pix2tex (dual engine)
- utils: dependency detection, images, tables
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Add scripts dir to path
sys.path.insert(0, str(Path(__file__).parent))

from backends.pandoc import convert_with_pandoc, install_pandoc
from backends.markitdown import convert_with_markitdown
from backends.mammoth import convert_with_mammoth
from utils.deps import is_pandoc, is_markitdown_class, is_markitdown_cli, is_mammoth


# === Backend configuration ===

BACKEND_SUPPORT = {
    "pandoc": {
        # Word
        ".docx", ".doc", ".rtf", ".odt",
        # PPT
        ".pptx", ".ppt", ".odp",
        # PDF & Ebook
        ".pdf", ".epub", ".mobi",
        # Text
        ".html", ".htm", ".xml",
    },
    "markitdown": {
        # PDF
        ".pdf",
        # Word
        ".docx", ".doc",
        # Excel
        ".xlsx", ".xls", ".xlsm", ".ods", ".csv",
        # PPT
        ".pptx", ".ppt", ".odp",
        # Images (OCR)
        ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".tiff", ".tif",
        # Audio (transcription)
        ".wav", ".mp3", ".m4a", ".flac", ".ogg",
        # Text & Data
        ".html", ".htm", ".json", ".xml", ".zip",
        # Markdown
        ".md", ".markdown", ".txt",
    },
    "mammoth": {".docx", ".doc"},
}
BACKEND_PRIORITY = ["pandoc", "markitdown", "mammoth"]

# All supported extensions (union)
ALL_SUPPORTED = {ext for exts in BACKEND_SUPPORT.values() for ext in exts}


def select_backend(suffix: str, requested: str) -> str:
    """Select best available backend for the file type."""
    if requested != "auto":
        return requested
    
    checks = {
        "pandoc": is_pandoc,
        "markitdown": lambda: is_markitdown_class() or is_markitdown_cli(),
        "mammoth": is_mammoth,
    }
    installs = {
        "pandoc": install_pandoc,
        "markitdown": lambda: None,  # Will be auto-installed by markitdown backend
        "mammoth": lambda: None,
    }
    
    for b in BACKEND_PRIORITY:
        if suffix in BACKEND_SUPPORT[b]:
            if checks[b]():
                return b
    
    for b in BACKEND_PRIORITY:
        if suffix in BACKEND_SUPPORT[b]:
            if installs[b]:
                installs[b]()
            return b
    
    return "markitdown"


# === Backend configuration ===

def md_to_json(md_text: str, source_name: str) -> dict:
    """Convert Markdown to structured JSON."""
    sections = []
    current = {"heading": None, "level": 0, "content": []}
    
    for line in md_text.splitlines():
        m = re.match(r"^(#{1,6})\s+(.*)", line)
        if m:
            if current["content"] or current["heading"]:
                sections.append(current)
            current = {
                "heading": m.group(2).strip(),
                "level": len(m.group(1)),
                "content": [],
            }
        else:
            current["content"].append(line)
    
    if current["content"] or current["heading"]:
        sections.append(current)
    
    for s in sections:
        while s["content"] and not s["content"][-1].strip():
            s["content"].pop()
        s["content"] = "\n".join(s["content"])
    
    return {"source": source_name, "sections": sections}


# === Backend configuration ===

def convert_file(
    input_path: Path,
    out_dir: Path,
    fmt: str = "md",
    backend: str = "auto",
    verbose: bool = False,
    timeout: int = 120
) -> Path:
    """Convert a single file."""
    suffix = input_path.suffix.lower()
    all_exts = ALL_SUPPORTED
    
    if suffix not in all_exts:
        print(f"[skip] Unsupported format: {input_path.name}")
        return None
    
    out_dir.mkdir(parents=True, exist_ok=True)
    md_path = out_dir / f"{input_path.stem}.md"
    images_dir = out_dir / "images"
    chosen = select_backend(suffix, backend)
    
    print(f"[converter] Backend: {chosen}  |  File: {input_path.name}")
    
    try:
        if chosen == "pandoc":
            convert_with_pandoc(input_path, md_path, images_dir, verbose, timeout)
        elif chosen == "markitdown":
            convert_with_markitdown(input_path, md_path, images_dir, verbose, timeout)
        elif chosen == "mammoth":
            convert_with_mammoth(input_path, md_path, images_dir, verbose)
    except Exception as e:
        print(f"[converter] {chosen} failed: {e}")
        _try_next_backend(input_path, md_path, images_dir, suffix, after=chosen, verbose=verbose, timeout=timeout)
    
    if fmt == "json":
        text = md_path.read_text(encoding="utf-8")
        data = md_to_json(text, input_path.name)
        json_path = out_dir / f"{input_path.stem}.json"
        json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[json]   {input_path.name} -> {json_path}")
        return json_path
    
    return md_path


def _try_next_backend(input_path, output_path, images_dir, suffix, after, verbose=False, timeout=120):
    """Try next available backend."""
    rem = ["pandoc", "markitdown", "mammoth"]
    try_idx = rem.index(after) + 1
    
    for backend in rem[try_idx:]:
        if suffix not in BACKEND_SUPPORT[backend]:
            continue
        print(f"[converter] Trying: {backend} ...")
        try:
            if backend == "pandoc":
                convert_with_pandoc(input_path, output_path, images_dir, verbose, timeout)
            elif backend == "markitdown":
                convert_with_markitdown(input_path, output_path, images_dir, verbose, timeout)
            elif backend == "mammoth":
                convert_with_mammoth(input_path, output_path, images_dir, verbose)
            print(f"[converter] {backend} succeeded!")
            return
        except Exception as e2:
            print(f"[{backend}] Failed: {e2}")
    
    print("[converter] All backends exhausted.")


def batch_convert(input_dir: Path, out_dir: Path, fmt: str, backend: str, verbose=False, timeout=120):
    """Batch convert all files in a directory."""
    all_exts = ALL_SUPPORTED
    files = [f for f in input_dir.iterdir() if f.is_file() and f.suffix.lower() in all_exts]
    
    if not files:
        print(f"[batch] No supported files in: {input_dir}")
        return
    
    total = len(files)
    print(f"[batch] Found {total} file(s) in {input_dir}")
    
    for i, f in enumerate(files, 1):
        if verbose:
            print(f"\n[batch] [{i}/{total}] Processing: {f.name}")
        try:
            convert_file(f, out_dir / f.stem, fmt=fmt, backend=backend, verbose=verbose, timeout=timeout)
        except Exception as e:
            print(f"[batch] FAILED {f.name}: {e}")



def check_dependencies():
    """Check if all dependencies are available."""
    print("=== Dependency Check ===")
    issues = []
    
    # Check pandoc
    if not is_pandoc():
        issues.append("pandoc - NOT FOUND")
        print("  pandoc: MISSING (run --install to fix)")
    else:
        print("  pandoc: OK")
    
    # Check markitdown
    if not is_markitdown_class() and not is_markitdown_cli():
        issues.append("markitdown - NOT FOUND")
        print("  markitdown: MISSING (run --install to fix)")
    else:
        print("  markitdown: OK")
    
    # Check mammoth
    if not is_mammoth():
        issues.append("mammoth - NOT FOUND")
        print("  mammoth: MISSING (run --install to fix)")
    else:
        print("  mammoth: OK")
    
    # Check OCR deps
    try:
        from ocr import rapidocr
        print("  RapidOCR: OK")
    except ImportError:
        issues.append("RapidOCR - NOT FOUND")
        print("  RapidOCR: MISSING (pip install rapidocr-onnxruntime)")
    
    if issues:
        print("\nRun `python main.py --install` to install missing dependencies")
        return False
    print("\nAll dependencies OK!")
    return True


def install_all():
    """Install all backend dependencies."""
    print("\n[setup] Installing all backends ...")
    install_pandoc()
    print("[setup] All backends ready\n")

def main():
    p = argparse.ArgumentParser(
        description="Convert PDF/DOCX/XLSX/PPT/Image -> Markdown or JSON",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Backends (priority order):
  pandoc     - Best for DOCX/Emoji/Formulas
  markitdown - Word/Excel/PPT/PDF/Image OCR
  mammoth    - DOCX plain text fallback

OCR Engine: RapidOCR + pix2tex (dual engine)

Examples:
  python main.py report.pdf                          # auto-select best backend
  python main.py data.xlsx -f json                   # Excel -> JSON
  python main.py ./docs --batch -b pandoc            # batch with pandoc
  python main.py scan.png -b markitdown              # OCR + Markdown
  python main.py scanned.pdf -b markitdown -v        # PDF OCR with verbose output
  python main.py large.docx --timeout 300            # 5-minute timeout
  python main.py --install                            # pre-install all backends
  python main.py --check                             # check dependencies
        """,
    )
    p.add_argument("input", nargs="?", help="Input file or directory (with --batch)")
    p.add_argument("-f", "--format", choices=["md", "json"], default="md")
    p.add_argument("-o", "--output", help="Output directory")
    p.add_argument("-b", "--backend", choices=["pandoc", "markitdown", "mammoth", "auto"], default="auto")
    p.add_argument("--batch", action="store_true", help="Batch convert directory")
    p.add_argument("--check", action="store_true", help="Check dependencies")
    p.add_argument("--install", action="store_true", help="Pre-install all backends")
    p.add_argument("-v", "--verbose", action="store_true", help="Show detailed progress")
    p.add_argument("--timeout", type=int, default=120, help="Timeout in seconds (default: 120)")
    args = p.parse_args()
    
    if args.check:
        check_dependencies()
        return
    
    if args.install:
        install_all()
        return
    
    if not args.input:
        p.print_help()
        return
    
    ip = Path(args.input).resolve()
    
    if args.batch:
        if not ip.is_dir():
            print("[error] --batch requires a directory")
            sys.exit(1)
        od = Path(args.output).resolve() if args.output else ip / "converted"
        batch_convert(ip, od, args.format, args.backend, verbose=args.verbose, timeout=args.timeout)
    else:
        if not ip.is_file():
            print(f"[error] File not found: {ip}")
            sys.exit(1)
        od = Path(args.output).resolve() if args.output else ip.parent / f"{ip.stem}_converted"
        convert_file(ip, od, fmt=args.format, backend=args.backend, verbose=args.verbose, timeout=args.timeout)


if __name__ == "__main__":
    main()
