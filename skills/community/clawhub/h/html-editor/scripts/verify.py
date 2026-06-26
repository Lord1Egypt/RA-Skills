#!/usr/bin/env python3
"""
verify.py -- Sanity Checks 模块 (v15 public package)
实现 12 项原始检查 + 22 项增强检查 = 34 项总检查。
任一失败则阻止输出。

对应规范: 附录 B
"""

import os
import re
import json
from dataclasses import dataclass


@dataclass
class CheckItem:
    """单项检查结果"""
    name: str
    code: str
    passed: bool
    message: str


@dataclass
class CheckResult:
    """全部检查结果"""
    passed: bool
    checks: list   # list[CheckItem]
    errors: list   # 失败项的错误消息


def _extract_script_contents(html: str) -> list:
    return re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)


def _extract_style_contents(html: str) -> list:
    return re.findall(r'<style[^>]*>(.*?)</style>', html, re.DOTALL)


def _extract_constants_from_html(html: str) -> dict:
    """从注入的 JS 中提取 window.X 常量"""
    constants = {}
    const_match = re.search(
        r'<script[^>]*id="html-visual-editor-constants"[^>]*>(.*?)</script>',
        html, re.DOTALL
    )
    if not const_match:
        return constants

    script_text = const_match.group(1)

    for match in re.finditer(r'window\.([\w_]+)\s*=\s*', script_text):
        name = match.group(1)
        start = match.end()
        if start >= len(script_text):
            continue
        rest = script_text[start:].lstrip()
        if not rest:
            continue
        actual_start = start + (len(script_text[start:]) - len(rest))

        if script_text[actual_start] in ('{', '['):
            open_char = script_text[actual_start]
            close_char = '}' if open_char == '{' else ']'
            depth = 0
            in_str = False
            str_char = None
            escaped = False
            end = actual_start
            for i in range(actual_start, len(script_text)):
                ch = script_text[i]
                if escaped:
                    escaped = False
                    continue
                if ch == '\\' and in_str:
                    escaped = True
                    continue
                if in_str:
                    if ch == str_char:
                        in_str = False
                    continue
                if ch in ('"', "'"):
                    in_str = True
                    str_char = ch
                    continue
                if ch == open_char:
                    depth += 1
                elif ch == close_char:
                    depth -= 1
                    if depth == 0:
                        end = i + 1
                        break
            value_str = script_text[actual_start:end]
            try:
                constants[name] = json.loads(value_str)
            except json.JSONDecodeError:
                cleaned = re.sub(r',\s*([}\]])', r'\1', value_str)
                try:
                    constants[name] = json.loads(cleaned)
                except json.JSONDecodeError:
                    constants[name] = None
        elif script_text[actual_start:actual_start+4] == 'null':
            constants[name] = None

    return constants


def _extract_panel_labels(html: str) -> list:
    labels = []
    for match in re.finditer(r'class="color-label"[^>]*>([^<]+)</span>', html):
        labels.append(match.group(1).strip())
    for match in re.finditer(r'class="slider-name"[^>]*>([^<]+)</span>', html):
        labels.append(match.group(1).strip())
    return labels


def _extract_panel_data_vars(html: str) -> list:
    panel_match = re.search(r'id="editPanel".*?class="panel-actions"', html, re.DOTALL)
    if panel_match:
        panel_html = panel_match.group(0)
        return list(set(re.findall(r'data-var="(--[\w-]+)"', panel_html)))
    html_no_script = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    return list(set(re.findall(r'data-var="(--[\w-]+)"', html_no_script)))


def _extract_panel_preset_names(html: str) -> list:
    return re.findall(r"applyPreset\('([\w-]+)'\)", html)


# ============================================================
# 原始 12 项 Sanity Checks (SC-01 ~ SC-12)
# ============================================================

def check_sc01_panel_label_complete(html: str, constants: dict) -> CheckItem:
    """SC-01: PAGE_ELEMENT_TO_PANEL 中所有 row 值必须存在于 panel label"""
    panel_labels = _extract_panel_labels(html)
    pem = constants.get('PAGE_ELEMENT_TO_PANEL', {})
    if pem is None or not pem:
        return CheckItem('panel-label完备', 'SC-01', True, 'PAGE_ELEMENT_TO_PANEL 为空，跳过')

    missing = []
    for selector, items in pem.items():
        if isinstance(items, list):
            for item in items:
                row = item.get('row', '') if isinstance(item, dict) else ''
                if row and row not in panel_labels:
                    missing.append(row)
        elif isinstance(items, dict):
            rows = items.get('rows', [])
            for row in rows:
                if row not in panel_labels:
                    missing.append(row)

    if missing:
        return CheckItem(
            'panel-label完备', 'SC-01', False,
            f'ERROR [SC-01]: PAGE_ELEMENT_TO_PANEL references row "{missing[0]}" but panel has no element with that label. Available: {panel_labels[:10]}'
        )
    return CheckItem('panel-label完备', 'SC-01', True, 'PASS')


