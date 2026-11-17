#!/usr/bin/env python3
"""
pdf_fill_form.py — PDF 表单填写工具
支持双路径：
  路径A：可填字段 PDF（fillable form）── 用 pypdf 检测/填写字段
  路径B：非可填字段 PDF（non-fillable）── 用 pymupdf 转图分析/注释填写

用法：
  python pdf_fill_form.py form.pdf --detect
  python pdf_fill_form.py form.pdf --fill-json values.json --outfile filled.pdf
  python pdf_fill_form.py form.pdf --analyze --outdir ./form_images
  python pdf_fill_form.py form.pdf --annotate-json annotations.json --outfile filled.pdf
"""

import argparse
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from utils import check_scanned_and_warn  # noqa: E402

# ── 依赖检查 ──────────────────────────────────
_missing = []
try:
    import pypdf
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import NameObject, BooleanObject, ArrayObject, TextStringObject
except ImportError:
    _missing.append("pypdf")

try:
    import fitz  # pymupdf
except ImportError:
    _missing.append("pymupdf")

if _missing:
    print(
        f"[错误] 缺少依赖：{', '.join(_missing)}\n"
        f"请运行：pip install {' '.join(_missing)}",
        file=sys.stderr,
    )
    sys.exit(1)


# ─────────────────────────────────────────────
# 路径A：检测可填字段
# ─────────────────────────────────────────────

def detect_fields(pdf_path: str) -> list:
    """
    使用 pypdf 检测 PDF 中的可填字段。

    返回字段列表，每项包含：
        name, type, page（1-indexed）, value（当前值）
    """
    reader = PdfReader(pdf_path)
    fields_info = []

    if reader.get_fields() is None:
        return fields_info

    # 建立字段名 → 页码映射
    field_page_map = {}
    for page_num, page in enumerate(reader.pages, start=1):
        annots = page.get("/Annots", None)
        if annots is None:
            continue
        for annot in annots:
            obj = annot.get_object()
            ft = obj.get("/FT")
            t = obj.get("/T")
            if t is not None:
                field_page_map[str(t)] = {
                    "page": page_num,
                    "ft": str(ft) if ft else None,
                    "rect": [float(v) for v in obj.get("/Rect", [0, 0, 0, 0])],
                }

    for field_name, field_obj in reader.get_fields().items():
        ft = field_obj.get("/FT", "")
        field_type = {
            "/Tx": "text",
            "/Btn": "checkbox",
            "/Ch": "select",
            "/Sig": "signature",
        }.get(str(ft), str(ft))

        # 判断是否为 radio group
        ff = field_obj.get("/Ff", 0)
        if isinstance(ff, int) and (ff & (1 << 15)):
            field_type = "radio_group"

        value = field_obj.get("/V", "")
        if hasattr(value, "__str__"):
            value = str(value)

        page_info = field_page_map.get(field_name, {})

        fields_info.append({
            "name": field_name,
            "type": field_type,
            "page": page_info.get("page", None),
            "rect": page_info.get("rect", []),
            "current_value": value if value not in ("/Off", "None", "") else "",
        })

    return fields_info


# ─────────────────────────────────────────────
# 路径A：填写可填字段
# ─────────────────────────────────────────────

def fill_fields(pdf_path: str, field_values: dict, outfile: str = None) -> str:
    """
    使用 pypdf 填写 PDF 可填字段。

    参数：
        pdf_path: 输入 PDF 路径
        field_values: {field_name: value} 字典
            - text 类型：str
            - checkbox 类型：True/False 或 "/Yes"/"/Off"
            - radio_group 类型：选项名称字符串
        outfile: 输出路径（可选）
    返回：
        输出文件路径
    """
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    writer.append(reader)

    # 填写字段
    writer.update_page_form_field_values(
        writer.pages[0],  # 先填第一页，下面循环全部页
        {},
    )

    # 对每一页都尝试填写
    for page in writer.pages:
        annots = page.get("/Annots", None)
        if annots is None:
            continue
        for annot_ref in annots:
            annot = annot_ref.get_object()
            field_name = annot.get("/T")
            if field_name is None:
                continue
            field_name = str(field_name)
            if field_name not in field_values:
                continue

            value = field_values[field_name]
            ft = annot.get("/FT", "")
            ft_str = str(ft)

            if ft_str == "/Btn":
                # checkbox / radio
                if isinstance(value, bool):
                    v = NameObject("/Yes") if value else NameObject("/Off")
                elif str(value).lower() in ("true", "yes", "1", "/yes"):
                    v = NameObject("/Yes")
                else:
                    v = NameObject("/Off")
                annot.update({
                    NameObject("/V"): v,
                    NameObject("/AS"): v,
                })
            else:
                # text / select
                annot.update({
                    NameObject("/V"): TextStringObject(str(value)),
                    NameObject("/DV"): TextStringObject(str(value)),
                })
                # 标记字段需要外观更新
                annot.update({
                    NameObject("/AP"): annot.get("/AP", ArrayObject()),
                })
                # 设置 NeedAppearances 标志
            print(f"  ✓ 填写字段 [{field_name}] = {value}")

    # 设置 NeedAppearances 以确保 PDF 阅读器渲染填写内容
    if "/AcroForm" in writer._root_object:
        acroform = writer._root_object["/AcroForm"].get_object()
        acroform.update({
            NameObject("/NeedAppearances"): BooleanObject(True)
        })

    out_path = outfile or _default_outfile(pdf_path, "_filled.pdf")
    with open(out_path, "wb") as f:
        writer.write(f)
    print(f"\n[完成] 已填写 {len(field_values)} 个字段 → {out_path}")
    return out_path


