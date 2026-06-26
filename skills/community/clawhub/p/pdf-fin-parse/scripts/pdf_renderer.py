"""PDF / 图片 → PNG bytes 的纯渲染层。

注意：本文件只做渲染（PDF 解码、栅格化、单页图片读取），**不抽取任何内容**。
所有"理解"由 vlm_client 负责。
"""
from __future__ import annotations

import io
import sys
from pathlib import Path
from typing import Iterator, List, Optional


# ---------------------------------------------------------------------------
# 主入口
# ---------------------------------------------------------------------------

def count_pdf_pages(path: str, password: Optional[str] = None) -> int:
    """返回 PDF/图片的页数；图片始终为 1。"""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"输入文件不存在: {path}")
    if _is_image(p):
        return 1
    return _open_pdf_and_count(path, password)


def render_pdf_pages(
    path: str,
    pages: List[int],
    *,
    dpi: int = 200,
    password: Optional[str] = None,
) -> Iterator[tuple[int, bytes]]:
    """yield (page_no, png_bytes)。pages 为 1-based 列表。

    图片输入只返回 (1, png_bytes)。
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"输入文件不存在: {path}")

    if _is_image(p):
        yield 1, _read_image_as_png(p)
        return

    yield from _render_pdf_pages(path, pages, dpi=dpi, password=password)


# ---------------------------------------------------------------------------
# 内部
# ---------------------------------------------------------------------------

_IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp", ".tiff", ".tif"}


def _is_image(p: Path) -> bool:
    return p.suffix.lower() in _IMAGE_EXTS


def _read_image_as_png(p: Path) -> bytes:
    """非 PNG 图片统一转 PNG（数据 URI 兼容）。"""
    if p.suffix.lower() == ".png":
        return p.read_bytes()
    try:
        from PIL import Image
    except ImportError as e:
        raise RuntimeError(f"Pillow 未安装: {e}")
    buf = io.BytesIO()
    img = Image.open(p)
    if img.mode in ("RGBA", "LA"):
        bg = Image.new("RGB", img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[-1])
        bg.save(buf, format="PNG")
    else:
        img.convert("RGB").save(buf, format="PNG")
    return buf.getvalue()


def _open_pdf_and_count(path: str, password: Optional[str]) -> int:
    try:
        import fitz  # PyMuPDF
    except ImportError as e:
        raise RuntimeError(f"PyMuPDF 未安装: {e}")
    doc = fitz.open(path)
    try:
        if doc.is_encrypted and not (password and doc.authenticate(password)):
            raise RuntimeError("PDF 加密，请通过 --password 提供密码")
        return len(doc)
    finally:
        doc.close()


def _render_pdf_pages(
    path: str,
    pages: List[int],
    *,
    dpi: int,
    password: Optional[str],
) -> Iterator[tuple[int, bytes]]:
    try:
        import fitz
    except ImportError as e:
        raise RuntimeError(f"PyMuPDF 未安装: {e}")
    doc = fitz.open(path)
    try:
        if doc.is_encrypted and not (password and doc.authenticate(password)):
            raise RuntimeError("PDF 加密，请通过 --password 提供密码")
        zoom = dpi / 72.0
        mat = fitz.Matrix(zoom, zoom)
        total = len(doc)
        for pn in pages:
            if pn < 1 or pn > total:
                print(f"[render] 跳过越界页 {pn} (total={total})", file=sys.stderr)
                continue
            page = doc[pn - 1]
            pix = page.get_pixmap(matrix=mat, alpha=False)
            yield pn, pix.tobytes("png")
    finally:
        doc.close()
