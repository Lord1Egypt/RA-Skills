---
title: MuninnDB Integration for Hermes Agent
category: mlops/vector-databases
name: muninndb-integration
description: Integrates MuninnDB as a cognitive memory system for Hermes Agent.
version: 1.0.0
---

# MuninnDB Integration for Hermes Agent

This skill integrates MuninnDB as cognitive memory system.

## Trigger
Use when user wants to configure MuninnDB.

## MCP Integration (aktiv seit 2026-05-10)

MuninnDB laeuft lokal auf Port 8475 (API) und 8750 (MCP).
Die Hermes-Integration erfolgt via MCP-Server:

```yaml
mcp_servers:
  muninndb:
    url: "http://127.0.0.1:8750/mcp"
    headers:                  # WICHTIG: "headers", NICHT "http_headers"
      Authorization: "Bearer <api-key>"
```

Stellt 39 Tools bereit (muninn_remember, muninn_recall, u.v.m.) im `mcp_muninndb_*` Namensraum.

**Pitfall:** Der native MCP-Client von Hermes erwartet den Key `headers` (nicht `http_headers`).
Letzterer wird ignoriert, was zu `401 Unauthorized` fuehrt, obwohl `hermes mcp list` den Server
als "enabled" anzeigt. Bei Auth-Problemen zuerst den Key-Namen in `config.yaml` pruefen.

## Cron-Job

Periodischer Memory-Snapshot (alle 30 Min) via `~/.hermes/scripts/muninndb-memory-snapshot.sh`.
`no_agent=true`, silent on success. Siehe `muninndb-auto-memory` Skill fuer den Workflow.

## Verwandte Skills

- **muninndb-auto-memory** — automatisierte Nutzung der MCP-Tools waehrend der Session
- **native-mcp** — MCP-Client-Konfiguration