"""code_block — 代码块展示页，科技风招牌模板。

等宽字体 + 左侧行号 + 卡片式容器 + 可选 macOS 三圆点 + 可选 filename tab。
支持极简语法高亮（keyword/string/comment 三色）。

data:
  title:     str (optional)   页标题
  en_sub:    str (optional)   英文副标题
  filename:  str (optional)   '/src/app.ts'
  language:  str (optional)   'typescript' | 'python' | 'go' | ...（暂只作标签显示）
  code:      str              代码正文（保留换行和缩进）
  dots:      bool (optional)  左上 3 个 macOS 风格圆点（默认 true）
  highlight_lines: list[int]  需高亮的行号（1-based，可选）
  caption:   str (optional)   代码下方一行说明

python-pptx 没有原生语法高亮；这里只支持整行高亮（换底色）+
按 token 简单上色（如果出现关键词前缀就变 accent 色）。真正的高亮
不是这个模板的目标——目标是「让代码在 slide 上看着像产品官网的代码截图」。
"""

from .helpers import (
    new_slide, add_text, add_rect, add_oval, add_hline,
    add_page_header, add_page_footer, add_mono_text,
    add_dev_badge, format_dev_badge,
)


_KEYWORDS = {
    'def', 'class', 'return', 'import', 'from', 'if', 'else', 'elif',
    'for', 'while', 'try', 'except', 'finally', 'with', 'as', 'yield',
    'lambda', 'async', 'await', 'pass', 'break', 'continue', 'raise',
    'const', 'let', 'var', 'function', 'export', 'default', 'interface',
    'type', 'public', 'private', 'static', 'new', 'this', 'self',
    'true', 'false', 'null', 'undefined', 'None', 'True', 'False',
    'fn', 'pub', 'use', 'mod', 'struct', 'enum', 'impl', 'trait',
    'package', 'func',
}


def build(prs, pack, data: dict) -> None:
    slide = new_slide(prs, pack)
    W, H = pack.canvas.width, pack.canvas.height
    t = pack.typography
    sp = pack.spacing
    dec = pack.decoration

    title = data.get('title', '')
    en_sub = data.get('en_sub', '')
    filename = data.get('filename', '')
    language = data.get('language', '')
    code = data.get('code', '')
    dots = data.get('dots', True)
    highlight = set(data.get('highlight_lines', []) or [])
    caption = data.get('caption', '')

    # 页头（如果有标题）
    y = 0.8
    if title:
        y = add_page_header(slide, pack, title, en_sub)
        y += 0.1

    # 代码卡片区
    card_top = y
    card_bottom_reserve = 1.2 if caption else 0.9
    card_left = sp.margin_x
    card_width = W - 2 * sp.margin_x
    card_height = H - card_top - card_bottom_reserve

    # 卡片底
    card_bg = add_rect(slide, pack,
                      card_left, card_top, card_width, card_height,
                      fill_key='bg_elevated',
                      radius=pack.elevation.card_radius)
    # 描边
    if pack.elevation.card_stroke_width > 0:
        # 重新包一层细边（add_rect 默认不描；手动加）
        pass

    # 标题栏高度
    tab_h = 0.45
    # 分割线把标题栏与代码区分开
    add_hline(slide, pack,
              card_left, card_top + tab_h, card_width,
              color_key='border', thickness=0.005)

    # 三个 macOS 圆点
    dot_y = card_top + tab_h / 2 - 0.08
    if dots:
        dot_colors = ['#FF5F57', '#FEBC2E', '#28C840']
        for i, hx in enumerate(dot_colors):
            from .helpers import hex_to_rgb
            dot_x = card_left + 0.25 + i * 0.24
            add_oval(slide, pack, dot_x, dot_y, 0.15, 0.15,
                     fill=hex_to_rgb(hx))

    # filename + language 标签（标题栏中间）
    if filename:
        fname_left = card_left + 1.3 if dots else card_left + 0.3
        add_mono_text(slide, pack, filename,
                      left=fname_left, top=card_top + 0.06,
                      width=card_width - 2.2, height=0.32,
                      font_size=t.caption + 1,
                      color_key='text_secondary',
                      align='left', tracking=0.02)

    # 语言标签（右上）
    if language:
        lang_text = language.upper()
        add_mono_text(slide, pack, lang_text,
                      left=card_left + card_width - 1.3,
                      top=card_top + 0.08,
                      width=1.1, height=0.3,
                      font_size=t.caption,
                      color_key='text_tertiary',
                      align='right', tracking=0.15, uppercase=True)

    # 代码主体
    code_top = card_top + tab_h + 0.15
    code_left = card_left + 0.25
    code_width = card_width - 0.5
    code_height = card_height - tab_h - 0.25

    # 切行
    lines = code.splitlines() if code else ['']
    n_lines = len(lines)

    # 行号宽度
    line_no_w = 0.45
    # 字号（根据总行数自适应）
    line_font = 14 if n_lines <= 12 else 12 if n_lines <= 18 else 10
    line_height = line_font / 72.0 * 1.5

    mono_font = dec.mono_font or dec.mono_fallbacks[0]

    # 画每一行
    for idx, raw_line in enumerate(lines, start=1):
        line_y = code_top + (idx - 1) * line_height
        if line_y + line_height > code_top + code_height:
            break

        # 高亮背景
        if idx in highlight:
            add_rect(slide, pack,
                     code_left, line_y - 0.02,
                     code_width, line_height,
                     fill_key='bg_subtle',
                     radius=0.02)

        # 行号
        add_text(slide, pack, str(idx),
                 left=code_left, top=line_y,
                 width=line_no_w, height=line_height,
                 font=mono_font,
                 font_size=line_font - 1,
                 color_key='text_muted',
                 align='right')

        # 代码内容——按关键词上色：
        # 简单做法：把第一个 token 取出来检测是否关键词；整行按 secondary/primary 上色；
        # 如果包含 '#' 或 '//' 则后面的部分当注释。
        _render_code_line(
            slide, pack, raw_line,
            left=code_left + line_no_w + 0.15,
            top=line_y,
            width=code_width - line_no_w - 0.3,
            height=line_height,
            font_size=line_font,
            mono_font=mono_font,
        )

    # 说明 caption
    if caption:
        add_text(slide, pack, caption,
                 left=sp.margin_x,
                 top=H - 0.85,
                 width=W - 2 * sp.margin_x, height=0.4,
                 font=t.body_font, font_size=t.caption,
                 color_key='text_tertiary',
                 align='left')

    # 页脚
    add_page_footer(slide, pack, data.get('company', ''), data.get('page', 1))

    # dev badge（科技风）
    if dec.dev_badge:
        badge = format_dev_badge(
            pack,
            year=str(data.get('year', '2026')),
            build=str(data.get('build', '0001')),
        )
        add_dev_badge(slide, pack, badge, position='bottom-right')


