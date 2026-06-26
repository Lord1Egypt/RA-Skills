#!/usr/bin/env bash
set -euo pipefail

# Language Tutor Pro — Vocab Review Trigger
# Shows vocabulary items due for spaced repetition review.
# Use this to see what's due, then tell your agent "vocab review" to start a session.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
DATA_DIR="$SKILL_DIR/data"
VOCAB_FILE="$DATA_DIR/vocabulary.jsonl"

if [[ ! -f "$VOCAB_FILE" ]]; then
    echo "❌ Vocabulary file not found at $VOCAB_FILE"
    echo "   Run scripts/setup.sh first, then complete a few sessions to build vocabulary."
    exit 1
fi

if [[ ! -s "$VOCAB_FILE" ]]; then
    echo "📚 No vocabulary items yet."
    echo "   Complete a few conversation sessions to start building your word list."
    exit 0
fi

if ! command -v python3 &>/dev/null; then
    echo "❌ python3 is required. Please install Python 3."
    exit 1
fi

# Optional: filter by language
LANGUAGE="${1:-}"

python3 - "$VOCAB_FILE" "$LANGUAGE" <<'PYEOF'
import json
import sys
from datetime import date

vocab_file = sys.argv[1]
lang_filter = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] else None
today = date.today().isoformat()

due = []
upcoming = []
total = 0

with open(vocab_file) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue

        total += 1

        if lang_filter and item.get("language", "").lower() != lang_filter.lower():
            continue

        review_date = item.get("next_review", "")
        if review_date <= today:
            due.append(item)
        elif review_date <= today[:8] + str(int(today[8:]) + 3).zfill(2):
            upcoming.append(item)

# Sort due items: lowest ease factor first (hardest words)
due.sort(key=lambda x: x.get("ease_factor", 2.5))

lang_label = f" ({lang_filter})" if lang_filter else ""
print(f"📚 Vocabulary Review Status{lang_label}")
print("━" * 40)
print(f"Total words tracked: {total}")
print(f"Due for review today: {len(due)}")
print(f"Coming up (next 3 days): {len(upcoming)}")
print()

if due:
    print("🔴 Due Now:")
    for i, item in enumerate(due[:25], 1):
        word = item.get("word", "?")
        translation = item.get("translation", "?")
        lang = item.get("language", "?")
        streak = item.get("correct_streak", 0)
        ease = item.get("ease_factor", 2.5)
        overdue = item.get("next_review", "?")
        difficulty = "🟢" if ease >= 2.5 else "🟡" if ease >= 2.0 else "🔴"
        print(f"  {i:2}. {difficulty} {word} — {translation} [{lang}] (streak: {streak}, due: {overdue})")
    if len(due) > 25:
        print(f"  ... and {len(due) - 25} more")
    print()

if upcoming:
    print("🟡 Coming Soon:")
    for item in upcoming[:10]:
        word = item.get("word", "?")
        translation = item.get("translation", "?")
        review = item.get("next_review", "?")
        print(f"  • {word} — {translation} (due: {review})")
    print()

if due:
    print(f"Tell your agent \"vocab review\" to start a review session with these {len(due)} words.")
elif upcoming:
    print("Nothing due today! Next reviews coming in the next few days.")
else:
    print("No reviews scheduled. Keep practicing to build your vocabulary!")
PYEOF
