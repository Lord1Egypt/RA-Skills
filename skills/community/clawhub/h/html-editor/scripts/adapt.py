#!/usr/bin/env python3
"""
adapt.py -- html-visual-editor 自动适配引擎主入口 (v15 public package)
将任意宿主 HTML 转换为可视化编辑版本。

使用方法：
    python adapt.py <input.html> [-o <output.html>] [--verbose] [--diagnose-only] [--fetch] [--force]

依赖：
    pip install beautifulsoup4
"""

import sys
import os
import argparse
import re
from pathlib import Path

# 确保可以导入同目录模块
sys.path.insert(0, str(Path(__file__).parent))

from parse_css import parse_css_from_html, count_css_variables, get_color_vars
from scan_dom import scan_dom
from generate_panel import generate_panel
from inject import inject, INJECT_BEGIN, extract_gradient_hex_to_vars, extract_solid_hex_to_vars
from verify import run_all_checks


def determine_compatibility_level(html_content: str, parse_result) -> str:
    """
    判定 HTML 的兼容性分级（Level A / B / C）
    """
    var_counts = count_css_variables(parse_result)
    total_vars = sum(var_counts.values())
    color_count = var_counts.get('color', 0)

    inline_styles = len(re.findall(r'style="[^"]{10,}"', html_content))
    has_canvas = '<canvas' in html_content.lower()
    has_iframe = '<iframe' in html_content.lower()

    if total_vars == 0 and inline_styles > 20:
        return 'C'
    if has_canvas and total_vars == 0:
        return 'C'
    if has_iframe and total_vars < 3:
        return 'C'

    if total_vars >= 5 and color_count >= 2:
        return 'A'

    tailwind_classes = len(re.findall(r'class="[^"]*(?:text-|bg-|border-)\w+', html_content))
    if tailwind_classes > 5 and total_vars < 5:
        return 'B'

    external_css = re.findall(r'<link[^>]+rel="stylesheet"[^>]+href="([^"]+)"', html_content)
    if external_css and total_vars < 5:
        return 'B'

    if 1 <= total_vars < 5:
        return 'B'

    if total_vars >= 5:
        return 'A'

    return 'C'


