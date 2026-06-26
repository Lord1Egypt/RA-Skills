#!/usr/bin/env python3
"""
parse_css.py — CSS 变量解析模块
从 HTML 的 <style> 标签中提取 CSS 变量，进行语义识别和分组。
"""

import re
from dataclasses import dataclass, field
from typing import Literal
from bs4 import BeautifulSoup


# CSS 命名色（常见的子集，用于识别颜色值）
CSS_NAMED_COLORS = {
    'black', 'white', 'red', 'green', 'blue', 'yellow', 'orange', 'purple',
    'pink', 'cyan', 'magenta', 'gray', 'grey', 'silver', 'gold', 'navy',
    'teal', 'maroon', 'olive', 'lime', 'aqua', 'fuchsia', 'coral',
    'salmon', 'crimson', 'indigo', 'violet', 'khaki', 'plum', 'orchid',
    'tan', 'tomato', 'turquoise', 'wheat', 'sienna', 'peru', 'ivory',
    'beige', 'lavender', 'linen', 'mintcream', 'honeydew', 'aliceblue',
    'antiquewhite', 'azure', 'bisque', 'blanchedalmond', 'burlywood',
    'cadetblue', 'chartreuse', 'chocolate', 'cornflowerblue', 'cornsilk',
    'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen',
    'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid',
    'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray',
    'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray',
    'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'gainsboro',
    'ghostwhite', 'goldenrod', 'greenyellow', 'hotpink', 'indianred',
    'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan',
    'lightgoldenrodyellow', 'lightgray', 'lightgreen', 'lightpink',
    'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray',
    'lightsteelblue', 'lightyellow', 'limegreen', 'mediumaquamarine',
    'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen',
    'mediumslateblue', 'mediumspringgreen', 'mediumturquoise',
    'mediumvioletred', 'midnightblue', 'mistyrose', 'moccasin',
    'navajowhite', 'oldlace', 'olivedrab', 'orangered', 'palegoldenrod',
    'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip',
    'peachpuff', 'powderblue', 'rosybrown', 'royalblue', 'saddlebrown',
    'sandybrown', 'seagreen', 'seashell', 'skyblue', 'slateblue',
    'slategray', 'snow', 'springgreen', 'steelblue', 'thistle',
    'transparent', 'inherit', 'currentColor',
}

# 中文 label 词典映射
WORD_MAP = {
    'primary': '主', 'secondary': '次', 'accent': '强调',
    'bg': '背景', 'background': '背景', 'text': '文字',
    'card': '卡片', 'surface': '表面', 'border': '边框',
    'title': '标题', 'body': '正文', 'heading': '标题',
    'safe': '安全', 'warn': '警告', 'danger': '危险', 'error': '错误',
    'success': '成功', 'info': '信息',
    'blue': '蓝', 'red': '红', 'green': '绿', 'purple': '紫',
    'orange': '橙', 'yellow': '黄', 'pink': '粉', 'white': '白',
    'black': '黑', 'gray': '灰', 'grey': '灰', 'dark': '深',
    'light': '浅', 'muted': '弱化', 'subtle': '微妙',
    'size': '大小', 'font': '字', 'fs': '字号', 'gap': '间距',
    'space': '间距', 'spacing': '间距',
    'padding': '内边距', 'pad': '内边距',
    'margin': '外边距',
    'radius': '圆角', 'round': '圆角',
    'shadow': '阴影', 'elevation': '层级',
    'color': '色', 'colour': '色',
    'hero': '主视觉', 'nav': '导航', 'header': '头部', 'footer': '底部',
    'sidebar': '侧栏', 'modal': '弹窗', 'overlay': '遮罩',
    'gradient': '渐变', 'hover': '悬停', 'active': '激活',
    'focus': '聚焦', 'disabled': '禁用',
    'container': '容器', 'wrapper': '包裹', 'content': '内容',
    'main': '主', 'sub': '副', 'alt': '备选',
    'link': '链接', 'btn': '按钮', 'button': '按钮',
    'input': '输入框', 'form': '表单',
}


@dataclass
class CSSVar:
    """单个 CSS 变量的完整描述"""
    name: str              # e.g. "--primary-blue"
    raw_value: str         # e.g. "#3B82F6"
    semantic: str          # 'color' | 'size' | 'spacing' | 'shadow' | 'radius' | 'gradient' | 'other'
    group: str             # 推断的分组名
    label_zh: str          # 自动生成的中文 label
    label_en: str          # 英文 label
    source_selector: str   # 定义所在的选择器


@dataclass
class CSSRule:
    """一条 CSS 规则"""
    selector: str
    properties: dict       # {property: value}
    referenced_vars: list  # 引用的 CSS 变量名列表


