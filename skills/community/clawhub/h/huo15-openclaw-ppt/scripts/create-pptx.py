#!/usr/bin/env python3
"""
create-pptx.py - 火一五 PPT 生成器（v3.0）

基于 4 层 design tokens（Palette / Typography / Spacing / Elevation / Decoration）+
10 个语义化页面模板（hero/section/stat/kpi/quote/list/compare/product/timeline/cta）。

输入形式：
  1. --spec deck.json          （完整 deck 规约；支持 v2/v3 语法）
  2. --cover "标题|副标题"      （快速生成单页封面）

风格 pack（v3 审美方案）：
  apple-keynote            真·苹果发布会（暗场 + SF Pro + 巨字号）
  apple-light              Apple.com 白场
  xiaohongshu-creator      奶油 + 鼠尾草 + 焦糖（生活博主）
  xiaohongshu-vintage      琥珀 + 雾霾蓝（复古胶片）
  jobs-dark                暗蓝乔布斯（v1.x legacy）
  xiaohongshu              小红书品牌红（v2.x legacy）

兼容：老的 v2.x 使用 `--style` 参数仍然工作，会自动映射到同名 pack。

公司名优先级：--company > ~/.huo15/company-info.json > 默认字符串
"""

import os
import sys
import json
import argparse

from pptx import Presentation
from pptx.util import Inches

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# v3 设计系统
from style_packs import get_pack, list_packs
from templates import get_template, list_templates

# 兼容层（万一有人 fallback 到 v2）
from styles import get_style, list_styles
import pptx_toolkit as pk


# ============================================================
# 公司信息
# ============================================================

def _load_company_name(explicit=None):
    if explicit:
        return explicit
    ci_path = os.path.expanduser('~/.huo15/company-info.json')
    if os.path.exists(ci_path):
        try:
            with open(ci_path, 'r', encoding='utf-8') as fh:
                data = json.load(fh)
            return data.get('company_name') or '青岛火一五信息科技有限公司'
        except (OSError, json.JSONDecodeError):
            pass
    return '青岛火一五信息科技有限公司'


# ============================================================
# Slide type 到 template 的映射（v2 → v3 别名都走 templates 注册表）
# ============================================================

# 其中一些 type 历史上只是 cover/section 这种简写，直接从 templates/__init__.py
# 的别名表消化。加几个扩展 alias：
_EXTRA_ALIAS = {
    'stat_big': 'big_stat',
    'big_number': 'big_stat',
    'kpi_card': 'kpi_triple',
    'kpi_row': 'kpi_triple',
    'vs': 'compare_columns',
    'before_after': 'compare_columns',
    'gallery': 'product_shot',
    'shot': 'product_shot',
    'story': 'timeline',
    'contact': 'call_to_action',
    'thanks': 'call_to_action',
}


def _resolve_slide_type(stype: str):
    """把 slide spec 里的 type 映射到 templates 注册表的一个 builder。"""
    stype = (stype or 'content_list').strip()
    if stype in _EXTRA_ALIAS:
        stype = _EXTRA_ALIAS[stype]
    return get_template(stype)


# ============================================================
# 构建 deck
# ============================================================

def build_presentation(spec, pack_name, company):
    pack = get_pack(pack_name)
    prs = Presentation()
    prs.slide_width = Inches(pack.canvas.width)
    prs.slide_height = Inches(pack.canvas.height)

    slides = spec.get('slides', [])
    year = spec.get('year', '')

    for idx, slide_spec in enumerate(slides, start=1):
        stype = slide_spec.get('type', 'content_list')
        builder = _resolve_slide_type(stype)

        # 统一注入公司名 / 页码 / 年份（模板如果用得到就会读）
        data = dict(slide_spec)
        data.setdefault('company', company)
        data.setdefault('page', idx)
        data.setdefault('year', year)

        # 兼容 v2 字段名 → v3
        _v2_to_v3_fields(stype, data)

        try:
            builder(prs, pack, data)
        except Exception as e:
            print(f'⚠️  slide #{idx} ({stype}) 构建失败: {e}', file=sys.stderr)
            import traceback
            traceback.print_exc(file=sys.stderr)

    return prs


def _v2_to_v3_fields(stype: str, data: dict):
    """老的 deck.json 字段名（subtitle/en_subtitle/...）向 v3 字段名的兼容桥。"""
    # en_subtitle → en_sub
    if 'en_subtitle' in data and 'en_sub' not in data:
        data['en_sub'] = data['en_subtitle']
    # v2 end type 的 sub → subtitle
    if 'sub' in data and 'subtitle' not in data:
        data['subtitle'] = data['sub']


def _quick_deck(args, company):
    title, _, subtitle = args.cover.partition('|')
    return {
        'slides': [
            {'type': 'hero_cover', 'title': title.strip(),
             'subtitle': subtitle.strip(),
             'footnote': f'{company}  ·  {args.year or ""}'.strip(' ·')},
        ],
        'year': args.year or '',
    }


# ============================================================
# CLI
# ============================================================

def main(argv=None):
    parser = argparse.ArgumentParser(
        prog='create-pptx',
        description='火一五 PPT 生成器（v3.0 — design tokens + 10 模板）',
    )
    parser.add_argument('--output', '-o', help='输出 .pptx 路径（生成时必填）')
    parser.add_argument(
        '--pack',
        dest='pack',
        help=f'审美方案（v3.0 新）。可选：{", ".join(list_packs())}',
    )
    parser.add_argument(
        '--style',
        dest='style',
        help='[兼容] 旧的风格参数，等价于 --pack',
    )
    parser.add_argument('--spec', help='deck JSON 规约路径')
    parser.add_argument('--cover', help='快速生成单页封面，格式："标题|副标题"')
    parser.add_argument('--company', help='覆盖公司名（默认读 ~/.huo15/company-info.json）')
    parser.add_argument('--year', default='', help='封面底部标注年份')
    parser.add_argument('--list-packs', action='store_true', help='列出所有 pack 并退出')
    parser.add_argument('--list-templates', action='store_true', help='列出所有 template 并退出')

    args = parser.parse_args(argv)

    # 信息性命令
    if args.list_packs:
        from style_packs import REGISTRY
        print('可用 pack（含别名）：')
        seen = set()
        for k, p in REGISTRY.items():
            if p.name in seen:
                continue
            seen.add(p.name)
            print(f'  {p.name:<26}  {p.display_name}')
            print(f'  {" ":<26}  {p.tagline}')
        return 0
    if args.list_templates:
        print('可用 template：')
        for name in list_templates():
            print(f'  {name}')
        return 0

    if not args.spec and not args.cover:
        parser.error('必须提供 --spec <deck.json> 或 --cover "标题|副标题"')
    if not args.output:
        parser.error('生成时必须提供 --output <deck.pptx>')

    pack_name = args.pack or args.style or 'apple-keynote'

    company = _load_company_name(args.company)

    if args.spec:
        with open(args.spec, 'r', encoding='utf-8') as fh:
            spec = json.load(fh)
    else:
        spec = _quick_deck(args, company)

    prs = build_presentation(spec, pack_name, company)
    os.makedirs(os.path.dirname(os.path.abspath(args.output)) or '.', exist_ok=True)
    prs.save(args.output)

    pack = get_pack(pack_name)
    print(
        f'✅ 已生成: {args.output}（pack: {pack.name} — {pack.display_name}，'
        f'幻灯片数: {len(spec.get("slides", []))}）'
    )
    return 0


if __name__ == '__main__':
    sys.exit(main())
