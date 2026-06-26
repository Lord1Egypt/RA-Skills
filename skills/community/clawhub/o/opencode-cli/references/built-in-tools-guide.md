# Built-in Tools Guide

> OpenCode Agent available tools reference

---

## File Operations

| Tool | Purpose | Example |
|------|---------|---------|
| `read` | Read file contents | `read path/to/file.ts` |
| `write` | Create or overwrite file | `write path/to/file.ts "content"` |
| `edit` | Exact string replacement | `edit old "new" in file.ts` |

## Shell Operations

| Tool | Purpose | Example |
|------|---------|---------|
| `bash` | Execute shell commands | `bash "npm test"` |
| `grep` | Regex search file contents | `grep "pattern" in src/` |
| `glob` | Pattern match find files | `glob "**/*.ts"` |

## Task Management

| Tool | Purpose |
|------|---------|
| `todowrite` | Create/update task lists |
| `todoread` | Read current task state |

## Others

| Tool | Purpose |
|------|---------|
| `skill` | Load skill files into conversation |
| `webfetch` | Fetch web page content |
| `lsp` | Language Server integration (experimental) |

---

## Tool Permissions

Different agents have different tool permissions:

| Agent | File Operations | Shell | Read-only Operations |
|-------|-----------------|-------|---------------------|
| `build` | ✅ Full access | ✅ Full access | ✅ |
| `plan` | ⚠️ Requires approval | ⚠️ Requires approval | ✅ |
| `explore` | ❌ | ❌ | ✅ |

---

*Tools Guide v1.0 - 2026-04-05*