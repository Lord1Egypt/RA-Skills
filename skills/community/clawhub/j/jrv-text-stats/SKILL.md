---
name: text-stats
description: Analyze text files for word count, character count, line count, sentence count, reading time, speaking time, readability scores (Flesch Reading Ease, Flesch-Kincaid Grade Level), and vocabulary statistics. Use when counting words, analyzing readability, estimating reading time, or getting text metrics for documents, essays, blog posts, or any text content.
---

# Text Stats

Analyze text for word count, readability, reading time, and more. Reads files or stdin.

## Quick Start

```bash
# Analyze a file
python3 scripts/text_stats.py README.md

# Multiple files
python3 scripts/text_stats.py file1.txt file2.txt

# From stdin
echo "The quick brown fox jumps over the lazy dog." | python3 scripts/text_stats.py

# JSON output
python3 scripts/text_stats.py essay.md -f json

# Compact (key metrics only)
python3 scripts/text_stats.py chapter.txt --compact
```

## Output Metrics

| Metric | Description |
|--------|-------------|
| Words | Total word count |
| Characters | Total characters (with and without spaces) |
| Lines | Total and non-blank line count |
| Sentences / Paragraphs | Count of each |
| Syllables | Estimated syllable count |
| Unique Words | Vocabulary diversity |
| Avg Word/Sentence Length | Average sizes |
| Reading Time | Estimated at 238 WPM |
| Speaking Time | Estimated at 150 WPM |
| Flesch Reading Ease | 0-100 scale (higher = easier) |
| Flesch-Kincaid Grade | US grade level equivalent |
| Difficulty | Easy / Standard / Fairly Difficult / Difficult / Very Difficult |

## Options

| Flag | Description |
|------|-------------|
| `-f, --format` | `plain` or `json` output |
| `--compact` | Show only words, sentences, reading time, grade, difficulty |

## Notes

- No external dependencies (Python 3 stdlib only)
- Handles UTF-8 text with graceful fallback for encoding errors
- Syllable counting is heuristic-based (English-optimized)
