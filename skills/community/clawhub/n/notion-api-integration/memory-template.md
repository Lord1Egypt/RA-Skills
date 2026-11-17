# Working File Templates — Notion API

Read this file only when WRITING. `config.yaml` is what the user **declared**; `memory.md` and everything it indexes is what you **observed** or produced. An observation never overwrites a declaration.

## Where each thing goes

| Data | Home | How it grows |
|---|---|---|
| Declared preferences — table keys and preference areas alike | `~/Clawic/data/notion-api-integration/config.yaml` | Key by key, read-modify-write |
| Workspace context, data-source index, integrations, gotchas, due dates, box index | `~/Clawic/data/notion-api-integration/memory.md` | Rewritten in place; stays small |
| The schema of a database or data source — property names, ids, types, options, relation targets | `~/Clawic/data/notion-api-integration/schemas/<data-source>.md` | Born as its own file, from the first one; re-read before writing to that target |
| Things you produced that get re-read — filter payloads that finally worked, import runbooks, modeling decisions | `~/Clawic/data/notion-api-integration/artifacts/<kebab-name>.md` | Born as its own file, from the first one |
| Bulk runs: imports, exports, backfills — counts, where it stopped, what failed | `~/Clawic/data/notion-api-integration/runs/<year>.md` | Append-only, cut by year |
| External id ↔ Notion page id mappings | `~/Clawic/data/notion-api-integration/mappings/<source>-to-notion.md` | One file per source system, grows by row |
| Integrations, capabilities, connected parent pages, webhook subscriptions | `## Integrations` in `memory.md` while it fits; `integrations.md` after the split | One entry per integration |
| The project this integration serves | `~/Clawic/data/projects/<project>.md` (**shared**) | One file per project |
| A client or workspace owner as a person | `~/Clawic/data/contacts/contacts.md` (**shared**) | One row per person, name only referenced from here |
| **Anything durable this table does not name** | `~/Clawic/data/notion-api-integration/<plural-noun>.md`, or `artifacts/<kebab-name>.md` if it is a long text read whole | Name the file after what it holds, never after when it was made; add its `## Boxes` line in the same turn |
| Tokens, secrets, signed URLs of any kind | Nowhere under `~/Clawic/data/` | Pointer only — see Secrets |

## When to write

No permission needed; every write is announced in one line that names the file. Writes and deletions stay inside the paths declared in this skill's `configPaths`. A deletion is named in that same line, and in a shared box only rows this skill itself wrote are ever updated or removed.

| It happened | Write |
|---|---|
| A database or data source schema was retrieved | `schemas/<data-source>.md`, and its line in `## Workspace` |
| A data source was discovered, renamed, or stopped being used | Its line in `## Workspace` |
| A filter or query payload finally returned the right rows | `artifacts/query-<what>.md` |
| A bulk import, export or backfill ran — or stopped partway | `runs/<year>.md`, with the last processed key |
| Pages were created from an external system | A row per pair in `mappings/<source>-to-notion.md` |
| An integration was connected, its capabilities changed, or a webhook was registered | `## Integrations` |
| A modeling choice was made and rejected alternatives matter | `artifacts/decision-<what>.md` |
| A quirk of *this* workspace cost real time to diagnose | `## Gotchas` — or the schema box if it is specific to one data source |
| The user declared a preference | Its key in `config.yaml` |
| Recurring work was scheduled or run | `## Due` |

## Start flat, split only when it hurts

Everything except schemas, artifacts, runs and mappings begins inside `memory.md`. Splitting is a procedure, not a suggestion:

1. Before appending to a section, count its entries.
2. If the append would take it past **~15 entries or ~40 lines of real content** — scaffolding, headings and comments do not count — then, in the same turn: create the new file in `~/Clawic/data/notion-api-integration/`, move the whole section into it, **delete the section from `memory.md`**, add its line to `## Boxes`, and append the new entry to the new file.
3. Keep the headings identical on both sides of the move, so the split is a copy-paste and never a rewrite.
4. Never leave a copy behind. If the same data ever appears in both places, the extracted file wins and the `memory.md` copy is deleted.

Schemas, artifacts, runs and mappings are the exception: each is born as its own file whatever its size, because each is read whole and only when its subject comes up — you open a schema to write to that data source, not to answer "what does this workspace look like".

## Secrets

Nothing under `~/Clawic/data/` ever holds a secret value — not the files named here, not files you create, not text the user pastes in and asks you to keep. Store the pointer in its place, in this shape: `<kind>:<locator>`.

