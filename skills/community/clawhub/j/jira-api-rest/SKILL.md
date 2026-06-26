---
name: jira-api
description: Jira automation via Jira Cloud REST API v3, complementing `jira-cli` when it is missing features (especially edit/delete worklogs, advanced JQL search, bulk inspection, or raw REST calls). Use when you need programmatic Jira operations from this workspace (gruporeacciona.atlassian.net), including: listing/filtering worklogs by date, deleting or updating a specific worklog by id, running JQL via /search/jql, or performing a one-off authenticated REST request.
---

# Jira API

Usa `jira-cli` cuando exista el comando (listar issues, ver issue, transiciones, etc.).
Usa **este skill** cuando `jira-cli` **no cubra** la operación o necesites una llamada REST directa.

## Quick start (scripts)

Script principal (sin dependencias externas):

- `skills/work/jira-api/scripts/jira_api.py`

Ejemplos:

1) Buscar issues por JQL (API nueva):

```bash
./skills/work/jira-api/scripts/jira_api.py search-jql "worklogAuthor = currentUser() AND worklogDate >= 2026-03-09 AND worklogDate <= 2026-03-15" --fields key,summary,status --max 100
```

2) Listar worklogs de una issue (y filtrar por rango de fechas):

```bash
./skills/work/jira-api/scripts/jira_api.py list-worklogs DES-355 --from 2026-03-09 --to 2026-03-15
```

3) Borrar un worklog concreto (revertir imputación):

```bash
./skills/work/jira-api/scripts/jira_api.py delete-worklog DES-355 29978 --adjustEstimate auto
```

4) Actualizar un worklog (tiempo / comentario / started):

```bash
./skills/work/jira-api/scripts/jira_api.py update-worklog DES-355 29978 --timeSpent "3h 30m" --comment "Ajuste" --started "2026-03-10 12:00:00" --timezone Europe/Madrid --adjustEstimate auto
```

5) Llamada REST genérica (para cubrir lo que falte):

```bash
./skills/work/jira-api/scripts/jira_api.py request GET /rest/api/3/myself
```

## Operativa y seguridad

- Autenticación esperada: **API token en `~/.netrc`** (no pegar tokens en chat).
- No imprimir respuestas que puedan contener secretos; si necesitas compartir, recorta y elimina cabeceras.
- Antes de acciones destructivas (DELETE/ediciones masivas): confirmar con César.

## Qué NO cubre `jira-cli` (motivación típica)

- **Borrar/editar worklogs** (en nuestro entorno, `jira issue worklog` solo tiene `add`).
- Operaciones REST puntuales que Jira Cloud expone pero el CLI no.
- Automatizaciones de “revertir”, “mover imputación”, “arreglar estimaciones”.

## Sprints / Agile (rápido)

El tablero DES suele ser el **184**.

```bash
# Ver sprints activos
./skills/work/jira-api/scripts/jira_api.py sprint-list --board 184 --state active

# Ver issues de un sprint
./skills/work/jira-api/scripts/jira_api.py sprint-issues <SPRINT_ID> --fields key,summary,status --max 200
```

## Referencias

- Notas REST mínimas: `references/jira-rest-notes.md` (endpoints + ADF).
- Mapa de endpoints (equivalencias con jira-cli): `references/endpoint-map.md`.
- Agile/Sprints: `references/agile-sprints.md`.
