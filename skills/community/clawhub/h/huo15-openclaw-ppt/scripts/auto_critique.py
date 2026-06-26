#!/usr/bin/env python3
"""
auto_critique.py — v4.0 自动 6 维设计评审（集成 huo15-openclaw-design-critique v2.0）

PPT 输出后一键跑：
  1. 把每张 slide 导出为 PNG（用 web_export → headless Chrome / 或调 LibreOffice）
  2. 跑 anti_slop_audit + wcag_audit + pptx_critique（v3.3 内置）
  3. 引导用户用 huo15-openclaw-design-critique v2.0 跑 6 维深度评审：
     美学 / 可用性 / 品牌一致 / 内容 / 技术实现 / 时代感
     输出 4 档审美档位（AI-Slop / Junior / Senior / Master）+ Master 对标差距

工作模式：
  --mode quick    — 仅跑内置 anti-slop + wcag（不需要 LLM）
  --mode deep     — 跑 quick + 调 design-critique 6 维（需 ANTHROPIC_API_KEY）
  --mode full     — quick + deep + 输出 PNG 截图供人工对比

用法：
    python3 scripts/auto_critique.py --deck /path/deck.json \\
        --pack apple-light --mode quick

    python3 scripts/auto_critique.py --pptx /path/d.pptx --mode full \\
        --output-dir /tmp/critique-report/
"""

from __future__ import annotations
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


CRITIQUE_DIMENSIONS = """\
6 维设计评审（参照 huo15-openclaw-design-critique v2.0）：

1. **美学（Aesthetic）** — 视觉冲击力 / 流派一致性 / 反 AI Slop / 字体对比
2. **可用性（Usability）** — 信息层级 / 阅读流 / 交互暗示 / 移动端适配
3. **品牌一致（Brand）** — 配色与品牌符合 / Logo 使用规范 / 字体延续性
4. **内容（Content）** — 文案质量 / 数据可信 / 故事弧 / 反 AI 腔（Allen 流）
5. **技术实现（Technical）** — 字体嵌入 / 图像分辨率 / 文件大小 / 兼容性
6. **时代感（Era）** — 视觉信号是否过时 / 是否撞 2023-2024 AI 通用风
"""

ERA_SIGNALS_OUTDATED = """\
9 类过时视觉信号（命中即扣分）：
- 紫色渐变背景（2023 AI 主流）
- 圆角卡 + 左侧彩条（Tailwind 默认）
- emoji 当 list bullet
- Inter / Roboto / Arial 默认字体
- iOS 系统色（#007AFF / #FF3B30）直套
- 千篇一律 hero+features+CTA 结构
- 16px / 12px border-radius（Tailwind 默认）
- backdrop-blur 滥用（每个卡都磨砂）
- AI 渐变模糊大色块（紫粉 / 蓝青 blur）
"""


def run_internal_audits(pack: str | None) -> dict:
    """跑 v3.3 内置三件套：anti_slop_audit / wcag_audit / pptx_critique"""
    if not pack:
        return {'error': 'pack 未指定'}

    scripts = Path(__file__).parent
    results = {}

    # 1. anti_slop_audit
    try:
        out = subprocess.run(
            [sys.executable, str(scripts / 'anti_slop_audit.py'), pack, '--json'],
            capture_output=True, text=True, timeout=10,
        )
        if out.returncode == 0:
            data = json.loads(out.stdout)
            results['anti_slop'] = data[0] if isinstance(data, list) else data
    except Exception as e:
        results['anti_slop'] = {'error': str(e)}

    # 2. wcag_audit
    try:
        out = subprocess.run(
            [sys.executable, str(scripts / 'wcag_audit.py'), pack, '--json'],
            capture_output=True, text=True, timeout=10,
        )
        if out.returncode == 0:
            data = json.loads(out.stdout)
            results['wcag'] = data[0] if isinstance(data, list) else data
    except Exception as e:
        results['wcag'] = {'error': str(e)}

    # 3. pptx_critique 综合（anti-slop 60% + wcag 40%）
    try:
        out = subprocess.run(
            [sys.executable, str(scripts / 'pptx_critique.py'), '--pack', pack, '--json'],
            capture_output=True, text=True, timeout=10,
        )
        if out.returncode == 0:
            results['combined'] = json.loads(out.stdout)
    except Exception as e:
        results['combined'] = {'error': str(e)}

    return results


