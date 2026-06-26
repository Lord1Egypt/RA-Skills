#!/usr/bin/env python3
"""
Markdown -> 微信兼容 HTML 转换器（文章模式）

用法:
  python3 md2article_html.py <input.md> [output.html]
  python3 md2article_html.py --config /path/to/config.yaml <input.md> [output.html]

文章模式：统一的长文叙事渲染，适配微信公众号文章样式。
默认配色为白底灰字 + 棕色标签（AI文章风格），可通过 config.yaml 的 style.article 节点
切换为泛黄报纸风格或自定义配色。
"""

import re
import sys
import os

from pygments import lex
from pygments.lexers import get_lexer_by_name
from pygments.token import Token

# ─── 配置路径 ──────────────────────────────────────────
CONFIG_PATH = os.path.join(os.path.expanduser("~/.md_push_wechat"), "config.yaml")


# ─── 文章模式 HTML 模板 ────────────────────────────────
# 所有需要动态填充的位置使用 __PLACEHOLDER__ 格式，
# 由 _build_article_template() 一次性完成全部替换。

_ARTICLE_RAW_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
/* 代码块浏览器端预览样式（微信平台自有 code-snippet CSS 白名单，此 style 仅用于浏览器预览） */
.code-snippet__fix{position:relative;margin:12px 0 18px;border-radius:6px;overflow:hidden;font-size:13px;line-height:1.6}
.code-snippet__fix .code-snippet__js{font-family:'SF Mono','Fira Code','Consolas','Menlo',monospace}
.code-snippet__line-index{position:absolute;top:0;left:0;width:40px;padding:12px 0;margin:0;list-style:none;text-align:right;background:#2b3137;color:#636d83;font-size:12px;line-height:1.6;border-right:1px solid #3a3f47;box-sizing:border-box}
.code-snippet__line-index li{padding:0 8px 0 0}
pre.code-snippet__js{margin:0;padding:12px 12px 12px 52px;background:#282c34;color:#abb2bf;overflow-x:auto;white-space:pre}
pre.code-snippet__js code{display:block;font-family:inherit}
.code-snippet__keyword{color:#c678dd;font-weight:bold}
.code-snippet__built_in{color:#e5c07b}
.code-snippet__string{color:#98c379}
.code-snippet__number{color:#d19a66}
.code-snippet__comment{color:#5c6370;font-style:italic}
.code-snippet__title{color:#61afef}
.code-snippet__subst{color:#56b6c2}
</style>
</head>
<body style="margin:0;padding:0;font-family:__FONT_FAMILY__;text-indent:0">
<section style="background:__BG__;padding:20px 16px">

<!-- 封面 -->
<section style="background:__HERO_BG__;padding:28px 20px 22px;margin:0 0 24px 0;border-top:4px solid __RULE__">
  <p style="margin:0 0 8px 0;font-size:11px;color:__RULE__;letter-spacing:3px;text-align:center;opacity:0.8">__COVER_LABEL__</p>
  <h1 style="margin:0 0 10px 0;font-size:__TITLE_FONT_SIZE__;font-weight:bold;color:__HERO_TITLE_COLOR__;line-height:1.4;text-align:center;border:none">__TITLE__</h1>
</section>

<!-- 正文区域 -->
<section style="font-size:__TEXT_FONT_SIZE__;line-height:2em;letter-spacing:1px;padding:0 4px 20px 4px;color:__TEXT_COLOR__;background:__CONTENT_BG__">
__CONTENT__
</section>

__FOOTER_SECTION__

__ENDING_SECTION__

</section>
</body>
</html>"""


def _build_article_html(s, title, content, footer_section="", ending_section=""):
    """用样式配置和内容数据一次性构建文章 HTML"""
    t = _ARTICLE_RAW_TEMPLATE
    hero_title_color = s.get("hero_title_color", "#faf7f0")
    text_color = s.get("text", s.get("dark", "rgb(85,85,85)"))
    rule = s.get("rule", "#c4a882")
    hero_style = s.get("hero_style", "default")

    # 如果 markdown 没有 # 一级标题，去掉空白封面区
    if not title:
        t = re.sub(
            r'<!-- 封面 -->.*?</section>\s*\n',
            '', t, flags=re.DOTALL
        )
    # minimal 模式：替换默认封面区为极简标题（无顶条、无 label，左对齐黑色大标题）
    elif hero_style == "minimal":
        title_size = s["title_font_size"]
        minimal_hero = (
            f'<!-- 封面 -->\n'
            f'<section style="margin:0 0 20px 0;padding:6px 0 14px 0">\n'
            f'  <h1 style="margin:0;font-size:{title_size};font-weight:bold;color:{hero_title_color};'
            f'line-height:1.4;text-align:left;border:none">{title}</h1>\n'
            f'</section>'
        )
        t = re.sub(
            r'<!-- 封面 -->.*?</section>',
            lambda m: minimal_hero,
            t, count=1, flags=re.DOTALL
        )

    for name, val in [
        ("BG", s["bg"]),
        ("FONT_FAMILY", s.get("font_family", "-apple-system,'PingFang SC','Microsoft YaHei',sans-serif")),
        ("HERO_BG", s.get("hero_bg", s["accent"])),
        ("RULE", rule),
        ("COVER_LABEL", s.get("cover_label", "AI 实践观察")),
        ("TITLE_FONT_SIZE", s["title_font_size"]),
        ("HERO_TITLE_COLOR", hero_title_color),
        ("TEXT_FONT_SIZE", s["text_font_size"]),
        ("TEXT_COLOR", text_color),
        ("CONTENT_BG", s.get("content_bg", "transparent")),
        ("TITLE", title),
        ("CONTENT", content),
        ("FOOTER_SECTION", footer_section),
        ("ENDING_SECTION", ending_section),
    ]:
        t = t.replace(f"__{name}__", val)
    return t


# ─── Markdown 解析 ─────────────────────────────────────

def parse_article(md_text):
    """
    解析文章 Markdown，支持：
    - # H1 标题
    - > ... 引用块
    - ## H2 章节标题
    - ### H3 子标题
    - --- 分隔线
    - 普通段落
    - **粗体**
    - 表格
    - 代码块
    - 有序列表 (1. 2. 3. ...)，支持嵌套
    - 无序列表 (- 或 * 或 +)，支持嵌套
    - 任务列表 (- [ ] / - [x])
    返回 {"title": str, "blocks": [...]}
    """
    lines = md_text.strip().split('\n')
    title = ""
    blocks = []
    para_buf = []
    in_code_block = False
    code_lines = []
    table_lines = []
    in_table = False
    bq_buf = []
    in_blockquote = False

    # ── 列表嵌套追踪 ──
    # list_stack: [{ "type": "ol"|"ul"|"task", "indent": int, "items": [...] }]
    list_stack = []

    def _line_indent(raw_line):
        """返回行首空格数（缩进层级）"""
        return len(raw_line) - len(raw_line.lstrip(' '))

    def _close_sibling_lists(indent):
        """关闭同缩进或更深的旧列表，确保不同类型列表为兄弟节点"""
        while list_stack and list_stack[-1]["indent"] >= indent:
            child = list_stack.pop()
            if list_stack:
                parent_items = list_stack[-1]["items"]
                if parent_items:
                    if parent_items[-1].get("children") is None:
                        parent_items[-1]["children"] = []
                    parent_items[-1]["children"].append(child)
            else:
                blocks.append(child)

    def _flush_lists_to_indent(target_indent):
        """将缩进大于 target_indent 的列表出栈，嵌套为父列表末项的 children"""
        while list_stack and list_stack[-1]["indent"] > target_indent:
            child = list_stack.pop()
            if list_stack:
                parent_items = list_stack[-1]["items"]
                if parent_items:
                    if parent_items[-1].get("children") is None:
                        parent_items[-1]["children"] = []
                    parent_items[-1]["children"].append(child)
            else:
                blocks.append(child)

    def _flush_all_lists():
        """将所有未关闭的列表逐级出栈并嵌套"""
        while list_stack:
            child = list_stack.pop()
            if list_stack:
                parent_items = list_stack[-1]["items"]
                if parent_items:
                    if parent_items[-1].get("children") is None:
                        parent_items[-1]["children"] = []
                    parent_items[-1]["children"].append(child)
            else:
                blocks.append(child)

    def flush_para():
        if para_buf:
            text = ' '.join(para_buf).strip()
            if text:
                blocks.append({"type": "para", "text": text})
            para_buf.clear()

    def flush_table():
        if table_lines:
            blocks.append({"type": "table", "rows": table_lines.copy()})
            table_lines.clear()

    def flush_bq():
        if bq_buf:
            text = '\n'.join(bq_buf).strip()
            if text:
                blocks.append({"type": "blockquote", "text": text})
            bq_buf.clear()

    for line in lines:
        raw = line.rstrip()
        stripped = raw.strip()

        # 代码块
        if stripped.startswith('```'):
            if in_code_block:
                blocks.append({"type": "code_block", "text": '\n'.join(code_lines),
                               "lang": code_lang})
                code_lines.clear()
            else:
                _flush_all_lists()
                flush_para()
                flush_table()
                # 提取语言标识，如 ```python → "python"
                code_lang = stripped[3:].strip().lower() or None
            in_code_block = not in_code_block
            continue

        if in_code_block:
            code_lines.append(raw)
            continue

        # H1 标题
        if stripped.startswith('# ') and not stripped.startswith('## '):
            _flush_all_lists()
            flush_para()
            flush_table()
            if not title:
                title = stripped[2:].strip()
            continue

        # 引用块
        if stripped.startswith('> '):
            _flush_all_lists()
            flush_para()
            flush_table()
            if not in_blockquote:
                flush_bq()
                in_blockquote = True
            bq_buf.append(stripped[2:].strip())
            continue

        if in_blockquote:
            flush_bq()
            in_blockquote = False

        # 图片（独立行）
        img_match = re.match(r'^!\[([^\]]*)\]\(([^)\n]+)\)$', stripped)
        if img_match:
            _flush_all_lists()
            flush_para()
            flush_table()
            blocks.append({"type": "image", "alt": img_match.group(1).strip(), "src": img_match.group(2).strip()})
            continue

        # H2 章节标题
        if stripped.startswith('## '):
            _flush_all_lists()
            flush_para()
            flush_table()
            blocks.append({"type": "heading", "text": stripped[3:].strip(), "level": 2})
            continue

        # H4 小标题（必须在 H3 之前，否则 #### 会误匹配 ### ）
        if stripped.startswith('#### '):
            _flush_all_lists()
            flush_para()
            flush_table()
            blocks.append({"type": "heading", "text": stripped[5:].strip(), "level": 4})
            continue

        # H3 子标题
        if stripped.startswith('### '):
            _flush_all_lists()
            flush_para()
            flush_table()
            blocks.append({"type": "heading", "text": stripped[4:].strip(), "level": 3})
            continue

        # 分隔线
        if stripped in ('---', '***', '* * *'):
            _flush_all_lists()
            flush_para()
            flush_table()
            continue

        # 表格行
        if stripped.startswith('|'):
            _flush_all_lists()
            def is_separator_row(cells):
                for c in cells:
                    s = c.strip()
                    if s and not all(ch in '-: ' for ch in s):
                        return False
                return True
            cells = stripped.split('|')[1:-1]
            if is_separator_row(cells):
                continue
            flush_para()
            if in_table:
                table_lines.append(stripped)
            else:
                in_table = True
                table_lines.append(stripped)
            continue
        elif in_table:
            flush_table()
            in_table = False

        # ── 列表解析（支持嵌套 + 任务列表）──
        indent = _line_indent(raw)

        # 任务列表: - [ ] 或 - [x] 或 * [ ] 或 + [ ]
        task_match = re.match(r'^[\-\*\+]\s+\[([ xX])\]\s+(.+)$', stripped)
        if task_match:
            flush_para()
            flush_table()
            checked = task_match.group(1).lower() == 'x'
            item_text = task_match.group(2)

            _flush_lists_to_indent(indent)

            item_data = {"text": item_text, "checked": checked, "children": None}
            if list_stack and list_stack[-1]["indent"] == indent and list_stack[-1]["type"] == "task":
                list_stack[-1]["items"].append(item_data)
            else:
                _close_sibling_lists(indent)
                list_stack.append({"type": "task", "indent": indent, "items": [item_data]})
            continue

        # 有序列表: 1. / 99. ...
        ol_match = re.match(r'^(\d+)\.\s+(.+)$', stripped)
        if ol_match:
            flush_para()
            flush_table()
            marker_value = int(ol_match.group(1))
            item_text = ol_match.group(2)

            _flush_lists_to_indent(indent)

            item_data = {"text": item_text, "value": marker_value, "children": None}
            if list_stack and list_stack[-1]["indent"] == indent and list_stack[-1]["type"] == "ol":
                list_stack[-1]["items"].append(item_data)
            else:
                _close_sibling_lists(indent)
                list_stack.append({"type": "ol", "indent": indent, "items": [item_data]})
            continue

        # 无序列表: - / * / +
        ul_match = re.match(r'^[\-\*\+]\s+(.+)$', stripped)
        if ul_match:
            flush_para()
            flush_table()
            item_text = ul_match.group(1)

            _flush_lists_to_indent(indent)

            item_data = {"text": item_text, "children": None}
            if list_stack and list_stack[-1]["indent"] == indent and list_stack[-1]["type"] == "ul":
                list_stack[-1]["items"].append(item_data)
            else:
                _close_sibling_lists(indent)
                list_stack.append({"type": "ul", "indent": indent, "items": [item_data]})
            continue

        # 空行 — 不关闭列表（允许列表项间有空行），只 flush 段落缓冲
        if not stripped:
            flush_para()
            continue

        # 非列表内容：关闭所有未完成的列表
        _flush_all_lists()

        # 普通段落
        para_buf.append(stripped)

    flush_para()
    flush_bq()
    _flush_all_lists()
    if in_table:
        flush_table()
    return {"title": title, "blocks": blocks}


# ─── HTML 生成 ─────────────────────────────────────────

def escape_html(text):
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    return text


def format_text(text, s):
    """文章文本格式化：粗体、链接、行内代码、图片"""
    text = escape_html(text)

    # 行内代码
    accent = s["accent"]
    def replace_code(m):
        return f'<code style="font-size:13px;background:#f5f5f5;color:{accent};padding:2px 6px">{m.group(1)}</code>'
    text = re.sub(r'`([^`]+)`', replace_code, text)

    # 内联图片（必须在链接之前处理，避免 ![...](url) 被链接正则误匹配）
    # 同时在回调中检查匹配位置是否在 <code> 标签内，避免误转换行内代码中的 ![]()
    def replace_img(m):
        # 检查是否在 <code> 标签内
        prefix = text[:m.start()]
        last_code_open = prefix.rfind('<code')
        last_code_close = prefix.rfind('</code>')
        if last_code_open > last_code_close:
            return m.group(0)  # 在 <code> 内，保持原样
        alt = m.group(1)
        src = m.group(2)
        return f'<img src="{src}" alt="{escape_html(alt)}" style="max-width:100%;height:auto;vertical-align:middle">'
    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_img, text)

    # 链接
    def replace_link(m):
        return f'<a href="{m.group(2)}" style="color:{accent};text-decoration:none">{m.group(1)}</a>'
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', replace_link, text)

    # 粗体
    bold_color = s.get("bold", "#333")
    def replace_bold(m):
        return f'<b style="font-weight:bold;color:{bold_color}">{m.group(1)}</b>'
    text = re.sub(r'\*\*([^*]+)\*\*', replace_bold, text)

    return text


def _split_table_row(row):
    """拆分表格行，保护行内代码（`...`）中的管道符不被误拆"""
    # 记录所有反引号对的位置
    code_spans = []
    i = 0
    while i < len(row):
        if row[i] == '`':
            j = row.find('`', i + 1)
            if j != -1:
                code_spans.append((i, j))
                i = j + 1
                continue
        i += 1

    # 检查每个 | 是否在反引号对内
    def _is_in_code(pos):
        for a, b in code_spans:
            if a < pos < b:
                return True
        return False

    # 用占位符替换反引号内的管道符
    PLACEHOLDER = '\x00PIPE\x00'
    chars = list(row)
    for pos in range(len(chars)):
        if chars[pos] == '|' and _is_in_code(pos):
            chars[pos] = PLACEHOLDER

    # 拆分后还原管道符
    return [c.strip().replace(PLACEHOLDER, '|')
            for c in ''.join(chars).split('|')[1:-1]]


def render_table(rows, s):
    """渲染表格为微信兼容 HTML"""
    if not rows:
        return ""

    headers = _split_table_row(rows[0])
    data_rows = []
    for row in rows[1:]:
        cells = _split_table_row(row)
        if cells:
            data_rows.append(cells)

    bold_color = s.get("bold", "#333")
    base = 'padding:10px 12px;border:1px solid #ddd'
    html = '<table style="width:100%;border-collapse:collapse;margin:16px 0;font-size:14px">\n'

    html += '  <thead>\n'
    html += '    <tr>\n'
    for h in headers:
        html += f'      <th style="{base};background:#f8f8f8;font-weight:bold;color:{bold_color};font-size:13px">{format_text(h, s)}</th>\n'
    html += '    </tr>\n'
    html += '  </thead>\n'

    html += '  <tbody style="padding:10px 12px">\n'
    for i, row in enumerate(data_rows):
        bg = '#fff' if i % 2 == 0 else '#fafafa'
        html += '    <tr>\n'
        for cell in row:
            html += f'      <td style="{base};background:{bg}">{format_text(cell, s)}</td>\n'
        html += '    </tr>\n'
    html += '  </tbody>\n'
    html += '</table>\n'

    return html


def render_blockquote(text, s):
    """渲染引用块 —— 每行用独立 <p> 分段，避免 <br> 被转义"""
    lines = text.split('\n')
    parts = []
    for line in lines:
        escaped = escape_html(line)
        formatted = format_text(escaped, s)
        parts.append(
            f'<p style="margin:0 0 8px 0;font-size:14px;font-style:italic;color:#888;line-height:1.9">{formatted}</p>'
        )
    # 去掉最后一行多余的底部 margin
    parts[-1] = parts[-1].replace('margin:0 0 8px 0', 'margin:0')
    html = (
        f'<section style="margin:16px 0;padding:14px 16px;background:#f8f8f8;'
        f'border-left:4px solid {s["accent"]}">'
        f'{"".join(parts)}'
        f'</section>'
    )
    return html
    html = (
        f'<section style="margin:16px 0;padding:14px 16px;background:#f8f8f8'
        f';border-left:4px solid {s["accent"]}">'
        f'<p style="margin:0;font-size:14px;font-style:italic;color:#888;line-height:1.9">{formatted}</p>'
        f'</section>'
    )
    return html


def _token_to_css_class(ttype):
    """将 Pygments token 类型映射到微信 code-snippet CSS class。"""
    # 注释
    if ttype in Token.Comment:
        return "code-snippet__comment"
    # 关键字
    if ttype in Token.Keyword:
        return "code-snippet__keyword"
    # 函数名、类名
    if ttype in Token.Name.Function or ttype in Token.Name.Class:
        return "code-snippet__title"
    # 字符串
    if ttype in Token.String:
        return "code-snippet__string"
    # f-string 插值 {var}
    if ttype in Token.String.Interpol:
        return "code-snippet__subst"
    # 数字
    if ttype in Token.Number:
        return "code-snippet__number"
    # 内置函数/类型
    if ttype in Token.Name.Builtin:
        return "code-snippet__built_in"
    # 普通文本、标点、空白等 — 不高亮
    return None


def highlight_code(code, lang=None):
    """用 Pygments 对代码做词法分析，返回按行分组的 token 列表。

    每行: [(text_str, css_class_or_None), ...]
    """
    if not code:
        return []

    # 获取 lexer：有指定语言则直接用，否则回退为纯文本（不猜测，避免误判）
    try:
        if lang:
            lexer = get_lexer_by_name(lang, stripall=True)
        else:
            lexer = get_lexer_by_name("text", stripall=True)
    except Exception:
        lexer = get_lexer_by_name("text", stripall=True)

    lines = []
    current_line = []

    for ttype, value in lex(code, lexer):
        css_class = _token_to_css_class(ttype)
        # 按换行切分 token
        parts = value.split('\n')
        for i, part in enumerate(parts):
            if i > 0:
                # 换行 — 结束当前行
                lines.append(current_line)
                current_line = []
            if part:
                current_line.append((part, css_class))

    if current_line:
        lines.append(current_line)

    return lines


def render_code_block(code, lang=None):
    """渲染微信 code-snippet 代码块（语法高亮 + 行号）。

    使用微信内置 code-snippet 组件：section > ul(行号) + pre > code×N(每行)。
    CSS 由微信平台 code-snippet class 白名单提供，无需 inline style。
    """
    if not code:
        return ""

    lines_tokens = highlight_code(code, lang)

    # 行号列表
    line_nums_html = ''.join('<li></li>' for _ in lines_tokens)

    # 逐行渲染
    code_lines_html = []
    for line_tokens in lines_tokens:
        if not line_tokens:
            # 空行 — 零宽占位符
            code_lines_html.append('<code><span leaf="">&#8203;</span></code>')
        else:
            parts = []
            for text, css_class in line_tokens:
                escaped = escape_html(text)
                if css_class:
                    parts.append(f'<span class="{css_class}">{escaped}</span>')
                else:
                    parts.append(escaped)
            line_html = ''.join(parts)
            code_lines_html.append(f'<code><span leaf="">{line_html}</span></code>')

    lang_attr = f' data-lang="{escape_html(lang)}"' if lang else ''

    return (
        f'<section class="code-snippet__fix code-snippet__js">\n'
        f'<ul class="code-snippet__line-index code-snippet__js">{line_nums_html}</ul>\n'
        f'<pre class="code-snippet__js"{lang_attr}>\n'
        + '\n'.join(code_lines_html) +
        f'\n</pre>\n</section>'
    )


def render_ending(s):
    """生成文章尾栏（如 AI 文章的三连/版权声明等）"""
    lines = s.get("ending_lines", None)
    if not lines:
        return ""

    base_style = 'font-size:12px;color:#888;letter-spacing:0.5px;line-height:1.9'
    lines_html = ''.join(
        f'<p style="margin:0 0 10px 0">{line}</p>'
        for line in lines
    )
    return (
        f'<section style="text-align:center;padding:24px 0 0 0;border-top:1px solid #eee;margin:20px 0 0 0;{base_style}">'
        f'{lines_html}'
        f'</section>'
    )


def render_footer(s):
    """生成页脚（如历史文章模式的底部署名）"""
    footer_text = s.get("footer", "")
    if not footer_text:
        return ""

    rule = s.get("rule", "#c4a882")
    caption = s.get("caption", "#a89880")
    return (
        f'<section style="border-top:2px solid {rule};margin:16px 0 0 0;padding:10px 0 0 0;text-align:center">'
        f'<p style="margin:0;font-size:11px;color:{caption};letter-spacing:1px">{escape_html(footer_text)}</p>'
        f'</section>'
    )


def _render_list_block(block, s):
    """递归渲染列表块（ol/ul/task），支持任意层级嵌套"""
    list_type = block["type"]
    list_attrs = ""

    if list_type == "ol":
        tag = "ol"
        list_style = 'margin:0 0 14px 0;padding-left:24px'
        first_value = block["items"][0].get("value") if block.get("items") else None
        if isinstance(first_value, int) and first_value > 0:
            list_attrs = f' start="{first_value}"'
    elif list_type == "task":
        tag = "ul"
        list_style = 'margin:0 0 14px 0;padding-left:24px;list-style:none'
    else:
        tag = "ul"
        list_style = 'margin:0 0 14px 0;padding-left:24px'

    items_html = []
    for item in block["items"]:
        item_text = item["text"]
        formatted = format_text(escape_html(item_text), s)

        # 任务列表渲染
        if list_type == "task":
            checked = item.get("checked", False)
            checkbox = "☑" if checked else "☐"
            color = "#999" if checked else "#333"
            li_content = f'<span style="color:{color};margin-right:6px;font-size:14px">{checkbox}</span>{formatted}'
        else:
            li_content = formatted

        # 嵌套子列表
        children_html = ""
        children = item.get("children")
        if children:
            if isinstance(children, list):
                for child_block in children:
                    children_html += _render_list_block(child_block, s)
            elif isinstance(children, dict):
                children_html = _render_list_block(children, s)

        li_attrs = ""
        if list_type == "ol":
            marker_value = item.get("value")
            if isinstance(marker_value, int) and marker_value > 0:
                li_attrs = f' value="{marker_value}"'

        if children_html:
            items_html.append(
                f'<li{li_attrs} style="margin:0 0 6px 0;line-height:1.9">{li_content}{children_html}</li>'
            )
        else:
            items_html.append(
                f'<li{li_attrs} style="margin:0 0 6px 0;line-height:1.9">{li_content}</li>'
            )

    # 去除 \\n：微信编辑器会把 HTML 元素间的换行解释为新列表项，产生多余带点空行
    return f'<{tag}{list_attrs} style="{list_style}">' + ''.join(items_html) + f'</{tag}>'


def _h2_index_text(index):
    return f"{index:02d}"


def render_h2(text, s, index):
    """渲染 H2（支持多种样式）"""
    style = s.get("h2_style", "pill")
    accent = s.get("accent", "#333")
    h2_size = s.get("h2_font_size", "18px")
    rule = s.get("rule", "#ddd")
    bold_color = s.get("bold", "#333")
    badge_bg = s.get("h2_badge_bg", "#f7b731")
    badge_text = s.get("h2_badge_text", "#ffffff")
    index_bg = s.get("h2_index_bg", accent)
    index_text = s.get("h2_index_text", "#ffffff")
    label = format_text(escape_html(text), s)

    if style == "framed_pill":
        # 紫绿学术风 H2：浅色底 + 主色文字 + 主色左粗边 + 圆角胶囊框
        frame_bg = s.get("h2_frame_bg", "#f8f0fb")
        frame_border = s.get("h2_frame_border", accent)
        frame_border_width = s.get("h2_frame_border_width", "5px")
        frame_radius = s.get("h2_frame_radius", "4px")
        return (
            f'<h2 style="margin:24px 0 14px 0;padding:12px 14px;font-size:{h2_size};font-weight:bold;'
            f'color:{accent};background:{frame_bg};border-left:{frame_border_width} solid {frame_border};'
            f'border-radius:{frame_radius};line-height:1.6;display:block">'
            f'{label}</h2>'
        )

    if style == "quote_line":
        return (
            f'<section style="margin:30px 0 20px 0;text-align:center">'
            f'<p style="margin:0 0 8px 0;font-size:56px;color:{accent};opacity:0.12;line-height:0.8;font-weight:bold">Q</p>'
            f'<h2 style="margin:0;font-size:{h2_size};font-weight:bold;color:{accent};line-height:1.6;display:block;background:none;padding:0">'
            f'“{label}”</h2>'
            f'<p style="margin:10px auto 0 auto;width:62%;max-width:420px;border-top:3px solid {accent};height:0"></p>'
            f'</section>'
        )

    if style == "badge_block":
        return (
            f'<section style="margin:30px 0 18px 0">'
            f'<p style="margin:0;line-height:1;text-align:left">'
            f'<span style="display:inline-block;vertical-align:top;background:{badge_bg};color:{badge_text};padding:10px 14px;border-radius:0 0 18px 18px;'
            f'font-size:24px;font-weight:bold;letter-spacing:1px">{_h2_index_text(index)}</span>'
            f'<span style="display:inline-block;vertical-align:top;margin-left:8px;background:{accent};color:#fff;padding:12px 16px;'
            f'font-size:{h2_size};font-weight:bold;line-height:1.4">{label}</span>'
            f'</p>'
            f'<p style="margin:12px 0 0 0;border-top:3px solid {accent};height:0"></p>'
            f'</section>'
        )

    if style == "center_card":
        return (
            f'<section style="margin:34px 0 24px 0;text-align:center">'
            f'<p style="margin:0;line-height:1">'
            f'<span style="display:inline-block;vertical-align:middle;width:34%;border-top:2px solid {rule};height:0"></span>'
            f'<span style="display:inline-block;vertical-align:middle;margin:0 10px;background:{index_bg};color:{index_text};padding:9px 14px;'
            f'font-size:24px;font-weight:bold;line-height:1;min-width:48px">{_h2_index_text(index)}</span>'
            f'<span style="display:inline-block;vertical-align:middle;width:34%;border-top:2px solid {rule};height:0"></span>'
            f'</p>'
            f'<h2 style="margin:16px 0 0 0;font-size:{h2_size};font-weight:bold;color:{bold_color};line-height:1.5;display:block;background:none;padding:0">'
            f'{label}</h2>'
            f'</section>'
        )

    # 默认胶囊样式（保持历史兼容）
    return (
        f'<h2 style="margin:28px auto 18px;padding:8px 24px;font-size:{h2_size};font-weight:bold;color:#fff;'
        f'background:{accent};text-align:center;display:block;'
        f'width:fit-content;line-height:1.6;box-shadow:0 2px 6px rgba(0,0,0,0.12)">'
        f'{label}</h2>'
    )


def generate_html(data, s):
    """生成微信兼容 HTML（文章模式）"""
    content_parts = []
    h2_index = 0

    for block in data["blocks"]:
        btype = block["type"]
        text = block.get("text", "")

        if btype == "heading" and block["level"] == 2:
            h2_index += 1
            content_parts.append(render_h2(text, s, h2_index))
        elif btype == "heading" and block["level"] == 3:
            h3_color = s.get("h3_color", "#333")
            content_parts.append(
                f'<p style="margin:22px 0 12px 0;font-size:16px;font-weight:bold;color:{h3_color};line-height:1.5">'
                f'{format_text(escape_html(text), s)}</p>'
            )
        elif btype == "heading" and block["level"] == 4:
            h4_color = s.get("h4_color", "#555")
            content_parts.append(
                f'<p style="margin:18px 0 10px 0;font-size:15px;font-weight:bold;color:{h4_color};line-height:1.5">'
                f'{format_text(escape_html(text), s)}</p>'
            )
        elif btype == "blockquote":
            content_parts.append(render_blockquote(text, s))
        elif btype == "code_block":
            content_parts.append(render_code_block(text, block.get("lang")))
        elif btype == "table":
            content_parts.append(render_table(block["rows"], s))
        elif btype == "image":
            alt_text = escape_html(block.get("alt", ""))
            img_src = block.get("src", "")
            content_parts.append(
                f'<p style="margin:16px auto;text-align:center">'
                f'<img src="{img_src}" alt="{alt_text}" style="max-width:100%;height:auto;display:block;margin:0 auto">'
                f'</p>'
            )
        elif btype == "para":
            formatted = format_text(escape_html(text), s)
            p_indent = s.get("p_indent", "0")
            indent_css = f';text-indent:{p_indent}' if p_indent and p_indent != "0" else ''
            content_parts.append(
                f'<p style="margin:0 0 14px 0{indent_css}">{formatted}</p>'
            )
        elif btype in ("ol", "ul", "task"):
            content_parts.append(_render_list_block(block, s))

    content = '\n'.join(content_parts)

    footer_section = render_footer(s)
    ending_section = render_ending(s)

    return _build_article_html(s, escape_html(data["title"]), content, footer_section, ending_section)


# ─── 样式配置加载 ─────────────────────────────────────

# 默认配置（白底灰字 + 棕色标签标题）
ARTICLE_DEFAULTS = {
    "bg": "#ffffff",
    "content_bg": "transparent",
    "font_family": "-apple-system,'PingFang SC','Microsoft YaHei',sans-serif",
    "text": "rgb(85,85,85)",
    "accent": "rgb(198,110,73)",
    "hero_bg": "rgb(198,110,73)",
    "hero_title_color": "#ffffff",
    "bold": "rgb(51,51,51)",
    "rule": "#ddd",
    "caption": "#888",
    "title_font_size": "22px",
    "text_font_size": "16px",
    "h2_font_size": "18px",
    "h2_style": "pill",
    "h2_badge_bg": "#f7b731",
    "h2_badge_text": "#ffffff",
    "h2_index_bg": "rgb(198,110,73)",
    "h2_index_text": "#ffffff",
    "h3_color": "#333",
    "h4_color": "#555",
    "h2_frame_bg": "#f8f0fb",
    "h2_frame_border": "rgb(198,110,73)",
    "h2_frame_border_width": "5px",
    "h2_frame_radius": "4px",
    "p_indent": "0",
    "hero_style": "default",
    "cover_label": "AI 实践观察",
    "footer": "",
    "ending_lines": [
        "—End—",
        "如果觉得不错 随手点个 <span style=\"color:#ff4c41\">赞</span>、<span style=\"color:#ff2941\">在看</span>、<span style=\"color:#ff4c41\">转发</span> 三连吧",
        "<span style=\"color:#ff2941\">关注+星标</span> 可第一时间收到更多精彩思考和总结",
        "您的支持是我继续写下去的动力",
        "注：原创不易，合作请在公众号后台留言，未经许可，不得随意修改及盗用原文。",
    ],
}

# 预置主题
ARTICLE_THEMES = {
    "nostalgic": {
        "bg": "#f6f1e7",
        "content_bg": "#f6f1e7",
        "text": "rgb(85,85,85)",
        "accent": "#3c2415",
        "hero_bg": "#3c2415",
        "hero_title_color": "#faf7f0",
        "bold": "rgb(51,51,51)",
        "rule": "#c4a882",
        "caption": "#a89880",
        "title_font_size": "24px",
        "text_font_size": "16px",
        "h2_font_size": "18px",
        "cover_label": "成语典故 · 历史人物",
        "footer": "成语典故 · 历史人物",
        "ending_lines": [],
    },
    "modern": {
        "bg": "#ffffff",
        "content_bg": "transparent",
        "text": "#2d2d2d",
        "accent": "#2563eb",
        "hero_bg": "#1e293b",
        "hero_title_color": "#f8fafc",
        "bold": "#111827",
        "rule": "#e5e7eb",
        "caption": "#9ca3af",
        "title_font_size": "24px",
        "text_font_size": "16px",
        "h2_font_size": "18px",
        "h2_style": "pill",
        "cover_label": "技术探索",
        "footer": "",
        "ending_lines": [
            "— End —",
            "如果觉得有用，欢迎 <span style=\"color:#2563eb\">点赞</span> <span style=\"color:#2563eb\">在看</span> <span style=\"color:#2563eb\">转发</span>",
        ],
    },
    "journal": {
        "bg": "#f8f8f6",
        "content_bg": "transparent",
        "text": "#2f3437",
        "accent": "#12a57a",
        "hero_bg": "#ffffff",
        "hero_title_color": "#1f2d2b",
        "bold": "#1f2d2b",
        "rule": "#d9e4df",
        "caption": "#8b9691",
        "title_font_size": "25px",
        "text_font_size": "16px",
        "h2_font_size": "30px",
        "h2_style": "quote_line",
        "cover_label": "COLUMN NOTE",
        "footer": "",
        "ending_lines": [],
    },
    "growth": {
        "bg": "#ffffff",
        "content_bg": "transparent",
        "text": "#2c2c2c",
        "accent": "#2f9d62",
        "hero_bg": "#2f9d62",
        "hero_title_color": "#ffffff",
        "bold": "#1f1f1f",
        "rule": "#dfe8e2",
        "caption": "#8a938d",
        "title_font_size": "24px",
        "text_font_size": "16px",
        "h2_font_size": "18px",
        "h2_style": "badge_block",
        "h2_badge_bg": "#f7b731",
        "h2_badge_text": "#ffffff",
        "cover_label": "WEEKLY INSIGHT",
        "footer": "",
        "ending_lines": [],
    },
    "blueprint": {
        "bg": "#f4f6f8",
        "content_bg": "transparent",
        "text": "#1f2329",
        "accent": "#1857b8",
        "hero_bg": "#1f2a37",
        "hero_title_color": "#f5f7fa",
        "bold": "#16191f",
        "rule": "#cfd8e3",
        "caption": "#7b8794",
        "title_font_size": "24px",
        "text_font_size": "17px",
        "h2_font_size": "42px",
        "h2_style": "center_card",
        "h2_index_bg": "#1857b8",
        "h2_index_text": "#ffffff",
        "cover_label": "PRODUCT BRIEF",
        "footer": "",
        "ending_lines": [],
    },
    "scholar": {
        "bg": "#ffffff",
        "content_bg": "transparent",
        "text": "#333333",
        "accent": "#9b59b6",
        "hero_bg": "#ffffff",
        "hero_title_color": "#1a1a1a",
        "bold": "#333333",
        "rule": "#eeeeee",
        "caption": "#888888",
        "title_font_size": "22px",
        "text_font_size": "15px",
        "h2_font_size": "17px",
        "h2_style": "framed_pill",
        "h2_frame_bg": "#f8f0fb",
        "h2_frame_border": "#9b59b6",
        "h2_frame_border_width": "5px",
        "h2_frame_radius": "4px",
        "h3_color": "#2e7d32",
        "p_indent": "2em",
        "hero_style": "minimal",
        "cover_label": "",
        "footer": "",
        "ending_lines": [],
    },
}


def load_article_style_config(config_path=None):
    """从 config.yaml 读取 style.article 配置，与内置默认值合并"""
    if config_path is None:
        config_path = CONFIG_PATH

    defaults = dict(ARTICLE_DEFAULTS)

    if not os.path.exists(config_path):
        return defaults

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return defaults

    style_match = re.search(r'^style\s*:', content, re.MULTILINE)
    if not style_match:
        return defaults

    style_block = content[style_match.start():]
    in_article = False
    sub_is_list = False
    sub_map = None
    list_initialized = set()
    theme_key = None  # 收集到的 theme 值

    def _parse_value(raw_v):
        raw_v = raw_v.strip()
        if raw_v and raw_v[0] in ('"', "'"):
            end_q = raw_v.find(raw_v[0], 1)
            if end_q > 0:
                return raw_v[1:end_q]
            return raw_v[1:].rstrip('"\'')
        comment_pos = raw_v.find(' #')
        if comment_pos >= 0:
            return raw_v[:comment_pos].strip()
        return raw_v

    for line in style_block.splitlines():
        raw_line = line
        stripped = raw_line.strip()

        # 遇到非 style 子节点的一级 key，停止解析
        if stripped and not stripped.startswith('#') and ':' in stripped and not raw_line.startswith(' ') and not raw_line.startswith('\t'):
            key = stripped.split(':')[0].strip()
            if key == 'style':
                continue
            else:
                break

        if not stripped or stripped.startswith('#'):
            continue

        # 进入 article 模式节点
        if re.match(r'^article\s*:\s*$', stripped):
            in_article = True
            sub_map = None
            sub_is_list = False
            theme_key = None
            continue

        # 遇到其他模式节点，退出 article
        if re.match(r'^(news|daily|ai|essay)\s*:\s*$', stripped):
            in_article = False
            sub_map = None
            sub_is_list = False
            theme_key = None
            continue

        if not in_article:
            continue

        # 列表项（ending_lines）
        if stripped.startswith('- ') and sub_map and sub_is_list:
            list_key = f"article.{sub_map}"
            if list_key not in list_initialized:
                defaults[sub_map] = []
                list_initialized.add(list_key)
            v = _parse_value(stripped[2:])
            if v:
                defaults[sub_map].append(v)
            continue

        # 空列表声明（key: []）
        empty_list_match = re.match(r'^(\w+)\s*:\s*\[\s*\]\s*$', stripped)
        if empty_list_match:
            k = empty_list_match.group(1)
            if k in defaults and isinstance(defaults[k], list):
                defaults[k] = []
                # 标记为已初始化，防止后续列表项添加
                list_initialized.add(f"article.{k}")
            sub_map = None
            sub_is_list = False
            continue

        # 子 key 无值行（列表声明）
        sub_key_match = re.match(r'^(\w+)\s*:\s*$', stripped)
        if sub_key_match:
            k = sub_key_match.group(1)
            if k in defaults and isinstance(defaults[k], list):
                sub_map = k
                sub_is_list = True
            else:
                sub_map = None
                sub_is_list = False
            continue

        # 普通 key: value
        kv_match = re.match(r'^(\w+)\s*:\s*(.+)$', stripped)
        if kv_match:
            k, raw_v = kv_match.group(1), kv_match.group(2)
            v = _parse_value(raw_v)
            sub_map = None
            sub_is_list = False
            # theme 字段特殊处理：收集起来，遍历完后再应用
            if k == "theme":
                theme_key = v
                continue
            if k in defaults:
                defaults[k] = v
            continue

    # 应用预置主题（config 中 theme 优先级最高；article 节内的独立字段会覆盖主题预设）
    if theme_key and theme_key in ARTICLE_THEMES:
        preset = ARTICLE_THEMES[theme_key]
        for pk, pv in preset.items():
            if pk not in list_initialized:
                defaults[pk] = pv

    return defaults


# ─── 前置处理 ─────────────────────────────────────────

def strip_frontmatter(md_text):
    """去掉 Markdown 文件开头的 YAML frontmatter"""
    if md_text.startswith("---"):
        parts = md_text.split("---", 2)
        if len(parts) >= 3:
            body = parts[2].strip()
            return body.lstrip("\n")
    return md_text


# ─── 主入口 ─────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    config_path = None
    no_title = True  # 默认去除标题块

    i = 0
    while i < len(args):
        if args[i] == '--config':
            i += 1
            if i < len(args):
                config_path = args[i]
        elif args[i] == '--no-title':
            no_title = True
        elif args[i] == '--with-title':
            no_title = False
        else:
            break
        i += 1
    args = args[i:]

    if not args:
        print("用法:")
        print("  python3 md2article_html.py <input.md> [output.html]")
        print("  python3 md2article_html.py --config /path/to/config.yaml <input.md> [output.html]")
        sys.exit(1)

    md_file = args[0]
    if len(args) >= 2:
        output_file = args[1]
    else:
        base = os.path.splitext(md_file)[0]
        output_file = f"{base}_article_wechat.html"

    if not os.path.exists(md_file):
        print(f"ERROR: 文件不存在: {md_file}")
        sys.exit(1)

    with open(md_file, "r", encoding="utf-8") as f:
        md_text = f.read()

    md_text = strip_frontmatter(md_text)
    s = load_article_style_config(config_path=config_path)

    data = parse_article(md_text)
    if no_title:
        data['title'] = ""
    html = generate_html(data, s)
    print(f"生成成功（文章模式）: {output_file}")
    print(f"   标题: {data['title']}")
    print(f"   段落块数: {len(data['blocks'])}")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    char_count = len(html)
    print(f"   总字符: {char_count}")


if __name__ == "__main__":
    main()
