#!/usr/bin/env python3
"""
scan_dom.py -- DOM 扫描模块 (v15 public package)
扫描 HTML body 中的可编辑元素，推断编辑维度，
生成 PAGE_ELEMENT_TO_PANEL 映射 [{tab, row}, ...] 和 CSS_VAR_TO_ELEMENTS 反查索引（字符串格式）。

对应规范: R7.1-R7.4, R8
"""

import re
from dataclasses import dataclass, field
from typing import Literal
from bs4 import BeautifulSoup, NavigableString


# 可编辑的文本标签
EDITABLE_TAGS = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'span',
                 'a', 'td', 'th', 'blockquote', 'figcaption', 'label',
                 'strong', 'em', 'b', 'i', 'small', 'dt', 'dd', 'caption'}

# 容器标签
CONTAINER_TAGS = {'div', 'section', 'article', 'main', 'header', 'footer',
                  'aside', 'nav', 'ul', 'ol', 'figure', 'details'}

# 容器语义 class（模糊匹配）
CONTAINER_CLASSES = {'card', 'container', 'section', 'grid', 'wrapper',
                     'panel', 'hero', 'stat', 'box', 'group', 'block',
                     'row', 'col', 'column', 'tile', 'item', 'list'}

# 最大元素扫描数量
MAX_ELEMENTS = 500


@dataclass
class EditableElement:
    """一个可编辑元素的描述"""
    selector: str
    tag: str
    classes: list
    text_content: str
    is_text: bool
    is_container: bool
    used_vars: list
    editable_dims: list


@dataclass
class ScanResult:
    """DOM 扫描结果"""
    elements: list            # list[EditableElement]
    page_structure: str       # 'slides' | 'single-page' | 'sections' | 'article'
    has_nav_dots: bool
    page_element_to_panel: dict   # {sel: [{tab, row}, ...]}  -- R7.1 新格式
    css_var_to_elements: dict     # {var: "sel1, sel2"}        -- R8 字符串格式
    present_elements: dict = None  # {tag: computed_font_size}
    _html: str = ''               # 原始 HTML（用于布局 slider 解析 fallback）
    # v1.8.0: 数据驱动颜色聚合
    color_usage: dict = None      # {'text': [(hex, char_count, vars_pointing_here), ...],
                                  #  'bg':   [(hex, elem_count, vars), ...],
                                  #  'border':[(hex, elem_count, vars), ...]}


def has_direct_text(el) -> bool:
    """判断元素是否有直接文本内容（非子元素文本）"""
    for child in el.children:
        if isinstance(child, NavigableString):
            text = child.strip()
            if text and len(text) > 1:
                return True
    return False


def best_selector(el) -> str:
    """
    为元素生成最优 CSS 选择器 (R7.2)
    优先用 .parent-class child-tag / .specific-class 组合，避免 nth-of-type。
    """
    tag = el.name
    classes = el.get('class', [])
    el_id = el.get('id', '')

    # 有 id 的情况（排除动态 id）
    if el_id and not re.match(r'^(__|js-|react-|vue-|ng-|html-visual-editor)', el_id):
        return f'#{el_id}'

    # 有语义化 class
    if classes:
        semantic_classes = [c for c in classes
                          if not re.match(r'^(p|m|w|h|text|bg|border|flex|grid|gap|rounded|shadow)-', c)
                          and len(c) > 2]
        if semantic_classes:
            # 尝试带父类组合选择器增强精确度
            parent = el.parent
            if parent and parent.name not in ('body', 'html', '[document]'):
                parent_classes = parent.get('class', [])
                parent_semantic = [c for c in parent_classes
                                   if not re.match(r'^(p|m|w|h|text|bg|border|flex|grid|gap|rounded|shadow)-', c)
                                   and len(c) > 2]
                if parent_semantic:
                    return f'.{parent_semantic[0]} .{semantic_classes[0]}'
            return f'.{semantic_classes[0]}'
        if classes:
            return f'.{classes[0]}'

    # 没有 class，用父元素 class + 子 tag（R7.2 推荐写法）
    parent = el.parent
    if parent and parent.name not in ('body', 'html', '[document]'):
        parent_classes = parent.get('class', [])
        parent_semantic = [c for c in parent_classes
                           if not re.match(r'^(p|m|w|h|text|bg|border|flex|grid|gap|rounded|shadow)-', c)
                           and len(c) > 2]
        if parent_semantic:
            return f'.{parent_semantic[0]} {tag}'
        # 检查祖父
        grandparent = parent.parent
        if grandparent and grandparent.name not in ('body', 'html', '[document]'):
            gp_classes = grandparent.get('class', [])
            gp_semantic = [c for c in gp_classes
                           if not re.match(r'^(p|m|w|h|text|bg|border|flex|grid|gap|rounded|shadow)-', c)
                           and len(c) > 2]
            if gp_semantic:
                return f'.{gp_semantic[0]} {tag}'

    # 最后兜底：纯 tag（不用 nth-of-type，按 R7.2 禁止）
    return tag


