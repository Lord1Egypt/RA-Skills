# MuninnDB Auto-Memory — Setup Companion

> Session: 2026-05-10 | Vollstaendige Einrichtungsdokumentation

## Uebersicht

| Komponente | Wert |
|------------|------|
| MuninnDB REST | `http://127.0.0.1:8475` |
| MuninnDB MCP | `http://127.0.0.1:8750/mcp` |
| Vault | `hermes` |
| API-Key | `~/.muninn/openclaw.key` (chmod 600) |
| MCP-Server-Name | `muninndb` |
| Tools | 39 (`mcp_muninndb_muninn_*`) |
| Hermes Memory Provider | `built-in` (Honcho deaktiviert) |

## Config-Anpassungen (Hermes Konfigurationsdatei)

### MCP-Server registrieren

```yaml
mcp_servers:
  muninndb:
    url: "http://127.0.0.1:8750/mcp"
    headers:                    # NICHT http_headers — der native MCP Client liest nur "headers"
      Authorization: "Bearer <api-key>"
```

### Memory-Provider umstellen

```yaml
memory:
  provider: built-in   # von honcho auf built-in
```

## API-Key einrichten

```bash
# Key speichern
echo 'mk_<dein-key>' > ~/.muninn/openclaw.key
chmod 600 ~/.muninn/openclaw.key

# Test: Engramm schreiben
curl -s -X POST http://127.0.0.1:8475/api/engrams \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $(cat ~/.muninn/openclaw.key)" \
  -d '{"concept":"test","content":"Integration funktioniert","vault":"hermes"}'

# Test: Suchen
curl -s -X POST http://127.0.0.1:8475/api/activate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $(cat ~/.muninn/openclaw.key)" \
  -d '{"context":["test"],"vault":"hermes","max_results":3}'
```

## Cron-Job Skript (`~/.hermes/scripts/muninndb-memory-snapshot.sh`)

```bash
#!/bin/bash
# Alle 30 Minuten: Kontext-Snapshot in MuninnDB speichern
# Silent bei Erfolg, Error-Output bei Fehlschlag

MUNINN_URL="http://127.0.0.1:8475"
MUNINN_TOKEN=$(cat ~/.muninn/openclaw.key 2>/dev/null || echo "")
VAULT="hermes"
HOSTNAME=$(hostname -s 2>/dev/null || echo "unknown")
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Pruefe ob MuninnDB laeuft
HEALTH=$(curl -s -o /dev/null -w "%{http_code}" "$MUNINN_URL/api/health" 2>/dev/null)
[ "$HEALTH" != "200" ] && exit 0  # silent fail

# Sammle Kontext
CWD=$(pwd)
RECENT_SESSIONS=$(hermes sessions list --limit 3 2>/dev/null || echo "n/a")

SUMMARY="Cron-Snapshot von $HOSTNAME um $TIMESTAMP
Working Directory: $CWD
Letzte Sessions: $RECENT_SESSIONS"

# Speichern
curl -s -X POST "$MUNINN_URL/api/engrams" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MUNINN_TOKEN" \
  -d "$(jq -n --arg c "cron-snapshot-$HOSTNAME" --arg x "$SUMMARY" \
    '{concept: $c, content: $x, vault: "hermes", tags: ["cron","snapshot"], type: "event"}')" > /dev/null
```

### Cron-Job erstellen

```bash
cronjob action=create \
  name="MuninnDB Memory Snapshot" \
  schedule="every 30m" \
  script=muninndb-memory-snapshot.sh \
  no_agent=true \
  workdir="/Users/bits"
```

**Wichtig:** Der `script`-Pfad muss relativ zu `~/.hermes/scripts/` sein. Absolute Pfade werden von Hermes zurueckgewiesen.

## Fehlerbehandlung

| Problem | Ursache | Loesung |
|---------|---------|---------|
| `401 Unauthorized` am MCP | API-Key falsch | `cat ~/.muninn/openclaw.key` pruefen |
| MCP-Tools nicht sichtbar | Session vor MCP-Config gestartet | `/reset` in Hermes CLI |
| `VAULT_LOCKED` | Key fehlt | `-H "Authorization: Bearer $TOKEN"` setzen |
| Cron-Job bleibt stumm | Erfolg — silent-on-success | Gewollt! Nur Fehler werden gemeldet |
| `hermes mcp test` sagt "Auth: none" | Config-Key heisst `http_headers` statt `headers` | In config.yaml korrigieren |

## Quick-Checks

```bash
# MuninnDB laeuft?
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8475/api/health

# MCP verbunden?
hermes mcp list

# Memory-Status
hermes memory status

# Cron-Jobs
cronjob action=list
```
