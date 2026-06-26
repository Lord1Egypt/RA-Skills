# Nudgen Agent Skills

Installable `SKILL.md` packages for working with Nudgen API workflows, the `nudgen` CLI, and email-sending best practices.

These skills are designed for agent environments that support installable skills, including Codex, Claude Code, and Cursor via the `skills` CLI.

## Install

For `skills` CLI setup and full flag documentation, use:

- https://skills.sh/docs/cli

Install from this package root:

```bash
# See available skills in this package
npx skills add https://github.com/Nudgen-Marketing/skills --list

# Install all Nudgen skills globally
npx skills add https://github.com/Nudgen-Marketing/skills --global

# Install specific skills globally
npx skills add https://github.com/Nudgen-Marketing/skills --global --skill api
npx skills add https://github.com/Nudgen-Marketing/skills --global --skill cli
npx skills add https://github.com/Nudgen-Marketing/skills --global --skill email-sending-best-practices
```

Project-scoped installs are also supported. Omit `--global` to install into the current repository only.

## Verify Install

After installation, try prompts that should trigger the skills:

- "Add a contact to Nudgen from my backend."
- "Authenticate `nudgen` CLI and switch to another team."
- "List Nudgen referral payouts in JSON from terminal."
- "Audit this retention email flow for deliverability issues."

## What's Included

This package currently ships:

- three installable skills that auto-load when relevant
- detailed reference files for API, CLI, and email-program guidance

This package does not currently ship:

- slash commands
- MCP servers

## Available Skills

### `api`

Use this skill when you need to:

- integrate Nudgen API workflows into backend code or automation
- manage contacts, campaigns, teams, brand configs, stats, and affiliate data
- decide request shape and error handling for `Authorization: Bearer <PAT>` APIs
- validate credentials and troubleshoot API behavior from application code

Example prompts:

- "Create a contact through Nudgen API after signup."
- "Switch team context through Nudgen API and then fetch campaigns."
- "Read dashboard overview stats from a backend service."

Skill file: [skills/api/SKILL.md](./skills/api/SKILL.md)

### `cli`

Use this skill when you need to:

- run `nudgen` command-line workflows
- authenticate with browser callback login and verify identity
- manage team context and run contacts, campaigns, stats, brand, and referral commands
- work with machine-readable `--json` output

Example prompts:

- "Log in to Nudgen CLI and show who I am."
- "Switch to a team and list campaigns in JSON."
- "Show referral activity from terminal."

Skill file: [skills/cli/SKILL.md](./skills/cli/SKILL.md)

### `email-sending-best-practices`

Use this skill when you need to:

- review inbox-placement and sender-reputation risk
- improve consent flows, list hygiene, and unsubscribe behavior
- improve subject lines, preview text, sender identity, and template quality
- decide campaign vs lifecycle vs transactional strategy in a Nudgen context

Example prompts:

- "Audit this onboarding flow for deliverability risk."
- "Should this message be campaign or transactional?"
- "How should we clean this stale audience before a comeback campaign?"

Skill file: [skills/email-sending-best-practices/SKILL.md](./skills/email-sending-best-practices/SKILL.md)

## Stability Notes

- This package is Nudgen-specific.
- CLI coverage tracks the current `nudgen-cli` command surface.
- Some CLI commands exist as placeholders; the `cli` skill calls those out explicitly.

## Source Of Truth

When behavior changes faster than this package, verify against:

- Nudgen CLI README: `https://github.com/Nudgen-Marketing/nudgen-cli/README.md`
- Nudgen CLI commands: `https://github.com/Nudgen-Marketing/nudgen-cli/cmd`
- Nudgen CLI API client: `https://github.com/Nudgen-Marketing/nudgen-cli/internal/api/client.go`

## Contributing

When updating a skill:

- keep `SKILL.md` concise and move detail into `references/`
- avoid duplicating the same guidance across files
- verify product details against Nudgen source code in this repository
- re-run `npx skills add https://github.com/Nudgen-Marketing/skills --list`

## Local Validation

```bash
git clone https://github.com/Nudgen-Marketing/skills.git
cd skills
npx skills add . --list
```

## Repository Structure

```text
skills/
  api/
    SKILL.md
    references/
  cli/
    SKILL.md
    references/
  email-sending-best-practices/
    SKILL.md
    references/
```
