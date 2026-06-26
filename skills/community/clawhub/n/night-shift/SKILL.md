---
name: night-shift
version: 1.0.5
description: "Queue coding plans during the day, approve them, execute later in isolated worktrees, and inspect reports. Background agentic execution requires an explicitly configured non-interactive runner."
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python3", "git"] },
        "optional":
          {
            "bins": ["agent", "cursor", "claude"],
            "env":
              [
                "OPENCLAW_WORKSPACE",
                "NIGHT_SHIFT_DATA_DIR",
                "NIGHT_SHIFT_MODEL",
                "CURSOR_CLI",
                "CURSOR_API_KEY",
                "TELEGRAM_BOT_TOKEN",
                "TELEGRAM_CHAT_ID",
                "NIGHT_SHIFT_CHAT_ID",
              ],
          },
        "capabilities":
          [
            "filesystem-read-write",
            "git-worktrees",
            "subprocess-execution",
            "optional-cursor-cli",
            "optional-claude-cli",
            "optional-telegram-notifications",
            "optional-model-provider-calls",
          ],
      },
  }
---

# Night Shift

Night Shift is an autonomous queued-execution skill for engineering work.

Instead of asking the agent to do one large coding task immediately, you build a queue of plans, review or approve them, then run them in a controlled batch window. Each plan is split into phases, executed in isolation, verified, checkpointed, and summarized in a report.

**Mental model:**
- Daytime: create and refine plans
- Before execution: approve what is safe to run
- Execution window: Night Shift runs plans phase by phase
- Morning: inspect results, merge, retry, or continue

This is useful when you want:
- deferred execution instead of immediate chat-time work
- safer batching for multi-step changes
- isolated worktrees per plan
- retry and checkpoint behavior
- a written report after execution

---

## When to Use

Use Night Shift when the user asks for things like:
- “good night”
- “queue this for later”
- “plan add …”
- “run these approved plans overnight”
- “night shift status”
- “show my morning report”
- “retry plan #3”
- “merge that finished plan”

Prefer Night Shift over immediate execution when:
- the work is multi-phase
- the task needs isolation from the main repo state
- the user wants review/approval before execution
- the work may take a long time
- you want a queue of tasks rather than one interactive run

Do **not** use Night Shift for:
- tiny one-off edits better handled immediately
- high-risk production actions without review
- tasks that require constant human decisions mid-run
- public/external actions that should be explicitly approved in the moment

---

## Core Concepts

### 1. Plan
A plan is the unit of queued work. It includes:
- title
- optional description
- optional repo URL
- priority
- token/time budget hints
- generated phases
- status and execution metadata

### 2. Phase
Each plan is split into phases. A phase has:
- a title
- a prompt/instruction
- an execution method
- verification settings
- retry state
- status

### 3. Execution Method
Each phase chooses one of several execution methods:
- `shell`
- `cursor`
- `claude-code`
- `subagent`

This lets the framework mix deterministic shell work with agentic coding work.

### 4. Worktree Isolation
Each plan runs in its own git worktree under `data/night-shift/worktrees/`.

That means Night Shift can:
- avoid trampling the main branch
- keep plan-specific diffs separate
- retry or inspect work in isolation
- support safer merge/rollback flows

### 5. Verification
Phases can be checked after execution using one of several verification modes, including:
- `files_exist`
- `check_git_diff`
- `run_tests`
- `lint_check`
- `smoke_test`
- `import_check`
- `integration_check`
- `snapshot_diff`
- `none`

### 6. Reporting
After execution, Night Shift writes a report so the next interaction starts from evidence instead of guesswork.

---

## Typical Workflow

### During the day
1. Add one or more plans
2. Review phases
3. Edit prompts or priorities if needed
4. Approve the plans that are safe to run

### At execution time
5. Start Night Shift
6. It acquires a lock, checks budgets, creates worktrees, and executes phases
7. It verifies each phase, checkpoints progress, records failures, and logs results

### After execution
8. Read the report
9. Inspect worktrees or diffs
10. Merge successful work, retry failed work, or queue follow-up plans

---

## User-Facing Commands

These are the command patterns the skill is designed around.

| Command | Purpose |
|---|---|
| `plan add <desc>` | Create a new plan with generated phases |
| `plan steal <url> <desc>` | Queue work derived from an external repo/project |
| `plan list [status]` | Show plans in the queue |
| `plan show #<id>` | Show full details for one plan |
| `plan approve #<id>` | Approve one plan |
| `plan approve all` | Approve all queued plans |
| `plan remove #<id>` | Remove a plan |
| `plan priority #<id> <level>` | Change priority |
| `plan edit #<id> phase <n> prompt <text>` | Refine a phase prompt |
| `good night` | Start execution of approved plans |
| `night shift status` | Show current state |
| `night shift stop` | Request stop / halt execution |
| `night shift dry-run` | Preview what would execute |
| `morning` | Show the latest execution report |
| `night shift merge #<id>` | Merge completed plan results |
| `night shift inspect #<id>` | Inspect outputs/worktree |
| `night shift retry #<id>` | Retry a failed or partial plan |