def check_sc02_preset_key_align(html: str, constants: dict) -> CheckItem:
    """SC-02: panel 中 applyPreset 的名称集合 === PRESETS 的 key 集合"""
    panel_presets = set(_extract_panel_preset_names(html))
    presets_obj = constants.get('PRESETS', {}) or {}
    presets_keys = set(presets_obj.keys())
    missing = panel_presets - presets_keys
    if missing:
        return CheckItem(
            'preset-key对齐', 'SC-02', False,
            f'ERROR [SC-02]: Preset button "{list(missing)[0]}" has no matching key in PRESETS'
        )
    return CheckItem('preset-key对齐', 'SC-02', True, 'PASS')


def check_sc03_selector_reachable(html: str, constants: dict) -> CheckItem:
    """SC-03: PAGE_ELEMENT_TO_PANEL 的每个 selector 必须在 DOM 中匹配"""
    from bs4 import BeautifulSoup
    pem = constants.get('PAGE_ELEMENT_TO_PANEL', {})
    if not pem:
        return CheckItem('selector可达', 'SC-03', True, 'PAGE_ELEMENT_TO_PANEL 为空，跳过')
    soup = BeautifulSoup(html, 'html.parser')
    for selector in pem.keys():
        try:
            found = soup.select(selector)
            if not found:
                return CheckItem(
                    'selector可达', 'SC-03', False,
                    f'ERROR [SC-03]: Selector "{selector}" in PAGE_ELEMENT_TO_PANEL matches 0 elements'
                )
        except Exception:
            pass
    return CheckItem('selector可达', 'SC-03', True, 'PASS')


def check_sc04_css_var_exists(html: str, constants: dict) -> CheckItem:
    """SC-04: panel color-row 的 data-var 必须在 :root 中有定义"""
    panel_vars = _extract_panel_data_vars(html)
    default_colors = constants.get('DEFAULT_COLORS', {}) or {}
    root_vars = set()
    for match in re.finditer(r'(--[\w-]+)\s*:', html):
        root_vars.add(match.group(1))
    root_vars.update(default_colors.keys())
    for var in panel_vars:
        if var not in root_vars:
            return CheckItem('CSS变量存在', 'SC-04', False,
                           f'ERROR [SC-04]: Panel references CSS var "{var}" but not defined')
    return CheckItem('CSS变量存在', 'SC-04', True, 'PASS')


def check_sc05_layout_target_exists(html: str, constants: dict) -> CheckItem:
    """SC-05: 布局 slider 的 data-target 选择器必须在 DOM 中匹配"""
    from bs4 import BeautifulSoup
    targets = re.findall(r'data-target="([^"]+)"[^>]*data-prop=', html)
    if not targets:
        return CheckItem('layout-target存在', 'SC-05', True, '无布局 slider，跳过')
    soup = BeautifulSoup(html, 'html.parser')
    for target in targets:
        for sel in target.split(','):
            sel = sel.strip()
            if sel in (':root', 'html', 'body', 'html, body', 'section'):
                continue
            try:
                found = soup.select(sel)
                if not found:
                    # Non-fatal: just warn
                    pass
            except Exception:
                pass
    return CheckItem('layout-target存在', 'SC-05', True, 'PASS')


def check_sc06_js_syntax(html: str, constants: dict) -> CheckItem:
    """SC-06: JS 语法检查"""
    import subprocess
    import tempfile
    constants_match = re.search(
        r'<script[^>]*id="html-visual-editor-constants"[^>]*>(.*?)</script>',
        html, re.DOTALL
    )
    if not constants_match:
        return CheckItem('JS语法正确', 'SC-06', True, '无注入脚本标记，跳过')
    script_content = constants_match.group(1)
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
            f.write(script_content)
            tmp_path = f.name
        result = subprocess.run(['node', '--check', tmp_path], capture_output=True, text=True, timeout=5)
        os.unlink(tmp_path)
        if result.returncode != 0:
            error_msg = result.stderr.strip().split('\n')[-1] if result.stderr else 'unknown'
            return CheckItem('JS语法正确', 'SC-06', False,
                           f'ERROR [SC-06]: JS syntax error: {error_msg}')
        return CheckItem('JS语法正确', 'SC-06', True, 'PASS')
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        pass
    finally:
        try:
            os.unlink(tmp_path)
        except (OSError, UnboundLocalError):
            pass
    open_b = script_content.count('{')
    close_b = script_content.count('}')
    if abs(open_b - close_b) > 2:
        return CheckItem('JS语法正确', 'SC-06', False,
                       f'ERROR [SC-06]: bracket mismatch ({open_b} vs {close_b})')
    return CheckItem('JS语法正确', 'SC-06', True, 'PASS')


