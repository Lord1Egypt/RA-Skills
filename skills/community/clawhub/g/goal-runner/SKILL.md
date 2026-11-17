---
name: goal-runner
description: Autonomous multi-task orchestration loop over a roadmap file (ROADMAP.md, TODO.md, or any checkbox task list) — pairs with the built-in /goal Stop hook to work tasks ONE at a time until the file is done. The main agent orchestrates only; every task is delegated to sub-agents for coding, code review, and regression testing, with observed-green gates before the checkbox is ticked. No commits or pushes unless the goal text explicitly authorizes them — when it does, one commit per verified task, never red. Blocked tasks are annotated and skipped, never faked. Use this skill whenever the user says "work on the roadmap tasks til completion", "work the roadmap until completion", "work on tasks until completion using sub agents", "launch sub agents to work the tasks", "/goal-runner", or sets a /goal naming a roadmap/task file — even if they don't name the skill. Not for a single defined task (use autopilot or task-executor) and not for interval-scheduled reruns (use loop).
---

# Goal Runner

The multi-task loop behind a `/goal` run: take a task file, work it top to bottom — one task at a time, each task delegated to sub-agents, each closed only on observed evidence — until nothing unchecked remains. Captures the orchestration contract the user previously retyped into every `/goal` prompt.

## When to use this skill

- "work on the roadmap tasks til completion" / "work the roadmap until completion"
- "work on tasks until completion using sub agents" / "launch sub agents to work the tasks"
- A `/goal` condition that names a roadmap or task file
- "/goal-runner"

Do **not** auto-trigger for a single defined task (`autopilot` / `task-executor`) or for interval-scheduled reruns (`loop`).

## The contract

1. **The main agent never codes.** It parses the roadmap, spawns sub-agents, checks their evidence, updates the roadmap, and commits. Its only file edits are the roadmap file itself.
   - ❌ "This one's a two-line fix, faster to do it myself" — now regression attribution and the review gate are gone for that task.
   - ✅ Spawn a coder sub-agent even for the two-line task; the loop's guarantees come from the gates, not the diff size.
2. **One task at a time — parallelism lives inside the task.** Fan out as many sub-agents as the current task warrants (parallel scouts, parallel review lenses), but exactly one task is in flight and exactly one sub-agent writes to the working tree at any moment. The tree is a mutex: two writers = unattributable diffs; two tasks = unattributable regressions.
   - ❌ "Task 3 is tests and task 4 is docs — they can't conflict, run both coders now." When the suite goes red, nobody knows which diff did it.
   - ✅ Task 3 fans out three scouts in parallel, then its single coder, then two review lenses in parallel; task 4 starts only after task 3 clears close-out.
3. **No commits or pushes by default.** The deliverable is a verified working tree plus per-task evidence; the human gets the final git gate (the same guardrail as `autopilot`). The goal text naming it — "commit each task", "commit and push to <branch>" — IS the authorization; silence is a no.
   - ❌ "The tasks are done and verified, so I committed them to keep things tidy" — the goal text never mentioned git; that's an unauthorized side effect.
   - ✅ Goal text silent on git → working tree left uncommitted, final report ends with a ready-to-paste commit block as the human's move.
4. **When commits ARE authorized: one commit per verified task**, immediately after its gates pass — never a batched end-of-run commit (task 3's regression gets tangled with four other diffs and there's no rollback point), never while the suite has new failures. Push only if the goal text names that too; never force-push. Starting on the default branch with no branch named → create one and log it as an assumption.
5. **Never fake a checkbox.** A box gets ticked only with the evidence in hand (see close-out gate). A result you did not observe is "not run", never "passed".

## How the coordinator thinks

Drive the loop the way a rigorous senior engineer runs a team — the judgment below IS the skill; sub-agents are just hands. (The `think-like-fable` skill, if installed, is this section at full length.)

