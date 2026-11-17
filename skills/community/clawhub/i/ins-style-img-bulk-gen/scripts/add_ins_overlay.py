from PIL import Image, ImageDraw, ImageFont, ImageFilter


# ============================ 排版常量 ============================

# ins 模式（灰蒙版 + 图文）字号比例，相对图片高度
INS_TITLE_RATIO = 0.035
INS_BODY_RATIO = 0.020  # 2026-09-20 内页正文缩到标题 57%，提高对比

# cover 模式（无蒙版、大字标题）字号比例。
# COVER_TITLE_RATIO = 普通标题的 2 倍；FLOOR 是下限保护 = 普通标题的 1.2 倍，
# 长标题缩到下限仍放不下时接受轻微溢出，也不把字缩到看不清。
COVER_TITLE_RATIO = 0.07  # 2026-09-20 封面 spec：字号回退到比最初还小一点
COVER_TITLE_FLOOR_RATIO = 0.05  # 2026-09-20 下限
COVER_MAX_LINE_W_RATIO = 0.90   # 无蒙版边框约束，可比 ins 的 0.76 更满
COVER_MAX_BLOCK_H_RATIO = 0.70
COVER_MAX_LINES = 4             # 自动切行的上限；手动 \n 不受此限制
# 多断一行必须换来 ≥10% 的字号增益才值得，避免 10 字标题为 3% 增益被拆成两行
COVER_SPLIT_GAIN_MIN = 1.10
# 以下三项均相对字号
COVER_STROKE_RATIO = 0.07
COVER_LINE_GAP_RATIO = 0.18  # 2026-09-20 行距收紧，更紧凑
COVER_SHADOW_RATIO = 0.06
COVER_SHADOW_BLUR_RATIO = 0.05

# 禁则用标点表
_OPENING_PUNCT = "（「《【〈〔［｛“‘([{<"
_CLOSING_PUNCT = "，。！？、；：）」》】〉〕］｝”’.,!?;:)]}>"
# 属于「同一个词」的 ASCII 符号，断行时不能从其内部切开（40+ / 3.5 / A/B）
_ASCII_WORD_EXTRA = "+-.%$#@&/_'~°"


# ============================ 字体候选表 ============================

# 说明：Arial Unicode MS 是关键兜底（macOS + Windows 均预装，覆盖几乎所有 Unicode
# 包括 ❤ ★ ♡ → 和完整 CJK；这是少数能正确渲染 ❤ 实心心形的字体）。

# 标题字体优先级（粗体）：Hiragino Sans GB W6 → Microsoft YaHei Bold → Source Han Sans CN Bold → SimHei → Arial Unicode
TITLE_FONT_CANDIDATES = [
    # macOS — Hiragino Sans GB W6 / W3（冬青黑体，CJK 字体优先）
    ("/System/Library/Fonts/Hiragino Sans GB.ttc", 1),
    ("/System/Library/Fonts/Hiragino Sans GB.ttc", 0),
    # Windows — Microsoft YaHei Bold（msyhbd.ttc）
    ("C:\\Windows\\Fonts\\msyhbd.ttc", 0),
    # Linux — Source Han Sans CN Bold / Noto Sans CJK Bold
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/source-han-sans/SourceHanSansSC-Bold.otf",
    # Windows — SimHei
    "C:\\Windows\\Fonts\\simhei.ttf",
    "SimHei.ttf",
    # macOS / Windows — Arial Unicode MS（完整 Unicode 兜底，含 ❤ 真字形）
    "/Library/Fonts/Arial Unicode.ttf",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "C:\\Windows\\Fonts\\Arialuni.ttf",
    "Arialuni.ttf",
    # Linux — 文泉驿微米黑
    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
]

# 正文字体优先级：Hiragino Sans GB W3 → Source Han Serif CN → LXGW WenKai → Arial → SimHei → Source Han Sans Regular → Arial Unicode
BODY_FONT_CANDIDATES = [
    # macOS — Hiragino Sans GB W3
    ("/System/Library/Fonts/Hiragino Sans GB.ttc", 0),
    # Linux — Source Han Serif CN
    "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc",
    "/usr/share/fonts/source-han-serif/SourceHanSerifSC-Regular.otf",
    # Linux — LXGW WenKai（霞鹜文楷）
    "/usr/share/fonts/truetype/lxgw-wenkai/LXGWWenKai-Regular.ttf",
    "/usr/share/fonts/lxgw-wenkai/LXGWWenKai-Regular.ttf",
    # Windows — SimSun（宋体）
    "C:\\Windows\\Fonts\\simsun.ttc",
    "SimSun.ttf",
    # Windows — Microsoft YaHei Regular（msyh.ttc）
    ("C:\\Windows\\Fonts\\msyh.ttc", 0),
    # 通用 — Source Han Sans CN Regular（Noto Sans CJK Regular）
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    # 跨平台 — Arial Unicode MS（兜底：含 ❤ 真字形 + 完整 CJK + 拉丁）
    "/Library/Fonts/Arial Unicode.ttf",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "C:\\Windows\\Fonts\\Arialuni.ttf",
    "Arialuni.ttf",
    # 跨平台 — Arial / Helvetica
    "Arial.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
]

