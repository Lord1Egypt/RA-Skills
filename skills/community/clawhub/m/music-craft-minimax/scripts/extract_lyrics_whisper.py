#!/usr/bin/env python3
"""extract_lyrics_whisper.py — Extract lyrics with timestamps from audio.

Uses OpenAI's Whisper model (openai-whisper pip package, MIT license) to
transcribe lyrics and return them as a structured body ready for structure-tagging.

Usage:
    python3 extract_lyrics_whisper.py /tmp/song.wav [--model medium] [--language en] [--output out.json]

Important — Whisper is not in the standard `python3`.
This script does `import whisper`. It will fail immediately on any Python
that does not have the `openai-whisper` package installed. The skill rule
is: do not auto-install. Find the right Python first.

How to find the right Python (any machine):
    which whisper
    # -> e.g. /opt/homebrew/bin/whisper, /usr/local/bin/whisper, ~/.local/bin/whisper
    head -1 "$(which whisper)"
    # -> shebang line tells you the working Python
    # Then call this script with that Python, for example:
    /opt/homebrew/bin/python3.11 scripts/extract_lyrics_whisper.py /tmp/song.mp3 --model medium

Output: JSON with:
  - raw_transcript: full text
  - segments: list of {start, end, text} time-stamped segments
  - section_tags: list of section labels parallel to segments
  - tagged_lyrics: segments joined with [Verse] / [Chorus] tags
  - model_used: which Whisper model ran
  - duration_seconds: audio length
  - sanity_warnings: list of risk patterns detected (looping hallucination,
    language mismatch, low vocabulary variety). ALWAYS read these before
    treating the transcript as final.

If openai-whisper is not installed, the script outputs {"error": "openai-whisper not installed",
"install": "pip install openai-whisper"} and exits 0 (not an error — the skill falls back).

Whisper model sizes (tradeoff: speed vs accuracy):
  - tiny:   ~75 MB, fast, lower accuracy
  - base:   ~150 MB, balanced
  - small:  ~500 MB, good accuracy
  - medium: ~1.5 GB, very good (DEFAULT)
  - large:  ~3 GB, best

Default: medium. CPU works but is slow; use small only for drafts.
"""
import sys
import json
import argparse
from collections import Counter

try:
    import whisper
    HAS_WHISPER = True
except ImportError:
    HAS_WHISPER = False


DEFAULT_WHISPER_MODEL = 'medium'


def lyrics_sanity_warnings(transcript, detected_language=None, expected_language=None, segments=None):
    """Return warnings for common Whisper hallucination patterns."""
    warnings = []
    detected = (detected_language or "").lower()
    expected = (expected_language or "").lower()
    if detected and expected and detected != expected:
        warnings.append(f"language mismatch: Whisper detected {detected_language}, expected {expected_language}")

    segment_texts = [str(seg.get('text', '')).strip().lower() for seg in (segments or []) if str(seg.get('text', '')).strip()]
    if len(segment_texts) >= 3:
        counts = Counter(segment_texts)
        most_common_text, most_common_count = counts.most_common(1)[0]
        if most_common_count >= 3 or most_common_count / len(segment_texts) >= 0.6:
            warnings.append(f"possible looping hallucination: repeated segment '{most_common_text[:80]}'")

    words = str(transcript or '').lower().split()
    if 20 <= len(words) <= 120:
        unique_ratio = len(set(words)) / max(len(words), 1)
        if unique_ratio < 0.35:
            warnings.append("possible looping hallucination: transcript has unusually low vocabulary variety")

    return warnings


