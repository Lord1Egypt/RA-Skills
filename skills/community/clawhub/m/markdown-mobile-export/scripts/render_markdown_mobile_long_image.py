from __future__ import annotations

import argparse
import importlib
import re
import shutil
import subprocess
import sys
from html import escape
from pathlib import Path


CSS = """
:root {
    --bg: #f7f1eb;
    --paper: #fffdfa;
    --paper-raised: #fff7f0;
    --ink: #2a1d19;
    --ink-strong: #1f1411;
    --muted: #6b5650;
    --muted-soft: #92766b;
    --line: #ead8cd;
    --line-strong: #dfc6b9;
    --accent: #d45a43;
    --accent-soft: rgba(212, 90, 67, 0.12);
    --accent-glow: rgba(212, 90, 67, 0.18);
    --quote: #fff7f1;
    --quote-ink: #6f534b;
    --code-bg: #2b2220;
    --code-bg-top: #352927;
    --code-ink: #f7eee7;
    --shadow: 0 28px 72px rgba(102, 63, 50, 0.12);
    --radius-xl: 36px;
    --radius-lg: 28px;
    --radius-md: 20px;
    --radius-sm: 12px;
    --space-8: 8px;
    --space-16: 16px;
    --space-24: 24px;
    --space-32: 32px;
    --space-40: 40px;
    --space-48: 48px;
}

* {
    box-sizing: border-box;
}

html {
    background:
        radial-gradient(circle at top left, rgba(212, 90, 67, 0.1), transparent 32%),
        radial-gradient(circle at top right, rgba(242, 177, 117, 0.14), transparent 28%),
        linear-gradient(180deg, #fcf7f2 0%, var(--bg) 100%);
}

body {
    margin: 0;
    color: var(--ink);
    font-family:
        "PingFang SC",
        "Hiragino Sans GB",
        "Noto Sans CJK SC",
        "Microsoft YaHei",
        sans-serif;
    line-height: 1.85;
    padding: var(--space-48) 0;
    -webkit-font-smoothing: antialiased;
    text-rendering: optimizeLegibility;
}

.page {
    width: 820px;
    margin: 0 auto;
    background: var(--paper);
    border: 1px solid rgba(212, 90, 67, 0.1);
    border-radius: var(--radius-xl);
    box-shadow: var(--shadow);
    overflow: hidden;
}

.page-inner {
    padding: var(--space-48) var(--space-40);
}

h1,
h2,
h3,
h4,
h5,
h6 {
    color: var(--ink-strong);
    line-height: 1.3;
    margin: 0 0 var(--space-16);
}

h1 {
    font-size: 46px;
    margin-bottom: var(--space-32);
    padding-bottom: var(--space-24);
    letter-spacing: -0.04em;
    font-weight: 800;
    position: relative;
}

h1::after {
    content: "";
    position: absolute;
    left: 0;
    bottom: 0;
    width: 88px;
    height: 4px;
    border-radius: 999px;
    background: linear-gradient(90deg, var(--accent) 0%, rgba(212, 90, 67, 0.2) 100%);
}

h2 {
    font-size: 34px;
    margin-top: var(--space-48);
    margin-bottom: var(--space-24);
    padding-left: var(--space-24);
    letter-spacing: -0.03em;
    font-weight: 780;
    position: relative;
}

h2::before {
    content: "";
    position: absolute;
    left: 0;
    top: 0.28em;
    width: 6px;
    height: 1.25em;
    border-radius: 999px;
    background: linear-gradient(180deg, var(--accent) 0%, rgba(212, 90, 67, 0.26) 100%);
    box-shadow: 0 0 0 8px var(--accent-soft);
}

h3 {
    font-size: 28px;
    margin-top: var(--space-32);
    margin-bottom: var(--space-16);
    letter-spacing: -0.02em;
    font-weight: 740;
}

h3::before {
    content: "";
    display: inline-block;
    width: 10px;
    height: 10px;
    margin-right: var(--space-16);
    border-radius: 50%;
    background: var(--accent);
    box-shadow: 0 0 0 6px rgba(212, 90, 67, 0.12);
    transform: translateY(-2px);
}

h4 {
    font-size: 21px;
    margin-top: var(--space-24);
    margin-bottom: var(--space-16);
    color: var(--muted-soft);
    font-weight: 720;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

p,
ul,
ol,
blockquote,
.table-wrap,
pre,
figure.content-figure {
    margin: 0 0 var(--space-24);
}

p,
li,
td,
th {
    font-size: 22px;
}

p {
    color: var(--ink);
    letter-spacing: 0.01em;
}

strong {
    color: var(--ink-strong);
    font-weight: 780;
}

em {
    color: var(--muted);
    font-style: italic;
    text-decoration-line: underline;
    text-decoration-color: rgba(212, 90, 67, 0.24);
    text-decoration-thickness: 0.08em;
    text-underline-offset: 0.14em;
}

hr {
    position: relative;
    border: 0;
    height: var(--space-32);
    margin: var(--space-40) 0;
    overflow: visible;
}

hr::before {
    content: "";
    position: absolute;
    left: 50%;
    top: 50%;
    width: 144px;
    height: 1px;
    transform: translate(-50%, -50%);
    background: linear-gradient(90deg, rgba(212, 90, 67, 0) 0%, rgba(212, 90, 67, 0.45) 50%, rgba(212, 90, 67, 0) 100%);
}

hr::after {
    content: "• • •";
    position: absolute;
    left: 50%;
    top: 50%;
    padding: 0 var(--space-16);
    transform: translate(-50%, -50%);
    background: var(--paper);
    color: var(--accent);
    font-size: 12px;
    letter-spacing: 0.45em;
}

blockquote {
    position: relative;
    padding: var(--space-24) var(--space-24) var(--space-24) var(--space-32);
    background: linear-gradient(135deg, rgba(255, 247, 241, 0.98) 0%, rgba(255, 240, 232, 0.92) 100%);
    border: 1px solid rgba(212, 90, 67, 0.12);
    border-radius: var(--radius-md);
    color: var(--quote-ink);
    overflow: hidden;
}

blockquote::before {
    content: "“";
    position: absolute;
    left: var(--space-16);
    top: var(--space-8);
    color: rgba(212, 90, 67, 0.22);
    font-size: 54px;
    font-style: italic;
    line-height: 1;
}

blockquote p,
blockquote li {
    color: var(--quote-ink);
    font-size: 20px;
}

blockquote > :last-child {
    margin-bottom: 0;
}

ul,
ol {
    padding-left: var(--space-32);
}

li {
    margin: 0;
    padding-left: var(--space-8);
}

li + li {
    margin-top: var(--space-8);
}

li > p:last-child {
    margin-bottom: 0;
}

li > strong:first-child {
    color: var(--ink-strong);
    font-weight: 800;
    letter-spacing: -0.01em;
}

ul > li::marker {
    color: var(--accent);
    font-size: 0.95em;
}

ol > li::marker {
    color: var(--accent);
    font-weight: 760;
}

ul ul,
ul ol,
ol ul,
ol ol {
    margin-top: var(--space-16);
    margin-bottom: var(--space-16);
    padding-left: var(--space-24);
    border-left: 2px solid rgba(212, 90, 67, 0.12);
}

a {
    color: var(--accent);
    text-decoration-line: underline;
    text-decoration-color: rgba(212, 90, 67, 0.28);
    text-decoration-thickness: 0.08em;
    text-underline-offset: 0.18em;
}

img.content-image {
    display: block;
    width: 100%;
    height: auto;
    margin: var(--space-24) 0 var(--space-32);
    border-radius: var(--radius-lg);
    box-shadow: 0 18px 48px rgba(88, 54, 44, 0.14);
    background: #f1e8e2;
}

figure.content-figure {
    margin-bottom: var(--space-32);
}

figure.content-figure img.content-image {
    margin: 0;
}

figcaption {
    margin-top: var(--space-16);
    color: var(--muted-soft);
    font-size: 18px;
    line-height: 1.7;
    text-align: center;
}

.table-wrap {
    overflow: hidden;
    border: 1px solid var(--line);
    border-radius: 22px;
    background: #fffdfa;
}

table {
    width: 100%;
    border-collapse: collapse;
    table-layout: fixed;
}

thead th {
    background: linear-gradient(180deg, rgba(212, 90, 67, 0.14) 0%, rgba(212, 90, 67, 0.08) 100%);
    color: #7a3428;
    font-weight: 800;
}

th,
td {
    border-bottom: 1px solid var(--line);
    padding: 18px 20px;
    text-align: left;
    vertical-align: top;
    word-break: break-word;
}

tr:nth-child(even) td {
    background: #fdf5ef;
}

tr:last-child td {
    border-bottom: 0;
}

code {
    font-family:
        "Maple Mono",
        "JetBrains Mono",
        "SFMono-Regular",
        "Consolas",
        monospace;
    font-size: 0.9em;
    background: rgba(82, 56, 48, 0.08);
    color: #754b40;
    padding: 0.18em 0.48em;
    border: 1px solid rgba(117, 75, 64, 0.12);
    border-radius: 8px;
}

pre {
    position: relative;
    padding: calc(var(--space-48) + var(--space-8)) var(--space-24) var(--space-24);
    overflow-x: auto;
    background: linear-gradient(180deg, var(--code-bg-top) 0%, var(--code-bg) 100%);
    color: var(--code-ink);
    border-radius: 24px;
    box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.05);
}

pre[data-language]::before {
    content: attr(data-language);
    position: absolute;
    top: var(--space-16);
    left: var(--space-24);
    padding: 4px 12px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.08);
    color: rgba(247, 238, 231, 0.84);
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

pre[data-language]::after {
    content: "";
    position: absolute;
    left: var(--space-24);
    right: var(--space-24);
    top: calc(var(--space-24) + var(--space-8));
    height: 1px;
    background: rgba(255, 255, 255, 0.12);
}

pre code {
    display: block;
    background: transparent;
    color: inherit;
    padding: 0;
    border: 0;
    border-radius: 0;
    white-space: pre-wrap;
    word-break: break-word;
    font-size: 20px;
    line-height: 1.75;
}

.page > .top-band {
    position: relative;
    height: 20px;
    background: linear-gradient(90deg, #ff7b63 0%, #f26f5d 48%, #ffb06c 100%);
}

.page > .top-band::after {
    content: "";
    position: absolute;
    inset: 0;
    background: repeating-linear-gradient(
        135deg,
        rgba(255, 255, 255, 0.28) 0 12px,
        rgba(255, 255, 255, 0) 12px 24px
    );
    opacity: 0.68;
}

.page > .bottom-band {
    position: relative;
    height: 24px;
    background: linear-gradient(180deg, rgba(244, 232, 224, 0.18) 0%, rgba(212, 90, 67, 0.08) 100%);
}

.page > .bottom-band::before {
    content: "";
    position: absolute;
    left: 50%;
    bottom: var(--space-8);
    width: 96px;
    height: 3px;
    transform: translateX(-50%);
    border-radius: 999px;
    background: linear-gradient(90deg, rgba(212, 90, 67, 0) 0%, rgba(212, 90, 67, 0.9) 50%, rgba(212, 90, 67, 0) 100%);
}

.page-inner > :first-child {
    margin-top: 0;
}

.page-inner > h1:first-child + blockquote {
    margin-top: 0;
}

mark {
    background: linear-gradient(180deg, rgba(255, 233, 124, 0.2) 0%, rgba(255, 233, 124, 0.56) 100%);
    color: inherit;
    padding: 0.08em 0.28em;
    border-radius: 6px;
}

del,
s {
    color: var(--muted-soft);
    text-decoration-color: rgba(146, 118, 107, 0.6);
    text-decoration-thickness: 0.1em;
}

@media (max-width: 860px) {
    body {
        padding: var(--space-24) 0 var(--space-40);
    }

    .page {
        width: min(100%, 100vw);
        border-radius: 0;
        border-left: 0;
        border-right: 0;
    }

    .page-inner {
        padding: var(--space-40) var(--space-24);
    }

    h1 {
        font-size: 40px;
        margin-bottom: var(--space-24);
        padding-bottom: var(--space-16);
    }

    h1::after {
        width: 72px;
    }

    h2 {
        font-size: 30px;
        margin-top: var(--space-40);
        padding-left: var(--space-16);
    }

    h2::before {
        width: 5px;
        box-shadow: 0 0 0 6px var(--accent-soft);
    }

    h3 {
        font-size: 25px;
    }

    h3::before {
        width: 8px;
        height: 8px;
        margin-right: 12px;
        box-shadow: 0 0 0 4px rgba(212, 90, 67, 0.12);
    }

    h4 {
        font-size: 19px;
    }

    p,
    li,
    td,
    th {
        font-size: 20px;
    }

    blockquote {
        padding: var(--space-24);
    }

    blockquote::before {
        left: 12px;
        top: 6px;
        font-size: 46px;
    }

    blockquote p,
    blockquote li,
    figcaption {
        font-size: 18px;
    }

    th,
    td {
        padding: var(--space-16);
    }

    pre {
        padding: calc(var(--space-40) + var(--space-16)) var(--space-16) var(--space-16);
        border-radius: var(--radius-md);
    }

    pre[data-language]::before {
        left: var(--space-16);
        top: 12px;
        font-size: 12px;
    }

    pre[data-language]::after {
        left: var(--space-16);
        right: var(--space-16);
        top: var(--space-40);
    }

    pre code {
        font-size: 18px;
    }

    hr::before {
        width: 112px;
    }
}
"""


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <style>{css}</style>
</head>
<body>
  <article class="page">
    <div class="top-band"></div>
    <div class="page-inner">
      {content}
    </div>
    <div class="bottom-band"></div>
  </article>
