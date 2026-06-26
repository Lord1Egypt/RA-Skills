#!/usr/bin/env python3
"""converter.py - Convert documents to Markdown.

Supported formats: .docx (via pandoc), .pdf (via pdftotext), .txt, .md
Usage: python3 scripts/converter.py <input_file> <output_md_path>
"""

import os
import shutil
import subprocess
import sys


def detect_format(path):
    ext = os.path.splitext(path)[1].lower()
    return ext


def convert_docx(input_path, output_path):
    """Convert .docx to markdown via pandoc."""
    if not shutil.which("pandoc"):
        print("ERROR: pandoc is not installed. Install with: brew install pandoc")
        sys.exit(1)
    result = subprocess.run(
        ["pandoc", "-f", "docx", "-t", "markdown", "--wrap=none", "-o", output_path, input_path],
        capture_output=True, text=True,
    )
    warnings = []
    if result.returncode != 0:
        msg = result.stderr.strip()
        print(f"WARNING: pandoc returned non-zero exit code: {msg}")
        warnings.append(f"pandoc warning: {msg}")
    elif result.stderr.strip():
        warnings.append(f"pandoc note: {result.stderr.strip()}")
    return warnings


def convert_pdf(input_path, output_path):
    """Convert .pdf to markdown via pdftotext."""
    warnings = []
    if shutil.which("pdftotext"):
        result = subprocess.run(
            ["pdftotext", "-layout", input_path, "-"],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            msg = result.stderr.strip()
            print(f"WARNING: pdftotext failed: {msg}")
            warnings.append(f"pdftotext error: {msg}")
            # fallback to raw read
            warnings.append("Falling back to raw binary text extraction")
            text = _extract_pdf_raw(input_path)
        else:
            text = result.stdout
            if result.stderr.strip():
                warnings.append(f"pdftotext note: {result.stderr.strip()}")
    else:
        print("WARNING: pdftotext not found. Install with: brew install poppler")
        print("Attempting basic text extraction...")
        warnings.append("pdftotext not available, used basic extraction")
        text = _extract_pdf_raw(input_path)

    # Check if we got meaningful text
    stripped = text.strip()
    if not stripped:
        warnings.append("PDF appears to be a scanned image or contains no extractable text")
        text = "<!-- WARNING: No text could be extracted from this PDF. It may be a scanned document. -->\n"
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    return warnings


def _extract_pdf_raw(input_path):
    """Last-resort: try to pull readable strings from a PDF."""
    try:
        with open(input_path, "rb") as f:
            data = f.read()
        # Attempt to decode readable text segments
        segments = []
        for chunk in data.split(b"("):
            idx = chunk.find(b")")
            if 0 < idx < 500:
                try:
                    segments.append(chunk[:idx].decode("utf-8", errors="ignore"))
                except Exception:
                    pass
        return "\n".join(s for s in segments if len(s.strip()) > 2)
    except Exception:
        return ""


def convert_txt(input_path, output_path):
    """Read .txt file directly."""
    warnings = []
    # Try common encodings
    text = None
    for enc in ("utf-8", "utf-8-sig", "gbk", "gb2312", "latin-1"):
        try:
            with open(input_path, "r", encoding=enc) as f:
                text = f.read()
            break
        except (UnicodeDecodeError, UnicodeError):
            continue
    if text is None:
        with open(input_path, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
        warnings.append("Encoding detection failed, used utf-8 with replacements")
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    return warnings


def convert_md(input_path, output_path):
    """Copy .md as-is."""
    if os.path.abspath(input_path) != os.path.abspath(output_path):
        shutil.copy2(input_path, output_path)
    return []


def convert(input_path, output_path):
    """Main conversion dispatcher. Returns list of warning strings."""
    if not os.path.exists(input_path):
        print(f"ERROR: Input file not found: {input_path}")
        sys.exit(1)
    
    file_size = os.path.getsize(input_path)
    if file_size == 0:
        print("WARNING: Input file is empty")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("<!-- Empty source document -->\n")
        return ["Input file is empty (0 bytes)"]

    fmt = detect_format(input_path)
    print(f"[converter] Format: {fmt}, Size: {file_size:,} bytes")

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    converters = {
        ".docx": convert_docx,
        ".pdf": convert_pdf,
        ".txt": convert_txt,
        ".text": convert_txt,
        ".md": convert_md,
        ".markdown": convert_md,
    }

    handler = converters.get(fmt)
    if handler is None:
        print(f"ERROR: Unsupported format '{fmt}'. Supported: {', '.join(converters.keys())}")
        sys.exit(1)
    
    warnings = handler(input_path, output_path)
    
    # Verify output
    if not os.path.exists(output_path):
        print("ERROR: Conversion produced no output file")
        sys.exit(1)
    
    out_size = os.path.getsize(output_path)
    print(f"[converter] Output: {output_path} ({out_size:,} bytes)")
    if warnings:
        for w in warnings:
            print(f"[converter] WARNING: {w}")
    else:
        print("[converter] Conversion completed successfully")
    
    return warnings


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 converter.py <input_file> <output_md_path>")
        sys.exit(1)
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    convert(input_path, output_path)


if __name__ == "__main__":
    main()
