#!/usr/bin/env python3
"""
发票合并工具
1. PDF 文件：两两合并一页（上下结构），输出 1 个 PDF
2. 图片文件：四个合并一页（上半 1-2，下半 3-4），输出 1 个 PDF
3. 输出目录：输入目录下 YYYYMMDD--已合并
"""

import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageOps
    from pypdf import PageObject, PdfReader, PdfWriter, Transformation
    from pypdf.generic import DecodedStreamObject, NameObject
except ImportError as e:
    print(f"缺少依赖: {e}")
    print("脚本当前实际使用的第三方依赖只有 pypdf 和 Pillow。")
    print("请先安装 Python 依赖，例如：")
    print("python -m pip install pypdf Pillow")
    sys.exit(1)

A4_WIDTH_PT = 595.2756
A4_HEIGHT_PT = 841.8898
MARGIN_PT = 15.0
CUT_LINE_SAFE_MARGIN_PT = 15.0
CUT_LINE_WIDTH_PT = 0.6
CUT_LINE_DASH_PT = 6.0
CUT_LINE_GAP_PT = 3.0
CUT_LINE_GRAY = 0.55

IMAGE_DPI = 150
PIXELS_PER_PT = IMAGE_DPI / 72
A4_WIDTH_PX = int(round(A4_WIDTH_PT * PIXELS_PER_PT))
A4_HEIGHT_PX = int(round(A4_HEIGHT_PT * PIXELS_PER_PT))
IMAGE_OUTER_MARGIN_PX = int(round(MARGIN_PT * PIXELS_PER_PT))
IMAGE_CELL_PADDING_PX = 0
IMAGE_COL_GAP_PX = int(round(MARGIN_PT * PIXELS_PER_PT))
IMAGE_ROW_GAP_PX = int(round(CUT_LINE_SAFE_MARGIN_PT * 2 * PIXELS_PER_PT))
IMAGE_CUT_LINE_WIDTH_PX = max(1, int(round(CUT_LINE_WIDTH_PT * PIXELS_PER_PT)))
IMAGE_CUT_LINE_DASH_PX = max(1, int(round(CUT_LINE_DASH_PT * PIXELS_PER_PT)))
IMAGE_CUT_LINE_GAP_PX = max(1, int(round(CUT_LINE_GAP_PT * PIXELS_PER_PT)))
IMAGE_CUT_LINE_GRAY = int(round(CUT_LINE_GRAY * 255))
MERGED_OUTPUT_DIR_PATTERN = re.compile(r"^\d{8}--已合并$")


def get_files(directory, extensions):
    """获取目录下指定扩展名的文件（不区分大小写）"""
    ext_set = {ext.lower() for ext in extensions}
    return sorted(
        p for p in Path(directory).iterdir() if p.is_file() and p.suffix.lower() in ext_set
    )


def create_output_dir(input_dir):
    """优先复用现有输出目录，否则在输入目录下创建：YYYYMMDD--已合并"""
    if is_generated_output_dir(input_dir):
        input_dir.mkdir(parents=True, exist_ok=True)
        return input_dir

    ts = datetime.now().strftime("%Y%m%d")
    output_dir = input_dir / f"{ts}--已合并"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def indexed_output_path(output_dir, base_name):
    """优先使用 base_name.pdf，重名时追加序号"""
    first = output_dir / f"{base_name}.pdf"
    if not first.exists():
        return first

    idx = 1
    while True:
        output = output_dir / f"{base_name}_{idx:03d}.pdf"
        if not output.exists():
            return output
        idx += 1


def is_generated_output_dir(path):
    """判断当前目录是否为本工具生成的输出目录"""
    return MERGED_OUTPUT_DIR_PATTERN.match(path.name) is not None


def is_generated_output_file(path):
    """跳过本工具之前生成的合并文件，避免二次合并导致版式继续缩小"""
    if path.suffix.lower() != ".pdf":
        return False

    stem = path.stem
    return (
        stem == "发票合并"
        or stem == "账单合并"
        or stem.startswith("发票合并_")
        or stem.startswith("账单合并_")
    )


def filter_input_files(files):
    """过滤工具自身生成的输出文件"""
    skipped_files = [path for path in files if is_generated_output_file(path)]
    kept_files = [path for path in files if not is_generated_output_file(path)]
    return kept_files, skipped_files


def get_pdf_layout_boxes():
    """统一的 PDF 排版安全区：外边距 15pt，中线两侧各留 15pt"""
    mid_y = A4_HEIGHT_PT / 2
    left_x = MARGIN_PT
    right_x = A4_WIDTH_PT - MARGIN_PT
    top_box = (
        left_x,
        mid_y + CUT_LINE_SAFE_MARGIN_PT,
        right_x,
        A4_HEIGHT_PT - MARGIN_PT,
    )
    bottom_box = (
        left_x,
        MARGIN_PT,
        right_x,
        mid_y - CUT_LINE_SAFE_MARGIN_PT,
    )
    return top_box, bottom_box