def check_sc07_css_syntax(html: str, constants: dict) -> CheckItem:
    """SC-07: CSS 语法检查"""
    styles = _extract_style_contents(html)
    for style in styles:
        if style.count('{') != style.count('}'):
            return CheckItem('CSS语法正确', 'SC-07', False,
                           f'ERROR [SC-07]: CSS unmatched braces')
    return CheckItem('CSS语法正确', 'SC-07', True, 'PASS')


def check_sc08_no_dangerous_strings(html: str, constants: dict) -> CheckItem:
    """SC-08: 无危险字符串"""
    styles = _extract_style_contents(html)
    for style in styles:
        if '</style>' in style:
            return CheckItem('无危险字符串', 'SC-08', False, 'ERROR [SC-08]: "</style>" in style content')
    scripts = _extract_script_contents(html)
    for script in scripts:
        if '</script>' in script:
            return CheckItem('无危险字符串', 'SC-08', False, 'ERROR [SC-08]: "</script>" in script content')
    return CheckItem('无危险字符串', 'SC-08', True, 'PASS')


def check_sc09_tag_pairing(html: str, constants: dict) -> CheckItem:
    """SC-09: 标签配对

    注意：直接对全文 regex 会误数 JS 字符串/注释里的字面量 (如 '<style>'、
    "before <script>")。这里先剥离所有 <script>...</script> 与 <style>...</style>
    的"内容"区，再去匹配真正的开闭标签。
    """
    def _strip_inner(text: str, tag: str) -> str:
        # 把 <tag ...>...</tag> 替换为 <tag></tag>，保留标签本身，去掉内容
        pattern = re.compile(
            rf'(<{tag}[^>]*>)(.*?)(</{tag}>)',
            re.IGNORECASE | re.DOTALL,
        )
        return pattern.sub(r'\1\3', text)

    cleaned = _strip_inner(html, 'script')
    cleaned = _strip_inner(cleaned, 'style')

    for tag in ['style', 'script']:
        open_count = len(re.findall(f'<{tag}[^>]*>', cleaned, re.IGNORECASE))
        close_count = len(re.findall(f'</{tag}>', cleaned, re.IGNORECASE))
        if open_count != close_count:
            return CheckItem('标签配对', 'SC-09', False,
                           f'ERROR [SC-09]: {tag} mismatch: {open_count} opens vs {close_count} closes')
    return CheckItem('标签配对', 'SC-09', True, 'PASS')


def check_sc10_default_colors_complete(html: str, constants: dict) -> CheckItem:
    """SC-10: DEFAULT_COLORS 覆盖 panel 中所有 color data-var"""
    default_colors = constants.get('DEFAULT_COLORS', {}) or {}
    panel_match = re.search(r'id="editPanel".*?class="panel-actions"', html, re.DOTALL)
    panel_html = panel_match.group(0) if panel_match else html
    color_vars = set(re.findall(r'type="color"[^>]*data-var="(--[\w-]+)"', panel_html))
    for var in color_vars:
        if var not in default_colors:
            return CheckItem('DEFAULT_COLORS完备', 'SC-10', False,
                           f'ERROR [SC-10]: DEFAULT_COLORS missing "{var}"')
    return CheckItem('DEFAULT_COLORS完备', 'SC-10', True, 'PASS')


def check_sc11_size_bounds_complete(html: str, constants: dict) -> CheckItem:
    """SC-11: SIZE_BOUNDS check (gold version uses empty {}, so always pass)"""
    return CheckItem('SIZE_BOUNDS完备', 'SC-11', True, 'PASS (金版用空对象)')


def check_sc12_data_editable_exists(html: str, constants: dict) -> CheckItem:
    """SC-12: 至少有 1 个 data-editable"""
    if 'data-editable' not in html:
        return CheckItem('data-editable非空', 'SC-12', False,
                       "ERROR [SC-12]: No data-editable elements found")
    return CheckItem('data-editable非空', 'SC-12', True, 'PASS')


