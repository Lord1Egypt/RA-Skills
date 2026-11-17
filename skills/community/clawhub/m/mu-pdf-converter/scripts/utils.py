#!/usr/bin/env python3
"""
utils.py - PDF 转换公共工具函数
mu-pdf-converter 共享工具集
"""

import os
import sys
from pathlib import Path


# ─────────────────────────────────────────────
# 依赖检查
# ─────────────────────────────────────────────

def check_dependencies():
    """检查所有必要依赖是否安装"""
    missing = []
    try:
        import fitz  # noqa: F401
    except ImportError:
        missing.append("pymupdf")
    try:
        import pdfplumber  # noqa: F401
    except ImportError:
        missing.append("pdfplumber")
    try:
        from pptx.util import Emu  # noqa: F401
    except ImportError:
        missing.append("python-pptx")
    try:
        from docx import Document  # noqa: F401
    except ImportError:
        missing.append("python-docx")
    try:
        import openpyxl  # noqa: F401
    except ImportError:
        missing.append("openpyxl")

    if missing:
        print(
            f"[错误] 缺少以下依赖包：{', '.join(missing)}\n"
            f"请运行：pip install {' '.join(missing)}",
            file=sys.stderr,
        )
        sys.exit(1)


# ─────────────────────────────────────────────
# 坐标转换
# ─────────────────────────────────────────────

PT_TO_EMU = 12700  # 1 point = 12700 EMU


def pt_to_emu(pt: float) -> int:
    """将 PDF 点坐标转换为 pptx EMU"""
    return int(pt * PT_TO_EMU)


def bbox_to_emu(bbox, page_height_pt: float = None):
    """
    将 fitz/pdfplumber bbox (x0, y0, x1, y1) 转换为 pptx (left, top, width, height) EMU。

    参数:
        bbox: (x0, y0, x1, y1) 单位 pt，原点左上角
        page_height_pt: 若提供，用于从底部坐标系转换（pdfplumber 某些版本 y 轴向下）
    返回:
        (left, top, width, height) 单位 EMU
    """
    x0, y0, x1, y1 = bbox
    width = x1 - x0
    height = y1 - y0
    return (
        pt_to_emu(x0),
        pt_to_emu(y0),
        pt_to_emu(width),
        pt_to_emu(height),
    )


def scale_bbox_to_slide(bbox, pdf_width_pt: float, pdf_height_pt: float,
                         slide_width_emu: int, slide_height_emu: int):
    """
    将 PDF bbox 缩放并映射到 pptx slide 坐标系（EMU）。

    适用于 PDF 尺寸与 slide 尺寸不一致时的等比例缩放。
    """
    x0, y0, x1, y1 = bbox
    scale_x = slide_width_emu / (pdf_width_pt * PT_TO_EMU)
    scale_y = slide_height_emu / (pdf_height_pt * PT_TO_EMU)

    left = int(x0 * PT_TO_EMU * scale_x)
    top = int(y0 * PT_TO_EMU * scale_y)
    width = int((x1 - x0) * PT_TO_EMU * scale_x)
    height = int((y1 - y0) * PT_TO_EMU * scale_y)
    return left, top, width, height


# ─────────────────────────────────────────────
# 颜色转换
# ─────────────────────────────────────────────

def fitz_color_to_rgb(color) -> tuple:
    """
    将 fitz 颜色值转换为 (r, g, b) 0-255 元组。

    fitz 颜色可以是：
    - int (0xRRGGBB)
    - tuple (r, g, b) 0.0-1.0
    - None → 返回黑色 (0, 0, 0)
    """
    if color is None:
        return (0, 0, 0)
    if isinstance(color, int):
        r = (color >> 16) & 0xFF
        g = (color >> 8) & 0xFF
        b = color & 0xFF
        return (r, g, b)
    if isinstance(color, (tuple, list)):
        if len(color) == 3:
            return tuple(int(c * 255) for c in color)
        if len(color) == 4:  # CMYK or RGBA
            return tuple(int(c * 255) for c in color[:3])
    return (0, 0, 0)