# Symbol 字体（CJK 字体常缺 ❤ ★ ♡ → 等符号；Arial Unicode 已含但保留作 per-glyph fallback）
SYMBOL_FONT_CANDIDATES = [
    # macOS / Windows — Arial Unicode MS（首选，含 ❤ 真字形）
    "/Library/Fonts/Arial Unicode.ttf",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "C:\\Windows\\Fonts\\Arialuni.ttf",
    "Arialuni.ttf",
    # macOS — Apple Symbols
    ("/System/Library/Fonts/Apple Symbols.ttf", 0),
    # macOS — CJKSymbolsFallback
    ("/System/Library/Fonts/CJKSymbolsFallback.ttc", 0),
    # Windows — Segoe UI Symbol
    "C:\\Windows\\Fonts\\seguisym.ttf",
    # Linux — Noto Sans Symbols / Noto Sans Symbols 2
    "/usr/share/fonts/truetype/noto/NotoSansSymbols-Regular.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansSymbols-Regular.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansSymbols2-Regular.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansSymbols2-Regular.ttf",
]


# ============================ 字符分类 / 字体加载 ============================

def is_cjk_or_ascii_text(ch):
    """判定一个字符是否属于 CJK/ASCII 文本字符（CJK 字体通常覆盖）。

    装饰符号（❤ ★ ♡ → ◆ ✓ 等 Unicode 符号区段）不在此列，走 symbol_font 路径。
    公开为模块级函数以便单测。
    """
    if not ch:
        return False
    cp = ord(ch)
    # 拉丁 ASCII + Latin-1 补充
    if cp < 0x250:
        return True
    # CJK 统一汉字
    if 0x4E00 <= cp <= 0x9FFF:
        return True
    if 0x3400 <= cp <= 0x4DBF:  # CJK 扩展 A
        return True
    if 0xF900 <= cp <= 0xFAFF:  # CJK 兼容
        return True
    # 全角 ASCII / 半角假名 / 全角假名 / 标点
    if 0xFF00 <= cp <= 0xFFEF:
        return True
    if 0x3000 <= cp <= 0x303F:  # CJK 标点
        return True
    # 数字 0-9 / 英文 a-z A-Z
    if 0x30 <= cp <= 0x39 or 0x41 <= cp <= 0x5A or 0x61 <= cp <= 0x7A:
        return True
    return False


def pick_font_for_char(ch, main_font, sym_font):
    """根据字符类型选字体：CJK/ASCII 走主字体，装饰符号走 symbol_font。

    公开为模块级函数以便单测。这是避免 tofu 渲染的关键路由逻辑。
    """
    if is_cjk_or_ascii_text(ch):
        return main_font
    return sym_font if sym_font is not None else main_font


def load_font(font_list, size):
    """按优先级加载第一个可用字体。tuple 表示 (path, index)。"""
    for entry in font_list:
        try:
            if isinstance(entry, tuple):
                path, idx = entry
                return ImageFont.truetype(path, size, index=idx)
            return ImageFont.truetype(entry, size, index=0)
        except (IOError, OSError):
            continue
    return None


def title_font_candidates(title_font_path=None, font_path=None):
    """标题字体候选：显式覆盖 > 旧 font_path 参数 > 默认优先级表。"""
    return (
        ([title_font_path] if title_font_path else [])
        + ([font_path] if font_path else [])
        + TITLE_FONT_CANDIDATES
    )


def body_font_candidates(body_font_path=None, font_path=None):
    """正文字体候选：显式覆盖 > 旧 font_path 参数 > 默认优先级表。"""
    return (
        ([body_font_path] if body_font_path else [])
        + ([font_path] if font_path else [])
        + BODY_FONT_CANDIDATES
    )


def symbol_font_candidates(symbol_font_path=None):
    return ([symbol_font_path] if symbol_font_path else []) + SYMBOL_FONT_CANDIDATES


# CJK 健全性阈值：实测（40px）真正能渲染中文的字体比值 ≥1.33（Hiragino 1.333、
# Songti 1.443、Arial Unicode 1.499），渲染成 tofu 方框的字体 ≈0.95（Helvetica）。
# 取 1.2 留出余量。注意不能取 1.5 —— 那会把所有中文字体全部拒掉。
CJK_WIDTH_RATIO_MIN = 1.2


def _cjk_width_ok(font_obj):
    """CJK 健全性检查：检测字体无法渲染中文（会出 tofu 方框）。

    中文字形是全角（1em），"AA" 通常不足 1.5em，故真中文字体的
    textlength("中文") / textlength("AA") 明显大于 1；tofu 方框则接近 1。
    """
    if font_obj is None:
        return False
    try:
        dummy = ImageDraw.Draw(Image.new("RGB", (1, 1)))
        w_cn = dummy.textlength("中文", font=font_obj)
        w_ascii = dummy.textlength("AA", font=font_obj)
        if w_ascii <= 0:
            return False
        return w_cn >= w_ascii * CJK_WIDTH_RATIO_MIN
    except Exception:
        return False


def load_cjk_font(font_list, size):
    """加载字体，并跳过无法渲染中文的候选（避免 tofu）。

    用户显式传入 --title-font 时可能给到纯英文字体；此时宁可退到候选表里
    真正能渲染中文的字体，也不要输出一排方框。所有候选都过不了检查时，
    退回第一个能加载的字体（尽力而为，至少不崩）。
    """
    fallback = None
    for entry in font_list:
        font = load_font([entry], size)
        if font is None:
            continue
        if fallback is None:
            fallback = font
        if _cjk_width_ok(font):
            return font
    return fallback


