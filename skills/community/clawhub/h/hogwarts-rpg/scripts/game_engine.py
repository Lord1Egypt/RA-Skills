#!/usr/bin/env python3
"""
Spiel-Engine — Spielstand-Verwaltung, Zustands-Fortschritt, Attribut-Berechnung.

Hogwarts-Variante (kindgerecht). Erweiterungen gegenüber dem novel-rpg-Original:
  1. DIVERGENZ-CAP (hart): Die Abweichung vom Kanon ist bei DIVERGENCE_CAP gedeckelt.
     Ist der Cap erreicht, wird `divergence_locked` gesetzt — ab dann sind KEINE
     Nicht-Kanon-Pfade mehr erlaubt; die Engine erzwingt den kanonischen Weg.
  2. BEZIEHUNGS-TIERS: Zu jeder Hauptfigur wird ein Status Fremde→Bekannt→Freund
     getrackt (abgeleitet aus `trust`).
  3. KREUZUNGSPUNKTE: An markierten Beats (`crossing_point`) kann die Spielerin an
     den Kanon „andocken". Genutzte Kreuzungen erhöhen einen Cliquen-Bindungszähler;
     „Teil der Clique" entsteht über eine Schwelle (CLIQUE_THRESHOLD), nie über einen
     einzelnen Schalter.

Die Engine ist bewusst deterministisch und ohne Netz-Zugriff. Die Erzählung selbst
erzeugt der Spielleiter (GM); dieses Skript verwaltet nur den Zustand.
"""

import json
import os
import sys
from datetime import datetime

DATA_DIR = os.environ.get("HOGWARTS_DATA_DIR") or os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
# Spielstände/Status liegen PERSISTENT außerhalb des Skills, damit ein Reinstall
# (skills install --force, das data/ überschreibt) sie NIE löscht. Bücher kommen
# weiter aus dem Skill (DATA_DIR/books), Content-Updates greifen also normal.
STATE_DIR = os.environ.get("HOGWARTS_STATE_DIR") or os.environ.get("HOGWARTS_DATA_DIR") or os.path.expanduser("~/.openclaw/hogwarts-state")
SAVES_DIR = os.path.join(STATE_DIR, "saves")
BOOKS_DIR = os.path.join(DATA_DIR, "books")

# ── Sicherheits-/Spielkonstanten (Hogwarts) ───────────────────────────────────
DIVERGENCE_CAP = 30        # HARTE Obergrenze der Abweichung (Auftrag: max. 30/100)
DIVERGENCE_STEP = 5        # Zuwachs pro Nicht-Kanon-Wahl
CLIQUE_THRESHOLD = 3       # informativer Bindungs-Schwellenwert (Anzeige)

# „Teil der Clique" (verschärfte Regel, V1):
#   mindestens CLIQUE_CROSSINGS_MIN genutzte Kreuzungspunkte UND
#   Beziehung zu JEDER Kern-Figur >= „Freund". Kein einzelner Schalter.
CLIQUE_CROSSINGS_MIN = 2
CORE_FRIENDS = ["Harry", "Ron", "Hermine"]   # Freundeskreis ist HAUSÜBERGREIFEND

# Frei wählbare Häuser (an der Hut-Zeremonie). Freundschaften/Clique sind
# bewusst nicht an das Haus gebunden — man kann in jedem Haus Teil der Clique werden.
HOUSES = ["Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"]

# Beziehungs-Stufen, abgeleitet aus trust (0-100)
REL_TIERS = [
    (0,  "Fremde"),
    (40, "Bekannt"),
    (70, "Freund"),
]


def tier_for_trust(trust):
    """Liefert den Beziehungs-Status-Namen für einen trust-Wert."""
    name = REL_TIERS[0][1]
    for threshold, label in REL_TIERS:
        if trust >= threshold:
            name = label
    return name


