#!/usr/bin/env python3
"""
extract_highlights.py - 从 PDF 中提取所有高亮标注内容，生成带 YAML Front Matter 的 Markdown 文件。

用法:
    python extract_highlights.py <pdf_path> [--output <output_dir>] [--color <color_name>]

参数:
    pdf_path        PDF 文件路径（必填）
    --output        输出目录（默认与 PDF 同目录）
    --color         只提取指定颜色的高亮（如 yellow、green、red），默认提取全部颜色

依赖:
    pip install pymupdf
"""

import sys
import os
import re
import json
import argparse
from datetime import date
from pathlib import Path

# ── 颜色名称映射（RGB 近似 → 颜色名） ─────────────────────────────────────
COLOR_MAP = {
    "yellow":  [(1.0, 1.0, 0.0), (1.0, 0.95, 0.0), (1.0, 1.0, 0.4), (1.0, 0.98, 0.2)],
    "green":   [(0.0, 1.0, 0.0), (0.0, 0.8, 0.0), (0.2, 0.9, 0.2), (0.0, 1.0, 0.5)],
    "red":     [(1.0, 0.0, 0.0), (1.0, 0.2, 0.2), (0.9, 0.0, 0.0)],
    "blue":    [(0.0, 0.0, 1.0), (0.0, 0.5, 1.0), (0.0, 0.7, 1.0), (0.2, 0.5, 1.0)],
    "pink":    [(1.0, 0.4, 0.7), (1.0, 0.0, 0.5), (1.0, 0.6, 0.8)],
    "orange":  [(1.0, 0.6, 0.0), (1.0, 0.5, 0.0), (1.0, 0.7, 0.2)],
    "purple":  [(0.5, 0.0, 1.0), (0.6, 0.2, 0.8), (0.7, 0.0, 1.0)],
    "cyan":    [(0.0, 1.0, 1.0), (0.0, 0.9, 0.9), (0.2, 0.9, 1.0)],
}