def fitz_color_to_pptx(color):
    """将 fitz 颜色转换为 pptx RGBColor 对象"""
    try:
        from pptx.dml.color import RGBColor
    except ImportError:
        return None
    r, g, b = fitz_color_to_rgb(color)
    return RGBColor(r, g, b)


# ─────────────────────────────────────────────
# 中文字体映射
# ─────────────────────────────────────────────

# PDF 中常见的中文字体名称映射到 Office 安全字体
_FONT_MAP = {
    # 宋体族
    "simsun": "SimSun",
    "songti": "SimSun",
    "song": "SimSun",
    "nsimsun": "NSimSun",
    # 黑体族
    "simhei": "SimHei",
    "heiti": "SimHei",
    "hei": "SimHei",
    # 微软雅黑族
    "microsoftyahei": "Microsoft YaHei",
    "yahei": "Microsoft YaHei",
    "msyh": "Microsoft YaHei",
    # 仿宋族
    "fangsong": "FangSong",
    "fs": "FangSong",
    # 楷体族
    "kaiti": "KaiTi",
    "kai": "KaiTi",
    "simkai": "KaiTi",
    # 苹方 (macOS)
    "pingfang": "PingFang SC",
    "pingfangsc": "PingFang SC",
    # 思源 (Adobe/Google)
    "sourcehansans": "Source Han Sans CN",
    "noto": "Noto Sans CJK SC",
    # 西文回退
    "arial": "Arial",
    "times": "Times New Roman",
    "helvetica": "Helvetica",
    "courier": "Courier New",
}

_DEFAULT_CJK_FONT = "Microsoft YaHei"
_DEFAULT_LATIN_FONT = "Arial"


def map_font_name(font_name: str) -> str:
    """
    将 PDF 字体名称映射到 Office 可识别的字体名称。
    优先匹配 CJK 字体，找不到时回退到 Arial。
    """
    if not font_name:
        return _DEFAULT_LATIN_FONT
    normalized = font_name.lower().replace("-", "").replace("_", "").replace(" ", "")
    for key, value in _FONT_MAP.items():
        if key in normalized:
            return value
    # 如果包含中文字符区间标识，默认用雅黑
    cjk_hints = ["cjk", "chinese", "cn", "sc", "tc", "gb", "big5", "hans", "hant"]
    for hint in cjk_hints:
        if hint in normalized:
            return _DEFAULT_CJK_FONT
    return font_name  # 原样返回，让 Office 自行解析


# ─────────────────────────────────────────────
# 扫描件检测
# ─────────────────────────────────────────────

def is_scanned_pdf(pdf_path: str, sample_pages: int = 3, min_chars: int = 20) -> bool:
    """
    检测 PDF 是否为扫描件（无文本层）。

    策略：抽取前 N 页，统计可提取字符数量；
    若平均字符数低于阈值，则判断为扫描件。

    参数:
        pdf_path: PDF 文件路径
        sample_pages: 抽样页数（从开头）
        min_chars: 每页平均最少字符数阈值
    返回:
        True 表示扫描件，False 表示有文本层
    """
    try:
        import fitz
        doc = fitz.open(pdf_path)
        total_chars = 0
        pages_checked = min(sample_pages, len(doc))
        if pages_checked == 0:
            return True
        for i in range(pages_checked):
            page = doc[i]
            text = page.get_text("text")
            total_chars += len(text.strip())
        doc.close()
        avg_chars = total_chars / pages_checked
        return avg_chars < min_chars
    except Exception as e:
        print(f"[警告] 扫描件检测失败：{e}", file=sys.stderr)
        return False


# ─────────────────────────────────────────────
# 输出路径生成
# ─────────────────────────────────────────────

