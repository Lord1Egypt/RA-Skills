#!/usr/bin/env python3
"""Transcribe podcast episodes using Whisper API or local whisper."""

import argparse
import hashlib
import ipaddress
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse

from utils import Transcript, TranscriptSegment, get_transcript_cache_path, get_whisper_config


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Transcribe podcast episodes using Whisper")
    parser.add_argument(
        "--episode",
        type=str,
        help="Path to episode JSON file or JSON string with episode data",
    )
    parser.add_argument("--audio-url", type=str, help="Direct URL to audio file")
    parser.add_argument("--output", type=Path, help="Output path for transcript JSON")
    parser.add_argument("--local", action="store_true", help="Use local whisper instead of API")
    parser.add_argument("--cache-dir", type=Path, help="Override cache directory path")
    return parser.parse_args()


def _episode_id_from_url(audio_url: str) -> str:
    return hashlib.sha256(audio_url.encode("utf-8")).hexdigest()[:12]


def _cache_path(episode_id: str, cache_dir_override: Optional[Path]) -> Path:
    if cache_dir_override is None:
        return get_transcript_cache_path(episode_id)
    cache_dir_override.mkdir(parents=True, exist_ok=True)
    return cache_dir_override / f"{episode_id}.json"


def validate_audio_url(url: str) -> Tuple[bool, str]:
    """Validate that URL is safe for ffmpeg fetches."""
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return False, "Only http/https audio URLs are allowed"

    host = parsed.hostname
    if not host:
        return False, "Audio URL missing hostname"

    lowered = host.lower()
    if lowered in {"localhost", "localhost.localdomain"}:
        return False, "Localhost audio URLs are blocked"

    try:
        addr = ipaddress.ip_address(host)
        if (
            addr.is_private
            or addr.is_loopback
            or addr.is_link_local
            or addr.is_multicast
            or addr.is_reserved
            or addr.is_unspecified
        ):
            return False, "Private/local IP audio URLs are blocked"
    except ValueError:
        # Host is a domain name; we allow it.
        pass

    return True, ""


