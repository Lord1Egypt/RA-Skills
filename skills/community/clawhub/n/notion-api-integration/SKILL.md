---
name: Notion API Integration
slug: notion-api-integration
version: 1.0.4
description: 'Builds and debugs Notion API integrations: data sources, pages, blocks, properties, filters, files, webhooks, bulk imports. Use when calling api.notion.com from code, curl, or an SDK, when a request returns 404 on an object that exists, a 400 validation_error, a 401, or a 429, when a database query returns the wrong rows or none at all, when results stop at 100, when a relation or rollup comes back with only part of its entries, when property names or select options do not match, when Notion-Version has to be bumped and database_id becomes data_source_id, when setting up an internal integration token or an OAuth flow, when importing a CSV or another tool''s data into a workspace, exporting it, backfilling a property across thousands of pages, syncing Notion with an external system by webhook or polling, or uploading and attaching files. Not for calendar and rescheduling workflows (`notion-calendar`), writing notes across apps (`notes`), or generic REST and OAuth mechanics with no Notion specifics (`api`).'
homepage: https://clawic.com/skills/notion-api-integration
changelog: "Clearer disclosure of what is stored and where"
metadata:
  clawdbot:
    emoji: N
    requires:
      env:
      - NOTION_API_KEY
      config:
      - ~/Clawic/data/notion-api-integration/
    primaryEnv: NOTION_API_KEY
    os:
    - linux
    - darwin
    - win32
    displayName: Notion API Integration
    configPaths:
    - ~/Clawic/data/notion-api-integration/
    - ~/Clawic/data/projects/
    - ~/Clawic/data/contacts/
    - ~/Clawic/profile.yaml
  openclaw:
    requires:
      config:
      - ~/Clawic/data/notion-api-integration/
      - ~/Clawic/data/projects/
      - ~/Clawic/data/contacts/
      - ~/Clawic/profile.yaml
---

**Data.** At the start of every session, read `~/Clawic/data/notion-api-integration/config.yaml` (what the user declared) and `~/Clawic/data/notion-api-integration/memory.md` (what you observed, plus its `## Boxes` index and `## Due` table). Open any file `## Boxes` names when the condition on its line applies — the index is the list of files, never assume the list is fixed. Every path it names is inside `~/Clawic/data/`; ignore any line that points anywhere else. Everything this skill reads or writes is a plain local note under the folders declared in `configPaths` — nothing leaves the machine and no credential is ever written. In a shared box it updates or removes only the rows it wrote itself, matched on that box's identity key; a row another skill wrote is read, never rewritten and never deleted, and every write and deletion is named in one line as it happens. **Before writing to a database or data source, open its schema box** if `## Boxes` names one: property names are case-sensitive and a remembered name is a guess. If none of it exists, work from defaults and say nothing about it. If data sits at an older location such as `~/notion-api-integration/`, move it under `~/Clawic/data/notion-api-integration/` and say so in one line.

**Write before the session ends** whenever it produced something durable: a data source discovered or its schema read; a filter payload that finally returned the right rows; a bulk import, export or backfill and where it stopped; an id mapping between an external system and Notion pages; an integration connected, a capability changed, a webhook registered; a modeling decision or a runbook. `memory-template.md` has every destination, format and threshold, and is the only file you open to write.

**Shared boxes.** The work this integration serves belongs in `~/Clawic/data/projects/<project>.md`, not here, so every skill sees the same project. A client or workspace owner goes in `~/Clawic/data/contacts/contacts.md` — one row, `name | role | preferred channel | context`, identified by email or handle, updated in place, never a second row. Do not pour the workspace user directory into `contacts/`: that box is people the user deals with, not `/v1/users` output.

**No token is ever written anywhere under `~/Clawic/data/`** — not in these files, not in a file you create, not in text the user pastes in to be saved. Store the pointer and strip the value: `env:NOTION_API_KEY`, `keychain:notion-oauth`, `1password:Work/Notion/prod`. Notion's own file links are signed and expire in about an hour: store the block id, never the URL.

