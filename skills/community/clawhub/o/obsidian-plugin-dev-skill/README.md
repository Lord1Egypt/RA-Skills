# obsidian-plugin-dev

A comprehensive AI agent skill for Obsidian plugin development with TypeScript. Covers the full development lifecycle from plugin creation to community submission.

## What This Is

This is a **skill** designed for AI coding agents (Claude Code, OpenCode, etc.) that provides deep, structured knowledge for building Obsidian community plugins. When the agent uses this skill, it gains access to:

- 20 Critical Rules that prevent instant rejection from community review
- 28 ESLint rules from `eslint-plugin-obsidianmd` v0.1.9
- 12 topic-based reference files covering every aspect of plugin development
- Real code patterns from production plugins, not toy demos

## Features

| Coverage | Details |
|----------|---------|
| **Plugin Lifecycle** | onload/onunload ordering, auto-cleanup vs manual cleanup |
| **CodeMirror 6** | Editor extensions, decorations, syntax highlighting |
| **React / Svelte / Vue** | Framework integration with proper lifecycle management |
| **Vault API** | File CRUD, frontmatter, events, debouncing, caching |
| **Settings** | UI, deep merge, versioned migration pipelines |
| **Security** | XSS prevention, SecretStorage, network requests |
| **Accessibility** | Keyboard nav, ARIA labels, focus indicators, 44px touch targets |
| **ESLint** | All 28 rules with severity, fixability, and examples |
| **CI/CD** | GitHub Actions workflows, version bumping |
| **Submission** | Manifest validation, naming rules, pre-submission checklist |

## Structure

```
obsidian-plugin-dev/
├── SKILL.md                 # Main skill file (quick reference + pointers)
├── LICENSE                  # MIT License
└── reference/
    ├── lifecycle.md         # Plugin lifecycle, views, modals, events
    ├── eslint-rules.md      # All 28 eslint-plugin-obsidianmd rules
    ├── accessibility.md     # MANDATORY a11y requirements
    ├── editor-extensions.md # CodeMirror 6 extensions
    ├── frameworks.md        # React, Svelte, Vue integration
    ├── vault-operations.md  # File CRUD, frontmatter, links
    ├── settings-migration.md # Settings UI, deep merge, migrations
    ├── security.md          # XSS, SecretStorage, network
    ├── css-accessibility.md # CSS variables, scoping, themes
    ├── dev-workflow.md      # Build, hot-reload, CLI, ESLint config
    ├── testing.md           # Unit tests, mocking Obsidian API
    └── cicd-release.md      # GitHub Actions, submission steps
```

## Installation

### Claude Code

Copy the `obsidian-plugin-dev/` folder to your Claude skills directory:

```bash
cp -r obsidian-plugin-dev ~/.claude/skills/
```

### OpenCode

Copy to the OpenCode skills directory:

```bash
cp -r obsidian-plugin-dev ~/.config/opencode/skills/
```

### Other AI Agents

Place the skill folder where your agent looks for skills. The skill follows the standard `SKILL.md` + `reference/` structure.

## How It Works

When you ask your AI agent to build an Obsidian plugin, the skill provides:

1. **Critical Rules** — 20 rules that prevent instant submission rejection
2. **Code Patterns** — Real TypeScript examples for every common task
3. **ESLint Compliance** — All 28 rules with explanations and fixes
4. **Pre-Submission Checklist** — Every item the submission bot checks

Example prompts that trigger this skill:

- "Create an Obsidian plugin that..."
- "Fix my plugin for community submission"
- "Add a React view to my Obsidian plugin"
- "Help me set up CI/CD for my Obsidian plugin"

## Tested Against

This skill was evaluated against 3 test cases:

| Test Case | Without Skill | With Skill |
|-----------|:------------:|:----------:|
| Create plugin from scratch | 70% | 100% |
| Fix buggy rejected plugin | 20% | 100% |
| React plugin with lifecycle | 50% | 100% |

## Acknowledgments

Built by studying and cross-referencing:

- [gapmiss/obsidian-plugin-skill](https://github.com/gapmiss/obsidian-plugin-skill) — ESLint rules, accessibility
- [Leonezz/obsidian-plugin-dev-skill](https://github.com/Leonezz/obsidian-plugin-dev-skill) — React integration, settings migration, testing
- [davidvkimball/obsidian-dev-skills](https://github.com/davidvkimball/obsidian-dev-skills) — Theme development, init scripts
- [adriangrantdotorg/Obsidian-SKILLS](https://github.com/adriangrantdotorg/Obsidian-SKILLS) — CLI skill, best practices
- [obsidianmd/eslint-plugin](https://github.com/obsidianmd/eslint-plugin) — Official 28 ESLint rules

## License

[MIT](LICENSE) — Yungho
