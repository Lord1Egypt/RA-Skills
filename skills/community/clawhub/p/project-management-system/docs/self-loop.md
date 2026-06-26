# Self-Loop Guarantee Mechanism

> Solves the meta-problem: Who ensures the system itself is running? Who ensures the agent won't forget to follow rules?
> This file is the system's "immune system", ensuring the self-loop doesn't break.

---

## I. Meta-Problems and Solutions

### Problem 1: How does the agent know to read the operation manual?

**Solutions (by priority):**

1. **Skill injection (best)** — If the platform supports skill mechanism, configure trigger conditions:
   - Received task spec path → Automatically remind to read `executor.md`
   - Asked to initiate project/break down/review → Automatically remind to read `coordinator.md`

2. **Write in dispatch message (fallback)** — If no skill mechanism, write directly in dispatch message:
   ```
   Please execute the task. Spec is at [path].
   Read system/docs/executor.md (Executor Operation Manual) before executing.
   ```

3. **README.md entry guidance (final fallback)** — Anyone getting the system, read README.md to know which file to read (Quick Start section).

**Don't rely on agent "remembering" to read manual.** Triple mechanism ensures: skill auto-inject → message explicitly states → README entry guides.

### Problem 2: How does the agent know to update the check-in sheet?

**Solution: Checklists in operation manual.**

The dispatch flow in coordinator.md states:
```
Before dispatch check:
- [ ] Project check-in sheet has no conflict
Immediately after dispatch update:
- task-spec status + communication record + project check-in sheet registration
```

This is not "suggestion", it's part of the process. Agent following the manual naturally executes.

### Problem 3: How does Heartbeat know to update?

**Solution: "Heartbeat Dynamic Update" mechanism in runtime.md.**

After each phase completes, update Heartbeat content. This is written in runtime.md, part of standard process.

### Problem 4: What if something goes wrong in the middle?

**Solution: Intermediate event record table (runtime.md) + Decision guide (decision-guide.md).**

- Something happened → Check "Intermediate Event Record" table in runtime.md, know where to record
- Don't know how to decide → Check decision-guide.md, has judgment standards

### Problem 5: Who ensures the agent followed these rules?

**Solution: Triple guarantee.**

1. **Skill injection** (passive) — When agent opens project-related functions, skill automatically reminds key rules
2. **Checklists** (active) — Checklists in operation manual, agent self-checks
3. **Check scripts** (automatic) — Scripts under `tools/`, mechanically check status consistency

This is the application of constraint three-stage rocket (governance.md):
- L1: Skill injection reminder
- L2: Process rules in operation manual
- L3: Check scripts automatically intercept

## II. Dual-Layer Self-Loop

**You are the global controller.** You simultaneously monitor two levels:
- **Project Level** — What status each task is in, who is doing what, what to push forward next
- **System Level** — Whether system rules need improvement, whether constraints need upgrade, whether templates are sufficient

Not "check system when have time", but both layers always in view. Project level is high-frequency daily, system level is low-frequency but equally important.

### Project Level Loop (Every Heartbeat / Every Conversation)

```
Agent wakes up
    │
    ▼
Read Heartbeat → Know which projects to check
    │
    ▼
Cold start recovery (runtime.md) → Scan files to recover project status
    │
    ▼
Discover project pending items → Read corresponding operation manual → Execute
    │
    ├─ Dispatch task → Update task-spec + project check-in sheet + communication record
    ├─ Review task → Write review-record + update status
    ├─ Handle intermediate events → Record to corresponding location (runtime.md indicates)
    │
    ▼
Phase complete → Update Heartbeat checklist (write what to do next)
    │
    ▼
Wait for next heartbeat / conversation → (Loop)
```

### System Level Loop (Every Completed Project / Monthly)

