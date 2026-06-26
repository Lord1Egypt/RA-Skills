# pyright: reportMissingImports=false
import asyncio
import os
import tempfile
from pathlib import Path

import edge_tts

from constants import (
    BIN_FFMPEG,
    TTS_DEFAULT_RATE,
    TTS_DEFAULT_VOICE,
    TTS_DEFAULT_VOLUME,
    TTS_MAX_CHARS,
    PDF_EXTENSIONS,
    DOCX_EXTENSIONS,
)
from utils import (
    clean_text,
    ensure_output_dir,
    is_binary_available,
    resolve_path,
    run_command,
    truncate_text,
)


def _extract_text_for_tts(path: Path) -> str | dict:
    """Pull plain text from a PDF or DOCX for TTS input."""
    suffix = path.suffix.lower()
    if suffix in PDF_EXTENSIONS:
        try:
            import pypdf

            reader = pypdf.PdfReader(str(path))
            parts = [page.extract_text() or "" for page in reader.pages]
            return clean_text("\n".join(parts))
        except Exception as exc:
            return {"error": f"Could not read PDF for TTS: {exc}"}
    elif suffix in DOCX_EXTENSIONS:
        try:
            import docx

            doc = docx.Document(str(path))
            return clean_text("\n".join(p.text for p in doc.paragraphs))
        except Exception as exc:
            return {"error": f"Could not read DOCX for TTS: {exc}"}
    else:
        # Treat as plain text
        try:
            return path.read_text(errors="replace")
        except Exception as exc:
            return {"error": f"Could not read file: {exc}"}


async def _synthesise(
    text: str, voice: str, rate: str, volume: str, tmp_wav: str
) -> None:
    """Use edge-tts to synthesise text to a file."""
    communicate = edge_tts.Communicate(text, voice, rate=rate, volume=volume)
    await communicate.save(tmp_wav)


def tts_to_mp3(
    text: str | None,
    file_str: str | None,
    output_str: str,
    voice: str = TTS_DEFAULT_VOICE,
    rate: str = TTS_DEFAULT_RATE,
    volume: str = TTS_DEFAULT_VOLUME,
) -> dict:
    """Convert text or a document to an MP3 file via edge-tts + ffmpeg."""
    if not is_binary_available(BIN_FFMPEG):
        return {
            "error": (
                "ffmpeg not found. Install ffmpeg:\n"
                "  macOS:  brew install ffmpeg\n"
                "  Linux:  apt install ffmpeg"
            )
        }

    # Resolve input text
    if file_str:
        file_path = resolve_path(file_str)
        if not file_path.exists():
            return {"error": f"File not found: {file_path}"}
        result = _extract_text_for_tts(file_path)
        if isinstance(result, dict):
            return result
        input_text = result
    elif text:
        input_text = text
    else:
        return {"error": "No text or file provided. Use --text or --file."}

    input_text = input_text.strip()
    if not input_text:
        return {"error": "Input text is empty after extraction."}

    input_text = truncate_text(input_text, TTS_MAX_CHARS, "TTS input")

    output = resolve_path(output_str)
    err = ensure_output_dir(output)
    if err:
        return {"error": err}

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_audio = os.path.join(tmpdir, "tts_out.mp3")

        try:
            asyncio.run(_synthesise(input_text, voice, rate, volume, tmp_audio))
        except Exception as exc:
            return {"error": f"edge-tts synthesis failed: {exc}"}

        if not os.path.exists(tmp_audio):
            return {"error": "edge-tts produced no output file."}

        # Convert to MP3 using ffmpeg (edge-tts already produces mp3, but run through
        # ffmpeg to normalise the container and ensure compatibility)
        rc, _, stderr = run_command(
            [
                BIN_FFMPEG,
                "-y",
                "-i",
                tmp_audio,
                "-codec:a",
                "libmp3lame",
                "-qscale:a",
                "2",
                str(output),
            ]
        )
        if rc != 0:
            return {"error": f"ffmpeg conversion failed: {stderr.strip()}"}

    file_size_kb = round(output.stat().st_size / 1024, 1) if output.exists() else 0
    return {
        "output": str(output),
        "voice": voice,
        "chars": len(input_text),
        "file_size_kb": file_size_kb,
    }
