#!/usr/bin/env python3
"""Transcribe downloaded podcast episodes using Whisper."""

import argparse
import json
import os
import sys
from pathlib import Path

DEFAULT_ARCHIVE = os.environ.get("HN_ARCHIVE_DIR", "./hn-podcast-archive")
DEFAULT_MODEL = os.environ.get("WHISPER_MODEL", "turbo")
DEFAULT_FORMAT = os.environ.get("WHISPER_FORMAT", "txt")


def find_untranscribed(archive_dir: Path, fmt: str) -> list[Path]:
    """Find episode dirs with audio but no transcript."""
    untranscribed = []
    ext = f".{fmt}"
    for d in sorted(archive_dir.iterdir()):
        if not d.is_dir():
            continue
        audio = None
        for name in ("audio.mp3", "audio.m4a", "audio.wav", "audio.ogg", "audio.flac"):
            if (d / name).exists():
                audio = d / name
                break
        transcript = d / f"transcript{ext}"
        if audio and not transcript.exists():
            untranscribed.append(d)
    return untranscribed


def transcribe_episode(ep_dir: Path, model: str, fmt: str) -> None:
    # Ensure ffmpeg is available (try static_ffmpeg first)
    try:
        import static_ffmpeg
        static_ffmpeg.add_paths()
    except Exception:
        pass

    import whisper

    audio_path = None
    for name in ("audio.mp3", "audio.m4a", "audio.wav", "audio.ogg", "audio.flac"):
        if (ep_dir / name).exists():
            audio_path = ep_dir / name
            break
    if not audio_path:
        print(f"  No audio found in {ep_dir.name}")
        return
    print(f"  Transcribing: {ep_dir.name} ({audio_path.name})")

    mdl = whisper.load_model(model)
    result = mdl.transcribe(str(audio_path))

    # Save transcript
    ext = f".{fmt}"
    out_path = ep_dir / f"transcript{ext}"

    if fmt == "txt":
        with open(out_path, "w") as f:
            f.write(result["text"])
    elif fmt == "srt":
        from whisper.utils import format_srt
        with open(out_path, "w") as f:
            f.write(format_srt(result["segments"]))
    elif fmt == "vtt":
        from whisper.utils import format_vtt
        with open(out_path, "w") as f:
            f.write(format_vtt(result["segments"]))
    elif fmt == "json":
        with open(out_path, "w") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
    else:
        with open(ep_dir / "transcript.txt", "w") as f:
            f.write(result["text"])

    # Update episode metadata
    meta_path = ep_dir / "episode.json"
    if meta_path.exists():
        with open(meta_path) as f:
            meta = json.load(f)
        meta["transcribed"] = True
        meta["whisper_model"] = model
        with open(meta_path, "w") as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)

    print(f"  Done: {out_path}")


def transcribe_all(archive_dir: str, model: str, fmt: str) -> int:
    archive = Path(archive_dir)
    if not archive.exists():
        print(f"Archive not found: {archive_dir}", file=sys.stderr)
        return 0

    untranscribed = find_untranscribed(archive, fmt)
    print(f"Found {len(untranscribed)} untranscribed episodes (model={model}, format={fmt})")

    for ep_dir in untranscribed:
        try:
            transcribe_episode(ep_dir, model, fmt)
        except Exception as e:
            print(f"  ERROR transcribing {ep_dir.name}: {e}", file=sys.stderr)

    return len(untranscribed)


def main():
    parser = argparse.ArgumentParser(description="Transcribe podcast episodes with Whisper")
    parser.add_argument("--archive", default=DEFAULT_ARCHIVE)
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Whisper model (tiny/base/small/medium/large/turbo)")
    parser.add_argument("--format", default=DEFAULT_FORMAT, choices=["txt", "srt", "vtt", "json"])
    args = parser.parse_args()
    count = transcribe_all(args.archive, args.model, args.format)
    print(f"Transcribed {count} episodes")


if __name__ == "__main__":
    main()
