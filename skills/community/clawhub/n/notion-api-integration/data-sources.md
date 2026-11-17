# Data Sources — The Model Change That Breaks Working Code

Recorded 2026-07. Under `Notion-Version: 2025-09-03` a database is a container that holds one or more **data sources**, and the thing you query is the data source. Older versions keep the one-database-one-schema model. Nothing else in the API moved this much.

**Contents:** [What Changed](#what-changed) · [Which Version Am I On](#which-version-am-i-on) · [Resolving a Data Source Id](#resolving-a-data-source-id) · [Endpoint Map](#endpoint-map) · [Migrating Existing Code](#migrating-existing-code) · [Multi-Source Databases in Practice](#multi-source-databases-in-practice) · [Version Policy](#version-policy)

## What Changed

| Concept | `2022-06-28` | `2025-09-03` |
|---|---|---|
| Holds the schema | The database | The data source |
| You query | `/v1/databases/{database_id}/query` | `/v1/data_sources/{data_source_id}/query` |
| A page's parent | `{"database_id": …}` | `{"type": "data_source_id", "data_source_id": …}` |
| Retrieve a database | Returns properties | Returns metadata plus a `data_sources` array |
| One schema per database | Always | Not necessarily |

The important consequence: **a `database_id` is not a valid query target on the new version**, and the id you have stored from an earlier integration is almost certainly a database id. This is the single most common reason a working integration breaks after a version bump.

## Which Version Am I On

`api_version` in `config.yaml`, default `2022-06-28`. When it is unset, say which version you are assuming before generating a payload (SKILL.md Rule 2) — the payloads are not interchangeable and a silent guess produces a 400 or, worse, writes to the wrong parent shape.

Signals that the answer is the new model:
- `GET /v1/databases/{id}` returns a `data_sources` array
- The workspace has databases with multiple sources or linked views the team calls "sources"
- Existing code queries `/v1/data_sources/...`

Signals for the old model: property definitions come back directly on the database object, and page parents are `database_id`.

## Resolving a Data Source Id

Do this once at startup, never per request, and write the result to `### Data Sources` in `memory.md`:

```bash
curl 'https://api.notion.com/v1/databases/DATABASE_ID' \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03"
```

The response lists each data source with its id and name. With one source, that id replaces the database id everywhere. With several, the *name* decides which one — and the names are user-editable, so store the id and keep the name as a label only.

Getting the database id itself from a URL: it is the 32-hex segment **before** `?v=`. Everything after `?v=` identifies a view, which is not addressable by the API at all. Dashes are optional in either form.

## Endpoint Map

| Operation | `2022-06-28` | `2025-09-03` |
|---|---|---|
| Query rows | `POST /v1/databases/{id}/query` | `POST /v1/data_sources/{id}/query` |
| Read schema | `GET /v1/databases/{id}` | `GET /v1/data_sources/{id}` |
| Change schema | `PATCH /v1/databases/{id}` | `PATCH /v1/data_sources/{id}` |
| Create a row | `POST /v1/pages` with `parent.database_id` | `POST /v1/pages` with `parent.data_source_id` |
| Create the container | `POST /v1/databases` | `POST /v1/databases`, then a data source under it |
| Find databases | `POST /v1/search` filtered to `database` | Same — search returns containers, then resolve sources |

Everything else — pages, blocks, users, comments, search, pagination, rate limits — is unchanged by the version bump.

## Migrating Existing Code

Order matters; steps 1-2 are read-only and can run against production safely.

1. Retrieve every database id the code uses on the new version and record the data source id for each in `### Data Sources`. Do not touch code yet.
2. Diff the schemas: property ids are preserved across the model change, names may not be if someone reorganized at the same time. Refresh every `schemas/<data-source>.md` box.
3. Replace query endpoints and page-parent shapes in one commit — a codebase half-migrated against one workspace produces failures that look intermittent.
4. Bump the pinned header last, in the same commit, and set `api_version` in `config.yaml`.
5. Run the read paths first, then one write against a single row, then the rest.

Rollback is: revert the commit. Both versions keep working against the same workspace, which is what makes a staged migration possible — and what makes a *partial* one dangerous.

## Multi-Source Databases in Practice

- Each data source has its own schema. "Add a property to the database" is not a thing; you add it to a source.
- Rows belong to a source, not to the database. A page created with the wrong `data_source_id` lands in a sibling table where nobody looks for it.
- Filters and sorts are per source, so a query cannot span two sources — union them in code.
- A relation targets a data source. When a target database gains a second source, verify which one the existing relation points at before assuming.

## Version Policy

- Pin one version per codebase and put it in `config.yaml`. Different services on different versions against one workspace is legal and is how a rename becomes a mystery.
- Old versions keep working; Notion announces deprecations with notice. That is an argument for a scheduled review, not for never moving.
- Put the review in `## Due` (`API version review`, quarterly is enough) and record the outcome even when the answer is "stay".

**After resolving ids or migrating a version**, write the data source ids, their parent database and the version each schema was read under into `### Data Sources` and the `schemas/` boxes of `~/Clawic/data/notion-api-integration/`, and record the migration decision in `artifacts/decision-<what>.md`. Re-deriving this mapping costs a full pass over the workspace.