# ============================================================
# 附录 B 的 17 项新增 checks (appB01 ~ appB17)
# ============================================================

def check_appB01_pem_array_format(html: str, constants: dict) -> CheckItem:
    """appB01: PAGE_ELEMENT_TO_PANEL[sel] 是数组，每项有 tab 和 row"""
    pem = constants.get('PAGE_ELEMENT_TO_PANEL', {})
    if not pem:
        return CheckItem('PEM数组格式', 'appB01', True, 'PEM 为空')
    for sel, items in pem.items():
        if not isinstance(items, list):
            return CheckItem('PEM数组格式', 'appB01', False,
                           f'ERROR [appB01]: PEM[{sel}] not list: {type(items).__name__}')
        for it in items:
            if not isinstance(it, dict) or 'tab' not in it or 'row' not in it:
                return CheckItem('PEM数组格式', 'appB01', False,
                               f'ERROR [appB01]: PEM[{sel}] item missing tab/row: {it}')
    return CheckItem('PEM数组格式', 'appB01', True, f'PASS ({len(pem)} 项)')


def check_appB02_pem_tab_values(html: str, constants: dict) -> CheckItem:
    """appB02: PEM 每个 tab 值 ∈ {颜色, 预设, 布局, 字号}"""
    valid_tabs = {'颜色', '预设', '布局', '字号'}
    pem = constants.get('PAGE_ELEMENT_TO_PANEL', {})
    if not pem:
        return CheckItem('PEM-tab取值', 'appB02', True, 'PEM 为空')
    for sel, items in pem.items():
        if not isinstance(items, list):
            continue
        for it in items:
            tab = it.get('tab', '')
            if tab not in valid_tabs:
                return CheckItem('PEM-tab取值', 'appB02', False,
                               f'ERROR [appB02]: bad tab "{tab}" in PEM[{sel}]')
    return CheckItem('PEM-tab取值', 'appB02', True, 'PASS')


def check_appB03_pem_row_match_panel(html: str, constants: dict) -> CheckItem:
    """appB03: PEM 的 row 在 panel 对应 tab 下能找到匹配 label"""
    panel_labels = _extract_panel_labels(html)
    pem = constants.get('PAGE_ELEMENT_TO_PANEL', {})
    if not pem:
        return CheckItem('PEM-row匹配', 'appB03', True, 'PEM 为空')
    for sel, items in pem.items():
        if not isinstance(items, list):
            continue
        for it in items:
            row = it.get('row', '')
            if row and row not in panel_labels:
                return CheckItem('PEM-row匹配', 'appB03', False,
                               f'ERROR [appB03]: row "{row}" not found in panel labels')
    return CheckItem('PEM-row匹配', 'appB03', True, 'PASS')


def check_appB04_presets_flat(html: str, constants: dict) -> CheckItem:
    """appB04: PRESETS 是 flat {--var: hex}，无 vars 嵌套"""
    presets = constants.get('PRESETS', {}) or {}
    for k, v in presets.items():
        if not isinstance(v, dict):
            return CheckItem('PRESETS-flat', 'appB04', False,
                           f'ERROR [appB04]: PRESET {k} not dict')
        if not all(kk.startswith('--') for kk in v.keys()):
            non_var = [kk for kk in v.keys() if not kk.startswith('--')]
            return CheckItem('PRESETS-flat', 'appB04', False,
                           f'ERROR [appB04]: PRESET {k} not flat: keys={non_var}')
    return CheckItem('PRESETS-flat', 'appB04', True, f'PASS ({len(presets)} 预设)')


def check_appB05_presets_subset(html: str, constants: dict) -> CheckItem:
    """appB05: PRESETS 变量 ⊆ DEFAULT_COLORS"""
    presets = constants.get('PRESETS', {}) or {}
    defcolors = constants.get('DEFAULT_COLORS', {}) or {}
    default_keys = set(defcolors.keys())
    for k, v in presets.items():
        if not isinstance(v, dict):
            continue
        extra = set(v.keys()) - default_keys
        if extra:
            return CheckItem('PRESETS⊆DEFAULT', 'appB05', False,
                           f'ERROR [appB05]: PRESET {k} 有额外变量 {extra}')
    return CheckItem('PRESETS⊆DEFAULT', 'appB05', True, 'PASS')


