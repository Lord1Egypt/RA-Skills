#!/usr/bin/env python3
"""
generate_panel.py -- 面板生成模块 (v15 public package)
基于 ParseResult + ScanResult 生成 panel DOM、toolbar DOM 和 window.X 常量。

对应规范: R1-R6, R12, R14, 附录 C (LABEL_FOR), 附录 D Steps 3-7,11
"""

import os
import re
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class PanelConfig:
    """面板生成结果"""
    color_rows: list       # [{var, label, default_value}]
    preset_themes: dict    # {name: {var: value}} -- FLAT
    layout_sliders: list   # [{target, prop, unit, min, max, default, label, key}]
    size_sliders: list     # [{target, prop, label, min, max, default, unit, key}]
    panel_html: str        # 渲染好的完整 panel DOM
    toolbar_html: str      # 定制后的 toolbar DOM
    constants_js: str      # window.DEFAULT_COLORS / PRESETS / SIZE_BOUNDS / PAGE_ELEMENT_TO_PANEL / CSS_VAR_TO_ELEMENTS
    label_for: dict        # LABEL_FOR single-source-of-truth
    # v1.7.0: 收敛策略产出
    display_color_groups: list = None    # 面板实际展示的 4 组颜色 (≤12)
    display_size_sliders: list = None    # 面板实际展示的字号 slider (≤10)
    color_var_to_rep: dict = None        # {var: representative_var}
    size_target_to_family: dict = None   # {original_target: family_target}


# 面板相关的路径
ASSETS_DIR = Path(__file__).parent.parent / 'assets'
PRESETS_DIR = Path(__file__).parent.parent / 'presets'

# ============================================================
# LABEL_FOR: single-source-of-truth (附录 C)
# {(tab_name, key): label_string}
# tab_name: '颜色' / '字号' / '布局'
# key: 颜色 tab 用 '--var-name'；字号/布局 tab 用 selector 字符串
# ============================================================
LABEL_FOR = {}

# 金版已知变量名 -> 语义 label 映射（启发式兜底）
GOLD_VAR_LABELS = {
    '--accent': '主色调 Accent',
    '--accent-soft': '主色浅 Accent Soft',
    '--warm': '暖色 Warm',
    '--warm-soft': '暖色浅 Warm Soft',
    '--gold': '金色 Gold',
    '--gold-soft': '金色浅 Gold Soft',
    '--sage': '青绿 Sage',
    '--sage-soft': '青绿浅 Sage Soft',
    '--bg': '页面底色 BG',
    '--ink': '主文字 Ink',
    '--ink-2': '次文字 Ink-2',
    '--ink-3': '辅文字 Ink-3',
    '--line': '分割线 Line',
    '--line-2': '分割线浅 Line-2',
}

# 颜色分段规则：哪些变量属于「主题色板」，其余归「文字色」
THEME_COLOR_PREFIXES = {'accent', 'warm', 'gold', 'sage', 'bg', 'primary', 'secondary'}
TEXT_COLOR_PREFIXES = {'ink', 'text', 'line', 'border'}

# ============================================================
# SEMANTIC_ALIAS: preset 命名 → host 实际命名候选 (P0-1 修复)
# 按优先级取第一个存在的 host 变量做映射
# ============================================================
SEMANTIC_ALIAS = {
    # 主色调系列
    '--accent':      ['--accent', '--primary', '--brand', '--blue', '--theme', '--main'],
    '--accent-soft': ['--accent-soft', '--accent-light', '--primary-light', '--blue-light', '--theme-light'],
    # 暖色 / 强调
    '--warm':        ['--warm', '--orange', '--accent-2', '--secondary', '--red'],
    '--warm-soft':   ['--warm-soft', '--orange-light', '--red-light'],
    # 金色 / 警示
    '--gold':        ['--gold', '--yellow', '--warning', '--amber'],
    '--gold-soft':   ['--gold-soft', '--yellow-light'],
    # 文字
    '--ink':         ['--ink', '--text', '--text-primary', '--fg', '--foreground', '--text-1'],
    '--ink-2':       ['--ink-2', '--text-muted', '--text-secondary', '--gray', '--text-2'],
    '--ink-3':       ['--ink-3', '--text-light', '--text-tertiary', '--gray-light', '--text-3'],
    # 边框 / 分割
    '--line':        ['--line', '--border', '--divider', '--separator'],
    '--line-2':      ['--line-2', '--border-light'],
    # 背景
    '--bg':          ['--bg', '--background', '--page-bg', '--body-bg'],
    '--bg-card':     ['--bg-card', '--card-bg', '--surface'],
    # 状态色
    '--success':     ['--success', '--green', '--ok'],
    '--success-soft':['--success-soft', '--green-light'],
    '--danger':      ['--danger', '--red', '--error'],
    '--danger-soft': ['--danger-soft', '--red-light'],
    # 青绿（金版有 sage）
    '--sage':        ['--sage', '--green', '--teal', '--mint'],
    '--sage-soft':   ['--sage-soft', '--green-light', '--teal-light'],
}


def _extract_preset_color(raw_vars: dict, role: str) -> str:
    """从预设的原始变量定义中，按语义角色提取颜色值。
    role: 'bg', 'accent', 'warm', 'gold', 'ink', 'text', 'line' 等
    按优先级搜索匹配的变量名，返回第一个有效的 hex 颜色值。
    """
    # 角色对应的变量名候选（按优先级排序）
    ROLE_CANDIDATES = {
        'bg':     ['--bg', '--background', '--bg-card', '--page-bg', '--body-bg'],
        'accent': ['--accent', '--primary', '--brand', '--theme', '--main', '--blue'],
        'warm':   ['--warm', '--orange', '--accent-2', '--secondary', '--red'],
        'gold':   ['--gold', '--yellow', '--warning', '--amber'],
        'ink':    ['--ink', '--text', '--text-primary', '--fg', '--foreground'],
        'text':   ['--text', '--ink', '--fg', '--foreground'],
        'line':   ['--line', '--border', '--divider'],
    }
    candidates = ROLE_CANDIDATES.get(role, [f'--{role}'])
    for key in candidates:
        val = raw_vars.get(key, '')
        if val and re.match(r'^#[0-9a-fA-F]{3,8}$', val):
            return val
    # 兜底：按前缀搜索
    prefix = f'--{role}'
    for key, val in raw_vars.items():
        if key.startswith(prefix) and val and re.match(r'^#[0-9a-fA-F]{3,8}$', val):
            return val
    return ''


def _is_color_dark(hex_color: str) -> bool:
    """判断颜色是否为深色（相对亮度 < 0.5）"""
    hex_color = hex_color.strip('#')
    if len(hex_color) == 3:
        hex_color = hex_color[0]*2 + hex_color[1]*2 + hex_color[2]*2
    try:
        r = int(hex_color[0:2], 16) / 255
        g = int(hex_color[2:4], 16) / 255
        b = int(hex_color[4:6], 16) / 255
        luminance = 0.299 * r + 0.587 * g + 0.114 * b
        return luminance < 0.5
    except (ValueError, IndexError):
        return True


def _map_preset_to_host_vars(preset_vars: dict, host_var_names: set) -> dict:
    """
    把语义命名的 preset 映射到 host 实际变量名。
    优先级：完全同名 > SEMANTIC_ALIAS 候选 > 前缀模式匹配。
    v16: 增加第三轮前缀模式匹配，支持 --text-xxxx / --bg-xxxx / --line-xxxx / --theme-xxxx 等命名。
    """
    mapped = {}
    used_targets = set()  # 避免一个 host 变量被多个 preset 变量映射

    # 第一轮：完全同名
    for var, val in preset_vars.items():
        if var in host_var_names:
            mapped[var] = val
            used_targets.add(var)

    # 第二轮：SEMANTIC_ALIAS 映射
    for var, val in preset_vars.items():
        if var in mapped:
            continue
        candidates = SEMANTIC_ALIAS.get(var, [])
        for candidate in candidates:
            if candidate in host_var_names and candidate not in used_targets:
                mapped[candidate] = val
                used_targets.add(candidate)
                break

    # 第三轮：v17 重写 — 语义分组 + 1:1 最佳匹配
    # 将 host 变量按前缀分为语义组，每组只从对应 preset 角色取值
    # todo22-A: --bg / --background / --card / --surface 前缀大面积底色，
    #          严禁映射到 --accent / --warm / --gold（强色），否则换肤后整页变单色。
    HOST_PREFIX_TO_PRESET_ROLE = {
        # host 变量前缀 → 优先取值的 preset 角色（按优先级排序）
        '--accent':  ['--accent', '--warm', '--gold'],
        '--brand':   ['--accent', '--warm'],
        '--theme':   ['--accent', '--warm', '--gold'],
        '--primary': ['--accent'],
        '--bg':      ['--bg', '--accent-soft', '--warm-soft'],     # 大面积底：只用 bg/soft
        '--background': ['--bg', '--accent-soft'],
        '--card':    ['--bg', '--accent-soft'],
        '--surface': ['--bg', '--accent-soft'],
        '--ink':     ['--ink', '--ink-2', '--ink-3'],
        '--text':    ['--ink', '--ink-2', '--ink-3'],
        '--fg':      ['--ink'],
        '--warm':    ['--warm', '--gold', '--accent'],
        '--orange':  ['--warm'],
        '--red':     ['--danger', '--warm'],
        '--gold':    ['--gold', '--warm'],
        '--yellow':  ['--gold'],
        '--amber':   ['--gold'],
        '--sage':    ['--sage', '--warm'],
        '--green':   ['--sage', '--success'],
        '--teal':    ['--sage'],
        '--mint':    ['--sage'],
        '--line':    ['--line', '--line-2'],
        '--stroke':  ['--line'],
        '--border':  ['--line', '--line-2'],
        '--divider': ['--line'],
        '--success': ['--success'],
        '--danger':  ['--danger'],
    }

    # 收集尚未映射的 host 变量
    unmapped_host = [v for v in sorted(host_var_names) if v not in used_targets]

    for host_var in unmapped_host:
        # 找到 host_var 最匹配的前缀组
        best_prefix = None
        best_len = 0
        for prefix in HOST_PREFIX_TO_PRESET_ROLE:
            if host_var.startswith(prefix) and len(prefix) > best_len:
                best_prefix = prefix
                best_len = len(prefix)

        if best_prefix is None:
            continue

        # 从该前缀对应的 preset 角色中，找第一个有值且未映射到其他 host 的
        role_candidates = HOST_PREFIX_TO_PRESET_ROLE[best_prefix]
        for role in role_candidates:
            if role in preset_vars and role not in mapped:
                mapped[host_var] = preset_vars[role]
                used_targets.add(host_var)
                break

    return mapped


