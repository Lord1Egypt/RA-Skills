#!/usr/bin/env python3
"""
Wartungshelfer: erzeugt aus den handkuratierten Quell-Dateien
(meta.json, characters.json, plot_graph.json) die gebündelte builtin_data.json
sowie data/books/_index.json neu.

Nach jeder inhaltlichen Änderung an den Buch-JSON aufrufen:
    python3 skill/scripts/build_book.py
    python3 skill/scripts/book_manager.py init-builtins   # in den Runtime-Ordner übernehmen
"""
import json
import os

REPO_BOOKS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "books"
)
BOOK_ID = "hogwarts"


def _load(name):
    with open(os.path.join(REPO_BOOKS_DIR, BOOK_ID, name), "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    meta = _load("meta.json")
    chars = _load("characters.json")
    plot = _load("plot_graph.json")

    builtin = {"id": BOOK_ID, "meta": meta, "characters": chars, "plot_graph": plot}
    with open(os.path.join(REPO_BOOKS_DIR, BOOK_ID, "builtin_data.json"), "w", encoding="utf-8") as f:
        json.dump(builtin, f, ensure_ascii=False, indent=2)

    index = {"books": [{
        "id": BOOK_ID,
        "title": meta["title"],
        "author": meta["author"],
        "type": "builtin",
        "status": "ready",
        "character_count": sum(1 for c in chars["characters"] if c.get("playable", True)),
        "chapter_count": len(meta["chapters"]),
    }]}
    with open(os.path.join(REPO_BOOKS_DIR, "_index.json"), "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    scenes = plot["scenes"]
    crossings = sum(1 for s in scenes if s.get("crossing_point"))
    print("builtin_data.json + _index.json neu erzeugt.")
    print(f"  Szenen: {len(scenes)} | Kreuzungspunkte: {crossings} | "
          f"spielbare Figuren: {index['books'][0]['character_count']}")


if __name__ == "__main__":
    main()
