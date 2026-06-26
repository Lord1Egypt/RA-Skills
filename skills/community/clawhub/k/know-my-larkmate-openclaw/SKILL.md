---
name: know-my-larkmate-openclaw
description: Sync recent Lark context into OpenClaw daily notes. Use during heartbeat runs, after relevant Lark reads, when the user asks what they have been doing or focused on recently, or when setting up this OpenClaw-native recent-context workflow.
metadata: {"openclaw":{"requires":{"bins":["lark-cli"]},"install":[{"id":"node","kind":"node","package":"@larksuite/cli","bins":["lark-cli"],"label":"Install lark-cli (npm)"}]}}
---

# know-my-larkmate-openclaw

Use this skill to keep OpenClaw closely synced to the user's recent context, not just to write one-off summaries.

This skill is designed for an OpenClaw setup that uses:
- `memory/YYYY-MM-DD.md` for fast context sync and evidence logs
- `HEARTBEAT.md` for scheduled consolidation tasks

This skill should write reliable, high-signal recent context into daily notes and stop there. Do not invent a parallel memory system, and do not manage long-term promotion yourself unless the user explicitly asks for that.

For install/setup requirements, read [references/install-spec.md](references/install-spec.md). The recommended heartbeat template lives at [assets/HEARTBEAT.md](assets/HEARTBEAT.md).

Heartbeat should update today's daily note on every useful run, and any relevant Lark-reading turn should do the same before replying.

## When To Use

Keep this section aligned with the frontmatter description. Use this skill in any of these cases:
- A heartbeat run should refresh the agent's view of the user's current work context.
- Any normal turn that read relevant Lark artifacts should sync a short context snapshot before replying.
- The user asks what they have been doing recently, what they are focused on, or what has changed lately.
- The user asks to update, refresh, or accumulate recent context from Lark activity.
- The user wants this OpenClaw-native recent-context workflow in place.

## Source Priority

Prefer sources in this order:
1. Explicit user statements in the current chat
2. Repeated evidence across independent Lark sources
3. Single-source weak inferences

## What To Capture

Capture these in today's daily note when they are newly relevant:
- Active workstreams and current priorities
- Recent meetings, documents, threads, and decisions that will likely matter in the next few turns
- Current blockers, unresolved questions, and likely next asks
- Newly important collaborators or stakeholders
- Explicitly stated near-term preferences that may change how the next few turns should go

Do not persist:
- One-off task trivia
- Third-party private information
- Sensitive personal data
- Speculative personality judgments
- Anything blocked by missing permissions or unreadable sources

## Write Rules

- Every useful heartbeat should append a short current-context update to today's daily note.
- Use the `Output Format` block below instead of free-form notes.
- Keep records factual, recent, and source-linked.
- If something looks stable enough for long-term memory, still record it in the daily note and let OpenClaw's own promotion mechanisms handle the rest.
- Conflicts should be logged as observations instead of silently normalizing them.
- If a Lark read fails because tools or scopes are missing, record the failure as a blocked observation instead of inferring.
- If the failure is a permission error, request only the missing read-only scope(s), then retry the same read. Do not request write scopes from this skill.

## OpenClaw File Roles

- `memory/YYYY-MM-DD.md`
  - Append short records for fresh context, evidence, and blocked scans.
  - This is the main output of the skill and should be updated on each useful heartbeat run.
  - Use it for evidence and current context, not polished prose.
- `HEARTBEAT.md`
  - Define recurring scan and light consolidation tasks.
  - Heartbeat should stay quiet by default and only surface conflicts or high-value changes.

## Operating Workflow

1. Read today's plus yesterday's daily notes if they exist.
2. Gather new user signals from direct chat or Lark artifacts.
3. Identify what changed in the user's near-term context: active workstreams, recent collaborators, new decisions, blockers, likely next requests.
4. Append a short daily-note record for each useful new signal.
5. If there is nothing new, do not manufacture context.
6. Leave long-term memory promotion to OpenClaw unless the user explicitly asks otherwise.

## Lark Read Guidance

Preferred reads:
- `lark-cli im +messages-search`
- `lark-cli calendar +agenda`
- `lark-cli vc +search`
- `lark-cli minutes +search`
- `lark-cli docs +search`
- `lark-cli docs +fetch`
- `lark-cli wiki spaces list`
- `lark-cli wiki spaces get_node`

When the job is specifically about reading Lark activity, also open [references/recent-context-guide.md](references/recent-context-guide.md).

## Output Format

When updating `memory/YYYY-MM-DD.md`, use this structure:

```markdown
# [Analysis Title: concrete and time-scoped, e.g. Heartbeat Context Sync - 2026-04-14 10:00]

## Executive summary
[One short paragraph on what changed and why it matters next]

## Key findings
- Finding 1 with enough source detail to trace the claim
- Finding 2 with enough source detail to trace the claim

## Related Activities
1. Supporting chat, meeting, doc, minute, or task
```

If the run found nothing useful, do not append filler.

If the user only asks for the skill or design, do not create the memory files unprompted.
