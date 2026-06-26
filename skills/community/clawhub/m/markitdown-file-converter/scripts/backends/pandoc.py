#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pandoc backend - universal document converter.
"""

import platform
import re
import shutil
import subprocess
from pathlib import Path
from typing import Optional

from utils.deps import is_pandoc, is_markitdown_class, pip_install
from utils.images import extract_images_from_docx, extract_images_from_xlsx
from utils.table import beautify_markdown_tables


def _pandoc_cmd() -> list:
    """Get pandoc command path."""
    p = shutil.which("pandoc")
    if p:
        return [p]
    
    if platform.system() == "Windows":
        wp = Path(r"C:\Program Files\Pandoc\pandoc.EXE")
        if wp.exists():
            return [str(wp)]
    elif platform.system() == "Darwin":
        mp = Path("/usr/local/bin/pandoc")
        if mp.exists():
            return [str(mp)]
    
    return []


def install_pandoc():
    """Install pandoc on the system."""
    if is_pandoc():
        print("[install] pandoc already installed")
        return
    
    import sys
    import zipfile
    import tempfile
    import urllib.request
    
    print("[install] pandoc not found. Installing...")
    
    if platform.system() == "Windows":
        try:
            subprocess.run(
                ["winget", "install", "--accept-package-agreements",
                 "--accept-source-agreements", "JohnMacFarlane.Pandoc"],
                check=True, capture_output=True,
            )
            return
        except Exception:
            pass
        
        try:
            url = "https://github.com/jgm/pandoc/releases/download/3.4/pandoc-3.4-windows-x86_64.zip"
            tmp = Path(tempfile.gettempdir()) / "pandoc.zip"
            print("[install] Downloading pandoc from GitHub ...")
            urllib.request.urlretrieve(url, tmp)
            ex = Path(tempfile.gettempdir()) / "pandoc_install"
            ex.mkdir(exist_ok=True)
            with zipfile.ZipFile(tmp) as z:
                z.extractall(ex)
            for exe in ex.rglob("pandoc.exe"):
                shutil.copy(exe, exe.parent / "pandoc.exe")
                import os
                os.environ["PATH"] = str(exe.parent) + os.pathsep + os.environ.get("PATH", "")
                print(f"[install] pandoc installed to {exe}")
                return
        except Exception as e:
            print(f"[install] Failed: {e}")
            print("[install] Please install manually: https://pandoc.org/installing.html")
            sys.exit(1)
    
    elif platform.system() == "Darwin":
        try:
            subprocess.run(["brew", "install", "pandoc"], check=True, capture_output=True)
        except Exception:
            print("[install] Run: brew install pandoc")
            sys.exit(1)
    else:
        try:
            subprocess.run(["sudo", "apt-get", "install", "-y", "pandoc"],
                          check=True, capture_output=True)
        except Exception:
            print("[install] Run: sudo apt-get install pandoc")
            sys.exit(1)


def convert_with_pandoc(
    input_path: Path,
    output_path: Path,
    images_dir: Path,
    verbose: bool = False,
    timeout: int = 120
) -> None:
    """Convert file using pandoc."""
    if not is_pandoc():
        install_pandoc()
    
    images_dir.mkdir(parents=True, exist_ok=True)
    suf = input_path.suffix.lower()
    
    # Extract images for supported formats
    if suf == ".docx":
        extract_images_from_docx(input_path, images_dir)
    elif suf in (".xlsx", ".xls"):
        extract_images_from_xlsx(input_path, images_dir)

    cmd = _pandoc_cmd() + [str(input_path), "-t", "markdown", "-o", str(output_path)]
    
    if verbose:
        print(f"[pandoc] Running: {' '.join(cmd)}")
    
    try:
        subprocess.check_call(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=timeout
        )
    except subprocess.CalledProcessError as e:
        print(f"[pandoc] convert failed: {e}")
        raise
    except subprocess.TimeoutExpired:
        print(f"[pandoc] Timeout after {timeout}s")
        raise

    text = output_path.read_text(encoding="utf-8")

    # Fix pandoc image syntax: ![alt](path/to/image.png){width="..." height="..."}
    def fix_img(m):
        fname = Path(m.group(1)).name
        return f"![{fname}]({fname})"

    text = re.sub(r"!\[\]\(([^()]*media/[^()]*)\)(?:\{[^}]*\})?", fix_img, text)
    text = re.sub(r"!\[([^\]]*)\]\(([^()]*media/[^()]*)\)(?:\{[^}]*\})?", fix_img, text)

    text = _clean_pandoc_output(text)
    text = beautify_markdown_tables(text)
    output_path.write_text(text, encoding="utf-8")
    print(f"[pandoc] {input_path.name} -> {output_path}")


def _clean_pandoc_output(text: str) -> str:
    """Clean pandoc output."""
    import re
    
    # Remove escaping of special characters
    text = re.sub(r"\\(?=[*^_~#\\])", "", text)
    text = re.sub(r"\{=[a-z]+\}", "", text)
    text = re.sub(r":::(\{[^}]*\})?\s*\n", "", text)
    text = re.sub(r"\n\s*:::\s*\n", "\n", text)
    text = re.sub(r"(#{1,6}\s+[^\n]+)\s*\{[^}]*\}\s*$", r"\1", text, flags=re.MULTILINE)
    
    # Clean up excessive blank lines
    out_lines = []
    blank_run = 0
    for line in text.splitlines(keepends=True):
        s = line.strip()
        is_sep = bool(re.match(r"^[\s\-=~]+$", s)) and len(re.sub(r"[^\-=~]", "", s)) >= 3
        if is_sep:
            out_lines.append(line)
            blank_run = 0
        elif not s:
            blank_run += 1
            if blank_run <= 2:
                out_lines.append("\n")
        else:
            blank_run = 0
            out_lines.append(line)
    
    return "".join(out_lines).rstrip() + "\n"