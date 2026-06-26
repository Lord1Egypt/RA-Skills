---
name: podcast-feed-manager
description: Manage personal podcast feeds through the fixed user-scoped huisheng.fm API from an installed skill package. Use when an AI agent should manage a user's huisheng.fm Podcast Feeds via HUISHENG_API_TOKEN in a sandbox or skill-registry environment, without configuring an MCP client.
---

# Podcast Feed Manager Skill

Use this skill to manage huisheng.fm Podcast Feeds from an agent sandbox. The skill calls the user-scoped REST API directly instead of calling the MCP endpoint.

## Entrypoint

Resolve the executable relative to the installed skill root:

```bash
./scripts/run_huisheng.sh --help
```

`./scripts/run_huisheng.sh` is the only executable script in this skill package. It is self-contained and calls the fixed REST API directly with `curl`. Do not hardcode `/mnt/skills/<id>` or `~/.codex/...` paths.

Before making API changes, run:

```bash
./scripts/run_huisheng.sh doctor
```

Use `doctor` before diagnosing API failures. `hasCurl: false` means the sandbox cannot run HTTP requests; `hasToken: false` means `HUISHENG_API_TOKEN` is not available in the command environment.

When the agent runtime executes commands in a separate sandbox working directory, copy `scripts/run_huisheng.sh` into that sandbox and run it from the copied location. This script has no sibling file dependencies.

## Authentication

The sandbox must provide this environment variable:

```text
HUISHENG_API_TOKEN
```

Every API request sends:

```text
Authorization: Bearer <HUISHENG_API_TOKEN>
```

Never print the full token in user-facing output.

## Fixed API

The API URL is fixed and does not need user configuration:

```text
https://huisheng.fm/api
```

## Common Commands

List feeds:

```bash
./scripts/run_huisheng.sh list-feeds
```

Create a feed:

```bash
./scripts/run_huisheng.sh create-feed --json '{"title":"Daily Brief","siteUrl":"https://example.com"}'
```

List episodes:

```bash
./scripts/run_huisheng.sh list-episodes <feed-key>
```

Create an episode:

```bash
./scripts/run_huisheng.sh create-episode <feed-key> --json-file ./episode-payload.json
```

## Operating Rules

- Require `HUISHENG_API_TOKEN`; do not invent fallback token names.
- Do not ask the user for an API URL; use `https://huisheng.fm/api`.
- Treat all operations as user-scoped. A token can only access Podcast Feeds owned by the authenticated dashboard user.
- Keep JSON arguments as structured JSON. Use `--json-file` for long episode payloads.
- If a feed is not found, list feeds first instead of assuming the feed is global.

## Reference

Read `references/api.md` only when you need the endpoint list.
