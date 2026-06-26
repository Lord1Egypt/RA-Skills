---
name: muninndb-auto-memory
description: "Proaktive Nutzung von MuninnDB als Memory-Schicht via MCP. Immer laden — kein manuelles Triggering noetig."
version: 1.1.1
clawhub: Bitsonwheels/muninndb-auto-memory
---

# MuninnDB Auto-Memory Workflow

Nutze MuninnDB (MCP-Tools `mcp_muninndb_muninn_*`) automatisch als primaere Memory-Schicht.
Der MCP-Server `muninndb` ist in der Hermes-Config registriert und immer verfuegbar.

## Konfiguration

- **Vault**: `hermes`
- **MCP-Tool-Prefix**: `mcp_muninndb_muninn_`
- **API-Key**: in `~/.muninn/openclaw.key` (Bearer-Token)

## Session-Start (automatisch)

Bei jeder neuen Session:
1. `mcp_muninndb_muninn_where_left_off(limit=10)` — was war zuletzt aktiv?
2. `mcp_muninndb_muninn_recall(context=["user preferences", "current project", "recent context"])` — Kontext aus vorherigen Sessions holen
3. Aus dem Ergebnis: relevante Fakten in den Kontext einweben

## Waehrend der Session (proaktiv)

Speichere automatisch wichtige Fakten via `mcp_muninndb_muninn_remember`:

- **Praeferenzen**: "Benutzer bevorzugt X"
- **Entscheidungen**: "Wir haben uns fuer Y entschieden, weil Z"
- **Projekt-Kontext**: "Aktuelles Projekt ist P mit Stack S"
- **Fehlerbehebung**: "Bug B wurde durch Loesung L gefixt"
- **Zusammenfassungen**: Nach komplexen Tasks eine kurze Zusammenfassung speichern

Wann speichern?
- Nachdem der Benutzer eine wichtige Entscheidung teilt
- Nach erfolgreichem Abschluss einer komplexen Task (5+ Tool-Calls)
- Wenn der Benutzer etwas korrigiert oder eine Praeferenz nennt
- Neue Projekt-Infrastruktur/Architektur

## Recall bei Unklarheit

Wenn Du Kontext aus frueheren Sessions brauchst:
1. `mcp_muninndb_muninn_recall(context=["<suchbegriff>"], vault="hermes")` — semantische Suche
2. `mcp_muninndb_muninn_entity(entity_name="<name>")` — was wissen wir ueber ein Entity?

## Session-Ende (optional, vor /reset oder Session-Wechsel)

Bei Bedarf: `mcp_muninndb_muninn_remember(concept="session-summary-<datum>", content="<Kurzzusammenfassung>", vault="hermes")`

## Cron-Job: Periodischer Snapshot

Ein Cron-Job (`MuninnDB Memory Snapshot`) speichert alle 30 Minuten einen Kontext-Snapshot:

```yaml
cron:
  name: "MuninnDB Memory Snapshot"
  schedule: "every 30m"
  script: "muninndb-memory-snapshot.sh"   # in ~/.hermes/scripts/
  no_agent: true                          # kein LLM, nur Skript
  workdir: "/Users/bits"
  silent_on_success: true                 # nur Fehler melden
```

Das Skript sammelt: Arbeitsverzeichnis, letzte Hermes-Sessions, Hostname, Timestamp.
Bei Erfolg: kein Output (kein Spam). Bei Fehler: Meldung an Benutzer.

**Verwaltung:**
```bash
cronjob action=list                                   # Status
cronjob action=pause job_id=<id>                      # Pausieren
cronjob action=run job_id=<id>                        # Manuelle Ausfuehrung
```

## REST-API Fallback (wenn MCP-Tools noch nicht sichtbar)

Falls die MCP-Tools (`mcp_muninndb_muninn_*`) noch nicht geladen sind (z.B. vor `/reset`):

```bash
MUNINN_URL="http://127.0.0.1:8475"
MUNINN_TOKEN=$(cat ~/.muninn/openclaw.key)

# Speichern
curl -s -X POST "$MUNINN_URL/api/engrams" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MUNINN_TOKEN" \
  -d '{"concept":"kurzer-titel","content":"vollstaendiger text","vault":"hermes"}'

# Suchen
curl -s -X POST "$MUNINN_URL/api/activate" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MUNINN_TOKEN" \
  -d '{"context":["suchbegriff"],"vault":"hermes","max_results":5}'
```

Vollstaendige Doku: `references/setup-companion.md`

## Wichtige Hinweise

- **Nicht ueberfrachten**: Speichere nur substanzielle Fakten, nicht jede Kleinigkeit
- **Atomic halten**: Ein Konzept pro Speicherung (bessere Recall-Qualitaet)
- **Kein Duplikat-Check noetig**: MuninnDB erkennt Duplikate selbst und gibt die existierende ID zurueck
- **MCP-Tools erscheinen erst nach `/reset`** — bis dahin REST-API nutzen
- **`mcp_muninndb_muninn_status`** fuer Vault-Statistiken
- **`headers`-Key** (nicht `http_headers`) im MCP-Config — der native MCP-Client erwartet `headers`