def find_vars_for_element(el, selector: str, parse_result) -> list:
    """找出元素使用的 CSS 变量（通过匹配 CSS 规则）"""
    used_vars = []
    el_classes = el.get('class', [])
    el_id = el.get('id', '')
    el_tag = el.name

    for rule in parse_result.rules:
        rule_sel = rule.selector.strip()
        matched = False

        if rule_sel == el_tag:
            matched = True
        elif rule_sel.startswith('.'):
            cls = rule_sel.split('.')[1].split(':')[0].split(' ')[0]
            if cls in el_classes:
                matched = True
        elif rule_sel.startswith('#') and el_id:
            if rule_sel.split(':')[0].split(' ')[-1] == f'#{el_id}':
                matched = True
        elif '.' in rule_sel and not rule_sel.startswith('.'):
            parts = rule_sel.split('.')
            tag = parts[0].split(' ')[-1].split(':')[0]
            cls = parts[1].split(':')[0].split(' ')[0]
            if tag == el_tag and cls in el_classes:
                matched = True
        elif ' ' in rule_sel:
            last_part = rule_sel.split()[-1]
            if last_part == el_tag:
                matched = True
            elif last_part.startswith('.'):
                cls = last_part[1:].split(':')[0]
                if cls in el_classes:
                    matched = True

        if matched:
            used_vars.extend(rule.referenced_vars)

    return list(set(used_vars))


def infer_dimensions(el, used_vars: list, parse_result) -> list:
    """推断元素的可编辑维度"""
    dims = []
    var_semantics = {v.name: v.semantic for v in parse_result.variables}

    for var in used_vars:
        sem = var_semantics.get(var, 'other')
        if sem == 'color' and 'color' not in dims:
            dims.append('color')
        elif sem == 'size' and 'font-size' not in dims:
            dims.append('font-size')
        elif sem == 'spacing' and 'layout' not in dims:
            dims.append('layout')

    if el.name in CONTAINER_TAGS and 'layout' not in dims:
        dims.append('layout')

    return dims


def detect_page_structure(soup) -> tuple:
    """检测页面结构类型"""
    body = soup.body
    if not body:
        return 'single-page', False

    slides = body.find_all(class_=re.compile(r'slide|page|screen', re.I))
    if len(slides) >= 2:
        return 'slides', True

    nav_dots = body.find(class_=re.compile(r'nav-dot|dot|indicator', re.I))
    has_nav = nav_dots is not None

    sections = body.find_all(['section', 'article'])
    if len(sections) >= 3:
        return 'sections', has_nav

    if body.find('article') or body.find(class_=re.compile(r'article|post|content', re.I)):
        return 'article', has_nav

    return 'single-page', has_nav


