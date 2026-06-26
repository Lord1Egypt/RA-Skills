---
name: build-execution-protocol
description: Systematic protocol for working through a project build queue (NEXT_TASKS.md). Use when a project has an ordered task list and you need to pick up, execute, verify, and hand off work across sessions. Triggers automatically when NEXT_TASKS.md exists in a project directory and Ray says "work on [project]", "continue the build", or "keep going". Ensures consistent quality, verification, and session handoff regardless of which session picks up the work. Mirrors the heartbeat enforcement pattern.
---

# Build Execution Protocol

Repeatable, enforced process for executing a build queue across sessions. Same discipline as the heartbeat — mandatory checklists, verification gates, no shortcuts.

## Auto-Trigger

If a project has `NEXT_TASKS.md`, follow this protocol automatically. Ray only needs to say "work on [project]" or "keep going."

---

## Phase 0: Session Setup (MANDATORY — COMPLETE IN ORDER, NO EXCEPTIONS)

□ **0. Context Check (HARD STOP)**
- Run `session_status` FIRST
- **If context > 70%:** Wrap up, update files, request fresh session. STOP.
- **If context > 85%:** CRITICAL. Save state immediately, do NOT start new work.
- Log context % for reference

□ **1. Read Project State (BEFORE model selection — you need to see the work first)**
- Read `NEXT_TASKS.md` — find the first unchecked `[ ]` item
- Read `STATUS.md` (if exists) — understand current build state
- Read today's + yesterday's `memory/YYYY-MM-DD.md` — know what happened recently
- Skim the last session's work log for any warnings or half-finished items

