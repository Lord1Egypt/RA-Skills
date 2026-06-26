"""
pdf-to-md.py  (v2 — security-hardened)
Converts a PDF file to Markdown.
- Pass 1: text extraction via pdfplumber (always runs, no API calls)
- Pass 2: vision fallback via Claude API (only with --allow-vision flag)

Usage:
    python pdf-to-md.py <input.pdf> <output.md> [--allow-vision]

Dependencies installed to /tmp/office_md_deps/ (isolated, pinned versions).
"""

import sys, time, base64, json, urllib.request, subprocess
from pathlib import Path

# ── isolated dependency install ───────────────────────────────────────────────
# Pinned versions reviewed 2025-05-07. Install to a temp dir — system Python
# environment is NOT modified.
_DEP_DIR = Path("/tmp/office_md_deps")
_DEP_DIR.mkdir(exist_ok=True)
subprocess.run(
    [
        sys.executable, "-m", "pip", "install", "--quiet",
        "--target", str(_DEP_DIR),
        "pdfplumber==0.11.4",
        "pymupdf==1.24.14",
    ],
    check=True,
)
if str(_DEP_DIR) not in sys.path:
    sys.path.insert(0, str(_DEP_DIR))

import pdfplumber
import fitz  # pymupdf


# ── vision helper (only called when --allow-vision is set) ────────────────────
def call_vision(b64_data: str, media_type: str = "image/png") -> str:
    """Send a single page image to Claude vision API and return Markdown text."""
    payload = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 2000,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": b64_data}},
                {"type": "text", "text": (
                    "Extract ALL text and structured content from this document page image into clean Markdown.\n"
                    "Rules:\n"
                    "- Preserve headings using # / ## / ### hierarchy\n"
                    "- Preserve bullet and numbered lists\n"
                    "- Convert any visible tables to Markdown table syntax\n"
                    "- If this is a form or quiz, mark selected/checked options with ✅\n"
                    "- Output ONLY the extracted markdown — no preamble or commentary"
                )}
            ]
        }]
    }
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "anthropic-version": "2023-06-01"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())["content"][0]["text"]
    except Exception as e:
        return f"*(vision extraction failed: {e})*"


# ── render one PDF page to base64 PNG ─────────────────────────────────────────
def render_page_b64(pdf_path: str, page_index: int, dpi: int = 150) -> str:
    doc = fitz.open(pdf_path)
    page = doc[page_index]
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    pix = page.get_pixmap(matrix=mat)
    img_bytes = pix.tobytes("png")
    doc.close()
    return base64.standard_b64encode(img_bytes).decode("utf-8")


# ── table helper ──────────────────────────────────────────────────────────────
def table_to_md(table) -> str:
    if not table or not table[0]:
        return ""
    clean = lambda c: str(c or "").replace("\n", " ")
    header = "| " + " | ".join(clean(c) for c in table[0]) + " |"
    sep    = "| " + " | ".join("---" for _ in table[0]) + " |"
    rows   = ["| " + " | ".join(clean(c) for c in row) + " |" for row in table[1:]]
    return "\n".join([header, sep] + rows)


# ── main ──────────────────────────────────────────────────────────────────────
def convert(src: str, dst: str, allow_vision: bool = False):
    md_lines = []
    image_pages = []

    # Pass 1 — text extraction (always runs)
    with pdfplumber.open(src) as pdf:
        total_pages = len(pdf.pages)
        for i, page in enumerate(pdf.pages):
            text   = page.extract_text() or ""
            tables = page.extract_tables() or []
            if text.strip() or tables:
                md_lines.append(f"## Page {i + 1}\n")
                if text.strip():
                    md_lines.append(text.strip())
                for t in tables:
                    md_lines.append(table_to_md(t))
                md_lines.append("")
            else:
                image_pages.append(i)

    # Pass 2 — vision for image-only pages (only if explicitly allowed)
    if image_pages:
        if not allow_vision:
            # Signal to caller how many pages need vision — do NOT call API
            for idx in image_pages:
                md_lines.append(f"## Page {idx + 1}\n")
                md_lines.append(
                    f"*(image-only page — vision extraction skipped; "
                    f"re-run with --allow-vision to extract)*"
                )
                md_lines.append("")
            print(
                f"  VISION_REQUIRED: {len(image_pages)} image-based page(s) detected. "
                f"Re-run with --allow-vision after user confirmation."
            )
        else:
            print(f"  {len(image_pages)} image-based page(s) → vision extraction")
            if len(image_pages) == total_pages:
                md_lines = []  # fully image-based, start fresh
            for idx in image_pages:
                print(f"  [vision] page {idx + 1}/{total_pages}")
                b64 = render_page_b64(src, idx, dpi=150)
                md_lines.append(f"## Page {idx + 1}\n")
                md_lines.append(call_vision(b64))
                md_lines.append("")
                time.sleep(0.3)

    Path(dst).write_text("\n".join(md_lines), encoding="utf-8")
    print(f"  Saved → {dst}  ({total_pages} pages, {len(image_pages)} image-only)")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: pdf-to-md.py <input.pdf> <output.md> [--allow-vision]")
        sys.exit(1)
    allow_vision = "--allow-vision" in sys.argv
    convert(sys.argv[1], sys.argv[2], allow_vision=allow_vision)
