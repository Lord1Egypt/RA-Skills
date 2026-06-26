#!/usr/bin/env python3
"""
Generate SRT/ASS/VTT subtitle files from transcription JSON output.

Usage:
  python3 generate_srt.py <transcript.json> <output.srt> [options]

Supported input formats: Whisper, Deepgram, AssemblyAI, generic {word,start,end} lists.
Supported output formats: .srt, .ass, .vtt (auto-detected from extension).
"""

import json
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Optional, Any


def format_srt_ts(seconds: float) -> str:
    """Convert seconds to SRT timestamp (HH:MM:SS,mmm)."""
    if seconds < 0:
        seconds = 0
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def format_vtt_ts(seconds: float) -> str:
    """Convert seconds to VTT timestamp (HH:MM:SS.mmm)."""
    return format_srt_ts(seconds).replace(",", ".")


def format_ass_ts(seconds: float) -> str:
    """Convert seconds to ASS timestamp (H:MM:SS.cc)."""
    if seconds < 0:
        seconds = 0
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int((seconds % 1) * 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def chunk_words(words: list, max_chars: int = 42, max_words: int = 8,
                max_duration: float = 6.0) -> list:
    """Group words into subtitle chunks based on character and word limits.

    Args:
        words: List of word dictionaries with 'word', 'start', 'end' keys
        max_chars: Maximum characters per subtitle line
        max_words: Maximum words per subtitle line
        max_duration: Maximum duration for a single subtitle in seconds

    Returns:
        List of chunk dictionaries with 'text', 'start', 'end' keys
    """
    chunks = []
    current_words = []
    current_text = ""
    chunk_start = None
    chunk_end = None

    def flush_chunk():
        """Add current chunk to chunks list and reset state."""
        nonlocal current_words, current_text, chunk_start, chunk_end
        if current_words and chunk_start is not None:
            chunks.append({
                "text": current_text,
                "start": chunk_start,
                "end": chunk_end if chunk_end else (current_words[-1].get("end", chunk_start + 1))
            })
        current_words = []
        current_text = ""
        chunk_start = None
        chunk_end = None

    for word_info in words:
        word = word_info.get("word", word_info.get("text", "")).strip()
        start = float(word_info.get("start", 0))
        end = float(word_info.get("end", start + 0.5))

        if not word:
            continue

        test_text = f"{current_text} {word}".strip() if current_text else word
        duration = end - (chunk_start if chunk_start else start)

        # Flush if exceeds any limit
        should_flush = False
        if current_words:
            if len(test_text) > max_chars:
                should_flush = True
            elif len(current_words) >= max_words:
                should_flush = True
            elif duration > max_duration:
                should_flush = True

        if should_flush:
            flush_chunk()
            # After flush, recompute test_text from the now-empty buffer so
            # the next chunk does not inherit the previous chunk's text.
            test_text = word

        # Start new chunk if needed
        if chunk_start is None:
            chunk_start = start

        current_words.append(word_info)
        current_text = test_text
        chunk_end = end

    # Flush remaining chunk
    if current_words:
        flush_chunk()

    return chunks


def generate_srt(chunks: list) -> str:
    """Generate SRT format subtitle content."""
    lines = []
    for i, c in enumerate(chunks, 1):
        lines.append(f"{i}")
        lines.append(f"{format_srt_ts(c['start'])} --> {format_srt_ts(c['end'])}")
        lines.append(c["text"])
        lines.append("")
    return "\n".join(lines)


def generate_vtt(chunks: list) -> str:
    """Generate VTT format subtitle content."""
    lines = ["WEBVTT", ""]
    for i, c in enumerate(chunks, 1):
        lines.append(f"{i}")
        lines.append(f"{format_vtt_ts(c['start'])} --> {format_vtt_ts(c['end'])}")
        lines.append(c["text"])
        lines.append("")
    return "\n".join(lines)


def generate_ass(chunks: list, font: str = "Arial", fontsize: int = 24,
                 primary: str = "&H00FFFFFF", outline: str = "&H00000000",
                 backcolor: str = "&H80000000") -> str:
    """Generate ASS format subtitle content."""
    header = f"""[Script Info]
Title: Auto-generated subtitles
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{font},{fontsize},{primary},&H000000FF,{outline},{backcolor},-1,0,0,0,100,100,0,0,1,2,1,2,20,20,50,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"""
    lines = [header]
    for c in chunks:
        text = c["text"].replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}")
        lines.append(f"Dialogue: 0,{format_ass_ts(c['start'])},{format_ass_ts(c['end'])},Default,,0,0,0,,{text}")
    return "\n".join(lines)


