from __future__ import annotations

from pathlib import Path

from html.parser import HTMLParser
from urllib.request import urlopen

from ..core.deps import require_bin, which
from ..core.exec import ExternalCommandError, run_cmd


def html_to_pdf(
    source: str,
    output_path: Path,
    *,
    margin_top: str = "10mm",
    margin_bottom: str = "10mm",
    margin_left: str = "10mm",
    margin_right: str = "10mm",
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    wkhtml = which("wkhtmltopdf")
    if wkhtml:
        cmd = [
            wkhtml,
            "--margin-top",
            margin_top,
            "--margin-bottom",
            margin_bottom,
            "--margin-left",
            margin_left,
            "--margin-right",
            margin_right,
            source,
            str(output_path),
        ]
        try:
            run_cmd(cmd)
            return
        except ExternalCommandError:
            _fallback_html_to_pdf(source, output_path)
            return

    chrome = which("google-chrome") or which("chromium") or which("chrome")
    if not chrome:
        raise RuntimeError("Install wkhtmltopdf or Chrome/Chromium for HTML to PDF")

    src = source
    source_path = Path(source)
    if source_path.exists():
        src = source_path.resolve().as_uri()

    cmd = [
        chrome,
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--no-first-run",
        "--disable-extensions",
        f"--print-to-pdf={output_path}",
        src,
    ]
    try:
        run_cmd(cmd)
    except ExternalCommandError:
        _fallback_html_to_pdf(source, output_path)


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        text = data.strip()
        if text:
            self.parts.append(text)


def _fallback_html_to_pdf(source: str, output_path: Path) -> None:
    html = _load_html(source)
    parser = _TextExtractor()
    parser.feed(html)
    text = "\\n".join(parser.parts)
    _text_to_pdf(text, output_path)


def _load_html(source: str) -> str:
    source_path = Path(source)
    if source_path.exists():
        return source_path.read_text(encoding="utf-8")
    if source.startswith("http://") or source.startswith("https://"):
        with urlopen(source) as resp:
            return resp.read().decode("utf-8", errors="ignore")
    return source


def _text_to_pdf(text: str, output_path: Path) -> None:
    from reportlab.pdfgen import canvas

    output_path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(output_path))
    y = 800
    for line in text.splitlines():
        if y < 40:
            c.showPage()
            y = 800
        c.setFont("Helvetica", 11)
        c.drawString(40, y, line[:120])
        y -= 14
    c.save()
