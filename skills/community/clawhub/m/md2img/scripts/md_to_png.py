#!/usr/bin/env python3
"""
Render Markdown into a single PNG using local code:
Markdown -> HTML -> headless Chromium screenshot (fullPage=True).

This intentionally does NOT depend on markdown-exporter.
"""

from __future__ import annotations

import argparse
import base64
import mimetypes
import re
import sys
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen


def _strip_wrapped_fence(md: str) -> str:
    """
    If the whole Markdown is wrapped by a single fenced code block, remove the wrapper.
    Example:
    ```markdown
    # hello
    ```
    """
    s = md.strip()
    m = re.match(r"^```[a-zA-Z0-9_-]*\s*\n(.*)\n```$", s, flags=re.DOTALL)
    return m.group(1).strip() if m else md


def _sanitize_html_fragment(html_fragment: str) -> str:
    """
    Sanitize the HTML fragment generated from Markdown before screenshotting.

    We prefer `bleach` for correctness. If it's not installed, we fall back to a
    minimal regex-based sanitizer (less safe).
    """

    # Recommended path: use bleach.
    try:
        import bleach  # type: ignore

        allowed_tags = [
            "p",
            "pre",
            "code",
            "ul",
            "ol",
            "li",
            "strong",
            "em",
            "blockquote",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "table",
            "thead",
            "tbody",
            "tr",
            "th",
            "td",
            "hr",
            "br",
            "a",
            "img",
            "div",
            "span",
        ]

        # Allow code highlighting markup from Pygments: spans/div with `class=...`
        allowed_attrs = {
            "a": ["href", "title"],
            "img": ["src", "alt", "title"],
            "div": ["class"],
            "span": ["class"],
            "code": ["class"],
            "pre": ["class"],
            "th": ["colspan", "rowspan"],
            "td": ["colspan", "rowspan"],
        }

        # Restrict URL schemes for safety.
        # Relative URLs (e.g. "./img.png") are typically allowed by bleach.
        cleaned = bleach.clean(
            html_fragment,
            tags=allowed_tags,
            attributes=allowed_attrs,
            protocols=["http", "https", "mailto"],
            strip=True,
        )
        return cleaned
    except ModuleNotFoundError:
        # Fallback: remove common dangerous patterns.
        # NOTE: this is best-effort and not a full HTML sanitizer.
        fragment = re.sub(
            r"(?is)<\s*(script|iframe|object|embed|form|input|button|textarea|select|style|link)\b[^>]*>.*?<\s*/\s*\1\s*>",
            "",
            html_fragment,
        )
        fragment = re.sub(
            r"(?is)<\s*(script|iframe|object|embed|form|input|button|textarea|select|style|link)\b[^>]*>",
            "",
            fragment,
        )
        # Remove inline event handlers like onerror/onload/onclick...
        fragment = re.sub(r"(?i)\s*on\w+\s*=\s*(\".*?\"|'.*?'|[^\s>]+)", "", fragment)
        # Remove javascript: URLs in href/src
        fragment = re.sub(
            r"(?i)\s*(href|src)\s*=\s*(\"|')\s*javascript:[^\"']*(\"|')",
            r"",
            fragment,
        )
        return fragment


def _inline_images_in_html(html_fragment: str, base_dir: Path, timeout_s: int = 10) -> str:
    """
    Inline <img src=...> into data:image/...;base64,... to make rendering self-contained.

    Supported src:
    - data:* (left as-is)
    - http(s)://... (download and inline)
    - filesystem paths: absolute (/a/b.png) or relative (relative to input markdown dir)

    On failure, keep the original src.
    """
    # Match <img ... src="..."> or <img ... src='...'> and capture the src value.
    img_src_re = re.compile(
        r'(<img\b[^>]*?\bsrc\s*=\s*)(["\'])(?P<src>[^"\']+)\2',
        flags=re.IGNORECASE,
    )

    def _resolve_local_path(src: str) -> Path | None:
        if src.startswith("/"):
            p = Path(src)
        else:
            p = (base_dir / src).resolve()
        return p

    def _guess_mime_from_path(p: Path) -> str:
        mime, _ = mimetypes.guess_type(str(p))
        return mime or "application/octet-stream"

    def _fetch_http(url: str) -> tuple[bytes, str]:
        req = Request(
            url,
            headers={
                # Some servers require UA.
                "User-Agent": "md2img/1.0",
                "Accept": "image/*,*/*;q=0.8",
            },
        )
        with urlopen(req, timeout=timeout_s) as resp:
            data = resp.read()
            content_type = resp.headers.get("Content-Type")
            if content_type:
                # e.g. "image/png; charset=binary" => keep only mime part
                mime = content_type.split(";", 1)[0].strip()
                if mime:
                    return data, mime
            # Fallback by URL extension
            ext = Path(url.split("?", 1)[0].split("#", 1)[0]).suffix
            if ext:
                mime, _ = mimetypes.guess_type(ext)
                if mime:
                    return data, mime
            return data, "application/octet-stream"

    def _inline_src(src: str) -> str | None:
        if src.startswith("data:"):
            return src
        try:
            if src.startswith("http://") or src.startswith("https://"):
                data, mime = _fetch_http(src)
            else:
                p = _resolve_local_path(src)
                if p is None or not p.exists() or not p.is_file():
                    return None
                data = p.read_bytes()
                mime = _guess_mime_from_path(p)
            b64 = base64.b64encode(data).decode("ascii")
            return f"data:{mime};base64,{b64}"
        except (URLError, OSError, ValueError):
            return None

    def _replace(match: re.Match[str]) -> str:
        prefix = match.group(1)
        quote = match.group(2)
        src = match.group("src")
        inlined = _inline_src(src)
        if not inlined:
            return match.group(0)  # keep original tag part
        return f"{prefix}{quote}{inlined}{quote}"

    return img_src_re.sub(_replace, html_fragment)


