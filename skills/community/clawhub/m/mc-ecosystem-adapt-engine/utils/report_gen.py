"""报告生成器模块

V1.0.2 优化：报告渲染性能提升
- CSS/JS 静态文件缓存
- 模板预编译
- 批量生成支持
- 字符串拼接优化

生成两类报告：
1. HTML报告：用户阅读，含中文释义和建议
2. JSON数据：程序间传递，遵循统一返回结构
"""

import json
import html
import time
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

# 项目根目录
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_REPORTS_DIR = _PROJECT_ROOT / "output" / "reports"
_STATIC_DIR = _PROJECT_ROOT / "assets" / "report_static"

# === V1.0.2 新增: 静态资源缓存 ===
_css_cache: Optional[str] = None
_js_cache: Optional[str] = None
_template_cache: Dict[str, str] = {}


def _ensure_static_dir() -> Path:
    """确保静态资源目录存在"""
    _STATIC_DIR.mkdir(parents=True, exist_ok=True)
    return _STATIC_DIR


def _get_css_content() -> str:
    """V1.0.2 新增: 获取CSS内容（带缓存）"""
    global _css_cache
    if _css_cache is not None:
        return _css_cache

    # 尝试从静态文件加载
    css_file = _STATIC_DIR / "report_style.css"
    if css_file.exists():
        _css_cache = css_file.read_text(encoding="utf-8")
        return _css_cache

    # 使用内联样式作为后备
    _css_cache = ReportGenerator.HTML_STYLE
    return _css_cache


def _get_js_content() -> str:
    """V1.0.2 新增: 获取JS内容（带缓存）"""
    global _js_cache
    if _js_cache is not None:
        return _js_cache

    # 尝试从静态文件加载
    js_file = _STATIC_DIR / "report_script.js"
    if js_file.exists():
        _js_cache = js_file.read_text(encoding="utf-8")
        return _js_cache

    # 使用内联脚本作为后备
    _js_cache = ReportGenerator.HTML_SCRIPT
    return _js_cache


def export_static_files() -> Dict[str, str]:
    """V1.0.2 新增: 导出CSS/JS到静态文件（供首次使用）"""
    _ensure_static_dir()

    css_path = _STATIC_DIR / "report_style.css"
    js_path = _STATIC_DIR / "report_script.js"

    css_path.write_text(ReportGenerator.HTML_STYLE, encoding="utf-8")
    js_path.write_text(ReportGenerator.HTML_SCRIPT, encoding="utf-8")

    return {
        "css": str(css_path),
        "js": str(js_path),
    }


