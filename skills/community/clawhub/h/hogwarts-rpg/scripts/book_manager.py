#!/usr/bin/env python3
"""Buchverwaltung — Built-in-Bücher initialisieren, auflisten, Figuren abfragen."""

import json
import os
import sys

DATA_DIR = os.environ.get("HOGWARTS_DATA_DIR") or os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
BOOKS_DIR = os.path.join(DATA_DIR, "books")
INDEX_FILE = os.path.join(BOOKS_DIR, "_index.json")
# Quelle der Built-in-Daten: data/books/ im Repo
REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_BOOKS_DIR = os.path.join(REPO_DIR, "data", "books")


def ensure_dirs():
    os.makedirs(BOOKS_DIR, exist_ok=True)
    os.makedirs(os.path.join(DATA_DIR, "saves"), exist_ok=True)


def load_index():
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"books": []}


def save_index(index):
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)


def init_builtins():
    """Built-in-Buchdaten in den Runtime-Ordner schreiben."""
    ensure_dirs()
    index = load_index()
    existing_ids = {b["id"] for b in index["books"]}

    builtins = get_builtin_books()
    added = 0

    for book in builtins:
        if book["id"] in existing_ids:
            continue

        book_dir = os.path.join(BOOKS_DIR, book["id"])
        os.makedirs(book_dir, exist_ok=True)
        os.makedirs(os.path.join(book_dir, "chunks"), exist_ok=True)

        # meta.json schreiben
        with open(os.path.join(book_dir, "meta.json"), "w", encoding="utf-8") as f:
            json.dump(book["meta"], f, ensure_ascii=False, indent=2)

        # characters.json schreiben
        with open(os.path.join(book_dir, "characters.json"), "w", encoding="utf-8") as f:
            json.dump(book["characters"], f, ensure_ascii=False, indent=2)

        # plot_graph.json schreiben
        with open(os.path.join(book_dir, "plot_graph.json"), "w", encoding="utf-8") as f:
            json.dump(book["plot_graph"], f, ensure_ascii=False, indent=2)

        index["books"].append({
            "id": book["id"],
            "title": book["meta"]["title"],
            "author": book["meta"]["author"],
            "type": "builtin",
            "status": "ready",
            "character_count": len(book["characters"]["characters"]),
            "chapter_count": len(book["meta"]["chapters"]),
        })
        added += 1

    save_index(index)
    print(f"Initialisierung fertig: {added} neu, {len(index['books'])} Buch/Bücher insgesamt")


def list_books():
    index = load_index()
    if not index["books"]:
        print("Noch keine Bücher. Mit `init-builtins` initialisieren.")
        return
    print(f"{len(index['books'])} Buch/Bücher:\n")
    for b in index["books"]:
        status = "✓" if b["status"] == "ready" else "..."
        print(f"  [{status}] {b['id']} - {b['title']}（{b['author']}）"
              f"  Figuren:{b['character_count']} Kapitel:{b['chapter_count']}")


def show_characters(book_id):
    char_file = os.path.join(BOOKS_DIR, book_id, "characters.json")
    if not os.path.exists(char_file):
        print(f"Buch {book_id} existiert nicht / nicht initialisiert")
        sys.exit(1)

    with open(char_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"Spielbare Figur(en) ({book_id}):\n")
    for c in data["characters"]:
        if c.get("playable", True):
            aliases = "、".join(c.get("aliases", []))
            alias_str = f"（{aliases}）" if aliases else ""
            print(f"  {c['id']} - {c['name']}{alias_str}")
            print(f"    Wesen: {c['personality']}")
            if c.get("abilities"):
                print(f"    Fähigkeiten: {', '.join(c['abilities'])}")
            print()


def get_builtin_books():
    """Built-in-Buchdaten aus den JSON-Dateien laden."""
    builtin_ids = ["hogwarts"]
    books = []
    for book_id in builtin_ids:
        json_path = os.path.join(REPO_BOOKS_DIR, book_id, "builtin_data.json")
        if os.path.exists(json_path):
            with open(json_path, "r", encoding="utf-8") as f:
                books.append(json.load(f))
    return books


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Aufruf: book_manager.py <befehl> [args]")
        print("Befehle: init-builtins | list | characters <book-id>")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "init-builtins":
        init_builtins()
    elif cmd == "list":
        list_books()
    elif cmd == "characters":
        if len(sys.argv) < 3:
            print("Aufruf: book_manager.py characters <book-id>")
            sys.exit(1)
        show_characters(sys.argv[2])
    else:
        print(f"Unbekannter Befehl: {cmd}")
        sys.exit(1)