@dataclass
class ParseResult:
    """CSS 解析的完整结果"""
    variables: list        # list[CSSVar]
    rules: list            # list[CSSRule]
    var_to_selectors: dict # var_name → [(selector, property)]
    raw_css: str           # 合并后的完整 CSS 文本


def extract_numeric(value: str):
    """从 CSS 值中提取数值部分"""
    m = re.match(r'^([\d.]+)', value.strip())
    if m:
        try:
            return float(m.group(1))
        except ValueError:
            return None
    return None


def classify_var(name: str, value: str) -> str:
    """启发式判断变量语义类型"""
    value_lower = value.strip().lower()

    # 颜色：#hex / rgb() / hsl() / oklch() / named colors
    if re.match(r'^#[0-9a-f]{3,8}$', value_lower):
        return 'color'
    if re.match(r'^(rgb|rgba|hsl|hsla|oklch|lab|lch)\(', value_lower):
        return 'color'
    if value_lower in CSS_NAMED_COLORS:
        return 'color'

    # 渐变
    if 'gradient' in value_lower:
        return 'gradient'

    # box-shadow
    if 'shadow' in name or re.match(r'^\d+px\s+\d+px', value_lower):
        return 'shadow'

    # 字体族（font-family 值）—— 必须在 size 判断之前
    # 包含逗号分隔的字体名、sans-serif/serif/monospace 等通用族名
    font_family_keywords = ['sans-serif', 'serif', 'monospace', 'cursive', 'fantasy',
                           'system-ui', 'ui-sans-serif', 'ui-serif', 'ui-monospace']
    if any(kw in value_lower for kw in font_family_keywords):
        return 'other'
    # 引号包裹的字体名
    if re.match(r"""^['"][^'"]+['"]""", value_lower):
        return 'other'

    # 尺寸判断
    num = extract_numeric(value_lower)
    if num is not None and any(u in value_lower for u in ['px', 'em', 'rem', 'vw', 'vh', '%']):
        if 'size' in name or 'font' in name or 'fs' in name:
            return 'size'
        if 'gap' in name or 'spacing' in name or 'padding' in name or 'margin' in name or 'space' in name:
            return 'spacing'
        if 'radius' in name or 'round' in name:
            return 'radius'

    # clamp() 表达式
    if value_lower.startswith('clamp('):
        if 'size' in name or 'font' in name or 'fs' in name:
            return 'size'
        return 'spacing'

    # 按变量名兜底判断颜色
    color_keywords = ['color', 'bg', 'text', 'accent', 'primary', 'surface',
                      'secondary', 'border', 'card', 'hover', 'active', 'focus',
                      'muted', 'subtle', 'foreground', 'background']
    if any(k in name for k in color_keywords):
        # 再次验证值是否可能是颜色（排除明显非颜色值）
        if not re.match(r'^[\d.]+\s*(px|em|rem|vw|vh|%|s|ms)$', value_lower):
            return 'color'

    if any(k in name for k in ['size', 'font', 'fs']):
        return 'size'
    if any(k in name for k in ['gap', 'space', 'pad', 'margin']):
        return 'spacing'

    return 'other'


def resolve_var_value(var_name: str, var_dict: dict, visited: set = None, max_depth: int = 5) -> str:
    """递归解析变量引用链，获取最终字面值"""
    if visited is None:
        visited = set()
    if var_name in visited or max_depth <= 0:
        return var_dict.get(var_name, '')
    visited.add(var_name)

    value = var_dict.get(var_name, '')
    # 检查是否引用了另一个变量
    ref_match = re.match(r'^\s*var\((--[\w-]+)', value)
    if ref_match:
        ref_name = ref_match.group(1)
        if ref_name in var_dict:
            return resolve_var_value(ref_name, var_dict, visited, max_depth - 1)
    return value


def generate_label(var_name: str) -> tuple:
    """从变量名生成 (中文label + 英文label, 英文label)"""
    # 去掉 -- 前缀
    name = var_name.lstrip('-')
    # 分词
    words = re.split(r'[-_]', name)
    words = [w for w in words if w]  # 过滤空串

    # 英文 label：Title Case
    en_label = ' '.join(w.capitalize() for w in words)

    # 中文 label：词典映射
    zh_parts = [WORD_MAP.get(w.lower(), w) for w in words]
    zh_label = ''.join(zh_parts)

    # 组合格式
    full_label = f"{zh_label} {en_label}"
    return full_label, en_label


