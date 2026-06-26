# Sign-Off Routine

End-of-day shutdown sequence that consolidates knowledge, updates memory, and optionally stops the gateway.

## Table of Contents

- [Trigger Phrases](#trigger-phrases)
- [The Routine](#the-routine)
- [Configuration](#configuration)
- [Implementation](#implementation)

## Trigger Phrases

Activate when the human says:
- "goodnight"
- "sign off"
- "wrap up for the day"
- "shut down"
- "end of day"
- "call it a night"

## The Routine

Execute these steps in order:

### Step 1: Run daily consolidation

```bash
openclaw cron run <consolidation-job-id>
```

**Skip if:** consolidation already ran within the last 2 hours (check cron history).

This reviews all sessions from the day and extracts knowledge into the memory system.

### Step 2: Update today's daily note

Append any items from the current session not yet captured in `memory/YYYY-MM-DD.md`. Include:
- Summary of conversations
- Decisions made
- Action items identified
- Anything notable that happened

### Step 3: Update MEMORY.md

Add any new tacit knowledge from today:
- Lessons learned
- Status changes (completed items, new open items)
- Infrastructure changes
- People/relationship updates

Move completed items from "Open Items" to "Completed Items".

### Step 4: Check running subagents

```bash
subagents list
```

If any are running, note their status in the daily note. **Do NOT kill them** — they may be mid-task and will complete independently.

### Step 5: Report to human

Provide a brief summary:
- What was accomplished today
- What's still pending
- Any open items for tomorrow
- Status of any running subagents

Keep it concise — end of day isn't the time for novels.

### Step 6: Stop the gateway (optional)

```bash
openclaw gateway stop
```

**Important:**
- Always confirm with the human before stopping. Say something like "Ready to shut down. Goodnight ✦"
- This must be the **last action** — after this, you're offline
- The human will see the gateway go offline but won't receive a confirmation message
- Skip this step if the human says "don't shut down" or wants the agent to remain active

## Configuration

### Skip consolidation

If the consolidation cron already ran recently, step 1 can be skipped. Check:
```bash
openclaw cron history
```
Look for a successful consolidation run within the last 2 hours.

### Skip gateway stop

Some users want the agent to remain active overnight (for heartbeats, monitoring, etc.). If configured to skip gateway stop, end after step 5.

### Custom sign-off message

Personalize the closing message to match your identity. Examples:
- "Shutting down. Rest well. ✦"
- "Logged off. See you tomorrow. 🌙"
- "All wrapped up. Goodnight!"

## Implementation

To add sign-off as a standalone skill (if not using Mindkeeper's integrated version), create a minimal SKILL.md:

```yaml
---
name: sign-off
description: "End-of-day shutdown routine. Use when the human says goodnight, sign off, shut down, wrap up for the day, or similar. Runs daily consolidation, updates memory, checks pending work, and stops the gateway."
---
```

With the body containing the steps above. Mindkeeper includes this as a reference rather than a separate skill to keep the memory system self-contained.

### Adding to AGENTS.md

Alternatively, add a section to your AGENTS.md:

```markdown
## End of Day

When the human signals end of day (goodnight, sign off, etc.):
1. Run consolidation if not recently done
2. Update daily note with session summary
3. Update MEMORY.md with new knowledge
4. Check subagents status
5. Report summary
6. Stop gateway (with confirmation)
```