class TranscriptFormatError(ValueError):
    """Raised when a transcript JSON file has a recognisable shape but a
    malformed field value (e.g. non-numeric start/end). Carries a short,
    user-facing message instead of a Python traceback."""


def _safe_float(value: Any, default: float, field: str) -> float:
    """Coerce value to float, raising a clean TranscriptFormatError on failure."""
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        raise TranscriptFormatError(
            f"transcript field '{field}' must be a number, got {value!r}"
        )


def parse_transcript(data: Any) -> list:
    """Extract word-level timing from various transcription JSON formats.

    Supported formats:
    - Whisper (with segments containing words)
    - Whisper (with segments containing text only)
    - Deepgram (with channels and alternatives)
    - AssemblyAI (with words array)
    - Generic list of {word/text, start, end}

    Raises:
      TranscriptFormatError if a recognised field has a non-numeric
      start/end value (caught in main() and turned into exit code 2).
    """
    words = []

    if isinstance(data, list):
        if not data:
            return words

        # Check if it's a direct list of words
        first_item = data[0]
        if isinstance(first_item, dict) and ("word" in first_item or "text" in first_item):
            for item in data:
                word = item.get("word", item.get("text", "")).strip()
                if word:
                    start = _safe_float(item.get("start", 0), 0.0, "start")
                    end = _safe_float(item.get("end", start + 0.5), start + 0.5, "end")
                    words.append({"word": word, "start": start, "end": end})
            return words

        # Extract words from segments
        for seg in data:
            if "words" in seg and isinstance(seg["words"], list):
                for w in seg["words"]:
                    word = w.get("word", w.get("text", "")).strip()
                    if word:
                        start = _safe_float(w.get("start", 0), 0.0, "start")
                        end = _safe_float(w.get("end", start + 0.5), start + 0.5, "end")
                        words.append({"word": word, "start": start, "end": end})
            elif "text" in seg and "start" in seg:
                text = seg.get("text", "").strip()
                start = _safe_float(seg.get("start", 0), 0.0, "start")
                end = _safe_float(seg.get("end", start + 1), start + 1.0, "end")
                seg_words = text.split()
                if seg_words:
                    dur = (end - start) / len(seg_words) if len(seg_words) > 1 else 0.5
                    for j, w in enumerate(seg_words):
                        words.append({
                            "word": w,
                            "start": start + j * dur,
                            "end": start + (j + 1) * dur
                        })

        return words

    if isinstance(data, dict):
        # Whisper format with segments
        if "segments" in data and isinstance(data["segments"], list):
            for seg in data["segments"]:
                if "words" in seg and isinstance(seg["words"], list):
                    for w in seg["words"]:
                        word = w.get("word", w.get("text", "")).strip()
                        if word:
                            start = _safe_float(w.get("start", 0), 0.0, "start")
                            end = _safe_float(w.get("end", start + 0.5), start + 0.5, "end")
                            words.append({"word": word, "start": start, "end": end})
                else:
                    text = seg.get("text", "").strip()
                    start = _safe_float(seg.get("start", 0), 0.0, "start")
                    end = _safe_float(seg.get("end", start + 1), start + 1.0, "end")
                    seg_words = text.split()
                    if seg_words:
                        dur = (end - start) / len(seg_words) if len(seg_words) > 1 else 0.5
                        for j, w in enumerate(seg_words):
                            words.append({
                                "word": w,
                                "start": start + j * dur,
                                "end": start + (j + 1) * dur
                            })
            return words

        # Deepgram format
        if "results" in data and isinstance(data["results"], dict):
            results = data["results"]
            if "channels" in results:
                for ch in results.get("channels", []):
                    if "alternatives" in ch:
                        for alt in ch["alternatives"]:
                            if "words" in alt:
                                for w in alt["words"]:
                                    word = w.get("word", w.get("punctuated_word", "")).strip()
                                    if word:
                                        start = _safe_float(w.get("start", 0), 0.0, "start")
                                        end = _safe_float(w.get("end", start + 0.5), start + 0.5, "end")
                                        words.append({"word": word, "start": start, "end": end})
            elif "words" in results:
                for w in results["words"]:
                    word = w.get("word", w.get("punctuated_word", "")).strip()
                    if word:
                        start = _safe_float(w.get("start", 0), 0.0, "start")
                        end = _safe_float(w.get("end", start + 0.5), start + 0.5, "end")
                        words.append({"word": word, "start": start, "end": end})
            return words

        # AssemblyAI or simple format
        if "words" in data and isinstance(data["words"], list):
            for w in data["words"]:
                word = w.get("word", w.get("text", "")).strip()
                if word:
                    start = _safe_float(w.get("start", 0), 0.0, "start")
                    end = _safe_float(w.get("end", start + 0.5), start + 0.5, "end")
                    words.append({"word": word, "start": start, "end": end})
            return words

        # Single utterance format
        if "text" in data and "start" in data:
            text = data["text"].strip()
            start = _safe_float(data.get("start", 0), 0.0, "start")
            end = _safe_float(data.get("end", start + 1), start + 1.0, "end")
            seg_words = text.split()
            if seg_words:
                dur = (end - start) / len(seg_words) if len(seg_words) > 1 else 0.5
                for j, w in enumerate(seg_words):
                    words.append({
                        "word": w,
                        "start": start + j * dur,
                        "end": start + (j + 1) * dur
                    })
            return words

    return words


