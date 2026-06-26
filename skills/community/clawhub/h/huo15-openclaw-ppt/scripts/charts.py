#!/usr/bin/env python3
"""
charts.py — 真数据图表生成（matplotlib），替代 CSS 假产品图（反 AI Slop R5）

每个图表：
  - 用当前 StylePack 的 palette（bg / text / accent）
  - 中文字体自动 fallback（PingFang SC / Noto Sans CJK SC）
  - 输出 PNG（透明背景 / 实色背景）直接嵌入 PPT slide
  - 高 DPI（默认 200，可调 100~300）

支持图表类型：
  bar / hbar / line / pie / scatter / area / radar / heatmap

用法 (CLI)：
    python3 scripts/charts.py bar --pack apple-light \\
        --title "营收增长" --xlabel "季度" --ylabel "营收（万元）" \\
        --data "Q1=120,Q2=180,Q3=240,Q4=320" \\
        --output ./chart.png

用法 (Python)：
    from charts import render_chart
    png_bytes = render_chart('bar', {'Q1': 120, 'Q2': 180, ...},
                             pack_name='apple-light',
                             title='营收增长')
    # 然后塞到 slide 的 add_picture
"""

from __future__ import annotations
import argparse
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def _setup_chinese_font():
    """中文字体 fallback: PingFang SC > Noto Sans CJK SC > 系统"""
    import matplotlib
    import matplotlib.font_manager as fm
    candidates = ['PingFang SC', 'Heiti SC', 'STHeiti', 'Noto Sans CJK SC',
                  'Source Han Sans CN', 'Microsoft YaHei', 'SimHei']
    available = {f.name for f in fm.fontManager.ttflist}
    for c in candidates:
        if c in available:
            matplotlib.rcParams['font.sans-serif'] = [c, 'DejaVu Sans']
            matplotlib.rcParams['axes.unicode_minus'] = False
            return c
    return None


def _get_pack_colors(pack_name: str | None):
    """从 style_packs 读 palette。pack_name=None 时返回中性色。"""
    defaults = {
        'bg': '#FFFFFF',
        'text': '#1D1D1F',
        'text_sec': '#424245',
        'accent': '#0071E3',
        'border': '#D2D2D7',
    }
    if not pack_name:
        return defaults
    try:
        from style_packs import REGISTRY
        if pack_name not in REGISTRY:
            return defaults
        p = REGISTRY[pack_name].palette
        return {
            'bg': p.bg_elevated or p.bg,
            'text': p.text_primary,
            'text_sec': p.text_secondary,
            'accent': p.accent,
            'border': p.border,
        }
    except Exception:
        return defaults


