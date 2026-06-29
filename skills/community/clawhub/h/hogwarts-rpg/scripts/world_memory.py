#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Welt-Memory (EBENE 3) — AKTIV.

Persistente, kindgerechte Erinnerung an die SELBST ERSCHAFFENEN Sandkasten-Inhalte
der Spielerin: erfundene Nebenfiguren, Lieblingsorte, eigene Mini-Stränge, bedeutsame
Ereignisse. Rein ADDITIV — färbt spätere Sandkasten-Szenen, überschreibt NIE den
Kanon-Faden.

Sicherheits-Prinzipien:
  • MODERATION BEIM SCHREIBEN: Jeder Kandidaten-Fakt läuft durch den Moderation-Layer,
    BEVOR er persistiert wird (nicht erst beim Anzeigen). Geflaggt → NICHT gespeichert,
    Vorfall ins Incident-Log. Bricht die Rückkopplungsschleife (gespeicherter Inhalt
    fließt in spätere Prompts zurück).
  • ELTERN-FENSTER: list / remove / clear — sehen und beschneiden, was sich das Spiel merkt.
  • GUARDRAILS bleiben: Divergenz-Cap, Orts-Whitelist, Kinderbuch-Ton; Fakten sind
    additiv, nie plot-verändernd. KEINE Kanon-Fakten speichern.

Daten-Vertrag  save["world_state"]:
    {"version": 1,
     "facts": [ {"id","typ","text","created_segment","last_seen_segment"} , ... ],
     "summary": <str|None> }   # komprimierte Kurzfassung älterer Fakten (Token-Budget)
  typ ∈ {"npc","ort","ereignis","beziehung"}

CLI:
  world_memory.py add-fact <save> <typ> <text...>   (vom GM in Sandkasten-Szenen)
  world_memory.py list <save>                        (Eltern-Fenster)
  world_memory.py remove <save> <fact-id>            (Eltern-Fenster)
  world_memory.py clear <save>                        (Eltern-Fenster)
  world_memory.py context <save> [ort] [anwesende,kommagetrennt]   (relevante Fakten)
