"""
md2view - MD 转 HTML
输入：.md 文件路径
输出：.html 文件（蓝白灰简约风格 + 表格对齐 + 代码高亮）
"""
import sys
import re
import html
import base64
import os
from datetime import datetime, timedelta
from pathlib import Path

IMG_MIME = {
    '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
    '.gif': 'image/gif', '.webp': 'image/webp', '.svg': 'image/svg+xml',
    '.bmp': 'image/bmp',
}

# 本地图片内嵌策略：'auto' 只允许 .md 同目录及子目录；'all' 显式放开限制
EMBED_LOCAL_IMAGES = 'auto'

# 批量导出模式的时间过滤阈值（None = 不过滤）；按文件修改时间筛选
SINCE = None

USAGE = ("用法: python md2share.py <md文件> [输出html] [--embed-local-images=auto]\n"
         "      python md2share.py <目录> [输出目录] [--since=today|week|7d|YYYY-MM-DD]\n"
         "      python md2share.py <md文件> --long-image[=750] [--png-scale=2] [--long-html-only]\n"
         "\n长图模式（v1.8.0）：输出一张手机可读的长图 PNG（默认 750px 宽 @2x），\n"
         "同时保留一份长图版 HTML 作为兜底。不装任何依赖：用本机已有的\n"
         "Chrome / Chromium / Edge 无头截图；没有浏览器时只出长图版 HTML。")


def parse_since(val, now=None):
    """把 --since 取值解析为 datetime 阈值。

    支持 today / week / 7d / 2026-09-29。只做本地文件修改时间比较，不写入任何状态文件。
    无法识别时返回 None（调用方负责退出）。
    """
    now = now or datetime.now()
    v = (val or '').strip().lower()
    if v in ('today', '今天', '今日'):
        return now.replace(hour=0, minute=0, second=0, microsecond=0)
    if v in ('week', '本周', '这周'):
        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
        return midnight - timedelta(days=midnight.weekday())
    if v.endswith('d') and v[:-1].isdigit():
        return now - timedelta(days=int(v[:-1]))
    try:
        return datetime.strptime(v, '%Y-%m-%d')
    except ValueError:
        print(f"[md2share] 无法识别的 --since 取值: {val}"
              f"（支持 today / week / 7d / 2026-09-29）", file=sys.stderr)
        return None

def split_row(line):
    """按未转义的 | 切分表格行，支持 \\| 转义"""
    line = line.strip()
    if line.startswith('|'):
        line = line[1:]
    if line.endswith('|'):
        line = line[:-1]
    cells = re.split(r'(?<!\\)\|', line)
    return [c.strip().replace('\\|', '|') for c in cells]

def parse_md(md_text):
    """简单 MD 解析器：标题/段落/表格/代码块/列表/引用块"""
    lines = md_text.split('\n')
    blocks = []
    footnotes = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # 代码块
        if line.strip().startswith('```'):
            lang = line.strip()[3:].strip() or 'text'
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            blocks.append({'type': 'code', 'lang': lang, 'content': '\n'.join(code_lines)})
            i += 1
            continue

        # 标题
        m = re.match(r'^(#{1,6})\s+(.+)$', line)
        if m:
            level = len(m.group(1))
            blocks.append({'type': 'h', 'level': level, 'content': m.group(2).strip()})
            i += 1
            continue

        # 分隔线
        if re.match(r'^\s*(?:-{3,}|\*{3,}|_{3,})\s*$', line):
            blocks.append({'type': 'hr'})
            i += 1
            continue

        # 脚注定义 [^id]: text
        m = re.match(r'^\s*\[\^(\w+)\]:\s*(.+)$', line)
        if m:
            footnotes.append({'id': m.group(1), 'text': m.group(2).strip()})
            i += 1
            continue

        # 引用块
        if re.match(r'^\s*>', line):
            quote_lines = []
            while i < len(lines) and re.match(r'^\s*>', lines[i]):
                quote_lines.append(re.sub(r'^\s*>\s?', '', lines[i]))
                i += 1
            blocks.append({'type': 'quote', 'content': ' '.join(quote_lines).strip()})
            continue

        # 表格（必须前后有空行）
        if '|' in line and i + 1 < len(lines) and re.match(r'^\|?\s*[-:|\s]+\|?$', lines[i+1]):
            header = split_row(line)
            i += 2  # 跳过分隔行
            rows = []
            while i < len(lines) and '|' in lines[i] and lines[i].strip():
                rows.append(split_row(lines[i]))
                i += 1
            blocks.append({'type': 'table', 'header': header, 'rows': rows})
            continue

        # 列表（无序/有序/任务/嵌套，统一解析）
        if re.match(r'^\s*(?:[-*]|\d+\.)\s+', line):
            items = []
            list_re = re.compile(r'^(\s*)([-*]|\d+\.)\s+(.*)$')
            while i < len(lines) and lines[i].strip():
                m = list_re.match(lines[i])
                if not m:
                    break
                indent = len(m.group(1).replace('\t', '    '))
                ordered = not m.group(2).startswith(('-', '*'))
                text = m.group(3).strip()
                task = None
                if not ordered:
                    tm = re.match(r'^\[( |x|X)\]\s+(.*)$', text)
                    if tm:
                        task = 'done' if tm.group(1).lower() == 'x' else 'todo'
                        text = tm.group(2)
                items.append({'indent': indent, 'ordered': ordered, 'text': text, 'task': task})
                i += 1
            blocks.append({'type': 'list', 'items': items})
            continue

        # 空行
        if not line.strip():
            i += 1
            continue

        # 普通段落（合并连续行）
        para = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(
                r'^(#{1,6}\s|```|\||\s*[-*]\s|\s*\d+\.\s|\s*>)', lines[i]):
            para.append(lines[i])
            i += 1
        blocks.append({'type': 'p', 'content': ' '.join(para).strip()})

    return blocks, footnotes

LANG_ALIASES = {
    'py': 'python', 'js': 'javascript', 'ts': 'typescript',
    'sh': 'bash', 'shell': 'bash', 'zsh': 'bash',
    'c++': 'cpp', 'cc': 'cpp', 'cxx': 'cpp',
    'golang': 'go', 'rs': 'rust', 'yml': 'yaml', 'kt': 'kotlin', 'rb': 'ruby',
}

MERMAID_TYPES = {
    'flowchart': '流程图', 'graph': '流程图', 'sequencediagram': '时序图',
    'classdiagram': '类图', 'statediagram': '状态图', 'erdiagram': '实体关系图',
    'journey': '用户旅程图', 'gantt': '甘特图', 'pie': '饼图',
    'mindmap': '思维导图', 'timeline': '时间线', 'quadrantchart': '四象限图',
    'gitgraph': 'Git 分支图', 'c4context': 'C4 上下文图', 'sankey': '桑基图',
    'xychart': 'XY 图', 'block': '块图', 'requirementdiagram': '需求图',
    'architecture': '架构图', 'packet': '报文图',
}