def _build_css_var_to_elements_from_css(parse_result) -> dict:
    """
    从 parsed CSS 构建 CSS_VAR_TO_ELEMENTS（R8）。
    扫描 CSS 规则中 var(--xxx) 引用，包含伪元素选择器。
    返回 {var_name: "sel1, sel2, sel3"} 字符串格式。
    """
    var_selectors = {}  # var_name -> set of selectors
    for rule in parse_result.rules:
        sel = rule.selector.strip()
        if sel.startswith(':root') or sel.startswith('html') or sel == '*':
            continue
        for prop_name, prop_value in rule.properties.items():
            for var_ref in re.findall(r'var\((--[\w-]+)', prop_value):
                if var_ref not in var_selectors:
                    var_selectors[var_ref] = set()
                var_selectors[var_ref].add(sel)

    # R8: value 是逗号分隔的字符串
    result = {}
    for var_name, sels in var_selectors.items():
        result[var_name] = ', '.join(sorted(sels))
    return result


def scan_dom(html_content: str, parse_result, label_for: dict = None) -> ScanResult:
    """
    扫描 HTML DOM，生成可编辑元素列表和映射。

    label_for: 来自 generate_panel 的 LABEL_FOR dict
               {(tab_name, key): label_string}
               用于填充 page_element_to_panel 的 row 字段。
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    body = soup.body
    if not body:
        return ScanResult(
            elements=[], page_structure='single-page',
            has_nav_dots=False, page_element_to_panel={},
            css_var_to_elements={}, _html=html_content
        )

    page_structure, has_nav_dots = detect_page_structure(soup)

    elements = []
    seen_selectors = set()
    count = 0

    for el in body.descendants:
        if count >= MAX_ELEMENTS:
            break
        if not hasattr(el, 'name') or el.name is None:
            continue
        if el.name in ['script', 'style', 'link', 'meta', 'br', 'hr', 'img', 'svg', 'path', 'input', 'button', 'select', 'textarea']:
            continue

        selector = best_selector(el)
        if selector in seen_selectors:
            continue

        is_text = el.name in EDITABLE_TAGS and has_direct_text(el)

        el_classes = el.get('class', [])
        is_container = (el.name in CONTAINER_TAGS and
                       (any(cls.lower() in CONTAINER_CLASSES
                            for cls in el_classes) or
                        has_direct_text(el) is False))

        if not is_text and not is_container:
            continue

        used_vars = find_vars_for_element(el, selector, parse_result)
        dims = infer_dimensions(el, used_vars, parse_result)
        text = el.get_text(strip=True)[:50] if is_text else ''

        elements.append(EditableElement(
            selector=selector,
            tag=el.tag if hasattr(el, 'tag') else el.name,
            classes=list(el_classes),
            text_content=text,
            is_text=is_text,
            is_container=is_container,
            used_vars=used_vars,
            editable_dims=dims
        ))
        seen_selectors.add(selector)
        count += 1

    # R7: 构建 PAGE_ELEMENT_TO_PANEL [{tab, row}, ...]
    page_element_to_panel = {}
    if label_for is None:
        label_for = {}

    color_vars_set = {v.name for v in parse_result.variables if v.semantic == 'color'}
    # Build reverse lookup: var_name -> label in 颜色 tab
    var_to_color_label = {}
    for (tab, key), label in label_for.items():
        if tab == '颜色':
            var_to_color_label[key] = label

    # Build reverse lookup: selector -> labels in 字号/布局 tab
    sel_to_size_label = {}
    sel_to_layout_label = {}
    for (tab, key), label in label_for.items():
        if tab == '字号':
            # key is a selector string (possibly comma-separated)
            for s in key.split(','):
                sel_to_size_label[s.strip()] = label
        elif tab == '布局':
            for s in key.split(','):
                sel_to_layout_label[s.strip()] = label

    for elem in elements:
        if not elem.is_text and not elem.used_vars:
            continue

        items = []

        # 颜色维度: match element's used vars to color labels
        for var_name in elem.used_vars:
            if var_name in var_to_color_label:
                row_label = var_to_color_label[var_name]
                item = {'tab': '颜色', 'row': row_label}
                if item not in items:
                    items.append(item)

        # 字号维度: check if this selector is a target in 字号 tab
        for sel_key, label in sel_to_size_label.items():
            # Check if the element's selector matches any of the targets
            if _selector_matches_element(elem.selector, sel_key, soup):
                item = {'tab': '字号', 'row': label}
                if item not in items:
                    items.append(item)

        # 布局维度: check if this selector is a target in 布局 tab
        for sel_key, label in sel_to_layout_label.items():
            if _selector_matches_element(elem.selector, sel_key, soup):
                item = {'tab': '布局', 'row': label}
                if item not in items:
                    items.append(item)

        if items:
            page_element_to_panel[elem.selector] = items

    # R8: CSS_VAR_TO_ELEMENTS 字符串格式, 从 CSS 规则构建（含伪元素）
    css_var_to_elements = _build_css_var_to_elements_from_css(parse_result)

    # 检测 present_elements
    SIZING_TAGS = ['h1', 'h2', 'h3', 'h4', 'p', 'li', 'blockquote', 'button', 'span']
    present_elements = {}
    for tag in SIZING_TAGS:
        found = body.find_all(tag, limit=3)
        if found:
            font_size = None
            for found_el in found:
                style = found_el.get('style', '')
                fs_match = re.search(r'font-size:\s*([\d.]+)(px|em|rem|pt)', style)
                if fs_match:
                    font_size = f"{fs_match.group(1)}{fs_match.group(2)}"
                    break
            if not font_size:
                for rule in parse_result.rules:
                    if rule.selector.strip() == tag or rule.selector.strip().endswith(' ' + tag):
                        for prop_name, prop_val in rule.properties.items():
                            if 'font-size' in prop_name:
                                fs_match = re.search(r'([\d.]+)(px|em|rem|pt)', prop_val)
                                if fs_match:
                                    font_size = f"{fs_match.group(1)}{fs_match.group(2)}"
                                    break
                        if font_size:
                            break
            present_elements[tag] = font_size

    return ScanResult(
        elements=elements,
        page_structure=page_structure,
        has_nav_dots=has_nav_dots,
        page_element_to_panel=page_element_to_panel,
        css_var_to_elements=css_var_to_elements,
        present_elements=present_elements,
        _html=html_content,
        color_usage=_aggregate_color_usage(soup, parse_result),
    )


def _selector_matches_element(elem_selector: str, target_selector: str, soup) -> bool:
    """Check if an element's selector matches/overlaps with a target selector."""
    # Exact match
    if elem_selector == target_selector:
        return True
    # Check if elem_selector is a child/descendant of target_selector
    # e.g. elem ".masthead h1" matches target ".masthead h1"
    # or elem ".masthead" is contained in target ".masthead .lead, .section-intro"
    es_parts = elem_selector.strip().split()
    ts_parts = target_selector.strip().split()
    # If target is a simple tag and elem ends with that tag
    if len(ts_parts) == 1 and len(es_parts) >= 1:
        if es_parts[-1] == ts_parts[0] or es_parts[-1].split('.')[0] == ts_parts[0]:
            return True
    # If they share the same last class/tag
    if len(es_parts) >= 1 and len(ts_parts) >= 1:
        if es_parts[-1] == ts_parts[-1]:
            return True
    return False


