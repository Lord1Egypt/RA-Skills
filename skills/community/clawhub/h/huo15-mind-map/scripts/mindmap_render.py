"""
mindmap_render.py — 基于 matplotlib 的思维导图渲染器

- 横向树形布局（左侧根，右侧展开）
- 节点用圆角矩形 + 贝塞尔连线
- 多种风格：modern / classic / dark / xiaohongshu
- 输出：PNG / PDF / SVG（由扩展名决定）
"""

from __future__ import annotations

import os
import platform
from dataclasses import dataclass, field
from typing import Dict, List, Optional

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, PathPatch
from matplotlib.path import Path
from matplotlib.font_manager import FontProperties, fontManager

from mindmap_tree import Node


# ============================================================
# 一、字体
# ============================================================

def _find_cjk_font():
    """按平台偏好找中文字体，返回 FontProperties。"""
    candidates_mac = [
        'PingFang SC', 'Hiragino Sans GB', 'Hiragino Sans', 'STHeiti',
        'Heiti SC', 'Songti SC', 'Arial Unicode MS',
    ]
    candidates_win = ['Microsoft YaHei', 'SimHei', 'SimSun']
    candidates_linux = ['Noto Sans CJK SC', 'WenQuanYi Micro Hei',
                        'DejaVu Sans']

    system = platform.system()
    if system == 'Darwin':
        prefs = candidates_mac + candidates_win + candidates_linux
    elif system == 'Windows':
        prefs = candidates_win + candidates_mac + candidates_linux
    else:
        prefs = candidates_linux + candidates_mac + candidates_win

    installed = {f.name for f in fontManager.ttflist}
    for name in prefs:
        if name in installed:
            return FontProperties(family=name)
    return FontProperties()


_CJK_FONT = None


def get_cjk_font():
    global _CJK_FONT
    if _CJK_FONT is None:
        _CJK_FONT = _find_cjk_font()
        matplotlib.rcParams['font.family'] = _CJK_FONT.get_name()
    return _CJK_FONT


# ============================================================
# 二、风格
# ============================================================

@dataclass
class Style:
    name: str
    bg: str = '#FFFFFF'
    root_fill: str = '#1F77B4'
    root_text: str = '#FFFFFF'
    branch_palette: List[str] = field(default_factory=lambda: [
        '#FF6B6B', '#F6A738', '#4ECDC4', '#556CC9', '#8E44AD', '#27AE60',
    ])
    branch_text: str = '#FFFFFF'
    leaf_fill: str = '#FFFFFF'
    leaf_stroke: str = '#CCCCCC'
    leaf_text: str = '#333333'
    edge_width: float = 2.0
    edge_alpha: float = 0.85
    font_title: float = 18
    font_branch: float = 14
    font_leaf: float = 11
    rounding: float = 0.35
    pad: float = 0.16


STYLE_MODERN = Style(
    name='modern',
    bg='#FFFFFF',
    root_fill='#2C3E50',
    root_text='#FFFFFF',
    branch_palette=['#E74C3C', '#E67E22', '#27AE60', '#2980B9',
                    '#8E44AD', '#16A085'],
    leaf_fill='#FDFEFE',
    leaf_stroke='#BDC3C7',
    leaf_text='#2C3E50',
)

STYLE_CLASSIC = Style(
    name='classic',
    bg='#FAFAFA',
    root_fill='#374785',
    root_text='#FFFFFF',
    branch_palette=['#A8D0DB', '#F7B538', '#DB3A34', '#6DA34D',
                    '#524B7F', '#117A65'],
    leaf_fill='#FFFFFF',
    leaf_stroke='#AAAAAA',
    leaf_text='#333333',
    rounding=0.15,
)

