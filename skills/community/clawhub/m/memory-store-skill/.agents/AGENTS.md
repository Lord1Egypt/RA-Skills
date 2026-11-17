# Workspace Rules for Memory Management

## Configured Memory Store Integration

Before any memory access, run `memory-store mode --json`. The safe default is `explicit`; do not automatically recall or persist anything unless the effective profile is `balanced` or `proactive`.

1. **Recall When History Matters**:
   - Search first when the user references prior decisions, progress, preferences, debugging history, conventions, or task handoff. Search when an ongoing task lacks historical context; skip recall for self-contained questions with no historical dependency.
   - Use `memory-store recall "<key_terms>" --as-agent <agent-id> --limit 3 --json` when the package binary is available, or `node scripts/memory_cli.js recall ... --json` from this repository.
   - Do not assume a hard-coded `~/.claude` location. The installer honors `CLAUDE_CONFIG_DIR` and `CODEX_CONFIG_DIR`, and other platforms use their own configuration roots.
   - For an explicit user request, pass `--intent explicit`. Policy-driven recall is allowed only in `balanced` or `proactive` and must pass `--intent automatic`.

2. **Policy-Governed Storage**:
   - `off`: never store automatically.
   - `explicit`: store only when the user explicitly asks to remember or save something.
   - `balanced`: automatically store only durable decisions, fixes, workflows, and explicitly stated preferences, up to 3 per conversation.
   - `proactive`: automatically store other durable memory types when useful, up to 5 per conversation.
   - Automatic writes must pass `--intent automatic --source-conv-id <id>` and briefly notify the user. Explicit requests pass `--intent explicit`. Never store secrets or raw transcripts.
