---
name: obsidian-vault-integration
description: Read and write data with an Obsidian vault used as a shared knowledge base. Use when an agent needs to read vault notes (business plan, tasks, milestones, team info), write updates back to vault files, or query vault contents. Triggers on phrases like "read the vault", "check the business plan", "update open questions", "add a milestone", "what's in the vault", "update the business plan", "check the vault".
metadata:
  env:
    OBSIDIAN_VAULT_PATH: "Path to the Obsidian vault directory. If not set, uses default from AGENTS.md."
---

# Obsidian Vault Integration

Integrates OpenClaw agents with an Obsidian vault for shared knowledge management. Supports structured reading of task lists, milestones, team info, and safe writes back to vault files.

## Configuration

Set the vault path via environment variable `OBSIDIAN_VAULT_PATH`. If not set, uses the default path noted in AGENTS.md.

**Environment variables used:**
- `OBSIDIAN_VAULT_PATH` — Path to the Obsidian vault directory (optional, defaults to agent's configured path)

## Quick Start

### Read tasks from vault

```bash
python scripts/vault-read.py <vault-path> --file open-questions.md --format json
```

Returns JSON array of tasks parsed from checkbox items, with priority (critical/important/nice), status (todo/done), owner, and title.

### Add a task to the vault

```bash
python scripts/vault-write.py <vault-path> --file open-questions.md --action add-task --title "New task" --priority important --owner Dave
```

### Mark a task done

```bash
python scripts/vault-write.py <vault-path> --file open-questions.md --action mark-done --task-id 3
```

## File Discovery

Files are discovered by their frontmatter `type:` field as the primary method. If a file is moved to a subfolder, it's still found by metadata.

```yaml
---
type: open-questions
status: active
---
```

**Fallback chain:**
1. Frontmatter `type:` field (most reliable — survives moves)
2. Filename pattern matching (e.g., `*open-questions*`)
3. Full-text search (slowest, last resort)

See `references/file-formats.md` for parsing rules per file type.

## Error Handling

| Code | Meaning | Recovery |
|------|---------|----------|
| ERR_VAULT_NOT_FOUND | Vault path doesn't exist | Check OBSIDIAN_VAULT_PATH or AGENTS.md |
| ERR_FILE_NOT_FOUND | Requested file not found | Run discovery to find by metadata |
| ERR_PARSE_FAILED | Malformed markdown | Return partial data with warning |
| ERR_CONFLICT | File changed since last read | Re-read, resolve manually |

## Safety

- All writes are logged to `<vault>/.vault-audit.log` (timestamp, agent, file, action)
- Timestamp check prevents overwrites when file has changed
- Solo mode (default): all agents can read/write everything
- Team mode (v2): per-agent folder permissions

## Permissions

**Solo mode (default):** No config needed. All agents have full read/write access.

**Team mode (v2, not yet implemented):** Optional permissions block in SKILL.md for folder-level access control per agent.

## Scripts

- `vault-read.py` — Read and parse vault files into structured JSON
- `vault-write.py` — Write updates back to vault files with safety checks

## References

- `references/file-formats.md` — Parsing rules for each file type
