"""
styles.py - 可复用的 PPT 风格预设

提供两套开箱即用的风格：
- JOBS_DARK  乔布斯极简暗蓝（原 v1.x 默认）
- XIAOHONGSHU 小红书风格（v2.0 新增，暖奶油 + 小红书红）

每套风格集中定义配色、字体、字号、卡片圆角/描边、封面副标题样式等。
`create-pptx.py` 和 `pptx_toolkit.py` 按风格参数化渲染。
"""

from dataclasses import dataclass, field
from typing import Tuple

from pptx.dml.color import RGBColor


def rgb(hex_str: str) -> RGBColor:
    """#RRGGBB → RGBColor"""
    s = hex_str.lstrip('#')
    return RGBColor(int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16))


@dataclass
class Style:
    """PPT 风格规格。所有尺寸单位为英寸（Inches），字号单位为 Pt。"""

    name: str

    # 画布
    slide_width: float = 13.33
    slide_height: float = 7.5  # 16:9 横版；小红书帖可改 9:16

    # 配色
    bg: RGBColor = field(default_factory=lambda: rgb('#060D1A'))
    card: RGBColor = field(default_factory=lambda: rgb('#0D182A'))
    accent: RGBColor = field(default_factory=lambda: rgb('#FFFFFF'))
    text: RGBColor = field(default_factory=lambda: rgb('#FFFFFF'))
    subtext: RGBColor = field(default_factory=lambda: rgb('#888888'))
    light: RGBColor = field(default_factory=lambda: rgb('#CCCCCC'))
    divider: RGBColor = field(default_factory=lambda: rgb('#333344'))

    # 字体
    font: str = 'PingFang SC'
    font_fallback: str = 'Microsoft YaHei'

    # 字号
    size_cover_title: int = 64
    size_cover_subtitle: int = 26
    size_cover_footnote: int = 14
    size_page_title: int = 28
    size_page_subtitle_en: int = 10
    size_card_title: int = 14
    size_body: int = 11
    size_small: int = 10
    size_footer: int = 9

    # 卡片
    card_line_width: float = 0.5
    card_stroke: RGBColor = field(default_factory=lambda: rgb('#333344'))

    # 封面是否加装饰（小红书风格会开）
    cover_decoration: bool = False

    # 页脚
    show_footer: bool = True
    footer_company_font_size: int = 9

    # 英文副标题是否大写
    upper_en_subtitle: bool = True


JOBS_DARK = Style(
    name='jobs-dark',
    bg=rgb('#060D1A'),
    card=rgb('#0D182A'),
    accent=rgb('#FFFFFF'),
    text=rgb('#FFFFFF'),
    subtext=rgb('#888888'),
    light=rgb('#CCCCCC'),
    divider=rgb('#333344'),
    card_stroke=rgb('#333344'),
)


XIAOHONGSHU = Style(
    name='xiaohongshu',
    # 暖奶油背景，小红书帖经典色调
    bg=rgb('#FFF8F3'),
    card=rgb('#FFFFFF'),
    accent=rgb('#FF2442'),        # 小红书红
    text=rgb('#1A1A1A'),          # 深黑
    subtext=rgb('#8A8A8A'),       # 中灰
    light=rgb('#4A4A4A'),         # 深灰
    divider=rgb('#F2E6E6'),       # 淡粉分隔
    card_stroke=rgb('#F5E6E6'),
    card_line_width=0.75,
    # 稍小字号，避免在暖底上显得笨重
    size_cover_title=60,
    size_cover_subtitle=24,
    size_page_title=30,
    size_card_title=16,
    size_body=12,
    cover_decoration=True,
    upper_en_subtitle=False,
)


XIAOHONGSHU_PORTRAIT = Style(
    name='xiaohongshu-portrait',
    # 9:16 适合直接导出图片发 Feed
    slide_width=7.5,
    slide_height=13.33,
    bg=rgb('#FFF8F3'),
    card=rgb('#FFFFFF'),
    accent=rgb('#FF2442'),
    text=rgb('#1A1A1A'),
    subtext=rgb('#8A8A8A'),
    light=rgb('#4A4A4A'),
    divider=rgb('#F2E6E6'),
    card_stroke=rgb('#F5E6E6'),
    card_line_width=0.75,
    size_cover_title=72,
    size_cover_subtitle=28,
    size_page_title=36,
    size_card_title=18,
    size_body=14,
    cover_decoration=True,
    upper_en_subtitle=False,
)


OCEAN = Style(
    name='ocean',
    bg=rgb('#F8FBFE'),
    card=rgb('#FFFFFF'),
    accent=rgb('#0077B6'),         # 海洋蓝
    text=rgb('#023E8A'),
    subtext=rgb('#5A7A9A'),
    light=rgb('#0077B6'),
    divider=rgb('#CAF0F8'),
    card_stroke=rgb('#CAF0F8'),
    card_line_width=0.75,
    upper_en_subtitle=True,
)


FOREST = Style(
    name='forest',
    bg=rgb('#F7FAF8'),
    card=rgb('#FFFFFF'),
    accent=rgb('#2D6A4F'),         # 森林绿
    text=rgb('#1B4332'),
    subtext=rgb('#5A7A6A'),
    light=rgb('#2D6A4F'),
    divider=rgb('#D8F3DC'),
    card_stroke=rgb('#D8F3DC'),
    card_line_width=0.75,
    upper_en_subtitle=True,
)


