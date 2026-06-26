---
name: memo-bridge
description: This skill should be used when the user wants to export, import, backup, migrate, or transfer AI memory/context between different AI tools. It handles memory extraction from tools like CodeBuddy, OpenClaw, Hermes Agent, Claude Code, and Cursor, and can import into any of these tools plus ChatGPT, Doubao (豆包), and Kimi. Trigger phrases include "记忆迁移", "导出记忆", "备份记忆", "memory migration", "memory export", "transfer context", "switch AI tool", "换工具", "迁移到", as well as any mention of moving preferences, context, or history between AI assistants.
---

# MemoBridge — AI Memory Migration Skill

## Purpose

MemoBridge extracts, standardizes, and migrates AI memories across tools and workspaces. AI assistants accumulate valuable context over time — user preferences, project history, knowledge progress, vocabulary lists, daily routines. This skill ensures none of that is lost when switching tools or machines.

## When to Use

- User wants to switch AI coding tools (CodeBuddy → Claude Code → Cursor → OpenClaw → Hermes)
- User wants to export or backup their AI memory
- User wants to onboard a new AI assistant with existing context
- User wants to share AI context with a teammate
- User is setting up a new machine or workspace
- User mentions "记忆迁移", "导出记忆", "memory export/import/migrate"

## Prerequisites

Node.js >= 22.0.0 must be installed. The MemoBridge CLI is available at the project root.

## Supported Tools (8 total)

| Tool | Extract | Import | Method |
|------|---------|--------|--------|
| CodeBuddy | ✅ | ✅ | Direct file read (`.codebuddy/` + `.memory/`) |
| OpenClaw | ✅ | ✅ | Direct file read (`~/.openclaw/workspace/`) |
| Hermes Agent | ✅ | ✅ | Direct file read (`~/.hermes/memories/`) |
| Claude Code | ✅ | ✅ | Direct file read (`CLAUDE.md` + `~/.claude/`) |
| Cursor | ✅ | ✅ | Direct file read (`.cursorrules` + `~/.cursor/`) |
| ChatGPT | ✅ (prompt) | ✅ | Prompt-guided export, instruction-based import |
| Doubao / 豆包 | ✅ (prompt) | ✅ | Prompt-guided export, instruction-based import |
| Kimi | ✅ (prompt) | ✅ | Prompt-guided export, context injection import |

## Core Workflow

### Step 1: Detect installed tools

Run the detect command to discover all AI tools on the system:

```bash
cd {project_root}
node dist/cli.js detect
```

This scans for local tools (CodeBuddy/OpenClaw/Hermes/Claude Code/Cursor) and lists cloud tools (ChatGPT/Doubao/Kimi) that require prompt-guided export.

### Step 2: Extract memories

For **local tools** (direct file access):

```bash
# CodeBuddy — auto-scans all workspaces
node dist/cli.js extract --from codebuddy -o ./memo-bridge.md

# CodeBuddy — specific workspace
node dist/cli.js extract --from codebuddy --workspace /path/to/project -o ./memo-bridge.md

# OpenClaw
node dist/cli.js extract --from openclaw -o ./memo-bridge.md

# Hermes Agent
node dist/cli.js extract --from hermes -o ./memo-bridge.md

# Claude Code
node dist/cli.js extract --from claude-code -o ./memo-bridge.md

# Cursor (with workspace for project rules)
node dist/cli.js extract --from cursor --workspace /path/to/project -o ./memo-bridge.md
```

For **cloud tools** (prompt-guided), generate the optimal export prompt:

```bash
node dist/cli.js prompt --for doubao
node dist/cli.js prompt --for kimi
node dist/cli.js prompt --for chatgpt
```

Then instruct the user to: copy the prompt → paste into the AI tool's chat → copy the AI's response → save as a file.

### Step 3: Import memories

For **file-based** tools:

