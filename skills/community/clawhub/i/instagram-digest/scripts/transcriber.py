"""
Downloads Instagram reel audio via yt-dlp and transcribes it with faster-whisper.
"""

import tempfile
from pathlib import Path

import yt_dlp
from faster_whisper import WhisperModel

_model = None


def _get_model():
    global _model
    if _model is None:
        print("  Loading Whisper model (first run only)...")
        _model = WhisperModel("base", device="cpu", compute_type="int8")
    return _model


def transcribe_reel(url: str) -> str:
    """Download a reel and return its audio transcription."""
    with tempfile.TemporaryDirectory(prefix="insta_audio_") as tmp:
        out_tmpl = str(Path(tmp) / "reel.%(ext)s")

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": out_tmpl,
            "quiet": True,
            "no_warnings": True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            return f"Download failed: {e}"

        files = [f for f in Path(tmp).iterdir() if f.is_file()]
        if not files:
            return "No audio file found after download."

        try:
            model = _get_model()
            segments, _ = model.transcribe(str(files[0]), beam_size=5)
            return " ".join(seg.text.strip() for seg in segments).strip()
        except Exception as e:
            return f"Transcription failed: {e}"
