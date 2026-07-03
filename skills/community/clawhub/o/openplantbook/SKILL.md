---
name: "openplantbook"
description: "Open Plantbook API workflows with schema-first plant search, detail, and user-plant writes."
homepage: https://open.plantbook.io/docs/
user-invocable: true
license: MIT
metadata:
  author: Slava Pisarevskiy
  version: "1.0.0"
  openclaw: {"emoji":"🌿","homepage":"https://open.plantbook.io/docs/","requires":{"anyBins":["python3","python"]},"primaryEnv":"OPENPLANTBOOK_API_KEY"}
---

# Open Plantbook

Use this skill when the user asks about Open Plantbook, plant-care thresholds, plant lookup by scientific/common name, plant details, multilingual aliases, creating/updating/deleting Open Plantbook user plants, or authenticated Open Plantbook plant workflows.

Open Plantbook is a community-sourced plant-care database. Its API supports API-key token authentication and OAuth2 client credentials. This skill uses direct HTTP against the live API schema; it does not require or depend on an SDK.

The packaged helper sends authenticated requests only to the official Open Plantbook API host, `https://open.plantbook.io`. Do not configure alternate API hosts for real user credentials. If you need to test a fork, mock, or staging API, use separate throwaway credentials outside this published helper.

## Schema-first rule

Before any Open Plantbook API operation where endpoint shape, payload fields, limits, or response shape matter, consult the live OpenAPI schema:

```bash
curl -sS -H 'Accept: application/json' -A 'openplantbook-agent-skill/1.0 (+https://open.plantbook.io/docs/)' https://open.plantbook.io/api/schema/
```

Canonical schema endpoint:

- `https://open.plantbook.io/api/schema/`

Do not use `/api/v1/schema/`; it returns 404. The schema verified during this update advertises OpenAPI `3.0.3` and API version `202606`.

Use the schema as the source of truth for paths, methods, security, parameters, request bodies, required fields, max lengths, numeric bounds, nullable flags, response schemas, and error shapes.

For simple repeated read-only helper calls, cached knowledge is fine after checking it against the live schema during the current task. For writes, stop and report the schema/configuration problem if the schema cannot be fetched unless the user explicitly tells you to proceed from known docs.

## API-only rule

For Open Plantbook plant data and plant operations, use only API-backed paths:

- `scripts/openplantbook_cli.py search ...`
- `scripts/openplantbook_cli.py detail ...`
- `scripts/openplantbook_cli.py create --from-dossier ...`
- direct HTTP calls matching the live OpenAPI schema

Do not use public Browse DB pages, web fetch, browser automation, HTML scraping, or search-engine snippets as a fallback for Open Plantbook plant data. If the helper cannot authenticate or an API call fails, stop and report the API/configuration error.

Do not recover credentials from backups, session transcripts, shell history, logs, browser storage, or other stale/private artifacts. Read credentials only from supported live sources.

Do not add or rely on an environment-selected API base URL. The helper uses the official Open Plantbook API host so Open Plantbook API keys and OAuth client secrets are not sent to a caller-selected host.

## Credentials

Read-only helper authentication can use either:

- `OPENPLANTBOOK_API_KEY` for token auth
- `OPENPLANTBOOK_CLIENT_ID` and `OPENPLANTBOOK_CLIENT_SECRET` for OAuth bearer auth
- `OPENPLANTBOOK_OAUTH_CREDENTIALS` for bundled OAuth credentials

Use OAuth bearer auth for write operations unless the live schema later says token auth supports them.

Do not treat `OPENPLANTBOOK_CLIENT_ID` as a standalone API key. Do not print secrets, echo secrets, write secrets into files, or include secrets in user-visible output.

If a UI or hub card exposes one secret field, label it as `Open Plantbook credential`, not `API key`. Accept these user-facing forms:

- Plain API key: use as `OPENPLANTBOOK_API_KEY`. This supports read/search/detail workflows only unless the live schema later permits token-auth writes.
- JSON OAuth bundle: `{"client_id":"...","client_secret":"..."}`. Prefer this form for OAuth because it is self-describing and does not need escaping.
- OAuth shorthand: `client_id:client_secret`. Support this only as a convenience fallback; parse on the first colon and prefer JSON in docs/examples.

Keep environment variable names stable. Store OAuth bundles in `OPENPLANTBOOK_OAUTH_CREDENTIALS`, or store split OAuth values in `OPENPLANTBOOK_CLIENT_ID` and `OPENPLANTBOOK_CLIENT_SECRET`.

Supported helper credential sources, in order:

1. Process environment variables.
2. Explicit private env file via `OPENPLANTBOOK_ENV_FILE=/path/to/openplantbook.env`.

Agent-specific adapters may map their own secret stores to these environment variables. Keep platform-specific secret paths and config formats in adapter documentation, not in this canonical skill.

The private env file should contain plain `KEY=value` lines. The helper parses this file directly and does not execute it as shell code. Example OAuth bundle:

