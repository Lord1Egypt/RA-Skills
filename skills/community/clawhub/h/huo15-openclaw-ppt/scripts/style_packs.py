"""
style_packs.py - 火一五 PPT v3.2 的 21+ 真·审美方案

每个 pack 是完整的 StylePack（Palette + Typography + Spacing + Elevation + Decoration）。

v3.0 基础 4 套：
  apple-keynote       - Apple 发布会（纯黑 + SF Pro + 巨字号）
  apple-light         - Apple.com 产品页（纯白 + 磨砂卡 + 极简）
  xiaohongshu-creator - 真·生活博主（奶油 + 鼠尾草 + 焦糖 / 衬线字）
  xiaohongshu-vintage - 博主复古胶片系（琥珀 + 雾霾蓝 / 衬线字）

v3.1 科技双套：
  tech-neon           - 赛博霓虹（深蓝黑 + 电青电紫 + 网格）
  tech-minimal        - Vercel/Linear 极简科技

v3.2 生产级 12 套（新增）：
  liquid-glass        - 🍎 Apple macOS 26 玻璃风（七彩光球 + 半透卡片）
  muji                - ⬜ 原研哉极简（米白 + 朱红印 + 细衬线）
  ink-wash            - 🖋 中国水墨（墨分五色 + 朱砂印 + 飞白）
  guofeng             - 🏮 国风/故宫（朱砂 + 藤黄 + 群青 + 篆刻）
  cyberpunk-vivid     - 🌃 赛博朋克绚彩（深紫黑 + 粉青黄三撞色）
  van-gogh            - 🎨 梵高油画（星夜蓝 + 麦田金 + 笔触感）
  da-vinci            - 📜 达芬奇手稿（羊皮纸 + 棕墨 + 手绘几何）
  xhs-fashion         - 👜 小红书时尚（莫兰迪粉 + 高级灰 + 细金线）
  morandi             - 🎭 莫兰迪高级灰（低饱和粉绿米）
  memphis             - 🔺 孟菲斯（80s 撞色几何）
  bauhaus             - 🟦 包豪斯（三原色 + 几何 + 等宽）
  wes-anderson        - 🍰 韦斯安德森（对称 + 粉绿米色）

附带 3 个 legacy pack 保持向后兼容：jobs-dark / xiaohongshu / xhs-portrait。
"""

from __future__ import annotations

from design_system import (
    StylePack, Palette, Typography, Spacing, Elevation, Decoration, Canvas,
)


# ============================================================
# 一、Apple Keynote（真·发布会暗场）
# ============================================================

APPLE_KEYNOTE = StylePack(
    name='apple-keynote',
    display_name='Apple 发布会（暗场）',
    tagline='纯黑 + SF Pro + 巨字号 + 极致留白',

    canvas=Canvas(width=13.33, height=7.5),

    palette=Palette(
        # Apple 发布会是纯黑而非蓝黑
        bg='#000000',
        bg_elevated='#1C1C1E',
        bg_subtle='#2C2C2E',
        # 文字白色渐变
        text_primary='#F5F5F7',
        text_secondary='#A1A1A6',
        text_tertiary='#86868B',
        text_muted='#48484A',
        # 品牌蓝
        accent='#0A84FF',
        accent_soft='#0A84FF',
        border='#2C2C2E',
        divider='#1C1C1E',
    ),

    typography=Typography(
        display_font='SF Pro Display',
        body_font='SF Pro Text',
        # Apple 发布会级字号
        hero=160,            # 巨字号
        section=96,
        page_title=48,
        page_sub=16,
        card_title=22,
        body=15,
        caption=11,
        page_number=9,
        hero_weight='bold',
        section_weight='bold',
        page_weight='semibold',
        card_weight='semibold',
        body_weight='regular',
        hero_tracking=-0.03,      # 巨字要收字距
        section_tracking=-0.02,
        page_tracking=-0.01,
        hero_leading=0.95,
        body_leading=1.4,
        uppercase_en_sub=True,    # OVERVIEW / INTRO
    ),

    spacing=Spacing(
        gutter=0.08,
        stack_sm=0.17,
        stack_md=0.33,
        stack_lg=0.66,
        stack_xl=1.33,
        margin_x=0.8,
        margin_x_hero=1.2,
        card_pad_x=0.33,
        card_pad_y=0.25,
    ),

    elevation=Elevation(
        card_radius=0.12,
        card_stroke_width=0.0,      # 无描边
        card_stroke_color='#2C2C2E',
        card_fill='#1C1C1E',
        use_fake_shadow=False,
        style='flat',
    ),

    decoration=Decoration(
        cover_hero_align='center',
        cover_hero_case='as-is',
        cover_bottom_line=False,
        cover_top_line=False,
        page_title_align='left',
        page_accent_bar=False,
        page_en_sub_position='under',
        tag_style='none',
        stat_hero_size=280,          # Apple 的 "2 Billion" 页
        stat_hero_weight='bold',
        image_treatment='full',
    ),
    show_footer=False,               # Apple 不显示页脚
)


# ============================================================
# 二、Apple Light（Apple.com 产品页）
# ============================================================

APPLE_LIGHT = StylePack(
    name='apple-light',
    display_name='Apple.com（白场）',
    tagline='纯白 + 磨砂卡 + 极简克制',

    canvas=Canvas(width=13.33, height=7.5),

    palette=Palette(
        bg='#FFFFFF',
        bg_elevated='#F5F5F7',      # Apple.com 的经典卡片灰
        bg_subtle='#FBFBFD',
        text_primary='#1D1D1F',
        text_secondary='#424245',
        text_tertiary='#6E6E73',
        text_muted='#D2D2D7',
        accent='#0071E3',           # Apple.com 的链接蓝
        accent_soft='#E6F0FD',
        border='#D2D2D7',
        divider='#F5F5F7',
    ),

    typography=Typography(
        display_font='SF Pro Display',
        body_font='SF Pro Text',
        hero=120,
        section=72,
        page_title=44,
        page_sub=15,
        card_title=21,
        body=15,
        caption=11,
        page_number=10,
        hero_tracking=-0.025,
        section_tracking=-0.02,
        page_tracking=-0.01,
        hero_leading=1.0,
        body_leading=1.45,
        uppercase_en_sub=False,
    ),

    spacing=Spacing(
        margin_x=0.8,
        margin_x_hero=1.0,
    ),

    elevation=Elevation(
        card_radius=0.18,           # 圆角更圆
        card_stroke_width=0.0,      # 无描边，靠填色区分
        card_stroke_color='#D2D2D7',
        card_fill='#F5F5F7',
        use_fake_shadow=False,
        style='soft',
    ),

    decoration=Decoration(
        cover_hero_align='center',
        stat_hero_size=200,
        image_treatment='rounded',
    ),
    show_footer=True,
)


# ============================================================
# 三、小红书博主风（奶油 + 鼠尾草 + 焦糖）
# ============================================================

XHS_CREATOR = StylePack(
    name='xiaohongshu-creator',
    display_name='小红书博主（奶油生活系）',
    tagline='奶油 + 鼠尾草 + 焦糖咖 + 衬线字',

    canvas=Canvas(width=13.33, height=7.5),

    palette=Palette(
        # 博主风是奶油底 + 低饱和
        bg='#FBF7F0',               # 奶油主背
        bg_elevated='#FFFFFF',      # 纯白卡片
        bg_subtle='#F5F1EA',        # 次奶油
        # 文字不用纯黑，用焦糖咖色
        text_primary='#3E2E1F',     # 焦糖咖替代黑
        text_secondary='#8B6F47',   # 奶茶咖
        text_tertiary='#B3A28A',    # 浅咖
        text_muted='#D4C8B8',
        # 鼠尾草绿作为点缀主色
        accent='#9FAE8B',           # 鼠尾草
        accent_soft='#E6EAD9',
        border='#E8DFD0',
        divider='#F0E8D9',
    ),

    typography=Typography(
        # 博主风关键：衬线字体！
        display_font='Noto Serif SC',
        display_fallbacks=[
            'Source Han Serif SC', 'Songti SC',
            'STSong', 'SimSun', 'serif',
        ],
        body_font='PingFang SC',
        body_fallbacks=[
            'Noto Sans CJK SC', 'Microsoft YaHei', 'sans-serif',
        ],
        hero=72,                    # 博主风不需要 Apple 那种巨字
        section=52,
        page_title=32,
        page_sub=14,
        card_title=18,
        body=14,
        caption=11,
        page_number=10,
        hero_weight='semibold',     # 衬线字体 semibold 足够
        section_weight='semibold',
        page_weight='semibold',
        card_weight='semibold',
        body_weight='regular',
        hero_tracking=0.02,         # 衬线字要放一点字距
        section_tracking=0.01,
        page_tracking=0.01,
        hero_leading=1.15,
        body_leading=1.6,           # 衬线字需要更大行高
        uppercase_en_sub=False,     # 博主风英文不全大写
    ),

    spacing=Spacing(
        margin_x=0.7,
        margin_x_hero=1.0,
        stack_md=0.4,               # 段落间距更大，呼吸感
        stack_lg=0.8,
    ),

    elevation=Elevation(
        card_radius=0.22,           # 圆润
        card_stroke_width=0.75,
        card_stroke_color='#E8DFD0',
        card_fill='#FFFFFF',
        use_fake_shadow=True,       # 微微阴影
        shadow_color='#E8DFD0',
        shadow_offset_y=0.06,
        style='soft',
    ),

    decoration=Decoration(
        cover_hero_align='left',    # 博主封面常左对齐
        cover_bottom_line=False,
        page_title_align='left',
        page_accent_bar=True,       # 标题左侧小竖条
        page_en_sub_position='above',
        tag_style='pill',
        stat_hero_size=140,
        image_treatment='rounded',
    ),
    show_footer=True,
)