class ReportGenerator:
    """HTML/JSON报告生成器（V1.0.2 优化版）

    优化特性：
    - CSS/JS 静态文件缓存，避免每次重复写入
    - 模板字符串预编译
    - 批量生成支持
    - 性能统计
    """

    # === HTML样式（与V1开发指导文件风格保持一致）===
    HTML_STYLE = """
    <style>
        :root {
            --bg: #0d1117;
            --bg2: #161b22;
            --bg3: #1c2330;
            --bg4: #222a3a;
            --ink: #e6edf3;
            --muted: #8b949e;
            --rule: #30363d;
            --accent: #58a6ff;
            --accent2: #3fb950;
            --accent3: #d29922;
            --red: #f85149;
            --cyan: #39d2c0;
            --purple: #bc8cff;
            --font: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            --mono: 'JetBrains Mono', 'Cascadia Code', Consolas, monospace;
        }
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: var(--font);
            background: var(--bg);
            color: var(--ink);
            line-height: 1.75;
            padding: 2rem;
        }
        .container { max-width: 1100px; margin: 0 auto; }
        .header {
            background: linear-gradient(135deg, #161b22 0%, #0d1117 100%);
            border: 1px solid var(--rule);
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 1.5rem;
        }
        .header h1 {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--ink);
            display: flex;
            align-items: center;
            gap: 0.5rem;
            flex-wrap: wrap;
        }
        .header .tag {
            color: var(--accent2);
            font-size: 0.85rem;
            font-weight: 500;
        }
        .header .meta {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
            margin-top: 1rem;
        }
        .pill {
            display: inline-block;
            padding: 3px 12px;
            border-radius: 14px;
            font-size: 0.75rem;
            font-weight: 600;
            background: var(--bg3);
            border: 1px solid var(--rule);
            color: var(--muted);
        }
        .pill.blue { color: var(--accent); border-color: rgba(88,166,255,0.3); }
        .pill.green { color: var(--accent2); border-color: rgba(63,185,80,0.3); }
        .pill.red { color: var(--red); border-color: rgba(248,81,73,0.3); }
        .pill.yellow { color: var(--accent3); border-color: rgba(210,153,34,0.3); }

        h2 {
            font-size: 1.2rem;
            color: var(--ink);
            margin: 2rem 0 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid var(--rule);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        h2 .tag {
            font-size: 0.7rem;
            font-family: var(--mono);
            background: var(--bg3);
            padding: 2px 8px;
            border-radius: 4px;
            border: 1px solid var(--rule);
            color: var(--accent);
        }
        h3 { font-size: 1rem; color: var(--accent); margin: 1.5rem 0 0.5rem; }
        p { margin-bottom: 0.6rem; font-size: 0.9rem; }
        strong { color: var(--accent); font-weight: 600; }
        code {
            font-family: var(--mono);
            background: var(--bg3);
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 0.85em;
            color: var(--cyan);
        }
        a { color: var(--accent); text-decoration: none; }
        a:hover { text-decoration: underline; }

        /* === Status Banner === */
        .status-banner {
            padding: 1rem 1.5rem;
            border-radius: 8px;
            margin-bottom: 1rem;
            border-left: 4px solid;
            background: var(--bg2);
        }
        .status-banner.success { border-left-color: var(--accent2); }
        .status-banner.partial { border-left-color: var(--accent3); }
        .status-banner.error { border-left-color: var(--red); }
        .status-banner .sb-title { font-weight: 700; margin-bottom: 0.3rem; }
        .status-banner.success .sb-title { color: var(--accent2); }
        .status-banner.partial .sb-title { color: var(--accent3); }
        .status-banner.error .sb-title { color: var(--red); }

        /* === Tables === */
        .table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.85rem;
            margin: 0.8rem 0;
            border: 1px solid var(--rule);
            border-radius: 6px;
            overflow: hidden;
        }
        .table th {
            background: var(--bg3);
            color: var(--accent);
            font-weight: 600;
            text-align: left;
            padding: 0.5rem 0.7rem;
            border-bottom: 1px solid var(--rule);
        }
        .table td {
            padding: 0.4rem 0.7rem;
            border-bottom: 1px solid var(--rule);
            vertical-align: top;
        }
        .table td:first-child { font-family: var(--mono); color: var(--cyan); }
        .table tr:last-child td { border-bottom: none; }
        .table tr:hover td { background: var(--bg3); }

        /* === Code Block === */
        .code-block {
            background: var(--bg);
            border: 1px solid var(--rule);
            border-radius: 6px;
            padding: 0.8rem 1rem;
            margin: 0.6rem 0;
            font-family: var(--mono);
            font-size: 0.8rem;
            color: var(--ink);
            line-height: 1.6;
            overflow-x: auto;
            white-space: pre;
        }

        /* === Callout === */
        .callout {
            background: var(--bg2);
            border-left: 4px solid var(--accent);
            border-radius: 0 6px 6px 0;
            padding: 0.8rem 1.2rem;
            margin: 1rem 0;
        }
        .callout.green { border-left-color: var(--accent2); }
        .callout.yellow { border-left-color: var(--accent3); }
        .callout.red { border-left-color: var(--red); }
        .callout .callout-title { font-weight: 700; margin-bottom: 0.3rem; }
        .callout.green .callout-title { color: var(--accent2); }
        .callout.yellow .callout-title { color: var(--accent3); }
        .callout.red .callout-title { color: var(--red); }

        /* === Tree === */
        .tree {
            background: var(--bg2);
            border: 1px solid var(--rule);
            border-radius: 6px;
            padding: 1rem;
            margin: 0.8rem 0;
            font-family: var(--mono);
            font-size: 0.8rem;
            line-height: 1.7;
        }
        .tree-node { padding-left: 1.2rem; }
        .tree-toggle {
            cursor: pointer;
            user-select: none;
            color: var(--accent);
        }
        .tree-toggle::before { content: '▼ '; font-size: 0.7rem; }
        .tree-toggle.collapsed::before { content: '▶ '; }
        .tree-children { padding-left: 1rem; border-left: 1px solid var(--rule); margin-left: 4px;}
        .tree-children.hidden { display: none; }
        .tree-file { color: var(--ink); }
        .tree-dir { color: var(--accent); }
        .tree-desc { color: var(--muted); margin-left: 0.5rem; }

        /* === Footer === */
        .footer {
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid var(--rule);
            color: var(--muted);
            font-size: 0.75rem;
            text-align: center;
        }
    </style>
    """

    # === JavaScript交互 ===
    HTML_SCRIPT = """
    <script>
        function toggleNode(el) {
            const children = el.parentElement.querySelector('.tree-children');
            if (children) {
                children.classList.toggle('hidden');
                el.classList.toggle('collapsed');
            }
        }
        function expandAll() {
            document.querySelectorAll('.tree-children').forEach(el => el.classList.remove('hidden'));
            document.querySelectorAll('.tree-toggle').forEach(el => el.classList.remove('collapsed'));
        }
        function collapseAll() {
            document.querySelectorAll('.tree-children').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('.tree-toggle').forEach(el => el.classList.add('collapsed'));
        }
    </script>
    """

    def __init__(self, feature: str = "main", use_static: bool = True):
        """初始化报告生成器

        Args:
            feature: 功能模块名
            use_static: 是否使用静态文件缓存（V1.0.2新增）
        """
        self.feature = feature
        self.use_static = use_static
        _REPORTS_DIR.mkdir(parents=True, exist_ok=True)

        # V1.0.2 新增: 性能统计
        self._render_count = 0
        self._total_render_time = 0.0

        # V1.0.2 新增: 预编译模板
        self._precompile_templates()

    def _precompile_templates(self) -> None:
        """V1.0.2 新增: 预编译HTML模板"""
        css = _get_css_content() if self.use_static else self.HTML_STYLE
        js = _get_js_content() if self.use_static else self.HTML_SCRIPT

        # 预编译完整模板
        self._base_template = (
            '<!DOCTYPE html>\n'
            '<html lang="zh-CN">\n'
            '<head>\n'
            '<meta charset="UTF-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            '<title>{title}</title>\n'
            f'{css}\n'
            f'{js}\n'
            '</head>\n'
            '<body>\n'
            '<div class="container">\n'
            '    <div class="header">\n'
            '        <h1>{title_escaped} <span class="tag">{feature_escaped}</span></h1>\n'
            '        {meta_html}\n'
            '    </div>\n'
            '    {status_html}\n'
            '    {content}\n'
            '    <div class="footer">\n'
            '        由 MC全生态智能适配工程师 V1 生成 · {footer_time}\n'
            '    </div>\n'
            '</div>\n'
            '</body>\n'
            '</html>'
        )

    def _generate_filename(self, suffix: str, mod_name: str = "") -> str:
        """生成文件名

        Args:
            suffix: 文件后缀（如 .html, .json）
            mod_name: 模组名（可选）

        Returns:
            文件名，格式为 {功能}_{模组名}_{时间戳}{后缀}
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        mod_part = f"{mod_name}_" if mod_name else ""
        return f"{self.feature}_{mod_part}{timestamp}{suffix}"

    def generate_json(
        self,
        data: Dict[str, Any],
        mod_name: str = "",
        output_path: Union[str, Path] = None,
    ) -> Path:
        """生成JSON报告

        Args:
            data: 要序列化的数据
            mod_name: 模组名（用于文件名）
            output_path: 自定义输出路径

        Returns:
            输出文件路径
        """
        if output_path is None:
            output_path = _REPORTS_DIR / self._generate_filename(".json", mod_name)
        else:
            output_path = Path(output_path)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return output_path

    def generate_html(
        self,
        title: str,
        content: str,
        status: str = "success",
        meta: Dict[str, str] = None,
        mod_name: str = "",
        output_path: Union[str, Path] = None,
    ) -> Path:
        """生成HTML报告（V1.0.2 优化版）

        Args:
            title: 报告标题
            content: HTML主体内容（不含html/head/body标签）
            status: 状态 success/partial/error
            meta: 头部元信息（pill标签）
            mod_name: 模组名（用于文件名）
            output_path: 自定义输出路径

        Returns:
            输出文件路径
        """
        start_time = time.time()

        if output_path is None:
            output_path = _REPORTS_DIR / self._generate_filename(".html", mod_name)
        else:
            output_path = Path(output_path)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        # V1.0.2 优化: 使用列表拼接而非字符串拼接
        parts = []

        # 构建meta pills
        if meta:
            pills = []
            for k, v in meta.items():
                cls = "blue"
                if k.lower() in ("status",) and v.lower() in ("success", "ok"):
                    cls = "green"
                elif k.lower() in ("status",) and v.lower() in ("error", "fail"):
                    cls = "red"
                elif k.lower() in ("warning", "partial"):
                    cls = "yellow"
                pills.append(f'<span class="pill {cls}">{html.escape(str(k))}: {html.escape(str(v))}</span>')
            parts.append(f'<div class="meta">{"".join(pills)}</div>')
        else:
            parts.append("")

        # 状态banner
        status_cn = {
            "success": "成功",
            "partial": "部分成功",
            "error": "失败",
        }.get(status, status)
        parts.append(
            f'<div class="status-banner {status}">'
            f'<div class="sb-title">状态: {status_cn}</div>'
            f'</div>'
        )

        # 组装HTML
        meta_html = parts[0]
        status_html = parts[1]
        footer_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        html_doc = self._base_template.format(
            title=html.escape(title),
            title_escaped=html.escape(title),
            feature_escaped=html.escape(self.feature),
            meta_html=meta_html,
            status_html=status_html,
            content=content,
            footer_time=footer_time,
        )

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_doc)

        # V1.0.2 新增: 性能统计
        self._render_count += 1
        self._total_render_time += time.time() - start_time

        return output_path

    def render_full_html(
        self,
        title: str,
        body_html: str,
        timestamp: str = "",
    ) -> str:
        """渲染完整HTML文档（返回字符串，不写入文件）

        Args:
            title: 报告标题
            body_html: HTML主体内容
            timestamp: 时间戳字符串

        Returns:
            完整HTML文档字符串
        """
        ts = timestamp or datetime.now().strftime("%Y%m%d_%H%M%S")

        html_doc = self._base_template.format(
            title=html.escape(title),
            title_escaped=html.escape(title),
            feature_escaped=html.escape(self.feature),
            meta_html=f'<div class="meta"><span class="pill blue">时间: {ts}</span></div>',
            status_html="",
            content=body_html,
            footer_time=ts,
        )
        return html_doc

    def generate_batch_html(
        self,
        items: List[Dict[str, Any]],
        output_dir: Optional[Path] = None,
    ) -> List[Path]:
        """V1.0.2 新增: 批量生成HTML报告

        Args:
            items: 报告项列表 [{"title": ..., "content": ..., "status": ..., "meta": ...}]
            output_dir: 输出目录

        Returns:
            输出文件路径列表
        """
        if output_dir is None:
            output_dir = _REPORTS_DIR

        output_paths = []
        for item in items:
            path = self.generate_html(
                title=item.get("title", "Report"),
                content=item.get("content", ""),
                status=item.get("status", "success"),
                meta=item.get("meta"),
                mod_name=item.get("mod_name", ""),
                output_path=output_dir / self._generate_filename(".html", item.get("mod_name", "")),
            )
            output_paths.append(path)

        return output_paths

    def get_performance_stats(self) -> Dict[str, Any]:
        """V1.0.2 新增: 获取性能统计"""
        avg_time = self._total_render_time / self._render_count if self._render_count > 0 else 0
        return {
            "total_renders": self._render_count,
            "total_time_seconds": round(self._total_render_time, 3),
            "avg_time_seconds": round(avg_time, 4),
            "use_static": self.use_static,
        }

    # === HTML片段生成辅助方法 ===
    def render_table(
        self,
        headers: List[str],
        rows: List[List[Any]],
        first_col_mono: bool = True,
    ) -> str:
        """生成HTML表格

        Args:
            headers: 表头
            rows: 行数据
            first_col_mono: 第一列是否使用等宽字体

        Returns:
            HTML表格字符串
        """
        # V1.0.2 优化: 使用列表拼接
        head = "".join(f"<th>{html.escape(str(h))}</th>" for h in headers)
        body_rows = []
        for row in rows:
            cells = []
            for i, cell in enumerate(row):
                cls = ' class="mono"' if (i == 0 and first_col_mono) else ""
                cells.append(f"<td{cls}>{html.escape(str(cell))}</td>")
            body_rows.append("<tr>" + "".join(cells) + "</tr>")
        return (
            f'<table class="table"><thead><tr>{head}</tr></thead>'
            f'<tbody>{"".join(body_rows)}</tbody></table>'
        )

    def render_callout(
        self, title: str, content: str, level: str = "info"
    ) -> str:
        """生成callout提示框

        Args:
            title: 标题
            content: 内容（HTML字符串）
            level: 级别 info/green/yellow/red

        Returns:
            HTML字符串
        """
        cls = level if level in ("info", "green", "yellow", "red") else "info"
        return (
            f'<div class="callout {cls}">'
            f'<div class="callout-title">{html.escape(title)}</div>'
            f'{content}'
            f'</div>'
        )

    def render_code_block(self, content: str, language: str = "") -> str:
        """生成代码块"""
        return (
            f'<div class="code-block">{html.escape(content)}</div>'
        )

    def render_tree(self, tree_data: Dict, depth: int = 0, max_depth: int = 3) -> str:
        """递归生成树形结构HTML

        Args:
            tree_data: 树数据字典
            depth: 当前深度
            max_depth: 默认展开最大深度

        Returns:
            HTML字符串
        """
        if not tree_data:
            return ""

        name = tree_data.get("name", "")
        node_type = tree_data.get("type", "file")
        desc_cn = tree_data.get("desc_cn", "")
        children = tree_data.get("children", [])

        is_dir = node_type in ("dir", "root")
        cls = "tree-dir" if is_dir else "tree-file"

        display = name
        if tree_data.get("size"):
            display += f" ({tree_data['size']})"
        if tree_data.get("mixin_count"):
            display += f" [{tree_data['mixin_count']} mixins]"
        if tree_data.get("key_count"):
            display += f" [{tree_data['key_count']} keys]"

        desc_html = f'<span class="tree-desc"># {html.escape(desc_cn)}</span>' if desc_cn else ""

        if not children:
            return (
                f'<div class="tree-node"><span class="{cls}">'
                f'{html.escape(display)}</span>{desc_html}</div>'
            )

        collapsed = "collapsed" if depth >= max_depth else ""
        hidden = "hidden" if depth >= max_depth else ""

        children_html = "".join(
            self.render_tree(child, depth + 1, max_depth) for child in children
        )

        return (
            f'<div class="tree-node">'
            f'<span class="tree-toggle {collapsed}" onclick="toggleNode(this)">{html.escape(display)}</span>'
            f'{desc_html}'
            f'<div class="tree-children {hidden}">{children_html}</div>'
            f'</div>'
        )

    def render_section(self, title: str, content: str, tag: str = "") -> str:
        """生成章节

        Args:
            title: 章节标题
            content: 内容HTML
            tag: 可选标签

        Returns:
            HTML字符串
        """
        tag_html = f'<span class="tag">{html.escape(tag)}</span>' if tag else ""
        return f'<h2>{html.escape(title)} {tag_html}</h2>{content}'

    def render_list(self, items: List[str], ordered: bool = False) -> str:
        """生成列表

        Args:
            items: 列表项
            ordered: 是否有序列表

        Returns:
            HTML字符串
        """
        tag = "ol" if ordered else "ul"
        items_html = "".join(f"<li>{item}</li>" for item in items)
        return f'<{tag}>{items_html}</{tag}>'

    def render_warnings(self, warnings: List[str]) -> str:
        """渲染警告列表"""
        if not warnings:
            return ""
        items = "".join(f"<li>{html.escape(w)}</li>" for w in warnings)
        return (
            f'<div class="callout yellow"><div class="callout-title">⚠️ 警告</div>'
            f'<ul>{items}</ul></div>'
        )

    def render_errors(self, errors: List[str]) -> str:
        """渲染错误列表"""
        if not errors:
            return ""
        items = "".join(f"<li>{html.escape(e)}</li>" for e in errors)
        return (
            f'<div class="callout red"><div class="callout-title">❌ 错误</div>'
            f'<ul>{items}</ul></div>'
        )


def generate_unified_output(
    feature: str,
    status: str,
    input_summary: Dict,
    result: Dict,
    title: str,
    html_content: str,
    warnings: List[str] = None,
    errors: List[str] = None,
    meta: Dict[str, str] = None,
    mod_name: str = "",
) -> Dict[str, str]:
    """生成统一的JSON+HTML双格式输出

    Args:
        feature: 功能名
        status: 状态 success/partial/error
        input_summary: 输入摘要
        result: 功能特定数据
        title: HTML报告标题
        html_content: HTML主体内容
        warnings: 警告列表
        errors: 错误列表
        meta: HTML头部元信息
        mod_name: 模组名（用于文件名）

    Returns:
        输出文件路径字典 {"report": html路径, "data": json路径}
    """
    import sys
    _PROJECT_ROOT_STR = str(Path(__file__).resolve().parent.parent)
    if _PROJECT_ROOT_STR not in sys.path:
        sys.path.insert(0, _PROJECT_ROOT_STR)
    import config

    warnings = warnings or []
    errors = errors or []

    # 构造统一返回结构
    unified = config.build_result(
        feature=feature,
        status=status,
        input_summary=input_summary,
        result=result,
        warnings=warnings,
        errors=errors,
    )

    gen = ReportGenerator(feature=feature)

    # 生成JSON
    json_path = gen.generate_json(unified, mod_name=mod_name)

    # 生成HTML
    html_path = gen.generate_html(
        title=title,
        content=html_content,
        status=status,
        meta=meta,
        mod_name=mod_name,
    )

    unified["output_files"] = {
        "report": str(html_path),
        "data": str(json_path),
    }

    # 重新写入JSON，包含输出文件路径
    gen.generate_json(unified, mod_name=mod_name, output_path=json_path)

    return unified["output_files"]


def get_report_stats() -> Dict[str, Any]:
    """V1.0.2 新增: 获取报告系统统计"""
    return {
        "reports_dir": str(_REPORTS_DIR),
        "reports_dir_exists": _REPORTS_DIR.exists(),
        "static_dir": str(_STATIC_DIR),
        "static_dir_exists": _STATIC_DIR.exists(),
        "css_cached": _css_cache is not None,
        "js_cached": _js_cache is not None,
    }
