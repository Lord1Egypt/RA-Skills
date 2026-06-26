"""
Nex Voice - Voice Note Transcription & Action Extractor
"""

from .config import Config, config
from .storage import Database, Recording, ActionItem, Speaker
from .transcriber import (
    transcribe_audio,
    convert_audio,
    check_whisper,
    check_ffmpeg,
    get_audio_duration,
    validate_audio_format,
)
from .action_extractor import extract_actions, generate_summary

__version__ = "1.0.0"
__all__ = [
    "Config",
    "config",
    "Database",
    "Recording",
    "ActionItem",
    "Speaker",
    "transcribe_audio",
    "convert_audio",
    "check_whisper",
    "check_ffmpeg",
    "get_audio_duration",
    "validate_audio_format",
    "extract_actions",
    "generate_summary",
]
