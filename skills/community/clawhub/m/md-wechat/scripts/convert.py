#!/usr/bin/env python3
"""
Markdown 到微信公众号格式转换脚本

基于 md 项目的核心转换逻辑实现
支持主题、字体、颜色、代码高亮等自定义配置
支持自动安装缺失的依赖
"""

import json
import re
import sys
import subprocess
from pathlib import Path
from typing import Optional


# ==================== 依赖管理 ====================

def install_package(package_name: str) -> bool:
    """
    自动安装 Python 包
    
    Args:
        package_name: 包名
        
    Returns:
        安装是否成功
    """
    try:
        print(f'[INFO] 正在安装依赖: {package_name}...')
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', package_name],
            capture_output=True,
            text=True,
            timeout=120
        )
        if result.returncode == 0:
            print(f'[OK] {package_name} 安装成功')
            return True
        else:
            print(f'[WARN] {package_name} 安装失败: {result.stderr}')
            return False
    except subprocess.TimeoutExpired:
        print(f'[WARN] {package_name} 安装超时')
        return False
    except Exception as e:
        print(f'[WARN] {package_name} 安装异常: {e}')
        return False


def check_and_import(module_name: str, package_name: str = None, auto_install: bool = True):
    """
    检查模块是否可用，如果不可用则尝试安装
    
    Args:
        module_name: 模块名（用于 import）
        package_name: 包名（用于 pip install，如果不同）
        auto_install: 是否自动安装
        
    Returns:
        模块对象或 None
    """
    if package_name is None:
        package_name = module_name
    
    try:
        # 尝试直接导入
        if '.' in module_name:
            parts = module_name.split('.')
            module = __import__(module_name)
            for part in parts[1:]:
                module = getattr(module, part)
            return module
        else:
            return __import__(module_name)
    except ImportError:
        if auto_install:
            if install_package(package_name):
                # 安装成功后再次尝试导入
                try:
                    if '.' in module_name:
                        parts = module_name.split('.')
                        module = __import__(module_name)
                        for part in parts[1:]:
                            module = getattr(module, part)
                        return module
                    else:
                        return __import__(module_name)
                except ImportError:
                    pass
        return None


def ensure_dependencies(features: list = None) -> dict:
    """
    确保所需的依赖已安装
    
    Args:
        features: 需要的功能列表，如 ['markdown', 'pygments', 'matplotlib']
        
    Returns:
        依赖状态字典
    """
    features = features or []
    status = {
        'markdown': False,
        'pygments': False,
        'matplotlib': False,
        'pillow': False
    }
    
    # markdown 库
    if 'markdown' in features or not features:
        try:
            import markdown
            from markdown.extensions import fenced_code, codehilite, toc, tables, footnotes
            status['markdown'] = True
        except ImportError:
            if 'markdown' in features:
                # 用户明确需要此功能，尝试安装
                if install_package('markdown'):
                    status['markdown'] = True
    
    # pygments 代码高亮
    if 'pygments' in features or not features:
        try:
            from pygments import highlight
            from pygments.lexers import get_lexer_by_name, guess_lexer
            from pygments.formatters import HtmlFormatter
            status['pygments'] = True
        except ImportError:
            if 'pygments' in features:
                if install_package('pygments'):
                    status['pygments'] = True
    
    # matplotlib 数学公式
    if 'matplotlib' in features:
        try:
            import matplotlib
            status['matplotlib'] = True
        except ImportError:
            if install_package('matplotlib'):
                status['matplotlib'] = True
    
    # pillow 图片处理
    if 'pillow' in features:
        try:
            import PIL
            status['pillow'] = True
        except ImportError:
            if install_package('pillow'):
                status['pillow'] = True
    
    return status


# 全局依赖状态
_DEPENDENCY_STATUS = None


def get_dependency_status() -> dict:
    """获取依赖状态（懒加载）"""
    global _DEPENDENCY_STATUS
    if _DEPENDENCY_STATUS is None:
        _DEPENDENCY_STATUS = ensure_dependencies()
    return _DEPENDENCY_STATUS


# 尝试导入可选依赖
try:
    import markdown
    from markdown.extensions import fenced_code, codehilite, toc, tables, footnotes
    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False