def infer_group(var_name: str, semantic: str) -> str:
    """推断变量的分组名"""
    name = var_name.lstrip('-')
    parts = re.split(r'[-_]', name)
    if len(parts) >= 2:
        prefix = parts[0].lower()
        # 常见的有意义前缀
        meaningful_prefixes = {
            'text', 'bg', 'card', 'border', 'surface', 'accent',
            'primary', 'secondary', 'nav', 'header', 'footer',
            'btn', 'button', 'link', 'input', 'modal', 'hero',
            'font', 'size', 'space', 'gap',
        }
        if prefix in meaningful_prefixes:
            return prefix

    # 兜底按语义类型分组
    group_map = {
        'color': 'colors',
        'size': 'typography',
        'spacing': 'spacing',
        'radius': 'shape',
        'shadow': 'effects',
        'gradient': 'effects',
        'other': 'other',
    }
    return group_map.get(semantic, 'other')


def parse_css_from_html(html_content: str) -> ParseResult:
    """
    解析 HTML 中所有 <style> 标签的 CSS 内容。
    提取 CSS 变量定义和规则，构建反查索引。
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # 合并所有 <style> 标签内容
    style_blocks = []
    for style_tag in soup.find_all('style'):
        if style_tag.string:
            style_blocks.append(style_tag.string)
    raw_css = '\n'.join(style_blocks)

    # 第一遍：提取所有变量定义（仅取 :root 中的作为默认值）
    # 匹配 :root { ... } 块
    var_dict = {}  # name → raw_value
    var_selectors = {}  # name → source_selector

    # 解析所有规则块
    # 使用正则匹配 selector { ... } 结构
    rule_pattern = re.compile(r'([^{}@]+?)\s*\{([^{}]*)\}', re.DOTALL)
    rules = []

    for match in rule_pattern.finditer(raw_css):
        selector = match.group(1).strip()
        block = match.group(2)

        # 跳过 @media 等 at-rule 内部（简化处理）
        if selector.startswith('@'):
            continue

        properties = {}
        referenced_vars = []

        # 解析每个属性声明
        for prop_match in re.finditer(r'([\w-]+)\s*:\s*([^;]+)', block):
            prop_name = prop_match.group(1).strip()
            prop_value = prop_match.group(2).strip()
            properties[prop_name] = prop_value

            # 收集引用的 CSS 变量
            for var_ref in re.findall(r'var\((--[\w-]+)', prop_value):
                if var_ref not in referenced_vars:
                    referenced_vars.append(var_ref)

            # 如果是变量定义（以 -- 开头的属性名）
            if prop_name.startswith('--'):
                # 优先取 :root 定义
                clean_selector = re.sub(r'\s+', ' ', selector).strip()
                is_root = ':root' in clean_selector or clean_selector in ['html', '*']
                if is_root or prop_name not in var_dict:
                    var_dict[prop_name] = prop_value
                    var_selectors[prop_name] = clean_selector

        if properties:
            rules.append(CSSRule(
                selector=selector.strip(),
                properties=properties,
                referenced_vars=referenced_vars
            ))

    # 解析变量，递归解析引用
    variables = []
    for name, raw_value in var_dict.items():
        # 递归解析变量引用获得最终值
        resolved_value = resolve_var_value(name, var_dict)
        # 语义分类
        semantic = classify_var(name, resolved_value)
        # 生成 label
        full_label, en_label = generate_label(name)
        # 推断分组
        group = infer_group(name, semantic)

        variables.append(CSSVar(
            name=name,
            raw_value=raw_value,
            semantic=semantic,
            group=group,
            label_zh=full_label,
            label_en=en_label,
            source_selector=var_selectors.get(name, ':root')
        ))

    # 构建反查索引：变量 → 使用该变量的 [(selector, property)]
    var_to_selectors = {}
    for rule in rules:
        for prop_name, prop_value in rule.properties.items():
            for var_ref in re.findall(r'var\((--[\w-]+)', prop_value):
                if var_ref not in var_to_selectors:
                    var_to_selectors[var_ref] = []
                var_to_selectors[var_ref].append((rule.selector, prop_name))

    return ParseResult(
        variables=variables,
        rules=rules,
        var_to_selectors=var_to_selectors,
        raw_css=raw_css
    )


def count_css_variables(parse_result: ParseResult) -> dict:
    """统计各语义类型的变量数量"""
    counts = {}
    for var in parse_result.variables:
        counts[var.semantic] = counts.get(var.semantic, 0) + 1
    return counts


def get_color_vars(parse_result: ParseResult) -> list:
    """获取所有颜色类型的变量"""
    return [v for v in parse_result.variables if v.semantic == 'color']


def get_size_vars(parse_result: ParseResult) -> list:
    """获取所有字号/尺寸类型的变量"""
    return [v for v in parse_result.variables if v.semantic == 'size']


def get_spacing_vars(parse_result: ParseResult) -> list:
    """获取所有间距类型的变量"""
    return [v for v in parse_result.variables if v.semantic == 'spacing']