def get_image_layout_boxes():
    """统一的图片排版安全区，确保内容不会压到中间裁剪线"""
    usable_w = A4_WIDTH_PX - 2 * IMAGE_OUTER_MARGIN_PX - IMAGE_COL_GAP_PX
    usable_h = A4_HEIGHT_PX - 2 * IMAGE_OUTER_MARGIN_PX - IMAGE_ROW_GAP_PX
    cell_w = usable_w // 2
    cell_h = usable_h // 2

    left_x1 = IMAGE_OUTER_MARGIN_PX
    left_x2 = left_x1 + cell_w
    right_x1 = left_x2 + IMAGE_COL_GAP_PX
    right_x2 = right_x1 + cell_w

    top_y1 = IMAGE_OUTER_MARGIN_PX
    top_y2 = top_y1 + cell_h
    bottom_y1 = top_y2 + IMAGE_ROW_GAP_PX
    bottom_y2 = bottom_y1 + cell_h

    boxes = [
        (left_x1, top_y1, left_x2, top_y2),
        (right_x1, top_y1, right_x2, top_y2),
        (left_x1, bottom_y1, left_x2, bottom_y2),
        (right_x1, bottom_y1, right_x2, bottom_y2),
    ]
    cut_line_y = (top_y2 + bottom_y1) // 2
    return boxes, cut_line_y


def merge_page_into_box(target_page, src_page, x1, y1, x2, y2):
    """将 src_page 按比例缩放并居中放入目标区域"""
    source_box = src_page.cropbox
    src_w = float(source_box.width)
    src_h = float(source_box.height)
    src_x = float(source_box.left)
    src_y = float(source_box.bottom)

    box_w = x2 - x1
    box_h = y2 - y1
    if src_w <= 0 or src_h <= 0 or box_w <= 0 or box_h <= 0:
        return

    scale = min(box_w / src_w, box_h / src_h)
    draw_w = src_w * scale
    draw_h = src_h * scale

    tx = x1 + (box_w - draw_w) / 2 - src_x * scale
    ty = y1 + (box_h - draw_h) / 2 - src_y * scale

    transform = Transformation().scale(scale, scale).translate(tx, ty)
    target_page.merge_transformed_page(src_page, transform)


def create_pdf_cut_line_overlay():
    """创建仅包含中间裁剪虚线的覆盖页"""
    y = A4_HEIGHT_PT / 2
    x1 = MARGIN_PT
    x2 = A4_WIDTH_PT - MARGIN_PT

    content = (
        "q\n"
        f"{CUT_LINE_WIDTH_PT:.2f} w\n"
        f"[{CUT_LINE_DASH_PT:.2f} {CUT_LINE_GAP_PT:.2f}] 0 d\n"
        f"{CUT_LINE_GRAY:.2f} {CUT_LINE_GRAY:.2f} {CUT_LINE_GRAY:.2f} RG\n"
        f"{x1:.2f} {y:.2f} m\n"
        f"{x2:.2f} {y:.2f} l\n"
        "S\n"
        "Q\n"
    )

    overlay = PageObject.create_blank_page(width=A4_WIDTH_PT, height=A4_HEIGHT_PT)
    stream = DecodedStreamObject()
    stream.set_data(content.encode("ascii"))
    overlay[NameObject("/Contents")] = stream
    return overlay


def add_pdf_cut_line(page):
    """将裁剪线覆盖页叠加到目标页"""
    page.merge_page(create_pdf_cut_line_overlay())


def merge_pdfs_two(pdf_files, output_dir):
    """PDF 两两合并（上下结构），输出 1 个 PDF（多页）"""
    if not pdf_files:
        return None

    output_file = indexed_output_path(output_dir, "发票合并")
    writer = PdfWriter()
    top_box, bottom_box = get_pdf_layout_boxes()

    for i in range(0, len(pdf_files), 2):
        pair = pdf_files[i : i + 2]
        page = writer.add_blank_page(width=A4_WIDTH_PT, height=A4_HEIGHT_PT)

        try:
            top_reader = PdfReader(str(pair[0]))
            if top_reader.pages:
                merge_page_into_box(
                    page,
                    top_reader.pages[0],
                    *top_box,
                )
        except Exception as e:
            print(f"  ⚠ PDF 读取失败: {pair[0].name}, {e}")

        if len(pair) > 1:
            try:
                bottom_reader = PdfReader(str(pair[1]))
                if bottom_reader.pages:
                    merge_page_into_box(
                        page,
                        bottom_reader.pages[0],
                        *bottom_box,
                    )
            except Exception as e:
                print(f"  ⚠ PDF 读取失败: {pair[1].name}, {e}")

        add_pdf_cut_line(page)
        print(
            f"✅ PDF 合并: {pair[0].name}"
            f" + {pair[1].name if len(pair) > 1 else ''}"
        )

    with output_file.open("wb") as f:
        writer.write(f)

    print(f"📄 PDF 输出: {output_file.name}")
    return output_file


