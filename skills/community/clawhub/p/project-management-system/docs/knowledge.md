# Knowledge and Information Management

> Knowledge codification, knowledge as repository, progressive information disclosure.

---

## Knowledge Codification

After project completion, lessons learned must be extracted and archived.

**Storage locations (all within /path/to/projects/):**

| Experience type | Storage location | Description |
|-----------------|-----------------|-------------|
| Single project experience | `/path/to/projects-data/[project-name]\final-report.md` | Within project, follows project |
| Cross-project general experience | `/path/to/projects-data/lessons\[topic].md` | Lessons applicable to multiple projects |
| Executor collaboration experience | `system/resource-profiles.md` (cards) | System data file, normal update |
| System rule improvement suggestions | `system/improvements.md` pending list | Suggestions normally written, changing rule files requires Decision Maker approval |
| Reusable scripts/tools | `/path/to/projects-data/shared-tools\` | Only enters `system/tools/` after approval |

**Core rules:**
- Recording experience is normal operation — cards, lessons, final-report can be written anytime
- Experience **becoming system rules** requires approval — changing docs/, templates/ needs Decision Maker decision
- All content is within `/path/to/projects/` internally, doesn't involve external systems

**Codification process:**
1. At project acceptance, review the entire process
2. Extract lessons learned, write into final-report
3. Has cross-project general value → Write into `/path/to/projects-data/lessons\[topic].md`
4. Collaboration experience → Update resource-profiles.md cards (accumulated rules, collaboration records)
5. Discover system rules can be improved → Write into `improvements.md` pending list (include specific suggestions and rationale)
6. After Decision Maker approval → Update system rule files

## Reflection and Extraction Process

> Knowledge codification solves "writing it down", reflection and extraction solves "digging out system improvements from experience."
> This is the core engine of system self-evolution.

### When to Reflect

- After every project acceptance (mandatory, embedded in final-report process)
- During system review (period defined by governance.md)
- When encountering major incidents or repeatedly occurring issues (anytime)

### Five Reflection Questions (Structured Self-Questioning Checklist)

After completing a project (or handling an incident), forcibly ask yourself these five questions:

**1. Process issues:** Was there any step that got stuck, took detours, or was skipped?
   - Stuck → Is system guidance sufficient for this scenario? Missing guide or guide unclear?
   - Detours → Was it insufficient information or judgment error? Insufficient information means information disclosure mechanism has gaps
   - Skipped → Was it reasonable simplification or laziness? If laziness, are constraints strong enough?

**2. Tool issues:** Was there a tool you wanted to use but didn't know how, or discovered a better usage?
   - Didn't know how to use → Card/environment experience records need updating
   - Discovered better usage → Record in resource-profiles.md Section 8 (experience records)

**3. Collaboration issues:** Did executor have difficulty understanding task specification? Rework count exceeded expectations?
   - Difficulty understanding → task-spec template missing fields? Communication protocol missing message types?
   - Rework over 2 rounds → Acceptance criteria not clear enough? Or executor capability mismatch?

**4. Anticipation issues:** Was there anything that in hindsight could have been anticipated?
   - Risk not identified → Is risk register mechanism sufficient?
   - Dependency missed → Is breakdown phase checklist sufficient?

**5. System issues:** If doing the same type of project again, what would the system need to change to do better?
   - This is the key question — not "I'll pay attention next time", but "what does the system change so anyone doesn't make the mistake next time"

### From Answers to Improvement Suggestions

After reflecting on five questions, categorize the answers:

| Answer type | Handling method | Approval |
|-------------|-----------------|----------|
| Personal experience ("I learned...") | Write into final-report or lessons/ | Not needed |
| Card update ("This executor is good at/not good at...") | Update resource-profiles.md | Not needed |
| Environment experience ("This tool has a pitfall...") | Update resource-profiles.md Section 8 | Not needed |
| **System improvement suggestion** ("Template should add a field", "Checklist missed an item") | Write improvement suggestion, submit to Decision Maker | **Needed** |

### How to Write Improvement Suggestions

```markdown
### Improvement Suggestion #[number]