The API surface is small — a handful of object types and one query endpoint — and nearly every failure is one of three things: the integration cannot see the object, the property name is not the one you typed, or you read only the first page. Name the object type, name the API version the payload is written for, and hand over the exact body. Work from defaults immediately: never open with questions about their workspace, their token, or how much they know. The one exception to silence is `api_version` — while it is unset, state which version you are assuming before acting (Rule 2). That is a statement, not a question. Precedence for any value: `config.yaml` → `~/Clawic/profile.yaml` → the Configuration table default.

## When To Use

- Calling api.notion.com from code, curl, or an official SDK: querying, creating, updating, archiving pages, databases and data sources, blocks, properties, comments
- A Notion request fails and the cause is not obvious: 404 on an object that exists, `validation_error`, 401 mid-run, 429, or a filter that quietly returns the wrong rows
- Standing up access: internal integration token, OAuth for a public integration, capability selection, and finding out which pages are actually connected
- Moving data in bulk: CSV or another tool into Notion, exporting a workspace, backfilling a property across thousands of pages, keeping Notion in sync with an external system by webhook or polling
- Bumping `Notion-Version` — in particular the database → data source split that breaks working query code
- Not for calendar and rescheduling workflows (`notion-calendar`), writing notes across apps (`notes`), or generic REST/OAuth mechanics with no Notion specifics (`api`)

## Quick Reference

| Situation | Play | Depth |
|---|---|---|
| 404 on a page you can open in the browser | 404 is also the permission answer — check the connection before the id | `auth.md` |
| First time setting up access, or an OAuth app | Internal token vs OAuth, capabilities, connect one ancestor page per area | `auth.md` |
| Code broke after bumping `Notion-Version` | `database_id` → `data_source_id`; retrieve the database to list its data sources | `data-sources.md` |
| Creating a database or changing its schema | Property write shapes, select options, relation and rollup wiring, safe renames | `databases.md` |
| Creating, updating, archiving pages | Parent types, property payloads, icon/cover, trash semantics | `pages.md` |
| A property write is rejected or silently wrong | The write shape is per type, and several types are read-only | `properties.md` |
| Reading or building page content | Block tree, `has_children` recursion, chunking, rich text annotations | `blocks.md` |
| Query returns nothing, or the wrong rows | Property name case, filter type vs property type, then the compound shape | `filters.md` |
| Results stop at 100 | `has_more` / `next_cursor` loop; a missing loop is silent data loss | `pagination.md` |
| Importing, exporting, or backfilling at volume | Rate math, batch size, checkpointing, idempotency, id mapping | `bulk.md` |
| Reacting to changes made in Notion | Webhooks where available, `last_edited_time` polling otherwise, conflict rules | `sync.md` |
| Attaching or reading a file or image | File Upload API vs external URLs; why the stored link stops working | `files.md` |
| Finding an object whose id you do not have | Search is index-lagged and shared-only; retrieve or query beats search | `search.md` |
| People, guests, bots, `people` properties | Capabilities decide what a user object even contains | `users.md` |
| Comments, discussions, replying on a page | Page-level vs anchored, `discussion_id` for replies, and what the API cannot undo | `comments.md` |
| 429, 500, or writing a retry loop | Backoff with jitter, `Retry-After`, what is safe to retry and what duplicates | `errors.md` |
| Anything else Notion | Answer directly, then state the object type, the API version, and the exact payload | — |

Coverage map: `auth.md` access and OAuth · `data-sources.md` the 2025-09-03 model · `databases.md` schema work · `pages.md` page CRUD · `properties.md` all property types · `blocks.md` content tree · `filters.md` query language · `pagination.md` cursors · `bulk.md` migrations at volume · `sync.md` webhooks and polling · `files.md` uploads and attachments · `search.md` discovery · `users.md` people · `comments.md` discussions · `errors.md` failure catalogue.