# 预设卡片显示名 (R5.3 — 色卡 UI 不再需要 emoji)
PRESET_DISPLAY_NAMES = {
    'original': '原版',
    'tencent-blue': '腾讯蓝',
    'newsprint': '报纸灰',
    'night': '夜间模式',
    'warm-sepia': '暖棕',
    'executive-navy': '深海商务',
    'linear-dusk': '幕光紫',
    'notion-journal': '手帐暖白',
    'arc-gradient': '彩虹弧光',
    'moss-earth': '苔藓大地',
    'raycast-noir': '炭火暗夜',
}


def _parse_size_value(value: str) -> dict:
    """解析尺寸值，返回 {value, unit, min, max}"""
    value = value.strip()
    clamp_match = re.match(r'clamp\(\s*([\d.]+)([\w%]+)\s*,\s*[^,]+\s*,\s*([\d.]+)([\w%]+)\s*\)', value)
    if clamp_match:
        min_val = float(clamp_match.group(1))
        unit = clamp_match.group(2)
        max_val = float(clamp_match.group(3))
        default_val = (min_val + max_val) / 2
        return {'default': default_val, 'min': min_val, 'max': max_val, 'unit': unit}

    num_match = re.match(r'^([\d.]+)\s*(px|em|rem|vw|vh|%)$', value)
    if num_match:
        num = float(num_match.group(1))
        unit = num_match.group(2)
        if unit == 'px':
            min_val = max(8, num * 0.4)
            max_val = num * 3
        elif unit in ('em', 'rem'):
            min_val = max(0.5, num * 0.4)
            max_val = num * 3
        else:
            min_val = max(1, num * 0.3)
            max_val = num * 3
        return {'default': num, 'min': round(min_val, 2), 'max': round(max_val, 2), 'unit': unit}

    return {'default': 16, 'min': 8, 'max': 72, 'unit': 'px'}


