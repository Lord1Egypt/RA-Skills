#!/usr/bin/env python3
"""Analyze text files or stdin for word count, character count, line count,
sentence count, reading time, average word length, and readability scores.

Supports Flesch-Kincaid readability metrics. No external dependencies.
"""

import argparse
import json
import math
import re
import sys
import textwrap


def count_syllables(word: str) -> int:
    """Estimate syllable count for an English word."""
    word = word.lower().strip()
    if not word:
        return 0
    if len(word) <= 3:
        return 1

    # Remove trailing silent e
    word = re.sub(r"e$", "", word)

    # Count vowel groups
    vowel_groups = re.findall(r"[aeiouy]+", word)
    count = len(vowel_groups)

    return max(1, count)


def analyze_text(text: str) -> dict:
    """Compute all text statistics."""
    lines = text.split("\n")
    line_count = len(lines)
    non_blank_lines = sum(1 for line in lines if line.strip())

    char_count = len(text)
    char_no_space = len(text.replace(" ", "").replace("\n", "").replace("\t", ""))

    # Words: split on whitespace, filter empty
    words = [w for w in re.split(r"\s+", text) if w]
    word_count = len(words)

    # Clean words (strip punctuation for analysis)
    clean_words = [re.sub(r"[^\w'-]", "", w) for w in words]
    clean_words = [w for w in clean_words if w]

    # Sentences: split on .!? followed by space or end
    sentences = [s.strip() for s in re.split(r"[.!?]+(?:\s|$)", text) if s.strip()]
    sentence_count = max(1, len(sentences))

    # Paragraphs: separated by blank lines
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    paragraph_count = max(1, len(paragraphs))

    # Average word length
    avg_word_length = 0.0
    if clean_words:
        avg_word_length = sum(len(w) for w in clean_words) / len(clean_words)

    # Syllable counts
    total_syllables = sum(count_syllables(w) for w in clean_words)

    # Reading time (average 238 WPM for adults)
    reading_time_min = word_count / 238.0
    speaking_time_min = word_count / 150.0

    # Flesch Reading Ease
    # 206.835 - 1.015 * (words/sentences) - 84.6 * (syllables/words)
    flesch_ease = 0.0
    flesch_grade = 0.0
    if word_count > 0 and sentence_count > 0:
        asl = word_count / sentence_count  # avg sentence length
        asw = total_syllables / word_count  # avg syllables per word
        flesch_ease = 206.835 - 1.015 * asl - 84.6 * asw
        flesch_ease = max(0, min(100, round(flesch_ease, 1)))

        # Flesch-Kincaid Grade Level
        flesch_grade = 0.39 * asl + 11.8 * asw - 15.59
        flesch_grade = max(0, round(flesch_grade, 1))

    # Unique words
    unique_words = len(set(w.lower() for w in clean_words))

    # Longest word
    longest_word = max(clean_words, key=len) if clean_words else ""

    # Difficulty label
    if flesch_ease >= 80:
        difficulty = "Easy"
    elif flesch_ease >= 60:
        difficulty = "Standard"
    elif flesch_ease >= 40:
        difficulty = "Fairly Difficult"
    elif flesch_ease >= 20:
        difficulty = "Difficult"
    else:
        difficulty = "Very Difficult"

    def fmt_time(minutes: float) -> str:
        if minutes < 1:
            return f"{int(minutes * 60)} sec"
        m = int(minutes)
        s = int((minutes - m) * 60)
        if s == 0:
            return f"{m} min"
        return f"{m} min {s} sec"

    return {
        "words": word_count,
        "characters": char_count,
        "characters_no_spaces": char_no_space,
        "lines": line_count,
        "non_blank_lines": non_blank_lines,
        "sentences": sentence_count,
        "paragraphs": paragraph_count,
        "syllables": total_syllables,
        "unique_words": unique_words,
        "avg_word_length": round(avg_word_length, 1),
        "avg_sentence_length": round(word_count / sentence_count, 1) if sentence_count else 0,
        "longest_word": longest_word,
        "reading_time": fmt_time(reading_time_min),
        "speaking_time": fmt_time(speaking_time_min),
        "flesch_reading_ease": flesch_ease,
        "flesch_kincaid_grade": flesch_grade,
        "difficulty": difficulty,
    }


def format_plain(stats: dict, filename: str = "") -> str:
    """Format stats as aligned plain text."""
    header = f"  Stats for: {filename}" if filename else "  Text Statistics"
    lines = [f"\n{header}", f"  {'─' * 40}"]

    labels = {
        "words": "Words",
        "characters": "Characters",
        "characters_no_spaces": "Characters (no spaces)",
        "lines": "Lines",
        "non_blank_lines": "Non-blank Lines",
        "sentences": "Sentences",
        "paragraphs": "Paragraphs",
        "syllables": "Syllables",
        "unique_words": "Unique Words",
        "avg_word_length": "Avg Word Length",
        "avg_sentence_length": "Avg Sentence Length",
        "longest_word": "Longest Word",
        "reading_time": "Reading Time",
        "speaking_time": "Speaking Time",
        "flesch_reading_ease": "Flesch Reading Ease",
        "flesch_kincaid_grade": "Flesch-Kincaid Grade",
        "difficulty": "Difficulty",
    }

    for key, label in labels.items():
        if key not in stats:
            continue
        val = stats[key]
        lines.append(f"  {label:<24} {val}")

    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Text statistics: word count, readability, reading time, and more.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              %(prog)s README.md                    # Analyze a file
              %(prog)s file1.txt file2.txt          # Analyze multiple files
              echo "Hello world" | %(prog)s         # Analyze from stdin
              %(prog)s essay.md -f json             # Output as JSON
              %(prog)s chapter.txt --compact        # Just the key numbers
        """),
    )
    parser.add_argument("files", nargs="*", help="Files to analyze (reads stdin if none)")
    parser.add_argument(
        "-f", "--format", choices=["plain", "json"], default="plain",
        dest="fmt", help="Output format (default: plain)",
    )
    parser.add_argument(
        "--compact", action="store_true",
        help="Show only key stats (words, sentences, reading time, grade)",
    )

    args = parser.parse_args()

    # Gather input
    inputs = []
    if args.files:
        for filepath in args.files:
            try:
                with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                    inputs.append((filepath, f.read()))
            except (FileNotFoundError, IsADirectoryError) as e:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(1)
    else:
        if sys.stdin.isatty():
            print("Error: No files specified and no stdin input.", file=sys.stderr)
            print("Usage: text_stats.py <file> [file2 ...] or pipe text via stdin", file=sys.stderr)
            sys.exit(1)
        inputs.append(("stdin", sys.stdin.read()))

    all_results = []
    for name, text in inputs:
        stats = analyze_text(text)

        if args.compact:
            stats = {k: stats[k] for k in [
                "words", "sentences", "reading_time",
                "flesch_kincaid_grade", "difficulty",
            ]}

        if args.fmt == "json":
            result = {"file": name, **stats} if len(inputs) > 1 else stats
            all_results.append(result)
        else:
            print(format_plain(stats, name if len(inputs) > 1 else ""))

    if args.fmt == "json":
        output = all_results if len(all_results) > 1 else all_results[0]
        print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
