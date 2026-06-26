# Self-Learning Mechanism — Mjolnir Brain

## Overview

AI agents don't truly "learn" — they don't update their weights between sessions. Mjolnir Brain bridges this gap with structured external memory that simulates learning through four mechanisms.

## Mechanism 1: Error Correction (Effectiveness: 8/10)

**How it works:**
1. Agent encounters an error
2. Records error + root cause + fix to MEMORY.md and/or strategies.json
3. Next session reads the file → never makes the same mistake

**Example:**
```
Session 5: pip install fails on NAS
→ Records: "NAS requires mirror flag -i https://mirrors.aliyun.com/"
Session 6: pip install on NAS → reads strategies.json → uses mirror → success
```

**Why it's effective:** Closed loop. Error → rule → enforcement. Zero repeat rate for recorded errors.

## Mechanism 2: Strategy Registry (Effectiveness: 7/10)

**How it works:**
- `strategies.json` maps problems to ranked solutions
- Each solution has a success rate (0.0-1.0) and attempt count
- On failure: try solutions in order of success rate
- After each attempt: update the rate via weighted average
- New problems: auto-create entries

**The math:**
```
new_rate = (old_rate × old_tries + result) / (old_tries + 1)
where result = 1.0 (success) or 0.0 (failure)
```

**Why it works:** Over time, the best solutions float to the top. Bad solutions sink. The system gets better with use.

## Mechanism 3: Write-Through Protocol (Effectiveness: 8/10)

**The problem:** AI learns things during a session but "forgets" them by next session.

**The fix:** Write everything the moment you learn it. No batching.

**Rules:**
- Learn something → write to file immediately
- Operation fails → check strategies.json, update rates
- Sub-task completes → write findings to `memory/learnings-queue.md`
- Main session reads the queue on next interaction

**Why it's effective:** Eliminates the "I'll remember it later" failure mode. Text persists; thoughts don't.

## Mechanism 4: Playbook System (Effectiveness: 6/10)

**The problem:** Repeating the same multi-step operation from scratch every time.

**The fix:** After 3+ repetitions, crystallize into a parameterized playbook.

**What it can't do:** It doesn't make execution faster (still runs the same commands). It makes *decision-making* faster — from reasoning to lookup.

## Consolidation: Turning Noise into Signal

Raw daily logs are noisy. The consolidation pipeline extracts signal:

```
Raw daily log (2-5KB of session details)
    ↓ AI summarization (not raw copy!)
Distilled entry in MEMORY.md (2-3 lines)
    ↓ If it's a rule
AGENTS.md / TOOLS.md / SOUL.md (permanent)
```

**Key principle:** Only write conclusions. "Chose A because X" ✅. Full discussion transcript ❌.

## Measuring Learning

Track these metrics to see if the system is working:

| Metric | How to Measure | Healthy Range |
|--------|---------------|---------------|
| Error repeat rate | Same error appearing twice in logs | 0% |
| Strategy coverage | % of encountered errors with strategy entries | >70% |
| MEMORY.md freshness | Days since last consolidation | <7 days |
| Playbook coverage | % of 3+ repeated operations with playbooks | >50% |

## Limitations

1. **Not real learning** — It's structured note-taking, not neural plasticity
2. **Requires discipline** — Write-through only works if the agent follows the rules
3. **No generalization** — Can't infer "all NAS devices need mirrors" from "this NAS needs a mirror"
4. **Session-boundary delay** — Knowledge written mid-session only helps next session

## Compared to Alternatives

| Approach | Pros | Cons |
|----------|------|------|
| **Mjolnir Brain** | Zero deps, reliable, auditable | No semantic search, manual tagging |
| RAG + Vector DB | Semantic search, scales | Complex setup, hallucination risk, opaque |
| Fine-tuning | True learning | Expensive, data requirements, can't undo |
| Prompt caching | Fast, no storage | Limited context, no persistence |

Mjolnir Brain optimizes for **reliability and simplicity** over sophistication. For personal assistants managing <100 files, this is the right tradeoff.