def recompute_clique(save):
    """Berechnet den „Teil der Clique"-Status nach der verschärften Regel.

    Bedingung: genug GENUTZTE Kreuzungspunkte UND alle Kern-Figuren (Harry, Ron,
    Hermine) jeweils mindestens auf Stufe „Freund". Setzt `in_clique` und vergibt
    einmalig den Erfolg. Ein Herabfallen unter die Bedingung setzt den Status
    bewusst NICHT zurück (einmal Freundeskreis, immer Freundeskreis).
    """
    enough_crossings = len(save.get("crossings_used", [])) >= CLIQUE_CROSSINGS_MIN
    rels = save.get("relationships", {})
    all_friends = all(
        rels.get(name, {}).get("status") == "Freund" for name in CORE_FRIENDS
    )
    if enough_crossings and all_friends and not save.get("in_clique"):
        save["in_clique"] = True
        if "Teil der Clique" not in save["achievements"]:
            save["achievements"].append("Teil der Clique")
    return save.get("in_clique", False)


def load_locations(book_id):
    """Lädt die Orts-Whitelist eines Buches (Sandkasten-Schauplätze)."""
    path = os.path.join(BOOKS_DIR, book_id, "locations.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"locations": []}


def ensure_dirs():
    os.makedirs(SAVES_DIR, exist_ok=True)


def load_save(save_id):
    path = os.path.join(SAVES_DIR, f"{save_id}.json")
    if not os.path.exists(path):
        print(f"Spielstand {save_id} existiert nicht")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_save(save_id, data):
    data["updated_at"] = datetime.now().isoformat()
    path = os.path.join(SAVES_DIR, f"{save_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_book_data(book_id):
    """Lädt Figuren- und Szenendaten eines Buches."""
    book_dir = os.path.join(BOOKS_DIR, book_id)
    chars = {}
    plot = {}
    char_file = os.path.join(book_dir, "characters.json")
    plot_file = os.path.join(book_dir, "plot_graph.json")
    if os.path.exists(char_file):
        with open(char_file, "r", encoding="utf-8") as f:
            chars = json.load(f)
    if os.path.exists(plot_file):
        with open(plot_file, "r", encoding="utf-8") as f:
            plot = json.load(f)
    return chars, plot


def _find_char(chars, character_id):
    for c in chars.get("characters", []):
        if c["id"] == character_id:
            return c
    return None


# ── Onboarding / Protagonist-Profil ──────────────────────────────────────────
# Geschlecht ist frei wählbar; Pronomen werden daraus abgeleitet und der Erzählung
# (SKILL.md) mitgegeben, damit die Spielfigur durchgehend richtig angesprochen wird.
PRONOUNS = {
    "weiblich": {"subjekt": "sie", "akkusativ": "sie", "dativ": "ihr",
                 "possessiv": "ihre", "anrede": "Mädchen"},
    "männlich": {"subjekt": "er", "akkusativ": "ihn", "dativ": "ihm",
                 "possessiv": "sein", "anrede": "Junge"},
    # neutral: keine gegenderten Pronomen — die Erzählung nutzt den Namen.
    "divers":  {"subjekt": "", "akkusativ": "", "dativ": "",
                "possessiv": "", "anrede": "Kind"},
}


def _normalize_gender(value):
    """Mappt freie Eingaben auf weiblich | männlich | divers (Default: weiblich)."""
    v = (value or "").strip().lower()
    if v in ("m", "männlich", "maennlich", "junge", "male", "boy", "j"):
        return "männlich"
    if v in ("w", "f", "weiblich", "mädchen", "maedchen", "female", "girl"):
        return "weiblich"
    if v in ("d", "divers", "neutral", "keine", "nonbinary", "non-binary", "enby"):
        return "divers"
    return "weiblich"


def _parse_profile_flags(rest):
    """Liest optionale Onboarding-Flags aus den restlichen CLI-Argumenten.

    Unterstützt: --name, --gender, --home/--hometown, --pet-name, --pet-kind.
    Gibt ein Dict mit nur den gesetzten Schlüsseln zurück (None-Werte fallen raus).
    """
    aliases = {"--home": "--hometown"}
    keys = {
        "--name": "name", "--gender": "gender", "--hometown": "hometown",
        "--pet-name": "pet_name", "--pet-kind": "pet_kind",
    }
    profile, i = {}, 0
    while i < len(rest):
        flag = aliases.get(rest[i], rest[i])
        if flag in keys and i + 1 < len(rest):
            profile[keys[flag]] = rest[i + 1]
            i += 2
        else:
            i += 1
    return profile


def _apply_profile(save_data, char_data, profile):
    """Wendet das Onboarding-Profil auf einen frischen Spielstand an.

    Setzt Name/Geschlecht/Heimatort/Haustier, leitet Pronomen ab und benennt die
    Begleiter-Beziehung um, falls das Haustier umgetauft wurde. Fehlende Felder
    fallen auf die Vorgaben der Figur zurück (Robin / Flocke / kleines Dorf).
    """
    profile = profile or {}
    default_pet = char_data.get("companion") or "Flocke"

    name = (profile.get("name") or "").strip() or char_data["name"]
    gender = _normalize_gender(profile.get("gender") or "weiblich")
    hometown = (profile.get("hometown") or "").strip() or "ein kleines Dorf"
    pet_name = (profile.get("pet_name") or "").strip() or default_pet
    pet_kind = (profile.get("pet_kind") or "").strip() or "Malteser-Hündchen"

    save_data["protagonist"] = {
        "name": name,
        "gender": gender,
        "pronouns": dict(PRONOUNS[gender]),
        "hometown": hometown,
        "pet": {"name": pet_name, "kind": pet_kind},
    }
    save_data["character_name"] = name
    save_data["companion"] = pet_name

    # Haustier umgetauft → Begleiter-Beziehung mit umbenennen, Notiz aktualisieren.
    rels = save_data.get("relationships", {})
    if pet_name != default_pet and default_pet in rels:
        rels[pet_name] = rels.pop(default_pet)
    if pet_name in rels:
        rels[pet_name]["note"] = f"dein treuer Begleiter ({pet_kind}), weicht dir nicht von der Seite"
    return save_data


def new_game(book_id, character_id, profile=None):
    """Erstellt ein neues Spiel.

    In der Hogwarts-Variante spielt man die EIGENE Protagonistin (z. B. der Char
    mit `is_player: true` in characters.json). Hauptfiguren wie Harry sind
    Nebenfiguren (playable:false) und werden hier als Beziehungs-Anker angelegt.
    """
    ensure_dirs()
    chars, plot = load_book_data(book_id)

    char_data = _find_char(chars, character_id)
    if not char_data:
        print(f"Figur {character_id} existiert nicht in {book_id}")
        sys.exit(1)

    scenes = plot.get("scenes", [])
    first_scene = scenes[0]["id"] if scenes else "y1_s01"

    save_id = _new_save_id()
    save_data = {
        "save_id": save_id,
        "book_id": book_id,
        "character_id": character_id,
        "character_name": char_data["name"],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "current_scene": first_scene,
        "chapter_progress": 1,
        # ── Sandkasten / Position ─────────────────────────────────────────────
        "current_location": None,      # aktueller Sandkasten-Ort (None = im Beat)
        "segment": 0,                  # Lücke zwischen Beat K und K+1 (linear, V1)
        "stats": dict(char_data.get("initial_stats", {
            "wisdom": 50, "combat": 50, "loyalty": 50, "reputation": 50
        })),
        "choices_made": [],
        "relationships": {},
        "divergence_score": 0,
        "divergence_locked": False,
        # ── Story-State (Persistenz „schlank", V1) ────────────────────────────
        "beats_completed": [],         # IDs abgeschlossener Kanon-Beats
        "crossings_used": [],          # genutzte Kreuzungspunkte (angedockt)
        "crossings_missed": [],        # verpasste Kreuzungspunkte (autonom gelaufen)
        "clique_bond": 0,              # informativer Bindungszähler (Anzeige)
        "in_clique": False,            # via recompute_clique() (verschärfte Regel)
        "achievements": [],
        "inventory": list(char_data.get("abilities", [])),
        "companion": char_data.get("companion"),   # persistenter Begleiter (z. B. Flocke)
        "house": char_data.get("house"),           # festes Haus (z. B. Gryffindor)
        "session_log": [],
        # ── Ebene-3-Seam: Welt-Memory (V1 inert, nur Andockpunkt) ─────────────
        "world_state": {"version": 1, "facts": [], "summary": None}
    }

    # Beziehungen initialisieren. Wert kann ein String (Notiz, Start 50 = Bekannt)
    # ODER ein Dict {"note":..., "start_trust":N} sein — so starten z. B. Lily auf
    # „Freund" und Harry/Ron/Hermine auf „Fremde".
    for name, val in char_data.get("relationships", {}).items():
        if isinstance(val, dict):
            trust = int(val.get("start_trust", 50))
            note = val.get("note", "")
        else:
            trust = 50
            note = val
        trust = max(0, min(100, trust))
        save_data["relationships"][name] = {
            "trust": trust,
            "status": tier_for_trust(trust),
            "note": note,
        }

    # Onboarding-Profil anwenden (Name/Geschlecht/Heimatort/Haustier).
    _apply_profile(save_data, char_data, profile)

    write_save(save_id, save_data)

    book_title = _book_title(book_id)
    prot = save_data["protagonist"]
    print("Neues Spiel erstellt!")
    print(f"  Spielstand-ID: {save_id}")
    print(f"  Buch: {book_title}")
    print(f"  Figur: {prot['name']} ({prot['gender']}) aus {prot['hometown']}")
    print(f"  Haustier: {prot['pet']['name']} ({prot['pet']['kind']})")
    print(f"  Startszene: {first_scene}")
    print(f"  Attribute: {json.dumps(save_data['stats'], ensure_ascii=False)}")


def _new_save_id():
    """Deterministische, kollisionsarme Save-ID ohne uuid (gut testbar)."""
    ensure_dirs()
    existing = {f[:-5] for f in os.listdir(SAVES_DIR) if f.endswith(".json")}
    n = 1
    while f"save{n:03d}" in existing:
        n += 1
    return f"save{n:03d}"


def advance(save_id, scene_id, choice_index, choice_desc=""):
    """Schreitet den Spielzustand fort."""
    save = load_save(save_id)
    chars, plot = load_book_data(save["book_id"])

    scene = None
    for s in plot.get("scenes", []):
        if s["id"] == scene_id:
            scene = s
            break
    if not scene:
        print(f"Warnung: Szene {scene_id} nicht gefunden — freier Fortschritt")

    choice_index = int(choice_index)

    is_canon = False
    stat_effects = {}
    relationship_effects = {}
    chosen_house = None
    choices = scene.get("choices", []) if scene else []
    if choices and choice_index < len(choices):
        choice = choices[choice_index]
        is_canon = choice.get("canon", False)
        stat_effects = choice.get("stat_effects", {})
        relationship_effects = choice.get("relationship_effects", {})
        chosen_house = choice.get("house")   # z. B. bei der Hut-Zeremonie
        if not choice_desc:
            choice_desc = choice.get("description", "")

    # ── DIVERGENZ-CAP (hart) ──────────────────────────────────────────────────
    # Ist die Abweichung bereits gedeckelt, wird eine Nicht-Kanon-Wahl NICHT als
    # Abweichung gewertet — die Geschichte bleibt auf Schienen. Der GM darf laut
    # SKILL.md oberhalb des Caps ohnehin keine Nicht-Kanon-Optionen mehr anbieten;
    # diese Engine-Sperre ist der zweite, harte Riegel.
    divergence_rejected = False
    if not is_canon:
        if save.get("divergence_locked"):
            divergence_rejected = True   # zählt nicht, kein weiterer Abdrift
        else:
            save["divergence_score"] = min(DIVERGENCE_CAP, save["divergence_score"] + DIVERGENCE_STEP)
            if save["divergence_score"] >= DIVERGENCE_CAP:
                save["divergence_locked"] = True

    # Attribute aktualisieren
    for stat, delta in stat_effects.items():
        if stat in save["stats"]:
            save["stats"][stat] = max(0, min(100, save["stats"][stat] + delta))

    # Beziehungen aktualisieren (inkl. Tier-Neuberechnung)
    for name, delta in relationship_effects.items():
        if name in save["relationships"]:
            rel = save["relationships"][name]
            rel["trust"] = max(0, min(100, rel["trust"] + delta))
            rel["status"] = tier_for_trust(rel["trust"])
        else:
            trust = max(0, min(100, 50 + delta))
            save["relationships"][name] = {
                "trust": trust,
                "status": tier_for_trust(trust),
                "note": "neu kennengelernt",
            }

    # ── HAUS (Hut-Zeremonie) ──────────────────────────────────────────────────
    # Trägt die gewählte Wahl ein `house`-Feld (z. B. an der Einsortierung), wird
    # das Haus jetzt ECHT im Spielstand gesetzt — frei wählbar aus allen vier Häusern.
    if chosen_house:
        save["house"] = chosen_house

    # ── KREUZUNGSPUNKT ────────────────────────────────────────────────────────
    # Dockt die Spielerin an (docks), wächst die Bindung und die Kreuzung gilt als
    # genutzt. Dockt sie NICHT an, läuft der Kanon autonom weiter (Recap) und die
    # Kreuzung gilt als verpasst — der Beat passiert trotzdem (siehe next_scenes).
    crossing_event = None
    autonomous = False
    if scene and scene.get("crossing_point"):
        choice = choices[choice_index] if choices and choice_index < len(choices) else {}
        if choice.get("docks", False):
            if scene_id not in save["crossings_used"]:
                save["crossings_used"].append(scene_id)
                save["clique_bond"] += int(scene.get("clique_bond_delta", 1))
            crossing_event = scene_id
        else:
            # nicht angedockt → autonome Kanon-Spur (nacherzählt)
            autonomous = True
            if scene_id not in save["crossings_missed"] and scene_id not in save["crossings_used"]:
                save["crossings_missed"].append(scene_id)

    # „Teil der Clique" nach verschärfter Regel (Kreuzungen UND Kern-Freundschaften)
    recompute_clique(save)

    # Abgeschlossenen Beat vermerken (Story-State-Persistenz)
    if scene_id not in save["beats_completed"]:
        save["beats_completed"].append(scene_id)

    # Wahl protokollieren
    save["choices_made"].append({
        "scene_id": scene_id,
        "choice_index": choice_index,
        "choice": choice_desc,
        "is_canon": is_canon,
        "divergence_rejected": divergence_rejected,
    })

    save["session_log"].append({
        "scene": scene_id,
        "action": choice_desc,
        "result": "Kanon" if is_canon else ("Kanon (Abweichung gesperrt)" if divergence_rejected else "Abweichung"),
        "stat_effects": stat_effects,
        "relationship_effects": relationship_effects,
        "crossing": crossing_event,
        "autonomous": autonomous,
    })
    save["session_log"] = save["session_log"][-10:]

    # Nächste Szene bestimmen. WICHTIG (V1): Beats sind linear verkettet — sowohl
    # Andocken als auch autonome Spur führen zum SELBEN nächsten Beat. Eine echte
    # Verzweigung gibt es nur, wenn ein Beat mehrere next_scenes hat (derzeit nicht).
    next_scenes = scene.get("next_scenes", []) if scene else []
    if next_scenes:
        if len(next_scenes) > 1 and choice_index < len(next_scenes) and not save.get("divergence_locked"):
            save["current_scene"] = next_scenes[choice_index]
        else:
            # Bei gedeckelter Divergenz immer auf den Kanon-Strang (Index 0)
            save["current_scene"] = next_scenes[0]
        next_scene_data = None
        for s in plot.get("scenes", []):
            if s["id"] == save["current_scene"]:
                next_scene_data = s
                break
        if next_scene_data:
            save["chapter_progress"] = next_scene_data.get("chapter", save["chapter_progress"])
            # Beim Beat-Wechsel ist die Spielerin „im Beat" (kein Sandkasten-Ort);
            # current_location folgt dem Schauplatz des neuen Beats.
            save["current_location"] = next_scene_data.get("location")
            save["segment"] = save.get("segment", 0) + 1
    else:
        save["current_scene"] = "END"

    write_save(save_id, save)

    print("Fortschritt gespeichert!")
    print(f"  Wahl: {choice_desc}")
    if is_canon:
        print("  ✓ Kanon")
    elif divergence_rejected:
        print("  ⟲ Abweichung gesperrt (Divergenz-Cap erreicht) — Geschichte bleibt auf Kurs")
    else:
        print(f"  ✗ Abweichung (Divergenz +{DIVERGENCE_STEP})")
    print(f"  Attribut-Änderung: {json.dumps(stat_effects, ensure_ascii=False)}")
    if relationship_effects:
        print(f"  Beziehungs-Änderung: {json.dumps(relationship_effects, ensure_ascii=False)}")
    if crossing_event:
        print(f"  ✦ Kreuzungspunkt genutzt ({crossing_event}) — angedockt")
    if autonomous:
        print(f"  ◷ Kreuzung verpasst — Kanon läuft autonom weiter (Recap erzählen): {scene_id}")
    if save["in_clique"]:
        print("  ✦ Status: Teil der Clique")
    print(f"  Nächste Szene: {save['current_scene']}")
    print(f"  Divergenz: {save['divergence_score']}/{DIVERGENCE_CAP}" + (" [GESPERRT]" if save.get("divergence_locked") else ""))


def load_game(save_id):
    """Lädt einen Spielstand und zeigt den Status."""
    save = load_save(save_id)
    book_title = _book_title(save["book_id"])

    print(f"Spielstand: {save['save_id']}")
    print(f"Buch: {book_title}")
    print(f"Figur: {save['character_name']}")
    prot = save.get("protagonist")
    if prot:
        pron = prot.get("pronouns", {})
        pron_str = f" · {pron['subjekt']}/{pron['possessiv']}" if pron.get("subjekt") else " · neutral (Name benutzen)"
        print(f"Profil: {prot.get('gender')}{pron_str} · aus {prot.get('hometown')}")
    print(f"Kapitel/Abschnitt: {save['chapter_progress']}")
    print(f"Aktuelle Szene: {save['current_scene']}")
    print(f"Attribute: {json.dumps(save['stats'], ensure_ascii=False)}")
    print(f"Divergenz: {save['divergence_score']}/{DIVERGENCE_CAP}" + (" [GESPERRT]" if save.get("divergence_locked") else ""))
    if save.get("current_location"):
        print(f"Aktueller Ort: {save['current_location']}")
    if save.get("companion"):
        print(f"Begleiter: {save['companion']}")
    if save.get("house"):
        print(f"Haus: {save['house']}")
    print("Teil der Clique: " + ("ja" if save.get("in_clique") else "noch nicht"))
    print(f"Beats abgeschlossen: {len(save.get('beats_completed', []))} | "
          f"Kreuzungen genutzt: {len(save.get('crossings_used', []))} | "
          f"verpasst: {len(save.get('crossings_missed', []))}")
    print(f"Getroffene Wahlen: {len(save['choices_made'])}")
    if save.get("relationships"):
        print("Beziehungen:")
        for name, rel in save["relationships"].items():
            print(f"  {name}: {rel['status']} (Vertrauen {rel['trust']})")
    if save.get("achievements"):
        print(f"Erfolge: {', '.join(save['achievements'])}")
    if save.get("session_log"):
        print("\nLetzte Ereignisse:")
        for log in save["session_log"][-3:]:
            print(f"  [{log['scene']}] {log['action']} → {log['result']}")


def move(save_id, location):
    """Sandkasten-Bewegung: setzt den aktuellen Ort — aber NUR auf einen Schauplatz
    der Orts-Whitelist. So ist das Verlassen von Welt/Setting technisch unmöglich
    (Leitplanke ist die Welt, nicht nur der Prompt). Divergenz-neutral: freier ORT,
    niemals freies THEMA — der Hauptplot wird dadurch nicht berührt.
    """
    save = load_save(save_id)
    locs = load_locations(save["book_id"]).get("locations", [])
    by_id = {l["id"]: l for l in locs}
    by_name = {l["name"].lower(): l for l in locs}
    loc = by_id.get(location) or by_name.get(location.lower())
    if not loc:
        print(f"✗ Ort '{location}' ist nicht auf der Whitelist — Bewegung abgelehnt.")
        print("  Erlaubte Orte: " + ", ".join(f"{l['id']} ({l['name']})" for l in locs))
        sys.exit(2)
    save["current_location"] = loc["name"]
    write_save(save_id, save)
    print(f"✓ Du bist jetzt: {loc['name']}")
    print(f"  Kontext: {loc.get('context', '')}")
    print(f"  (Sandkasten — divergenz-neutral; nächster Beat: {save['current_scene']})")


def set_house(save_id, house):
    """Setzt das Haus der Spielerin (frei aus den vier Häusern wählbar).

    Wird von der Hut-Zeremonie automatisch über das `house`-Feld der Wahl gesetzt;
    dieser Befehl erlaubt es zusätzlich, das Haus direkt zu wählen/korrigieren.
    """
    save = load_save(save_id)
    match = next((h for h in HOUSES if h.lower() == (house or "").lower()), None)
    if not match:
        print(f"✗ '{house}' ist kein gültiges Haus. Wähle: {', '.join(HOUSES)}")
        sys.exit(2)
    save["house"] = match
    write_save(save_id, save)
    print(f"✓ Haus gesetzt: {match}")


def set_profile(save_id, profile):
    """Ändert das Protagonist-Profil eines bestehenden Spielstands.

    Nur gesetzte Felder werden überschrieben; der Rest bleibt. Praktisch, wenn die
    Spielerin sich beim Onboarding vertippt oder später umbenennen möchte.
    """
    save = load_save(save_id)
    prot = save.get("protagonist") or {}
    default_pet = save.get("companion") or "Flocke"

    if profile.get("name"):
        save["character_name"] = profile["name"].strip()
        prot["name"] = profile["name"].strip()
    if profile.get("gender"):
        g = _normalize_gender(profile["gender"])
        prot["gender"] = g
        prot["pronouns"] = dict(PRONOUNS[g])
    if profile.get("hometown"):
        prot["hometown"] = profile["hometown"].strip()
    if profile.get("pet_name") or profile.get("pet_kind"):
        pet = prot.get("pet") or {"name": default_pet, "kind": "Malteser-Hündchen"}
        new_name = (profile.get("pet_name") or pet["name"]).strip()
        new_kind = (profile.get("pet_kind") or pet["kind"]).strip()
        rels = save.get("relationships", {})
        if new_name != pet["name"] and pet["name"] in rels:
            rels[new_name] = rels.pop(pet["name"])
        if new_name in rels:
            rels[new_name]["note"] = f"dein treuer Begleiter ({new_kind}), weicht dir nicht von der Seite"
        pet["name"], pet["kind"] = new_name, new_kind
        prot["pet"] = pet
        save["companion"] = new_name

    save["protagonist"] = prot
    write_save(save_id, save)
    print(f"✓ Profil aktualisiert: {prot.get('name')} ({prot.get('gender')}) aus "
          f"{prot.get('hometown')} · Haustier {prot['pet']['name']} ({prot['pet']['kind']})")


def list_saves():
    """Listet alle Spielstände."""
    ensure_dirs()
    saves = []
    for f in os.listdir(SAVES_DIR):
        if f.endswith(".json"):
            with open(os.path.join(SAVES_DIR, f), "r", encoding="utf-8") as fp:
                saves.append(json.load(fp))

    if not saves:
        print("Noch keine Spielstände.")
        return

    saves.sort(key=lambda x: x.get("updated_at", ""), reverse=True)
    print(f"{len(saves)} Spielstand/Spielstände:\n")
    for s in saves:
        book_title = _book_title(s["book_id"])
        status = "Durchgespielt" if s["current_scene"] == "END" else f"Abschnitt {s['chapter_progress']}"
        clique = " · Clique" if s.get("in_clique") else ""
        print(f"  {s['save_id']} | {book_title} · {s['character_name']} | {status} | Divergenz:{s['divergence_score']}{clique}")


def delete_save(save_id):
    """Löscht einen Spielstand."""
    path = os.path.join(SAVES_DIR, f"{save_id}.json")
    if os.path.exists(path):
        os.remove(path)
        print(f"Spielstand {save_id} gelöscht")
    else:
        print(f"Spielstand {save_id} existiert nicht")


def _book_title(book_id):
    meta_file = os.path.join(BOOKS_DIR, book_id, "meta.json")
    if os.path.exists(meta_file):
        with open(meta_file, "r", encoding="utf-8") as f:
            return json.load(f).get("title", book_id)
    return book_id


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Aufruf: game_engine.py <befehl> [args]")
        print("Befehle:")
        print("  new-game <book-id> <character-id> [--name N --gender g --home O --pet-name P --pet-kind K]  Neues Spiel (mit Onboarding)")
        print("  set-profile <save-id> [--name N --gender g --home O --pet-name P --pet-kind K]  Profil nachträglich ändern")
        print("  advance <save-id> <scene-id> <choice-index> [choice-desc]  Fortschritt (Beat)")
        print("  move <save-id> <ort>                                      Sandkasten-Bewegung (Whitelist)")
        print("  load <save-id>                                            Spielstand laden")
        print("  list-saves                                                Spielstände auflisten")
        print("  delete <save-id>                                          Spielstand löschen")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "new-game":
        if len(sys.argv) < 4:
            print("Aufruf: game_engine.py new-game <book-id> <character-id> "
                  "[--name N --gender g --home O --pet-name P --pet-kind K]")
            sys.exit(1)
        new_game(sys.argv[2], sys.argv[3], _parse_profile_flags(sys.argv[4:]))
    elif cmd == "set-profile":
        if len(sys.argv) < 3:
            print("Aufruf: game_engine.py set-profile <save-id> "
                  "[--name N --gender g --home O --pet-name P --pet-kind K]")
            sys.exit(1)
        set_profile(sys.argv[2], _parse_profile_flags(sys.argv[3:]))
    elif cmd == "advance":
        if len(sys.argv) < 5:
            print("Aufruf: game_engine.py advance <save-id> <scene-id> <choice-index> [choice-desc]")
            sys.exit(1)
        desc = sys.argv[5] if len(sys.argv) > 5 else ""
        advance(sys.argv[2], sys.argv[3], sys.argv[4], desc)
    elif cmd == "move":
        if len(sys.argv) < 4:
            print("Aufruf: game_engine.py move <save-id> <ort>")
            sys.exit(1)
        move(sys.argv[2], sys.argv[3])
    elif cmd == "set-house":
        if len(sys.argv) < 4:
            print("Aufruf: game_engine.py set-house <save-id> <Gryffindor|Ravenclaw|Hufflepuff|Slytherin>")
            sys.exit(1)
        set_house(sys.argv[2], sys.argv[3])
    elif cmd == "load":
        if len(sys.argv) < 3:
            print("Aufruf: game_engine.py load <save-id>")
            sys.exit(1)
        load_game(sys.argv[2])
    elif cmd == "list-saves":
        list_saves()
    elif cmd == "delete":
        if len(sys.argv) < 3:
            print("Aufruf: game_engine.py delete <save-id>")
            sys.exit(1)
        delete_save(sys.argv[2])
    else:
        print(f"Unbekannter Befehl: {cmd}")
        sys.exit(1)
