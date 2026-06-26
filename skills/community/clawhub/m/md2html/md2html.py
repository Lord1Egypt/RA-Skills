#!/usr/bin/env python3
"""
Markdown / HTML 互转及 PDF 技能 for OpenClaw.
支持：Markdown → HTML、Markdown → PDF、HTML → Markdown；从文件或传入内容。
"""

import base64
import json
import os
import sys
from io import BytesIO
from typing import Any, Tuple, Optional


def _get_content(req: dict) -> Tuple[str, Optional[str]]:
    """
    从 path 或 content 获取文本。返回 (content, error_message)。

    为避免被恶意 Agent 利用读取任意系统文件，这里对 path 做了简单限制：
    - 只允许相对路径（不允许绝对路径、盘符、.. 等）
    - 仅允许常见文本扩展名：.md/.markdown/.txt/.html/.htm
    """
    path = req.get("path")
    content = req.get("content")

    if path:
        raw_path = str(path).strip()
        # 禁止绝对路径、盘符以及路径穿越
        if os.path.isabs(raw_path) or ":" in raw_path or ".." in raw_path:
            return "", "Path not allowed. Please use a relative path under the project (no '..', no drive letters)."

        allowed_ext = (".md", ".markdown", ".txt", ".html", ".htm")
        _, ext = os.path.splitext(raw_path)
        if ext.lower() not in allowed_ext:
            return "", f"Unsupported extension: {ext}. Allowed: {', '.join(allowed_ext)}"

        safe_path = os.path.join(os.getcwd(), raw_path)
        if not os.path.isfile(safe_path):
            return "", f"File not found: {raw_path}"
        try:
            with open(safe_path, "r", encoding="utf-8") as f:
                return f.read(), None
        except Exception as e:
            return "", str(e)

    if content is not None:
        return str(content), None

    return "", "Either 'path' or 'content' is required"


def _html_document(body: str, title: str = "Document") -> str:
    """包装为完整 HTML 文档。"""
    return (
        "<!DOCTYPE html>\n"
        "<html lang=\"zh-CN\">\n"
        "<head>\n"
        "  <meta charset=\"UTF-8\">\n"
        f"  <title>{title}</title>\n"
        "  <style>\n"
        "    body { font-family: system-ui, sans-serif; line-height: 1.6; max-width: 720px; margin: 1em auto; padding: 0 1em; }\n"
        "    pre { background: #f5f5f5; padding: 0.75em; overflow-x: auto; }\n"
        "    code { background: #f5f5f5; padding: 0.2em 0.4em; }\n"
        "    table { border-collapse: collapse; }\n"
        "    th, td { border: 1px solid #ddd; padding: 0.4em 0.6em; }\n"
        "  </style>\n"
        "</head>\n<body>\n"
        f"{body}\n"
        "</body>\n</html>"
    )


def md_to_html(content: str, standalone: bool = True, title: str = "Document") -> str:
    """Markdown 转 HTML。"""
    try:
        import markdown
    except ImportError:
        return {"error": "missing_dependency", "message": "Install: pip install markdown"}
    html_body = markdown.markdown(
        content,
        extensions=["extra", "codehilite", "tables"],
        extension_configs={"codehilite": {"css_class": "highlight"}},
    )
    if standalone:
        return _html_document(html_body, title=title)
    return html_body


def html_to_pdf(html_str: str) -> bytes | dict:
    """HTML 转 PDF，返回 PDF 字节或错误 dict。"""
    try:
        from xhtml2pdf import pisa
    except ImportError:
        return {
            "error": "missing_dependency",
            "message": "Install: pip install xhtml2pdf",
        }
    out = BytesIO()
    try:
        pisa.CreatePDF(html_str.encode("utf-8"), dest=out, encoding="utf-8")
    except Exception as e:
        return {"error": "pdf_error", "message": str(e)}
    pdf_bytes = out.getvalue()
    if len(pdf_bytes) == 0:
        return {"error": "pdf_error", "message": "Generated PDF is empty"}
    return pdf_bytes


def cmd_html(req: dict) -> Any:
    """转为 HTML。请求 JSON: {"path": "a.md"} 或 {"content": "# Hello"}，可选 "title"。"""
    content, err = _get_content(req)
    if err:
        return {"error": "input_error", "message": err}
    title = (req.get("title") or "Document").strip() or "Document"
    html = md_to_html(content, standalone=True, title=title)
    if isinstance(html, dict):
        return html
    return {"html": html}


def cmd_pdf(req: dict) -> Any:
    """转为 PDF。请求 JSON: {"path": "a.md"} 或 {"content": "# Hello"}，可选 "title"。返回 pdf_base64。"""
    content, err = _get_content(req)
    if err:
        return {"error": "input_error", "message": err}
    title = (req.get("title") or "Document").strip() or "Document"
    html = md_to_html(content, standalone=True, title=title)
    if isinstance(html, dict):
        return html
    result = html_to_pdf(html)
    if isinstance(result, dict):
        return result
    return {"pdf_base64": base64.b64encode(result).decode("ascii")}


def html_to_md(html_str: str) -> str | dict:
    """HTML 转 Markdown。"""
    try:
        import html2text
    except ImportError:
        return {
            "error": "missing_dependency",
            "message": "Install: pip install html2text",
        }
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.body_width = 0
    return h.handle(html_str)


def cmd_html2md(req: dict) -> Any:
    """HTML 转 Markdown。请求 JSON: {"path": "a.html"} 或 {"content": "<p>...</p>"}。"""
    content, err = _get_content(req)
    if err:
        return {"error": "input_error", "message": err}
    result = html_to_md(content)
    if isinstance(result, dict):
        return result
    return {"markdown": result}


def _read_json_arg() -> dict:
    if len(sys.argv) < 3 or not sys.argv[2].strip():
        return {}
    raw = sys.argv[2]
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}", file=sys.stderr)
        sys.exit(1)
    if not isinstance(obj, dict):
        print("Error: JSON body must be an object.", file=sys.stderr)
        sys.exit(1)
    return obj


def main():
    if len(sys.argv) < 2:
        print(
            "Usage:\n"
            "  md2html.py html '{\"path\":\"README.md\"}'           # Markdown → HTML\n"
            "  md2html.py pdf '{\"path\":\"README.md\"}'            # Markdown → PDF（返回 base64）\n"
            "  md2html.py html2md '{\"path\":\"page.html\"}'        # HTML → Markdown\n"
            "  md2html.py html2md '{\"content\":\"<p>Hi</p>\"}'     # HTML 内容 → Markdown",
            file=sys.stderr,
        )
        sys.exit(1)

    cmd = sys.argv[1].strip().lower()
    req = _read_json_arg()

    if cmd == "html":
        result = cmd_html(req)
    elif cmd == "pdf":
        result = cmd_pdf(req)
    elif cmd == "html2md":
        result = cmd_html2md(req)
    else:
        print(f"Error: unknown command '{cmd}'", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
