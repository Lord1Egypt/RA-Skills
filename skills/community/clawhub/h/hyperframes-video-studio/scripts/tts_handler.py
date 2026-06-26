#!/usr/bin/env python3
"""Free TTS router for Hyperframes Video Studio."""

from __future__ import annotations

import argparse
import asyncio
import json
import shutil
import subprocess
import sys
import wave
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
CACHE_DIR = BASE_DIR / ".cache"
AUDIO_DIR = CACHE_DIR / "audio"
LOCAL_NPM_BIN = CACHE_DIR / "npm" / "node_modules" / ".bin"


def _print(payload: dict) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def _read_json(path: Path) -> dict:
    with path.expanduser().open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _wav_duration(path: Path) -> float | None:
    try:
        with wave.open(str(path), "rb") as handle:
            frames = handle.getnframes()
            rate = handle.getframerate()
            return frames / float(rate)
    except Exception:
        return None


def _probe_duration(path: Path) -> float | None:
    ffprobe = _which("ffprobe")
    if not ffprobe:
        return _wav_duration(path)
    command = [
        ffprobe,
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(path),
    ]
    try:
        output = subprocess.check_output(command, text=True).strip()
        return float(output)
    except Exception:
        return _wav_duration(path)


def _subtitle_chunks(text: str, duration: float) -> list[dict]:
    words = text.split()
    if not words:
        return []
    chunk_size = 7
    chunks = [" ".join(words[i : i + chunk_size]) for i in range(0, len(words), chunk_size)]
    step = duration / max(1, len(chunks))
    subtitles = []
    for index, chunk in enumerate(chunks):
        start = round(index * step, 3)
        end = round(min(duration, (index + 1) * step), 3)
        subtitles.append({"start": start, "end": end, "text": chunk})
    return subtitles


def _estimated_duration(text: str) -> float:
    words = max(1, len(text.split()))
    return max(1.5, words / 2.6)


def _piper_available() -> str | None:
    return _which("piper") or _which("piper-tts")


def _which(name: str) -> str | None:
    candidates = []
    if sys.platform == "win32":
        candidates.append(LOCAL_NPM_BIN / f"{name}.cmd")
    candidates.extend(
        [
            LOCAL_NPM_BIN / name,
            BASE_DIR / ".venv" / ("Scripts" if sys.platform == "win32" else "bin") / name,
            Path(sys.executable).with_name(name),
        ]
    )
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    return shutil.which(name)


def _python_module_available(name: str) -> bool:
    try:
        __import__(name)
        return True
    except Exception:
        return False


def _edge_available() -> bool:
    return _which("edge-tts") is not None or _python_module_available("edge_tts")


def _run_piper(text: str, output: Path, voice: str | None, piper_bin: str) -> dict:
    if output.suffix.lower() != ".wav":
        output = output.with_suffix(".wav")
    model = voice
    if not model:
        return {
            "status": "dependency_missing",
            "message": "Piper is installed, but a Piper model path is required as voice for fully local TTS.",
            "provider": "piper",
        }

    command = [piper_bin, "--model", model, "--output_file", str(output)]
    try:
        subprocess.run(command, input=text, text=True, check=True, capture_output=True)
    except subprocess.CalledProcessError as exc:
        return {
            "status": "tts_failed",
            "provider": "piper",
            "message": "Piper failed to generate audio.",
            "stderr": exc.stderr[-2000:],
        }

    duration = _probe_duration(output) or _estimated_duration(text)
    return {
        "status": "ok",
        "provider": "piper",
        "audio_path": str(output.resolve()),
        "duration_seconds": round(duration, 3),
        "subtitles": _subtitle_chunks(text, duration),
    }


async def _run_edge_tts(text: str, output: Path, voice: str | None) -> dict:
    selected_voice = voice or "en-US-JennyNeural"
    subtitle_path = output.with_suffix(".srt")
    cli = _which("edge-tts")
    if cli:
        command = [
            cli,
            "--voice",
            selected_voice,
            "--text",
            text,
            "--write-media",
            str(output),
            "--write-subtitles",
            str(subtitle_path),
        ]
        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as exc:
            return {
                "status": "tts_failed",
                "provider": "edge-tts",
                "message": "edge-tts failed to generate audio.",
                "stderr": exc.stderr[-2000:],
            }
    else:
        try:
            import edge_tts  # type: ignore
        except Exception:
            return {
                "status": "dependency_missing",
                "provider": "edge-tts",
                "message": "edge-tts is not installed. Install with: python3 -m pip install --user edge-tts",
            }

        communicate = edge_tts.Communicate(text, selected_voice)
        try:
            await communicate.save(str(output))
        except Exception as exc:
            return {"status": "tts_failed", "provider": "edge-tts", "message": str(exc)}
        subtitle_path.write_text("", encoding="utf-8")

    duration = _probe_duration(output) or _estimated_duration(text)
    return {
        "status": "ok",
        "provider": "edge-tts",
        "audio_path": str(output.resolve()),
        "duration_seconds": round(duration, 3),
        "subtitle_path": str(subtitle_path.resolve()),
        "subtitles": _subtitle_chunks(text, duration),
    }


def _edge_output_path(output: Path) -> Path:
    if output.suffix.lower() in ("", ".wav"):
        return output.with_suffix(".mp3")
    return output


def _edge_missing() -> dict:
    if not _edge_available():
        return {
            "status": "dependency_missing",
            "provider": "edge-tts",
            "message": "edge-tts is not installed. Install with: python3 -m pip install --user edge-tts. If pip is externally managed, use a virtualenv.",
            "install_hints": [
                "python3 -m venv .cache/venv",
                ".cache/venv/bin/python -m pip install edge-tts",
                "python3 -m pip install --user edge-tts"
            ],
        }
    return {"status": "ok"}


def synthesize(request: dict) -> dict:
    text = str(request.get("text", "")).strip()
    if not text:
        return {"status": "invalid_request", "message": "Missing non-empty text."}

    provider = request.get("provider", "auto")
    voice = request.get("voice")
    output = Path(request.get("output") or AUDIO_DIR / "voice.mp3").expanduser()
    if not output.is_absolute():
        output = (BASE_DIR / output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    if provider in ("auto", "piper"):
        piper_bin = _piper_available()
        if piper_bin:
            result = _run_piper(text, output, voice, piper_bin)
            if result["status"] == "ok" or provider == "piper":
                return result

    if provider in ("auto", "edge-tts"):
        missing = _edge_missing()
        if missing["status"] != "ok":
            return missing
        edge_output = _edge_output_path(output)
        return asyncio.run(_run_edge_tts(text, edge_output, voice))

    return {
        "status": "dependency_missing",
        "message": "No free TTS provider is available. Install Piper for local TTS or edge-tts for zero-cost keyless TTS.",
        "providers_checked": ["piper", "edge-tts"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate narration and subtitle timing.")
    parser.add_argument("--input-json", required=True)
    args = parser.parse_args()

    result = synthesize(_read_json(Path(args.input_json)))
    _print(result)
    return 0 if result.get("status") == "ok" else 2


if __name__ == "__main__":
    sys.exit(main())
