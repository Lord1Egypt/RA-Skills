#!/usr/bin/env python3
"""
smart_layouts.py — v3.5 Smart Layouts（媲美 Gamma 12+ smart layouts）

4 种生产级布局，matplotlib 渲染为 PNG 嵌入 slide：
  smart_timeline  横向多节点时间线（4-7 个里程碑）
  smart_pyramid   金字塔（3-5 层，从下往上收窄）
  smart_funnel    漏斗（3-6 层，从上往下收窄）
  smart_steps     步骤箭头（左→右 3-7 步，自动衔接）

每个布局：
  - 用当前 StylePack palette（accent / text / bg）
  - CJK 字体 fallback（PingFang SC / Heiti / Noto Sans CJK SC）
  - 高 DPI（默认 200）
  - 自适应文字长度 + 换行

用法 (CLI)：
    python3 scripts/smart_layouts.py timeline --pack apple-light \\
        --nodes "2024Q1=团队组建|2024Q3=产品 MVP|2025Q1=A 轮融资|2026Q1=10万 DAU" \\
        --output ./timeline.png

    python3 scripts/smart_layouts.py pyramid --pack guofeng \\
        --layers "愿景|战略|战术|执行" --output ./pyramid.png

    python3 scripts/smart_layouts.py funnel --pack tech-minimal \\
        --layers "访问 10万|注册 1万|付费 1千|留存 200" --output ./funnel.png

    python3 scripts/smart_layouts.py steps --pack ink-wash \\
        --steps "调研|设计|开发|测试|上线" --output ./steps.png

用法 (Python)：
    from smart_layouts import render_layout
    png = render_layout('pyramid', layers=['愿景', '战略', '战术', '执行'],
                        pack_name='apple-light', title='OKR 体系')
"""

from __future__ import annotations
import argparse
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def _setup_chinese_font():
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
    defaults = {
        'bg': '#FFFFFF', 'text': '#1D1D1F', 'text_sec': '#424245',
        'accent': '#0071E3', 'border': '#D2D2D7',
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


def _setup_fig(width: float, height: float, dpi: int, transparent: bool, colors: dict):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(width, height), dpi=dpi)
    if transparent:
        fig.patch.set_alpha(0)
        ax.set_facecolor('none')
    else:
        fig.patch.set_facecolor(colors['bg'])
        ax.set_facecolor(colors['bg'])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    return fig, ax


def _to_buf(fig, dpi, transparent, bg_color):
    import matplotlib.pyplot as plt
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=dpi,
                facecolor='none' if transparent else bg_color,
                transparent=transparent, bbox_inches='tight', pad_inches=0.3)
    plt.close(fig)
    return buf.getvalue()


# ============================================================
# 1. Timeline — 横向多节点
# ============================================================

def render_timeline(nodes: list[tuple[str, str]], *,
                    pack_name: str | None = None,
                    title: str = '',
                    width: float = 14, height: float = 6,
                    dpi: int = 200, transparent: bool = False) -> bytes:
    """nodes: [(date, label), ...]"""
    _setup_chinese_font()
    c = _get_pack_colors(pack_name)
    fig, ax = _setup_fig(width, height, dpi, transparent, c)

    if title:
        ax.text(50, 92, title, ha='center', va='center',
                fontsize=18, fontweight='bold', color=c['text'])

    n = len(nodes)
    if n == 0:
        return _to_buf(fig, dpi, transparent, c['bg'])
    xs = [10 + 80 * i / max(n - 1, 1) for i in range(n)]
    y_line = 50

    # 主线
    ax.plot([xs[0], xs[-1]], [y_line, y_line], color=c['border'], linewidth=2,
            zorder=1)

    for i, ((date, label), x) in enumerate(zip(nodes, xs)):
        # 节点圆
        ax.scatter([x], [y_line], s=400, color=c['accent'], zorder=3,
                   edgecolors=c['bg'], linewidths=2)
        # 编号
        ax.text(x, y_line, str(i + 1), ha='center', va='center',
                fontsize=11, fontweight='bold', color=c['bg'], zorder=4)
        # 日期（线上方）
        ax.text(x, y_line + 12, date, ha='center', va='center',
                fontsize=12, fontweight='bold', color=c['text'])
        # 标签（线下方）
        ax.text(x, y_line - 12, label, ha='center', va='top',
                fontsize=11, color=c['text_sec'], wrap=True)

    return _to_buf(fig, dpi, transparent, c['bg'])


# ============================================================
# 2. Pyramid — 从下往上收窄（3-5 层）
# ============================================================

