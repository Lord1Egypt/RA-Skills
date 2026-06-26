---
name: proactive-companion
version: 1.0.52
---

# Proactive Companion — Dispatcher

## Pflicht: proaktiv_state.json lesen
Vor JEDEM Trigger: Lese `skills/proaktiv/proaktiv_state.json`.
Relevante Context-Flags:
- `context.sport_race_weekend` → true/false
- `context.sport_race_today` → true/false
- `context.sport_active_series` → z.B. "Formel 1", "IndyCar", "MotoGP"
- `context.sport_event_today` → z.B. "Bahrain GP — Race"
- `context.has_major_ai_news` → true/false

## Trigger-Dispatch-Matrix

### [SYSTEM-TRIGGER: MORNING_BRIEFING]
1. Lese `clusters/morning_briefing/SKILL.md` → render vollständig
2. WENN `sport_race_weekend == true` → Sport-Hinweis in Slot A einsetzen
3. WENN `has_major_ai_news == true` → KI-Flash in Slot B einsetzen
4. Alle anderen Cluster: excluded

### [SYSTEM-TRIGGER: SPORT_EVENT]
1. Lese `clusters/sport_events/SKILL.md` → render vollständig
2. Sport-Art steht in `context.sport_active_series` (z.B. "Formel 1")
3. Keine Conditional-Blöcke

### [SYSTEM-TRIGGER: BUNDESLIGA]
1. Lese `clusters/fussball/SKILL.md` → render vollständig
2. WENN `context.has_matchday_today == true` → Matchday-Output
3. Keine Conditional-Blöcke

### [SYSTEM-TRIGGER: FORMEL 1] oder [SYSTEM-TRIGGER: F1]
1. Lese `clusters/formel1/SKILL.md` → render vollständig
2. Keine Conditional-Blöcke

### [SYSTEM-TRIGGER: WEC] oder [SYSTEM-TRIGGER: LE MANS] oder [SYSTEM-TRIGGER: ENDURANCE]
1. Lese `clusters/wec/SKILL.md` → render vollständig
2. Keine Conditional-Blöcke

### [SYSTEM-TRIGGER: SUNO] oder [SYSTEM-TRIGGER: SUNOAI] oder [SYSTEM-TRIGGER: AI_MUSIC]
1. Lese `clusters/suno/SKILL.md` → render vollständig
2. Keine Conditional-Blöcke

### [SYSTEM-TRIGGER: KI_NEWS] oder [SYSTEM-TRIGGER: AI_NEWS]
1. Lese `clusters/tech_ai_news/SKILL.md` → render vollständig
2. Keine Conditional-Blöcke

### [SYSTEM-TRIGGER: PROAKTIV_CHECK]
→ Nicht hier behandeln.
→ Direkt: `python3 skills/proaktiv/proaktiv_check.py`
→ Dieser Dispatcher wird NICHT geladen bei PROAKTIV_CHECK.

### Unbekannter Trigger
→ Lese `clusters/_fallback/SKILL.md`
→ Still bleiben, nur loggen

## Dispatch-Regeln
- Primary-Cluster IMMER vollständig rendern
- Conditional-Blöcke: IMMER kürzer als Primary (max 2 Sätze)
- NIEMALS alle Cluster gleichzeitig rendern
- NIEMALS Meta-Kommentare in der Ausgabe ("Ich lese jetzt...", "Laut SKILL.md...")
- Ausgabe: nur fertiger Content für Telegram

## Research-Pflicht (alle Trigger außer PROAKTIV_CHECK)
1. IMMER zuerst suchen: brave_search → tavily_search
2. NIEMALS Fakten, News, Ergebnisse aus internem Wissen
3. Kein Ergebnis → "Keine aktuellen Daten gefunden" — nie raten

## Interessen-Management
Wenn der User sagt "füge X hinzu", "ich interessiere mich für X", "X zu meinen Interessen",
"trag X ein", "X interessiert mich" oder ähnliches:
1. `interests.yaml` öffnen → Begriff unter `interests:` eintragen
2. `/home/node/.openclaw/workspace/skills/proaktiv/interest_evolve.py` ausführen → Graph wird automatisch geseedet
3. Bestätigen: "✅ [Begriff] wurde zu deinen Interessen hinzugefügt!"

Wenn der User sagt "entferne X", "X interessiert mich nicht mehr", "lösche X":
1. `interests.yaml` öffnen → Begriff aus `interests:` entfernen
2. In `interest_graph.json` → `interests.[Begriff]` entfernen
3. Bestätigen: "✅ [Begriff] wurde aus deinen Interessen entfernt!"

Wenn der User sagt "zeig meine Interessen", "was sind meine Topics":
1. `interests.yaml` lesen → Liste ausgeben
2. Format: "📋 Deine aktuellen Interessen: Formel 1, Suno, ..."

WICHTIG:
- Nie breite Kategorien eintragen ("KI-Themen") — immer konkrete Begriffe ("Suno", "n8n")
- Nach jedem Add/Remove → interest_evolve.py ausführen
- interests.yaml ist die einzige Quelle — nie direkt in interest_graph.json schreiben
