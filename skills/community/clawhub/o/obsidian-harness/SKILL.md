---
name: agent-harness
description: "Production-grade Agent Harness combining execution discipline, knowledge compounding, and product thinking into a single adaptive workflow. Use when: (1) building features or fixing bugs with AI agents, (2) user says 'build', 'plan', 'spec', 'review', 'ship', 'debug', (3) managing multi-step or multi-agent tasks, (4) need structured engineering workflow with quality gates. Provides: task complexity auto-grading (simple/medium/complex), anti-rationalization guards, concurrent subagent scheduling (≤4 hard limit), tool-chain continuity enforcement, context budget management, verification protocols, and experience compounding. Triggers: 'agent harness', 'engineering workflow', 'build protocol', 'multi-agent task', 'coding discipline', 'subagent orchestration'."
version: 2.0.1
---

# Agent Harness

A unified engineering harness combining execution discipline, knowledge compounding, and product thinking. Born from ~450k characters of real-world AI textbook writing + 15+ production incidents.

> **GAIA benchmark shows scaffold design = 30pp+ performance boost** — same model, HAL scaffold 74.6% vs bare model ~44%. The harness is the multiplier.

## Core Philosophy

> Agent = Model + Harness. The model provides capability; the harness provides discipline.

Three layers, one workflow:

1. **Challenge** — Is this the right thing to build?
2. **Execute** — Build it with engineering rigor
3. **Compound** — Learn from what happened

## Task Complexity Auto-Grading

Before starting any task, assess complexity. This determines which workflow steps to run.

**🟢 Simple** (bug fix, config change, small tweak)
- Skip spec/plan → Direct edit → Verify → Done

**🟡 Medium** (new feature, module, integration)
- Plan → Build incrementally → Test → Review → Done

**🔴 Complex** (architecture change, multi-module, new system)
- Full pipeline: Challenge → Spec → Plan → Build → Test → Review → Ship

When unsure, start at 🟡. Upgrade to 🔴 if you discover hidden complexity. Never downgrade mid-task.

## Layer 1: Challenge (🔴 Complex tasks only)

Before writing any code, answer these questions:

1. **Problem validity** — Is the user solving a real problem?
2. **Simplest approach** — Is there a simpler way?
3. **Scope clarity** — Can you explain "done" in one sentence?
4. **Risk assessment** — What's the worst outcome if this goes wrong?

Output: A one-paragraph problem statement the user confirms before proceeding.

## Layer 2: Execute

### Spec (🟡🔴 only)

- **Goal**: One sentence describing the outcome
- **Interface**: Inputs, outputs, API contracts
- **Constraints**: What you will NOT do
- **Acceptance criteria**: How to verify it works (must be testable)

### Plan (🟡🔴 only)

Break the spec into atomic tasks:
- Each task modifies ≤3 files
- Each task has a clear verification step
- Tasks ordered by dependency (independent tasks can parallelize)

### Build

Execute tasks incrementally. After each task:
1. Verify the task works (run it, test it, check the output)
2. Checkpoint progress to file
3. Only then move to the next task

**Critical rules:**
- Never modify code you haven't read first
- Don't add features beyond what was asked
- Don't refactor "while you're at it"
- If tests fail, report honestly — don't claim success

### Verify

Every deliverable must have **evidence**, not just "looks good":

| Deliverable type | Required evidence |
|---|---|
| Code change | Tests pass (show output) |
| Config change | Restart + verify (show status) |
| File generation | `wc -l` + `grep` key content |
| API integration | Show actual response |
| Documentation | Spot-check 3 claims for accuracy |

🔴 **Reading is not verification. Run it.**

### Review (🟡🔴 only)

Self-review from 5 dimensions:
1. **Correctness** — Does it do what was asked?
2. **Edge cases** — Empty input, huge input, concurrent access?
3. **Security** — Injection points, leaked secrets, missing auth?
4. **Performance** — Will it work at 10x scale?
5. **Maintainability** — Will someone understand this in 6 months?

### Ship (🔴 only)

Pre-ship checklist:
- [ ] All tests pass
- [ ] Rollback plan exists (undo in <5 min?)
- [ ] Feature flag or gradual rollout if risky
- [ ] Monitoring covers the new code path

## Layer 3: Compound

After completing any task, spend 30 seconds on:

1. **What broke?** — Errors, retries, unexpected behavior? → Record the specific lesson
2. **What was slow?** — Bottlenecks? → Note them
3. **What would you do differently?** — Better approach with hindsight?

Only record **specific, actionable lessons**. Not generic advice.

**Good**: "Bedrock throttles at >4 concurrent requests. Use model rotation or serial execution."
**Bad**: "Remember to handle API limits properly."

## Anti-Rationalization Table

