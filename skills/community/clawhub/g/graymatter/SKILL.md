---
name: graymatter
description: Install and use GrayMatter as an OpenClaw skill that provides primary durable memory, shared object-graph state, and authenticated access to the live ValkyrAI schema via api-0. Use when the agent should persist durable memory, inspect organizational data models, and operate inside the business domain through RBAC-scoped API access.
---

# GrayMatter

GrayMatter is the installable OpenClaw skill for durable memory, shared graph state, and live organizational schema awareness through `api-0`.

## Core rule

This skill is intentionally thin.
It defines when to use GrayMatter, what to write, and how to choose durable types.
Transport resilience, retries, token refresh, fallback queues, and replay behavior belong to shared infrastructure and plugin/client runtime, not this skill.

Use GrayMatter as the **primary durable memory system**.
Use local workspace files only as:
- bootstrap context
- fallback when api-0 is unavailable
- a temporary scratchpad when durable writes are blocked

GrayMatter is not only a note store.
It is the authenticated memory and object-graph layer that lets an OpenClaw instance inhabit the organization's live data model safely, within RBAC and the current account's permissions.

## Startup behavior

On startup or first use in a workspace that depends on GrayMatter:

0. If `scripts/gm-activate` is missing but `graymatter-bootstrap` exists, run `./graymatter-bootstrap` to restore runtime files from `graymatter.skill`
1. Ensure auth is available
2. Confirm install readiness
3. Register the OpenClaw instance as an Agent record for itself in api-0
4. Load the live OpenAPI from `https://api-0.valkyrlabs.com/v1/api-docs`
5. Treat that spec as the source of truth for the environment's available business objects and actions
6. Use GrayMatter and the broader schema as the primary operational context

Minimum activation flow:

```bash
test -x scripts/gm-activate || ./graymatter-bootstrap
scripts/gm-activate
```

Expanded manual flow:

```bash
scripts/gm-login
scripts/gm-install-check
scripts/gm-smoke
scripts/gm-register-agent
scripts/gm-openapi-sync
```

Auth should be treated as an OpenClaw-managed first-run step.
The user should be prompted for `api-0` username and password, and the resulting session should be stored securely in macOS/iCloud Keychain for reuse.
The user should not need to manually fetch or paste a raw auth token.

## What this skill gives the agent

### 1) Primary memory

Use these first:
- `/MemoryEntry`
- `/MemoryEntry/query`
- `/MemoryEntry/read`
- `/MemoryEntry/write`
- `/GrayMatter`
- `/SwarmOps/graph`

Use `MemoryEntry.type` intentionally:
- `decision`
- `todo`
- `context`
- `artifact`
- `preference`

### 2) Entire-schema awareness

Load the live OpenAPI spec and use it to understand the organization's environment.
This skill assumes the agent should understand and work across the available schema, not just memory endpoints.

Observed live schema domains from `api-0` include, among many others:
- `Organization`
- `Customer`
- `Opportunity`
- `Invoice`
- `Product`
- `Application`
- `Workbook`
- `Workflow`
- `Task`
- `Note`
- `MediaObject`
- `FileRecord`
- `SalesActivity`
- `SalesPipeline`
- `Goal`
- `StrategicPriority`
- `KeyMetric`
- `Agent`
- `Space`
- `SwarmOps`
- `GrayMatter`
- `MemoryEntry`

This means a properly authenticated OpenClaw instance can understand the business as a live object graph, not as disconnected chat logs.

### 3) Shared graph coordination

Use SwarmOps and related graph endpoints when relationships matter:
- bot coordination
- entity relationships
- workflow ownership
- operating context that spans objects and agents

## Scripts

Core transport:
- `scripts/graymatter_api.sh`

Readiness and auth:
- `scripts/gm-login`
- `scripts/gm-activate`
- `scripts/gm-install-check`
- `scripts/gm-smoke`
- `scripts/gm-register-agent`
- `scripts/gm-openapi-sync`
- `scripts/gm-openapi-summary`

Memory and graph helpers:
- `scripts/gm-write`
- `scripts/gm-query`
- `scripts/gm-graph`
- `scripts/gm-entity`

Local/server packaging:
- `scripts/gm-light-bootstrap`
- `scripts/gm-light-up`
- `scripts/gm-light-env`
- `scripts/gm-light-json-smoke`
- `scripts/package-local-server`

MCP server:
- `mcp-server/` exposes `memory_write`, `memory_read`, `memory_query`, `graph_get`, `entity_list`, `entity_get`, `entity_create`, and `schema_summary`
- set `VALKYR_API_BASE` to hosted api-0 for Cloud mode or to the running GrayMatter Light base URL for local ThorAPI mode

