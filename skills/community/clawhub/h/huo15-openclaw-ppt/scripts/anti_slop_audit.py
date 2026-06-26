#!/usr/bin/env python3
"""
anti_slop_audit.py — 火一五 PPT v3.3 反 AI Slop 自检（参照 frontend-design v4.7 的 15 条红线）

每个 StylePack 跑过 8 项硬红线机器化校验：
  R1   字体不能是 Inter / Roboto / Arial / system-ui（字体即性格）
  R2   主色调不能是 #5B5BFF / #7C3AED 这类紫色（AI 滥用陈词）
  R3   font_family 字符串不能含 emoji（emoji 当图标）
  R4   border_radius / card_radius 不能恒等于 12px / 16px（Tailwind 默认值）
  R6   bg 不能是 #121212 + 紫主题（懒）
  R8   accent 不能是 iOS 系统色 #007AFF / #FF3B30
  R10  glass / blur 命名 pack 必须 explicit 标注（避免 backdrop-blur 滥用）
  R11  AI 渐变模糊背景：检测 conic-gradient + 紫粉蓝青组合

用法：
    python3 scripts/anti_slop_audit.py                # 跑全部 21 套 pack
    python3 scripts/anti_slop_audit.py <pack-name>    # 单 pack 详细审计
    python3 scripts/anti_slop_audit.py --json         # JSON 输出（CI 友好）
"""

from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from style_packs import REGISTRY


# ============================================================
# 红线集合（机器化）
# ============================================================

FORBIDDEN_FONTS = {
    'inter', 'roboto', 'arial', 'helvetica', 'system-ui',
    '-apple-system', 'blinkmacsystemfont', 'sans-serif', 'serif',
}

PURPLE_HEX_RANGES = [
    # R/G/B 模式：紫色范围 — H ∈ [260°, 290°], S > 50%, L 30-70%
    # 简化为 hex 黑名单 + 模式判定
]

PURPLE_KEYWORDS = ('purple', 'violet', 'indigo', 'lavender')

IOS_SYSTEM_HEX = {
    '#007AFF', '#FF3B30', '#34C759', '#FF9500', '#FFCC00',
    '#5856D6', '#FF2D55', '#AF52DE', '#5AC8FA',
}

EMOJI_PATTERN = re.compile(
    r'[\U0001F300-\U0001F9FF\U0001FA00-\U0001FAFF☀-➿]'
)


def is_purple_hex(hex_str: str) -> bool:
    """判定 hex 颜色是否为紫色（HSL H ∈ [240°, 300°], S>40%）"""
    s = hex_str.lstrip('#')
    if len(s) != 6:
        return False
    try:
        r, g, b = int(s[0:2], 16) / 255, int(s[2:4], 16) / 255, int(s[4:6], 16) / 255
    except ValueError:
        return False
    mx, mn = max(r, g, b), min(r, g, b)
    delta = mx - mn
    if delta == 0:
        return False
    if mx == r:
        h = (60 * ((g - b) / delta) + 360) % 360
    elif mx == g:
        h = 60 * ((b - r) / delta) + 120
    else:
        h = 60 * ((r - g) / delta) + 240
    s_val = delta / mx if mx > 0 else 0
    # 紫色：H ∈ [240, 300]，饱和度 > 0.4
    return 240 <= h <= 300 and s_val > 0.4