def download_audio(url: str, temp_dir: Path) -> Optional[Path]:
    """Download audio from URL to temp WAV file."""
    is_valid, reason = validate_audio_url(url)
    if not is_valid:
        print(f"Unsafe audio URL rejected: {reason}", file=sys.stderr)
        return None

    audio_file = temp_dir / "audio.wav"
    cmd = [
        "ffmpeg",
        "-nostdin",
        "-hide_banner",
        "-loglevel",
        "error",
        "-i",
        url,
        "-vn",
        "-ac",
        "1",
        "-ar",
        "16000",
        "-acodec",
        "pcm_s16le",
        "-f",
        "wav",
        str(audio_file),
        "-y",
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    except Exception as exc:
        print(f"Error downloading audio: {exc}", file=sys.stderr)
        return None

    if result.returncode != 0:
        print(f"Error downloading/converting audio: {result.stderr}", file=sys.stderr)
        return None

    return audio_file


def _seg_value(seg: Any, key: str, default: Any) -> Any:
    if isinstance(seg, dict):
        return seg.get(key, default)
    return getattr(seg, key, default)


def transcribe_with_openai(audio_file: Path, model: str = "whisper-1") -> Optional[Dict[str, Any]]:
    """Transcribe using OpenAI Whisper API."""
    try:
        from openai import OpenAI
        from utils import get_openai_config

        config = get_openai_config()
        client = OpenAI(api_key=config["api_key"], base_url=config["base_url"])

        with open(audio_file, "rb") as handle:
            transcript = client.audio.transcriptions.create(
                model=model,
                file=handle,
                response_format="verbose_json",
            )

        segments = []
        for seg in getattr(transcript, "segments", []) or []:
            segments.append(
                {
                    "start": float(_seg_value(seg, "start", 0.0)),
                    "end": float(_seg_value(seg, "end", 0.0)),
                    "text": str(_seg_value(seg, "text", "")),
                }
            )

        return {
            "text": getattr(transcript, "text", ""),
            "segments": segments,
            "language": getattr(transcript, "language", "en"),
        }
    except Exception as exc:
        print(f"Error transcribing with OpenAI: {exc}", file=sys.stderr)
        return None


def transcribe_with_local(audio_file: Path, model: str = "base.en") -> Optional[Dict[str, Any]]:
    """Transcribe using local openai-whisper package if installed."""
    try:
        import whisper
    except Exception:
        print(
            "Local whisper transcription requires `openai-whisper`. "
            "Install it and rerun with --local.",
            file=sys.stderr,
        )
        return None

    local_model = model
    if model == "whisper-1":
        local_model = "base.en"

    try:
        model_obj = whisper.load_model(local_model)
        result = model_obj.transcribe(str(audio_file), fp16=False)
    except Exception as exc:
        print(f"Error transcribing locally: {exc}", file=sys.stderr)
        return None

    segments = []
    for seg in result.get("segments", []) or []:
        segments.append(
            {
                "start": float(seg.get("start", 0.0)),
                "end": float(seg.get("end", 0.0)),
                "text": str(seg.get("text", "")).strip(),
            }
        )

    return {
        "text": str(result.get("text", "")),
        "segments": segments,
        "language": str(result.get("language", "en")),
    }


def transcript_from_cache(cache_path: Path, episode_id: str) -> Optional[Transcript]:
    """Load transcript from cache file."""
    try:
        with open(cache_path, "r") as handle:
            data = json.load(handle)
        return Transcript(
            episode_id=episode_id,
            segments=[TranscriptSegment(**segment) for segment in data.get("segments", [])],
            full_text=data.get("full_text", ""),
            word_count=int(data.get("word_count", 0)),
            language=data.get("language", "en"),
        )
    except Exception as exc:
        print(f"Warning: failed to load cached transcript: {exc}", file=sys.stderr)
        return None


def transcribe_episode(
    episode_data: Dict[str, Any],
    use_local: bool = False,
    cache_dir_override: Optional[Path] = None,
) -> Optional[Transcript]:
    """Transcribe a single episode."""
    episode_id = str(episode_data.get("id") or _episode_id_from_url(episode_data.get("audio_url", "")))
    audio_url = episode_data.get("audio_url")

    if not audio_url:
        print(f"No audio URL provided for episode {episode_id}", file=sys.stderr)
        return None

    cache_path = _cache_path(episode_id, cache_dir_override)
    if cache_path.exists():
        cached = transcript_from_cache(cache_path, episode_id)
        if cached:
            return cached

    with tempfile.TemporaryDirectory() as temp_dir:
        audio_file = download_audio(audio_url, Path(temp_dir))
        if not audio_file:
            print(f"Failed to download audio for {episode_id}", file=sys.stderr)
            return None

        config = get_whisper_config()
        model = config.get("model", "whisper-1")
        should_use_local = use_local or bool(config.get("use_local", False))

        if should_use_local:
            result = transcribe_with_local(audio_file, model)
        else:
            result = transcribe_with_openai(audio_file, model)

        if not result:
            print(f"Transcription failed for {episode_id}", file=sys.stderr)
            return None

        segments: List[TranscriptSegment] = [
            TranscriptSegment(
                start=float(segment.get("start", 0.0)),
                end=float(segment.get("end", 0.0)),
                text=str(segment.get("text", "")),
            )
            for segment in result.get("segments", [])
        ]

        full_text = str(result.get("text", ""))
        if not segments and full_text:
            segments = [TranscriptSegment(start=0.0, end=0.0, text=full_text)]

        transcript = Transcript(
            episode_id=episode_id,
            segments=segments,
            full_text=full_text,
            word_count=len(full_text.split()),
            language=str(result.get("language", "en")),
        )

        try:
            cache_payload = {
                "episode_id": transcript.episode_id,
                "segments": [
                    {"start": seg.start, "end": seg.end, "text": seg.text}
                    for seg in transcript.segments
                ],
                "full_text": transcript.full_text,
                "word_count": transcript.word_count,
                "language": transcript.language,
            }
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            with open(cache_path, "w") as handle:
                json.dump(cache_payload, handle, indent=2)
        except Exception as exc:
            print(f"Warning: failed to cache transcript: {exc}", file=sys.stderr)

        return transcript


def load_episode_payload(args: argparse.Namespace) -> Dict[str, Any]:
    """Load episode data from --episode or --audio-url."""
    if args.episode:
        try:
            return json.loads(args.episode)
        except json.JSONDecodeError:
            with open(args.episode, "r") as handle:
                return json.load(handle)

    if args.audio_url:
        return {
            "id": _episode_id_from_url(args.audio_url),
            "audio_url": args.audio_url,
            "title": "Manual Episode",
        }

    raise ValueError("Must provide --episode or --audio-url")


def main() -> None:
    """Main transcription entry point."""
    args = parse_args()

    try:
        episode_data = load_episode_payload(args)
    except Exception as exc:
        print(f"Error loading episode data: {exc}", file=sys.stderr)
        sys.exit(1)

    transcript = transcribe_episode(
        episode_data,
        use_local=args.local,
        cache_dir_override=args.cache_dir,
    )
    if not transcript:
        sys.exit(1)

    output = {
        "episode_id": transcript.episode_id,
        "segments": [
            {"start": segment.start, "end": segment.end, "text": segment.text}
            for segment in transcript.segments
        ],
        "full_text": transcript.full_text,
        "word_count": transcript.word_count,
        "language": transcript.language,
    }

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w") as handle:
            json.dump(output, handle, indent=2)
    else:
        print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
