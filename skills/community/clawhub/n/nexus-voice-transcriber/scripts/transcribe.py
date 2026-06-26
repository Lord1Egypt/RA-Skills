#!/usr/bin/env python3
"""
Voice Transcriber - Transcribe audio files using local Whisper or Deepgram API.

Usage:
  python3 transcribe.py --file <path_or_url> --provider <whisper|deepgram> [options]

Options:
  --file         Path to local audio/video file or URL
  --provider     whisper | deepgram
  --model        Whisper model: tiny, base, small, medium, large (default: base)
  --format       Output format: txt, srt, vtt, json (default: txt)
  --diarize      Enable speaker diarization (Deepgram only)
  --split        Split long audio into chunks before processing
  --output-dir   Directory to save transcript (default: ~/voice-transcriber/transcripts)
  --audio-dir    Directory to save audio (default: ~/voice-transcriber/audio)
  --save-audio   Save original audio file to audio-dir
  --language     Language code (e.g., en, es, fr). Whisper auto-detects if omitted.
  --help         Show this help

Examples:
  # Local Whisper transcription
  python3 transcribe.py --file voice_note.m4a --provider whisper --model medium

  # Deepgram with speaker labels
  python3 transcribe.py --file meeting.mp3 --provider deepgram --diarize --format json

  # Split long file, transcribe with Whisper
  python3 transcribe.py --file long_lecture.wav --provider whisper --split --format srt
"""

import argparse
import json
import os
import sys
import tempfile
import shutil
from pathlib import Path
import subprocess
import requests

# ============================================================
# Utility functions
# ============================================================

def ensure_dir(path: str) -> Path:
    p = Path(path).expanduser()
    p.mkdir(parents=True, exist_ok=True)
    return p

def download_file(url: str, dest: Path) -> Path:
    """Download a file from URL to dest path."""
    print(f"Downloading {url} ...")
    try:
        r = requests.get(url, stream=True, timeout=60)
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print(f"Saved to {dest}")
        return dest
    except Exception as e:
        print(f"Error downloading {url}: {e}", file=sys.stderr)
        sys.exit(1)

def extract_audio_ffmpeg(video_path: Path, audio_path: Path = None) -> Path:
    """Extract audio from video using ffmpeg. Returns path to extracted audio."""
    if audio_path is None:
        audio_path = video_path.with_suffix(".wav")
    cmd = [
        "ffmpeg", "-y", "-i", str(video_path),
        "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
        str(audio_path)
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"Extracted audio to {audio_path}")
        return audio_path
    except subprocess.CalledProcessError as e:
        print(f"ffmpeg error: {e.stderr.decode()}", file=sys.stderr)
        sys.exit(1)

