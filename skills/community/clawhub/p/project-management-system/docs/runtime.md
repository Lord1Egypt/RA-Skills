# Runtime Self-sustaining Mechanism

> Ensure agent can fully continue previous work after recovering at any breakpoint.
> Core principle: **Don't rely on memory, rely on files. Each phase end leaves enough clues for next-time self (or others) to continue.**

---

## Handover Record Mechanism

Each work phase end, must leave "handover record" in corresponding file, telling next-time waking self (or person taking over):

1. **Just finished what**
2. **Current status is what**
3. **Next step should do what**
4. **Any pending problems**

### Where Handover Record is Written

No need for separate file. Handover info is distributed in existing files' standard fields:

| Phase | Handover info location | Specific field |
|-------|------------------------|----------------|
| Initiation complete | brief.md | Requirements confirmation record → Last record status |
| Breakdown complete | Each task-spec | Status field (all are "Pending") |
| Dispatch complete | task-spec + project task-registry.md | Status changed to "In Progress" + project sign-in sheet register |
| Review complete | task-spec + review-record | Status changed to "Accepted/Rework" + review conclusion |
| Rework instruction | task-spec communication log | Last record = Feedback content |
| Project complete | final-report + data_structure.md | Acceptance report + Index status update |

### Cold Start Recovery Process

**Standard recovery steps after agent wakes (whether heartbeat triggered, new conversation, or dispatched):**

**Important: Every heartbeat trigger, must go through cold start recovery.** Heartbeat tells you "which projects to watch", cold start recovery tells you "what project actual status is". Both work together: First scan files to recover real status, then process Heartbeat check items.

```
1. Read data_structure.md → Know which active projects
2. Enter project directory:
   a. Has status.md? → Read status.md recover global status (large projects)
   b. No status.md? → Read brief.md status + Scan each task-spec status field
   c. Check any "Rework" status tasks → Need re-dispatch
   d. Check any "Pending" and dependencies-ready tasks → Can dispatch
   e. Check any "Pending Review" tasks → Need review
3. Have something to do → Do
4. Nothing to do → Wait
```

**Context size:** data_structure.md (~20 lines) + Each task-spec only read first 5 lines status = **~50 lines can recover global status**

### Heartbeat Check Item Dynamic Update

Heartbeat isn't written once and never changed. Each phase complete, update check items:

**Phase 1 — Breakdown complete:**
```markdown
## auto-release project
- Three tasks pending (TASK-001/002/003)
- TASK-001 no dependencies, priority dispatch
```

**Phase 2 — TASK-001 dispatched:**
```markdown
## auto-release project
- TASK-001 In Progress (communication ID: xxx), check if complete
- TASK-002/003 waiting prerequisite
```

**Phase 3 — TASK-001 Pending Review:**
```markdown
## auto-release project
- TASK-001 Pending Review, needs review
- TASK-002 prerequisite ready, can dispatch after review pass
```

**Principle: Heartbeat only writes "what to do next", no history. History is in project files.**

