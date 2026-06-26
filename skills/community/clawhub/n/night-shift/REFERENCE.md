# Night Shift Reference

This file is the operational reference for the Night Shift skill.

It complements `SKILL.md` by focusing on setup, runtime expectations, file layout, and practical caveats.

---

## 1. What Night Shift Actually Is

Night Shift is a queued autonomous execution framework for coding work.

It is **not** just a prompt pattern. It includes:
- plan storage
- phase generation
- isolated worktrees
- execution routing
- verification
- checkpointing
- reporting
- monitoring helpers

Think of it as a lightweight unattended engineering operator.

---

## 2. Minimum Runtime Expectations

Night Shift expects a host environment with:
- Python 3
- git
- a writable workspace
- permission to create directories/files under `data/night-shift/`
- a repo or project context where worktrees and diffs make sense

If those are missing, the skill may still partially function, but the core value drops sharply.

---

## 3. Security Review Notes

Night Shift is powerful by design. It can run shell commands, create git worktrees, call coding CLIs, and write reports/checkpoints. That means automated registries may classify it as suspicious even when the package is behaving as intended.

Expected capabilities:
- local file and directory writes under the configured workspace
- git worktree / diff / commit / reset operations
- subprocess execution for approved phase methods
- optional calls to host-provided tools such as Cursor CLI, Claude Code, or subagents
- optional Telegram notifications when notification environment variables are configured

Not expected:
- bundled secrets or private tokens
- cryptocurrency mining
- hidden persistence outside the configured workspace
- unsolicited external network calls beyond host-configured tools/notifications
- production deployment unless a user-approved phase explicitly performs it

Recommended first-run posture:

```bash
# install into a disposable workspace first if reviewing a public copy
clawhub install night-shift --force

# inspect docs and scripts before use
find skills/night-shift -maxdepth 3 -type f | sort

# run only approved test plans initially
```

If your ClawHub client requires `--force`, it is usually because of these intentional automation primitives. Review before running, then proceed only in a workspace where unattended coding is acceptable.

---

## 4. Workspace Assumptions

The portable version of Night Shift uses workspace auto-detection.

Default behavior:
- detect workspace from the skill location
- store runtime data in `data/night-shift/`

Override with:

```bash
export OPENCLAW_WORKSPACE=/path/to/workspace
```

This controls where Night Shift reads/writes:
- queue state
- plan files
- worktrees
- logs
- reports
- budget / checkpoint / failure memory data

---

## 4. Important Environment Variables

### Core

```bash
export OPENCLAW_WORKSPACE=/path/to/workspace
export NIGHT_SHIFT_MODEL=auto
export CURSOR_CLI=/path/to/agent
```

### Notifications

```bash
export TELEGRAM_BOT_TOKEN=...
export NIGHT_SHIFT_CHAT_ID=123456789
# or fallback
export TELEGRAM_CHAT_ID=123456789
```

### Notes
- `NIGHT_SHIFT_MODEL` is a hint used by some model-driven helpers.
- `CURSOR_CLI` is useful if the `agent` binary is not discoverable on PATH.
- Notification variables are optional.

---

## 5. Storage Layout

Runtime state is stored under:

```text
data/night-shift/
├── queue.json
├── plans/
├── worktrees/
├── execution/
├── reports/
├── failure-memory.json
├── budget.json
└── execution.log
```

### Recommended hygiene
- back up `plans/` and `reports/` if they matter
- prune stale worktrees periodically
- inspect `failure-memory.json` if repeated failures feel suspicious
- keep `queue.json` and `plans/` in sync by using the provided queue operations, not ad hoc edits

---

## 6. Execution Methods

Night Shift supports multiple execution styles at the phase level.

### `shell`
Use for deterministic commands.

Best for:
- codegen via scripts
- test runs
- linters
- file transforms
- scripted maintenance

### `cursor`
Use for agentic coding via a Cursor/agent-style runner.

Best for:
- implementation-heavy code changes
- multi-file refactors
- coding tasks where a model benefits from repo context

### `claude-code`
Use for Claude Code based execution if your host supports it.

Best for:
- careful repo-aware coding work
- structured implementation with strong text output

### `subagent`
Use when the host environment supports agent delegation.

Best for:
- isolated research or coding subtasks
- delegated steps with separate context

---

## 7. Worktree Behavior

Night Shift’s safety story depends heavily on worktree isolation.

Per-plan worktrees help with:
- safer concurrent plan handling
- easier diff inspection
- cleaner retry/reset behavior
- less contamination of the main working tree

Operational advice:
- use Night Shift in repos with healthy git state
- avoid starting with a dirty or half-merged repo if you can
- inspect worktrees before merging if the task was complex

---

## 8. Verification Modes

Available verification labels include:
- `files_exist`
- `check_git_diff`
- `run_tests`
- `lint_check`
- `smoke_test`
- `import_check`
- `integration_check`
- `snapshot_diff`
- `none`

### Practical guidance
- use `run_tests` when repo tests are reliable
- use `lint_check` for style/static checks
- use `smoke_test` for lightweight runtime confidence
- avoid `none` unless the phase is inherently non-testable or very small

Night Shift is only as trustworthy as the verification attached to its phases.

---

## 9. Budget and Stop Conditions

The framework tracks budgets across multiple scopes.