def render_pyramid(layers: list[str], *,
                   pack_name: str | None = None,
                   title: str = '',
                   width: float = 10, height: float = 8,
                   dpi: int = 200, transparent: bool = False) -> bytes:
    """layers: 从底层到顶层 ['执行', '战术', '战略', '愿景']"""
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon
    from matplotlib.colors import to_rgb
    _setup_chinese_font()
    c = _get_pack_colors(pack_name)
    fig, ax = _setup_fig(width, height, dpi, transparent, c)

    if title:
        ax.text(50, 95, title, ha='center', va='center',
                fontsize=18, fontweight='bold', color=c['text'])

    n = len(layers)
    if n == 0:
        return _to_buf(fig, dpi, transparent, c['bg'])

    # 金字塔几何：底层最宽 80，顶层最窄 20
    bottom_y = 10
    top_y = 80
    layer_h = (top_y - bottom_y) / n
    bottom_w = 80
    top_w = 20
    cx = 50

    ar, ag, ab = to_rgb(c['accent'])
    for i, label in enumerate(layers):
        # 当前层的上下宽度（线性插值）
        y0 = bottom_y + i * layer_h
        y1 = bottom_y + (i + 1) * layer_h
        w0 = bottom_w - (bottom_w - top_w) * i / n
        w1 = bottom_w - (bottom_w - top_w) * (i + 1) / n
        verts = [
            (cx - w0 / 2, y0), (cx + w0 / 2, y0),
            (cx + w1 / 2, y1), (cx - w1 / 2, y1),
        ]
        # 越上层颜色越浓
        alpha = 0.4 + 0.5 * (i / max(n - 1, 1))
        ax.add_patch(Polygon(verts, closed=True,
                             facecolor=(ar, ag, ab, alpha),
                             edgecolor=c['bg'], linewidth=2))
        # 标签
        ax.text(cx, (y0 + y1) / 2, label, ha='center', va='center',
                fontsize=14, fontweight='bold', color=c['bg'])

    return _to_buf(fig, dpi, transparent, c['bg'])


# ============================================================
# 3. Funnel — 从上往下收窄（3-6 层，常用转化率）
# ============================================================

def render_funnel(layers: list[str], *,
                  pack_name: str | None = None,
                  title: str = '',
                  width: float = 10, height: float = 8,
                  dpi: int = 200, transparent: bool = False) -> bytes:
    """layers: 从顶层（最大）到底层（最小） ['访问 10万', '注册 1万', '付费 1千']"""
    from matplotlib.patches import Polygon
    from matplotlib.colors import to_rgb
    _setup_chinese_font()
    c = _get_pack_colors(pack_name)
    fig, ax = _setup_fig(width, height, dpi, transparent, c)

    if title:
        ax.text(50, 95, title, ha='center', va='center',
                fontsize=18, fontweight='bold', color=c['text'])

    n = len(layers)
    if n == 0:
        return _to_buf(fig, dpi, transparent, c['bg'])

    bottom_y = 10
    top_y = 80
    layer_h = (top_y - bottom_y) / n
    top_w = 80
    bottom_w = 20
    cx = 50

    ar, ag, ab = to_rgb(c['accent'])
    for i, label in enumerate(layers):
        # 第 i 层（从顶往下）
        y1 = top_y - i * layer_h         # 上边
        y0 = top_y - (i + 1) * layer_h   # 下边
        w1 = top_w - (top_w - bottom_w) * i / n
        w0 = top_w - (top_w - bottom_w) * (i + 1) / n
        verts = [
            (cx - w0 / 2, y0), (cx + w0 / 2, y0),
            (cx + w1 / 2, y1), (cx - w1 / 2, y1),
        ]
        alpha = 0.9 - 0.5 * (i / max(n - 1, 1))  # 上深下浅
        ax.add_patch(Polygon(verts, closed=True,
                             facecolor=(ar, ag, ab, alpha),
                             edgecolor=c['bg'], linewidth=2))
        ax.text(cx, (y0 + y1) / 2, label, ha='center', va='center',
                fontsize=13, fontweight='bold', color=c['bg'])

    return _to_buf(fig, dpi, transparent, c['bg'])


# ============================================================
# 4. Steps — 左→右步骤箭头（3-7 步）
# ============================================================

