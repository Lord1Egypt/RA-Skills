---
name: memory-sync-protocol
description: Synchronize durable behavior or preference changes across TOOLS.md, MEMORY.md, AGENTS.md, and memory/YYYY-MM-DD.md with one consistent workflow. Use when user says to remember/update rules, skill routing, defaults, operating conventions, or asks for "sync across files" / "记住并同步" / "更新记忆治理".
---

# Memory Sync Protocol

When this skill is triggered, execute the following sequence strictly.

## 1) Classify the change
- **Execution detail** (tool/profile/path/routing trigger) → `TOOLS.md`
- **Long-term stable preference** (high-level) → `MEMORY.md`
- **Governance/process rule** (how to maintain) → `AGENTS.md`
- **Event log / audit trail** (what changed today) → `memory/YYYY-MM-DD.md`

## 2) Update files with minimal duplication
- Write detailed routing/trigger logic in `TOOLS.md`.
- Write only high-level summary in `MEMORY.md`.
- Avoid copying large sections between files.
- If adding a new policy, also add short maintenance note in `AGENTS.md`.

## 3) Append daily log
- In `memory/YYYY-MM-DD.md`, record:
  - what changed,
  - why,
  - affected files.

## 4) Git discipline
- Before major rewrites: create a backup commit.
- After updates: commit with semantic message, e.g.
  - `docs(routing): ...`
  - `docs(memory): ...`
  - `chore(memory): ...`

## 5) Reply format
Return a concise sync report:
- Updated files
- Key rules added/changed
- Commit hash/message

## Guardrails
- Do not store sensitive secrets in MEMORY/TOOLS unless user explicitly asks.
- Do not bloat MEMORY with skill inventories or transient logs.
- Prefer TOOLS for concrete calling rules; MEMORY for durable preference only.
