# ============================================================
# 色板注册表 —— 分档的唯一分界线
#
#   community.py  开源版自带，MIT，随仓库分发
#   brand.py      付费包独占（品牌推导四套，含两套亮色）
#                 开源仓的 .gitignore 会排掉它；没有它时生成器照常工作，
#                 只是少四套主题、默认主题回退到 tokyo-night。
#
# 加自己的主题：新建 palettes/mine.py，里面写 PALETTES = {...}，
# 本文件会自动发现（扫同目录下所有 .py，除了 __init__）。
# ============================================================
import importlib
import os
import pkgutil

from . import _audit

# 缺 brand.py 时的默认主题回退顺序（第一个存在的即为默认）
DEFAULT_ORDER = ["ember", "tokyo-night", "catppuccin-mocha"]

# 旧主题名 → 新主题名。色板键已改成英文名，但用户机器上的 pin、scene.env、
# auto.conf、workspace 记录可能还留着旧名，脚本侧用这张表兜底。
# ⚠️ 与 lib/aliases.sh 保持同步；改一边记得改另一边。
ALIASES = {
    "v2-mihei": "ember",
    "v1-keji": "voltage",
    "v2-mibai": "parchment",
    "v3-caijing-bai": "ledger",
}

# 归一化记录：{主题名: [改动, …]}，供 _generate.py 打印。
# 社区色板是把上游原值抄进来的，上游并不遵守「normal≠bright / 对比度地板」，
# 所以 load() 会就地解一次；品牌四套按约束解出来的，不过这道工序。
ADJUSTMENTS: dict[str, list[dict]] = {}

# 付费包提供的主题名 —— 仅用于生成器打印分档提示，不参与逻辑判断
BRAND_THEMES = ["ember", "voltage", "parchment", "ledger"]


def load():
    """扫本包下所有模块，合并它们的 PALETTES。返回 (palettes, 来源映射)。"""
    palettes, origin = {}, {}
    here = os.path.dirname(__file__)
    # community 先加载，其余按名字排序 —— 同名主题后加载的覆盖先加载的
    names = sorted(
        (m.name for m in pkgutil.iter_modules([here])),
        key=lambda n: (n != "community", n),
    )
    for mod_name in names:
        mod = importlib.import_module(f"{__name__}.{mod_name}")
        for key, val in getattr(mod, "PALETTES", {}).items():
            # 品牌四套已经在解空间里，再归一化只会把品牌色推走；
            # 其余（社区 / 用户导入 / 自己写的 mine.py）统一补约束。
            if mod_name != "brand" and val.get("ansi") and val.get("normalize", True):
                val, changes = _audit.normalize_palette(key, val)
                if changes:
                    ADJUSTMENTS[key] = changes
            # 提彩度对品牌/非品牌都适用：只放大 A/B，色相与明度不动。
            factor = float(val.get("vivid", _audit.VIVID_DEFAULTS.get(key, 1.0)))
            if factor != 1.0:
                val, vchanges = _audit.vivid_palette(key, val, factor)
                if vchanges:
                    ADJUSTMENTS.setdefault(key, []).extend(vchanges)
            # 品牌/导入主题补红绿色盲分离；社区主题保持上游色相，不强行改
            if mod_name in ("brand", "imported") and val.get("ansi"):
                val, cchanges = _audit.fix_cvd_palette(val)
                if cchanges:
                    ADJUSTMENTS.setdefault(key, []).extend(cchanges)
            # 签名强调色：优先色板自己的 accent，其次内置表，最后回退 cursor
            accent = val.get("accent", _audit.ACCENT_DEFAULTS.get(key, val.get("cursor", "")))
            if accent:
                val["accent"] = str(accent).lstrip("#")
                val["cursor"] = val["accent"]
            palettes[key] = val
            origin[key] = mod_name
    return palettes, origin


def default_theme(palettes):
    for name in DEFAULT_ORDER:
        if name in palettes:
            return name
    return next(iter(palettes), "")
