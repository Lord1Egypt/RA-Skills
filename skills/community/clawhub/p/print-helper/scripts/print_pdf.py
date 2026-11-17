"""Print helper for PDFs with silent printing support."""
import argparse
import os
import sys
import subprocess
import shutil
import time


def find_sumatra():
    """Find SumatraPDF executable."""
    candidates = [
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "SumatraPDF", "SumatraPDF.exe"),
        os.path.join(os.environ.get("PROGRAMFILES", ""), "SumatraPDF", "SumatraPDF.exe"),
        os.path.join(os.environ.get("PROGRAMFILES(X86)", ""), "SumatraPDF", "SumatraPDF.exe"),
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return shutil.which("SumatraPDF.exe") or shutil.which("SumatraPDF")


def print_pdf_silent(filepath, pages=None, printer=None):
    """Silent print PDF using SumatraPDF."""
    sumatra = find_sumatra()
    if not sumatra:
        return False, "SumatraPDF not found. Install from https://www.sumatrapdfreader.org/ for silent printing."

    cmd = [sumatra, "-print-to-default"]
    if printer:
        cmd = [sumatra, "-print-to", printer]
    if pages:
        cmd.extend(["-print-settings", f"pages={pages}"])
    cmd.append(filepath)

    try:
        subprocess.run(cmd, check=True, capture_output=True, timeout=120)
        return True, f"Sent to printer: {filepath} (pages={pages or 'all'})"
    except subprocess.TimeoutExpired:
        return False, "Print timeout"
    except subprocess.CalledProcessError as e:
        return False, f"Print error: {e}"


def print_duplex(filepath, flip_seconds=30, total_pages=None):
    """Print manual duplex: odd pages -> wait -> even pages."""
    if total_pages is None:
        import fitz
        doc = fitz.open(filepath)
        total_pages = len(doc)
        doc.close()

    odd = ",".join(str(i) for i in range(1, total_pages + 1, 2))
    even = ",".join(str(i) for i in range(2, total_pages + 1, 2))

    results = []
    ok, msg = print_pdf_silent(filepath, pages=odd)
    results.append(f"奇数页: {msg}")
    if not ok:
        return results

    results.append(f"等待 {flip_seconds} 秒后打印偶数页，请现在翻面...")
    time.sleep(flip_seconds)

    ok, msg = print_pdf_silent(filepath, pages=even)
    results.append(f"偶数页: {msg}")
    return results


def main():
    parser = argparse.ArgumentParser(description="Print PDF with options")
    parser.add_argument("--file", required=True, help="PDF file path")
    parser.add_argument("--printer", help="Printer name")
    parser.add_argument("--duplex", action="store_true", help="Manual duplex: odd then even")
    parser.add_argument("--pages", help="Page range, e.g. 1-3,5")
    parser.add_argument("--copies", type=int, default=1, help="Number of copies")
    parser.add_argument("--flip-seconds", type=int, default=30, help="Seconds to wait between odd/even pages")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"File not found: {args.file}")
        sys.exit(1)

    if args.duplex:
        results = print_duplex(args.file, flip_seconds=args.flip_seconds)
        for r in results:
            print(r)
    else:
        ok, msg = print_pdf_silent(args.file, pages=args.pages, printer=args.printer)
        print(msg)
        if not ok:
            sys.exit(1)


if __name__ == "__main__":
    main()
