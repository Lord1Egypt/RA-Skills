#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Image extraction utilities - extract images from DOCX/XLSX files.
"""

import os
import re
import zipfile
from pathlib import Path
from typing import List


def extract_images_from_docx(docx_path: Path, images_dir: Path) -> List[str]:
    """Extract images from DOCX file."""
    images_dir.mkdir(parents=True, exist_ok=True)
    saved = []
    idx = [0]
    
    with zipfile.ZipFile(str(docx_path)) as z:
        for name in z.namelist():
            if name.startswith("word/media/"):
                img_data = z.read(name)
                ext = os.path.splitext(name)[-1].lower()
                if not ext or ext not in (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"):
                    ext = ".png"
                img_name = f"image_{idx[0]}{ext}"
                (images_dir / img_name).write_bytes(img_data)
                saved.append(img_name)
                idx[0] += 1
    
    return saved


def extract_images_from_xlsx(xlsx_path: Path, images_dir: Path) -> List[str]:
    """Extract images from XLSX file."""
    images_dir.mkdir(parents=True, exist_ok=True)
    saved = []
    idx = [0]
    
    with zipfile.ZipFile(str(xlsx_path)) as z:
        for name in z.namelist():
            if name.startswith("xl/media/"):
                img_data = z.read(name)
                ext = os.path.splitext(name)[-1].lower()
                if not ext or ext not in (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"):
                    ext = ".png"
                img_name = f"image_{idx[0]}{ext}"
                (images_dir / img_name).write_bytes(img_data)
                saved.append(img_name)
                idx[0] += 1
    
    return saved


def append_image_links(md_text: str, images_dir: Path) -> str:
    """Append image links at the end of Markdown text if not already present."""
    if not images_dir.exists():
        return md_text
    
    imgs = sorted(images_dir.iterdir())
    if not imgs:
        return md_text
    
    # Skip if markdown already has images
    if re.search(r"!\[[^\]]*\]\([^)]+\)", md_text):
        return md_text
    
    try:
        rel_dir = images_dir.relative_to(Path.cwd())
    except ValueError:
        rel_dir = images_dir
    
    lines = ["\n\n## Extracted Images\n"]
    for img in imgs:
        lines.append(f"![{img.name}]({(rel_dir / img.name).as_posix()})\n")
    
    return md_text + "".join(lines)


def rewrite_base64_images(md_text: str, images_dir: Path) -> str:
    """Rewrite base64 encoded images as file references."""
    import base64
    
    images_dir.mkdir(parents=True, exist_ok=True)
    idx = [0]

    def replacer(m):
        try:
            b64 = m.group(1)
            fname = f"image_{idx[0]}.png"
            idx[0] += 1
            img_path = images_dir / fname
            if not img_path.exists():
                img_path.write_bytes(base64.b64decode(b64))
            return f"![{fname}]({fname})"
        except Exception:
            return m.group(0)

    return re.sub(r"!\[\]\(data:image/\w+;base64,(.+?)\)", replacer, md_text)