```text
OPENPLANTBOOK_OAUTH_CREDENTIALS={"client_id":"...","client_secret":"..."}
```

## Plant operations

The live schema verified for API version `202606` lists these plant operations:

- `GET /api/v1/plant/search`
- `GET /api/v1/plant/detail/{pid}/`
- `POST /api/v1/plant/create`
- `PATCH /api/v1/plant/update`
- `DELETE /api/v1/plant/delete`

Always re-check `/api/schema/` before using these for writes or when field details matter.

### Search plants

Use `GET /api/v1/plant/search` when the user asks to find plants by scientific name, alias, or common name.

Security in schema: OAuth `read`, cookie auth, or token auth.

Query parameters:

- `alias`: search text, minimum 3 characters unless `userplant=true` is used to list user plants.
- `userplant`: optional scope selector. `true` searches user plants only, `false` searches public plants only, omitted searches both with de-duplication where user plants supersede public matches.
- `limit`, `offset`: pagination.

Preferred helper path:

```bash
python3 {baseDir}/scripts/openplantbook_cli.py search "abelia"
```

If constructing HTTP directly, encode UTF-8 safely and preserve pagination fields. The result may match common names without telling you which field matched, so mention potential ambiguity when names look surprising.

### Retrieve plant details

Use `GET /api/v1/plant/detail/{pid}/` when the user asks for details, thresholds, care fields, common names, or a specific PID.

Security in schema: OAuth `read`, cookie auth, or token auth.

Parameters:

- `pid` path parameter, required.
- `lang` query parameter: optional 2-letter ISO 639-1 code or regional tag such as `en-GB` / `pt_BR`.
- `include` query parameter: optional extra categories such as `care`, `care,poison`, or `*` when supported by the schema.

Preferred helper path:

```bash
python3 {baseDir}/scripts/openplantbook_cli.py detail "abelia chinensis" --lang en --include care
```

If the caller has a user plant with the PID, the customized user plant is returned with `user_plant: true`; otherwise the public plant is returned.

### Create user plant

Use `POST /api/v1/plant/create` only when the user explicitly asks to create a new Open Plantbook user plant or push a plant dossier into Open Plantbook.

Security in schema: OAuth `read write`, or cookie auth. Do not use token auth for create unless the schema later says it supports it.

Request schema:

- Resolve `#/components/schemas/PlantCreateRequest` from `/api/schema/`.
- `display_pid` is required.
- `pid`, `user`, and `common_names` are server-managed or unsupported for create and should not be supplied.
- A plant that already exists in public DB or the caller profile returns conflict; update it instead.

Observed schema limits for API `202606`:

- `display_pid`: string max 100, required.
- `alias`: string max 100, nullable.
- `category`: string max 100, nullable.
- `sunlight`: string max 200, nullable.
- `watering`: string max 200, nullable.
- `fertilization`: string max 250, nullable.
- `pruning`: string max 200, nullable.
- `soil`: string max 150, nullable.
- `origin`: string max 100, nullable.
- Threshold fields such as `min_temp`, `max_temp`, `min_light_lux`, `max_light_lux`, `min_env_humid`, `max_env_humid`, `min_soil_moist`, `max_soil_moist`, `min_soil_ec`, `max_soil_ec`, `min_light_mmol`, and `max_light_mmol`: nullable int64 with schema numeric bounds.

Use direct HTTP with a stable API client user agent:

```text
openplantbook-agent-skill/1.0 (+https://open.plantbook.io/docs/)
```

A live urllib request without an explicit user agent was blocked by Cloudflare with Error 1010.

For dossier-based creation, prefer the helper:

```bash
python3 {baseDir}/scripts/openplantbook_cli.py create --from-dossier plant_dossiers/chlorophytum_orchidastrum.json
```

The dossier JSON must already use `PlantCreateRequest` field names. The helper does not rename legacy dossier fields such as `min_temp_c` or `min_soil_ec_uScm`; fields that are not in the live create schema are ignored and reported. It validates types and numeric bounds, requires `display_pid`, and truncates overlong string fields to schema `maxLength` for the outgoing payload unless `--no-truncate` is supplied.

Do not map PPFD fields into `min_light_mmol` / `max_light_mmol` unless the dossier explicitly stores Open Plantbook-compatible mmol values. PPFD in umol/m2/s is not the same field.

Before creating, summarize the chosen source dossier and generated payload keys. If the user has already explicitly asked to create the plant, proceed; otherwise ask for confirmation because this is a write action to an external service.

Report results without secrets:

- `201`: created successfully; include returned `pid`/identifier if present.
- `409`: plant already exists in user or main DB; report duplicate rather than retrying; use update if the user wants changes.
- `400`: validation error; summarize API error details and payload keys, not credentials. If schema max lengths explain the failure, shorten or omit offending text fields once and retry if the user already asked to create.
- `429`: report throttling and server-provided wait time; do not retry until that time has passed.
- Auth errors: report credential configuration/authentication failure without printing secret values.

### Update plant

