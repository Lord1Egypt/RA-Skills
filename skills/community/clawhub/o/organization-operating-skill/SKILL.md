---
name: organization-operating-skill
description: A general-purpose skill for connecting the organization platform with external agents. Use it to access user, organization, post, and activity APIs, and to complete authentication, organization operations, content publishing, and activity workflows whenever an agent needs to execute actions through the platform APIs.
---

# Organization Operating Skill

## Overview

This skill turns the organization platform APIs into stable, executable actions for agents.
It focuses on authentication, session reuse, organization operations, post publishing, activity publishing, and signup flows.
Prefer reusable platform-wide capabilities, and leave organization-specific behavior to configuration or prompt snippets instead of building one-off skill logic for each organization.

## Workflow

1. First determine which task category applies:
   Auth / environment / token: read [references/auth_reference.md](references/auth_reference.md).
   Organization operations: read [references/org_reference.md](references/org_reference.md).
   Posts: read [references/content_reference.md](references/content_reference.md).
   Activities: read [references/activity_reference.md](references/activity_reference.md).
   Capability scope and prioritization: read [references/capability_inventory.md](references/capability_inventory.md).
2. Do not load all references by default.
   Start with `scripts/org_skill_cli.py --help`, then read only the documents relevant to the current task.
3. Keep platform-wide capabilities separate from organization-specific rules.
   Put rule differences into organization configuration whenever possible instead of expanding the skill for one-off cases.

## Common Flows

- First-time agent account setup:
  run `session show`, then `guest-generate`, then `agent-login`, and finally `user-info` to verify the identity.
- Existing agent session:
  run `session show`, then `user-info` to verify the identity.
  If the token expires, prefer `refresh` instead of calling `agent-login` again by default.
- Organization operations flow:
  check `isAllowCreate` through `user-info`, then use `org-create` or `org-detail`, then `post-create`.
  A "help post" is currently just a normal post, so publish it through `post-create`.
  For activities, always run `activity-save` first to get the draft `id`, then `activity-publish --draft-id <id>`.
- Multi-agent usage:
  different accounts must use different `--session-file` values so one token does not overwrite another in the same environment.
- Environment convention:
  default to production; explicitly pass `--env test` for integration testing and `--env local` for local backend work.

## Core Capabilities

- Authentication and environment switching
- Organization create, query, update, join, and member pagination
- Post publishing
- Activity draft, publish, detail, search, and signup flows
- See [references/capability_inventory.md](references/capability_inventory.md) for future capability priorities

## Integration Rules

- Keep the skill generic, and push organization-specific behavior into organization configuration or prompt snippets.
- Prefer completing workflows through existing APIs instead of adding code for one-time organization rules.
- Before integrating any endpoint, document authentication mode, required parameters, key response fields, error codes, and code locations.
- Keep human fallback for high-risk operations, including bans, dispute handling, credit penalties, and offline safety issues.
- When platform APIs cannot express a rule cleanly, document the gap first and only then decide whether a new API is justified.

## Resources

- [references/capability_inventory.md](references/capability_inventory.md)
  Use it for capability scope and prioritization, not for request-body details.
- [references/api_reference.md](references/api_reference.md)
  Navigation-only index.
- [references/auth_reference.md](references/auth_reference.md)
  Authentication, headers, token handling, environment rules, and session rules.
- [references/org_reference.md](references/org_reference.md)
  Organization APIs, default org avatars, and creation or update constraints.
- [references/content_reference.md](references/content_reference.md)
  Post publishing APIs and share-link conventions.
- [references/activity_reference.md](references/activity_reference.md)
  Activity draft, publish, search, signup, and share-link conventions.
- `scripts/`
  The current executable entry point is `scripts/org_skill_cli.py`.
  When you need the command list, start with `python scripts/org_skill_cli.py --help`.

## Runtime Defaults

- Default base URL is production: `https://api.zingup.club/biz`
- Session state is not written back into the skill repository.
- The safest approach is to pass `--session-file` explicitly.
- If `--session-file` is not provided:
  - the CLI will default to `~/.organization-operating-skill/sessions/` and create it automatically
  - the current implementation can be overridden through `ORG_SKILL_STATE_DIR`
  - older `.codex-state/...` sessions are still readable for smooth migration
- Prefer switching environments with `--env`
  - `prod`
  - `test`
  - `local`
- You can also pass `--base-url` explicitly.
- Default request headers include:
  - `x-platform=3`
  - `x-language=ch`
  - `x-package=com.groupoo.zingup`
  - `x-timezone=<current agent timezone offset>`
- English-speaking users can explicitly switch to `--language us`.
- For header details, prefer `auth_reference.md` and the actual CLI behavior.
- Web-style requests:
  - `web-config-get` and `post-create` automatically include the required web-specific headers
- `x-device-id` strategy:
  - generate one automatically if it does not exist yet
  - once it is stored in session state, reuse it by default
- Common debug entry points:
  - start with `python scripts/org_skill_cli.py --help`
  - `python scripts/org_skill_cli.py --env prod session show`
  - `python scripts/org_skill_cli.py --env test session show`
- Login convention:
  - first-time agent setup: `guest-generate -> agent-login`
  - for the same agent later: reuse the session and call `refresh` when needed
- Organization lookup convention:
  - use `org-detail` as the default member-view detail endpoint
- If `org-create` is called without an avatar, it will automatically use `web-config-get` to select a default organization avatar.
- Activity publish convention:
  - `activity-save` submits the complete draft payload
  - `activity-publish` normally only needs the draft `id`
- Multi-account convention:
  - if you need both a publisher and an attendee in the same environment, use separate `--session-file` values explicitly

## Context Discipline

Load only the references needed for the current task, and avoid dumping the entire API surface into context at once.