# ============================================================
# 四、小红书复古胶片（琥珀 + 雾霾蓝）
# ============================================================

XHS_VINTAGE = StylePack(
    name='xiaohongshu-vintage',
    display_name='小红书博主（复古胶片）',
    tagline='琥珀 + 雾霾蓝 + 衬线字 + 胶片质感',

    canvas=Canvas(width=13.33, height=7.5),

    palette=Palette(
        bg='#F2EAD9',               # 复古米
        bg_elevated='#FFFAF1',      # 象牙白
        bg_subtle='#E8D0CD',        # 琥珀粉
        text_primary='#4A3526',     # 深栗咖
        text_secondary='#7A5C42',
        text_tertiary='#A88B6D',
        text_muted='#C9B195',
        # 雾霾蓝点缀
        accent='#A8B8C6',           # 雾霾蓝
        accent_soft='#D6DFE8',
        border='#D9C8A8',
        divider='#E8D7B5',
    ),

    typography=Typography(
        display_font='Noto Serif SC',
        display_fallbacks=[
            'Source Han Serif SC', 'Songti SC',
            'STSong', 'serif',
        ],
        body_font='Noto Serif SC',   # 胶片风全衬线
        body_fallbacks=[
            'Source Han Serif SC', 'Songti SC', 'serif',
        ],
        hero=64,
        section=46,
        page_title=30,
        page_sub=13,
        card_title=17,
        body=14,
        caption=11,
        page_number=10,
        hero_weight='semibold',
        section_weight='semibold',
        page_weight='semibold',
        card_weight='semibold',
        body_weight='regular',
        hero_tracking=0.03,           # 复古字距更松
        section_tracking=0.02,
        page_tracking=0.01,
        hero_leading=1.2,
        body_leading=1.65,
        uppercase_en_sub=False,
    ),

    spacing=Spacing(
        margin_x=0.75,
        margin_x_hero=1.0,
        stack_md=0.4,
        stack_lg=0.8,
    ),

    elevation=Elevation(
        card_radius=0.08,            # 复古卡片角不要太圆
        card_stroke_width=1.0,
        card_stroke_color='#D9C8A8',
        card_fill='#FFFAF1',
        use_fake_shadow=False,
        style='outline',
    ),

    decoration=Decoration(
        cover_hero_align='left',
        cover_top_line=True,
        cover_bottom_line=True,
        page_title_align='left',
        page_accent_bar=False,
        page_en_sub_position='above',
        tag_style='underline',
        stat_hero_size=110,
        image_treatment='film',
    ),
    show_footer=True,
)


# ============================================================
# 五、Tech Neon（深蓝黑 + 电青电紫霓虹 + 网格）
# ============================================================

TECH_NEON = StylePack(
    name='tech-neon',
    display_name='科技霓虹（赛博黑蓝）',
    tagline='深蓝黑 + 电青→电紫渐变 + 网格 + 辉光',

    canvas=Canvas(width=13.33, height=7.5),

    palette=Palette(
        # 深蓝黑近乎纯黑，但带蓝色投影
        bg='#050510',
        bg_elevated='#0D0D1F',       # 浮起卡片略抬
        bg_subtle='#13152A',         # 更深的分隔背景
        # 文字纯白偏冷
        text_primary='#F0F4FF',
        text_secondary='#8B95B3',    # 冷灰蓝
        text_tertiary='#5A6484',
        text_muted='#2E3550',
        # 电青作为主强调
        accent='#00D9FF',            # electric cyan
        accent_soft='#7C3AED',       # electric purple 作为辅助
        border='#1F2240',
        divider='#13152A',
    ),

    typography=Typography(
        display_font='Space Grotesk',  # v3.3 反 AI Slop R1
        display_fallbacks=[
            'SF Pro Display', 'PingFang SC', 'Microsoft YaHei',
            'Helvetica Neue', 'sans-serif',
        ],
        body_font='JetBrains Mono',  # v3.3 反 AI Slop R1: Inter→JetBrains Mono
        body_fallbacks=[
            'SF Pro Text', 'PingFang SC', 'Microsoft YaHei', 'sans-serif',
        ],
        hero=144,
        section=88,
        page_title=44,
        page_sub=14,
        card_title=22,
        body=15,
        caption=11,
        page_number=9,
        hero_weight='bold',
        section_weight='bold',
        page_weight='semibold',
        card_weight='semibold',
        body_weight='regular',
        hero_tracking=-0.025,        # 数码感大字轻微收紧
        section_tracking=-0.02,
        page_tracking=0.0,
        hero_leading=0.95,
        body_leading=1.5,
        uppercase_en_sub=True,
    ),

    spacing=Spacing(
        margin_x=0.8,
        margin_x_hero=1.0,
        stack_md=0.35,
        stack_lg=0.7,
    ),

    elevation=Elevation(
        card_radius=0.08,            # 科技感不要太圆
        card_stroke_width=0.75,
        card_stroke_color='#1F2240', # 冷灰蓝描边
        card_fill='#0D0D1F',
        use_fake_shadow=False,
        style='outline',
    ),

    decoration=Decoration(
        cover_hero_align='left',     # 科技风封面常左对齐
        cover_hero_case='as-is',
        cover_bottom_line=False,
        cover_top_line=False,
        page_title_align='left',
        page_accent_bar=False,
        page_en_sub_position='above',
        tag_style='square',
        stat_hero_size=260,
        stat_hero_weight='bold',
        image_treatment='full',

        # 科技装饰
        gradient_bg=('#050510', '#0B0E1F', 135),     # 极微对角线渐变，增加深度
        accent_gradient=('#00D9FF', '#7C3AED'),      # 电青→电紫，hero 大字用
        grid_overlay=True,
        grid_color='#12152A',
        grid_spacing=0.4,
        grid_thickness=0.005,
        glow_accent=True,
        glow_strength=0.7,
        corner_marks=True,
        corner_size=0.28,
        corner_thickness=0.018,
        dev_badge=True,
        dev_badge_template='BUILD · {date}',
        mono_font='JetBrains Mono',
        scanline=False,
    ),
    show_footer=True,
)


# ============================================================
# 六、Tech Minimal（Vercel / Linear 风）
# ============================================================