STYLE_DARK = Style(
    name='dark',
    bg='#0F172A',
    root_fill='#38BDF8',
    root_text='#0F172A',
    branch_palette=['#F472B6', '#F59E0B', '#34D399', '#60A5FA',
                    '#A78BFA', '#F87171'],
    branch_text='#0F172A',
    leaf_fill='#1E293B',
    leaf_stroke='#334155',
    leaf_text='#E2E8F0',
    edge_alpha=0.9,
)

STYLE_XIAOHONGSHU = Style(
    name='xiaohongshu',
    bg='#FFF8F3',
    root_fill='#FF2442',
    root_text='#FFFFFF',
    branch_palette=['#FF2442', '#FF7043', '#FFB347', '#6BCB77',
                    '#4D96FF', '#9D4EDD'],
    leaf_fill='#FFFFFF',
    leaf_stroke='#F5E6E6',
    leaf_text='#1A1A1A',
    rounding=0.45,
)

STYLE_OCEAN = Style(
    name='ocean',
    bg='#F8FBFE',
    root_fill='#0077B6',
    root_text='#FFFFFF',
    branch_palette=['#023E8A', '#0096C7', '#48CAE4', '#00B4D8',
                    '#FB8500', '#219EBC'],
    leaf_fill='#E7F5FA',
    leaf_stroke='#90CAF9',
    leaf_text='#023E8A',
)

STYLE_FOREST = Style(
    name='forest',
    bg='#F7FAF8',
    root_fill='#2D6A4F',
    root_text='#FFFFFF',
    branch_palette=['#40916C', '#52B788', '#95D5B2', '#D68C45',
                    '#B08968', '#1B4332'],
    leaf_fill='#F1F8E9',
    leaf_stroke='#AED581',
    leaf_text='#1B4332',
)

STYLE_SUNSET = Style(
    name='sunset',
    bg='#FFFBF5',
    root_fill='#E76F51',
    root_text='#FFFFFF',
    branch_palette=['#F4A261', '#E9C46A', '#2A9D8F', '#264653',
                    '#E76F51', '#F2CC8F'],
    leaf_fill='#FFF6E9',
    leaf_stroke='#F4A261',
    leaf_text='#9D3B1E',
)

STYLE_MINIMAL = Style(
    name='minimal',
    bg='#FFFFFF',
    root_fill='#2E2E2E',
    root_text='#FFFFFF',
    branch_palette=['#404040', '#595959', '#737373', '#8C8C8C',
                    '#0A4D8E', '#A6A6A6'],
    leaf_fill='#FAFAFA',
    leaf_stroke='#D4D4D4',
    leaf_text='#2E2E2E',
    rounding=0.1,
)

STYLE_PASTEL = Style(
    name='pastel',
    bg='#FFFBFC',
    root_fill='#B5D8FA',
    root_text='#2D3748',
    branch_palette=['#FFB5A7', '#FCD5CE', '#FFE5EC', '#C4A4E1',
                    '#A2D2FF', '#FAD2E1'],
    branch_text='#2D3748',
    leaf_fill='#FFFFFF',
    leaf_stroke='#F7D8D8',
    leaf_text='#2D3748',
    rounding=0.5,
)

STYLE_GITHUB = Style(
    name='github',
    bg='#FFFFFF',
    root_fill='#24292E',
    root_text='#FFFFFF',
    branch_palette=['#0366D6', '#28A745', '#D73A49', '#6F42C1',
                    '#F66A0A', '#005CC5'],
    leaf_fill='#F6F8FA',
    leaf_stroke='#E1E4E8',
    leaf_text='#24292E',
    rounding=0.2,
)

# v1.2 ⭐ 编辑杂志 NYT 风：米色卡底 + 衬线感 + 报头朱红
STYLE_EDITORIAL = Style(
    name='editorial',
    bg='#FAF8F5',                  # 米白底
    root_fill='#0F0F0F',           # 报纸黑
    root_text='#FAF8F5',
    branch_palette=['#D0021B', '#0F0F0F', '#A56B33', '#1F2A1F',
                    '#FF6347', '#3A3A3A'],  # 报头红 + 黑 + 棕 + 深绿 + 番茄红
    leaf_fill='#F5EFE0',           # 米色卡
    leaf_stroke='#D6CFB8',
    leaf_text='#0F0F0F',
    rounding=0.08,                 # 接近直角，杂志感
    edge_width=1.8,
)

