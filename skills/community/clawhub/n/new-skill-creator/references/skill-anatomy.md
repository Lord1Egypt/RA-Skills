# Skill Anatomy

Read this reference when deciding how to structure a new skill.

## Directory Layout

Every skill is a folder with a required SKILL.md and optional resource directories:

```
skill-name/
├── SKILL.md              # Required. Frontmatter + instructions.
├── references/           # Optional. Docs loaded into context on demand.
│   ├── domain-a.md
│   └── domain-b.md
├── scripts/              # Optional. Executable code for deterministic tasks.
│   └── do_thing.py
├── bin/                  # Optional. CLI entry points (Node.js skills).
│   └── cli.js
└── assets/               # Optional. Templates, images, fonts used in output.
    └── template.html
```

## SKILL.md Structure

### Frontmatter (YAML)

The frontmatter sits between `---` delimiters at the top of the file. It controls discovery and triggering.

Required fields:

- `name` — skill identifier. Must match the directory name exactly. Lowercase letters, digits, and hyphens only. 1-64 characters. No leading or trailing hyphens.
- `description` — what the skill does and when to use it. This is the primary trigger signal. 110-420 characters is optimal for search recall and list-page scanning.

Optional fields:

- `metadata` — platform-specific gating. For OpenClaw, must be a single-line JSON object.
- `homepage` — URL to source repo or documentation.
- `license` — SPDX identifier.
- `compatibility` — environment requirements as free text.

Example:

```yaml
---
name: pdf-redline
description: Compare two PDF documents and generate a redline diff highlighting additions, deletions, and formatting changes. Use when you need to review contract revisions, audit document versions, or produce a visual diff between two PDFs.
metadata: { "openclaw": { "emoji": "📑", "requires": { "bins": ["python3"] } } }
---
```

### Body (Markdown)

The body is loaded only after the skill triggers. Keep it under 500 lines. Recommended section order:

1. One-sentence summary (first line after frontmatter)
2. Quick Start or Prerequisites
3. When to Use / When Not to Use
4. Example Prompts (at least 3)
5. Workflow (numbered steps)
6. Commands (with `{baseDir}` paths)
7. Definition of Done (measurable criteria)
8. Resources (links to references/)

## Resource Directories

### references/

Documentation loaded into context on demand. Use when content is too long for SKILL.md or only needed in specific situations.

When to split into references/:
- Content exceeds 20 lines and is only sometimes needed
- Multiple domains or variants exist (one file per domain)
- Heavy reference material like API docs, schemas, or policies

Reference from SKILL.md with relative links:

```markdown
Read [references/api-docs.md](references/api-docs.md) for endpoint details.
```

### scripts/

Executable code for deterministic or repetitive tasks. Python or Bash preferred for portability.

When to include scripts/:
- The same code would be rewritten every time the skill runs
- Deterministic reliability matters more than flexibility
- A CLI tool wraps a multi-step operation

Reference from SKILL.md using `{baseDir}`:

```sh
python3 {baseDir}/scripts/analyze.py <input>
```

### bin/

CLI entry points, typically for Node.js skills using `package.json` bin fields.

### assets/

Files used in the skill's output, not loaded into context. Templates, images, fonts, boilerplate code.

## Progressive Disclosure

Skills use a three-level loading system:

1. **Metadata** (name + description) — always in context. ~100 tokens. This is what the agent reads to decide whether to invoke the skill.
2. **SKILL.md body** — loaded when the skill triggers. Target under 500 lines.
3. **Bundled resources** — loaded on demand. Scripts can execute without being read into context.

The goal: minimize token cost while maximizing usefulness.

## Cross-Platform Compatibility

A well-structured SKILL.md is recognized by all major agent platforms:

Platform | Minimum requirement | Optional extras
--- | --- | ---
OpenClaw | SKILL.md with `name` + `description` | `metadata.openclaw` for emoji, requires, gating
Codex | SKILL.md or AGENTS.md | `agents/openai.yaml` for UI metadata
Claude Code | SKILL.md | `.claude/agents/` or `.claude/commands/`
Cursor | SKILL.md or AGENTS.md | `.cursor/rules/`

For maximum compatibility:
- Always include SKILL.md with valid frontmatter
- Use `{baseDir}` for command paths
- Declare dependencies in `metadata.openclaw.requires` for OpenClaw gating
- Keep the name lowercase-hyphenated (OpenClaw enforces this)

## Token Cost Awareness

Every line in SKILL.md costs tokens when the skill is active. Challenge each piece of content:

- Does the agent need this to do the job?
- Would the agent already know this without being told?
- Can this be moved to references/ and loaded only when needed?

Prefer concise examples over verbose explanations. The agent is smart; tell it what it does not already know.