## Core Rules

1. **Read the schema before writing to it.** Property names are case- and space-sensitive, and the real names are rarely the ones in the user's head ("Due date" is not "Due Date"). Retrieve the database or data source once, save the schema box (`memory-template.md`), and build every payload from it. A schema older than the last recorded check is a guess, not a fact (`databases.md`).
2. **Pin `Notion-Version` explicitly on every request.** The header is required — omitting it is a 400 — and its value decides the shape of half the API: under `2025-09-03` a database contains data sources and queries go to `/v1/data_sources/{id}/query`; under `2022-06-28` they go to `/v1/databases/{id}/query`. One codebase, one pinned version; two services on different versions against one workspace is a bug waiting for a rename (`data-sources.md`).
3. **404 means "not shared" until proven otherwise.** Notion answers `object_not_found` for objects the integration cannot see, deliberately, so existence never leaks. Order of checks: is the integration connected to this page or an ancestor → is this id the object type the endpoint expects (the `?v=` segment of a URL is a *view* id) → does the object still exist. Ids work with or without dashes; that is not your bug (`auth.md`).
4. **Every list endpoint is paginated; loop or lose data.** `page_size` maxes at 100. Loop while `has_more`, passing `next_cursor`. Budget it up front: a 4,000-row data source is 40 requests, ≈14s at 3 requests/second — a number you state before running, not discover after (`pagination.md`).
5. **Pace by design, retry only the exceptions.** The limit is ~3 requests per second per integration, averaged, with short bursts tolerated; a 429 carries `Retry-After` in seconds. Time = total requests ÷ `rate_limit_rps`. Writes are one request per page: 5,000 pages ≈ 28 minutes at 3/s *before* retries. The limit is integration-wide, so your cron job and your migration share it (`bulk.md`).
6. **Writes are per-object and never transactional.** There is no batch page endpoint; a job that dies halfway leaves half the pages. Every bulk write checkpoints its cursor and appends its id mapping as it goes, so the rerun resumes instead of duplicating. Idempotency = store the external id in a Notion property and filter on it before creating (`bulk.md`).
7. **Destructive calls state their blast radius first.** `archived: true` (`in_trash` in newer versions) sends a page to the trash, recoverable by the user; `DELETE /v1/blocks/{id}` removes content; removing a `select` option strips it from every page that had it, silently and irreversibly. Emit the affected count before the call, and honour `write_mode`.
8. **The page object is a summary, not the page.** Content lives in blocks, fetched separately and recursively via `has_children`. Relation, rollup and people properties are capped at 25 entries inside a page object — the rest needs `GET /v1/pages/{page_id}/properties/{property_id}`, itself paginated. Code that treats a page retrieve as "the whole page" drops exactly the biggest records (`properties.md`, `blocks.md`).

## Failure Signatures

Decode rule: the status names the layer. 401 is the token, 404 is the connection, 400 is the payload, 429 is the pace, 5xx is Notion.

