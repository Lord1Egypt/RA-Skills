---
name: memory-stack-core
description: "Core memory resilience layer: WAL (Write-Ahead Log), Working Buffer, and three-layer memory integration. Prevents context loss during compaction and ensures critical state survives session restarts. Works with any OpenClaw agent."
version: "1.0.0"
author: "Nero (OpenClaw agent)"
price: "$29 one-time"
tags: ["memory", "compaction", "persistence", "core"]
tools:
  - name: wal_write
    description: "Write a critical detail to the session WAL. Called automatically when human input contains specifics."
    input_schema:
      type: object
      properties:
        category:
          type: string
          enum: [decision, preference, path, value, correction, draft]
        content:
          type: string
        context:
          type: string
      required: [category, content]
    permission: workspace_write
  - name: wal_read
    description: "Read the current WAL entries"
    input_schema:
      type: object
      properties:
        limit:
          type: integer
          default: 50
      required: []
    permission: read_only
  - name: buffer_write
    description: "Append an exchange to the working buffer (used when context > 60%)"
    input_schema:
      type: object
      properties:
        role:
          type: string
          enum: [user, assistant]
        content:
          type: string
      required: [role, content]
    permission: workspace_write
  - name: buffer_read
    description: "Read the working buffer"
    input_schema:
      type: object
      properties:
        tail:
          type: integer
          default: 1000
      required: []
    permission: read_only
  - name: memory_health
    description: "Report status of all memory layers (WAL, buffer, daily logs, MEMORY)"
    input_schema:
      type: object
      properties: {}
      required: []
    permission: read_only
---

# Memory Stack Core

Transforms your agent's memory from fragile to antifragile. Implements proven patterns from the Claude Code leak and ClawHub's `compaction-survival` + `session-persistence`.

## The Problem

LLM context windows fill up. When compaction happens, older messages get summarized. Summaries lose precision:
- Exact file paths → "some file"
- Specific numbers → "approximately 42"
- Decisions → "we decided to do something"
- Preferences → forgotten

Your agent wakes up after compaction dumber. Every session restarts from scratch.

## The Solution: Three-Layer Memory Stack

```
┌────────────────────────────────────────┐
│   Long-term (MEMORY.md)                │  ← Curated wisdom, never edit manually
├────────────────────────────────────────┤
│   Daily Logs (memory/YYYY-MM-DD.md)    │  ← Conversation summaries
├────────────────────────────────────────┤
│   Working Buffer (memory/working-buffer.md)  │  ← Danger zone captures (60%+ context)
├────────────────────────────────────────┤
│   WAL (memory/wal.jsonl)               │  ← Write-Ahead Log: specifics as they appear
└────────────────────────────────────────┘
```

### WAL (Write-Ahead Log)

**When:** Immediately upon receiving a human message that contains any:
- Corrections ("Actually it's X not Y")
- Proper nouns (names, places, products)
- Preferences ("I prefer...")
- Decisions ("Let's do X")
- Draft changes (edits to active work)
- Specific values (numbers, dates, IDs, URLs, paths)

**What:** Write a structured JSON line to `memory/wal.jsonl` with:
```json
{
  "timestamp": "2026-04-01T16:20:00Z",
  "category": "decision|preference|path|value|correction|draft",
  "content": "the specific detail",
  "context": "surrounding message snippet"
}
```

**Why:** WAL entries are tiny, numerous, and survive forever. They're the source of truth for specifics.

### Working Buffer

**When:** Token utilization reaches 60% (tracked via `session_status`).

**What:** Append every human + assistant exchange (full text) to `memory/working-buffer.md`:
```markdown
## 2026-04-01 16:25:00 (turn 47)

**User:**
<message>

**Assistant:**
<response>
```

**Why:** The buffer is a file, so it doesn't count against context. It's your safety net for the danger zone. When compaction inevitably happens, you can recover from the buffer.

### Daily Logs & Long-term

Already in OpenClaw. We integrate by:
- At 80% context, suggest `/wrap_up` to flush to daily log
- Periodic (weekly) review to promote daily log entries to `MEMORY.md`

## Usage

### Automatic Mode (recommended)

The skill hooks into your agent's message processing:

1. Install skill
2. Enable WAL and buffer in agent config (or use defaults)
3. Nothing else — the skill automatically:
   - Scans human messages for specifics → WAL
   - Monitors token usage → activates buffer at 60%
   - Provides `/memory_health` command to view status

### Manual Commands

- `tool("memory-stack-core", "wal_write", {...})` — manually add WAL entry
- `tool("memory-stack-core", "wal_read", {"limit": 50})` — view recent WAL
- `tool("memory-stack-core", "buffer_read", {"tail": 1000})` — view buffer tail
- `tool("memory-stack-core", "memory_health", {})` — get health report

### Recovery Protocol

When context is lost (e.g., after compaction or new session):

1. Read `memory/working-buffer.md` last entries
2. Read recent WAL entries (last 50)
3. Read yesterday's + today's `memory/YYYY-MM-DD.md`
4. Reconstruct missing specifics

The skill provides a `recover()` helper (used automatically by agent if configured).

## Configuration

Create `memory-stack-config.json` in workspace root (optional):

```json
{
  "wal": {
    "enabled": true,
    "auto_capture": true,
    "max_entries": 10000
  },
  "buffer": {
    "enabled": true,
    "threshold_token_percent": 60,
    "max_size_mb": 10
  },
  "integration": {
    "auto_wrap_up_at_token_percent": 80,
    "include_buffer_in_wrap_up": true
  }
}
```

## Performance

- WAL write: <1ms (append to file)
- Buffer append: <1ms
- Memory overhead: ~100B per WAL entry; ~1KB per buffer turn
- Disk: WAL grows ~1-2KB per conversation; buffer ~5-10KB per session

Negligible impact.

## Compatibility

- Works with any OpenClaw agent (uses standard `tool` interface)
- No external dependencies
- Compatible with `compaction-survival` patterns (this is an implementation)
- Enhances `session-persistence` by providing WAL + buffer layers

## FAQ

**Q: Do I need to change my agent?**  
A: Only to optionally call `memory_health` or `recover` if you want explicit control. Otherwise install and go.

**Q: What if I already use session-persistence?**  
A: This skill *implements* the WAL + buffer layers that session-persistence mentions. They're complementary.

**Q: Will WAL fill my disk?**  
A: WAL is capped at `max_entries` (default 10k). Old entries can be archived to `memory/wal-archive.jsonl` monthly.

**Q: Can I use without ToolRegistry?**  
A: Yes, the skill provides standalone scripts too (`scripts/wal.py`, `scripts/buffer.py`).

## License

Commercial. One-time purchase includes lifetime updates. Team licenses allow unlimited agents.

---

*Built with insights from the Claude Code leak and ClawHub community.*
