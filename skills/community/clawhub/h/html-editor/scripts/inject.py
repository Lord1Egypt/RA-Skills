#!/usr/bin/env python3
"""
inject.py — HTML 注入模块
将 toolbar/panel DOM + window.X 常量 + editor-core.js/css 注入到宿主 HTML 中。
使用 html-visual-editor::BEGIN/END 标记实现幂等注入。
"""

import re
from dataclasses import dataclass
from pathlib import Path
from bs4 import BeautifulSoup


# 注入标记
INJECT_BEGIN = '<!-- html-visual-editor::BEGIN -->'
INJECT_END = '<!-- html-visual-editor::END -->'

# 资源文件路径
ASSETS_DIR = Path(__file__).parent.parent / 'assets'


# ============================================================
# v15 修复: 渐变里硬编码 hex 提取为 CSS 变量
# ============================================================

# 在 :root 块中已有的常见上下文关键字 -> 推断新变量名前缀
def _infer_gradient_var_name(selector: str, existing_vars: set, used_names: set, index: int) -> str:
    """根据 selector 推断一个语义化新变量名，避免与已有变量冲突"""
    # 取 selector 的第一段（去掉空格、>、,）
    first = re.split(r'[\s,>+~]', selector.strip())[0]
    # 取 class（最后一个 .name）或 tag
    cls_match = re.findall(r'\.([\w-]+)', first)
    if cls_match:
        base = cls_match[-1]
    else:
        tag_match = re.match(r'^([\w-]+)', first)
        base = tag_match.group(1) if tag_match else 'gradient'

    base = re.sub(r'[^\w-]', '', base) or 'gradient'

    candidate = f'--{base}-bg-2'
    i = 2
    while candidate in existing_vars or candidate in used_names:
        candidate = f'--{base}-bg-{i}'
        i += 1
    return candidate


