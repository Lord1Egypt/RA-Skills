"""
design_system.py - 火一五 PPT v3.0 设计系统 tokens

把「审美」分解成 4 层独立 tokens：
  1. Palette     - 配色（不只是 primary/accent，而是完整的层级色）
  2. Typography  - 字体阶梯（hero / section / page / card / body / caption 6 级）
  3. Spacing     - 间距系统（8pt grid）
  4. Elevation   - 卡片/阴影语言

每个 StylePack 聚合这 4 层 tokens + 装饰标志。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from pptx.dml.color import RGBColor


# ============================================================
# 工具
# ============================================================

def hex_to_rgb(hex_str: str) -> RGBColor:
    """#RRGGBB → RGBColor"""
    s = hex_str.lstrip('#')
    return RGBColor(int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16))


# ============================================================
# 一、配色
# ============================================================

@dataclass
class Palette:
    """完整的色板 — 背景 3 级 / 文字 4 级 / 强调 / 边框。"""

    # 背景层次
    bg: str = '#FFFFFF'               # 画布最底
    bg_elevated: str = '#F8F8FA'      # 浮起卡片
    bg_subtle: str = '#F0F0F2'        # 三级背景（分隔块）

    # 文字层次（让正文有呼吸感的关键）
    text_primary: str = '#1D1D1F'     # 主标题 / 核心内容
    text_secondary: str = '#4A4A4F'   # 副标题 / 次要内容
    text_tertiary: str = '#86868B'    # 辅助文字 / 标签
    text_muted: str = '#D2D2D7'       # 最弱文字 / 页码

    # 品牌强调（只在关键位置用）
    accent: str = '#0071E3'           # 主强调（链接、CTA）
    accent_soft: str = '#E6F0FD'      # 弱强调（高亮背景）

    # 边框 / 分隔
    border: str = '#E5E5EA'           # 卡片描边
    divider: str = '#F0F0F2'          # 细分隔线

    # RGBColor 缓存
    def rgb(self, key: str) -> RGBColor:
        return hex_to_rgb(getattr(self, key))


# ============================================================
# 二、字体
# ============================================================

@dataclass
class Typography:
    """字体阶梯。每级包含字号 + 字重 + 字距 + 行高。"""

    # 字体 stack
    display_font: str = 'SF Pro Display'     # 标题用
    display_fallbacks: List[str] = field(
        default_factory=lambda: [
            'PingFang SC', 'Microsoft YaHei', 'Noto Sans CJK SC',
            '-apple-system', 'Helvetica Neue', 'sans-serif',
        ]
    )
    body_font: str = 'SF Pro Text'           # 正文用
    body_fallbacks: List[str] = field(
        default_factory=lambda: [
            'PingFang SC', 'Microsoft YaHei', 'Noto Sans CJK SC',
            '-apple-system', 'sans-serif',
        ]
    )

    # 字号阶梯（pt）— 6 级
    hero: int = 140       # 封面大字（Apple 发布会 hero）
    section: int = 80     # 分章大字
    page_title: int = 44  # 内容页标题
    page_sub: int = 18    # 内容页副标题（英文小字）
    card_title: int = 22  # 卡片标题
    body: int = 15        # 正文
    caption: int = 11     # 标注 / 脚注
    page_number: int = 10 # 页码

    # 字重
    hero_weight: str = 'bold'       # 'bold' | 'semibold' | 'medium' | 'regular'
    section_weight: str = 'bold'
    page_weight: str = 'semibold'
    card_weight: str = 'semibold'
    body_weight: str = 'regular'

    # 字距（tracking，% of em；Apple 风格大字用 -3% 字距）
    hero_tracking: float = -0.03
    section_tracking: float = -0.02
    page_tracking: float = -0.01
    body_tracking: float = 0.0

    # 行高倍数
    hero_leading: float = 0.95
    body_leading: float = 1.45

    # 英文副标题是否大写（Apple 风会全大写）
    uppercase_en_sub: bool = True


# ============================================================
# 三、间距
# ============================================================

@dataclass
class Spacing:
    """8pt grid — 所有间距都是 8 的倍数。单位: inch（与 python-pptx 对齐）。

    8pt ≈ 0.111 inch。
    """
    # 垂直间距
    gutter: float = 0.08         # 6pt — 同组元素之间（超紧凑）
    stack_sm: float = 0.17       # 12pt — 标题到副标题
    stack_md: float = 0.33       # 24pt — 段落之间
    stack_lg: float = 0.66       # 48pt — 大版块之间
    stack_xl: float = 1.33       # 96pt — hero 留白

    # 水平 / 页边距
    margin_x: float = 0.8        # 页面左右大边距
    margin_x_hero: float = 1.2   # 封面/分章用大边距

    # 卡片内边距
    card_pad_x: float = 0.33     # 卡片横向内边距
    card_pad_y: float = 0.25     # 卡片纵向内边距


# ============================================================
# 四、卡片 / 阴影语言
# ============================================================

@dataclass
class Elevation:
    """卡片/描边/阴影规则。python-pptx 不支持真阴影，用偏移填色模拟。"""
    card_radius: float = 0.12       # 圆角 inch
    card_stroke_width: float = 0.5  # pt
    card_stroke_color: str = '#E5E5EA'
    card_fill: str = '#F8F8FA'

    # 假阴影（下方错位色块）
    use_fake_shadow: bool = False
    shadow_color: str = '#00000014'  # 带 alpha 的十六进制（RGBA → 转灰度）
    shadow_offset_y: float = 0.05

    # 卡片语言：flat / outline / soft / glass
    style: str = 'flat'