# v1.2 ⭐ 包豪斯 三原色硬填 + 黑描边 + 0 圆角
STYLE_BAUHAUS = Style(
    name='bauhaus',
    bg='#FAFAFA',                  # 象牙白
    root_fill='#0A0A0A',           # 黑根节点
    root_text='#FAFAFA',
    branch_palette=['#D32F2F', '#FFD600', '#1565C0', '#0A0A0A',
                    '#D32F2F', '#1565C0'],  # 红黄蓝黑循环
    branch_text='#0A0A0A',         # 分支文字黑（黄底配黑）
    leaf_fill='#FAFAFA',
    leaf_stroke='#0A0A0A',
    leaf_text='#0A0A0A',
    rounding=0.0,                  # 0 圆角，严格几何
    edge_width=2.0,
)

# v1.2 ⭐ 瑞士国际主义 Helvetica 网格 + 黑白红
STYLE_SWISS = Style(
    name='swiss',
    bg='#FFFFFF',                  # 纯白
    root_fill='#000000',           # 黑根
    root_text='#FFFFFF',
    branch_palette=['#000000', '#D4181F', '#666666', '#000000',
                    '#999999', '#D4181F'],  # 黑红灰循环
    leaf_fill='#FFFFFF',
    leaf_stroke='#000000',
    leaf_text='#000000',
    rounding=0.0,                  # 0 圆角
    edge_width=1.0,                # 1px 细描边
)


REGISTRY: Dict[str, Style] = {
    'modern': STYLE_MODERN,
    'classic': STYLE_CLASSIC,
    'dark': STYLE_DARK,
    'xiaohongshu': STYLE_XIAOHONGSHU,
    'xhs': STYLE_XIAOHONGSHU,
    '小红书': STYLE_XIAOHONGSHU,
    'ocean': STYLE_OCEAN,
    '海洋': STYLE_OCEAN,
    '蓝': STYLE_OCEAN,
    '蓝色': STYLE_OCEAN,
    'forest': STYLE_FOREST,
    '森林': STYLE_FOREST,
    '绿': STYLE_FOREST,
    '绿色': STYLE_FOREST,
    '自然': STYLE_FOREST,
    'sunset': STYLE_SUNSET,
    '夕阳': STYLE_SUNSET,
    '暖橙': STYLE_SUNSET,
    '橙': STYLE_SUNSET,
    'minimal': STYLE_MINIMAL,
    '极简': STYLE_MINIMAL,
    '素雅': STYLE_MINIMAL,
    '黑白': STYLE_MINIMAL,
    '学术': STYLE_MINIMAL,
    '论文': STYLE_MINIMAL,
    'pastel': STYLE_PASTEL,
    '马卡龙': STYLE_PASTEL,
    '粉嫩': STYLE_PASTEL,
    '粉': STYLE_PASTEL,
    '儿童': STYLE_PASTEL,
    'github': STYLE_GITHUB,
    '极客': STYLE_GITHUB,
    '程序员': STYLE_GITHUB,
    'gh': STYLE_GITHUB,
    '现代': STYLE_MODERN,
    '商务': STYLE_MODERN,
    '经典': STYLE_CLASSIC,
    '稳重': STYLE_CLASSIC,
    '暗色': STYLE_DARK,
    '黑色': STYLE_DARK,
    '霓虹': STYLE_DARK,
    # v1.2 ⭐ 三个有性格风格
    'editorial': STYLE_EDITORIAL,
    '编辑': STYLE_EDITORIAL,
    '杂志': STYLE_EDITORIAL,
    '纽约客': STYLE_EDITORIAL,
    '纽约时报': STYLE_EDITORIAL,
    'nyt': STYLE_EDITORIAL,
    'monocle': STYLE_EDITORIAL,
    'bauhaus': STYLE_BAUHAUS,
    '包豪斯': STYLE_BAUHAUS,
    '三原色': STYLE_BAUHAUS,
    '几何': STYLE_BAUHAUS,
    'swiss': STYLE_SWISS,
    '瑞士': STYLE_SWISS,
    '国际主义': STYLE_SWISS,
    'helvetica': STYLE_SWISS,
    'grid': STYLE_SWISS,
    'müller': STYLE_SWISS,
    'brockmann': STYLE_SWISS,
}


