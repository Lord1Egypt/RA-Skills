# Harness Engineering Skill

`harness-engineering` is a Codex skill for evolving an existing repository toward Harness Engineering.

It is meant for real codebases that already have product code, delivery history, and project-specific constraints. The goal is not to force every repo into the same greenfield template. The goal is to make the repo easier for agents to work in by reducing hidden context, improving repository-local source of truth, and replacing policy-only documentation with executable checks.

## What this skill does

- Audits a repository for agent legibility gaps
- Strengthens `AGENTS.md` and supporting docs
- Adds or repairs repo-local source-of-truth artifacts
- Replaces placeholder governance with runnable validation
- Improves CI so agent workflows are enforced, not just described
- Encourages incremental adoption instead of broad rewrites

## Good fit

Use this skill when you want to:

- assess a repo against Harness Engineering ideas
- improve an existing repository so agents can operate with less chat-only context
- add `AGENTS.md`, architecture docs, execution plans, and quality scorecards
- introduce lightweight governance checks with `bun`
- reduce documentation drift and architectural drift over time

## Not the goal

This skill is not primarily about turning every repository into the same universal template.

It should preserve:

- the existing product structure
- the current stack where it makes sense
- project-specific naming and domain boundaries

It should remove:

- hidden tribal knowledge
- dead references
- fake automation claims
- placeholder CI that never checks anything real

## Files

- `SKILL.md`: the skill instructions and trigger description
- `agents/openai.yaml`: UI metadata for the skill
- `references/checklist.md`: compact review checklist for repo audits

## Suggested usage

Example prompt:

```text
Use $harness-engineering to audit this repository and evolve it toward Harness Engineering without forcing a greenfield rewrite.
```

## Installation

Copy this folder into your Codex skills directory:

```text
$CODEX_HOME/skills/harness-engineering
```

On this machine, that path is:

```text
C:\Users\kisde\.codex\skills\harness-engineering
```

## License

Add a license here if you plan to publish the skill as a standalone GitHub repository.