try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name, guess_lexer
    from pygments.formatters import HtmlFormatter
    HAS_PYGMENTS = True
except ImportError:
    HAS_PYGMENTS = False


# ==================== 主题 CSS 定义 ====================

BASE_CSS = '''
/**
 * MD 基础主题样式
 */
section, container {
  font-family: var(--md-font-family);
  font-size: var(--md-font-size);
  line-height: 1.75;
  text-align: left;
}

/* 去除第一个元素的 margin-top */
section > :first-child {
  margin-top: 0 !important;
}
'''

DEFAULT_THEME_CSS = '''
/**
 * MD 默认主题（经典主题）
 */

/* 标题 */
h1 {
  display: table;
  padding: 0 1em;
  border-bottom: 2px solid var(--md-primary-color);
  margin: 2em auto 1em;
  color: #333;
  font-size: 1.2em;
  font-weight: bold;
  text-align: center;
}

h2 {
  display: table;
  padding: 0 0.2em;
  margin: 2em auto 1em;
  color: #fff;
  background: var(--md-primary-color);
  font-size: 1.2em;
  font-weight: bold;
  text-align: center;
}

h3 {
  padding-left: 8px;
  border-left: 3px solid var(--md-primary-color);
  margin: 1.5em 8px 0.75em 0;
  color: #333;
  font-size: 1.1em;
  font-weight: bold;
}

h4 {
  margin: 1.5em 8px 0.5em;
  color: var(--md-primary-color);
  font-size: 1em;
  font-weight: bold;
}

h5, h6 {
  margin: 1.5em 8px 0.5em;
  color: var(--md-primary-color);
  font-size: 1em;
}

/* 段落 */
p {
  margin: 1.2em 8px;
  letter-spacing: 0.1em;
  color: #333;
}

/* 引用块 */
blockquote {
  font-style: normal;
  padding: 1em;
  border-left: 4px solid var(--md-primary-color);
  border-radius: 6px;
  color: #333;
  background: #f7f7f7;
  margin: 1em 8px;
}

blockquote p {
  margin: 0;
}

/* 代码块 */
pre {
  font-size: 90%;
  overflow-x: auto;
  border-radius: 8px;
  padding: 1em;
  margin: 10px 8px;
  background: #282c34;
  color: #abb2bf;
}

pre code {
  background: none;
  padding: 0;
  color: inherit;
}

/* 行内代码 */
code {
  font-size: 90%;
  color: #d14;
  background: rgba(27, 31, 35, 0.05);
  padding: 3px 5px;
  border-radius: 4px;
}

/* 删除线 */
s, del {
  text-decoration: line-through;
  color: #999;
}

/* 高亮 */
mark {
  background: var(--md-primary-color);
  color: #fff;
  padding: 2px 4px;
  border-radius: 2px;
}

/* 下划线 */
u {
  text-decoration: underline;
}

/* Ruby 注音 */
ruby {
  display: inline-ruby;
}
ruby rt {
  font-size: 0.65em;
  color: #666;
}

/* 图片 */
img {
  display: block;
  max-width: 100%;
  margin: 0.5em auto;
  border-radius: 4px;
}

figcaption {
  text-align: center;
  color: #888;
  font-size: 0.8em;
  margin-top: 0.5em;
}

/* 列表 */
ol, ul {
  padding-left: 1.5em;
  margin: 0.5em 8px;
  color: #333;
}

li {
  margin: 0.3em 0;
}

/* 分隔线 */
hr {
  border: none;
  border-top: 2px solid #eee;
  margin: 1.5em 0;
}

/* 强调 */
strong {
  color: var(--md-primary-color);
  font-weight: bold;
}

em {
  font-style: italic;
}

/* 链接 */
a {
  color: #576b95;
  text-decoration: none;
}

/* 表格 */
table {
  border-collapse: collapse;
  width: 100%;
  margin: 1em 0;
}

th, td {
  border: 1px solid #ddd;
  padding: 0.5em;
  text-align: left;
}

th {
  background: #f5f5f5;
  font-weight: bold;
}
'''