TECH_MINIMAL = StylePack(
    name='tech-minimal',
    display_name='科技极简（Vercel/Linear 风）',
    tagline='近黑 + 电紫 + 点阵 + 等宽 metadata',

    canvas=Canvas(width=13.33, height=7.5),

    palette=Palette(
        # 近黑偏冷
        bg='#0A0A0F',
        bg_elevated='#111118',
        bg_subtle='#16161E',
        # 文字克制
        text_primary='#F4F4F6',
        text_secondary='#9090A0',
        text_tertiary='#606070',
        text_muted='#303040',
        # 电紫为唯一主色
        accent='#0EA5E9',            # v3.3 反 AI Slop R2: 紫(#8B5CF6)→青蓝
        accent_soft='#0284C7',       # v3.3: 浅紫(#A78BFA)→深青蓝
        border='#1F1F28',
        divider='#16161E',
    ),

    typography=Typography(
        display_font='Geist Sans',  # v3.3 反 AI Slop R1
        display_fallbacks=[
            'SF Pro Display', 'PingFang SC', 'Microsoft YaHei',
            'Helvetica Neue', 'sans-serif',
        ],
        body_font='Geist Sans',  # v3.3 反 AI Slop R1: Inter→Geist Sans
        body_fallbacks=[
            'SF Pro Text', 'PingFang SC', 'Microsoft YaHei', 'sans-serif',
        ],
        hero=120,
        section=72,
        page_title=40,
        page_sub=13,
        card_title=20,
        body=14,
        caption=11,
        page_number=9,
        hero_weight='semibold',       # Vercel 风不过粗
        section_weight='semibold',
        page_weight='semibold',
        card_weight='semibold',
        body_weight='regular',
        hero_tracking=-0.02,
        section_tracking=-0.015,
        page_tracking=-0.005,
        hero_leading=1.0,
        body_leading=1.55,
        uppercase_en_sub=True,
    ),

    spacing=Spacing(
        margin_x=0.8,
        margin_x_hero=1.0,
        stack_md=0.35,
        stack_lg=0.7,
    ),

    elevation=Elevation(
        card_radius=0.1,
        card_stroke_width=0.75,
        card_stroke_color='#1F1F28',
        card_fill='#111118',
        use_fake_shadow=False,
        style='outline',
    ),

    decoration=Decoration(
        cover_hero_align='left',
        cover_hero_case='as-is',
        page_title_align='left',
        page_accent_bar=False,
        page_en_sub_position='above',
        tag_style='square',
        stat_hero_size=220,
        stat_hero_weight='semibold',
        image_treatment='rounded',

        # 极简科技装饰：没有网格，只有点阵
        gradient_bg=None,             # 纯色底
        accent_gradient=None,         # 无渐变文字
        grid_overlay=False,
        dot_grid=True,
        dot_color='#1C1C26',
        dot_spacing=0.5,
        dot_size=0.035,
        glow_accent=True,
        glow_strength=0.4,
        corner_marks=False,
        dev_badge=True,
        dev_badge_template='v{year} · BUILD {build}',
        mono_font='JetBrains Mono',
        scanline=False,
    ),
    show_footer=True,
)


# ============================================================
# v3.2 ❶ Liquid Glass — Apple macOS 26 / iOS 26（玻璃风）
#   半透磨砂卡 + 七彩光球 + 大圆角 + 浮空层叠
# ============================================================

LIQUID_GLASS = StylePack(
    name='liquid-glass',
    display_name='Apple Liquid Glass（macOS 26）',
    tagline='半透磨砂玻璃 + 七彩光球 + 浮空层叠',

    canvas=Canvas(width=13.33, height=7.5),

    palette=Palette(
        # 浅色玻璃底（Apple WWDC 25 主视觉）
        bg='#F2F2F7',              # systemGroupedBackgroundLight
        bg_elevated='#FFFFFF',      # 玻璃卡片用纯白叠透明（运行时叠 alpha）
        bg_subtle='#FAFAFC',
        # 文字深灰（玻璃风永远不要纯黑文字）
        text_primary='#1D1D1F',
        text_secondary='#3A3A3C',
        text_tertiary='#6E6E73',
        text_muted='#AEAEB2',
        # Apple system colors（用作光球+强调）
        accent='#0A84FF',           # systemBlue
        accent_soft='#BF5AF2',      # systemPurple（次强调）
        border='#E5E5EA',           # 玻璃边
        divider='#F2F2F7',
    ),

    typography=Typography(
        display_font='SF Pro Display',
        display_fallbacks=[
            'PingFang SC', 'Inter', 'Microsoft YaHei',
            'Helvetica Neue', '-apple-system', 'sans-serif',
        ],
        body_font='SF Pro Text',
        body_fallbacks=[
            'PingFang SC', 'Inter', 'Microsoft YaHei',
            'Helvetica Neue', '-apple-system', 'sans-serif',
        ],
        hero=128,                   # 玻璃卡上的标题不用 Apple 那么巨
        section=80,
        page_title=44,
        page_sub=14,
        card_title=22,
        body=15,
        caption=11,
        page_number=10,
        hero_weight='semibold',     # 玻璃质感配半粗即可
        section_weight='semibold',
        page_weight='semibold',
        card_weight='semibold',
        body_weight='regular',
        hero_tracking=-0.025,
        section_tracking=-0.018,
        page_tracking=-0.008,
        hero_leading=1.0,
        body_leading=1.5,
        uppercase_en_sub=False,
    ),

    spacing=Spacing(
        margin_x=0.9,
        margin_x_hero=1.2,
        stack_md=0.4,
        stack_lg=0.85,
    ),

    elevation=Elevation(
        card_radius=0.5,            # 大圆角是玻璃卡灵魂
        card_stroke_width=0.5,
        card_stroke_color='#FFFFFF',  # 玻璃边白色细线
        card_fill='#FFFFFFE6',         # 90% alpha 白
        use_fake_shadow=True,
        shadow_color='#1D1D1F1A',
        shadow_offset_y=0.08,
        style='glass',
    ),

    decoration=Decoration(
        cover_hero_align='center',
        cover_hero_case='as-is',
        cover_bottom_line=False,
        page_title_align='left',
        page_accent_bar=False,
        page_en_sub_position='above',
        tag_style='pill',
        stat_hero_size=240,
        stat_hero_weight='semibold',
        image_treatment='rounded',

        # 玻璃风招牌：彩色光球渐变背景
        gradient_bg=('#E8F0FE', '#F5E8FE', 135),  # 蓝紫粉极淡渐变
        accent_gradient=('#0A84FF', '#BF5AF2'),    # hero 大字蓝→紫渐变
        grid_overlay=False,
        dot_grid=False,
        glow_accent=True,
        glow_strength=0.85,         # 强光晕模拟折射
        corner_marks=False,
        dev_badge=False,
        mono_font='SF Mono',
        scanline=False,
    ),
    show_footer=True,
)


# ============================================================
# v3.2 ❷ MUJI / 原研哉极简
#   米白 + 朱红方印 + 细衬线 + 70%+ 留白
# ============================================================

MUJI = StylePack(
    name='muji',
    display_name='原研哉极简（无印良品）',
    tagline='纸感米白 + 朱红方印 + 细衬线 + 70% 留白',

    canvas=Canvas(width=13.33, height=7.5),

    palette=Palette(
        bg='#FAF7EB',              # 纸感米白（关键 — 非冷白）
        bg_elevated='#F5F2E8',
        bg_subtle='#F0EDE0',
        text_primary='#2B2B2B',     # 炭墨非纯黑
        text_secondary='#555555',
        text_tertiary='#888888',
        text_muted='#B5907D',       # 原木棕
        accent='#7F0019',           # MUJI 朱红
        accent_soft='#E8D9D9',
        border='#D9D2C0',
        divider='#E5DFD2',
    ),

    typography=Typography(
        display_font='Noto Serif SC',
        display_fallbacks=[
            'Source Han Serif SC', 'Songti SC', 'STSong',
            'Hiragino Mincho ProN', 'serif',
        ],
        body_font='Noto Sans SC',
        body_fallbacks=[
            'PingFang SC', 'Hiragino Sans', 'Microsoft YaHei',
            'Helvetica Neue Light', 'sans-serif',
        ],
        hero=72,                    # 原研哉风字号克制
        section=48,
        page_title=30,
        page_sub=12,
        card_title=16,
        body=13,
        caption=10,
        page_number=9,
        hero_weight='regular',      # 极轻字重是关键
        section_weight='regular',
        page_weight='regular',
        card_weight='regular',
        body_weight='regular',
        hero_tracking=0.04,         # 字距大 — 呼吸感
        section_tracking=0.03,
        page_tracking=0.02,
        body_tracking=0.01,
        hero_leading=1.4,
        body_leading=1.8,           # 行高极大
        uppercase_en_sub=False,
    ),

    spacing=Spacing(
        gutter=0.12,
        stack_sm=0.25,
        stack_md=0.55,              # 间距巨大 — 留白美学
        stack_lg=1.1,
        stack_xl=2.0,
        margin_x=1.5,               # 边距夸张
        margin_x_hero=2.0,
        card_pad_x=0.5,
        card_pad_y=0.4,
    ),

    elevation=Elevation(
        card_radius=0.0,            # 不要圆角
        card_stroke_width=0.25,     # 0.25pt 发丝线
        card_stroke_color='#B5907D',
        card_fill='#F5F2E8',
        use_fake_shadow=False,
        style='outline',
    ),

    decoration=Decoration(
        cover_hero_align='left',
        cover_hero_case='as-is',
        cover_bottom_line=False,
        cover_top_line=False,
        page_title_align='left',
        page_accent_bar=False,
        page_en_sub_position='above',
        tag_style='none',           # 极简 — 不要胶囊
        stat_hero_size=160,
        stat_hero_weight='regular',
        image_treatment='full',

        gradient_bg=None,
        accent_gradient=None,
        grid_overlay=False,
        dot_grid=False,
        glow_accent=False,
        corner_marks=False,
        dev_badge=False,
        mono_font=None,
        scanline=False,
    ),
    show_footer=True,
)