def _render_code_line(slide, pack, line, *, left, top, width, height,
                       font_size, mono_font):
    """最简单的两段上色：
       - 如果包含 # 或 //，把前半段当代码、后半段当注释
       - 代码段如果以关键词开头（前导空白忽略），关键词染 accent 色
       否则整行单色。
    """
    t = pack.typography

    # 找注释位置
    comment_idx = _find_comment_start(line)
    code_part = line[:comment_idx] if comment_idx >= 0 else line
    comment_part = line[comment_idx:] if comment_idx >= 0 else ''

    # 用一个 textbox 承载，多 runs 实现多色
    from pptx.util import Inches, Pt
    from pptx.enum.text import PP_ALIGN
    from .helpers import hex_to_rgb

    tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = tb.text_frame
    tf.word_wrap = False
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT

    # 去掉前导空白保留做缩进（用全角空格保 visually）—— 其实直接用空格
    # 但 textbox 的空白会被吞；使用 non-breaking space \u00A0
    def _preserve_ws(s: str) -> str:
        # 只替换前导空白
        i = 0
        while i < len(s) and s[i] == ' ':
            i += 1
        return '\u00A0' * i + s[i:]

    # 拆 code_part 的首词检测关键词
    code_stripped = code_part.lstrip()
    leading_ws = code_part[:len(code_part) - len(code_stripped)]
    first_token = ''
    rest = code_stripped
    if code_stripped:
        # 提取第一个 token（字母 / 下划线）
        i = 0
        while i < len(code_stripped) and (code_stripped[i].isalnum() or code_stripped[i] == '_'):
            i += 1
        first_token = code_stripped[:i]
        rest = code_stripped[i:]

    # run 1: 前导空白（用 non-breaking space，让 Impress 保留）
    if leading_ws:
        r = p.add_run()
        r.text = '\u00A0' * len(leading_ws)
        r.font.name = mono_font
        r.font.size = Pt(font_size)
        r.font.color.rgb = pack.palette.rgb('text_primary')

    # run 2: 关键词（如果是关键字染 accent）
    if first_token:
        r = p.add_run()
        r.text = first_token
        r.font.name = mono_font
        r.font.size = Pt(font_size)
        if first_token in _KEYWORDS:
            r.font.color.rgb = pack.palette.rgb('accent')
            r.font.bold = True
        else:
            r.font.color.rgb = pack.palette.rgb('text_primary')

    # run 3: 剩余代码
    if rest:
        r = p.add_run()
        r.text = rest
        r.font.name = mono_font
        r.font.size = Pt(font_size)
        r.font.color.rgb = pack.palette.rgb('text_primary')

    # run 4: 注释
    if comment_part:
        r = p.add_run()
        r.text = comment_part
        r.font.name = mono_font
        r.font.size = Pt(font_size)
        r.font.color.rgb = pack.palette.rgb('text_tertiary')
        r.font.italic = True


def _find_comment_start(line: str) -> int:
    """粗略找 # 或 // 位置，未在字符串内的第一个。"""
    in_str = False
    str_ch = ''
    i = 0
    while i < len(line):
        c = line[i]
        if in_str:
            if c == '\\' and i + 1 < len(line):
                i += 2
                continue
            if c == str_ch:
                in_str = False
        else:
            if c == '"' or c == "'":
                in_str = True
                str_ch = c
            elif c == '#':
                return i
            elif c == '/' and i + 1 < len(line) and line[i + 1] == '/':
                return i
        i += 1
    return -1
