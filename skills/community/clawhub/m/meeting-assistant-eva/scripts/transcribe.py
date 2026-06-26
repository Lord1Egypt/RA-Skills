#!/usr/bin/env python3
"""
Transcribe 模块 — Whisper 语音转文字
支持批量转录、实时转录最近N分钟、多语言
"""

import argparse
import json
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = SKILL_DIR / "config.json"


def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)


def transcribe_file(audio_path, output_dir=None, model="base", language="zh", device="cpu"):
    """
    Transcribe a single audio file using Whisper CLI.

    Returns: Path to transcript text file, or None on failure.
    """
    audio_path = Path(audio_path)
    if not audio_path.exists():
        print(f"[Transcribe] File not found: {audio_path}")
        return None

    if output_dir is None:
        output_dir = audio_path.parent
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        "whisper",
        str(audio_path),
        "--model", model,
        "--language", language,
        "--output_format", "txt",
        "--output_dir", str(output_dir),
    ]

    if device != "cpu":
        cmd.extend(["--device", device])

    print(f"[Transcribe] Processing: {audio_path.name} (model={model}, lang={language})")

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)

    if result.returncode != 0:
        print(f"[Transcribe] Error: {result.stderr[:300]}")
        return None

    # Find the output file (whisper names it based on input)
    expected = output_dir / f"{audio_path.stem}.txt"
    if expected.exists():
        print(f"[Transcribe] Done: {expected}")
        return expected

    # Search for any new .txt files
    candidates = list(output_dir.glob(f"{audio_path.stem}*.txt"))
    if candidates:
        return candidates[0]

    print("[Transcribe] Output file not found")
    return None


def transcribe_chunks(chunks_dir, output_dir, config=None):
    """Transcribe all audio chunks in a directory and merge results."""
    if config is None:
        config = load_config()

    chunks_dir = Path(chunks_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    model = config.get("whisper_model", "base")
    language = config.get("whisper_language", "zh")
    device = config.get("integration", {}).get("whisper_device", "cpu")
    chunk_minutes = config.get("audio_chunk_minutes", 5)

    chunks = sorted(chunks_dir.glob("*.wav"))
    if not chunks:
        print("[Transcribe] No audio chunks found")
        return None

    print(f"[Transcribe] Processing {len(chunks)} chunks...")
    transcripts = []

    for i, chunk in enumerate(chunks):
        result = transcribe_file(chunk, output_dir, model, language, device)
        if result:
            transcripts.append((i, result))

    # Merge into full transcript
    full_path = output_dir / "full_transcript.txt"
    with open(full_path, "w", encoding="utf-8") as out:
        out.write(f"# Meeting Transcript\n")
        out.write(f"# Generated: {datetime.now().isoformat()}\n")
        out.write(f"# Model: {model}, Language: {language}\n\n")

        for i, t_path in transcripts:
            text = t_path.read_text(encoding="utf-8").strip()
            start_min = i * chunk_minutes
            end_min = start_min + chunk_minutes
            out.write(f"\n## [{start_min:02d}:{00:02d} - {end_min:02d}:{00:02d}]\n\n")
            out.write(text + "\n")

    print(f"[Transcribe] Full transcript saved: {full_path}")
    return full_path


def transcribe_recent(audio_path, last_minutes=5, config=None):
    """Extract and transcribe the last N minutes of an audio file."""
    if config is None:
        config = load_config()

    audio_path = Path(audio_path)
    if not audio_path.exists():
        print(f"[Transcribe] Audio not found: {audio_path}")
        return None

    model = config.get("whisper_model", "base")
    language = config.get("whisper_language", "zh")
    device = config.get("integration", {}).get("whisper_device", "cpu")

    # Extract last N minutes
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp_path = Path(tmp.name)

    cmd = [
        "ffmpeg", "-y",
        "-sseof", f"-{last_minutes * 60}",
        "-i", str(audio_path),
        "-c", "copy",
        str(tmp_path)
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0 or not tmp_path.exists():
        print(f"[Transcribe] Failed to extract audio clip")
        return None

    transcript = transcribe_file(tmp_path, tmp_path.parent, model, language, device)

    # Read and return text
    text = None
    if transcript and transcript.exists():
        text = transcript.read_text(encoding="utf-8").strip()
        transcript.unlink(missing_ok=True)

    tmp_path.unlink(missing_ok=True)
    return text


def check_whisper_installed():
    """Check if Whisper is available."""
    try:
        result = subprocess.run(
            ["whisper", "--help"],
            capture_output=True, text=True, timeout=10
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Whisper transcription utility")
    sub = parser.add_subparsers(dest="command")

    p_file = sub.add_parser("file", help="Transcribe single file")
    p_file.add_argument("audio", help="Audio file path")
    p_file.add_argument("--output-dir", "-o", help="Output directory")

    p_chunks = sub.add_parser("chunks", help="Transcribe all chunks in directory")
    p_chunks.add_argument("chunks_dir", help="Directory with audio chunks")
    p_chunks.add_argument("--output-dir", "-o", required=True)

    p_recent = sub.add_parser("recent", help="Transcribe last N minutes")
    p_recent.add_argument("audio", help="Full audio file path")
    p_recent.add_argument("--last", type=int, default=5, help="Last N minutes")

    p_check = sub.add_parser("check", help="Check Whisper installation")

    args = parser.parse_args()

    if args.command == "file":
        config = load_config()
        transcribe_file(
            args.audio,
            args.output_dir,
            model=config.get("whisper_model", "base"),
            language=config.get("whisper_language", "zh"),
            device=config.get("integration", {}).get("whisper_device", "cpu")
        )

    elif args.command == "chunks":
        transcribe_chunks(args.chunks_dir, args.output_dir)

    elif args.command == "recent":
        text = transcribe_recent(args.audio, args.last)
        if text:
            print(f"\n--- Last {args.last} minutes ---\n")
            print(text)
        else:
            print("Transcription failed")

    elif args.command == "check":
        if check_whisper_installed():
            print("Whisper is installed and available")
        else:
            print("Whisper not found. Install with: pip install openai-whisper")

    else:
        parser.print_help()