□ **2. Model Selection (NOW that you've seen the tasks)**
- Review the upcoming tasks and select model based on what they need:
  - **Haiku:** Simple doc updates, formatting, config changes, trivial fixes
  - **Sonnet:** Standard coding, implementation, routine bug fixes, test writing
  - **Opus:** Architecture decisions, complex algorithms, hard debugging, security-critical work
- **If the session has a mix:** Start with Sonnet, switch to Opus for complex tasks, back to Sonnet after
- Switch model now if needed: `session_status(model="...")`

□ **3. Verify Previous Session's Work (DO THIS BEFORE NEW WORK)**
- Look at what the last session claimed to complete (from memory files / NEXT_TASKS.md checked items)
- **Actually verify it:** Run the code, check the output, read the files
- If anything was marked done but doesn't work → uncheck it, fix it first
- **This exists because sessions lie to themselves.** Trust but verify.

□ **4. Baseline Test Run (NON-NEGOTIABLE)**
- Run the full fast test suite BEFORE touching any code:
  ```bash
  python3 -m pytest -x -q --ignore=tests/integration
  ```
- **Record the count:** `N passed, 0 failed`
- **If tests are already failing:** Fix them FIRST using `test-suite-repair` skill
- **You must end the session with ≥ this test count**

□ **5. Git Checkpoint**
- If the project uses git: `git add -A && git commit -m "checkpoint: session start — N tests passing"`
- If no git: copy critical files to a backup location
- **Why:** If task 3 breaks something silently, you can diff back to this known-good state
- Create a new checkpoint after each completed task

□ **6. Check Jinx Status**
- `ssh -i ~/.ssh/lucky_to_mac luckyai@100.90.7.148 "curl -s http://localhost:3001/status"`
- If Jinx has completed results → review and verify them first (apply same verification standard)
- If Jinx is idle → good, we'll queue tasks as we go

□ **7. Plan the Session**
- Look at remaining unchecked tasks in NEXT_TASKS.md
- Pick 2-4 tasks you can realistically complete this session
- **WIP limit:** 1 task active at a time. Finish or park before starting another.
- **Size check:** If a task will take >45 min of coding, consider:
  - Breaking it into subtasks
  - Spawning a coding agent via `coding-agent` skill for the implementation
  - Queuing parts to Jinx

---

## Phase 1: Task Execution Loop

For EACH task, follow this loop without skipping steps:

### Step 1: Understand (2-5 minutes)

□ **Read the task description** in NEXT_TASKS.md
□ **Read the relevant source files** (use the quick reference table at bottom of NEXT_TASKS.md)
□ **Read the spec section** — find the actual requirement in the spec and **quote it**:
  ```
  SPEC REQUIREMENT: "The Judge worker evaluates 5-10 variants and selects 
  the best with a decision trace including confidence score." 
  — master_spec_full.txt, Section 4.2
  ```
  **Why:** This is how we avoid building the wrong thing. If you can't find a spec reference, ask Ray before implementing.
□ **Define "done"** — one sentence: "This task is done when ___"
□ **Jinx check:** "Can Jinx do this?" If it doesn't need live coding/testing → queue for Jinx, skip to next task

### Step 2: Implement

□ **Jinx split check:** Before coding, break the task into parts. Can any part run on Jinx?
  - **Lucky does:** Live coding, file system changes, testing, anything needing imports/execution
  - **Jinx does:** Writing docs from existing code, analyzing patterns, generating test data, reviewing logic, drafting boilerplate
  - **Split pattern:** Lucky writes the core logic → queues Jinx to write tests/docs/edge-case analysis for it
  - **Queue Jinx parts NOW** so they run in parallel while you code your parts
□ Write the code
□ **Stay focused** — one task only. Don't drift into adjacent work.
□ If you discover something broken, **note it in NEXT_TASKS.md as a new item** but don't fix it now unless it blocks you
□ **Check skills** — if this task type matches a skill (judge-worker-pattern, pipeline-debugging, ui-truth-mapping, etc.), read and follow that skill first

### Step 3: Test (MANDATORY)

□ Write tests for the new code (if the task warrants tests)
□ Run the full fast test suite:
  ```bash
  python3 -m pytest -x -q --ignore=tests/integration
  ```
□ **Must pass with 0 failures before proceeding**
□ **Test count must be ≥ baseline** — you cannot lose tests

### Step 4: Verify (NOT THE SAME AS "TESTS PASS" — USE OPUS)

This is the step that gets skipped. **Don't skip it.**

□ **Switch to Opus model** for verification: `session_status(model="opus")`
  - Opus catches things Sonnet misses — logic gaps, spec mismatches, subtle bugs
  - This is the quality gate. Use the strongest model here.
□ **Read back the code you wrote** — does it do what the task asked? Not "does it compile" — does it actually implement the requirement?
□ **Check the output** — call the function/endpoint/CLI and look at what it returns. Print it. Read it.
  ```python
  # Actually run it and look at the output
  result = the_thing_you_built(test_input)
  print(json.dumps(result, indent=2))
  ```
□ **Compare to spec** — re-read the spec requirement you quoted in Step 1. Does the output match?
□ **Edge cases** — empty input, null, unexpected types, boundary values
□ **If UI copy:** Read the copy. Does it make sense to a human who isn't a developer?
□ **Switch back to Sonnet** after verification (don't burn Opus tokens on the next task's implementation)

**Verification failures:**
- If gaps found → fix them before marking done (stay on Opus for the fix if it's complex)
- If can't fix quickly → mark task `[partial]` with notes on what's missing, add fix as new task

### Step 5: Checkpoint + Mark Done (ENFORCEMENT GATE — CANNOT SKIP)

□ **Git checkpoint:** `git add -A && git commit -m "done: [task description] — N tests passing"`
□ **Queue Jinx follow-up BEFORE marking done:** After EVERY completed task, ask "What can Jinx do now?"
  - Tests? Docs? Code review? Edge case analysis? Performance audit?
  - **Jinx should NEVER be idle when follow-up work exists**
  - **Actually submit the Jinx task via curl NOW — not "later"**
□ **Update NEXT_TASKS.md:** Check the box `[ ]` → `[x]`, add notes if needed
□ **RUN THE ENFORCEMENT GATE (MANDATORY — NO EXCEPTIONS):**
  ```bash
  ~/.openclaw/workspace/scripts/enforce.sh "<project_dir>" "<task_name>" "<memory_file>"
  ```
  - **If it exits non-zero: you are NOT DONE. Fix every failure before proceeding.**
  - **Do NOT mark the task done, do NOT move to the next task, do NOT pass Go.**
  - **This gate checks:** memory log exists with spec quote + verification + Jinx follow-up, tests pass, git clean, NEXT_TASKS.md updated
  - If the task revealed new work → add it to the appropriate priority section

### Step 6: Log (Structured Format)

Update `memory/YYYY-MM-DD.md` using this format:
```markdown
### Task: [name from NEXT_TASKS.md]
- **Status:** ✅ Done / ⚠️ Partial / ❌ Blocked
- **What was built:** [1-2 sentences]
- **Files changed:** [list]
- **Tests:** [before] → [after] (added N)
- **Verified:** [how — what you checked beyond tests]
- **Spec match:** [yes/no — quote spec if relevant]
- **Jinx queued:** [what follow-up work]
- **Surprises:** [anything unexpected, lessons learned]
```

Update `STATUS.md` if this was a significant milestone.
Log to Mission Control if available.

### Step 7: Skill Extraction Check

□ **Did this task produce a reusable pattern?**
  - New algorithm that could apply to other projects?
  - Debugging technique worth capturing?
  - Architecture pattern worth documenting?
□ If yes → note it in the Learning Capture section of today's memory
□ If it's substantial → create a skill (check existing skills first to avoid duplicates)

### Step 8: Context Check + Continue

□ Run `session_status` — check context usage
□ **If context > 60%:** 1-2 more tasks max. Be selective.
□ **If context > 70%:** Finish current task, go to Phase 3 (wrap-up). STOP new work.
□ **If context OK:** Move to next unchecked task, repeat from Step 1.

---

## Phase 2: Blocker Handling

When you hit a blocker:

□ **Classify:**
  - **Needs Ray:** Decision, approval, info only Ray has
  - **Technical:** Bug, missing dependency, unclear spec
  - **Dependency:** Task X depends on unfinished Task Y

□ **Handle by type:**
  - **Needs Ray:** Mark `[blocked: waiting on Ray — reason]` in NEXT_TASKS.md, message Ray, skip to next task
  - **Technical:** Attempt to solve (switch to Opus if complex). If stuck >15 min, mark blocked, move on.
  - **Dependency:** Skip to the dependency task first, or skip both and note the chain

□ **Never let one blocker stop all progress.**

□ **If ALL tasks blocked:**
  - Log blockers clearly
  - Check for supporting work (tests, docs, refactoring, skills)
  - Message Ray with the full blocker list and what you did instead

---

## Phase 3: Session Wrap-Up (MANDATORY)

□ **NEXT_TASKS.md current:**
  - All completed items checked `[x]`
  - New discovered items added
  - Blockers noted with reasons
  - **"Next session starts here"** marker on the first unchecked task

□ **Final test run:**
  ```bash
  python3 -m pytest -x -q --ignore=tests/integration
  ```
  - 0 failures confirmed
  - Test count ≥ starting baseline

□ **Final git checkpoint:**
  ```bash
  git add -A && git commit -m "session end: [N] tasks done, [M] tests passing"
  ```

□ **Structured handoff note** in `memory/YYYY-MM-DD.md`:
  ```markdown
  ## Session Wrap-Up [time]
  - **Tasks completed:** N (list them)
  - **Tests:** start count → end count
  - **Next task:** [first unchecked item]
  - **Blockers:** [list or "none"]  
  - **Warnings for next session:** [anything tricky, gotchas, or "none"]
  - **Jinx tasks queued:** [list or "none"]
  - **Context at wrap:** X%
  ```

□ **Update STATUS.md** with current test count and completion %

□ **Queue Jinx overnight work** if applicable

□ **DO NOT leave work half-done.** Finish or revert.

---

## Progress Reporting to Ray

**When to message Ray:**
- **After completing 3+ tasks in a session** — batch summary, not per-task spam
- **When hitting a blocker that needs Ray** — immediately, with specific question
- **When a milestone completes** (e.g., entire Priority section done) — celebration-worthy
- **When something unexpected happens** — broken assumptions, spec contradictions, major discoveries
- **At session wrap if significant progress was made**

**Don't message Ray for:** routine task completion, passing tests, minor progress. Save it for batches.

---

## Quality Gates (ENFORCEMENT)

A task is NOT done unless ALL of these are true:
- [ ] Code written and saved
- [ ] Tests written (if applicable)
- [ ] Full fast suite passes with 0 failures
- [ ] Output verified with Opus model (not just "tests pass")
- [ ] Spec requirement quoted and matched
- [ ] Git checkpoint committed
- [ ] NEXT_TASKS.md checkbox marked
- [ ] Jinx follow-up queued (if applicable)
- [ ] No regressions (test count ≥ baseline)

**Red Lines (Never Cross):**
- Never mark a task done without verification
- Never decrease test count
- Never start a new task with failing tests
- Never continue past 70% context without wrapping up
- Never leave NEXT_TASKS.md out of date
- Never implement without reading the spec requirement first
- Never skip verifying the previous session's work

---

## Learning Capture

After completing any task, write one line:
- **What worked** — technique, pattern, or approach worth reusing
- **What didn't** — mistake, false start, or wasted time
- **Skill candidate?** — if this pattern is reusable, note it for potential skill extraction

If it's worth keeping long-term → update MEMORY.md at end of day.