# ============================================================
# v1.8.0: 数据驱动颜色聚合 (todo38/39/44)
# ============================================================
HEX_RE = re.compile(r'#([0-9a-fA-F]{3,8})\b')
RGB_RE = re.compile(r'rgba?\(\s*([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)(?:[,\s]+([\d.]+))?\s*\)')


def _normalize_hex(s: str) -> str:
    """从一段 CSS value 中提取 hex；支持 #abc / #abcdef / rgb()/rgba()。返回 #RRGGBB 或 ''。"""
    if not s:
        return ''
    s = s.strip()
    m = HEX_RE.search(s)
    if m:
        h = m.group(1)
        if len(h) == 3:
            h = ''.join(c * 2 for c in h)
        elif len(h) >= 6:
            h = h[:6]
        else:
            return ''
        return '#' + h.upper()
    m = RGB_RE.search(s)
    if m:
        r, g, b = int(float(m.group(1))), int(float(m.group(2))), int(float(m.group(3)))
        return '#{:02X}{:02X}{:02X}'.format(r, g, b)
    return ''


def _hex_distance(a: str, b: str) -> float:
    try:
        ha = a.lstrip('#'); hb = b.lstrip('#')
        if len(ha) >= 6 and len(hb) >= 6:
            r1, g1, b1 = int(ha[0:2], 16), int(ha[2:4], 16), int(ha[4:6], 16)
            r2, g2, b2 = int(hb[0:2], 16), int(hb[2:4], 16), int(hb[4:6], 16)
            return ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5
    except Exception:
        pass
    return 999.0


