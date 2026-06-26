# System Governance Mechanism

> Constraint escalation, rule codification, template versioning, system review, sandbox environment, Heartbeat self-loop.

---

## Three-Level Constraint Rocket

Some rules are written in documents but not followed, same issues repeat.

**Three levels:**

| Level | Form | Execution method | Example |
|-------|------|-----------------|---------|
| L1 Recommendation | Text in persona/work files | Relies on executor self-discipline | "Try to quantify acceptance criteria" |
| L2 Documentation | System process rules / skill reminders | Injected as reminders on load | "Must have review record before review" |
| L3 Code | Check scripts under `tools/` | Mechanical execution, auto-block | dashboard.py checks status inconsistency |

**Escalation rules:**
- Same issue first time → Verbal reminder (L1)
- Appears again → Write into process rules (L2)
- Third time → Write check script to auto-block (L3)

**Principle: When you repeatedly correct the same issue in reviews, don't fix the task, fix the rule.**

## System Change Approval

**`system/` directory contains two types of files with different permissions:**

### System Rule Files (Modification Requires Approval)

Files that define "how the system works." Changing them means changing the rules.

- All files under `docs/` (processes, principles, operation manuals)
- All templates under `templates/`
- `README.md` (system entry and changelog)
- `data_structure.md` (system index)
- Scripts under `tools/`

**Change process:**
1. Discover need for improvement → Write into `improvements.md` (pending improvements list, system data file, normal read/write. Contains issue, suggestion, impact analysis, source)
2. Decision Maker fully hears analysis and verification then decides:
   - ✅ Approve → Execute modification + record changelog + submit Git snapshot (`python tools/system-check.py --commit "change description"`)
   - ❌ Reject → Record reason, close
   - 🔄 Need more info → Supplement and re-review
3. Only exception: Obvious text errors (typos, formatting) can be fixed directly, but must be recorded

### System Data Files (Normal Read/Write)

"External interfaces" that record runtime information. Naturally produced and updated data during system operation.

**Preset data files:**
- `resource-profiles.md` — Executor cards, collaboration records, accumulated rules
- `task-registry.md` — Task sign-in sheet description (sign-in sheet belongs to project directory)
- `improvements.md` — Pending improvements list (system improvement suggestion collection)

**Extensibility:** Data files are not limited to the above two. Dispatcher can create new data files under `system/` as needed to record new topics of runtime information. For example:
- Recording commonly used environment configurations → Create `environments.md`
- Recording cross-project tech stack preferences → Create `tech-preferences.md`
- Recording common errors and solutions → Create `troubleshooting.md`

**Creation rules:**
1. Mark file header with `> System data file — normal read/write, no approval needed` to distinguish
2. Update `data_structure.md` index
3. Briefly record in changelog (no approval needed, but leave a trace)

**Rebuildability:** All data files are "experience accumulation" not "system skeleton." Even if all deleted, system rule files remain intact, system continues operating. Next run will naturally recreate empty data files:
- First task dispatch → Discover project sign-in sheet doesn't exist → Create new one per format
- First collaboration with new executor → Discover card doesn't exist → Create new one per template
- What's lost is only historical experience, not operational capability

**This is the essence of "external interface": pluggable, extensible, rebuildable.**

## System Rule Codification (Enhanced)

Knowledge codification after project completion, adding three system-level check items:

1. **Reusable rules → Upgrade to system**
   - Good rules discovered in project worth becoming system-level processes? → Write new process mechanism
2. **Repeated issues → Escalate constraint level**
   - Is current constraint level sufficient? → Escalate per three-level constraint rocket
3. **New task types → Update adaptation table**
   - Involved task types not in `quality.md` adaptation table? → Supplement

**System evolution chain:**
```
Project practice → Discover issues/good rules → Codify into system → Next project benefits → Continuous improvement
```

## System Extension Process

When needing to add new functionality to the system (new modules, templates, tools), follow this process:

### Adding New docs Module

1. Create new file under `docs/`, name it `topic-name.md`
2. Write positioning and purpose at file header (one sentence)
3. Update README.md index table (Section 4 "Need to check detailed rules")
4. Update data_structure.md directory structure
5. Update self-loop.md "timing→file" quick reference table (add "when to read this file")
6. Update self-loop.md guide file hierarchy diagram
7. Record in README.md changelog

### Adding New Template

1. Create new template under `templates/`
2. Update README.md template list (Section 5)
3. Update data_structure.md
4. Update places in coordinator.md or executor.md that reference templates (if any)
5. Record in README.md changelog

### Adding New Tool Script

1. Create script under `tools/`
2. Update data_structure.md
3. Document purpose and usage in corresponding docs file
4. Record in README.md changelog

### Modifying Existing Modules

1. Directly modify corresponding docs file
2. Check if other files reference this module's content → Update synchronously if needed
3. Record in README.md changelog

### Checklist (Self-check after extension)

- [ ] Is the new file referenced by at least one other file?
- [ ] Is README.md index table updated?
- [ ] Is data_structure.md directory structure updated?
- [ ] Is self-loop.md quick reference table updated?
- [ ] Is changelog recorded?
- [ ] Is there impact on in-progress projects? Yes → Notify related executors (use communication.md Share type)

### System Upgrade and In-Progress Projects

