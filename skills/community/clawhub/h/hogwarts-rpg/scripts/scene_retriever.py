#!/usr/bin/env python3
"""Szenen-Kontext-Abruf — token-sparende Kernkomponente für den GM."""

import json
import os
import sys

DATA_DIR = os.environ.get("HOGWARTS_DATA_DIR") or os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
# Saves liegen persistent außerhalb des Skills (überleben Reinstalls) — wie game_engine
STATE_DIR = os.environ.get("HOGWARTS_STATE_DIR") or os.environ.get("HOGWARTS_DATA_DIR") or os.path.expanduser("~/.openclaw/hogwarts-state")
BOOKS_DIR = os.path.join(DATA_DIR, "books")
SAVES_DIR = os.path.join(STATE_DIR, "saves")


def load_json(path):
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_scene(plot, scene_id):
    for s in plot.get("scenes", []):
        if s["id"] == scene_id:
            return s
    return None


def get_adjacent_scenes(plot, scene_id):
    """Zusammenfassung der vorigen/nächsten Szene holen."""
    scenes = plot.get("scenes", [])
    prev_scene = None
    next_scene = None
    for i, s in enumerate(scenes):
        if s["id"] == scene_id:
            if i > 0:
                prev_scene = scenes[i - 1]
            if i < len(scenes) - 1:
                next_scene = scenes[i + 1]
            break
    return prev_scene, next_scene


def context(book_id, scene_id):
    """Vollständigen Szenen-Kontext liefern (für den GM)."""
    book_dir = os.path.join(BOOKS_DIR, book_id)
    meta = load_json(os.path.join(book_dir, "meta.json"))
    chars = load_json(os.path.join(book_dir, "characters.json"))
    plot = load_json(os.path.join(book_dir, "plot_graph.json"))

    if not plot:
        print(f"Buchdaten für {book_id} existieren nicht")
        sys.exit(1)

    scene = get_scene(plot, scene_id)
    if not scene:
        print(f"Szene {scene_id} existiert nicht")
        sys.exit(1)

    prev_scene, next_scene = get_adjacent_scenes(plot, scene_id)

    # Kapitel-Info holen
    chapter_info = None
    if meta:
        for ch in meta.get("chapters", []):
            if ch["number"] == scene.get("chapter"):
                chapter_info = ch
                break

    # Info zu anwesenden Figuren holen
    present_chars = []
    if chars:
        char_ids = scene.get("characters_present", [])
        for c in chars.get("characters", []):
            if c["id"] in char_ids:
                present_chars.append({
                    "name": c["name"],
                    "personality": c["personality"],
                    "abilities": c.get("abilities", []),
                })

    # Prüfen, ob Textbausteine vorhanden sind (importierte Bücher)
    chunk_file = os.path.join(book_dir, "chunks", f"{scene_id}.txt")
    chunk_text = None
    if os.path.exists(chunk_file):
        with open(chunk_file, "r", encoding="utf-8") as f:
            chunk_text = f.read()

    # Strukturierten Kontext ausgeben
    output = {
        "book": meta.get("title", book_id) if meta else book_id,
        "chapter": chapter_info.get("title", "") if chapter_info else "",
        "chapter_number": scene.get("chapter", 0),
        "scene": {
            "id": scene["id"],
            "title": scene["title"],
            "location": scene.get("location", ""),
            "summary": scene.get("summary", ""),
            "plot_type": scene.get("plot_type", ""),
            "challenge_potential": scene.get("challenge_potential", 3),
        },
        "characters_present": present_chars,
        "choices": scene.get("choices", []),
        "previous_scene": prev_scene["summary"] if prev_scene else None,
        "next_scene_hint": next_scene["title"] if next_scene else "Ende der Geschichte",
    }

    if chunk_text:
        output["original_text"] = chunk_text

    print(json.dumps(output, ensure_ascii=False, indent=2))


def character(book_id, character_id, scene_id=None):
    """Figuren-Info liefern."""
    book_dir = os.path.join(BOOKS_DIR, book_id)
    chars = load_json(os.path.join(book_dir, "characters.json"))

    if not chars:
        print(f"Figurendaten für {book_id} existieren nicht")
        sys.exit(1)

    for c in chars.get("characters", []):
        if c["id"] == character_id:
            output = {
                "name": c["name"],
                "aliases": c.get("aliases", []),
                "personality": c["personality"],
                "abilities": c.get("abilities", []),
                "relationships": c.get("relationships", {}),
                "arc_summary": c.get("arc_summary", ""),
            }
            print(json.dumps(output, ensure_ascii=False, indent=2))
            return

    print(f"Figur {character_id} existiert nicht")


def lookahead(book_id, scene_id, count=3):
    """Folgeszenen vorausschauen (Planungshilfe für den GM)."""
    book_dir = os.path.join(BOOKS_DIR, book_id)
    plot = load_json(os.path.join(book_dir, "plot_graph.json"))

    if not plot:
        print(f"Buchdaten für {book_id} existieren nicht")
        sys.exit(1)

    scenes = plot.get("scenes", [])
    found = False
    upcoming = []

    for s in scenes:
        if found:
            upcoming.append({
                "id": s["id"],
                "title": s["title"],
                "plot_type": s.get("plot_type", ""),
                "challenge_potential": s.get("challenge_potential", 3),
                "summary": s.get("summary", "")[:60] + "...",
            })
            if len(upcoming) >= count:
                break
        if s["id"] == scene_id:
            found = True

    if not upcoming:
        print("Bereits die letzte Szene")
    else:
        print(json.dumps(upcoming, ensure_ascii=False, indent=2))