def paste_image_to_box(page_img, img_path, box):
    """将图片按比例缩放并居中粘贴到 box 区域"""
    x1, y1, x2, y2 = box
    target_w = x2 - x1 - IMAGE_CELL_PADDING_PX * 2
    target_h = y2 - y1 - IMAGE_CELL_PADDING_PX * 2
    if target_w <= 0 or target_h <= 0:
        return

    with Image.open(img_path) as img:
        img = ImageOps.exif_transpose(img).convert("RGB")
        ratio = min(target_w / img.width, target_h / img.height)
        new_w = max(1, int(round(img.width * ratio)))
        new_h = max(1, int(round(img.height * ratio)))

        resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        px = x1 + (x2 - x1 - new_w) // 2
        py = y1 + (y2 - y1 - new_h) // 2
        page_img.paste(resized, (px, py))


def draw_image_cut_line(page_img, y):
    """在图片页面中间绘制虚线裁剪线"""
    draw = ImageDraw.Draw(page_img)
    x_start = IMAGE_OUTER_MARGIN_PX
    x_end = A4_WIDTH_PX - IMAGE_OUTER_MARGIN_PX
    x = x_start
    while x < x_end:
        x2 = min(x + IMAGE_CUT_LINE_DASH_PX, x_end)
        draw.line(
            [(x, y), (x2, y)],
            fill=(IMAGE_CUT_LINE_GRAY, IMAGE_CUT_LINE_GRAY, IMAGE_CUT_LINE_GRAY),
            width=IMAGE_CUT_LINE_WIDTH_PX,
        )
        x += IMAGE_CUT_LINE_DASH_PX + IMAGE_CUT_LINE_GAP_PX


def merge_images_four(image_files, output_dir):
    """图片四个合并一页（上半 1-2，下半 3-4），输出 1 个 PDF（多页）"""
    if not image_files:
        return None

    output_file = indexed_output_path(output_dir, "账单合并")
    pages = []
    boxes, cut_line_y = get_image_layout_boxes()

    for i in range(0, len(image_files), 4):
        group = image_files[i : i + 4]
        page = Image.new("RGB", (A4_WIDTH_PX, A4_HEIGHT_PX), "white")

        for idx, img_path in enumerate(group):
            try:
                paste_image_to_box(page, img_path, boxes[idx])
            except Exception as e:
                print(f"  ⚠ 图片加载失败: {img_path.name}, {e}")

        draw_image_cut_line(page, cut_line_y)
        pages.append(page)
        print(f"✅ 图片合并: {len(group)} 张")

    first, *rest = pages
    first.save(
        output_file,
        "PDF",
        resolution=IMAGE_DPI,
        save_all=True,
        append_images=rest,
    )

    for page in pages:
        page.close()

    print(f"🖼️ 图片 PDF 输出: {output_file.name}")
    return output_file


def process_directory(input_path):
    """处理目录"""
    input_path = Path(input_path).resolve()

    if not input_path.exists() or not input_path.is_dir():
        print(f"❌ 目录不存在: {input_path}")
        return []

    pdf_files, skipped_pdf_files = filter_input_files(get_files(input_path, [".pdf"]))
    image_files = get_files(input_path, [".jpg", ".jpeg", ".png"])

    print(f"📄 找到 {len(pdf_files)} 个 PDF")
    print(f"🖼️ 找到 {len(image_files)} 个图片")
    if skipped_pdf_files:
        print(f"↩ 已跳过 {len(skipped_pdf_files)} 个历史合并 PDF，避免重复缩版")

    if not pdf_files and not image_files:
        print("❌ 未找到可处理文件")
        return []

    output_dir = create_output_dir(input_path)
    print(f"📁 输出目录: {output_dir.name}")
    if output_dir == input_path and is_generated_output_dir(input_path):
        print("↩ 当前目录已是输出目录，将直接复用并按编号生成新文件")

    outputs = []

    pdf_output = merge_pdfs_two(pdf_files, output_dir)
    if pdf_output:
        outputs.append(pdf_output)

    image_output = merge_images_four(image_files, output_dir)
    if image_output:
        outputs.append(image_output)

    print(f"\n🎉 完成！共生成 {len(outputs)} 个文件")
    for out in outputs:
        print(f"   - {out.name}")

    return outputs


def open_output_files(output_files):
    """按操作系统使用默认程序打开输出文件"""
    for output_file in output_files:
        try:
            if sys.platform == "darwin":
                subprocess.run(["open", str(output_file)], check=False)
            elif sys.platform == "win32":
                os.startfile(str(output_file))
            elif sys.platform.startswith("linux"):
                subprocess.run(["xdg-open", str(output_file)], check=False)
        except Exception as e:
            print(f"⚠ 自动打开失败: {output_file.name}, {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 merge_invoices.py <目录路径>")
        sys.exit(1)

    output_files = process_directory(sys.argv[1])

    if output_files:
        open_output_files(output_files)
