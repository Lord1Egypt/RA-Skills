#!/usr/bin/env python3
import json
import random
import sys
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "kaomojis.json"

def load_db():
    if not DB_PATH.exists():
        return {"version": 1, "items": []}
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def score_item(item, tags):
    score = 0
    tags = set(t.lower() for t in tags)

    for field in ("usage", "tone"):
        for v in item.get(field, []):
            if v.lower() in tags:
                score += 2

    meaning = item.get("meaning", "").lower()
    for t in tags:
        if t in meaning:
            score += 1

    return score

def main():
    tags = sys.argv[1:]
    db = load_db()
    items = db.get("items", [])

    if not items:
        print("")
        return

    scored = [(score_item(item, tags), item) for item in items]
    scored.sort(key=lambda x: x[0], reverse=True)

    best_score = scored[0][0]
    candidates = [item for s, item in scored if s == best_score]

    chosen = random.choice(candidates)
    print(chosen["kaomoji"])

if __name__ == "__main__":
    main()