def analyze_mermaid(code):
    """识别 Mermaid 图表类型并抽取图内可见文本，供手机端在没有渲染器时读懂结构。

    返回 (类型中文名, 节点标签列表, 正文行数)。纯正则，不执行任何图表代码。
    """
    raw_lines = [ln for ln in code.splitlines() if ln.strip()]
    lines = [ln.strip() for ln in raw_lines
             if not ln.strip().startswith('%%')]
    head = lines[0].lower() if lines else ''
    mtype = ''
    for key in sorted(MERMAID_TYPES, key=len, reverse=True):
        if head.startswith(key):
            mtype = MERMAID_TYPES[key]
            break

    labels = []
    # 方括号 / 花括号 / 圆括号内的节点文本（flowchart、class、state 等）
    for m in re.finditer(r'[\[\{\(（【]([^\[\]\{\}\(\)（）【】\n|]{1,60})[\]\}\)）】]', code):
        t = m.group(1).strip().strip('"\'')
        if t and not re.fullmatch(r'[\d\s,\.\-]+', t) and t not in labels:
            labels.append(t)
    # 引号内的边标签或参与方名称
    for m in re.finditer(r'"([^"\n]{1,40})"', code):
        t = m.group(1).strip()
        if t and t not in labels:
            labels.append(t)
    # sequenceDiagram 的参与方
    for m in re.finditer(r'^\s*(?:participant|actor)\s+([^\s]+)', code, re.M):
        t = m.group(1).strip()
        if t not in labels:
            labels.append(t)

    return mtype, labels[:8], len(raw_lines)


def render_mermaid_block(code, safe_lang):
    """Mermaid 图表在没有渲染器时的降级卡片：类型 + 结构摘要 + 可折叠源码 + 复制。

    不引入任何外链脚本、不上传、不执行图表代码，纯静态 HTML。
    """
    mtype, labels, nlines = analyze_mermaid(code)
    code_html = highlight_code(code, 'text')
    type_label = mtype or 'Mermaid 图表'

    if labels:
        chips = ''.join(
            f'<span class="mmd-chip">{html.escape(t)}</span>' for t in labels
        )
        label_block = (
            '<div class="mmd-sec">'
            '<div class="mmd-sec-title">图里的内容</div>'
            f'<div class="mmd-chips">{chips}</div>'
            '</div>'
        )
    else:
        label_block = ''

    more = '…' if len(labels) >= 8 else ''
    return (
        f'<div class="code-block mmd-card">'
        f'<div class="code-header">'
        f'<span class="code-lang">MERMAID</span>'
        f'<button class="copy-btn">Copy</button>'
        f'</div>'
        f'<div class="mmd-body">'
        f'<div class="mmd-title">'
        f'<span class="mmd-badge">{html.escape(type_label)}</span>'
        f'<span class="mmd-meta">{nlines} 行源码{more}</span>'
        f'</div>'
        f'<div class="mmd-hint">手机端不加载图表渲染库，所以这里显示的是结构摘要。'
        f'要看到实际图形，复制源码后粘贴到任意支持 Mermaid 的编辑器即可。</div>'
        f'{label_block}'
        f'<details class="mmd-src"><summary>展开图表源码</summary>'
        f'<pre><code>{code_html}</code></pre></details>'
        f'</div>'
        f'</div>'
    )


def highlight_code(code, lang):
    """单遍 tokenize 高亮：注释 → 字符串 → 关键字 → 数字，互不嵌套错乱"""
    lang_l = LANG_ALIASES.get((lang or '').lower(), (lang or '').lower())

    keywords_map = {
        'python': ['def', 'class', 'import', 'from', 'return', 'if', 'else', 'elif', 'for', 'while', 'in', 'is', 'not', 'and', 'or', 'try', 'except', 'finally', 'with', 'as', 'lambda', 'pass', 'break', 'continue', 'yield', 'async', 'await', 'True', 'False', 'None', 'self'],
        'javascript': ['function', 'const', 'let', 'var', 'return', 'if', 'else', 'for', 'while', 'do', 'switch', 'case', 'break', 'continue', 'class', 'extends', 'new', 'this', 'super', 'import', 'export', 'from', 'async', 'await', 'try', 'catch', 'finally', 'throw', 'typeof', 'instanceof', 'true', 'false', 'null', 'undefined'],
        'typescript': ['function', 'const', 'let', 'var', 'return', 'if', 'else', 'for', 'while', 'do', 'switch', 'case', 'break', 'continue', 'class', 'extends', 'implements', 'interface', 'type', 'enum', 'namespace', 'readonly', 'public', 'private', 'protected', 'new', 'this', 'super', 'import', 'export', 'from', 'async', 'await', 'try', 'catch', 'finally', 'throw', 'typeof', 'instanceof', 'keyof', 'true', 'false', 'null', 'undefined'],
        'bash': ['if', 'then', 'fi', 'else', 'elif', 'for', 'while', 'do', 'done', 'case', 'esac', 'function', 'return', 'echo', 'export', 'local'],
        'sql': ['SELECT', 'FROM', 'WHERE', 'JOIN', 'INNER', 'LEFT', 'RIGHT', 'ON', 'GROUP', 'BY', 'ORDER', 'HAVING', 'LIMIT', 'INSERT', 'INTO', 'VALUES', 'UPDATE', 'SET', 'DELETE', 'CREATE', 'TABLE', 'DROP', 'ALTER', 'AS', 'AND', 'OR', 'NOT', 'NULL', 'IS'],
        'java': ['public', 'private', 'protected', 'class', 'interface', 'extends', 'implements', 'static', 'final', 'void', 'new', 'return', 'if', 'else', 'for', 'while', 'do', 'switch', 'case', 'break', 'continue', 'try', 'catch', 'finally', 'throw', 'throws', 'import', 'package', 'boolean', 'int', 'long', 'double', 'float', 'char', 'byte', 'short', 'null', 'true', 'false', 'this', 'super', 'abstract', 'synchronized', 'instanceof', 'enum'],
        'c': ['int', 'char', 'float', 'double', 'void', 'long', 'short', 'unsigned', 'signed', 'struct', 'union', 'enum', 'typedef', 'static', 'const', 'return', 'if', 'else', 'for', 'while', 'do', 'switch', 'case', 'break', 'continue', 'sizeof', 'goto', 'extern', 'register', 'volatile', 'NULL'],
        'cpp': ['int', 'char', 'float', 'double', 'void', 'long', 'short', 'unsigned', 'signed', 'struct', 'union', 'enum', 'typedef', 'static', 'const', 'return', 'if', 'else', 'for', 'while', 'do', 'switch', 'case', 'break', 'continue', 'sizeof', 'class', 'public', 'private', 'protected', 'virtual', 'namespace', 'using', 'template', 'typename', 'new', 'delete', 'this', 'bool', 'true', 'false', 'nullptr', 'override', 'try', 'catch', 'throw'],
        'go': ['package', 'import', 'func', 'var', 'const', 'type', 'struct', 'interface', 'map', 'chan', 'go', 'defer', 'if', 'else', 'for', 'range', 'switch', 'case', 'default', 'return', 'break', 'continue', 'nil', 'true', 'false', 'string', 'int', 'int64', 'float64', 'bool', 'byte', 'rune', 'error', 'select', 'fallthrough'],
        'rust': ['fn', 'let', 'mut', 'const', 'static', 'struct', 'enum', 'impl', 'trait', 'use', 'pub', 'mod', 'match', 'if', 'else', 'loop', 'while', 'for', 'in', 'return', 'break', 'continue', 'self', 'Self', 'Some', 'None', 'Ok', 'Err', 'where', 'as', 'dyn', 'async', 'await', 'unsafe', 'move', 'ref', 'true', 'false'],
        'php': ['function', 'class', 'public', 'private', 'protected', 'static', 'echo', 'print', 'return', 'if', 'else', 'elseif', 'foreach', 'for', 'while', 'do', 'switch', 'case', 'break', 'continue', 'new', 'extends', 'implements', 'interface', 'trait', 'namespace', 'use', 'const', 'true', 'false', 'null', 'try', 'catch', 'finally', 'throw', 'instanceof', 'global', 'array'],
        'ruby': ['def', 'end', 'class', 'module', 'if', 'elsif', 'else', 'unless', 'while', 'until', 'for', 'do', 'then', 'require', 'require_relative', 'attr_accessor', 'attr_reader', 'attr_writer', 'nil', 'true', 'false', 'self', 'puts', 'print', 'lambda', 'proc', 'yield', 'rescue', 'ensure', 'begin', 'return', 'break', 'continue', 'case', 'when', 'raise', 'new'],
        'kotlin': ['fun', 'val', 'var', 'class', 'object', 'interface', 'data', 'sealed', 'when', 'if', 'else', 'for', 'while', 'return', 'break', 'continue', 'null', 'true', 'false', 'is', 'in', 'as', 'companion', 'override', 'open', 'abstract', 'lateinit', 'init', 'suspend', 'import', 'package', 'private', 'public', 'internal', 'protected', 'this', 'super'],
        'swift': ['func', 'let', 'var', 'class', 'struct', 'enum', 'protocol', 'extension', 'if', 'else', 'guard', 'for', 'while', 'repeat', 'switch', 'case', 'default', 'return', 'break', 'continue', 'in', 'nil', 'true', 'false', 'self', 'Self', 'init', 'deinit', 'import', 'as', 'is', 'throws', 'rethrows', 'try', 'catch', 'async', 'await', 'some', 'any', 'where', 'static', 'public', 'private', 'internal', 'override', 'final'],
        'json': ['true', 'false', 'null'],
        'yaml': ['true', 'false', 'null', 'yes', 'no', 'on', 'off'],
        'css': ['important', 'media', 'supports', 'keyframes', 'import', 'font-face', 'root'],
    }

    comment_pat = {
        'python': r'#[^\n]*',
        'bash': r'#[^\n]*',
        'yaml': r'#[^\n]*',
        'ruby': r'#[^\n]*',
        'javascript': r'//[^\n]*|/\*[\s\S]*?\*/',
        'typescript': r'//[^\n]*|/\*[\s\S]*?\*/',
        'java': r'//[^\n]*|/\*[\s\S]*?\*/',
        'c': r'//[^\n]*|/\*[\s\S]*?\*/',
        'cpp': r'//[^\n]*|/\*[\s\S]*?\*/',
        'go': r'//[^\n]*|/\*[\s\S]*?\*/',
        'rust': r'//[^\n]*|/\*[\s\S]*?\*/',
        'php': r'//[^\n]*|#[^\n]*|/\*[\s\S]*?\*/',
        'sql': r'--[^\n]*',
        'css': r'/\*[\s\S]*?\*/',
    }.get(lang_l)

    keywords = keywords_map.get(lang_l, [])

    alts = []
    if comment_pat:
        alts.append(f'(?P<cmt>{comment_pat})')
    alts.append(r"(?P<str>\"[^\"\n]*\"|'[^'\n]*'|`[^`\n]*`)")
    if keywords:
        kw_alt = '|'.join(re.escape(k) for k in sorted(keywords, key=len, reverse=True))
        alts.append(rf'(?P<kw>\b(?:{kw_alt})\b)')
    alts.append(r'(?P<num>\b\d+\.?\d*\b)')

    pattern = re.compile('|'.join(alts))

    out = []
    pos = 0
    for m in pattern.finditer(code):
        out.append(html.escape(code[pos:m.start()]))
        gd = m.groupdict()
        if gd.get('cmt') is not None:
            cls = 'cmt'
        elif gd.get('str') is not None:
            cls = 'str'
        elif gd.get('kw') is not None:
            cls = 'kw'
        else:
            cls = 'num'
        out.append(f'<span class="{cls}">{html.escape(m.group(0))}</span>')
        pos = m.end()
    out.append(html.escape(code[pos:]))

    return ''.join(out)

