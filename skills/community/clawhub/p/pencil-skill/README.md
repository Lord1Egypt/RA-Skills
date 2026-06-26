# Pencil Skill

[![Agent Skills Directory](https://img.shields.io/badge/skills.sh-Agent%20Skills%20Directory-0D9488)](https://skills.sh)
[![GitHub](https://img.shields.io/badge/GitHub-de--novo%2Fpencil--skill-181717?logo=github)](https://github.com/de-novo/pencil-skill)

Create and edit Pencil (`.pen`) UI design files programmatically with production-minded guardrails.

**Pencil** is a JSON-based design format for UI mockups and flows. This skill gives AI agents a reliable way to generate and modify `.pen` files while avoiding common low-quality “AI-looking” UI output.

Available on the [Agent Skills directory at skills.sh](https://skills.sh).

## Why this skill matters

Most AI-generated UI artifacts fail because they ignore design systems, spacing rhythm, visual hierarchy, and practical component composition. Pencil Skill addresses that by combining schema-aware tooling with strong design constraints, so generated output is more usable, consistent, and presentation-ready.

## Supported agents

This skill is designed to work across popular agent environments, including:

- Claude Code
- Cursor
- Codex / OpenAI coding agents
- Gemini CLI
- Other Agent Skills-compatible runtimes

## Features

- **41 curated design rules** to improve structure, hierarchy, and visual consistency
- **Anti-AI aesthetic guidance** to avoid generic, repetitive AI-style layouts
- **8 CLI tools** for `.pen` inspection, editing, variable management, and layout ops
- **Schema and reference assets** for safer, predictable transformations
- **Batch-edit workflows** for repeatable design updates at scale

## Requirements

- **Node.js 18+**

## Installation

```bash
npx skills add de-novo/pencil-skill
```

## Quick Start

```bash
# Validate a .pen file
node scripts/validate-pen.mjs mydesign.pen

# Read document tree
node scripts/read-tree.mjs mydesign.pen

# Search for nodes by type or name
node scripts/search-nodes.mjs mydesign.pen --type text
node scripts/search-nodes.mjs mydesign.pen --name "button"

# Get/set design variables (teal example)
node scripts/get-variables.mjs mydesign.pen
node scripts/set-variables.mjs mydesign.pen --var 'color.primary=color:#0D9488'

# Batch operations
node scripts/batch-design.mjs mydesign.pen --ops '[{"op":"update","id":"node1","props":{"name":"Header"}}]'

# Find available space for new elements
node scripts/find-space.mjs mydesign.pen --width 200 --height 100
```

## Repository

- GitHub: https://github.com/de-novo/pencil-skill

## What’s inside

- **SKILL.md** — Complete skill instructions and agent workflow
- **scripts/** — 8 CLI tools for `.pen` file manipulation + utility scripts
- **rules/** — 41 design rules for high-quality UI output
- **references/** — Schema (JSON + TypeScript), mappings, and component patterns
- **assets/** — Example `.pen` files for experimentation

## Documentation

See [SKILL.md](SKILL.md) for the full skill specification and usage guidance.

## License

MIT
