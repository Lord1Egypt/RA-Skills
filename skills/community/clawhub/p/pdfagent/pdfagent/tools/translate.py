from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader
from reportlab.pdfgen import canvas

from ..core.llm import generate_text


def translate_pdf(
    input_path: Path,
    output_path: Path,
    *,
    source_lang: str | None,
    target_lang: str,
    provider: str,
    llm_cmd: str | None,
    model: str | None,
    text_out: Path | None = None,
) -> None:
    text = _extract_text(input_path)
    prompt = _build_prompt(text, source_lang, target_lang)
    translated = generate_text(provider=provider, prompt=prompt, cmd=llm_cmd, model=model)

    if text_out:
        text_out.parent.mkdir(parents=True, exist_ok=True)
        text_out.write_text(translated, encoding="utf-8")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    _text_to_pdf(translated, output_path)


def _extract_text(path: Path) -> str:
    reader = PdfReader(str(path))
    parts: list[str] = []
    for page in reader.pages:
        parts.append(page.extract_text() or "")
    return "\n\n".join(parts)


def _build_prompt(text: str, source_lang: str | None, target_lang: str) -> str:
    source = source_lang or "auto-detect"
    return (
        f"Translate the following text from {source} to {target_lang}. "
        "Preserve paragraph breaks. Return only the translated text.\n\n"
        f"{text}"
    )


def _text_to_pdf(text: str, output_path: Path) -> None:
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
