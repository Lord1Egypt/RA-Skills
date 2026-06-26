#!/usr/bin/env python3
import json
import sys
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "kaomojis.json"

def load_db():
    if not DB_PATH.exists():
        return {"version": 1, "items": []}
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(db):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

def normalize_list(x):
    if x is None:
        return []
    if isinstance(x, list):
        return [str(i).strip() for i in x if str(i).strip()]
    return [s.strip() for s in str(x).split(",") if s.strip()]

def upsert_kaomoji(kaomoji, meaning, usage=None, tone=None):
    db = load_db()
    usage = normalize_list(usage)
    tone = normalize_list(tone)

    for item in db["items"]:
        if item["kaomoji"] == kaomoji:
            if meaning:
                item["meaning"] = meaning
            if usage:
                item["usage"] = sorted(set(item.get("usage", []) + usage))
            if tone:
                item["tone"] = sorted(set(item.get("tone", []) + tone))
            save_db(db)
            return {"status": "updated", "item": item}

    item = {
        "kaomoji": kaomoji,
        "meaning": meaning or "",
        "usage": usage,
        "tone": tone,
    }
    db["items"].append(item)
    save_db(db)
    return {"status": "created", "item": item}

def main():
    if len(sys.argv) < 3:
        print("Usage: save_kaomoji.py <kaomoji> <meaning> [usage_csv] [tone_csv]")
        sys.exit(1)

    kaomoji = sys.argv[1]
    meaning = sys.argv[2]
    usage = sys.argv[3] if len(sys.argv) > 3 else ""
    tone = sys.argv[4] if len(sys.argv) > 4 else ""

    result = upsert_kaomoji(kaomoji, meaning, usage, tone)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()