def _md_to_html(md: str, base_dir: Path, inline_images: bool) -> str:
    """
    Keep rendering simple and deterministic:
    - use python-markdown for Markdown -> HTML
    - wrap with basic CSS for typography
    """
    # Local import so the error message is more actionable.
    try:
        from markdown import markdown  # type: ignore
    except ModuleNotFoundError as e:
        raise RuntimeError(
            "缺少 Python 依赖 `markdown`。请先安装：\n"
            "  python3 -m pip install markdown"
        ) from e

    # Disable script tags to reduce risk when rendering arbitrary Markdown.
    # Note: this is not a full sanitizer; we still sanitize the final HTML later.
    md = re.sub(r"(?is)<\s*script[^>]*>.*?<\s*/\s*script\s*>", "", md)

    extensions = ["extra", "sane_lists"]
    # Enable syntax highlighting if pygments is present.
    try:
        import pygments  # type: ignore  # noqa: F401

        extensions.append("codehilite")
    except ModuleNotFoundError:
        pass

    body_html = markdown(md, extensions=extensions, output_format="html5")
    body_html = _sanitize_html_fragment(body_html)
    if inline_images:
        body_html = _inline_images_in_html(body_html, base_dir=base_dir)

    # Use system fonts with CJK fallbacks.
    css = """
    body {
      margin: 24px;
      padding-bottom: 40px;
      box-sizing: border-box;
      font-family: -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial,
        "PingFang SC", "Hiragino Sans GB", "Noto Sans CJK SC", "Microsoft YaHei", sans-serif;
      font-size: 16px;
      line-height: 1.6;
      background: #ffffff;
      color: #111827;
    }
    pre, code {
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
    }
    pre {
      background: #f9fafb;
      padding: 14px;
      border-radius: 10px;
      overflow: auto;
    }
    .codehilite {
      background: #f9fafb;
      padding: 14px;
      border-radius: 10px;
      overflow: auto;
    }
    .codehilite code {
      background: transparent;
    }
    img { max-width: 100%; }
    table { border-collapse: collapse; }
    th, td { border: 1px solid #e5e7eb; padding: 6px 10px; }

    /* Dark mode (best-effort): makes the output nicer on dark systems. */
    @media (prefers-color-scheme: dark) {
      body {
        background: #0f172a;
        color: #e5e7eb;
      }
      pre, .codehilite {
        background: #0b1220;
      }
      th, td { border-color: #334155; }
    }
    """

    html_doc = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <style>{css}</style>
</head>
<body>
{body_html}
</body>
</html>"""
    return html_doc


def _render_html_to_png(html_doc: str, output_png: Path, width: int) -> None:
    # Local import so dependency errors surface clearly.
    try:
        from playwright.sync_api import sync_playwright  # type: ignore
    except ModuleNotFoundError as e:
        raise RuntimeError(
            "缺少 Python 依赖 `playwright`。请先安装：\n"
            "  python3 -m pip install playwright\n"
            "并安装 Chromium：\n"
            "  python3 -m playwright install chromium"
        ) from e

    output_png.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = None
        try:
            browser = p.chromium.launch(
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                ]
            )
            page = browser.new_page(viewport={"width": width, "height": 800})
            page.set_content(html_doc, wait_until="load")

            # Wait for network (for images/fonts) and for fonts to be ready.
            try:
                page.wait_for_load_state("networkidle", timeout=5000)
            except Exception:
                pass
            try:
                # Wait for CSS Font Loading API (CJK fonts especially).
                page.evaluate("document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()")
            except Exception:
                pass
            # Small fallback delay to reduce screenshot timing artifacts.
            page.wait_for_timeout(150)

            # full_page=True returns ONE image representing the entire scroll height.
            page.screenshot(path=str(output_png), full_page=True)
        except Exception as e:
            msg = str(e).lower()
            if "executable" in msg and "chromium" in msg:
                raise RuntimeError(
                    "Playwright 找不到 Chromium 可执行文件。请运行：\n"
                    "  python3 -m playwright install chromium"
                ) from e
            raise
        finally:
            if browser is not None:
                browser.close()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Markdown input file path")
    parser.add_argument("--output", required=True, help="Output PNG file path")
    parser.add_argument(
        "--width",
        type=int,
        default=1200,
        help="(Deprecated) Viewport width used for rendering. Prefer --image-width.",
    )
    parser.add_argument(
        "--image-width",
        type=int,
        default=None,
        help="Output rendering width in pixels (sets browser viewport width).",
    )
    parser.add_argument("--strip-wrapper", action="store_true", help="Strip surrounding fenced wrapper if present")
    parser.add_argument(
        "--no-inline-images",
        action="store_true",
        help="Do not inline images; keep original <img src> (may require network and correct paths).",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Input markdown not found: {input_path}", file=sys.stderr)
        return 2

    output_png = Path(args.output)
    md = input_path.read_text(encoding="utf-8", errors="replace")
    if args.strip_wrapper:
        md = _strip_wrapped_fence(md)

    viewport_width = args.image_width if args.image_width is not None else args.width
    if viewport_width <= 0:
        print(f"Invalid --image-width/--width: {viewport_width}", file=sys.stderr)
        return 2

    html_doc = _md_to_html(
        md,
        base_dir=input_path.parent,
        inline_images=not args.no_inline_images,
    )
    _render_html_to_png(html_doc, output_png, width=viewport_width)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

