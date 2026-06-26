#!/usr/bin/env python3
"""
YouTube transcript extraction module.

Fetches video transcripts/subtitles via youtube-transcript-api (v1.x API).
Supports language fallback, plain-text and JSON output, and save-to-Nextcloud.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
    InvalidVideoId,
)

# Regex patterns for YouTube video ID extraction
YOUTUBE_URL_PATTERNS = [
    re.compile(r"(?:youtube\.com/watch\?.*v=)([a-zA-Z0-9_-]{11})"),
    re.compile(r"(?:youtu\.be/)([a-zA-Z0-9_-]{11})"),
    re.compile(r"(?:youtube\.com/shorts/)([a-zA-Z0-9_-]{11})"),
    re.compile(r"(?:youtube\.com/embed/)([a-zA-Z0-9_-]{11})"),
]

RAW_ID_PATTERN = re.compile(r"^[a-zA-Z0-9_-]{11}$")


def extract_video_id(input_str: str) -> str:
    """Extract an 11-char YouTube video ID from a URL or raw ID string.

    Args:
        input_str: A YouTube URL or bare video ID.

    Returns:
        The 11-character video ID.

    Raises:
        ValueError: If no valid video ID can be extracted.
    """
    cleaned = input_str.strip()

    for pattern in YOUTUBE_URL_PATTERNS:
        m = pattern.search(cleaned)
        if m:
            return m.group(1)

    if RAW_ID_PATTERN.match(cleaned):
        return cleaned

    raise ValueError(
        f"Could not extract YouTube video ID from: {input_str!r}. "
        "Provide a youtube.com/watch?v=..., youtu.be/..., or raw 11-char ID."
    )


def get_transcript(
    video_id: str,
    languages: tuple[str, ...] = ("en",),
    fmt: str = "text",
) -> dict[str, Any]:
    """Fetch a YouTube video transcript with language fallback.

    Args:
        video_id: The 11-character YouTube video ID.
        languages: Ordered tuple of language codes to try (e.g. ("ro", "en")).
        fmt: Output format — "text" strips timestamps, "json" includes them.

    Returns:
        Dict with keys: ok, video_id, lang (the matched language), transcript,
        and snippet_count.

    Raises:
        NoTranscriptFound: None of the requested languages are available.
        TranscriptsDisabled: Video has captions turned off.
        VideoUnavailable: Video is private/deleted/region-blocked.
    """
    api = YouTubeTranscriptApi()
    transcript = api.fetch(video_id, languages=languages)
    matched_lang = transcript.language_code  # type: ignore[attr-defined]
    snippets = list(transcript)

    if fmt == "json":
        payload = [
            {"text": s.text, "start": s.start, "duration": s.duration}
            for s in snippets
        ]
    else:
        payload = " ".join(s.text.replace("\n", " ") for s in snippets)

    return {
        "ok": True,
        "video_id": video_id,
        "lang": matched_lang,
        "transcript": payload,
        "snippet_count": len(snippets),
    }


def list_languages(video_id: str) -> dict[str, Any]:
    """List all available caption languages for a video.

    Args:
        video_id: The 11-character YouTube video ID.

    Returns:
        Dict with keys: ok, video_id, languages (list of dicts with code, name,
        is_generated, is_translatable).

    Raises:
        VideoUnavailable: Video is private/deleted/not found.
    """
    api = YouTubeTranscriptApi()
    transcript_list = api.list(video_id)

    langs = []
    for entry in transcript_list:
        langs.append(
            {
                "code": entry.language_code,
                "name": entry.language,
                "is_generated": entry.is_generated,
                "is_translatable": entry.is_translatable,
            }
        )

    return {
        "ok": True,
        "video_id": video_id,
        "languages": langs,
    }


def format_filename(video_id: str, lang: str, fmt: str) -> str:
    """Build a Nextcloud-safe filename for a transcript."""
    ext = "txt" if fmt == "text" else "json"
    return f"{video_id}_{lang}.{ext}"


def save_to_nextcloud(
    video_id: str,
    content: str,
    fmt: str,
    lang: str,
) -> str:
    """Save transcript content to Nextcloud under /Alex's Assistant/YouTube/.

    Uses the Nexlink Nextcloud module for the actual upload.

    Args:
        video_id: YouTube video ID.
        content: Transcript text or JSON string.
        fmt: "text" or "json" — determines file extension.
        lang: Language code used for the transcript.

    Returns:
        The remote path where the file was saved.

    Raises:
        ImportError: If the Nextcloud module's upload function is unavailable.
        Exception: Upload failures from the Nextcloud client.
    """
    from modules.nextcloud.nextcloud import NextcloudClient

    filename = format_filename(video_id, lang, fmt)
    remote_dir = "/Alex's Assistant/YouTube/"
    remote_path = remote_dir + filename

    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=f".{filename.rsplit('.', 1)[1]}", delete=False
    )
    try:
        tmp.write(content)
        tmp.close()

        client = NextcloudClient()
        ok = client.upload(tmp.name, remote_path)
        if not ok:
            raise RuntimeError(f"Upload to {remote_path} failed")
    finally:
        os.unlink(tmp.name)

    return remote_path


def cmd_transcript(args: argparse.Namespace) -> None:
    """Handle 'nexlink youtube transcript <URL> [options]'."""
    try:
        video_id = extract_video_id(args.url)
    except ValueError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}))
        sys.exit(1)

    languages = tuple(l.strip() for l in args.lang.split(",") if l.strip())
    if not languages:
        languages = ("en",)

    try:
        result = get_transcript(video_id, languages=languages, fmt=args.format)
    except NoTranscriptFound:
        msg = (
            f"No transcript found for video {video_id} in languages: {args.lang}. "
            f"Try 'nexlink youtube languages {args.url}' to see available captions."
        )
        print(json.dumps({"ok": False, "error": msg}))
        sys.exit(1)
    except TranscriptsDisabled:
        print(
            json.dumps(
                {
                    "ok": False,
                    "error": f"Transcripts are disabled for video {video_id}.",
                }
            )
        )
        sys.exit(1)
    except VideoUnavailable:
        print(
            json.dumps(
                {
                    "ok": False,
                    "error": f"Video {video_id} is unavailable (private, deleted, or blocked).",
                }
            )
        )
        sys.exit(1)
    except InvalidVideoId:
        print(
            json.dumps(
                {
                    "ok": False,
                    "error": f"Invalid video ID: {video_id}.",
                }
            )
        )
        sys.exit(1)
    except Exception as exc:
        print(
            json.dumps(
                {
                    "ok": False,
                    "error": f"Failed to fetch transcript: {exc}",
                }
            )
        )
        sys.exit(1)

    # Save to Nextcloud if requested
    saved_path = None
    if args.save:
        content = result["transcript"]
        if isinstance(content, list):
            content = json.dumps(content, indent=2)
        try:
            saved_path = save_to_nextcloud(video_id, content, args.format, result["lang"])
        except Exception as exc:
            print(
                json.dumps(
                    {
                        "ok": False,
                        "error": f"Transcript fetched but save-to-Nextcloud failed: {exc}",
                        "video_id": video_id,
                        "lang": result["lang"],
                    }
                )
            )
            sys.exit(1)

    output = {
        "ok": True,
        "video_id": video_id,
        "lang": result["lang"],
        "snippet_count": result["snippet_count"],
        "format": args.format,
    }
    if saved_path:
        output["saved_to"] = saved_path

    if args.format == "json":
        output["transcript"] = result["transcript"]
    else:
        output["transcript"] = result["transcript"]

    print(json.dumps(output, indent=2, ensure_ascii=False))


def cmd_languages(args: argparse.Namespace) -> None:
    """Handle 'nexlink youtube languages <URL>'."""
    try:
        video_id = extract_video_id(args.url)
    except ValueError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}))
        sys.exit(1)

    try:
        result = list_languages(video_id)
    except VideoUnavailable:
        print(
            json.dumps(
                {
                    "ok": False,
                    "error": f"Video {video_id} is unavailable.",
                }
            )
        )
        sys.exit(1)
    except Exception as exc:
        print(
            json.dumps(
                {
                    "ok": False,
                    "error": f"Failed to list languages: {exc}",
                }
            )
        )
        sys.exit(1)

    print(json.dumps(result, indent=2, ensure_ascii=False))


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for the youtube module."""
    parser = argparse.ArgumentParser(
        prog="nexlink youtube",
        description="Extract and work with YouTube video transcripts.",
    )
    sub = parser.add_subparsers(dest="youtube_cmd", required=True)

    # transcript subcommand
    p_transcript = sub.add_parser("transcript", help="Fetch a video transcript")
    p_transcript.add_argument("url", help="YouTube URL or video ID")
    p_transcript.add_argument(
        "--lang",
        default="en",
        help="Comma-separated language codes (e.g. 'ro,en'). Tried in order. (default: en)",
    )
    p_transcript.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format: 'text' strips timestamps, 'json' includes them. (default: text)",
    )
    p_transcript.add_argument(
        "--save",
        action="store_true",
        help="Save the transcript to Nextcloud under /Alex's Assistant/YouTube/",
    )
    p_transcript.set_defaults(func=cmd_transcript)

    # languages subcommand
    p_lang = sub.add_parser("languages", help="List available caption languages for a video")
    p_lang.add_argument("url", help="YouTube URL or video ID")
    p_lang.set_defaults(func=cmd_languages)

    return parser


def run_cli(argv: list[str] | None = None) -> int:
    """Entry point for 'nexlink youtube <subcommand>'."""
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)
    return 0


def main() -> None:
    """Direct entry point (python3 -m modules.youtube)."""
    run_cli()


if __name__ == "__main__":
    main()
