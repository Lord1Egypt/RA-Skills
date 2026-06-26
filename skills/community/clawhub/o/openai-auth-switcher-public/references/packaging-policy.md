# Packaging policy

## ClawHub / AgentSkill alignment

A publishable skill should be:

- self-contained
- metadata-valid
- free of live secrets
- structured around `SKILL.md` plus optional `scripts/`, `references/`, and `assets/`

## Forbidden contents

Do not package these into a public artifact:

- real auth snapshots
- backups
- callback submissions
- oauth session folders
- local usage ledgers from a real environment
- local logs with account identifiers
- generated runtime files such as `skill-data/runtime/install-info.json`, pid files, and preview logs
- `__pycache__`
- machine-specific generated service files with user paths baked in

State layout guidance:
- temporary runtime files may stay under the skill runtime area for easy cleanup during uninstall
- important persistent state should prefer an external state base via `OPENAI_AUTH_SWITCHER_PUBLIC_STATE_DIR`, not the skill tree itself

## Release checklist

Before publication:

1. Validate the skill structure.
2. Check `SKILL.md` frontmatter.
3. Re-scan the source tree for forbidden files.
4. Re-check compatibility wording.
5. Ensure service files are templates, not machine-bound units.
6. Confirm package output is produced from the public track only.
7. Confirm the public source tree itself is clean and does not currently contain generated `skill-data/state/*` files before publication.

## Versioning policy

Suggested first public release: `0.1.0`

Suggested listing name: `OpenAI Auth Switcher Public`
Suggested slug: `openai-auth-switcher-public`

Use semantic versioning for the public track.

- patch: docs, packaging, minor bugfixes
- minor: new safe capabilities or broader compatibility
- major: breaking path model, file layout, or workflow changes