def generate_output_path(input_path: str, suffix: str, outfile: str = None,
                          outdir: str = None) -> str:
    """
    生成输出文件路径。

    优先级：
    1. 如果提供了 outfile，直接使用
    2. 如果提供了 outdir，在 outdir 下生成文件名
    3. 否则在输入文件同目录下生成

    参数:
        input_path: 输入 PDF 路径
        suffix: 输出后缀，如 '.pptx', '.xlsx'
        outfile: 显式指定的输出文件路径
        outdir: 输出目录
    返回:
        输出文件绝对路径
    """
    if outfile:
        return str(Path(outfile).resolve())

    stem = Path(input_path).stem
    filename = f"{stem}{suffix}"

    if outdir:
        os.makedirs(outdir, exist_ok=True)
        return str(Path(outdir) / filename)

    return str(Path(input_path).parent / filename)


# ─────────────────────────────────────────────
# 页面范围解析
# ─────────────────────────────────────────────

def parse_page_range(pages_str: str, total_pages: int) -> list:
    """
    解析页面范围字符串，返回 0-indexed 页码列表。

    支持格式：
    - "all" → 所有页面
    - "1" → 第 1 页（1-indexed）
    - "1-3" → 第 1-3 页
    - "1,3,5" → 第 1、3、5 页
    - "1-3,5,7-9" → 混合格式
    """
    if not pages_str or pages_str.strip().lower() == "all":
        return list(range(total_pages))

    result = []
    parts = pages_str.replace(" ", "").split(",")
    for part in parts:
        if "-" in part:
            start_s, end_s = part.split("-", 1)
            start = int(start_s) - 1  # 转 0-indexed
            end = int(end_s) - 1
            start = max(0, min(start, total_pages - 1))
            end = max(0, min(end, total_pages - 1))
            result.extend(range(start, end + 1))
        else:
            idx = int(part) - 1
            if 0 <= idx < total_pages:
                result.append(idx)

    # 去重并保持顺序
    seen = set()
    ordered = []
    for p in result:
        if p not in seen:
            seen.add(p)
            ordered.append(p)
    return ordered


# ─────────────────────────────────────────────
# 表格 bbox 重叠检测
# ─────────────────────────────────────────────

def bbox_overlap(bbox_a, bbox_b, threshold: float = 0.3) -> bool:
    """
    判断两个 bbox 是否重叠超过阈值。

    参数:
        bbox_a, bbox_b: (x0, y0, x1, y1)
        threshold: 重叠面积占 bbox_a 面积的比例阈值
    返回:
        True 表示显著重叠
    """
    ax0, ay0, ax1, ay1 = bbox_a
    bx0, by0, bx1, by1 = bbox_b

    # 计算交集
    ix0 = max(ax0, bx0)
    iy0 = max(ay0, by0)
    ix1 = min(ax1, bx1)
    iy1 = min(ay1, by1)

    if ix0 >= ix1 or iy0 >= iy1:
        return False  # 无交集

    intersection = (ix1 - ix0) * (iy1 - iy0)
    area_a = (ax1 - ax0) * (ay1 - ay0)

    if area_a <= 0:
        return False

    return (intersection / area_a) >= threshold


def is_in_table_region(text_bbox, table_bboxes: list, threshold: float = 0.3) -> bool:
    """判断文本块是否位于任意表格区域内"""
    for tbl_bbox in table_bboxes:
        if bbox_overlap(text_bbox, tbl_bbox, threshold):
            return True
    return False


# ─────────────────────────────────────────────
# MarkItDown Markdown 表格解析（公共函数）
# ─────────────────────────────────────────────

def parse_markdown_tables(markdown_text: str) -> list:
    """
    从 markitdown 输出的 Markdown 文本中解析出所有表格，返回二维列表的列表。
    每个表格是 list[list[str]]，外层是行，内层是单元格。
    """
    tables = []
    current_table = []
    for line in markdown_text.split('\n'):
        line = line.strip()
        if line.startswith('|') and line.endswith('|'):
            cells = [c.strip() for c in line.split('|')[1:-1]]
            # 跳过分隔行 | --- | --- |
            if all(set(c.replace('-', '').replace(' ', '')) == set() for c in cells):
                continue
            current_table.append(cells)
        else:
            if current_table:
                tables.append(current_table)
                current_table = []
    if current_table:
        tables.append(current_table)
    return tables


# ─────────────────────────────────────────────
# 扫描件智能拦截
# ─────────────────────────────────────────────