GRACE_THEME_CSS = '''
/**
 * MD 优雅主题 (@brzhang)
 */

h1 {
  padding: 0.5em 1em;
  border-bottom: 2px solid var(--md-primary-color);
  font-size: 1.4em;
}

h2 {
  padding: 0.3em 1em;
  border-radius: 8px;
  font-size: 1.3em;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h3 {
  padding-left: 12px;
  font-size: 1.2em;
  border-left: 4px solid var(--md-primary-color);
  border-bottom: 1px dashed var(--md-primary-color);
}

blockquote {
  font-style: italic;
  padding: 1em 1em 1em 2em;
  border-left: 4px solid var(--md-primary-color);
  border-radius: 6px;
  color: rgba(0, 0, 0, 0.6);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

pre {
  box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.05);
}

img {
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

hr {
  height: 1px;
  border: none;
  background: linear-gradient(to right, transparent, rgba(0,0,0,0.1), transparent);
}

table {
  border-collapse: separate;
  border-spacing: 0;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}
'''

SIMPLE_THEME_CSS = '''
/**
 * MD 简洁主题 (@okooo5km)
 */

h1 {
  padding: 0.5em 1em;
  font-size: 1.4em;
}

h2 {
  padding: 0.3em 1.2em;
  font-size: 1.3em;
  border-radius: 8px 24px 8px 24px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
}

h3 {
  padding-left: 12px;
  font-size: 1.2em;
  border-radius: 6px;
  line-height: 2.4;
  border-left: 4px solid var(--md-primary-color);
  background: rgba(0, 0, 0, 0.03);
}

blockquote {
  font-style: italic;
  padding: 1em 1em 1em 2em;
  color: rgba(0, 0, 0, 0.6);
  border: 1px solid rgba(0, 0, 0, 0.05);
}

pre {
  border: 1px solid rgba(0, 0, 0, 0.05);
}

img {
  border-radius: 8px;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

hr {
  height: 1px;
  border: none;
  background: linear-gradient(to right, transparent, rgba(0,0,0,0.1), transparent);
}
'''

THEME_MAP = {
    'default': DEFAULT_THEME_CSS,
    'grace': GRACE_THEME_CSS,
    'simple': SIMPLE_THEME_CSS,
}


# ==================== 代码高亮主题 ====================

CODE_THEMES = {
    'atom-one-dark': '''
pre { background: #282c34; color: #abb2bf; }
.hljs-keyword, .hljs-selector-tag { color: #c678dd; }
.hljs-string, .hljs-title { color: #98c379; }
.hljs-number { color: #d19a66; }
.hljs-function { color: #61afef; }
.hljs-comment { color: #5c6370; font-style: italic; }
.hljs-variable, .hljs-attr { color: #e06c75; }
''',
    'atom-one-light': '''
pre { background: #fafafa; color: #383a42; }
.hljs-keyword, .hljs-selector-tag { color: #a626a4; }
.hljs-string, .hljs-title { color: #50a14f; }
.hljs-number { color: #986801; }
.hljs-function { color: #4078f2; }
.hljs-comment { color: #a0a1a7; font-style: italic; }
.hljs-variable, .hljs-attr { color: #e45649; }
''',
    'github': '''
pre { background: #f6f8fa; color: #24292e; }
.hljs-keyword, .hljs-selector-tag { color: #d73a49; }
.hljs-string { color: #032f62; }
.hljs-number { color: #005cc5; }
.hljs-function { color: #6f42c1; }
.hljs-comment { color: #6a737d; }
.hljs-variable { color: #e36209; }
''',
    'monokai': '''
pre { background: #272822; color: #f8f8f2; }
.hljs-keyword, .hljs-selector-tag { color: #f92672; }
.hljs-string { color: #e6db74; }
.hljs-number { color: #ae81ff; }
.hljs-function { color: #a6e22e; }
.hljs-comment { color: #75715e; }
.hljs-variable { color: #fd971f; }
''',
}


# ==================== 核心转换类 ====================