def extract_gradient_hex_to_vars(html_content: str) -> tuple:
    """
    v15: 把宿主 CSS 里 linear-gradient / radial-gradient 中硬编码的 hex 色
    提取为新的 :root 变量并替换为 var(...)。

    只动渐变里的 hex，不动其它内联 hex（避免触发副作用）。

    返回 (修改后的 html_content, new_vars_dict {var_name: hex_value})
    """
    SKIP_HEX = {'#fff', '#ffffff', '#000', '#000000'}

    # 找到所有 <style>...</style> 块
    style_blocks = list(re.finditer(r'(<style[^>]*>)(.*?)(</style>)', html_content, re.DOTALL | re.IGNORECASE))
    if not style_blocks:
        return html_content, {}

    new_vars = {}  # var_name -> hex_value
    used_var_names = set()

    # 先收集 :root 已有变量，避免命名冲突
    existing_vars = set()
    for m in re.finditer(r'(--[\w-]+)\s*:', html_content):
        existing_vars.add(m.group(1))

    # 遍历每个 style 块，处理渐变
    modified_html = html_content
    offset_delta = 0  # 累计偏移
    for sb in style_blocks:
        block_start = sb.start(2) + offset_delta
        block_end = sb.end(2) + offset_delta
        original_block = modified_html[block_start:block_end]
        new_block = original_block

        # 在 block 内找每个 CSS 规则
        # 简化策略: 一次性扫所有 linear-gradient(...) / radial-gradient(...) 并记录其所在 selector
        # 用正则定位"selector { ... gradient ... }"
        rule_pattern = re.compile(r'([^{}@/]+?)\s*\{([^{}]*?)\}', re.DOTALL)

        # 收集需要替换的 (substring, replacement) 列表
        # 为了避免破坏正则位置，统一一次性 replace
        replacements = []  # list of (find_str, replace_str)
        rule_var_assignments = []  # list of (var_name, hex_value)

        for rule_match in rule_pattern.finditer(new_block):
            selector = rule_match.group(1).strip()
            body = rule_match.group(2)
            # 跳过 :root 块本身（里面的 hex 是颜色变量定义，不要碰）
            if ':root' in selector or selector.startswith('@'):
                continue

            # 找该 body 内的 gradient (用栈匹配嵌套括号)
            def _find_gradients(text):
                """返回 [(start, end, fn_name, args_str)] 的列表"""
                results = []
                grad_keywords = ('linear-gradient', 'radial-gradient', 'conic-gradient')
                i = 0
                while i < len(text):
                    matched_kw = None
                    for kw in grad_keywords:
                        if text[i:i+len(kw)] == kw and (i + len(kw) < len(text)) and text[i+len(kw)] in ' \t(':
                            matched_kw = kw
                            break
                    if not matched_kw:
                        i += 1
                        continue
                    # 找开始的 (
                    j = i + len(matched_kw)
                    while j < len(text) and text[j] in ' \t':
                        j += 1
                    if j >= len(text) or text[j] != '(':
                        i += 1
                        continue
                    # 栈匹配到对应的 )
                    depth = 1
                    args_start = j + 1
                    k = args_start
                    while k < len(text) and depth > 0:
                        if text[k] == '(':
                            depth += 1
                        elif text[k] == ')':
                            depth -= 1
                        k += 1
                    if depth != 0:
                        i = j + 1
                        continue
                    args_str = text[args_start:k-1]
                    results.append((i, k, matched_kw, args_str))
                    i = k
                return results

            new_body = body
            body_modified = False
            gradients = _find_gradients(body)
            # 倒序替换以保证 index 不偏
            for g_start, g_end, grad_fn, grad_args in reversed(gradients):
                # 找渐变里的硬编码 hex
                hex_pattern = re.compile(r'#[0-9a-fA-F]{3,8}\b')
                new_grad_args = grad_args
                grad_modified = False
                # 倒序替换 hex
                hex_matches = list(hex_pattern.finditer(grad_args))
                for hm in reversed(hex_matches):
                    hex_val = hm.group(0)
                    hex_low = hex_val.lower()
                    if hex_low in SKIP_HEX:
                        continue
                    if len(hex_low) == 4:
                        normalized = '#' + ''.join(c * 2 for c in hex_low[1:])
                    else:
                        normalized = hex_low

                    # 看是否已经有变量保存了同一颜色
                    existing_match = None
                    for vn, vv in new_vars.items():
                        if vv.lower() == normalized.lower():
                            existing_match = vn
                            break
                    if existing_match:
                        var_name = existing_match
                    else:
                        var_name = _infer_gradient_var_name(
                            selector, existing_vars, used_var_names, len(new_vars) + 1
                        )
                        used_var_names.add(var_name)
                        stored_val = hex_val.upper() if len(hex_val) > 4 else normalized.upper()
                        new_vars[var_name] = stored_val
                        rule_var_assignments.append((var_name, stored_val))

                    # 替换 grad_args 里的此 hex 为 var(...)
                    new_grad_args = new_grad_args[:hm.start()] + f'var({var_name})' + new_grad_args[hm.end():]
                    grad_modified = True

                if grad_modified:
                    old_grad = body[g_start:g_end]
                    new_grad = f'{grad_fn}({new_grad_args})'
                    new_body = new_body[:g_start] + new_grad + new_body[g_end:]
                    body_modified = True

            if body_modified:
                old_rule_text = rule_match.group(0)
                # 重新构造 rule（保留 selector { body }）
                new_rule_text = old_rule_text.replace(body, new_body, 1)
                replacements.append((old_rule_text, new_rule_text))

        # 应用替换
        for find_str, replace_str in replacements:
            new_block = new_block.replace(find_str, replace_str, 1)

        # 把新变量插到 :root {} 里。若没有 :root 块，则在 block 开头添加一个。
        if rule_var_assignments:
            root_match = re.search(r':root\s*\{([^}]*)\}', new_block)
            extra = ''
            for vn, vv in rule_var_assignments:
                extra += f'\n    {vn}: {vv};'
            if root_match:
                new_root_body = root_match.group(1).rstrip() + extra + '\n  '
                new_root = f':root {{{new_root_body}}}'
                new_block = new_block[:root_match.start()] + new_root + new_block[root_match.end():]
            else:
                new_block = f':root {{{extra}\n  }}\n' + new_block

        if new_block != original_block:
            modified_html = modified_html[:block_start] + new_block + modified_html[block_end:]
            offset_delta += len(new_block) - len(original_block)

    return modified_html, new_vars


