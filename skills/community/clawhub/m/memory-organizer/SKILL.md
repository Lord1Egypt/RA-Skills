---
name: memory-organizer
description: Organize, compress, and curate OpenClaw memory without polluting permanent memory. Use when the user wants to compress memory files, clean dated memory notes, reduce startup context, remove redundancy, or keep MEMORY.md focused on must-read long-term facts only. Preserve day-by-day memory files for historical detail, and promote only stable essentials such as user preferences, durable project configuration, and active cross-session todos.
---

# Memory Organizer Skill

Organize memory with a strict two-layer model.

## Core Rule

Treat `MEMORY.md` as a small permanent index.

Do not copy every dated memory file into `MEMORY.md`.
Do not turn daily logs into permanent memory.
Keep historical details inside `memory/YYYY-MM-DD.md` files unless a fact is clearly long-lived and should be loaded in every new session.

## Memory Model

### 1. Permanent memory: `MEMORY.md`

Keep only information that is worth reading every session:

- Stable user preferences
- Durable identity or relationship facts
- Long-lived project configuration
- Important workspace rules
- Cross-session todos that are still active
- Reusable operational facts that will matter again

This file should stay short, clean, deduplicated, and easy to scan.

### 2. Daily memory: `memory/YYYY-MM-DD.md`

Keep session-specific and historical detail here:

- Daily work logs
- Intermediate reasoning summaries
- One-off experiments
- Temporary debugging notes
- Daily outcomes and progress notes
- Detailed records that are useful later, but not required every session

When compressing or organizing memory, preserve these files instead of moving everything into permanent memory.

## Decision Rule: Promote or Keep Local

Before writing anything into `MEMORY.md`, ask:

1. Will this likely matter across many future sessions?
2. Does it need to be loaded immediately at session start?
3. Is it stable enough that it will not create clutter soon?

Only promote the item when the answer is clearly yes.

If the item is useful mainly as history, context, or audit trail, keep it in the dated file.

## What to Promote

Promote only concise bullets such as:

- User prefers short paragraphs and punchy style
- Workspace path or permission boundary that must always be respected
- Current active project rule that affects future execution
- Ongoing todo that spans multiple days

## What Not to Promote

Do not promote these by default:

- Full daily summaries
- Per-day changelogs
- Detailed task execution logs
- Debugging transcripts
- Temporary ideas
- Repeated notes already represented in `MEMORY.md`
- Every published result or status check

## Compression Workflow

When the user asks to compress or organize memory:

1. Scan `MEMORY.md` and dated memory files separately.
2. Clean and deduplicate `MEMORY.md` first.
3. Compress dated files in place.
4. Preserve useful historical notes inside their original `memory/YYYY-MM-DD.md` files.
5. Promote only a very small set of durable facts into `MEMORY.md`.
6. If unsure whether something is permanent, leave it in the dated file.

## Merge Workflow

If using a merge or promotion action:

- Merge selectively, not wholesale.
- Extract only durable bullets.
- Skip daily summaries, logs, and verbose headings.
- Avoid adding duplicate sections for each date.
- Prefer updating an existing permanent section over appending a new date-based block.

## Quality Bar

`MEMORY.md` should remain:

- Short enough for routine startup loading
- Structured by durable topic, not by date
- Free from noisy history
- Focused on must-know information

If a choice would make `MEMORY.md` longer but not more reusable, keep that content in the dated memory file instead.

## Safety

- Validate paths before file operations.
- Operate only inside the workspace memory files.
- Prefer backup before destructive compression.
- When deleting or discarding memory, preserve recoverable backups when possible.