def validate_input_file(filepath: str) -> bool:
    """Validate that input file exists and is readable."""
    path = Path(filepath)
    if not path.exists():
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        return False
    if not path.is_file():
        print(f"Error: Not a file: {filepath}", file=sys.stderr)
        return False
    if path.stat().st_size == 0:
        print(f"Error: File is empty: {filepath}", file=sys.stderr)
        return False
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Generate subtitles from transcription JSON",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage with Whisper JSON
  python3 generate_srt.py transcript.json subtitles.srt

  # Custom styling for ASS format
  python3 generate_srt.py transcript.json subtitles.ass --font "Helvetica" --fontsize 28

  # Adjust chunk settings for different languages
  python3 generate_srt.py transcript.json subtitles.srt --max-chars 60 --max-words 10

Supported transcription formats:
  - OpenAI Whisper (with word-level timing)
  - Deepgram API
  - AssemblyAI
  - Generic JSON with word, start, end fields
        """
    )
    parser.add_argument("input", help="Path to transcription JSON file")
    parser.add_argument("output", help="Output path (.srt, .vtt, or .ass)")
    parser.add_argument("--max-chars", type=int, default=42,
                       help="Max characters per line (default: 42)")
    parser.add_argument("--max-words", type=int, default=8,
                       help="Max words per line (default: 8)")
    parser.add_argument("--max-duration", type=float, default=6.0,
                       help="Max duration per subtitle in seconds (default: 6.0)")
    parser.add_argument("--font", default="Arial",
                       help="Font name for ASS format (default: Arial)")
    parser.add_argument("--fontsize", type=int, default=24,
                       help="Font size for ASS format (default: 24)")
    parser.add_argument("--quiet", "-q", action="store_true",
                       help="Suppress non-error output")

    args = parser.parse_args()

    # Validate input
    if not validate_input_file(args.input):
        sys.exit(1)

    # Read and parse JSON
    try:
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {args.input}: {e}", file=sys.stderr)
        sys.exit(1)
    except UnicodeDecodeError:
        # Try with different encoding
        try:
            with open(args.input, "r", encoding="latin-1") as f:
                data = json.load(f)
        except Exception as e:
            print(f"Error: Cannot read {args.input}: {e}", file=sys.stderr)
            sys.exit(1)

    # Extract words from transcript
    try:
        words = parse_transcript(data)
    except TranscriptFormatError as e:
        print(f"Error: malformed transcript: {e}", file=sys.stderr)
        sys.exit(2)
    if not words:
        print("Error: Could not extract word timings from transcript.", file=sys.stderr)
        print("Supported formats: Whisper, Deepgram, AssemblyAI, or list of {word, start, end}.", file=sys.stderr)
        sys.exit(2)

    # Chunk words into subtitle segments
    chunks = chunk_words(
        words,
        max_chars=args.max_chars,
        max_words=args.max_words,
        max_duration=args.max_duration
    )

    if not chunks:
        print("Error: No subtitle chunks generated.", file=sys.stderr)
        sys.exit(1)

    # Generate output based on file extension
    ext = Path(args.output).suffix.lower()
    allowed_exts = {".srt", ".vtt", ".ass"}
    if ext not in allowed_exts:
        print(
            f"Error: unsupported output extension {ext!r}. "
            f"Allowed: {', '.join(sorted(allowed_exts))}.",
            file=sys.stderr,
        )
        sys.exit(2)

    try:
        if ext == ".vtt":
            content = generate_vtt(chunks)
        elif ext == ".ass":
            content = generate_ass(
                chunks,
                font=args.font,
                fontsize=args.fontsize
            )
        else:
            content = generate_srt(chunks)

        # Ensure output directory exists
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write output
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(content)

        if not args.quiet:
            duration = chunks[-1]["end"] if chunks else 0
            print(f"Generated {len(chunks)} subtitle entries ({ext}) → {args.output}")
            print(f"  Total duration: {duration:.1f}s")
            print(f"  Settings: max_chars={args.max_chars}, max_words={args.max_words}, max_duration={args.max_duration}s")

    except IOError as e:
        print(f"Error: Cannot write to {args.output}: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
