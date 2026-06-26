#!/usr/bin/env python3
"""
v2_l5_ocr.py — L5 OCR 替换模块（Image-based PDF Text Replacement）

将 PyPI 包 pdf_text_replace.ocr（实际路径：pdf_text_replace_v2_ocr.py）
中的实现适配为 openclaw 主入口（pdf_text_replace.py）期望的接口：

    is_image_based(pdf_path, page_num) -> bool
    replace_text_ocr(pdf_path, old_text, new_text, output_path, page_num) -> bool

流水线：检测 → OCR → 涂抹（inpaint）→ 渲染 → 保存
"""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path
from typing import Optional


# ─────────────────────────────────────────────────────────────────────────────
# 可选依赖导入（全部守卫，优雅降级）
# ─────────────────────────────────────────────────────────────────────────────

try:
    import fitz  # pymupdf
    HAS_FITZ = True
except ImportError:
    HAS_FITZ = False

try:
    import cv2
    import numpy as np
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False

try:
    from paddleocr import PaddleOCR
    HAS_PADDLE = True
except ImportError:
    HAS_PADDLE = False

try:
    import pytesseract
    HAS_TESSERACT = True
except ImportError:
    HAS_TESSERACT = False

try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    raise ImportError("Pillow 是必要依赖。请安装: pip install Pillow")

try:
    from pypdf import PdfReader
    HAS_PYPDF = True
except ImportError:
    try:
        from PyPDF2 import PdfReader
        HAS_PYPDF = True
    except ImportError:
        HAS_PYPDF = False

try:
    from reportlab.pdfgen import canvas as rl_canvas
    from reportlab.lib.utils import ImageReader
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False


# ─────────────────────────────────────────────────────────────────────────────
# CJK 字体查找
# ─────────────────────────────────────────────────────────────────────────────

_CJK_FONT_SEARCH_PATHS = [
    "/System/Library/Fonts",
    "/System/Library/AssetsV2/com_apple_MobileAsset_Font7",
    "/System/Library/AssetsV2/com_apple_MobileAsset_Font6",
    "/Library/Fonts",
    os.path.expanduser("~/Library/Fonts"),
    "/usr/share/fonts",
    "/usr/local/share/fonts",
]

_CJK_FONT_NAMES = [
    "PingFang SC Regular.ttf",
    "PingFang.ttc",
    "STHeiti Light.ttc",
    "STHeiti Medium.ttc",
    "Hiragino Sans GB.ttc",
    "NotoSansCJK-Regular.ttc",
    "NotoSansMonoCJKsc-Regular.otf",
    "WenQuanYiMicroHei.ttf",
    "Arial.ttf",
    "DejaVuSans.ttf",
]


def _find_cjk_font() -> Optional[str]:
    for search_root in _CJK_FONT_SEARCH_PATHS:
        if not os.path.isdir(search_root):
            continue
        for dirpath, _dirnames, filenames in os.walk(search_root):
            for fname in filenames:
                if fname in _CJK_FONT_NAMES:
                    return os.path.join(dirpath, fname)
    return None


# ─────────────────────────────────────────────────────────────────────────────
# 步骤 1：检测（Detection）
# ─────────────────────────────────────────────────────────────────────────────

def is_image_based_pdf(pdf_path: str, page_num: int = 0) -> bool:
    """检测 PDF 页面是否为图像型（无可提取文本）。"""
    if HAS_PYPDF:
        try:
            reader = PdfReader(pdf_path)
            if page_num >= len(reader.pages):
                raise ValueError(f"页码 {page_num} 超出范围（共 {len(reader.pages)} 页）")
            text = (reader.pages[page_num].extract_text() or "").strip()
            return len(text.replace(" ", "").replace("\n", "")) < 20
        except Exception as e:
            print(f"[pdf_ocr] pypdf 提取失败: {e}，假定为图像型")
            return True

    if HAS_FITZ:
        try:
            doc = fitz.open(pdf_path)
            page = doc[page_num]
            image_list = page.get_images(full=True)
            page_area = abs(page.rect.width * page.rect.height)
            for img in image_list:
                xref = img[0]
                img_info = doc.extract_image(xref)
                img_w = img_info.get("width", 0)
                img_h = img_info.get("height", 0)
                if img_w * img_h > page_area * 0.5:
                    doc.close()
                    return True
            doc.close()
            return len(image_list) > 0
        except Exception as e:
            print(f"[pdf_ocr] fitz 图像检查失败: {e}")
            return True

    print("[pdf_ocr] 无 PDF 库可用，假定为图像型")
    return True