def check_image_magic(path):
    """校验文件头部 magic bytes 是否与声明扩展名匹配，防止伪装成图片的文件被内嵌"""
    ext = path.suffix.lower()
    try:
        with open(path, 'rb') as f:
            head = f.read(16)
    except OSError:
        return False
    if ext == '.png':
        return head.startswith(b'\x89PNG\r\n\x1a\n')
    if ext in ('.jpg', '.jpeg'):
        return head.startswith(b'\xff\xd8')
    if ext == '.gif':
        return head.startswith(b'GIF87a') or head.startswith(b'GIF89a')
    if ext == '.webp':
        return head[:4] == b'RIFF' and head[8:12] == b'WEBP'
    if ext == '.bmp':
        return head.startswith(b'BM')
    if ext == '.svg':
        return b'<' in head[:64]
    return True


def resolve_image_path(url, base_dir):
    """解析图片路径；返回 (absolute_path, allowed)。

    - 远程图片：返回 (None, False)
    - 本地图片：resolve 后只允许 .md 同目录及子目录（沙箱内），
      绝对路径和目录遍历一律拒绝
    - 不存在或格式不支持：返回 (resolved_path, False)
    """
    if re.match(r'^(https?:)', url, re.I):
        return None, False
    if not base_dir:
        return None, False
    try:
        p = Path(url)
        base_resolved = base_dir.resolve()
        if p.is_absolute():
            # 绝对路径永不内嵌：防止把任意位置的本地文件打包进输出 HTML
            return p.resolve(), False
        resolved = (base_resolved / p).resolve()
        return resolved, resolved.is_relative_to(base_resolved)
    except (OSError, ValueError):
        pass
    return None, False


def render_inline(text, base_dir=None):
    """内联处理：**bold** *italic* `code` [link](url) ![img](path) [^fn]"""
    text = html.escape(text)

    # 脚注引用 [^id] → 上标角标
    text = re.sub(r'\[\^(\w+)\]',
                  lambda m: f'<sup class="fn-ref" id="fnref-{m.group(1)}"><a href="#fn-{m.group(1)}">{m.group(1)}</a></sup>',
                  text)

    # 图片 ![alt](url) —— 本地图片内嵌 base64（离线可看），远程图片渲染为链接占位（不自动发请求）
    def img_repl(m):
        alt, url = m.group(1), m.group(2)
        resolved, allowed = resolve_image_path(url, base_dir)
        if resolved is None:
            label = alt or url
            return (f'<span class="img-ext">🖼 <a href="{url}" target="_blank" '
                    f'rel="noopener">{label}</a></span>')
        if allowed and resolved.exists() and resolved.suffix.lower() in IMG_MIME \
                and check_image_magic(resolved):
            data = base64.b64encode(resolved.read_bytes()).decode()
            # 透明度：把每个实际内嵌的本地文件路径打到 stderr
            print(f"[md2share] embedded local image: {resolved}", file=sys.stderr)
            return (f'<img class="md-img" src="data:{IMG_MIME[resolved.suffix.lower()]};'
                    f'base64,{data}" alt="{alt}">')
        # 不可访问或越界的本地图片保持原样，避免静默吞掉
        return m.group(0)
    text = re.sub(r'!\[([^\]]*)\]\(([^)\s]+)\)', img_repl, text)

    # 链接 [text](url) —— 只放行安全协议
    def link_repl(m):
        label, url = m.group(1), m.group(2)
        if re.match(r'^(https?:|mailto:)', url, re.I):
            return f'<a href="{url}" target="_blank" rel="noopener">{label}</a>'
        return m.group(0)
    text = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', link_repl, text)

    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
    text = re.sub(r'`([^`]+)`', r'<code class="inline">\1</code>', text)
    return text

