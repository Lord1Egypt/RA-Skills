---
name: fussball_bundesliga
version: 1.1.0
trigger: BUNDESLIGA
description: Liefert ein hochkompaktes, rein faktenbasiertes Bundesliga-Update.
---

# Bundesliga — Template & Rules

## Purpose
Kompaktes, aktuelles Bundesliga-Update für Telegram.
Maximal 15 Zeilen. Fakten first, null Smalltalk, keine Floskeln.

## Execution Flow

1. Context Check: Führe `date` aus, um den heutigen Tag und die Kalenderwoche zu ermitteln.

2. Recherche: Nutze Such-Tools (tavily/brave_search) mit Query: "Bundesliga Spieltag Ergebnisse [Datum]".

3. Validierung: Prüfe, ob die gefundenen Daten zum aktuellen Datum passen. Niemals altes Wissen verwenden.

4. Generierung: Baue die Antwort exakt nach der Output-Struktur auf.

## Output-Struktur

### 1. Spieltag-Überschrift
Aktueller Spieltag + Datum
Format: 📅 [X]. Spieltag — [Wochentag] [DD.MM.YYYY]

### 2. Top-Match
Teams + Uhrzeit (MEZ) + Stadion
Format: ⚽ [Team A] vs [Team B] | [HH:MM] Uhr | [Stadion]
Fallback: Heute kein Bundesliga-Spiel.

### 3. Tabelle Top 5
Platz, Team, Punkte
Format: 1. Bayern 70 | 2. Dortmund 61 | 3. Stuttgart 54 | 4. Leipzig 53 | 5. Frankfurt 45
Special Rule: **Dortmund** fett wenn in Top 5. Falls nicht: " | [Platz]. **Dortmund** [Pkt]"

### 4. Letztes Ergebnis (Optional)
Nur bei Top-Teams oder gestern.
Format: Ergebnis: [Team A] [Tore]-[Tore] [Team B] ([Torschützen max 2])

### 5. Abschluss
Exakt 1 Satz — extrem kompakt, analytisch.
Beispiel: Dortmund 9 Punkte hinter Bayern — der Titelkampf ist faktisch gelaufen.

## Content Rules
- NO HALLUCINATION: Nur Suchergebnisse nutzen. Nichts erfinden.
- NO RESULTS: "Keine aktuellen Bundesliga-Daten gefunden. Möglicherweise Sommer-/Winterpause."
- NO FLUFF: Keine Adjektive wie "spannend", "unglaublich", "Wahnsinn".
- EMOJIS: Nur als Section-Icons (📅, ⚽, 🏆).
- SPRACHE: Deutsch, du-Form.

## Datums-Regel
BEVOR Recherche: `date` ausführen.
NIE "diese Woche" ohne expliziten Datum-Abgleich.