---
name: install-global-skill-from-clawhub
description: Install or upgrade a ClawHub skill, then make the global copy under the machine's OpenClaw home `skills/` directory the final source of truth. Use when the user wants a skill installed from ClawHub, updated to the latest version, switched to the global skill directory, or kept in sync globally across agents.
---

# Install Global Skill From ClawHub

Install or update one ClawHub skill with the official CLI, then promote the staged copy into the global skill directory.

## Rules

- Treat `<openclaw-home>/skills/<slug>` as the final destination.
- Treat `<openclaw-home>/workspaces/<agent>/skills/<slug>` as a temporary staging location used by the CLI.
- Resolve `<openclaw-home>` from `--openclaw-home`, then `OPENCLAW_HOME`, else `$HOME/.openclaw`.
- Resolve `<agent>` from `--agent`, then `OPENCLAW_AGENT`, else `lan`.
- Derive the workspace as `<openclaw-home>/workspaces/<agent>`.
- Prefer `scripts/install-global-skill.js` over manual file operations.
- Try `openclaw skills update` first; if the skill is not tracked, use `openclaw skills install --force`.
- Backup an existing global skill before replacement unless the user explicitly says otherwise.
- Promote through a temporary directory, then rename into place.
- Remove the staged copy after promotion unless the user wants to keep it.
- For destructive actions such as deleting an existing global skill or staging copy, ask for confirmation unless the user already asked for replacement or upgrade.
- Do not modify or create Agents. This skill only manages skill files.
- Keep the workflow focused on one slug at a time unless the user explicitly asks for a batch.

## Workflow

1. Confirm the target skill slug.
2. Prefer running `node scripts/install-global-skill.js --slug <slug>`.
3. Verify the staged origin file at `<openclaw-home>/workspaces/<agent>/skills/<slug>/.clawhub/origin.json`.
4. Backup the current global directory when it exists.
5. Promote the staged copy into `<openclaw-home>/skills/<slug>`.
6. Verify the global origin file and installed version after promotion.
7. Report the result.

## Verification

- `<openclaw-home>/skills/<slug>/SKILL.md` exists
- `<openclaw-home>/skills/<slug>/.clawhub/origin.json` exists
- `installedVersion` in the global copy matches the staged copy

## Delivery

- target slug
- final global path
- installed version
- whether update or install was used
- backup path if one was created
- whether the staging copy was removed
- any blocker, such as CLI failure or missing ClawHub package