def export_slides_to_png(deck_path: str, pack: str, output_dir: Path) -> list[Path]:
    """把 deck 的每页转 PNG（先转 HTML 再 headless 截图）"""
    output_dir.mkdir(parents=True, exist_ok=True)
    scripts = Path(__file__).parent

    # 1. JSON → HTML
    html_path = output_dir / 'preview.html'
    subprocess.run([
        sys.executable, str(scripts / 'web_export.py'),
        deck_path, '--pack', pack, '--output', str(html_path),
    ], check=True, capture_output=True)

    # 2. HTML → PNG（用 macOS Chrome headless）
    chrome_paths = [
        '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        '/Applications/Chromium.app/Contents/MacOS/Chromium',
    ]
    chrome = next((p for p in chrome_paths if os.path.exists(p)), None)
    if not chrome:
        return []

    # 用 print-to-pdf 全 deck 一张 PDF，再 pdftoppm 拆 PNG
    pdf_path = output_dir / 'preview.pdf'
    subprocess.run([
        chrome, '--headless', '--disable-gpu', '--no-sandbox',
        '--print-to-pdf=' + str(pdf_path),
        '--print-to-pdf-no-header',
        '--virtual-time-budget=2000',
        f'file://{html_path.absolute()}',
    ], capture_output=True, timeout=30)

    if not pdf_path.exists():
        return []

    # pdftoppm 拆每页 PNG
    subprocess.run([
        'pdftoppm', '-png', '-r', '120',
        str(pdf_path), str(output_dir / 'slide'),
    ], capture_output=True)

    return sorted(output_dir.glob('slide-*.png'))


def render_report(deck: dict, pack: str, audits: dict,
                  pngs: list[Path], mode: str) -> str:
    """生成 Markdown 评审报告"""
    n = len(deck.get('slides', []))
    lines = [
        f'# 火一五 PPT 设计评审报告',
        '',
        f'- pack: `{pack}`',
        f'- slides: {n}',
        f'- mode: {mode}',
        '',
        '## 内置自检（v3.3 三件套）',
        '',
    ]

    if 'combined' in audits and isinstance(audits['combined'], dict) and 'tier' in audits['combined']:
        c = audits['combined']
        tier_icon = {'Master': '🏆', 'Senior': '✅', 'Junior': '⚠️', 'AI-Slop': '❌'}.get(c['tier'], '?')
        lines.extend([
            f'**综合分**: {c["score_combined"]:.1f}  →  {tier_icon} **{c["tier"]}**',
            f'**原因**: {c["tier_reason"]}',
            '',
            f'- 反 AI Slop（视觉个性）: {c["score_anti_slop"]:.1f}',
            f'- WCAG 对比度（可读性）: {c["score_wcag"]:.1f}',
            '',
        ])
        if c.get('keep'):
            lines.append('### ✅ Keep（保持）\n')
            for k in c['keep']:
                lines.append(f'- {k}')
            lines.append('')
        if c.get('fix'):
            lines.append('### ⚠️  Fix（必修）\n')
            for f in c['fix']:
                lines.append(f'- {f}')
            lines.append('')
        if c.get('quick_wins'):
            lines.append('### 💡 Quick Wins（建议）\n')
            for q in c['quick_wins']:
                lines.append(f'- {q}')
            lines.append('')

    if pngs:
        lines.append('## Slide 截图\n')
        for i, p in enumerate(pngs, 1):
            lines.append(f'### Slide {i}\n\n![slide-{i}]({p.name})\n')

    if mode in ('deep', 'full'):
        lines.extend([
            '',
            '## 6 维深度评审引导（huo15-openclaw-design-critique v2.0）',
            '',
            '本工具完成内置自检。如需 4 档审美档位识别（AI-Slop / Junior / Senior / Master）+ ',
            'Master 级标杆对标，请把上方 Slide 截图喂给 design-critique skill：',
            '',
            CRITIQUE_DIMENSIONS,
            '',
            ERA_SIGNALS_OUTDATED,
        ])

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='火一五 PPT v4.0 自动设计评审')
    parser.add_argument('--deck', help='JSON deck 路径（与 --pptx 二选一）')
    parser.add_argument('--pptx', help='已生成的 PPTX 路径（与 --deck 二选一）')
    parser.add_argument('--pack', help='style pack（从 deck 读则可省）')
    parser.add_argument('--mode', choices=['quick', 'deep', 'full'], default='quick')
    parser.add_argument('--output-dir', default='/tmp/critique-report')
    args = parser.parse_args()

    if not args.deck and not args.pptx:
        print("  ✗ 必须指定 --deck 或 --pptx", file=sys.stderr)
        sys.exit(1)

    deck = {}
    pack = args.pack
    if args.deck:
        deck = json.loads(Path(args.deck).read_text())
        pack = pack or deck.get('pack')

    if not pack:
        print("  ✗ pack 未指定（用 --pack 或 deck 内含 pack 字段）", file=sys.stderr)
        sys.exit(1)

    print(f"  🔍 评审 pack={pack} mode={args.mode}", file=sys.stderr)

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"  ⚙️  跑内置自检（anti_slop + wcag + 综合）...", file=sys.stderr)
    audits = run_internal_audits(pack)

    pngs = []
    if args.mode == 'full' and args.deck:
        print(f"  📸 导出每张 slide 为 PNG...", file=sys.stderr)
        pngs = export_slides_to_png(args.deck, pack, out_dir)
        print(f"  ✓ 共 {len(pngs)} 张截图", file=sys.stderr)

    report = render_report(deck, pack, audits, pngs, args.mode)
    report_path = out_dir / 'report.md'
    report_path.write_text(report)
    print(f"  📋 报告: {report_path}", file=sys.stderr)
    print(f"\n{'─' * 60}")
    print(report[:2000])
    if len(report) > 2000:
        print(f"\n... (完整报告见 {report_path})")


if __name__ == '__main__':
    main()
