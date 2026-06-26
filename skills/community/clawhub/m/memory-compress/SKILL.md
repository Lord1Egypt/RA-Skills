---
name: memory-compress
description: "Never let your agent forget what matters. Compress verbose daily logs into structured summaries — 4-8x compression, zero information loss. Inspired by classical Chinese writing: strip redundancy, keep turning points, let structure carry meaning. Smart hybrid extraction finds key events, lessons, decisions and todos from any markdown format. No API keys, no vector DB, no dependencies. Just run it. Works with any OpenClaw agent, Cursor, Claude Code, or any markdown-based memory system."
---

# Memory Compress

> Your agent's memory is drowning in daily logs. This fixes it.

I built this because my agent's MEMORY.md hit 15,000 words and daily logs kept piling up at 2,500 words/day. Needed a way to compress without losing the important stuff.

The key insight came from classical Chinese writing — ancient scholars compressed entire dynasties into single sentences. Same principle here:

1. **Strip redundancy** — mention it once, not three times
2. **Keep only turning points** — what changed, not what continued
3. **Let structure carry meaning** — bullet hierarchy > verbose paragraphs
4. **Drop the process, keep the result** — "failed 3 times, then X worked" > 3 failure descriptions

Result: **4-8x compression ratio**, zero loss on key events. Zero dependencies.

```
Before: 2,500 words of raw daily log
After:    400 words of structured insight
```

## Architecture

```
┌────────────────────────────────────────────────┐
│           THREE-LAYER MEMORY SYSTEM            │
├────────────────────────────────────────────────┤
│                                                │
│  Layer 1: IDENTITY (SOUL.md)                   │
│           Ultra-compressed, stable             │
│           Who you are. What matters.           │
│                                                │
│  Layer 2: CURATED MEMORY (MEMORY.md)     ◄──┐ │
│           4:1 compressed summaries          │ │
│           Key events + lessons + todos      │ │
│                                             │ │
│  Layer 3: RAW LOGS (memory/YYYY-MM-DD.md)   │ │
│           Full detail, everything        ───┘ │
│           ~2,500 words/day                     │
│                                                │
│  memory-compress: Layer 3 ──► Layer 2          │
└────────────────────────────────────────────────┘
```

## Quick Start

```bash
# Compress today's log
node scripts/memory-compress.js memory/2026-03-14.md

# Specify output
node scripts/memory-compress.js memory/2026-03-14.md /tmp/compressed.md

# Append to long-term memory
node scripts/memory-compress.js memory/2026-03-14.md /tmp/today.md
cat /tmp/today.md >> MEMORY.md
```

## How It Works

### Smart Hybrid Extraction

Most memory tools choke on unstructured logs. This one doesn't.

**Step 1 — Keyword Matching**: Scans headers for 40+ patterns across Chinese & English:
- Events: 重大进展, breakthrough, milestone, decision…
- Lessons: 教训, 反思, insight, takeaway…
- Growth: 进化, evolution, improvement…
- Action items: 待办, 🔴, 🟡, todo, next step…

**Step 2 — Fallback Extraction**: When no keywords match (e.g. time-based headers like `## 08:44 Standup`), automatically extracts all sections with top items. **No data loss, ever.**

**Step 3 — Hybrid Mode**: For multi-day files, matched sections use keyword extraction while unmatched sections use fallback. Both coexist. Nothing gets dropped.

### The Classical Chinese Compression Philosophy

This isn't just "summarize shorter." It's a deliberate compression methodology:

| Principle | What it means | Example |
|-----------|--------------|---------|
| 去重复 (Strip redundancy) | Mentioned once = enough | Don't repeat "WebSocket reconnection" across 3 sections |
| 留转折 (Keep turning points) | Only what *changed* | "Switched from nginx to direct Node.js WSS" > 5 paragraphs of debugging |
| 去过程 (Drop process) | Result > journey | "3 failures → fixed with X" > 3 failure descriptions |
| 留白 (Leave blanks) | Let reader infer | Bullet hierarchy implies relationship |
| 形式即内容 (Form is content) | Structure carries meaning | Nested lists > flat paragraphs |

### Output Format

```markdown
## 2026-03-14 Key Experiences

### Key Events
- **Event title**
  - Detail 1
  - Detail 2

### Core Lessons
- Lesson learned

### Pending/Remaining
- 🔴 Urgent items
- 🟡 Important items
```

## Batch Compression

```bash
# Compress last 7 days
for file in memory/2026-03-{08..14}.md; do
    [ -f "$file" ] && node scripts/memory-compress.js "$file" "/tmp/$(basename $file)"
done
```

## Heartbeat Integration

Add to your maintenance cycle:

```markdown
## Memory Maintenance (every 2-3 days)
1. Run: node scripts/memory-compress.js memory/YYYY-MM-DD.md /tmp/compressed.md
2. Review for accuracy
3. Append: cat /tmp/compressed.md >> MEMORY.md
4. Timestamp: date +%s > .last-memory-maintenance
```

## Edge Cases

| Scenario | Behavior |
|----------|----------|
| Empty file | Graceful skip |
| BOM-encoded | Auto-detected, stripped |
| Non-UTF-8 | Warning + continues |
| Missing output dir | Auto-created |
| No markdown structure | Friendly message |
| Multi-day concatenated | Hybrid strategy, all days preserved |

## CLI

```
node scripts/memory-compress.js <log-file> [output-file]
node scripts/memory-compress.js --help
```
