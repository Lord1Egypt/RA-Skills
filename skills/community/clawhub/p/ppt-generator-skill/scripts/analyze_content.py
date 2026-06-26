#!/usr/bin/env python3
"""
analyze_content.py — Parse uploaded reference materials for PPT generation.

Supports: .txt, .md, .pdf, .pptx, .docx, .csv, .json

v4 changes vs v3:
  - Replaced the blunt 12,000-char hard cut with smart chunking:
      * Respects paragraph / section boundaries
      * Keeps a structural map (headings + first sentence of each section)
      * For long docs: outputs full_content_path (temp file) + summary for LLM
      * Agent decides whether to use summary or full path
  - --max-chars flag (default 40000) for explicit override
  - --summary-only flag for large docs where only structure is needed
  - CSV row limit raised from 200 → 500, with column stats header
"""

import os
import sys
import json
import argparse
import re
import tempfile
from pathlib import Path

DEFAULT_MAX_CHARS = 40000   # ~10k tokens — fits comfortably in modern LLM contexts
SUMMARY_THRESHOLD = 40000   # above this, also emit a structural summary


# ── Extractors ────────────────────────────────────────────────────────────────

def extract_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def extract_md(path: str) -> str:
    return extract_txt(path)


def extract_pdf(path: str) -> str:
    try:
        import subprocess
        result = subprocess.run(
            ["python3", "-m", "markitdown", path],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout
        import pypdf
        reader = pypdf.PdfReader(path)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception as e:
        return f"[PDF extraction error: {e}]"


def extract_pptx(path: str) -> str:
    try:
        import subprocess
        result = subprocess.run(
            ["python3", "-m", "markitdown", path],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            return result.stdout
    except Exception:
        pass
    return f"[PPTX extraction failed for {path}]"


def extract_docx(path: str) -> str:
    try:
        import subprocess
        result = subprocess.run(
            ["python3", "-m", "markitdown", path],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            return result.stdout
    except Exception:
        pass
    return f"[DOCX extraction failed for {path}]"


def extract_csv(path: str) -> str:
    """Extract CSV with column stats header and up to 500 data rows."""
    try:
        import csv
        rows = []
        col_stats = {}
        with open(path, newline="", encoding="utf-8", errors="ignore") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames or []
            for col in headers:
                col_stats[col] = 0

            data_rows = []
            for i, row in enumerate(reader):
                if i >= 500:
                    rows.append(f"... (showing 500/{i+1} rows)")
                    break
                data_rows.append(" | ".join(str(row.get(h, "")) for h in headers))
                for col in headers:
                    if row.get(col, "").strip():
                        col_stats[col] += 1

            # Header: column names + non-empty count
            header_line = " | ".join(headers)
            stats_line  = "Columns: " + ", ".join(
                f"{c}({col_stats[c]} values)" for c in headers
            )
            rows = [header_line, stats_line, "---"] + data_rows + rows
        return "\n".join(rows)
    except Exception as e:
        return f"[CSV extraction error: {e}]"


def extract_json_file(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return json.dumps(data, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"[JSON extraction error: {e}]"


EXTRACTORS = {
    ".txt":  extract_txt,
    ".md":   extract_md,
    ".pdf":  extract_pdf,
    ".pptx": extract_pptx,
    ".docx": extract_docx,
    ".csv":  extract_csv,
    ".json": extract_json_file,
}


# ── Smart chunking ────────────────────────────────────────────────────────────

def extract_structure(text: str) -> str:
    """
    Build a structural summary of a long document:
    - All headings (lines starting with # or all-caps lines or numbered sections)
    - First sentence of each paragraph
    This lets the LLM see the full outline even when the full text is long.
    """
    lines = text.split("\n")
    summary_lines = []
    prev_was_heading = False

    heading_re = re.compile(
        r"^(#{1,4}\s.+|"           # Markdown headings
        r"\d+[\.\)]\s+.{3,60}|"   # Numbered sections like "1. Introduction"
        r"[A-Z\u4e00-\u9fff][\u4e00-\u9fff\s]{2,30}[：:])$"  # Chinese section headers
    )

    for line in lines:
        stripped = line.strip()
        if not stripped:
            prev_was_heading = False
            continue

        is_heading = bool(heading_re.match(stripped)) or (
            len(stripped) < 60 and stripped.isupper()
        )

        if is_heading:
            summary_lines.append(f"\n## {stripped}")
            prev_was_heading = True
        elif not prev_was_heading:
            # First sentence of paragraph
            first_sentence = re.split(r"[。.!！?？\n]", stripped)[0]
            if len(first_sentence) > 10:
                summary_lines.append(f"  → {first_sentence[:120]}")
            prev_was_heading = False

    return "\n".join(summary_lines)


def smart_truncate_content(content: str, max_chars: int) -> tuple[str, bool, str]:
    """
    Truncate content intelligently at a paragraph boundary.
    Returns: (truncated_text, was_truncated, structural_summary)
    """
    structural_summary = ""
    was_truncated = len(content) > max_chars

    if not was_truncated:
        return content, False, ""

    # Build structural summary of the full document
    structural_summary = extract_structure(content)

    # Find a good cut point: paragraph boundary within the max_chars window
    window = content[:max_chars]

    # Try to cut at double newline (paragraph break)
    cut = window.rfind("\n\n")
    if cut > max_chars * 0.7:
        truncated = window[:cut]
    else:
        # Try single newline
        cut = window.rfind("\n")
        if cut > max_chars * 0.7:
            truncated = window[:cut]
        else:
            # Try sentence end
            for punct in ["。", ".", "！", "!", "？", "?"]:
                cut = window.rfind(punct)
                if cut > max_chars * 0.7:
                    truncated = window[:cut + 1]
                    break
            else:
                truncated = window

    chars_remaining = len(content) - len(truncated)
    truncated += (
        f"\n\n... [TRUNCATED: {chars_remaining:,} chars remaining ({len(content):,} total). "
        f"Structural outline follows.]\n\n"
        f"=== DOCUMENT STRUCTURE (FULL) ===\n{structural_summary}"
    )

    return truncated, True, structural_summary


# ── File analysis ─────────────────────────────────────────────────────────────

def analyze_file(path: str, max_chars: int, summary_only: bool) -> dict:
    p = Path(path)
    ext = p.suffix.lower()
    file_type = ext.lstrip(".") or "unknown"
    size_kb = round(p.stat().st_size / 1024, 1) if p.exists() else 0

    extractor = EXTRACTORS.get(ext)
    if not extractor:
        return {
            "filename": p.name,
            "file_type": file_type,
            "size_kb": size_kb,
            "status": f"unsupported file type: {ext}",
            "content": "",
        }

    raw_content = extractor(path)
    total_chars = len(raw_content)

    if summary_only and total_chars > SUMMARY_THRESHOLD:
        summary = extract_structure(raw_content)
        return {
            "filename": p.name,
            "file_type": file_type,
            "size_kb": size_kb,
            "status": "ok",
            "total_chars": total_chars,
            "truncated": True,
            "truncation_mode": "summary_only",
            "content": f"=== STRUCTURAL SUMMARY (full doc: {total_chars:,} chars) ===\n{summary}",
        }

    content, was_truncated, summary = smart_truncate_content(raw_content, max_chars)

    result = {
        "filename": p.name,
        "file_type": file_type,
        "size_kb": size_kb,
        "status": "ok",
        "total_chars": total_chars,
        "truncated": was_truncated,
        "content": content,
    }

    if was_truncated:
        result["truncation_note"] = (
            f"Document is {total_chars:,} chars. "
            f"Showing first {max_chars:,} chars plus full structural outline. "
            f"If critical information is missing from the slide plan, "
            f"re-run with --max-chars {total_chars} to include full document."
        )

    return result


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Analyze uploaded files for PPT generation")
    parser.add_argument("files", nargs="+", help="Paths to uploaded files")
    parser.add_argument("--template",     help="Explicitly mark a file as the PPT template")
    parser.add_argument("--max-chars",    type=int, default=DEFAULT_MAX_CHARS,
                        help=f"Max chars per file before smart truncation (default: {DEFAULT_MAX_CHARS})")
    parser.add_argument("--summary-only", action="store_true",
                        help="For long docs, output structural summary only (faster, less tokens)")
    args = parser.parse_args()

    results = []
    template_path = args.template

    for path in args.files:
        if not os.path.exists(path):
            results.append({
                "filename": os.path.basename(path),
                "status": "file not found",
                "content": "",
            })
            continue

        info = analyze_file(path, args.max_chars, args.summary_only)

        # Tag role
        if template_path and os.path.abspath(path) == os.path.abspath(template_path):
            info["role"] = "template"
        elif info["file_type"] == "pptx" and not template_path:
            info["role"] = "template_candidate"
        else:
            info["role"] = "content"

        results.append(info)

    # Truncation warnings for agent
    truncated_files = [r["filename"] for r in results if r.get("truncated")]

    output = {
        "file_count": len(results),
        "files": results,
        "truncated_files": truncated_files,
        "instructions": (
            "Pass the 'content' fields from role='content' files to the LLM. "
            "If 'truncated' is true, the content includes a structural outline of the remaining sections — "
            "use this outline to ensure all major topics are covered in the slide plan even if the full text was not sent. "
            "Use role='template' or role='template_candidate' pptx as the visual base via template_builder.py. "
            "If no template file exists, generate from scratch using generate_ppt.py."
        )
    }

    if truncated_files:
        output["truncation_warning"] = (
            f"Files truncated: {truncated_files}. "
            f"Re-run with --max-chars <larger_number> to include more content. "
            f"The structural outline embedded in 'content' shows all headings and section starts."
        )

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
