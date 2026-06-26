---
name: log-collector
description: Permanent log collection agent. Collects logs and history from all nodes via SSH/VPN every 3 hours. Stores in logs.db with 30-day retention. Multi-node capable with fallback logic.
---

# Log Collector Sub-Agent

Permanenter Log-Sammel-Agent für alle Nodes im Cluster.

## Aufgaben

| Intervall | Aufgabe | Details |
|-----------|---------|---------|
| **3 Stunden** | Node-Abfrage | SSH über VPN zu allen Nodes |
| **3 Stunden** | Log-Collection | System-Logs, OpenClaw-Logs, VPN-Status |
| **3 Stunden** | Datenbank-Update | Schreibt in logs.db |
| **Täglich** | Retention-Cleanup | Löscht Logs > 30 Tage |

## Multi-Node Support

| Node | Verbindung | Priorität |
|------|------------|-----------|
| Node 1 (Gateway) | Lokal | Primär (Sammel-Node) |
| Node 2 (Netcup) | SSH → 10.10.0.2 | Abfrage-Ziel |
| Node 3 (xNetX) | SSH → 10.10.0.3 | Abfrage-Ziel |
| Node 4+ | SSH → 10.10.0.X | Variable Erreichbarkeit |

## VPN-Priorität

```
1. Tailscale (primär) → schneller, stabil
2. WireGuard (fallback) → zuverlässiger Tunnel
3. SSH WAN (letzter Fallback) → langsamster
```

## Datenbank: logs.db

### Tabellen

| Tabelle | Inhalt |
|---------|--------|
| **nodes** | Bekannte Nodes mit VPN-IP, SSH-Keys |
| **logs** | Gesammelte Logs (max. 30 Tage) |
| **ssh_connections** | Verbindungs-Log (Erfolg/Fehler) |
| **vpn_status** | Tailscale/WireGuard Status |
| **collection_runs** | Abfrage-Tracking pro Durchlauf |
| **node_logs_raw** | Roh-Logs unverarbeitet |

### Retention

```sql
-- Automatisch: Logs > 30 Tage löschen
DELETE FROM logs WHERE retention_until < datetime('now');
```

## Abfrage-Workflow

```python
# Für jeden Node in nodes-Tabelle:
for node in nodes:
    # 1. VPN-Status prüfen
    vpn_status = check_vpn(node.tailscale_ip) or \
                 check_vpn(node.wireguard_ip)
    
    # 2. SSH-Verbindung versuchen
    if ssh_connect(node.ssh_key_path, node.vpn_ip):
        # 3. Logs abholen
        logs = ssh_exec('journalctl -n 1000')
        
        # 4. In logs.db speichern
        insert_logs(node.node_id, logs)
    else:
        # 5. Fehler loggen
        insert_ssh_error(node.node_id, "Connection failed")
```

## Variable Erreichbarkeit

| Szenario | Verhalten |
|----------|-----------|
| **Node immer erreichbar** | Normale Abfrage, vollständige Logs |
| **Node manchmal erreichbar** | Best-effort, sammelt wenn möglich |
| **Node nie erreichbar** | Wird trotzdem versucht, Fehler geloggt |
| **Gateway offline** | Lokale Buffer, später Übertragung |

## Berechtigungen

```yaml
exec: read_write_ssh
nodes: query_all
logs: collect_store
retention: cleanup_30d
```

## Konfiguration

```json
{
  "log-collector": {
    "enabled": true,
    "collection_interval_hours": 3,
    "retention_days": 30,
    "nodes": [
      {"id": "node1", "local": true},
      {"id": "node2", "ssh_key": "~/.ssh/node2_key"},
      {"id": "node3", "ssh_key": "~/.ssh/node3_key"},
      {"id": "node4", "ssh_key": "~/.ssh/node4_key", "optional": true}
    ],
    "vpn_priority": ["tailscale", "wireguard", "wan"]
  }
}
```

## Scripts

| Script | Zweck |
|--------|-------|
| `log_collector.py` | Haupt-Collection-Logik |
| `ssh_connector.py` | SSH-Verbindungen mit Fallback |
| `vpn_checker.py` | VPN-Status-Prüfung |
| `retention_cleanup.py` | 30-Tage Cleanup |

## Logs

```
logs/log-collector/
├── 2026-04-18.log
├── collection-errors.log
└── run-summary.json
```

## Installation

```bash
# Skill installieren
clawhub install log-collector

# Cron aktivieren (alle 3 Stunden)
0 */3 * * * /usr/bin/python3 /home/openclaw/.openclaw/workspace/skills/log-collector/scripts/log_collector.py
```

## Troubleshooting

### Problem: SSH-Verbindung fehlgeschlagen

**Prüfung:**
```bash
# VPN erreichbar?
ping 10.10.0.2

# SSH-Key korrekt?
ssh -i ~/.ssh/node2_key openclaw@10.10.0.2
```

### Problem: Logs nicht in Datenbank

**Prüfung:**
```bash
# logs.db existiert?
ls -la db/logs.db

# Fehler-Log
tail logs/log-collector/collection-errors.log
```

## Integration

- **db-maintainer:** Separate DB, gleiche Backup-Strategie
- **workspace-db:** Dokumentations-Index (separat)
- **tree.db v2:** Datei-Tracking (separat)

---
**Hinweis:** Konfiguration (SSH-Keys, IPs) nicht im Skill - muss in env/db konfiguriert werden.
