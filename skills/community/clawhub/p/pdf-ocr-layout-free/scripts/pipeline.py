#!/usr/bin/env python3
"""
PDF OCR Layout Pipeline — PaddleOCR-VL-1.5
==========================================
Split PDF → OCR API → Layout-preserving PDF → Merge

Usage:
    python pipeline.py input.pdf [--output out.pdf] [--work-dir dir] [--chunk-size 90]

Resume-safe: intermediate files are cached; re-run to continue after interruption.
"""

import argparse
import io
import json
import math
import os
import re
import sys
import time
import urllib.request

import requests
from PIL import Image
from pypdf import PdfReader, PdfWriter
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.platypus import Paragraph

# ── API config ─────────────────────────────────────────────────────────────────
API_URL = "https://paddleocr.aistudio-app.com/api/v2/ocr/jobs"
TOKEN   = os.environ.get("PADDLEOCR_TOKEN", "YOUR_PADDLEOCR_TOKEN_HERE")
MODEL   = "PaddleOCR-VL-1.5"

OPTIONAL_PAYLOAD = {
    "useDocOrientationClassify": False,
    "useDocUnwarping": False,
    "useChartRecognition": False,
}

# ── Coordinate system (OCR image → A4 PDF) ────────────────────────────────────
# PaddleOCR image size varies by document (e.g. 812×1269 or 1191×1799).
# We detect it from the data at render time; these are just fallback defaults.
PDF_W, PDF_H = A4          # 595.28 × 841.89 pt


def detect_img_size(pages: list) -> tuple:
    """
    Detect the source image dimensions by fetching the first available inputImage.
    Falls back to inferring from max bbox coordinates if the URL is unreachable.
    Called once per chunk — result is cached and reused for all pages.
    """
    # Try fetching actual image dimensions from URL
    for page in pages[:5]:
        url = page.get("inputImage", "")
        if url:
            try:
                data = urllib.request.urlopen(url, timeout=10).read()
                img = Image.open(io.BytesIO(data))
                w, h = img.size
                print(f"  Image size detected: {w}×{h}px (from inputImage)")
                return w, h
            except Exception:
                pass

    # Fallback: infer from max bbox coordinates across all blocks
    max_x, max_y = 812, 1269
    for page in pages:
        for block in page.get("prunedResult", {}).get("parsing_res_list", []):
            bbox = block["block_bbox"]
            max_x = max(max_x, bbox[2])
            max_y = max(max_y, bbox[3])
    print(f"  Image size inferred: {max_x}×{max_y}px (from bbox ranges)")
    return max_x, max_y


# ══════════════════════════════════════════════════════════════════════════════
# STEP 1 — Split PDF
# ══════════════════════════════════════════════════════════════════════════════

def split_pdf(input_path: str, work_dir: str, chunk_size: int) -> list[str]:
    """Split input PDF into ≤chunk_size page chunks. Returns list of chunk paths."""
    reader = PdfReader(input_path)
    total = len(reader.pages)
    print(f"  PDF: {total} pages → chunks of ≤{chunk_size}")

    chunks = []
    for start in range(0, total, chunk_size):
        end = min(start + chunk_size, total)
        chunk_path = os.path.join(work_dir, f"chunk_{start:04d}_{end:04d}.pdf")
        chunks.append(chunk_path)

        if os.path.exists(chunk_path):
            print(f"  [skip] chunk {start+1}–{end} already split")
            continue

        writer = PdfWriter()
        for i in range(start, end):
            writer.add_page(reader.pages[i])
        with open(chunk_path, "wb") as f:
            writer.write(f)
        print(f"  Chunk {start+1}–{end}: {chunk_path}")

    return chunks


# ══════════════════════════════════════════════════════════════════════════════
# STEP 2 — Submit to API
# ══════════════════════════════════════════════════════════════════════════════