**Priority for multiple projects:**
- Sort by project priority (high→medium→low)
- Same priority sorted by urgency (someone waiting > has deadline > routine)
- Urgent projects always first
- Maximum 3 check items per project
- System maintenance items last (low frequency, doesn't affect project progress)

**System maintenance item example:**
```markdown
## System Maintenance
- Last review: [date] (next: [date])
```

Detailed system-level Heartbeat rules see `governance.md`.

## Intermediate Event Recording

Various intermediate events occur during project execution (review return, change request, urgent insertion etc.). Each event has clear recording location:

| Intermediate Event | Recording Location | Format |
|--------------------|--------------------| -------|
| Review feedback (return) | task-spec communication log + review-record | Time, feedback content, items needing improvement |
| New instruction to executor | task-spec communication log | Time, instruction content, communication ID |
| Requirements change | changes/CR-XXX.md | change-request template |
| Big picture adjustment | brief.md requirements confirmation record | Add new confirmation record, mark adjustment content |
| Risk change | risk-register.md | Update risk entry |
| Executor feedback problem | task-spec communication log | Time, problem description, handling method |
| Switch executor | task-spec status tracking + communication log | Mark "switch executor", reason, new communication ID |
| Task abandon switch approach | task-spec status changed to "Abandoned" + New task-spec | Reference original task number |

**Principle: Each event recorded in place when occurs, don't retroactively fill afterward. Recording location is corresponding file's standard field, no need to create another file.**

## Index Update Checkpoint

Index (data_structure.md) must stay synchronized with actual files. These timing must check and update index:

| Timing | Check What |
|--------|------------|
| New project created | Active projects table updated |
| Project complete/pause/cancel | Project moved from active table |
| New system file created (docs/, tools/) | Directory structure updated |
| Each Heartbeat cold start | Glance index vs /path/to/projects-data/ directory consistency |

**Self-check method:** `ls /path/to/projects-data/` directory list vs data_structure.md active projects table, both should match.

### Time Budget Check

**During long tasks (>30 minutes):**

1. **At start** — In task-spec status tracking write "Started execution, expected XX complete"
2. **At halfway** — If execution time exceeds expected 50%, self-ask:
   - Is current progress meeting expectation?
   - Need to adjust expected time?
   - Need to feedback Dispatcher?
3. **At overtime** — If execution time exceeds expected 100%, must:
   - Write reason in communication log
   - Notify Dispatcher whether need extension or adjustment

**Dispatcher responsibility:**
- Write expected time when dispatching
- Exceeds expected 50% no delivery received → Proactively ask
- Exceeds expected 100% → Decide whether need adjustment or switch approach

## Breakpoint Recovery Complete Checklist

**Anytime interrupted and come back, follow this checklist to recover:**

- [ ] Read data_structure.md — Which active projects?
- [ ] Each active project: Scan task-spec status — Which are In Progress/Pending Review/Pending?
- [ ] Has "In Progress" tasks → Check communication log communication ID, can contact executor?
- [ ] Has "Pending Review" tasks → Start review
- [ ] Has "Pending" and dependencies ready → Dispatch
- [ ] Has "Rework" tasks → Check if resubmitted
- [ ] Project sign-in sheet task-registry.md → Any expired uncleaned records? Consistent with task-spec status?
- [ ] Heartbeat check items → Reflect current actual status? (Not reflecting then update)

## Anti-disconnection Mechanism During Continuous Work

_This section solves problem: Agent might disconnect anytime during long work (session timeout, context overflow, network interruption). If disconnected but didn't leave enough clues, recovery wastes lots of time or even duplicate work._

### Meta-cognition: Proactively Use Platform Capabilities for Own Service

**You know what tools you have.** Your runtime platform already told you — timers, Heartbeat, message channels, file systems etc. Listed here are just common few, **your platform might have more capabilities, don't limit to those mentioned here.** Proactively discover, proactively use.

**But "knowing have" and "proactively using" are two things.**

This is a meta-cognitive capability: **Realizing might disconnect anytime, and proactively using existing platform tools to protect work continuity.**

Specifically, need to develop three habits:

1. **Set safeguards for yourself** — Before starting long task, proactively set timer or update Heartbeat, ensure if disconnected someone wakes you
2. **Write notes for future self** — Periodically record progress in files during work, because next waking you remember nothing
3. **Proactively choose sleep strategy** — When needing wait, evaluate how long, choose appropriate wake method (timer precise wake vs Heartbeat periodic patrol)

**Don't passively wait.** Your platform gave you timers, Heartbeat, file systems these tools. **Proactively orchestrate your work rhythm.** Good usage methods discovered record to `resource-profiles.md` Section VIII.

### Three Safeguard Tools

| Tool | Feature | Applicable Scenario |
|------|---------|---------------------|
| **Heartbeat** | Framework-layer fixed interval trigger, agent can edit check content | Routine polling, project progress, system maintenance |
| **Timer (Cron)** | Agent self-set precise time trigger, one-time or repeat | "Wait 5 minutes then check result", "Tomorrow 9AM remind" |
| **Intermediate record** | Doesn't wake, but leaves clues in files for next time to continue | Progress save during long task execution |

**Heartbeat can't replace timer.** Heartbeat is "periodic patrol", timer is "precise wake". Need precise time scenarios must use timer.

**Above just common three.** Your platform might provide more tools (event listening, webhook, background tasks etc.). Don't limit to this table, proactively discover and utilize.

### Anti-disconnection Three-step Method (During Long Task Execution)

**Agent executing over 5 minutes work should proactively do anti-disconnection:**

#### First step: Set safeguard before start

Just starting a possibly long-duration work phase:

1. **Update Heartbeat** — Write what currently doing, where at, what's next
2. **If need precise wake** — Set timer (like "15 minutes later check if TASK-003 has result return")
3. **task-spec status updated** — Ensure even if disconnect now, status in file is correct

**Timer trigger message writing:** When timer triggers might already forgot context. Message must contain enough info for future self to immediately know what to do:

```
❌ "Check the task"
✅ "Timer reminder: Check auto-release project TASK-002 (path: /path/to/projects-data/auto-release\tasks\TASK-002-api-design.md) has executor reply. If yes → Review. If no → Ask through communication log's communication ID."
```

**Principle: Timer message = A mini task-spec.** Contains: What to do, where, judgment standard, next action.

#### Second step: Periodically save during work

After each key step completion:

1. **Update task-spec status tracking** — Record progress
2. **Update Heartbeat** — Update "next step" to actual next step
3. **If waiting external result** — Set timer to wake self to check

**Frequency judgment:**
- Task estimated 5-15 minutes → Save once at start and end
- Task estimated 15-60 minutes → Save once each key step
- Task estimated over 1 hour → Segment by milestone, save each segment end

#### Third step: Proactively sleep when waiting

When needing wait for external result (executor complete, API return, human confirm):

1. **Evaluate wait time** — Roughly how long?
2. **Choose tool:**
   - Wait < 5 minutes → Don't sleep, poll or continue other work
   - Wait 5-30 minutes → Set timer, precise wake
   - Wait 30+ minutes → Write to Heartbeat, wait next heartbeat check
   - Wait uncertain duration → Heartbeat + timer dual safeguard
3. **Before sleep ensure:**
   - Heartbeat content reflects current status
   - task-spec status updated
   - Project sign-in sheet updated

### Heartbeat Interval Self-adaptation (Decision Guide)

Different project phases have different needs for check frequency. If framework supports adjusting Heartbeat interval:

| Project Phase | Suggested Interval | Reason |
|---------------|-------------------|--------|
| Just dispatched task, waiting execution | 15-30 minutes | Need timely discover completion or problem |
| All tasks In Progress, no blocking | 30-60 minutes | Routine patrol suffices |
| Has tasks Pending Review | ASAP | Review is pipeline bottleneck |
| Waiting Decision Maker confirmation | 60+ minutes | Human response time uncertain |
| No active projects | Longest interval | Only need system maintenance check |

**If framework doesn't support dynamic interval adjustment:** Use timer supplement. Heartbeat keeps fixed interval for routine patrol, urgent ones use timer precise wake.

### Applies to All Roles

**This mechanism isn't just for Dispatcher.** Every agent role should:

1. **Executor** — Periodically write intermediate records during long tasks (executor.md already has suggestion); When waiting input set timer remind self to follow up
2. **Dispatcher** — Set timer to check when waiting executor result; Multi-project parallel set different frequency checks by priority
3. **Independent verifier** — Notify immediately after verifying, no need anti-disconnection (one-time task)
4. **Any agent** — First thing after assigned work: Ensure "wake self" mechanism is active

### Relationship with Existing Mechanisms

```
Anti-disconnection three-step method → Solves "suddenly disconnected during work what to do"
    ↓
Intermediate record + Heartbeat + Timer → Three safeguard tools
    ↓
Cold start recovery → Solves "after disconnected how to continue"
    ↓
Breakpoint recovery checklist → Specific steps to continue
```

**Anti-disconnection is "prevention", cold start recovery is "treatment". Both indispensable.**