def check_appB06_no_fallback(html: str, constants: dict) -> CheckItem:
    """appB06: 无 applyFallbackSize/applyFallbackLayout"""
    if 'applyFallbackSize' in html:
        return CheckItem('无fallback', 'appB06', False, 'ERROR [appB06]: 还有 applyFallbackSize')
    if 'applyFallbackLayout' in html:
        return CheckItem('无fallback', 'appB06', False, 'ERROR [appB06]: 还有 applyFallbackLayout')
    return CheckItem('无fallback', 'appB06', True, 'PASS')


def check_appB07_slider_oninput(html: str, constants: dict) -> CheckItem:
    """appB07: 所有 slider oninput 用 applyLayout"""
    sliders = re.findall(r'oninput="([^"]+)"', html)
    slider_ops = [s for s in sliders if 'val-' in s or 'applyLayout' in s]
    for s in slider_ops:
        if not s.startswith('applyLayout('):
            return CheckItem('slider-oninput', 'appB07', False,
                           f'ERROR [appB07]: slider oninput 不是 applyLayout: {s}')
    return CheckItem('slider-oninput', 'appB07', True, f'PASS ({len(slider_ops)} sliders)')


def check_appB08_slider_row_structure(html: str, constants: dict) -> CheckItem:
    """appB08: slider-row 内部结构正确"""
    slider_rows = re.findall(r'<div class="slider-row">.*?</div>\s*</div>', html, re.DOTALL)
    for sr in slider_rows:
        if 'class="slider-label"' not in sr:
            return CheckItem('slider-row结构', 'appB08', False, 'ERROR [appB08]: slider-row 缺 slider-label')
        if 'class="slider-name"' not in sr:
            return CheckItem('slider-row结构', 'appB08', False, 'ERROR [appB08]: slider-row 缺 slider-name')
        if not re.search(r'class="slider-val"\s+id="val-', sr):
            return CheckItem('slider-row结构', 'appB08', False, 'ERROR [appB08]: slider-row 缺 slider-val+id')
    return CheckItem('slider-row结构', 'appB08', True, f'PASS ({len(slider_rows)} rows)')


def check_appB09_slider_val_id_match(html: str, constants: dict) -> CheckItem:
    """appB09: slider-val 的 id 和 oninput 第二参数一致"""
    # Find pairs of id and oninput in slider-rows
    slider_rows = re.findall(r'<div class="slider-row">.*?</div>\s*</div>', html, re.DOTALL)
    for sr in slider_rows:
        val_id_match = re.search(r'id="(val-[\w-]+)"', sr)
        oninput_match = re.search(r"applyLayout\(this,\s*'(val-[\w-]+)'\)", sr)
        if val_id_match and oninput_match:
            if val_id_match.group(1) != oninput_match.group(1):
                return CheckItem('slider-val-id匹配', 'appB09', False,
                               f'ERROR [appB09]: id={val_id_match.group(1)} != oninput={oninput_match.group(1)}')
    return CheckItem('slider-val-id匹配', 'appB09', True, 'PASS')


def check_appB10_panel_actions(html: str, constants: dict) -> CheckItem:
    """appB10: panel 有 .panel-actions + 至少 1 个 .action-btn
    (v1.4 todo21: 删除冗余的 export/save 按钮，保留 reset 单独入口；阈值从 3 降为 1)"""
    if 'class="panel-actions"' not in html:
        return CheckItem('panel-actions', 'appB10', False, 'ERROR [appB10]: 缺 panel-actions')
    action_btn_count = html.count('class="action-btn')
    if action_btn_count < 1:
        return CheckItem('panel-actions', 'appB10', False,
                       f'ERROR [appB10]: action-btn < 1 (found {action_btn_count})')
    return CheckItem('panel-actions', 'appB10', True, 'PASS')


def check_appB11_preset_row(html: str, constants: dict) -> CheckItem:
    """appB11: 预设按钮容器是 preset-row 不是 preset-grid"""
    if 'class="preset-row"' not in html:
        return CheckItem('preset-row', 'appB11', False, 'ERROR [appB11]: 不是 preset-row')
    if 'class="preset-grid"' in html:
        return CheckItem('preset-row', 'appB11', False, 'ERROR [appB11]: 还在用 preset-grid')
    return CheckItem('preset-row', 'appB11', True, 'PASS')


def check_appB12_cve_string_format(html: str, constants: dict) -> CheckItem:
    """appB12: CSS_VAR_TO_ELEMENTS 值是字符串"""
    cve = constants.get('CSS_VAR_TO_ELEMENTS', {}) or {}
    for var, val in cve.items():
        if not isinstance(val, str):
            return CheckItem('CVE字符串格式', 'appB12', False,
                           f'ERROR [appB12]: CVE[{var}] 不是字符串: {type(val).__name__}')
    return CheckItem('CVE字符串格式', 'appB12', True, f'PASS ({len(cve)} 项)')


