"""
Nex Voice - Audio Transcription
"""

import subprocess
import json
from pathlib import Path
from typing import Dict, Optional, List, Any

from .config import WHISPER_CMD, WHISPER_MODEL, WHISPER_LANGUAGE, MAX_AUDIO_DURATION


def check_whisper() -> bool:
    """Check if whisper CLI is available"""
    try:
        subprocess.run(
            [WHISPER_CMD, "--version"],
            capture_output=True,
            check=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def check_ffmpeg() -> bool:
    """Check if ffmpeg is available"""
    try:
        subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            check=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def get_audio_duration(file_path: str) -> float:
    """Get audio duration in seconds using ffmpeg"""
    try:
        result = subprocess.run(
            [
                "ffmpeg",
                "-i", file_path,
            ],
            capture_output=True,
            text=True,
        )

        # Parse duration from ffmpeg output
        for line in result.stderr.split("\n"):
            if "Duration:" in line:
                duration_str = line.split("Duration:")[1].split(",")[0].strip()
                hours, minutes, seconds = duration_str.split(":")
                total_seconds = int(hours) * 3600 + int(minutes) * 60 + float(seconds)
                return total_seconds

        raise ValueError(f"Could not parse duration from {file_path}")

    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        raise RuntimeError(f"FFmpeg error: {e}")


def convert_audio(input_path: str, output_format: str = "wav") -> str:
    """Convert audio to specified format using ffmpeg"""
    input_path = Path(input_path)

    if not input_path.exists():
        raise FileNotFoundError(f"Audio file not found: {input_path}")

    # Create output path with new extension
    output_path = input_path.parent / f"{input_path.stem}_converted.{output_format}"

    try:
        subprocess.run(
            [
                "ffmpeg",
                "-i", str(input_path),
                "-y",  # Overwrite output file
                str(output_path),
            ],
            capture_output=True,
            check=True,
        )
        return str(output_path)

    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        raise RuntimeError(f"Audio conversion failed: {e}")


def transcribe_audio(
    file_path: str,
    language: Optional[str] = None,
    model: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Transcribe audio file using Whisper CLI.

    Returns:
        {
            "text": str,
            "language": str,
            "duration": float,
            "segments": list,
        }
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Audio file not found: {file_path}")

    # Check duration
    duration = get_audio_duration(str(file_path))
    if duration > MAX_AUDIO_DURATION:
        raise ValueError(
            f"Audio duration ({duration:.1f}s) exceeds maximum ({MAX_AUDIO_DURATION}s)"
        )

    language = language or WHISPER_LANGUAGE
    model = model or WHISPER_MODEL

    # Prepare Whisper command
    cmd = [
        WHISPER_CMD,
        str(file_path),
        "--model", model,
        "--language", language,
        "--output_format", "json",
        "--output_dir", str(file_path.parent),
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
        )

        # Read JSON output
        json_path = file_path.parent / f"{file_path.stem}.json"

        if not json_path.exists():
            raise RuntimeError("Whisper did not produce JSON output")

        with open(json_path, "r") as f:
            whisper_output = json.load(f)

        # Clean up JSON file
        json_path.unlink()

        # Extract transcript
        transcript = whisper_output.get("text", "").strip()

        if not transcript:
            raise ValueError("Transcription produced empty result")

        return {
            "text": transcript,
            "language": language,
            "duration": duration,
            "segments": whisper_output.get("segments", []),
        }

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Whisper transcription failed: {e.stderr}")
    except (json.JSONDecodeError, IOError) as e:
        raise RuntimeError(f"Failed to parse Whisper output: {e}")


def validate_audio_format(file_path: str, supported_formats: set = None) -> bool:
    """Check if audio file is in supported format"""
    if supported_formats is None:
        from .config import SUPPORTED_FORMATS
        supported_formats = SUPPORTED_FORMATS

    file_path = Path(file_path)
    return file_path.suffix.lstrip(".").lower() in supported_formats