# ============================================================
# v3.2 ❸ Ink Wash / 中国水墨
#   宣纸底 + 墨分五色 + 朱砂方印 + 飞白笔触
# ============================================================

INK_WASH = StylePack(
    name='ink-wash',
    display_name='中国水墨（墨分五色）',
    tagline='宣纸底 + 焦浓重淡清 + 朱砂印 + 飞白',

    canvas=Canvas(width=13.33, height=7.5),

    palette=Palette(
        bg='#FDFBF5',              # 宣纸米白
        bg_elevated='#F8F5EC',
        bg_subtle='#E8E4D9',        # 宣纸纤维
        text_primary='#1A1A1A',     # 焦墨
        text_secondary='#4A4A4A',   # 浓墨
        text_tertiary='#8B8B8B',    # 重墨
        text_muted='#BFBFBF',       # 淡墨
        accent='#A62828',           # 朱砂印章
        accent_soft='#E8D5D0',
        border='#D9D2C0',
        divider='#E8E4D9',
    ),

    typography=Typography(
        display_font='Noto Serif SC',
        display_fallbacks=[
            'STKaiti', 'Kaiti SC', 'STSong', 'Songti SC',
            'Source Han Serif SC', 'serif',
        ],
        body_font='Noto Serif SC',
        body_fallbacks=[
            'STSong', 'Songti SC', 'Source Han Serif SC',
            'serif',
        ],
        hero=84,
        section=58,
        page_title=34,
        page_sub=13,
        card_title=18,
        body=14,
        caption=11,
        page_number=10,
        hero_weight='semibold',
        section_weight='semibold',
        page_weight='semibold',
        card_weight='regular',
        body_weight='regular',
        hero_tracking=0.06,         # 中文古典字距宽
        section_tracking=0.04,
        page_tracking=0.03,
        body_tracking=0.02,
        hero_leading=1.3,
        body_leading=1.85,
        uppercase_en_sub=False,
    ),

    spacing=Spacing(
        gutter=0.1,
        stack_md=0.45,
        stack_lg=0.95,
        margin_x=1.0,
        margin_x_hero=1.4,
    ),

    elevation=Elevation(
        card_radius=0.04,
        card_stroke_width=0.3,
        card_stroke_color='#BFBFBF',
        card_fill='#F8F5EC',
        use_fake_shadow=False,
        style='outline',
    ),

    decoration=Decoration(
        cover_hero_align='left',
        cover_hero_case='as-is',
        cover_top_line=False,
        cover_bottom_line=False,
        page_title_align='left',
        page_accent_bar=False,
        page_en_sub_position='above',
        tag_style='none',
        stat_hero_size=180,
        stat_hero_weight='semibold',
        image_treatment='torn',     # 不规则毛边

        gradient_bg=None,
        accent_gradient=None,
        grid_overlay=False,
        dot_grid=False,
        glow_accent=False,
        corner_marks=False,
        dev_badge=False,
        mono_font=None,
        scanline=False,
    ),
    show_footer=True,
)


# ============================================================
# v3.2 ❹ Guofeng / 国风·故宫
#   朱砂红 + 藤黄 + 群青 + 篆刻印 + 万字纹边框
# ============================================================

GUOFENG = StylePack(
    name='guofeng',
    display_name='国风故宫（红黄青三色）',
    tagline='朱砂宫墙红 + 藤黄金瓦 + 群青 + 篆刻印章',

    canvas=Canvas(width=13.33, height=7.5),

    palette=Palette(
        bg='#F5E8C7',              # 米黄绢本
        bg_elevated='#FAF0D6',
        bg_subtle='#EDDFAE',
        text_primary='#1A1A1A',     # 墨色
        text_secondary='#5D3A1F',   # 漆木色
        text_tertiary='#8B6F47',
        text_muted='#B89968',
        accent='#E60012',           # 朱砂宫墙红
        accent_soft='#FFB61E',      # 藤黄（次强调）
        border='#B22222',
        divider='#D9C8A8',
    ),

    typography=Typography(
        display_font='Noto Serif SC',
        display_fallbacks=[
            'STSong', 'Songti SC', 'STKaiti',
            'Source Han Serif SC', 'serif',
        ],
        body_font='Noto Serif SC',
        body_fallbacks=[
            'STSong', 'Songti SC', 'serif',
        ],
        hero=88,
        section=60,
        page_title=36,
        page_sub=13,
        card_title=18,
        body=14,
        caption=11,
        page_number=10,
        hero_weight='bold',         # 故宫风骨感
        section_weight='bold',
        page_weight='semibold',
        card_weight='semibold',
        body_weight='regular',
        hero_tracking=0.05,
        section_tracking=0.04,
        page_tracking=0.03,
        hero_leading=1.25,
        body_leading=1.75,
        uppercase_en_sub=False,
    ),

    spacing=Spacing(
        margin_x=0.9,
        margin_x_hero=1.2,
        stack_md=0.4,
        stack_lg=0.85,
    ),

    elevation=Elevation(
        card_radius=0.0,            # 中式不要圆角
        card_stroke_width=0.5,
        card_stroke_color='#E60012', # 朱红描边
        card_fill='#FAF0D6',
        use_fake_shadow=False,
        style='outline',
    ),

    decoration=Decoration(
        cover_hero_align='left',
        cover_hero_case='as-is',
        cover_top_line=True,        # 金线
        cover_bottom_line=True,
        page_title_align='left',
        page_accent_bar=True,       # 朱红竖条
        page_en_sub_position='above',
        tag_style='square',
        stat_hero_size=200,
        stat_hero_weight='bold',
        image_treatment='full',

        gradient_bg=None,
        accent_gradient=('#E60012', '#FFB61E'),  # 朱→金渐变
        grid_overlay=False,
        dot_grid=False,
        glow_accent=False,
        corner_marks=True,          # 万字纹角标
        corner_size=0.32,
        corner_thickness=0.025,
        dev_badge=False,
        mono_font=None,
        scanline=False,
    ),
    show_footer=True,
)


# ============================================================
# v3.2 ❺ Cyberpunk Vivid / 赛博朋克绚彩
#   深紫黑 + 粉/青/黄三撞色 + Blade Runner 橙 + 扫描线
# ============================================================