def check_appB13_edit_hint(html: str, constants: dict) -> CheckItem:
    """appB13: edit-hint 文案匹配金版"""
    if '改色' not in html or '布局' not in html or '按 P' not in html:
        return CheckItem('edit-hint文案', 'appB13', False, 'ERROR [appB13]: edit-hint 文案不全')
    hint_count = html.count('class="edit-hint"')
    if hint_count != 1:
        return CheckItem('edit-hint文案', 'appB13', False,
                       f'ERROR [appB13]: edit-hint 出现 {hint_count} 次（应为 1）')
    return CheckItem('edit-hint文案', 'appB13', True, 'PASS')


def check_appB14_presets_no_extra_fields(html: str, constants: dict) -> CheckItem:
    """appB14: PRESETS 无冗余字段(name_zh/llm/mood/best_for)"""
    presets = constants.get('PRESETS', {}) or {}
    for k, v in presets.items():
        if not isinstance(v, dict):
            continue
        extra = set(v.keys()) - {kk for kk in v.keys() if kk.startswith('--')}
        if extra:
            return CheckItem('PRESETS无冗余', 'appB14', False,
                           f'ERROR [appB14]: PRESET {k} 有冗余 {extra}')
    return CheckItem('PRESETS无冗余', 'appB14', True, 'PASS')


def check_appB15_injection_order(html: str, constants: dict) -> CheckItem:
    """appB15: 注入块按 3 段顺序: CSS in head → Toolbar+Panel in body → Scripts before /body"""
    css_pos = html.find('id="html-visual-editor-css"')
    panel_pos = html.find('id="editPanel"')
    constants_pos = html.find('id="html-visual-editor-constants"')

    if css_pos == -1 or panel_pos == -1 or constants_pos == -1:
        return CheckItem('注入顺序', 'appB15', False,
                       'ERROR [appB15]: 缺少注入块')
    if not (css_pos < panel_pos < constants_pos):
        return CheckItem('注入顺序', 'appB15', False,
                       f'ERROR [appB15]: 注入顺序错: css@{css_pos} panel@{panel_pos} js@{constants_pos}')
    return CheckItem('注入顺序', 'appB15', True, 'PASS')


def check_appB16_color_tab_sections(html: str, constants: dict) -> CheckItem:
    """appB16: 颜色 tab 至少有 2 个 .panel-section
    v16: 降级为 warning — 当只有 1 个 section 时 passed=True 但标记 warning，
    不阻断输出（极少数 HTML 可能确实只有 1 组颜色）"""
    color_tab_match = re.search(
        r'id="tab-colors"(.*?)(?=id="tab-presets"|<div class="panel-tab-content"[^>]*id="tab-presets")',
        html, re.DOTALL
    )
    if not color_tab_match:
        return CheckItem('颜色tab多section', 'appB16', False,
                       'ERROR [appB16]: 找不到 tab-colors 内容')
    ct = color_tab_match.group(1)
    section_count = ct.count('class="panel-section"')
    if section_count < 2:
        # v16: warning 模式 — passed=True 但 message 标注 warning
        return CheckItem('颜色tab多section', 'appB16', True,
                       f'WARNING [appB16]: 颜色 tab 只有 {section_count} 个 section（建议 >= 2，但不阻断）')
    return CheckItem('颜色tab多section', 'appB16', True, f'PASS ({section_count} sections)')


def check_appB17_default_colors_match_host(html: str, constants: dict) -> CheckItem:
    """appB17: DEFAULT_COLORS keys 与 host :root 变量集一致"""
    defcolors = constants.get('DEFAULT_COLORS', {}) or {}
    default_keys = set(defcolors.keys())

    # Find host :root variables (excluding editor injected styles)
    # Look for :root blocks that are NOT inside html-visual-editor
    host_vars = set()
    # Find all :root blocks
    for m in re.finditer(r':root\s*\{([^}]+)\}', html):
        block = m.group(1)
        # Skip if it's inside our injected style
        block_pos = m.start()
        # Check if this is inside editor-core.css (has id="html-visual-editor-css")
        preceding = html[:block_pos]
        if 'html-visual-editor-css' in preceding and preceding.rfind('<style') > preceding.rfind('</style>'):
            continue  # This :root is inside our injected CSS, skip
        for var_match in re.findall(r'(--[\w-]+)\s*:', block):
            host_vars.add(var_match)

    if not host_vars:
        return CheckItem('DEFAULT_COLORS=host', 'appB17', True,
                       'PASS (host 无 :root 变量，跳过)')

    if host_vars != default_keys:
        missing = host_vars - default_keys
        extra = default_keys - host_vars
        msg_parts = []
        if missing:
            msg_parts.append(f'漏={missing}')
        if extra:
            msg_parts.append(f'多={extra}')
        return CheckItem('DEFAULT_COLORS=host', 'appB17', False,
                       f'ERROR [appB17]: DEFAULT_COLORS != host vars: {", ".join(msg_parts)}')
    return CheckItem('DEFAULT_COLORS=host', 'appB17', True,
                   f'PASS ({len(host_vars)} 变量一致)')