# 主入口期望的别名（is_image_based）
def is_image_based(pdf_path: str, page_num: int = 0) -> bool:
    """is_image_based_pdf 的别名，供 pdf_text_replace.py 调用。"""
    return is_image_based_pdf(pdf_path, page_num)


# ─────────────────────────────────────────────────────────────────────────────
# 步骤 2：OCR
# ─────────────────────────────────────────────────────────────────────────────

def ocr_page(image: "Image.Image", lang: str = "chi_sim+eng", engine: str = "auto") -> list:
    """对页面图像执行 OCR，返回带边界框的文本列表。

    返回: [{'text': str, 'bbox': (x, y, w, h), 'confidence': float}]
    """
    use_paddle = False
    use_tesseract = False

    if engine == "paddle":
        if not HAS_PADDLE:
            print("[pdf_ocr] PaddleOCR 未安装")
            return []
        use_paddle = True
    elif engine == "tesseract":
        if not HAS_TESSERACT:
            print("[pdf_ocr] pytesseract 未安装")
            return []
        use_tesseract = True
    else:
        if HAS_PADDLE:
            use_paddle = True
        elif HAS_TESSERACT:
            use_tesseract = True
        else:
            print("[pdf_ocr] 无 OCR 引擎可用。请安装 paddleocr 或 pytesseract。")
            return []

    results = []

    if use_paddle:
        try:
            if not HAS_CV2:
                import numpy as np_local
                img_array = np_local.array(image.convert("RGB"))
            else:
                img_array = cv2.cvtColor(
                    cv2.UMat(cv2.imdecode(
                        cv2.imencode(".png", _pil_to_cv2(image))[1],
                        cv2.IMREAD_COLOR
                    )).get(),
                    cv2.COLOR_BGR2RGB,
                )

            paddle_lang = "ch" if "chi" in lang else "en"
            ocr = PaddleOCR(use_angle_cls=True, lang=paddle_lang, show_log=False)
            paddle_result = ocr.ocr(img_array, cls=True)

            if paddle_result and paddle_result[0]:
                for line in paddle_result[0]:
                    box_pts, (text, conf) = line
                    xs = [p[0] for p in box_pts]
                    ys = [p[1] for p in box_pts]
                    x, y = int(min(xs)), int(min(ys))
                    w, h = int(max(xs) - min(xs)), int(max(ys) - min(ys))
                    results.append({"text": text, "bbox": (x, y, w, h), "confidence": float(conf)})
            return results
        except Exception as e:
            print(f"[pdf_ocr] PaddleOCR 失败 ({e})，回退到 tesseract")
            if not HAS_TESSERACT:
                return []
            use_tesseract = True

    if use_tesseract:
        try:
            data = pytesseract.image_to_data(image, lang=lang, output_type=pytesseract.Output.DICT)
            n = len(data["text"])
            for i in range(n):
                text = data["text"][i].strip()
                if not text:
                    continue
                conf_raw = data["conf"][i]
                conf = float(conf_raw) / 100.0 if conf_raw != -1 else 0.0
                x = int(data["left"][i])
                y = int(data["top"][i])
                w = int(data["width"][i])
                h = int(data["height"][i])
                results.append({"text": text, "bbox": (x, y, w, h), "confidence": conf})
            return results
        except Exception as e:
            print(f"[pdf_ocr] pytesseract 失败: {e}")
            return []

    return results