# ─────────────────────────────────────────────
# 路径B：转图分析
# ─────────────────────────────────────────────

def analyze_as_images(pdf_path: str, outdir: str = None, dpi: int = 150) -> list:
    """
    使用 pymupdf 将 PDF 每页转为 PNG，输出到 outdir（或临时目录）。
    打印分析提示帮助 AI 助手识别字段位置。

    返回：图片路径列表
    """
    if outdir:
        out_path = Path(outdir)
        out_path.mkdir(parents=True, exist_ok=True)
    else:
        out_path = Path(tempfile.mkdtemp(prefix="pdf_form_"))

    doc = fitz.open(pdf_path)
    image_paths = []
    matrix = fitz.Matrix(dpi / 72, dpi / 72)

    print(f"[分析] 将 PDF 转为图片（{dpi} DPI）→ {out_path}")
    for page_num in range(len(doc)):
        page = doc[page_num]
        pix = page.get_pixmap(matrix=matrix)
        img_file = out_path / f"page_{page_num + 1:03d}.png"
        pix.save(str(img_file))
        image_paths.append(str(img_file))
        print(f"  ✓ 第 {page_num + 1} 页 → {img_file}  ({page.rect.width:.0f}×{page.rect.height:.0f} pt)")

    doc.close()

    print(f"\n[提示] 请查看以下图片，识别需要填写的字段位置，然后构建 annotations.json：")
    print(f"  图片目录：{out_path}")
    print(f"  PDF 坐标系：原点在左上角，单位为 pt（1pt ≈ 0.353mm）")
    print(f"\n  annotations.json 格式示例：")
    print(json.dumps([
        {"page": 1, "x": 150, "y": 200, "text": "张三", "font_size": 11},
        {"page": 1, "x": 350, "y": 200, "text": "2024-03-15", "font_size": 11},
    ], ensure_ascii=False, indent=2))
    print(f"\n  然后运行：")
    print(f"  python pdf_fill_form.py {pdf_path} --annotate-json annotations.json --outfile filled.pdf")

    return image_paths


# ─────────────────────────────────────────────
# 路径B：注释填写
# ─────────────────────────────────────────────

def annotate_pdf(pdf_path: str, annotations: list, outfile: str = None) -> str:
    """
    使用 pymupdf 在 PDF 指定坐标插入文本注释。

    参数：
        pdf_path: 输入 PDF 路径
        annotations: 注释列表，每项格式：
            {"page": 1, "x": 150, "y": 200, "text": "张三", "font_size": 11}
        outfile: 输出路径（可选）
    返回：
        输出文件路径
    """
    doc = fitz.open(pdf_path)

    # 按页分组
    from collections import defaultdict
    by_page = defaultdict(list)
    for ann in annotations:
        page_num = ann.get("page", 1)
        by_page[page_num].append(ann)

    total = 0
    for page_num, items in by_page.items():
        if page_num < 1 or page_num > len(doc):
            print(f"  [警告] 页码 {page_num} 超出范围（共 {len(doc)} 页），跳过", file=sys.stderr)
            continue
        page = doc[page_num - 1]
        for item in items:
            x = float(item.get("x", 0))
            y = float(item.get("y", 0))
            text = str(item.get("text", ""))
            font_size = float(item.get("font_size", 11))
            color = item.get("color", [0, 0, 0])  # RGB 0-1
            if isinstance(color, list) and len(color) == 3:
                color_rgb = tuple(color)
            else:
                color_rgb = (0, 0, 0)

            # 插入文本（使用 insert_text，直接写入 PDF 内容流）
            page.insert_text(
                point=fitz.Point(x, y),
                text=text,
                fontsize=font_size,
                color=color_rgb,
                overlay=True,
            )
            print(f"  ✓ 第 {page_num} 页 ({x}, {y}) → {text!r}")
            total += 1

    out_path = outfile or _default_outfile(pdf_path, "_annotated.pdf")
    doc.save(out_path)
    doc.close()
    print(f"\n[完成] 已插入 {total} 个文本注释 → {out_path}")
    return out_path