def main():
    parser = argparse.ArgumentParser(
        prog='adapt.py',
        description='html-visual-editor v15 自动适配引擎 — 将任意 HTML 转为可视化编辑版本',
        epilog='示例: python adapt.py my-page.html -o my-page-editable.html --verbose'
    )
    parser.add_argument('input', help='输入 HTML 文件路径')
    parser.add_argument('-o', '--output', help='输出文件路径（默认: <input>-editable.html）')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细模式')
    parser.add_argument('--diagnose-only', action='store_true', help='仅诊断不生成输出')
    parser.add_argument('--fetch', action='store_true', help='允许下载远程 CSS 文件')
    parser.add_argument('--force', action='store_true', help='强制覆盖已有编辑器注入')
    parser.add_argument('--skip-checks', action='store_true', help='跳过 sanity checks，强制输出（用于复杂布局）')

    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        print(f"错误: 输入文件不存在: {input_path}")
        sys.exit(1)

    with open(input_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    if INJECT_BEGIN in html_content:
        if not args.force:
            print("检测到已有 html-visual-editor 注入。")
            print("使用 --force 强制覆盖，或手动清理后重试。")
            sys.exit(1)
        else:
            print("检测到旧注入，将自动清理并重新注入...")
            # v16 修复: --force 时立即清理旧注入，确保后续所有步骤在干净 HTML 上运行
            from inject import _strip_old_injection
            html_content = _strip_old_injection(html_content)
            print("  旧注入已清理。")

    # v15 预处理: 把宿主 CSS 渐变里硬编码的 hex 提取为 :root 变量
    # 这样后续 parse_css 能识别它们为颜色变量并加进 DEFAULT_COLORS
    html_content, _gradient_new_vars = extract_gradient_hex_to_vars(html_content)
    if args.verbose and _gradient_new_vars:
        print(f"\n[预处理] 渐变提取: 新增 {len(_gradient_new_vars)} 个 CSS 变量")
        for vn, vv in _gradient_new_vars.items():
            print(f"    {vn}: {vv}")

    # v16 预处理: 把宿主 CSS 里非渐变颜色属性中硬编码的 hex 提取为 :root 变量
    html_content, _solid_new_vars = extract_solid_hex_to_vars(html_content)
    if args.verbose and _solid_new_vars:
        print(f"\n[预处理] 非渐变颜色提取: 新增 {len(_solid_new_vars)} 个 CSS 变量")
        for vn, vv in _solid_new_vars.items():
            print(f"    {vn}: {vv}")

    _all_new_vars = {**_gradient_new_vars, **_solid_new_vars}
    if _all_new_vars and args.verbose:
        print(f"\n[预处理] 共新增 {len(_all_new_vars)} 个 CSS 变量")

    # 步骤 1：解析 CSS
    if args.verbose:
        print("=" * 50)
        print("[1/5] 解析 CSS 变量...")

    parse_result = parse_css_from_html(html_content)

    if args.verbose:
        var_counts = count_css_variables(parse_result)
        print(f"  发现 {len(parse_result.variables)} 个 CSS 变量:")
        for semantic, count in sorted(var_counts.items()):
            print(f"    {semantic}: {count}")
        print(f"  发现 {len(parse_result.rules)} 条 CSS 规则")

    # 步骤 2：判定兼容性等级
    level = determine_compatibility_level(html_content, parse_result)

    if args.verbose:
        print(f"\n[兼容性] Level {level}")

    if level == 'C':
        print("=" * 60)
        print("错误: 该 HTML 不适合自动适配 (Level C)")
        print("原因可能是：")
        print("  - 无 CSS 变量 + 大量行内样式")
        print("  - 纯 Canvas/SVG 渲染")
        print("  - iframe 嵌套结构")
        print("建议：先重构 HTML，将硬编码样式提取为 CSS 变量后重试。")
        print("=" * 60)
        sys.exit(1)

    if level == 'B':
        print("注意: 该 HTML 为 Level B（部分支持），面板功能可能受限。")

    if args.diagnose_only:
        print("\n=== 诊断结果 ===")
        print(f"兼容性等级: Level {level}")
        print(f"CSS 变量总数: {len(parse_result.variables)}")
        color_vars = get_color_vars(parse_result)
        print(f"颜色变量: {len(color_vars)}")
        for v in color_vars:
            print(f"  {v.name}: {v.raw_value} → {v.label_zh}")
        print(f"规则数: {len(parse_result.rules)}")
        sys.exit(0)

    # 步骤 3：扫描 DOM (初始扫描，不带 label_for)
    if args.verbose:
        print(f"\n[2/5] 扫描 DOM 元素...")

    scan_result = scan_dom(html_content, parse_result)

    if args.verbose:
        print(f"  页面结构: {scan_result.page_structure}")
        print(f"  可编辑元素: {len(scan_result.elements)}")
        text_count = sum(1 for e in scan_result.elements if e.is_text)
        container_count = sum(1 for e in scan_result.elements if e.is_container)
        print(f"    文本元素: {text_count}")
        print(f"    容器元素: {container_count}")

    # 步骤 4：生成面板（含 LLM labeling 和 LABEL_FOR 构建）
    if args.verbose:
        print(f"\n[3/5] 生成面板配置（含 LLM labeling）...")

    panel_config = generate_panel(parse_result, scan_result)

    # 步骤 4.5：用 LABEL_FOR 重新扫描 DOM 以填充 page_element_to_panel
    if args.verbose:
        print(f"\n[3.5/5] 用 LABEL_FOR 重建 PAGE_ELEMENT_TO_PANEL...")

    scan_result = scan_dom(html_content, parse_result, label_for=panel_config.label_for)

    # 步骤 4.6 (P0-2 修复): 把布局 / 字号 slider 的 data-target 反向索引到 PEM，
    # 让 PEM 真正包含 '布局' / '字号' tab。
    # v1.7.0: size slider 用收敛后的 display 版本，确保 PEM 中 row 直接是 friendly label
    from generate_panel import (
        _build_constants_js,
        _add_layout_targets_to_pem,
        _add_size_targets_to_pem,
        collapse_pem_rows,
    )
    from bs4 import BeautifulSoup
    _pem_soup = BeautifulSoup(html_content, 'html.parser')
    _add_layout_targets_to_pem(panel_config.layout_sliders, scan_result.page_element_to_panel, _pem_soup)
    _add_size_targets_to_pem(
        panel_config.display_size_sliders or panel_config.size_sliders,
        scan_result.page_element_to_panel,
        _pem_soup,
    )

    # 步骤 4.7 (v1.7.0): 把 PEM 中所有 raw color/size row 改写为面板上显示的 friendly label
    collapse_pem_rows(scan_result.page_element_to_panel, panel_config)

    # 重新用更新后的 scan_result 生成 constants_js
    panel_config.constants_js = _build_constants_js(
        panel_config.color_rows, panel_config.size_sliders,
        panel_config.preset_themes,
        scan_result.page_element_to_panel,
        scan_result.css_var_to_elements,
        color_var_to_rep=panel_config.color_var_to_rep,
        size_target_to_family=panel_config.size_target_to_family,
    )

    if args.verbose:
        print(f"  颜色行: {len(panel_config.color_rows)}")
        print(f"  字号滑块: {len(panel_config.size_sliders)}")
        print(f"  布局滑块: {len(panel_config.layout_sliders)}")
        print(f"  预设主题: {len(panel_config.preset_themes)}")
        print(f"  PAGE_ELEMENT_TO_PANEL: {len(scan_result.page_element_to_panel)} 项")

    # 步骤 5：注入
    if args.verbose:
        print(f"\n[4/5] 注入编辑器组件...")

    if args.output:
        output_path = Path(args.output).resolve()
    else:
        stem = input_path.stem
        output_path = input_path.parent / f"{stem}-editable.html"

    inject_result = inject(html_content, panel_config, scan_result, output_path)

    # 步骤 6：Sanity Checks
    if args.verbose:
        print(f"\n[5/5] 运行 sanity checks...")

    check_result = run_all_checks(inject_result.output_html)

    if not check_result.passed:
        if args.skip_checks:
            print("\n" + "=" * 60)
            print(f"WARNING: {len(check_result.errors)} sanity check(s) FAILED (skipped via --skip-checks):")
            for err in check_result.errors:
                print(f"  {err}")
            print("=" * 60)
            print("输出文件将继续写入（结果可能不完美，请手动检查）。")
        else:
            print("\n" + "=" * 60)
            print(f"ADAPT FAILED: {len(check_result.errors)} sanity check(s) failed:")
            for err in check_result.errors:
                print(f"  {err}")
            print("=" * 60)
            print("Output file NOT written. Fix the issues above and retry.")
            sys.exit(1)

    if args.verbose:
        print(f"  所有 {len(check_result.checks)} 项检查通过 ✓")
        for check in check_result.checks:
            status = "✓" if check.passed else "✗"
            print(f"    [{status}] {check.code} {check.name}")

    # 写入输出文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(inject_result.output_html)

    print(f"\n完成! 输出文件: {output_path}")
    print(f"  兼容性等级: Level {level}")
    print(f"  颜色变量: {len(panel_config.color_rows)}")
    print(f"  字号滑块: {len(panel_config.size_sliders)}")
    print(f"  布局滑块: {len(panel_config.layout_sliders)}")
    print(f"  预设主题: {len(panel_config.preset_themes)}")
    print(f"  data-editable 元素: {inject_result.output_html.count('data-editable')}")


if __name__ == '__main__':
    main()