def build_list_tree(items):
    """把缩进的扁平列表项组成树"""
    def parse(idx, indent):
        nodes = []
        while idx < len(items) and items[idx]['indent'] >= indent:
            it = items[idx]
            if it['indent'] == indent:
                idx += 1
                children = []
                if idx < len(items) and items[idx]['indent'] > indent:
                    children, idx = parse(idx, items[idx]['indent'])
                nodes.append({**it, 'children': children})
            else:
                # 比当前层级更深且没有同层节点兜着，挂到上一个节点下
                sub, idx = parse(idx, items[idx]['indent'])
                if nodes:
                    nodes[-1]['children'].extend(sub)
                else:
                    nodes.extend(sub)
        return nodes, idx
    if not items:
        return []
    tree, _ = parse(0, items[0]['indent'])
    return tree

def render_list(nodes, base_dir=None):
    """递归渲染嵌套列表"""
    if not nodes:
        return ''
    tag = 'ol' if nodes[0]['ordered'] else 'ul'
    parts = [f'<{tag}>']
    for n in nodes:
        if n.get('task'):
            cls = 'task-done' if n['task'] == 'done' else 'task-todo'
            box = '☑' if n['task'] == 'done' else '☐'
            parts.append(f'<li class="{cls}"><span class="cbx">{box}</span> {render_inline(n["text"], base_dir)}')
        else:
            parts.append(f'<li>{render_inline(n["text"], base_dir)}')
        if n['children']:
            parts.append(render_list(n['children'], base_dir))
        parts.append('</li>')
    parts.append(f'</{tag}>')
    return ''.join(parts)

def render_html(blocks, title="md2view", base_dir=None, footnotes=None):
    """渲染 blocks 为 HTML；title 为 None 时不注入文件名标题（正文已有 h1）

    h2/h3 数量 >= 3 时自动生成可折叠目录（锚点跳转，暗色适配）。
    """
    # 给 h2/h3 分配锚点 id，并构建 TOC
    toc_entries = []
    sec_n = 0
    for b in blocks:
        if b['type'] == 'h' and b['level'] in (2, 3):
            sec_n += 1
            b['_id'] = f'sec-{sec_n}'
            toc_entries.append((b['level'], b['_id'], b['content']))

    parts = []
    if title is not None:
        parts.append(f'<h1 class="title">{html.escape(title)}</h1>')

    # 目录：h2 >= 3 个才生成（短文档不需要跳转）
    h2_count = sum(1 for lvl, _, _ in toc_entries if lvl == 2)
    if h2_count >= 3:
        parts.append('<details class="toc"><summary>目录 · Contents</summary><nav>')
        for lvl, sec_id, content in toc_entries:
            cls = 'toc-h3' if lvl == 3 else 'toc-h2'
            parts.append(
                f'<a class="{cls}" href="#{sec_id}">{html.escape(content)}</a>'
            )
        parts.append('</nav></details>')

    for b in blocks:
        if b['type'] == 'h':
            lvl = b['level']
            tag = f'h{lvl}'
            sec_id = b.get('_id')
            id_attr = f' id="{sec_id}"' if sec_id else ''
            parts.append(f'<{tag} class="{tag}"{id_attr}>{render_inline(b["content"], base_dir)}</{tag}>')
        elif b['type'] == 'p':
            parts.append(f'<p>{render_inline(b["content"], base_dir)}</p>')
        elif b['type'] == 'quote':
            parts.append(f'<blockquote>{render_inline(b["content"], base_dir)}</blockquote>')
        elif b['type'] == 'hr':
            parts.append('<hr class="md-hr">')
        elif b['type'] == 'list':
            parts.append(render_list(build_list_tree(b['items']), base_dir))
        elif b['type'] == 'code':
            # code-fence 语言标注来自不可信输入，只保留安全字符集并转义，防 HTML 注入（T09）
            _safe_lang = re.sub(r'[^A-Za-z0-9+#._-]', '', (b['lang'] or '').strip())[:24]
            if _safe_lang.lower() == 'mermaid':
                parts.append(render_mermaid_block(b['content'], _safe_lang))
                continue
            code_html = highlight_code(b['content'], b['lang'])
            lang_label = html.escape(_safe_lang.upper()) if _safe_lang else 'TEXT'
            parts.append(
                f'<div class="code-block">'
                f'<div class="code-header">'
                f'<span class="code-lang">{lang_label}</span>'
                f'<button class="copy-btn">Copy</button>'
                f'</div>'
                f'<pre><code>{code_html}</code></pre>'
                f'</div>'
            )
        elif b['type'] == 'table':
            parts.append('<div class="table-wrap"><table>')
            parts.append('<thead><tr>')
            for h in b['header']:
                parts.append(f'<th>{render_inline(h, base_dir)}</th>')
            parts.append('</tr></thead>')
            parts.append('<tbody>')
            for ri, row in enumerate(b['rows']):
                cls = 'odd' if ri % 2 else 'even'
                parts.append(f'<tr class="{cls}">')
                for c in row:
                    parts.append(f'<td>{render_inline(c, base_dir)}</td>')
                parts.append('</tr>')
            parts.append('</tbody></table></div>')

    if footnotes:
        parts.append('<section class="footnotes">')
        parts.append('<div class="fn-title">NOTES · 注释</div>')
        for fn in footnotes:
            parts.append(
                f'<div class="fn-item" id="fn-{fn["id"]}">'
                f'<span class="fn-num">[{fn["id"]}]</span> {render_inline(fn["text"], base_dir)}'
                f'<a class="fn-back" href="#fnref-{fn["id"]}"> ↩</a></div>'
            )
        parts.append('</section>')

    return '\n'.join(parts)