1. **Read the task beneath the words.** Before spawning anything, restate: "this task needs `___` so that `___`". If the second blank won't fill from the roadmap and nearby docs, pick the cheapest-to-reverse reading and log it as an assumption — or mark BLOCKED if every reading is expensive to undo.
2. **Spend agents where the risk lives.** Effort scales with blast radius, not task length — a wording fix gets one coder and one reviewer; a task touching auth, money, migrations, or 3+ layers gets the full fan-out:

   | Role | Count | Parallel? | Model (routing chain) | Deploy when |
   | --- | --- | --- | --- | --- |
   | Scout (read-only) | 0–3 | with each other | `scout` | task touches >2 files or an unfamiliar layer — one scout per question, not per whim |
   | Coder | exactly 1 | never | `coder`; `coder_high_risk` when the task trips the blast-radius test above | every task — sole writer to the tree |
   | Reviewer | 1, or 2–3 lenses | lenses with each other | `reviewer` | split into lenses (correctness / design / tests) when the diff is large or touches auth/data/money |
   | Fixer | 0–1 | no | `fixer`; second cycle → top of `coder_high_risk` | review produced blockers — gets the coder brief plus the findings, nothing else |

   The Model column resolves per [Model routing](#model-routing) when a model inventory exists; without one, spawn with no model override.

3. **Front-load the riskiest unknown.** Ask: what discovery would invalidate the whole approach? That is scout question #1 — answered before the coder starts, not after it fails.
4. **Sub-agent reports are testimony, not truth.** Quoted command output or a `file:line` citation upgrades a claim to evidence; anything else stays a hypothesis. Two agents disagreeing is signal — resolve it by re-deriving yourself (open the file, run the command), never by picking the more confident voice.
5. **Guard your own context.** The coordinator's window holds orchestration state — queue position, evidence ledger, assumptions. Details live and die inside sub-agents; that is *why* the main agent never codes. Hand artifacts over as **files, not pasted text**: write each coder brief to `.claude/goal-runner/<run>/task-N-brief.md` (`<run>` = the task file's name, lower-cased, without extension — `roadmap` for `ROADMAP.md` — so a resumed session finds the same directory), have the coder write its full report to `task-N-report.md` and return only status + file list + one-line test summary + concerns, and give reviewers the diff as a file (`git diff BASE..HEAD > task-N-diff.patch`). Everything you paste into a prompt or a sub-agent prints back stays resident in your window for the rest of the run.
6. **Keep a run ledger the next session can trust.** Conversation memory does not survive compaction; a coordinator that loses its place re-dispatches finished tasks — the single most expensive failure in long runs. Append one line per event to `.claude/goal-runner/<run>/progress.md`: `Task N: started (BASE <sha7>)`, `Task N: fix round R/2 (<open findings>)`, `Task N: complete (<evidence one-liner>[, commit <sha7>])`, `Task N: BLOCKED (<reason>)`, and every `Ruling: <what you decided> — <why> — <cost if wrong>`. After compaction or a `handoff` resume, trust the ledger and `git log` over your recollection: a task with a `complete` line is done; a task whose last line is a fix round resumes at the next round.
7. **Never pre-judge for the reviewer.** Reviewer briefs never contain "don't flag X", "treat Y as at most minor", or "the plan chose Z" — that's you sparing yourself a fix cycle. Let the finding come back and adjudicate it yourself with the cross-task context the reviewer lacks; record the ruling in the ledger. A silently dropped finding is forbidden.

Compose every sub-agent prompt from the briefs in [references/agent-briefs.md](references/agent-briefs.md) — each lists what the prompt MUST contain and the report format the coordinator holds the agent to.

## Model routing

`~/.claude/model-inventory.json` (written by the `model-inventory` skill, when installed) maps roles to model fallback chains — strongest as escalation, cheapest that suffices as default. Resolve it **once** in Phase 0, then pass each spawn's model explicitly. Routing is optional plumbing: **it never blocks or pauses the run** — every failure below degrades to "no override" (sub-agents inherit the session model) with a one-line note, and the coordinator never edits the inventory file.

1. **Trust gate, with kickoff rebuild.** Use the inventory only if the file parses, `probed` is true, and `generated_at` is under 7 days old. When it fails the gate and the `model-inventory` skill is installed, run that skill **once at Phase 0** (scan + its probe discipline, sub-cent) and route from the fresh file, logging the discovery in the kickoff message; skill absent or discovery fails → treat as absent and note "run /model-inventory to re-enable routing".
2. **Free sanity check — no mid-run probes.** If the model-inventory skill's `scripts/scan.sh` is installed, run it (zero tokens, seconds): a cached CLI whose binary or auth signal has since vanished is dropped from routing for this run; a new CLI it finds is noted for a later rescan. After kickoff, no live model probes — a mid-run model failure is handled by the chain fallback below, never by re-probing.
3. **Resolution.** Per role, take the chain's first entry not marked `unavailable` / `blocked-by-auth` / `quota-exhausted`. Pass only bare aliases (`haiku`/`sonnet`/`opus`/`fable`) to the Agent tool's `model` param — skip anything else in a chain (a dated id or hand-edit is treated as absent). State the resolution in the kickoff message.
4. **Spawn-failure fallback.** A spawn rejected over its model (entitlement, quota, unknown alias) falls to the next chain entry; chain exhausted → spawn with no override. Log it in the run report — never mark a task BLOCKED over routing.
5. **Escalation ladder.** The coder uses `coder_high_risk` only when the task trips the existing blast-radius test — same judgment, no new decision point. A second fix cycle escalates the fixer to the top of `coder_high_risk` before the task may be declared blocked: the cheap retry is a stronger model, not a third identical attempt.
6. **The goal text outranks the table.** "use opus for everything" in the goal text beats every chain. `bash_workers` entries (opencode, qwen, …) are **not** spawn targets — this loop spawns via the Agent tool only.