CYBERPUNK_VIVID = StylePack(
    name='cyberpunk-vivid',
    display_name='赛博朋克绚彩（粉青黄撞色）',
    tagline='深紫黑 + 热粉 + 电青 + 赛博黄 + 银翼橙',

    canvas=Canvas(width=13.33, height=7.5),

    palette=Palette(
        bg='#0A0014',              # 深紫黑（带紫调）
        bg_elevated='#13002A',
        bg_subtle='#1A0033',
        text_primary='#FFFFFF',
        text_secondary='#E5C8FF',   # 浅紫
        text_tertiary='#9988CC',
        text_muted='#554477',
        accent='#FF2DAA',           # 热粉主霓虹
        accent_soft='#00E5FF',      # 电光青次强调
        border='#2A0055',
        divider='#1A0033',
    ),

    typography=Typography(
        display_font='Orbitron',
        display_fallbacks=[
            'Rajdhani', 'Inter', 'SF Pro Display',
            'PingFang SC', 'Microsoft YaHei', 'sans-serif',
        ],
        body_font='Rajdhani',
        body_fallbacks=[
            'Inter', 'SF Pro Text', 'PingFang SC', 'sans-serif',
        ],
        hero=152,                   # 赛博风超大字
        section=92,
        page_title=46,
        page_sub=14,
        card_title=22,
        body=15,
        caption=11,
        page_number=10,
        hero_weight='bold',
        section_weight='bold',
        page_weight='bold',
        card_weight='semibold',
        body_weight='regular',
        hero_tracking=0.02,         # 赛博字距偏宽
        section_tracking=0.015,
        page_tracking=0.01,
        hero_leading=0.95,
        body_leading=1.5,
        uppercase_en_sub=True,
    ),

    spacing=Spacing(
        margin_x=0.8,
        margin_x_hero=1.0,
        stack_md=0.35,
        stack_lg=0.7,
    ),

    elevation=Elevation(
        card_radius=0.04,
        card_stroke_width=1.0,
        card_stroke_color='#FF2DAA',  # 粉色霓虹边
        card_fill='#13002A',
        use_fake_shadow=False,
        style='outline',
    ),

    decoration=Decoration(
        cover_hero_align='left',
        cover_hero_case='upper',
        cover_top_line=False,
        cover_bottom_line=False,
        page_title_align='left',
        page_accent_bar=False,
        page_en_sub_position='above',
        tag_style='square',
        stat_hero_size=280,
        stat_hero_weight='bold',
        image_treatment='full',

        gradient_bg=('#0A0014', '#2A0055', 135),
        accent_gradient=('#FF2DAA', '#00E5FF'),  # 粉→青双色
        grid_overlay=True,
        grid_color='#1A0033',
        grid_spacing=0.35,
        grid_thickness=0.005,
        dot_grid=False,
        glow_accent=True,
        glow_strength=0.95,         # 强霓虹辉光
        corner_marks=True,
        corner_size=0.3,
        corner_thickness=0.022,
        dev_badge=True,
        dev_badge_template='SYS://NIGHT_CITY · {date}',
        mono_font='JetBrains Mono',
        scanline=True,              # 招牌扫描线
        scanline_color='#FF2DAA',
    ),
    show_footer=True,
)


# ============================================================
# v3.2 ❻ Van Gogh / 梵高油画
#   星夜深蓝 + 麦田金 + 笔触感（用色块叠加模拟）
# ============================================================

VAN_GOGH = StylePack(
    name='van-gogh',
    display_name='梵高油画（星夜麦田）',
    tagline='星夜深蓝 + 麦田金 + 鸢尾紫 + 油画笔触',

    canvas=Canvas(width=13.33, height=7.5),

    palette=Palette(
        bg='#0E2A47',              # 星夜深蓝
        bg_elevated='#1A3A5C',
        bg_subtle='#23456E',
        text_primary='#FFE082',     # 麦田金（标题）
        text_secondary='#F0D88B',
        text_tertiary='#C8B273',
        text_muted='#7A8FA8',
        accent='#FFC107',           # 向日葵金
        accent_soft='#7B5FA8',      # 鸢尾紫
        border='#3D5680',
        divider='#1A3A5C',
    ),

    typography=Typography(
        display_font='Cormorant Garamond',
        display_fallbacks=[
            'Playfair Display', 'Noto Serif SC', 'Songti SC',
            'STSong', 'serif',
        ],
        body_font='EB Garamond',
        body_fallbacks=[
            'Cormorant Garamond', 'Noto Serif SC', 'serif',
        ],
        hero=92,
        section=64,
        page_title=38,
        page_sub=14,
        card_title=20,
        body=15,
        caption=12,
        page_number=11,
        hero_weight='semibold',
        section_weight='semibold',
        page_weight='semibold',
        card_weight='semibold',
        body_weight='regular',
        hero_tracking=0.02,
        section_tracking=0.015,
        page_tracking=0.01,
        hero_leading=1.15,
        body_leading=1.7,
        uppercase_en_sub=False,
    ),

    spacing=Spacing(
        margin_x=0.9,
        margin_x_hero=1.2,
        stack_md=0.4,
        stack_lg=0.85,
    ),

    elevation=Elevation(
        card_radius=0.06,
        card_stroke_width=1.5,      # 油画粗笔触感
        card_stroke_color='#FFC107',
        card_fill='#1A3A5C',
        use_fake_shadow=True,
        shadow_color='#000000AA',
        shadow_offset_y=0.06,
        style='outline',
    ),

    decoration=Decoration(
        cover_hero_align='left',
        cover_hero_case='as-is',
        cover_top_line=False,
        cover_bottom_line=False,
        page_title_align='left',
        page_accent_bar=True,
        page_en_sub_position='above',
        tag_style='underline',
        stat_hero_size=220,
        stat_hero_weight='semibold',
        image_treatment='rounded',

        gradient_bg=('#0E2A47', '#1A3A5C', 135),
        accent_gradient=('#FFC107', '#FFE082'),  # 金光渐变
        grid_overlay=False,
        dot_grid=False,
        glow_accent=True,
        glow_strength=0.65,
        corner_marks=False,
        dev_badge=False,
        mono_font=None,
        scanline=False,
    ),
    show_footer=True,
)


# ============================================================
# v3.2 ❼ Da Vinci / 达芬奇手稿
#   羊皮纸 + 棕墨 + 手绘几何 + 镜像文字
# ============================================================

DA_VINCI = StylePack(
    name='da-vinci',
    display_name='达芬奇手稿（羊皮纸）',
    tagline='羊皮纸 + 棕墨 + 黄金分割 + 手绘几何',

    canvas=Canvas(width=13.33, height=7.5),

    palette=Palette(
        bg='#E8D9B5',              # 羊皮纸黄
        bg_elevated='#F0E2C0',
        bg_subtle='#DCC998',
        text_primary='#3D2817',     # 棕墨
        text_secondary='#5D3A1F',
        text_tertiary='#8B6F47',
        text_muted='#B89968',
        accent='#8B0000',           # 朱砂红 — 标注用
        accent_soft='#C8A876',
        border='#8B6F47',
        divider='#C8A876',
    ),

    typography=Typography(
        display_font='Cormorant Garamond',
        display_fallbacks=[
            'EB Garamond', 'Playfair Display',
            'Noto Serif SC', 'Songti SC', 'serif',
        ],
        body_font='EB Garamond',
        body_fallbacks=[
            'Cormorant Garamond', 'Noto Serif SC', 'serif',
        ],
        hero=80,
        section=56,
        page_title=34,
        page_sub=13,
        card_title=18,
        body=14,
        caption=11,
        page_number=10,
        hero_weight='semibold',
        section_weight='semibold',
        page_weight='semibold',
        card_weight='regular',
        body_weight='regular',
        hero_tracking=0.04,         # 文艺复兴字距宽松
        section_tracking=0.03,
        page_tracking=0.02,
        hero_leading=1.2,
        body_leading=1.75,
        uppercase_en_sub=False,
    ),

    spacing=Spacing(
        margin_x=1.0,
        margin_x_hero=1.4,
        stack_md=0.45,
        stack_lg=0.95,
    ),

    elevation=Elevation(
        card_radius=0.0,
        card_stroke_width=0.75,
        card_stroke_color='#8B6F47',
        card_fill='#F0E2C0',
        use_fake_shadow=False,
        style='outline',
    ),

    decoration=Decoration(
        cover_hero_align='left',
        cover_hero_case='as-is',
        cover_top_line=True,
        cover_bottom_line=True,
        page_title_align='left',
        page_accent_bar=False,
        page_en_sub_position='above',
        tag_style='underline',
        stat_hero_size=180,
        stat_hero_weight='semibold',
        image_treatment='full',

        gradient_bg=None,
        accent_gradient=None,
        grid_overlay=True,          # 黄金分割辅助网格
        grid_color='#C8A876',
        grid_spacing=0.5,
        grid_thickness=0.004,
        dot_grid=False,
        glow_accent=False,
        corner_marks=True,
        corner_size=0.28,
        corner_thickness=0.018,
        dev_badge=False,
        mono_font=None,
        scanline=False,
    ),
    show_footer=True,
)


# ============================================================
# v3.2 ❽ XHS Fashion / 小红书时尚款
#   莫兰迪粉 + 高级灰 + 细金线（区别于已有的奶油/胶片）
# ============================================================

