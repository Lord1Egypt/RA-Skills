---
name: sport_events
version: 2.0.0
trigger: SPORT_EVENT
---

# Sport Events — Template & Rules

## Purpose
Kompaktes Sport-Update via Telegram.
Welcher Sport aktiv ist, steht in proaktiv_state.json →
context.sport_active_series (z.B. "Formel 1", "IndyCar", "DTM", "MotoGP").

## Output-Struktur
1. Emoji + Series-Name + Session (aus context.sport_event_today)
2. Top 5 Ergebnis — suche nach "{sport_active_series} Ergebnis heute"
3. Meisterschafts-Stand Top 3 (Fahrer + Punkte)
4. 1 Satz Kontext (Wetter, Drama, Safety Car, etc.)

## Qualifying-Struktur
1. Session + Datum
2. Top 5 Startaufstellung
3. 1 Satz Highlight

## Wer setzt sport_active_series?
- proaktiv_check.py liest interests.yaml → motorsport-Eintrag
- Schreibt in proaktiv_state.json → context.sport_active_series
- Beispiel: interests.yaml hat "IndyCar" → sport_active_series = "IndyCar"

## Content Rules
- IMMER zuerst suchen: brave_search("{sport_active_series} Ergebnis heute")
- Kein Ergebnis → "Keine aktuellen {sport_active_series}-Daten gefunden"
- NIEMALS Ergebnisse aus internem Wissen — immer suchen
- Mehrere Motorsport-Interessen → mehrere kompakte Blöcke, je max 5 Zeilen
- Max 15 Zeilen gesamt

## Style
- Deutsch, direkt, Fakten first
