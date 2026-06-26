#!/usr/bin/env python3
"""
pptx_critique.py — PPT 输出后跑设计自评（集成 design-critique v2.0 6 维 + 雷达图）

跑两层评审：
  1. 内置自检：anti_slop_audit (15 条红线) + wcag_audit (AA 对比度)
  2. 引导用户用 huo15-openclaw-design-critique 跑深度 6 维评审（美学 / 可用性 /
     品牌一致 / 内容 / 技术实现 / 时代感 + 4 档审美档位识别）

输出：
  - 综合分 + 4 档定位（AI-Slop / Junior / Senior / Master）
  - Keep / Fix / Quick Wins 三分类
  - 跑 design-critique CLI 的命令提示

用法：
    # 跑 pack 自检
    python3 scripts/pptx_critique.py --pack apple-light

    # 跑全部 pack 综合评分（仿 design-critique 的多对象对比）
    python3 scripts/pptx_critique.py --all

    # 引导跑 design-critique 深度评审
    python3 scripts/pptx_critique.py --pack apple-light --deep
"""

from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def critique_one_pack(pack_name: str) -> dict:
    """对一个 pack 跑两层自检：anti-slop + wcag，合成综合分"""
    from anti_slop_audit import audit_pack as audit_slop
    from wcag_audit import audit_pack as audit_wcag
    from style_packs import REGISTRY

    if pack_name not in REGISTRY:
        return {'error': f'未知 pack: {pack_name}'}

    pack = REGISTRY[pack_name]
    slop = audit_slop(pack)
    wcag = audit_wcag(pack)

    # 综合分：anti-slop 60% + wcag 40%（视觉个性 vs 可读性）
    combined = round(slop['score'] * 0.6 + wcag['score'] * 0.4, 1)

    if combined >= 90:
        tier = 'Master'
        tier_reason = '反 AI Slop 红线全过 + AA 合规'
    elif combined >= 75:
        tier = 'Senior'
        tier_reason = '主要质量已达，少数维度待提升'
    elif combined >= 50:
        tier = 'Junior'
        tier_reason = '可用，但视觉个性 / 可读性需加强'
    else:
        tier = 'AI-Slop'
        tier_reason = '触红线 / 不可读，需重设计'

    keep = []
    fix = []
    quick_wins = []
    for v in slop['violations']:
        if v['severity'] == 'hard':
            fix.append(f"[反 AI Slop {v['rule']}] {v['detail']}")
        else:
            quick_wins.append(f"[反 AI Slop {v['rule']}] {v['detail']}")
    for p in wcag['pairs']:
        if not p['pass']:
            fix.append(f"[WCAG] {p['pair']} ratio {p['ratio']:.2f} < {p['threshold']}")

    if not fix and not quick_wins:
        keep = ['全部红线 + AA 对比度均已达标，保持当前状态。']

    return {
        'pack': pack_name,
        'display_name': pack.display_name,
        'score_anti_slop': slop['score'],
        'score_wcag': wcag['score'],
        'score_combined': combined,
        'tier': tier,
        'tier_reason': tier_reason,
        'keep': keep,
        'fix': fix,
        'quick_wins': quick_wins,
    }


def render_radar_text(scores: dict) -> str:
    """文本版雷达图（5 档刻度）"""
    dims = list(scores.items())
    max_label = max(len(k) for k, _ in dims)
    out = []
    for label, score in dims:
        filled = int(score / 10)
        bar = '█' * filled + '░' * (10 - filled)
        out.append(f'  {label:<{max_label}}  [{bar}]  {score:>5.1f}')
    return '\n'.join(out)


def main():
    parser = argparse.ArgumentParser(description='火一五 PPT 设计自评（集成 design-critique）')
    parser.add_argument('--pack', help='指定 pack 名')
    parser.add_argument('--all', action='store_true', help='跑全部 pack 综合排名')
    parser.add_argument('--deep', action='store_true',
                        help='输出 huo15-openclaw-design-critique 深度评审引导命令')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    if args.all:
        from style_packs import REGISTRY
        seen_ids = set()
        unique_packs = []
        for p in REGISTRY.values():
            if id(p) in seen_ids:
                continue
            seen_ids.add(id(p))
            unique_packs.append(p)
        results = [critique_one_pack(p.name) for p in unique_packs]
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
            return
        print('\n  🎨 火一五 PPT 21 套 pack 设计自评综合排名\n')
        for r in sorted(results, key=lambda x: -x['score_combined']):
            icon = {'Master': '🏆', 'Senior': '✅',
                    'Junior': '⚠️ ', 'AI-Slop': '❌'}.get(r['tier'], '?')
            print(f"  {icon} {r['score_combined']:>5.1f}  {r['pack']:<22}  "
                  f"({r['tier']}) {r['display_name']}")
        return

    pack_name = args.pack or 'apple-light'
    result = critique_one_pack(pack_name)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if 'error' in result:
        print(f"  ✗ {result['error']}", file=sys.stderr)
        sys.exit(1)

    print(f"\n  🎨 火一五 PPT 设计自评：{result['pack']}（{result['display_name']}）\n")
    print(f"  综合分：{result['score_combined']:.1f}  →  {result['tier']}")
    print(f"  原因：{result['tier_reason']}\n")
    print('  分维度：')
    print(render_radar_text({
        '反 AI Slop（视觉个性）': result['score_anti_slop'],
        'WCAG 对比度（可读性）': result['score_wcag'],
    }))

    if result['keep']:
        print('\n  ✅ Keep（保持）:')
        for k in result['keep']:
            print(f'     • {k}')
    if result['fix']:
        print('\n  ⚠️  Fix（必修）:')
        for f in result['fix']:
            print(f'     • {f}')
    if result['quick_wins']:
        print('\n  💡 Quick Wins（建议）:')
        for q in result['quick_wins']:
            print(f'     • {q}')

    if args.deep:
        print('\n  🔍 深度 6 维评审（用 huo15-openclaw-design-critique）：')
        print(f'     1. 把 PPT 导出为 PNG（每张 slide 一张）')
        print(f'     2. 调用 huo15-openclaw-design-critique 跑：')
        print(f'        美学 / 可用性 / 品牌一致 / 内容 / 技术实现 / 时代感 6 维')
        print(f'     3. 拿 4 档审美档位（AI-Slop / Junior / Senior / Master）')
        print(f'     4. 对照 8 流派 Master 级标杆找差距')

    print()


if __name__ == '__main__':
    main()