If your host agent uses a different natural-language wrapper, preserve the same intent and lifecycle.

---

## Architecture

Night Shift is split into a few major parts.

### Queue and Models
- `models.py` — core plan/phase data models and enums
- `queue.py` — CRUD, queue index, plan storage, approvals, updates
- `phase_generator.py` — creates initial phases from plan input

### Execution Engine
- `executor.py` — main run loop, orchestration, locking, budget checks, reporting
- `phase_runner.py` — executes individual phases using the chosen method
- `subagent_runner.py` — helper for subagent-based execution

### Safety and Recovery
- `verifier.py` — phase verification logic
- `checkpoint.py` — save/resume progress
- `failure_memory.py` — track known failures and avoid blind repetition
- `lock.py` — prevent overlapping runs
- `budget.py` — per-phase/per-plan/night budget tracking
- `memory_guard.py` — watchdog for memory/process hygiene

### Repo / Git Operations
- `git_manager.py` — worktree setup, commit/reset helpers

### Visibility and Operations
- `reporter.py` — morning-style summaries
- `monitor.py` — notifications and health checks
- `watchdog.py` — execution monitoring
- `status.py` — status helpers
- `cron_trigger.sh` / `ns-control.sh` — optional shell wrappers

### Optional Extensions
The `bmad_*.py` files are advanced helpers for richer planning/PRD flows. They are **not required** for the core Night Shift lifecycle.

---

## Execution Flow

A typical run looks like this:

1. **Preflight**
   - confirm no conflicting lock
   - load queue
   - check for approved plans
   - initialize budget / logs / monitors

2. **Plan selection**
   - choose approved plans in queue order / priority order

3. **Per-plan setup**
   - create or prepare isolated worktree
   - load checkpoint if resuming

4. **Per-phase execution**
   - build phase prompt
   - dispatch via the selected execution method
   - capture output, status, timing, and any token/cost metadata available

5. **Verification**
   - run configured verification step
   - mark success/failure
   - record failure memory if relevant

6. **Persistence**
   - update plan JSON
   - update queue index
   - save checkpoint/logs

7. **Completion**
   - finalize plan status
   - generate report
   - release lock

---

## Safety Model

Night Shift is designed to be agentic, but not reckless.

### Safety features
- **approval gate** before execution
- **worktree isolation** per plan
- **execution lock** to prevent overlapping runs
- **phase-by-phase progression** instead of one giant opaque run
- **verification hooks** after phases
- **checkpointing** for resumes/recovery
- **failure memory** to reduce repeated mistakes
- **budget caps** across phase/plan/night scopes
- **watchdog/monitoring** support

### What this protects against
- clobbering the main branch
- executing multiple Night Shift loops at once
- losing progress on interruption
- repeating the same failing step forever
- oversized unattended execution sessions

### What it does **not** guarantee
- perfect code quality
- correct architectural judgment for every task
- safe production deployment by default
- zero hallucination from external coding models

You still need sensible approval and review.

### Trust, permissions, and security scanners

Night Shift may be flagged by automated scanners because it intentionally includes operational automation primitives:

- shell wrappers (`cron_trigger.sh`, `ns-control.sh`, `claude-wrapper.sh`)
- Python subprocess execution for approved phases
- git worktree, commit, reset, and diff helpers
- optional Cursor CLI / Claude Code / subagent dispatch
- optional Telegram notification support

These are expected for an unattended coding workflow, but they deserve review before use. Night Shift does **not** bundle private keys, hidden credentials, miners, persistence malware, or background network beacons. It only uses credentials and CLIs already available in the host environment.

Before running it in a new workspace:

1. Review queued plans and phase prompts before approval.
2. Run `night shift dry-run` first when available.
3. Start with a disposable test repo or branch.
4. Keep production deploys as explicit manual steps unless you intentionally add deploy phases.
5. Inspect diffs/reports before merging completed work.

For non-interactive ClawHub installs, some registries may require `--force` after scanner warnings. Treat that as a prompt to review the code, not as a failure signal.

---

## Storage Layout

Night Shift stores runtime state under:

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

### Important files
- `queue.json` — lightweight queue index
- `plans/*.json` — full plan records
- `worktrees/<plan_id>/` — isolated git worktree per plan
- `failure-memory.json` — prior failed step fingerprints
- `budget.json` — current budget tracking
- `execution.log` — main execution log

---

## Environment Variables

Night Shift now supports portable configuration instead of relying on hardcoded local paths.

### Core
- `OPENCLAW_WORKSPACE` — override workspace root
- `NIGHT_SHIFT_MODEL` — preferred model hint for model-driven helpers
- `CURSOR_CLI` — explicit path to Cursor CLI / `agent` binary

### Notifications
- `NIGHT_SHIFT_CHAT_ID` — target chat for Night Shift notifications
- `TELEGRAM_CHAT_ID` — fallback notification target
- `TELEGRAM_BOT_TOKEN` — Telegram Bot token for notifications

### Execution environment
Night Shift also inherits normal environment from the host runtime, including anything needed by:
- git
- Python
- shell commands
- coding harnesses / subagents

If a specific execution method requires additional auth or binaries, document that at the host level.

---

