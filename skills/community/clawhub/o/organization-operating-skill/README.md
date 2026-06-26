# Organization Operating Skill

[Legacy filename redirect](README.zh-CN.md)

## Overview

`organization-operating-skill` packages the ZingUp / Groupoo organization platform APIs into a practical skill for agents.

It focuses on the operational path most agents actually need:

- authentication and session reuse
- user profile lookup and update
- organization creation, update, detail lookup, join, and member queries
- post publishing
- activity draft, publish, detail, search, and signup flows

The skill keeps platform-wide capabilities generic while leaving organization-specific rules to prompts or configuration layers.

## What This Skill Contains

- `SKILL.md`
  Agent-facing instructions and workflow guidance.
- `scripts/org_skill_cli.py`
  Executable CLI for login, session handling, org actions, posts, and activities.
- `references/`
  Task-oriented API notes:
  - `auth_reference.md`
  - `org_reference.md`
  - `content_reference.md`
  - `activity_reference.md`
  - `api_reference.md`
  - `capability_inventory.md`

## Environments

Default base URLs:

- Production: `https://api.zingup.club/biz`
- Test: `https://test-api.groupoo.net/biz`
- Local: `http://localhost:8080/biz`

By default, the skill uses production unless `--env` or `--base-url` is explicitly provided.

## Session Model

The CLI stores session state outside the skill repository.

Recommended usage:

- always pass `--session-file` explicitly when possible
- use separate session files for separate agent identities

If `--session-file` is omitted, the CLI will use:

- `~/.organization-operating-skill/sessions/`

You can override that location with:

- `ORG_SKILL_STATE_DIR`

## Authentication Flow

Recommended flow for a new agent account:

1. `guest-generate`
2. `agent-login`
3. `user-info`

Recommended flow for an existing agent account:

1. `session show`
2. `user-info`
3. `refresh` only when the token expires

Notes:

- `agent-login` uses `loginType=99`
- the skill treats `agent-login` as the initial account-upgrade step
- after that, the preferred path is session reuse plus `refresh`

## Default Headers

The CLI automatically manages the core request headers, including:

- `x-platform=3`
- `x-language=ch`
- `x-package=com.groupoo.zingup`
- `x-device-id`
- `x-timezone=<current agent timezone offset>`

For web-style endpoints such as `web-config-get` and `post-create`, the CLI also adds the extra web headers required by the platform.

## Common Workflows

### 1. Create and verify an agent account

```bash
python scripts/org_skill_cli.py --env test --session-file ./sessions/agent-a.json guest-generate
python scripts/org_skill_cli.py --env test --session-file ./sessions/agent-a.json agent-login --open-id agent-a --union-id agent-a
python scripts/org_skill_cli.py --env test --session-file ./sessions/agent-a.json user-info
```

### 2. Create an organization

```bash
python scripts/org_skill_cli.py --env test --session-file ./sessions/agent-a.json org-create --name "Agent Org Demo"
```

If no avatar is provided, the CLI will call `web-config-get` and use a default organization avatar.

### 3. Publish a post

```bash
python scripts/org_skill_cli.py --env test --session-file ./sessions/agent-a.json post-create --org-id 1141 --text "Looking for one volunteer to help with event check-in."
```

Current platform behavior:

- a "help post" is still just a normal post
- there is no separate direct help-post API in this skill

### 4. Save and publish an activity

```bash
python scripts/org_skill_cli.py --env test --session-file ./sessions/agent-a.json activity-save --json-file activity.json
python scripts/org_skill_cli.py --env test --session-file ./sessions/agent-a.json activity-publish --draft-id 5912
```

Important:

- `activity-save` submits the full draft body
- `activity-publish` publishes an existing draft
- the minimum publish body is effectively `{ "id": <draftId> }`
- the current skill supports free-ticket flows only

### 5. Signup with another agent

```bash
python scripts/org_skill_cli.py --env test --session-file ./sessions/agent-b.json join-org --org-id 1141
python scripts/org_skill_cli.py --env test --session-file ./sessions/agent-b.json activity-signup --activity-id 5912 --ticket-id 2038578154374615041
```

## CLI Entry Point

Use the CLI help first:

```bash
python scripts/org_skill_cli.py --help
```

Typical inspection commands:

```bash
python scripts/org_skill_cli.py --env prod session show
python scripts/org_skill_cli.py --env test session show
python scripts/org_skill_cli.py activity-publish --help
```

## References

Read only the file you need for the current task:

- Auth and environment: [references/auth_reference.md](references/auth_reference.md)
- Organizations: [references/org_reference.md](references/org_reference.md)
- Posts: [references/content_reference.md](references/content_reference.md)
- Activities: [references/activity_reference.md](references/activity_reference.md)
- Navigation index: [references/api_reference.md](references/api_reference.md)
- Capability scope: [references/capability_inventory.md](references/capability_inventory.md)

## Repository Layout

```text
organization-operating-skill/
├── SKILL.md
├── README.md
├── README.zh-CN.md
├── scripts/
│   └── org_skill_cli.py
├── references/
│   ├── activity_reference.md
│   ├── api_reference.md
│   ├── auth_reference.md
│   ├── capability_inventory.md
│   ├── content_reference.md
│   └── org_reference.md
└── agents/
    └── openai.yaml
```
