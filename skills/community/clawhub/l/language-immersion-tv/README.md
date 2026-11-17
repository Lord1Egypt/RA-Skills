# Language Immersion TV

**Turn movies and TV shows into personalized language-learning material by extracting vocabulary from subtitles and building study decks.**

## The Real-World Problem

Language learning apps teach you generic vocabulary ("the cat is on the table"). But when you watch an actual movie in your target language, you barely understand anything — because real speech uses different words, idioms, and speed than textbooks.

The gap between **textbook language** and **real language** is the #1 frustration for intermediate learners. You've studied for a year, but Netflix in Spanish is still incomprehensible.

The solution: **learn the vocabulary from the specific content you want to watch**. This tool extracts the most frequent, useful words from subtitle files and builds flashcard decks so you can pre-study before watching.

## Who Needs This

- **Language learners (A2–C1)** who want to graduate from textbooks to real media
- **Intermediate plateaus** — learners stuck at "I can read but can't understand speech"
- **Self-directed learners** using TV shows, movies, or YouTube for immersion
- **Language teachers** building lesson material from films
- **Expats and immigrants** learning the local language through TV
- **Anyone using comprehensible input** (Krashen's theory) for language acquisition

## How It Works

1. **Parse** subtitle files (.srt, .vtt) — strip timestamps, HTML tags, and noise
2. **Tokenize** — split dialogue into individual words
3. **Filter** — remove stop words ("the", "is", "and") using language-specific lists
4. **Frequency rank** — count how often each word appears; the most frequent = highest study value
5. **Extract phrases** — detect common collocations and multi-word expressions
6. **Score difficulty** — estimate CEFR level (A1–C1) based on frequency percentile
7. **Export decks** — generate Anki TSV, CSV, or JSON flashcards with the original subtitle sentence as context

## Quick Start

```bash
# Analyze a subtitle file
python scripts/immersion.py analyze movie.srt --language es

# Build a study deck for a TV season
python scripts/immersion.py build-season ~/subs/ --language es --output season_deck.json

# Export Anki-importable flashcards
python scripts/immersion.py export movie.srt --language fr --format anki --output cards.tsv
```

## Example Scenario

**Carlos** is learning English. He loves *Breaking Bad* but can't follow the dialogue. He has 62 episode subtitle files.

1. **Build master list**: `build-season ~/subs/ --language en --output bb_master.json`
   - The tool finds 8,421 unique words across the series. The top 500 words cover 85% of all dialogue.
2. **Export Anki deck**: `export ~/subs/s01e01.srt --language en --format anki`
   - Generates 120 cards: word, frequency, CEFR level, and the original sentence context.
3. **Pre-study**: Carlos studies the deck for episode 1 (30 minutes). He now recognizes the key vocabulary.
4. **Watch**: He watches the episode. Words he just studied appear in context — they stick.
5. **Compare**: `compare ~/subs/ --top 200` shows words that appear across many episodes — his highest-value study targets.

Over a season, Carlos builds a 3,000-word vocabulary deck drawn from content he genuinely enjoys. His listening comprehension jumps from 30% to 70%.

## Why It Works

- **Comprehensible input** (Krashen, 1982): We acquire language best from meaningful content slightly above our level (i+1)
- **Spaced repetition**: Anki decks ensure forgotten words resurface at optimal intervals
- **Contextual learning**: Words learned in sentences stick better than isolated words
- **Motivation**: Studying vocabulary from a show you love is far more engaging than generic lists

## Installation

```bash
git clone https://github.com/voronindenis5/language-immersion-tv.git
cd language-immersion-tv
# No external dependencies required — pure Python
```

## License

MIT — free for personal and educational use.
