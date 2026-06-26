---
name: opencode-cli
description: "OpenCode CLI integration skill. Designed for AI agents like OpenClaw to execute coding tasks via OpenCode CLI. Core features: (1) Plan→Build workflow (2) Session management (3) MCP integration (4) Background task monitoring. Use this skill when you need: multi-step coding, Plan→Build workflow, MCP integration, or background task monitoring. NOT for: simple one-line edits (use edit tool directly), quick file reads (use read tool directly)."
dependencies:
  skills:
    - using-superpowers
  tools:
    - bash
    - read
    - write
    - edit
    - process
env:
  optional:
    - CONTEXT7_API_KEY
    - SUPABASE_URL
    - SUPABASE_ANON_KEY
---

# OpenCode CLI Integration

This skill is designed for **AI agents like OpenClaw to execute coding tasks via OpenCode CLI**.

OpenCode is an AI-powered code editor CLI. When called via OpenClaw, **only CLI mode is used**.

---

## Security Scope

**What this skill does:**
- Integrates with OpenCode CLI for coding tasks
- Manages sessions, plans, and builds
- Optionally connects to configured MCP servers (Playwright, Supabase, Context7)

**What this skill does NOT do:**
- Install or modify system-wide packages
- Access credentials outside configured MCP servers
- Persist beyond user-initiated sessions

**Credential access:**
- MCP servers (if configured) may use environment variables like `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `CONTEXT7_API_KEY`
- Skills run in project context; avoid committing secrets to version control
- Only use this skill in repositories/environments you trust

---

## Core Command

```bash
opencode run -m <provider/model> -- "<prompt>"
```

**Example:**
```bash
opencode run -m <provider/model> -- "Add error handling to the login function"
```

---

## Plan→Build Workflow (Core)

### ⚠️ Key Rule: Maintain Same Session

**Correct approach:**
```bash
# 1. Start Plan (creates session)
opencode run -m <model> -- 'Analyze task, output plan.'

# 2. Wait for user APPROVE

# 3. Switch to Build (continue same session)
opencode run --continue --agent build -- 'Implement approved plan.'
```

**Wrong approach (context lost):**
```bash
❌ opencode run --agent plan "..."   # session A
❌ opencode run --agent build "..."  # session B (separate!)
```

### Agent Options

| Agent | Purpose |
|-------|---------|
| `plan` | Planning, analysis, design |
| `build` | Implementation, coding, modification |
| `explore` | Codebase exploration |

---

## Session Management

```bash
opencode run --continue -- '<prompt>'
opencode run --session <id> -- '<prompt>'
opencode run --continue --fork -- '<prompt>'
opencode session list
opencode session delete <id>
```

---

## OpenClaw Integration

### Standard Task
```bash
opencode run -m <model> -- '<task>'
```

### Background Task
```bash
opencode run -m <model> -- '<task>'
process action:poll sessionId:<id> timeout:30000
process action:log sessionId:<id>
process action:kill sessionId:<id>
```

### Monitoring Discipline

> ⚠️ **Mandatory**: After starting, must actively monitor. Do not wait for system event.

```
Start → Get sessionId
  ↓
Every 30-60s: poll + log
  ↓
Progress → Report
Error → Report immediately
Complete → Report result (do not wait for event)
```

**Violation criteria:**
- Start without monitoring → Abandoning responsibility
- User asks "is it done?" before checking → Failure

---

## MCP Integration

OpenCode supports MCP integration to extend capabilities. Must run in project root directory.

**Common tools:** Playwright (UI automation), Supabase (database)

**Scenario guide:**

| Scenario | Reference |
|----------|-----------|
| Need UI automation testing (Playwright) | `references/mcp-config-guide.md` |
| Need database operations (Supabase) | `references/mcp-config-guide.md` |
| MCP not loading, troubleshoot config | `references/mcp-config-guide.md` |

---

## Built-in Tools

OpenCode Agent built-in tools: read/write/edit, bash, grep/glob, todowrite, skill, webfetch

**Scenario guide:**

| Scenario | Reference |
|----------|-----------|
| Unsure if Agent can perform an operation | `references/built-in-tools-guide.md` |
| Plan Agent reports insufficient permissions | `references/built-in-tools-guide.md` (see tool permissions table) |

---

## Practical Tips

- **File reference**: Use `@filename` to quickly reference files
- **Undo changes**: `/undo` to undo, `/redo` to restore

**Scenario guide:**

| Scenario | Reference |
|----------|-----------|
| Want to reference file instead of typing path | `references/tips-guide.md` (file reference) |
| Made mistake and want to rollback | `references/tips-guide.md` (undo/redo) |
| Want to learn TUI shortcuts | `references/tips-guide.md` (shortcuts) |

---

## Skills Configuration

**Scenario guide:**

| Scenario | Reference |
|----------|-----------|
| Want to add custom skill | `references/skills-config-guide.md` |
| Unsure where to place skill files | `references/skills-config-guide.md` |

---

## Common Patterns

> **Note**: Examples use `openclaw system event` for optional task notification. This is an OpenClaw platform command. Omit if running outside OpenClaw.

### Planning Task

```bash
opencode run -m <model> -- 'Analyze task, output plan.'
```

For detailed plan format, see project workflow documentation.

### Implementation Task

```bash
opencode run -m <model> -- 'Execute approved plan.'
```

Verify with: `npm run build && npm test`

### Database Operations

```bash
cd /path/to/project
opencode run -m <model> -- 'Use Supabase MCP for database operations.'
```

See: `references/mcp-config-guide.md` for MCP setup.

### UI Testing

```bash
opencode run -m <model> -- 'Use Playwright MCP for UI testing.'
```

See: `references/mcp-config-guide.md` for MCP setup.

---

## Troubleshooting

### sysctl not found

```bash
export PATH="/usr/sbin:/usr/bin:/sbin:/bin:$PATH"
```

### MCP not loading

Ensure running in project root:
```bash
cd /path/to/project && opencode run ...
```

See: `references/mcp-config-guide.md`

### Session context lost

Use `--continue` instead of separate starts:
```bash
✅ opencode run --continue --agent build "..."
❌ opencode run --agent build "..."
```

---

## Quick Reference

### Common Commands

| Task | Command |
|------|---------|
| Plan task | `opencode run -m <model> -- 'Analyze...'` |
| Build (continue session) | `opencode run --continue --agent build -- 'Implement...'` |
| Continue last session | `opencode run --continue` |
| Specific session | `opencode run --session <id>` |
| Fork session | `opencode run --continue --fork` |
| List sessions | `opencode session list` |
| Delete session | `opencode session delete <id>` |
| View models | `opencode models` |

### OpenClaw Integration

| Task | Command |
|------|---------|
| Background task | `pty:true background:true command:"opencode run..."` |
| Monitor progress | `process action:poll sessionId:<id>` |
| View logs | `process action:log sessionId:<id>` |
| Terminate task | `process action:kill sessionId:<id>` |

### Configuration Guide Index

| Scenario | Reference |
|----------|-----------|
| UI automation / Database operations | `references/mcp-config-guide.md` |
| Agent tool capabilities / Permissions | `references/built-in-tools-guide.md` |
| Shortcuts / File reference / Undo | `references/tips-guide.md` |
| Add custom skill | `references/skills-config-guide.md` |

---

*CLI Integration v2.6 - 2026-04-05*