SUNSET = Style(
    name='sunset',
    bg=rgb('#FFFBF5'),
    card=rgb('#FFFFFF'),
    accent=rgb('#E76F51'),         # 夕阳橙
    text=rgb('#9D3B1E'),
    subtext=rgb('#A07860'),
    light=rgb('#E76F51'),
    divider=rgb('#FFEBD6'),
    card_stroke=rgb('#FFEBD6'),
    card_line_width=0.75,
    upper_en_subtitle=False,
)


MINIMAL = Style(
    name='minimal',
    bg=rgb('#FFFFFF'),
    card=rgb('#FFFFFF'),
    accent=rgb('#2E2E2E'),         # 近黑强调
    text=rgb('#2E2E2E'),
    subtext=rgb('#8A8A8A'),
    light=rgb('#2E2E2E'),
    divider=rgb('#D4D4D4'),
    card_stroke=rgb('#D4D4D4'),
    card_line_width=0.5,
    # 极简风字号克制
    size_cover_title=60,
    size_cover_subtitle=22,
    size_page_title=26,
    size_card_title=13,
    size_body=11,
    upper_en_subtitle=True,
    cover_decoration=False,
)


PASTEL = Style(
    name='pastel',
    bg=rgb('#FFFBFC'),
    card=rgb('#FFFFFF'),
    accent=rgb('#C4A4E1'),         # 马卡龙紫
    text=rgb('#2D3748'),
    subtext=rgb('#8B8B95'),
    light=rgb('#B5D8FA'),
    divider=rgb('#FFE5EC'),
    card_stroke=rgb('#FFE5EC'),
    card_line_width=0.75,
    upper_en_subtitle=False,
)


GITHUB = Style(
    name='github',
    bg=rgb('#FFFFFF'),
    card=rgb('#F6F8FA'),
    accent=rgb('#0366D6'),         # GitHub 蓝
    text=rgb('#24292E'),
    subtext=rgb('#586069'),
    light=rgb('#28A745'),           # 辅助绿
    divider=rgb('#E1E4E8'),
    card_stroke=rgb('#E1E4E8'),
    card_line_width=0.5,
    upper_en_subtitle=True,
)


TECH_BLUE = Style(
    # 经典科技深蓝，适合企业/科技/投融资
    name='tech-blue',
    bg=rgb('#0A2540'),
    card=rgb('#133A6A'),
    accent=rgb('#00D4FF'),          # 霓虹蓝强调
    text=rgb('#FFFFFF'),
    subtext=rgb('#A3B8D0'),
    light=rgb('#64A6E8'),
    divider=rgb('#1E4D7F'),
    card_stroke=rgb('#1E4D7F'),
    card_line_width=0.75,
    upper_en_subtitle=True,
    cover_decoration=False,
)


REGISTRY = {
    'jobs': JOBS_DARK,
    'jobs-dark': JOBS_DARK,
    'dark': JOBS_DARK,
    '暗色': JOBS_DARK,
    '乔布斯': JOBS_DARK,
    'xiaohongshu': XIAOHONGSHU,
    'xhs': XIAOHONGSHU,
    '小红书': XIAOHONGSHU,
    '奶油': XIAOHONGSHU,
    'xiaohongshu-portrait': XIAOHONGSHU_PORTRAIT,
    'xhs-portrait': XIAOHONGSHU_PORTRAIT,
    '小红书竖版': XIAOHONGSHU_PORTRAIT,
    'ocean': OCEAN,
    '海洋': OCEAN,
    '蓝': OCEAN,
    '蓝色': OCEAN,
    'forest': FOREST,
    '森林': FOREST,
    '绿': FOREST,
    '绿色': FOREST,
    '自然': FOREST,
    'sunset': SUNSET,
    '夕阳': SUNSET,
    '暖橙': SUNSET,
    '橙': SUNSET,
    'minimal': MINIMAL,
    '极简': MINIMAL,
    '素雅': MINIMAL,
    '黑白': MINIMAL,
    '学术': MINIMAL,
    '论文': MINIMAL,
    'pastel': PASTEL,
    '马卡龙': PASTEL,
    '粉嫩': PASTEL,
    '粉': PASTEL,
    '儿童': PASTEL,
    'github': GITHUB,
    '极客': GITHUB,
    '程序员': GITHUB,
    'gh': GITHUB,
    'tech-blue': TECH_BLUE,
    'tech_blue': TECH_BLUE,
    'techblue': TECH_BLUE,
    '科技蓝': TECH_BLUE,
    '科技': TECH_BLUE,
    '投融资': TECH_BLUE,
}


def get_style(name: str) -> Style:
    """按名字查风格；未知名称回落到 jobs-dark。"""
    if name in REGISTRY:
        return REGISTRY[name]
    # 大小写/空白容忍
    key = (name or '').strip().lower()
    if key in REGISTRY:
        return REGISTRY[key]
    return JOBS_DARK


def list_styles() -> Tuple[str, ...]:
    """返回主要风格名（用于 CLI --help）。"""
    return (
        'jobs-dark',
        'xiaohongshu',
        'xiaohongshu-portrait',
        'ocean',
        'forest',
        'sunset',
        'minimal',
        'pastel',
        'github',
        'tech-blue',
    )