XHS_FASHION = StylePack(
    name='xhs-fashion',
    display_name='小红书时尚（莫兰迪粉灰）',
    tagline='莫兰迪粉 + 高级灰 + 细金线 + 香奈儿感',

    canvas=Canvas(width=13.33, height=7.5),

    palette=Palette(
        bg='#F5EAE5',              # 莫兰迪藕粉
        bg_elevated='#FFFFFF',
        bg_subtle='#EDE0DA',
        text_primary='#2C2825',     # 暖黑
        text_secondary='#5C5650',
        text_tertiary='#928A82',
        text_muted='#C5BCB3',
        accent='#A0826D',           # 摩卡咖
        accent_soft='#D4B896',      # 香槟金
        border='#D9C7BD',
        divider='#EBDED5',
    ),

    typography=Typography(
        display_font='Playfair Display',
        display_fallbacks=[
            'Cormorant Garamond', 'Noto Serif SC',
            'Source Han Serif SC', 'serif',
        ],
        body_font='Noto Serif SC',
        body_fallbacks=[
            'Source Han Serif SC', 'PingFang SC', 'serif',
        ],
        hero=84,
        section=60,
        page_title=34,
        page_sub=13,
        card_title=18,
        body=14,
        caption=11,
        page_number=10,
        hero_weight='semibold',
        section_weight='semibold',
        page_weight='semibold',
        card_weight='semibold',
        body_weight='regular',
        hero_tracking=0.03,
        section_tracking=0.02,
        page_tracking=0.015,
        hero_leading=1.15,
        body_leading=1.7,
        uppercase_en_sub=True,      # FASHION 风英文小标全大写
    ),

    spacing=Spacing(
        margin_x=0.9,
        margin_x_hero=1.2,
        stack_md=0.4,
        stack_lg=0.85,
    ),

    elevation=Elevation(
        card_radius=0.05,           # 时尚风不要太圆
        card_stroke_width=0.5,
        card_stroke_color='#D4B896', # 细金线
        card_fill='#FFFFFF',
        use_fake_shadow=True,
        shadow_color='#2C28250D',
        shadow_offset_y=0.05,
        style='outline',
    ),

    decoration=Decoration(
        cover_hero_align='center',
        cover_hero_case='as-is',
        cover_top_line=True,
        cover_bottom_line=True,
        page_title_align='center',
        page_accent_bar=False,
        page_en_sub_position='above',
        tag_style='underline',
        stat_hero_size=180,
        stat_hero_weight='semibold',
        image_treatment='rounded',

        gradient_bg=None,
        accent_gradient=None,
        grid_overlay=False,
        dot_grid=False,
        glow_accent=False,
        corner_marks=False,
        dev_badge=False,
        mono_font=None,
        scanline=False,
    ),
    show_footer=True,
)


# ============================================================
# v3.2 ❾ Morandi / 莫兰迪高级灰
#   全色域低饱和 — 静物画大师的色彩谱
# ============================================================

MORANDI = StylePack(
    name='morandi',
    display_name='莫兰迪高级灰（静物画）',
    tagline='低饱和粉绿米 + 哑光高级灰 + 油画静物',

    canvas=Canvas(width=13.33, height=7.5),

    palette=Palette(
        bg='#E8E3D9',              # 莫兰迪米灰
        bg_elevated='#F0EBE0',
        bg_subtle='#D9D2C5',
        text_primary='#3A3633',     # 灰墨
        text_secondary='#6B6660',
        text_tertiary='#928A82',
        text_muted='#B5AEA5',
        accent='#9AAB9C',           # 莫兰迪绿
        accent_soft='#C9B8B0',      # 莫兰迪粉
        border='#C5BCB3',
        divider='#D9D2C5',
    ),

    typography=Typography(
        display_font='Playfair Display',
        display_fallbacks=[
            'Cormorant Garamond', 'EB Garamond',
            'Noto Serif SC', 'serif',
        ],
        body_font='Noto Serif SC',
        body_fallbacks=[
            'Source Han Serif SC', 'PingFang SC', 'serif',
        ],
        hero=78,
        section=56,
        page_title=32,
        page_sub=13,
        card_title=18,
        body=14,
        caption=11,
        page_number=10,
        hero_weight='regular',
        section_weight='regular',
        page_weight='regular',
        card_weight='regular',
        body_weight='regular',
        hero_tracking=0.03,
        section_tracking=0.02,
        page_tracking=0.015,
        hero_leading=1.25,
        body_leading=1.75,
        uppercase_en_sub=False,
    ),

    spacing=Spacing(
        margin_x=1.1,
        margin_x_hero=1.5,
        stack_md=0.5,
        stack_lg=1.0,
    ),

    elevation=Elevation(
        card_radius=0.08,
        card_stroke_width=0.4,
        card_stroke_color='#B5AEA5',
        card_fill='#F0EBE0',
        use_fake_shadow=False,
        style='soft',
    ),

    decoration=Decoration(
        cover_hero_align='left',
        cover_hero_case='as-is',
        cover_top_line=False,
        cover_bottom_line=False,
        page_title_align='left',
        page_accent_bar=False,
        page_en_sub_position='above',
        tag_style='pill',
        stat_hero_size=160,
        stat_hero_weight='regular',
        image_treatment='rounded',

        gradient_bg=None,
        accent_gradient=None,
        grid_overlay=False,
        dot_grid=False,
        glow_accent=False,
        corner_marks=False,
        dev_badge=False,
        mono_font=None,
        scanline=False,
    ),
    show_footer=True,
)


# ============================================================
# v3.2 ❿ Memphis / 孟菲斯 80s 撞色几何
#   黑白条纹 + 粉黄绿三撞色 + 圆/三角/波浪
# ============================================================

MEMPHIS = StylePack(
    name='memphis',
    display_name='孟菲斯 80s（撞色几何）',
    tagline='粉黄绿撞色 + 黑白条纹 + 不规则几何',

    canvas=Canvas(width=13.33, height=7.5),

    palette=Palette(
        bg='#FFF8E7',              # 浅米黄底
        bg_elevated='#FFFFFF',
        bg_subtle='#FFE8D6',
        text_primary='#1A1A1A',
        text_secondary='#4A4A4A',
        text_tertiary='#8A8A8A',
        text_muted='#C0C0C0',
        accent='#FF3399',           # 孟菲斯粉
        accent_soft='#FFD93D',      # 孟菲斯黄（次）
        border='#1A1A1A',
        divider='#E0E0E0',
    ),

    typography=Typography(
        display_font='Rubik Mono One',  # v3.3 反 AI Slop R1
        display_fallbacks=[
            'Helvetica Neue', 'PingFang SC', 'sans-serif',
        ],
        body_font='Space Mono',  # v3.3 反 AI Slop R1: Inter→Space Mono
        body_fallbacks=[
            'Helvetica Neue', 'PingFang SC', 'sans-serif',
        ],
        hero=120,
        section=72,
        page_title=42,
        page_sub=14,
        card_title=22,
        body=15,
        caption=11,
        page_number=10,
        hero_weight='bold',
        section_weight='bold',
        page_weight='bold',
        card_weight='bold',
        body_weight='regular',
        hero_tracking=-0.02,
        section_tracking=-0.015,
        page_tracking=0.0,
        hero_leading=0.95,
        body_leading=1.5,
        uppercase_en_sub=True,
    ),

    spacing=Spacing(
        margin_x=0.85,
        margin_x_hero=1.1,
        stack_md=0.4,
        stack_lg=0.8,
    ),

    elevation=Elevation(
        card_radius=0.15,           # 圆角不规则
        card_stroke_width=2.0,      # 孟菲斯粗描边
        card_stroke_color='#1A1A1A',
        card_fill='#FFFFFF',
        use_fake_shadow=True,
        shadow_color='#1A1A1A',     # 偏移黑投影是孟菲斯灵魂
        shadow_offset_y=0.08,
        style='outline',
    ),

    decoration=Decoration(
        cover_hero_align='left',
        cover_hero_case='upper',
        cover_top_line=False,
        cover_bottom_line=False,
        page_title_align='left',
        page_accent_bar=False,
        page_en_sub_position='above',
        tag_style='square',
        stat_hero_size=240,
        stat_hero_weight='bold',
        image_treatment='full',

        gradient_bg=None,
        accent_gradient=('#FF3399', '#FFD93D'),  # 粉→黄
        grid_overlay=False,
        dot_grid=True,
        dot_color='#1A1A1A',
        dot_spacing=0.5,
        dot_size=0.05,
        glow_accent=False,
        corner_marks=False,
        dev_badge=False,
        mono_font='JetBrains Mono',
        scanline=False,
    ),
    show_footer=True,
)


# ============================================================
# v3.2 ⓫ Bauhaus / 包豪斯
#   红黄蓝三原色 + 几何块面 + 等宽数字
# ============================================================