# ─────────────────────────────────────────────────────────────────────────────
# PIL ↔ OpenCV 转换辅助
# ─────────────────────────────────────────────────────────────────────────────

def _pil_to_cv2(pil_image: "Image.Image"):
    import numpy as _np
    rgb = pil_image.convert("RGB")
    arr = _np.array(rgb)
    return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)


def _cv2_to_pil(cv2_image) -> "Image.Image":
    rgb = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgb)


# ─────────────────────────────────────────────────────────────────────────────
# 步骤 3：背景修复（Inpainting）
# ─────────────────────────────────────────────────────────────────────────────

def inpaint_region(image: "Image.Image", bbox: tuple, method: str = "telea") -> "Image.Image":
    """从图像区域中移除文本并用周围纹理填充。"""
    x, y, w, h = bbox

    if not HAS_CV2:
        img_copy = image.copy().convert("RGBA")
        draw = ImageDraw.Draw(img_copy)
        border = 5
        sample_region = (
            max(0, x - border), max(0, y - border),
            min(image.width, x + w + border), min(image.height, y + h + border),
        )
        crop = image.crop(sample_region).convert("RGB")
        pixels = list(crop.getdata())
        avg_r = int(sum(p[0] for p in pixels) / len(pixels))
        avg_g = int(sum(p[1] for p in pixels) / len(pixels))
        avg_b = int(sum(p[2] for p in pixels) / len(pixels))
        draw.rectangle([x, y, x + w, y + h], fill=(avg_r, avg_g, avg_b, 255))
        return img_copy.convert("RGB")

    cv_img = _pil_to_cv2(image)
    mask = np.zeros(cv_img.shape[:2], dtype=np.uint8)
    pad = max(2, h // 8)
    x1 = max(0, x - pad)
    y1 = max(0, y - pad)
    x2 = min(cv_img.shape[1], x + w + pad)
    y2 = min(cv_img.shape[0], y + h + pad)
    mask[y1:y2, x1:x2] = 255

    inpaint_flag = cv2.INPAINT_TELEA if method == "telea" else cv2.INPAINT_NS
    radius = max(3, h // 4)
    result = cv2.inpaint(cv_img, mask, inpaintRadius=radius, flags=inpaint_flag)
    return _cv2_to_pil(result)


# ─────────────────────────────────────────────────────────────────────────────
# 步骤 4：渲染新文本
# ─────────────────────────────────────────────────────────────────────────────

def render_text_on_image(
    image: "Image.Image",
    text: str,
    bbox: tuple,
    font_path: str = None,
    font_size: int = None,
    color: tuple = (0, 0, 0),
) -> "Image.Image":
    """在图像指定位置渲染文本。"""
    x, y, w, h = bbox
    img_copy = image.copy().convert("RGBA")
    draw = ImageDraw.Draw(img_copy)

    resolved_font_path = font_path or _find_cjk_font()
    if font_size is None:
        font_size = max(8, int(h * 0.80))

    font = None
    if resolved_font_path and os.path.isfile(resolved_font_path):
        try:
            font = ImageFont.truetype(resolved_font_path, font_size)
        except Exception as e:
            print(f"[pdf_ocr] 无法加载字体 {resolved_font_path}: {e}")

    if font is None:
        try:
            font = ImageFont.load_default()
        except Exception:
            font = None

    if font:
        try:
            if hasattr(font, "getbbox"):
                tb = font.getbbox(text)
                text_w = tb[2] - tb[0]
                text_h = tb[3] - tb[1]
            else:
                text_w, text_h = font.getsize(text)  # type: ignore[attr-defined]
        except Exception:
            text_w, text_h = w, h
    else:
        text_w, text_h = w, h

    text_x = x
    text_y = y + max(0, (h - text_h) // 2)

    draw.text((text_x, text_y), text, fill=color + (255,), font=font)
    return img_copy.convert("RGB")


# ─────────────────────────────────────────────────────────────────────────────
# 步骤 5：写回 PDF
# ─────────────────────────────────────────────────────────────────────────────

def replace_page_image(
    pdf_path: str,
    page_num: int,
    new_image: "Image.Image",
    output_path: str,
) -> None:
    """将修改后的图像替换回 PDF 页面。"""
    if HAS_FITZ:
        _replace_page_fitz(pdf_path, page_num, new_image, output_path)
    elif HAS_REPORTLAB:
        _replace_page_reportlab(pdf_path, page_num, new_image, output_path)
    else:
        raise RuntimeError(
            "需要 pymupdf 或 reportlab。请安装: pip install pymupdf 或 pip install reportlab"
        )


def _replace_page_fitz(pdf_path: str, page_num: int, new_image: "Image.Image", output_path: str) -> None:
    doc = fitz.open(pdf_path)
    page = doc[page_num]
    rect = page.rect

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp_path = tmp.name
    try:
        new_image.save(tmp_path, format="PNG", dpi=(300, 300))
        page.clean_contents()
        page.insert_image(rect, filename=tmp_path, keep_proportion=False)
        doc.save(output_path, garbage=4, deflate=True)
    finally:
        doc.close()
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


def _replace_page_reportlab(pdf_path: str, page_num: int, new_image: "Image.Image", output_path: str) -> None:
    if not HAS_REPORTLAB:
        raise RuntimeError("reportlab 未安装")

    page_width_pt = 595.0
    page_height_pt = 842.0

    if HAS_PYPDF:
        reader = PdfReader(pdf_path)
        if page_num < len(reader.pages):
            mb = reader.pages[page_num].mediabox
            page_width_pt = float(mb.width)
            page_height_pt = float(mb.height)

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        img_tmp = tmp.name
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp2:
        overlay_pdf = tmp2.name

    try:
        new_image.save(img_tmp, format="PNG")
        c = rl_canvas.Canvas(overlay_pdf, pagesize=(page_width_pt, page_height_pt))
        c.drawImage(
            ImageReader(img_tmp),
            0, 0,
            width=page_width_pt, height=page_height_pt,
            preserveAspectRatio=False,
        )
        c.save()

        if HAS_PYPDF:
            try:
                from pypdf import PdfWriter
            except ImportError:
                from PyPDF2 import PdfWriter

            reader_src = PdfReader(pdf_path)
            reader_overlay = PdfReader(overlay_pdf)
            writer = PdfWriter()

            for i, pg in enumerate(reader_src.pages):
                if i == page_num:
                    writer.add_page(reader_overlay.pages[0])
                else:
                    writer.add_page(pg)

            with open(output_path, "wb") as f_out:
                writer.write(f_out)
        else:
            import shutil
            shutil.copy2(overlay_pdf, output_path)

    finally:
        for p in (img_tmp, overlay_pdf):
            try:
                os.unlink(p)
            except OSError:
                pass


# ─────────────────────────────────────────────────────────────────────────────
# PDF 页面 → PIL 图像
# ─────────────────────────────────────────────────────────────────────────────

def _pdf_page_to_image(pdf_path: str, page_num: int, dpi: int = 300) -> "Image.Image":
    """将 PDF 页面光栅化为 PIL Image。"""
    if HAS_FITZ:
        doc = fitz.open(pdf_path)
        page = doc[page_num]
        zoom = dpi / 72.0
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        doc.close()
        return Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    try:
        from pdf2image import convert_from_path
        images = convert_from_path(pdf_path, dpi=dpi, first_page=page_num + 1, last_page=page_num + 1)
        if images:
            return images[0]
    except ImportError:
        pass

    raise RuntimeError(
        "无法光栅化 PDF。请安装 pymupdf（pip install pymupdf）"
        "或 pdf2image（pip install pdf2image）并安装 poppler。"
    )


# ─────────────────────────────────────────────────────────────────────────────
# 文本搜索辅助
# ─────────────────────────────────────────────────────────────────────────────

def _find_text_in_ocr_results(ocr_results: list, target_text: str, fuzzy: bool = True) -> list:
    """在 OCR 结果中查找与目标文本匹配的条目。"""
    hits = []
    target_lower = target_text.lower().strip()
    for item in ocr_results:
        item_text = item["text"].strip()
        if fuzzy:
            if target_lower in item_text.lower():
                hits.append(item)
        else:
            if item_text == target_text:
                hits.append(item)
    return hits


# ─────────────────────────────────────────────────────────────────────────────
# 完整流水线（文件级）
# ─────────────────────────────────────────────────────────────────────────────

def replace_text_in_image_pdf(
    pdf_path: str,
    old_text: str,
    new_text: str,
    output_path: str = None,
    page_num: int = 0,
    dpi: int = 300,
    lang: str = "chi_sim+eng",
    engine: str = "auto",
    font_path: str = None,
    inpaint_method: str = "telea",
    color: tuple = (0, 0, 0),
) -> bool:
    """完整 OCR 替换流水线：检测 → OCR → 涂抹 → 渲染 → 保存。

    返回 True 表示至少完成一次替换，False 表示未找到目标文本。
    """
    pdf_path = str(pdf_path)

    if output_path is None:
        base, ext = os.path.splitext(pdf_path)
        output_path = f"{base}_ocr_replaced{ext}"

    print(f"[pdf_ocr] 处理: {pdf_path}")
    print(f"[pdf_ocr] 替换 '{old_text}' → '{new_text}'，第 {page_num} 页，{dpi} DPI")

    image_based = is_image_based_pdf(pdf_path, page_num)
    if not image_based:
        print("[pdf_ocr] 页面有可提取文本，仍继续 OCR 流水线")

    print("[pdf_ocr] 光栅化页面...")
    page_image = _pdf_page_to_image(pdf_path, page_num, dpi=dpi)
    print(f"[pdf_ocr] 页面图像尺寸: {page_image.size[0]}x{page_image.size[1]} px")

    print(f"[pdf_ocr] 运行 OCR（engine={engine}, lang={lang}）...")
    ocr_results = ocr_page(page_image, lang=lang, engine=engine)
    print(f"[pdf_ocr] OCR 识别到 {len(ocr_results)} 个文本区域")

    if not ocr_results:
        print("[pdf_ocr] 无 OCR 结果，无法继续")
        return False

    matches = _find_text_in_ocr_results(ocr_results, old_text)
    if not matches:
        print(f"[pdf_ocr] 文本 '{old_text}' 未在 OCR 结果中找到")
        print("[pdf_ocr] 前 10 条 OCR 结果（调试）:")
        for item in ocr_results[:10]:
            print(f"  conf={item['confidence']:.2f}  bbox={item['bbox']}  text={item['text']!r}")
        return False

    print(f"[pdf_ocr] 找到 {len(matches)} 个匹配区域")

    working_image = page_image.copy()
    for i, match in enumerate(matches):
        bbox = match["bbox"]
        print(f"[pdf_ocr] 匹配 {i+1}: bbox={bbox}  conf={match['confidence']:.2f}  text={match['text']!r}")
        working_image = inpaint_region(working_image, bbox, method=inpaint_method)
        working_image = render_text_on_image(
            working_image, new_text, bbox,
            font_path=font_path, color=color,
        )

    print(f"[pdf_ocr] 写入输出: {output_path}")
    replace_page_image(pdf_path, page_num, working_image, output_path)
    print("[pdf_ocr] 完成。")
    return True


# ─────────────────────────────────────────────────────────────────────────────
# 主入口期望的别名（replace_text_ocr）
# ─────────────────────────────────────────────────────────────────────────────

def replace_text_ocr(
    pdf_path: str,
    old_text: str,
    new_text: str,
    output_path: str,
    page_num: int = 0,
) -> bool:
    """replace_text_in_image_pdf 的简化别名，供 pdf_text_replace.py 调用。"""
    return replace_text_in_image_pdf(
        pdf_path=pdf_path,
        old_text=old_text,
        new_text=new_text,
        output_path=output_path,
        page_num=page_num,
    )