- **Adding new mechanisms (addition)** → Generally doesn't affect in-progress projects, new projects automatically use
- **Modifying existing mechanisms** → Check if affects tasks currently executing
  - No impact → Silent upgrade
  - Has impact → Notify related Dispatchers and Executors, explain changes
- **Template changes** → Only affect tasks created after change, old tasks unaffected
- **Old tasks need adaptation to new template** → Treat as change request

## Template Version Compatibility

- Template changes don't affect already-issued tasks — Check against version at creation time
- New fields only take effect for tasks created after change
- Major changes noted in changelog as "not backward compatible"
- Old tasks need adaptation to new template → Treat as change request

## System Review

After every 3-5 projects completed, or once a month (whichever comes first), conduct system review:

- Is the process smooth? Where did it get stuck?
- Are templates sufficient? Which fields are never filled?
- How's review quality? High rework rate?
- Is resource allocation reasonable?
- Is improvements.md pending improvements list backlogged?

Review results update to `improvements.md` pending improvements list and README.md changelog.

## Garbage Collection Mechanism (Combating Entropy)

_Source: OpenAI Harness Engineering — "Periodically running agent, finding document inconsistencies or architecture constraint violations"_

Projects run long enough, state decays: sign-in sheets have stale entries, task-spec status doesn't match reality, index omissions, outdated cards.

**Garbage collection = periodic health scan.** Not waiting for problems to fix, but proactively discovering issues regularly.

### Scan Checklist

| Check item | Check method | Frequency |
|-----------|--------------|-----------|
| Project sign-in sheet has stale uncleaned entries | Entries in each project's task-registry.md marked "In Progress" over 7 days | Every system-level Heartbeat |
| task-spec status matches project sign-in sheet | Cross-compare | Every system-level Heartbeat + spot check on every cold-start recovery |
| data_structure.md index matches actual files | Scan directory vs index | Monthly |
| Template files complete (not accidentally deleted/corrupted) | Check files count and headers under templates/ | Monthly |
| system/ rule files integrity | `python tools/system-check.py` (based on Git comparison) | Every system-level Heartbeat |
| Cards with "last collaboration time" over 3 months | Mark as "needs update" or "needs cleanup" | Monthly |
| Document cross-reference validity | Do `reference.md` files under docs/ point to existing files, do section titles match | Monthly |
| Are completed projects under /path/to/projects-data/ archived | Check projects with completed status still in /path/to/projects-data/ | Monthly |
| Are there residual entries from completed projects in Heartbeat | Read Heartbeat compare with project status | Every system-level Heartbeat |

### Execution Method

- **L1 (starting):** Write in system-level Heartbeat, Dispatcher manually checks on every heartbeat
- **L2 (mature):** Use dashboard.py or similar script to auto-scan, output report
- **L3 (complete):** Auto-fix simple issues (like cleaning stale sign-in sheet entries), generate fix recommendations for complex issues

### Scan Result Handling

- Discover inconsistency → Fix (data files fix directly, rule files need approval)
- Discover systemic issue (same inconsistency type repeats) → Escalate constraint level
- Record to `/path/to/projects-data/lessons\garbage-collection-log.md` (system data file, normal write)

## Sandbox Environment Utilization

Sandbox is an available execution environment, use flexibly based on task nature:

| Scenario | Description |
|----------|-------------|
| Build in sandbox | Development, testing, experimental tasks, move outputs out after completion |
| Sandbox as deliverable | Web apps, services, etc., sandbox itself is runtime environment |
| Sandbox verification | Verify feasibility in sandbox first, then execute formally |

Tasks requiring local file system access must execute on host.

## Heartbeat Self-Loop Mechanism

_Note: Applies to agent frameworks supporting heartbeat mechanism. For environments not supporting heartbeat, Dispatcher manually checks periodically._

### Project-Level Heartbeat (High Frequency)

After project starts, lead writes project check tasks in heartbeat config, using heartbeat to auto-resume.

**Process:**
1. Project starts → Write project check entry
2. Each heartbeat → Check project status
3. Has pending items → Auto-progress (dispatch, review, check progress)
4. Project completes → Delete check entry

**Advantages:**
- Doesn't rely on persistent session, auto-resumes after disconnection
- Project files are memory
- Auto-cleans up after completion

**Important: Update check content as project progresses, don't write and leave unchanged.**

### System-Level Heartbeat (Low Frequency)

Besides project checks, Heartbeat should also include system-level periodic checks:

```markdown
## System Maintenance (check once a month)
- Last system review: [date] (over 1 month? → Do review, process see "System Review" section in this file)
- Is improvements.md pending improvements list backlogged?
- Any constraints need upgrading from L1 to L2/L3? (Review recent projects' review feedback)
- Do resource-profiles.md cards need updating?
- Garbage collection scan (see "Garbage Collection Mechanism" scan checklist in this file)
```

**Trigger condition:** Every 3-5 projects completed, or last review over 1 month.
**Review process see "System Review" section in this file.**

### Two-Layer Heartbeat Writing

```markdown
## [Project Name A] (High Priority)
- TASK-003 In Progress, check if completed
- TASK-004 Pending, depends on TASK-003

## [Project Name B] (Medium Priority)
- All tasks pending, prioritize TASK-001

## System Maintenance
- Last review: YYYY-MM-DD (Next: YYYY-MM-DD)
```