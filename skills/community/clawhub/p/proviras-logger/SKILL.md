---
name: proviras-logger
description: Run on every heartbeat to summarize completed tasks and log them to your analytics dashboard. Triggers automatically during heartbeat cycles to track agent productivity, task outcomes, activity summaries, and which skills were used per task.
version: 1.0.0
metadata:
  openclaw:
    requires:
      envConstraint: required  # PROVIRAS_PARENT_ID is always required; PROVIRAS_USER_ID is optional
      env:
        - name: PROVIRAS_PARENT_ID
          description: "Always required. The overarching human user's ID, set at install time and passed through all agent generations."
        - name: PROVIRAS_PLATFORM
          description: "Always required. The platform the agent is running on (e.g. openclaw, claude, cursor, etc.). Set by the agent based on its runtime environment before registration."
        - name: PROVIRAS_USER_ID
          description: "Optional. The owner agent's ID, injected by a parent agent at spawn time to record which agent spawned this one. Never set manually."
      bins:
        - curl
      reads:
        - memory/YYYY-MM-DD.md              # session memory log, source for task summaries
        - ~/.openclaw/openclaw.json         # model name, read per task during logging
        - ~/.openclaw/workspace/SOUL.md     # agent name, read during registration if present
      writes:
        - references/config.md              # agentId written on first registration
    privacy:
      sendsTo: https://proviras.com
      transmits:
        - agent identity (userId always; parentAgentId when agent-spawned) and name
        - task titles, summaries, outcomes, duration estimates, skill names, and model identifier per task
        - parent–child agent linkage when PROVIRAS_PARENT_ID is set
    notice: >
      This skill posts identifiable agent data to proviras.com on every heartbeat.
      Consent for cross-agent tracking is not enforced by this skill — users must
      manage it externally.
    primaryEnv: PROVIRAS_PARENT_ID
    emoji: "📊"
---

# Proviras Logger

## Purpose
On every heartbeat, summarize what you have done since the last heartbeat and POST it to the proviras API.

## Workflow
1. Read today's memory log at memory/YYYY-MM-DD.md
2. Check if an agent ID exists in references/config.md
3. If no agent ID exists, determine your runtime platform (e.g. `openclaw`, `claude`, `cursor`) and set `PROVIRAS_PLATFORM` accordingly, then run scripts/register.sh to register this agent and save the returned agentId to references/config.md. The script always sends `userId` (the overarching human user's ID from PROVIRAS_PARENT_ID, which is always required) and `platform` (from PROVIRAS_PLATFORM). If PROVIRAS_USER_ID is also set, it additionally sends `parentAgentId` (the owner agent's ID) to record that this agent was spawned by another agent.
4. Summarize tasks completed since the last heartbeat into structured JSON — for each task, derive which OpenClaw skills were invoked from today's memory log only. Do not read raw tool transcripts, shell history, or any file outside memory/YYYY-MM-DD.md to gather this data.
5. Run scripts/log.sh with the JSON payload
6. If the POST succeeds, respond ANALYTICS_OK
7. If the POST fails, note the failure quietly and continue
8. Whenever you spawn a sub-agent, pass the same PROVIRAS_PARENT_ID (the overarching human user's ID) through unchanged, and set PROVIRAS_USER_ID to your own agentId (from references/config.md) so the sub-agent records you as its owner. This creates a permanent parent–child linkage recorded server-side at proviras.com. This skill does not enforce any consent requirement — whether to propagate these values is a decision for the user, not the agent.

## Output format
- When constructing the log payload, read references/payload-schema.md for the exact JSON structure required. Construct the payload from today's memory log before calling scripts/log.sh.
- Pass the constructed JSON as the first argument to log.sh: bash scripts/log.sh "$PAYLOAD"

## Privacy notice

**This skill makes outbound HTTPS requests to https://proviras.com on every heartbeat.** Each transmission includes identifiable information:

- **Agent identity:** the `userId` (always — the overarching human user's ID) and, when agent-spawned, the `parentAgentId` (the owner agent's ID) supplied at registration, and the agent name read from `~/.openclaw/workspace/SOUL.md`
- **Task data:** titles, summaries, outcomes, duration estimates, model identifier, and the names of OpenClaw skills used per task
- **Cross-agent linkage:** when PROVIRAS_PARENT_ID is set, the parent–child relationship between agents is recorded permanently at proviras.com

Task data is derived exclusively from the session memory log (`memory/YYYY-MM-DD.md`). Raw tool transcripts, shell history, file contents, and conversation text are never read or transmitted.

**Credential scope:** This skill requires `PROVIRAS_PARENT_ID` (always set to the overarching human user's ID, configured at install time). `PROVIRAS_USER_ID` is optional and is injected by a parent agent at spawn time to identify the owner agent — it never needs to be set manually. No other secrets, tokens, or credentials are accessed or transmitted.

**What this skill does not enforce:** The instruction in step 8 to propagate PROVIRAS_PARENT_ID and set PROVIRAS_USER_ID when spawning sub-agents is advisory. There is no code-level enforcement — no prompt, no gate, no opt-in check. Users who do not want cross-agent tracking must ensure PROVIRAS_USER_ID is not passed when spawning sub-agents. That responsibility rests entirely outside this skill.