def measure_line_width(draw, line, font, symbol_font, stroke_width=0):
    """按显示宽度测量一行文字（逐字符分流字体，与绘制逻辑一致）。

    Pillow 不做跨字体回退，所以 ❤ 等符号在 CJK 字体里是 tofu —— 必须按字符
    分别测量，否则宽度会与实际绘制不符。
    """
    if not line or font is None:
        return 0
    total = 0.0
    for ch in line:
        total += draw.textlength(
            ch, font=pick_font_for_char(ch, font, symbol_font)
        )
    return total + stroke_width * 2


def _text_bbox(draw, xy, text, font, stroke_width=0):
    """textbbox 的 stroke 兼容包装（stroke_width 参数需要 Pillow 8.0+）。"""
    try:
        return draw.textbbox(xy, text, font=font, stroke_width=stroke_width)
    except TypeError:
        return draw.textbbox(xy, text, font=font)


# ============================ 禁则 / 自动切行 ============================

def is_ascii_word_char(ch):
    """是否属于「不能从中间切断」的 ASCII 词内字符（40+ / 3.5 / A/B）。"""
    return ch.isascii() and (ch.isalnum() or ch in _ASCII_WORD_EXTRA)


def is_valid_break(text, i):
    """在 i 处断行（text[:i] / text[i:]）是否合法。

    确定性禁则，不猜语义：
      - 闭标点不能落到行首（"你好，" / "世界" ❌）
      - 开标点不能留在行尾（"你好（" / "世界）" ❌）
      - ASCII 词内不能切断（"40" / "+后才明白" ❌）
    语义层面的句子切分由 agent 通过 \\n 提供，不在这里猜。
    """
    if i <= 0 or i >= len(text):
        return False
    prev_ch, next_ch = text[i - 1], text[i]
    if next_ch in _CLOSING_PUNCT:
        return False
    if prev_ch in _OPENING_PUNCT:
        return False
    # 空格是天然的断点（英文标题）；不留到下一行行首
    if prev_ch == " " or next_ch == " ":
        return True
    if is_ascii_word_char(prev_ch) and is_ascii_word_char(next_ch):
        return False
    return True


def _balanced_split(text, n_lines, unit_widths):
    """把 text 均衡切成 n_lines 行，最小化「最大行宽」；遵守禁则。

    经典 minimax 折行 DP：枚举所有合法断点，取最大行宽最小的方案。
    只按显示宽度均衡 —— 语义断点由调用方的 \\n 决定。
    unit_widths[i] = 第 i 个字符的显示宽度。
    Returns: list[str]，切不出合法方案时返回 None。
    """
    L = len(text)
    if n_lines <= 1:
        return [text]
    if n_lines > L:
        return None
    prefix = [0.0]
    for w in unit_widths:
        prefix.append(prefix[-1] + w)
    allowed = {i for i in range(1, L) if is_valid_break(text, i)}
    if len(allowed) < n_lines - 1:
        return None

    # dp[k][end] = (该 k 行方案下的最小「最大行宽」, 上一行结束位置)
    dp = [dict() for _ in range(n_lines + 1)]
    dp[0][0] = (0.0, None)
    for k in range(1, n_lines + 1):
        for prev in dp[k - 1]:
            for end in range(prev + 1, L + 1):
                if k < n_lines and end not in allowed:
                    continue
                width = prefix[end] - prefix[prev]
                cost = max(dp[k - 1][prev][0], width)
                cur = dp[k].get(end)
                if cur is None or cost < cur[0]:
                    dp[k][end] = (cost, prev)
    if L not in dp[n_lines]:
        return None

    lines = []
    end = L
    for k in range(n_lines, 0, -1):
        prev = dp[k][end][1]
        lines.append(text[prev:end])
        end = prev
    return list(reversed(lines))


def _fit_cover_font_size(lines, base_size, max_line_w, max_block_h,
                         title_font_path=None, symbol_font_path=None):
    """求这些行在版心内能用的最大字号（未做下限保护，即 ideal size）。

    文字像素宽度对字号近似线性，故可闭式求解：
        width(s) = width(base) * s / base  ≤  max_line_w
    """
    draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    font = load_font(title_font_candidates(title_font_path), base_size)
    sym_font = load_font(symbol_font_candidates(symbol_font_path), base_size)
    if font is None:
        return base_size

    base_w = max(
        (measure_line_width(draw, ln, font, sym_font) for ln in lines),
        default=0,
    )
    if base_w <= 0:
        return base_size
    size = min(base_size, int(base_size * max_line_w / base_w))

    # 高度约束：block_h ≈ n * 行高(1.4×字号) + (n-1) * 行距(0.2×字号)
    n = len(lines)
    factor = 1.4 * n + COVER_LINE_GAP_RATIO * (n - 1)
    if factor > 0:
        size = min(size, int(max_block_h / factor))
    return max(size, 1)