"""
import json
import os
import sys

import game_engine          # gemeinsame Save-Mechanik (eine Quelle der Wahrheit)
import moderation           # Moderation-on-Write

WORLD_STATE_VERSION = 1
VALID_TYPES = {"npc", "ort", "ereignis", "beziehung"}

# ── Tuning (Defaults, freigegeben) ───────────────────────────────────────────
SUMMARIZE_THRESHOLD = 12    # ab so vielen Fakten wird Älteres in summary gefaltet
KEEP_VERBATIM = 8           # so viele jüngste/aktivste Fakten bleiben wörtlich
RECENT_WINDOW = 2           # Fakten der letzten N Segmente gelten als „aktiv"
MAX_ACTIVE_IN_CONTEXT = 8   # Obergrenze relevanter Fakten pro Szene (Token-Budget)


def empty_world_state():
    return {"version": WORLD_STATE_VERSION, "facts": [], "summary": None}


def _ensure_world_state(save):
    """Initialisiert/migriert world_state sauber (alte Saves ohne Feld)."""
    ws = save.get("world_state")
    if not isinstance(ws, dict) or "facts" not in ws:
        ws = empty_world_state()
        save["world_state"] = ws
    ws.setdefault("version", WORLD_STATE_VERSION)
    ws.setdefault("facts", [])
    ws.setdefault("summary", None)
    return ws


def _next_fact_id(ws):
    n = 1
    existing = {f.get("id") for f in ws["facts"]}
    while f"f{n:03d}" in existing:
        n += 1
    return f"f{n:03d}"


# ── 1./2. Fact-Capture mit Moderation-on-Write ───────────────────────────────
def add_fact(save_id, typ, text):
    """Speichert einen Sandkasten-Fakt — NUR wenn die Moderation ihn freigibt.

    Fail-Closed: geflaggter (oder bei Störung nicht freigegebener) Fakt wird NICHT
    gespeichert; der Vorfall landet im Incident-Log. Liefert das gespeicherte
    Fakt-Dict oder None (abgelehnt).
    """
    typ = (typ or "").lower()
    if typ not in VALID_TYPES:
        print(f"✗ Unbekannter Typ '{typ}'. Erlaubt: {', '.join(sorted(VALID_TYPES))}")
        return None
    text = (text or "").strip()
    if not text:
        print("✗ Leerer Fakt — nichts gespeichert.")
        return None

    # MODERATION VOR dem Persistieren (bricht die Rückkopplungsschleife)
    verdict = moderation.moderate(text)
    if verdict["flagged"]:
        moderation.log_incident(text, verdict, context={"source": "world_memory.add_fact",
                                                        "save": save_id, "typ": typ})
        print(f"✗ Fakt abgelehnt (Moderation: {verdict['reason']}). Nicht gespeichert.")
        return None

    save = game_engine.load_save(save_id)
    ws = _ensure_world_state(save)
    seg = int(save.get("segment", 0))
    fact = {"id": _next_fact_id(ws), "typ": typ, "text": text,
            "created_segment": seg, "last_seen_segment": seg}
    ws["facts"].append(fact)
    summarize(save)                      # bei Bedarf Älteres komprimieren
    game_engine.write_save(save_id, save)
    print(f"✓ Fakt gespeichert: {fact['id']} [{typ}] {text}")
    return fact


# ── 4. Kontext-Injektion (nur RELEVANTE Fakten) ──────────────────────────────
def get_context(save, ort=None, segment=None, anwesende=None, touch=False):
    """Liefert die für die aktuelle Szene relevanten Fakten (+ summary für Älteres).

    Relevanz: Ort-Treffer ODER eine anwesende Figur im Fakt-Text ODER jüngstes
    Segment (RECENT_WINDOW). `touch=True` aktualisiert `last_seen_segment` der
    aufgetauchten Fakten (hält häufig referenzierte „aktiv").
    """
    ws = _ensure_world_state(save)
    seg = int(segment if segment is not None else save.get("segment", 0))
    anwesende = [a.lower() for a in (anwesende or []) if a]
    ortl = (ort or "").lower()

    active = []
    for f in ws["facts"]:
        txt = f.get("text", "").lower()
        recent = isinstance(f.get("last_seen_segment"), int) and f["last_seen_segment"] >= seg - RECENT_WINDOW
        loc_match = bool(ortl) and ortl in txt
        char_match = any(a in txt for a in anwesende)
        if recent or loc_match or char_match:
            active.append(f)

    # jüngste zuerst; Einfüge-Reihenfolge (Index in facts) als Tiebreaker
    order = {id(f): i for i, f in enumerate(ws["facts"])}
    active.sort(key=lambda f: (f.get("last_seen_segment", 0), f.get("created_segment", 0), order.get(id(f), 0)), reverse=True)
    active = active[:MAX_ACTIVE_IN_CONTEXT]
    if touch:
        for f in active:
            f["last_seen_segment"] = seg

    return {
        "aktive_fakten": [{"id": f["id"], "typ": f["typ"], "text": f["text"]} for f in active],
        "summary": ws.get("summary"),
    }


# ── 5. Summarization / Token-Budget ──────────────────────────────────────────
def summarize(save):
    """Faltet ältere/inaktive Fakten in `summary`, hält jüngste/aktivste verbatim.

    Wird automatisch in add_fact aufgerufen, sobald > SUMMARIZE_THRESHOLD Fakten
    vorliegen. Häufig referenzierte (jüngstes last_seen) bleiben bevorzugt erhalten.
    """
    ws = _ensure_world_state(save)
    facts = ws["facts"]
    if len(facts) <= SUMMARIZE_THRESHOLD:
        return save
    # jüngste zuerst; Einfüge-Reihenfolge als Tiebreaker (gleiche Segmente)
    indexed = sorted(enumerate(facts),
                     key=lambda p: (p[1].get("last_seen_segment", 0), p[1].get("created_segment", 0), p[0]),
                     reverse=True)
    ordered = [f for _, f in indexed]
    keep = ordered[:KEEP_VERBATIM]
    old = ordered[KEEP_VERBATIM:]
    parts = []
    if ws.get("summary"):
        parts.append(ws["summary"])
    parts.extend(f"{f['typ']}: {f['text']}" for f in old)
    ws["summary"] = " · ".join(p for p in parts if p)
    ws["facts"] = keep
    return save


# ── 3. Eltern-Fenster ────────────────────────────────────────────────────────
def list_facts(save_id):
    save = game_engine.load_save(save_id)
    ws = _ensure_world_state(save)
    print(f"=== Welt-Memory von {save_id} ===")
    if not ws["facts"] and not ws.get("summary"):
        print("  (noch leer)")
    for f in ws["facts"]:
        print(f"  {f['id']} [{f['typ']}] {f['text']}  (Segment {f.get('created_segment')}→{f.get('last_seen_segment')})")
    if ws.get("summary"):
        print(f"\n  Zusammengefasst (älter): {ws['summary']}")


def remove_fact(save_id, fact_id):
    save = game_engine.load_save(save_id)
    ws = _ensure_world_state(save)
    before = len(ws["facts"])
    ws["facts"] = [f for f in ws["facts"] if f.get("id") != fact_id]
    game_engine.write_save(save_id, save)
    if len(ws["facts"]) < before:
        print(f"✓ Fakt {fact_id} entfernt.")
    else:
        print(f"  Fakt {fact_id} nicht gefunden.")


def clear_facts(save_id):
    save = game_engine.load_save(save_id)
    save["world_state"] = empty_world_state()
    game_engine.write_save(save_id, save)
    print(f"✓ Welt-Memory von {save_id} komplett geleert.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Aufruf: world_memory.py <befehl> [args]")
        print("  add-fact <save> <typ> <text...>   Sandkasten-Fakt (moderiert) speichern")
        print("  list <save>                       alle Fakten anzeigen (Eltern)")
        print("  remove <save> <fact-id>           einen Fakt löschen (Eltern)")
        print("  clear <save>                      Welt-Memory leeren (Eltern)")
        print("  context <save> [ort] [anwesende]  relevante Fakten (kommagetrennt)")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "add-fact":
        if len(sys.argv) < 5:
            print("Aufruf: world_memory.py add-fact <save> <typ> <text...>")
            sys.exit(1)
        res = add_fact(sys.argv[2], sys.argv[3], " ".join(sys.argv[4:]))
        sys.exit(0 if res else 2)
    elif cmd == "list":
        list_facts(sys.argv[2])
    elif cmd == "remove":
        remove_fact(sys.argv[2], sys.argv[3])
    elif cmd == "clear":
        clear_facts(sys.argv[2])
    elif cmd == "context":
        save = game_engine.load_save(sys.argv[2])
        ort = sys.argv[3] if len(sys.argv) > 3 else None
        anw = sys.argv[4].split(",") if len(sys.argv) > 4 else []
        ctx = get_context(save, ort=ort, segment=save.get("segment"), anwesende=anw, touch=True)
        game_engine.write_save(sys.argv[2], save)   # last_seen-Touch persistieren
        print(json.dumps(ctx, ensure_ascii=False, indent=2))
    else:
        print(f"Unbekannter Befehl: {cmd}")
        sys.exit(1)