</body>
</html>
"""


def _run_install(package_name: str) -> None:
    ensure_commands = [
        [sys.executable, "-m", "ensurepip", "--upgrade"],
    ]
    install_commands = [
        [sys.executable, "-m", "pip", "install", package_name],
    ]
    uv_path = shutil.which("uv")
    if uv_path:
        install_commands.append([uv_path, "pip", "install", "--python", sys.executable, package_name])

    for ensure_command in ensure_commands:
        subprocess.run(ensure_command, check=False)

    last_error: Exception | None = None
    for command in install_commands:
        try:
            subprocess.run(command, check=True)
            return
        except Exception as exc:  # noqa: BLE001
            last_error = exc
    if last_error is not None:
        raise last_error


def ensure_markdown_it() -> None:
    try:
        importlib.import_module("markdown_it")
        return
    except ImportError:
        pass

    _run_install("markdown-it-py")
    importlib.import_module("markdown_it")


def build_markdown_renderer() -> MarkdownIt:
    ensure_markdown_it()
    from markdown_it import MarkdownIt

    return (
        MarkdownIt("commonmark", {"html": True, "linkify": True, "breaks": True})
        .enable("table")
        .enable("strikethrough")
    )


def _ensure_tag_class(tag_html: str, class_name: str) -> str:
    class_match = re.search(r'\bclass="([^"]*)"', tag_html, flags=re.IGNORECASE)
    if class_match is None:
        return tag_html[:-1] + f' class="{class_name}">'

    classes = class_match.group(1).split()
    if class_name in classes:
        return tag_html

    classes.append(class_name)
    updated_class_attr = f'class="{" ".join(classes)}"'
    return tag_html[: class_match.start()] + updated_class_attr + tag_html[class_match.end() :]


def _format_language_label(raw_language: str) -> str:
    normalized = raw_language.strip().lower()
    aliases = {
        "bash": "Bash",
        "c#": "C#",
        "cpp": "C++",
        "c++": "C++",
        "cs": "C#",
        "css": "CSS",
        "html": "HTML",
        "js": "JavaScript",
        "json": "JSON",
        "md": "Markdown",
        "py": "Python",
        "rb": "Ruby",
        "shell": "Shell",
        "sql": "SQL",
        "ts": "TypeScript",
        "tsx": "TSX",
        "xml": "XML",
        "yaml": "YAML",
        "yml": "YAML",
    }
    if normalized in aliases:
        return aliases[normalized]

    parts = [part for part in re.split(r"[-_]+", normalized) if part]
    if not parts:
        return "Code"
    return " ".join(part.upper() if len(part) <= 3 else part.capitalize() for part in parts)


def enhance_rendered_html(html: str) -> str:
    html = re.sub(
        r"<img\b[^>]*>",
        lambda match: _ensure_tag_class(match.group(0), "content-image"),
        html,
        flags=re.IGNORECASE,
    )
    html = re.sub(
        r"<p>\s*(?P<img><img\b[^>]*class=\"[^\"]*\bcontent-image\b[^\"]*\"[^>]*>)\s*</p>\s*<p>\s*<em>(?P<caption>.*?)</em>\s*</p>",
        lambda match: (
            '<figure class="content-figure">'
            f'{match.group("img")}'
            f'<figcaption>{match.group("caption").strip()}</figcaption>'
            "</figure>"
        ),
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    html = html.replace("<table>", '<div class="table-wrap"><table>')
    html = html.replace("</table>", "</table></div>")
    html = re.sub(
        r"<a\b(?P<attrs>[^>]*?)href=\"(?P<href>[^\"]+)\"(?P<tail>[^>]*)>",
        lambda match: (
            "<a"
            f'{match.group("attrs")}href="{match.group("href")}"'
            f'{match.group("tail")}'
            + (' target="_blank"' if "target=" not in match.group(0).lower() else "")
            + (' rel="noopener noreferrer"' if "rel=" not in match.group(0).lower() else "")
            + ">"
        ),
        html,
        flags=re.IGNORECASE,
    )
    html = re.sub(
        r"<pre(?P<pre_attrs>[^>]*)>\s*<code(?P<code_attrs>[^>]*)class=\"(?P<class_names>[^\"]*\blanguage-(?P<lang>[A-Za-z0-9_#+.-]+)[^\"]*)\"(?P<tail>[^>]*)>",
        lambda match: (
            f'<pre{match.group("pre_attrs")} data-language="{escape(_format_language_label(match.group("lang")), quote=True)}">'
            f'<code{match.group("code_attrs")}class="{match.group("class_names")}"{match.group("tail")}>'
        ),
        html,
        flags=re.IGNORECASE,
    )
    return html


def render_markdown_text(markdown_text: str, title_hint: str = "") -> str:
    renderer = build_markdown_renderer()
    rendered = renderer.render(markdown_text)
    title = infer_title(markdown_text, title_hint=title_hint)
    content_html = enhance_rendered_html(rendered)
    return HTML_TEMPLATE.format(title=title, css=CSS, content=content_html)


def infer_title(markdown_text: str, title_hint: str = "") -> str:
    for line in markdown_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return title_hint or "Markdown Long Image"


def write_rendered_html(markdown_path: Path, output_html: Path) -> Path:
    markdown_text = markdown_path.read_text(encoding="utf-8")
    html = render_markdown_text(markdown_text, title_hint=markdown_path.stem)
    output_html.parent.mkdir(parents=True, exist_ok=True)
    output_html.write_text(html, encoding="utf-8")
    return output_html


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render a Markdown file into mobile-friendly HTML for long-image export."
    )
    parser.add_argument("input", help="Path to the source Markdown file.")
    parser.add_argument("output", help="Path to the output HTML file.")
    args = parser.parse_args()

    write_rendered_html(Path(args.input).resolve(), Path(args.output).resolve())


if __name__ == "__main__":
    main()