def get_style(name):
    if not name:
        return STYLE_MODERN
    return REGISTRY.get(name.strip().lower(), STYLE_MODERN)


def list_styles():
    return (
        'modern', 'classic', 'dark', 'xiaohongshu',
        'ocean', 'forest', 'sunset', 'minimal', 'pastel', 'github',
    )


# ============================================================
# 三、布局（横向树）
# ============================================================

@dataclass
class Layout:
    node: Node
    depth: int
    x: float = 0.0
    y: float = 0.0
    width: float = 0.0
    height: float = 0.7
    parent: Optional['Layout'] = None
    children: List['Layout'] = field(default_factory=list)


def _estimate_text_width(text, font_size):
    """粗略按字符数估算宽度（英寸）。中文字符占 1 个 width unit，英文 0.6。"""
    w = 0.0
    for ch in text:
        if '\u4e00' <= ch <= '\u9fff':
            w += 1.0
        elif ch.isspace():
            w += 0.4
        else:
            w += 0.58
    width = max(1.2, w * font_size / 20)
    return min(width, 4.8)


def _build_layout(node: Node, depth: int, style: Style, parent=None):
    if depth == 0:
        fs = style.font_title
    elif depth == 1:
        fs = style.font_branch
    else:
        fs = style.font_leaf
    width = _estimate_text_width(node.title, fs) + 0.6
    layout = Layout(node=node, depth=depth, width=width,
                    height=0.8 if depth < 2 else 0.7, parent=parent)
    for child in node.children:
        layout.children.append(_build_layout(child, depth + 1, style, layout))
    return layout


_Y_GAP = 0.38
_X_GAP = 1.1


def _assign_positions(layout: Layout, current_y=[0.0]):
    """后序遍历分配 y 坐标：叶子顺序递增，父节点取子的平均。"""
    if not layout.children:
        layout.y = current_y[0]
        current_y[0] += layout.height + _Y_GAP
        return

    for child in layout.children:
        _assign_positions(child, current_y)

    ys = [c.y for c in layout.children]
    layout.y = (min(ys) + max(ys)) / 2.0


def _assign_x(layout: Layout, x=0.0):
    layout.x = x
    # 下一级从当前节点右边缘 + 间距开始
    next_x = x + layout.width + _X_GAP
    for child in layout.children:
        _assign_x(child, next_x)


def compute_layout(root: Node, style: Style) -> Layout:
    lay = _build_layout(root, 0, style)
    _assign_positions(lay)
    _assign_x(lay)
    return lay


# ============================================================
# 四、绘制
# ============================================================

def _color_for(branch_index, style: Style):
    palette = style.branch_palette
    return palette[branch_index % len(palette)]


def _draw_box(ax, layout, fill, stroke, text_color, font_size,
              rounding, bold=False):
    x, y = layout.x, layout.y
    w, h = layout.width, layout.height
    patch = FancyBboxPatch(
        (x, y - h / 2),
        w, h,
        boxstyle=f'round,pad=0.02,rounding_size={rounding}',
        linewidth=1.6,
        edgecolor=stroke,
        facecolor=fill,
        zorder=3,
    )
    ax.add_patch(patch)
    font = get_cjk_font()
    weight = 'bold' if bold else 'normal'
    ax.text(x + w / 2, y, layout.node.title,
            ha='center', va='center',
            fontsize=font_size, fontweight=weight,
            color=text_color,
            fontproperties=font,
            zorder=5, wrap=True)


