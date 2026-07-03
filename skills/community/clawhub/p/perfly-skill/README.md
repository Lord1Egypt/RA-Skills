# Perfly Agent Sync Skill

This package contains the English canonical skill instructions for Perfly Agent Sync.

Use this package for skill hubs or registries. It is intentionally separate from MCP metadata because skill distribution platforms and MCP registries usually require different packaging formats.

## Entry Point

- `SKILL.md`

## Setup

Configure the hosted Perfly MCP endpoint in the user's MCP client:

```text
https://api.perfly.dev/mcp
```

OAuth discovery is the recommended setup. Manual bearer tokens are fallback-only for headless, SSH, devcontainer, CI, or remote sandbox workflows that cannot complete browser OAuth.

## Required MCP Tools

- `perfly_preview_work_items`
- `perfly_add_work_items`
- `perfly_check_connection`
- `perfly_get_ingestion_policy`

## Privacy Boundary

The skill instructs agents to submit concise work summary metadata only. It explicitly blocks source code, diffs, logs, secrets, customer data, document bodies, issue bodies, pull request bodies, attachments, and full terminal output.

## ClawHub

Published package:

```text
https://clawhub.ai/levi840714/skills/perfly-skill
```

Version source:

```text
skill/manifest.json
```

Preview updates from the Perfly monorepo with:

```bash
make publish-clawhub-skill
make release-clawhub-skill-dry-run
```

Release flow:

```bash
# 1. Bump skill/manifest.json version.
# 2. Commit the monorepo changes.
# 3. Publish perfly-agent/ and tag the public repo.
make release-clawhub-skill
```

The release script pushes `perfly-agent/` to `perfly-dev/perfly-agent`, then creates `perfly-skill-v<version>` on that public repo. The ClawHub GitHub Action publishes only from those public repo tags and fails if the tag version does not match `skill/manifest.json`.
