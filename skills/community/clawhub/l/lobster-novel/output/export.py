#!/usr/bin/env python3
"""
lobster-novel: Export manager — MD / TXT / HTML
"""
from pathlib import Path
from typing import Optional


class ExportManager:
    """Export novel to various formats."""

    @staticmethod
    def to_md(chapters_dir: Path, output: Path, title: str = "Novel"):
        """Concatenate all chapter files into a single markdown."""
        chapter_files = sorted(chapters_dir.glob("ch*.md"))
        if not chapter_files:
            raise FileNotFoundError(f"No chapter files found in {chapters_dir}")

        lines = [f"# {title}\n"]
        for cf in chapter_files:
            lines.append(cf.read_text(encoding="utf-8"))
            lines.append("\n\n---\n\n")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text("\n".join(lines), encoding="utf-8")
        return output

    @staticmethod
    def to_txt(chapters_dir: Path, output: Path, title: str = "Novel"):
        """Plain text: strip markdown headers, keep paragraph structure."""
        import re
        chapter_files = sorted(chapters_dir.glob("ch*.md"))
        if not chapter_files:
            raise FileNotFoundError(f"No chapter files found in {chapters_dir}")

        lines = [f"{title}\n{'=' * len(title)}\n"]
        for cf in chapter_files:
            text = cf.read_text(encoding="utf-8")
            # Strip markdown headers, keep content
            text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
            text = re.sub(r'[*_~`]', '', text)
            lines.append(text)
            lines.append("\n\n")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text("\n".join(lines), encoding="utf-8")
        return output

    @staticmethod
    def to_html(chapters_dir: Path, output: Path, title: str = "Novel", css: Optional[str] = None):
        """Simple self-contained HTML."""
        chapter_files = sorted(chapters_dir.glob("ch*.md"))
        if not chapter_files:
            raise FileNotFoundError(f"No chapter files found in {chapters_dir}")

        default_css = (
            "body{max-width:720px;margin:auto;padding:2em;font-family:serif;"
            "line-height:1.8;font-size:18px;color:#222}"
            "h1,h2,h3{text-align:center;margin:2em 0 1em}"
            "p{text-indent:2em;margin:0.5em 0}"
            "hr{border:none;border-top:1px solid #ccc;margin:3em 0}"
        )
        style = css or default_css

        body_parts = [f"<h1>{title}</h1>"]
        for cf in chapter_files:
            text = cf.read_text(encoding="utf-8")
            # Minimal MD→HTML: headers, paragraphs, breaks
            html = _md_to_html(text)
            body_parts.append(f"<hr>\n{html}")

        doc = f"""<!DOCTYPE html>
<html lang=zh-CN>
<head><meta charset=utf-8><title>{title}</title><style>{style}</style></head>
<body>{"".join(body_parts)}</body></html>"""
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(doc, encoding="utf-8")
        return output


def _md_to_html(text: str) -> str:
    """Minimal markdown-to-HTML conversion for novel text."""
    import re
    lines = text.split("\n")
    html_parts = []
    in_para = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if in_para:
                html_parts.append("</p>")
                in_para = False
            continue
        if stripped.startswith("# "):
            if in_para:
                html_parts.append("</p>")
                in_para = False
            html_parts.append(f"<h2>{stripped[2:]}</h2>")
        elif stripped.startswith("## "):
            if in_para:
                html_parts.append("</p>")
                in_para = False
            html_parts.append(f"<h3>{stripped[3:]}</h3>")
        elif stripped.startswith("---"):
            if in_para:
                html_parts.append("</p>")
                in_para = False
            html_parts.append("<hr>")
        else:
            if not in_para:
                html_parts.append("<p>")
                in_para = True
            html_parts.append(stripped)
    if in_para:
        html_parts.append("</p>")
    return "\n".join(html_parts)