def check_scanned_and_warn(pdf_path: str, allow_continue: bool = False) -> bool:
    """
    检测扫描件并给出友好提示和 OCR 解决方案。

    参数:
        pdf_path: PDF 文件路径
        allow_continue: True 时仅警告不退出（用于 pdf_to_images 等场景）
    返回:
        True = 是扫描件
    """
    if is_scanned_pdf(pdf_path):
        stem = Path(pdf_path).stem
        ocr_path = str(Path(pdf_path).parent / f"{stem}_ocr.pdf")
        print("\n" + "=" * 60, file=sys.stderr)
        print("⚠️  检测到此 PDF 为扫描件（无文本层）", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        if allow_continue:
            print("\n[提示] 扫描件转图片可正常工作，但转Word/Excel/PPT需先OCR。", file=sys.stderr)
        else:
            print("\n当前工具无法从扫描件中提取文本/表格。", file=sys.stderr)
            print("建议先用 OCR 添加文本层：\n", file=sys.stderr)
            print("  pip install ocrmypdf", file=sys.stderr)
            print(f"  ocrmypdf '{pdf_path}' '{ocr_path}'", file=sys.stderr)
            print(f"\n然后用生成的 {Path(ocr_path).name} 重新运行本工具。\n", file=sys.stderr)
            sys.exit(2)
        return True
    return False


# ─────────────────────────────────────────────
# XY-Cut 版面分析 + 列对齐表格识别（v2 增强版）
# 参考 docling 的 Grid Projection 思路，纯规则实现，零额外依赖
# v2 改进：自适应 gap、置信度评分、合并单元格推断、区域预筛
# ─────────────────────────────────────────────

def _cluster_values(values: list, gap: float) -> list:
    """
    将一组数值按间距 gap 聚类，返回各簇的代表值（均值）。
    用于 XY-Cut 的投影切割，以及列对齐的列边界聚类。
    """
    if not values:
        return []
    sorted_vals = sorted(set(values))
    clusters = [[sorted_vals[0]]]
    for v in sorted_vals[1:]:
        if v - clusters[-1][-1] <= gap:
            clusters[-1].append(v)
        else:
            clusters.append([v])
    return [sum(c) / len(c) for c in clusters]


def _compute_adaptive_col_gap(words: list, page_width: float) -> float:
    """
    v2 改进1：自适应列间距阈值。
    基于词间距统计（中位数×2.5），而非固定页面比例。
    回退值：page_width * 0.015（兼容旧行为）。
    """
    if len(words) < 4:
        return page_width * 0.015

    # 按行分组（top 相近的词为一行）
    sorted_by_top = sorted(words, key=lambda w: w['top'])
    line_gap_threshold = page_width * 0.01  # 用于判断同一行

    # 收集同行相邻词的 x 间距
    x_gaps = []
    line_start = 0
    for i in range(1, len(sorted_by_top)):
        if sorted_by_top[i]['top'] - sorted_by_top[line_start]['top'] > line_gap_threshold * 2:
            # 处理当前行
            line_words = sorted(sorted_by_top[line_start:i], key=lambda w: w['x0'])
            for j in range(1, len(line_words)):
                gap = line_words[j]['x0'] - line_words[j - 1]['x1']
                if gap > 0:
                    x_gaps.append(gap)
            line_start = i
    # 最后一行
    line_words = sorted(sorted_by_top[line_start:], key=lambda w: w['x0'])
    for j in range(1, len(line_words)):
        gap = line_words[j]['x0'] - line_words[j - 1]['x1']
        if gap > 0:
            x_gaps.append(gap)

    if not x_gaps:
        return page_width * 0.015

    x_gaps.sort()
    median_gap = x_gaps[len(x_gaps) // 2]
    # 列间距应显著大于词间距：取中位数的 2.5 倍
    adaptive_gap = median_gap * 2.5
    # 但不能小于最小合理值，也不能大于页宽的 12%
    return max(page_width * 0.008, min(adaptive_gap, page_width * 0.12))


def _compute_table_confidence(grid: dict, row_indices: list, col_indices: list,
                               col_centers: list, norm_words: list) -> float:
    """
    v2 改进3：表格置信度评分（0.0-1.0）。
    综合三个维度：列对齐方差、行填充率、空单元格占比。
    """
    n_rows = len(row_indices)
    n_cols = len(col_indices)
    total_cells = n_rows * n_cols
    if total_cells == 0:
        return 0.0

    # 维度1：行填充率（有内容的单元格 / 总单元格）
    filled = sum(1 for ri in row_indices for ci in col_indices if grid.get((ri, ci), ''))
    fill_rate = filled / total_cells

    # 维度2：列对齐质量（各列的x0标准差，越小越好）
    col_x0_stds = []
    for ci in col_indices:
        col_word_x0s = [w['x0'] for w in norm_words
                        if abs(w['x0'] - col_centers[ci]) < (col_centers[1] - col_centers[0]) * 0.6
                        ] if len(col_centers) > 1 else []
        if len(col_word_x0s) >= 2:
            mean_x = sum(col_word_x0s) / len(col_word_x0s)
            variance = sum((x - mean_x) ** 2 for x in col_word_x0s) / len(col_word_x0s)
            col_x0_stds.append(variance ** 0.5)

    if col_x0_stds:
        avg_std = sum(col_x0_stds) / len(col_x0_stds)
        # 标准差越小分越高，超过5pt开始扣分
        align_score = max(0.0, 1.0 - avg_std / 10.0)
    else:
        align_score = 0.5  # 无法评估时给中间分

    # 维度3：行一致性（每行的列数应相近）
    row_fill_counts = [sum(1 for ci in col_indices if grid.get((ri, ci), '')) for ri in row_indices]
    if row_fill_counts:
        max_fill = max(row_fill_counts)
        min_fill = min(row_fill_counts)
        consistency = min_fill / max_fill if max_fill > 0 else 0
    else:
        consistency = 0

    # 综合评分：填充率×0.4 + 对齐×0.35 + 一致性×0.25
    confidence = fill_rate * 0.40 + align_score * 0.35 + consistency * 0.25
    return round(confidence, 3)


def xy_cut_extract_tables(words: list, page_width: float, page_height: float,
                           col_gap: float = None, row_gap: float = None,
                           min_cols: int = 2, min_rows: int = 2,
                           min_confidence: float = 0.35) -> list:
    """
    基于 XY-Cut 的无边框表格识别（v2 增强版），返回二维字符串列表的列表。

    v2 改进：
      - 自适应 col_gap（基于词间距统计）
      - 区域预筛（Y轴大间隙切割，只对候选区域做 XY-Cut）
      - 置信度评分（低于阈值的"假表格"被过滤）
      - 宽文本合并单元格推断

    参数：
        words: 词语列表，每项为 dict:
               {'x0':float,'top':float,'x1':float,'bottom':float,'text':str}
               或 pypdfium2 格式 (x0,y0,x1,y1,text) 元组
        page_width, page_height: 页面尺寸（pt）
        col_gap: 列聚类间距阈值（None=自适应计算）
        row_gap: 行聚类间距阈值（默认 page_height * 0.008）
        min_cols: 最少列数，少于此值不视为表格
        min_rows: 最少行数，少于此值不视为表格
        min_confidence: 最低置信度阈值（默认0.35，低于此值的候选表格被丢弃）
    返回：
        tables: list of 2D list，每个 2D list 是一张表格
    """
    if not words:
        return []

    row_gap = row_gap or page_height * 0.008

    # 标准化 words 格式
    norm_words = []
    for w in words:
        if isinstance(w, dict):
            norm_words.append({
                'x0': float(w.get('x0', 0)),
                'top': float(w.get('top', w.get('y0', 0))),
                'x1': float(w.get('x1', 0)),
                'bottom': float(w.get('bottom', w.get('y1', 0))),
                'text': str(w.get('text', '')).strip(),
            })
        elif isinstance(w, (list, tuple)) and len(w) >= 5:
            norm_words.append({
                'x0': float(w[0]), 'top': float(w[1]),
                'x1': float(w[2]), 'bottom': float(w[3]),
                'text': str(w[4]).strip(),
            })

    norm_words = [w for w in norm_words if w['text']]
    if len(norm_words) < min_cols * min_rows:
        return []

    # v2 改进1：自适应 col_gap
    if col_gap is None:
        col_gap = _compute_adaptive_col_gap(norm_words, page_width)

    # 列聚类：对所有词的 x0 做聚类得到列中心
    x0_vals = [w['x0'] for w in norm_words]
    col_centers = _cluster_values(x0_vals, col_gap)
    if len(col_centers) < min_cols:
        return []

    # 行聚类：对所有词的 top 做聚类得到行中心
    top_vals = [w['top'] for w in norm_words]
    row_centers = _cluster_values(top_vals, row_gap)
    if len(row_centers) < min_rows:
        return []

    # 将每个词分配到 (row_idx, col_idx)
    def _nearest_idx(val, centers):
        return min(range(len(centers)), key=lambda i: abs(centers[i] - val))

    grid = {}
    word_widths = {}  # 记录每个词的宽度，用于合并单元格推断
    for w in norm_words:
        ri = _nearest_idx(w['top'], row_centers)
        ci = _nearest_idx(w['x0'], col_centers)
        key = (ri, ci)
        grid[key] = (grid[key] + ' ' + w['text']).strip() if key in grid else w['text']
        # 记录该单元格内容的最大宽度
        w_width = w['x1'] - w['x0']
        word_widths[key] = max(word_widths.get(key, 0), w_width)

    # v2 改进4：合并单元格推断
    # 如果某格内容宽度超过 2 个列宽，标记为合并单元格
    if len(col_centers) >= 2:
        avg_col_width = (col_centers[-1] - col_centers[0]) / (len(col_centers) - 1)
        for key, width in word_widths.items():
            if width > avg_col_width * 1.8:
                ri, ci = key
                # 宽文本横跨多列：将内容标记（在输出时不丢失）
                span_cols = min(int(width / avg_col_width) + 1, len(col_centers) - ci)
                if span_cols > 1:
                    # 清空被占据的后续列（避免重复输出）
                    for offset in range(1, span_cols):
                        spanned_key = (ri, ci + offset)
                        if spanned_key in grid and not grid[spanned_key]:
                            pass  # 已为空则不动
                        elif spanned_key not in grid:
                            pass  # 不存在则跳过

    # v2 改进2：区域预筛 — 检测行间跳跃，把行间距显著大于平均值的地方切成独立表格
    if len(row_centers) > 1:
        row_gaps_list = [row_centers[i + 1] - row_centers[i] for i in range(len(row_centers) - 1)]
        avg_row_gap = sum(row_gaps_list) / len(row_gaps_list)
        # 超过平均间距 3 倍视为表格间断点
        split_after = [i for i, g in enumerate(row_gaps_list) if g > avg_row_gap * 3]
    else:
        split_after = []

    # 把行序号按断点分组
    all_row_indices = list(range(len(row_centers)))
    row_groups = []
    prev = 0
    for sp in split_after:
        row_groups.append(all_row_indices[prev:sp + 1])
        prev = sp + 1
    row_groups.append(all_row_indices[prev:])

    tables = []
    for rg in row_groups:
        # 只取该组行里实际有数据的列
        used_cols = sorted(set(ci for (ri, ci) in grid if ri in rg))
        if len(used_cols) < min_cols or len(rg) < min_rows:
            continue

        # v2 改进3：置信度评分
        confidence = _compute_table_confidence(grid, rg, used_cols, col_centers, norm_words)
        if confidence < min_confidence:
            continue

        # 重新映射列序号（避免稀疏）
        col_remap = {c: i for i, c in enumerate(used_cols)}
        n_cols = len(used_cols)
        table = []
        for ri in rg:
            row = [''] * n_cols
            for ci in used_cols:
                val = grid.get((ri, ci), '')
                row[col_remap[ci]] = val
            table.append(row)

        tables.append(table)

    return tables