# ============================================================
# v16 新增: 非渐变颜色属性中硬编码 hex 提取为 CSS 变量
# ============================================================

# 颜色相关 CSS 属性
_COLOR_PROPERTIES = frozenset({
    'color', 'background', 'background-color',
    'border-color', 'border', 'border-top-color', 'border-bottom-color',
    'border-left-color', 'border-right-color',
    'outline-color', 'outline',
    'fill', 'stroke',
    'box-shadow', 'text-shadow',
    'text-decoration-color', 'column-rule-color', 'caret-color',
})

# 编辑器自身的选择器关键字（跳过不提取）
_EDITOR_SELECTOR_KEYWORDS = (
    'toolbar', 'panel', 'edit-', 'color-row', 'color-swatch', 'color-label',
    'slider-row', 'slider-label', 'slider-val', 'slider-name',
    'preset-row', 'preset-btn', 'save-indicator', 'edit-hint',
    'html-visual-editor',
)

# 属性 → 变量前缀映射
_PROP_TO_PREFIX = {
    'color': '--text',
    'text-decoration-color': '--text',
    'caret-color': '--text',
    'background': '--bg',
    'background-color': '--bg',
    'border-color': '--line',
    'border': '--line',
    'border-top-color': '--line',
    'border-bottom-color': '--line',
    'border-left-color': '--line',
    'border-right-color': '--line',
    'outline-color': '--line',
    'outline': '--line',
    'fill': '--fill',
    'stroke': '--stroke',
    'box-shadow': '--shadow',
    'text-shadow': '--shadow',
    'column-rule-color': '--line',
}

# 属性 → 角色分类（用于 generate_panel 的 _classify_color_section）
_PROP_TO_ROLE = {
    'color': 'text',
    'text-decoration-color': 'text',
    'caret-color': 'text',
    'background': 'bg',
    'background-color': 'bg',
    'border-color': 'line',
    'border': 'line',
    'border-top-color': 'line',
    'border-bottom-color': 'line',
    'border-left-color': 'line',
    'border-right-color': 'line',
    'outline-color': 'line',
    'outline': 'line',
    'fill': 'bg',
    'stroke': 'line',
    'box-shadow': 'bg',
    'text-shadow': 'bg',
    'column-rule-color': 'line',
}


def _is_editor_selector(selector: str) -> bool:
    """判断选择器是否属于编辑器自身（不应对其提取颜色变量）"""
    sel_low = selector.lower()
    return any(kw in sel_low for kw in _EDITOR_SELECTOR_KEYWORDS)


def _infer_solid_var_name(hex_val: str, roles: set, existing_vars: set, used_names: set, counter: dict) -> str:
    """
    根据颜色值和角色推断语义化变量名。
    roles: {'text', 'bg', 'line', 'shadow', 'fill', 'stroke'} 的子集
    """
    # 混合用途 → --theme-N
    if len(roles) > 1:
        prefix = '--theme'
    elif 'text' in roles:
        prefix = '--text'
    elif 'bg' in roles:
        prefix = '--bg'
    elif 'line' in roles:
        prefix = '--line'
    elif 'fill' in roles:
        prefix = '--fill'
    elif 'stroke' in roles:
        prefix = '--stroke'
    elif 'shadow' in roles:
        prefix = '--shadow'
    else:
        prefix = '--color'

    # 用 hex 后4位做辨识（避免纯递增数字，让变量名更有信息量）
    hex_suffix = hex_val.lstrip('#')[-4:].lower()
    candidate = f'{prefix}-{hex_suffix}'

    # 如果有冲突，加数字后缀
    if candidate in existing_vars or candidate in used_names:
        i = 2
        candidate = f'{prefix}-{hex_suffix}-{i}'
        while candidate in existing_vars or candidate in used_names:
            i += 1
            candidate = f'{prefix}-{hex_suffix}-{i}'

    return candidate