# ============================================================
# 五、装饰（每种风格独有）
# ============================================================

@dataclass
class Decoration:
    """装饰标志。每个 pack 有自己的视觉口头禅。"""

    # 封面
    cover_hero_align: str = 'center'       # 'center' | 'left' | 'bottom-left'
    cover_hero_case: str = 'as-is'         # 'as-is' | 'upper' | 'lower'
    cover_bottom_line: bool = False        # 底部品牌线条
    cover_top_line: bool = False           # 顶部品牌线条

    # 页面
    page_title_align: str = 'left'
    page_accent_bar: bool = False          # 标题左侧小竖条
    page_en_sub_position: str = 'under'    # 'under' | 'above' | 'none'

    # tag / 胶囊
    tag_style: str = 'pill'                # 'pill' | 'square' | 'underline' | 'none'

    # 数据大字（Apple 特色）
    stat_hero_size: int = 260              # 单数字超大字号
    stat_hero_weight: str = 'bold'

    # 照片 / 图块
    image_treatment: str = 'full'          # 'full' | 'rounded' | 'torn' | 'film'

    # ---- v3.1 科技风新增装饰 ----

    # 背景渐变：(from_hex, to_hex, angle_deg) —— 不为 None 时覆盖纯色背景
    # angle: 0=水平左→右, 90=竖直上→下, 135=对角线
    gradient_bg: Optional[Tuple[str, str, int]] = None

    # 强调色渐变（hero / stat 大字用）：(from_hex, to_hex)
    accent_gradient: Optional[Tuple[str, str]] = None

    # 网格叠加层（科技风招牌装饰）
    grid_overlay: bool = False
    grid_color: str = '#1A1D2E'
    grid_spacing: float = 0.4              # inch
    grid_thickness: float = 0.006          # inch (≈ 0.43pt)

    # 圆点网格（极简点阵）
    dot_grid: bool = False
    dot_color: str = '#2A2D3F'
    dot_spacing: float = 0.5
    dot_size: float = 0.04

    # 强调色发光（stat / hero 周围叠多层半透明椭圆）
    glow_accent: bool = False
    glow_strength: float = 0.6             # 0~1

    # 四角 L 型刻度（取景框感）
    corner_marks: bool = False
    corner_size: float = 0.35
    corner_thickness: float = 0.02

    # 左下开发版本戳
    dev_badge: bool = False
    dev_badge_template: str = 'BUILD · {date}'  # {date} / {year} / {n} 占位

    # 等宽字体（用于 caption / metadata / badge）
    mono_font: Optional[str] = None
    mono_fallbacks: List[str] = field(
        default_factory=lambda: [
            'JetBrains Mono', 'Menlo', 'Monaco', 'Consolas',
            'Source Code Pro', 'Courier New', 'monospace',
        ]
    )

    # 水平扫描线装饰（retro-tech）
    scanline: bool = False
    scanline_color: str = '#1A1D2E'


# ============================================================
# 六、画布 & 完整 StylePack
# ============================================================

@dataclass
class Canvas:
    width: float = 13.33   # inch, 16:9
    height: float = 7.5


@dataclass
class StylePack:
    """一个完整的审美方案：Palette + Typography + Spacing + Elevation + Decoration + Canvas。"""

    name: str
    display_name: str
    tagline: str

    palette: Palette = field(default_factory=Palette)
    typography: Typography = field(default_factory=Typography)
    spacing: Spacing = field(default_factory=Spacing)
    elevation: Elevation = field(default_factory=Elevation)
    decoration: Decoration = field(default_factory=Decoration)
    canvas: Canvas = field(default_factory=Canvas)

    # 页脚 / 页码
    show_footer: bool = True

    # 兼容老的 Style 接口（给现有 pptx_toolkit 用）
    def to_legacy_style(self):
        """把 v3 StylePack 压扁成 v2 Style，让旧代码能跑。"""
        from styles import Style
        p = self.palette
        t = self.typography
        return Style(
            name=self.name,
            slide_width=self.canvas.width,
            slide_height=self.canvas.height,
            bg=p.rgb('bg'),
            card=p.rgb('bg_elevated'),
            accent=p.rgb('accent'),
            text=p.rgb('text_primary'),
            subtext=p.rgb('text_tertiary'),
            light=p.rgb('text_secondary'),
            divider=p.rgb('divider'),
            card_stroke=hex_to_rgb(self.elevation.card_stroke_color),
            card_line_width=self.elevation.card_stroke_width,
            font=t.display_font,
            font_fallback=t.display_fallbacks[0] if t.display_fallbacks else 'PingFang SC',
            size_cover_title=t.hero,
            size_cover_subtitle=t.page_sub,
            size_cover_footnote=t.caption,
            size_page_title=t.page_title,
            size_page_subtitle_en=t.page_sub,
            size_card_title=t.card_title,
            size_body=t.body,
            size_small=t.caption,
            size_footer=t.page_number,
            cover_decoration=self.decoration.cover_top_line or self.decoration.cover_bottom_line,
            show_footer=self.show_footer,
            footer_company_font_size=t.page_number,
            upper_en_subtitle=t.uppercase_en_sub,
        )


# ============================================================
# 七、font-weight 映射（python-pptx 只有 bold/regular）
# ============================================================

def resolve_weight(weight: str) -> bool:
    """python-pptx 不支持 semibold/medium，统一回落到 bold/regular。"""
    return weight in ('bold', 'semibold', 'black', 'heavy')