def _build_selector_rule_index(parse_result):
    """构造 {selector: properties} 缓存，方便按选择器找属性。"""
    idx = {}
    for rule in (parse_result.rules if parse_result else []):
        sel = (rule.selector or '').strip()
        if not sel:
            continue
        for sub in [s.strip() for s in sel.split(',') if s.strip()]:
            idx.setdefault(sub, {}).update(rule.properties or {})
    return idx


def _resolve_var_to_hex(value: str, var_to_hex: dict, visited=None) -> str:
    """递归解析 var(--xxx) 到最终 hex。"""
    if visited is None: visited = set()
    if not value:
        return ''
    val = value.strip()
    # 直接是颜色
    direct = _normalize_hex(val)
    if direct:
        return direct
    # var(--xxx[, fallback])
    m = re.search(r'var\(\s*(--[^\s,)]+)(?:\s*,\s*([^)]+))?\s*\)', val)
    if m:
        var_name = m.group(1)
        if var_name in visited:
            return ''
        visited.add(var_name)
        nxt = var_to_hex.get(var_name, '')
        resolved = _resolve_var_to_hex(nxt, var_to_hex, visited)
        if resolved:
            return resolved
        if m.group(2):
            return _resolve_var_to_hex(m.group(2), var_to_hex, visited)
    return ''


def _element_matches_rule_selector(el, sel: str, soup) -> bool:
    """简单判断 el 是否被 selector 命中。用 soup.select 做严格匹配。"""
    try:
        matched = soup.select(sel)
        return el in matched
    except Exception:
        return False


def _compute_prop_for_element(el, prop_name: str, sel_index: dict, var_to_hex: dict, soup):
    """对 el 计算 prop_name 的最终 hex（粗略版 cascade）。
    优先级：
      1) inline style
      2) host CSS 规则（按 selector specificity 简单估计：含 class/id 的规则优先）
    返回 (hex, source_var_name)。
    """
    # 1) inline
    style = el.get('style', '') if hasattr(el, 'get') else ''
    if style:
        for decl in style.split(';'):
            if ':' not in decl:
                continue
            k, v = decl.split(':', 1)
            if k.strip().lower() == prop_name:
                resolved = _resolve_var_to_hex(v, var_to_hex)
                if resolved:
                    return resolved, ''  # inline 不挂任何变量
    # 2) host CSS rules
    # 找所有命中此元素的 selector，取最后定义、含 class/id 更优
    matched_rules = []
    for sel, props in sel_index.items():
        if prop_name not in props:
            continue
        try:
            if el in soup.select(sel):
                # specificity 估计
                spec = sel.count('.') + sel.count('#') * 2 + sel.count('[')
                if sel.startswith('.') or sel.startswith('#'):
                    spec += 1
                matched_rules.append((spec, sel, props[prop_name]))
        except Exception:
            continue
    if not matched_rules:
        return '', ''
    matched_rules.sort(key=lambda x: x[0], reverse=True)
    raw_value = matched_rules[0][2]
    resolved = _resolve_var_to_hex(raw_value, var_to_hex)
    # 找 source var (如果值是 var(--x))
    m = re.search(r'var\(\s*(--[^\s,)]+)', raw_value)
    src_var = m.group(1) if m else ''
    return resolved, src_var


