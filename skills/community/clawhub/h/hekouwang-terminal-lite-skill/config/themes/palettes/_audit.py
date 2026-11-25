# ============================================================
# 色板视觉审计 · 对比度 / 明暗分档 / 约束解算
#
# 被 palettes/__init__.py 在 load() 时调用（归一化社区与导入色板），
# 以及 config/themes/_audit.py（只读审计，读**生成后的 JSON**）。
#
# 为什么要有这个文件：brand.py 头部那四条方法（WCAG 反解、normal≠bright、
# 饱和按性格定、色相是身份）以前只是**写在注释里的规矩**，社区色板原样照抄
# 上游，于是 rose-pine / tokyo-night / catppuccin 有三到七对 normal=bright，
# tokyo-night 的 ANSI 8 只有 1.9:1 —— 提示符右栏（bright-black）几乎是空的。
# 规矩不落到代码里，就一定会被下一套导入的主题破坏。
#
# 约束（只改明度，不动色相）：
#   1. 正文槽 1–6 对 bg ≥ 4.5:1   —— WCAG AA
#   2. 强调槽 9–14 对 bg ≥ 6.0:1  —— 明暗必须真的分成两档
#   3. 暗字槽 8 对 bg ≥ 3.0:1     —— 提示符右栏 / 自动补全都用它
#   4. normal 与 bright 的 OKLab ΔE ≥ 0.03 —— 否则 ls / git diff 的强调被静默吞掉
#   5. diff 新增/删除底 OKLab ΔL ≥ 0.025 —— 灰度、色盲、差投影仪下也要分得开
#   6. 红绿在 deuteranopia / protanopia 下 ΔE ≥ 0.03（修正目标 0.045）
#   7. 中性梯 surface(1.12) < overlay(1.22) < border(1.35)，且 fg/surface ≥4.5
#
# ⚠️ 品牌四套（brand.py）**不归一化**：它们是按同一套约束解出来的，
#    已经在解空间里；再跑一遍只会把品牌色 nud 走。判据是来源，不是结果。
# ============================================================
from __future__ import annotations

import math

MIN_DELTA_E = 0.03          # OKLab 欧氏距离，约一个 JND —— 判「是否同色」的及格线
TARGET_DELTA_E = 0.075      # 解算目标：品牌四套实测 0.11–0.15，社区色板推到 0.075
                            # 已能看出明显一档；再往上靠近白的槽会撞色域上限
CONTRAST_BODY = 4.5         # 正文槽 1–6
CONTRAST_BRIGHT = 6.0       # 强调槽 9–14
CONTRAST_DIM = 3.0          # 暗字槽 8
CONTRAST_SELECTION_LIGHT = 1.40   # 选区底对亮底：低于这个值基本看不出来
CONTRAST_SELECTION_DARK = 1.50    # 选区底对暗底
CONTRAST_SELECTION_TEXT = 4.5     # 选中文字对选区底
CONTRAST_MATCH_BG = 2.0           # 搜索命中底对背景
CONTRAST_MATCH_FG = 4.0           # 正文对搜索命中底
CONTRAST_CURSOR = 3.0             # 光标对背景（非文本 UI 的 3:1 底线）
CONTRAST_LIGHT_WHITE = 3.0        # 亮底主题的 ANSI 7 不能再是“白”
CONTRAST_FAINT = 3.0              # SGR 2 暗字的有效对比
CONTRAST_SYNTAX_SURFACE = 3.0     # 语法角色落在 diff / 语义表面上的可读底线
MIN_NEUTRAL_DELTA_E = 0.03        # 亮底 0/15 不能是同一个中性槽
MIN_HUE_DELTA_E = 0.06            # 六个色相两两之间的最低可区分度
MIN_DIFF_DELTA_L = 0.025          # diff 新增/删除底的明度差：灰度下也要分得开
MIN_CVD_DELTA = 0.03              # 红绿在色盲模拟下的及格线（约一个 JND）
TARGET_CVD_DELTA = 0.045          # 修正目标：留出一点余量

# 提彩度：只放大 OKLab 的 A/B（色相不变），不碰 L。品牌四套的“饱和度性格”
# 仍然由 brand.py 决定，这里只是把已经解出来的色再往前推一档，让 9 套在主题
# 列表和投屏里更容易一眼分开。想收敛某套：在色板里写 "vivid": 1.0 覆盖。
VIVID_DEFAULTS = {
    "catppuccin-mocha": 1.15,     # 粉彩再往前一点，别糊成灰
    "claude-code-light": 1.18,    # 导入的亮色，原本偏灰
    "gruvbox-dark": 1.10,         # 土色系小幅提彩，保住复古感
    "rose-pine": 1.22,            # 莫兰迪色系提彩，否则和 catppuccin 太像
    "tokyo-night": 1.06,          # 本来就够霓虹，只补一点
    "voltage": 1.05,              # 89% 饱和，再推会撞色域
    "parchment": 1.28,            # 编辑部 42% 太克制，提一档才立得住
    "ember": 1.20,                # 同上，暗底更需要彩度
    "ledger": 1.12,               # Material 72%，小幅提亮
}

