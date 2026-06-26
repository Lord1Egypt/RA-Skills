"""全局配置：颜色、字体、常量"""
from dataclasses import dataclass, field
import matplotlib.font_manager as fm
import platform


# ---------- 颜色方案 ----------
@dataclass(frozen=True)
class Colors:
    # 主色系 — 稳重深蓝（机构级金融报告标准色）
    PRIMARY: str = "#1B3A5C"       # 藏青蓝，沉稳大气
    SECONDARY: str = "#2D6A9F"    # 钴蓝，层次递进
    ACCENT: str = "#D4A03C"       # 哑光金，高端强调（替代刺眼橙色）
    # 表格
    HEADER_BG: str = "#1B3A5C"    # 表头与主色统一
    HEADER_TEXT: str = "#FFFFFF"
    ROW_ALT: str = "#EDF2F7"      # 冷灰蓝交替行（比纯灰更协调）
    # 语义色
    POSITIVE: str = "#1A7F37"     # 深松绿（比亮绿更专业）
    NEGATIVE: str = "#CF222E"     # 正红（比暗红更清晰）
    NEUTRAL: str = "#57606A"      # 石墨灰
    # 背景与边框
    LIGHT_BG: str = "#F6F8FA"     # 极浅灰蓝
    BORDER: str = "#D1D9E0"       # 柔和边框
    # 警告色
    WARN_ORANGE: str = "#BF6A02"  # 琥珀橙（柔和但醒目）
    WARN_RED: str = "#A40E26"     # 深红警告


COLORS = Colors()

# ---------- 多系列图表色板（16+色，板块/品种折线图用） ----------
SECTOR_PALETTE = [
    "#E63946",  # 红
    "#457B9D",  # 钢蓝
    "#2A9D8F",  # 青绿
    "#E9C46A",  # 金黄
    "#264653",  # 深青
    "#F4A261",  # 橙
    "#6A4C93",  # 紫
    "#1982C4",  # 天蓝
    "#8AC926",  # 黄绿
    "#FF595E",  # 珊瑚红
    "#BC6C25",  # 棕
    "#606C38",  # 橄榄绿
    "#CA6702",  # 琥珀
    "#AE2012",  # 砖红
    "#0A9396",  # 暗青
    "#9B2226",  # 深红
    "#94D2BD",  # 薄荷
    "#BB3E03",  # 深橙
]

# ---------- reportlab 颜色元组 ----------
def hex_to_rgb(h: str):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4))


# ---------- 字体探测 ----------
def find_chinese_font() -> str:
    candidates = [
        "Songti SC", "PingFang SC", "STHeiti", "Heiti SC",
        "PingFang HK", "Heiti TC", "STSong", "SimHei",
        "Microsoft YaHei", "WenQuanYi Micro Hei", "Noto Sans CJK SC",
    ]
    available = {f.name for f in fm.fontManager.ttflist}
    for c in candidates:
        if c in available:
            return c
    # fallback: search ttc/ttf files
    for f in fm.findSystemFonts():
        if any(k in f.lower() for k in ["pingfang", "heiti", "stheiti"]):
            prop = fm.FontProperties(fname=f)
            return prop.get_name()
    return "sans-serif"


CHINESE_FONT = find_chinese_font()

# ---------- matplotlib 全局配置 ----------
def setup_matplotlib():
    import matplotlib as mpl
    mpl.rcParams["font.sans-serif"] = [CHINESE_FONT, "DejaVu Sans"]
    mpl.rcParams["axes.unicode_minus"] = False
    mpl.rcParams["figure.dpi"] = 150
    mpl.rcParams["savefig.dpi"] = 150
    mpl.rcParams["figure.facecolor"] = "white"
    mpl.rcParams["axes.facecolor"] = "white"
    mpl.rcParams["axes.edgecolor"] = "#D1D9E0"
    mpl.rcParams["axes.linewidth"] = 0.8
    mpl.rcParams["axes.grid"] = False
    mpl.rcParams["grid.color"] = "#E8ECF0"
    mpl.rcParams["grid.linewidth"] = 0.5
    mpl.rcParams["xtick.color"] = "#57606A"
    mpl.rcParams["ytick.color"] = "#57606A"
    mpl.rcParams["xtick.labelsize"] = 9
    mpl.rcParams["ytick.labelsize"] = 9
    mpl.rcParams["legend.framealpha"] = 0.9
    mpl.rcParams["legend.edgecolor"] = "#D1D9E0"
    mpl.rcParams["legend.fancybox"] = True