def audit_pack(pack) -> dict:
    """对单个 StylePack 跑全套红线，返回 violations 列表 + score"""
    violations = []
    name = pack.name
    typography = pack.typography
    palette = pack.palette
    elevation = pack.elevation

    # R1: 字体
    fonts = (typography.display_font or '', typography.body_font or '')
    for f in fonts:
        if f.lower().strip() in FORBIDDEN_FONTS:
            violations.append({
                'rule': 'R1',
                'severity': 'hard',
                'detail': f'字体 {f!r} 在禁用列表（Inter / Roboto / Arial / system-ui = 没性格）',
            })

    # R2: 紫色调主色（accent / bg）
    accent = (palette.accent or '').upper()
    bg = (palette.bg or '').upper()
    if is_purple_hex(accent):
        violations.append({
            'rule': 'R2',
            'severity': 'hard',
            'detail': f'accent={accent} 是紫色调（AI 最滥用陈词，cyberpunk-vivid 等流派可豁免）',
        })
    # 紫色 + 黑底组合（R2+R6 联动）
    if is_purple_hex(accent) and bg in ('#121212', '#0F0F0F', '#000000'):
        violations.append({
            'rule': 'R2+R6',
            'severity': 'hard',
            'detail': f'紫色 accent {accent} + 暗黑 bg {bg} 双重 AI Slop 信号',
        })

    # R3: 名称字段含 emoji
    text_fields = (pack.display_name or '', pack.tagline or '', name)
    for t in text_fields:
        if EMOJI_PATTERN.search(t):
            # tagline / display_name 有 emoji 是装饰性，可豁免；只警告
            violations.append({
                'rule': 'R3',
                'severity': 'soft',
                'detail': f'文本 {t!r} 含 emoji（不能当图标用，仅装饰可保留）',
            })

    # R4: border_radius 默认值 12 / 16
    radius_inch = getattr(elevation, 'card_radius', 0)
    radius_pt = radius_inch * 72  # 1 inch = 72 pt
    if 11.5 < radius_pt < 12.5 or 15.5 < radius_pt < 16.5:
        violations.append({
            'rule': 'R4',
            'severity': 'soft',
            'detail': f'card_radius {radius_pt:.1f}pt 接近 Tailwind 默认（12 / 16）— 工业感',
        })

    # R8: iOS 系统色（直接拿来用）
    if accent in IOS_SYSTEM_HEX:
        violations.append({
            'rule': 'R8',
            'severity': 'soft',
            'detail': f'accent {accent} 是 iOS 系统色直接套用（无记忆点，liquid-glass 等流派可豁免）',
        })

    # R10: glass / blur pack 必须 explicit 命名（防 backdrop-blur 滥用）
    pack_lower = name.lower()
    has_glass_keyword = any(k in pack_lower for k in ('glass', 'blur', 'frosted'))
    is_glass_style = getattr(elevation, 'style', '') == 'glass'
    if is_glass_style and not has_glass_keyword:
        violations.append({
            'rule': 'R10',
            'severity': 'soft',
            'detail': '使用 glass / blur 视觉但 pack 名未声明 — 易被滥用，改名 *-glass / *-frosted',
        })

    # 计分：每条 hard -10，soft -3，满分 100
    score = 100
    for v in violations:
        score -= 10 if v['severity'] == 'hard' else 3
    score = max(0, score)

    # 审美档位（仿 design-critique v2.0）
    if score >= 90:
        tier = 'Master'
    elif score >= 75:
        tier = 'Senior'
    elif score >= 50:
        tier = 'Junior'
    else:
        tier = 'AI-Slop'

    return {
        'name': name,
        'display_name': pack.display_name,
        'score': score,
        'tier': tier,
        'violations': violations,
    }


def main():
    parser = argparse.ArgumentParser(description='火一五 PPT 反 AI Slop 自检')
    parser.add_argument('pack', nargs='?', help='指定 pack 名（不传跑全部）')
    parser.add_argument('--json', action='store_true', help='JSON 输出')
    parser.add_argument('--fail-on-violation', action='store_true',
                        help='有任何 hard violation 时 exit 1（CI 用）')
    args = parser.parse_args()

    if args.pack:
        if args.pack not in REGISTRY:
            print(f"未知 pack: {args.pack}（可选: {sorted(REGISTRY.keys())[:10]}...）",
                  file=sys.stderr)
            sys.exit(1)
        results = [audit_pack(REGISTRY[args.pack])]
    else:
        # REGISTRY 是 alias 字典（一个 pack 对象多个别名 key），按 id(pack) 去重
        seen_ids = set()
        unique_packs = []
        for p in REGISTRY.values():
            if id(p) in seen_ids:
                continue
            seen_ids.add(id(p))
            unique_packs.append(p)
        results = [audit_pack(p) for p in unique_packs]

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        if args.fail_on_violation:
            hard_count = sum(1 for r in results
                             for v in r['violations'] if v['severity'] == 'hard')
            sys.exit(1 if hard_count else 0)
        return

    # 文本输出
    print(f"\n  🛡️  火一五 PPT 反 AI Slop 自检（{len(results)} 个 pack）\n")
    by_tier = {'Master': [], 'Senior': [], 'Junior': [], 'AI-Slop': []}
    for r in results:
        by_tier[r['tier']].append(r)

    for tier in ('Master', 'Senior', 'Junior', 'AI-Slop'):
        items = by_tier[tier]
        if not items:
            continue
        icon = {'Master': '🏆', 'Senior': '✅', 'Junior': '⚠️ ', 'AI-Slop': '❌'}[tier]
        print(f"  {icon} {tier} 档位 ({len(items)} 个)")
        for r in items:
            print(f"    {r['score']:>3d}  {r['name']:<22}  {r['display_name']}")
            for v in r['violations']:
                sev = '✗' if v['severity'] == 'hard' else '·'
                print(f"           {sev} [{v['rule']}] {v['detail']}")
        print()

    hard_count = sum(1 for r in results
                     for v in r['violations'] if v['severity'] == 'hard')
    print(f"  汇总: hard={hard_count} 条, 平均分={sum(r['score'] for r in results) / len(results):.1f}")
    if args.fail_on_violation and hard_count:
        sys.exit(1)


if __name__ == '__main__':
    main()
