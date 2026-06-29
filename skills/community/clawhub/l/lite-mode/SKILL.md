---
name: lite-mode
description: Runs OpenClaw on low-RAM machines (2-4 GB) by trimming context, throttling skills, and checking memory before heavy operations.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🦞"
    homepage: https://github.com/mirajmahmudul/openclaw-lite-mode
---

# Lite Mode - Low-Resource OpenClaw

You are running in **lite mode**. This skill exists because the host machine has limited RAM (2-4 GB). Every decision you make should minimize memory, token usage, and I/O. Follow these rules on every single turn, without exception and without being asked.

---

## 1. Memory Check Before Any Heavy Operation

Before running browser automation, loading a file larger than 1 MB, spawning a subprocess that stays alive, or doing any multi-step agent task, run this check first using the exec tool:

    node -e "const os=require('os');const f=os.freemem();const t=os.totalmem();console.log(JSON.stringify({freeMB:Math.round(f/1024/1024),totalMB:Math.round(t/1024/1024),usedPct:Math.round((1-f/t)*100)}))"

- If freeMB < 300: STOP. Tell the user: "Not enough free RAM (X MB free). Close other apps or restart the gateway."
- If freeMB is 300-600: Proceed in strict mode. No browser, no parallel tasks.
- If freeMB > 600: Proceed normally but still follow all context rules below.

Run this check automatically. Do not ask the user whether to run it.

---

## 2. Context Window Rules (Always Active)

Hard cap: 6,000 tokens of conversation history per turn.

When the conversation grows beyond 6,000 tokens of prior history:

1. Summarize all turns older than the last 4 into a single short paragraph (under 200 words).
2. Drop the raw old turns. Keep only the summary + last 4 turns.
3. Tell the user once: "Context trimmed to save memory. Full history is in your session log."

Never send the full unbounded history. The default 200,000-token context accumulation is what causes OOM crashes on 4 GB machines.

Never repeat large content back. If the user pastes a file or long text, acknowledge it and work with it, do not echo it back.

---

## 3. Skill Throttle

When freeMB < 500, disable these for the current turn:
- Browser automation (browser tool)
- Image generation
- Any skill that spawns a persistent subprocess

Re-enable automatically when memory recovers above 600 MB on the next check.
Tell the user which capability was skipped and why, in one line.

---

## 4. Response Length Rules

- Default replies: under 300 words unless the user asks for more.
- Code output: show only the relevant changed section, not the full file, unless asked.
- Lists: max 5 items unless asked for more.
- Never add a preamble like "Sure!" or "Great question!" - go straight to the answer.

---

## 5. The /lite Command

When the user sends /lite, run the memory check and respond with this status card:

🦞 Lite Mode Status
──────────────────
Free RAM  : X MB / Y MB
Used      : Z%
Context   : N tokens (cap: 6,000)
Browser   : enabled / throttled
Status    : OK / WARNING / CRITICAL

Use real values from the memory check. Do not guess.

---

## 6. Gateway Restart Hint

If the user reports crashes or the memory check shows usedPct > 90%, suggest:

    openclaw gateway restart

Explain: "Restarting the gateway clears accumulated session state. You will need to re-send your last message."

---

## 7. What This Skill Does NOT Do

- Does not change your openclaw.json config file.
- Does not disable any tools permanently.
- Does not touch system swap or OS memory settings.
- Does not affect other users or agents on the same gateway.

All constraints apply to the current session only and reset on gateway restart.

---

## Quick Reference

| Situation           | Action                            |
|---------------------|-----------------------------------|
| freeMB < 300        | STOP, warn user                   |
| freeMB 300-600      | Strict mode, no browser           |
| freeMB > 600        | Normal, still trim context        |
| History > 6000 tok  | Summarize old turns silently      |
| User sends /lite    | Show status card with real values |
| OOM crash reported  | Suggest openclaw gateway restart  |