| Your excuse | Why it's wrong | Do this instead |
|---|---|---|
| "Too simple to need tests" | 40% of P0 incidents come from "too simple" code | Write the test. It takes 2 minutes. |
| "I already checked, looks fine" | Reading ≠ verifying | Run it. `ls`, `wc -l`, `grep`, actual execution. |
| "I'll write tests after the feature" | You won't. Test debt only grows. | Write the test NOW. |
| "This old code looks unused, I'll delete it" | Chesterton's Fence: understand before removing | `git blame` first. Ask why it exists. |
| "It should work" | "Should" is not evidence | Provide logs, output, or data. |
| "Let me refactor while I'm here" | Scope creep. | File a separate TODO for the refactor. |
| "I'll handle errors later" | Error handling IS the feature in production | Handle errors now. |
| "The context is too long, I'll skip details" | Skipping details = skipping correctness | Checkpoint to file, compact context, continue with full fidelity. |
| "I already ran it once, it should still work" | Stateful systems change. | Run it again. Every time. |

## Concurrent Subagent Scheduling

**Hard limits:**
- ≤4 subagents parallel (hard limit; check `subagents list` before spawning)
- System hard ceiling: 8
- 5+? Re-slice into sequential batches first
- Always check current count before spawning: `subagents(action=list)`

**Task delegation rules:**
- Instructions must be self-contained (paste content directly, don't reference files)
- Each subagent writes to its own independent output file
- Subagents never communicate directly — everything goes through coordinator
- Use `sessions_yield` after spawning, not a poll loop

**After yield returns — mandatory checks:**
1. `subagents(action=list)` — confirm all spawned subagents ended
2. `ls` output files — verify files exist with expected mtimes
3. If any subagent missing or no output file → investigate, don't assume success

> Why: OpenClaw subagent completion announce has a known race condition. Never rely on announce as the sole signal. Active verification is the backup system.

**Failure classification (before retrying):**
- Design failure? → Fix the spec first
- Alignment failure? → Clarify the instruction
- Verification failure? → The work was done but not confirmed
- See [references/mast-failure-taxonomy.md](references/mast-failure-taxonomy.md) for full taxonomy

## Tool-Chain Continuity (🔴 Critical)

Every tool call return must be followed by one of:
- Next tool call
- Progress message to user
- `sessions_yield`

**Never**: respond with "I'll continue..." and then have no tool call.

Pre-tool-return self-check:
- [ ] Task complete? No → what's the next tool call?
- [ ] Waiting for external input? → Send message explaining + yield
- [ ] "Thinking about next step"? → Danger signal. Pick an action NOW.

## Context Budget Management

| Water level | Mode | Action |
|---|---|---|
| < 70% | 🟢 Normal | Full mode, observation masking always on |
| 70–85% | 🟡 Auto-Concise | No new large files, tool output truncated, subagent instructions <1500 chars |
| 85–95% | 🟠 Preservation | No files >100 lines, force checkpoint to memory, delegate reads to subagent |
| > 95% | 🔴 Emergency | Flush state, alert user to /reset, stop accepting new tasks |

**Observation Masking** (apply immediately after consuming any tool output):
- After reading a file and extracting conclusions: don't re-quote the raw content
- After exec output: keep only key lines
- After subagent delivery: extract deliverable + quality verdict, discard process noise

## Critical Safety Rules

🔫 **Never restart your own process from inside an agent turn.**
- ❌ `systemctl restart <service>`, `pkill <process>`, `gateway restart` in cron prompts
- ✅ Use the platform's safe restart tool (e.g., `gateway` tool's `restart` action)
- Why: Agent terminal runs inside the gateway process. Restarting the service = SIGKILL yourself.

🔫🔫 **Never put restart commands in cron job prompts.**
- once job + agent turn + restart = suicide loop: cron fires → agent runs → restart kills agent → turn never completes → scheduler sees incomplete once job → re-fires on next boot → infinite loop
- Restart/self-check logic must live in an external wrapper (systemd ExecStartPost= or standalone systemd-run unit), completely outside the agent process.

## Verification Protocol

For important deliverables, use an independent verifier:

1. Verifier does NOT read the original requirements
2. Verifier only reads the output/deliverable
3. Verifier independently assesses: correct? complete? well-formed?
4. Core principle: **"The implementer is an LLM. Reading is not verification. Run it."**

## Checkpoint Protocol

Protect progress against crashes:

1. **Write to file after each step** — Don't accumulate results in memory
2. **Design tasks as idempotent** — Re-running produces the same result
3. **Only retry the failed step** — Don't restart from scratch
4. **Progress must be observable** — `ls` shows what's done, not model memory

See [references/checkpoint-patterns.md](references/checkpoint-patterns.md) for detailed patterns.

## Known Tool Pitfalls

- **`\n` literal in exec/write content**: In some platforms, multiline scripts passed as strings get `\n` treated as literal characters, not newlines. Always use real line breaks. Verify with `read` after writing.
- **Concurrent writes**: Multiple subagents writing to the same file = corruption. Each subagent must have its own output file.
- **Reading ≠ Verifying**: `grep` and `wc -l` are faster than `read` for verification. Use them.

## Quick Reference

```
🟢 Simple:  Edit → Verify → Done
🟡 Medium:  Plan → Build → Test → Review → Done
🔴 Complex: Challenge → Spec → Plan → Build → Test → Review → Ship → Compound
```

After every tool call: next action or yield. Never stall.