# 不参与统计的标签
_SKIP_TAGS = {'script', 'style', 'link', 'meta', 'br', 'hr', 'svg', 'path',
              'input', 'button', 'select', 'textarea', 'noscript', 'iframe', 'canvas'}


def _aggregate_color_usage(soup, parse_result) -> dict:
    """v1.8.0: 数据驱动颜色聚合

    扫遍所有可见 DOM 节点，统计：
      - text:  color 属性 → 按"该元素直接文字字符数"加权
      - bg:    background-color → 按"元素出现次数"计（无法精确估面积）
      - border:border-color / border-*-color → 按"元素出现次数"计

    输出 {category: [(hex, weight, [source_vars]), ...]}（已按 weight 降序，做过 hex 距离 < 20 合并）
    """
    if not soup or not soup.body:
        return {'text': [], 'bg': [], 'border': []}

    # 构造 var_to_hex（递归解析）
    var_to_hex = {}
    if parse_result:
        for v in parse_result.variables:
            var_to_hex[v.name] = v.raw_value

    sel_index = _build_selector_rule_index(parse_result)

    text_buckets = {}    # {hex: [char_count, set(source_vars)]}
    bg_buckets = {}
    border_buckets = {}

    # 限制扫描数量，防止超大 HTML 卡死
    MAX_ELEMENTS_SCAN = 3000
    count = 0
    for el in soup.body.descendants:
        if count >= MAX_ELEMENTS_SCAN:
            break
        name = getattr(el, 'name', None)
        if not name:
            continue
        if name in _SKIP_TAGS:
            continue
        count += 1

        # === 文字色 ===
        # 只对"有直接文字"的节点统计
        direct_text = ''
        for child in el.children:
            if isinstance(child, NavigableString) and not isinstance(child, type(soup).Comment if False else type(None)):
                t = str(child).strip()
                if t:
                    direct_text += t
        if direct_text:
            char_count = len(direct_text)
            hex_v, src_var = _compute_prop_for_element(el, 'color', sel_index, var_to_hex, soup)
            if hex_v:
                bucket = text_buckets.setdefault(hex_v, [0, set()])
                bucket[0] += char_count
                if src_var:
                    bucket[1].add(src_var)

        # === 背景色 ===
        bg_hex, bg_var = _compute_prop_for_element(el, 'background-color', sel_index, var_to_hex, soup)
        if not bg_hex:
            # 试 background 简写
            bg_hex, bg_var = _compute_prop_for_element(el, 'background', sel_index, var_to_hex, soup)
        if bg_hex:
            bucket = bg_buckets.setdefault(bg_hex, [0, set()])
            bucket[0] += 1
            if bg_var:
                bucket[1].add(bg_var)

        # === 边框色 ===
        for bprop in ['border-color', 'border-top-color', 'border-bottom-color',
                      'border-left-color', 'border-right-color', 'border']:
            bd_hex, bd_var = _compute_prop_for_element(el, bprop, sel_index, var_to_hex, soup)
            if bd_hex:
                bucket = border_buckets.setdefault(bd_hex, [0, set()])
                bucket[0] += 1
                if bd_var:
                    bucket[1].add(bd_var)
                break

    def _merge_and_sort(buckets: dict, threshold: float = 12.0):
        # 按 weight 降序排
        items = sorted(buckets.items(), key=lambda kv: -kv[1][0])
        merged = []  # [(hex, weight, set(vars))]
        for hx, (w, vs) in items:
            placed = False
            for i, (mh, mw, mv) in enumerate(merged):
                if _hex_distance(hx, mh) < threshold:
                    merged[i] = (mh, mw + w, mv | vs)  # 合并到已有代表
                    placed = True
                    break
            if not placed:
                merged.append((hx, w, set(vs)))
        merged.sort(key=lambda x: -x[1])
        return [(h, w, sorted(vs)) for h, w, vs in merged]

    return {
        'text':   _merge_and_sort(text_buckets),
        'bg':     _merge_and_sort(bg_buckets),
        'border': _merge_and_sort(border_buckets),
    }