def build_page(content_html, title="md2view"):
    """完整 HTML 页面（蓝白灰风格）"""
    css = """
:root {
  --primary: #1F4E79;
  --accent: #3B7DD8;
  --bg: #F5F7FA;
  --card: #FFFFFF;
  --text: #333333;
  --text-light: #666666;
  --border: #E1E5EB;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: system-ui, -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.7;
  padding: 20px;
  -webkit-text-size-adjust: 100%;
}
.container {
  max-width: 720px;
  margin: 0 auto;
  background: var(--card);
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(31, 78, 121, 0.08);
  padding: 32px 24px;
}
.title {
  color: var(--primary);
  font-size: 28px;
  font-weight: 700;
  border-bottom: 2px solid var(--primary);
  padding-bottom: 12px;
  margin-bottom: 24px;
}
h1, h2, h3, h4, h5, h6 {
  color: var(--primary);
  margin: 24px 0 12px;
  font-weight: 600;
}
h1 { font-size: 24px; }
h2 { font-size: 20px; }
h3 { font-size: 18px; }
p {
  margin: 12px 0;
  font-size: 16px;
}
strong { color: var(--primary); font-weight: 600; }
em { color: var(--accent); }
a {
  color: var(--accent);
  text-decoration: none;
  border-bottom: 1px solid rgba(59, 125, 216, 0.35);
  word-break: break-all;
}
blockquote {
  margin: 16px 0;
  padding: 10px 16px;
  border-left: 4px solid var(--accent);
  background: #EEF2F7;
  color: var(--text-light);
  border-radius: 0 6px 6px 0;
}
ul, ol {
  margin: 12px 0 12px 24px;
}
ul ul, ul ol, ol ul, ol ol { margin: 6px 0 6px 20px; }
li { margin: 6px 0; }
.md-img {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  margin: 8px 0;
  border: 1px solid var(--border);
}
.img-ext {
  display: inline-block;
  background: #EEF2F7;
  border-radius: 4px;
  padding: 2px 8px;
  font-size: 14px;
}
li.task-done, li.task-todo { list-style: none; margin-left: -20px; }
li.task-done { color: var(--text-light); text-decoration: line-through; }
li.task-done .cbx { text-decoration: none; }
code.inline {
  background: #EEF2F7;
  color: var(--primary);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: "SF Mono", Menlo, Monaco, Consolas, monospace;
  font-size: 14px;
}
.code-block {
  margin: 16px 0;
  background: #F8FAFC;
  border-left: 3px solid var(--primary);
  border-radius: 6px;
  overflow: hidden;
  position: relative;
}
.code-header {
  background: var(--primary);
  color: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 4px 0;
}
.mmd-card {
  border-left-color: #7C5CD6;
  background: #FAF8FF;
}
.mmd-card .code-header { background: #5B44A8; }
.mmd-body { padding: 14px 16px 16px; }
.mmd-title {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 8px;
}
.mmd-badge {
  background: #EDE7FB;
  color: #4A3590;
  font-size: 13px;
  font-weight: 700;
  padding: 3px 10px;
  border-radius: 999px;
  border: 1px solid #D9CDF5;
}
.mmd-meta {
  font-size: 12px;
  color: #8A8798;
}
.mmd-hint {
  font-size: 13px;
  line-height: 1.6;
  color: #5F5B6E;
  background: #F2EEFC;
  border-radius: 6px;
  padding: 8px 10px;
  margin-bottom: 10px;
}
.mmd-sec { margin-bottom: 10px; }
.mmd-sec-title {
  font-size: 12px;
  font-weight: 600;
  color: #6B6480;
  letter-spacing: 0.3px;
  margin-bottom: 6px;
}
.mmd-chips { display: flex; flex-wrap: wrap; gap: 6px; }
.mmd-chip {
  font-size: 12.5px;
  line-height: 1.4;
  color: #3B3560;
  background: #FFFFFF;
  border: 1px solid #E0D9F2;
  border-radius: 5px;
  padding: 2px 8px;
  max-width: 100%;
  overflow-wrap: anywhere;
}
.mmd-src summary {
  font-size: 13px;
  color: #5B44A8;
  cursor: pointer;
  padding: 4px 0;
  font-weight: 600;
  list-style: none;
}
.mmd-src summary::-webkit-details-marker { display: none; }
.mmd-src summary::before { content: '▸ '; }
.mmd-src[open] summary::before { content: '▾ '; }
.mmd-src pre {
  margin-top: 6px;
  border-radius: 6px;
}
body.dark .code-block.mmd-card { background: #1A1725; }
body.dark .code-block.mmd-card .code-header { background: #4A3585; }
body.dark .mmd-badge { background: #2E2745; color: #C9B8F5; border-color: #443A63; }
body.dark .mmd-hint { background: #241F35; color: #B9B2CC; }
body.dark .mmd-sec-title { color: #A79FBF; }
body.dark .mmd-chip { background: #221E30; color: #D6CDF0; border-color: #3A3350; }
body.dark .mmd-src summary { color: #B49BF0; }
.code-lang {
  padding: 0 12px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.5px;
}
.copy-btn {
  background: rgba(255, 255, 255, 0.15);
  color: #fff;
  border: 1px solid rgba(255, 255, 255, 0.3);
  padding: 3px 10px;
  font-size: 12px;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 8px;
  font-family: inherit;
  transition: all 0.2s;
}
.copy-btn:hover { background: rgba(255, 255, 255, 0.25); }
.copy-btn.copying { background: #3B7DD8; border-color: #3B7DD8; }
.copy-btn.copied { background: #27AE60; border-color: #27AE60; }
.copy-btn.copied::after { content: ' ✓'; }
.code-block pre {
  padding: 16px;
  overflow-x: auto;
  font-family: "SF Mono", Menlo, Monaco, Consolas, monospace;
  font-size: 14px;
  line-height: 1.6;
}
.code-block code .kw { color: #C0392B; font-weight: 600; }
.code-block code .str { color: #27AE60; }
.code-block code .num { color: #2980B9; }
.code-block code .cmt { color: #7F8C8D; font-style: italic; }
.table-wrap {
  margin: 16px 0;
  overflow-x: auto;
  border-radius: 6px;
  border: 1px solid var(--border);
}
table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}
th {
  background: var(--primary);
  color: #fff;
  padding: 10px 12px;
  text-align: left;
  font-weight: 600;
  white-space: nowrap;
}
td {
  padding: 10px 12px;
  border-bottom: 1px solid var(--border);
}
tr.odd { background: #FAFBFC; }
tr.even { background: #FFFFFF; }
tr:hover { background: #EEF2F7; }
.md-hr {
  border: none;
  height: 2px;
  background: linear-gradient(to right, transparent, var(--border) 15%, var(--accent) 50%, var(--border) 85%, transparent);
  margin: 28px 0;
}
/* ---- TOC 目录 ---- */
details.toc {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  margin: 20px 0;
  overflow: hidden;
}
details.toc summary {
  cursor: pointer;
  padding: 12px 18px;
  font-size: 13px;
  font-weight: 600;
  color: var(--primary);
  letter-spacing: 1px;
  user-select: none;
  list-style: none;
}
details.toc summary::-webkit-details-marker { display: none; }
details.toc summary::before { content: '▸ '; }
details.toc[open] summary::before { content: '▾ '; }
details.toc nav {
  display: flex;
  flex-direction: column;
  padding: 4px 18px 14px;
}
details.toc a {
  color: var(--text);
  text-decoration: none;
  font-size: 14px;
  line-height: 1.5;
  padding: 5px 0;
  border-bottom: 1px dashed var(--border);
}
details.toc a:last-child { border-bottom: none; }
details.toc a.toc-h3 {
  padding-left: 18px;
  font-size: 13px;
  color: var(--text-light);
}
h2[id], h3[id] { scroll-margin-top: 12px; }
.footnotes {
  margin-top: 32px;
  padding-top: 16px;
  border-top: 1px dashed var(--border);
}
.fn-title {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-light);
  letter-spacing: 2px;
  margin-bottom: 8px;
}
.fn-item {
  font-size: 13px;
  color: var(--text-light);
  margin: 6px 0;
  line-height: 1.6;
}
.fn-num { color: var(--accent); font-weight: 600; }
sup.fn-ref { font-size: 12px; }
sup.fn-ref a { border: none; text-decoration: none; font-weight: 600; }
.fn-back { border: none; }
.theme-toggle {
  position: fixed;
  top: 16px;
  right: 16px;
  width: 38px;
  height: 38px;
  border-radius: 50%;
  border: 1px solid var(--border);
  background: var(--card);
  color: var(--text);
  font-size: 16px;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0,0,0,0.12);
  z-index: 99;
}
/* 暗色模式：跟随系统 + 可手动切换 */
@media (prefers-color-scheme: dark) {
  body:not(.light) {
    --primary: #8AB6E8; --accent: #5C9BE0;
    --bg: #14181D; --card: #1E242B;
    --text: #D8DEE6; --text-light: #97A2AE; --border: #39434E;
  }
  body:not(.light) .code-block { background: #161B21; }
  body:not(.light) blockquote,
  body:not(.light) code.inline,
  body:not(.light) .img-ext { background: #232B34; }
  body:not(.light) tr.odd { background: #23282F; }
  body:not(.light) tr.even { background: #1E242B; }
  body:not(.light) tr:hover { background: #2A323C; }
}
body.dark {
  --primary: #8AB6E8; --accent: #5C9BE0;
  --bg: #14181D; --card: #1E242B;
  --text: #D8DEE6; --text-light: #97A2AE; --border: #39434E;
}
body.dark .code-block { background: #161B21; }
body.dark blockquote,
body.dark code.inline,
body.dark .img-ext { background: #232B34; }
body.dark tr.odd { background: #23282F; }
body.dark tr.even { background: #1E242B; }
body.dark tr:hover { background: #2A323C; }
@media (max-width: 480px) {
  body { padding: 12px; }
  .container { padding: 20px 16px; }
  .title { font-size: 22px; }
  th, td { padding: 8px 10px; font-size: 13px; }
}
"""
    js = """
// 主题切换（跟随系统 + 手动覆盖，记忆选择）
(function () {
  const saved = (() => { try { return localStorage.getItem('md2view-theme'); } catch (e) { return null; } })();
  if (saved === 'dark') document.body.classList.add('dark');
  else if (saved === 'light') document.body.classList.add('light');
  const toggle = document.createElement('button');
  toggle.className = 'theme-toggle';
  const updateIcon = () => { toggle.textContent = document.body.classList.contains('dark') ? '☀️' : '🌙'; };
  toggle.addEventListener('click', () => {
    if (document.body.classList.contains('dark')) {
      document.body.classList.remove('dark'); document.body.classList.add('light');
    } else {
      document.body.classList.remove('light'); document.body.classList.add('dark');
    }
    try { localStorage.setItem('md2view-theme', document.body.classList.contains('dark') ? 'dark' : 'light'); } catch (e) {}
    updateIcon();
  });
  updateIcon();
  document.body.appendChild(toggle);
})();
document.querySelectorAll('.copy-btn').forEach(btn => {
  btn.addEventListener('click', async () => {
    const pre = btn.closest('.code-block') && btn.closest('.code-block').querySelector('pre');
    const code = pre ? pre.textContent : '';
    btn.classList.add('copying');
    btn.textContent = 'Copying...';
    try {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(code);
      } else {
        const ta = document.createElement('textarea');
        ta.value = code;
        ta.style.position = 'fixed';
        ta.style.opacity = '0';
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
      }
      btn.classList.remove('copying');
      btn.classList.add('copied');
      btn.textContent = 'Copied!';
      setTimeout(() => {
        btn.classList.remove('copied');
        btn.textContent = 'Copy';
      }, 2000);
    } catch (e) {
      btn.classList.remove('copying');
      btn.textContent = 'Failed';
      setTimeout(() => { btn.textContent = 'Copy'; }, 2000);
    }
  });
});
"""
    title_esc = html.escape(title)
    return (
        "<!DOCTYPE html>\n"
        "<html lang=\"zh-CN\">\n"
        "<head>\n"
        "<meta charset=\"UTF-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"
        "<title>" + title_esc + "</title>\n"
        "<style>" + css + "</style>\n"
        "</head>\n"
        "<body>\n"
        "<div class=\"container\">\n"
        + content_html + "\n"
        "</div>\n"
        "<script>" + js + "</script>\n"
        "</body>\n"
        "</html>\n"
    )