def _draw_edge(ax, parent, child, color, width, alpha):
    x0 = parent.x + parent.width
    y0 = parent.y
    x1 = child.x
    y1 = child.y

    mx = (x0 + x1) / 2
    verts = [(x0, y0), (mx, y0), (mx, y1), (x1, y1)]
    codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
    path = Path(verts, codes)
    patch = PathPatch(path, facecolor='none', edgecolor=color,
                      linewidth=width, alpha=alpha, zorder=2,
                      capstyle='round')
    ax.add_patch(patch)


def _walk_draw(ax, layout, style: Style, branch_index=0):
    if layout.depth == 0:
        _draw_box(ax, layout,
                  fill=style.root_fill, stroke=style.root_fill,
                  text_color=style.root_text,
                  font_size=style.font_title, rounding=style.rounding + 0.15,
                  bold=True)
    elif layout.depth == 1:
        color = _color_for(branch_index, style)
        _draw_box(ax, layout,
                  fill=color, stroke=color,
                  text_color=style.branch_text,
                  font_size=style.font_branch, rounding=style.rounding,
                  bold=True)
    else:
        _draw_box(ax, layout,
                  fill=style.leaf_fill, stroke=style.leaf_stroke,
                  text_color=style.leaf_text,
                  font_size=style.font_leaf, rounding=style.rounding)

    for i, child in enumerate(layout.children):
        branch_idx = i if layout.depth == 0 else branch_index
        color = _color_for(branch_idx, style)
        _draw_edge(ax, layout, child, color=color,
                   width=style.edge_width, alpha=style.edge_alpha)
        _walk_draw(ax, child, style, branch_idx)


def render(root: Node, output_path, style_name='modern',
           dpi=200, title_text=None):
    style = get_style(style_name)
    layout = compute_layout(root, style)

    # 计算画布范围
    xs, ys = [], []
    for lay, _ in _iter(layout):
        xs.append(lay.x)
        xs.append(lay.x + lay.width)
        ys.append(lay.y - lay.height / 2)
        ys.append(lay.y + lay.height / 2)
    if not xs:
        xs = [0, 1]
        ys = [0, 1]

    width = max(xs) - min(xs) + 2.0
    height = max(ys) - min(ys) + 2.0
    width = max(width, 7)
    height = max(height, 5)

    fig, ax = plt.subplots(figsize=(width, height), dpi=dpi)
    fig.patch.set_facecolor(style.bg)
    ax.set_facecolor(style.bg)
    ax.set_xlim(min(xs) - 0.8, max(xs) + 1.0)
    ax.set_ylim(min(ys) - 0.8, max(ys) + 1.2)
    ax.set_aspect('equal')
    ax.axis('off')

    if title_text:
        font = get_cjk_font()
        ax.text((min(xs) + max(xs)) / 2, max(ys) + 0.8, title_text,
                ha='center', va='bottom', fontsize=22, fontweight='bold',
                color=style.leaf_text,
                fontproperties=font, zorder=6)

    _walk_draw(ax, layout, style)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)) or '.',
                exist_ok=True)
    ext = os.path.splitext(output_path)[1].lower().lstrip('.')
    if ext == 'pdf':
        fig.savefig(output_path, format='pdf', bbox_inches='tight',
                    facecolor=style.bg)
    elif ext == 'svg':
        fig.savefig(output_path, format='svg', bbox_inches='tight',
                    facecolor=style.bg)
    else:
        fig.savefig(output_path, format='png', bbox_inches='tight',
                    facecolor=style.bg, dpi=dpi)
    plt.close(fig)
    return output_path


def _iter(layout):
    yield layout, layout.depth
    for child in layout.children:
        yield from _iter(child)
