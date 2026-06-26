# Packaging

This folder is structured to be `.skill`-ready.

## Expected layout
- `SKILL.md`
- `references/`
- `scripts/`
- root examples and templates only when they directly support use of the skill

## Included packaging-friendly files
- `config.example.json`
- `state.example.json`
- `trades.example.json`
- `openclaw-cron-templates.json`

## Before packaging
- keep `SKILL.md` concise
- keep references one level deep
- ensure scripts are executable
- avoid unrelated docs
- test representative scripts
- verify examples do not contain real secrets
- verify approval/live files do not submit directly to exchange APIs without an explicit integration layer

## Package
Use the OpenClaw / AgentSkills packager in an environment that has the packaging utility available.
The resulting archive should preserve this folder structure and be named `moneysharks.skill`.

## Validation checklist
- `SKILL.md` frontmatter is valid
- references are discoverable from `SKILL.md`
- scripts run locally with sample inputs
- cron templates are disabled by default (enabled automatically by onboarding on ACCEPT)
- `autonomous_live_consent` defaults to `false` in `config.example.json` (set only by onboarding gate)
- no real credentials present in any example file

## Important
Package only after reviewing the skill for your own risk tolerance and exchange-account safety.