def submit_chunk(chunk_path: str) -> str:
    """Submit a PDF chunk to the OCR API. Returns job ID."""
    headers = {"Authorization": f"bearer {TOKEN}"}
    data    = {"model": MODEL, "optionalPayload": json.dumps(OPTIONAL_PAYLOAD)}

    with open(chunk_path, "rb") as f:
        resp = requests.post(API_URL, headers=headers, data=data,
                             files={"file": f}, timeout=120)

    if resp.status_code != 200:
        raise RuntimeError(f"API error {resp.status_code}: {resp.text[:300]}")

    job_id = resp.json()["data"]["jobId"]
    print(f"  Submitted → job {job_id}")
    return job_id


# ══════════════════════════════════════════════════════════════════════════════
# STEP 3 — Poll + Download results
# ══════════════════════════════════════════════════════════════════════════════

def poll_job(job_id: str, poll_interval: int = 10) -> str:
    """Poll until the job is done. Returns JSONL download URL."""
    headers = {"Authorization": f"bearer {TOKEN}"}

    while True:
        resp = requests.get(f"{API_URL}/{job_id}", headers=headers, timeout=30)
        resp.raise_for_status()
        data  = resp.json()["data"]
        state = data["state"]

        if state == "done":
            prog = data.get("extractProgress", {})
            print(f"  Done — {prog.get('extractedPages', '?')} pages extracted")
            return data["resultUrl"]["jsonUrl"]

        if state == "failed":
            raise RuntimeError(f"Job {job_id} failed: {data.get('errorMsg', '?')}")

        # running / pending
        try:
            prog = data["extractProgress"]
            done_p = prog.get("extractedPages", 0)
            tot_p  = prog.get("totalPages", "?")
            print(f"  {state}: {done_p}/{tot_p} pages", flush=True)
        except (KeyError, TypeError):
            print(f"  {state}…", flush=True)

        time.sleep(poll_interval)


def parse_jsonl(content: str) -> list[dict]:
    """Parse JSONL text into a flat list of per-page result dicts."""
    pages = []
    for line in content.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        data   = json.loads(line)
        result = data.get("result", data)
        for page_result in result.get("layoutParsingResults", [result]):
            pages.append(page_result)
    return pages


def download_results(jsonl_url: str, save_path: str) -> list[dict]:
    """Download (or load from cache) JSONL results. Returns list of page dicts."""
    if os.path.exists(save_path):
        print(f"  [cache] {save_path}")
        with open(save_path, encoding="utf-8") as f:
            return parse_jsonl(f.read())

    resp = requests.get(jsonl_url, timeout=120)
    resp.raise_for_status()
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(resp.text)
    print(f"  Saved JSONL → {save_path}")
    return parse_jsonl(resp.text)


# ══════════════════════════════════════════════════════════════════════════════
# STEP 4 — Convert JSON pages → layout-preserving PDF
# ══════════════════════════════════════════════════════════════════════════════

def bbox_to_pdf(bbox: list, sx: float, sy: float) -> tuple:
    """[x1,y1,x2,y2] px → (x_left, y_bottom, width, height) PDF points."""
    x1, y1, x2, y2 = bbox
    return x1 * sx, PDF_H - y2 * sy, (x2 - x1) * sx, (y2 - y1) * sy


def calc_fs(text: str, ph_pt: float, pw_pt: float) -> float:
    """
    Geometric font-size formula — fills the block with text.

    Derivation:
      block_h = n_lines × fs × leading
      n_lines = n_chars / chars_per_line
      chars_per_line = block_w / (fs × avg_char_width)
    Combining → fs = sqrt(block_h × block_w / (n_chars × avg_char_width × leading))

    avg_char_width × leading ≈ 0.50 × 1.30 = 0.65 (calibrated for Times-Roman)

    The min() with h×0.72 prevents oversizing single-line blocks
    (single-line: all block height = one line height → h×0.72 ≈ correct font size).

    Empirically verified: body text blocks converge to ~13–14pt for this book.
    """
    n = len(re.sub(r"\s+", " ", text.replace("\n", " ")).strip())
    if n == 0 or pw_pt < 5 or ph_pt < 5:
        return 11.0
    fs_geo = math.sqrt(ph_pt * pw_pt / (n * 0.65))
    fs_max = ph_pt * 0.72   # single-line upper bound

    # For explicitly line-broken content (references, footnotes), each \n is a
    # hard line break that the font-size formula ignores.  Cap by the height each
    # line is actually allowed: ph / (n_lines × leading_ratio).
    n_lines = text.count("\n") + 1
    if n_lines > 1:
        fs_max = min(fs_max, ph_pt / (n_lines * 1.30))

    return min(fs_geo, fs_max)


