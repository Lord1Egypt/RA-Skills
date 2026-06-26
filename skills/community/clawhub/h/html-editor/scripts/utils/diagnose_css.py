#!/usr/bin/env python3
"""
diagnose_css.py — 诊断 HTML 文件的 CSS 来源，判断 html-visual-editor 能否直接应用

用法：
    python3 diagnose_css.py <input.html>

输出 JSON：
{
    "verdict": "ready" | "need-files" | "need-fetch" | "unsupported",
    "summary": "一句话总结",
    "inline_style_chars": 12345,       # <style>...</style> 总字符数
    "local_css_files": [...],          # 同目录或相对路径的 .css 文件
    "missing_local_css": [...],        # 相对路径但文件不在本地
    "remote_css": [...],               # http(s) 或 // 开头的外部链接
    "has_inline_style_attr": true,     # 有多少 style="..." 行内样式
    "inline_style_attr_count": 8,
    "css_vars_defined": 12,            # :root 里定义的 CSS 变量数（驱动能力）
    "actions": ["给出的具体下一步建议"]
}

退出码：
    0 = ready（可直接使用 skill）
    1 = need-files（需要用户补齐文件）
    2 = need-fetch（需要远程拉取）
    3 = unsupported（不适合可视化编辑）
"""
import sys
import re
import json
from pathlib import Path
from urllib.parse import urlparse


def diagnose(html_path: Path) -> dict:
    content = html_path.read_text(encoding='utf-8', errors='replace')
    result = {
        'file': str(html_path),
        'inline_style_chars': 0,
        'local_css_files': [],
        'missing_local_css': [],
        'remote_css': [],
        'has_inline_style_attr': False,
        'inline_style_attr_count': 0,
        'css_vars_defined': 0,
        'actions': [],
    }

    # 1. Inline <style>
    style_blocks = re.findall(r'<style[^>]*>(.*?)</style>', content, re.DOTALL | re.IGNORECASE)
    inline_css = '\n'.join(style_blocks)
    result['inline_style_chars'] = len(inline_css)

    # 2. <link rel="stylesheet" href="...">
    link_re = re.compile(
        r'<link[^>]+rel=["\']?stylesheet["\']?[^>]*>|<link[^>]+href=[^>]*\.css[^>]*>',
        re.IGNORECASE
    )
    href_re = re.compile(r'href=["\']([^"\']+)["\']', re.IGNORECASE)
    for tag in link_re.findall(content):
        m = href_re.search(tag)
        if not m:
            continue
        href = m.group(1)
        parsed = urlparse(href)

        if parsed.scheme in ('http', 'https') or href.startswith('//'):
            result['remote_css'].append(href)
        elif href.startswith('/'):
            # Absolute path — only works in a server context
            result['missing_local_css'].append({
                'href': href,
                'reason': 'absolute path (server-rooted) — local file opens cannot resolve this'
            })
        else:
            # Relative path
            candidate = (html_path.parent / href).resolve()
            if candidate.exists():
                result['local_css_files'].append(str(candidate))
            else:
                result['missing_local_css'].append({
                    'href': href,
                    'expected_path': str(candidate),
                    'reason': 'relative path but file not found'
                })

    # 3. Inline style="..." attributes
    inline_attrs = re.findall(r'\sstyle\s*=\s*["\'][^"\']*["\']', content)
    result['inline_style_attr_count'] = len(inline_attrs)
    result['has_inline_style_attr'] = len(inline_attrs) > 0

    # 4. CSS custom properties defined in :root (driver potential)
    full_css = inline_css
    for fp in result['local_css_files']:
        try:
            full_css += '\n' + Path(fp).read_text(encoding='utf-8', errors='replace')
        except Exception:
            pass
    css_vars = re.findall(r'--[\w-]+\s*:', full_css)
    result['css_vars_defined'] = len(set(css_vars))

    # 5. Verdict
    actions = []
    if result['missing_local_css']:
        result['verdict'] = 'need-files'
        missing_list = ', '.join(m['href'] for m in result['missing_local_css'])
        result['summary'] = f'需要额外的 CSS 文件：{missing_list}'
        actions.append(
            f'告知用户：此 HTML 引用了 {len(result["missing_local_css"])} 个外部 CSS 文件但在本地找不到。'
            '请让用户把 HTML 同目录下的所有 .css 文件（或整个项目文件夹/zip）一起发来。'
        )
        for m in result['missing_local_css']:
            if m['href'].startswith('/'):
                actions.append(
                    f'  · "{m["href"]}" 是服务器绝对路径——本地文件打开时无效。'
                    '建议用户提供完整的网站目录结构，或在浏览器 DevTools → Sources 保存整页样式。'
                )
    elif result['inline_style_chars'] < 500 and not result['local_css_files'] and result['remote_css']:
        result['verdict'] = 'need-fetch'
        result['summary'] = '页面几乎没有本地样式，主要靠远程 CSS（如 Tailwind CDN）'
        actions.append(
            f'此 HTML 主要依赖 {len(result["remote_css"])} 个远程 CSS（{", ".join(result["remote_css"][:3])}）。'
            '编辑层仍可用，但调色/字号面板只会控制我们注入的 CSS 变量，'
            '原页面的 utility class 样式需要在编辑层里覆盖或改写。'
        )
    elif result['inline_style_attr_count'] > 20 and result['css_vars_defined'] == 0:
        result['verdict'] = 'unsupported'
        result['summary'] = (
            f'大量行内 style="..."（{result["inline_style_attr_count"]} 处）且无 CSS 变量，'
            '难以用"改一个变量驱动全局"的面板方式'
        )
        actions.append(
            '建议先用 edit-existing-file skill 把常用颜色/字号提取成 CSS 变量，'
            '再跑 html-visual-editor。'
        )
    elif result['inline_style_chars'] > 0 or result['local_css_files']:
        result['verdict'] = 'ready'
        pieces = []
        if result['inline_style_chars'] > 0:
            pieces.append(f'{result["inline_style_chars"]} 字符内联样式')
        if result['local_css_files']:
            pieces.append(f'{len(result["local_css_files"])} 个本地 CSS 文件')
        result['summary'] = f'CSS 完整（{" + ".join(pieces)}），可直接应用 html-visual-editor'
        if result['css_vars_defined'] < 5:
            actions.append(
                f'警告：只定义了 {result["css_vars_defined"]} 个 CSS 变量，'
                '面板可调范围有限。建议先把关键颜色/字号抽成 CSS 变量。'
            )
        else:
            actions.append(
                f'已检测到 {result["css_vars_defined"]} 个 CSS 变量，'
                '可生成对应的颜色/字号面板控件。'
            )
    else:
        result['verdict'] = 'unsupported'
        result['summary'] = '未检测到任何样式（内联或外部），不是典型的可编辑 HTML'
        actions.append('此文件可能是模板或部分片段，请确认是否完整。')

    result['actions'] = actions
    return result


VERDICT_EXIT = {'ready': 0, 'need-files': 1, 'need-fetch': 2, 'unsupported': 3}


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(4)
    html_path = Path(sys.argv[1])
    if not html_path.exists():
        print(json.dumps({'error': f'File not found: {html_path}'}, ensure_ascii=False))
        sys.exit(4)

    result = diagnose(html_path)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(VERDICT_EXIT.get(result['verdict'], 4))


if __name__ == '__main__':
    main()