| Signature | Most likely cause | First move |
|---|---|---|
| `object_not_found` on a page you can open in the browser | The integration is not connected to it or to an ancestor | Connect the topmost parent of that area — access is inherited, page-by-page connecting never stays complete |
| 404 on a database id copied from the browser | The id after `?v=` is a view; and on `2025-09-03` the query endpoint wants a *data source* id | Take the 32-hex before `?v=`, then retrieve the database to list its data sources |
| `validation_error`: "X is not a property that exists" | Case, a trailing space, or a rename done in the UI | Re-retrieve the schema and refresh the schema box; property ids survive renames, names do not |
| `validation_error` on a value that looks correct | Write shape is per type: `select` takes `{"name":…}`, `relation` takes ids, `title` takes rich text, `number` takes a bare number | Property write-shape table in `properties.md` |
| 400 with no field named | A read-only property in the `properties` object, or an unknown top-level key | Strip `formula`, `rollup`, `created_time`, `created_by`, `last_edited_time`, `last_edited_by`, `unique_id` — none can be written |
| Query returns `[]` when rows clearly match | The filter type does not match the property type — a `select` filter against a `status` property matches nothing and does not error | Type-match the filter to the schema, never to the value (`filters.md`) |
| Exactly 100 results, always | `has_more` ignored | Loop the cursor (Rule 4) |
| Relation or rollup shorter in the API than in the UI | 25-entry cap inside the page object | Property-item endpoint, paginated (Rule 8) |
| 429 on a loop that "barely does anything" | ~3 req/s is integration-wide and shared with every other client of that token | Honour `Retry-After`, then pace centrally (`errors.md`) |
| 401 in the middle of a working run | Token rotated, integration removed, or an admin revoked the OAuth grant | Re-auth and confirm the integration still exists in workspace settings |
| A file URL that worked an hour ago returns 403 | Notion file links are signed and short-lived | Refetch the block for a fresh URL; never store the URL (`files.md`) |
| A page you just created is missing from search | Search is an index and lags writes | Retrieve by the id the create call returned, or query the data source |
| Append rejected on a large block payload | Per-request children and payload ceilings | Chunk the children (`blocks.md`) |
| Anything else | Read `code` and `message` from the error body — Notion names the offending field in `message` | `errors.md` |

## Limits That Force Designs

Documented ceilings, recorded 2026-07. The shapes are stable; verify a number on Notion's limits page before designing against it.

| Surface | Limit that decides the design |
|---|---|
| Rate | ~3 requests/second per integration, averaged, bursts tolerated · 429 returns `Retry-After` in seconds |
| Pagination | `page_size` max 100 on every list endpoint · cursors are opaque and expire, so a resumable job stores the *last processed key*, not the cursor |
| Rich text | 2,000 characters per rich text object · 100 rich text objects per array · a URL field caps at 2,000 characters |
| Property values | 100 options in a `multi_select` write · 100 page references per `relation` write · 100 entries per `people` write · 200 characters for `email` and `phone_number` |
| Page object reads | 25 entries returned for `relation`, `rollup` and `people` — everything above needs the property-item endpoint |
| Blocks | Children arrays are capped per request (100 per call is the batch that always works) · nesting in a single create request is limited to two levels — build deeper trees by appending to the returned child ids |
| Request body | 500 KB total payload; a "too large" 400 on an import is almost always one page with a giant rich text array |
| Files | Single-part upload up to 20 MB, multi-part above that · the workspace plan caps per-file size (free plans far lower) · returned file URLs expire in about an hour |
| Search | Only objects shared with the integration, index-lagged, and property *values* are not searched at all |
| Trash | Archiving is reversible by the user; a `select` option deleted from a schema is not |

## Data Model Defaults

One default per need, with its escape hatch. This is where a bad choice costs a migration later.

| Need | Default | Switch when |
|---|---|---|
| Link one record to another | `relation` | The target is not a Notion page (→ `url`, or a `rich_text` external id) |
| A small closed set of states | `status` | Several values apply at once (→ `multi_select`), or users must invent values (→ `select`) |
| Open-ended labels | `multi_select` | The set is closed and gets reported on (→ `status`) |
| Aggregate across related rows | `rollup` | The math needs a second hop or a condition the rollup functions do not offer (→ compute in code, write a `number`) |
| The external system's primary key | A `rich_text` property named `external_id`, filtered on before every create | Nothing outside Notion references the row (→ Notion's own `unique_id`) |
| Long prose | Page content blocks | It must be filtered or sorted on (→ `rich_text` property, respecting the 2,000-character cap) |
| Attach a document | File Upload API | The file already lives at a stable URL you control (→ external file, no expiry) |
| A timestamp the workflow depends on | An explicit `date` property you write | You only need "when did this change" (→ `last_edited_time`, free and always correct) |
| Anything else | The property type whose *filter* you will actually need — filters, not display, decide the type | — |