def plan_cover_layout(title, img_w, img_h, title_font_path=None,
                      symbol_font_path=None):
    """规划 cover 标题排版：断行 + 字号 + 描边。

    断行策略：**手动 \\n 优先**（语义断点由 agent 负责），没有 \\n 时按显示宽度
    均衡切 N 行（N = 1..COVER_MAX_LINES），只保证禁则不出错。

    选行原则：字号越大越好；但多断一行必须换来 ≥ COVER_SPLIT_GAIN_MIN 的增益，
    否则不值得（避免为了 3% 的字号把 10 字标题拆成两行）。

    Returns dict: font_size / lines / stroke_width / line_gap / block_h
    """
    base_size = max(1, int(img_h * COVER_TITLE_RATIO))
    floor_size = max(1, int(img_h * COVER_TITLE_FLOOR_RATIO))
    max_line_w = max(1, int(img_w * COVER_MAX_LINE_W_RATIO))
    max_block_h = max(1, int(img_h * COVER_MAX_BLOCK_H_RATIO))

    draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))

    manual_lines = title.split("\n")
    if len(manual_lines) > 1:
        # agent 已经给了语义断行，原样采用，不再重切
        candidates = [manual_lines]
    else:
        base_font = load_font(title_font_candidates(title_font_path), base_size)
        sym_font = load_font(symbol_font_candidates(symbol_font_path), base_size)
        if base_font is None:
            base_font = ImageFont.load_default()
        unit_widths = [
            draw.textlength(ch, font=pick_font_for_char(ch, base_font, sym_font))
            for ch in title
        ]
        candidates = []
        for n in range(1, COVER_MAX_LINES + 1):
            lines = _balanced_split(title, n, unit_widths)
            if lines:
                candidates.append(lines)
        if not candidates:
            candidates = [[title]]

    # 行数升序评估，理想字号
    scored = [
        (
            _fit_cover_font_size(
                lines, base_size, max_line_w, max_block_h,
                title_font_path, symbol_font_path,
            ),
            lines,
        )
        for lines in candidates
    ]

    best_size = max(size for size, _ in scored)
    threshold = best_size / COVER_SPLIT_GAIN_MIN
    chosen = next(
        ((size, lines) for size, lines in scored if size >= threshold),
        max(scored, key=lambda t: t[0]),
    )
    font_size, lines = chosen

    # 下限保护：长标题缩到下限仍放不下时接受轻微溢出，也不缩到看不清
    font_size = max(font_size, floor_size)
    stroke_width = max(2, int(font_size * COVER_STROKE_RATIO))

    # 实测校验：上面的闭式解按字符宽度线性缩放估算，取整与 hinting 会让实际
    # 宽度略有出入，且描边还要额外占 2×stroke。超出时按比例缩到刚好放得下。
    while font_size > floor_size:
        font = load_font(title_font_candidates(title_font_path), font_size)
        sym_font = load_font(symbol_font_candidates(symbol_font_path), font_size)
        stroke_width = max(2, int(font_size * COVER_STROKE_RATIO))
        if font is None:
            break
        widest = max(
            measure_line_width(draw, ln, font, sym_font) for ln in lines
        )
        avail = max_line_w - stroke_width * 2
        if widest <= avail or widest <= 0:
            break
        font_size = max(
            floor_size, min(font_size - 1, int(font_size * avail / widest))
        )

    # 居中排布所需的块高
    font = load_font(title_font_candidates(title_font_path), font_size)
    sym_font = load_font(symbol_font_candidates(symbol_font_path), font_size)
    line_gap = int(font_size * COVER_LINE_GAP_RATIO)
    heights = []
    for ln in lines:
        bb = _text_bbox(draw, (0, 0), ln, font, stroke_width)
        heights.append(bb[3] - bb[1])
    block_h = sum(heights) + line_gap * (len(lines) - 1)

    return {
        "font_size": font_size,
        "lines": lines,
        "stroke_width": stroke_width,
        "line_gap": line_gap,
        "block_h": block_h,
    }


# ============================ 留白分析（ins 模式 auto 定位） ============================

