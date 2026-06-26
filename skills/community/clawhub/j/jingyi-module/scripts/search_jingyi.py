import argparse
import json
import pathlib
import re
import sys


BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
INDEX_FILE = BASE_DIR / "data" / "command_index.jsonl"


def tokenize(text: str):
    parts = re.split(r"[\s_/\-，。；、（）()\[\]【】]+", text.lower())
    return [p for p in parts if p]


def load_index():
    if not INDEX_FILE.exists():
        raise FileNotFoundError(f"index file not found: {INDEX_FILE}")
    items = []
    with INDEX_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            items.append(json.loads(line))
    return items


def score_item(query: str, item: dict) -> int:
    q = query.lower().strip()
    score = 0
    name = item.get("name", "").lower()
    short_name = item.get("short_name", "").lower()
    path = item.get("canonical_path", "").lower()
    summary = item.get("summary", "").lower()
    keywords = " ".join(item.get("keywords", [])).lower()

    if q == name:
        score += 200
    if q == short_name and short_name:
        score += 180
    if q in name:
        score += 120
    if q in short_name and short_name:
        score += 100
    if q in path:
        score += 80
    if q in summary:
        score += 40
    if q in keywords:
        score += 30

    for token in tokenize(q):
        if token in name:
            score += 35
        if token in short_name and short_name:
            score += 28
        if token in path:
            score += 20
        if token in summary:
            score += 8
        if token in keywords:
            score += 12

    return score


def main():
    parser = argparse.ArgumentParser(description="Search 精易模块 command index")
    parser.add_argument("query", help="search keyword")
    parser.add_argument("--top", type=int, default=8)
    args = parser.parse_args()

    try:
        items = load_index()
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False, indent=2))
        sys.exit(1)

    ranked = []
    for item in items:
        score = score_item(args.query, item)
        if score > 0:
            ranked.append((score, item))

    ranked.sort(
        key=lambda x: (
            -x[0],
            len(x[1].get("short_name", "") or x[1].get("name", "")),
            x[1].get("id", 0),
        )
    )
    result = []
    for score, item in ranked[: args.top]:
        result.append(
            {
                "id": item.get("id"),
                "name": item.get("name"),
                "short_name": item.get("short_name"),
                "canonical_path": item.get("canonical_path"),
                "cmdtype": item.get("cmdtype"),
                "score": score,
                "summary": item.get("summary", ""),
            }
        )

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
