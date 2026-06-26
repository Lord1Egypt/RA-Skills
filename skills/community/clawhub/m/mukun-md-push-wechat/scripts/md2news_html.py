#!/usr/bin/env python3
"""
Markdown -> 微信兼容 HTML 转换器（新闻模式）

用法:
  python3 md2news_html.py <input.md> [output.html]
  python3 md2news_html.py --config /path/to/config.yaml <input.md> [output.html]

新闻模式：一条消息对应一条新闻，分板块展示，报纸风格配色。
板块颜色、总结表格颜色等均可在 config.yaml 的 style.news 节点中自定义。
"""

import re
import sys
import os

# ─── 配置路径 ──────────────────────────────────────────
CONFIG_PATH = os.path.join(os.path.expanduser("~/.md_push_wechat"), "config.yaml")

# ─── 报纸风格配色 ──────────────────────────────────────
PAPER_BG      = "#f6f1e7"    # 报纸底色：泛黄暖白
PAPER_CARD    = "#faf7f0"    # 卡片底色：略浅的黄白
PAPER_DARK    = "#2c1810"    # 主文字色：深棕
PAPER_HEADING = "#3c2415"    # 标题色：焦棕
PAPER_ACCENT  = "#8b4513"    # 强调色：鞍褐
PAPER_RULE    = "#c4a882"    # 分隔线：浅棕
PAPER_MUTED   = "#8a7e6b"    # 辅助文字：灰棕
PAPER_CAPTION = "#a89880"    # 来源/脚注：淡棕
PAPER_HERO_BG = "#3c2415"    # 封面背景：深棕
PAPER_TABLE_BG = "#f0ead8"   # 表头底色

# 内置默认分类颜色（可在 config.yaml 的 style.news.section_colors 中覆盖）
DEFAULT_SECTION_COLORS = {
    "行业动态":              "#b8860b",
    "AI 工具与智能体更新":    "#556b2f",
    "AI 工具":              "#556b2f",
    "模型发布与更新":         "#4a3728",
    "模型发布":              "#4a3728",
    "重要研究进展":           "#2f4f4f",
    "研究进展":              "#2f4f4f",
    "今日要点总结":           "#3c2415",
    "本周要点总结":           "#3c2415",
}

# 内置默认要点总结表格的类别颜色
DEFAULT_SUMMARY_COLORS = {
    "行业": "#b8860b",
    "工具": "#556b2f",
    "模型": "#4a3728",
    "研究": "#2f4f4f",
}

# 内置默认触发总结表格渲染的板块名称关键词列表
DEFAULT_SUMMARY_SECTIONS = ["总结"]


def _extract_date(meta_text):
    """从 meta 文本中提取日期（YYYY-MM-DD 格式），无匹配返回空字符串"""
    m = re.search(r'(\d{4}-\d{2}-\d{2})', meta_text)
    return m.group(1) if m else ""


# ─── 新闻模式 HTML 模板 ────────────────────────────────

