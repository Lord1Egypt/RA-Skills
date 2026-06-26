"""火一五流程图 — 10 种 2026 现代风格主题。

v1.3 改造重点（经过行业设计调研后的设计取向）：
- **soft light 默认范式**：浅色填充 + 彩色描边 + 深色文字（Linear/Vercel/Stripe/Radix 风）
  取代旧版的"深色大色块 + 白字"老旧扁平风
- **双层 drop-shadow**：`drop-shadow(0 1px 2px) drop-shadow(0 4px 12px)`
  复刻 Linear / Vercel 的"柔和浮起"质感
- **判定菱形强调色**：decision 节点独立 classDef，用 accent 色突出
- **排版**：nodeSpacing=60、rankSpacing=80、padding=20、fontSize=15，Inter 字体栈
- **曲线按类型**：flowchart/state basis、sequence/c4 step、swimlane linear
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Style:
    key: str
    name: str
    # Mermaid theme：default / neutral / forest / dark / base
    mermaid_theme: str = "base"
    # ---- 核心色板（软色范式）----
    primary_color: str = "#EEF2FF"          # 节点主填充（浅色系）
    primary_text_color: str = "#1E293B"     # 节点文字（深色，在浅填充上保证对比）
    primary_border_color: str = "#6366F1"   # 节点描边（彩色，成为视觉焦点）
    secondary_color: str = "#F1F5F9"        # 次级节点 / 容器填充
    tertiary_color: str = "#E2E8F0"         # 三级节点 / 容器描边
    line_color: str = "#64748B"             # 连线
    background: str = "#FFFFFF"             # 画布背景
    accent_color: str = "#F59E0B"           # 判断菱形 / 强调色
    accent_text_color: str = "#FFFFFF"      # 判断菱形文字
    accent_border_color: str = "#D97706"    # 判断菱形描边
    note_color: str = "#FEF3C7"
    note_border: str = "#FBBF24"
    # ---- 字体（Inter 优先）----
    font_family: str = (
        '"Inter", -apple-system, BlinkMacSystemFont, "PingFang SC", '
        '"HarmonyOS Sans SC", "Microsoft YaHei", "Noto Sans CJK SC", '
        'ui-sans-serif, system-ui, sans-serif'
    )
    font_size: str = "15px"
    font_weight_node: int = 500
    # ---- 现代化视觉参数 ----
    gradient_start: str = ""                # drawio 渐变起色（空 = 无渐变）
    gradient_end: str = ""                  # drawio 渐变终色
    corner_radius: int = 10                 # 圆角半径
    stroke_width: float = 1.5               # 描边宽度
    # 双层阴影：紧邻层 + 扩散层（Linear/Vercel 招牌质感）
    shadow_close_blur: int = 2
    shadow_close_offset: int = 1
    shadow_close_opacity: float = 0.06
    shadow_far_blur: int = 12
    shadow_far_offset: int = 4
    shadow_far_opacity: float = 0.08
    shadow_color: str = "#0F172A"
    # ---- 布局留白 ----
    node_spacing: int = 60
    rank_spacing: int = 80
    padding: int = 20
    # ---- 备用 palette ----
    palette: List[str] = field(default_factory=list)
    # v1.3.2：category 渲染模式
    # "soft"（默认）→ tertiary_color 填充 + palette 色描边/文字（适合 Linear/Vercel 风）
    # "bold"        → palette 色填充 + 固定深色文字/描边（适合 Neubrutalism/Ink 风）
    category_mode: str = "soft"


# ============================================================
# 现代商务 modern —— Radix Indigo/Slate 风，商务文档/技术默认
# 浅 indigo 填充 + 紫色描边 + 深灰字 + 琥珀判断色
# ============================================================
MODERN = Style(
    key="modern",
    name="现代商务",
    mermaid_theme="base",
    primary_color="#EEF2FF",
    primary_text_color="#1E293B",
    primary_border_color="#6366F1",
    secondary_color="#F8FAFC",
    tertiary_color="#E2E8F0",
    line_color="#64748B",
    background="#FFFFFF",
    accent_color="#F59E0B",
    accent_text_color="#78350F",
    accent_border_color="#D97706",
    note_color="#FEF3C7",
    note_border="#FBBF24",
    gradient_start="#E0E7FF",
    gradient_end="#C7D2FE",
    palette=["#6366F1", "#0EA5E9", "#10B981", "#F59E0B", "#EF4444"],
)

# ============================================================
# 经典稳重 classic —— 咨询报告风，浅蓝卡 + 琥珀判断
# ============================================================
CLASSIC = Style(
    key="classic",
    name="经典稳重",
    mermaid_theme="base",
    primary_color="#DBEAFE",
    primary_text_color="#1E3A8A",
    primary_border_color="#2563EB",
    secondary_color="#F0F9FF",
    tertiary_color="#BFDBFE",
    line_color="#1E40AF",
    background="#FDFCFA",
    accent_color="#D97706",
    accent_text_color="#78350F",
    accent_border_color="#B45309",
    note_color="#FEF3C7",
    note_border="#FBBF24",
    gradient_start="#BFDBFE",
    gradient_end="#93C5FD",
    palette=["#1E40AF", "#6366F1", "#D97706", "#DC2626", "#059669"],
)

# ============================================================
# 暗色霓虹 dark —— Linear Dark / Vercel 深色模式
# 深色画布 + 浅节点 + 紫色描边 + 青色强调
# ============================================================
DARK = Style(
    key="dark",
    name="暗色霓虹",
    mermaid_theme="dark",
    primary_color="#1E293B",
    primary_text_color="#F1F5F9",
    primary_border_color="#8B5CF6",
    secondary_color="#334155",
    tertiary_color="#475569",
    line_color="#94A3B8",
    background="#0F172A",
    accent_color="#22D3EE",
    accent_text_color="#0F172A",
    accent_border_color="#06B6D4",
    note_color="#1E293B",
    note_border="#8B5CF6",
    gradient_start="#334155",
    gradient_end="#0F172A",
    shadow_color="#8B5CF6",
    shadow_far_opacity=0.25,
    shadow_far_blur=18,
    palette=["#8B5CF6", "#22D3EE", "#F472B6", "#34D399", "#FBBF24"],
)

# ============================================================
# 小红书暖奶油 xiaohongshu —— 种草封面 / 女性向
# 奶油背景 + 浅粉节点 + 玫红描边
# ============================================================
XIAOHONGSHU = Style(
    key="xiaohongshu",
    name="小红书暖奶油",
    mermaid_theme="base",
    primary_color="#FFE4E6",
    primary_text_color="#881337",
    primary_border_color="#E11D48",
    secondary_color="#FFF1F2",
    tertiary_color="#FECDD3",
    line_color="#F43F5E",
    background="#FFF8F3",
    accent_color="#F59E0B",
    accent_text_color="#78350F",
    accent_border_color="#D97706",
    note_color="#FEF3C7",
    note_border="#FDE68A",
    gradient_start="#FECDD3",
    gradient_end="#FDA4AF",
    palette=["#E11D48", "#F59E0B", "#F472B6", "#A855F7", "#14B8A6"],
)

# ============================================================
# 海洋蓝 ocean —— SaaS 官网 / 技术架构
# ============================================================
OCEAN = Style(
    key="ocean",
    name="海洋蓝",
    mermaid_theme="base",
    primary_color="#E0F2FE",
    primary_text_color="#075985",
    primary_border_color="#0284C7",
    secondary_color="#F0F9FF",
    tertiary_color="#BAE6FD",
    line_color="#0369A1",
    background="#F0F9FF",
    accent_color="#F97316",
    accent_text_color="#7C2D12",
    accent_border_color="#EA580C",
    note_color="#E0F2FE",
    note_border="#7DD3FC",
    gradient_start="#BAE6FD",
    gradient_end="#7DD3FC",
    palette=["#0284C7", "#06B6D4", "#10B981", "#F97316", "#F43F5E"],
)

# ============================================================
# 森林绿 forest —— 环保 / 健康 / ESG
# ============================================================
FOREST = Style(
    key="forest",
    name="森林绿",
    mermaid_theme="base",
    primary_color="#D1FAE5",
    primary_text_color="#064E3B",
    primary_border_color="#047857",
    secondary_color="#F0FDF4",
    tertiary_color="#A7F3D0",
    line_color="#059669",
    background="#F0FDF4",
    accent_color="#EA580C",
    accent_text_color="#7C2D12",
    accent_border_color="#C2410C",
    note_color="#ECFCCB",
    note_border="#BEF264",
    gradient_start="#A7F3D0",
    gradient_end="#6EE7B7",
    palette=["#047857", "#65A30D", "#CA8A04", "#EA580C", "#0891B2"],
)

# ============================================================
# 夕阳暖橙 sunset —— 运营活动 / 温暖叙事
# ============================================================
SUNSET = Style(
    key="sunset",
    name="夕阳暖橙",
    mermaid_theme="base",
    primary_color="#FFEDD5",
    primary_text_color="#7C2D12",
    primary_border_color="#EA580C",
    secondary_color="#FFF7ED",
    tertiary_color="#FED7AA",
    line_color="#F97316",
    background="#FFF7ED",
    accent_color="#0891B2",
    accent_text_color="#FFFFFF",
    accent_border_color="#0E7490",
    note_color="#FFEDD5",
    note_border="#FDBA74",
    gradient_start="#FED7AA",
    gradient_end="#FDBA74",
    palette=["#EA580C", "#F59E0B", "#D946EF", "#0891B2", "#059669"],
)

# ============================================================
# 极简素雅 minimal —— Notion / 学术出版物
# 纯白 + 细灰描边 + 深字 + 单一蓝色强调
# ============================================================
MINIMAL = Style(
    key="minimal",
    name="极简素雅",
    mermaid_theme="neutral",
    primary_color="#F9FAFB",
    primary_text_color="#111827",
    primary_border_color="#374151",
    secondary_color="#FFFFFF",
    tertiary_color="#E5E7EB",
    line_color="#6B7280",
    background="#FFFFFF",
    accent_color="#2563EB",
    accent_text_color="#FFFFFF",
    accent_border_color="#1D4ED8",
    note_color="#F3F4F6",
    note_border="#D1D5DB",
    gradient_start="",   # 极简风不使用渐变
    gradient_end="",
    stroke_width=1.2,
    shadow_close_opacity=0.04,
    shadow_far_opacity=0.05,
    shadow_far_blur=8,
    palette=["#111827", "#2563EB", "#B45309", "#047857", "#7C3AED"],
)

# ============================================================
# 马卡龙粉嫩 pastel —— 儿童教育 / 女性向
# ============================================================
PASTEL = Style(
    key="pastel",
    name="马卡龙粉嫩",
    mermaid_theme="base",
    primary_color="#EDE9FE",
    primary_text_color="#4C1D95",
    primary_border_color="#A78BFA",
    secondary_color="#FCE7F3",
    tertiary_color="#FBCFE8",
    line_color="#C084FC",
    background="#FEFAFF",
    accent_color="#F472B6",
    accent_text_color="#831843",
    accent_border_color="#DB2777",
    note_color="#FFF1F2",
    note_border="#FDA4AF",
    gradient_start="#DDD6FE",
    gradient_end="#C4B5FD",
    shadow_color="#A78BFA",
    shadow_far_opacity=0.14,
    palette=["#A78BFA", "#F472B6", "#60A5FA", "#34D399", "#FBBF24"],
)

# ============================================================
# 极客 github —— 开源 README / 文档
# GitHub 品牌蓝 + 细描边 + 白背景
# ============================================================
GITHUB = Style(
    key="github",
    name="极客 GitHub",
    mermaid_theme="base",
    primary_color="#DDF4FF",
    primary_text_color="#0969DA",
    primary_border_color="#0969DA",
    secondary_color="#F6F8FA",
    tertiary_color="#D0D7DE",
    line_color="#57606A",
    background="#FFFFFF",
    accent_color="#2DA44E",
    accent_text_color="#FFFFFF",
    accent_border_color="#1A7F37",
    note_color="#FFF8C5",
    note_border="#D4A72C",
    gradient_start="#B6E3FF",
    gradient_end="#54AEFF",
    palette=["#0969DA", "#2DA44E", "#CF222E", "#9A6700", "#8250DF"],
)


# ============================================================
# 企业蓝金 corporate —— 正式 / 金融 / 政府 / 年报
# 深海蓝节点 + 暖金色 accent + 白底
# ============================================================
CORPORATE = Style(
    key="corporate",
    name="企业蓝金",
    mermaid_theme="base",
    primary_color="#E8EFF7",
    primary_text_color="#0B1F3A",
    primary_border_color="#1E3A8A",
    secondary_color="#F6F8FC",
    tertiary_color="#C7D2FE",
    line_color="#1E3A8A",
    background="#FDFCF8",
    accent_color="#C9A227",
    accent_text_color="#44371A",
    accent_border_color="#A47E11",
    note_color="#FEF9E7",
    note_border="#D4A72C",
    gradient_start="#C7D2FE",
    gradient_end="#93C5FD",
    corner_radius=6,
    stroke_width=1.6,
    palette=["#1E3A8A", "#C9A227", "#0B1F3A", "#7C6D2A", "#475569"],
)

# ============================================================
# 水墨朱砂 ink —— 中国风 / 文化 / 国学 / 出版物
# 米色宣纸底 + 墨黑节点 + 朱砂红 accent
# ============================================================
INK = Style(
    key="ink",
    name="水墨朱砂",
    mermaid_theme="neutral",
    primary_color="#F6F2E7",
    primary_text_color="#1A1A1A",
    primary_border_color="#2D2D2D",
    secondary_color="#FAF6EC",
    tertiary_color="#D9D4C4",
    line_color="#3A3A3A",
    background="#FAF4E6",
    accent_color="#C0392B",
    accent_text_color="#FFFFFF",
    accent_border_color="#922B21",
    note_color="#FFF8E1",
    note_border="#D6B370",
    gradient_start="",
    gradient_end="",
    corner_radius=4,
    stroke_width=1.4,
    shadow_close_opacity=0.05,
    shadow_far_opacity=0.06,
    palette=["#2D2D2D", "#C0392B", "#7D6608", "#34495E", "#6D4C41"],
)

# ============================================================
# 新粗野主义 neubrutalism —— 潮流 / 独立站 / 设计师作品集
# 亮色粗边 + 硬阴影（4px 偏移，无模糊）+ 0 圆角
# ============================================================
NEUBRUTALISM = Style(
    key="neubrutalism",
    name="新粗野主义",
    mermaid_theme="base",
    primary_color="#FFE066",
    primary_text_color="#111111",
    primary_border_color="#111111",
    secondary_color="#FFFFFF",
    tertiary_color="#111111",
    line_color="#111111",
    background="#FFFBEA",
    accent_color="#FF3E6C",
    accent_text_color="#111111",
    accent_border_color="#111111",
    note_color="#D4FFEF",
    note_border="#111111",
    gradient_start="",
    gradient_end="",
    corner_radius=0,
    stroke_width=2.8,
    # 硬阴影（无模糊 + 大偏移）
    shadow_close_blur=0,
    shadow_close_offset=4,
    shadow_close_opacity=1.0,
    shadow_far_blur=0,
    shadow_far_offset=0,
    shadow_far_opacity=0,
    shadow_color="#111111",
    font_weight_node=700,
    category_mode="bold",
    palette=["#FFE066", "#FF3E6C", "#4CC9F0", "#06D6A0", "#B892FF"],
)

# ============================================================
# 双色调 duotone —— Stripe / Vercel 官方 blog 风
# 深蓝 + 珊瑚粉两色极简，高级感强
# ============================================================
DUOTONE = Style(
    key="duotone",
    name="双色调",
    mermaid_theme="base",
    primary_color="#FFFFFF",
    primary_text_color="#0A2540",
    primary_border_color="#0A2540",
    secondary_color="#F6F9FC",
    tertiary_color="#E3EBF6",
    line_color="#425466",
    background="#FFFFFF",
    accent_color="#FF5A5F",
    accent_text_color="#FFFFFF",
    accent_border_color="#E63946",
    note_color="#F6F9FC",
    note_border="#FF5A5F",
    gradient_start="#F6F9FC",
    gradient_end="#E3EBF6",
    corner_radius=14,
    stroke_width=1.8,
    shadow_close_opacity=0.04,
    shadow_far_opacity=0.10,
    shadow_far_blur=16,
    palette=["#0A2540", "#FF5A5F", "#00D4FF", "#635BFF", "#425466"],
)

# ============================================================
# 编辑杂志 editorial —— NYT / Monocle 风（v1.4 新增）
# 米色底 + 衬线感（mermaid 字体 stack 调整）+ 朱砂报头红 + 长篇排版感
# ============================================================
EDITORIAL = Style(
    key="editorial",
    name="编辑杂志",
    mermaid_theme="base",
    primary_color="#F5EFE0",          # NYT 米色卡
    primary_text_color="#0F0F0F",     # 报纸黑
    primary_border_color="#D0021B",   # NYT 报头红
    secondary_color="#FAF8F5",        # 浅米
    tertiary_color="#D6CFB8",         # 边线浅棕
    line_color="#3A3A3A",
    background="#FAF8F5",             # 米白底
    accent_color="#FF6347",           # 番茄红
    accent_text_color="#FFFFFF",
    accent_border_color="#C0392B",
    note_color="#FFF6DC",
    note_border="#D6B370",
    font_family=(
        '"Cheltenham", "NYT Imperial", "Plantin MT", "Times New Roman", '
        '"Songti SC", "Source Serif Pro", "Noto Serif SC", '
        '"PingFang SC", serif'
    ),
    font_weight_node=600,
    gradient_start="",
    gradient_end="",
    corner_radius=2,                  # 接近直角，杂志感
    stroke_width=1.5,
    shadow_close_opacity=0.05,
    shadow_far_opacity=0.06,
    shadow_far_blur=10,
    palette=["#D0021B", "#0F0F0F", "#A56B33", "#1F2A1F", "#FF6347"],
)

# ============================================================
# 包豪斯 bauhaus —— 红黄蓝三原色 + 几何块面（v1.4 新增）
# 象牙底 + 三原色硬填 + 1.5pt 黑描边 + 0 圆角 + Futura 风
# ============================================================
BAUHAUS = Style(
    key="bauhaus",
    name="包豪斯",
    mermaid_theme="base",
    primary_color="#D32F2F",          # 包豪斯红
    primary_text_color="#FAFAFA",     # 象牙文字（红底用白）
    primary_border_color="#0A0A0A",   # 黑描边
    secondary_color="#FFD600",        # 包豪斯黄
    tertiary_color="#1565C0",         # 包豪斯蓝
    line_color="#0A0A0A",
    background="#FAFAFA",             # 象牙白底
    accent_color="#FFD600",           # 强调色用黄
    accent_text_color="#0A0A0A",
    accent_border_color="#0A0A0A",
    note_color="#FFFDE7",
    note_border="#0A0A0A",
    font_family=(
        '"Futura", "Avenir Next", "Century Gothic", "Trebuchet MS", '
        '"PingFang SC", "Microsoft YaHei", sans-serif'
    ),
    font_weight_node=700,
    gradient_start="",
    gradient_end="",
    corner_radius=0,                  # 严格几何
    stroke_width=1.8,
    shadow_close_blur=0,
    shadow_close_offset=0,
    shadow_close_opacity=0,
    shadow_far_blur=0,
    shadow_far_offset=0,
    shadow_far_opacity=0,
    shadow_color="#0A0A0A",
    category_mode="bold",
    palette=["#D32F2F", "#FFD600", "#1565C0", "#0A0A0A", "#FAFAFA"],
)

# ============================================================
# 瑞士国际主义 swiss —— Müller-Brockmann / Helvetica 网格（v1.4 新增）
# 纯白底 + 黑文字 + 1px 黑描边 + 朱砂红 accent + Helvetica
# ============================================================
SWISS = Style(
    key="swiss",
    name="瑞士国际主义",
    mermaid_theme="base",
    primary_color="#FFFFFF",          # 纯白节点
    primary_text_color="#000000",     # 纯黑文字
    primary_border_color="#000000",   # 纯黑描边
    secondary_color="#F5F5F5",        # 极浅灰
    tertiary_color="#E0E0E0",         # 网格灰
    line_color="#000000",
    background="#FFFFFF",
    accent_color="#D4181F",           # 报头红
    accent_text_color="#FFFFFF",
    accent_border_color="#000000",
    note_color="#F5F5F5",
    note_border="#000000",
    font_family=(
        '"Helvetica Neue", "Helvetica", "Akzidenz-Grotesk", '
        '"Inter", "PingFang SC", "Microsoft YaHei", sans-serif'
    ),
    font_weight_node=500,
    gradient_start="",
    gradient_end="",
    corner_radius=0,                  # Swiss grid = 严格直角
    stroke_width=1.0,                 # 1px 细描边
    shadow_close_blur=0,
    shadow_close_offset=0,
    shadow_close_opacity=0,
    shadow_far_blur=0,
    shadow_far_offset=0,
    shadow_far_opacity=0,
    shadow_color="#000000",
    palette=["#000000", "#D4181F", "#666666", "#999999", "#CCCCCC"],
)


_ALL = {
    s.key: s
    for s in (
        MODERN,
        CLASSIC,
        DARK,
        XIAOHONGSHU,
        OCEAN,
        FOREST,
        SUNSET,
        MINIMAL,
        PASTEL,
        GITHUB,
        CORPORATE,
        INK,
        NEUBRUTALISM,
        DUOTONE,
        EDITORIAL,
        BAUHAUS,
        SWISS,
    )
}
_ALIAS = {
    "现代": MODERN.key,
    "商务": MODERN.key,
    "linear": MODERN.key,
    "vercel": MODERN.key,
    "经典": CLASSIC.key,
    "稳重": CLASSIC.key,
    "暗色": DARK.key,
    "黑色": DARK.key,
    "霓虹": DARK.key,
    "dark-neon": DARK.key,
    "linear-dark": DARK.key,
    "小红书": XIAOHONGSHU.key,
    "xhs": XIAOHONGSHU.key,
    "奶油": XIAOHONGSHU.key,
    "海洋": OCEAN.key,
    "蓝": OCEAN.key,
    "蓝色": OCEAN.key,
    "森林": FOREST.key,
    "绿": FOREST.key,
    "绿色": FOREST.key,
    "自然": FOREST.key,
    "夕阳": SUNSET.key,
    "暖橙": SUNSET.key,
    "橙": SUNSET.key,
    "橙色": SUNSET.key,
    "极简": MINIMAL.key,
    "素雅": MINIMAL.key,
    "黑白": MINIMAL.key,
    "学术": MINIMAL.key,
    "论文": MINIMAL.key,
    "notion": MINIMAL.key,
    "马卡龙": PASTEL.key,
    "粉嫩": PASTEL.key,
    "粉": PASTEL.key,
    "粉色": PASTEL.key,
    "儿童": PASTEL.key,
    "极客": GITHUB.key,
    "程序员": GITHUB.key,
    "gh": GITHUB.key,
    # v1.3.2 新增
    "企业": CORPORATE.key,
    "蓝金": CORPORATE.key,
    "金融": CORPORATE.key,
    "政府": CORPORATE.key,
    "正式": CORPORATE.key,
    "年报": CORPORATE.key,
    "水墨": INK.key,
    "朱砂": INK.key,
    "中国风": INK.key,
    "国学": INK.key,
    "国画": INK.key,
    "宣纸": INK.key,
    "粗野": NEUBRUTALISM.key,
    "新粗野": NEUBRUTALISM.key,
    "潮流": NEUBRUTALISM.key,
    "brutalism": NEUBRUTALISM.key,
    "brutalist": NEUBRUTALISM.key,
    "nb": NEUBRUTALISM.key,
    "双色": DUOTONE.key,
    "双色调": DUOTONE.key,
    "stripe": DUOTONE.key,
    "珊瑚": DUOTONE.key,
    "coral": DUOTONE.key,
    # v1.4 新增：编辑杂志 / 包豪斯 / 瑞士国际主义
    "编辑": EDITORIAL.key,
    "杂志": EDITORIAL.key,
    "纽约客": EDITORIAL.key,
    "纽约时报": EDITORIAL.key,
    "nyt": EDITORIAL.key,
    "monocle": EDITORIAL.key,
    "editorial": EDITORIAL.key,
    "report": EDITORIAL.key,
    "包豪斯": BAUHAUS.key,
    "三原色": BAUHAUS.key,
    "几何": BAUHAUS.key,
    "bauhaus": BAUHAUS.key,
    "primary-colors": BAUHAUS.key,
    "瑞士": SWISS.key,
    "国际主义": SWISS.key,
    "swiss": SWISS.key,
    "swiss-style": SWISS.key,
    "international": SWISS.key,
    "helvetica": SWISS.key,
    "grid": SWISS.key,
    "müller": SWISS.key,
    "brockmann": SWISS.key,
}


def get_style(key: str) -> Style:
    k = (key or "modern").strip().lower()
    if k in _ALL:
        return _ALL[k]
    if k in _ALIAS:
        return _ALL[_ALIAS[k]]
    raise ValueError(f"未知风格：{key}；可选 {list(_ALL)}")


def list_styles() -> Dict[str, Style]:
    return dict(_ALL)


def to_mermaid_theme_variables(style: Style) -> Dict[str, str]:
    """Mermaid initialize 支持的 themeVariables。"""
    return {
        "primaryColor": style.primary_color,
        "primaryTextColor": style.primary_text_color,
        "primaryBorderColor": style.primary_border_color,
        "lineColor": style.line_color,
        "secondaryColor": style.secondary_color,
        "tertiaryColor": style.tertiary_color,
        "background": style.background,
        "mainBkg": style.primary_color,
        "secondBkg": style.secondary_color,
        "tertiaryBkg": style.tertiary_color,
        "fontFamily": style.font_family,
        "fontSize": style.font_size,
        "noteBkgColor": style.note_color,
        "noteBorderColor": style.note_border,
        "noteTextColor": style.primary_text_color,
        "actorBkg": style.primary_color,
        "actorBorder": style.primary_border_color,
        "actorTextColor": style.primary_text_color,
        "activationBkgColor": style.secondary_color,
        "sequenceNumberColor": style.primary_text_color,
        "clusterBkg": style.secondary_color,
        "clusterBorder": style.tertiary_color,
        "titleColor": style.primary_border_color,
        "edgeLabelBackground": style.background,
        "signalColor": style.line_color,
        "signalTextColor": style.primary_text_color,
        "labelBoxBkgColor": style.secondary_color,
        "labelBoxBorderColor": style.tertiary_color,
        "labelTextColor": style.primary_text_color,
        "loopTextColor": style.primary_text_color,
        "activationBorderColor": style.primary_border_color,
    }


def to_mermaid_init_directive(style: Style, diagram_type: str = "flowchart") -> str:
    """返回 `%%{init: {...}}%%` 这一行，放在 Mermaid 代码最前。

    diagram_type 用于按图类选择最佳曲线（不同图适合不同 curve）。
    """
    import json
    # 按图类选择曲线
    curve_by_type = {
        "flowchart": "basis",
        "architecture": "basis",
        "state": "basis",
        "swimlane_mermaid": "linear",
        "sequence": "basis",
        "c4_context": "basis",
        "c4_container": "basis",
    }
    curve = curve_by_type.get(diagram_type, "basis")
    cfg = {
        "theme": style.mermaid_theme,
        "themeVariables": to_mermaid_theme_variables(style),
        "flowchart": {
            "curve": curve,
            "htmlLabels": True,
            "useMaxWidth": False,
            "nodeSpacing": style.node_spacing,
            "rankSpacing": style.rank_spacing,
            "padding": style.padding,
            "diagramPadding": 24,
            "defaultRenderer": "dagre-wrapper",
        },
        "sequence": {
            "mirrorActors": False,
            "showSequenceNumbers": False,
            "actorMargin": 80,
            "boxMargin": 14,
            "messageMargin": 45,
            "noteMargin": 14,
            "wrap": True,
            "width": 160,
        },
        "gantt": {
            "barHeight": 24,
            "barGap": 8,
            "topPadding": 60,
            "leftPadding": 90,
            "fontSize": 13,
            "sectionFontSize": 14,
            "numberSectionStyles": 4,
        },
        "er": {
            "layoutDirection": "TB",
            "entityPadding": 18,
            "fontSize": 13,
            "minEntityWidth": 120,
            "minEntityHeight": 80,
        },
        "state": {
            "padding": 16,
            "titleTopMargin": 20,
        },
        "themeCSS": _mermaid_css(style),
    }
    return "%%{init: " + json.dumps(cfg, ensure_ascii=False) + "}%%"


def _hex_rgb(hex_color: str) -> str:
    h = (hex_color or "#0F172A").lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"{r},{g},{b}"


def _mermaid_css(style: Style) -> str:
    """注入自定义 CSS：圆角、双层投影、边标签 pill、箭头圆润、标题对齐。Mermaid 10+ 支持 themeCSS。

    双层 drop-shadow 模拟 Linear / Vercel 的浮起质感。
    """
    r = style.corner_radius
    sw = style.stroke_width
    shadow_rgb = _hex_rgb(style.shadow_color)
    primary_rgb = _hex_rgb(style.primary_border_color)
    # 双层阴影：近处 + 远处
    close = (
        f"drop-shadow(0 {style.shadow_close_offset}px "
        f"{style.shadow_close_blur}px rgba({shadow_rgb},{style.shadow_close_opacity}))"
    )
    far = (
        f"drop-shadow(0 {style.shadow_far_offset}px "
        f"{style.shadow_far_blur}px rgba({shadow_rgb},{style.shadow_far_opacity}))"
    )
    shadow = f"{close} {far}"
    return (
        # ---- 节点形状 ----
        f".node rect,.node path{{"
        f"rx:{r}px;ry:{r}px;stroke-width:{sw}px;"
        f"filter:{shadow};"
        f"}}"
        f".node circle,.node ellipse{{"
        f"stroke-width:{sw}px;filter:{shadow};"
        f"}}"
        f".node polygon{{stroke-width:{sw}px;filter:{shadow};stroke-linejoin:round;}}"
        # ---- 连线（更粗 + 圆端点 + 实端平滑）----
        f".edgePath .path{{"
        f"stroke-width:{sw + 0.2}px;"
        f"stroke-linecap:round;stroke-linejoin:round;"
        f"}}"
        # 箭头 marker 增大
        f"marker#flowchart-pointEnd,marker#flowchart-pointStart,"
        f"marker path,.flowchart-link>path{{stroke-linejoin:round;}}"
        f"defs marker{{overflow:visible;}}"
        # ---- 容器（cluster / subgraph）----
        f".cluster rect{{"
        f"rx:{r + 4}px;ry:{r + 4}px;"
        f"stroke-width:{max(sw - 0.3, 1.0)}px;"
        f"stroke-dasharray:none;"
        f"filter:{close};"
        f"}}"
        # 标题字体 + 位置（强制向上）
        f".cluster .cluster-label,.cluster .label,.cluster text,"
        f".cluster .nodeLabel{{"
        f"font-weight:700;font-size:14px;"
        f"color:{style.primary_border_color};"
        f"fill:{style.primary_border_color};"
        f"letter-spacing:.3px;"
        f"}}"
        f".cluster .cluster-label foreignObject{{overflow:visible;}}"
        # ---- 节点字体 ----
        f".node .label,.node text,.nodeLabel{{"
        f"font-weight:{style.font_weight_node};letter-spacing:.2px;"
        f"}}"
        f".label foreignObject{{overflow:visible;}}"
        # ---- 边标签 pill（关键美化点）----
        f".edgeLabel{{"
        f"background-color:{style.background};"
        f"padding:3px 10px;"
        f"border-radius:999px;"
        f"font-size:12px;font-weight:500;"
        f"color:{style.primary_text_color};"
        f"border:1px solid {style.tertiary_color};"
        f"box-shadow:0 1px 3px rgba({primary_rgb},0.08);"
        f"}}"
        f".edgeLabel rect{{fill:{style.background};}}"
        # ---- 时序图修饰 ----
        f".actor{{rx:{r}px;ry:{r}px;filter:{close};}}"
        f".actor-line{{stroke:{style.tertiary_color};stroke-dasharray:2,3;}}"
        f".messageText{{font-size:13px;font-weight:500;}}"
        f".note,.noteText{{rx:8px;ry:8px;filter:{close};}}"
        f".loopText tspan,.sequenceNumber{{font-weight:600;}}"
        # ---- 状态图 ----
        f".state-start,.state-end{{stroke-width:{sw}px;filter:{close};}}"
        # ---- 标题 ----
        f".mermaid text.titleText{{"
        f"font-weight:700;font-size:18px;"
        f"fill:{style.primary_border_color};"
        f"}}"
    )


def semantic_colors(style: Style) -> Dict[str, str]:
    """语义边配色：success / warning / error / info / neutral。

    每个语义对应一个连线色（stroke + 文字）。暗色系下稍微提亮。
    """
    is_dark = style.background.lstrip("#").lower() in (
        "0f172a", "111827", "1a1a1a", "000000", "0a0a0a",
    )
    if is_dark:
        return {
            "success": "#34D399",
            "warning": "#FBBF24",
            "error":   "#F87171",
            "info":    "#60A5FA",
            "neutral": style.line_color,
        }
    return {
        "success": "#10B981",
        "warning": "#F59E0B",
        "error":   "#EF4444",
        "info":    "#3B82F6",
        "neutral": style.line_color,
    }


def decision_classdef(style: Style) -> str:
    """用于 flowchart 内的 classDef decision 行：判断菱形用 accent 配色。"""
    return (
        f"classDef decision fill:{style.accent_color},"
        f"stroke:{style.accent_border_color},"
        f"color:{style.accent_text_color},"
        f"stroke-width:{style.stroke_width}px,"
        f"font-weight:600"
    )


def database_classdef(style: Style) -> str:
    """数据库节点配色（cylinder）。"""
    return (
        f"classDef database fill:{style.secondary_color},"
        f"stroke:{style.line_color},"
        f"color:{style.primary_text_color},"
        f"stroke-width:{style.stroke_width}px"
    )


def terminal_classdef(style: Style) -> str:
    """开始/结束（stadium/圆角胶囊）节点：实色填充 + 描边 accent，像 START 按钮。"""
    return (
        f"classDef terminal fill:{style.primary_border_color},"
        f"stroke:{style.primary_border_color},"
        f"color:#FFFFFF,"
        f"stroke-width:{style.stroke_width}px,"
        f"font-weight:700"
    )


def category_classdefs(style: Style) -> List[str]:
    """生成 5 个基于 palette 的 classDef，支持 category: c1..c5 做视觉分组。

    两种模式：
    - soft（默认，Linear/Vercel 风）：浅色 tertiary 填充 + palette 描边/文字
    - bold（Neubrutalism/Ink 风）：palette 色填充 + 深色文字 + 深色描边
    """
    out: List[str] = []
    mode = getattr(style, "category_mode", "soft")
    if mode == "bold":
        # 深色文字 = primary_text_color（通常 #111）
        # 深色描边 = 同上
        dark = style.primary_text_color
        for i, col in enumerate(style.palette[:5], start=1):
            out.append(
                f"classDef c{i} fill:{col},"
                f"stroke:{dark},color:{dark},"
                f"stroke-width:{max(style.stroke_width, 2.2)}px,"
                f"font-weight:700"
            )
    else:
        for i, col in enumerate(style.palette[:5], start=1):
            out.append(
                f"classDef c{i} fill:{style.tertiary_color},"
                f"stroke:{col},color:{col},"
                f"stroke-width:{style.stroke_width}px,"
                f"font-weight:600"
            )
    return out


def to_plantuml_skinparam(style: Style) -> str:
    """PlantUML skinparam 片段（泳道图 / 活动图 / 时序图 / C4 用）。

    PlantUML 不支持 CSS drop-shadow；改用 shadowing + 单色阴影近似。
    """
    font_name = style.font_family.split(",")[0].strip('"').strip()
    shadow = "true" if style.shadow_far_opacity > 0.03 else "false"
    return f"""skinparam backgroundColor {style.background}
