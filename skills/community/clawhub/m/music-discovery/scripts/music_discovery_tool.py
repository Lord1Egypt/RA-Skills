#!/usr/bin/env python3
"""
Music discovery — CLI stub for recommend / playlist / mood flows.

Usage:
    python3 music_discovery_tool.py recommend [args]
    python3 music_discovery_tool.py playlist [args]
    python3 music_discovery_tool.py mood [args]
"""

import json
import os
import sys
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
DATA_FILE = os.path.join(DATA_DIR, "music_discovery_data.json")
LEGACY_DATA_FILE = os.path.join(DATA_DIR, "music_recommender_data.json")

REF_URLS = [
    "https://developer.spotify.com/documentation/web-api",
    "https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/daily-reddit-digest.md",
    "https://musicbrainz.org/doc/MusicBrainz_API",
    "https://github.com/spotipy-dev/spotipy",
    "https://news.ycombinator.com/item?id=42457780",
]


def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    if os.path.exists(LEGACY_DATA_FILE):
        with open(LEGACY_DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        data["tool"] = "music-discovery"
        save_data(data)
        return data
    return {"records": [], "created": datetime.now().isoformat(), "tool": "music-discovery"}


def save_data(data):
    ensure_data_dir()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def recommend(args):
    """Recommend tracks."""
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
        "reference_urls": REF_URLS[:3],
    }


def playlist(args):
    """Build playlist concept."""
    data = load_data()
    record = {
        "timestamp": datetime.now().isoformat(),
        "command": "playlist",
        "input": " ".join(args) if args else "",
        "status": "completed",
    }
    data["records"].append(record)
    save_data(data)
    return {
        "status": "success",
        "command": "playlist",
        "message": "Playlist step completed",
        "record": record,
        "total_records": len(data["records"]),
        "reference_urls": REF_URLS[:3],
    }


def mood(args):
    """Recommend by mood."""
    data = load_data()
    record = {
        "timestamp": datetime.now().isoformat(),
        "command": "mood",
        "input": " ".join(args) if args else "",
        "status": "completed",
    }
    data["records"].append(record)
    save_data(data)
    return {
        "status": "success",
        "command": "mood",
        "message": "Mood recommendation step completed",
        "record": record,
        "total_records": len(data["records"]),
        "reference_urls": REF_URLS[:3],
    }


def main():
    cmds = ["recommend", "playlist", "mood"]
    if len(sys.argv) < 2 or sys.argv[1] not in cmds:
        print(
            json.dumps(
                {
                    "error": f"Usage: music_discovery_tool.py <{','.join(cmds)}> [args]",
                    "available_commands": {c: "" for c in cmds},
                    "tool": "music-discovery",
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
    elif cmd == "playlist":
        result = playlist(args)
    elif cmd == "mood":
        result = mood(args)
    else:
        result = {"error": f"Unknown command: {cmd}"}

    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