# Label → (font, fs_min, fs_max, alignment)
LABEL_CFG = {
    "doc_title":       ("Times-Bold",   12, 72, TA_CENTER),
    "paragraph_title": ("Times-Bold",   10, 20, TA_LEFT),
    "abstract":        ("Times-Italic", 10, 18, TA_JUSTIFY),
    "content":         ("Times-Roman",  10, 18, TA_JUSTIFY),
    "text":            ("Times-Roman",   8, 20, TA_JUSTIFY),
    "header":          ("Times-Roman",   7, 13, TA_CENTER),
    "footer":          ("Times-Roman",   7, 13, TA_CENTER),
    "footer_image":    ("Times-Roman",   6, 10, TA_CENTER),
    "number":          ("Times-Roman",   7, 13, TA_CENTER),
    "footnote":        ("Times-Roman",   7, 12, TA_JUSTIFY),
    "figure_title":    ("Times-Italic",  8, 13, TA_CENTER),
    "aside_text":      ("Times-Italic",  8, 13, TA_LEFT),
}


def make_style(label: str, ph_pt: float, pw_pt: float, text: str) -> ParagraphStyle:
    fs_auto = calc_fs(text, ph_pt, pw_pt)
    font_name, fs_min, fs_max, align = LABEL_CFG.get(
        label, ("Times-Roman", 8, 18, TA_LEFT)
    )
    fs = max(float(fs_min), min(fs_auto, float(fs_max)))
    return ParagraphStyle(
        f"s_{label}",
        fontName=font_name,
        fontSize=fs,
        leading=fs * 1.30,
        alignment=align,
        spaceAfter=0,
    )


def clean_text(content: str) -> str:
    """Strip markdown markup to plain text."""
    t = re.sub(r"^#{1,6}\s*", "", content, flags=re.MULTILINE)
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", t)
    t = re.sub(r"\*(.+?)\*",     r"\1", t)
    t = re.sub(r"<[^>]+>",       "",    t)
    t = re.sub(r"\$\s*\^{(.+?)}\s*\$", r"(\1)", t)   # LaTeX superscript
    t = re.sub(r"\$(.+?)\$",     r"\1", t)             # inline math
    return t.strip()


def to_para_html(text: str) -> str:
    """Convert plain text to reportlab-safe XML (paragraph/line breaks)."""
    t = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    paras = re.split(r"\n{2,}", t)
    parts = [p.replace("\n", "<br/>").strip() for p in paras if p.strip()]
    return "<br/><br/>".join(parts)


_img_cache: dict = {}

def fetch_image(url: str):
    """Download image from URL (cached). Returns PIL Image or None."""
    if url in _img_cache:
        return _img_cache[url]
    try:
        data = urllib.request.urlopen(url, timeout=15).read()
        img  = Image.open(io.BytesIO(data)).convert("RGB")
        _img_cache[url] = img
        return img
    except Exception:
        _img_cache[url] = None
        return None