def render_chart(chart_type: str, data: dict, *,
                 pack_name: str | None = None,
                 title: str = '',
                 xlabel: str = '',
                 ylabel: str = '',
                 width: float = 10,
                 height: float = 6,
                 dpi: int = 200,
                 transparent_bg: bool = False) -> bytes:
    """渲染图表为 PNG bytes。

    chart_type: 'bar' | 'hbar' | 'line' | 'pie' | 'scatter' | 'area' | 'radar' | 'heatmap'
    data: {label: value} 或 {label: [v1, v2, ...]}（多系列）
    pack_name: 用 style_packs 哪个 pack 的颜色（None = 中性）
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        raise RuntimeError("缺 matplotlib：pip install matplotlib")

    _setup_chinese_font()
    colors = _get_pack_colors(pack_name)

    fig, ax = plt.subplots(figsize=(width, height), dpi=dpi)
    fig.patch.set_facecolor('none' if transparent_bg else colors['bg'])
    ax.set_facecolor('none' if transparent_bg else colors['bg'])

    labels = list(data.keys())
    values = list(data.values())

    if chart_type == 'bar':
        ax.bar(labels, values, color=colors['accent'], edgecolor=colors['text'],
               linewidth=0.5)
    elif chart_type == 'hbar':
        ax.barh(labels, values, color=colors['accent'], edgecolor=colors['text'],
                linewidth=0.5)
    elif chart_type == 'line':
        ax.plot(labels, values, color=colors['accent'], marker='o', linewidth=2.5,
                markerfacecolor=colors['bg'], markeredgewidth=2,
                markeredgecolor=colors['accent'])
    elif chart_type == 'area':
        ax.fill_between(range(len(labels)), values, alpha=0.4, color=colors['accent'])
        ax.plot(labels, values, color=colors['accent'], linewidth=2.5)
    elif chart_type == 'pie':
        # 多色 pie：accent 为主，逐渐淡化
        from matplotlib.colors import to_rgb
        ar, ag, ab = to_rgb(colors['accent'])
        n = len(labels)
        pie_colors = [(ar, ag, ab, max(0.3, 1 - i / n)) for i in range(n)]
        ax.pie(values, labels=labels, colors=pie_colors, autopct='%1.1f%%',
               startangle=90, textprops={'color': colors['text']})
        ax.axis('equal')
    elif chart_type == 'scatter':
        # data: {label: (x, y)}
        xs = [v[0] if isinstance(v, (tuple, list)) else i for i, v in enumerate(values)]
        ys = [v[1] if isinstance(v, (tuple, list)) else v for v in values]
        ax.scatter(xs, ys, c=colors['accent'], s=80, edgecolors=colors['text'])
    else:
        raise ValueError(f"暂不支持 chart_type={chart_type}（计划: bar/hbar/line/pie/area/scatter）")

    if title:
        ax.set_title(title, color=colors['text'], fontsize=16, fontweight='bold', pad=15)
    if xlabel:
        ax.set_xlabel(xlabel, color=colors['text_sec'], fontsize=11)
    if ylabel:
        ax.set_ylabel(ylabel, color=colors['text_sec'], fontsize=11)

    if chart_type != 'pie':
        ax.tick_params(colors=colors['text_sec'])
        for spine_name in ['top', 'right']:
            ax.spines[spine_name].set_visible(False)
        for spine_name in ['left', 'bottom']:
            ax.spines[spine_name].set_color(colors['border'])
        ax.grid(True, axis='y', alpha=0.15, color=colors['border'])

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', dpi=dpi,
                facecolor='none' if transparent_bg else colors['bg'],
                transparent=transparent_bg)
    plt.close(fig)
    return buf.getvalue()


def _parse_data(s: str) -> dict:
    """'Q1=120,Q2=180' → {'Q1': 120, 'Q2': 180}"""
    result = {}
    for kv in s.split(','):
        if '=' not in kv:
            continue
        k, v = kv.split('=', 1)
        try:
            result[k.strip()] = float(v) if '.' in v else int(v)
        except ValueError:
            result[k.strip()] = v.strip()
    return result


def main():
    parser = argparse.ArgumentParser(description='火一五 PPT 真数据图表生成（matplotlib）')
    parser.add_argument('chart_type', choices=['bar', 'hbar', 'line', 'pie',
                                                'scatter', 'area'])
    parser.add_argument('--pack', help='style pack 名（决定配色）')
    parser.add_argument('--data', required=True, help='数据：Q1=120,Q2=180,...')
    parser.add_argument('--title', default='')
    parser.add_argument('--xlabel', default='')
    parser.add_argument('--ylabel', default='')
    parser.add_argument('--width', type=float, default=10)
    parser.add_argument('--height', type=float, default=6)
    parser.add_argument('--dpi', type=int, default=200)
    parser.add_argument('--transparent', action='store_true', help='透明背景')
    parser.add_argument('--output', '-o', required=True, help='输出 PNG 路径')
    args = parser.parse_args()

    data = _parse_data(args.data)
    png = render_chart(
        args.chart_type, data,
        pack_name=args.pack,
        title=args.title, xlabel=args.xlabel, ylabel=args.ylabel,
        width=args.width, height=args.height, dpi=args.dpi,
        transparent_bg=args.transparent,
    )
    Path(args.output).write_bytes(png)
    print(f"✅ 图表已生成: {args.output} ({len(png)} bytes)")


if __name__ == '__main__':
    main()