```
Project complete
    │
    ▼
Experience precipitation (knowledge.md) → Extract lessons
    │
    ├─ Reusable rules → Upgrade to system files (governance.md extension process)
    ├─ Repeated problems → Constraint upgrade (L1→L2→L3)
    ├─ New task types → Update quality.md adaptation table
    ├─ Executor performance → Update resource-profiles.md card
    │
    ▼
System review check (governance.md) → Process smooth? Templates sufficient? Rework rate high?
    │
    ▼
Update system files → Record change log
    │
    ▼
Next project benefits → (Loop)
```

### Relationship Between Two Loops

- **Project Level** is high-frequency loop (every heartbeat), focuses on "where project progress is, what to do next"
- **System Level** is low-frequency loop (every completed project), focuses on "whether system itself needs improvement"
- Problems and lessons from project level feed into system level; improvements from system level benefit next project level

**System-level checklist items in Heartbeat:**
```markdown
## System Maintenance (Low frequency, check monthly)
- When was the last system review? More than 1 month ago?
- Any backlog in improvements.md pending improvement list?
- Any constraints need upgrade from L1 to L2/L3?
```

**Key: Both loops don't rely on memory, both driven by files.**

## III. Break Detection

### When Does Self-Loop Break?

| Break point | Symptom | Fix method |
|--------|------|----------|
| Agent didn't read operation manual | Skipped process steps | Skill reminder triggered |
| Check-in sheet not updated | Duplicate dispatch | dashboard.py checks status inconsistency |
| Heartbeat not updated | Next heartbeat doesn't know what to do | Cold start recovery process as fallback |
| Index not updated | Can't find project | Heartbeat self-check during cold start |
| Communication record not written | Recovery doesn't know who was talked to | Review checks communication record completeness |
| Intermediate event not recorded | Decision basis lost | Review discovers missing, backfill |

### Fallback Mechanism

Even if some record is missed, the system won't crash, because there are **multiple recovery paths**:

1. **task-spec status field** — Most basic recovery info, as long as status is right, can resume
2. **Project check-in sheet** — Cross-validation, know who is doing what
3. **Communication record** — Recover communication context
4. **Heartbeat** — Know what to do next
5. **Cold start recovery process** — Ultimate fallback, scan files from scratch to recover

Losing any one of these can recover through other paths. Probability of losing all is almost zero (because distributed across different files).

## IV. Timing→File Quick Reference Table

**Agent at any moment, just check this table to know what to read:**

| What I want to do now | What to read |
|---------------|--------|
| First contact with this system / Want to understand design philosophy | `philosophy.md` |
| Just woke up, don't know what to do | `runtime.md` cold start recovery process |
| Want to initiate project / break down / dispatch / review | `coordinator.md` |
| Received task spec, want to execute | `executor.md` |
| Don't know how to judge staff delivery quality | `decision-guide.md` review decision guide |
| Don't know how to write task-spec / review record | `decision-guide.md` file writing guide |
| Don't know how to communicate with certain type of executor | `communication.md` communication method matrix |
| Facing unfamiliar executor/platform | `philosophy.md` meta-capability: explore unknown system → create card to `resource-profiles.md` after exploration |
| Want to dispatch task to an executor | `resource-profiles.md` read their card (capability/preference/call method) |
| Give executor feedback after project completion | `communication.md` Feedback type → then update `resource-profiles.md` card |
| Don't know where to record intermediate events | `runtime.md` intermediate event record table |
| Task has problems don't know how to handle | `scheduling.md` exception handling and escalation |
| Project wants to pause / cancel / resume | `lifecycle.md` |
| System itself needs modification / add new module | `governance.md` system extension process |
| Want to understand why system is designed this way | `philosophy.md` design philosophy origins |
| Not sure where system might break | This file (self-loop.md)|
| System needs review / constraint needs upgrade | `governance.md` system review + constraint three-stage rocket + garbage collection |
| Need independent verifier review | `quality.md` independent verification role |
| Task status transition uncertain | `task-management.md` task state machine + guard conditions |
| Long task executing afraid of disconnection | `runtime.md` anti-disconnection three-step method |
| Need to wait a while then check | `runtime.md` timer vs Heartbeat selection guide |