# ============================================================
# 长图导出（v1.8.0）
# ============================================================
# 设计取舍：长图不是"把网页截个图"，它有三个硬约束，网页版 CSS 一条都不满足：
#   1. 不能横向滚动 —— 滚动区在图片里等于被裁掉，表格/代码必须换行
#   2. 不能有交互控件 —— 复制按钮、主题开关截进图里就是死的假 UI
#   3. 不能有目录 —— 图片里的锚点是废的，只会白占版面
# 所以长图走独立 CSS + 独立页面壳，正文仍复用同一套 render_html，保证两种出口长得一致。

LONG_IMAGE = False      # 是否启用长图模式
LONG_WIDTH = 750        # 画布宽度（CSS px）
PNG_SCALE = 2           # 输出倍率：2 = 1500px 宽，手机上看不糊
LONG_KEEP_ONLY_HTML = False   # 只要长图版 HTML，不尝试截图

LONG_CSS = """
:root {
  --primary: #1F4E79;
  --accent: #3B7DD8;
  --card: #FFFFFF;
  --text: #333333;
  --text-light: #666666;
  --border: #E1E5EB;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
html { background: #FFFFFF; }
body {
  width: %(width)dpx;
  margin: 0 auto;
  background: #FFFFFF;
  color: var(--text);
  font-family: system-ui, -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif;
  font-size: 17.5px;
  line-height: 1.85;
  padding: 44px 40px 36px;
  -webkit-font-smoothing: antialiased;
  -webkit-text-size-adjust: 100%%;
}
.container { width: 100%%; }
.title {
  color: var(--primary);
  font-size: 32px;
  font-weight: 700;
  line-height: 1.35;
  border-bottom: 3px solid var(--primary);
  padding-bottom: 14px;
  margin-bottom: 26px;
}
h1, h2, h3, h4, h5, h6 { color: var(--primary); font-weight: 600; line-height: 1.4; }
h1 { font-size: 28px; margin: 34px 0 16px; }
h2 {
  font-size: 24px;
  margin: 36px 0 16px;
  padding-left: 12px;
  border-left: 5px solid var(--accent);
}
h3 { font-size: 20.5px; margin: 28px 0 12px; }
h4, h5, h6 { font-size: 18px; margin: 22px 0 10px; color: var(--text); }
p { margin: 14px 0; }
ul, ol { margin: 14px 0; padding-left: 26px; }
li { margin: 7px 0; }
li > ul, li > ol { margin: 7px 0; }
strong { color: #1a1a1a; font-weight: 600; }
em { color: var(--text-light); }
a { color: var(--accent); text-decoration: none; border-bottom: 1px solid rgba(59,125,216,.35); word-break: break-all; }
/* 图片里的链接点不动，把地址直接印在文字后面 */
a[href^="http"]::after {
  content: " (" attr(href) ")";
  font-size: 12.5px;
  color: #9AA5B1;
  border: 0;
  word-break: break-all;
}
a[href^="#"]::after { content: ""; }
code {
  font-family: "SF Mono", Menlo, Monaco, Consolas, monospace;
  font-size: 0.9em;
  background: #F0F3F8;
  color: #C0392B;
  border-radius: 4px;
  padding: 2px 5px;
  word-break: break-word;
}
/* 代码块：不滚动、不裁切，整段折行 */
.code-block {
  margin: 18px 0;
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
  background: #FAFBFD;
}
.code-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #EDF1F7;
  border-bottom: 1px solid var(--border);
  padding: 7px 14px;
}
.code-lang {
  font-size: 12px;
  font-weight: 600;
  letter-spacing: .08em;
  color: #5B6B7C;
  text-transform: uppercase;
}
.copy-btn { display: none; }
.code-block pre {
  margin: 0;
  padding: 14px 16px;
  overflow: visible;
  white-space: pre-wrap;
  word-break: break-all;
  font-family: "SF Mono", Menlo, Monaco, Consolas, monospace;
  font-size: 13.5px;
  line-height: 1.65;
  color: #2B2B2B;
}
.code-block pre code { background: none; padding: 0; color: inherit; font-size: inherit; }
/* 表格：拆掉横向滚动，允许单元格折行 */
.table-wrap { overflow: visible; margin: 18px 0; }
table {
  width: 100%%;
  border-collapse: collapse;
  font-size: 15.5px;
  table-layout: fixed;
}
th, td {
  border: 1px solid var(--border);
  padding: 9px 11px;
  text-align: left;
  vertical-align: top;
  word-break: break-word;
  overflow-wrap: anywhere;
}
th {
  background: var(--primary);
  color: #FFFFFF;
  font-weight: 600;
  white-space: normal;
}
tbody tr:nth-child(even) { background: #F7F9FC; }
blockquote {
  margin: 18px 0;
  padding: 12px 18px;
  border-left: 4px solid var(--accent);
  background: #F7F9FC;
  color: #4A5568;
  border-radius: 0 6px 6px 0;
}
blockquote p { margin: 6px 0; }
.md-hr { border: 0; border-top: 1px solid var(--border); margin: 30px 0; }
/* 图片里目录的锚点是废的，整块隐藏 */
.toc { display: none !important; }
.footnotes { margin-top: 30px; padding-top: 16px; border-top: 1px solid var(--border); font-size: 14.5px; color: var(--text-light); }
.md-footer {
  margin-top: 34px;
  padding-top: 14px;
  border-top: 1px dashed var(--border);
  font-size: 13px;
  color: #9AA5B1;
  display: flex;
  justify-content: space-between;
  gap: 16px;
}
"""


