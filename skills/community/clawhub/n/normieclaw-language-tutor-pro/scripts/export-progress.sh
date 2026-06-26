#!/usr/bin/env bash
set -euo pipefail

# Language Tutor Pro — Export Progress
# Generates a JSON summary of learning stats and vocabulary for dashboard integration.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
DATA_DIR="$SKILL_DIR/data"

if [[ ! -d "$DATA_DIR" ]]; then
    echo "❌ Data directory not found at $DATA_DIR"
    echo "   Run scripts/setup.sh first."
    exit 1
fi

if [[ ! -f "$DATA_DIR/learner-profile.json" ]]; then
    echo "❌ Learner profile not found. Run scripts/setup.sh first."
    exit 1
fi

if ! command -v python3 &>/dev/null; then
    echo "❌ python3 is required. Please install Python 3."
    exit 1
fi

echo "📊 Exporting progress data..."

python3 - "$DATA_DIR" <<'PYEOF'
import json
import os
import sys
from datetime import datetime, timezone

data_dir = sys.argv[1]

with open(os.path.join(data_dir, "learner-profile.json")) as f:
    profile = json.load(f)

def read_jsonl(path):
    items = []
    if os.path.exists(path) and os.path.getsize(path) > 0:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        items.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
    return items

vocab_items = read_jsonl(os.path.join(data_dir, "vocabulary.jsonl"))
grammar_items = read_jsonl(os.path.join(data_dir, "grammar.jsonl"))
sessions = read_jsonl(os.path.join(data_dir, "sessions.jsonl"))

total_minutes = sum(s.get("duration_minutes", 0) for s in sessions)

languages = []
for lang in profile.get("target_languages", []):
    lname = lang["language"]
    lv = [v for v in vocab_items if v.get("language") == lname]
    lg = [g for g in grammar_items if g.get("language") == lname]
    ls = [s for s in sessions if s.get("language") == lname]

    lv_mastered = len([v for v in lv if v.get("correct_streak", 0) >= 5 and v.get("interval_days", 0) >= 30])
    lg_mastered = len([g for g in lg if g.get("status") == "mastered"])
    lang_errors = sum(s.get("errors_corrected", 0) for s in ls)
    lang_total = lang_errors + sum(v.get("correct_streak", 0) for v in lv)

    languages.append({
        "language": lname,
        "level": lang["current_level"],
        "started": lang.get("started"),
        "vocabulary_total": len(lv),
        "vocabulary_mastered": lv_mastered,
        "vocabulary_active": len(lv) - lv_mastered,
        "grammar_rules_total": len(lg),
        "grammar_mastered": lg_mastered,
        "grammar_learning": len(lg) - lg_mastered,
        "total_sessions": len(ls),
        "total_minutes": sum(s.get("duration_minutes", 0) for s in ls),
        "current_streak": profile.get("current_streak_days", 0),
        "longest_streak": profile.get("longest_streak_days", 0),
        "avg_accuracy": round(1 - (lang_errors / max(lang_total, 1)), 2),
        "last_session": ls[-1]["date"] if ls else None,
    })

vm = len([v for v in vocab_items if v.get("correct_streak", 0) >= 5 and v.get("interval_days", 0) >= 30])
gm = len([g for g in grammar_items if g.get("status") == "mastered"])

export = {
    "exported_at": datetime.now(timezone.utc).isoformat(),
    "learner": {
        "native_language": profile.get("native_language"),
        "total_sessions": profile.get("total_sessions", 0),
        "total_minutes": total_minutes,
        "current_streak": profile.get("current_streak_days", 0),
        "longest_streak": profile.get("longest_streak_days", 0),
        "languages": languages,
    },
    "recent_sessions": sessions[-20:],
    "vocabulary_summary": {
        "total": len(vocab_items),
        "mastered": vm,
        "active": len(vocab_items) - vm,
    },
    "grammar_summary": {
        "total": len(grammar_items),
        "mastered": gm,
        "learning": len(grammar_items) - gm,
    },
}

output = os.path.join(data_dir, "dashboard-export.json")
with open(output, "w") as f:
    json.dump(export, f, indent=2)

print(f"✅ Export written to {output}")
print(f"   Languages: {len(languages)}")
print(f"   Vocabulary: {len(vocab_items)} words ({vm} mastered)")
print(f"   Grammar: {len(grammar_items)} rules ({gm} mastered)")
print(f"   Sessions: {len(sessions)} ({total_minutes} minutes total)")
PYEOF