def _load_builtin_presets() -> dict:
    """加载内置预设"""
    presets_file = PRESETS_DIR / 'builtin.json'
    if presets_file.exists():
        try:
            with open(presets_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {}


def _generate_color_row_html(var_name: str, label: str, default_value: str) -> str:
    """生成单行颜色控件 HTML (R2.2)"""
    hex_value = default_value if re.match(r'^#[0-9a-fA-F]{3,8}$', default_value) else '#888888'
    if len(hex_value) == 4:
        hex_value = f'#{hex_value[1]*2}{hex_value[2]*2}{hex_value[3]*2}'
    hex_upper = hex_value.upper()

    return f'''        <div class="color-row">
            <span class="color-label">{label}</span>
            <div class="color-swatch" style="background:{hex_value};"><input type="color" value="{hex_value}" data-var="{var_name}" onchange="applyColor(this)" oninput="previewColor(this)"></div>
            <input type="text" class="color-hex" value="{hex_upper}" data-var="{var_name}" onchange="applyHex(this)">
        </div>'''


def _generate_slider_html(label: str, key: str, target: str, prop: str, unit: str,
                           min_val, max_val, step, default_val) -> str:
    """
    生成通用 slider HTML (R3.1 / R4.1)
    金版结构: slider-row > slider-label > (slider-name + slider-val[id]) + input[oninput=applyLayout]
    """
    display_val = f"{default_val}{unit}" if unit else str(default_val)
    return f'''        <div class="slider-row">
            <div class="slider-label">
                <span class="slider-name">{label}</span>
                <span class="slider-val" id="val-{key}">{display_val}</span>
            </div>
            <input type="range" min="{min_val}" max="{max_val}" step="{step}" value="{default_val}" data-target="{target}" data-prop="{prop}" data-unit="{unit}" oninput="applyLayout(this, 'val-{key}')">
        </div>'''


def _classify_color_section(var_name: str) -> str:
    """根据变量名判断属于 主题色板 还是 文字色"""
    name = var_name.lstrip('-')
    first_part = name.split('-')[0] if '-' in name else name
    if first_part in TEXT_COLOR_PREFIXES:
        return '文字色'
    return '主题色板'


# ============================================================
# v1.7.0: 颜色面板收敛（todo25 + todo26）
# 把 38+ 个 raw 变量按"角色 + 视觉相似度"折叠为 ≤12 个面板项
# 每个面板项是一个 group，含 1 个"代表变量"(representative) 和 N 个 alias
# 用户调整代表色 → editor-core.js 会把同组 alias 一并刷新
# ============================================================

# 4 个角色组（顺序就是面板展示顺序）
COLOR_ROLE_GROUPS = ['accent', 'text', 'bg', 'border']

COLOR_ROLE_LABELS = {
    'accent': ('强调 / 主色 Accent', 'group_accent'),
    'text':   ('文字 Text',          'group_text'),
    'bg':     ('背景 Background',    'group_bg'),
    'border': ('边框 / 分割线 Border', 'group_border'),
}

# 每组面板最多展示几项；超出折叠（折叠交给前端，这里只限制候选数）
MAX_PER_GROUP = 3
MAX_TOTAL_DISPLAY = 12

# 用户友好的 group label —— 不再带 hex 后缀
# (zh, en)
COLOR_FRIENDLY_LABELS = {
    'accent_primary':   ('主色 Brand', '主色 Brand'),
    'accent_secondary': ('辅强调 Accent 2', 'Accent 2'),
    'accent_3':         ('辅强调 Accent 3', 'Accent 3'),
    'text_body':        ('正文 Body', 'Body'),
    'text_muted':       ('次要 Muted', 'Muted'),
    'text_subtle':      ('弱化 Subtle', 'Subtle'),
    'bg_page':          ('页面底色 Page Bg', 'Page Bg'),
    'bg_card':          ('卡片底色 Card Bg', 'Card Bg'),
    'bg_banner':        ('Banner 底色 Banner Bg', 'Banner Bg'),
    'bg_alt':           ('备用底色 Alt Bg', 'Alt Bg'),
    'border_divider':   ('主分割线 Divider', 'Divider'),
    'border_card':      ('卡片描边 Card Border', 'Card Border'),
}


def _classify_color_role(var_name: str, hex_value: str) -> str:
    """把一个变量归到 accent / text / bg / border 之一。"""
    name = var_name.lstrip('-').lower()
    first = name.split('-')[0] if '-' in name else name

    # 中文 prefix（用户截图里 host 用了 --文字XXXX / --页面底色XXXX / --分割线XXXX）
    # 用 raw 名（去前缀 --）做子串匹配，因为 split 不能切中文
    raw = var_name.lstrip('-')
    if raw.startswith('文字'):
        return 'text'
    if raw.startswith('分割线') or raw.startswith('边框'):
        return 'border'
    if raw.startswith('页面底色') or raw.startswith('卡片') or raw.startswith('banner') or raw.startswith('statbox') or raw.startswith('upcomingbox') or raw.startswith('背景'):
        return 'bg'
    if raw.startswith('主题') or raw.startswith('强调') or raw.startswith('主色'):
        return 'accent'

    # 文字色
    if first in {'ink', 'text', 'fg', 'foreground'}:
        return 'text'
    # 边框 / 分割线
    if first in {'line', 'border', 'divider', 'separator'}:
        return 'border'
    # 背景
    if first in {'bg', 'background', 'banner', 'statbox', 'upcomingbox', 'card', 'surface', 'page'}:
        return 'bg'
    # accent / theme / 主色
    if first in {'accent', 'primary', 'brand', 'theme', 'main', 'warm', 'gold', 'sage', 'success', 'warning', 'danger', 'info'}:
        return 'accent'

    # 兜底：用 hex 亮度+饱和度判断
    try:
        h = hex_value.lstrip('#')
        if len(h) == 3:
            h = ''.join(c * 2 for c in h)
        if len(h) >= 6:
            r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
            # 灰阶（R≈G≈B）→ border or text
            max_c, min_c = max(r, g, b), min(r, g, b)
            if max_c - min_c < 12:
                # 灰，再按亮度区分
                lum = (r + g + b) / 3
                if lum >= 230:
                    return 'bg'      # 极浅灰 → 当背景
                if lum < 90:
                    return 'text'    # 深 → 文字
                return 'border'      # 中间灰 → 分割线
            # 彩色但很浅 → 背景
            lum = (r + g + b) / 3
            if lum >= 230:
                return 'bg'
            # 彩色中等以上饱和度 → 主色
            return 'accent'
    except Exception:
        pass
    return 'accent'


def _hex_brightness(hex_value: str) -> float:
    """返回 hex 亮度 0~255，用于排序/过滤"""
    try:
        h = hex_value.lstrip('#')
        if len(h) == 3: h = ''.join(c * 2 for c in h)
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return (r * 299 + g * 587 + b * 114) / 1000
    except Exception:
        return 128.0


def _hex_saturation(hex_value: str) -> float:
    """返回 HSL saturation 0~1"""
    try:
        h = hex_value.lstrip('#')
        if len(h) == 3: h = ''.join(c * 2 for c in h)
        r, g, b = int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255
        mx, mn = max(r, g, b), min(r, g, b)
        l = (mx + mn) / 2
        if mx == mn:
            return 0.0
        d = mx - mn
        return d / (2 - mx - mn) if l > 0.5 else d / (mx + mn)
    except Exception:
        return 0.0


def _hex_distance(a: str, b: str) -> float:
    """两个 hex 颜色的近似 RGB 距离 (0~441)。"""
    try:
        ha = a.lstrip('#'); hb = b.lstrip('#')
        if len(ha) == 3: ha = ''.join(c * 2 for c in ha)
        if len(hb) == 3: hb = ''.join(c * 2 for c in hb)
        r1, g1, b1 = int(ha[0:2], 16), int(ha[2:4], 16), int(ha[4:6], 16)
        r2, g2, b2 = int(hb[0:2], 16), int(hb[2:4], 16), int(hb[4:6], 16)
        return ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5
    except Exception:
        return 999.0


def _collapse_color_rows(color_rows: list, css_var_to_elements: dict, color_usage: dict = None) -> tuple:
    """
    v1.8.0 重写：数据驱动颜色面板。

    优先使用 scan_result.color_usage（top-N hex 聚合）；若为空则降级到旧的"按角色分类"策略。

    返回 (display_groups, var_to_group):
      display_groups: [{role, label, var (代表变量), default_value, aliases, group_label, weight}]
      var_to_group:   {var_name: representative_var}  -- 给 editor-core.js 用
    """
    # 若没拿到 color_usage，回退旧策略（保留向后兼容）
    if not color_usage or not isinstance(color_usage, dict):
        return _collapse_color_rows_legacy(color_rows, css_var_to_elements)

    # 把 raw color_rows 索引为 {hex: [row, row, ...]}（同色 multi-var）
    hex_to_rows = {}
    for row in color_rows:
        hx = _normalize_hex_local(row['default_value'])
        if hx:
            hex_to_rows.setdefault(hx, []).append(row)

    # 频次语义命名（todo46）+ 角色前缀（todo56）
    LABELS_BY_RANK = [
        ('主要', 'Primary'),
        ('次要', 'Secondary'),
        ('强调', 'Highlight'),
        ('装饰', 'Accent'),
        ('偶用', 'Subtle'),
    ]
    ROLE_PREFIX = {
        'text':   ('文字', 'Text'),
        'bg':     ('背景', 'Bg'),
        'border': ('边框', 'Border'),
    }

    TOP_N = {'text': 5, 'bg': 4, 'border': 3}
    ROLE_TITLE = {
        'text':   '文字 Text',
        'bg':     '背景 Background',
        'border': '边框 / 分割线 Border',
    }

    display_groups = []
    var_to_group = {}

    global_fallback_rep = None

    for role in ['text', 'bg', 'border']:
        items = (color_usage.get(role) or [])
        if not items:
            continue
        kept = items[:TOP_N[role]]
        spilled = items[TOP_N[role]:]

        for idx, (hx, w, src_vars) in enumerate(kept):
            if idx < len(LABELS_BY_RANK):
                rank_zh, rank_en = LABELS_BY_RANK[idx]
            else:
                rank_zh, rank_en = f'其他{idx+1}', f'Other {idx+1}'
            role_zh, role_en = ROLE_PREFIX.get(role, ('', ''))
            # v1.8.3 todo60: 行内 label 去角色前缀，只留频次词；section title 已经显示"文字/背景/边框"上下文
            label = f'{rank_zh} {rank_en}'.strip()
            # 同 hex 在 color_rows 中的所有 raw row（这些都是"同色多变量"，需要联动）
            same_hex_rows = hex_to_rows.get(hx, [])
            if same_hex_rows:
                rep_var = same_hex_rows[0]['var']
            elif src_vars:
                rep_var = src_vars[0]
            else:
                # 该 hex 在源 HTML 是裸 hex，合成一个变量（前端会照常 setProperty 但不会回写到原 inline）
                rep_var = '--hve-{}-{}'.format(role, hx.lstrip('#').lower())

            display_groups.append({
                'role': role,
                'group_label': ROLE_TITLE[role],
                'var': rep_var,
                'label': label,
                'default_value': hx,
                'aliases': [r['var'] for r in same_hex_rows if r['var'] != rep_var],
                'weight': w,
            })

            for r in same_hex_rows:
                var_to_group[r['var']] = rep_var

            if global_fallback_rep is None:
                global_fallback_rep = rep_var

        # 溢出 hex 的 raw vars 也指向 kept[0] 的 rep，保持点击代表色时连带刷新
        if kept and spilled:
            anchor_hex = kept[0][0]
            anchor_rows = hex_to_rows.get(anchor_hex, [])
            anchor_rep = anchor_rows[0]['var'] if anchor_rows else None
            if anchor_rep:
                for hx, _, _ in spilled:
                    for r in hex_to_rows.get(hx, []):
                        var_to_group.setdefault(r['var'], anchor_rep)

    # 兜底：每个 raw color_row 都必须有映射
    if global_fallback_rep:
        for r in color_rows:
            var_to_group.setdefault(r['var'], global_fallback_rep)

    return display_groups, var_to_group


def _normalize_hex_local(s: str) -> str:
    """本地版 hex 归一化"""
    if not s:
        return ''
    s = s.strip()
    m = re.match(r'#([0-9a-fA-F]{3,8})', s)
    if not m:
        return ''
    h = m.group(1)
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    elif len(h) >= 6:
        h = h[:6]
    else:
        return ''
    return '#' + h.upper()


def _collapse_color_rows_legacy(color_rows: list, css_var_to_elements: dict) -> tuple:
    """
    将完整 color_rows 折叠为面板展示版 (todo25 + todo26)。

    返回 (display_groups, var_to_group):
      display_groups: [{role, label_zh, label_en, i18n_key, var (代表变量), default_value, aliases: [其他同组变量]}]
      var_to_group:   {var_name: representative_var}  -- 给 editor-core.js 用：调 representative 时同步 alias

    策略：
    1. 按角色分到 4 组 (accent/text/bg/border)
    2. 每组内按 hex 聚类（距离 < 30 视为同类），同类合并
    3. 每个 cluster 选"使用频率最高"的为代表
    4. 每组取 Top MAX_PER_GROUP；超出的合并到最后一组的代表里（或丢弃，由 var_to_group 同步）
    5. 总数控制在 ≤ MAX_TOTAL_DISPLAY
    """
    # Step 1: 按角色分桶
    buckets = {r: [] for r in COLOR_ROLE_GROUPS}
    for row in color_rows:
        role = _classify_color_role(row['var'], row['default_value'])
        buckets[role].append(row)

    # Step 2 + 3: 每个角色内按 hex 聚类
    def _cluster(rows):
        clusters = []  # [[row, row, ...], ...]
        for row in rows:
            placed = False
            for c in clusters:
                if _hex_distance(row['default_value'], c[0]['default_value']) < 30:
                    c.append(row)
                    placed = True
                    break
            if not placed:
                clusters.append([row])
        return clusters

    # 角色内排序：每个角色用合适的"代表"逻辑
    def _sort_clusters(role, clusters):
        def key_fn(cluster):
            rep = cluster[0]
            hexv = rep['default_value']
            br = _hex_brightness(hexv)
            sat = _hex_saturation(hexv)
            usage = -len((css_var_to_elements or {}).get(rep['var'], '').split(','))
            if role == 'accent':
                # 主色：高饱和度 + 适中亮度优先；剔除接近白/黑的（饱和度极低）
                # 排序 key：(饱和度倒序, 使用频次倒序)
                return (-sat, usage)
            if role == 'text':
                # 文字：暗的优先（正文一般是 #1A1A1A / #333）
                return (br, usage)
            if role == 'bg':
                # 背景：亮的优先（页面底一般是浅色）
                return (-br, usage)
            if role == 'border':
                # 分割线：中等亮度优先
                return (abs(br - 200), usage)
            return (usage,)
        # 同 cluster 内也排序（rep = 最合适那个）
        for c in clusters:
            c.sort(key=lambda r: key_fn([r]))
        clusters.sort(key=key_fn)
        return clusters

    role_clusters = {r: _sort_clusters(r, _cluster(buckets[r])) for r in COLOR_ROLE_GROUPS}

    # 进一步：accent 组剔除饱和度 < 0.15 的（当成"准灰色"，不该是"主色"）
    # 被剔除的变量记录下来，后面统一映射到其他角色的代表（避免 PEM row 丢失）
    accent_filtered_out = [c for c in role_clusters['accent'] if _hex_saturation(c[0]['default_value']) < 0.15]
    role_clusters['accent'] = [c for c in role_clusters['accent'] if _hex_saturation(c[0]['default_value']) >= 0.15]

    # Step 4: 取每组前 MAX_PER_GROUP；剩下的也并入代表
    display_groups = []
    var_to_group = {}
    total = 0

    # 用更友好的 cluster label
    def _friendly_label(role, idx, rep_var, rep_value):
        # 优先用 GOLD_VAR_LABELS
        if rep_var in GOLD_VAR_LABELS:
            return GOLD_VAR_LABELS[rep_var]
        # 用预定义角色 label
        if role == 'accent':
            return ['主色 Brand', '辅强调 Accent 2', '辅强调 Accent 3'][idx] if idx < 3 else f'强调 Accent {idx+1}'
        if role == 'text':
            return ['正文 Body', '次要 Muted', '弱化 Subtle'][idx] if idx < 3 else f'文字 Text {idx+1}'
        if role == 'bg':
            return ['页面底色 Page Bg', '卡片底色 Card Bg', 'Banner 底色 Banner Bg'][idx] if idx < 3 else f'背景 Bg {idx+1}'
        if role == 'border':
            return ['主分割线 Divider', '卡片描边 Card Border', '辅分割线 Divider 2'][idx] if idx < 3 else f'边框 Border {idx+1}'
        return _generate_heuristic_label(rep_var)

    for role in COLOR_ROLE_GROUPS:
        clusters = role_clusters.get(role, [])
        kept = clusters[:MAX_PER_GROUP]
        spilled = clusters[MAX_PER_GROUP:]

        for idx, cluster in enumerate(kept):
            rep = cluster[0]
            label = _friendly_label(role, idx, rep['var'], rep['default_value'])
            display_groups.append({
                'role': role,
                'role_label_zh': COLOR_ROLE_LABELS[role][0].split(' ')[0],
                'role_label_en': COLOR_ROLE_LABELS[role][0].split(' ', 1)[-1] if ' ' in COLOR_ROLE_LABELS[role][0] else '',
                'role_i18n_key': COLOR_ROLE_LABELS[role][1],
                'var': rep['var'],
                'label': label,
                'default_value': rep['default_value'],
                'aliases': [r['var'] for r in cluster[1:]],
            })
            total += 1
            # 同组所有变量都映射到 representative
            for r in cluster:
                var_to_group[r['var']] = rep['var']
            if total >= MAX_TOTAL_DISPLAY:
                break
        # 溢出的 cluster：仍然把它们的变量映射到本组第一个代表（保持一致改色）
        if kept and spilled:
            anchor_rep = kept[0][0]['var']
            for cluster in spilled:
                for r in cluster:
                    var_to_group.setdefault(r['var'], anchor_rep)

        if total >= MAX_TOTAL_DISPLAY:
            break

    # 兜底：每个 raw color row 都必须有 representative（accent_filtered_out 可能落单 + 角色过满溢出）
    # 找一个全局 fallback rep：优先 bg 第一个、其次 accent 第一个、其次 text 第一个
    fallback_rep = None
    for r in ['bg', 'accent', 'text', 'border']:
        if role_clusters.get(r):
            fallback_rep = role_clusters[r][0][0]['var']
            break
    if fallback_rep:
        for cluster in accent_filtered_out:
            for row in cluster:
                var_to_group.setdefault(row['var'], fallback_rep)
        for row in color_rows:
            var_to_group.setdefault(row['var'], fallback_rep)

    return display_groups, var_to_group


# ============================================================
# v1.7.0: 字号面板收敛（todo26）
# 把 25 个 raw slider 合并为 ≤10 个；重复的 strong/data/upcoming/event 等族群合 1
# ============================================================
SIZE_FAMILY_PATTERNS = [
    # 顺序敏感：越精确的 kw 越往前；section-title 等放在 section h2 之前
    {'kw': ['.section-title', 'section-title', '.section h2', 'section h2', 'h2'], 'family': 'section', 'label': '章节标题 Section Title', 'group': '标题层级 Heading'},
    {'kw': ['header h1', '.header h1', '.banner h1', 'banner h1', 'h1'],          'family': 'h1',       'label': '主标题 H1',              'group': '标题层级 Heading'},
    {'kw': ['.section-icon', 'section-icon'],                                     'family': 'sec_icon', 'label': '章节图标 Section Icon',  'group': '标题层级 Heading'},
    {'kw': ['.section h3', '.section h4', 'h3'],                                  'family': 'h3',       'label': '三级标题 Section H3',    'group': '标题层级 Heading'},
    {'kw': ['.stat-card .number', 'stat-card .number', '.stat-num', 'stat-num', 'number'], 'family': 'stat_num', 'label': '数字大字 Stat Number', 'group': '标题层级 Heading'},
    {'kw': ['.banner-sub', 'banner-sub', '.subtitle', 'subtitle', '.banner-tag', 'banner-tag'], 'family': 'subtitle', 'label': '副标题 / Banner 标签 Subtitle', 'group': '标题层级 Heading'},
    {'kw': ['.section p', 'p ', 'body', '.lead'],                                 'family': 'body',     'label': '正文 Body',              'group': '正文层级 Body'},
    {'kw': ['li ', '.section ul', '.section ol'],                                 'family': 'list',     'label': '列表项 List',            'group': '正文层级 Body'},
    {'kw': ['strong', 'b '],                                                      'family': 'strong',   'label': '加粗强调 Strong',        'group': '正文层级 Body'},
    {'kw': ['.upcoming', 'upcoming-', '.next-card', 'next-card'],                 'family': 'upcoming', 'label': 'Upcoming 区块 Upcoming', 'group': '正文层级 Body'},
    {'kw': ['.event', 'event-'],                                                  'family': 'event',    'label': 'Event 区块 Event',       'group': '正文层级 Body'},
    {'kw': ['data-', '.data-', 'data row'],                                       'family': 'data',     'label': '数据文字 Data Text',     'group': '正文层级 Body'},
    {'kw': ['.badge', '.tag ', ' .tag', '.ptag', '.pill'],                        'family': 'tag',      'label': '标签 Tag',               'group': '辅助 Auxiliary'},
    {'kw': ['.footer', 'footer'],                                                 'family': 'footer',   'label': '页脚 Footer',            'group': '辅助 Auxiliary'},
    {'kw': ['th ', 'td ', ' th', ' td', 'table'],                                 'family': 'table',    'label': '表格 Table',             'group': '辅助 Auxiliary'},
    {'kw': ['.meta', ' meta'],                                                    'family': 'meta',     'label': '元信息 Meta',            'group': '辅助 Auxiliary'},
]
MAX_SIZE_SLIDERS = 10


def _match_size_family(selector: str):
    """把一个 selector 匹配到某个 family；找不到返回 None。

    用 regex 词边界匹配，避免 'p' 在 '.upcoming' 里乱命中。
    """
    sel_lower = selector.lower().strip()
    # 裸 tag 直接命中
    BARE_TAG_MAP = {
        'th': 'table', 'td': 'table', 'table': 'table',
        'h1': 'h1', 'h2': 'section', 'h3': 'h3',
        'p': 'body', 'li': 'list', 'strong': 'strong',
    }
    if sel_lower in BARE_TAG_MAP:
        target_fam = BARE_TAG_MAP[sel_lower]
        for fam in SIZE_FAMILY_PATTERNS:
            if fam['family'] == target_fam:
                return fam
    # 关键词包含匹配（按 pattern 顺序）
    for fam in SIZE_FAMILY_PATTERNS:
        for kw in fam['kw']:
            if kw and kw.lower() in sel_lower:
                return fam
    # 兜底：包含某些常见 class 关键词
    FALLBACK_KW = [
        ('summary', 'subtitle'), ('banner', 'subtitle'),
        ('timeline', 'body'), ('meta', 'meta'),
        ('label', 'tag'), ('caption', 'meta'),
    ]
    for kw, target_fam in FALLBACK_KW:
        if kw in sel_lower:
            for fam in SIZE_FAMILY_PATTERNS:
                if fam['family'] == target_fam:
                    return fam
    return None


def _collapse_size_sliders(size_sliders: list) -> tuple:
    """
    把原始 size_sliders 收敛为 ≤10 个面板项。
    返回 (display_sliders, target_to_family):
      display_sliders: [{family, label, group, target (合并 selector), prop, unit, min, max, default, step, key, aliases (合并的目标 selector 列表)}]
      target_to_family: {original_target: family_key}  -- 给前端用：调代表时同步刷其他选择器

    策略：
    - 每个 family 选默认 px 最大的为代表（视觉影响最大）
    - target 用逗号拼接全部 alias，应用时一并改
    - 同 family 重复条目丢弃
    """
    families = {}  # family_key -> {'rep': slider, 'aliases': [target_str, ...], 'group': str, 'label': str}
    unmatched = []  # 没匹配到 family 的原样保留（但仍受 MAX_SIZE_SLIDERS 限制）

    for s in size_sliders:
        fam = _match_size_family(s['target'])
        if not fam:
            unmatched.append(s)
            continue
        key = fam['family']
        if key not in families:
            families[key] = {
                'rep': s,
                'aliases': [s['target']],
                'group': fam['group'],
                'label': fam['label'],
            }
        else:
            # 已有 -- 若当前 slider 默认 px 更大，更新为 rep
            if float(s['default']) > float(families[key]['rep']['default']):
                families[key]['rep'] = s
            families[key]['aliases'].append(s['target'])

    # 转为 list；按 group 顺序 + 同组内按默认 px 倒序
    GROUP_ORDER = ['标题层级 Heading', '正文层级 Body', '辅助 Auxiliary']
    items = []
    for f in families.values():
        rep = dict(f['rep'])
        # 合并 target
        rep['target'] = ', '.join(dict.fromkeys(f['aliases']))  # 去重保序
        rep['label'] = f['label']
        rep['group'] = f['group']
        rep['family'] = next((k for k, v in families.items() if v is f), '')
        rep['aliases'] = f['aliases']
        items.append(rep)

    items.sort(key=lambda x: (GROUP_ORDER.index(x['group']) if x['group'] in GROUP_ORDER else 99, -float(x['default'])))
    # 加上没匹配的（罕见）
    for s in unmatched:
        ss = dict(s)
        ss['group'] = '辅助 Auxiliary'
        ss['family'] = ''
        ss['aliases'] = [s['target']]
        items.append(ss)
    # 截断
    items = items[:MAX_SIZE_SLIDERS]

    # target_to_family 反向表
    target_to_family = {}
    for it in items:
        for a in it.get('aliases', []):
            target_to_family[a] = it['target']

    return items, target_to_family


def _generate_heuristic_label(var_name: str) -> str:
    """启发式生成 label (R2.3 格式: 中文语义 英文PascalCase)"""
    if var_name in GOLD_VAR_LABELS:
        return GOLD_VAR_LABELS[var_name]

    name = var_name.lstrip('-')
    parts = re.split(r'[-_]', name)
    parts = [w for w in parts if w]

    # 中文映射
    WORD_MAP = {
        'primary': '主色', 'secondary': '次色', 'accent': '主色调',
        'bg': '页面底色', 'background': '背景', 'text': '文字',
        'card': '卡片', 'surface': '表面', 'border': '边框',
        'title': '标题', 'body': '正文', 'heading': '标题',
        'blue': '蓝色', 'red': '红色', 'green': '绿色', 'purple': '紫色',
        'orange': '橙色', 'yellow': '黄色', 'pink': '粉色', 'white': '白色',
        'black': '黑色', 'gray': '灰色', 'grey': '灰色', 'dark': '深色',
        'light': '浅色', 'muted': '弱化', 'subtle': '淡化',
        'ink': '文字', 'warm': '暖色', 'gold': '金色', 'sage': '青绿',
        'soft': '浅', 'line': '分割线',
        'color': '色', 'hover': '悬停', 'active': '激活',
        'success': '成功', 'warning': '警告', 'danger': '危险', 'info': '信息',
        'link': '链接', 'shadow': '阴影', 'radius': '圆角',
    }

    zh_parts = []
    for p in parts:
        zh_parts.append(WORD_MAP.get(p.lower(), p))
    zh_label = ''.join(zh_parts)

    en_label = ' '.join(w.capitalize() for w in parts)

    return f"{zh_label} {en_label}"


def _try_llm_labels(variables_info: list) -> dict:
    """
    尝试调用 LLM 生成语义化 label (Step 10)。
    返回 {var_name: label_string} 或 None（降级到启发式）。
    """
    import os

    api_key = os.environ.get('ANTHROPIC_API_KEY', '')
    api_type = 'anthropic'
    if not api_key:
        api_key = os.environ.get('OPENAI_API_KEY', '')
        api_type = 'openai'
    if not api_key:
        print("  [warning] 未配置 LLM API，使用启发式 label，可能不如人工命名优雅")
        return None

    # Load prompt template
    prompt_path = PRESETS_DIR / 'llm_label_prompt.txt'
    if not prompt_path.exists():
        print("  [warning] 缺少 llm_label_prompt.txt，降级到启发式")
        return None

    with open(prompt_path, 'r', encoding='utf-8') as f:
        prompt_template = f.read()

    variables_json = json.dumps(variables_info, ensure_ascii=False, indent=2)
    prompt = prompt_template.replace('{variables_json}', variables_json)

    try:
        import requests

        if api_type == 'anthropic':
            resp = requests.post(
                'https://api.anthropic.com/v1/messages',
                headers={
                    'x-api-key': api_key,
                    'anthropic-version': '2023-06-01',
                    'content-type': 'application/json',
                },
                json={
                    'model': 'claude-sonnet-4-20250514',
                    'max_tokens': 1024,
                    'messages': [{'role': 'user', 'content': prompt}],
                },
                timeout=30,
            )
            if resp.status_code == 200:
                content = resp.json()['content'][0]['text']
                return json.loads(content)
        elif api_type == 'openai':
            resp = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json',
                },
                json={
                    'model': 'gpt-4o-mini',
                    'messages': [{'role': 'user', 'content': prompt}],
                    'max_tokens': 1024,
                },
                timeout=30,
            )
            if resp.status_code == 200:
                content = resp.json()['choices'][0]['message']['content']
                # Extract JSON from possible markdown wrapping
                json_match = re.search(r'\{[^{}]*\}', content, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
    except Exception as e:
        print(f"  [warning] LLM 调用失败 ({e})，降级到启发式")
        return None

    print("  [warning] LLM 返回异常，降级到启发式")
    return None


def _build_label_for(parse_result, scan_result) -> dict:
    """
    构建 LABEL_FOR single-source-of-truth (附录 C)。
    先尝试 LLM，失败则用启发式。
    """
    global LABEL_FOR
    LABEL_FOR = {}

    color_vars = [v for v in parse_result.variables if v.semantic == 'color']

    # 尝试 LLM labeling
    variables_info = []
    for v in color_vars:
        usages = parse_result.var_to_selectors.get(v.name, [])
        selectors = [sel for sel, prop in usages]
        variables_info.append({
            'name': v.name,
            'value': v.raw_value,
            'used_in': selectors[:5],
        })

    llm_labels = _try_llm_labels(variables_info)

    # 颜色 tab labels
    for v in color_vars:
        if llm_labels and v.name in llm_labels:
            label = llm_labels[v.name]
        else:
            label = _generate_heuristic_label(v.name)
        LABEL_FOR[('颜色', v.name)] = label

    # 字号 tab labels: 从 scan_result 推断
    # 查找 host 中实际的文本元素，生成 slider 配置
    _build_size_labels(parse_result, scan_result)

    # 布局 tab labels: 从 scan_result 推断
    _build_layout_labels(parse_result, scan_result)

    return LABEL_FOR


def _build_size_labels(parse_result, scan_result):
    """为字号 tab 构建 LABEL_FOR 条目"""
    from bs4 import BeautifulSoup

    present = scan_result.present_elements or {}

    # 按金版规范 R3.2-R3.4，为每种文本元素建立一条 slider
    # 需要用真实 DOM 选择器
    TAG_LABEL_MAP = {
        'h1': ('主标题 Title (h1)', 'h1'),
        'h2': ('二级标题 H2', 'h2'),
        'h3': ('卡片标题 H3', 'h3'),
        'h4': ('四级标题 H4', 'h4'),
        'p': ('正文 Body', 'body'),
        'li': ('列表项 List', 'list'),
    }

    # 尝试找到真实的限定选择器
    for elem in scan_result.elements:
        if not elem.is_text:
            continue
        tag = elem.tag if hasattr(elem, 'tag') else elem.selector.split()[-1].split('.')[0].split(':')[0]
        if tag in TAG_LABEL_MAP and tag in present:
            label, key = TAG_LABEL_MAP[tag]
            selector = elem.selector
            # Use the element's actual selector as data-target
            existing_key = ('字号', selector)
            if existing_key not in LABEL_FOR:
                LABEL_FOR[existing_key] = label

    # 确保至少覆盖 present 中有的 tags（如果没从 elements 里找到）
    for tag in ['h1', 'h2', 'h3', 'p']:
        if tag in present:
            label, key = TAG_LABEL_MAP.get(tag, (tag, tag))
            # Check if we already have a label for this tag
            found = False
            for (tab, sel), lab in LABEL_FOR.items():
                if tab == '字号' and (sel == tag or sel.endswith(f' {tag}')):
                    found = True
                    break
            if not found:
                LABEL_FOR[('字号', tag)] = label


def _build_layout_labels(parse_result, scan_result):
    """为布局 tab 构建 LABEL_FOR 条目"""
    from bs4 import BeautifulSoup

    # 按 R4.2 必含维度列表
    LAYOUT_DIMS = [
        ('页面宽度 Page Width', '.page', 'max-width', 'px', 640, 1400, 20, 960, 'page-w'),
        ('页面左右内距', '.page', 'padding-left', 'px', 16, 120, 4, 56, 'page-pad'),
        ('段落最大宽 Lead', '.masthead .lead, .section-intro', 'max-width', 'px', 400, 960, 10, 680, 'lead-w'),
        ('章节间距 Section Gap', 'section', 'margin-bottom', 'px', 16, 120, 4, 68, 'sec-gap'),
        ('中台卡片间距 ZT Gap', '.zt-grid', 'gap', 'px', 4, 40, 2, 14, 'zt-gap'),
        ('卡片内边距 Card Padding', '.zt-card', 'padding', 'px', 8, 40, 2, 20, 'card-pad'),
    ]

    for label, target, prop, unit, min_v, max_v, step, default, key in LAYOUT_DIMS:
        LABEL_FOR[('布局', target)] = label


def generate_panel(parse_result, scan_result) -> PanelConfig:
    """根据分析结果生成完整的面板配置。"""

    # Step 11: 构建 LABEL_FOR
    label_for = _build_label_for(parse_result, scan_result)

    # === 颜色行 ===
    color_vars = [v for v in parse_result.variables if v.semantic == 'color']
    color_rows = []
    for v in color_vars:
        label = label_for.get(('颜色', v.name), _generate_heuristic_label(v.name))
        color_rows.append({
            'var': v.name,
            'label': label,
            'default_value': v.raw_value
        })

    # === v1.7.0 todo25/26 → v1.8.0 todo38/39/44 数据驱动: 颜色面板收敛 ===
    css_var_to_elements = getattr(scan_result, 'css_var_to_elements', {}) or {}
    color_usage = getattr(scan_result, 'color_usage', None)
    display_color_groups, color_var_to_rep = _collapse_color_rows(color_rows, css_var_to_elements, color_usage)

    # 注：PEM 重写发生在 adapt.py 的步骤 4.7（在第二次 scan_dom 之后）

    # === 字号滑块 (R3) ===
    size_sliders = _build_size_sliders(parse_result, scan_result, label_for)
    # === v1.7.0 todo26: 字号面板收敛 ===
    display_size_sliders, size_target_to_family = _collapse_size_sliders(size_sliders)
    # 注：PEM 重写发生在 adapt.py 步骤 4.7（在第二次 scan_dom 之后）

    # === 布局滑块 (R4) ===
    layout_sliders = _build_layout_sliders(parse_result, scan_result, label_for)

    # === 预设主题 (R5) ===
    preset_themes = _build_presets(color_rows)

    # === 生成 Panel HTML ===
    panel_html = _build_panel_html(
        color_rows, size_sliders, layout_sliders, preset_themes,
        display_color_groups=display_color_groups,
        display_size_sliders=display_size_sliders,
    )

    # === 生成 Toolbar HTML (R14) ===
    toolbar_html = _build_toolbar_html(scan_result.page_structure, scan_result.has_nav_dots)

    # === 生成 window.X 常量 JS ===
    constants_js = _build_constants_js(
        color_rows, size_sliders, preset_themes,
        scan_result.page_element_to_panel,
        scan_result.css_var_to_elements,
        color_var_to_rep=color_var_to_rep,
        size_target_to_family=size_target_to_family,
    )

    return PanelConfig(
        color_rows=color_rows,
        preset_themes=preset_themes,
        layout_sliders=layout_sliders,
        size_sliders=size_sliders,
        panel_html=panel_html,
        toolbar_html=toolbar_html,
        constants_js=constants_js,
        label_for=label_for,
        display_color_groups=display_color_groups,
        display_size_sliders=display_size_sliders,
        color_var_to_rep=color_var_to_rep,
        size_target_to_family=size_target_to_family,
    )


def _build_size_sliders(parse_result, scan_result, label_for) -> list:
    """
    构建字号 slider 列表 (R3)。

    v15 修复: 不再硬编码 [h1, h2, h3, h4, p, li] 6 个 fallback slider。
    改为从 parse_result.rules 反推所有声明了 font-size 的 CSS 规则，
    每条规则生成一个 slider（去重 / 验证 / 跳过编辑器自身选择器）。
    """
    from bs4 import BeautifulSoup
    # _html 是 scan_dom 时的 HTML 快照（包含 gradient + solid 预处理后的变量替换，
    # 但不含最终注入的编辑器代码）。用于 DOM 验证——检查 CSS 选择器是否匹配实际元素。
    html_src = scan_result._html if hasattr(scan_result, '_html') else ''
    soup = BeautifulSoup(html_src, 'html.parser') if html_src else None

    # 编辑器自身的 selector 前缀，反推时跳过
    EDITOR_SELECTOR_KEYWORDS = (
        'toolbar', 'edit-panel', 'edit-hint', 'panel-tab', 'panel-section',
        'panel-actions', 'panel-close', 'panel-header', 'panel-title',
        'color-row', 'color-label', 'color-swatch', 'color-hex',
        'slider-row', 'slider-label', 'slider-name', 'slider-val',
        'preset-row', 'preset-btn', 'action-btn', 'toolbar-btn',
        'btn-icon', 'save-indicator', 'toolbar-divider',
        'html-visual-editor',
    )

    sliders = []
    seen_selectors = set()
    used_keys = set()

    # v15: 清除可能由 _build_size_labels 旧逻辑留下的 字号 LABEL_FOR 条目
    # 我们只信任本函数从 CSS 反推出的 (selector, label)
    stale_keys = [k for k in label_for if isinstance(k, tuple) and len(k) == 2 and k[0] == '字号']
    for k in stale_keys:
        del label_for[k]
    # 同步清理全局 LABEL_FOR（_build_label_for 写过的）
    try:
        for k in [kk for kk in LABEL_FOR if isinstance(kk, tuple) and len(kk) == 2 and kk[0] == '字号']:
            del LABEL_FOR[k]
    except Exception:
        pass

    def _make_key(selector: str) -> str:
        """Generate a safe DOM id-friendly key from selector."""
        k = re.sub(r'[^\w]+', '-', selector).strip('-').lower()
        if not k:
            k = 'size'
        # Ensure uniqueness
        base = k
        i = 2
        while k in used_keys:
            k = f"{base}-{i}"
            i += 1
        used_keys.add(k)
        return k

    def _bounds_for(default_px: float) -> dict:
        """从默认字号推算 slider 范围 (0.5x ~ 2x)"""
        default_px = float(default_px)
        min_v = max(8, round(default_px * 0.5))
        max_v = max(min_v + 4, round(default_px * 2))
        step = 0.5 if default_px <= 14 else 1
        return {'min': min_v, 'max': max_v, 'step': step}

    # 主循环：从 CSS 规则反推
    rules = getattr(parse_result, 'rules', None) or []
    for rule in rules:
        props = getattr(rule, 'properties', {}) or {}
        if 'font-size' not in props:
            continue

        selector = (getattr(rule, 'selector', '') or '').strip()
        if not selector:
            continue

        # 去掉 CSS 注释 /* ... */ (selector 里偶尔被解析器捎进来)
        selector = re.sub(r'/\*.*?\*/', '', selector, flags=re.DOTALL).strip()
        # 归一化空白（换行 / 多空格 → 单空格）
        selector = re.sub(r'\s+', ' ', selector)
        if not selector:
            continue

        # 跳过编辑器自身 selector
        sel_lower = selector.lower()
        if any(kw in sel_lower for kw in EDITOR_SELECTOR_KEYWORDS):
            continue

        # 多选择器组（用逗号分隔）拆开处理
        for sub_sel in [s.strip() for s in selector.split(',') if s.strip()]:
            # 跳过 @-rule / pseudo-only
            if sub_sel.startswith('@') or sub_sel.startswith(':root'):
                continue

            # 验证选择器在 host DOM 中真实存在
            if soup is not None:
                try:
                    found = soup.select(sub_sel)
                    if not found:
                        continue
                except Exception:
                    continue

            if sub_sel in seen_selectors:
                continue
            seen_selectors.add(sub_sel)

            # 解析默认字号 (例如 "28px" / "1.2em" / "clamp(...)" )
            fs_value = props['font-size'].strip()
            parsed = _parse_size_value(fs_value)
            default_px = parsed['default']
            unit = parsed['unit'] if parsed['unit'] in ('px', 'em', 'rem') else 'px'

            bounds = _bounds_for(default_px)

            label = _generate_size_label(sub_sel)
            label_for[('字号', sub_sel)] = label

            sliders.append({
                'target': sub_sel,
                'prop': 'font-size',
                'label': label,
                'min': bounds['min'],
                'max': bounds['max'],
                'default': default_px,
                'unit': unit,
                'step': bounds['step'],
                'key': _make_key(sub_sel),
            })

    # 排序：按默认字号从大到小
    sliders.sort(key=lambda s: -float(s['default']))

    return sliders


# ============================================================
# 字号 slider label 推断 (v15)
# ============================================================
SIZE_SLIDER_LABEL_MAP = {
    # header 体系
    '.header h1':                ('主标题 Header H1', 'header-h1'),
    '.header .subtitle':         ('副标题 Subtitle', 'subtitle'),
    '.header .meta':             ('元信息 Meta', 'meta'),
    # section 体系
    '.section h2':               ('章节标题 Section H2', 'section-h2'),
    '.section h3':               ('三级标题 Section H3', 'section-h3'),
    '.section p':                ('正文 Body', 'body'),
    # stat-card 数字看板
    '.stat-card .number':        ('数字大字 Stat Number', 'stat-number'),
    '.stat-card .label':         ('数字标签 Stat Label', 'stat-label'),
    # 表格
    'th':                        ('表头 Table Header', 'th'),
    'td':                        ('单元格 Table Cell', 'td'),
    'table':                     ('表格 Table', 'table'),
    # badge / ptag
    '.badge':                    ('状态徽章 Badge', 'badge'),
    '.ptag':                     ('优先级标签 Priority Tag', 'ptag'),
    # 组织盒子
    '.org-box h4':               ('组织标题 Org H4', 'org-h4'),
    '.org-box .role':            ('角色 Role', 'org-role'),
    '.org-box ul li':            ('组织列表 Org List', 'org-list'),
    # 时间轴
    '.timeline-item .t-date':    ('时间轴日期 Timeline Date', 'timeline-date'),
    '.timeline-item .t-content': ('时间轴内容 Timeline Content', 'timeline-content'),
    # next-card
    '.next-card .num':           ('Next 数字 Next Num', 'next-num'),
    '.next-card .desc':          ('Next 描述 Next Desc', 'next-desc'),
    '.next-card .detail':        ('Next 细节 Next Detail', 'next-detail'),
    # 其它
    '.footer':                   ('页脚 Footer', 'footer'),
    '.support-item':             ('支持项 Support Item', 'support-item'),
    '.summary-banner':           ('汇总条 Summary Banner', 'summary-banner'),
    # 裸 heading（金版兜底）
    'h1': ('主标题 H1', 'h1'),
    'h2': ('二级标题 H2', 'h2'),
    'h3': ('三级标题 H3', 'h3'),
    'h4': ('四级标题 H4', 'h4'),
    'h5': ('五级标题 H5', 'h5'),
    'h6': ('六级标题 H6', 'h6'),
    'p':  ('正文 Body', 'body'),
    'li': ('列表项 List', 'list'),
    'body': ('页面正文 Page Body', 'page-body'),
}


_CHINESE_LABEL_WORDS = {
    'header': '头部', 'footer': '页脚', 'subtitle': '副标题',
    'meta': '元信息', 'section': '章节', 'card': '卡片',
    'stat': '数字', 'number': '数字', 'label': '标签',
    'badge': '徽章', 'tag': '标签', 'org': '组织', 'role': '角色',
    'timeline': '时间轴', 'date': '日期', 'content': '内容',
    'next': 'Next', 'num': '数字', 'desc': '描述', 'detail': '细节',
    'summary': '汇总', 'banner': '横幅', 'support': '支持', 'item': '项',
    'title': '标题', 'body': '正文', 'list': '列表', 'box': '盒子',
    'grid': '网格', 'row': '行', 'col': '列', 'block': '块',
    'page': '页面', 'main': '主体', 'side': '侧栏', 'aside': '侧栏',
    'nav': '导航', 'menu': '菜单', 'btn': '按钮', 'button': '按钮',
    'link': '链接', 'text': '文字', 'lead': '导语', 'intro': '简介',
    'caption': '说明', 'note': '备注', 'tip': '提示', 'hint': '提示',
    'name': '名称', 'value': '值', 'desc': '描述',
}


def _generate_size_label(selector: str) -> str:
    """
    根据选择器生成中英双语 label (v15)。
    优先查 SIZE_SLIDER_LABEL_MAP；否则按选择器最后一段做启发式中文化。
    """
    sel = selector.strip()
    if sel in SIZE_SLIDER_LABEL_MAP:
        return SIZE_SLIDER_LABEL_MAP[sel][0]

    # 取最后一段做语义推断
    last = sel.split()[-1] if ' ' in sel else sel
    last = last.split('>')[-1].strip()

    # 拆出 class / tag
    # 形如 .foo-bar / .foo / div.bar / h2 / .a.b
    classes = re.findall(r'\.([\w-]+)', last)
    tag_match = re.match(r'^([a-zA-Z][\w-]*)', last)
    tag = tag_match.group(1) if tag_match else ''

    # 用 classes + tag 拼 label
    name_parts = []
    for cls in classes:
        name_parts.extend(re.split(r'[-_]', cls))
    if tag and tag.lower() not in {'div', 'span'}:
        name_parts.append(tag)
    name_parts = [p for p in name_parts if p]

    if not name_parts:
        # 兜底：用整个 selector
        name_parts = [re.sub(r'[^\w]+', '-', sel).strip('-') or 'size']

    zh = ''.join(_CHINESE_LABEL_WORDS.get(p.lower(), p) for p in name_parts)
    en = ' '.join(w.capitalize() for w in name_parts)
    return f"{zh} {en}"


def _build_layout_sliders(parse_result, scan_result, label_for) -> list:
    """
    构建布局 slider 列表 (R4)。
    必含 6 条: 页面宽度/左右内距/段落最大宽/章节间距/卡片间距/卡片内边距。
    对每条 slider，验证 data-target 在 host DOM 中可 querySelector 到，否则用 fallback 替换 (P0-2)。
    """
    from bs4 import BeautifulSoup
    html_src = scan_result._html if hasattr(scan_result, '_html') else ''
    soup = BeautifulSoup(html_src, 'html.parser') if html_src else None

    LAYOUT_DIMS = [
        {'label': '页面宽度 Page Width', 'target': '.page', 'prop': 'max-width', 'unit': 'px', 'min': 640, 'max': 1400, 'step': 20, 'default': 960, 'key': 'page-w', 'section': '页面尺寸 Page Size'},
        {'label': '页面左右内距 Page Padding', 'target': '.page', 'prop': 'padding-left', 'unit': 'px', 'min': 16, 'max': 120, 'step': 4, 'default': 56, 'key': 'page-pad', 'section': '页面尺寸 Page Size'},
        {'label': '段落最大宽 Lead Width', 'target': '.masthead .lead, .section-intro', 'prop': 'max-width', 'unit': 'px', 'min': 400, 'max': 960, 'step': 10, 'default': 680, 'key': 'lead-w', 'section': '页面尺寸 Page Size'},
        {'label': '行高 Line Height', 'target': 'body', 'prop': 'line-height', 'unit': '', 'min': 1.2, 'max': 2.2, 'step': 0.05, 'default': 1.6, 'key': 'line-h', 'section': '页面尺寸 Page Size'},
        {'label': '章节间距 Section Gap', 'target': 'section', 'prop': 'margin-bottom', 'unit': 'px', 'min': 16, 'max': 120, 'step': 4, 'default': 68, 'key': 'sec-gap', 'section': '章节间距 Section Gap'},
        {'label': '卡片间距 Card Gap', 'target': '.zt-grid', 'prop': 'gap', 'unit': 'px', 'min': 4, 'max': 40, 'step': 2, 'default': 14, 'key': 'card-gap', 'section': '卡片网格 Card Grid'},
        {'label': '卡片内边距 Card Padding', 'target': '.zt-card', 'prop': 'padding', 'unit': 'px', 'min': 8, 'max': 40, 'step': 2, 'default': 20, 'key': 'card-pad', 'section': '卡片网格 Card Grid'},
    ]

    sliders = []
    for dim in LAYOUT_DIMS:
        original_target = dim['target']
        if soup is not None:
            resolved = _resolve_layout_target(original_target, soup)
            if resolved:
                dim = dict(dim)
                dim['target'] = resolved
            else:
                # 无法解析时仍保留原 target（避免 6 条 slider 数量缩水）
                pass
        sliders.append(dim)

    return sliders


def _build_presets(color_rows: list) -> dict:
    """
    构建 PRESETS flat 格式。
    todo23: builtin 预设不再"应用 CSS 变量"，改为复制 prompt（HVE_STYLE_PRESETS）。
            此函数仅产出 'original'（host 默认值）供 resetAll 使用。
    """
    preset_themes = {}

    # "original" 预设：HTML 自身的默认颜色值（供 reset 用）
    original_vars = {}
    for row in color_rows:
        original_vars[row['var']] = row['default_value']
    if original_vars:
        preset_themes['original'] = original_vars

    return preset_themes


def _build_panel_html(color_rows: list, size_sliders: list, layout_sliders: list, preset_themes: dict,
                       display_color_groups: list = None, display_size_sliders: list = None) -> str:
    """组装完整的 panel HTML

    v1.7.0: 若提供 display_color_groups / display_size_sliders，则面板用收敛后版本渲染，
            底层 color_rows / size_sliders 仍传给 constants_js（保证导出 HTML 渲染不被破坏）。
    """
    template_path = ASSETS_DIR / 'panel.template.html'
    if template_path.exists():
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
    else:
        template = _get_fallback_panel_template()

    # === 颜色 tab 内容 (v1.7.0: 4 角色分组) ===
    color_tab_parts = []
    if display_color_groups:
        ROLE_TITLE = {
            'text':   '文字 Text',
            'bg':     '背景 Background',
            'border': '边框 / 分割线 Border',
            'accent': '强调 / 主色 Accent',  # 仅兼容旧 legacy 数据
        }
        # v1.8.0: 渲染顺序 text → bg → border（数据驱动后没有 accent）
        RENDER_ORDER = ['text', 'bg', 'border', 'accent']
        by_role = {}
        for g in display_color_groups:
            by_role.setdefault(g['role'], []).append(g)
        for role in RENDER_ORDER:
            items = by_role.get(role, [])
            if not items:
                continue
            color_tab_parts.append('    <div class="panel-section">')
            color_tab_parts.append(f'        <div class="panel-section-title">{ROLE_TITLE.get(role, role)}</div>')
            for g in items:
                color_tab_parts.append(_generate_color_row_html(g['var'], g['label'], g['default_value']))
            color_tab_parts.append('    </div>')
    else:
        # fallback 旧行为
        theme_colors = []
        text_colors = []
        for row in color_rows:
            section = _classify_color_section(row['var'])
            html = _generate_color_row_html(row['var'], row['label'], row['default_value'])
            if section == '文字色':
                text_colors.append(html)
            else:
                theme_colors.append(html)
        if theme_colors:
            color_tab_parts.append('    <div class="panel-section">')
            color_tab_parts.append('        <div class="panel-section-title">主题色板 Theme</div>')
            color_tab_parts.extend(theme_colors)
            color_tab_parts.append('    </div>')
        if text_colors:
            color_tab_parts.append('    <div class="panel-section">')
            color_tab_parts.append('        <div class="panel-section-title">文字色 Text</div>')
            color_tab_parts.extend(text_colors)
            color_tab_parts.append('    </div>')

    if not color_tab_parts:
        color_tab_parts.append('    <p class="empty-hint">未检测到颜色变量</p>')

    color_tab_content = '\n'.join(color_tab_parts)

    # === 字号 tab 内容 (v1.7.0: 3 组分段) ===
    sliders_to_render = display_size_sliders if display_size_sliders is not None else size_sliders
    size_tab_parts = []
    if sliders_to_render:
        SIZE_GROUP_ORDER = ['标题层级 Heading', '正文层级 Body', '辅助 Auxiliary']
        sec_map = {}
        for s in sliders_to_render:
            sec = s.get('group', '标题大小 Size')
            sec_map.setdefault(sec, []).append(s)
        # 按预设顺序优先，其它附后
        ordered = [g for g in SIZE_GROUP_ORDER if g in sec_map] + [g for g in sec_map if g not in SIZE_GROUP_ORDER]
        for sec in ordered:
            size_tab_parts.append('    <div class="panel-section">')
            size_tab_parts.append(f'        <div class="panel-section-title">{sec}</div>')
            for s in sec_map[sec]:
                size_tab_parts.append(_generate_slider_html(
                    s['label'], s['key'], s['target'], s['prop'], s['unit'],
                    s['min'], s['max'], s['step'], s['default']
                ))
            size_tab_parts.append('    </div>')
    else:
        size_tab_parts.append('    <p class="empty-hint">未检测到文本元素</p>')
    size_tab_content = '\n'.join(size_tab_parts)

    # === 布局 tab 内容 (R4.4: 3 个子分段) ===
    layout_tab_parts = []
    sections_map = {}  # section_name -> [(label, slider_html)]
    for s in layout_sliders:
        sec = s.get('section', '间距与布局')
        if sec not in sections_map:
            sections_map[sec] = []
        sections_map[sec].append((s['label'], _generate_slider_html(
            s['label'], s['key'], s['target'], s['prop'], s['unit'],
            s['min'], s['max'], s['step'], s['default']
        )))
    for sec_name, entries in sections_map.items():
        layout_tab_parts.append('    <div class="panel-section">')
        # v1.8.0 todo41: 若 section 只有 1 个 slider 且 label 与 section name 同名，省 section title
        skip_title = False
        if len(entries) == 1:
            slider_lbl = entries[0][0].strip()
            sec_clean = sec_name.strip()
            if slider_lbl == sec_clean or slider_lbl.split(' ')[0] == sec_clean.split(' ')[0]:
                skip_title = True
        if not skip_title:
            layout_tab_parts.append(f'        <div class="panel-section-title">{sec_name}</div>')
        layout_tab_parts.extend(html for _, html in entries)
        layout_tab_parts.append('    </div>')
    if not layout_tab_parts:
        layout_tab_parts.append('    <p class="empty-hint">未检测到布局元素</p>')
    layout_tab_content = '\n'.join(layout_tab_parts)

    # === Style 卡片 (todo23: 点击复制 prompt 给 AI；不再应用 CSS) ===
    # 新 schema：每个 preset 有 id/name_zh/name_en/vibe_zh/vibe_en/palette/is_dark
    # original 不参与卡片渲染（Reset 由 panel 底部按钮承担）
    preset_html_parts = []
    dark_presets = []
    light_presets = []

    builtin_raw = _load_builtin_presets()

    for preset_id, data in builtin_raw.items():
        if not isinstance(data, dict):
            continue
        # 跳过旧 schema（含 vars 字段但无 palette）
        palette = data.get('palette')
        if not isinstance(palette, dict):
            continue

        bg_val     = palette.get('bg',        '#1a1a1a')
        accent_val = palette.get('accent',    '#888888')
        secondary  = palette.get('secondary', accent_val)
        text_val   = palette.get('text',      '#ffffff')
        display_zh = data.get('name_zh', preset_id)
        is_dark    = data.get('is_dark')
        if is_dark is None:
            is_dark = _is_color_dark(bg_val)

        # id snake-case 用于 data-i18n key
        i18n_key = 'preset_name_' + preset_id.replace('-', '_')

        card_html = (
            f'            <div class="preset-card{" preset-card-dark" if is_dark else " preset-card-light"}" '
            f'onclick="copyStylePrompt(\'{preset_id}\')" '
            f'data-preset-id="{preset_id}" '
            f'title="{display_zh}">'
            f'<div class="preset-card-swatch">'
            f'<div class="preset-card-accent" style="background:{accent_val}"></div>'
            f'<div class="preset-card-warm" style="background:{secondary}"></div>'
            f'</div>'
            f'<div class="preset-card-body" style="background:{bg_val};color:{text_val}">'
            f'<span class="preset-card-name" data-i18n="{i18n_key}">{display_zh}</span>'
            f'</div></div>'
        )

        if is_dark:
            dark_presets.append(card_html)
        else:
            light_presets.append(card_html)

    # 浅色组在前，深色组在后
    preset_html_parts.extend(light_presets)
    preset_html_parts.extend(dark_presets)
    presets_html = '\n'.join(preset_html_parts)

    # 填充模板
    panel_html = template.replace('{{COLOR_TAB_CONTENT}}', color_tab_content)
    panel_html = panel_html.replace('{{SIZE_TAB_CONTENT}}', size_tab_content)
    panel_html = panel_html.replace('{{LAYOUT_TAB_CONTENT}}', layout_tab_content)
    panel_html = panel_html.replace('{{PRESET_BUTTONS}}', presets_html)

    return panel_html


def _build_toolbar_html(page_structure: str, has_nav_dots: bool) -> str:
    """生成 toolbar HTML (R14: 金版文案)
    todo20: 所有可翻译文本加 data-i18n，运行时由 editor-core.js 切换中/英。
    """
    toolbar = '''<!-- ======== EDIT TOOLBAR ======== -->
<div class="edit-toolbar" id="editToolbar">
    <div class="toolbar-drag-handle" id="toolbarDragHandle" title="拖动 / Drag"></div>
    <button class="toolbar-btn" id="btnToggleEdit" onclick="toggleEditMode()" title="切换编辑模式 (E)">
        <span class="btn-icon">✏️</span>
        <span id="btnEditText" data-i18n="edit">编辑</span>
    </button>
    <div class="toolbar-divider"></div>
    <button class="toolbar-btn" onclick="saveToStorage()" title="保存 (⌘S)">
        <span class="btn-icon">👁️</span>
        <div class="btn-text-block">
            <span class="btn-text-main" data-i18n="preview">预览</span>
            <span class="btn-text-sub" data-i18n="preview_sub">仅限当前窗口</span>
        </div>
    </button>
    <button class="toolbar-btn" id="btnUndo" onclick="undoLast()" title="撤销上一步 (⌘Z)" disabled>
        <span class="btn-icon">↩</span>
        <span data-i18n="undo">撤销</span>
    </button>
    <div class="toolbar-divider"></div>
    <button class="toolbar-btn" onclick="exportHTML()" title="导出为文件">
        <span class="btn-icon">📥</span>
        <div class="btn-text-block">
            <span class="btn-text-main" data-i18n="export">导出 .html</span>
            <span class="btn-text-sub" data-i18n="export_sub">生成新 HTML</span>
        </div>
    </button>
    <button class="toolbar-btn" onclick="resetAll()" title="重置为默认值">
        <span class="btn-icon">🔄</span>
        <span data-i18n="reset">重置</span>
    </button>
    <div class="toolbar-divider"></div>
    <button class="toolbar-btn toolbar-lang-btn" id="btnLang" onclick="switchLang()" title="切换语言 / Switch language">
        <span id="langLabel" class="lang-pair"><span class="lang-zh">中</span><span class="lang-sep">/</span><span class="lang-en">EN</span></span>
    </button>
    <span class="save-indicator" id="saveIndicator" data-i18n="saved">已保存 ✓</span>
</div>'''

    if page_structure == 'slides':
        toolbar += '''

<!-- Navigation -->
<nav class="nav-dots" id="navDots"></nav>
<div class="keyboard-hint">← → or Space to navigate · 按 E 切换编辑模式 · 编辑时按 P 固定提示</div>'''

    return toolbar


# Layout slider target fallback chains (P0-2 修复)
# 如果 host DOM 中找不到原 target, 尝试这些 fallback 选择器
LAYOUT_TARGET_FALLBACKS = {
    '.page':                            ['body > .page', '.page', '.container', '.wrapper', 'main', 'body'],
    '.masthead .lead, .section-intro':  ['.lead', '.section-intro', '.intro', '.subtitle', '.summary-banner', '.desc'],
    'section':                          ['section', '.section', 'article', '.timeline-item'],
    '.zt-grid':                         ['.zt-grid', '.grid', '.card-grid', '.cards', '.stat-row', '.org-chart', '.next-steps'],
    '.zt-card':                         ['.zt-card', '.card', '.goal-card', '.item', '.stat-card', '.next-card', '.org-box', '.support-item'],
}


def _resolve_layout_target(target: str, soup) -> str:
    """
    给定一个布局 slider 的 data-target, 返回 host DOM 中能查得到的选择器（保持逗号组合）。
    优先原 target 中能 select 到的部分；都不行则用 LAYOUT_TARGET_FALLBACKS 找替代。
    返回 '' 表示无可用选择器。
    """
    if soup is None:
        return target

    # 原 target 拆开后过滤
    valid_parts = []
    for sel in target.split(','):
        sel = sel.strip()
        if not sel:
            continue
        try:
            if soup.select(sel):
                valid_parts.append(sel)
        except Exception:
            pass
    if valid_parts:
        return ', '.join(valid_parts)

    # 找 fallback
    candidates = LAYOUT_TARGET_FALLBACKS.get(target, [])
    for cand in candidates:
        try:
            if soup.select(cand):
                return cand
        except Exception:
            continue
    return ''


def _add_layout_targets_to_pem(layout_sliders: list, pem: dict, soup=None) -> None:
    """
    P0-2 修复: 把布局 slider 的 data-target 反向索引到 PAGE_ELEMENT_TO_PANEL，
    让 PEM 包含 '布局' tab。原地修改 pem。
    如果传入 soup，会跳过 DOM 中匹配不到的 selector（满足 SC-03）。
    """
    for slider in layout_sliders:
        targets = slider.get('target', '')
        label = slider.get('label', '')
        if not targets or not label:
            continue
        for sel in targets.split(','):
            sel = sel.strip()
            if not sel:
                continue
            # 跳过无法 querySelector 到的 selector，避免触发 SC-03
            if soup is not None:
                try:
                    if not soup.select(sel):
                        continue
                except Exception:
                    continue
            if sel not in pem:
                pem[sel] = []
            if not any(it.get('row') == label and it.get('tab') == '布局' for it in pem[sel]):
                pem[sel].append({'tab': '布局', 'row': label})


def _add_size_targets_to_pem(size_sliders: list, pem: dict, soup=None) -> None:
    """
    P0-2 修复: 把字号 slider 的 data-target 反向索引到 PAGE_ELEMENT_TO_PANEL，
    确保 '字号' tab 在 PEM 里有对应项。原地修改 pem。
    """
    for slider in size_sliders:
        targets = slider.get('target', '')
        label = slider.get('label', '')
        if not targets or not label:
            continue
        for sel in targets.split(','):
            sel = sel.strip()
            if not sel:
                continue
            if soup is not None:
                try:
                    if not soup.select(sel):
                        continue
                except Exception:
                    continue
            if sel not in pem:
                pem[sel] = []
            if not any(it.get('row') == label and it.get('tab') == '字号' for it in pem[sel]):
                pem[sel].append({'tab': '字号', 'row': label})


def collapse_pem_rows(pem: dict, panel_config: 'PanelConfig') -> None:
    """v1.7.0: 把 PEM 中 raw row 改写为面板实际展示的 friendly label。
    - 颜色 row：用 color_var_to_rep + display_color_groups 反查
    - 字号 row：用 size_target_to_family + 原始 label → family label

    原地修改 pem。
    """
    # 颜色：raw color label → friendly group label
    raw_color_label_to_friendly = {}
    var_to_friendly = {g['var']: g['label'] for g in (panel_config.display_color_groups or [])}
    for raw_row in (panel_config.color_rows or []):
        rep = (panel_config.color_var_to_rep or {}).get(raw_row['var'])
        if rep and rep in var_to_friendly:
            raw_color_label_to_friendly[raw_row['label']] = var_to_friendly[rep]

    # 字号：raw label → family label
    raw_size_label_to_friendly = {}
    for s in (panel_config.size_sliders or []):
        fam = _match_size_family(s.get('target', ''))
        if fam:
            raw_size_label_to_friendly[s.get('label', '')] = fam['label']

    for sel, items in list(pem.items()):
        if not isinstance(items, list):
            continue
        new_items = []
        seen = set()
        for it in items:
            if not isinstance(it, dict):
                continue
            tab = it.get('tab', '')
            row = it.get('row', '')
            if tab == '颜色' and row in raw_color_label_to_friendly:
                row = raw_color_label_to_friendly[row]
            elif tab == '字号' and row in raw_size_label_to_friendly:
                row = raw_size_label_to_friendly[row]
            key = (tab, row)
            if key in seen:
                continue
            seen.add(key)
            new_items.append({'tab': tab, 'row': row})
        pem[sel] = new_items


def _build_constants_js(color_rows: list, size_sliders: list, preset_themes: dict,
                        page_element_to_panel: dict, css_var_to_elements: dict,
                        color_var_to_rep: dict = None, size_target_to_family: dict = None) -> str:
    """
    生成 window.X 常量注入代码。
    R5.1: PRESETS flat
    R6: DEFAULT_COLORS
    R7: PAGE_ELEMENT_TO_PANEL [{tab, row}]
    R8: CSS_VAR_TO_ELEMENTS 字符串
    R9: SIZE_BOUNDS 空对象
    R12: 无 fallback 函数, 无 adapter IIFE, 无 LLM_PRESET_HOOK
    v1.7.0: 新增 HVE_COLOR_GROUP / HVE_SIZE_FAMILY 供 editor-core.js 做"同组联动"
    """
    # DEFAULT_COLORS
    default_colors = {}
    for row in color_rows:
        default_colors[row['var']] = row['default_value']

    # SIZE_BOUNDS: 金版用空对象 (R9)
    size_bounds = {}

    # PRESETS: todo23 改造后只保留 original（供 resetAll/applyPreset('original') 使用）
    # 其他 builtin preset 不再注入 PRESETS（不再"应用"），改走 HVE_STYLE_PRESETS（复制 prompt）
    presets_for_apply = {}
    if preset_themes and 'original' in preset_themes:
        presets_for_apply['original'] = preset_themes['original']

    # HVE_STYLE_PRESETS: todo23 — 完整 style 元数据（id/name/vibe/palette），供 copyStylePrompt 读取
    style_presets = {}
    builtin_raw = _load_builtin_presets()
    for preset_id, data in builtin_raw.items():
        if isinstance(data, dict) and isinstance(data.get('palette'), dict):
            style_presets[preset_id] = {
                'id':        data.get('id', preset_id),
                'name_zh':   data.get('name_zh', preset_id),
                'name_en':   data.get('name_en', preset_id),
                'vibe_zh':   data.get('vibe_zh', ''),
                'vibe_en':   data.get('vibe_en', ''),
                'palette':   data['palette'],
                'is_dark':   bool(data.get('is_dark', False)),
            }

    js_parts = [
        '// === html-visual-editor v12 自动生成常量 ===',
        f'window.DEFAULT_COLORS = {json.dumps(default_colors, ensure_ascii=False)};',
        '',
        f'window.PRESETS = {json.dumps(presets_for_apply, ensure_ascii=False)};',
        '',
        '// todo23: Style prompt 元数据（点击 Style 卡片由 copyStylePrompt 读取）',
        f'window.HVE_STYLE_PRESETS = {json.dumps(style_presets, ensure_ascii=False)};',
        '',
        f'window.SIZE_BOUNDS = {json.dumps(size_bounds, ensure_ascii=False)};',
        '',
        f'window.PAGE_ELEMENT_TO_PANEL = {json.dumps(page_element_to_panel, ensure_ascii=False)};',
        '',
        f'window.CSS_VAR_TO_ELEMENTS = {json.dumps(css_var_to_elements, ensure_ascii=False)};',
        '',
        '// v1.7.0 todo25/26: 颜色/字号同组联动表',
        f'window.HVE_COLOR_GROUP = {json.dumps(color_var_to_rep or {}, ensure_ascii=False)};',
        f'window.HVE_SIZE_FAMILY = {json.dumps(size_target_to_family or {}, ensure_ascii=False)};',
    ]

    return '\n'.join(js_parts)


def _get_fallback_panel_template() -> str:
    """内联 panel 模板兜底"""
    return '''<!-- ======== EDIT PANEL (sidebar) ======== -->
<div class="edit-panel" id="editPanel">
    <div class="panel-header">
        <span class="panel-title">🎨 样式面板</span>
        <button class="panel-close-btn" onclick="toggleEditMode()">✕</button>
    </div>
    <div class="panel-tabs">
        <button class="panel-tab active" data-tab="colors" onclick="switchPanelTab('colors')">颜色</button>
        <button class="panel-tab" data-tab="presets" onclick="switchPanelTab('presets')">预设</button>
        <button class="panel-tab" data-tab="layout" onclick="switchPanelTab('layout')">布局</button>
        <button class="panel-tab" data-tab="size" onclick="switchPanelTab('size')">字号</button>
    </div>
    <div class="panel-tab-content active" id="tab-colors">
{{COLOR_TAB_CONTENT}}
    </div>
    <div class="panel-tab-content" id="tab-presets">
        <div class="panel-section">
            <div class="panel-section-title">一键换肤</div>
            <div class="preset-row">
{{PRESET_BUTTONS}}
            </div>
        </div>
    </div>
    <div class="panel-tab-content" id="tab-layout">
{{LAYOUT_TAB_CONTENT}}
    </div>
    <div class="panel-tab-content" id="tab-size">
{{SIZE_TAB_CONTENT}}
    </div>
    <div class="panel-actions">
        <div class="panel-autosave-hint">✓ 修改自动保存到当前浏览器（导出请用顶部工具栏）</div>
        <button class="action-btn action-btn-secondary" onclick="resetAll()">🔄 恢复默认设置</button>
    </div>
</div>'''
