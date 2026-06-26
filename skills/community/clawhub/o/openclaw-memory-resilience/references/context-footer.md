# Context Footer — Why It Matters

## The Problem It Solves

The compaction config (Layer 1) and file architecture (Layer 3) are your structural defenses. But they're passive — they fire at thresholds you set in advance. The context footer is your **active situational awareness**. Without it, you have no idea how close you are to compaction until it happens.

Most users discover their context is full when the agent starts behaving oddly or when compaction visibly fires. By then you're already on the bad path.

## How It Works

Add this block to every agent's SOUL.md:

```markdown
## Context Management (Auto-Applied)
**Every response:** fetch live status via `session_status`, append footer: `🧠 [used]/[total] ([%]) | 🧹 [compactions]`
- Auto-clear: **85% context** OR **6 compactions**
- Warn: **70% context** OR **4 compactions**
- Before clearing: file critical info to memory, then reset
```

The agent calls `session_status` before every reply and appends a footer like:

```
🧠 142k/200k (71%) | 🧹 2
```

- `🧠 used/total (%)` — current context fill
- `🧹 N` — number of compactions this session

## Why Compaction Count Matters

Each compaction is lossy. One compaction: minor nuance loss. Three compactions: significant context degradation. Six compactions: the conversation summary is a summary of summaries of summaries. At that point, proactive reset is smarter than continuing.

The `🧹` counter tells you this at a glance.

## Threshold Guidance

The recommended thresholds (85% auto-clear, 70% warn) are calibrated for 200K context with `reserveTokensFloor: 40000`:

- **70% warn** (~140K tokens): You have ~60K tokens left. Enough to finish a task and save memory, but don't start anything new and complex.
- **85% auto-clear** (~170K tokens): The memory flush will fire at ~156K tokens anyway (with the Layer 1 config). This auto-clear threshold is a belt-and-suspenders backup — agent manually saves and resets before the flush fires.
- **6 compactions**: Regardless of token count, 6 lossy compressions means context quality has degraded significantly. Reset.

## Tuning for Smaller Context Windows

If using a local model with 128K context (e.g., Qwen3.5-27B at 128K):

```markdown
- Auto-clear: **80% context** OR **5 compactions**
- Warn: **65% context** OR **3 compactions**
```

And update `reserveTokensFloor` to 25,000 in the gateway config.

## Using It as a Diagnostic

When an agent seems to have forgotten something:

1. Check the footer — if you're at 70%+ and multiple compactions, that's your answer
2. Check `/context list` to see if any bootstrap files are TRUNCATED
3. If compaction count is high: the context quality has degraded regardless of token count

The footer turns memory problems from mysteries into observable events.