Use `PATCH /api/v1/plant/update` when the user asks to modify an existing user plant or customize a public plant into the caller profile.

Security in schema: OAuth `read write`, or cookie auth.

Request schema:

- Resolve `#/components/schemas/PatchedPlantUpdateRequest` from `/api/schema/`.
- `pid` is required by endpoint behavior even if the patch schema itself marks all fields optional.
- At least one plant attribute besides `pid` must be supplied.
- Only `PATCH` is supported. `PUT` is not supported and can return 405.

Behavior:

- If `pid` refers to a user plant, that user plant is updated.
- If `pid` refers to a public plant, Open Plantbook clones it into the caller profile and applies the requested changes to that copy.
- Public plants are not modified in place.

Use schema max lengths and nullable flags exactly as for create. Shorten long care text before sending, or omit optional fields that cannot be safely shortened.

Confirm before updating unless the user explicitly gave the target PID and fields or explicitly asked to update from a named dossier/file.

Report results without secrets:

- `200`: update successful; include returned `pid`, `display_pid`, and `user_plant` if present.
- `400`: validation error; summarize field-level errors.
- `404`: PID exists neither in user nor public plants.
- `405`: method unsupported, usually from using PUT instead of PATCH.
- `429`: throttled; report wait time and stop.
- `500`: report server error and avoid blind retries.

### Delete user plant

Use `DELETE /api/v1/plant/delete` only when the user explicitly asks to delete a user plant.

Security in schema: OAuth `read write`, or cookie auth.

Request schema:

- Resolve `#/components/schemas/PlantDeleteRequest` from `/api/schema/`.
- Required field: `pid`.
- `pid` is case-sensitive.

Behavior:

- Deletes a plant from the caller profile only.
- Public plants cannot be removed.
- Known schema/docs issue: omitted `pid` may return `404` rather than `400` because the missing value is used as the lookup key.

Always confirm destructive deletes unless the user's message already includes an explicit delete instruction and an exact PID. For ambiguous names, search/detail first and ask for the exact PID.

Report results without secrets:

- `204`: deleted successfully.
- `404`: user plant not found, public plant cannot be deleted, or `pid` omitted.
- `429`: throttled; report wait time and stop.

## Advanced sensor-upload integration

Sensor upload is an advanced developer integration topic, not a headline skill workflow. Do not present sensor upload as a general agent feature, and do not infer plant-health/status answers from uploaded sensor history unless Open Plantbook exposes a read/status API for that data.

When explicitly asked to help build or debug an Open Plantbook sensor uploader:

- Fetch `/api/schema/` before building payloads.
- Use OAuth `read write`; do not use token auth unless the schema later permits it.
- Register the plant instance first with `POST /api/v1/sensor-data/instance`, binding `pid` plus a device/app `custom_id`.
- Use the returned plant-instance UUID in JTS upload columns; sensor upload binds to the instance UUID, not directly to the plant PID.
- Upload JSON Time Series data to `POST /api/v1/sensor-data/upload`; use `dry_run=true` while testing integrations.

## Publishing and maintenance

When preparing this skill for ClawHub/OpenClaw Hub publication, read `{baseDir}/references/publish-notes.md` for the package checklist, suggested listing copy, validation commands, and release command template.
- Validate supported measurement names and units before upload: `temp` in deg C, `soil_ec` in uS/cm, `env_humid` in %, `soil_moist` in %, and `light_lux` in lux.
- Preserve ISO 8601 timestamps with timezone offsets.
- Avoid uploading bogus values. Preserve privacy: include location only when the user explicitly opted in.

## Safety and privacy

- Treat plant database output as informational plant-care guidance, not medical, veterinary, food-safety, or toxicity advice.
- Do not identify plants from images with Open Plantbook unless paired with a plant-identification tool.
- For pet/child safety, verify toxicity with an authoritative source before making strong claims.
- Never expose Open Plantbook credentials.
- Respect rate limits; back off on HTTP 429 and use `Retry-After` or the API error wait time when present.

## Helper CLI

This skill folder includes `scripts/openplantbook_cli.py` for quick CLI workflows:

```bash
python3 skills/openplantbook/scripts/openplantbook_cli.py search "abelia"
python3 skills/openplantbook/scripts/openplantbook_cli.py detail "abelia chinensis" --lang en --include care
python3 skills/openplantbook/scripts/openplantbook_cli.py create --from-dossier plant_dossiers/chlorophytum_orchidastrum.json --dry-run
```

The helper is direct-HTTP only. It does not depend on `openplantbook-sdk`. It supports read-only `search`/`detail` plus OAuth-backed `create --from-dossier`; use schema-backed direct HTTP for update/delete and advanced integration tasks.

Do not use public Open Plantbook HTML pages, web fetch, or browser automation as fallback for helper failures.

## Output style

Give concise, practical plant-care answers. Include raw JSON only when the user asks for API/debug output. When multiple matches are returned, ask the user to choose only if there is real ambiguity; otherwise pick the best API match and mention that it was the best API match.