def render_steps(steps: list[str], *,
                 pack_name: str | None = None,
                 title: str = '',
                 width: float = 14, height: float = 5,
                 dpi: int = 200, transparent: bool = False) -> bytes:
    """steps: ['调研', '设计', '开发', '测试', '上线']"""
    from matplotlib.patches import FancyArrowPatch
    from matplotlib.colors import to_rgb
    _setup_chinese_font()
    c = _get_pack_colors(pack_name)
    fig, ax = _setup_fig(width, height, dpi, transparent, c)

    if title:
        ax.text(50, 92, title, ha='center', va='center',
                fontsize=18, fontweight='bold', color=c['text'])

    n = len(steps)
    if n == 0:
        return _to_buf(fig, dpi, transparent, c['bg'])

    box_w = 80 / n
    pad = 1.0
    y_top = 60
    y_bot = 35

    ar, ag, ab = to_rgb(c['accent'])
    for i, label in enumerate(steps):
        x0 = 10 + i * box_w + pad
        x1 = 10 + (i + 1) * box_w - pad
        cx = (x0 + x1) / 2
        # 阶梯式着色（越往后越深）
        alpha = 0.4 + 0.5 * (i / max(n - 1, 1))
        from matplotlib.patches import FancyBboxPatch
        ax.add_patch(FancyBboxPatch(
            (x0, y_bot), x1 - x0, y_top - y_bot,
            boxstyle='round,pad=0.3', linewidth=0,
            facecolor=(ar, ag, ab, alpha)))
        ax.text(cx, (y_top + y_bot) / 2 + 3, str(i + 1),
                ha='center', va='center', fontsize=11, color=c['bg'])
        ax.text(cx, (y_top + y_bot) / 2 - 4, label,
                ha='center', va='center', fontsize=13,
                fontweight='bold', color=c['bg'])
        # 箭头到下一步
        if i < n - 1:
            arrow_x_start = x1 + 0.3
            arrow_x_end = 10 + (i + 1) * box_w + pad - 0.3
            ax.annotate('', xy=(arrow_x_end, (y_top + y_bot) / 2),
                        xytext=(arrow_x_start, (y_top + y_bot) / 2),
                        arrowprops=dict(arrowstyle='->', color=c['text_sec'],
                                        lw=1.5))

    return _to_buf(fig, dpi, transparent, c['bg'])


# ============================================================
# CLI
# ============================================================

LAYOUTS = {
    'timeline': render_timeline,
    'pyramid': render_pyramid,
    'funnel': render_funnel,
    'steps': render_steps,
}


def render_layout(layout: str, *, pack_name: str | None = None, **kwargs) -> bytes:
    """统一入口"""
    if layout not in LAYOUTS:
        raise ValueError(f"unknown layout {layout!r}, choose from {list(LAYOUTS)}")
    return LAYOUTS[layout](pack_name=pack_name, **kwargs)


def main():
    parser = argparse.ArgumentParser(description='火一五 PPT v3.5 Smart Layouts')
    sub = parser.add_subparsers(dest='layout', required=True)

    # timeline
    p1 = sub.add_parser('timeline', help='横向时间线')
    p1.add_argument('--nodes', required=True,
                    help='节点：date1=label1|date2=label2|...')

    # pyramid
    p2 = sub.add_parser('pyramid', help='金字塔（底→顶）')
    p2.add_argument('--layers', required=True, help='底→顶用 | 分隔')

    # funnel
    p3 = sub.add_parser('funnel', help='漏斗（顶→底）')
    p3.add_argument('--layers', required=True, help='顶→底用 | 分隔')

    # steps
    p4 = sub.add_parser('steps', help='步骤箭头（左→右）')
    p4.add_argument('--steps', required=True, help='步骤名用 | 分隔')

    for p in (p1, p2, p3, p4):
        p.add_argument('--pack', help='style pack 名')
        p.add_argument('--title', default='')
        p.add_argument('--output', '-o', required=True)
        p.add_argument('--dpi', type=int, default=200)
        p.add_argument('--transparent', action='store_true')

    args = parser.parse_args()

    if args.layout == 'timeline':
        nodes = []
        for token in args.nodes.split('|'):
            if '=' in token:
                d, l = token.split('=', 1)
                nodes.append((d.strip(), l.strip()))
        png = render_timeline(nodes, pack_name=args.pack, title=args.title,
                              dpi=args.dpi, transparent=args.transparent)
    elif args.layout == 'pyramid':
        layers = [s.strip() for s in args.layers.split('|') if s.strip()]
        png = render_pyramid(layers, pack_name=args.pack, title=args.title,
                             dpi=args.dpi, transparent=args.transparent)
    elif args.layout == 'funnel':
        layers = [s.strip() for s in args.layers.split('|') if s.strip()]
        png = render_funnel(layers, pack_name=args.pack, title=args.title,
                            dpi=args.dpi, transparent=args.transparent)
    elif args.layout == 'steps':
        steps = [s.strip() for s in args.steps.split('|') if s.strip()]
        png = render_steps(steps, pack_name=args.pack, title=args.title,
                           dpi=args.dpi, transparent=args.transparent)

    Path(args.output).write_bytes(png)
    print(f"✅ {args.layout} 已生成: {args.output} ({len(png)} bytes)")


if __name__ == '__main__':
    main()
