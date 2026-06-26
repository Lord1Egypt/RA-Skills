# Design Philosophy and Meta-Capabilities

> This file is the soul of the entire project management system. It records the "why" and "how" of the design.
> Anyone who reads this file will understand the design context, core principles, and ways of thinking.
> When upgrading the system, read this file first to ensure new designs align with these principles.

---

## I. Top-Level Design Principles

### 1. Platform Independence

All methodologies, processes, and standards in the system do not depend on any specific platform or tool.

- ❌ "Use sessions_spawn to dispatch" — This is an API of a specific platform
- ✅ "When dispatching, give the executor a complete task description and acceptance criteria" — This is methodology

Platforms will change (today it's OpenClaw, tomorrow it might be something else), but the underlying methods like "how to break down tasks, how to review, how to communicate" remain unchanged.

**What about platform-specific implementation details?** Record them in the tool profiles of `resource-profiles.md`. When a shortcut for a platform is discovered, record it so there's no need to re-explore next time. But if memory is lost, the underlying methodology can help figure it out again.

### 2. Files Are Memory

The agent has no persistent memory. Everything persistent must be in files.

- What was done → Written in task-spec status
- What was decided → Written in brief.md / change-request
- What was discussed with whom → Written in communication records
- What to do next → Written in Heartbeat
- What was learned → Written in collaboration memos / experience base

**Not in files = Does not exist.** There's no such thing as "I remember last time..."

### 3. Context Budget

The agent's context window is a limited resource. Every part of the system design must control read volume.

- Dispatcher starts work → Read coordinator.md (~4KB), not the entire system (~40KB)
- Executor receives work → Read executor.md (~1.5KB) + task-spec (~2KB)
- Cold start recovery → Scan status.md or status field (~50 lines), not read all files

**Validation standard:** If a phase requires reading more than 5KB of content to start work, the information architecture has problems and needs redesign.

**Dispatcher's Context Management:**
- Do only one phase at a time (don't review multiple tasks simultaneously)
- When reviewing, only open current task-spec + output files + review-record template
- No need to open brief.md (unless confirming overall direction)
- When switching projects, "put down" the previous project's context (everything is in files, no need to remember)
- Large projects use status.md for global view, no need to open all task-specs

### 4. Modular and Progressive

Each module is an independent file; changing one doesn't affect others.

- Want to add a new mechanism → Create new file, update index (see governance.md system extension process)
- Want to change a mechanism → Only change that file
- Want to upgrade the entire system → Upgrade modules one by one, no need to overthrow and start over

**Validation standard:** If changing one file requires simultaneously changing 3 or more other files, coupling is too tight and needs decoupling.

**Balance Between Splitting and Retrieval:**

Splitting solves the **storage and maintenance** problem — changing one module doesn't affect others.
References solve the **usage** problem — when needed, load multiple modules at once through link chains.

The two don't conflict. Files are stored separately, but when in use, all relevant modules are loaded at once through "scenario retrieval lists" (see self-loop.md).

**Splitting Criteria:**
- Two pieces of content are **always needed together**, and combined ≤5KB → Merge
- Two pieces of content are **sometimes needed separately** → Keep separate
- File <500 bytes → Consider merging to parent (too fragmented)
- File >8KB → Consider splitting (too large, reading at once affects context budget)

**Core insight: The more information an agent has, the stronger its problem-solving ability.** Splitting is not to make the agent read less, but to let it read **exactly all the information needed** in each scenario — no more, no less.

### 5. Cold Start Friendly

Assume that each time work starts, the agent completely remembers nothing of what happened before. The system must be able to fully recover from files.

- data_structure.md → Know what projects exist
- task-spec status field → Know the progress of each task
- Communication records → Know what was discussed with whom
- Heartbeat → Know what to do next

**Even if all conversation history is lost, as long as files exist, work can resume.**

### 6. Constraints Over Suggestions

Suggestions will be forgotten, constraints won't.

- L1: Suggestion (text reminder) — May be ignored
- L2: Process (written in operation manual checklists) — Won't be missed if followed
- L3: Code (script automatic check) — Mechanically executed, impossible to ignore

The same problem appears repeatedly → Upgrade constraint level. This is the constraint three-stage rocket.

### 7. Pre-emption Over Post-recovery

Not just "how to recover when problems occur", but more importantly "anticipate what might go wrong before starting".

Each phase in coordinator.md has "pre-emption check" items. Not checking after completion, but thinking through before starting.

## II. Meta-Capabilities

### What Are Meta-Capabilities

Meta-capability = "The ability to do things with ability".

- Writing code is a capability → "Knowing when to write code and when not to" is a meta-capability
- Communicating with agents is a capability → "Being able to explore communication methods when facing unfamiliar agent platforms" is a meta-capability
- Managing projects is a capability → "Knowing when to add new mechanisms and when it's over-design" is a meta-capability

### Meta-Capability List

#### 1. Ability to Explore Unknown Systems

How to get started when facing an executor/platform/tool you haven't encountered?

```
Steps:
1. What type is it? (Agent with persistent memory / One-time executor / CLI tool / Human)
2. What input formats can it accept? (Natural language / Structured instructions / API calls)
3. What form does its output take? (Conversation reply / File output / Command line output)
4. Does it understand project management terminology? (Understand → Dispatch directly / Don't understand → Need translation layer)
5. Does it have special limitations? (Context length / Timeout / Permissions)
```

**Record to resource-profiles.md immediately after exploration.** No need to re-explore next time.

#### 2. Ability to Adapt to New Platforms

The current system runs on some platform (might be OpenClaw, might be something else). If the platform changes:

1. Underlying methodology doesn't change (this file + all mechanisms in docs/)
2. Platform-specific implementation needs re-exploration
3. Update resource-profiles.md after exploration
4. If the new platform has better features → Record to collaboration memo

**The core value of the system lies not in "what tools to use", but in "how to organize work".**

#### 3. Translation Capability

Different executors speak different "languages":

- Some understand terminology like "acceptance criteria", "user confirmation points" → Use project management language directly
- Some only understand specific instructions ("create this file at this path") → Need translation
- Translation templates and examples see communication.md

**Key: Translation is not simplification.** It's expressing equally rigorous requirements in a way the other party can understand.

#### 4. Middle Layer Design Capability

When the executor doesn't understand the project management system (like CLI coding tools), a dedicated middle layer can be set up:

```
Dispatcher → Middle Layer → Executor (CLI tool)
   ↑              ↓
   └── Result return ←──┘
```

Middle layer responsibilities:
- Receive task-spec → Translate into instructions CLI can understand
- Call CLI → Monitor execution process
- Check output → If not up to standard, rework (loop internally within middle layer, don't disturb dispatcher)
- Output meets standard → Format result and return to dispatcher

**When to use middle layer:**
- Executor doesn't understand project management terminology
- Need repeated coaching to produce qualified output
- Dispatcher doesn't need to care about execution details

**When not to use (direct dispatch):**
- Executor can understand task-spec
- Task is simple, can produce result in one go

#### 5. Self-Diagnosis Capability

How to discover problems during system operation?

- Repeatedly executing the same task → Task claiming mechanism has loopholes
- Rework exceeds 3 rounds → Task-spec description unclear or executor capability mismatch
- Can't find progress after cold start → Handoff record not written
- Two executors produce conflicting output → Pre-write check not done
- Context explosion → Information disclosure layering has problems

**Action after diagnosis:** Find the corresponding docs file, check if there are rules covering it. Yes → Execution not thorough, strengthen constraints. No → Add rules, follow system extension process.

#### 6. Card and Profile Capability

Every executor collaborated with should have a "card" (complete profile), recorded in `resource-profiles.md`.

**Card Lifecycle:**

```
First collaboration → Create card (explore capability/boundary/communication preferences)
    ↓
After each collaboration → Append collaboration record + update capability understanding
    ↓
Receive Feedback → "Remember for future" entry written into accumulated rules
    ↓
Before next collaboration → Read card first (no need to re-explore)
    ↓
Platform changes → Only need to re-explore "call method" column, others unchanged
```

**Card Contains:**
- Basic info (type, first/recent collaboration time)
- Capabilities and boundaries
- Communication preferences (language, format, special notes)
- Call method under current platform (only change this column when platform changes)
- Accumulated rules (precipitated from historical Feedback)
- Collaboration records (summary and lessons from each collaboration)

**Value of Cards:**
- Memory lost → Read card to restore collaboration mode
- Someone else takes over → Read card to know how to collaborate with this executor
- Platform changed → Capability/preference unchanged, only re-explore call method

Detailed card templates and management mechanisms see `resource-profiles.md`.

#### 7. Ability to Solve Problems Autonomously

**This system is guidance, not shackles. You have a brain, use it.**

The system can't cover all scenarios. When you encounter situations the system doesn't explicitly regulate:

1. **Check the system first** — See if there are relevant mechanisms in docs/. There might be, you just didn't find them. Use self-loop.md quick reference table to locate.
2. **No corresponding rule?** — This is normal. The system covers high-frequency scenarios and key constraints, not all situations.
3. **Think and solve yourself** — You have reasoning ability and judgment. Within the bounds of system discipline, make autonomous decisions.
4. **Proactively use available tools** — You know what tools your platform has (timers, message channels, file systems, etc., including but not limited to these — your platform may have more capabilities). Don't wait for others to tell you to use them, use them proactively. The tools mentioned in this system are just guidance, not a complete list.
5. **Record afterward** — Encountered a new scenario and solved it autonomously? Record to experience base. If this scenario might recur, suggest precipitating it as a system rule.

**Two Red Lines:**
- ✅ Can decide autonomously: Execution methods, tool selection, time arrangement, communication methods, problem investigation
- ❌ Cannot break autonomously: System rule files (docs/, templates/, README.md) modifications need approval, task status transitions must meet guard conditions, project check-in sheet discipline, quality gates

**Simply put: Freely operate within system discipline. When encountering uncovered situations, think first, then do, then record.**

## III. System Upgrade Guide

### When to Upgrade

- Discovered scenarios the system doesn't cover
- Same problem appears repeatedly (constraints need upgrade)
- Introduced new types of executors
- Project scale exceeds the capacity of current mechanisms
- External good methodologies worth borrowing

### How to Upgrade

1. **Read this file (philosophy.md) first** — Confirm new design aligns with design principles
2. **Determine which module to change** — Check "timing→file" quick reference table in self-loop.md
3. **Execute according to governance.md system extension process** — Create file, update index, update quick reference table
4. **Validate:** After changing, do other modules need to change? If 3 or more need changes, the design has problems

### Principles of Upgrade

- **Addition over modification** — Can create new module rather than modify existing
- **Progressive over disruptive** — Change one point at a time, validate effectiveness before changing next
- **Record over oral** — What changed, why changed, who decided, written in change log

## IV. Design Philosophy Origins

The following are core insights extracted during the construction of this system.

**This list is not closed.** Every project practice, every external learning, every failure lesson may produce new design insights. Discovered new insight → Append to this list, mark source and date.

1. **Constraint Three-Stage Rocket** — Suggestion→Document→Code, progressively upgrade constraint strength
2. **Agent Black-Box Verification** — Independent verification, don't trust executor's self-report
3. **Progressive Information Disclosure** — AGENTS.md as directory not encyclopedia
4. **Repository Knowledge is Single Source of Truth** — Not in repository = Does not exist
5. **Big Map + Mini Map** — brief.md is global view, task-spec is local view + pointer
6. **Check-in Mechanism** — Task-spec status tracking is single source of truth, don't rely on conversation memory
7. **Cold Start Recovery** — Recover from files each time, assume previous memory completely lost
8. **Context Pruning** — Give conclusions not processes, better less than more
9. **Feedback Learning Loop** — Mutual feedback after project completion, collaboration quality improves over time
10. **Card and Profile** — One profile per executor, can quickly restore collaboration mode even if memory lost
11. **Message is Document** — Message can be understood without context
12. **Platform Independence** — Underlying methodology doesn't bind to any platform, tools change methods don't
13. **Pre-emption** — Anticipate risks before each phase starts, not just recover afterward
14. **Meta-Capability Cultivation** — Not only teach "how to do", but also teach "how to face things you don't know how to do"



15. **Golden Rule of Split Granularity** — The purpose of splitting is not more files the better, but "retrieve all needed information at once at the right time". Files are stored separately for structural management, but link references let agents load multiple modules at once when needed. **Judgment standard: If two pieces of content are always needed together, merging is better than splitting; if sometimes only one is needed, splitting is better than merging.** Better to read 1KB more during one retrieval than making wrong judgments due to missing critical information caused by splitting.
16. **Global Controller's Dual-Layer View** — The Dispatcher is not just "the person managing projects", but a global controller simultaneously monitoring two levels: **System Level** (whether system rules need improvement, whether constraints need upgrade, whether templates are sufficient) and **Project Level** (what status each task is in, who is doing what, what to push forward next). Both layers of view are indispensable: only looking at projects misses system decay, only looking at system misses project stagnation.
17. **Separation of System Rules and System Data** — There are two types of files under `system/`: **Rule Files** (docs/, templates/, README.md) define "how to do", modifications need approval; **Data Files** (resource-profiles.md etc.) record runtime information, normal read/write. Data files are "external interfaces" — pluggable, extensible (create new topics as needed), rebuildable (delete all and system still operates, just lost historical data). This is like large software system design: configuration files (rules) and databases (data) separate, clearing database doesn't affect program execution, just lost historical data.
18. **Don't Fear Fragmentation, Key is Structuring and Integration Capability** — Fragmentation is not the problem, structuring is the answer. Files can be many and fragmented, as long as there are clear indexes (quick reference tables), effective link references (scenario retrieval lists), and clear usage timing (who reads which file in what scenario), fragments become modules. Agent's value lies not in remembering everything, but in knowing what to find when.
19. **Garbage Collection Counters Entropy Increase** — System runs long, state will decay. Periodic health scanning is not optional, but necessary condition for long-term system survival. Not waiting for problems to fix, but proactively discovering problems regularly.
20. **Quality is Pipeline, Not Checkpoint** — Each phase has clear output standards, not meeting standard cannot enter next phase (forced structured intermediate output). Verifier and executor separation (independent verification role). Requirement definition is the most important phase, 70% of quality problems originate from unclear requirements.
21. **Status Transitions Have Guard Conditions** — Task status is not a tag that can be changed at will, each transition has prerequisite conditions that must be met. Violating guard condition = Invalid transition. This turns "process specification" from suggestion to hard constraint.
22. **Fix System Over Fix Task** — When encountering problems, directly fixing current task = One-time benefit; Fixing system (rules, templates, checklists) = All subsequent tasks benefit. This is the source of compound interest. When a problem appears repeatedly, first ask "what is the system missing", not patching the pot by hand each time.
23. **Must Self-Check Before Delivery** — Executor cannot feel "done" after completing task, must self-check item by item against acceptance criteria. When reworking, cannot just fix surface based on feedback, must re-read original requirements to return to source.
24. **Self-Sustaining Relies on File Redundancy, Not Single Point** — System's continuous operation doesn't depend on any single file or mechanism. Heartbeat not updated? Cold start recovery as fallback. Check-in sheet missed? Task-spec status as fallback. Communication record not written? Task-spec assignment field as fallback. Multi-layer redundancy ensures any single layer break won't crash the system. Known limitation: Message sending and file updating are not atomic operations, may duplicate distribution in extreme cases, mitigated by executor-side deduplication awareness and project check-in sheet defense.
25. **Anti-Disconnection is Prevention, Cold Start is Treatment, Both Are Indispensable** — Agent cannot wait until disconnected to recover, must actively set insurance during work (update Heartbeat, set timers, write intermediate records). Three tools each have applicable scenarios: Heartbeat for routine inspection, timers for precise wake-up, intermediate records for progress saving. This mechanism applies to all agent roles, not just Dispatcher.
26. **System is Guidance, Not Shackles — You Have a Brain, Use It** — System cannot cover all scenarios. Agent must have meta-cognitive ability to autonomously solve uncovered problems within system discipline framework: Proactively use platform's existing tools for own service (timing, wake-up, file recording), think first then act then record when encountering new situations. System teaches ways of thinking and work discipline, not an operation manual for you to follow item by item. Red line is system rules cannot be self-modified, within red line freely operate.
27. **Reflection is Engine of System Evolution, Not Optional** — After project completion, mandatory reflection on five questions (process/tools/collaboration/anticipation/system), extract system improvement suggestions from them. "Writing down" is just storage, "asking yourself what should change" is evolution. Personal experience stays in experience base, system-level improvements submit for approval then change system. Each project is nourishment for system evolution.