def sandbox_context(book_id, location, save_id=None):
    """Liefert den Leitplanken-Kontext für eine freie SANDKASTEN-Szene.

    Kernidee: Freie Bewegung heißt freier ORT, niemals freies THEMA. Dieser Block
    nagelt Setting, Ort, Schuljahr-Abschnitt und Ton fest, damit der GM in den
    Lücken zwischen den Beats erzählen kann, ohne die Welt zu verlassen.

    EBENE-3-SEAM: `world_state_summary` wird (falls ein Spielstand übergeben ist)
    schon mitgelesen — in V1 ist es None/leer. Hier dockt später das wachsende
    Welt-Memory an (selbst erschaffene Figuren/Orte/Stränge, komprimiert).
    """
    book_dir = os.path.join(BOOKS_DIR, book_id)
    meta = load_json(os.path.join(book_dir, "meta.json")) or {}
    locs_data = load_json(os.path.join(book_dir, "locations.json")) or {"locations": []}
    locs = locs_data.get("locations", [])
    by_id = {l["id"]: l for l in locs}
    by_name = {l["name"].lower(): l for l in locs}
    loc = by_id.get(location) or by_name.get((location or "").lower())

    # Nächster Beat + Schuljahr-Abschnitt + Welt-Memory aus dem Spielstand
    next_beat = None
    welt_memory = {"aktive_fakten": [], "summary": None}
    if save_id:
        save_path = os.path.join(SAVES_DIR, f"{save_id}.json")
        save = load_json(save_path)
        if save:
            plot = load_json(os.path.join(book_dir, "plot_graph.json")) or {}
            for s in plot.get("scenes", []):
                if s["id"] == save.get("current_scene"):
                    next_beat = {"id": s["id"], "title": s.get("title"),
                                 "school_time": s.get("school_time")}
                    break
            # EBENE-3-Seam AKTIV: nur relevante Welt-Memory-Fakten injizieren
            import world_memory
            welt_memory = world_memory.get_context(
                save, ort=(loc["name"] if loc else None),
                segment=save.get("segment"), anwesende=[], touch=True)
            with open(save_path, "w", encoding="utf-8") as f:   # last_seen-Touch persistieren
                json.dump(save, f, ensure_ascii=False, indent=2)

    output = {
        "mode": "sandbox",
        "setting": locs_data.get("setting", "Schloss Hogwarts, altersgerecht (~12)"),
        "location": {
            "id": loc["id"], "name": loc["name"],
            "context": loc.get("context", ""), "access": loc.get("access", "tagsueber"),
        } if loc else None,
        "location_invalid": loc is None,
        "allowed_locations": [{"id": l["id"], "name": l["name"]} for l in locs],
        "next_beat": next_beat,
        "tone": "altersgerecht (~12), Niveau der HP-Buecher/Filme: spannend, darf gruseln und verliebt sein",
        "guardrails": [
            "Freier ORT, niemals freies THEMA (altersgerecht ~12).",
            "Nur Schauplätze der Whitelist; die Welt/das Setting nie verlassen.",
            "Moderation läuft auch über Sandkasten-Szenen (Pflicht).",
            "Divergenz-neutral: Sandkasten überschreibt den Hauptplot nicht.",
        ],
        # Ebene-3-Seam AKTIV: relevante Sandkasten-Fakten (verbatim) + summary (älter)
        "welt_memory": welt_memory,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Aufruf: scene_retriever.py <befehl> [args]")
        print("Befehle:")
        print("  context <book-id> <scene-id>                    Szenen-Kontext holen")
        print("  character <book-id> <character-id> [scene-id]   Figuren-Info holen")
        print("  lookahead <book-id> <scene-id> [count]          Folgeszenen vorausschauen")
        print("  sandbox-context <book-id> <ort> [save-id]       Sandkasten-Leitplanke")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "context":
        if len(sys.argv) < 4:
            print("Aufruf: scene_retriever.py context <book-id> <scene-id>")
            sys.exit(1)
        context(sys.argv[2], sys.argv[3])
    elif cmd == "character":
        if len(sys.argv) < 4:
            print("Aufruf: scene_retriever.py character <book-id> <character-id> [scene-id]")
            sys.exit(1)
        sid = sys.argv[4] if len(sys.argv) > 4 else None
        character(sys.argv[2], sys.argv[3], sid)
    elif cmd == "lookahead":
        if len(sys.argv) < 4:
            print("Aufruf: scene_retriever.py lookahead <book-id> <scene-id> [count]")
            sys.exit(1)
        cnt = int(sys.argv[4]) if len(sys.argv) > 4 else 3
        lookahead(sys.argv[2], sys.argv[3], cnt)
    elif cmd == "sandbox-context":
        if len(sys.argv) < 4:
            print("Aufruf: scene_retriever.py sandbox-context <book-id> <ort> [save-id]")
            sys.exit(1)
        sid = sys.argv[4] if len(sys.argv) > 4 else None
        sandbox_context(sys.argv[2], sys.argv[3], sid)
    else:
        print(f"Unbekannter Befehl: {cmd}")
        sys.exit(1)
