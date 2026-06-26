# Kiipu Skills

Standalone Kiipu skill assets for Claude Code workflows.

`@kiipu/skills` publishes the raw Kiipu skill markdown used by Claude Code integrations. Choose this package when you want the skill assets themselves, without the full plugin packaging layer.

Use it when you want:

- the standalone Kiipu skill files without the full plugin package
- to inspect the published skill behavior directly
- to bundle the Kiipu skill assets into your own Claude Code workflow

If you want a ready-to-install Claude Code plugin, use `@kiipu/claude-plugin` instead.

## Install

```bash
npm install @kiipu/skills
```

## What It Includes

The package publishes static skill markdown under:

```text
skills/
  kiipu-cli/
    SKILL.md
```

These files define how Kiipu should be used from a Claude Code skill workflow.

## Which Package To Choose

Choose `@kiipu/skills` when you need the standalone skill assets by themselves.

Choose `@kiipu/claude-plugin` when you want the full packaged Claude Code plugin surface.

Choose `@kiipu/cli` when you want the executable command line tool used by the skill.

## Related Packages

- `@kiipu/cli` is the executable CLI used for real Kiipu actions
- `@kiipu/skills` publishes the standalone skill assets
- `@kiipu/claude-plugin` packages those assets for Claude Code installation
