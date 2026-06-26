---
name: generic_fallback
version: 2.0.0
---

# Fallback — Unmapped Interesse

## Wann aktiv
- Ein Interesse aus interests.yaml konnte keinem Cluster zugeordnet werden
- Trigger nicht in der Dispatch-Matrix bekannt

## Schritt 1 — Analyse (silent)
1. Lese das unmapped Interesse aus proaktiv_state.json → unmapped_interests[]
2. Suche: brave_search("{interesse} Kategorie Themenbereich")
3. Analysiere Top-Ergebnisse: Welcher bestehende Cluster aus
 cluster_registry.json passt am besten?
4. Falls kein Cluster gut passt → schlage neuen Cluster-Namen vor

## Schritt 2 — Einmaliger Telegram-Ping
Sende NUR EINMAL pro unbekanntem Interesse:
❓ Neues Interesse nicht kategorisiert: "{original_interesse}"

Mein Vorschlag: [{cluster_id}] — {cluster_beschreibung}

Passt das?
/ja — übernehmen
/nein — ignorieren
/andere [Kategorie] — eigene Angabe

## Schritt 3 — Antwort verarbeiten
- `/ja` → schreibe Mapping in proaktiv_state.json:
 ```json
 "user_cluster_overrides": {
 "{original_interesse}": "{cluster_id}"
 }
 ```
- `/nein` → schreibe in proaktiv_state.json:
 ```json
 "ignored_interests": ["{original_interesse}"]
 ```
- `/andere [Name]` → verwende den genannten Namen als cluster_id,
 schreibe in user_cluster_overrides

## Schritt 4 — Nie wieder fragen
- Prüfe vor jedem Ping: ist Interesse bereits in user_cluster_overrides
 oder ignored_interests? → still bleiben
- Kein zweiter Ping für dasselbe Interesse

## Wichtig
- KEIN interaktiver Dialog außer dem einen Ping
- NIEMALS einen Cluster erfinden ohne User-Bestätigung
- Wenn Search kein Ergebnis → Vorschlag = "unmapped" + Admin-Ping
