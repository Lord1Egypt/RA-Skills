# OpenClaw Skill Variant

Use this path only when the user explicitly wants an OpenClaw skill.

## Good fit

Build a skill when the workflow needs to repeatedly:

- generate persona product folders
- normalize pack structure
- audit prompts for consistency
- split outputs into system prompt / examples / config / sales files

## Poor fit

Do not turn a single persona pack into a skill unless the value is agent-side reuse.

## Suggested structure

`skill-name/`
- `SKILL.md`
- `references/`
- optional `assets/templates/`
- optional `scripts/`

## Skill idea examples

- `persona-pack-builder`
- `prompt-product-auditor`
- `companion-persona-factory`

## Packaging note

After editing the skill, run the validator or package script from the skill-creator toolkit before distribution.