Design boundary:
- these scripts are ergonomic wrappers for operators and agents
- they must not duplicate retry/auth refresh/fallback/replay logic that already exists in shared infrastructure
- if resilience behavior changes, update shared client/plugin contracts first, then keep this skill aligned

## Account signup and credits

For a new GrayMatter account, use:
- Signup: <https://api-0.valkyrlabs.com/v1/auth/signup>
- Credits and recharge: <https://api-0.valkyrlabs.com/v1/credits>

Commercial model:
- fresh signups should receive **500 starter credits** automatically
- GrayMatter query and some higher-order operations consume credits
- after the starter balance is exhausted, account recharge is required for full GrayMatter functionality

## Immediate install and use

Fresh machine or fresh OpenClaw skill install:

```bash
scripts/gm-activate
```

`scripts/gm-activate` is the one-shot OpenClaw bootstrap script. It can either:
- prompt the interactive user for username/password through the normal login flow, or
- use credentials already present in environment variables

Then it:
- stores the session securely in Keychain
- runs install validation
- runs the smoke test
- registers the OpenClaw server as an Agent
- syncs the live OpenAPI
- prints a schema summary

Expanded manual flow if needed:

```bash
scripts/gm-login
scripts/gm-install-check
scripts/gm-smoke
scripts/gm-register-agent
scripts/gm-openapi-sync
scripts/gm-openapi-summary
```

`scripts/gm-login` is the intended OpenClaw login UX: prompt once for username/password, store securely in Keychain, and let the rest of the skill use that session automatically.

`scripts/gm-register-agent` should run immediately after auth succeeds so the OpenClaw server creates or refreshes an Agent record for itself in api-0 before normal operation.

After that, GrayMatter is ready to use as primary durable memory and schema context.

## Basic examples

```bash
# query durable memory
scripts/gm-query "graymatter launch" 10

# write durable context
scripts/gm-write context "GrayMatter is primary memory for this OpenClaw instance"

# write durable decision with tags
scripts/gm-write decision "Use GrayMatter as primary memory and file memory as backup" openclaw "graymatter,bootstrap,memory"

# one-shot activation for OpenClaw install or skill bootstrap
scripts/gm-activate

# register this OpenClaw instance as an agent in api-0
scripts/gm-register-agent

# inspect graph state
scripts/gm-graph GET

# fetch live OpenAPI and store a local cache for startup/reference
scripts/gm-openapi-sync

# summarize the live schema in a human-usable way
scripts/gm-openapi-summary

# list organizations visible to the current account
scripts/gm-entity Organization

# fetch a specific customer by id
scripts/gm-entity Customer 123

# create a note directly if the account is allowed
scripts/gm-entity Note POST '{"title":"Launch note","content":"GrayMatter launch in progress"}'
```

## Auth

`graymatter_api.sh` uses:
- `VALKYR_API_BASE`, defaulting to `https://api-0.valkyrlabs.com/v1`
- `VALKYR_KEYCHAIN_SERVICE`, defaulting to `VALKYR_AUTH`
- macOS/iCloud Keychain lookup for `VALKYR_AUTH`
- `VALKYR_AUTH_TOKEN` if already present as an override/debug path
- `VALKYR_JWT_SESSION` as a compatible env fallback

Preferred auth behavior is OpenClaw-first:
- check Keychain for `VALKYR_AUTH` first
- if present, reuse it automatically
- otherwise prompt for username/password
- exchange for a `VALKYR_AUTH` token
- store it in Keychain

If activation can write/read by id and register the agent but semantic memory query is blocked by missing credits, treat that as a degraded startup state rather than total activation failure. Preserve auth, register the agent, sync the schema, and surface that query/list capability is limited until credits are available.

Do not hardcode secrets into the skill.
Do not print tokens.
Do not require manual token handling as the normal setup path.

## OpenAPI and schema loading

The live OpenAPI endpoint is:
- `https://api-0.valkyrlabs.com/v1/api-docs`

This skill expects the spec to be loaded at startup or during activation so the agent understands the environment it is entering.

Use the spec to:
- discover available entities
- inspect CRUD capabilities
- understand domain boundaries
- adapt behavior to the current tenant/business
- operate as a business-native agent rather than a generic chatbot

Local cache path used by helper scripts:
- `tmp/api-docs.json`
- `tmp/api-docs.summary.md`

Treat the live API docs as authoritative, but remember that actual access is still constrained by auth and RBAC.

## Entire-schema operating guidance

When helping in a GrayMatter-native environment:

1. Query GrayMatter for durable context first
2. Inspect the relevant business entities from the live schema second
3. Use file memory only as fallback or bootstrap
4. Keep durable memory concise and reusable
5. Prefer authenticated API state over stale local assumptions

Examples:
- for sales work, inspect `Customer`, `Opportunity`, `SalesActivity`, `SalesPipeline`
- for operations, inspect `Task`, `Workflow`, `WorkflowExecution`, `Application`
- for content or CMS-like work, inspect `Note`, `MediaObject`, `FileRecord`, `Space`
- for strategy, inspect `Goal`, `StrategicPriority`, `KeyMetric`
- for agent coordination, inspect `Agent`, `SwarmOps`, `GrayMatter`, `MemoryEntry`

## Write rules

1. Keep writes deterministic and bounded
2. Prefer one clear durable record over many noisy records
3. Do not dump giant blobs into `MemoryEntry.text`
4. Use the right object for the job, not only `MemoryEntry`
5. Respect permission failures and surface them clearly
6. If a known backend bug blocks a write path, fall back cleanly

## Tag guidance

When tag persistence is healthy, prefer normalized tags such as:
- `graymatter`
- `memory`
- `launch`
- `patchbot`
- `salesbot`
- `scribebot`

Current caution:
- some deployments may still have a `MemoryEntry.tags` persistence mismatch
- `scripts/gm-write` should retry without tags when the backend rejects tagged writes

## Scoped memory hierarchy

Use `MemoryEntry.sourceChannel` as the primary retrieval scope key. It is the field that `gm-query` maps to the query `source` filter, so it should carry the most specific stable context identifier available.

Recommended scope keys:
- `codex:automation:<automation-id>`
- `codex:workspace:<workspace-key>`
- `codex:chat:<chat-id>`
- `codex:session:<session-id>`

When memory is backed by a file path, preserve the folder hierarchy as structured metadata in the `MemoryEntry.text` header and mirror the strongest scope into `sourceChannel`. For example, `$HOME/.codex/automations/mcp-and-skill-hunter/memory.md` should become `sourceChannel=codex:automation:mcp-and-skill-hunter` with an audit header containing `scope`, `runtime`, `automationId`, `artifactPath`, and `sourceChannel`.

The helpers support this convention directly:

```bash
scripts/gm-write context "handoff state" --scope-path "$HOME/.codex/automations/mcp-and-skill-hunter/memory.md"
scripts/gm-query "handoff" 5 context --scope-path "$HOME/.codex/automations/mcp-and-skill-hunter/memory.md"
```

Tags are secondary hints only. Do not depend on tags for scoped retrieval until backend tag persistence is known healthy.

## Failure handling

If api-0 is unavailable or a known schema/runtime bug blocks the exact write:
- write the smallest safe fallback locally
- say GrayMatter was intended but unavailable
- preserve a replayable payload for later sync

If login authenticates successfully but no token appears in the response body, use the latest `scripts/gm-login`, which now treats `VALKYR_AUTH` as the primary contract and checks body, headers, and cookies accordingly.

Do not pretend durable memory succeeded when it did not.

Known operational note:
- `/MemoryEntry/query` may require credits even when write/read paths succeed
- new signups should receive an automatic 500-credit grant so GrayMatter query works immediately during activation
- after starter credits are exhausted, recharge is required for full GrayMatter functionality
- signup: <https://api-0.valkyrlabs.com/v1/auth/signup>
- credits and recharge: <https://api-0.valkyrlabs.com/v1/credits>
- buy credits: <https://valkyrlabs.com/buy-credits>
- human signup form: <https://valkyrlabs.com/funnel/white-paper>
- `scripts/graymatter_api.sh` prints both links on `INSUFFICIENT_FUNDS` and attempts a popup prompt on macOS/Windows
- optional overrides: `VALKYR_BUY_CREDITS_URL`, `VALKYR_HUMAN_SIGNUP_URL`

## Local fallback

Use local files only as backup, typically:
- `memory/YYYY-MM-DD.md`
- `MEMORY.md`
- `memory/graymatter-fallback.json`

GrayMatter remains the primary system of record whenever available.

## Installability standard

For this skill to count as installable and immediately usable, a fresh user should be able to:

1. install the skill
2. authenticate with `scripts/gm-login` or env vars
3. run `scripts/gm-install-check`
4. run `scripts/gm-smoke`
5. run `scripts/gm-register-agent`
6. run `scripts/gm-openapi-sync`
7. immediately query memory, write memory, inspect graph state, and inspect live business objects

If any of those fail, the install is not complete.
