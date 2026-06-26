#!/usr/bin/env python3
"""
Movie advisor — CLI stub for recommend / search / detail flows.

Usage:
    python3 movie_advisor_tool.py recommend [args]
    python3 movie_advisor_tool.py search [args]
    python3 movie_advisor_tool.py detail [args]
"""

import json
import os
import sys
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

# APIs + one aggregator; streaming homepages for agent context (availability is regional).
REF_URLS = [
    "https://developer.themoviedb.org/docs/getting-started",
    "https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/daily-youtube-digest.md",
    "https://www.omdbapi.com/",
    "https://github.com/public-apis/public-apis",
    "https://news.ycombinator.com/item?id=43600632",
    "https://www.justwatch.com",
    "https://www.netflix.com",
    "https://www.youtube.com/movies",
    "https://www.primevideo.com",
    "https://www.disneyplus.com",
    "https://www.max.com",
    "https://tv.apple.com",
    "https://www.hulu.com",
    "https://www.paramountplus.com",
    "https://www.peacocktv.com",
    "https://www.crunchyroll.com",
]


def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def load_data():
    data_file = os.path.join(DATA_DIR, "movie_advisor_data.json")
    if os.path.exists(data_file):
        with open(data_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"records": [], "created": datetime.now().isoformat(), "tool": "movie-advisor"}


def save_data(data):
    ensure_data_dir()
    data_file = os.path.join(DATA_DIR, "movie_advisor_data.json")
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def recommend(args):
    """Recommend movies or shows."""
    data = load_data()
    record = {
        "timestamp": datetime.now().isoformat(),
        "command": "recommend",
        "input": " ".join(args) if args else "",
        "status": "completed",
    }
    data["records"].append(record)
    save_data(data)
    return {
        "status": "success",
        "command": "recommend",
        "message": "Recommendation step completed",
        "record": record,
        "total_records": len(data["records"]),
        "reference_urls": REF_URLS[:8],
    }


def search(args):
    """Search or filter titles."""
    data = load_data()
    record = {
        "timestamp": datetime.now().isoformat(),
        "command": "search",
        "input": " ".join(args) if args else "",
        "status": "completed",
    }
    data["records"].append(record)
    save_data(data)
    return {
        "status": "success",
        "command": "search",
        "message": "Search step completed",
        "record": record,
        "total_records": len(data["records"]),
        "reference_urls": REF_URLS[:8],
    }


def detail(args):
    """Show title details."""
    data = load_data()
    record = {
        "timestamp": datetime.now().isoformat(),
        "command": "detail",
        "input": " ".join(args) if args else "",
        "status": "completed",
    }
    data["records"].append(record)
    save_data(data)
    return {
        "status": "success",
        "command": "detail",
        "message": "Detail step completed",
        "record": record,
        "total_records": len(data["records"]),
        "reference_urls": REF_URLS[:8],
    }


def main():
    cmds = ["recommend", "search", "detail"]
    if len(sys.argv) < 2 or sys.argv[1] not in cmds:
        print(
            json.dumps(
                {
                    "error": f"Usage: movie_advisor_tool.py <{','.join(cmds)}> [args]",
                    "available_commands": {c: "" for c in cmds},
                    "tool": "movie-advisor",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        sys.exit(1)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    if cmd == "recommend":
        result = recommend(args)
    elif cmd == "search":
        result = search(args)
    elif cmd == "detail":
        result = detail(args)
    else:
        result = {"error": f"Unknown command: {cmd}"}

    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
