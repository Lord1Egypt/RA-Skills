#!/usr/bin/env python3
"""
build-book.py — Baut das komplette OpenClaw-Buch als KDP-PDF
Verwendung: python build-book.py [output.pdf]
            python build-book.py --chapter kapitel-01-final.md [output.pdf]
"""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from md2typ import md2typ
from compile import compile_typst_to_pdf, inject_qr_codes, health_check

# ── Konfiguration ─────────────────────────────────────────────────────────────

KAPITEL_DIR = os.path.expanduser(
    "~/Desktop/openclaw-projekt/buch-review/kapitel"
)

CHAPTER_ORDER = [
    "vorwort-v3-final.md",
    "kapitel-01-final.md",
    "kapitel-02-final.md",
    "kapitel-03-final.md",
    "kapitel-04-final.md",
    "kapitel-05-final.md",
    "kapitel-06-final.md",
    "kapitel-07-final.md",
    "kapitel-08-final.md",
    "kapitel-09-final.md",
    "kapitel-10-final.md",
    "kapitel-11-final.md",
    "kapitel-12-final.md",
    "kapitel-13-final.md",
    "kapitel-13-teil2-final.md",
    "kapitel-13-teil3-final.md",
    "kapitel-14-final.md",
    "kapitel-15-final.md",
]

TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kdp-book.typ.txt")

BOOK_HEADER = """\
#import "kdp-book.typ": *

#show: kdp-setup.with(
  title: "OpenClaw — Agentic Authorship",
  author: "Thomas Iburg",
  subtitle: "Wie KI-Agenten dein Buch schreiben",
  language: "de",
  trim: "6x9",
  page-count-estimate: 300,
  bleed: false,
  body-font: "Inter",
  heading-font: "Inter",
  body-size: 11pt,
  chapters-on-recto: true,
)
"""

IMPORT_HEADER = '#import "kdp-book.typ": *\n\n'

# ── Hilfsfunktionen ───────────────────────────────────────────────────────────

def convert_chapter(md_path):
    """Konvertiert ein Markdown-Kapitel zu Typst (ohne Import-Header)."""
    md_text = open(md_path, encoding="utf-8").read()
    typ_text = md2typ(md_text)
    # Import-Header entfernen — wird einmalig im BOOK_HEADER gesetzt
    if typ_text.startswith(IMPORT_HEADER):
        typ_text = typ_text[len(IMPORT_HEADER):]
    return typ_text


def build_main_typ(chapters):
    """Erzeugt den vollständigen main.typ-Inhalt aus einer Liste von MD-Pfaden."""
    parts = [BOOK_HEADER]
    for md_path in chapters:
        name = os.path.basename(md_path)
        print(f"[build] Konvertiere: {name}")
        body = convert_chapter(md_path)
        parts.append(f"\n// ── {name} ──\n\n{body}")
    return "\n".join(parts)


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]

    # --chapter <datei> [output]
    if args and args[0] == "--chapter":
        if len(args) < 2:
            print("Verwendung: build-book.py --chapter <datei.md> [output.pdf]")
            sys.exit(1)
        md_file = args[1]
        if not os.path.isabs(md_file):
            md_file = os.path.join(KAPITEL_DIR, md_file)
        output_file = args[2] if len(args) > 2 else "output/chapter-test.pdf"
        chapters = [md_file]
        # Für einzelne Kapitel: mit BOOK_HEADER (inkl. kdp-setup)
        main_content = BOOK_HEADER + "\n" + convert_chapter(md_file)
    else:
        output_file = args[0] if args else "output/openclaw-buch.pdf"
        chapters = [os.path.join(KAPITEL_DIR, f) for f in CHAPTER_ORDER]
        for path in chapters:
            if not os.path.exists(path):
                print(f"[build] Fehler: {path} nicht gefunden")
                sys.exit(1)
        main_content = build_main_typ(chapters)

    # Template laden
    if not os.path.exists(TEMPLATE_PATH):
        print(f"[build] Fehler: {TEMPLATE_PATH} nicht gefunden")
        sys.exit(1)
    aux = {"kdp-book.typ": open(TEMPLATE_PATH, encoding="utf-8").read()}

    # QR-Codes injizieren
    print("[build] QR-Codes injizieren...")
    main_content, aux = inject_qr_codes(main_content, aux)

    # API-Check
    if not health_check():
        print("[build] Fehler: TypeTex API nicht erreichbar")
        sys.exit(1)

    # Kompilieren
    os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
    print(f"[build] Kompiliere → {output_file}")
    result = compile_typst_to_pdf(main_content, aux, output_file)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["success"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