def find_chromium():
    """找本机已有的 Chromium 系浏览器。找不到就返回 None —— 不装、不下载任何东西。"""
    import shutil
    import platform

    candidates = []
    if platform.system() == 'Darwin':
        candidates += [
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            '/Applications/Chromium.app/Contents/MacOS/Chromium',
            '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
            '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser',
        ]
    for name in ('google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser',
                 'microsoft-edge', 'msedge', 'brave-browser', 'chrome'):
        p = shutil.which(name)
        if p:
            candidates.append(p)
    if platform.system() == 'Windows':
        candidates += [
            r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
            r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        ]
    for c in candidates:
        if c and os.path.isfile(c) and os.access(c, os.X_OK):
            return c
    return None


PRIVACY_PATTERNS = [
    ('手机号', re.compile(r'(?<!\d)1[3-9]\d{9}(?!\d)')),
    ('身份证号', re.compile(r'(?<!\d)\d{17}[\dXx](?!\d)')),
    ('邮箱', re.compile(r'[\w.+-]+@[\w-]+\.[\w.]{2,}')),
    ('疑似密钥', re.compile(r'(?:sk-|ghp_|gho_|AKIA|AIza)[A-Za-z0-9_\-]{12,}')),
    ('银行卡号', re.compile(r'(?<!\d)\d{16,19}(?!\d)')),
]


def scan_privacy(md_text):
    """出图前的隐私自检。

    长图比文本更容易被随手转发（转发一张图不用看内容，转发一段文字要先读一遍），
    所以这里只在长图模式下触发。刻意不打印命中的原文，只报类别和数量——
    否则日志本身又成了泄露源。
    """
    findings = []
    for label, pat in PRIVACY_PATTERNS:
        hits = pat.findall(md_text)
        if hits:
            findings.append((label, len(hits)))
    return findings


def build_long_page(content_html, title="md2view", width=750):
    """长图专用页面壳：固定宽度、无 JS、无交互控件、无目录。"""
    # 用 body.scrollHeight 而不是 documentElement 的：后者会被视口高度托底，
    # 内容比视口短时就会截出一大截空白。
    meta_js = (
        "<script>window.addEventListener('load',function(){"
        "var h=Math.ceil(document.body.scrollHeight);"
        "var m=document.createElement('meta');"
        "m.setAttribute('name','md-height');m.setAttribute('content',h);"
        "document.head.appendChild(m);});</script>"
    )
    stamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    footer = (
        "<div class=\"md-footer\">"
        f"<span>{html.escape(title)}</span>"
        f"<span>生成于 {stamp}</span>"
        "</div>"
    )
    return (
        "<!DOCTYPE html>\n"
        "<html lang=\"zh-CN\">\n"
        "<head>\n"
        "<meta charset=\"UTF-8\">\n"
        f"<meta name=\"viewport\" content=\"width={width}, initial-scale=1.0\">\n"
        f"<title>{html.escape(title)}</title>\n"
        f"<style>{LONG_CSS % {'width': width}}</style>\n"
        f"{meta_js}\n"
        "</head>\n"
        "<body>\n"
        "<div class=\"container\">\n"
        + content_html + "\n"
        + footer + "\n"
        "</div>\n"
        "</body>\n"
        "</html>\n"
    )


def _run_chrome(chrome, extra_args, timeout):
    """跑一次无头 Chrome，先按常规参数，失败了再补 --no-sandbox 重试。

    为什么不一上来就 --no-sandbox：它会关掉 Chrome 的进程沙箱。对一个只渲染
    用户自己 markdown 的本地工具来说风险不大，但没必要默认关——先按正常参数试，
    只有在受限环境（容器、CI、某些公司策略机）里报错时才降级重试。
    每次都用一次性的 user-data-dir，绝不碰用户已登录的 Chrome 配置。
    """
    import subprocess
    import shutil as _shutil
    import tempfile

    base = [chrome, '--headless=new', '--disable-gpu',
            '--hide-scrollbars', '--no-first-run', '--no-default-browser-check',
            '--disable-extensions', '--disable-background-networking',
            '--disable-sync', '--virtual-time-budget=4000']

    last_err = None
    for extra in ([], ['--no-sandbox', '--disable-dev-shm-usage']):
        profile = tempfile.mkdtemp(prefix='md2share-chrome-')
        try:
            cmd = base + [f'--user-data-dir={profile}'] + extra + extra_args
            r = subprocess.run(cmd, capture_output=True, timeout=timeout)
            if r.returncode == 0:
                return r
            last_err = (r.stderr or b'').decode('utf-8', 'ignore')[-300:]
        except (subprocess.TimeoutExpired, OSError) as e:
            last_err = str(e)
        finally:
            _shutil.rmtree(profile, ignore_errors=True)
    if last_err:
        print(f"[md2share] Chrome 执行失败：{last_err}", file=sys.stderr)
    return None


def measure_page_height(chrome, html_path, width, timeout=120):
    """第一遍：让页面把 scrollHeight 写进 <meta>，再用 --dump-dom 读回来。

    为什么不能直接截全页：无头 Chrome 的 --screenshot 只截视口，全页截图得先知道高度。
    CDP 的 captureBeyondViewport 要 websocket，标准库没有；两遍渲染是纯标准库能做到的最稳办法。
    """
    import urllib.parse

    url = 'file://' + urllib.parse.quote(str(html_path.resolve()))
    r = _run_chrome(chrome, [
        f'--window-size={width},1600',
        '--dump-dom', url,
    ], timeout=timeout)
    if r is None:
        return None
    dom = r.stdout.decode('utf-8', 'ignore')
    m = (re.search(r'name="md-height"\s+content="(\d+)"', dom)
         or re.search(r'content="(\d+)"\s+name="md-height"', dom))
    return int(m.group(1)) if m else None


def capture_png(chrome, html_path, png_path, width, height, scale=2, timeout=180):
    """第二遍：按测出来的高度整页截图，默认 2 倍图。"""
    import urllib.parse

    url = 'file://' + urllib.parse.quote(str(html_path.resolve()))
    _run_chrome(chrome, [
        f'--window-size={width},{height}',
        f'--force-device-scale-factor={scale}',
        '--default-background-color=FFFFFFFF',
        f'--screenshot={png_path.resolve()}',
        url,
    ], timeout=timeout)
    return png_path.exists() and png_path.stat().st_size > 1024


