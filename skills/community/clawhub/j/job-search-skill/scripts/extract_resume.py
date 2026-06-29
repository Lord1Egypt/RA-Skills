#!/usr/bin/env python3
"""
extract_resume.py
Extracts plain text from workspace/resume.pdf and prints it to stdout.
The OpenClaw agent reads this output and uses it for job scoring and cover letters.
No LLM calls are made here — text extraction only.
"""

from pathlib import Path
import sys

RESUME_PATH = Path(__file__).parent.parent / "workspace" / "resume.pdf"

def extract(pdf_path: Path) -> str:
    if not pdf_path.exists():
        print(
            f"ERROR: Resume PDF not found at {pdf_path}\n"
            "Place your CV as workspace/resume.pdf and try again.",
            file=sys.stderr
        )
        sys.exit(1)

    text = ""

    # Attempt 1: pypdf
    try:
        from pypdf import PdfReader
        reader = PdfReader(str(pdf_path))
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
        if text.strip():
            return text.strip()
    except ImportError:
        pass
    except Exception as e:
        print(f"[pypdf] failed: {e}", file=sys.stderr)

    # Attempt 2: pdfplumber
    try:
        import pdfplumber
        with pdfplumber.open(str(pdf_path)) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"
        if text.strip():
            return text.strip()
    except ImportError:
        pass
    except Exception as e:
        print(f"[pdfplumber] failed: {e}", file=sys.stderr)

    # Attempt 3: pdftotext CLI
    try:
        import subprocess
        result = subprocess.run(
            ["pdftotext", "-layout", str(pdf_path), "-"],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except Exception as e:
        print(f"[pdftotext] failed: {e}", file=sys.stderr)

    print(
        "ERROR: Could not extract text from resume.pdf.\n"
        "Fix: pip install pypdf",
        file=sys.stderr
    )
    sys.exit(1)

if __name__ == "__main__":
    print(extract(RESUME_PATH))
