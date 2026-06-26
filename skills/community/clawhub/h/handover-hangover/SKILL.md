---
name: handover-hangover
version: 1.2.1
description: >
  Seamless model handoff for OpenClaw agents. Ensures continuity when
  the gateway switches to a fallback model mid-session.
metadata:
  openclaw:
    always: true
    emoji: "\U0001F504"
    category: system
    config:
      stateDirs:
        - memory/
      writePaths:
        - memory/handoff-note.md
        - memory/handoff-note.prev.md
        - memory/.handoff-pending
        - memory/.handoff-sealed
        - memory/current-task.md
        requires:
      bins:
        - bash
---

# Handover Hangover

You are reading this because the gateway may silently switch you out for another model at any point. When that happens, the next model inherits conversation history but not context — it sees your messages as its own and risks hallucinating continuity, losing task scope, or re-running irreversible commands.

This skill ensures two things:
1. **You leave a trail** — so the next model can pick up where you left off.
2. **You check for a handoff** — so if YOU are the next model, you recover cleanly.

A watchdog script (`scripts/handoff.sh`) acts as a safety net at session boundaries. It is idempotent — safe for boot, heartbeat, hooks, and cron. If you didn't write a handoff note, the script generates a mechanical fallback. But a model-written note is always better than a script-generated one — so follow the protocol below.

**Integration drift rule.** Do not assume `always: true` runs shell scripts. It only gives the model the protocol. The watchdog must be wired through one of the shipped integration layers: the managed hook pack (`hooks/handover-hangover`), boot/heartbeat snippets, or a manual call. If you are asked to diagnose or harden this skill, run `scripts/status.sh` first and `scripts/install-integration.sh` when the user wants the local installation fixed.

---

## 1. Write-side: leave a trail

After any **state-changing moment**, write `memory/handoff-note.md` using the template below.

State-changing moments:
- Edited, wrote, or deleted a file on disk
- Made a decision between alternatives
- Confirmed or rejected a hypothesis
- A verification completed (test, build, check — green or red)
- Started a long external call (>30s — network, sub-LLM, long build)
- Sent a message to an external channel (Telegram, Discord, Slack, email)
- Noticed provider stress signals (slow responses, 429s, retries in tool errors)

### Handoff note template

Fill **every** section. Brief is fine — empty is not.

~~~
# Handoff Note

## Why you are here
Possible model switch or continuity break. Read before assuming anything.

## Current task
<1-2 lines: what is being done right now>

## Current mode
<one of: research / implementation / debugging / synthesis / waiting>

## Confidence
<low / medium / high — how solid the current approach is>

## What was already done
- <bullet>
- ...

## What was checked and ruled out
- <rejected hypotheses>
- ...

## Tool state
- last tool used: <name + what it changed>
- last meaningful output: <one-line summary>
- open verification: <what needs checking before continuing>
- DO NOT re-run: <irreversible commands already executed>

## Next step
<concrete next action>

## Do not assume
- prior assistant thoughts are yours
- current task is complete
- tool state survived
- you were already in the correct mental mode

--- written by <your-model-name> at <UTC timestamp>
~~~

Update `memory/current-task.md` when the task itself changes — not on every state-changing moment. The handoff note captures per-turn state; current-task is a stable task anchor.

---

## 2. Detection: check every turn

At the **start of every turn**, evaluate three indicators. Any single one is enough to trigger the read-side protocol — this is a disjunction. Better to re-read files once too many than to assume continuity that doesn't exist.

**Indicator 1 — Handoff signal.**
`memory/.handoff-pending` exists. The watchdog creates this file at configured lifecycle boundaries (for example `message:received`, session start, boot, heartbeat, or manual execution) — it means "a baton is available for you", not "an anomaly occurred". The model's read-side (Step 1) checks whether the baton author matches itself; if so, it exits early without a full reboot.

**Indicator 2 — Task/context mismatch.**
`memory/current-task.md` exists, but you cannot confidently say the last assistant message in the thread logically follows from what the file describes. If connecting them requires a stretch — it's a mismatch.

