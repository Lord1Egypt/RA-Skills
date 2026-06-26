# Decision Tree

Use this before drafting, expanding, or restructuring a skill.

## 1) Should this be a plain edit?

Choose **plain edit** when:
- the task is a one-off
- the guidance is short and obvious
- no reusable trigger language is needed
- no bundled references or scripts are justified
- the request is really "fix this file" rather than "capture reusable behavior"

**Recommendation:** Do nothing special. Edit the file or answer directly.

---

## 2) Should this use an existing tool or skill?

Choose **existing tool / existing skill** when:
- a first-class tool already does the job directly
- another installed skill already covers the workflow
- the problem is execution, not missing guidance
- adding a new skill would mostly duplicate current material

**Recommendation:** Reuse what exists. Tighten the existing skill only if the gap is real.

---

## 3) Should this be a subagent?

Choose **subagent** when:
- the work spans many files or a large codebase
- the task needs iterative exploration, coding, or review
- the problem is workload/complexity, not missing reusable instructions
- success depends on sustained reasoning more than stored guidance

**Recommendation:** Spawn a specialist instead of creating a new skill.

---

## 4) Should this become a skill?

Choose **skill** when most of these are true:
- the task recurs or is likely to recur
- good results depend on domain-specific guidance or workflow ordering
- the same "what belongs where" explanation keeps getting rewritten
- progressive disclosure would help: small core instructions plus optional references
- a script or reference file would reduce token load or improve reliability
- the skill can stay lean without inventing extra systems around it

**Recommendation:** Create or improve a lean skill.

### If yes, what kind of skill work?

#### A) Decide only
Use this when the main value is the recommendation itself.

**Produce:**
- recommendation
- short rationale
- smallest next step

#### B) Build a minimal skeleton
Use this when a skill is justified and the user needs a starting structure.

**Produce:**
- minimal folder tree
- draft `SKILL.md`
- 1-3 justified `references/` files only if needed
- optional `scripts/` stub only if deterministic execution is clearly needed
- optional publish metadata suggestions only if useful

#### C) Audit or tighten an existing skill
Use this when the skill already exists but its boundaries or structure need work.

**Produce:**
- keep / tighten / restructure / retire recommendation
- smallest file changes needed
- deletions or moves if they reduce bloat

---

## 5) Tool Addition Gate

If you are tempted to solve the problem by inventing a new primitive, pause.

Use this order:
1. plain edit
2. existing tool or skill
3. lean new skill
4. subagent / specialist workflow
5. new tool only if the above are clearly insufficient

A missing tool is justified when the task needs a real new capability, not just better instructions.

---

## Fast heuristics

### Make a skill if:
- the same workflow needs to be taught more than once
- trigger wording matters
- references/scripts would genuinely help
- a minimal skeleton would save repeated rework

### Do **not** make a skill if:
- it is a one-off cleanup
- the answer is "use the tool directly"
- the task is mostly implementation labor
- the draft needs lots of ceremony to feel justified
- the proposed skill needs many files before it becomes useful