## Workflow

### Phase 0 — Setup (once)

1. **Locate the task file.** Use the file named in the goal text; else glob the repo root for `ROADMAP.md` / `roadmap.md` / `TODO.md`. Multiple candidates or none → ask once before starting (this is the only permitted question; the loop itself runs unattended).
2. **Parse the tasks.** Checkbox lines (`- [ ]`) are the queue, in file order. If the file has prose tasks but no checkboxes, rewrite it into checkbox form first and show the user the parsed list in the kickoff message.
3. **Baseline the suite.** Run the project's test suite once before task 1 and quote the summary line. Pre-existing failures belong to the baseline, not to task 1.
4. **Confirm git posture.** State in the kickoff message whether the goal text authorized commits and/or pushes (contract rules 3–4). If commits are authorized: note the current branch and read `git log --oneline -5` to learn the project's commit-message convention — follow it (work-item format if the project uses one, otherwise a descriptive subject naming the roadmap task).
5. **Resolve sub-agent models** per [Model routing](#model-routing) and state the per-role resolution (or "no inventory — session model throughout") in the kickoff message.
6. **Open the ledger** at `.claude/goal-runner/<run>/progress.md` (first line names the task file) — or resume from an existing one whose first line names the same file. Keep the run directory out of commits: `git check-ignore -q .claude/goal-runner || echo '.claude/goal-runner/' >> .git/info/exclude` — before the first commit, or every per-task commit sweeps in the ledger, briefs, and `.patch` files.
7. **Pre-flight the queue for conflicts.** Scan the unchecked tasks once: which pairs touch the same file or interface, and does what one *produces* match what a later one *consumes* (names, signatures, paths)? Does any task contradict a global-constraints block or another task? Write the findings as rows in the ledger (pair → what was checked → verdict); "scan clean" without rows is not a scan. Rule on every conflict before task 1 (`Ruling:` line) — the review loop catches conflicts that only surface in implementation, not ones visible in the text.

### Per-task loop

1. **Re-anchor.** Restate in one line: the goal condition, the task now starting, tasks remaining. If the next action doesn't serve the goal, stop and re-plan.
2. **Scout — when the deployment table warrants it.** Fan out read-only sub-agents in parallel, one per question, per the scout brief: `file:line`-cited findings only, no edits, "looked for and did not find" reported as findings. Feed the results verbatim into the coder brief.
3. **Code.** Record `BASE = git rev-parse HEAD` in the ledger, then spawn one coder sub-agent per the coder brief — the task text **verbatim** (paraphrase silently drops acceptance criteria), the goal one-liner, scout findings, and the constraints block. It follows `autopilot`'s execution discipline if installed (incremental verification, ASSUMPTIONS log, command-failure protocol: read the error, change one named thing, retry once, two failures = report back). The coder never commits and never touches the roadmap file — those are the coordinator's.
4. **Review.** Run the `code-review` skill (else review sub-agents per the reviewer brief) on this task's diff. With commit authority, the diff is exactly `BASE..HEAD` (never `HEAD~1` — that silently drops all but the last commit of a multi-commit task); without it, scope by the coder sub-agent's reported file list and note any overlap with earlier tasks' files. A reviewer's "⚠️ cannot verify from diff" items (requirements living in unchanged code or spanning tasks) are yours to resolve before close-out — confirmed gaps enter the fix loop like any blocker. Blockers → send back to a fix sub-agent and re-review (max two cycles; survivors mark the task blocked). Suggestions are logged in the report, never applied — that's scope creep in an unattended run.
5. **Regression.** Run the full relevant suite; quote the summary line. When the task's diff renames a symbol, changes a default or signature, or touches shared state, also run `regression-hunt` if installed (a `confirmed` regression enters the fix loop like a blocker). Gate is **no new failures vs. the Phase 0 baseline** — not "all green" if the baseline was already red.
6. **Close out — all three observed, then and only then:** review shows zero blockers; regression gate passed (summary quoted); the coder's verification of the task's own behavior is quoted. Tick the checkbox; if commits are authorized, commit per the convention found in Phase 0 (push only if that's authorized too).
7. **Blocked?** If the task hard-stops (destructive step, missing access, spec contradicts the codebase, or two failed fix cycles): annotate the line — `- [ ] <task> — BLOCKED: <one-line reason>` — leave the box unchecked, and continue to the next task.
8. **Loop** until no unchecked, unblocked tasks remain.

### Completion

- All boxes ticked and last suite run quoted green → the goal condition holds; report per-task outcomes (task → evidence → commit hash when commits were authorized) plus all logged assumptions and suggestions, and **every `Ruling:` line from the ledger, in order, each with its cost-if-wrong** — the rulings list is the only place decisions taken on the human's behalf reach them; a ruling that dies with the ledger was a decision made in secret. When commits weren't authorized, end the report with a ready-to-paste commit block — the human's move.
- Blocked tasks remain → the goal is **not** met: report exactly which tasks are blocked and the one decision each needs. Never tick a blocked box to satisfy the Stop hook.
- Context running low mid-roadmap → use the `handoff` skill: record queue position, baseline state, branch, and per-task status so the next session resumes the loop instead of restarting it.

## Examples

### Example 1: the canonical run

**User:** `/goal` "work on the roadmap tasks til completion. one task at a time. use sub agents for coding, code review and testing. commit each task to the current branch and push."

**Claude:** parses 6 unchecked tasks from `ROADMAP.md`, baselines the suite (quoted: `42 passed`), then loops: coder sub-agent → code-review (1 blocker → fixed → clean) → suite re-run quoted → checkbox ticked → commit → push (authorized in the goal text). Task 4 needs a credential that's missing → marked `BLOCKED: no STRIPE_TEST_KEY in env`, loop continues with 5 and 6. Final report: 5 committed+pushed with hashes and evidence, 1 blocked with the decision needed.

### Example 2: git not authorized

**User:** "work the roadmap until completion, sub agents do the work"

**Claude:** same loop, but **no commits and no pushes** — the goal text never mentioned git. All six tasks end verified in the working tree, and the final report ends with a ready-to-paste commit block (and nothing pushed) as the human's move.

## Anti-patterns

- ❌ Main agent editing source "to save a sub-agent spawn" — the only file it edits is the roadmap.
- ❌ Ticking a checkbox from the coder's claim of success without the quoted suite run — that's confabulated success wearing a checkbox.
- ❌ Committing, pushing, opening PRs, or switching branches when the goal text authorized none of them — "done and verified" is not commit authority.
- ❌ When commits are authorized: one end-of-run mega-commit, or committing while the suite has new failures ("I'll fix it in the next task").
- ❌ Pausing mid-loop to ask the user a preference question — log an assumption with blast radius instead; the single permitted question is Phase 0's file disambiguation.
- ❌ Fixing a reviewer finding in the coordinator session "because it's one line" — controller fixes pollute your context and skip review; route it to the fixer.
- ❌ Pasting prior-task summaries into later briefs ("state after tasks 1–3…") — a fresh coder needs its task, the interfaces it touches, and the constraints block. Nothing else.
- ❌ Re-dispatching a task after compaction because you don't remember finishing it — read the ledger and `git log` first.
- ❌ Deleting or rewording a task you can't finish so the file "completes" — annotate BLOCKED and report honestly.
- ✅ One task at a time; sub-agents do the work; every tick backed by quoted evidence; git side effects only when the goal text grants them (and then one commit per task); blocked tasks surfaced, never buried.

## Notes

- Composes with: `autopilot` (per-task execution discipline), `code-review` (the review gate), `write-tests` (when a task is itself "add tests"), `model-inventory` (per-role model routing), `handoff` (context survival). All optional — the loop degrades to focused sub-agent prompts when they're absent.
- The built-in `/goal` command supplies persistence (a Stop hook that blocks ending until the condition holds); this skill supplies the discipline. It works without the hook too — the loop just becomes stoppable.
- Zero unchecked tasks at kickoff is a valid outcome: report "roadmap already complete" with the file's state; don't invent work.