def extract_solid_hex_to_vars(html_content: str) -> tuple:
    """
    v16: 把宿主 CSS 里非渐变颜色属性中硬编码的 hex 提取为 :root 变量。

    与 extract_gradient_hex_to_vars 互补：
    - gradient 版处理渐变中的 hex
    - 本函数处理 color / background / border 等属性中的 hex

    返回 (修改后的 html_content, new_vars_dict {var_name: hex_value})
    """
    SKIP_HEX = set()  # v1.3: 不再跳过 #fff/#000，让所有硬编码颜色进入变量体系

    # 找到所有 <style>...</style> 块
    style_blocks = list(re.finditer(r'(<style[^>]*>)(.*?)(</style>)', html_content, re.DOTALL | re.IGNORECASE))
    if not style_blocks:
        return html_content, {}

    # 先收集 :root 已有变量，避免命名冲突
    existing_vars = set()
    for m in re.finditer(r'(--[\w-]+)\s*:', html_content):
        existing_vars.add(m.group(1))

    new_vars = {}       # var_name -> hex_value
    used_var_names = set()
    counter = {}        # prefix -> count（备用）

    # 第一遍：收集所有颜色 hex 的使用信息（同色合并）
    # hex_normalized -> {roles: set, selectors: list, occurrences: [(style_idx, rule_start, rule_end, prop, hex_pos_in_prop_val)]}
    hex_info = {}

    for sb_idx, sb in enumerate(style_blocks):
        block_content = sb.group(2)
        rule_pattern = re.compile(r'([^{}@/]+?)\s*\{([^{}]*?)\}', re.DOTALL)

        for rule_match in rule_pattern.finditer(block_content):
            selector = rule_match.group(1).strip()
            body = rule_match.group(2)

            # 跳过 :root / @规则 / 编辑器选择器
            if ':root' in selector or selector.startswith('@') or _is_editor_selector(selector):
                continue

            # 跳过含 var() 的属性值（已有变量引用，不需提取）
            for prop_match in re.finditer(r'([\w-]+)\s*:\s*([^;]+)', body):
                prop_name = prop_match.group(1).strip().lower()
                prop_value = prop_match.group(2).strip()

                if prop_name not in _COLOR_PROPERTIES:
                    continue
                # 跳过渐变值（已由 extract_gradient_hex_to_vars 处理）
                if 'gradient' in prop_value.lower():
                    continue
                # 跳过已含 var() 的值
                if 'var(' in prop_value:
                    continue

                # 找该属性值中的 hex
                for hex_m in re.finditer(r'#[0-9a-fA-F]{3,8}\b', prop_value):
                    hex_val = hex_m.group(0)
                    hex_low = hex_val.lower()

                    # 跳过极端色
                    if hex_low in SKIP_HEX:
                        continue

                    # 标准化：3位 → 6位
                    if len(hex_low) == 4:
                        normalized = '#' + ''.join(c * 2 for c in hex_low[1:])
                    else:
                        normalized = hex_low

                    role = _PROP_TO_ROLE.get(prop_name, 'bg')

                    if normalized not in hex_info:
                        hex_info[normalized] = {
                            'roles': set(),
                            'selectors': [],
                            'occurrences': [],
                        }
                    hex_info[normalized]['roles'].add(role)
                    hex_info[normalized]['selectors'].append(selector)

    if not hex_info:
        return html_content, {}

    # 第二遍：为每个唯一 hex 分配变量名
    hex_to_var = {}  # normalized_hex -> var_name
    for hex_norm, info in sorted(hex_info.items(), key=lambda x: -len(x[1]['occurrences'])):
        var_name = _infer_solid_var_name(hex_norm, info['roles'], existing_vars, used_var_names, counter)
        used_var_names.add(var_name)
        # 存储值用大写
        stored_val = hex_norm.upper()
        new_vars[var_name] = stored_val
        hex_to_var[hex_norm] = var_name

    # 第三遍：替换 CSS 中的 hex 为 var()
    modified_html = html_content
    offset_delta = 0

    for sb_idx, sb in enumerate(style_blocks):
        block_start = sb.start(2) + offset_delta
        block_end = sb.end(2) + offset_delta
        original_block = modified_html[block_start:block_end]
        new_block = original_block

        rule_pattern = re.compile(r'([^{}@/]+?)\s*\{([^{}]*?)\}', re.DOTALL)
        replacements = []
        rule_var_assignments = []

        for rule_match in rule_pattern.finditer(new_block):
            selector = rule_match.group(1).strip()
            body = rule_match.group(2)

            if ':root' in selector or selector.startswith('@') or _is_editor_selector(selector):
                continue

            new_body = body
            body_modified = False

            for prop_match in re.finditer(r'([\w-]+)\s*:\s*([^;]+)', body):
                prop_name = prop_match.group(1).strip().lower()
                prop_value = prop_match.group(2).strip()

                if prop_name not in _COLOR_PROPERTIES:
                    continue
                if 'gradient' in prop_value.lower():
                    continue
                if 'var(' in prop_value:
                    continue

                # 找该属性值中的 hex 并替换
                prop_replacements = []
                for hex_m in re.finditer(r'#[0-9a-fA-F]{3,8}\b', prop_value):
                    hex_val = hex_m.group(0)
                    hex_low = hex_val.lower()
                    if hex_low in SKIP_HEX:
                        continue
                    if len(hex_low) == 4:
                        normalized = '#' + ''.join(c * 2 for c in hex_low[1:])
                    else:
                        normalized = hex_low

                    var_name = hex_to_var.get(normalized)
                    if var_name:
                        # 记录变量赋值（去重）
                        if (var_name, new_vars[var_name]) not in rule_var_assignments:
                            rule_var_assignments.append((var_name, new_vars[var_name]))
                        prop_replacements.append((hex_m.group(0), f'var({var_name})'))

                if prop_replacements:
                    new_prop_value = prop_value
                    for old_hex, new_var_ref in prop_replacements:
                        new_prop_value = new_prop_value.replace(old_hex, new_var_ref, 1)
                    new_body = new_body.replace(prop_value, new_prop_value, 1)
                    body_modified = True

            if body_modified:
                old_rule_text = rule_match.group(0)
                new_rule_text = old_rule_text.replace(body, new_body, 1)
                replacements.append((old_rule_text, new_rule_text))

        # 应用替换
        for find_str, replace_str in replacements:
            new_block = new_block.replace(find_str, replace_str, 1)

        # 把新变量插到 :root 块
        if rule_var_assignments:
            root_match = re.search(r':root\s*\{([^}]*)\}', new_block)
            extra = ''
            for vn, vv in rule_var_assignments:
                extra += f'\n    {vn}: {vv};'
            if root_match:
                new_root_body = root_match.group(1).rstrip() + extra + '\n  '
                new_root = f':root {{{new_root_body}}}'
                new_block = new_block[:root_match.start()] + new_root + new_block[root_match.end():]
            else:
                new_block = f':root {{{extra}\n  }}\n' + new_block

        if new_block != original_block:
            modified_html = modified_html[:block_start] + new_block + modified_html[block_end:]
            offset_delta += len(new_block) - len(original_block)

    return modified_html, new_vars