def find_blank_region(img, box_w, box_h, num_bands=8):
    """在图片中找最"留白"的矩形位置放置文字蒙版。

    智能评分（5 维）：
    1. blank_score    — 行内标准差越低 = 颜色越均匀 = 留白越多（最高权重）
    2. brightness     — 亮度适中（接近 180 的浅色背景），避免全黑/全白
    3. edge_alignment — band 处于图片边缘（上/下 1/4）时奖励，mask 边对齐图片边更稳
    4. neighborhood   — 相邻 band 也是留白时奖励，避免 mask 被 busy 边缘切断
    5. cross_block    — band 跨越 busy↔empty 边界时惩罚（说明它跨越了不同物体）

    同时做水平方向切片检查（如果 mask 比 image 窄很多）以避免占据 busy 的左/右半。

    Returns: (box_x, box_y) 左上角坐标
    """
    img_w, img_h = img.size
    box_w = min(box_w, img_w)
    box_h = min(box_h, img_h)

    # 转灰度计算
    gray = img.convert("L")
    pixels = list(gray.getdata())
    row_stdev = []
    row_mean = []
    for y in range(img_h):
        row = pixels[y * img_w:(y + 1) * img_w]
        if not row:
            row_stdev.append(255.0)
            row_mean.append(128)
            continue
        mean = sum(row) / len(row)
        var = sum((p - mean) ** 2 for p in row) / len(row)
        row_stdev.append(var ** 0.5)
        row_mean.append(mean)

    # 聚合到 num_bands 个水平条带
    band_h = max(int(img_h / num_bands), 1)
    bands = []
    for i in range(num_bands):
        y0 = i * band_h
        y1 = min(y0 + band_h, img_h)
        stdevs = row_stdev[y0:y1]
        means = row_mean[y0:y1]
        if not stdevs:
            continue
        bands.append({
            "y0": y0, "y1": y1,
            "avg_stdev": sum(stdevs) / len(stdevs),
            "avg_mean": sum(means) / len(means),
        })

    if not bands:
        box_x = (img_w - box_w) // 2
        box_y = max(0, min(int(img_h * 0.42), img_h - box_h))
        return box_x, box_y

    # 邻居索引函数（环形）
    def neighbor(i, offset):
        return bands[(i + offset) % len(bands)]

    # 算全局 stdev 范围用于归一化
    all_stdevs = [b["avg_stdev"] for b in bands]
    min_s, max_s = min(all_stdevs), max(all_stdevs)
    stdev_range = max(max_s - min_s, 1)

    best_score = float("-inf")
    best_band_idx = 0

    for i, b in enumerate(bands):
        # 1. blank_score：标准差越低越好，归一化到 [0, 100]
        norm_stdev = (b["avg_stdev"] - min_s) / stdev_range
        blank_score = (1.0 - norm_stdev) * 100  # 0=最忙, 100=最空

        # 2. brightness：亮度接近 180 的高光区最舒服（米色/奶油背景）
        #    太黑(<50)或太白(>230)都不利于白色文字阅读
        brightness_penalty = abs(b["avg_mean"] - 180) / 180.0  # 0=好, 1=差
        brightness_score = (1.0 - brightness_penalty) * 25

        # 3. edge_alignment：前 25% 或后 25% 的 band 边缘奖励
        #    （mask 上下边与图片上下边对齐，视觉稳定）
        rel_pos = i / max(len(bands) - 1, 1)  # 0=top, 1=bottom
        edge_dist = min(rel_pos, 1 - rel_pos)  # 0=edge, 0.5=center
        edge_score = max(0, 0.25 - edge_dist) * 80  # 0~20 分

        # 4. neighborhood：上下邻居 band 也是空白时奖励
        nb_blank = (neighbor(i, -1)["avg_stdev"] + neighbor(i, +1)["avg_stdev"]) / 2
        nb_norm = (nb_blank - min_s) / stdev_range
        neighborhood_score = (1.0 - nb_norm) * 15

        # 5. cross_block：如果 band 内行间标准差差异大（top 忙 bottom 空或反之），惩罚
        #    用 row_stdev 在 band 内的变异系数衡量
        band_rows = row_stdev[b["y0"]:b["y1"]]
        if band_rows:
            row_var = sum((r - b["avg_stdev"]) ** 2 for r in band_rows) / len(band_rows)
            row_stdev_of_stdev = row_var ** 0.5
            cross_block_penalty = min(row_stdev_of_stdev / 30, 1.0) * 30  # 0~30 分惩罚
        else:
            cross_block_penalty = 0

        score = blank_score + brightness_score + edge_score + neighborhood_score - cross_block_penalty

        if score > best_score:
            best_score = score
            best_band_idx = i

    chosen = bands[best_band_idx]
    # 把 mask 放在该 band 中心（box_h 可能比 band_h 大；用全图位置）
    candidate_y = (chosen["y0"] + chosen["y1"]) // 2 - box_h // 2

    # 水平方向细化：如果 mask 宽度 < img_w 的 60%，检查左右半哪个更空
    if box_w < img_w * 0.6:
        gray_w = gray.crop((0, max(0, candidate_y),
                            img_w, min(candidate_y + box_h, img_h)))
        left_stdev = _region_stdev(gray_w.crop((0, 0, img_w // 2, gray_w.height)))
        right_stdev = _region_stdev(gray_w.crop((img_w // 2, 0, img_w, gray_w.height)))
        if right_stdev < left_stdev - 5:  # 右边明显更空
            box_x = max(0, img_w - box_w - int(img_w * 0.06))  # 偏右
        elif left_stdev < right_stdev - 5:
            box_x = int(img_w * 0.06)  # 偏左
        else:
            box_x = (img_w - box_w) // 2  # 居中
    else:
        box_x = (img_w - box_w) // 2

    # 边界保护
    box_y = max(0, min(candidate_y, img_h - box_h))
    return box_x, box_y


def _region_stdev(crop_gray):
    """小工具：计算灰度图的 stdev（用于水平方向留白判断）。"""
    pixels = list(crop_gray.getdata())
    if not pixels:
        return 0.0
    mean = sum(pixels) / len(pixels)
    var = sum((p - mean) ** 2 for p in pixels) / len(pixels)
    return var ** 0.5


# ============================ 文字绘制（带阴影 / 描边） ============================

def draw_shadow_run(overlay, draw, xy, run_text, run_font, stroke_width,
                    dx, dy, blur_radius, shadow_color):
    """绘制单段阴影：临时层 → 模糊 → 贴回 overlay。

    在 shadow_layer 这个独立透明图层上，文字起始坐标就是 (margin + dx, margin + dy)，
    不是 (margin - bbox[0] + dx, ...)。后者会把阴影错误地画在文字左上方。
    阴影也带描边 —— 描边文字投出的影子才与本体形状一致。
    """
    if not run_text or run_font is None:
        return
    bbox = _text_bbox(draw, xy, run_text, run_font, stroke_width)
    margin = int(max(abs(dx), abs(dy)) + blur_radius * 2 + stroke_width)
    tmp_w = bbox[2] - bbox[0] + margin * 2
    tmp_h = bbox[3] - bbox[1] + margin * 2
    if tmp_w <= 0 or tmp_h <= 0:
        return
    shadow_layer = Image.new("RGBA", (tmp_w, tmp_h), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow_layer)
    kwargs = {}
    if stroke_width:
        kwargs = {"stroke_width": stroke_width, "stroke_fill": shadow_color}
    try:
        sd.text((margin + dx, margin + dy), run_text, font=run_font,
                fill=shadow_color, **kwargs)
    except TypeError:
        sd.text((margin + dx, margin + dy), run_text, font=run_font,
                fill=shadow_color)
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    overlay.alpha_composite(shadow_layer, (xy[0] - margin, xy[1] - margin))


def draw_text_block(overlay, draw, xy, text, font, symbol_font, fill_color,
                    stroke_width=0, stroke_fill=None,
                    dx=2, dy=2, blur_radius=1.5, line_extra_gap=0,
                    align="left", max_w=None, shadow_color=(0, 0, 0, 120)):
    """绘制带柔和投影（可选黑色描边）的多行文字。返回块总高度。

    - 按行拆开处理（避免 multiline_textbbox 在混合字体下的复杂性）
    - 行内逐字分流：CJK/ASCII → 主字体；装饰符号（❤ ★ 等）→ symbol_font
    - 主文字 + 阴影分别按 "run" 绘制；run 切分处 cursor_x 平移用 textlength 测量
    - align="center" 时按 max_w 逐行居中（cover 模式用）
    """
    if not text or font is None:
        return 0
    lines = text.split("\n")
    block_h = 0
    for idx, line in enumerate(lines):
        bbox = _text_bbox(draw, (0, 0), line, font, stroke_width)
        line_w = bbox[2] - bbox[0]
        line_h = bbox[3] - bbox[1]
        if align == "center" and max_w:
            cursor_x = xy[0] + (max_w - line_w) // 2 - bbox[0]
        else:
            cursor_x = xy[0]
        cursor_y = xy[1] + block_h

        current_run = ""
        current_font = font
        for ch in line:
            use_font = pick_font_for_char(ch, font, symbol_font)
            if use_font is not current_font and current_run:
                _draw_run_pair(overlay, draw, (cursor_x, cursor_y), current_run,
                               current_font, fill_color, stroke_width, stroke_fill,
                               dx, dy, blur_radius, shadow_color)
                cursor_x += int(draw.textlength(current_run, font=current_font))
                current_run = ""
            current_run += ch
            current_font = use_font
        if current_run:
            _draw_run_pair(overlay, draw, (cursor_x, cursor_y), current_run,
                           current_font, fill_color, stroke_width, stroke_fill,
                           dx, dy, blur_radius, shadow_color)

        block_h += line_h
        if idx < len(lines) - 1:
            block_h += line_extra_gap
    return block_h


def _draw_run_pair(overlay, draw, xy, run_text, run_font, fill_color,
                   stroke_width, stroke_fill, dx, dy, blur_radius, shadow_color):
    """先画阴影，再画带描边的主文字。"""
    draw_shadow_run(overlay, draw, xy, run_text, run_font, stroke_width,
                    dx, dy, blur_radius, shadow_color)
    if stroke_width:
        try:
            draw.text(xy, run_text, font=run_font, fill=fill_color,
                      stroke_width=stroke_width,
                      stroke_fill=stroke_fill or (0, 0, 0, 255))
            return
        except TypeError:
            pass
    draw.text(xy, run_text, font=run_font, fill=fill_color)


# ============================ 主入口 ============================

def add_ins_overlay(
    image_path,
    output_path,
    title,
    body=None,
    font_path=None,
    position="auto",
    title_font_path=None,
    body_font_path=None,
    mode="ins",
):
    """
    给单图或拼图添加排版文字。

    :param image_path: 输入图片路径
    :param output_path: 输出图片路径
    :param title: 主标题（支持符号，如 "❤ 每天记账..."；cover 模式用 \\n 指定语义断行）
    :param body: 正文长文本（cover 模式忽略）
    :param font_path: 兼容旧参数——若提供则同时用作标题/正文字体
    :param title_font_path: 标题字体（推荐 PingFang SC Semibold / 思源黑体 Bold / 微软雅黑 Bold）
    :param body_font_path: 正文字体（推荐 思源宋体 / 霞鹜文楷 / Arial / SimHei）
    :param position: 蒙版位置 ("auto", "bottom", "center")；cover 模式忽略（恒为居中）
    :param mode: "ins" = 半透明灰蒙版 + 标题/正文（默认）；
                  "cover" = 无蒙版，居中大字标题 + 黑白描边 + 加强阴影，且不含正文
    """
    base_img = Image.open(image_path).convert("RGBA")
    img_w, img_h = base_img.size

    if mode == "cover":
        _render_cover(base_img, output_path, title, img_w, img_h,
                      title_font_path=title_font_path,
                      font_path=font_path)
        return

    body = body or ""

    # 字号根据图片高度自适应
    title_size = int(img_h * INS_TITLE_RATIO)
    body_size = int(img_h * INS_BODY_RATIO)

    title_font = load_cjk_font(title_font_candidates(title_font_path, font_path), title_size)
    body_font = load_cjk_font(body_font_candidates(body_font_path, font_path), body_size)

    # 终极兜底：默认字体（极端情况下中文仍 tofu，但至少不崩）
    if title_font is None:
        title_font = ImageFont.load_default()
    if body_font is None:
        body_font = ImageFont.load_default()

    # 处理文本换行：用实测像素宽度做折行，避免 CJK / 数字混排时 CJK 一字当一字算导致溢出
    padding = int(img_w * 0.06)  # 边距
    line_spacing = int(img_h * 0.02)  # 标题与正文间距
    box_w = int(img_w * 0.88)  # 蒙版宽度占图片 88%
    max_line_w = box_w - padding * 2  # 正文每行最大像素宽度
    dummy_draw = ImageDraw.Draw(base_img)

    # 标题 bbox
    title_bbox = dummy_draw.textbbox((0, 0), title, font=title_font)
    title_h = title_bbox[3] - title_bbox[1]

    # 正文按字符贪心折行：每加一字若行宽度 ≤ max_line_w 才接受
    def _wrap_by_pixel_width(text, font, max_px):
        """按实测像素宽度折行（不依赖估算的字符宽度）。CJK 字符 ≈ Latin 字符 2× 宽，
        用 textlength 准确测量后判断换行点。"""
        out_lines = []
        current = ""
        current_w = 0
        for ch in text:
            if ch == "\n":
                out_lines.append(current)
                current = ""
                current_w = 0
                continue
            ch_w = dummy_draw.textlength(ch, font=font)
            if current_w + ch_w > max_px and current:
                out_lines.append(current)
                current = ch
                current_w = ch_w
            else:
                current += ch
                current_w += ch_w
        if current:
            out_lines.append(current)
        return out_lines

    wrapped_lines = _wrap_by_pixel_width(body, body_font, max_line_w)
    wrapped_body = "\n".join(wrapped_lines)

    # 计算正文总高度：每行单独测高，再加行间距（与 draw_text_block 的
    # line_extra_gap 一致，避免蒙版高度低估导致最后一行被截断）
    body_line_gap_for_box = int(body_size * 0.5)
    body_line_heights = []
    for line in wrapped_lines:
        bb = dummy_draw.textbbox((0, 0), line, font=body_font)
        body_line_heights.append(bb[3] - bb[1])
    body_total_h = sum(body_line_heights) + max(len(wrapped_lines) - 1, 0) * body_line_gap_for_box

    # 蒙版总高度 = 标题高 + 标题-正文间距 + 正文总高 + 上下 padding
    box_h = title_h + line_spacing + body_total_h + padding * 2

    # 如果文字特别多，动态撑满整页或大面积覆盖
    if box_h > img_h * 0.7:
        box_h = int(img_h * 0.85)

    # 计算蒙版坐标（支持自动留白 / 固定位置）
    if position == "auto":
        # 自动留白分析：找最"空"的水平带放置文字蒙版
        box_x, box_y = find_blank_region(base_img, box_w, box_h)
    elif position == "center":
        box_x = (img_w - box_w) // 2
        box_y = (img_h - box_h) // 2
    else:  # "bottom" 或其他
        box_x = (img_w - box_w) // 2
        box_y = int(img_h * 0.42)  # 贴近视觉中心偏下

    # 创建半透明灰色蒙版层 (Alpha 200 约等于 0.8 透明度)
    overlay = Image.new("RGBA", base_img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # 绘制灰色半透明矩形框 (RGB: 110, 110, 110 偏高级灰，A: 200 对应 0.8 灰度)
    draw.rectangle(
        [box_x, box_y, box_x + box_w, box_y + box_h],
        fill=(105, 105, 105, 178)  # alpha 178 ≈ 0.70 opacity（0.65-0.7 区间，让背景更通透）
    )

    # 绘制文字（带柔和投影 + 白色字）—— 先单独渲一层阴影做高斯模糊，再盖上白字
    text_x = box_x + padding
    current_y = box_y + padding

    title_color = (255, 255, 255, 255)
    body_color = (240, 240, 240, 245)  # 极浅灰白（off-white）

    # Symbol 字体加载（❤ ★ ♡ → 这类装饰符号）
    symbol_font = load_font(symbol_font_candidates(), title_size)

    # 绘制主标题（白字 + 柔和阴影；ins 模式不加描边）
    draw_text_block(
        overlay, draw, (text_x, current_y), title, title_font, symbol_font,
        title_color, dx=3, dy=3, blur_radius=2.0,  # 标题字号大，阴影稍夸张
        shadow_color=(0, 0, 0, 120),
    )
    current_y += title_h + line_spacing

    # 正文行间额外间距（base_line_h 已含字体 ascent+descent；额外加 0.5×字号让行距更舒展）
    body_line_gap = int(body_size * 0.5)

    # 绘制正文（off-white + 较弱阴影，保持安静感）
    draw_text_block(
        overlay, draw, (text_x, current_y), wrapped_body, body_font, symbol_font,
        body_color, dx=2, dy=2, blur_radius=1.2, line_extra_gap=body_line_gap,
        shadow_color=(0, 0, 0, 120),
    )

    # 合并图层并保存
    final_img = Image.alpha_composite(base_img, overlay)
    final_img.convert("RGB").save(output_path, "JPEG", quality=95)
    print(f"成功生成排版图片: {output_path}")


def _render_cover(base_img, output_path, title, img_w, img_h,
                  title_font_path=None, font_path=None):
    """cover 模式：不画灰蒙版，居中写一个大字标题（黑白描边 + 加强阴影）。

    只有 title，没有 body —— 社媒封面（小红书 / 公众号 / 视频号）的视觉惯例是
    用超大标题压住整张图，靠描边保证在任何背景上都读得清，而不是靠灰色蒙版。
    """
    if not (title or "").strip():
        raise ValueError("cover 模式必须提供 --title")

    plan = plan_cover_layout(title, img_w, img_h,
                             title_font_path=title_font_path or font_path)

    font = load_cjk_font(title_font_candidates(title_font_path, font_path),
                         plan["font_size"])
    symbol_font = load_font(symbol_font_candidates(), plan["font_size"])
    if font is None:
        font = ImageFont.load_default()

    overlay = Image.new("RGBA", base_img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    font_size = plan["font_size"]
    # 阴影随字号放大，让大字从背景里"浮"出来
    shadow_dx = max(3, int(font_size * COVER_SHADOW_RATIO))
    shadow_blur = max(2.0, font_size * COVER_SHADOW_BLUR_RATIO)

    block_top = max(0, (img_h - plan["block_h"]) // 2)
    draw_text_block(
        overlay, draw, (0, block_top), "\n".join(plan["lines"]),
        font, symbol_font,
        fill_color=(255, 255, 255, 255),
        stroke_width=plan["stroke_width"],
        stroke_fill=(0, 0, 0, 255),
        dx=shadow_dx, dy=shadow_dx, blur_radius=shadow_blur,
        line_extra_gap=plan["line_gap"],
        align="center", max_w=img_w,
        shadow_color=(0, 0, 0, 150),  # 比 ins 模式更重，凸显大字
    )

    final_img = Image.alpha_composite(base_img, overlay)
    final_img.convert("RGB").save(output_path, "JPEG", quality=95)
    print(f"成功生成 cover 图片: {output_path} "
          f"(字号 {font_size}px, {len(plan['lines'])} 行, "
          f"描边 {plan['stroke_width']}px)")

# === CLI 入口 ===
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="INS 风排版：灰蒙版图文（ins）或大字封面标题（cover）（Pillow）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # ins 模式：半透明灰蒙版 + 标题 + 正文
  python add_ins_overlay.py --input photo.jpg --output styled.jpg \\
      --title "❤ 富婆的 12 个隐秘爱好" --body-file body.txt --position auto

  python add_ins_overlay.py --input collage.jpg --output final.jpg \\
      --title "★ 户外控的 8 件好物" --body "1、托特包\\n2、马克杯\\n3、旅行日记" --position bottom

  # cover 模式：无蒙版，居中大字标题 + 黑白描边（只有标题，没有正文）
  python add_ins_overlay.py --input collage.jpg --output cover.jpg --mode cover \\
      --title "40+后才明白\\n女人越来越差的9个原因"

mode 取值:
  ins     半透明灰蒙版 + 标题 + 正文（默认）
  cover   社媒封面：无蒙版，居中大字标题（约 2× 普通标题）+ 黑白描边 + 加强阴影

position 取值（仅 ins 模式生效）:
  bottom  偏下（默认，最适合 INS 风，保护顶部视觉焦点）
  auto    自动分析留白，落到最空的位置
  center  居中
        """,
    )
    parser.add_argument("-i", "--input", required=True,
                        help="输入图片路径（jpg/png）")
    parser.add_argument("-o", "--output", required=True,
                        help="输出图片路径（jpg）")
    parser.add_argument("-t", "--title", required=True,
                        help="标题文字（支持符号如 ❤ ★ 1、；cover 模式用 \\n 指定语义断行）")
    parser.add_argument("-b", "--body", default=None,
                        help="正文（多行用 \\n）；cover 模式忽略")
    parser.add_argument("--body-file", default=None,
                        help="从文件读取正文；cover 模式忽略")
    parser.add_argument("-m", "--mode", default="ins",
                        choices=["ins", "cover"],
                        help="排版模式（默认 ins）")
    parser.add_argument("-p", "--position", default="bottom",
                        choices=["bottom", "auto", "center"],
                        help="蒙版位置（默认 bottom；仅 ins 模式生效）")
    parser.add_argument("--title-font", default=None,
                        help="标题字体路径（覆盖自动选择）")
    parser.add_argument("--body-font", default=None,
                        help="正文字体路径（覆盖自动选择）")
    parser.add_argument("--opacity", type=float, default=None,
                        help="蒙版不透明度 0-1（默认 0.70）")

    args = parser.parse_args()

    # 读取正文（cover 模式不需要正文）
    if args.body_file and args.mode == "ins":
        with open(args.body_file, encoding="utf-8") as f:
            body_text = f.read().rstrip("\n")
    else:
        body_text = args.body or ""

    if not args.title.strip():
        parser.error("--title 不能为空")
    if args.mode == "ins" and not body_text:
        parser.error("ins 模式需要 --body 或 --body-file 提供正文（只要封面请用 --mode cover）")

    # 注：当前 alpha=178 硬编码 (~0.70)；如果以后想支持自定义 opacity，需要在
    # add_ins_overlay() 里加 mask_alpha 参数；现在 --opacity 仅打印提示
    if args.opacity is not None and args.mode == "ins":
        print(f"ℹ️ 当前 --opacity 参数仅提示，未生效（默认 0.70）；"
              f"如需自定义请修改 add_ins_overlay.py 内的 alpha=178")

    add_ins_overlay(
        image_path=args.input,
        output_path=args.output,
        title=args.title,
        body=body_text,
        title_font_path=args.title_font,
        body_font_path=args.body_font,
        position=args.position,
        mode=args.mode,
    )