```bash
# To Claude Code (appends to CLAUDE.md)
node dist/cli.js import --to claude-code --input ./memo-bridge.md

# To Hermes Agent (auto-trims to 2200 UTF-8 bytes)
node dist/cli.js import --to hermes --input ./memo-bridge.md

# To OpenClaw (appends to MEMORY.md)
node dist/cli.js import --to openclaw --input ./memo-bridge.md

# To Cursor (requires --workspace)
node dist/cli.js import --to cursor --input ./memo-bridge.md --workspace /path/to/project

# To CodeBuddy
node dist/cli.js import --to codebuddy --input ./memo-bridge.md --workspace /path/to/project
```

For **instruction-based** tools:

```bash
# Generates text for user to paste into ChatGPT/Doubao/Kimi
node dist/cli.js import --to doubao --input ./memo-bridge.md
node dist/cli.js import --to chatgpt --input ./memo-bridge.md
node dist/cli.js import --to kimi --input ./memo-bridge.md
```

### Step 4: One-step migration (shortcut)

```bash
node dist/cli.js migrate --from codebuddy --to claude-code
node dist/cli.js migrate --from openclaw --to hermes
```

## Key Options

| Option | Description |
|--------|-------------|
| `--workspace <path>` | Specify a single workspace path |
| `--scan-dir <path>` | Specify root directory for auto-discovery |
| `--output <path>` | Output file path (default: `./memo-bridge.md`) |
| `--input <path>` | Input file path |
| `--dry-run` | Preview mode, no actual writes |
| `--overwrite` | Overwrite existing files instead of appending |
| `--verbose` | Detailed output |

## Extending with Custom Adapters

Third-party adapters can be registered at runtime via the public registry
API — useful when a user has a proprietary or yet-unsupported tool:

```typescript
import { extractorRegistry, importerRegistry, BaseExtractor } from 'memo-bridge';

class MyToolExtractor extends BaseExtractor {
  readonly toolId = 'my-tool' as any;
  async extract() { /* ... */ }
}

extractorRegistry.register('my-tool' as any, () => new MyToolExtractor());
```

See `references/adapter-guide.md` for the full three-step adapter recipe.

## Intermediate Format

The standard interchange format is `memo-bridge.md` — Markdown with YAML front matter. See `references/format-spec.md` for the complete specification.

Key properties:
- Human-readable (any text editor)
- LLM-friendly (can be used directly as CLAUDE.md)
- Git-friendly (plain text, version-trackable)
- Tool-namespaced `extensions` section preserves tool-specific data
  (Hermes skills, OpenClaw SOUL/DREAMS, …) across migrations without
  polluting the common memory lists.

## Security Features

- **Privacy sanitization**: Automatically redacts 18 types of sensitive
  information (API keys, passwords, tokens, SSH keys, emails, private
  IPs, Authorization headers, custom API headers like `X-API-Key`,
  database connection strings with embedded credentials).
- **Path validation**: Prevents path traversal and symlink attacks;
  case-insensitive on Windows so `c:\program files` can't bypass the
  denylist.
- **Content size limits**: 5MB write limit, 10MB read limit enforced on
  every extractor file read (no more unbounded reads).
- **System directory protection**: Blocks writes to `/etc`, `/bin`,
  `/usr`, etc. — except OS-managed temp subtrees (`/var/folders/`,
  `/var/tmp/`, `/private/tmp/`).
- **Strict tool-id validation**: CLI `--from` / `--to` / `--for` args
  are validated against the registered tool list before dispatch.

## Error Handling

- If no workspaces found: suggest `--workspace` or `--scan-dir` flags
- If tool not detected: suggest installing the tool or using prompt-guided export
- If import fails due to permissions: suggest checking file permissions or using `--dry-run` first
- If Hermes import exceeds limit: content is automatically prioritized and trimmed

## Building from Source

To build the CLI before first use:

```bash
cd {project_root}
npm install
npm run build
```

The project has 395 unit tests and a GitHub Actions CI that runs
`lint → test → build` on every push. To verify the local install:

```bash
npm test    # ~500ms
```