## Prerequisites

### Required
- Python 3
- git
- workspace write access
- ability to create and modify files in `data/night-shift/`
- a host environment that can run shell commands and Python scripts

### Optional but useful
- Cursor CLI / agent binary for `cursor` execution
- Claude Code for `claude-code` execution
- subagent support for delegated runs
- Telegram bot setup for notifications

### Strongly recommended
- run inside a git-backed workspace
- use approval before unattended execution
- keep tests/lint scripts working in the target repo

---

## Examples

### Example 1 — queue a feature for later
User intent:
> Add OAuth login to the app, but do it overnight.

Night Shift flow:
1. `plan add add OAuth login to the app`
2. inspect generated phases
3. `plan approve #<id>`
4. later: `good night`

### Example 2 — multiple plans in one batch
User intent:
> Queue three fixes now, run them all tonight.

Flow:
1. add three plans
2. set priorities as needed
3. approve the safe ones
4. run Night Shift
5. read the morning report

### Example 3 — dry run before execution
User intent:
> Show me what would run tonight.

Flow:
- `night shift dry-run`

### Example 4 — retry a failed plan
User intent:
> Retry the failed parser plan.

Flow:
- inspect plan/report
- refine the phase prompt if needed
- `night shift retry #<id>`

### Example 5 — inspect before merge
User intent:
> Show me what Night Shift changed before we merge.

Flow:
- `night shift inspect #<id>`
- review diff/worktree/tests
- `night shift merge #<id>` when satisfied

---

## How to Operate the Skill Well

### Good plan inputs
Night Shift works best when the plan title/description is concrete.

Better:
- “Add retry logic to payment webhooks and verify with integration tests”
- “Refactor dashboard query caching and run frontend smoke tests”

Worse:
- “make it better”
- “fix the app somehow”

### Good approval policy
Approve unattended runs when:
- the repo is in a sane state
- the task is scoped
- verification exists
- you can tolerate isolated failures

Avoid approval when:
- the task is ambiguous
- the run might touch production systems directly
- the work needs live stakeholder decisions

### Good execution method selection
Use:
- `shell` for deterministic scripted work
- `cursor` / `claude-code` for coding-heavy phases
- `subagent` for delegated structured work

---

## Limitations

Be honest about these.

- It is not a general scheduler for arbitrary business processes.
- It is optimized for engineering work in a writable workspace.
- Quality depends heavily on phase quality and verification quality.
- If the underlying coding harness is weak or unavailable, outcomes degrade.
- Worktree-based isolation assumes the repo supports normal git operations.
- Some wrapper scripts and helpers are host-environment dependent.
- Long unattended runs still need human review before high-trust deployment.

---

## Troubleshooting

### “No approved plans found”
Approve at least one plan before starting execution.

### “Night Shift already running”
A lock file or active run exists. Inspect status before forcing a restart.

### “Worktree creation failed”
Check:
- git repo health
- branch/worktree permissions
- existing conflicting worktrees

### “Phase keeps failing”
- inspect the plan’s phase prompt
- review verification settings
- check failure memory / logs
- reduce scope and retry

### “Notifications are not sent”
Check notification env vars:
- `TELEGRAM_BOT_TOKEN`
- `NIGHT_SHIFT_CHAT_ID` or `TELEGRAM_CHAT_ID`

### “Cursor / Claude execution not found”
Set the expected binary path explicitly or install the required tool:
- `CURSOR_CLI`
- whichever CLI your host maps to `claude-code`

### “Execution stopped midway”
Inspect checkpoints, report output, logs, and plan status. Resume/retry instead of starting from scratch blindly.

---

## Publishing Notes

Night Shift is publishable as a **power-user engineering skill**.

Its strongest differentiators are:
- queued plan lifecycle
- isolated worktrees
- phase verification
- checkpointing and retry behavior
- morning-report workflow

Its biggest adoption caveats are:
- requires a repo-aware writable environment
- works best with supporting CLIs/tools already installed
- more operational than a simple one-file prompt skill

That is fine. Don’t oversell it as “plug-and-play for everyone.” Sell it as a serious autonomous coding workflow for advanced users.

---

## Files

Core engine files in `scripts/` include:
- `models.py`
- `queue.py`
- `phase_generator.py`
- `executor.py`
- `phase_runner.py`
- `verifier.py`
- `checkpoint.py`
- `failure_memory.py`
- `budget.py`
- `git_manager.py`
- `lock.py`
- `reporter.py`
- `monitor.py`
- `watchdog.py`
- `subagent_runner.py`
- `memory_guard.py`

Optional/advanced helpers:
- `bmad_batch.py`
- `bmad_context.py`
- `bmad_guardrails.py`
- `bmad_phases.py`
- `bmad_prd_evolve.py`
- `bmad_queue.py`
- `bmad_rollback.py`

Shell helpers:
- `cron_trigger.sh`
- `ns-control.sh`
- `claude-wrapper.sh`

---

## See Also

- `REFERENCE.md` — operational reference, setup notes, environment variables, and troubleshooting
- `scripts/test_queue.py` — queue behavior checks
- `scripts/test_integration.py` — end-to-end integration checks