def render_page(c, page_data: dict, sx: float, sy: float) -> None:
    """Render one OCR page result onto the reportlab canvas."""
    md        = page_data.get("markdown", {})
    md_images = md.get("images", {}) if isinstance(md, dict) else {}

    # Prefer structured prunedResult (has bboxes) over raw markdown
    blocks = page_data.get("prunedResult", {}).get("parsing_res_list", [])

    if not blocks:
        # Fallback: flow raw markdown text as plain body text
        text = (md.get("text", "") if isinstance(md, dict) else str(md)).strip()
        if text:
            style = ParagraphStyle("fallback", fontName="Times-Roman",
                                   fontSize=11, leading=14.3, alignment=TA_JUSTIFY)
            para = Paragraph(to_para_html(clean_text(text)), style)
            w, h = para.wrap(PDF_W - 72, PDF_H - 72)
            para.drawOn(c, 36, PDF_H - 36 - h)
        return

    def sort_key(b):
        order = b.get("block_order")
        # Ordered blocks (text/title) first, then unordered (images) by y-position
        return (0, order) if order is not None else (1, b["block_bbox"][1])

    for block in sorted(blocks, key=sort_key):
        label   = block["block_label"]
        content = block["block_content"]
        px, py, pw, ph = bbox_to_pdf(block["block_bbox"], sx, sy)

        if pw < 2 or ph < 2:
            continue

        # ── Image block ────────────────────────────────────────────────────
        if label == "image":
            url = None
            src_m = re.search(r'src="([^"]+)"', content)
            if src_m:
                # Normal case: content has <img src="...">
                url = md_images.get(src_m.group(1))
            elif md_images:
                # JSONL case: block_content is empty; match by bbox coords in filename.
                # Filenames are like: imgs/img_in_image_box_x1_y1_x2_y2.jpg
                bbox = block["block_bbox"]
                for key, val in md_images.items():
                    nums = list(map(int, re.findall(r"\d+", os.path.basename(key))))
                    if len(nums) >= 4 and nums[-4:] == [int(v) for v in bbox]:
                        url = val
                        break
                # Fallback: single image on page — unambiguous match
                if url is None and len(md_images) == 1:
                    url = next(iter(md_images.values()))
            if url:
                img = fetch_image(url)
                if img:
                    buf = io.BytesIO()
                    img.save(buf, format="JPEG", quality=85)
                    buf.seek(0)
                    c.drawImage(
                        rl_canvas.ImageReader(buf),
                        px, py, pw, ph,
                        preserveAspectRatio=True, anchor="c",
                    )
            # If image unavailable: leave blank (user's explicit preference)
            continue

        # ── Text block ─────────────────────────────────────────────────────
        text = clean_text(content)
        if not text:
            continue

        style   = make_style(label, ph, pw, text)
        rl_text = to_para_html(text)

        try:
            para = Paragraph(rl_text, style)
            _, h = para.wrap(pw, ph * 2)
            if h > ph * 1.05:
                # Text overflows bbox — shrink font proportionally to fit
                fs2 = max(style.fontSize * (ph / h), 6.0)
                style = ParagraphStyle(
                    style.name + "_fit",
                    fontName=style.fontName,
                    fontSize=fs2,
                    leading=fs2 * 1.30,
                    alignment=style.alignment,
                    spaceAfter=0,
                )
                para = Paragraph(rl_text, style)
                _, h = para.wrap(pw, ph * 2)
            para.drawOn(c, px, py + ph - h)       # top-align within bbox
        except Exception:
            # Minimal fallback — at least get some text on the page
            try:
                c.setFont("Times-Roman", 9)
                c.drawString(px, py + ph - 10, text[:120])
            except Exception:
                pass


def pages_to_pdf(pages: list, out_path: str) -> None:
    """Convert a list of OCR page results to a layout-preserving PDF."""
    img_w, img_h = detect_img_size(pages)
    sx = PDF_W / img_w
    sy = PDF_H / img_h

    c = rl_canvas.Canvas(out_path, pagesize=(PDF_W, PDF_H))
    for page_data in pages:
        render_page(c, page_data, sx, sy)
        c.showPage()
    c.save()
    print(f"  PDF: {out_path}  ({os.path.getsize(out_path) // 1024}KB, {len(pages)} pages)")


# ══════════════════════════════════════════════════════════════════════════════
# STEP 5 — Merge chunk PDFs
# ══════════════════════════════════════════════════════════════════════════════

def merge_pdfs(pdf_paths: list, output_path: str) -> None:
    writer = PdfWriter()
    total_pages = 0
    for path in pdf_paths:
        reader = PdfReader(path)
        for page in reader.pages:
            writer.add_page(page)
        total_pages += len(reader.pages)
    with open(output_path, "wb") as f:
        writer.write(f)
    print(f"  Merged {len(pdf_paths)} chunk(s), {total_pages} pages → {output_path}")


