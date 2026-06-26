---
name: lobster-debugging
version: 1.0.0
description: "Systematic debugging framework. 4-phase root-cause analysis with defense-in-depth. Never guess, never patch symptoms. From Claude Code + Superpowers."
author: "Super Lobster 🦞"
tags: ["debugging", "testing", "quality", "root-cause"]
license: MIT
---

# Lobster Debugging 🦞

**Systematic root-cause debugging. No guessing. No symptom patches. Ever.**

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

## 4-Phase Process

### Phase 1: Root Cause Investigation
1. Read error messages completely (they often contain the solution)
2. Reproduce consistently (can't fix what you can't reproduce)
3. Check recent changes (git diff, recent commits)
4. Add diagnostic instrumentation at component boundaries
5. Binary search the codebase to isolate the failure point

### Phase 2: Condition-Based Waiting
- Replace `sleep(5000)` with event-based waiting
- Wait for conditions, not timeouts
- Flaky tests = unfixed bug, not "timing issue"

### Phase 3: Defense-in-Depth
- Fix the root cause
- Add a test that would have caught it
- Add a guard that prevents the class of bug
- Document why it happened

### Phase 4: Academic Verification
- Prove the fix works with a test
- Prove the fix doesn't break anything else
- Prove the fix handles edge cases
- Prove the original bug can't recur

## Red Flags — Stop and Re-Investigate

- "Just one quick fix" — there's no such thing
- Already tried multiple fixes — you don't understand the problem
- Under time pressure — rushing guarantees rework
- "Seems simple" — simple bugs have root causes too

## When to Escalate

After 2 failed fix attempts:
1. Stop. You're guessing.
2. Go back to Phase 1.
3. If still stuck, bring in a second agent with fresh context.