skinparam defaultFontName {font_name}
skinparam defaultFontSize 14
skinparam defaultFontColor {style.primary_text_color}
skinparam roundCorner {style.corner_radius}
skinparam shadowing {shadow}
skinparam handwritten false
skinparam monochrome false
skinparam padding 6
skinparam dpi 120

skinparam titleFontSize 18
skinparam titleFontColor {style.primary_border_color}
skinparam titleFontStyle bold
skinparam titleBorderThickness 0

skinparam activity {{
    BackgroundColor {style.primary_color}
    BorderColor {style.primary_border_color}
    BorderThickness {style.stroke_width}
    FontColor {style.primary_text_color}
    FontStyle bold
    DiamondBackgroundColor {style.accent_color}
    DiamondBorderColor {style.accent_border_color}
    DiamondFontColor {style.accent_text_color}
    StartColor {style.primary_border_color}
    EndColor {style.accent_color}
    BarColor {style.line_color}
}}

skinparam swimlane {{
    BorderColor {style.tertiary_color}
    BorderThickness 1.2
    TitleBackgroundColor {style.secondary_color}
    TitleFontColor {style.primary_text_color}
    TitleFontStyle bold
}}

skinparam note {{
    BackgroundColor {style.note_color}
    BorderColor {style.note_border}
    BorderThickness 1
    FontColor {style.primary_text_color}
}}