# ─────────────────────────────────────────────
# 工具函数
# ─────────────────────────────────────────────

def _default_outfile(pdf_path: str, suffix: str) -> str:
    p = Path(pdf_path)
    return str(p.parent / (p.stem + suffix))


# ─────────────────────────────────────────────
# CLI 入口
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="PDF 表单填写工具（双路径：可填字段 / 注释填写）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
路径A（可填字段 PDF）：
  python pdf_fill_form.py form.pdf --detect
      检测并输出所有可填字段的 JSON 结构

  python pdf_fill_form.py form.pdf --fill-json values.json --outfile filled.pdf
      按 values.json 填写字段并输出 PDF
      values.json 格式：{"姓名": "张三", "日期": "2024-03-15", "同意": true}

路径B（非可填字段 PDF）：
  python pdf_fill_form.py form.pdf --analyze --outdir ./form_images
      将每页转为 PNG，输出分析提示和坐标参考

  python pdf_fill_form.py form.pdf --annotate-json annotations.json --outfile filled.pdf
      按坐标在 PDF 上插入文本
      annotations.json 格式：
        [{"page":1, "x":150, "y":200, "text":"张三", "font_size":11}]
        """,
    )
    parser.add_argument("input", help="输入 PDF 文件路径")

    # 路径A 参数
    parser.add_argument(
        "--detect", action="store_true",
        help="[路径A] 检测并输出可填字段结构 JSON",
    )
    parser.add_argument(
        "--fill-json", metavar="VALUES_JSON",
        help="[路径A] 字段值 JSON 文件路径，填写可填字段",
    )

    # 路径B 参数
    parser.add_argument(
        "--analyze", action="store_true",
        help="[路径B] 将 PDF 转为图片，输出坐标分析提示",
    )
    parser.add_argument(
        "--annotate-json", metavar="ANNOTATIONS_JSON",
        help="[路径B] 注释坐标 JSON 文件路径，在 PDF 上插入文本",
    )

    # 公共参数
    parser.add_argument(
        "--outfile", default=None,
        help="输出 PDF 文件路径（--fill-json / --annotate-json 模式有效）",
    )
    parser.add_argument(
        "--outdir", default=None,
        help="图片输出目录（--analyze 模式有效）",
    )
    parser.add_argument(
        "--dpi", type=int, default=150,
        help="图片分辨率 DPI（--analyze 模式有效，默认 150）",
    )

    args = parser.parse_args()

    pdf_path = args.input
    if not Path(pdf_path).exists():
        print(f"[错误] 文件不存在：{pdf_path}", file=sys.stderr)
        sys.exit(1)

    check_scanned_and_warn(pdf_path)

    # ── 路径A：检测字段 ──
    if args.detect:
        fields = detect_fields(pdf_path)
        if not fields:
            print("[提示] 未检测到可填字段，该 PDF 为非可填类型。")
            print("       建议使用 --analyze 转图后再用 --annotate-json 填写。")
        else:
            print(f"[检测] 发现 {len(fields)} 个可填字段：\n")
            print(json.dumps(fields, ensure_ascii=False, indent=2))
        return

    # ── 路径A：填写字段 ──
    if args.fill_json:
        with open(args.fill_json, "r", encoding="utf-8") as f:
            field_values = json.load(f)
        fill_fields(pdf_path, field_values, outfile=args.outfile)
        return

    # ── 路径B：转图分析 ──
    if args.analyze:
        analyze_as_images(pdf_path, outdir=args.outdir, dpi=args.dpi)
        return

    # ── 路径B：注释填写 ──
    if args.annotate_json:
        with open(args.annotate_json, "r", encoding="utf-8") as f:
            annotations = json.load(f)
        annotate_pdf(pdf_path, annotations, outfile=args.outfile)
        return

    # 未指定任何操作
    parser.print_help()


if __name__ == "__main__":
    main()
