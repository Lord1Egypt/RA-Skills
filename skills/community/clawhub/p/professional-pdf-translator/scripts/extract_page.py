"""
PDF Batch Translator — 单页文本提取与术语匹配
用法: python extract_page.py --pdf <path> --page <num> --terms <glossary1.md> [glossary2.md ...]
"""

import argparse
import json
import os
import re
import sys

try:
    import fitz  # PyMuPDF
except ImportError:
    print(json.dumps({"error": "缺失 PyMuPDF 依赖，请在终端执行: python -m pip install pymupdf"}, ensure_ascii=False))
    sys.exit(1)


def _is_dual_column(page, text_blocks, page_width):
    """检测页面是否为双栏排版"""
    mid_x = page_width / 2
    has_left = False
    has_right = False
    for b in text_blocks:
        x0, y0, x1, y1, text, block_no, block_type = b
        width = x1 - x0
        # 只统计窄块（跨栏块不参与双栏判断）
        if width > page_width * 0.65:
            continue
        if x0 < mid_x:
            has_left = True
        else:
            has_right = True
        if has_left and has_right:
            return True
    return False


def get_text_column_sorted(page):
    """智能处理排版：自动检测双栏/单栏，双栏时按中轴线分割左右栏分别排序"""
    blocks = page.get_text("blocks")
    text_blocks = [b for b in blocks if b[6] == 0]

    if not text_blocks:
        return ""

    page_width = page.rect.width
    page_height = page.rect.height
    mid_x = page_width / 2
    is_dual = _is_dual_column(page, text_blocks, page_width)

    header_blocks = []
    footer_blocks = []

    if is_dual:
        left_blocks = []
        right_blocks = []
    else:
        body_blocks = []

    for b in text_blocks:
        x0, y0, x1, y1, text, block_no, block_type = b
        width = x1 - x0

        # 跨度超过页面宽度 65% 的块视为标题或跨栏段落
        if width > page_width * 0.65:
            if y0 < page_height / 2:
                header_blocks.append(b)
            else:
                footer_blocks.append(b)
        else:
            if is_dual:
                if x0 < mid_x:
                    left_blocks.append(b)
                else:
                    right_blocks.append(b)
            else:
                body_blocks.append(b)

    # 各组内按垂直位置排序
    header_blocks.sort(key=lambda b: b[1])
    footer_blocks.sort(key=lambda b: b[1])

    if is_dual:
        left_blocks.sort(key=lambda b: b[1])
        right_blocks.sort(key=lambda b: b[1])
        ordered = header_blocks + left_blocks + right_blocks + footer_blocks
    else:
        body_blocks.sort(key=lambda b: b[1])
        ordered = header_blocks + body_blocks + footer_blocks

    return "\n".join([b[4].strip() for b in ordered if b[4].strip()])


def extract(pdf_path, page_num, terms_paths):
    try:
        with fitz.open(pdf_path) as doc:
            if page_num < 1 or page_num > len(doc):
                return {"error": f"页码 {page_num} 超出范围 (文档总页数: {len(doc)})"}

            page = doc[page_num - 1]
            text = get_text_column_sorted(page)

            if not text:
                return {"is_empty": True, "text": "", "matched_terms": []}

            matched = []
            matched_set = set()
            text_lower = text.lower()

            for path in terms_paths:
                if not os.path.exists(path):
                    continue
                with open(path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line_clean = line.strip()
                        if not line_clean or line_clean.startswith('#'):
                            continue

                        # 提取术语行中的英文单词片段（长度 >= 2 的单词作为匹配锚点）
                        eng_parts = re.findall(r'[a-zA-Z]+', line_clean)
                        eng_parts = [p.lower() for p in eng_parts if len(p) > 1]

                        for p in eng_parts:
                            # 使用词边界匹配，避免子串误匹配（如 "class" 不会匹配 "subclass"）
                            if re.search(r'\b' + re.escape(p) + r'\b', text_lower):
                                if line_clean not in matched_set:
                                    matched_set.add(line_clean)
                                    matched.append(line_clean)
                                break

            return {
                "is_empty": False,
                "text": text,
                "matched_terms": matched,
            }

    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="从 PDF 中提取单页文本并匹配术语表")
    parser.add_argument("--pdf", required=True, help="PDF 文件绝对路径")
    parser.add_argument("--page", type=int, required=True, help="页码 (从 1 开始)")
    parser.add_argument("--terms", nargs="+", default=[], help="术语表 md 文件的路径列表")
    args = parser.parse_args()

    result = extract(args.pdf, args.page, args.terms)
    if sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))