@dataclass
class InjectResult:
    """注入结果"""
    output_html: str
    output_path: Path


def _read_asset(filename: str) -> str:
    """读取 assets 目录下的文件"""
    filepath = ASSETS_DIR / filename
    if not filepath.exists():
        raise FileNotFoundError(f"缺少资源文件: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def _strip_old_injection(html_content: str) -> str:
    """
    检测并清理旧的注入内容。
    查找所有 html-visual-editor::BEGIN/END 标记对并删除中间所有内容。
    """
    pattern = re.compile(
        re.escape(INJECT_BEGIN) + r'.*?' + re.escape(INJECT_END),
        re.DOTALL
    )
    cleaned = html_content
    while pattern.search(cleaned):
        cleaned = pattern.sub('', cleaned)
    return cleaned


def _has_old_injection(html_content: str) -> bool:
    """检测是否有旧的注入标记"""
    return INJECT_BEGIN in html_content


def _add_data_editable(html_content: str, scan_result) -> str:
    """
    为文本元素添加 data-editable="" 属性 (R13 合规)。

    标记策略 (来自金版分布: span 51 / li 18 / div 17 / p 5 / h2 5 / h3 4 / h1 1)：
    - 所有 heading (h1-h6)
    - 直接含文字的 p / li / blockquote
    - 含文字的 th / td
    - 含 direct text node 的 span / 语义 div (排除容器类)
    - 不标 strong/em/b/i/a/code (避免双标和点击干扰)
    """
    EXCLUDE_CLASSES = {
        'edit-toolbar', 'edit-panel', 'edit-hint',
        'panel-tab', 'panel-section', 'panel-section-title', 'panel-tab-content',
        'panel-tabs', 'panel-header', 'panel-actions', 'panel-close-btn', 'panel-title',
        'color-row', 'color-label', 'color-swatch', 'color-hex',
        'slider-row', 'slider-label', 'slider-name', 'slider-val',
        'preset-row', 'preset-btn',
        'toolbar-btn', 'toolbar-divider', 'btn-icon', 'save-indicator',
        'action-btn',
    }
    CONTAINER_CLASS_KEYWORDS = ('grid', 'container', 'wrapper', 'panel-')
    CONTAINER_CLASS_EXACT = {
        'row', 'col', 'section', 'main', 'header', 'footer', 'nav',
        'card-container', 'aside',
    }
    HEADINGS = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}
    PARAGRAPHS = {'p', 'li', 'blockquote'}
    CELLS = {'th', 'td'}
    SKIP_TAGS = {'a', 'strong', 'em', 'b', 'i', 'code', 'kbd', 'small', 'sub', 'sup'}

    soup = BeautifulSoup(html_content, 'html.parser')
    body = soup.body
    if not body:
        return html_content

    def _is_container(classes):
        for cls in classes:
            if cls in CONTAINER_CLASS_EXACT:
                return True
            for kw in CONTAINER_CLASS_KEYWORDS:
                if kw in cls:
                    return True
            if cls.startswith('col-'):
                return True
        return False

    def _direct_text(el):
        parts = []
        for child in el.children:
            if isinstance(child, str):
                parts.append(child)
        return ''.join(parts).strip()

    count = 0
    for el in body.find_all():
        if el.has_attr('data-editable'):
            continue
        classes = el.get('class') or []
        if any(cls in EXCLUDE_CLASSES for cls in classes):
            continue
        # 跳过编辑器 DOM 内的所有子元素
        skip = False
        for cls in EXCLUDE_CLASSES:
            if el.find_parent(class_=cls):
                skip = True
                break
        if skip:
            continue
        if el.name in SKIP_TAGS:
            continue
        # 跳过 script/style/svg 内部
        if el.find_parent(['script', 'style', 'svg']):
            continue
        if el.name in ('script', 'style', 'svg', 'path', 'g', 'circle', 'rect', 'line', 'polyline', 'polygon', 'use'):
            continue

        should_mark = False

        if el.name in HEADINGS:
            text = el.get_text(strip=True)
            if text and len(text) >= 2:
                should_mark = True
        elif el.name in PARAGRAPHS:
            direct = _direct_text(el)
            full = el.get_text(strip=True)
            # p/li 即使文字嵌在 strong/em 里也允许，要求至少 full 文本 >= 2
            if full and len(full) >= 2 and (direct or el.name in PARAGRAPHS):
                should_mark = True
        elif el.name in CELLS:
            text = el.get_text(strip=True)
            if text and len(text) >= 2:
                should_mark = True
        elif el.name in ('div', 'span'):
            direct = _direct_text(el)
            if not direct or len(direct) < 2:
                continue
            if _is_container(classes):
                continue
            should_mark = True

        if should_mark:
            el['data-editable'] = ''
            count += 1

    print(f"  标记 data-editable: {count} 个元素")
    return str(soup)