def rgb_to_name(color_tuple) -> str:
    """将 RGB 三元组转换为颜色名称，返回最接近的颜色"""
    if color_tuple is None:
        return "unknown"
    r, g, b = color_tuple
    min_dist = float("inf")
    best = "unknown"
    for name, candidates in COLOR_MAP.items():
        for cr, cg, cb in candidates:
            dist = ((r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2) ** 0.5
            if dist < min_dist:
                min_dist = dist
                best = name
    return best if min_dist < 0.35 else "unknown"


def extract_highlights(pdf_path: str, target_color: str | None = None) -> list[dict]:
    """
    提取 PDF 中的高亮标注内容。
    返回列表，每项包含: {page, color, text}
    """
    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("[ERROR] 缺少依赖库，请先安装：pip install pymupdf", file=sys.stderr)
        sys.exit(1)

    doc = fitz.open(pdf_path)
    results = []

    for page_num, page in enumerate(doc, start=1):
        annots = page.annots()
        if not annots:
            continue

        for annot in annots:
            # 只处理高亮类型 (type 8 = Highlight)
            if annot.type[0] != 8:
                continue

            # 获取颜色
            color_rgb = annot.colors.get("stroke") or annot.colors.get("fill")
            color_name = rgb_to_name(color_rgb) if color_rgb else "unknown"

            # 颜色过滤
            if target_color and color_name != target_color:
                continue

            # 提取高亮区域文字
            quads = annot.vertices
            if not quads:
                continue

            text_pieces = []
            # quads 是 4 点一组的四边形顶点列表
            for i in range(0, len(quads), 4):
                quad = quads[i:i+4]
                if len(quad) < 4:
                    continue
                # 用四边形区域裁剪文本
                rect = fitz.Quad(quad).rect
                # 稍微扩大矩形以确保完整覆盖
                rect = rect + (-1, -1, 1, 1)
                clip_text = page.get_text("text", clip=rect).strip()
                if clip_text:
                    text_pieces.append(clip_text)

            combined = " ".join(text_pieces).strip()
            combined = re.sub(r'\s+', ' ', combined)  # 合并多余空白

            if combined:
                results.append({
                    "page": page_num,
                    "color": color_name,
                    "text": combined,
                })

    doc.close()
    return results


def generate_tags_and_title(highlights: list[dict], pdf_name: str) -> tuple[str, list[str]]:
    """
    使用简单关键词提取生成标题和 tags。
    实际运行时会由 WorkBuddy AI 生成更优质的标题和 tags，
    这里提供一个基础回退方案。
    """
    # 合并所有高亮文本
    all_text = " ".join(h["text"] for h in highlights)

    # 基础标题：PDF 文件名去扩展名（AI 会在后续步骤覆盖）
    base_name = Path(pdf_name).stem
    title = base_name.replace("-", " ").replace("_", " ").title()

    # 基础 tags：从文件名提取关键词
    raw_tags = re.split(r'[-_\s]+', Path(pdf_name).stem)
    tags = [t.lower() for t in raw_tags if len(t) > 2][:5]
    tags.append("highlights")

    return title, tags


def build_markdown(highlights: list[dict], title: str, tags: list[str], pdf_name: str) -> str:
    """生成完整的 Markdown 内容（含 YAML Front Matter）"""
    today = date.today().isoformat()

    # YAML Front Matter
    tags_str = "\n".join(f"  - {t}" for t in tags)
    yaml_block = f"""---
title: "{title}"
date: {today}
tags:
{tags_str}
---
"""

    # 正文 —— 高亮原文列表
    lines = [yaml_block, "", f"# {title}", "", "## 摘录原文", ""]

    current_page = None
    for h in highlights:
        if h["page"] != current_page:
            current_page = h["page"]
            lines.append(f"\n### 第 {current_page} 页\n")
        lines.append(f"- {h['text']}")

    # 总结区域（留给 AI 填写）
    lines += [
        "",
        "---",
        "",
        "## 内容总结",
        "",
        "> _（由 AI 根据以上摘录内容生成总结）_",
        "",
    ]

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="从 PDF 提取高亮内容并生成 Markdown 文件"
    )
    parser.add_argument("pdf_path", help="PDF 文件路径")
    parser.add_argument(
        "--output", "-o", default=None,
        help="输出目录（默认与 PDF 同目录）"
    )
    parser.add_argument(
        "--color", "-c", default=None,
        help="只提取指定颜色的高亮（如 yellow、green）"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="以 JSON 格式输出高亮列表（供 AI 后处理使用）"
    )
    args = parser.parse_args()

    pdf_path = Path(args.pdf_path).resolve()
    if not pdf_path.exists():
        print(f"[ERROR] 文件不存在: {pdf_path}", file=sys.stderr)
        sys.exit(1)
    if pdf_path.suffix.lower() != ".pdf":
        print(f"[ERROR] 不是 PDF 文件: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    print(f"[INFO] 正在提取高亮: {pdf_path.name}", file=sys.stderr)

    highlights = extract_highlights(str(pdf_path), target_color=args.color)

    if not highlights:
        print("[WARN] 未找到任何高亮标注。", file=sys.stderr)
        sys.exit(0)

    print(f"[INFO] 共提取到 {len(highlights)} 条高亮，来自 {len(set(h['page'] for h in highlights))} 页", file=sys.stderr)

    # JSON 模式：只输出高亮数据，由 AI 负责生成 Markdown
    if args.json:
        print(json.dumps(highlights, ensure_ascii=False, indent=2))
        return

    # 生成 Markdown
    title, tags = generate_tags_and_title(highlights, pdf_path.name)
    md_content = build_markdown(highlights, title, tags, pdf_path.name)

    # 确定输出路径
    output_dir = Path(args.output).resolve() if args.output else pdf_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{pdf_path.stem}_highlights.md"

    output_file.write_text(md_content, encoding="utf-8")
    print(f"[OK] 已生成 Markdown: {output_file}", file=sys.stderr)

    # 标准输出高亮数据供 AI 读取和完善
    print(json.dumps({
        "output_file": str(output_file),
        "highlights": highlights,
        "title_draft": title,
        "tags_draft": tags,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