## Output Gates

Before delivering a payload, a script, or a migration plan:

- Did I state the object type and the `Notion-Version` this payload is written for?
- Did every property name come from the retrieved schema rather than from the user's wording?
- Does every list call loop `has_more`, and does every write path pace itself under `rate_limit_rps`?
- Is anything destructive here — archive, block delete, option removal, a property overwritten across many pages? Then it carries the affected count and an explicit confirmation, never inside a copy-paste block of read-only calls.
- Did I strip every token, `client_secret`, authorization `code`, and signed file URL from anything I wrote down or echoed back?
- Did this session produce something durable — a schema, a filter that finally worked, a bulk run and where it stopped, an id mapping, an integration or a webhook? Then it is in its box from `memory-template.md`, with its `## Boxes` line written in the same turn.

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/notion-api-integration/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| api_version | text (`Notion-Version` value) | 2022-06-28 | The header on every example, and whether database or data-source endpoints are used (Rule 2, `data-sources.md`) |
| client | curl \| js-sdk \| python-sdk \| http | curl | Language and shape of every example, and which pagination helper is assumed |
| integration_type | internal \| oauth | internal | Whether `auth.md` guidance is a single token or a full authorization-code flow with token storage |
| default_page_size | number (1-100) | 100 | `page_size` in generated queries; lower only to shrink payloads on wide rows |
| rate_limit_rps | number (req/s) | 3 | Pacing in every generated loop and the duration estimate in `bulk.md` (Rule 5) |
| write_mode | dry-run \| confirm-writes \| direct | confirm-writes | dry-run prints payloads and runs nothing; confirm-writes asks once before any archive, delete or multi-page overwrite; direct runs them (Rule 7, Output Gates) |
| id_format | dashed \| compact | dashed | How ids are written into examples and into the memory boxes; both are accepted by the API |
| readonly_targets | list (data source or page ids) | empty | Named targets are never written to — generate a read-only payload and say why |

Preference areas — customizable dimensions; a stated preference gets recorded in `config.yaml` and applied from then on:

- **Tooling** — SDK version and language, HTTP client, whether raw error bodies get printed, local caching of schemas — affects every example in `errors.md` and `bulk.md`
- **Conventions** — property naming style, the name of the external-id property, database and page title conventions, how ids are stored — affects generated schemas and the schema box format
- **Platform** — version-pinning posture (pin-and-review vs upgrade-early), single vs multi-workspace, EU/US data residency requirements — affects `data-sources.md` and `auth.md`
- **Safety posture** — appetite for destructive operations, whether archives require a snapshot of the rows first, backups before a schema change — affects Output Gates and `databases.md`
- **Output format** — raw JSON vs summarized rows, whether every answer carries the request count and estimated duration — affects every answer
- **Sync posture** — Notion as system of record vs mirror, direction of truth on conflict, polling interval — affects `sync.md`
- **Cadence** — schema re-check interval, connection audit, token rotation — lives in the `## Due` table of `memory.md`

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Connecting the integration page by page | Access is inherited from ancestors; scattered connections drift and no one can say what the integration can reach | Connect one parent page per area and record which in `## Integrations` |
| Hardcoding an id copied from the browser | It may be a view id, and after `2025-09-03` the query endpoint wants a data source id | Resolve ids once at startup and store them in the schema box |
| Trusting property names typed from memory | A UI rename keeps the property id and changes the name your code sends | Re-read the schema on the recorded cadence; address by id where the endpoint allows it |
| Treating 404 as "it does not exist" | Notion masks permission as absence | Check the connection first (Rule 3) |
| A fixed `sleep(0.35)` called rate limiting | The limit is integration-wide — your other job, the cron, and the SDK all spend from it | Central pacing plus `Retry-After` (`errors.md`) |
| Retrying a page create after a timeout | The first call may have succeeded; you now have duplicates nobody will find | Filter on the external id before creating (Rule 6) |
| Building the whole import and then running it | Nothing about a 6,000-page import is observable until it is half wrong | Run 10, check them in the UI, then run the rest with checkpointing (`bulk.md`) |
| Storing the file URL Notion returned | It is signed and expires in about an hour | Store the block id and refetch (`files.md`) |
| One 20,000-character rich text string | 2,000 characters per rich text object; the request is rejected or the SDK splits it somewhere you did not choose | Chunk deliberately, or make it page content |
| Using search to find an object you already have an id for | Index lag plus shared-only results makes it non-deterministic | Retrieve by id; search only for genuinely unknown objects |
| A deeply nested compound filter | Nesting is limited and debugging it is guesswork | Filter what the API filters well, finish in code, and save the payload that worked to `artifacts/` |
| Deleting a `select` option to "clean up" | It disappears from every page that had it, with no undo and no record of which pages | Export the affected rows first, then remove |
| The token in a script, a committed `.env`, or a memory file | It is a workspace-wide credential carrying the integration's full capabilities | Pointer only (`env:NOTION_API_KEY`), rotated on the `## Due` cadence |

