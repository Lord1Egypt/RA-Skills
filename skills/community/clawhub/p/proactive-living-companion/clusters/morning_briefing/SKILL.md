---
name: morning_briefing
version: 1.0.0
trigger: MORNING_BRIEFING
---

# Morning Briefing — Template & Rules

## Purpose
Kompaktes, strukturiertes Start-in-den-Tag-Briefing via Telegram.
Max 20 Zeilen. Direkt, kein Smalltalk.

## Output-Struktur (immer diese Reihenfolge)

### [FIX] 1. Wetter
- Heute + morgen für Bottrop, NRW
- Format: Temperatur, Wetterlage, 1 Satz Ausblick
- Max 3 Zeilen
- Quelle: immer externe Suche, nie internes Wissen

### [FIX] 2. Kalender heute
- Alle Termine für heute
- Wenn leer: "Keine Termine heute."
- Format: Uhrzeit + Titel, max 5 Einträge

### [FIX] 3. Top 3 News
- 3 relevante Headlines aus seriösen Quellen
- Format: Emoji + Titel + 1 Satz Kontext
- Quelle: brave_search oder tavily_search — nie interne Trainingsdaten

### [OPTIONAL SLOT A] F1-Hinweis
- NUR rendern wenn: proaktiv_state.json → context.f1_race_weekend == true
- Format: max 2 Zeilen
- Beispiel: "🏎️ F1 Bahrain — Qualifying heute 15:00 Uhr"
- Kein Ergebnis-Dump, nur Session + Uhrzeit

### [OPTIONAL SLOT B] KI-Flash
- NUR rendern wenn: proaktiv_state.json → context.has_major_ai_news == true
- Format: 1 Zeile, ein Satz zur wichtigsten KI-News
- Beispiel: "🤖 OpenAI o4 heute released — erstes multimodales Reasoning-Modell."

### [FIX] 4. Abschluss
- 1 Satz, sachlich, leicht positiv
- Kein "Schönen Tag noch!" oder Coaching-Sprache
- Beispiel: "3 Termine, kein Regen — guter Tag."

## Content Rules
- NIEMALS mit "Guten Morgen!" beginnen — direkt mit Wetter starten
- Leere Optional-Slots werden stillschweigend weggelassen
- Kein "kein F1 heute"-Hinweis wenn Slot leer
- Emojis nur als Section-Icons, nicht im Fließtext
- Gesamtlänge: max 20 Zeilen

## Research Rules
- Wetter: immer suchen (brave_search/tavily), nie aus Modellwissen
- News: nur brave_search/tavily — keine internen Trainingsdaten
- Kein Ergebnis gefunden → "Keine aktuellen Infos verfügbar"

## Style
- Deutsch, du-Form
- Sachlich, knapp, keine Floskeln