Examples mentioned in the implementation/docs include:
- per-phase limits
- per-plan limits
- whole-night limits

Operationally, budget checks are there to prevent:
- endless unattended work
- overconsumption of model/tool resources
- a single bad plan dominating the whole run

If a plan is repeatedly too large, split it into smaller plans or improve the generated phases.

---

## 10. Checkpoints and Failure Memory

### Checkpoints
Checkpointing allows a run to resume or be inspected without pretending the whole night never happened.

Use this when:
- a run was interrupted
- the system restarted
- you want to retry after partial progress

### Failure Memory
Failure memory records prior failure fingerprints / patterns to reduce blind repetition.

Use it as a signal, not an oracle.
If the same phase keeps failing:
- simplify the phase
- change the execution method
- improve the prompt
- tighten verification

---

## 11. Monitoring and Notifications

Night Shift includes monitoring/reporting helpers.

Capabilities may include:
- execution logs
- morning summaries
- Telegram notifications
- watchdog-style checks

These are useful, but optional. The core queue/executor flow should still make sense without notifications.

If you enable notifications, treat them as operational visibility — not as a replacement for review.

---

## 12. Optional BMAD Extensions

The `scripts/` folder may include BMAD-related helpers such as:
- `bmad_batch.py`
- `bmad_context.py`
- `bmad_guardrails.py`
- `bmad_phases.py`
- `bmad_prd_evolve.py`
- `bmad_queue.py`
- `bmad_rollback.py`

These are advanced extensions.

They are **not** required for the baseline Night Shift lifecycle:
- queue
- approve
- execute
- verify
- report

If you publish Night Shift, present BMAD as an optional advanced lane, not the first thing a new user must understand.

---

## 13. Shell Helpers

Shell wrappers in `scripts/` may include:
- `cron_trigger.sh`
- `ns-control.sh`
- `claude-wrapper.sh`

These are convenience helpers, not the whole product.

Use them when:
- your environment wants cron-style launches
- you prefer shell entrypoints
- you want lightweight control wrappers

Avoid making your documentation depend entirely on them.

---

## 14. Testing Notes

In the current skill-local portable version, the queue and integration checks have been exercised successfully.

Files of interest:
- `scripts/test_queue.py`
- `scripts/test_integration.py`

When validating changes, prefer:
1. queue tests
2. integration checks
3. a dry run
4. a small real plan in a non-critical repo

That progression gives much better confidence than jumping straight to a large unattended batch.

---

## 15. Recommended Rollout Strategy for New Users

If someone installs this skill fresh, the safest adoption path is:

### Stage 1 — Read and inspect
- read `SKILL.md`
- inspect `scripts/`
- confirm required binaries and Python availability

### Stage 2 — Dry run
- create one simple plan
- run `night shift dry-run`

### Stage 3 — Small real run
- approve one low-risk plan
- run the executor
- inspect report and worktree

### Stage 4 — Multi-plan batch
- queue several tasks
- use priorities
- review morning report quality

### Stage 5 — Advanced automation
- add notifications
- add cron wrappers
- experiment with BMAD extensions

---

## 16. Common Failure Modes

### A. No plans execute
Likely causes:
- no approved plans
- stale lock
- queue/index mismatch

### B. Worktree setup fails
Likely causes:
- broken git state
- repo permissions
- conflicting worktrees/branches

### C. Model-backed phase fails repeatedly
Likely causes:
- vague phase prompt
- wrong execution method
- tool/harness missing
- verification too strict for the phase shape

### D. Reports are weak
Likely causes:
- low-quality phase structure
- missing verification
- oversized tasks crammed into one plan

### E. Notifications never arrive
Likely causes:
- missing `TELEGRAM_BOT_TOKEN`
- missing `NIGHT_SHIFT_CHAT_ID` / `TELEGRAM_CHAT_ID`
- network or bot permissions issues

---

## 17. What to Be Honest About in a Public Listing

Night Shift is powerful, but it is not beginner-simple.

Be explicit that it is best for:
- advanced OpenClaw / agent users
- repo-centric engineering workflows
- users who understand approval, git, and execution risk

Do **not** market it like:
- “set and forget magic coding forever”
- “safe for any repo with zero setup”
- “works equally well without verification or review”

The real pitch is better:
> a structured autonomous execution framework for deferred engineering work

---

## 18. Good Public Positioning

A strong public framing is:

- **What it is:** queued overnight coding workflow
- **Why it matters:** safe-ish deferred execution with worktrees and reports
- **Who it’s for:** power users running multi-step repo tasks
- **Why it stands out:** phase-based execution + isolation + verification + reporting

---

## 19. Suggested Setup Snippet

```bash
export OPENCLAW_WORKSPACE="$HOME/.openclaw/workspace"
export CURSOR_CLI="$(command -v agent)"
export NIGHT_SHIFT_MODEL="auto"
# Optional notifications
export TELEGRAM_BOT_TOKEN="..."
export NIGHT_SHIFT_CHAT_ID="123456789"
```

---

## 20. Final Advice

Night Shift gets most of its value from discipline, not bravado.

If results are shaky:
- shrink the plan
- improve the phases
- improve verification
- inspect worktrees
- retry surgically

The framework is strongest when it helps you run a calm engineering pipeline, not when it is treated like a slot machine.
