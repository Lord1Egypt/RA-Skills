---
name: nervtimer
description: Set one-shot or recurring timers across channels and keep nagging every 5 minutes until the user explicitly says it is done. Uses cron for scheduling, deterministic local state for nagging lifecycle, and LLM-generated reminder text that escalates in urgency over time.
user-invocable: true
---

# NervTimer

Use this skill when the user wants OpenClaw to set a reminder timer and keep reminding until explicit completion.

This skill is designed to be published via ClawHub and installed with:

```bash
openclaw skills install nervtimer
```

## Required behavior

1. Parse user intent into structured timer data.
2. Support `one_shot` and `recurrent` schedules.
3. Extract optional reason/purpose text from user intent.
4. When due, start nagging every 5 minutes.
5. Stop nagging only when the user explicitly says done.
6. For recurring timers: done ends only the current nagging phase, not the whole recurring schedule.

## Deterministic + generative split

- Deterministic:
  - state transitions (`scheduled`, `nagging`, `done`)
  - nag interval (5 minutes)
  - escalation stage from `nag_count`
  - schedule payload construction
- Generative (LLM):
  - final reminder sentence style
  - personality adaptation
  - increasing urgency/annoyance within policy bounds

## Files in this skill

- `{baseDir}/references/intent-schema.md`
- `{baseDir}/references/escalation-policy.md`
- `{baseDir}/scripts/validate-intent.sh`
- `{baseDir}/scripts/state.sh`
- `{baseDir}/scripts/build-cron-payload.sh`

## Workflow

Execution rule:

- Always execute skill scripts via `bash <script-path> ...`.
- Do not execute scripts directly via shebang path.
- If a script call fails, immediately fall back to direct `cron` tool calls and inform the user briefly.
- Never keep "typing" without either creating the timer or returning a concrete error.

### A) Create timer

1. Build a structured intent JSON from the user message (see intent schema reference).
2. Validate it:

```bash
printf '%s' "$INTENT_JSON" | bash "{baseDir}/scripts/validate-intent.sh"
```

3. Upsert timer state:

```bash
printf '%s' "$TIMER_JSON" | bash "{baseDir}/scripts/state.sh" upsert
```

4. Build cron payload(s):

```bash
printf '%s' "$TIMER_JSON" | bash "{baseDir}/scripts/build-cron-payload.sh"
```

5. Call `cron` tool with `action=add` for each payload.

Important defaults:

- For reminder output use isolated runs (`sessionTarget: "isolated"`, `payload.kind: "agentTurn"`).
- Route delivery to current channel context unless user requests another target.

### B) Scheduled execution (nagging tick)

When a cron reminder turn runs:

1. Call:

```bash
bash "{baseDir}/scripts/state.sh" next-nag "<timer_id>"
```

2. If `should_nag=false`, do not send a reminder text.
3. If `should_nag=true`, generate one short reminder using:
   - task title
   - reason (if present)
   - `tone_stage`
   - OpenClaw personality
4. Message must become more urgent as `nag_count` increases.
5. Apply tone guardrails from escalation policy.

### C) User says done

If user explicitly confirms completion (for example "done", "erledigt", "hab ich gemacht"):

1. Resolve active timer.
2. Mark done:

```bash
bash "{baseDir}/scripts/state.sh" mark-done "<timer_id>"
```

3. For recurring timers:
   - keep recurring schedule active
   - reset nagging phase only

### D) Ambiguity rules

- If exactly one active nagging timer exists: auto-map completion.
- If multiple active nagging timers exist: ask a short disambiguation question.

### E) Fast fallback (important for reliability)

If deterministic helper scripts cannot run for any reason:

- create/update cron jobs directly with the `cron` tool in the same turn
- use the same schedule and nagging semantics
- confirm the resulting timer setup to the user
- if no schedule can be parsed confidently, ask one short clarification question

## Safety and tone constraints

- Keep reminders short (1 to 2 sentences).
- No insults, threats, or manipulative guilt language.
- "More annoyed" means stylistic urgency only, not abuse.
- Never claim the task is done unless user explicitly confirms it.

## Packaging note (ClawHub)

Keep this folder self-contained so it can be published directly:

```bash
clawhub skill publish ./nervtimer --slug nervtimer --name "NervTimer" --version 0.1.0 --tags latest
```