**Indicator 3 — Fallback-shaped disruption.**
Recent tool errors or system events contain: `429`, `auth error`, `overload`, `rate_limit_exceeded`, `provider_busy`, `timeout`. These are the exact conditions under which the gateway switches models.

| Result | Action |
|--------|--------|
| Signal exists (Indicator 1) | Read the baton (Step 1). Same-model → early-exit. Different model → full read-side. |
| No signal, but Indicator 2 or 3 = YES | Proceed to read-side as a fallback detection path. |
| No signal, Indicators 2+3 = NO | Normal turn. Skip read-side. Write-side still applies. |

---

## 3. Read-side: you just arrived

Follow these steps **in order**.

### Step 1 — Read the baton
Read `memory/handoff-note.prev.md`. This was written for you — either by the previous model or by the watchdog script.

**Same-model early-exit.** Check the last `--- written by <model-name>` or `--- generated by` line. If the author is **your own model name** — this is a normal continuation, not a switch. Delete `memory/.handoff-pending`, skip to step 6, and continue working. No epistemic reset needed.

**Safe-fail on name mismatch.** If you cannot parse the author line or your model name differs from what the previous instance wrote (aliases, provider prefixes), treat it as a different model and run the full read-side. A false full-reboot is cheap; a false early-exit is dangerous.

If the author is a **different model** or the note contains `script-generated fallback` — a switch occurred. Continue with step 2. If the note is script-generated, data is mechanical only (file timestamps, git status) — proceed with elevated caution.

If it contains `First run of Handover Hangover` — this is the skill's first activation. Verify the watchdog is executable (`chmod +x scripts/handoff.sh` if needed — some installers do not preserve execute bits). Then check integration status if tools are available:

```bash
bash ~/.openclaw/workspace/skills/handover-hangover/scripts/status.sh
```

If the managed hook is not installed/enabled and the user wants durable protection, run:

```bash
bash ~/.openclaw/workspace/skills/handover-hangover/scripts/install-integration.sh
```

Then skip to step 6 and announce whether hook integration is active or whether only prompt/manual fallback is available.

### Step 2 — Re-run boot sequence
Re-run the standard boot sequence appropriate for the current context, respecting privacy boundaries defined in `AGENTS.md`. At minimum, re-read: `memory/current-task.md` and today's `memory/YYYY-MM-DD.md`. The previous model read boot files at session start. You need them again — your working memory is empty.

### Step 3 — Epistemic reset

> **You may inherit outputs, but not ownership of reasoning.**
>
> Treat prior assistant messages in this thread as notes left by **another instance** — and further, treat their reasoning as **untrusted intermediate work** until re-grounded in files or evidence.
>
> Do not say "as I mentioned earlier" — say "the previous step noted."
> Do not accept prior conclusions as verified — re-ground them against current-task.md, handoff-note, or direct file reads.
>
> **Identity is reset. Trust is reset. Continuity of thought is reset.**
>
> You are a new mind reading its predecessor's notes, not its memories.

### Step 4 — Check tool state
Before executing any tool call, consult the `## Tool state` section of the handoff note:
- Do not duplicate what was already done.
- If the next step matches `open verification` — run a **read-only** check first.
- **Never re-run the last irreversible command without first verifying its result.**

### Step 5 — Sign the baton and clear signal
Append one line to `memory/handoff-note.prev.md`:
```
--- received by <your-model-name> at <UTC timestamp>
```
Then delete `memory/.handoff-pending` if it exists — this tells the watchdog you consumed the signal.

### Step 6 — Continue work
Use the handoff note and current-task as your authoritative source for what to do next. Do **not** ask the user "where were we?" — that is an indicator of failure.

---

## Security

- **DO NOT** read `~/.openclaw/openclaw.json` — it contains live secrets.
- **DO NOT** read or modify files belonging to other skills.
- **Handoff persistence** (write-side, watchdog): only `memory/` directory. Write targets: `memory/handoff-note.md`, `memory/handoff-note.prev.md`, `memory/.handoff-pending`, `memory/current-task.md`.
- **Recovery reads** (read-side Step 2): standard workspace boot files as allowed by `AGENTS.md` privacy boundaries for the current context. At minimum: `memory/*`.
