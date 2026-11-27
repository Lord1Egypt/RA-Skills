#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check a onepager-render HTML file against the 1-3 page budget.

Usage:
    python check_onepager.py <file.html>

Exit code:
    0 = pass (warnings allowed)
    1 = hard failure
"""

import html
import re
import sys
from pathlib import Path

BUDGET = {1: 900, 2: 1700, 3: 2600}  # CJK chars, ~12% headroom over 800/1600/2400
MIN_PT = 9.0
FRESH_INLINE_MAX = 4   # freshness-rules.md: inline block <= 4 items
FRESH_PAGE_MAX = 12    # freshness-rules.md: appendix page <= 12 rows
GLOSSARY_PAGE_MAX = 12 # glossary appendix (page--glossary): <= 12 rows
IMG_MAX_BYTES = 400 * 1024        # single embedded image
IMG_TOTAL_MAX_BYTES = 2 * 1024 * 1024   # all embedded images
FILE_MAX_BYTES = 3 * 1024 * 1024  # whole HTML file

# Abstract words that make two headings look like the same topic.
# Shared, unqualified use of one of these is flagged for editorial review.
HEADING_ABSTRACT = {
    "输出", "标准", "格式", "规范", "目标", "流程", "边界", "评测", "迭代",
    "资源", "权限", "状态", "依赖", "异常", "兜底", "配置", "管理", "设计",
    "实现", "机制", "方案", "模块", "系统", "能力", "工作流", "验收", "呈现",
    "内容", "形式",
}


def drop_comments(raw: str) -> str:
    return re.sub(r"<!--.*?-->", "", raw, flags=re.S)


def extract_balanced(fragment: str, start: int) -> str:
    """Return the full <div>...</div> (or <section>...</section>) block starting at `start`,
    honoring nesting, so inner </div> (e.g. freshness-head) cannot truncate the match."""
    tag = re.match(r"<(div|section)\b", fragment[start:])
    if not tag:
        return fragment[start:start + 200]
    name = tag.group(1)
    depth = 0
    for m in re.finditer(rf"<{name}\b[^>]*>|</{name}>", fragment[start:], flags=re.I):
        depth += -1 if m.group(0).startswith("</") else 1
        if depth == 0:
            return fragment[start:start + m.end()]
    return fragment[start:]  # unbalanced; be permissive


def extract_all(fragment: str, class_name: str, wrapper: str = r"<(div|section)\b") -> list:
    out = []
    for m in re.finditer(
            rf'{wrapper}[^>]*class="[^"]*\b{class_name}\b(?!-)[^"]*"[^>]*>',
            fragment, flags=re.S | re.I):
        out.append(extract_balanced(fragment, m.start()))
    return out


def visible_text(fragment: str) -> str:
    text = re.sub(r"<script\b.*?</script>", " ", fragment, flags=re.S | re.I)
    text = re.sub(r"<style\b.*?</style>", " ", text, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    return html.unescape(text)


def count_cjk(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def extract_headings(fragment: str) -> list:
    headings = []
    for m in re.finditer(r"<h([2-4])\b[^>]*>(.*?)</h\1>", fragment, flags=re.S | re.I):
        text = re.sub(r"\s+", " ", visible_text(m.group(2))).strip()
        if text:
            headings.append((int(m.group(1)), text))
    return headings


def heading_collisions(headings: list) -> list:
    hits = []
    for i in range(len(headings)):
        for j in range(i + 1, len(headings)):
            la, a = headings[i]
            lb, b = headings[j]
            if la != lb:          # only compare sibling-level headings
                continue
            if a == b:
                hits.append((a, b, {"重复标题"}))
                continue
            shared = {w for w in HEADING_ABSTRACT if w in a and w in b}
            if shared:
                hits.append((a, b, shared))
    return hits


def main(path: str) -> int:
    raw = Path(path).read_text(encoding="utf-8")
    body = drop_comments(raw)

    # --- freshness extraction (contract: references/freshness-rules.md) ---
    fresh_appendix = extract_all(body, "page--freshness", wrapper=r"<section\b")
    fresh_blocks = extract_all(body, "freshness", wrapper=r"<div\b")
    fresh_html = "\n".join(fresh_appendix + fresh_blocks)
    fresh_items = len(re.findall(r"<li\b", fresh_html, flags=re.I)) + \
        max(0, len(re.findall(r"<tr\b", fresh_html, flags=re.I)) - 1 * len(fresh_appendix))
    fresh_chars = count_cjk(visible_text(fresh_html))
    fresh_page_count = len(fresh_appendix)
    fresh_inline_items = sum(
        len(re.findall(r"<li\b", b, flags=re.I)) for b in fresh_blocks)

    # --- glossary appendix (page--glossary): exempt from page/char budget ---
    glossary_appendix = extract_all(body, "page--glossary", wrapper=r"<section\b")
    glossary_rows = sum(
        max(0, len(re.findall(r"<tr\b", b, flags=re.I)) - 1) for b in glossary_appendix)

    # --- main content = everything except freshness parts ---
    without_fresh = body
    for b in fresh_appendix + fresh_blocks + glossary_appendix:
        without_fresh = without_fresh.replace(b, " ")

    text = visible_text(without_fresh)
    pages = len(re.findall(
        r'<section[^>]*class="[^"]*\bpage\b(?!--freshness)[^"]*"', without_fresh, flags=re.I))
    cjk = count_cjk(text)
    words = len(re.findall(r"[A-Za-z0-9_]+", text))
    svgs = len(re.findall(r"<svg\b", without_fresh, flags=re.I))
    tables = len(re.findall(r"<table\b", without_fresh, flags=re.I))
    imgs = len(re.findall(r"<img\b", without_fresh, flags=re.I))

    # --- embedded images (contract: references/html-spec.md §6) ---
    img_tags = re.findall(r"<img\b[^>]*>", without_fresh, flags=re.I)
    data_imgs = [t for t in img_tags
                 if re.search(r'src\s*=\s*["\']data:image/', t, flags=re.I)]
    ext_imgs = [t for t in img_tags
                if re.search(r'src\s*=\s*["\'](?:https?:)?//', t, flags=re.I)]
    missing_alt = [t for t in img_tags
                   if not re.search(r'\balt\s*=\s*["\'][^"\']+', t, flags=re.I)]
    img_bytes = []
    for t in data_imgs:
        m = re.search(r'base64,([^"\']+)', t)
        if m:
            img_bytes.append(len(m.group(1)) * 3 // 4)
    embedded_bytes = sum(img_bytes)

    font_sizes = [float(x) for x in re.findall(
        r"font-size\s*:\s*([0-9.]+)\s*pt", raw, flags=re.I)]
    min_font = min(font_sizes) if font_sizes else None

    external = re.findall(r'(?:src|href)\s*=\s*["\'](?:https?:)?//', body, flags=re.I)
    scripts = re.findall(r"<script\b", body, flags=re.I)
    details = re.findall(r"<details\b", body, flags=re.I)
    fixed = re.findall(r"position\s*:\s*fixed", body, flags=re.I)
    vh = re.findall(r"[0-9.]+vh\b", body, flags=re.I)
    placeholders = re.findall(r"\{\{[^}]+\}\}", body)
    has_page_rule = "@page" in raw and "size:A4" in raw.replace(" ", "")
    has_color_adjust = "print-color-adjust" in raw
    has_break_inside = "break-inside" in raw

    errors = []
    warnings = []

    if pages not in (1, 2, 3):
        errors.append(f"正文页数必须是 1、2 或 3，当前为 {pages}（附录页已单独统计）")
    if cjk == 0:
        errors.append("没有检测到中文正文，确认文件内容是否正确")
    if pages in BUDGET and cjk > BUDGET[pages]:
        errors.append(f"中文字符 {cjk} 超过 {pages} 页预算 {BUDGET[pages]}，按压缩阶梯删内容")
    if min_font is not None and min_font < MIN_PT:
        errors.append(f"最小字号 {min_font}pt 低于 {MIN_PT}pt，不要靠缩字号硬塞")
    if not has_page_rule:
        errors.append("缺少 @page { size: A4 }，打印尺寸不可控")
    if not has_color_adjust:
        warnings.append("缺少 print-color-adjust: exact，打印可能丢失背景色")
    if not has_break_inside:
        warnings.append("缺少 break-inside: avoid，图/卡片可能跨页断裂")
    if external:
        errors.append(f"存在 {len(external)} 个外部资源引用，离线打印可能失败")
    if scripts:
        warnings.append(f"存在 {len(scripts)} 个 <script>，打印内容不应依赖 JS")
    if details:
        errors.append("存在 <details>，折叠内容在打印时可能丢失")
    if fixed:
        errors.append("存在 position: fixed，打印会重复或错位")
    if vh:
        warnings.append("存在 vh 单位，打印尺寸不稳定")
    if ext_imgs:
        errors.append(f"存在 {len(ext_imgs)} 张外链图片，离线打印会白图；改为 base64 内嵌")
    if missing_alt:
        errors.append(f"存在 {len(missing_alt)} 张图片缺少非空 alt，必须写“这张图回答什么问题”")
    if img_bytes and max(img_bytes) > IMG_MAX_BYTES:
        over = max(img_bytes) / 1024
        warnings.append(
            f"单张内嵌图约 {over:.0f}KB，超过 {IMG_MAX_BYTES // 1024}KB 上限；"
            f"请降采样（长边 1600px、JPEG q85）后再内嵌")
    if embedded_bytes > IMG_TOTAL_MAX_BYTES:
        errors.append(
            f"内嵌图片合计约 {embedded_bytes / 1024 / 1024:.1f}MB，超过 "
            f"{IMG_TOTAL_MAX_BYTES // 1024 // 1024}MB 上限；删图或降采样")
    if imgs and not data_imgs and not ext_imgs:
        warnings.append(f"存在 {imgs} 个 <img> 但未检测到 data:image，确认图片是否真的内嵌")
    if placeholders:
        errors.append(f"还有 {len(placeholders)} 个未替换的 {{{{占位符}}}}")
    figures = svgs + imgs
    if pages == 1 and figures + tables > 2:
        warnings.append("1 页内图（SVG＋原图）+表超过 2 个，检查是否过密")
    if pages == 2 and figures + tables > 4:
        warnings.append("2 页内图（SVG＋原图）+表超过 4 个，检查是否过密")
    if pages == 3 and figures + tables > 6:
        warnings.append("3 页内图（SVG＋原图）+表超过 6 个，检查是否过密")
    if pages == 3 and imgs == 0 and svgs == 0:
        warnings.append("3 页档没有图：确认升页理由成立（应为结构断裂/图片载荷/记忆量），否则回 2 页")
    try:
        file_size = Path(path).stat().st_size
        if file_size > FILE_MAX_BYTES:
            warnings.append(
                f"文件约 {file_size / 1024 / 1024:.1f}MB，超过 {FILE_MAX_BYTES // 1024 // 1024}MB；"
                f"检查图片是否未压缩")
    except OSError:
        pass

    # --- editorial: heading collision ---
    for a, b, shared in heading_collisions(extract_headings(without_fresh)):
        warnings.append(
            f"标题撞词：「{a}」与「{b}」共享 {'/'.join(sorted(shared))}；"
            f"请加限定词（内容/呈现/验收/执行）或写清边界")

    # --- freshness contract checks ---
    if fresh_blocks and fresh_page_count:
        errors.append("时效内容同时出现内联区块和附录页，二选一（契约 §1）")
    if fresh_inline_items > FRESH_INLINE_MAX:
        errors.append(
            f"内联时效区块 {fresh_inline_items} 条，超过上限 {FRESH_INLINE_MAX}；"
            f"改用附录页形态 B")
    if fresh_page_count and fresh_items > FRESH_PAGE_MAX:
        errors.append(f"时效附录页 {fresh_items} 条，超过上限 {FRESH_PAGE_MAX}，回到分级收紧")
    if glossary_rows > GLOSSARY_PAGE_MAX:
        errors.append(
            f"术语附录页 {glossary_rows} 行，超过上限 {GLOSSARY_PAGE_MAX}，回到筛选收紧")
    if len(glossary_appendix) > 1:
        errors.append("术语附录页超过 1 页，只保留一页（合并或删低价值条目）")
    if fresh_html:
        if not re.search(r"核实", fresh_html):
            errors.append("时效区块首行缺少“核实”字样（契约要求注明核实日期）")
        if not re.search(r"\d{4}-\d{2}-\d{2}", fresh_html):
            warnings.append("时效区块未检测到 YYYY-MM-DD 核实日期")
        if not re.search(r"手册|Release|docs?|http|§|\d+\.\d+\.\d+", fresh_html, flags=re.I):
            warnings.append("时效条目未检测到出处（章节号/链接），每条必须带出处")
        stale_tags = re.findall(r"\[(演进|未核实)\][^<]*", visible_text(fresh_html))
        if stale_tags:
            print(f"[NOTE] 时效区块含 {len(stale_tags)} 条 [演进]/[未核实]，确认正文已按当前版本改写，且交付报告逐条列出")
    elif fresh_items == 0:
        print("[NOTE] 未包含时效区块；若主题含版本敏感断言，建议跑 fact-freshness-check")

    print("== onepager-render check ==")
    print(f"file         : {path}")
    print(f"pages        : {pages} (+{fresh_page_count} freshness appendix, "
          f"+{len(glossary_appendix)} glossary appendix)")
    print(f"cjk chars    : {cjk} (budget {BUDGET.get(pages, 'n/a')}, freshness {fresh_chars} exempt)")
    print(f"ascii words  : {words}")
    print(f"svg / table  : {svgs} / {tables}")
    print(f"img          : {imgs} ({len(data_imgs)} embedded, "
          f"{embedded_bytes / 1024:.0f}KB)")
    print(f"freshness    : {fresh_items} item(s), {fresh_chars} chars")
    print(f"glossary     : {glossary_rows} row(s), exempt")
    print(f"min font     : {min_font if min_font is not None else 'unknown'} pt")
    print(f"external     : {len(external)}")
    print()

    for w in warnings:
        print(f"[WARN] {w}")
    for e in errors:
        print(f"[FAIL] {e}")

    if errors:
        print("\nRESULT: FAIL")
        return 1
    if warnings:
        print("\nRESULT: PASS (with warnings)")
    else:
        print("\nRESULT: PASS")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_onepager.py <file.html>", file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