# ══════════════════════════════════════════════════════════════════════════════
# Main pipeline
# ══════════════════════════════════════════════════════════════════════════════

def run_pipeline(input_pdf: str, output_pdf: str, work_dir: str, chunk_size: int) -> None:
    os.makedirs(work_dir, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"Input:      {input_pdf}")
    print(f"Output:     {output_pdf}")
    print(f"Work dir:   {work_dir}")
    print(f"Chunk size: {chunk_size} pages")
    print(f"{'='*60}\n")

    # ── 1. Split ───────────────────────────────────────────────────────────
    print("[ 1/5 ] Splitting PDF…")
    chunks = split_pdf(input_pdf, work_dir, chunk_size)

    # ── 2-4. For each chunk: submit → poll → download → render PDF ─────────
    jobs_file = os.path.join(work_dir, "jobs.json")
    jobs: dict = json.loads(open(jobs_file).read()) if os.path.exists(jobs_file) else {}

    chunk_pdfs = []
    for idx, chunk_path in enumerate(chunks, 1):
        chunk_name = os.path.basename(chunk_path)
        result_pdf = chunk_path.replace(".pdf", "_ocr.pdf")
        chunk_pdfs.append(result_pdf)

        print(f"\n[ Chunk {idx}/{len(chunks)} ] {chunk_name}")

        if os.path.exists(result_pdf):
            print(f"  [skip] OCR PDF already exists")
            continue

        # Submit (or reuse cached job id)
        print("  [ 2/5 ] Submitting to PaddleOCR API…")
        if chunk_name not in jobs:
            job_id = submit_chunk(chunk_path)
            jobs[chunk_name] = job_id
            with open(jobs_file, "w") as f:
                json.dump(jobs, f, indent=2)
        else:
            job_id = jobs[chunk_name]
            print(f"  [resume] job {job_id}")

        # Poll
        print(f"  [ 3/5 ] Waiting for job {job_id}…")
        jsonl_path = chunk_path.replace(".pdf", "_results.jsonl")

        if not os.path.exists(jsonl_path):
            jsonl_url = poll_job(job_id)
            print(f"  [ 4/5 ] Downloading results…")
            pages = download_results(jsonl_url, jsonl_path)
        else:
            print(f"  [ 3-4/5 ] Using cached JSONL")
            pages = download_results("", jsonl_path)

        # Render
        print(f"  [ 4/5 ] Rendering {len(pages)} pages to PDF…")
        pages_to_pdf(pages, result_pdf)

    # ── 5. Merge ───────────────────────────────────────────────────────────
    print(f"\n[ 5/5 ] Merging {len(chunk_pdfs)} chunk PDF(s)…")
    merge_pdfs(chunk_pdfs, output_pdf)

    size_mb = os.path.getsize(output_pdf) / 1024 / 1024
    print(f"\n✓  Done!  {output_pdf}  ({size_mb:.1f} MB)")


# ══════════════════════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="PDF OCR Pipeline — PaddleOCR-VL-1.5 with layout preservation"
    )
    parser.add_argument("input_pdf",    help="Path to the input (scanned) PDF")
    parser.add_argument("--output",  "-o", help="Output PDF path (default: <input>_ocr.pdf)")
    parser.add_argument("--work-dir","-w", help="Working directory for intermediate files")
    parser.add_argument("--chunk-size", type=int, default=90,
                        help="Pages per API submission chunk (default: 90)")
    args = parser.parse_args()

    input_path = os.path.abspath(args.input_pdf)
    if not os.path.exists(input_path):
        print(f"Error: file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    base        = os.path.splitext(input_path)[0]
    output_path = args.output   or f"{base}_ocr.pdf"
    work_dir    = args.work_dir or f"{base}_ocr_work"

    run_pipeline(input_path, output_path, work_dir, args.chunk_size)
