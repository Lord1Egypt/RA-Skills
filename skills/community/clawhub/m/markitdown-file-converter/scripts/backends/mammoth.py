#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mammoth backend - DOCX to Markdown converter (fallback).
"""

import re
import zipfile
from pathlib import Path

from utils.deps import is_mammoth, pip_install
from utils.images import rewrite_base64_images


def convert_with_mammoth(
    input_path: Path,
    output_path: Path,
    images_dir: Path,
    verbose: bool = False
) -> None:
    """Convert DOCX file using mammoth."""
    if not is_mammoth():
        pip_install("mammoth")
    
    from bs4 import BeautifulSoup
    import mammoth

    suf = input_path.suffix.lower()
    images_dir.mkdir(parents=True, exist_ok=True)

    if suf in (".docx", ".doc"):
        _extract_docx_images(input_path, images_dir)

    if verbose:
        print(f"[mammoth] Processing {input_path.name} ...")

    with open(str(input_path), "rb") as f:
        html_result = mammoth.convert_to_html(fileobj=f)
    soup = BeautifulSoup(html_result.value, "html.parser")

    # Convert tables to Markdown
    for table_el in soup.find_all("table"):
        md_lines = _html_table_to_md(table_el)
        replacement = soup.new_string("\n" + "\n".join(md_lines) + "\n")
        table_el.replace_with(replacement)

    text = _html_to_text(str(soup))
    text = rewrite_base64_images(text, images_dir)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    output_path.write_text(text, encoding="utf-8")
    print(f"[mammoth] {input_path.name} -> {output_path}")


def _extract_docx_images(docx_path: Path, images_dir: Path) -> list:
    """Extract images from DOCX file."""
    saved = []
    idx = [0]
    
    with zipfile.ZipFile(str(docx_path)) as z:
        for name in z.namelist():
            if name.startswith("word/media/"):
                img_data = z.read(name)
                ext = re.sub(r"[^.]*$", "", name).lower()
                if not ext or ext not in (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"):
                    ext = ".png"
                img_name = f"image_{idx[0]}{ext}"
                (images_dir / img_name).write_bytes(img_data)
                saved.append(img_name)
                idx[0] += 1
    
    return saved


def _html_table_to_md(table_el) -> list:
    """Convert HTML table to Markdown."""
    rows = []
    for tr in table_el.find_all("tr"):
        cells = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
        if cells:
            rows.append(cells)
    
    if not rows:
        return []
    
    cc = len(rows[0])
    md = ["| " + " | ".join(rows[0]) + " |"]
    md.append("| " + " | ".join(["---"] * cc) + " |")
    for row in rows[1:]:
        while len(row) < cc:
            row.append("")
        md.append("| " + " | ".join(row) + " |")
    
    return md


def _html_to_text(html: str) -> str:
    """Convert HTML to Markdown text."""
    from bs4 import BeautifulSoup
    
    soup = BeautifulSoup(html, "html.parser")
    img_idx = [0]

    def walk(el) -> str:
        if el.name is None:
            return str(el)
        
        if el.name == "img":
            src = el.get("src", "")
            if src.startswith("data:image/"):
                m = re.search(r"data:image/(\w+);base64,(.+)", src)
                if m:
                    fname = f"image_{img_idx[0]}.{m.group(1)}"
                    img_idx[0] += 1
                    return f"![{fname}]({fname})"
            alt = el.get("alt", "image")
            return f"![{alt}]({src})" if src else ""
        
        if el.name in ("h1", "h2", "h3", "h4", "h5", "h6"):
            inner = "".join(walk(c) for c in el.children)
            return f"\n{'#' * int(el.name[1])} {inner.strip()}\n\n"
        
        if el.name == "p":
            inner = "".join(walk(c) for c in el.children).strip()
            return inner + "\n\n" if inner else ""
        
        if el.name == "br":
            return "\n"
        
        if el.name == "hr":
            return "\n---\n\n"
        
        if el.name == "blockquote":
            inner = "".join(walk(c) for c in el.children).strip()
            return "\n> " + inner.replace("\n", "\n> ") + "\n\n"
        
        if el.name == "ul":
            parts = []
            for li in el.find_all("li", recursive=False):
                parts.append("- " + "".join(walk(c) for c in li.children).strip())
            return "\n" + "\n".join(parts) + "\n\n"
        
        if el.name == "ol":
            parts = []
            for i, li in enumerate(el.find_all("li", recursive=False), 1):
                parts.append(f"{i}. " + "".join(walk(c) for c in li.children).strip())
            return "\n" + "\n".join(parts) + "\n\n"
        
        if el.name in ("strong", "b"):
            return "**" + "".join(walk(c) for c in el.children) + "**"
        
        if el.name == "em":
            return "_" + "".join(walk(c) for c in el.children) + "_"
        
        if el.name == "code":
            return "`" + "".join(walk(c) for c in el.children) + "`"
        
        if el.name == "pre":
            return f"\n```\n{el.get_text(strip=True)}\n```\n\n"
        
        if el.name in ("table", "thead", "tbody", "tr", "td", "th"):
            return "".join(walk(c) for c in el.children)
        
        return "".join(walk(c) for c in el.children)

    body = soup.body if soup.body else soup
    return "".join(walk(c) for c in body.children)