# 签名强调色：社区四套原来的 cursor 基本等于前景色，badge/tab 没有记忆点。
# 这里给每套钉一个独立 accent，部署时同时作为 cursor / badge / tab 的来源。
ACCENT_DEFAULTS = {
    "catppuccin-mocha": "fab387",   # peach
    "claude-code-light": "d67555",  # clay orange (3.05:1)
    "gruvbox-dark": "fe8019",       # bright orange
    "rose-pine": "eb6f92",          # rose
    "tokyo-night": "7dcfff",        # cyan
    "ember": "e08a5f",              # warm orange
    "voltage": "00d4aa",            # mint
    "parchment": "b85433",          # clay, deepened for cursor text contrast
    "ledger": "1a73e8",             # Material blue
}

SLOT_NAMES = [
    "black", "red", "green", "yellow", "blue", "magenta", "cyan", "white",
    "br-black", "br-red", "br-green", "br-yellow", "br-blue", "br-magenta",
    "br-cyan", "br-white",
]


# ---- 基础色值 -------------------------------------------------
def parse(h: str) -> tuple[float, float, float]:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))  # type: ignore[return-value]


def to_hex(rgb: tuple[float, float, float]) -> str:
    return "".join(f"{max(0, min(255, round(c * 255))):02x}" for c in rgb)