class MDToWechatConverter:
    """Markdown 到微信公众号格式转换器"""
    
    def __init__(self, config: dict, auto_install: bool = True):
        self.config = config
        self.auto_install = auto_install
        self.theme_name = config.get('theme', {}).get('name', 'default')
        self.style = config.get('style', {})
        self.code_block = config.get('codeBlock', {})
        self.image = config.get('image', {})
        self.link = config.get('link', {})
        self.content = config.get('content', {})
        self.heading_styles = config.get('headingStyles', {})
        self.custom_css = config.get('customCSS', '')
        
    def _detect_required_features(self, text: str) -> list:
        """
        检测 Markdown 文本中需要的特殊功能
        
        Args:
            text: Markdown 文本
            
        Returns:
            需要的功能列表
        """
        features = []
        
        # 检测数学公式 ($$...$$ 或 $...$)
        if re.search(r'\$\$[\s\S]+?\$\$|\$[^\$\n]+?\$', text):
            features.append('matplotlib')
            print('[INFO] 检测到数学公式，需要 matplotlib 库')
        
        # 检测代码块（需要 pygments 做语法高亮）
        if re.search(r'^```[\w]*\n', text, re.MULTILINE):
            features.append('pygments')
        
        # 检测脚注（需要 markdown 库）
        if re.search(r'\[\^.+?\]', text):
            features.append('markdown')
        
        # 复杂的 Markdown 文档建议使用 markdown 库
        if re.search(r'^#{1,6}\s', text, re.MULTILINE) or \
           re.search(r'^\|.+?\|$', text, re.MULTILINE) or \
           re.search(r'^[-*+]\s', text, re.MULTILINE):
            features.append('markdown')
        
        return list(set(features))
        
    def convert(self, markdown_text: str) -> str:
        """
        转换 Markdown 为微信公众号格式的 HTML
        
        Args:
            markdown_text: Markdown 文本
            
        Returns:
            带内联样式的 HTML 字符串
        """
        global HAS_MARKDOWN, HAS_PYGMENTS
        
        # 检测需要的功能并确保依赖
        if self.auto_install:
            required_features = self._detect_required_features(markdown_text)
            if required_features:
                status = ensure_dependencies(required_features)
                # 更新全局状态
                HAS_MARKDOWN = status.get('markdown', False)
                HAS_PYGMENTS = status.get('pygments', False)
        
        # 1. 解析 Markdown 为 HTML
        html_content = self._parse_markdown(markdown_text)
        
        # 2. 生成 CSS 样式
        css = self._generate_css()
        
        # 3. 内联样式（微信公众号要求）
        html_with_styles = self._inline_styles(html_content, css)
        
        # 4. 包装为完整的 HTML 文档
        return self._wrap_html(html_with_styles)
    
    def _parse_markdown(self, text: str) -> str:
        """解析 Markdown 文本"""
        if HAS_MARKDOWN:
            return self._parse_with_markdown_lib(text)
        else:
            return self._parse_basic(text)
    
    def _parse_with_markdown_lib(self, text: str) -> str:
        """使用 Python-markdown 库解析"""
        extensions = [
            'fenced_code',
            'codehilite',
            'tables',
            'toc',
            'footnotes',
            'nl2br',
        ]
        
        md = markdown.Markdown(extensions=extensions)
        html = md.convert(text)
        
        # 处理 markdown 库不支持的扩展语法
        html = self._process_extended_syntax(html)
        
        # 处理代码块
        html = self._process_code_blocks(html)
        
        return html
    
    def _process_extended_syntax(self, html: str) -> str:
        """
        处理 markdown 库不支持的扩展语法
        
        包括：删除线、高亮、下划线、Ruby注音等
        注意：这些语法在代码块内不应该被处理
        """
        # 不处理代码块内的内容
        # 使用正则表达式分段处理，跳过 <pre> 和 <code> 标签内的内容
        
        def process_text_outside_code(match):
            """处理代码块外的文本"""
            return match.group(0)
        
        def process_non_code_content(text: str) -> str:
            """处理非代码区域的内容"""
            # 删除线 ~~text~~ - 确保不匹配代码块内的内容
            text = re.sub(r'~~([^~]+)~~', r'<s>\1</s>', text)
            
            # 高亮 ==text== - 确保不匹配代码块内的内容  
            text = re.sub(r'==([^=]+)==', r'<mark>\1</mark>', text)
            
            # 下划线 ++text++
            text = re.sub(r'\+\+([^\+]+)\+\+', r'<u>\1</u>', text)
            
            # Ruby 注音 [文字]{注音}
            text = re.sub(r'\[([^\]]+)\]\{([^}]+)\}', r'<ruby>\1<rt>\2</rt></ruby>', text)
            
            # Ruby 注音 [文字]^(注音)
            text = re.sub(r'\[([^\]]+)\]\^\(([^)]+)\)', r'<ruby>\1<rt>\2</rt></ruby>', text)
            
            return text
        
        # 分割 HTML，保护代码块内容
        parts = re.split(r'(<pre[^>]*>.*?</pre>|<code[^>]*>.*?</code>)', html, flags=re.DOTALL)
        
        result = []
        for part in parts:
            if part.startswith('<pre') or part.startswith('<code'):
                # 代码块内容不处理
                result.append(part)
            else:
                # 非代码块内容处理扩展语法
                result.append(process_non_code_content(part))
        
        return ''.join(result)
    
    def _parse_basic(self, text: str) -> str:
        """基础 Markdown 解析（无依赖）"""
        lines = text.split('\n')
        html_parts = []
        in_code_block = False
        code_content = []
        code_lang = ''
        in_table = False
        table_rows = []
        
        # 列表处理
        list_stack = []  # 栈存储列表状态: (type, indent, items)
        
        def close_all_lists():
            nonlocal list_stack
            result = []
            while list_stack:
                list_type, indent, items = list_stack.pop()
                result.insert(0, f'<{list_type}>\n' + '\n'.join(items) + f'\n</{list_type}>')
            list_stack = []
            return '\n'.join(result)
        
        def close_table():
            nonlocal in_table, table_rows
            if in_table and table_rows:
                table_html = '<table>\n'
                for i, row in enumerate(table_rows):
                    if i == 0:
                        table_html += '<thead><tr>'
                        for cell in row:
                            table_html += f'<th>{self._process_inline(cell)}</th>'
                        table_html += '</tr></thead>\n<tbody>\n'
                    else:
                        table_html += '<tr>'
                        for cell in row:
                            table_html += f'<td>{self._process_inline(cell)}</td>'
                        table_html += '</tr>\n'
                table_html += '</tbody>\n</table>'
                html_parts.append(table_html)
            in_table = False
            table_rows = []
        
        def get_list_indent(line):
            """获取列表缩进级别"""
            match = re.match(r'^(\s*)([-*+]|\d+\.)\s+', line)
            if match:
                return len(match.group(1)) // 2  # 每两个空格一个级别
            return 0
        
        def parse_list_line(line):
            """解析列表行，返回 (type, indent, text)"""
            # 无序列表
            ul_match = re.match(r'^(\s*)([-*+])\s+(.+)$', line)
            if ul_match:
                indent = len(ul_match.group(1)) // 2
                text = ul_match.group(3)
                return ('ul', indent, text)
            
            # 有序列表
            ol_match = re.match(r'^(\s*)(\d+)\.\s+(.+)$', line)
            if ol_match:
                indent = len(ol_match.group(1)) // 2
                text = ol_match.group(3)
                return ('ol', indent, text)
            
            return None
        
        for i, line in enumerate(lines):
            # 代码块开始/结束
            if line.startswith('```'):
                if not in_code_block:
                    # 关闭所有列表和表格
                    closed = close_all_lists()
                    if closed:
                        html_parts.append(closed)
                    close_table()
                    in_code_block = True
                    code_lang = line[3:].strip()
                    code_content = []
                else:
                    in_code_block = False
                    html_parts.append(self._render_code_block(
                        '\n'.join(code_content), code_lang
                    ))
                continue
            
            if in_code_block:
                code_content.append(line)
                continue
            
            # 标题
            if line.startswith('#'):
                closed = close_all_lists()
                if closed:
                    html_parts.append(closed)
                close_table()
                match = re.match(r'^(#{1,6})\s+(.+)$', line)
                if match:
                    level = len(match.group(1))
                    text = match.group(2)
                    html_parts.append(f'<h{level}>{text}</h{level}>')
                    continue
            
            # 多层引用
            if line.startswith('>'):
                closed = close_all_lists()
                if closed:
                    html_parts.append(closed)
                close_table()
                
                # 处理多层引用
                depth = 0
                temp_line = line
                while temp_line.startswith('>'):
                    depth += 1
                    temp_line = temp_line[1:]
                    if temp_line.startswith(' '):
                        temp_line = temp_line[1:]
                
                # 构建嵌套引用 - 正确的嵌套方式
                quote_content = self._process_inline(temp_line)
                for d in range(depth):
                    if d == 0:
                        quote_content = f'<blockquote><p>{quote_content}</p></blockquote>'
                    else:
                        # 内层引用不需要额外的 <p>
                        quote_content = f'<blockquote>{quote_content}</blockquote>'
                html_parts.append(quote_content)
                continue
            
            # 分隔线
            if re.match(r'^[-*_]{3,}$', line.strip()):
                closed = close_all_lists()
                if closed:
                    html_parts.append(closed)
                close_table()
                html_parts.append('<hr>')
                continue
            
            # 表格行
            if '|' in line and line.strip().startswith('|'):
                closed = close_all_lists()
                if closed:
                    html_parts.append(closed)
                if not in_table:
                    in_table = True
                    table_rows = []
                
                # 跳过分隔行
                if re.match(r'^\|[\s\-:|]+\|$', line.strip()):
                    continue
                
                # 解析表格单元格
                cells = [c.strip() for c in line.strip().split('|')[1:-1]]
                if cells:
                    table_rows.append(cells)
                continue
            elif in_table:
                close_table()
            
            # 列表处理
            list_info = parse_list_line(line)
            if list_info:
                list_type, indent, text = list_info
                
                # 检查是否需要关闭更深层级的列表
                while list_stack and list_stack[-1][1] >= indent:
                    closed_type, closed_indent, closed_items = list_stack.pop()
                    if closed_items:
                        closed_html = f'<{closed_type}>\n' + '\n'.join(closed_items) + f'\n</{closed_type}>'
                        if list_stack:
                            # 嵌套到父列表项中
                            list_stack[-1][2][-1] = list_stack[-1][2][-1].replace('</li>', '\n' + closed_html + '</li>')
                        else:
                            html_parts.append(closed_html)
                
                # 检查是否是同一层级继续
                if list_stack and list_stack[-1][1] == indent and list_stack[-1][0] == list_type:
                    list_stack[-1][2].append(f'<li>{self._process_inline(text)}</li>')
                else:
                    # 新层级
                    list_stack.append([list_type, indent, [f'<li>{self._process_inline(text)}</li>']])
                continue
            
            # 非列表行，关闭所有列表
            if line.strip() == '':
                closed = close_all_lists()
                if closed:
                    html_parts.append(closed)
                continue
            
            # 图片
            img_match = re.match(r'^!\[([^\]]*)\]\(([^)]+)\)', line)
            if img_match:
                closed = close_all_lists()
                if closed:
                    html_parts.append(closed)
                close_table()
                alt, src = img_match.groups()
                html_parts.append(
                    f'<figure><img src="{src}" alt="{alt}"/>'
                    f'<figcaption>{alt}</figcaption></figure>'
                )
                continue
            
            # 空行
            if not line.strip():
                continue
            
            # 普通段落
            closed = close_all_lists()
            if closed:
                html_parts.append(closed)
            close_table()
            html_parts.append(f'<p>{self._process_inline(line)}</p>')
        
        # 处理末尾未关闭的元素
        closed = close_all_lists()
        if closed:
            html_parts.append(closed)
        if in_table and table_rows:
            close_table()
        
        return '\n'.join(html_parts)
    
    def _process_inline(self, text: str) -> str:
        """处理行内元素"""
        # 粗体
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'__(.+?)__', r'<strong>\1</strong>', text)
        
        # 斜体
        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
        text = re.sub(r'_(.+?)_', r'<em>\1</em>', text)
        
        # 删除线
        text = re.sub(r'~~(.+?)~~', r'<s>\1</s>', text)
        
        # 高亮 ==text==
        text = re.sub(r'==(.+?)==', r'<mark>\1</mark>', text)
        
        # 下划线 ++text++
        text = re.sub(r'\+\+(.+?)\+\+', r'<u>\1</u>', text)
        
        # 波浪线 ~text~ (单波浪线，非删除线)
        # 注意：要区分 ~~删除线~~ 和 ~波浪线~
        
        # Ruby 注音 [文字]{注音}
        text = re.sub(r'\[([^\]]+)\]\{([^}]+)\}', r'<ruby>\1<rt>\2</rt></ruby>', text)
        text = re.sub(r'\[([^\]]+)\]\^\(([^)]+)\)', r'<ruby>\1<rt>\2</rt></ruby>', text)
        
        # 行内代码
        text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
        
        # 链接
        text = re.sub(
            r'\[([^\]]+)\]\(([^)]+)\)',
            r'<a href="\2">\1</a>',
            text
        )
        
        return text
    
    def _render_code_block(self, code: str, lang: str = '') -> str:
        """渲染代码块"""
        if HAS_PYGMENTS and lang:
            try:
                lexer = get_lexer_by_name(lang, stripall=True)
                formatter = HtmlFormatter(nowrap=True)
                highlighted = highlight(code, lexer, formatter)
                return f'<pre><code class="language-{lang}">{highlighted}</code></pre>'
            except:
                pass
        
        # 基础渲染
        escaped = code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        return f'<pre><code class="language-{lang}">{escaped}</code></pre>'
    
    def _process_code_blocks(self, html: str) -> str:
        """处理代码块，添加 Mac 风格装饰"""
        if not self.code_block.get('isMacStyle', True):
            return html
        
        # Mac 风格装饰 SVG
        mac_svg = '''
<svg xmlns="http://www.w3.org/2000/svg" width="45" height="13" style="position:absolute;top:0;right:0;padding:10px 14px 0;">
  <ellipse cx="50" cy="65" rx="50" ry="52" stroke="rgb(220,60,54)" stroke-width="2" fill="rgb(237,108,96)"/>
  <ellipse cx="225" cy="65" rx="50" ry="52" stroke="rgb(218,151,33)" stroke-width="2" fill="rgb(247,193,81)"/>
  <ellipse cx="400" cy="65" rx="50" ry="52" stroke="rgb(27,161,37)" stroke-width="2" fill="rgb(100,200,86)"/>
</svg>
'''
        
        # 为代码块添加装饰
        html = re.sub(
            r'<pre>',
            f'<pre style="position:relative;">{mac_svg}',
            html
        )
        
        return html
    
    def _generate_css(self) -> str:
        """生成 CSS 样式"""
        # 基础 CSS 变量
        primary_color = self.style.get('primaryColor', '#0F4C81')
        font_family = self.style.get(
            'fontFamily',
            '-apple-system-font, BlinkMacSystemFont, Helvetica Neue, PingFang SC, sans-serif'
        )
        font_size = self.style.get('fontSize', '16px')
        
        css_vars = f'''
:root {{
  --md-primary-color: {primary_color};
  --md-font-family: {font_family};
  --md-font-size: {font_size};
}}
'''
        
        # 基础样式
        css = BASE_CSS + '\n' + css_vars
        
        # 主题样式
        theme_css = THEME_MAP.get(self.theme_name, DEFAULT_THEME_CSS)
        css += '\n' + theme_css
        
        # 代码高亮主题
        code_theme = self.code_block.get('themeName', 'atom-one-dark')
        if code_theme in CODE_THEMES:
            css += '\n' + CODE_THEMES[code_theme]
        
        # 段落缩进
        if self.content.get('useIndent'):
            css += '\np { text-indent: 2em; }'
        
        # 两端对齐
        if self.content.get('useJustify'):
            css += '\np { text-align: justify; }'
        
        # 标题样式
        css += self._generate_heading_styles()
        
        # 自定义 CSS
        if self.custom_css:
            css += '\n' + self.custom_css
        
        return css
    
    def _generate_heading_styles(self) -> str:
        """生成标题样式"""
        css = ''
        styles = self.heading_styles or {}
        
        for level in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            style = styles.get(level, 'default')
            if style == 'color-only':
                css += f'\n{level} {{ color: var(--md-primary-color); background: transparent; }}'
            elif style == 'border-bottom':
                css += f'\n{level} {{ border-bottom: 2px solid var(--md-primary-color); color: var(--md-primary-color); }}'
            elif style == 'border-left':
                css += f'\n{level} {{ border-left: 4px solid var(--md-primary-color); color: var(--md-primary-color); padding-left: 10px; }}'
        
        return css
    
    def _inline_styles(self, html: str, css: str) -> str:
        """将 CSS 样式内联到 HTML 元素"""
        # 解析 CSS 规则
        rules = self._parse_css(css)
        
        # 应用样式到元素
        for selector, styles in rules.items():
            # 简单的样式内联（实际项目中可以使用 css_inline 等库）
            pass
        
        # 返回带 style 标签的 HTML
        return f'<style>{css}</style>\n{html}'
    
    def _parse_css(self, css: str) -> dict:
        """解析 CSS 为规则字典"""
        rules = {}
        pattern = r'([^{]+)\s*\{([^}]+)\}'
        
        for match in re.finditer(pattern, css, re.DOTALL):
            selector = match.group(1).strip()
            styles = match.group(2).strip()
            rules[selector] = styles
        
        return rules
    
    def _wrap_html(self, content: str) -> str:
        """包装为完整 HTML 文档"""
        primary_color = self.style.get('primaryColor', '#0F4C81')
        font_family = self.style.get(
            'fontFamily',
            '-apple-system-font, BlinkMacSystemFont, Helvetica Neue, PingFang SC, sans-serif'
        )
        font_size = self.style.get('fontSize', '16px')
        
        # 生成字数统计
        word_count_info = ''
        if self.content.get('countStatus'):
            # 简单的字数统计
            text_only = re.sub(r'<[^>]+>', '', content)
            words = len(text_only)
            minutes = max(1, words // 400)
            word_count_info = f'''
<blockquote style="border-left:4px solid {primary_color};padding:1em;background:#f7f7f7;">
<p style="margin:0;">字数 {words}，阅读大约需 {minutes} 分钟</p>
</blockquote>
'''
        
        return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>微信公众号文章</title>
</head>
<body style="margin:0;padding:20px;background:#fff;">
<section style="
  font-family: {font_family};
  font-size: {font_size};
  line-height: 1.75;
  max-width: 100%;
  color: #333;
">
{word_count_info}
{content}
</section>
</body>
</html>'''


# ==================== 命令行接口 ====================

def convert_file(
    input_path: str,
    output_path: Optional[str] = None,
    config_path: str = 'md-config.json',
    auto_install: bool = True
) -> str:
    """
    转换 Markdown 文件为微信公众号格式
    
    Args:
        input_path: 输入 Markdown 文件路径
        output_path: 输出 HTML 文件路径（可选）
        config_path: 配置文件路径
        auto_install: 是否自动安装缺失的依赖
        
    Returns:
        输出文件路径
    """
    input_file = Path(input_path)
    
    if not input_file.exists():
        raise FileNotFoundError(f'文件不存在: {input_path}')
    
    # 加载配置
    config = load_config(config_path)
    
    # 读取 Markdown
    with open(input_file, 'r', encoding='utf-8') as f:
        markdown_text = f.read()
    
    # 转换
    converter = MDToWechatConverter(config, auto_install=auto_install)
    html = converter.convert(markdown_text)
    
    # 确定输出路径
    if not output_path:
        output_file = input_file.with_name(f'{input_file.stem}-wechat.html')
    else:
        output_file = Path(output_path)
    
    # 写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f'[OK] 转换完成: {output_file}')
    return str(output_file)


def load_config(config_path: str = 'md-config.json') -> dict:
    """加载配置文件"""
    path = Path(config_path)
    
    if not path.exists():
        # 尝试初始化配置
        from init_config import init_config
        init_config(str(path.parent))
    
    with open(path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 过滤说明字段
    def filter_config(obj):
        if isinstance(obj, dict):
            return {k: filter_config(v) for k, v in obj.items() if not k.startswith('_')}
        return obj
    
    return filter_config(config)


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='将 Markdown 转换为微信公众号格式'
    )
    parser.add_argument(
        'input',
        help='输入 Markdown 文件路径'
    )
    parser.add_argument(
        '-o', '--output',
        help='输出 HTML 文件路径'
    )
    parser.add_argument(
        '-c', '--config',
        default='md-config.json',
        help='配置文件路径'
    )
    parser.add_argument(
        '--no-auto-install',
        action='store_true',
        help='禁用自动安装缺失的依赖'
    )
    
    args = parser.parse_args()
    
    auto_install = not args.no_auto_install
    
    try:
        output = convert_file(args.input, args.output, args.config, auto_install)
        print(f'输出文件: {output}')
    except Exception as e:
        print(f'[ERROR] 转换失败: {e}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