**Principle: This table is agent's "master navigation". When unsure what to read, check this table first.**

## V. Scenario Retrieval List (One-time Load)

**Splitting is for management, referencing is for use.** Files are stored separately but retrieved all at once through reference chains.

Below are files that need **one-time read** for each work scenario. When entering a scenario, agent loads all needed files at once according to the list, not "checking while doing":

| Work Scenario | One-time Load | Total Size | Notes |
|----------|-----------|--------|------|
| **Break down task** | coordinator.md + task-management.md + quality.md (acceptance criteria section) | ~8KB | Dependencies, quantified standards all at hand |
| **Dispatch task** | coordinator.md (dispatch section) + resource-profiles.md (target executor card) + communication.md (Ask format) | ~6KB | Know who to dispatch to, how to say |
| **Review task** | coordinator.md (review section) + quality.md + decision-guide.md (review decision) + task-spec + output files | ~8KB+output | Judgment standards and decision guide all at hand |
| **Handle change** | coordinator.md (change section) + decision-guide.md (brief adjustment) + change-request template | ~5KB | Assess impact + write change request |
| **Urgent task** | scheduling.md (urgent channel section) + task-spec template | ~4KB | Fast track process |
| **Project complete** | coordinator.md (acceptance section) + knowledge.md + communication.md (Feedback) + resource-profiles.md | ~10KB | Experience precipitation + feedback + card update |
| **Cold start recovery** | runtime.md + data_structure.md + status.md (if exists) | ~3KB | Minimum recovery set |
| **Execute task** | executor.md + task-spec | ~5KB | Executor only needs these two |

**Key design concept: Files stored separately is for "not taking space when not needed", reference list is for "getting everything at once when needed".**

**This is not contradictory.** Splitting solves storage and maintenance problems (changing one doesn't affect others), referencing solves usage problems (get everything at once when needed). The two connect through link references.

## VI. System Guidance File Hierarchy

```
README.md                    ← System outline (entry point)
    │
    ├─ docs/philosophy.md    ← Design philosophy and meta-capabilities (system soul)
    │
    ├─ docs/coordinator.md   ← Dispatcher "how to do"
    ├─ docs/executor.md      ← Executor "how to do"
    │
    ├─ docs/runtime.md       ← "What to do after waking up"
    ├─ docs/decision-guide.md ← "How to make decisions"
    ├─ docs/communication.md  ← "How to talk to people"
    ├─ docs/self-loop.md      ← "How to ensure no break"
    │
    ├─ docs/task-management.md ← Rule details (look up as needed)
    ├─ docs/quality.md
    ├─ docs/scheduling.md
    ├─ docs/lifecycle.md
    ├─ docs/collaboration.md
    ├─ docs/knowledge.md
    └─ docs/governance.md
```

**Philosophy Layer (System Soul):** philosophy.md — Why designed this way, how to face unknown
**Entry Layer (Must Read):** README.md → Points to operation manual
**Operation Layer (Read by Role):** coordinator.md or executor.md
**Guarantee Layer (Look Up as Needed):** runtime / decision-guide / communication / self-loop
**Rule Layer (Look Up When Encountering Specific Problems):** 7 topic files

**Agent doesn't need to read all layers at once. Skill will remind which to read at appropriate time.**

## VII. Is Automation Script Needed?

**Current judgment: File mechanism sufficient, no extra scripts needed for now.**

Reasons:
1. File read/write is agent's native capability, no extra tools needed
2. Checklists embedded in operation manual, naturally covered following process
3. dashboard.py already provides status consistency check

**When to add scripts (L3 constraint upgrade):**
- Same omission appears 3 times → Write check script to automatically intercept
- For example: Agent repeatedly forgets to update check-in sheet → Write script to automatically check project check-in sheet during dispatch

This follows constraint three-stage rocket principle: Rely on documentation first, then code if not working.
