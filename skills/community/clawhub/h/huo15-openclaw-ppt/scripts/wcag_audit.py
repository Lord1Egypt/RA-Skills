#!/usr/bin/env python3
"""
wcag_audit.py — WCAG 2.2 AA 文字对比度自检（参照 frontend-design v4.7 的无障碍审计）

每个 StylePack 校验：
  - text_primary ↔ bg          ≥ 4.5 (AA 正文)
  - text_secondary ↔ bg        ≥ 4.5
  - text_primary ↔ bg_elevated ≥ 4.5（卡片场景）
  - accent ↔ bg                ≥ 3.0 (AA 大字 / 装饰元素)

对比度公式：WCAG 2.2 标准
  L = 0.2126*R + 0.7152*G + 0.0722*B（先做 sRGB → linear）
  ratio = (max(L1, L2) + 0.05) / (min(L1, L2) + 0.05)

用法：
    python3 scripts/wcag_audit.py                # 全部 pack
    python3 scripts/wcag_audit.py <pack-name>    # 单 pack 详细
    python3 scripts/wcag_audit.py --json
"""

from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from style_packs import REGISTRY


def hex_to_linear(hex_str: str) -> tuple[float, float, float]:
    """sRGB hex → linear RGB（用于 luminance）"""
    s = hex_str.lstrip('#')
    if len(s) == 3:
        s = ''.join(c * 2 for c in s)
    r, g, b = int(s[0:2], 16) / 255, int(s[2:4], 16) / 255, int(s[4:6], 16) / 255

    def linearize(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    return linearize(r), linearize(g), linearize(b)


def luminance(hex_str: str) -> float:
    r, g, b = hex_to_linear(hex_str)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(fg: str, bg: str) -> float:
    """WCAG 2.2 contrast ratio: 1.0~21.0"""
    l1 = luminance(fg)
    l2 = luminance(bg)
    lighter, darker = (l1, l2) if l1 > l2 else (l2, l1)
    return (lighter + 0.05) / (darker + 0.05)


def audit_pack(pack) -> dict:
    p = pack.palette
    pairs = [
        ('text_primary on bg', p.text_primary, p.bg, 4.5, 'AA 正文'),
        ('text_secondary on bg', p.text_secondary, p.bg, 4.5, 'AA 正文'),
        ('text_primary on bg_elevated', p.text_primary, p.bg_elevated, 4.5, 'AA 卡片正文'),
        ('accent on bg', p.accent, p.bg, 3.0, 'AA 大字 / 装饰'),
    ]
    results = []
    fail_count = 0
    for label, fg, bg, threshold, note in pairs:
        ratio = contrast_ratio(fg, bg)
        passed = ratio >= threshold
        if not passed:
            fail_count += 1
        results.append({
            'pair': label,
            'fg': fg,
            'bg': bg,
            'ratio': round(ratio, 2),
            'threshold': threshold,
            'pass': passed,
            'note': note,
        })

    score = 100 - fail_count * 25
    return {
        'name': pack.name,
        'display_name': pack.display_name,
        'pairs': results,
        'fail_count': fail_count,
        'score': max(0, score),
        'aa_compliant': fail_count == 0,
    }


def main():
    parser = argparse.ArgumentParser(description='火一五 PPT WCAG 2.2 AA 自检')
    parser.add_argument('pack', nargs='?')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--fail-on-violation', action='store_true')
    args = parser.parse_args()

    if args.pack:
        if args.pack not in REGISTRY:
            print(f"未知 pack: {args.pack}", file=sys.stderr)
            sys.exit(1)
        results = [audit_pack(REGISTRY[args.pack])]
    else:
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
        if args.fail_on_violation and any(not r['aa_compliant'] for r in results):
            sys.exit(1)
        return

    print(f"\n  ♿ 火一五 PPT WCAG 2.2 AA 文字对比度自检（{len(results)} 个 pack）\n")
    pass_count = sum(1 for r in results if r['aa_compliant'])
    print(f"  AA 合规率: {pass_count}/{len(results)}\n")

    for r in sorted(results, key=lambda x: x['score']):
        icon = '✅' if r['aa_compliant'] else '⚠️ '
        print(f"  {icon} {r['name']:<22} score={r['score']:>3d}  {r['display_name']}")
        for p in r['pairs']:
            mark = '✓' if p['pass'] else '✗'
            print(f"        {mark} {p['pair']:<32} {p['fg']} ↔ {p['bg']}  "
                  f"ratio={p['ratio']:.2f}  目标≥{p['threshold']} ({p['note']})")
        print()

    if args.fail_on_violation and any(not r['aa_compliant'] for r in results):
        sys.exit(1)


if __name__ == '__main__':
    main()
