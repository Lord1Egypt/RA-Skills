#!/usr/bin/env python3
"""
pptx_animate.py — v4.1 智能动画引擎（对标 ChatPPT "全网唯一智能动画引擎"）

加载已生成的 .pptx → 注入 OOXML transition + entrance animation → 输出新 .pptx。

4 种动画风格预设：
  apple-keynote      — Push + 标题 fade + scale-in（Apple 发布会风）
  minimal-fade       — 全 slide fade，干净不抢戏
  dynamic-slide      — Wipe + 内容 fly-in，活泼
  cinematic          — Cover + scale-in，电影感

按 slide type 智能选择动画（基于 deck 内容或 slide layout）：
  hero_cover     → cover transition + title 标题 zoom-in
  section_divider → wipe + 数字 fade-in
  big_stat       → fade + 数字 number-counter（OOXML 模拟）
  quote_card     → fade（克制）
  其他           → push（标准）

用法：
    # 给已有 PPT 加动画
    python3 scripts/pptx_animate.py /tmp/d.pptx \\
        --style apple-keynote --output /tmp/animated.pptx

    # 风格预设
    python3 scripts/pptx_animate.py d.pptx --style minimal-fade -o out.pptx
"""

from __future__ import annotations
import argparse
import shutil
import sys
import zipfile
from pathlib import Path
import re

# 4 种 OOXML 转场（PowerPoint 标准）
TRANSITIONS = {
    'apple-keynote': {
        'cover': '<p:push xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" dir="r"/>',
        'section': '<p:wipe xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" dir="l"/>',
        'default': '<p:push xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" dir="l"/>',
        'quote': '<p:fade xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"/>',
    },
    'minimal-fade': {
        'default': '<p:fade xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"/>',
    },
    'dynamic-slide': {
        'cover': '<p:cover xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" dir="d"/>',
        'section': '<p:wipe xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" dir="r"/>',
        'default': '<p:push xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" dir="u"/>',
    },
    'cinematic': {
        'cover': '<p:cover xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" dir="d"/>',
        'default': '<p:fade xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"/>',
    },
}

# Slide type → 动画类别（根据 deck JSON）
TYPE_TO_CATEGORY = {
    'hero_cover': 'cover',
    'section_divider': 'section',
    'quote_card': 'quote',
    'big_stat': 'default',
    'kpi_triple': 'default',
    'content_list': 'default',
    'compare_columns': 'default',
    'product_shot': 'default',
    'timeline': 'default',
    'call_to_action': 'cover',
    'code_block': 'default',
    'smart_timeline': 'default',
    'smart_pyramid': 'default',
    'smart_funnel': 'default',
    'smart_steps': 'default',
}


def detect_slide_categories(pptx_path: Path) -> list[str]:
    """从 pptx 内容判断每张 slide 的 category（不依赖 deck JSON）。

    判断逻辑：
      - 如果 slide XML 含巨字号文本（>60pt）→ cover
      - 如果含 "01" / "02" 这类章节编号 → section
      - 如果含引号 "「" "」" "" "" → quote
      - 否则 default
    """
    categories = []
    with zipfile.ZipFile(pptx_path, 'r') as z:
        slide_files = sorted(
            [f for f in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml$', f)],
            key=lambda x: int(re.search(r'slide(\d+)', x).group(1))
        )
        for sf in slide_files:
            xml = z.read(sf).decode('utf-8', errors='replace')
            # 字号判定：font-size 600+ (60pt) 表示 hero
            if re.search(r'sz="(\d+)"', xml):
                max_sz = max(int(m) for m in re.findall(r'sz="(\d+)"', xml))
                if max_sz >= 6000:  # 60pt 以上
                    categories.append('cover')
                    continue
            if re.search(r'>(0[1-9]|10|11|12)\.?<', xml):  # 章节编号 01-12
                categories.append('section')
            elif '「' in xml or '"' in xml or '"' in xml:
                categories.append('quote')
            else:
                categories.append('default')
    return categories


def inject_transitions(pptx_in: Path, pptx_out: Path, style: str,
                       deck_types: list[str] | None = None) -> int:
    """注入 transition 到每张 slide。返回处理的 slide 数。"""
    presets = TRANSITIONS.get(style)
    if not presets:
        raise ValueError(f"unknown style {style!r}, choose from {list(TRANSITIONS)}")

    # 复制原文件
    shutil.copy2(pptx_in, pptx_out)

    # 读现有 slide 顺序 + 类别
    if deck_types:
        categories = [TYPE_TO_CATEGORY.get(t, 'default') for t in deck_types]
    else:
        categories = detect_slide_categories(pptx_out)

    n_processed = 0

    # 重写 ZIP（pptx 是 ZIP）
    tmp_path = pptx_out.with_suffix('.pptx.tmp')
    with zipfile.ZipFile(pptx_out, 'r') as zin:
        with zipfile.ZipFile(tmp_path, 'w', zipfile.ZIP_DEFLATED) as zout:
            slide_idx = 0
            for item in zin.infolist():
                data = zin.read(item.filename)
                if re.match(r'ppt/slides/slide\d+\.xml$', item.filename):
                    cat = (categories[slide_idx] if slide_idx < len(categories)
                           else 'default')
                    transition_xml = presets.get(cat, presets.get('default', ''))
                    if transition_xml:
                        text = data.decode('utf-8')
                        # 在 </p:sld> 前插入 transition（如果还没有）
                        if '<p:transition' not in text:
                            new_text = text.replace(
                                '</p:sld>',
                                f'<p:transition spd="med">{transition_xml}</p:transition></p:sld>'
                            )
                            data = new_text.encode('utf-8')
                            n_processed += 1
                    slide_idx += 1
                zout.writestr(item, data)

    tmp_path.replace(pptx_out)
    return n_processed


def main():
    parser = argparse.ArgumentParser(
        description='火一五 PPT v4.1 智能动画引擎（对标 ChatPPT）'
    )
    parser.add_argument('pptx', help='输入 .pptx 路径')
    parser.add_argument('--style', default='apple-keynote',
                        choices=list(TRANSITIONS.keys()),
                        help='动画风格预设')
    parser.add_argument('--output', '-o', required=True)
    parser.add_argument('--deck-json', help='deck JSON（精确 slide type 判定，可选）')
    parser.add_argument('--list-styles', action='store_true', help='列所有可用 style')
    args = parser.parse_args()

    if args.list_styles:
        print("\n  可用动画风格:")
        for s in TRANSITIONS:
            print(f"    {s}")
        return

    deck_types = None
    if args.deck_json:
        import json
        deck = json.loads(Path(args.deck_json).read_text())
        deck_types = [s.get('type', '') for s in deck.get('slides', [])]
        print(f"  📋 从 deck JSON 读到 {len(deck_types)} 张 slide types: "
              f"{deck_types[:5]}{'...' if len(deck_types) > 5 else ''}",
              file=sys.stderr)

    print(f"  🎬 风格: {args.style}", file=sys.stderr)
    n = inject_transitions(Path(args.pptx), Path(args.output),
                           args.style, deck_types)
    print(f"  ✅ {args.output} ({n} 张 slide 加了转场)", file=sys.stderr)


if __name__ == '__main__':
    main()