BAUHAUS = StylePack(
    name='bauhaus',
    display_name='包豪斯（红黄蓝三原色）',
    tagline='红黄蓝三原色 + 几何块面 + 功能主义',

    canvas=Canvas(width=13.33, height=7.5),

    palette=Palette(
        bg='#F5F1E8',              # 包豪斯象牙底
        bg_elevated='#FFFFFF',
        bg_subtle='#E8E0D0',
        text_primary='#1A1A1A',
        text_secondary='#3A3A3A',
        text_tertiary='#6A6A6A',
        text_muted='#A0A0A0',
        accent='#D32F2F',           # 包豪斯红
        accent_soft='#1565C0',      # 包豪斯蓝（次）
        border='#1A1A1A',
        divider='#D0D0D0',
    ),

    typography=Typography(
        display_font='Space Grotesk',  # v3.3 反 AI Slop R1       # 模拟 Futura/Universal
        display_fallbacks=[
            'Futura', 'Helvetica Neue', 'PingFang SC', 'sans-serif',
        ],
        body_font='Space Grotesk',  # v3.3 反 AI Slop R1: Inter→Space Grotesk
        body_fallbacks=[
            'Helvetica Neue', 'PingFang SC', 'sans-serif',
        ],
        hero=128,
        section=80,
        page_title=44,
        page_sub=13,
        card_title=20,
        body=14,
        caption=11,
        page_number=10,
        hero_weight='bold',
        section_weight='bold',
        page_weight='semibold',
        card_weight='semibold',
        body_weight='regular',
        hero_tracking=-0.02,
        section_tracking=-0.015,
        page_tracking=0.0,
        hero_leading=0.95,
        body_leading=1.5,
        uppercase_en_sub=True,
    ),

    spacing=Spacing(
        margin_x=0.8,
        margin_x_hero=1.0,
        stack_md=0.35,
        stack_lg=0.7,
    ),

    elevation=Elevation(
        card_radius=0.0,            # 包豪斯不要圆角
        card_stroke_width=1.5,
        card_stroke_color='#1A1A1A',
        card_fill='#FFFFFF',
        use_fake_shadow=False,
        style='outline',
    ),

    decoration=Decoration(
        cover_hero_align='left',
        cover_hero_case='as-is',
        cover_top_line=False,
        cover_bottom_line=False,
        page_title_align='left',
        page_accent_bar=True,       # 红色竖条
        page_en_sub_position='above',
        tag_style='square',
        stat_hero_size=240,
        stat_hero_weight='bold',
        image_treatment='full',

        gradient_bg=None,
        accent_gradient=None,
        grid_overlay=True,
        grid_color='#E0DDD0',
        grid_spacing=0.5,
        grid_thickness=0.005,
        dot_grid=False,
        glow_accent=False,
        corner_marks=False,
        dev_badge=True,
        dev_badge_template='№ {n} / {date}',
        mono_font='JetBrains Mono',
        scanline=False,
    ),
    show_footer=True,
)


# ============================================================
# v3.2 ⓬ Wes Anderson / 韦斯安德森
#   对称粉绿米 + 衬线字 + 复古感
# ============================================================

WES_ANDERSON = StylePack(
    name='wes-anderson',
    display_name='韦斯安德森（对称粉绿米）',
    tagline='糖果粉 + 薄荷绿 + 米色 + 极致对称',

    canvas=Canvas(width=13.33, height=7.5),

    palette=Palette(
        bg='#F4D5C2',              # 糖果粉米
        bg_elevated='#FFEAD9',
        bg_subtle='#EBC4AD',
        text_primary='#2D2D1A',     # 暖黑
        text_secondary='#5C5440',
        text_tertiary='#8B8268',
        text_muted='#B5AC8A',
        accent='#3D6E5B',           # 复古薄荷
        accent_soft='#E8B4A0',      # 蜜桃粉
        border='#C8A98B',
        divider='#E0C4A8',
    ),

    typography=Typography(
        display_font='Playfair Display',
        display_fallbacks=[
            'Cormorant Garamond', 'Futura',
            'Noto Serif SC', 'serif',
        ],
        body_font='EB Garamond',
        body_fallbacks=[
            'Cormorant Garamond', 'Noto Serif SC', 'serif',
        ],
        hero=80,
        section=58,
        page_title=34,
        page_sub=13,
        card_title=18,
        body=14,
        caption=11,
        page_number=10,
        hero_weight='semibold',
        section_weight='semibold',
        page_weight='semibold',
        card_weight='semibold',
        body_weight='regular',
        hero_tracking=0.04,
        section_tracking=0.03,
        page_tracking=0.02,
        hero_leading=1.2,
        body_leading=1.7,
        uppercase_en_sub=True,
    ),

    spacing=Spacing(
        margin_x=1.0,
        margin_x_hero=1.4,
        stack_md=0.45,
        stack_lg=0.9,
    ),

    elevation=Elevation(
        card_radius=0.04,
        card_stroke_width=0.75,
        card_stroke_color='#3D6E5B',
        card_fill='#FFEAD9',
        use_fake_shadow=False,
        style='outline',
    ),

    decoration=Decoration(
        cover_hero_align='center',  # 对称是 Wes 灵魂
        cover_hero_case='as-is',
        cover_top_line=True,
        cover_bottom_line=True,
        page_title_align='center',
        page_accent_bar=False,
        page_en_sub_position='above',
        tag_style='underline',
        stat_hero_size=180,
        stat_hero_weight='semibold',
        image_treatment='rounded',

        gradient_bg=None,
        accent_gradient=None,
        grid_overlay=False,
        dot_grid=False,
        glow_accent=False,
        corner_marks=True,
        corner_size=0.3,
        corner_thickness=0.015,
        dev_badge=False,
        mono_font=None,
        scanline=False,
    ),
    show_footer=True,
)


# ============================================================
# 七、Legacy packs（向后兼容老的 v2.x）
# ============================================================

JOBS_DARK = StylePack(
    name='jobs-dark',
    display_name='乔布斯极简暗蓝（v1.x 默认）',
    tagline='深蓝暗底 + 白灰克制',

    palette=Palette(
        bg='#060D1A',
        bg_elevated='#0D182A',
        bg_subtle='#14243D',
        text_primary='#FFFFFF',
        text_secondary='#CCCCCC',
        text_tertiary='#888888',
        text_muted='#444455',
        accent='#FFFFFF',
        border='#333344',
        divider='#333344',
    ),
    typography=Typography(
        hero=64, section=48, page_title=28, page_sub=10,
        card_title=14, body=11, caption=10, page_number=9,
        uppercase_en_sub=True,
    ),
    elevation=Elevation(
        card_stroke_width=0.5,
        card_stroke_color='#333344',
        card_fill='#0D182A',
    ),
    decoration=Decoration(),
    show_footer=True,
)


XIAOHONGSHU_BRAND = StylePack(
    name='xiaohongshu',
    display_name='小红书品牌风（v2.x 默认）',
    tagline='小红书红 + 暖奶油',

    palette=Palette(
        bg='#FFF8F3',
        bg_elevated='#FFFFFF',
        bg_subtle='#F5E6E6',
        text_primary='#1A1A1A',
        text_secondary='#4A4A4A',
        text_tertiary='#8A8A8A',
        text_muted='#C8C8C8',
        accent='#FF2442',
        accent_soft='#FFE5EC',
        border='#F5E6E6',
        divider='#F2E6E6',
    ),
    typography=Typography(
        hero=60, section=48, page_title=30, page_sub=12,
        card_title=16, body=12, caption=10, page_number=9,
        uppercase_en_sub=False,
    ),
    elevation=Elevation(
        card_stroke_width=0.75,
        card_stroke_color='#F5E6E6',
        card_fill='#FFFFFF',
    ),
    decoration=Decoration(
        cover_top_line=True,
        page_accent_bar=True,
        tag_style='pill',
    ),
    show_footer=True,
)


XIAOHONGSHU_PORTRAIT = StylePack(
    name='xiaohongshu-portrait',
    display_name='小红书品牌风 · 竖版 9:16',
    tagline='直接发帖用的竖版',

    canvas=Canvas(width=7.5, height=13.33),
    palette=XIAOHONGSHU_BRAND.palette,
    typography=Typography(
        hero=72, section=56, page_title=36, page_sub=13,
        card_title=18, body=14, caption=11, page_number=10,
        uppercase_en_sub=False,
    ),
    elevation=XIAOHONGSHU_BRAND.elevation,
    decoration=XIAOHONGSHU_BRAND.decoration,
    show_footer=True,
)


# ============================================================
# 六、注册表
# ============================================================