def _find_element_by_selector(root, selector: str):
    """简化的选择器查找（支持 #id / tag.class / tag:nth-of-type）"""
    if selector.startswith('#'):
        return root.find(id=selector[1:])

    # tag.class 格式
    tag_class_match = re.match(r'^(\w+)\.([\w-]+)$', selector)
    if tag_class_match:
        tag = tag_class_match.group(1)
        cls = tag_class_match.group(2)
        return root.find(tag, class_=cls)

    # 纯 tag 格式
    if re.match(r'^\w+$', selector):
        return root.find(selector)

    # tag:nth-of-type(n) 格式
    nth_match = re.match(r'^(\w+):nth-of-type\((\d+)\)$', selector)
    if nth_match:
        tag = nth_match.group(1)
        n = int(nth_match.group(2))
        all_tags = root.find_all(tag)
        if len(all_tags) >= n:
            return all_tags[n - 1]

    return None


def inject(html_content: str, panel_config, scan_result, output_path: Path = None) -> InjectResult:
    """
    将编辑器组件注入到宿主 HTML 中。

    流程：
    1. 检测并清理旧注入
    2. 添加 data-editable 属性
    3. 在 </head> 前注入 editor-core.css
    4. 在 <body> 开头注入 toolbar + panel
    5. 在 </body> 前注入 window.X 常量 + editor-core.js
    6. 用 BEGIN/END 标记包裹所有注入内容
    """
    # 步骤 1：清理旧注入
    if _has_old_injection(html_content):
        html_content = _strip_old_injection(html_content)

    # 步骤 2：添加 data-editable
    html_content = _add_data_editable(html_content, scan_result)

    # 读取资源文件
    editor_css = _read_asset('editor-core.css')
    editor_js = _read_asset('editor-core.js')

    # 步骤 3：在 </head> 前注入 CSS
    css_injection = f'''{INJECT_BEGIN}
<style id="html-visual-editor-css">
{editor_css}
</style>
{INJECT_END}'''

    if '</head>' in html_content:
        html_content = html_content.replace('</head>', f'{css_injection}\n</head>', 1)
    elif '<body' in html_content:
        # 没有 </head>，在 <body 前插入
        html_content = html_content.replace('<body', f'{css_injection}\n<body', 1)
    else:
        # 极端情况：直接在最前面加
        html_content = css_injection + '\n' + html_content

    # 步骤 4：在 <body> 开头注入 toolbar + panel + edit-hint (R14: hint 在 panel 之后)
    edit_hint = '<div class="edit-hint" id="editHint">✏️ 点击任意文字直接编辑 · 改色/布局请用右侧面板 · 按 P 固定提示</div>'
    body_injection = f'''{INJECT_BEGIN}
{panel_config.toolbar_html}

{panel_config.panel_html}

{edit_hint}
{INJECT_END}'''

    # 找到 <body...> 标签结束位置
    body_tag_match = re.search(r'<body[^>]*>', html_content, re.IGNORECASE)
    if body_tag_match:
        insert_pos = body_tag_match.end()
        html_content = html_content[:insert_pos] + '\n' + body_injection + '\n' + html_content[insert_pos:]
    else:
        # 没有 <body> 标签，在 CSS 注入后追加
        html_content += '\n' + body_injection

    # 步骤 5：在 </body> 前注入 JS
    js_injection = f'''{INJECT_BEGIN}
<script id="html-visual-editor-constants">
{panel_config.constants_js}
</script>
<script id="html-visual-editor-core">
{editor_js}
</script>
{INJECT_END}'''

    if '</body>' in html_content:
        html_content = html_content.replace('</body>', f'{js_injection}\n</body>', 1)
    elif '</html>' in html_content:
        html_content = html_content.replace('</html>', f'{js_injection}\n</html>', 1)
    else:
        html_content += '\n' + js_injection

    return InjectResult(
        output_html=html_content,
        output_path=output_path
    )
