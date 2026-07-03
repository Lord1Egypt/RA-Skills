# Open Plantbook publish notes

Use these notes when reviewing or publishing the `openplantbook` skill to ClawHub/OpenClaw Hub.

## Listing copy

- Display name: `Open Plantbook`
- Slug: `openplantbook`
- Owner: `@slaxor505`
- Author: `Slava Pisarevskiy`
- Version: `1.0.0`
- Short description: `Schema-first Open Plantbook API workflows`
- Homepage: `https://open.plantbook.io/docs/`
- Suggested tags: `plants`, `openplantbook`, `api`, `home-assistant`, `care-data`

Suggested long description:

```text
Open Plantbook gives agents a schema-first workflow for the Open Plantbook API. It can search plants, retrieve detail and care fields, and create authenticated user plants from schema-aligned dossier JSON without relying on an SDK or scraped HTML. The skill fetches the live OpenAPI schema before operations where endpoint shape or payload validation matters, keeps secrets out of output, and treats write/delete actions as external changes that need explicit user intent.
```

Suggested first changelog:

```text
Initial ClawHub release: schema-first API guidance, direct-HTTP Python helper for search/detail/create, credential-source handling, and publishing notes.
```

## Package contents

Include:

- `SKILL.md`
- `agents/openai.yaml`
- `scripts/openplantbook_cli.py`
- `references/publish-notes.md`
- `skill-card.md`

Exclude:

- `README.md`
- `requirements.txt`
- `scripts/__pycache__/`
- `*.pyc`
- `.env`, `*.env`, credentials, logs, or local test dossiers

The helper is intentionally direct-HTTP only and has no SDK dependency.

## Feature surface

Headline workflows:

- Search Open Plantbook plants by scientific/common name or alias.
- Retrieve plant details and care fields through `include=care`.
- Create user plants from Open Plantbook-schema-aligned dossier JSON.

Advanced guidance only:

- Update/delete user plants through schema-backed direct HTTP.
- Sensor upload integration.

Do not present sensor upload as a primary user feature unless Open Plantbook exposes a sensor history/status read API.

## Credential model

Public listing should say:

- The setup credential field should be labeled `Open Plantbook credential`, not `API key`.
- A plain credential value is treated as `OPENPLANTBOOK_API_KEY` for read/search/detail workflows.
- OAuth write workflows need client credentials, preferably as JSON: `{"client_id":"...","client_secret":"..."}`.
- The helper keeps its existing env vars: `OPENPLANTBOOK_API_KEY`, `OPENPLANTBOOK_OAUTH_CREDENTIALS`, or split `OPENPLANTBOOK_CLIENT_ID` plus `OPENPLANTBOOK_CLIENT_SECRET`.
- `OPENPLANTBOOK_OAUTH_CREDENTIALS` may also accept `client_id:client_secret` as a shorthand fallback, but JSON is the documented canonical form.
- The helper can also read the private local env file documented in `SKILL.md`.

Never publish credentials, local env files, generated logs, or session transcripts with the skill.

## Security review gate before publish

Every publish or republish to ClawHub/OpenClaw Hub must pass a security review before the publish command is run.

Review checklist:

- The canonical skill uses only the portable credential contract: `OPENPLANTBOOK_API_KEY`, `OPENPLANTBOOK_OAUTH_CREDENTIALS`, `OPENPLANTBOOK_CLIENT_ID`, `OPENPLANTBOOK_CLIENT_SECRET`, and optional explicit `OPENPLANTBOOK_ENV_FILE`.
- OpenClaw-specific secret paths, config paths, and local filesystem details appear only in adapter documentation such as `OPENCLAW.md`, never in the packaged canonical skill.
- No real credentials, tokens, OAuth client secrets, private env files, logs, transcripts, generated caches, local dossiers, or private test data are included.
- Credential examples use placeholders only, such as `{"client_id":"...","client_secret":"..."}`.
- The packaged helper sends credentialed requests only to `https://open.plantbook.io` and does not support an environment-selected API base URL.
- Write/delete behavior still requires explicit user intent and reports API errors without leaking credential values.
- Package contents match the expected file list below.

Run these scans from the repository root and review any output before publishing:

```bash
PLATFORM_PATTERN='OPENCLAW|openclaw|[.]config|/home/|/Users/|apiKey|(^|[[:space:]/])[.]env($|[[:space:]/])|[*][.]env'
CREDENTIAL_PATTERN='client_secret|OPENPLANTBOOK_API_KEY|OPENPLANTBOOK_OAUTH_CREDENTIALS|token'
rg -n "$PLATFORM_PATTERN" plugins/openplantbook/skills/openplantbook skills/openplantbook -g '!**/references/publish-notes.md'
rg -n "$CREDENTIAL_PATTERN" plugins/openplantbook/skills/openplantbook skills/openplantbook
find plugins/openplantbook/skills/openplantbook -name '__pycache__' -o -name '*.pyc' -o -name '.env' -o -name '*.env'
```

The `find` command should produce no output. The `rg` commands may show documented metadata, placeholders, and env-var names; investigate anything that looks like a local filesystem path, platform-specific config path, or literal secret value.

## Validation before publish

Run from this repository root:

```bash
python3 -m py_compile plugins/openplantbook/skills/openplantbook/scripts/openplantbook_cli.py
python3 plugins/openplantbook/skills/openplantbook/scripts/openplantbook_cli.py --help
find plugins/openplantbook/skills/openplantbook -type f | sort
```

Expected file list:

```text
plugins/openplantbook/skills/openplantbook/SKILL.md
plugins/openplantbook/skills/openplantbook/agents/openai.yaml
plugins/openplantbook/skills/openplantbook/references/publish-notes.md
plugins/openplantbook/skills/openplantbook/scripts/openplantbook_cli.py
plugins/openplantbook/skills/openplantbook/skill-card.md
```

If the generic AgentSkills validator rejects `homepage` or `user-invocable`, prefer OpenClaw's skill commands for this package. Those frontmatter keys are documented OpenClaw fields for hub/UI presentation.

## Publish command template

Install/login to the standalone ClawHub CLI before publishing:

```bash
clawhub login
clawhub whoami
```

Then publish from the workspace:

```bash
clawhub skill publish ./plugins/openplantbook/skills/openplantbook --version 1.0.0
```

Select owner `@slaxor505` if the CLI prompts for an owner. ClawHub publishes under:

```text
https://clawhub.ai/slaxor505/openplantbook
```

The package stays hidden from normal install/download surfaces until ClawHub review and security checks finish.