REGISTRY = {
    # v3.0 审美 pack
    'apple-keynote': APPLE_KEYNOTE,
    'apple-dark': APPLE_KEYNOTE,
    'apple': APPLE_KEYNOTE,
    '苹果': APPLE_KEYNOTE,
    '苹果发布会': APPLE_KEYNOTE,
    '发布会': APPLE_KEYNOTE,
    '乔布斯科技简约': APPLE_KEYNOTE,
    '乔布斯简约': APPLE_KEYNOTE,
    'jobs-modern': APPLE_KEYNOTE,

    'apple-light': APPLE_LIGHT,
    'apple-white': APPLE_LIGHT,
    '苹果白': APPLE_LIGHT,
    '苹果官网': APPLE_LIGHT,

    'xiaohongshu-creator': XHS_CREATOR,
    'xhs-creator': XHS_CREATOR,
    '博主风': XHS_CREATOR,
    '生活博主': XHS_CREATOR,
    '博主': XHS_CREATOR,
    '奶油博主': XHS_CREATOR,

    'xiaohongshu-vintage': XHS_VINTAGE,
    'xhs-vintage': XHS_VINTAGE,
    '复古': XHS_VINTAGE,
    '胶片': XHS_VINTAGE,
    '复古胶片': XHS_VINTAGE,

    # v3.1 科技风
    'tech-neon': TECH_NEON,
    'tech': TECH_NEON,
    'neon': TECH_NEON,
    '科技': TECH_NEON,
    '科技风': TECH_NEON,
    '霓虹': TECH_NEON,
    '赛博': TECH_NEON,

    'tech-minimal': TECH_MINIMAL,
    'minimal-tech': TECH_MINIMAL,
    'vercel': TECH_MINIMAL,
    'linear': TECH_MINIMAL,
    '极简科技': TECH_MINIMAL,
    '暗黑极简': TECH_MINIMAL,
    'saas': TECH_MINIMAL,

    # ============ v3.2 生产级 12 套 ============

    # ❶ Liquid Glass
    'liquid-glass': LIQUID_GLASS,
    'glass': LIQUID_GLASS,
    'apple-glass': LIQUID_GLASS,
    'macos-26': LIQUID_GLASS,
    'macos26': LIQUID_GLASS,
    'tahoe': LIQUID_GLASS,
    'ios26': LIQUID_GLASS,
    '玻璃': LIQUID_GLASS,
    '液态玻璃': LIQUID_GLASS,
    '苹果玻璃': LIQUID_GLASS,
    '苹果26': LIQUID_GLASS,
    '玻璃风': LIQUID_GLASS,
    'macos-tahoe': LIQUID_GLASS,

    # ❷ MUJI / 原研哉
    'muji': MUJI,
    'kenya-hara': MUJI,
    'hara': MUJI,
    '原研哉': MUJI,
    '原研哉极简': MUJI,
    '无印良品': MUJI,
    '无印': MUJI,
    'mu-ji': MUJI,

    # ❸ Ink Wash / 水墨
    'ink-wash': INK_WASH,
    'ink': INK_WASH,
    'chinese-ink': INK_WASH,
    '水墨': INK_WASH,
    '中国水墨': INK_WASH,
    '墨分五色': INK_WASH,
    '宣纸': INK_WASH,

    # ❹ Guofeng / 国风
    'guofeng': GUOFENG,
    'gugong': GUOFENG,
    'forbidden-city': GUOFENG,
    'chinese-imperial': GUOFENG,
    '国风': GUOFENG,
    '故宫': GUOFENG,
    '故宫文创': GUOFENG,
    '中国风': GUOFENG,

    # ❺ Cyberpunk Vivid
    'cyberpunk-vivid': CYBERPUNK_VIVID,
    'cyberpunk': CYBERPUNK_VIVID,
    'cyber': CYBERPUNK_VIVID,
    'cp2077': CYBERPUNK_VIVID,
    'blade-runner': CYBERPUNK_VIVID,
    '赛博朋克': CYBERPUNK_VIVID,
    '赛博朋克绚彩': CYBERPUNK_VIVID,
    '银翼杀手': CYBERPUNK_VIVID,
    '霓虹绚彩': CYBERPUNK_VIVID,

    # ❻ Van Gogh
    'van-gogh': VAN_GOGH,
    'vangogh': VAN_GOGH,
    'starry-night': VAN_GOGH,
    '梵高': VAN_GOGH,
    '星夜': VAN_GOGH,
    '油画': VAN_GOGH,
    '梵高油画': VAN_GOGH,

    # ❼ Da Vinci
    'da-vinci': DA_VINCI,
    'davinci': DA_VINCI,
    'leonardo': DA_VINCI,
    '达芬奇': DA_VINCI,
    '达芬奇手稿': DA_VINCI,
    '羊皮纸': DA_VINCI,
    '手稿': DA_VINCI,
    '文艺复兴': DA_VINCI,

    # ❽ XHS Fashion
    'xhs-fashion': XHS_FASHION,
    'xiaohongshu-fashion': XHS_FASHION,
    'fashion': XHS_FASHION,
    '小红书时尚': XHS_FASHION,
    '时尚': XHS_FASHION,
    '香奈儿': XHS_FASHION,
    'chanel': XHS_FASHION,
    '奢侈品': XHS_FASHION,

    # ❾ Morandi
    'morandi': MORANDI,
    'morandi-grey': MORANDI,
    '莫兰迪': MORANDI,
    '高级灰': MORANDI,
    '莫兰迪色': MORANDI,
    '静物': MORANDI,

    # ❿ Memphis
    'memphis': MEMPHIS,
    'memphis-design': MEMPHIS,
    '孟菲斯': MEMPHIS,
    '80s': MEMPHIS,
    '撞色': MEMPHIS,

    # ⓫ Bauhaus
    'bauhaus': BAUHAUS,
    'bauhaus-100': BAUHAUS,
    '包豪斯': BAUHAUS,
    '三原色': BAUHAUS,
    '功能主义': BAUHAUS,

    # ⓬ Wes Anderson
    'wes-anderson': WES_ANDERSON,
    'wes': WES_ANDERSON,
    'anderson': WES_ANDERSON,
    '韦斯安德森': WES_ANDERSON,
    '布达佩斯大饭店': WES_ANDERSON,
    '对称美学': WES_ANDERSON,

    # Legacy packs
    'jobs-dark': JOBS_DARK,
    'jobs': JOBS_DARK,
    '乔布斯': JOBS_DARK,
    '乔布斯暗': JOBS_DARK,

    'xiaohongshu': XIAOHONGSHU_BRAND,
    'xhs': XIAOHONGSHU_BRAND,
    '小红书': XIAOHONGSHU_BRAND,

    'xiaohongshu-portrait': XIAOHONGSHU_PORTRAIT,
    'xhs-portrait': XIAOHONGSHU_PORTRAIT,
    '小红书竖版': XIAOHONGSHU_PORTRAIT,
}


def get_pack(name: str) -> StylePack:
    if not name:
        return APPLE_KEYNOTE
    key = name.strip().lower()
    if key in REGISTRY:
        return REGISTRY[key]
    if name in REGISTRY:
        return REGISTRY[name]
    return APPLE_KEYNOTE


def list_packs():
    """主要 pack 名，供 --help 展示。"""
    return (
        # v3.0 基础
        'apple-keynote',
        'apple-light',
        'xiaohongshu-creator',
        'xiaohongshu-vintage',
        # v3.1 科技
        'tech-neon',
        'tech-minimal',
        # v3.2 生产级
        'liquid-glass',
        'muji',
        'ink-wash',
        'guofeng',
        'cyberpunk-vivid',
        'van-gogh',
        'da-vinci',
        'xhs-fashion',
        'morandi',
        'memphis',
        'bauhaus',
        'wes-anderson',
        # Legacy
        'jobs-dark',
        'xiaohongshu',
        'xiaohongshu-portrait',
    )


def all_packs():
    """v3.2: 返回所有 21 套 pack 实例 — 用于批量预览生成。"""
    return [
        APPLE_KEYNOTE, APPLE_LIGHT, XHS_CREATOR, XHS_VINTAGE,
        TECH_NEON, TECH_MINIMAL,
        LIQUID_GLASS, MUJI, INK_WASH, GUOFENG, CYBERPUNK_VIVID,
        VAN_GOGH, DA_VINCI, XHS_FASHION, MORANDI, MEMPHIS,
        BAUHAUS, WES_ANDERSON,
        JOBS_DARK, XIAOHONGSHU_BRAND, XIAOHONGSHU_PORTRAIT,
    ]
