---
name: Learn
description: |
  This skill should be used when the user asks to
  "record what we learned", "save lessons", "knowledge capture",
  "reflect on what happened", "write down experience",
  "what did we learn", "lessons learned", "retrospective",
  "log this plan", "what were we doing", "save plan log",
  or after completing a task that involved trial and error.
version: 0.2.0
---

# Learn: Explore, Reflect, Anneal

Capture knowledge and experience from work sessions. Turn mistakes into system improvements through structured reflection and self-annealing.

## When to Use

- After completing a non-trivial task
- After encountering and fixing an error
- After discovering something unexpected
- When the user says "record this" or "what did we learn"

## The Learning Cycle

Every learning opportunity follows this cycle:

```
Explore → Attempt → Observe Result → Reflect → Record → Anneal
```

### 1. Explore: What Did We Try?

Record the actions taken, in order:

- What was the goal?
- What approach did we choose and why?
- What alternatives did we consider?

### 2. Reflect: What Happened?

Analyze results honestly:

- What worked? Why?
- What failed? What was the root cause (not the symptom)?
- What surprised us?
- What assumption turned out to be wrong?

### 3. Record: Structured Knowledge Capture

Write each lesson in this format:

```markdown
## [Topic]: [One-line summary]

**Context:** What we were doing when we learned this.
**What happened:** The specific event or error.
**Root cause:** Why it happened (not just what happened).
**Fix/Solution:** What we did to resolve it.
**Lesson:** The reusable knowledge (applicable beyond this specific case).
**Prevention:** What mechanism prevents this from happening again.
```

### 4. Anneal: Make the System Stronger

The most important step. A lesson that only lives in notes will be forgotten. Annealing means embedding the lesson into the system itself:

```
Error occurred
  → Fix the immediate problem
  → Update the tool/script that failed
  → Test the updated tool
  → Update the directive/documentation
  → System is now stronger against this class of error
```

**Annealing targets (in order of durability):**

| Target | Durability | Example |
|--------|-----------|---------|
| Code/Script | Highest | Add validation, fix the bug, add error handling |
| Automated check | High | Add to pre-push script, CI check, linter rule |
| Directive/Playbook | Medium | Update the SOP with new step or warning |
| Memory/Notes | Lowest | Save as memory for future conversations |

Always aim for the highest durability target. A lesson embedded in code cannot be forgotten.

## Do / Don't Checklist

### Do

- [ ] Record the root cause, not just the symptom
- [ ] Distinguish **fact** (verified, reproducible) from **inference** (likely but unproven) from **assumption** (believed but untested)
- [ ] Include the specific error message, file path, or command that triggered the learning
- [ ] Write lessons as reusable knowledge (applicable beyond the specific case)
- [ ] Embed prevention into tools/scripts when possible (annealing)
- [ ] Record what DIDN'T work (negative knowledge is valuable)
- [ ] Date the entry (knowledge has a shelf life)

### Don't

- [ ] Don't record obvious things everyone knows
- [ ] Don't write vague lessons ("be more careful next time")
- [ ] Don't skip the root cause analysis ("it just broke" is not a lesson)
- [ ] Don't only record successes — failures teach more
- [ ] Don't reference external files that won't be available later
- [ ] Don't mix facts with assumptions without labeling them

## The Reflection Process

When the user asks to reflect or record lessons, follow this exact process:

**Step 1: Inventory**
List everything that happened in the session — actions, errors, fixes, discoveries.

**Step 2: Classify**
For each event, ask: Is this a **fact**, **inference**, or **assumption**?

| Type | Definition | Example |
|------|-----------|---------|
| Fact | Verified by output, test, or tool | "API returns 404 when token is expired" |
| Inference | Likely based on evidence, but not directly tested | "The rate limit is probably per-IP based on the error pattern" |
| Assumption | Believed but not verified | "This endpoint probably supports pagination" |

**Step 3: Extract Lessons**
For each non-trivial event, write the structured lesson (Context → What happened → Root cause → Fix → Lesson → Prevention).

**Step 4: Anneal**
For each lesson, identify the highest-durability target and implement the prevention mechanism.

**Step 5: Verify**
Read back the recorded lessons. Ask:
- Is the root cause correct, or just a guess?
- Is the lesson specific enough to be actionable?
- Is the prevention mechanism actually implemented, or just written down?

## Self-Annealing Examples

**Weak annealing (just a note):**
> "Remember to check CI after pushing."

**Strong annealing (embedded in tooling):**
> Added `gh pr checks` call to `pre_push_check.py`. Script now blocks if CI hasn't been checked. The lesson cannot be forgotten because the tool enforces it.

**Weak annealing:**
> "Don't use `\s` in grep character classes."

**Strong annealing:**
> Added shell script linter rule that flags `\s` inside `[...]`. Also added to the shell script checklist in the directive. Two layers of prevention.

## Plan Log: Track Intent, Prevent Drift

Attention drift is real. You start with Plan A, get pulled into a side task, and forget what you originally set out to do. The Plan Log solves this.

### How It Works

Every time a plan is created or a non-trivial task begins, save a timestamped snapshot:

```
PlanLog/
├── 202604111430_apify-skills-collection.md
├── 202604111600_clawhub-distribution.md
├── 202604111730_clawhub-deep-dive.md
└── 202604111800_learn-skill-update.md
```

### Plan Log Entry Format

```markdown
# Plan: [Title]
**Created:** YYYY-MM-DD HH:mm
**Status:** in-progress | completed | paused | abandoned
**Original goal:** [What we set out to do]

## Tasks
- [x] Completed task
- [ ] Pending task
- [ ] Task that got deferred

## Outcome
[What actually happened — filled in at the end]

## Drift Log
[If attention shifted, record when and why]
- HH:mm — Shifted to X because Y
- HH:mm — Returned to original plan / Decided to continue with X instead
```

### When to Write a Plan Log Entry

- When entering plan mode or starting a multi-step task
- When the user says "let's do X" and X is non-trivial
- When you notice attention has drifted from the original goal

### When to Review the Plan Log

- At the start of a new session (read recent entries for context)
- When unsure what was supposed to happen next
- When the user asks "what were we doing?" or "what's left?"
- Before declaring a task complete (check: did we finish what we planned?)

### Attention Drift Checklist

- [ ] What was the original goal for this session?
- [ ] Are we still working toward it, or did we get pulled into something else?
- [ ] If we drifted, was it intentional (new priority) or accidental (got distracted)?
- [ ] Are there unfinished tasks from the original plan?
- [ ] Should we return to the original plan or update it?

## Where to Save Knowledge

| Knowledge type | Where to save |
|---------------|--------------|
| Technical fact (reusable) | Directive or knowledge base file |
| Project-specific context | Memory system or project notes |
| Tool bug or limitation | Comment in the tool's source code |
| Process improvement | Update the relevant SOP/playbook |
| One-time context | Don't save — it's ephemeral |

## Tips

- The best time to record is immediately after the event, while context is fresh.
- If you can't articulate the root cause, you haven't learned the lesson yet.
- A lesson without a prevention mechanism is a lesson that will repeat.
- Negative knowledge ("X doesn't work because Y") is often more valuable than positive knowledge.
- Date everything. Knowledge decays. APIs change. Tools update.
