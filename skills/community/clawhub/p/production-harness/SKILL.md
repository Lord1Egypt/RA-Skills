---
name: agent-harness
description: "Production-grade Agent Harness combining execution discipline (Superpower), knowledge compounding (CE), and product thinking (Gstack) into a single adaptive workflow. Use when: (1) building features or fixing bugs with AI agents, (2) user says 'build', 'plan', 'spec', 'review', 'ship', 'debug', (3) managing multi-step development tasks, (4) need structured engineering workflow with quality gates. Provides: task complexity auto-grading (simple/medium/complex), anti-rationalization guards, concurrent subagent scheduling, verification protocols, experience compounding, and product-level requirement validation."
---

# Agent Harness

A unified engineering harness that combines execution discipline, knowledge compounding, and product thinking. Born from 45万字 of real-world AI textbook writing + 9 production incidents.

## Core Philosophy

> Agent = Model + Harness. The model provides capability; the harness provides discipline.

Three layers, one workflow:

1. **Challenge** — Is this the right thing to build? (from Gstack)
2. **Execute** — Build it with engineering rigor (from Superpower)
3. **Compound** — Learn from what happened (from CE)

## Task Complexity Auto-Grading

Before starting any task, assess complexity. This determines which workflow steps to run.

**🟢 Simple** (bug fix, config change, small tweak)
- Skip spec/plan → Direct edit → Verify → Done
- Example: "fix the typo in line 42", "update the API endpoint"

**🟡 Medium** (new feature, module, integration)
- Plan → Build incrementally → Test → Review → Done
- Example: "add user authentication", "integrate payment API"

**🔴 Complex** (architecture change, multi-module, new system)
- Full pipeline: Challenge → Spec → Plan → Build → Test → Review → Ship
- Example: "redesign the database schema", "build a multi-agent orchestrator"

When unsure, start at 🟡. Upgrade to 🔴 if you discover hidden complexity. Never downgrade mid-task.

## Layer 1: Challenge (🔴 Complex tasks only)

Before writing any code, answer these questions. If any answer is "no" or uncertain, pause and discuss with the user.

1. **Problem validity** — Is the user solving a real problem or building a solution looking for a problem?
2. **Simplest approach** — Is there a simpler way that doesn't require building this?
3. **Scope clarity** — Can you explain what "done" looks like in one sentence?
4. **Risk assessment** — What's the worst thing that happens if this goes wrong?

Output: A one-paragraph problem statement that the user confirms before proceeding.

## Layer 2: Execute

### Spec (🟡🔴 only)

Define what you're building before you build it:
- **Goal**: One sentence describing the outcome
- **Interface**: Inputs, outputs, API contracts
- **Constraints**: What you will NOT do (equally important as what you will do)
- **Acceptance criteria**: How to verify it works (must be testable)

### Plan (🟡🔴 only)

Break the spec into atomic tasks:
- Each task modifies ≤3 files
- Each task has a clear verification step
- Tasks are ordered by dependency (independent tasks can parallelize)
- Estimate: simple tasks ~5min, medium ~15min, complex ~30min

### Build

Execute tasks incrementally. After each task:
1. Verify the task works (run it, test it, check the output)
2. Commit or checkpoint the progress
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

### Review (🟡🔴 only)

Self-review from 5 dimensions:
1. **Correctness** — Does it do what was asked?
2. **Edge cases** — What happens with empty input, huge input, concurrent access?
3. **Security** — Any injection points, leaked secrets, missing auth?
4. **Performance** — Will it work at 10x scale?
5. **Maintainability** — Will someone understand this code in 6 months?

### Ship (🔴 only)

Pre-ship checklist:
- [ ] All tests pass
- [ ] Rollback plan exists (can you undo this in <5 min?)
- [ ] Feature flag or gradual rollout if risky
- [ ] Monitoring/alerting covers the new code path

## Layer 3: Compound

After completing any task (regardless of complexity), spend 30 seconds on:

1. **What broke?** — Any errors, retries, unexpected behavior? → Record the specific lesson
2. **What was slow?** — Any step that took longer than expected? → Note the bottleneck
3. **What would you do differently?** — With hindsight, was there a better approach?

Only record **specific, actionable lessons**. Not generic advice like "be more careful".

**Good**: "Bedrock throttles at >2 concurrent requests to the same model. Use model rotation or serial execution."
**Bad**: "Remember to handle API limits properly."

## Anti-Rationalization Table

When you catch yourself thinking any of these, stop and follow the rebuttal:

| Your excuse | Why it's wrong | Do this instead |
|---|---|---|
| "Too simple to need tests" | 40% of P0 incidents come from "too simple" code | Write the test. It takes 2 minutes. |
| "I already checked, looks fine" | Reading ≠ verifying | Run it. `ls`, `wc -l`, `grep`, actual execution. |
| "I'll write tests after the feature is complete" | You won't. Test debt only grows. | Write the test NOW, before moving on. |
| "This old code looks unused, I'll delete it" | Chesterton's Fence: understand before removing | `git blame` first. Ask why it exists. |
| "It should work" | "Should" is not evidence | Provide logs, output, or data. |
| "Let me refactor this while I'm here" | Scope creep. You weren't asked to refactor. | Do only what was requested. File a separate TODO for the refactor. |
| "I'll handle errors later" | Error handling IS the feature in production | Handle errors now. Happy path without error handling is a prototype. |
| "The context is too long, I'll summarize and skip details" | Skipping details = skipping correctness | Checkpoint to file, compact context, continue with full fidelity. |

## Concurrent Subagent Scheduling

When delegating to subagents:

**Concurrency limits:**
- ≤2 subagents parallel to same API endpoint
- >2? Serialize or distribute across regions/models
- 4+ parallel = 75% failure rate (tested). Don't do it.

**Task delegation rules:**
- Task instructions must be self-contained (don't say "go read file X")
- Include content directly in the instruction, not file references
- Each subagent writes to its own independent file
- Subagents never communicate directly — everything goes through coordinator

**Failure handling:**
- Don't blindly retry. First classify: Design failure? Alignment failure? Verification failure?
- Check `sessions_history` for the actual error, don't guess
- See [references/mast-failure-taxonomy.md](references/mast-failure-taxonomy.md) for the full classification framework

## Verification Protocol

For important deliverables, use an independent verifier:

1. Verifier does NOT read the original requirements
2. Verifier only reads the output/deliverable
3. Verifier independently assesses: Is this correct? Complete? Well-formed?
4. Core principle: **"The implementer is an LLM. Verify independently. Reading is not verification. Run it."**

## Checkpoint Protocol

Protect progress against crashes:

1. **Write to file after each step** — Don't accumulate results in memory
2. **Design tasks as idempotent** — Re-running a step produces the same result
3. **Only retry the failed step** — Don't restart from scratch
4. **Progress must be observable** — `ls` shows what's done, not model memory

See [references/checkpoint-patterns.md](references/checkpoint-patterns.md) for detailed patterns.

## Quick Reference

```
🟢 Simple:  Edit → Verify → Done
🟡 Medium:  Plan → Build → Test → Review → Done
🔴 Complex: Challenge → Spec → Plan → Build → Test → Review → Ship → Compound
```
