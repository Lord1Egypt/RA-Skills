#!/bin/bash
# Check Learning Progress
# Usage: ./check_progress.sh [topic-slug]
# Without args: shows all active learning topics
# With topic-slug: shows detailed status for that topic

set -euo pipefail

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
LEARNING_DIR="${WORKSPACE}/memory/learning"

if [ ! -d "$LEARNING_DIR" ]; then
    echo "No learning topics found. Directory does not exist: $LEARNING_DIR"
    exit 0
fi

show_topic() {
    local topic_dir="$1"
    local slug
    slug=$(basename "$topic_dir")
    local state_file="${topic_dir}/state.json"

    if [ ! -f "$state_file" ]; then
        echo "  [!] No state.json found"
        return
    fi

    # Parse state.json with python (available on most systems)
    python3 - "$state_file" <<'PYEOF' 2>/dev/null || echo "  [!] Could not parse state.json"
import json, sys
with open(sys.argv[1]) as f:
    s = json.load(f)
topic = s.get('topic', 'unknown')
status = s.get('status', 'unknown')
day = s.get('currentDay', '?')
session = s.get('currentSession', '?')
idx = s.get('currentSubtopicIndex', 0)
curr = s.get('curriculum', [])
subtopic = curr[idx] if idx < len(curr) else 'N/A'
total = len(curr)
mastered = sum(1 for h in s.get('history', []) if h.get('mastered'))
history = s.get('history', [])
avg_s2 = avg_s4 = 0
if history:
    s2_scores = [h['s2Score'] for h in history if 's2Score' in h and h['s2Score'] is not None]
    s4_scores = [h['s4Score'] for h in history if 's4Score' in h and h['s4Score'] is not None]
    avg_s2 = sum(s2_scores) / len(s2_scores) if s2_scores else 0
    avg_s4 = sum(s4_scores) / len(s4_scores) if s4_scores else 0
print(f'  Topic:    {topic}')
print(f'  Status:   {status}')
print(f'  Day:      {day} | Session: {session}')
print(f'  Progress: {mastered}/{total} subtopics mastered')
print(f'  Current:  {subtopic}')
if history:
    print(f'  Avg S2:   {avg_s2:.0f}% | Avg S4: {avg_s4:.0f}% | Avg improvement: {avg_s4-avg_s2:+.0f}%')
    last = history[-1]
    ls2 = last.get('s2Score', '?')
    ls4 = last.get('s4Score', '?')
    print(f'  Last day: S2={ls2}% S4={ls4}%')
PYEOF
}

if [ $# -ge 1 ]; then
    # Show specific topic
    TOPIC_DIR="${LEARNING_DIR}/$1"
    if [ ! -d "$TOPIC_DIR" ]; then
        echo "Topic not found: $1"
        echo "Available topics:"
        ls -1 "$LEARNING_DIR" 2>/dev/null || echo "  (none)"
        exit 1
    fi
    echo "=== Learning Progress: $1 ==="
    show_topic "$TOPIC_DIR"
else
    # Show all topics
    echo "=== Active Learning Topics ==="
    echo ""
    found=0
    for topic_dir in "${LEARNING_DIR}"/*/; do
        [ -d "$topic_dir" ] || continue
        slug=$(basename "$topic_dir")
        echo "--- ${slug} ---"
        show_topic "$topic_dir"
        echo ""
        found=$((found + 1))
    done
    if [ "$found" -eq 0 ]; then
        echo "No learning topics found."
    else
        echo "Total: ${found} topic(s)"
    fi
fi