# ---------- 行业基准 ----------
INDUSTRY_BENCHMARKS = {
    "年化收益率": {"good": 0.15, "excellent": 0.25},
    "年化波动率": {"good": 0.20, "warning": 0.30},
    "最大回撤": {"good": -0.20, "warning": -0.30},
    "夏普比率": {"good": 1.0, "excellent": 1.5},
    "卡玛比率": {"good": 1.5, "excellent": 2.0},
    "索提诺比率": {"good": 1.5, "excellent": 2.0},
    "日胜率": {"good": 0.50},
    "日盈亏比": {"good": 1.5},
}

# ---------- CTA 市场均值 (用于对比) ----------
CTA_MARKET_AVG = {
    "累计收益率": 0.65,
    "年化收益率": 0.10,
    "最大回撤": -0.15,
    "夏普比率": 0.7,
    "年化波动率": 0.18,
}

CTA_TOP = {
    "累计收益率": 1.80,
    "年化收益率": 0.25,
    "最大回撤": -0.12,
    "夏普比率": 1.5,
    "年化波动率": 0.22,
}

# ---------- 板块映射（16 板块，来源：板块.xlsx） ----------
SECTOR_MAP = {
    "农副": ["AP", "CJ", "jd", "lg", "lh", "op", "SP"],
    "黑色": ["hc", "i", "j", "jm", "rb", "SF", "SM", "wr"],
    "国债": ["T", "TF", "TL", "TS"],
    "建材": ["bb", "fb", "FG", "SA"],
    "油化": ["l", "PF", "pp", "PR", "PX", "TA", "v"],
    "煤化": ["bz", "eb", "eg", "MA", "PL", "SH", "UR"],
    "能源": ["bu", "fu", "lu", "pg", "sc", "ZC"],
    "谷物": ["JR", "LR", "PM", "RI", "rr", "WH"],
    "有色": ["ad", "al", "ao", "bc", "cu", "ni", "pb", "sn", "ss", "zn"],
    "新能源": ["lc", "ps", "si"],
    "油脂": ["OI", "p", "y"],
    "油料": ["a", "b", "c", "cs", "m", "PK", "RM", "RS"],
    "贵金": ["ag", "au", "pd", "pt"],
    "橡胶": ["br", "nr", "ru"],
    "软商": ["CF", "CY", "SR"],
    "指数": ["ec", "IC", "IF", "IH", "IM"],
}

# 构建反向索引（品种→板块），加速查找
_VARIETY_TO_SECTOR: dict[str, str] = {}
for _sector, _varieties in SECTOR_MAP.items():
    for _v in _varieties:
        _VARIETY_TO_SECTOR[_v] = _sector


def get_sector(variety: str) -> str:
    # 精确匹配
    if variety in _VARIETY_TO_SECTOR:
        return _VARIETY_TO_SECTOR[variety]
    # 去除后缀匹配（处理 _o、_F 等期权/远期变体）
    base = variety.rsplit("_", 1)[0] if "_" in variety else variety
    if base in _VARIETY_TO_SECTOR:
        return _VARIETY_TO_SECTOR[base]
    return "其他"


# ---------- 评级星级 ----------
def star_rating(sharpe: float, ret: float, mdd: float) -> str:
    score = 0
    if ret > 0.30: score += 2
    elif ret > 0.15: score += 1
    if sharpe > 1.0: score += 2
    elif sharpe > 0.5: score += 1
    if mdd > -0.15: score += 1
    stars = min(5, max(1, score))
    return "★" * stars + "☆" * (5 - stars)