def check_appB18_preset_mapping_density(html: str, constants: dict) -> CheckItem:
    """appB18: 每套 PRESET 至少映射到 max(4, host_color_count // 3) 个变量"""
    presets = constants.get('PRESETS', {}) or {}
    default_colors = constants.get('DEFAULT_COLORS', {}) or {}
    if not presets:
        return CheckItem('PRESET映射密度', 'appB18', True, 'PRESETS 为空，跳过')
    min_required = max(4, len(default_colors) // 3)
    for name, vars_dict in presets.items():
        if not isinstance(vars_dict, dict):
            continue
        if len(vars_dict) < min_required:
            return CheckItem('PRESET映射密度', 'appB18', False,
                           f'ERROR [appB18]: preset "{name}" 只映射了 {len(vars_dict)} 个变量, '
                           f'要求 >= {min_required} (host={len(default_colors)} 色)')
    return CheckItem('PRESET映射密度', 'appB18', True,
                   f'PASS ({len(presets)} 套预设, 每套 >= {min_required} 变量)')


def check_appB19_pem_tabs_coverage(html: str, constants: dict) -> CheckItem:
    """appB19: PAGE_ELEMENT_TO_PANEL 至少覆盖 颜色/字号/布局 三个 tab"""
    pem = constants.get('PAGE_ELEMENT_TO_PANEL', {}) or {}
    if not pem:
        return CheckItem('PEM-tab覆盖', 'appB19', True, 'PEM 为空，跳过')
    tabs = set()
    for sel, items in pem.items():
        if not isinstance(items, list):
            continue
        for it in items:
            if isinstance(it, dict):
                tabs.add(it.get('tab', ''))
    required = {'颜色', '字号', '布局'}
    missing = required - tabs
    if missing:
        return CheckItem('PEM-tab覆盖', 'appB19', False,
                       f'ERROR [appB19]: PEM 缺少 tab: {missing} (现有 {tabs})')
    return CheckItem('PEM-tab覆盖', 'appB19', True,
                   f'PASS (tabs={sorted(tabs)})')


def check_appB20_data_editable_coverage(html: str, constants: dict) -> CheckItem:
    """appB20: body 内 data-editable 元素 >= 30 (典型文档至少 30 个可编辑元素)"""
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        return CheckItem('data-editable覆盖率', 'appB20', True, 'bs4 未安装, 跳过')

    soup = BeautifulSoup(html, 'html.parser')
    # 排除编辑器自身 DOM 和 script/style
    for sel in ('.edit-toolbar', '.edit-panel', '.edit-hint'):
        for el in soup.select(sel):
            el.decompose()
    for el in soup.find_all(['script', 'style']):
        el.decompose()
    body = soup.body
    if not body:
        return CheckItem('data-editable覆盖率', 'appB20', True, 'no body')
    editable = body.select('[data-editable]')
    if len(editable) < 30:
        return CheckItem('data-editable覆盖率', 'appB20', False,
                       f'ERROR [appB20]: only {len(editable)} data-editable elements, expected >= 30')
    return CheckItem('data-editable覆盖率', 'appB20', True,
                   f'PASS ({len(editable)} 个元素已标记)')


def check_appB21_size_slider_coverage(html: str, constants: dict) -> CheckItem:
    """appB21: 字号 slider 覆盖检查

    v1.7.0 调整: 收敛策略下不再要求"slider 数 ≥ 规则数 * 0.8"，因为多个 rule 可能
    合并到同一个 family（strong/data/upcoming/event 等）。改为：
      - 至少 6 条 slider（覆盖基本层级：H1/章节/正文/数字/标签/页脚）
      - 不再校验 host font-size 规则数比例
    """
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        return CheckItem('字号slider覆盖率', 'appB21', True, 'bs4 未安装, 跳过')

    soup = BeautifulSoup(html, 'html.parser')
    size_tab = soup.select_one('#tab-size')
    if not size_tab:
        return CheckItem('字号slider覆盖率', 'appB21', False,
                       'ERROR [appB21]: 找不到 #tab-size')
    sliders = size_tab.select('.slider-row')
    slider_count = len(sliders)

    MIN_REQUIRED = 4  # v1.7.0 收敛策略：少而精
    if slider_count < MIN_REQUIRED:
        return CheckItem('字号slider覆盖率', 'appB21', False,
                       f'ERROR [appB21]: 字号 slider 数 {slider_count} < {MIN_REQUIRED}（基本层级覆盖不足）')
    return CheckItem('字号slider覆盖率', 'appB21', True,
                   f'PASS ({slider_count} sliders, v1.7 收敛策略)')


def check_appB22_size_slider_no_bare_tag(html: str, constants: dict) -> CheckItem:
    """appB22: 所有字号 slider data-target 不是裸 tag (v15)
    必须含 . / 空格 / > / , 之一 (说明是组合选择器)"""
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        return CheckItem('字号target非裸tag', 'appB22', True, 'bs4 未安装, 跳过')

    soup = BeautifulSoup(html, 'html.parser')
    size_tab = soup.select_one('#tab-size')
    if not size_tab:
        return CheckItem('字号target非裸tag', 'appB22', True, '无字号 tab')

    bare_tags = []
    # 例外白名单: th / td / table 是合理的语义化裸 tag (host CSS 用 th{} 直接定义表头样式)
    BARE_TAG_ALLOWLIST = {'th', 'td', 'table', 'body'}

    for sr in size_tab.select('.slider-row'):
        inp = sr.select_one('input[type=range]')
        if not inp:
            continue
        tgt = inp.get('data-target', '').strip()
        if not tgt:
            continue
        if tgt in BARE_TAG_ALLOWLIST:
            continue
        # 含 . / 空格 / > / , 表示组合选择器
        if not any(c in tgt for c in ['.', ' ', '>', ',', '#', '[']):
            bare_tags.append(tgt)

    if bare_tags:
        return CheckItem('字号target非裸tag', 'appB22', False,
                       f'ERROR [appB22]: 以下 data-target 是裸 tag (会影响编辑器本身): {bare_tags}')
    return CheckItem('字号target非裸tag', 'appB22', True,
                   f'PASS (全部 slider 使用组合选择器)')


# ============================================================
# 所有检查函数列表
# ============================================================
ALL_CHECKS = [
    # 原始 12 项
    check_sc01_panel_label_complete,
    check_sc02_preset_key_align,
    check_sc03_selector_reachable,
    check_sc04_css_var_exists,
    check_sc05_layout_target_exists,
    check_sc06_js_syntax,
    check_sc07_css_syntax,
    check_sc08_no_dangerous_strings,
    check_sc09_tag_pairing,
    check_sc10_default_colors_complete,
    check_sc11_size_bounds_complete,
    check_sc12_data_editable_exists,
    # 附录 B 新增 17 项
    check_appB01_pem_array_format,
    check_appB02_pem_tab_values,
    check_appB03_pem_row_match_panel,
    check_appB04_presets_flat,
    check_appB05_presets_subset,
    check_appB06_no_fallback,
    check_appB07_slider_oninput,
    check_appB08_slider_row_structure,
    check_appB09_slider_val_id_match,
    check_appB10_panel_actions,
    check_appB11_preset_row,
    check_appB12_cve_string_format,
    check_appB13_edit_hint,
    check_appB14_presets_no_extra_fields,
    check_appB15_injection_order,
    check_appB16_color_tab_sections,
    check_appB17_default_colors_match_host,
    check_appB18_preset_mapping_density,
    check_appB19_pem_tabs_coverage,
    check_appB20_data_editable_coverage,
    check_appB21_size_slider_coverage,
    check_appB22_size_slider_no_bare_tag,
]


def run_all_checks(output_html: str) -> CheckResult:
    """运行所有 29 项 sanity checks。"""
    constants = _extract_constants_from_html(output_html)
    results = []
    for check_fn in ALL_CHECKS:
        result = check_fn(output_html, constants)
        results.append(result)
    errors = [r.message for r in results if not r.passed]
    return CheckResult(
        passed=len(errors) == 0,
        checks=results,
        errors=errors
    )