def detect_repeated_sections(segments, similarity_threshold=0.6):
    """Detect repeated lyric sections (verses that recur).

    Compares segment text using a simple word-set Jaccard similarity.
    When a segment is similar to a previous one, it gets a [Verse X] tag
    and the original gets the same number. This is a heuristic, not perfect.

    Returns: list of section tags in same order as segments.
    """
    if not segments:
        return []

    def word_set(text):
        return set(text.lower().split())

    section_map = {}  # frozenset of words -> section number
    next_section = 1
    tags = []

    for seg in segments:
        words = word_set(seg['text'])
        matched = None
        for prev_words, sec_num in section_map.items():
            intersection = len(words & prev_words)
            union = len(words | prev_words) + 1e-9
            similarity = intersection / union
            if similarity >= similarity_threshold and len(words) > 3:
                matched = sec_num
                break

        if matched is None:
            section_map[frozenset(words)] = next_section
            tags.append(next_section)
            next_section += 1
        else:
            tags.append(matched)

    type_cycle = ['Verse', 'Chorus', 'Verse 2', 'Chorus 2', 'Bridge', 'Verse 3', 'Chorus 3', 'Outro']
    final_tags = []
    for sec_num in tags:
        if sec_num <= len(type_cycle):
            final_tags.append(type_cycle[sec_num - 1])
        else:
            final_tags.append(type_cycle[-1])

    return final_tags


def format_tagged_lyrics(segments, tags):
    """Convert segments + section tags into a MiniMax-ready lyrics body."""
    if not segments:
        return ""

    lines = ["[Intro]", "(instrumental)", ""]
    current_tag = None
    current_block = []

    for seg, tag in zip(segments, tags):
        text = seg['text'].strip()
        if not text:
            continue
        if tag != current_tag:
            if current_block:
                lines.append(f"[{current_tag}]")
                lines.extend(current_block)
                lines.append("")
            current_tag = tag
            current_block = [text]
        else:
            current_block.append(text)

    if current_block:
        lines.append(f"[{current_tag}]")
        lines.extend(current_block)
        lines.append("")

    return "\n".join(lines)


def transcribe(audio_path, model_name=DEFAULT_WHISPER_MODEL, language=None):
    """Run Whisper transcription on the audio file."""
    if not HAS_WHISPER:
        return {
            "error": "openai-whisper not installed",
            "install": "pip install openai-whisper",
        }

    try:
        model = whisper.load_model(model_name)
        options = {}
        if language:
            options['language'] = language
        result = model.transcribe(audio_path, **options)

        segments = [
            {
                'start_seconds': round(seg['start'], 2),
                'end_seconds': round(seg['end'], 2),
                'text': seg['text'].strip(),
            }
            for seg in result.get('segments', [])
        ]

        tags = detect_repeated_sections(segments)
        tagged = format_tagged_lyrics(segments, tags)

        sanity_warnings = lyrics_sanity_warnings(
            result.get('text', '').strip(),
            detected_language=result.get('language'),
            expected_language=language,
            segments=segments,
        )

        return {
            'model_used': model_name,
            'language': result.get('language'),
            'raw_transcript': result.get('text', '').strip(),
            'segments': segments,
            'section_tags': tags,
            'tagged_lyrics': tagged,
            'sanity_warnings': sanity_warnings,
            'duration_seconds': round(segments[-1]['end_seconds'], 1) if segments else 0,
        }
    except Exception as e:
        return {
            "error": f"Whisper transcription failed: {str(e)}",
            "model_attempted": model_name,
        }


def main():
    parser = argparse.ArgumentParser(description='Extract lyrics from audio using Whisper')
    parser.add_argument('audio', help='Audio file path (WAV/MP3/FLAC)')
    parser.add_argument('--model', default=DEFAULT_WHISPER_MODEL,
                        choices=['tiny', 'base', 'small', 'medium', 'large'],
                        help=f'Whisper model size (default: {DEFAULT_WHISPER_MODEL})')
    parser.add_argument('--language', default=None, help='Language code (e.g., en, es) or auto-detect')
    parser.add_argument('--output', help='Output JSON file path')
    args = parser.parse_args()

    print(f"Transcribing: {args.audio} (model={args.model})", file=sys.stderr)
    result = transcribe(args.audio, args.model, args.language)

    if 'error' in result and 'segments' not in result:
        print(f"ERROR: {result['error']}", file=sys.stderr)
        if 'install' in result:
            print(f"Install with: {result['install']}", file=sys.stderr)

    json_out = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        with open(args.output, 'w') as f:
            f.write(json_out)
        print(f"Written: {args.output}", file=sys.stderr)
    else:
        print(json_out)


if __name__ == '__main__':
    main()