`env:NOTION_API_KEY` · `keychain:notion-oauth` · `1password:Work/Notion/prod` · `bitwarden:Notion/client-secret` · `vault:secret/notion/prod` · `file:~/.config/notion/token`

When the user pastes something to save — a script, a `.env`, a curl command with its header, an OAuth callback URL — replace each secret value before writing and leave the pointer visible: `Authorization: Bearer <env:NOTION_API_KEY>`. Say in one line that you did it.

In this domain — **not secrets, keep them**: page, block, database, data source, user, bot and workspace ids; property names and ids; select and status option names; integration names and capabilities; `Notion-Version` values; OAuth `client_id` and redirect URIs; the workspace domain.

**Secrets, strip them**: internal integration tokens (`ntn_…`, `secret_…`), OAuth `client_secret`, the authorization `code`, `access_token` and `refresh_token`, the value of any `Authorization` header, webhook verification tokens and signing secrets, and Notion's signed file URLs — those are short-lived credentials in URL form and are worthless an hour later anyway.

**Contents:** [config.yaml](#configyaml) · [memory.md](#memorymd) · [schemas/](#schemas) · [artifacts/](#artifacts) · [runs/](#runs) · [mappings/](#mappings) · [shared project record](#shared-project-record) · [shared contacts](#shared-contacts) · [split-out files](#split-out-files)

## config.yaml

Keys come from the Configuration table in `SKILL.md`, plus free-form keys nested under a preference area. Write a key only when the user states the preference.

**Writing is read-modify-write**: load the existing file, set or replace only the key just declared, keep every other key byte for byte. Never emit a `config.yaml` from this template — the template shows shape, not content. Create `~/Clawic/data/notion-api-integration/` if it does not exist.

```yaml
api_version: "2025-09-03"
client: python-sdk
integration_type: internal
default_page_size: 100
rate_limit_rps: 3
write_mode: confirm-writes
id_format: dashed
readonly_targets:
  - 1a2b3c4d-…            # Finance data source: read-only by agreement

# Preference areas — free-form keys added as the user reveals them.
# A preference the user states is a declaration and belongs here, never in memory.md.
conventions:
  external_id_property: external_id
  title_property: Name
sync_posture:
  source_of_truth: postgres      # Notion is the mirror
  poll_interval_minutes: 15
safety_posture:
  snapshot_before_schema_change: true
```

If you find a preference recorded in `memory.md`, move it here and note the move.

## memory.md

Write only the sections you have content for — a heading with nothing under it is noise, and it inflates the line count that decides a split. Never copy these hints into the user's file. `## Boxes` is the one section that is never dropped when `memory.md` is rewritten: deleting a line there orphans a file forever. This is what a populated file looks like:

```markdown
# Notion API Memory

## Status
status: ongoing
last: 2026-07-26

## Boxes
- Tasks data source schema → `schemas/tasks.md`; read before any write to Tasks
- CRM data source schema → `schemas/crm-companies.md`; read before any write to Companies
- Overdue-by-owner filter that works → `artifacts/query-overdue-by-owner.md`; read when a Tasks query has to filter on owner or date
- Airtable→Notion import runbook → `artifacts/runbook-airtable-import.md`; read before re-running or extending the import
- Bulk runs (2026) → `runs/2026.md`; read before restarting any import, export or backfill
- Airtable id map (4,180 rows) → `mappings/airtable-to-notion.md`; read before creating any page that may already exist

## Due
| What | Every | Last run | Next due |
|------|-------|----------|----------|
| Re-read cached schemas | month | 2026-07-01 | 2026-08-01 |
| Connection audit (what can the integration reach) | quarter | 2026-05-12 | 2026-08-12 |
| Token rotation | year | 2025-11-03 | 2026-11-03 |
| API version review | quarter | 2026-07-10 | 2026-10-10 |

## Workspace
Team workspace, ~40 members. Integration reaches the "Operations" parent page only.

### Data Sources
| Name | Data source id | Parent database | Purpose | Rows (as of) | Schema |
|------|----------------|-----------------|---------|--------------|--------|
| Tasks | 1a2b…c3d4 | Work OS | day-to-day task tracking | ~4,200 (2026-07-20) | `schemas/tasks.md` |
| Companies | 5e6f…a7b8 | CRM | accounts and owners | ~310 (2026-07-20) | `schemas/crm-companies.md` |

### Known Gaps
Marketing databases are not connected to the integration; asked for 2026-08.

## Integrations
| Name | Type | Version pinned | Capabilities | Connected to | Token |
|------|------|----------------|--------------|--------------|-------|
| ops-agent | internal | 2025-09-03 | read, update, insert, comment | Operations (parent page) | env:NOTION_API_KEY |

### Webhooks
- `page.properties_updated` on Tasks → https://ops.internal/hooks/notion, verified 2026-06-30

## Gotchas
Tasks has two properties reading "Owner": `Owner` (people) and `Owner ` (rich_text, trailing space, legacy). Filter on the people one.
Status option "Blocked" was renamed to "Waiting" on 2026-06-11; old filters silently return nothing.

## How They Work
Python SDK, migrations as one-off scripts. Wants the payload and the request count, not the concepts.

---
*Updated: 2026-07-26*
```

Rules that keep this readable next month:

- **`## Boxes`**: one line per file that exists — `<what> (<volume>) → <file>; read when <condition>`. Written in the same turn the file is created. Never delete a line without deleting the file it points to. A box with no index line does not exist.
- **`## Due`**: check it against today's date at the start of a session and state any overdue item in one line — a statement, not a question. Every recurring thing this skill schedules belongs here. Schema re-checks and connection audits are the two that actually prevent failures.
- **`### Data Sources`**: one row per data source, not per database — a database can hold several. Row counts always carry the date they were counted; a count with no date gets re-counted rather than trusted. When the schema file exists, its path goes in the last column and in `## Boxes`.
- **`## Integrations`**: the token column holds a pointer, never a token. When an integration is removed, delete its row and note the date — a list of integrations that only grows stops being an audit.
- `### Data Sources`, `### Known Gaps` are exactly the headings `workspace-map.md` gets when `## Workspace` outgrows this file, so the split stays a copy-paste.

| Status | Meaning |
|---|---|
| `ongoing` | Still learning their workspace |
| `complete` | Know their data sources, schemas and conventions well |

## schemas/

One file per data source, at `~/Clawic/data/notion-api-integration/schemas/<kebab-name>.md`, created the first time you retrieve it. This is the box that pays for itself: every `validation_error` about a property name is a session that did not have it.

```markdown
# Schema — Tasks
*Read before any write to Tasks. Data source `1a2b…c3d4` (database "Work OS"). Retrieved 2026-07-20, Notion-Version 2025-09-03.*

| Property | Id | Type | Writable | Notes |
|----------|-----|------|----------|-------|
| Name | title | title | yes | rich text array, not a string |
| Status | %7BdX | status | yes | To Do · In Progress · Waiting · Done — "Blocked" removed 2026-06-11 |
| Owner | k%3AqP | people | yes | user ids; the trailing-space `Owner ` rich_text is legacy, do not write |
| Due | Nq%5Ea | date | yes | date-only in practice; time zone never set |
| Company | b8%3Fz | relation | yes | → Companies data source `5e6f…a7b8`, dual property |
| Effort | c1%23w | formula | no | read-only |
| external_id | p9%2Bk | rich_text | yes | Airtable record id; filter on it before creating |
```

- Record the property **id** as well as the name: a rename in the UI changes the name and keeps the id, and the id is what tells you a "missing property" is really a rename.
- Record the retrieval date and the API version. A schema is a snapshot, and the `## Due` re-check exists because it goes stale silently.
- Select and status **option names** belong here in full: they are the values your filters compare against, and a removed option is invisible from the outside.
- When a write fails on a property this file describes, re-retrieve before editing anything else, then update this file in the same turn.

## artifacts/

One file per thing, at `~/Clawic/data/notion-api-integration/artifacts/<kebab-name>.md`, created the first time it exists. Canonical types here: **a query payload that finally worked**, **an import or export runbook**, **a modeling decision**. Every artifact opens with when to read it, and gets its `## Boxes` line in the same turn.

```markdown
# Query — overdue tasks by owner
*Read when a Tasks query has to filter on owner or date. Written 2026-07-24, Notion-Version 2025-09-03.*

POST /v1/data_sources/1a2b…c3d4/query
{ "filter": { "and": [ … ] }, "sorts": [ … ], "page_size": 100 }

Why it is shaped this way: `status` needs a `status` filter, not `select`; the people filter takes a user id, not a name.
Returns ~120 rows, 2 requests.
```

```markdown
# Decision — companies as a relation, not a text field
*Read before changing the Tasks or Companies schema. 2026-07-18.*

Decision: Tasks.Company is a dual-property relation to Companies.
Rejected: multi_select of company names — renames orphan history, and rollups become impossible.
Cost of reversal: a backfill over ~4,200 pages, ≈24 min at 3 req/s.
```

If the user tracks this work as a project, the decision summary also belongs in the shared `~/Clawic/data/projects/<project>.md`, with the payload staying here and referenced by name.

## runs/

Append-only, one file per year. Written *while* the job runs, not after it: the value of this box is that a failed import can resume.

```markdown
# Bulk runs — 2026

| Date | Job | Target | Attempted | Created | Updated | Failed | Last processed key | Notes |
|------|-----|--------|-----------|---------|---------|--------|--------------------|-------|
| 2026-07-22 | airtable import | Tasks | 4,200 | 4,180 | 0 | 20 | recAbc123 | 20 failures: rich text over 2,000 chars, listed below |
| 2026-07-25 | owner backfill | Tasks | 4,180 | 0 | 4,180 | 0 | — | 24 min, 3 req/s, no 429s |

## Failures — 2026-07-22 airtable import
recDef456 — description 3,412 chars, needs chunking
```

- **Last processed key is the external key, never the Notion cursor.** Cursors are opaque and expire; a rerun resumes by filtering on the external id.
- Record the measured duration and whether 429s appeared: it is the only honest input to the next estimate.
- A run that was interrupted gets its row written anyway, with what had completed. A missing row means the next session re-imports everything.

## mappings/

One file per source system, at `mappings/<source>-to-notion.md`. Read before creating any page that might already exist.

```markdown
# Airtable → Notion — Tasks
*Read before creating a Tasks page from Airtable. 4,180 pairs, last appended 2026-07-22.*

| External id | Notion page id | Created |
|-------------|----------------|---------|
| recAbc123 | 9f8e…7d6c | 2026-07-22 |
```

- Append as you create, not at the end — a crash halfway through must leave the pairs already written.
- Past ~2,000 rows the file is only useful to a script, so keep the columns fixed and never reformat it.
- The mapping is a convenience copy: the authority is the `external_id` property on the Notion page itself, which is what the pre-create filter checks.

## Shared project record

Lives at `~/Clawic/data/projects/<project>.md` and is shared with every other skill — the user may not have any of them installed, so the format travels with this skill.

```markdown
# Project — Airtable to Notion migration

Goal: retire Airtable, Tasks and Companies live in Notion.
Status: import done 2026-07-22, two-way sync pending.
Decisions: Company modeled as relation (see notion-api-integration artifacts).
Milestones: import ✓ · backfill ✓ · sync — 2026-08.
```

- **Identity is the project name**, which is the filename slug. Read the folder before creating a file: if a project by that name exists, update it in place; only its absence justifies a new file.
- Add your lines, never rewrite sections another skill wrote. If the file already uses different headings, follow them.
- Notion-specific detail (payloads, schemas, id maps) stays in this skill's folder; the project file gets the one-line summary and the pointer by name.
- When the project ends, mark it closed with the date rather than deleting the file.

## Shared contacts

Lives at `~/Clawic/data/contacts/contacts.md`. Only people the user actually deals with — a client whose workspace this is, the admin who grants connections. Never the output of `/v1/users`.

```markdown
# Contacts

| Name | Role | Preferred channel | Context |
|------|------|-------------------|---------|
| Marta Ruiz | Notion workspace admin at Acme | email marta@acme.com | grants integration connections; approves schema changes |
```

- **Identity is the email or handle.** Read the file before adding. If that person is already there, update the row in place — never a second row. Rows written by other skills are not yours to rewrite.
- **Foreign columns win.** If `contacts.md` already exists with a different column set, match its columns and add anything missing as a trailing note. Never rewrite its header.
- **Scale cut**: one row per person while there are ≤15. Past that, one file per person at `~/Clawic/data/contacts/<name>.md` with the same fields, and `contacts.md` becomes the index (`Name | Role | → file`). If you arrive and the folder already looks like that, follow it — do not start a parallel `contacts.md`.
- **Removal is part of the box.** When a person is no longer involved, delete the row and note the date in `memory.md`.
- Any amount recorded carries its currency in the value (`90 USD/mo`), because other skills add these columns up.
- Never a token, password, or invite link — a pointer at most.

## Split-out files

Created only by the split procedure above, never on day one. Each keeps the exact headings it had inside `memory.md`.

`workspace-map.md` — `## Data Sources`, `## Known Gaps`. Appears once a workspace has more than ~15 tracked data sources; `memory.md` keeps only the `## Boxes` line pointing here.

`integrations.md` — `## Integrations`, `## Webhooks`. Appears when several integrations or several webhook subscriptions exist; it is also what a connection audit reads and updates.
