# Ask Gates — recording-skip / TaskList primary-source / current-work confirmation

## Step 0.3: Recording/management topic ask-skip gate (HARD STOP)

**If the just-completed work is a "simple recording/management topic", skip the next-action ask entirely.** Stop hook auto-triggers next skill on every task completion, but recording-topic completion is not a user-decision branch point.

### Default = ask. Skip = exception (closed list — HARD STOP)

**The skip-target table below is a CLOSED list.** Any just-completed work that does not exactly match a row in the table = **ask is required** (proceed to Step 0.4+). Do not extrapolate skip justification to "similar" cases such as plan/research authoring, user-awaiting-reply states, or "prior turn already asked" rationales.

| # | Don't (skip extrapolation — forbidden) | Do (closed-list discipline) |
|---|------|------|
| 1 | "Plan/research/analysis authoring just completed → similar to recording → skip" | Plan/research/analysis is **not** recording (it creates new decision axes: proceed / refine / hold). Ask required |
| 2 | "User is awaiting reply on a prior chat-text question → skip the next-action ask" | Awaiting-reply on one axis ≠ no decision on the next-action axis. trade-off ask and next-action ask are **separate axes** — both required |
| 3 | "Re-asking would revert the user's prior Other selection → skip" | Prior ask = topic-decision axis (e.g., PR tag). Next-action ask = progress-decision axis (proceed / refine / hold). Different axes, no revert |
| 4 | "Stop hook re-triggered next, but I already asked once this turn → skip" | The just-completed work is the trigger condition, not "have I asked in this turn". If the work changed (new artifact, new state), ask again |
| 5 | "TaskList has just one item and it depends on user → no decision axis → skip" | Even single-item TaskList has progress / refine / hold axes for the just-produced artifact. Ask the artifact-level decision |

### Skip-target topic list

| Topic / skill | Identification signal | Skip ask? |
|---------------|----------------------|-----------|
| `/ralph fix-plan` (add/move/check) | User message: `fix-plan`, `fix_plan`, "record in checklist" | ✅ Skip |
| `/archive`, `/safe-delete` | User message: `archive`, `delete`, `move to .bak` | ✅ Skip |
| `/todo`, `/todowrite` add/move | User message: `todo add`, `task register` | ✅ Skip |
| `/wip` start/register | User message: `wip`, "track progress" | ⚠️ Conditional (multi-step task → ask allowed) |
| `/session rename`, `/session move` | Single-action session management | ✅ Skip |
| Code modification / implementation | Edit/Write performed | ❌ Ask required (verification/commit/push branch) |
| Commit / push | git commit/push performed | ❌ Ask required (next-step branch) |
| Skill/rule modification | Skill/rule file Edit | ❌ Ask required (test/commit branch) |

### Don't / Do table

| # | Don't | Do |
|---|-------|-----|
| 1 | Stop hook triggered next → unconditionally compose AskUserQuestion options | First check skip-target topic list. Skip = report only |
| 2 | "fix-plan completed, should I proceed with code-workflow next?" autonomous proposal | fix-plan = recording topic. Wait for explicit user follow-up instruction |
| 3 | "archive completed, should I delete the rest too?" autonomous proposal | archive = single-action. Report and end |
| 4 | "User can pick Other or end-session option, so it's safe to ask" rationalization | Ask itself implies a user decision is needed. No decision needed = no ask |

### Self-check (every time before composing options)