def _lin(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _delinear(c: float) -> float:
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def luminance(h: str) -> float:
    r, g, b = (_lin(c) for c in parse(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: str, b: str) -> float:
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def mix(a: str, b: str, t: float) -> str:
    """把 a 按比例 t 混进 b（t=0 全是 b，t=1 全是 a）。与 _generate.mix 同口径。"""
    ra, ga, ba = parse(a)
    rb, gb, bb = parse(b)
    return to_hex((ra * t + rb * (1 - t),
                   ga * t + gb * (1 - t),
                   ba * t + bb * (1 - t)))


def blend(fg: str, bg: str, alpha: float) -> str:
    """模拟 SGR 2 / 半透明前景落在背景上的实际颜色。"""
    return mix(fg, bg, alpha)


# ---- OKLab（Björn Ottosson）----------------------------------
def srgb_to_oklab(h: str) -> tuple[float, float, float]:
    r, g, b = (_lin(c) for c in parse(h))
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = l ** (1 / 3), m ** (1 / 3), s ** (1 / 3)
    return (
        0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
        1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
        0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_,
    )


def _oklab_to_linear(L: float, A: float, B: float):
    l_ = L + 0.3963377774 * A + 0.2158037573 * B
    m_ = L - 0.1055613458 * A - 0.0638541728 * B
    s_ = L - 0.0894841775 * A - 1.2914855480 * B
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    return (
        4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
        -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
        -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s,
    )


def oklab_to_srgb(L: float, A: float, B: float) -> str:
    """越界时回缩彩度，保住明度与色相 —— 比直接 clamp 三个通道更接近原色。"""
    def render(scale: float) -> tuple[float, float, float] | None:
        r, g, b = _oklab_to_linear(L, A * scale, B * scale)
        rgb = tuple(_delinear(c) for c in (r, g, b))
        if all(-1e-6 <= c <= 1 + 1e-6 for c in rgb):
            return tuple(min(1.0, max(0.0, c)) for c in rgb)
        return None

    ok = render(1.0)
    if ok is None:
        lo, hi = 0.0, 1.0
        for _ in range(24):
            mid = (lo + hi) / 2
            if render(mid) is None:
                hi = mid
            else:
                lo = mid
        ok = render(lo) or (0.0, 0.0, 0.0)
    return to_hex(ok)


def delta_e(a: str, b: str) -> float:
    la, aa, ba = srgb_to_oklab(a)
    lb, ab, bb = srgb_to_oklab(b)
    return ((la - lb) ** 2 + (aa - ab) ** 2 + (ba - bb) ** 2) ** 0.5


# Machado 2009，severity 1.0。线性 RGB 上做，再回 sRGB 算 OKLab ΔE。
_CVD_MATRICES = {
    "deuteranopia": (
        (0.367322, 0.860646, -0.227968),
        (0.280085, 0.672501, 0.047413),
        (-0.011820, 0.042940, 0.968881),
    ),
    "protanopia": (
        (0.152286, 1.052583, -0.204868),
        (0.114503, 0.786281, 0.099216),
        (-0.003882, -0.048116, 1.051998),
    ),
}


def simulate_cvd(color: str, kind: str) -> str:
    """把 sRGB 色投到红绿色盲的感知空间（线性 RGB 矩阵）。"""
    r, g, b = (_lin(c) for c in parse(color))
    m = _CVD_MATRICES[kind]
    out = [sum(m[i][j] * v for j, v in enumerate((r, g, b))) for i in range(3)]
    return to_hex(tuple(_delinear(max(0.0, min(1.0, c))) for c in out))


def cvd_delta(a: str, b: str) -> float:
    """两种常见红绿色盲里，两个颜色最差的那一个的 OKLab ΔE。"""
    return min(
        delta_e(simulate_cvd(a, kind), simulate_cvd(b, kind))
        for kind in _CVD_MATRICES
    )


# ---- 解算 -----------------------------------------------------
def _direction(bg: str) -> int:
    """远离底色 = 暗底往上提亮，亮底往下压深。"""
    return -1 if srgb_to_oklab(bg)[0] > 0.5 else 1


def lift_to_contrast(color: str, bg: str, target: float, light: bool | None = None) -> str:
    """只动 OKLab 明度，把 color 对 bg 的对比度提到 target。色相保持。"""
    if contrast(color, bg) >= target:
        return color
    L, A, B = srgb_to_oklab(color)
    dark_bg = (srgb_to_oklab(bg)[0] <= 0.5) if light is None else (not light)
    step = 0.004 if dark_bg else -0.004
    for _ in range(math_ceil(0.5 / abs(step))):
        L += step
        if L <= 0.02 or L >= 0.995:
            break
        cand = oklab_to_srgb(L, A, B)
        if contrast(cand, bg) >= target:
            return cand
    return oklab_to_srgb(1.0 if dark_bg else 0.0, A, B)


def separate(normal: str, bright: str, bg: str, target: float = TARGET_DELTA_E) -> str:
    """normal 与 bright 太像时，把 bright 往远离底色的方向推。

    越靠近色域边界越推不动（浅黄、近白），所以取**一路上最远的那一个**返回，
    而不是「推不到目标就原样退回」—— 后者会让近白的槽永远停在同色，
    审计照样报错，等于什么都没修。
    """
    if delta_e(normal, bright) >= target:
        return bright
    L, A, B = srgb_to_oklab(bright)
    dark_bg = srgb_to_oklab(bg)[0] <= 0.5
    step = 0.004 if dark_bg else -0.004
    best, best_de = bright, delta_e(normal, bright)
    for _ in range(math_ceil(0.5 / abs(step))):
        L += step
        if L <= 0.02 or L >= 0.995:
            break
        cand = oklab_to_srgb(L, A, B)
        de = delta_e(normal, cand)
        if de > best_de:
            best, best_de = cand, de
        if de >= target:
            return cand
    return best


def math_ceil(x: float) -> int:
    n = int(x)
    return n if n >= x else n + 1


def solve_match(bg: str, fg: str, hue: str,
                min_bg: float = CONTRAST_MATCH_BG,
                min_fg: float = CONTRAST_MATCH_FG) -> str:
    """搜索命中底色：保持 hue 的色相，找同时满足「对背景可见、对正文可读」的明度。

    没有 Match Foreground Color 这个键，命中行只能用正文色画字 —— 所以命中底
    必须同时和 bg、fg 拉开距离。旧配方 `mix(黄, bg, 0.45)` 只管“看起来像黄”，
    暗底会吃掉浅色字（实测 catppuccin fg 只有 3.07），亮底又浅到看不见命中。
    """
    L, A, B = srgb_to_oklab(hue)
    mid = (srgb_to_oklab(bg)[0] + srgb_to_oklab(fg)[0]) / 2
    best = None
    for i in range(1, 500):
        l = 0.02 + i * 0.00194
        cand = oklab_to_srgb(l, A, B)
        cb, cf = contrast(cand, bg), contrast(fg, cand)
        score = min(cb / min_bg, cf / min_fg)
        key = (score, -abs(l - mid))
        if best is None or key > best[0]:
            best = (key, cand)
    return best[1] if best else hue


def min_hue_delta(ansi: list[str]) -> tuple[float, tuple[int, int]]:
    """六个色相里最接近的一对，用来发现 ls / git diff 会混淆的颜色。"""
    best = (9.9, (1, 2))
    for group in (range(1, 7), range(9, 15)):
        slots = list(group)
        for i, si in enumerate(slots):
            for sj in slots[i + 1:]:
                d = delta_e(ansi[si], ansi[sj])
                if d < best[0]:
                    best = (d, (si, sj))
    return best


def diff_surfaces(p: dict) -> tuple[str, str]:
    """diff 新增/删除底色；没有显式 surfaces 时用 19% / 10% 的不对称配方。"""
    s = p.get("surfaces") or {}
    return (
        s.get("diff_add", mix(p["ansi"][2], p["bg"], 0.19)),
        s.get("diff_delete", mix(p["ansi"][1], p["bg"], 0.10)),
    )


# 语法角色会落上去的表面：只看 diff 行底。
# 不把 error/warn/success 表面算进来：那些是日志词/编辑器 squiggle 的背景，
# 上面通常不是语法高亮代码；comment 本身是刻意压暗的次要层，不参与这条 gate。
SYNTAX_SURFACE_KEYS = ("diff_add", "diff_delete")

# 语义表面：错误 > 警告 > 成功 > 信息，重量依次递减
SURFACE_SPECS = {
    "error":   {"slot": 1, "min_bg": 2.35},
    "warn":    {"slot": 3, "min_bg": 2.05},
    "success": {"slot": 2, "min_bg": 1.6},
    "info":    {"slot": 4, "min_bg": 1.4},
}


def solve_surface(bg: str, fg: str, hue: str, min_bg: float,
                  min_text: float = 4.5) -> str:
    """解语义表面：对背景足够可见、正文落在上面仍可读；优先贴近 min_bg。"""
    best = None
    fallback = None
    for i in range(1, 100):
        t = i / 100
        cand = mix(hue, bg, t)
        cb, cf = contrast(cand, bg), contrast(fg, cand)
        score = min(cb / min_bg, cf / min_text)
        if fallback is None or score > fallback[0]:
            fallback = (score, cand)
        if cb >= min_bg - 1e-9 and cf >= min_text + 0.03 - 1e-9:
            key = (abs(cb - min_bg), -cf)
            if best is None or key < best[0]:
                best = (key, cand)
    return best[1] if best else (fallback[1] if fallback else hue)


# 中性梯：背景 → surface → overlay → border → muted → 前景
NEUTRAL_TARGETS = {
    "surface": 1.12,
    "overlay": 1.22,
    "border": 1.35,
}


def neutral_ramp(p: dict) -> dict:
    """解主题的六档中性梯；`neutrals` 可以显式覆盖任意一档。

    用 WCAG 对比度目标而不是固定 OKLab L 偏移：近黑主题需要更大的 L 步进，
    亮色主题需要更小的步进，固定偏移会让 Voltage 的边框几乎看不见。
    """
    explicit = p.get("neutrals") or {}
    bg, fg = p["bg"], p["fg"]
    light = bool(p.get("light"))
    base = mix(p["ansi"][0], bg, 0.10)
    out = {"bg": bg, "fg": fg}
    prev = 1.0
    for key, target in NEUTRAL_TARGETS.items():
        val = explicit.get(key)
        if val:
            out[key] = str(val).lstrip("#")
            prev = max(prev, contrast(out[key], bg))
            continue
        # 基准色本身可能已经超过目标（亮色主题尤其明显），所以每一步都要
        # 至少比上一档再高一档，不能三个都停在同一个 base 上。
        step_target = max(target, prev + 0.08)
        out[key] = lift_to_contrast(base, bg, step_target, light)
        prev = contrast(out[key], bg)
    muted = explicit.get("muted") or p["ansi"][8]
    muted = str(muted).lstrip("#")
    if contrast(muted, bg) < CONTRAST_DIM - 1e-9:
        muted = lift_to_contrast(muted, bg, CONTRAST_DIM, light)
    out["muted"] = muted
    return out


def surface_set(p: dict) -> dict:
    """返回完整的语义表面：diff + error/warn/success/info（含文字色）。

    色板可以在 `surfaces` 里显式覆盖任意一项；没写的按 ANSI 色相解算。
    """
    explicit = p.get("surfaces") or {}
    bg, fg = p["bg"], p["fg"]
    plus, minus = diff_surfaces(p)
    out = {
        "diff_add": str(explicit.get("diff_add", plus)).lstrip("#"),
        "diff_add_emph": str(explicit.get(
            "diff_add_emph", mix(p["ansi"][2], bg, 0.30))).lstrip("#"),
        "diff_delete": str(explicit.get("diff_delete", minus)).lstrip("#"),
        "diff_delete_emph": str(explicit.get(
            "diff_delete_emph", mix(p["ansi"][1], bg, 0.22))).lstrip("#"),
    }
    for key, spec in SURFACE_SPECS.items():
        bg_key, fg_key = f"{key}_bg", f"{key}_fg"
        surf = explicit.get(bg_key)
        surf = str(surf).lstrip("#") if surf else solve_surface(
            bg, fg, p["ansi"][spec["slot"]], spec["min_bg"])
        text = explicit.get(fg_key)
        if text:
            text = str(text).lstrip("#")
        else:
            text = fg if contrast(fg, surf) >= 4.5 else (
                bg if contrast(bg, surf) >= 4.5 else fg)
        out[bg_key] = surf
        out[fg_key] = text
    return out


def fix_cvd_pair(red: str, green: str, bg: str, floor: float,
                 target: float = TARGET_CVD_DELTA) -> str:
    """在保住色相/彩度的前提下推绿色明度，让红绿在色盲模拟下拉开。

    不动红色：错误色通常比成功色更敏感，改绿的成功色代价更小。
    """
    if cvd_delta(red, green) >= target:
        return green
    L, A, B = srgb_to_oklab(green)
    for i in range(1, 41):
        for sign in (1, -1):
            l = L + sign * i * 0.002
            if not 0.02 < l < 0.995:
                continue
            cand = oklab_to_srgb(l, A, B)
            if contrast(cand, bg) < floor - 1e-9:
                continue
            if cvd_delta(red, cand) >= target:
                return cand
    # 明度走不通时，给色相一个很小的预算（≤10°），往青/品红方向让一点
    C = (A * A + B * B) ** 0.5
    h = math.atan2(B, A)
    for deg in range(2, 11, 2):
        for sign in (1, -1):
            hh = h + sign * math.radians(deg)
            cand = oklab_to_srgb(L, C * math.cos(hh), C * math.sin(hh))
            if contrast(cand, bg) < floor - 1e-9:
                continue
            if cvd_delta(red, cand) >= target:
                return cand
    return green


def fix_cvd_palette(p: dict) -> tuple[dict, list[dict]]:
    """只修普通/亮绿两个槽，记录一条汇总变更。"""
    out = dict(p)
    ansi = list(p["ansi"])
    bg = p["bg"]
    changes = []
    for n, b in ((1, 2), (9, 10)):
        floor = CONTRAST_BODY if n < 8 else CONTRAST_BRIGHT
        fixed = fix_cvd_pair(ansi[n], ansi[b], bg, floor)
        if fixed != ansi[b]:
            changes.append({"slot": "cvd", "old": ansi[b], "new": fixed,
                            "why": f"{SLOT_NAMES[b]} red/green {cvd_delta(ansi[n], ansi[b]):.3f}"})
            ansi[b] = fixed
    if changes:
        sep = separate(ansi[2], ansi[10], bg)
        # separate 只允许在不破坏色盲分离的前提下生效
        if cvd_delta(ansi[9], sep) >= cvd_delta(ansi[9], ansi[10]):
            ansi[10] = sep
    out["ansi"] = ansi
    return out, changes


def boost_chroma(color: str, factor: float) -> str:
    """放大 OKLab 的 A/B，保留 L 与色相；越界时由 oklab_to_srgb 回缩彩度。"""
    if factor == 1.0:
        return color
    L, A, B = srgb_to_oklab(color)
    if (A * A + B * B) ** 0.5 < 1e-4:
        return color
    return oklab_to_srgb(L, A * factor, B * factor)


def vivid_palette(name: str, p: dict, factor: float) -> tuple[dict, list[dict]]:
    """提彩度：只动 1–6 / 9–14 的彩度，色相与明度不变；再复查对比度与明暗分档。"""
    if factor == 1.0:
        return p, []
    out = dict(p)
    light = bool(p.get("light"))
    bg = p["bg"]
    ansi = list(p["ansi"])
    for i in list(range(1, 7)) + list(range(9, 15)):
        new = boost_chroma(ansi[i], factor)
        floor = CONTRAST_BODY if i < 8 else CONTRAST_BRIGHT
        if contrast(new, bg) < floor - 1e-9:
            new = lift_to_contrast(new, bg, floor, light)
        ansi[i] = new
    for i in range(8):
        j = i + 8
        ansi[j] = separate(ansi[i], ansi[j], bg)
    out["ansi"] = ansi
    return out, [{"slot": "vivid", "old": "1.00", "new": f"{factor:.2f}",
                  "why": "chroma boost"}]


# ---- 归一化 ---------------------------------------------------
def normalize_palette(name: str, p: dict) -> tuple[dict, list[dict]]:
    """返回 (新色板, 改动列表)。不改原字典，方便调用方对比。"""
    light = bool(p.get("light"))
    bg = p["bg"]
    out = dict(p)
    ansi = list(p["ansi"])
    changes: list[dict] = []

    def note(i: int, old: str, new: str, why: str) -> None:
        changes.append({"slot": SLOT_NAMES[i], "old": old, "new": new, "why": why})

    def note_named(label: str, old: str, new: str, why: str) -> None:
        changes.append({"slot": label, "old": old, "new": new, "why": why})

    # 1) 对比度地板（正文 / 强调 / 暗字）
    for i in list(range(1, 7)) + [8] + list(range(9, 15)):
        floor = CONTRAST_BODY if i < 8 else (CONTRAST_DIM if i == 8 else CONTRAST_BRIGHT)
        if contrast(ansi[i], bg) < floor - 1e-9:
            fixed = lift_to_contrast(ansi[i], bg, floor, light)
            if fixed != ansi[i]:
                note(i, ansi[i], fixed, f"contrast {contrast(ansi[i], bg):.2f} < {floor}")
                ansi[i] = fixed

    # 2) 明暗分档（放在地板之后：先保证能读，再保证有层次）
    for i in range(8):
        j = i + 8
        fixed = separate(ansi[i], ansi[j], bg)
        if fixed != ansi[j]:
            note(j, ansi[j], fixed,
                 f"ΔE {delta_e(ansi[i], ansi[j]):.3f} < {MIN_DELTA_E}")
            ansi[j] = fixed

    # 3) 亮底中性槽：ANSI 7 不能是“白”，ANSI 15 不能和 0 同色
    #    亮底上 ANSI 7 = 背景色，等于把一个色槽挖空；很多 TUI 把 7 当“白”前景。
    if light:
        if contrast(ansi[7], bg) < CONTRAST_LIGHT_WHITE - 1e-9:
            fixed = lift_to_contrast(ansi[7], bg, CONTRAST_LIGHT_WHITE, True)
            if fixed != ansi[7]:
                note(7, ansi[7], fixed,
                     f"contrast {contrast(ansi[7], bg):.2f} < {CONTRAST_LIGHT_WHITE}")
                ansi[7] = fixed
        if delta_e(ansi[0], ansi[15]) < MIN_NEUTRAL_DELTA_E - 1e-9:
            fixed = mix(ansi[0], ansi[7], 0.35)
            if delta_e(ansi[0], fixed) < MIN_NEUTRAL_DELTA_E:
                fixed = mix(ansi[0], ansi[7], 0.5)
            note(15, ansi[15], fixed,
                 f"ANSI 15 = ANSI 0 (ΔE {delta_e(ansi[0], ansi[15]):.3f})")
            ansi[15] = fixed

    # 4) 选区：选中底对背景要看得出来，选中文字对选中底仍要能读
    sel = out.get("selbg")
    if sel:
        floor = CONTRAST_SELECTION_LIGHT if light else CONTRAST_SELECTION_DARK
        fixed = lift_to_contrast(sel, bg, floor, light)
        if fixed != sel:
            note_named("selection", sel, fixed,
                       f"contrast {contrast(sel, bg):.2f} < {floor}")
            out["selbg"] = fixed
        selfg = out.get("selfg")
        if selfg and contrast(selfg, fixed) < CONTRAST_SELECTION_TEXT - 1e-9:
            fixed_text = lift_to_contrast(
                selfg, fixed, CONTRAST_SELECTION_TEXT,
                srgb_to_oklab(fixed)[0] > 0.5)
            if fixed_text != selfg:
                note_named("selection-text", selfg, fixed_text,
                           f"contrast {contrast(selfg, fixed):.2f} < {CONTRAST_SELECTION_TEXT}")
                out["selfg"] = fixed_text

    # 5) 光标：竖条对背景的 3:1 底线
    cur = out.get("cursor")
    if cur and contrast(cur, bg) < CONTRAST_CURSOR - 1e-9:
        fixed = lift_to_contrast(cur, bg, CONTRAST_CURSOR, light)
        if fixed != cur:
            note_named("cursor", cur, fixed,
                       f"contrast {contrast(cur, bg):.2f} < {CONTRAST_CURSOR}")
            out["cursor"] = fixed

    # 6) 搜索命中：显式给了 matchbg 的色板也重新解一次，避免旧配方留下低对比
    old_match = out.get("matchbg")
    if old_match:
        fixed = solve_match(bg, p["fg"], old_match)
        if fixed != old_match:
            note_named("match", old_match, fixed,
                       f"bg {contrast(old_match, bg):.2f} / fg {contrast(p['fg'], old_match):.2f}")
            out["matchbg"] = fixed

    # 7) SGR 2 暗字：有效对比不够就抬高 alpha
    old_alpha = float(out.get("faint_text_alpha", 0.55))
    alpha = old_alpha
    while alpha < 0.90 and contrast(blend(p["fg"], bg, alpha), bg) < CONTRAST_FAINT - 1e-9:
        alpha = round(alpha + 0.05, 2)
    if alpha != old_alpha:
        note_named("faint", str(old_alpha), str(alpha),
                   f"effective contrast {contrast(blend(p['fg'], bg, old_alpha), bg):.2f} < {CONTRAST_FAINT}")
        out["faint_text_alpha"] = alpha

    out["ansi"] = ansi
    return out, changes


# ---- 审计 -----------------------------------------------------
def evaluate(name: str, p: dict) -> dict:
    """对一份色板（或生成后的 profile 字典）出体检结果。"""
    light = bool(p.get("light"))
    bg = p["bg"]
    fg = p["fg"]
    ansi = p["ansi"]
    dups, low, issues = [], [], []

    for i in range(8):
        pair_de = delta_e(ansi[i], ansi[i + 8])
        if pair_de < MIN_DELTA_E - 1e-9:
            dups.append({"slot": SLOT_NAMES[i], "delta_e": round(pair_de, 3)})

    for i in list(range(1, 7)) + [8] + list(range(9, 15)):
        floor = CONTRAST_BODY if i < 8 else (CONTRAST_DIM if i == 8 else CONTRAST_BRIGHT)
        ratio = contrast(ansi[i], bg)
        if ratio < floor - 1e-9:
            low.append({"slot": SLOT_NAMES[i], "ratio": round(ratio, 2), "floor": floor})

    # ---- 选区 / 搜索 / 光标 / 亮底中性槽 / 暗字 ----
    sel = p.get("selbg")
    selfg = p.get("selfg")
    sel_floor = CONTRAST_SELECTION_LIGHT if light else CONTRAST_SELECTION_DARK
    sel_ratio = contrast(sel, bg) if sel else None
    if sel_ratio is not None and sel_ratio < sel_floor - 1e-9:
        issues.append(f"selection {sel_ratio:.2f} < {sel_floor}")
    sel_text_ratio = contrast(selfg, sel) if (sel and selfg) else None
    if sel_text_ratio is not None and sel_text_ratio < CONTRAST_SELECTION_TEXT - 1e-9:
        issues.append(f"selected text {sel_text_ratio:.2f} < {CONTRAST_SELECTION_TEXT}")

    match = p.get("matchbg")
    match_bg_ratio = contrast(match, bg) if match else None
    match_fg_ratio = contrast(fg, match) if match else None
    if match_bg_ratio is not None and match_bg_ratio < CONTRAST_MATCH_BG - 1e-9:
        issues.append(f"match/bg {match_bg_ratio:.2f} < {CONTRAST_MATCH_BG}")
    if match_fg_ratio is not None and match_fg_ratio < CONTRAST_MATCH_FG - 1e-9:
        issues.append(f"match/fg {match_fg_ratio:.2f} < {CONTRAST_MATCH_FG}")

    cursor = p.get("cursor")
    cursor_ratio = contrast(cursor, bg) if cursor else None
    if cursor_ratio is not None and cursor_ratio < CONTRAST_CURSOR - 1e-9:
        issues.append(f"cursor {cursor_ratio:.2f} < {CONTRAST_CURSOR}")
    cursor_text_ratio = None
    if cursor:
        cursor_text_ratio = max(contrast(fg, cursor), contrast(bg, cursor))
        if cursor_text_ratio < CONTRAST_BODY - 1e-9:
            issues.append(f"cursor text {cursor_text_ratio:.2f} < {CONTRAST_BODY}")

    white_ratio = None
    neutral_delta = None
    if light:
        white_ratio = contrast(ansi[7], bg)
        if white_ratio < CONTRAST_LIGHT_WHITE - 1e-9:
            issues.append(f"ansi7 {white_ratio:.2f} < {CONTRAST_LIGHT_WHITE}")
        neutral_delta = delta_e(ansi[0], ansi[15])
        if neutral_delta < MIN_NEUTRAL_DELTA_E - 1e-9:
            issues.append(f"ansi0=ansi15 ΔE {neutral_delta:.3f}")

    faint_alpha = float(p.get("faint_text_alpha", 0.55))
    faint_ratio = contrast(blend(fg, bg, faint_alpha), bg)
    if faint_ratio < CONTRAST_FAINT - 1e-9:
        issues.append(f"faint {faint_ratio:.2f} < {CONTRAST_FAINT}")

    # diff 新增/删除底：色相差之外还要有明度差，灰度/色盲下才分得开
    plus, minus = diff_surfaces(p)
    diff_l = abs(srgb_to_oklab(plus)[0] - srgb_to_oklab(minus)[0])
    diff_cvd = cvd_delta(plus, minus)
    if diff_l < MIN_DIFF_DELTA_L - 1e-9:
        issues.append(f"diff ΔL {diff_l:.3f} < {MIN_DIFF_DELTA_L}")

    # 语义表面：error/warn/success/info 的文字对比、可见度、层级与色盲分离
    surf = surface_set(p)
    surf_metrics = {}
    for key in ("error", "warn", "success", "info"):
        sb, sf = surf[f"{key}_bg"], surf[f"{key}_fg"]
        tc, bc = contrast(sf, sb), contrast(sb, bg)
        surf_metrics[key] = {"text": round(tc, 2), "bg": round(bc, 2)}
        if tc < CONTRAST_BODY - 1e-9:
            issues.append(f"{key} text {tc:.2f} < {CONTRAST_BODY}")
        if bc < 1.2 - 1e-9:
            issues.append(f"{key} surface {bc:.2f} < 1.2")
    err_succ_dl = abs(srgb_to_oklab(surf["error_bg"])[0]
                      - srgb_to_oklab(surf["success_bg"])[0])
    err_succ_cvd = cvd_delta(surf["error_bg"], surf["success_bg"])
    if err_succ_dl < 0.04 - 1e-9:
        issues.append(f"error/success ΔL {err_succ_dl:.3f} < 0.04")
    if err_succ_cvd < MIN_CVD_DELTA - 1e-9:
        issues.append(f"error/success cvd {err_succ_cvd:.3f} < {MIN_CVD_DELTA}")
    order = [contrast(surf[f"{k}_bg"], bg) for k in ("error", "warn", "success", "info")]
    order_ok = all(order[i] > order[i + 1] - 1e-9 for i in range(3))
    if not order_ok:
        issues.append("surface order error>warn>success>info broken")

    # 中性梯：surface / overlay / border 必须单调且可见，muted 仍是文字档
    neu = neutral_ramp(p)
    neu_ratios = {k: contrast(neu[k], bg) for k in ("surface", "overlay", "border")}
    neu_floor = {"surface": 1.10, "overlay": 1.20, "border": 1.30}
    for k, floor in neu_floor.items():
        if neu_ratios[k] < floor - 1e-9:
            issues.append(f"neutral {k} {neu_ratios[k]:.2f} < {floor}")
    neu_order = (neu_ratios["surface"] < neu_ratios["overlay"] < neu_ratios["border"])
    if not neu_order:
        issues.append("neutral order surface<overlay<border broken")
    if delta_e(neu["surface"], neu["overlay"]) < 0.012 - 1e-9:
        issues.append("neutral surface/overlay too close")
    if delta_e(neu["overlay"], neu["border"]) < 0.012 - 1e-9:
        issues.append("neutral overlay/border too close")
    if contrast(fg, neu["surface"]) < CONTRAST_BODY - 1e-9:
        issues.append(f"neutral fg/surface {contrast(fg, neu['surface']):.2f} < {CONTRAST_BODY}")
    if contrast(neu["muted"], bg) < CONTRAST_DIM - 1e-9:
        issues.append(f"neutral muted {contrast(neu['muted'], bg):.2f} < {CONTRAST_DIM}")

    # 红绿在 deuteranopia / protanopia 下的最差分离度
    cvd_normal = cvd_delta(ansi[1], ansi[2])
    cvd_bright = cvd_delta(ansi[9], ansi[10])
    cvd_min = min(cvd_normal, cvd_bright)
    if cvd_min < MIN_CVD_DELTA - 1e-9:
        issues.append(f"cvd {cvd_min:.3f} < {MIN_CVD_DELTA}")

    # 语法角色层：每个角色对背景的地板，以及关键字/函数/类型/字符串/数字的分离度
    syntax = p.get("syntax") or {}
    syn_ratios = {}
    syntax_sep = None
    syntax_surface = {"min": None, "role": None, "surface": None, "ok": True}
    if syntax:
        def _syn_color(item):
            if isinstance(item, (tuple, list)):
                return str(item[0]).lstrip("#")
            if isinstance(item, dict):
                return str(item.get("color", "")).lstrip("#")
            return str(item).lstrip("#")

        for role, item in syntax.items():
            color = _syn_color(item)
            if not color:
                continue
            floor = 3.0 if role in ("comment", "link") else 4.5
            ratio = contrast(color, bg)
            syn_ratios[role] = round(ratio, 2)
            if ratio < floor - 1e-9:
                issues.append(f"syntax {role} {ratio:.2f} < {floor}")
        keys = [k for k in ("keyword", "function", "type", "string", "number", "operator")
                if k in syntax]
        pairs = []
        for i, ka in enumerate(keys):
            for kb in keys[i + 1:]:
                pairs.append(delta_e(_syn_color(syntax[ka]), _syn_color(syntax[kb])))
        if pairs:
            syntax_sep = min(pairs)
            if syntax_sep < 0.03 - 1e-9:
                issues.append(f"syntax sep {syntax_sep:.3f} < 0.03")

        # 语法 × 表面：diff / error / warn / success / info 底上仍要能读。
        # 与上面的「对 bg」是两回事；只报全局最差的一对，避免 detail 刷屏。
        worst = None
        for role, item in syntax.items():
            if role == "comment":
                continue
            color = _syn_color(item)
            if not color:
                continue
            for key in SYNTAX_SURFACE_KEYS:
                ratio = contrast(color, surf[key])
                if worst is None or ratio < worst[0]:
                    worst = (ratio, role, key)
        if worst:
            ratio, role, key = worst
            syntax_surface = {
                "min": round(ratio, 2),
                "role": role,
                "surface": key,
                "ok": ratio >= CONTRAST_SYNTAX_SURFACE - 1e-9,
            }
            if not syntax_surface["ok"]:
                issues.append(f"syntax/surface {ratio:.2f} "
                              f"< {CONTRAST_SYNTAX_SURFACE} ({role} on {key})")

    # 色相区分度：报告项，不参与 ok/score —— 品牌色相是身份，不能为了数值硬拧
    hue_delta, hue_pair = min_hue_delta(ansi)
    hue_ok = hue_delta >= MIN_HUE_DELTA_E - 1e-9

    # CLI 差异渲染：ANSI 主题会把亮绿/亮红当背景，橙字/正文落上去的底线
    # 只报告，不 gate：亮槽本来就该亮，压暗会毁掉它们作为前景的强调作用。
    cli_pairs = ((fg, ansi[10]), (ansi[11], ansi[10]), (fg, ansi[9]), (ansi[11], ansi[9]))
    cli_ratios = [contrast(a, b) for a, b in cli_pairs]
    cli_min = min(cli_ratios)
    cli_worst = cli_pairs[cli_ratios.index(cli_min)]

    score = max(0, 100 - 4 * len(dups) - 6 * len(low) - 4 * len(issues))
    return {
        "name": name,
        "light": light,
        "fg_contrast": round(contrast(fg, bg), 2),
        "dim_contrast": round(contrast(ansi[8], bg), 2),
        "duplicates": dups,
        "low": low,
        "issues": issues,
        "selection": {"ratio": round(sel_ratio, 2) if sel_ratio is not None else None,
                      "text_ratio": round(sel_text_ratio, 2) if sel_text_ratio is not None else None},
        "match": {"bg_ratio": round(match_bg_ratio, 2) if match_bg_ratio is not None else None,
                  "fg_ratio": round(match_fg_ratio, 2) if match_fg_ratio is not None else None},
        "cursor": round(cursor_ratio, 2) if cursor_ratio is not None else None,
        "cursor_text": round(cursor_text_ratio, 2) if cursor_text_ratio is not None else None,
        "white_ratio": round(white_ratio, 2) if white_ratio is not None else None,
        "neutral_delta": round(neutral_delta, 3) if neutral_delta is not None else None,
        "faint": round(faint_ratio, 2),
        "diff": {"plus": plus, "minus": minus,
                 "delta_l": round(diff_l, 3), "cvd": round(diff_cvd, 3),
                 "ok": diff_l >= MIN_DIFF_DELTA_L - 1e-9},
        "surfaces": {"roles": surf_metrics,
                     "error_success_delta_l": round(err_succ_dl, 3),
                     "error_success_cvd": round(err_succ_cvd, 3),
                     "order_ok": order_ok,
                     "min_text": min(x["text"] for x in surf_metrics.values())},
        "neutral": {"surface": round(neu_ratios["surface"], 2),
                    "overlay": round(neu_ratios["overlay"], 2),
                    "border": round(neu_ratios["border"], 2),
                    "muted": round(contrast(neu["muted"], bg), 2),
                    "fg_surface": round(contrast(fg, neu["surface"]), 2),
                    "ok": not any(x.startswith("neutral ") for x in issues)},
        "cvd": {"normal": round(cvd_normal, 3), "bright": round(cvd_bright, 3),
                "min": round(cvd_min, 3), "ok": cvd_min >= MIN_CVD_DELTA - 1e-9,
                "warn": cvd_min < TARGET_CVD_DELTA - 1e-9},
        "syntax": {"min_contrast": round(min(syn_ratios.values()), 2) if syn_ratios else None,
                   "sep": round(syntax_sep, 3) if syntax_sep is not None else None,
                   "ok": not any(x.startswith("syntax ") for x in issues),
                   "roles": len(syn_ratios)},
        "syntax_surface": syntax_surface,
        "hue_delta": round(hue_delta, 3),
        "hue_pair": f"{SLOT_NAMES[hue_pair[0]]}-{SLOT_NAMES[hue_pair[1]]}",
        "hue_ok": hue_ok,
        "cli_diff": round(cli_min, 2),
        "cli_diff_pair": f"{cli_worst[0]} on {cli_worst[1]}",
        "cli_diff_ok": cli_min >= 3.0 - 1e-9,
        "score": score,
        "ok": not dups and not low and not issues,
    }