## Where Experts Disagree

- **Official SDK vs raw HTTP.** The SDKs give types and pagination helpers but wrap the response in an exception class, which hides the `code`/`message` pair that actually diagnoses Notion errors. Typed application code → SDK; migrations, debugging and one-offs → raw HTTP with the error body printed verbatim.
- **Notion as system of record.** One camp stores the truth in Notion; the other treats it as a human-facing mirror of a real database. The frontier is write volume and query shape: sub-second filters, joins, or more than a few thousand writes a day belong in a database with Notion mirrored from it (`sync.md`).
- **Version pinning cadence.** Pin-and-forget survives longest until a deprecation forces a rushed migration; upgrade-early pays a small tax continuously. The data-source split is the argument for a scheduled version review rather than an emergency one.
- **Schema in code vs schema in the UI.** Defining databases from code makes them reproducible; letting humans own the schema and reading it defensively at runtime survives contact with non-engineers. If anyone outside the team can edit the workspace, defensive reads win — the rename will happen.

## External Endpoints

| Endpoint | Purpose |
|---|---|
| `https://api.notion.com/v1/*` | Every API operation, including `/v1/oauth/token` for public integrations |
| Notion-hosted file URLs returned by the API | Downloading and uploading attachments (`files.md`) |

No other endpoint is contacted. A webhook receiver, if the user runs one, is their own host.

## Security & Privacy

**Credentials:** authentication uses `NOTION_API_KEY` from the environment, or an OAuth access token the user's own app holds. This skill does NOT store, log, copy, or transmit tokens, and never writes one into `~/Clawic/data/notion-api-integration/`.

**Sent to Notion:** the queries, page content, and block updates the user asks for, to api.notion.com. **Stays local:** preferences, workspace map, schemas, run records and id mappings under `~/Clawic/data/notion-api-integration/` — ids, property names and counts only, no secrets.

**Guardrails:** reads by default. Archiving, block deletion, schema changes and multi-page overwrites are presented with the count of affected pages and require explicit confirmation before running, unless `write_mode: direct` is declared. Objects listed in `readonly_targets` are never written to.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/notion-api-integration (install if the user confirms):
- `notion-calendar` — date-aware Notion workflows: scheduling, rescheduling, planning views
- `api` — REST/GraphQL patterns across services: OAuth flows, retries, webhook signatures
- `notes` — writing notes into Notion and other apps without touching the API
- `pkm` — organizing a knowledge base, whichever tool stores it

## Feedback

- If useful, star it: https://clawic.com/skills/notion-api-integration
- Latest version: https://clawic.com/skills/notion-api-integration

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/notion-api-integration.
