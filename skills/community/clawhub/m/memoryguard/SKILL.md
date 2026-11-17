---
name: memoryguard
description: Local-first MCP memory backend and governance console for coding agents. Auto-organize, quarantine, supersede, and rollback shared memories across multiple agents.
version: 0.1.0
author: irisxc4
homepage: https://github.com/irisxc4/memoryguard
repository: https://github.com/irisxc4/memoryguard
license: MIT
tags:
  - mcp
  - memory
  - agent
  - governance
  - claude-code
  - cursor
  - codex
  - local-first
  - sqlite
---

# MemoryGuard

Shared memory for coding agents, without shared-memory chaos.

## What It Does

MemoryGuard provides a local MCP stdio memory backend that coding agents
(Claude Code, Codex, Cursor) can write to. Every write is auto-organized:
classified, deduplicated, superseded, quarantined, or compressed.

## Install

```bash
pip install agent-memguard
```

## MCP Configuration

Add to your agent's MCP config:

```json
{
  "mcpServers": {
    "memoryguard": {
      "command": "python",
      "args": ["-m", "memoryguard.mcp_server"]
    }
  }
}
```

## Tools

- `memoryguard_memory_read` - Read a single memory record by ID
- `memoryguard_memory_search` - Search memories by query, kind, or status
- `memoryguard_memory_write` - Write a new memory; auto-organizes on write
- `memoryguard_memory_update` - Update a memory (body / kind / status)
- `memoryguard_memory_delete` - Soft-delete a memory
- `memoryguard_memory_status` - Get shared memory group status
- `memoryguard_binding_create` - Bind an agent to a share group
- `memoryguard_binding_list` - List agent bindings
- `memoryguard_extract_memories` - Extract memory segments from a source file
- `memoryguard_accept_candidates` - Accept extracted candidates and write to shared memory
- `memoryguard_semantic_check` - Check text for semantic duplicates / conflicts
- `memoryguard_provider_install` - Install provider adapter (Claude / Codex / Cursor)

## Privacy

No account. No server. No telemetry. All data stays in local SQLite under `.memoryguard/`.