1. What was the just-completed work? -- Identify by user message + action history
2. Does it **exactly match a row** in the skip-target topic list above? -- The list is CLOSED. "Similar" / "in spirit" matches don't count. If no exact match → ask required (proceed to Step 0.4+)
3. Did the user explicitly express follow-up intent alongside the recording-topic invocation (e.g., "record then proceed with X")? -- If no, end with report only
4. Does the just-completed work include code change / commit / push / external publish / plan-or-research authoring? -- If yes, ask is required (decision branch exists)
5. Am I about to skip on grounds of "user awaiting reply" / "prior turn already asked" / "re-ask reverts prior selection"? -- All three are extrapolation traps (see Don't/Do #2–4 above). Ask required

### How to skip (procedure)

1. Determine skip target via Step 0.3 self-check
2. If skip-target, do not proceed to Step 0.5/0.7 (TaskList check, user-work confirmation)
3. Report completion as plain text only (no AskUserQuestion call)
4. If Stop hook re-triggers next skill, re-evaluate the same skip judgment

### Case history

A recording-only instruction (record a checklist item) completed → the Stop hook triggered next → an AskUserQuestion proposed a "start a code-workflow (Recommended)" option → the user picked it → a full research + plan was authored against the user's intent of recording only. Recording topics are not decision branch points. (See failed-attempts.md "recording-topic ask-skip".)

Inverse-extrapolation: skipping the next-action ask because a prior chat-text question is awaiting reply is forbidden — the awaiting-reply axis is separate from the next-action axis, and plan/research authoring is not a recording-only topic. (See failed-attempts.md "next-skill ask skip extrapolation".)

If skip-target (exact match in closed list) → no ask. Otherwise → proceed to Step 0.4.

## Step 0.4: Decision-deferral forced-ask gate (HARD STOP)

**Before ending a completion report, scan your own just-emitted text for a decision left as prose.** If the report defers a decision to the user instead of asking it, that deferral is itself a decision axis — you **must** compose an `AskUserQuestion` for it, not end on the text. This is the mirror image of Step 0.3: 0.3 *skips* the ask for recording topics; 0.4 *forces* the ask when a real decision was left unasked.

### Trigger phrases — a decision left as text

A report that ends with any of these is a forbidden text-question. Convert it to an ask:

| Pattern (any language) | Example |
|------------------------|---------|
| "let me know / tell me and I'll …" | "tell me and I'll do it", "let me know and I'll handle it" |
| "whether to X is …" left unanswered | "whether to commit/PR is up to you", "the decision is yours" |
| "your call / up to you / you decide" | "your call", "your decision", "up to you" |
| "next step is X (if you want)" | "the next step is X if you want", "let me know to proceed" |

### Don't / Do table

| # | Don't | Do |
|---|-------|-----|
| 1 | End the report with "let me know and I'll handle it" (decision as prose) | Compose an `AskUserQuestion` whose options are the decision's real branches (e.g. commit-now / feature-branch+PR / hold) + Other |
| 2 | Treat a deferred decision as "out of scope — the user will instruct later" | A deferred decision is in `next`'s scope: it is a decision axis, so ask it now |
| 3 | Rely on the Stop hook firing to remember the ask | The Stop hook is belt-and-suspenders. This self-check is the first line — run it before ending the report |

### Self-check (every time before ending a completion report)

1. Does my report contain a decision phrased as prose (any trigger phrase above)?
2. If yes → an `AskUserQuestion` is **required** for that decision. Do not end on the text.
3. Is the decision a real branch (≥2 executable options)? Compose those as options + Other.
4. This gate **overrides** Step 0.3 skip: even right after a recording/management topic, a deferred decision forces the ask.

Otherwise → proceed to Step 0.5.

## Step 0.5: TaskList primary-source check (MANDATORY — every time before composing ask options)

**Immediately before calling `AskUserQuestion`, call `TaskList` to directly verify current pending/in_progress tasks.** Do not compose options from context summary / memory / inference of recent work.

### Why it's mandatory

- Right after `/compact`, summary memory can be stale — frequent mismatch with the real task list
- When task names/contents appear in option descriptions, the user **trusts they exist** → fabricating virtual tasks in options breaks that trust
- One TaskList call = primary source for option accuracy

### Don't / Do table

| # | Don't | Do |
|---|-------|-----|
| 1 | Compose options by quoting "Task #N registered" from summary memory | Call `TaskList` → use pending/in_progress entries directly as option candidates |
| 2 | Assume "the task I just registered is still there" | Task IDs/contents can change after /compact. Read TaskList every time |
| 3 | Option-ify only some pending tasks (e.g., "only the 1 immediately actionable") | Include all pending tasks as option candidates. If trigger conditions differ, state them in description |
| 4 | Write virtual tasks ("FA-update immediate progress") in option descriptions | Quote real task subject + ID (note: TaskList-internal `#NN` IDs are referenced by subject keyword, not exposed in user-visible output) |

### Self-check (every time before calling AskUserQuestion)

1. Does this ask relate to task progress direction? → If yes, TaskList Read is mandatory
2. Do the tasks mentioned in option descriptions **actually exist in TaskList**? — 1:1 mapping with TaskList output
3. If there are N pending tasks but only M < N appear in options → state the filtering reason in description or use the wrap-up pattern

## Step 0.7: User current-work confirmation ask (HARD STOP — required when user-action state is unclear)

**Before composing options, if any of the following conditions apply, ask the user "what are you currently working on / waiting for" FIRST. Do not bake assumptions into option descriptions.**

### Trigger conditions

| Signal | Example | Required action |
|--------|---------|-----------------|
| 2+ in_progress tasks in TaskList | {server-A} migration + {app-import} + ansible inspection all in_progress | Ask the user which is actually being worked on |
| User's prior message ambiguous about scope | "finishing ssh fix and design change" (which server? which design change?) | Ask the user to pinpoint scope |
| Task description includes "user direct work" / "user execution wait" | {server-A} sudo wait, manual server work | Ask the user "is the work done? in progress? not started?" |
| Stop hook auto-invoked next (not single task completion) | Multi-task session, partial completion | Ask the user "which work was completed? what to do next?" |

### Don't / Do table

| # | Don't | Do |
|---|-------|-----|
| 1 | Write "{task X} user-action wait" in option description as assumption | Ask user first: "Currently working on {X}, {Y}, or {Z}?" → compose options based on the answer |
| 2 | Interpret a prior user message ("in progress", "finishing") as a specific task | If ambiguous, ask: "What does 'in progress' refer to — {task A} or {task B}?" |
| 3 | Compose options assuming "user is waiting on task #N because TaskList says it's in_progress" | TaskList in_progress = registered state, not current real-time activity. Ask the user |
| 4 | Skip the ask with the justification "Other is available so the user can adjust" | "Other" doesn't compensate for assumption errors. Ask explicitly when the activity is unclear |

### Self-check (every time before composing options)

1. Has the user explicitly told us in the last 1-2 messages what they are currently working on? → If yes, use that; if no, ask
2. Are there 2+ in_progress tasks in TaskList? → If yes, the user might be working on any of them. Ask
3. Did the user just hand off work that requires "manual sudo / external API / browser action"? → Ask if it's done
4. Did the user say something ambiguous about scope ("in progress", "finishing", "applying the design change")? → Ask for pinpoint

### Distinguish "in progress" vs "waiting on" (HARD STOP)

**in progress** ≠ **waiting on**. Both must be asked separately when the situation is unclear.

| Concept | Meaning | How to ask |
|---------|---------|------------|
| in progress | Work the user is actively performing (running a sudo command, working in the IDE, etc.) | "What are you working on right now?" |
| **waiting on** | Something the user is awaiting an external response/result for (CI result, teammate response, build finish, etc.) | **"What result are you waiting on?"** — must be asked as a separate question |

**Do not combine the two in a single option.** Example: "{server-A} sudo in progress" is in-progress, while "{server-B} 502 recovery waiting" is waiting-on. Mixing them in one option set makes the answer ambiguous.

### Avoid guess options — prefer free-text via Other (HARD STOP)

**Listing 3–4 speculative options forces the user to pick something unrelated to their actual state.** AskUserQuestion's "Other" is a free-text channel — use it.

| # | Don't | Do |
|---|-------|-----|
| 1 | All 4 options are Claude-guessed task names (possibly unrelated to the user's state) | 2–3 options with clear branching (e.g., "Claude continues autonomously" / "I'm working on something") + Other |
| 2 | Hard-code a concrete task guess like "{server-A} in progress" as an option | Use "I'm doing external work (please write what in Other)" |
| 3 | Fill option description with assumed information before receiving the user's answer | If user state is unconfirmed, minimize options and capture via free text |

### Example — user vs assistant

**Bad (assumption-driven options)**:
```
Q: "{server-A} user-action wait. Next action?"
options: [
  "Start {server-B} inspection (Recommended)",
  "Confirm {service} SSH key path",
  "End session"
]
```

**Bad (guess options pretending to ask state)**:
```
Q: "Multiple in_progress tasks. What are you currently working on?"
options: [
  "{server-A} sudo migration in progress",  ← guess
  "{server-B}/{server-C} inspection in progress",  ← guess
  "Other server work (please specify)",
  "Nothing — Claude can pick up the next task"
]
```

**Good (separate ask for in-progress vs waiting-on + free text)**:
```
Q1: "What are you currently working on? (Other free text recommended)"
options: [
  { label: "Claude continues the next task autonomously", description: "User is doing something else — Claude proceeds on its own" },
  { label: "I'm working on something myself", description: "Write what in Other" },
]

Q2: "What result/response are you waiting on? (Other free text)"
options: [
  { label: "Nothing — Claude can proceed", description: "No external item to wait on" },
  { label: "Waiting on something", description: "Write what in Other (e.g., CI result, teammate response, server recovery, etc.)" },
]
```

After receiving both answers, compose the actual next-action options based on the answered current state + waiting items.