def convert_to_long_image(md_path, base_output=None):
    """md → 长图版 HTML（+ 尽力产出 PNG）。返回 (html_path, png_path or None)。"""
    md_text = md_path.read_text(encoding='utf-8')
    blocks, footnotes = parse_md(md_text)
    has_h1 = any(b['type'] == 'h' and b['level'] == 1 for b in blocks)
    title = None if has_h1 else md_path.stem
    content = render_html(blocks, title=title, base_dir=md_path.parent, footnotes=footnotes)

    html_path = (base_output.with_suffix('.long.html') if base_output
                 else md_path.with_suffix('.long.html'))
    html_doc = build_long_page(content, title=md_path.stem, width=LONG_WIDTH)
    html_path.write_text(html_doc, encoding='utf-8')

    # —— 出图前隐私自检（长图更容易被随手转发，转发前不一定有人细读） ——
    findings = scan_privacy(md_text)
    if findings:
        detail = '、'.join(f'{k}×{n}' for k, n in findings)
        print(f"[md2share] ⚠️ 隐私自检：检测到 {detail}。"
              f"长图可能被随手转发，请先确认是否要出图。", file=sys.stderr)

    if LONG_KEEP_ONLY_HTML:
        return html_path, None

    chrome = find_chromium()
    if not chrome:
        print("[md2share] 未找到 Chrome/Chromium/Edge，已只生成长图版 HTML。"
              "可以直接在浏览器里打开并整页截图，或安装任一 Chromium 系浏览器后重跑。",
              file=sys.stderr)
        return html_path, None

    height = measure_page_height(chrome, html_path, LONG_WIDTH)
    if not height:
        print("[md2share] 未能测出页面高度，已保留长图版 HTML，请手动整页截图。",
              file=sys.stderr)
        return html_path, None

    height = min(height + 4, 20000)   # 兜底：超长文档不超过 20000px
    if height >= 20000:
        print("[md2share] 文档太长，长图已按 20000px 截断。建议拆分后分段出图。",
              file=sys.stderr)
    png_path = (base_output.with_suffix('.long.png') if base_output
                else md_path.with_suffix('.long.png'))
    ok = capture_png(chrome, html_path, png_path, LONG_WIDTH, height, PNG_SCALE)
    if not ok:
        print("[md2share] 截图未成功，已保留长图版 HTML。", file=sys.stderr)
        return html_path, None
    return html_path, png_path


def parse_cli(argv):
    """解析命令行参数。格式: md2share.py <md> [output] [--embed-local-images=auto]

    --embed-local-images=all 已弃用（v1.5.0 起内嵌始终沙箱在 .md 目录内）；
    传入 all 时按 auto 处理并打印弃用提示，保证旧调用不报错。
    """
    global EMBED_LOCAL_IMAGES, SINCE, LONG_IMAGE, LONG_WIDTH, PNG_SCALE, LONG_KEEP_ONLY_HTML
    positional = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == '--long-image' or a.startswith('--long-image='):
            LONG_IMAGE = True
            if '=' in a:
                val = a.split('=', 1)[1].strip()
                if val.isdigit() and 480 <= int(val) <= 1600:
                    LONG_WIDTH = int(val)
                else:
                    print("[md2share] --long-image 的宽度需在 480~1600 之间", file=sys.stderr)
                    sys.exit(1)
        elif a == '--png-scale' or a.startswith('--png-scale='):
            if '=' in a:
                val = a.split('=', 1)[1]
            elif i + 1 < len(argv):
                i += 1
                val = argv[i]
            else:
                print(USAGE)
                sys.exit(1)
            if val not in ('1', '2', '3'):
                print("[md2share] --png-scale 只支持 1 / 2 / 3", file=sys.stderr)
                sys.exit(1)
            PNG_SCALE = int(val)
        elif a == '--long-html-only':
            LONG_KEEP_ONLY_HTML = True
        elif a == '--since' or a.startswith('--since='):
            if '=' in a:
                val = a.split('=', 1)[1]
            elif i + 1 < len(argv):
                i += 1
                val = argv[i]
            else:
                print(USAGE)
                sys.exit(1)
            SINCE = parse_since(val)
            if SINCE is None:
                sys.exit(1)
        elif a == '--embed-local-images' or a.startswith('--embed-local-images='):
            if '=' in a:
                val = a.split('=', 1)[1]
            elif i + 1 < len(argv):
                i += 1
                val = argv[i]
            else:
                print(USAGE)
                sys.exit(1)
            if val not in ('auto', 'all'):
                print(USAGE)
                sys.exit(1)
            if val == 'all':
                print("[md2share] --embed-local-images=all 已弃用（v1.5.0）："
                      "图片内嵌始终限制在 .md 文件所在目录及子目录", file=sys.stderr)
                val = 'auto'
            EMBED_LOCAL_IMAGES = val
        elif a.startswith('-'):
            print(f"未知选项: {a}")
            print(USAGE)
            sys.exit(1)
        else:
            positional.append(a)
        i += 1
    return positional


def convert_one(md_path, output_path):
    """把单个 .md 渲染成 .html 并写入。长图模式下改走长图出口。"""
    if LONG_IMAGE:
        html_path, png_path = convert_to_long_image(md_path, output_path)
        return [p for p in (png_path, html_path) if p]
    md_text = md_path.read_text(encoding='utf-8')
    blocks, footnotes = parse_md(md_text)
    # 正文自带 h1 时不再注入文件名标题，避免双标题
    has_h1 = any(b['type'] == 'h' and b['level'] == 1 for b in blocks)
    title = None if has_h1 else md_path.stem
    content = render_html(blocks, title=title, base_dir=md_path.parent,
                          footnotes=footnotes)
    html_doc = build_page(content, title=md_path.stem)
    output_path.write_text(html_doc, encoding='utf-8')
    return [output_path]


def main():
    positional = parse_cli(sys.argv[1:])
    if len(positional) < 1:
        print(USAGE)
        sys.exit(1)

    src = Path(positional[0])

    # 批量模式：输入是目录 → 转换该目录下的 .md（只扫一层，不递归）。
    # 时间过滤用文件自身的 mtime，不写任何状态文件，输出默认与源文件同目录。
    if src.is_dir():
        if SINCE is not None and len(positional) > 1:
            print("[md2share] 批量模式下第二个参数是输出目录，--since 仅用于筛选源文件",
                  file=sys.stderr)
        out_dir = Path(positional[1]) if len(positional) > 1 else None
        targets = sorted(p for p in src.glob('*.md') if p.is_file())
        if SINCE is not None:
            targets = [p for p in targets
                       if datetime.fromtimestamp(p.stat().st_mtime) >= SINCE]
        if not targets:
            scope = f"（--since 过滤后为空）" if SINCE is not None else ""
            print(f"没有需要转换的 .md：{src}{scope}")
            return
        if out_dir is not None:
            out_dir.mkdir(parents=True, exist_ok=True)
        written = []
        for p in targets:
            dest = (out_dir / (p.stem + '.html')) if out_dir else p.with_suffix('.html')
            written.extend(convert_one(p, dest))
        label = "长图" if LONG_IMAGE else "文件"
        print(f"✅ 批量完成：{len(targets)} 个源文件 → {len(written)} 个{label}")
        for w in written:
            print(f"   - {w}")
        return

    if not src.exists():
        print(f"找不到: {src}")
        sys.exit(1)

    output_path = Path(positional[1]) if len(positional) > 1 else src.with_suffix('.html')
    written = convert_one(src, output_path)
    if LONG_IMAGE:
        if len(written) > 1 and written[0].suffix == '.png':
            print(f"✅ 长图已生成: {written[0]}（{LONG_WIDTH * PNG_SCALE}px 宽）")
            print(f"   兜底 HTML: {written[1]}")
        else:
            print(f"✅ 长图版 HTML 已生成: {written[0]}")
    else:
        print(f"✅ 已生成: {output_path}")

if __name__ == '__main__':
    main()