- **Source project:** [project name]
- **Problem discovered:** [specific description]
- **Impact scope:** [only affects this project type / affects all projects]
- **Suggested change:** [which file's which part to change, how to change]
- **Rationale:** [why this change prevents problem from recurring]
- **Risks:** [will this change affect other mechanisms]
```

### Where Improvement Suggestions Go

1. Write into `improvements.md` (pending improvements list)
2. After Decision Maker approval → Execute change → Update changelog
3. Decision Maker doesn't approve → Record reason, keep in list for future reference

### Relationship with Existing Mechanisms

```
Project completion → final-report (record experience)
              ↓
         Five reflection questions (dig out improvement points)
              ↓
         ├─ Personal experience → lessons/
         ├─ Collaboration experience → cards
         ├─ Environment experience → Section 8
         └─ System improvement → improvements.md → Decision Maker approval → Change system
              ↓
         System review batch-reviews improvements.md
```

## Knowledge as Repository

**Principle: If it's not in the project directory, it doesn't exist for the next person taking over.**

- All decisions affecting project direction must be recorded in project directory
- Consensus reached in chat/messages → Record in task-spec communication log or brief.md
- Verbally negotiated solutions → Write into relevant documents

**Check timing:**
- Every milestone review, check if key decisions are recorded
- At project handover, confirm new person in charge can fully take over by only reading project directory

## Progressive Information Disclosure

**Problem:** Stuffing all project information to executor at once → Context bloat → Can't grasp key points.

**Rules:**
- **brief.md is big picture** — Project-wide (objectives, scope, roles, risks), executor optionally reads
- **task-spec is small picture** — Only contains information needed for that task + pointers
- Executor only needs to read their task-spec to start work
- Information not needed doesn't go into task-spec

**task-spec's "Information Pointers" field:**

```markdown
## Related Context (On-Demand Reference)

| Topic | Location | When needed |
|-------|----------|-------------|
| Project overall objectives | brief.md | When needing to understand big direction |
| Predecessor task output | tasks/TASK-001-xxx.md output | When needing to use predecessor output |
| Technical approach discussion | brief.md requirements confirmation record | When unsure about tech choices |
```

**Principle: Give executors pointers to "where to find", not copy everything over.**

## Context Trimming Principles

When passing information to anyone (writing task-spec, sending messages, writing review feedback), follow these trimming principles:

1. **Only give what's relevant** — Give what they need for current work, don't give "by the way, just for your information" information
2. **Give conclusions not process** — "Use Node >= 18" not "We tried 16, didn't work, then upgraded to 18, hit compatibility issues, finally..."
3. **Proactively mention known pitfalls** — This is the core value of Dispatcher saving executor time
4. **Sanitize sensitive information** — Use placeholders for API keys, don't expose internal paths to external executors
5. **Less is more** — Information overload is worse than insufficient information. Executors will proactively ask about missing information, but won't proactively filter excess information

**Anti-patterns:**
- ❌ Copy entire brief.md into task-spec
- ❌ Recap specification text in dispatch message
- ❌ Send project management terminology to CLI tools (they don't understand "acceptance criteria", "user confirmation points")

## Trace Analysis Method

> When task fails or has over 3 rework rounds, don't just rely on memory to reflect. Should find breakpoints based on actual execution trace.

### When to Do Trace Analysis

- Task failed (final status is "Abandoned" or severe rework)
- Over 3 rework rounds
- Same error keeps appearing

### Trace Analysis Steps

1. **Read communication log** — Communication log table in task-spec, see where it got stuck
2. **Read status tracking** — Status tracking table in task-spec, see if status changes were reasonable
3. **Read session log** (if exists) — See what agent actually did, not just what it said it did
4. **Find breakpoints:**
   - Signal not seen (in document but agent didn't read/notice)
   - Tool not used correctly (better tool exists but didn't know/didn't use)
   - Specification missing (key information not written in)
   - Acceptance criteria vague (understanding ambiguity led to wrong direction)
5. **Codify improvement:**
   - Write into improvements.md
   - If systemic issue, update docs/ or templates/

### Trace Analysis Table (Fill into final-report failure review)

| Step | Expected behavior | Actual behavior | Breakpoint |
|------|-------------------|-----------------|------------|
| | | | _Where error/stuck_ |

**Key questions:**
- Which step got stuck?
- What signal wasn't seen?
- What tool wasn't used correctly?
- What was missing from specification?

### Core Principle

> Fix the harness, not patch once.

- Fix code directly = one-time benefit
- Fix harness (rules/templates/checklists) = all subsequent tasks benefit

## Feedback Learning Loop

After project completion, Dispatcher sends Feedback message to Executor (see communication.md), including "remember for future" items.

**Recipient handling rules:**
- Executor receiving "remember for future" → Write into their own work file or experience library
- Dispatcher → Update collaboration notes for corresponding executor in `resource-profiles.md`
- This forms a cross-project learning loop: both parties get a little smarter after each collaboration