def split_audio_ffmpeg(audio_path: Path, chunk_sec: int = 600) -> list[Path]:
    """Split audio into chunks of chunk_sec seconds. Returns list of chunk paths."""
    chunk_pattern = audio_path.parent / f"chunk_%03d{audio_path.suffix}"
    cmd = [
        "ffmpeg", "-y", "-i", str(audio_path),
        "-f", "segment", "-segment_time", str(chunk_sec),
        "-c", "copy", str(chunk_pattern)
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        # collect generated chunks
        chunks = sorted(audio_path.parent.glob("chunk_*" + audio_path.suffix))
        print(f"Split into {len(chunks)} chunks")
        return chunks
    except subprocess.CalledProcessError as e:
        print(f"ffmpeg split error: {e.stderr.decode()}", file=sys.stderr)
        sys.exit(1)

# ============================================================
# Whisper (local) transcription
# ============================================================

def transcribe_whisper(
    file_path: Path,
    model_size: str = "base",
    output_format: str = "txt",
    language: str = None
) -> str:
    """Transcribe using local Whisper. Returns transcript text."""
    try:
        import whisper
    except ImportError:
        print("Error: openai-whisper not installed. Run: pip install openai-whisper", file=sys.stderr)
        sys.exit(1)

    print(f"Loading Whisper model '{model_size}'...")
    model = whisper.load_model(model_size)

    transcribe_options = {}
    if language:
        transcribe_options["language"] = language

    print(f"Transcribing {file_path} ...")
    result = model.transcribe(str(file_path), **transcribe_options)

    # Format output
    if output_format == "json":
        # Whisper returns segments with start, end, text
        segments = [
            {
                "start": seg["start"],
                "end": seg["end"],
                "text": seg["text"].strip()
            }
            for seg in result["segments"]
        ]
        return json.dumps({"text": result["text"], "segments": segments}, ensure_ascii=False, indent=2)

    elif output_format == "srt":
        def srt_timestamp(seconds: float) -> str:
            h = int(seconds // 3600)
            m = int((seconds % 3600) // 60)
            s = int(seconds % 60)
            ms = int((seconds - int(seconds)) * 1000)
            return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

        lines = []
        for i, seg in enumerate(result["segments"]):
            lines.append(str(i + 1))
            lines.append(f"{srt_timestamp(seg['start'])} --> {srt_timestamp(seg['end'])}")
            lines.append(seg["text"].strip())
            lines.append("")
        return "\n".join(lines)

    elif output_format == "vtt":
        lines = ["WEBVTT", ""]
        for seg in result["segments"]:
            start = seg["start"]
            end = seg["end"]
            h = int(start // 3600)
            m = int((start % 3600) // 60)
            s = start % 60
            start_str = f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")
            h = int(end // 3600)
            m = int((end % 3600) // 60)
            s = end % 60
            end_str = f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")
            lines.append(f"{start_str} --> {end_str}")
            lines.append(seg["text"].strip())
            lines.append("")
        return "\n".join(lines)

    else:  # txt
        return result["text"].strip()

# ============================================================
# Deepgram transcription
# ============================================================

def transcribe_deepgram(
    file_path: Path,
    output_format: str = "txt",
    diarize: bool = False,
    language: str = None
) -> str:
    """Transcribe using Deepgram API. Returns transcript text/json."""
    api_key = os.environ.get("DEEPGRAM_API_KEY")
    if not api_key:
        print("Error: DEEPGRAM_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)

    url = "https://api.deepgram.com/v1/listen"
    params = {"punctuate": "true", "utterances": "true"}
    if diarize:
        params["diarize"] = "true"
    if language:
        params["language"] = language

    headers = {
        "Authorization": f"Token {api_key}",
        "Content-Type": "audio/*"
    }

    print(f"Sending {file_path} to Deepgram...")
    try:
        with open(file_path, "rb") as f:
            response = requests.post(url, params=params, headers=headers, data=f, timeout=300)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Deepgram API error: {e}", file=sys.stderr)
        sys.exit(1)

    result = response.json()

    # Extract transcript based on format
    if output_format == "json":
        return json.dumps(result, ensure_ascii=False, indent=2)

    # Get the full transcript text
    transcript = result.get("results", {}).get("channels", [{}])[0].get("alternatives", [{}])[0].get("transcript", "")

    if output_format == "txt":
        if diarize:
            # Build speaker-labeled text
            utterances = result.get("results", {}).get("utterances", [])
            lines = []
            for u in utterances:
                speaker = u.get("speaker", "?")
                text = u.get("transcript", "").strip()
                lines.append(f"[Speaker {speaker}] {text}")
            return "\n".join(lines)
        else:
            return transcript.strip()

    elif output_format == "srt":
        # Build SRT from utterances or words
        if diarize:
            utterances = result.get("results", {}).get("utterances", [])
            def srt_ts(seconds):
                h = int(seconds // 3600)
                m = int((seconds % 3600) // 60)
                s = int(seconds % 60)
                ms = int((seconds - int(seconds)) * 1000)
                return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
            lines = []
            for i, u in enumerate(utterances):
                lines.append(str(i + 1))
                lines.append(f"{srt_ts(u['start'])} --> {srt_ts(u['end'])}")
                lines.append(f"[Speaker {u.get('speaker', '?')}] {u.get('transcript', '').strip()}")
                lines.append("")
            return "\n".join(lines)
        else:
            # Fallback to word-level timing if available
            words = result.get("results", {}).get("channels", [{}])[0].get("alternatives", [{}])[0].get("words", [])
            if not words:
                return transcript.strip()
            # group words into sentences (simple logic by pause > 1s)
            segments = []
            current = {"start": words[0]["start"], "end": words[0]["end"], "text": words[0]["word"]}
            for w in words[1:]:
                if w["start"] - current["end"] > 1.0:
                    segments.append(current)
                    current = {"start": w["start"], "end": w["end"], "text": w["word"]}
                else:
                    current["end"] = w["end"]
                    current["text"] += f" {w['word']}"
            segments.append(current)
            def srt_ts2(seconds):
                h = int(seconds // 3600)
                m = int((seconds % 3600) // 60)
                s = int(seconds % 60)
                ms = int((seconds - int(seconds)) * 1000)
                return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
            lines = []
            for i, seg in enumerate(segments):
                lines.append(str(i + 1))
                lines.append(f"{srt_ts2(seg['start'])} --> {srt_ts2(seg['end'])}")
                lines.append(seg["text"].strip())
                lines.append("")
            return "\n".join(lines)

    elif output_format == "vtt":
        # Similar to SRT but VTT format
        if diarize:
            utterances = result.get("results", {}).get("utterances", [])
            lines = ["WEBVTT", ""]
            for u in utterances:
                start = u["start"]
                end = u["end"]
                h = int(start // 3600)
                m = int((start % 3600) // 60)
                s = start % 60
                start_str = f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")
                h = int(end // 3600)
                m = int((end % 3600) // 60)
                s = end % 60
                end_str = f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")
                lines.append(f"{start_str} --> {end_str}")
                lines.append(f"[Speaker {u.get('speaker', '?')}] {u.get('transcript', '').strip()}")
                lines.append("")
            return "\n".join(lines)
        else:
            return "WEBVTT\n\n" + transcript.strip()

    else:
        return transcript.strip()

# ============================================================
# Main logic
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="Transcribe audio files")
    parser.add_argument("--file", required=True, help="Path to audio/video file or URL")
    parser.add_argument("--provider", choices=["whisper", "deepgram"], default="whisper", help="Transcription provider")
    parser.add_argument("--model", default="base", help="Whisper model size (tiny/base/small/medium/large)")
    parser.add_argument("--format", choices=["txt", "srt", "vtt", "json"], default="txt", help="Output format")
    parser.add_argument("--diarize", action="store_true", help="Enable speaker diarization (Deepgram only)")
    parser.add_argument("--split", action="store_true", help="Split long audio into chunks before processing")
    parser.add_argument("--output-dir", default="~/voice-transcriber/transcripts", help="Directory to save transcript")
    parser.add_argument("--audio-dir", default="~/voice-transcriber/audio", help="Directory to save audio")
    parser.add_argument("--save-audio", action="store_true", help="Save original audio file")
    parser.add_argument("--language", help="Language code (e.g., en, es, fr)")
    args = parser.parse_args()

    # Resolve file path
    file_path = Path(args.file)
    temp_dir = None
    is_url = args.file.startswith("http://") or args.file.startswith("https://")

    if is_url:
        temp_dir = Path(tempfile.mkdtemp())
        dest = temp_dir / "audio_input"
        # try to keep extension
        ext = Path(args.file).suffix or ".mp3"
        dest = dest.with_suffix(ext)
        download_file(args.file, dest)
        file_path = dest
    else:
        if not file_path.exists():
            print(f"Error: File not found: {file_path}", file=sys.stderr)
            sys.exit(1)

    # If video file, extract audio
    video_exts = {".mp4", ".mov", ".avi", ".mkv", ".webm"}
    if file_path.suffix.lower() in video_exts:
        print("Video file detected, extracting audio...")
        audio_path = file_path.with_suffix(".wav")
        file_path = extract_audio_ffmpeg(file_path, audio_path)

    # Split if requested
    chunks = []
    if args.split:
        print("Splitting audio into chunks...")
        chunks = split_audio_ffmpeg(file_path, chunk_sec=600)
    else:
        chunks = [file_path]

    # Transcribe each chunk
    transcript_parts = []
    for i, chunk in enumerate(chunks):
        print(f"Transcribing chunk {i+1}/{len(chunks)}: {chunk.name} ...")
        if args.provider == "whisper":
            part = transcribe_whisper(
                chunk,
                model_size=args.model,
                output_format=args.format,
                language=args.language
            )
        else:  # deepgram
            part = transcribe_deepgram(
                chunk,
                output_format=args.format,
                diarize=args.diarize,
                language=args.language
            )
        transcript_parts.append(part)

    # Merge transcripts
    if args.format == "json":
        # For JSON, just concatenate the 'text' fields (simplistic)
        merged = {"text": " ".join([json.loads(p).get("text", "") for p in transcript_parts])}
        final_transcript = json.dumps(merged, ensure_ascii=False, indent=2)
    else:
        final_transcript = "\n".join(transcript_parts)

    # Save transcript
    output_dir = ensure_dir(args.output_dir)
    transcript_path = output_dir / f"transcript_{Path(args.file).stem}.{args.format}"
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(final_transcript)
    print(f"Transcript saved to: {transcript_path}")

    # Save audio if requested
    if args.save_audio:
        audio_dir = ensure_dir(args.audio_dir)
        audio_dest = audio_dir / file_path.name
        shutil.copy2(file_path, audio_dest)
        print(f"Audio saved to: {audio_dest}")

    # Cleanup temp files
    if temp_dir and temp_dir.exists():
        shutil.rmtree(temp_dir)
    if args.split and len(chunks) > 1:
        # remove chunk files (they are in same dir as original or temp)
        for chunk in chunks:
            try:
                chunk.unlink()
            except:
                pass

    print("Done.")
    # Output transcript to stdout as well (so agent can read it)
    print("\n--- Transcript Preview ---")
    preview = final_transcript[:2000] + ("..." if len(final_transcript) > 2000 else "")
    print(preview)

if __name__ == "__main__":
    main()
