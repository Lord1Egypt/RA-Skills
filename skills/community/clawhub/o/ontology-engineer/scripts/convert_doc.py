#!/usr/bin/env python3
"""
convert_doc.py - Batch convert .doc files to .docx format.

Windows: Uses win32com COM automation (requires pywin32 + Microsoft Word installed).
Linux:   Uses LibreOffice headless mode (requires libreoffice installed).

Usage:
    python convert_doc.py <input_dir_or_file> [--output-dir <dir>] [--max-files 100]

Examples:
    # Convert all .doc files in a directory
    python convert_doc.py /path/to/project --output-dir /path/to/converted

    # Convert a single file
    python convert_doc.py /path/to/file.doc

    # Convert only the first 50 .doc files (sorted by priority)
    python convert_doc.py /path/to/project --max-files 50
"""

import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path


def convert_doc_to_docx_win32com(doc_path: Path, output_path: Path) -> bool:
    """Convert .doc to .docx using win32com (Windows only)."""
    import win32com.client
    import pythoncom

    pythoncom.CoInitialize()
    word = None
    doc = None
    try:
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        word.DisplayAlerts = False

        doc = word.Documents.Open(str(doc_path.resolve()))
        # wdFormatXMLDocument = 12
        doc.SaveAs2(str(output_path.resolve()), FileFormat=12)
        doc.Close(False)
        return True
    except Exception as e:
        print(f"  ERROR converting {doc_path.name}: {e}", file=sys.stderr)
        return False
    finally:
        if doc:
            try:
                doc.Close(False)
            except Exception:
                pass
        if word:
            try:
                word.Quit()
            except Exception:
                pass
        pythoncom.CoUninitialize()


def convert_doc_to_docx_libreoffice(doc_path: Path, output_dir: Path) -> bool:
    """Convert .doc to .docx using LibreOffice headless (Linux/macOS)."""
    lo_cmd = shutil.which("libreoffice") or shutil.which("soffice")
    if not lo_cmd:
        print("ERROR: LibreOffice not found. Install with: sudo apt install libreoffice", file=sys.stderr)
        return False

    try:
        result = subprocess.run(
            [lo_cmd, "--headless", "--convert-to", "docx", "--outdir", str(output_dir), str(doc_path)],
            capture_output=True,
            text=True,
            timeout=120,
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"  TIMEOUT converting {doc_path.name}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"  ERROR converting {doc_path.name}: {e}", file=sys.stderr)
        return False


def convert_doc_to_docx(doc_path: Path, output_dir: Path) -> bool:
    """
    Cross-platform .doc → .docx conversion.
    Automatically selects win32com (Windows) or LibreOffice (Linux/macOS).
    """
    output_path = output_dir / (doc_path.stem + ".docx")

    if output_path.exists():
        return True  # Already converted

    if sys.platform == "win32":
        return convert_doc_to_docx_win32com(doc_path, output_path)
    else:
        return convert_doc_to_docx_libreoffice(doc_path, output_dir)


def batch_convert(
    input_path: Path,
    output_dir: Path,
    max_files: int = 0,
    scan_result_path: Path | None = None,
) -> dict:
    """
    Batch convert .doc files to .docx.

    Args:
        input_path: A single .doc file or a directory to scan.
        output_dir: Directory to write .docx output files.
        max_files: Max number of files to convert (0 = all).
        scan_result_path: Optional path to scan_result.json for priority ordering.

    Returns:
        Conversion report dict.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # Collect .doc files
    if input_path.is_file() and input_path.suffix.lower() == ".doc":
        doc_files = [input_path]
    elif input_path.is_dir():
        doc_files = sorted(input_path.rglob("*.doc"))
        # Exclude already-.docx files that happen to match (case sensitivity)
        doc_files = [f for f in doc_files if f.suffix.lower() == ".doc"]
    else:
        print(f"Error: '{input_path}' is not a .doc file or directory", file=sys.stderr)
        return {"success": 0, "failed": 0, "skipped": 0, "files": []}

    # If scan result available, sort by priority
    if scan_result_path and scan_result_path.exists():
        with open(scan_result_path, "r", encoding="utf-8") as f:
            scan_data = json.load(f)
        priority_map = {}
        for entry in scan_data.get("files", []):
            priority_map[entry["path"]] = entry["priority"]

        def sort_key(p):
            return priority_map.get(str(p), "P7")

        doc_files.sort(key=sort_key)

    # Apply max_files limit
    if max_files > 0:
        doc_files = doc_files[:max_files]

    total = len(doc_files)
    if total == 0:
        print("No .doc files found.")
        return {"success": 0, "failed": 0, "skipped": 0, "files": []}

    print(f"Converting {total} .doc files to .docx...")
    if sys.platform == "win32":
        print("Backend: win32com (Microsoft Word)")
    else:
        print("Backend: LibreOffice headless")

    success = 0
    failed = 0
    skipped = 0
    results = []
    start_time = time.time()

    for i, doc_path in enumerate(doc_files, 1):
        output_path = output_dir / (doc_path.stem + ".docx")

        if output_path.exists():
            skipped += 1
            results.append({"source": str(doc_path), "output": str(output_path), "status": "skipped"})
            continue

        print(f"  [{i}/{total}] {doc_path.name}...", end=" ", flush=True)

        ok = convert_doc_to_docx(doc_path, output_dir)
        if ok:
            success += 1
            print("OK")
            results.append({"source": str(doc_path), "output": str(output_path), "status": "success"})
        else:
            failed += 1
            print("FAILED")
            results.append({"source": str(doc_path), "output": str(output_path), "status": "failed"})

    elapsed = time.time() - start_time
    report = {
        "success": success,
        "failed": failed,
        "skipped": skipped,
        "total": total,
        "elapsed_seconds": round(elapsed, 1),
        "output_dir": str(output_dir),
        "files": results,
    }

    print(f"\nDone in {elapsed:.1f}s: {success} converted, {failed} failed, {skipped} skipped")
    return report


def main():
    parser = argparse.ArgumentParser(description="Batch convert .doc to .docx")
    parser.add_argument("input", help="Input .doc file or directory")
    parser.add_argument("--output-dir", "-o", default=None, help="Output directory for .docx files")
    parser.add_argument("--max-files", "-n", type=int, default=0, help="Max files to convert (0=all)")
    parser.add_argument("--scan-result", default=None, help="Path to scan_result.json for priority ordering")
    parser.add_argument("--report", default=None, help="Save conversion report to JSON file")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: '{input_path}' does not exist", file=sys.stderr)
        sys.exit(1)

    # Default output dir: <input>_converted or same dir as input file
    if args.output_dir:
        output_dir = Path(args.output_dir)
    elif input_path.is_dir():
        output_dir = input_path / "_converted_docx"
    else:
        output_dir = input_path.parent

    scan_result = Path(args.scan_result) if args.scan_result else None

    report = batch_convert(input_path, output_dir, args.max_files, scan_result)

    if args.report:
        with open(args.report, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"Report saved to: {args.report}")


if __name__ == "__main__":
    main()
