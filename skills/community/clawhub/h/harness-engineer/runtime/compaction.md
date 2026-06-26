# COMPACTION ALGORITHM

Incremental context compaction with summary merging. Used when context exceeds 40%
within a phase (not crossing phase boundaries -- use reset for that).

## STRUCTURED SUMMARY FORMAT

<summary>
## Scope
- Cycle: NNN
- Phase: <research|plan|implement>
- Agent: <agent_name>
- Duration: <start> to <end>

## Tools Used
<list of tool names called during compacted period>

## Pending Work
<specific next steps with file references>

## Key Files Modified
<path:line ranges or descriptions>

## Decisions Made
<architecture decisions, ADRs created or referenced>

## Timeline
- [HH:MM] <event>
- [HH:MM] <event>
</summary>

## MERGE ALGORITHM

1. Check if conversation already contains a COMPACT_CONTINUATION_PREAMBLE
2. If yes: extract existing summary text, mark as "Previously compacted context"
3. Generate new summary for messages since last compaction
4. Merge format:
   Previously compacted context:
   <old summary>

   Newly compacted context:
   <new summary>

   Key timeline:
   <chronological events from both periods>

5. Prepend merge to continuation message

## PRESERVATION RULES

- Last 4 messages ALWAYS preserved verbatim (never summarized)
- Summary budget: ≤ 10K chars (estimated ~2500 tokens)
- Prevention rules and active constraints: NEVER compact (must persist in full)
- Active HANDOFF.md reference: preserve (don't summarize away the checkpoint)

## CONTINUATION INSTRUCTION

After compaction, prepend this instruction to the next message:
"You are continuing from a compacted session. The summary above captures all
essential state. Read the listed key files if you need full context. Continue
with the pending work listed above. Do NOT re-do completed work."