skinparam arrow {{
    Color {style.line_color}
    Thickness {style.stroke_width}
    FontColor {style.primary_text_color}
    FontSize 12
}}

skinparam sequence {{
    ArrowColor {style.line_color}
    ArrowThickness {style.stroke_width}
    LifeLineBorderColor {style.tertiary_color}
    LifeLineBackgroundColor {style.secondary_color}
    ParticipantBackgroundColor {style.primary_color}
    ParticipantBorderColor {style.primary_border_color}
    ParticipantFontColor {style.primary_text_color}
    ParticipantFontStyle bold
    ActorBackgroundColor {style.primary_color}
    ActorBorderColor {style.primary_border_color}
    ActorFontColor {style.primary_text_color}
    BoxBackgroundColor {style.secondary_color}
    BoxBorderColor {style.tertiary_color}
    DividerBackgroundColor {style.tertiary_color}
    GroupBackgroundColor {style.secondary_color}
    GroupBorderColor {style.tertiary_color}
    GroupFontColor {style.primary_text_color}
}}

skinparam rectangle {{
    BackgroundColor {style.secondary_color}
    BorderColor {style.tertiary_color}
    BorderThickness 1
    FontColor {style.primary_text_color}
    roundCorner {style.corner_radius}
}}

skinparam package {{
    BackgroundColor {style.secondary_color}
    BorderColor {style.tertiary_color}
    FontColor {style.primary_text_color}
    FontStyle bold
}}
"""
