#!/usr/bin/env python3
"""Ergebnis nach Testnamen und Beispieldaten durchsuchen.

Beim Entwickeln braucht man ein konkretes Beispiel. Es darf nur nicht im
Ergebnis landen: Ein Werkzeug mit dem Testkonto des Entwicklers im Code ist
fuer den Nutzer wertlos. Dieser Fehler faellt einem selbst nicht auf, weil man
den Namen hundertmal gelesen hat — deshalb pruefen statt erinnern.

    python check_no_hardcode.py . --forbid meintestkonto --forbid 12345
    python check_no_hardcode.py . --forbid meintestkonto --keep data/

Rueckgabewert 1, wenn etwas gefunden wurde — damit es in einer Pruefkette
auffaellt.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build", ".idea"}
SKIP_SUFFIX = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf", ".zip",
               ".gz", ".woff", ".woff2", ".ttf", ".mp4", ".mp3", ".pyc", ".so", ".dll"}


def walk(root: pathlib.Path, keep: list[str]):
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() in SKIP_SUFFIX:
            continue
        rel = path.relative_to(root)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if any(str(rel).replace("\\", "/").startswith(k.rstrip("/") + "/") or str(rel) == k
               for k in keep):
            continue
        yield path, rel


def main() -> int:
    ap = argparse.ArgumentParser(description="Testnamen und Beispieldaten aufspueren")
    ap.add_argument("root", nargs="?", default=".", help="Ordner (Standard: hier)")
    ap.add_argument("--forbid", action="append", default=[], metavar="TEXT",
                    help="verbotener Text, mehrfach angebbar")
    ap.add_argument("--keep", action="append", default=[], metavar="PFAD",
                    help="Pfad ausnehmen, z. B. data/ mit echten Nutzerdaten")
    ap.add_argument("--quiet", action="store_true", help="nur Treffer ausgeben")
    args = ap.parse_args()

    if not args.forbid:
        print("Nichts zu suchen — mindestens ein --forbid angeben.", file=sys.stderr)
        return 2

    root = pathlib.Path(args.root).resolve()
    patterns = [(t, re.compile(re.escape(t), re.IGNORECASE)) for t in args.forbid]
    hits: list[tuple[str, int, str, str]] = []
    scanned = 0

    for path, rel in walk(root, args.keep):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        scanned += 1
        for lineno, line in enumerate(text.splitlines(), 1):
            for term, rx in patterns:
                if rx.search(line):
                    hits.append((str(rel).replace("\\", "/"), lineno, term, line.strip()[:110]))

    if not args.quiet:
        print(f"{scanned:,} Dateien durchsucht in {root}")
        if args.keep:
            print(f"ausgenommen: {', '.join(args.keep)}")

    if not hits:
        print(f"Sauber — keiner der {len(args.forbid)} Begriffe kommt vor.")
        return 0

    print(f"\n{len(hits)} Treffer:\n")
    current = None
    for rel, lineno, term, line in hits:
        if rel != current:
            print(f"  {rel}")
            current = rel
        print(f"    Zeile {lineno:>4}  [{term}]  {line}")

    print("\nJeden Treffer durch ein Eingabefeld oder einen neutralen Platzhalter"
          "\nersetzen (creator, beispiel, <name>). Echte Nutzerdaten gehoeren nicht"
          "\nhierher — solche Ordner mit --keep ausnehmen.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