_NEWS_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
/* 代码块浏览器端预览样式（微信平台自有 code-snippet CSS 白名单，此 style 仅用于浏览器预览） */
.code-snippet__fix{{position:relative;margin:12px 0 18px;border-radius:6px;overflow:hidden;font-size:13px;line-height:1.6}}
.code-snippet__fix .code-snippet__js{{font-family:'SF Mono','Fira Code','Consolas','Menlo',monospace}}
.code-snippet__line-index{{position:absolute;top:0;left:0;width:40px;padding:12px 0;margin:0;list-style:none;text-align:right;background:#2b3137;color:#636d83;font-size:12px;line-height:1.6;border-right:1px solid #3a3f47;box-sizing:border-box}}
.code-snippet__line-index li{{padding:0 8px 0 0}}
pre.code-snippet__js{{margin:0;padding:12px 12px 12px 52px;background:#282c34;color:#abb2bf;overflow-x:auto;white-space:pre}}
pre.code-snippet__js code{{display:block;font-family:inherit}}
.code-snippet__keyword{{color:#c678dd;font-weight:bold}}
.code-snippet__built_in{{color:#e5c07b}}
.code-snippet__string{{color:#98c379}}
.code-snippet__number{{color:#d19a66}}
.code-snippet__comment{{color:#5c6370;font-style:italic}}
.code-snippet__title{{color:#61afef}}
.code-snippet__subst{{color:#56b6c2}}
</style>
</head>
<body style="margin:0;padding:24px 16px;background:__BG__;font-family:-apple-system,'PingFang SC','Microsoft YaHei',sans-serif;text-indent:0">

<!-- hero / cover -->
<section style="background:__HERO_BG__;padding:24px 20px 20px;margin:0 0 6px 0;border-top:4px solid __RULE__">
  <p style="margin:0 0 10px 0;font-size:11px;color:__RULE__;letter-spacing:2px;text-align:center">__COVER_LABEL__</p>
  <h1 style="margin:0;font-size:__TITLE_FONT_SIZE__;font-weight:bold;color:#faf7f0;line-height:1.5;text-align:center;border:none">{title}</h1>
</section>

<!-- meta -->
<section style="background:__CARD__;padding:10px 16px;margin:0 0 24px 0;border:1px solid __RULE__;border-top:none">
  <p style="margin:0;font-size:12px;color:__MUTED__;line-height:1.7;text-align:center;letter-spacing:0.5px">{meta}</p>
</section>

{content}

<!-- footer -->
<section style="border-top:2px solid __RULE__;margin:24px 0 0 0;padding:12px 0 0 0;text-align:center">
  <p style="margin:0;font-size:11px;color:__CAPTION__;letter-spacing:1px">{footer}</p>
</section>

</body>
</html>"""


def _build_template(s):
    """用样式配置 s 替换新闻模板占位符"""
    t = _NEWS_TEMPLATE
    for name, val in [
        ("BG", s["bg"]), ("CARD", s["card"]),
        ("DARK", s["dark"]), ("HEADING", s["heading"]),
        ("ACCENT", s["accent"]), ("RULE", s["rule"]),
        ("MUTED", s["muted"]), ("CAPTION", s["caption"]),
        ("HERO_BG", s["hero_bg"]), ("TABLE_BG", s["table_bg"]),
        ("TITLE_FONT_SIZE", s["title_font_size"]),
        ("COVER_LABEL", s.get("cover_label", "AI WEEKLY REVIEW")),
    ]:
        t = t.replace(f"__{name}__", val)
    return t


# ─── Markdown 解析 ─────────────────────────────────────

def parse_markdown(md_text, source_prefixes=None):
    """解析新闻 Markdown，返回结构化数据"""
    if source_prefixes is None:
        source_prefixes = ["来源：", "来源:"]
    lines = md_text.strip().split('\n')

    title = ""
    meta = ""
    sections = []
    current_section = None
    current_items = []
    current_item = None
    in_table = False
    table_lines = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if line.startswith('# ') and not title:
            title = line[2:].strip()
            i += 1
            continue

        if line.startswith('> '):
            meta = line[2:].strip()
            i += 1
            continue

        if line == '---' or line == '***':
            if current_item:
                current_items.append(current_item)
                current_item = None
            if current_section and current_items:
                sections.append({"name": current_section, "items": current_items})
                current_items = []
            i += 1
            continue

        if line.startswith('## '):
            if current_item:
                current_items.append(current_item)
                current_item = None
            if current_section and current_items:
                sections.append({"name": current_section, "items": current_items})
                current_items = []
            current_section = line[3:].strip()
            i += 1
            continue

        if line.startswith('### '):
            if current_item:
                current_items.append(current_item)
            current_item = {
                "title": line[4:].strip(),
                "description": "",
                "source": "",
                "table": None
            }
            i += 1
            continue

        # 支持 **加粗** 作为条目开头（日报格式）
        if line.startswith('**') and current_section:
            if current_item:
                current_items.append(current_item)
            m = re.match(r'\*\*(.+?)\*\*\s*(.*)', line)
            if m:
                item_title = m.group(1)
                item_desc = m.group(2).lstrip('。')
            else:
                item_title = line.strip('*')
                item_desc = ""
            current_item = {
                "title": item_title,
                "description": item_desc,
                "source": "",
                "table": None
            }
            i += 1
            continue

        if line.startswith('|'):
            if not in_table:
                in_table = True
                table_lines = []
            table_lines.append(line)
            i += 1
            continue
        elif in_table and not line.startswith('|'):
            in_table = False
            if current_item:
                current_item["table"] = parse_table(table_lines)
            table_lines = []

        source_matched = False
        for prefix in source_prefixes:
            if line.startswith(prefix):
                if current_item:
                    current_item["source"] = line[len(prefix):].strip()
                source_matched = True
                break
        if source_matched:
            i += 1
            continue

        if not line:
            i += 1
            continue

        if current_item:
            if current_item["description"]:
                current_item["description"] += " " + line
            else:
                current_item["description"] = line

        i += 1

    if in_table and table_lines and current_item:
        current_item["table"] = parse_table(table_lines)
    if current_item:
        current_items.append(current_item)
    if current_section and current_items:
        sections.append({"name": current_section, "items": current_items})

    footer = ""
    for line in lines:
        if line.strip().startswith('*') and line.strip().endswith('*'):
            footer = line.strip().strip('*').strip()
            break

    return {"title": title, "meta": meta, "sections": sections, "footer": footer}


def parse_table(table_lines):
    """解析 Markdown 表格为结构化数据"""
    rows = []
    headers = []

    for i, line in enumerate(table_lines):
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if i == 0:
            headers = cells
        elif i == 1:
            continue
        else:
            rows.append(cells)

    return {"headers": headers, "rows": rows}


# ─── HTML 生成 ─────────────────────────────────────────

def escape_html(text):
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    return text


def md_link_to_html(text, s):
    accent = s["accent"]
    def replace_link(m):
        link_text = m.group(1)
        link_url = m.group(2)
        return f'<a href="{link_url}" style="color: {accent}; text-decoration: none">{link_text}</a>'
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', replace_link, text)


def md_bold_to_html(text, s):
    heading = s["heading"]
    def replace_bold(m):
        return f'<b style="color: {heading}">{m.group(1)}</b>'
    return re.sub(r'\*\*([^*]+)\*\*', replace_bold, text)


def md_code_to_html(text, s):
    table_bg = s.get("table_bg", PAPER_TABLE_BG)
    accent = s["accent"]
    def replace_code(m):
        code = m.group(1)
        return f'<code style="font-size: 12px; background: {table_bg}; color: {accent}; padding: 2px 6px">{code}</code>'
    return re.sub(r'`([^`]+)`', replace_code, text)


def format_text(text, s):
    text = escape_html(text)
    # 行内代码（必须在图片之前处理，避免 `![]()` 被误识别）
    text = md_code_to_html(text, s)
    # 内联图片（必须在链接之前处理，检查是否在 <code> 内）
    def replace_img(m):
        prefix = text[:m.start()]
        last_code_open = prefix.rfind('<code')
        last_code_close = prefix.rfind('</code>')
        if last_code_open > last_code_close:
            return m.group(0)
        alt = m.group(1)
        src = m.group(2)
        return f'<img src="{src}" alt="{escape_html(alt)}" style="max-width:100%;height:auto;vertical-align:middle">'
    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_img, text)
    text = md_link_to_html(text, s)
    text = md_bold_to_html(text, s)
    return text


def render_table(table_data, s):
    if not table_data:
        return ""

    headers = table_data["headers"]
    rows = table_data["rows"]

    col_count = len(headers)
    if col_count == 3:
        col_widths = ["36%", "64%"]
    elif col_count == 2:
        col_widths = ["20%", "80%"]
    else:
        col_widths = [f"{100//col_count}%"] * col_count

    html = f'<table style="width:100%;border-collapse:collapse;margin:0;font-size:13px;border:1px solid {s["rule"]}">\n'

    html += '  <colgroup>\n'
    for w in col_widths:
        html += f'    <col style="width:{w}" />\n'
    html += '  </colgroup>\n'

    html += '  <thead>\n'
    html += f'    <tr style="background:{s["table_bg"]}">\n'
    for h in headers:
        html += f'      <th style="padding:8px 10px;border:1px solid {s["rule"]};text-align:left;font-weight:bold;color:{s["heading"]};font-size:12px;background:{s["table_bg"]}">{format_text(h, s)}</th>\n'
    html += '    </tr>\n'
    html += '  </thead>\n'

    html += '  <tbody>\n'
    for i, row in enumerate(rows):
        html += '    <tr>\n'
        for j, cell in enumerate(row):
            cell_html = format_text(cell, s)
            if '⭐' in cell:
                cell_html = re.sub(r'(\d{1,3}(?:,\d{3})*)', r'<span style="color:#b8860b;font-weight:bold">\1</span>', cell_html)
            border_bottom = f';border-bottom:1px solid #ede5d0' if i < len(rows) - 1 else ''
            html += f'      <td style="padding:8px 10px;border:1px solid {s["rule"]};border-top:none;color:{s["dark"]}{border_bottom}">{cell_html}</td>\n'
        html += '    </tr>\n'
    html += '  </tbody>\n'
    html += '</table>\n'

    return html


def render_item(item, color, s, date=""):
    """渲染单条新闻为 HTML 卡片"""
    card_fs = s.get("card_font_size", s["text_font_size"])
    html = f'<section style="background:{s["card"]};padding:16px;margin:0 0 12px 0;border-left:3px solid {color};border-bottom:1px solid #ede5d0;font-size:{card_fs};color:{s["dark"]};line-height:1.9">\n'

    html += f'  <h3 style="margin:0 0 8px 0;font-size:16px;font-weight:bold;color:{s["heading"]};line-height:1.5">{format_text(item["title"], s)}</h3>\n'

    if item["description"]:
        html += f'  <p style="margin:0 0 8px 0">{format_text(item["description"], s)}</p>\n'

    if item["table"]:
        html += '  ' + render_table(item["table"], s).replace('\n', '\n  ').rstrip() + '\n'

    if item["source"]:
        source_label = s.get("source_label", "来源：")
        source_html = format_text(item["source"], s)
        # 来源文本已含日期，则不再追加全局日期，避免重复
        source_has_date = bool(re.search(r'\d{4}-\d{2}-\d{2}', item["source"]))
        if source_has_date:
            date_suffix = ""
        else:
            date_suffix = f" | {date}" if date else ""
        html += f'  <p style="margin:8px 0 0 0;font-size:11px;color:{s["caption"]};letter-spacing:0.5px">{source_label}{source_html}{date_suffix}</p>\n'

    html += '</section>\n'
    return html


def render_summary_table(item, s):
    """渲染要点总结表格"""
    if not item or not item.get("table"):
        return ""

    table_data = item["table"]
    headers = table_data["headers"]
    rows = table_data["rows"]

    html = f'<section style="background:{s["card"]};padding:16px;border:1px solid {s["rule"]}">\n'
    html += '  <table style="width:100%;border-collapse:collapse;margin:0;font-size:14px">\n'
    html += '    <colgroup>\n'
    html += '      <col style="width:18%" />\n'
    html += '      <col style="width:82%" />\n'
    html += '    </colgroup>\n'
    html += '    <tbody>\n'

    cat_colors = s.get("summary_colors", DEFAULT_SUMMARY_COLORS)

    for i, row in enumerate(rows):
        border = f' style="border-bottom:1px solid {s["rule"]}"' if i < len(rows) - 1 else ''
        cat = row[0].strip('*').strip() if row else ""
        color = cat_colors.get(cat, s["heading"])
        content = format_text(row[1], s) if len(row) > 1 else ""
        html += f'      <tr{border}>\n'
        html += f'        <td style="padding:10px 0;font-weight:bold;color:{color};font-size:14px;background:{s["card"]};vertical-align:top;letter-spacing:1px">{format_text(cat, s)}</td>\n'
        html += f'        <td style="padding:10px 0;color:{s["dark"]};line-height:1.8;font-size:14px;background:{s["card"]}">{content}</td>\n'
        html += '      </tr>\n'

    html += '    </tbody>\n'
    html += '  </table>\n'
    html += '</section>\n'
    return html


def generate_html(data, s):
    """生成微信兼容 HTML（新闻模式）"""
    sections_html = []

    # 从 meta 提取日期
    date = _extract_date(data.get("meta", ""))

    for section in data["sections"]:
        section_name = section["name"]
        section_colors = s.get("section_colors", DEFAULT_SECTION_COLORS)
        color = section_colors.get(section_name, s["accent"])

        section_html = f'<section style="margin:0 0 12px 0">\n'
        section_html += f'  <h2 style="margin:0;font-size:{s["h2_font_size"]};font-weight:bold;color:{s["heading"]};line-height:1;padding:0 0 8px 0;border-bottom:2px solid {s["heading"]};letter-spacing:2px">{section_name}</h2>\n'
        section_html += f'  <hr style="border:none;border-top:1px solid {s["rule"]};margin:0" />\n'
        section_html += '</section>\n'

        summary_sections = s.get("summary_sections", DEFAULT_SUMMARY_SECTIONS)
        is_summary = any(kw in section_name for kw in summary_sections)

        if is_summary:
            if section["items"]:
                section_html += render_summary_table(section["items"][0], s)
        else:
            for item in section["items"]:
                section_html += render_item(item, color, s, date=date)

        if section != data["sections"][-1]:
            section_html += f'<hr style="border:none;border-top:1px solid {s["rule"]};margin:20px 0" />\n'

        sections_html.append(section_html)

    content = '\n'.join(sections_html)

    template = _build_template(s)

    # 如果 markdown 没有 # 一级标题，去掉空白封面区和信息来源栏
    if not data["title"]:
        template = re.sub(
            r'<!-- hero / cover -->.*?<!-- meta -->.*?</section>\s*\n',
            '', template, flags=re.DOTALL
        )

    return template.format(
        title=escape_html(data["title"]),
        meta=format_text(data["meta"], s),
        content=content,
        footer=escape_html(data["footer"])
    )


# ─── 样式配置加载 ─────────────────────────────────────

def load_news_style_config(config_path=None):
    """从 config.yaml 读取 style.news 配置，与内置默认值合并"""
    if config_path is None:
        config_path = CONFIG_PATH

    defaults = {
        "bg": PAPER_BG,
        "card": PAPER_CARD,
        "dark": PAPER_DARK,
        "heading": PAPER_HEADING,
        "accent": PAPER_ACCENT,
        "rule": PAPER_RULE,
        "muted": PAPER_MUTED,
        "caption": PAPER_CAPTION,
        "hero_bg": PAPER_HERO_BG,
        "table_bg": PAPER_TABLE_BG,
        "title_font_size": "22px",
        "text_font_size": "15px",
        "h2_font_size": "18px",
        "card_font_size": "15px",
        "cover_label": "AI WEEKLY REVIEW",
        "section_colors": dict(DEFAULT_SECTION_COLORS),
        "summary_colors": dict(DEFAULT_SUMMARY_COLORS),
        "summary_sections": list(DEFAULT_SUMMARY_SECTIONS),
        "source_label": "来源：",
        "source_prefixes": ["来源：", "来源:"],
    }

    if not os.path.exists(config_path):
        return defaults

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return defaults

    # 定位 style.news 节点
    style_match = re.search(r'^style\s*:', content, re.MULTILINE)
    if not style_match:
        return defaults

    style_block = content[style_match.start():]
    in_news = False
    sub_map = None
    sub_is_list = False
    list_initialized = set()

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

        # 进入 news 模式节点
        if re.match(r'^news\s*:\s*$', stripped):
            in_news = True
            sub_map = None
            sub_is_list = False
            continue

        # 遇到其他模式节点（如 article），退出 news
        if re.match(r'^(daily|ai|essay|article)\s*:\s*$', stripped):
            in_news = False
            sub_map = None
            sub_is_list = False
            continue

        if not in_news:
            continue

        # 列表项
        if stripped.startswith('- ') and sub_map and sub_is_list:
            list_key = f"news.{sub_map}"
            if list_key not in list_initialized:
                defaults[sub_map] = []
                list_initialized.add(list_key)
            v = _parse_value(stripped[2:])
            if v:
                defaults[sub_map].append(v)
            continue

        # 子 map/list key 行
        sub_key_match = re.match(r'^(\w+)\s*:\s*$', stripped)
        if sub_key_match:
            k = sub_key_match.group(1)
            if k in defaults and isinstance(defaults[k], dict):
                sub_map = k
                sub_is_list = False
                defaults[k] = {}
            elif k in defaults and isinstance(defaults[k], list):
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
            if sub_map and not sub_is_list and sub_map in defaults:
                defaults[sub_map][k] = v
                continue
            sub_map = None
            sub_is_list = False
            if k in defaults:
                defaults[k] = v
            continue

        # 含中文的 key: value
        cn_kv = re.match(r'^(.+?)\s*:\s*(.+)$', stripped)
        if cn_kv and sub_map and not sub_is_list:
            k = cn_kv.group(1).strip()
            v = _parse_value(cn_kv.group(2))
            if sub_map in defaults and isinstance(defaults[sub_map], dict):
                defaults[sub_map][k] = v

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
        print("  python3 md2news_html.py <input.md> [output.html]")
        print("  python3 md2news_html.py --config /path/to/config.yaml <input.md> [output.html]")
        sys.exit(1)

    md_file = args[0]
    if len(args) >= 2:
        output_file = args[1]
    else:
        base = os.path.splitext(md_file)[0]
        output_file = f"{base}_news_wechat.html"

    if not os.path.exists(md_file):
        print(f"ERROR: 文件不存在: {md_file}")
        sys.exit(1)

    with open(md_file, "r", encoding="utf-8") as f:
        md_text = f.read()

    md_text = strip_frontmatter(md_text)
    s = load_news_style_config(config_path=config_path)

    data = parse_markdown(md_text, source_prefixes=s.get("source_prefixes", ["来源：", "来源:"]))
    if no_title:
        data['title'] = ""
    html = generate_html(data, s)
    print(f"生成成功（新闻模式）: {output_file}")
    print(f"   标题: {data['title']}")
    print(f"   板块数: {len(data['sections'])}")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    char_count = len(html)
    print(f"   总字符: {char_count}")


if __name__ == "__main__":
    main()
