# parallel-orchestrate

> **Status:** Stable, in regular use. v1.6.

Orchestrates a gstack implementation plan by shredding it into parallel subtasks, dispatching each to an isolated git worktree via the Claude Code `Agent` tool, then cherry-picking the results onto your working branch wave by wave.

Sits between `/autoplan` (or `/plan-eng-review`) and `/review` + `/ship`.

---

## What it does

You hand it a plan file. It:

1. **Pre-flights** the repo (base branch, clean tree, freeze marker, jq, stack detection)
2. **Auto-discovers** your plan from `~/.gstack/projects/<slug>/ceo-plans/` or `.gstack/plans/`
3. **Shreds** it into parallel tasks grouped into waves (foundation → core → surface)
4. Shows you the dependency graph + a rough cost estimate, asks for approval
5. **Dispatches** each task as an `Agent` subagent with `isolation: "worktree"` so parallel commits never race on the git index lock
6. **Cherry-picks** each successful task's commit onto your working branch in dependency order
7. Runs the full test suite at every wave boundary
8. Hands off to `/review` then `/ship` when the build is green

The orchestrator never writes feature code itself. Every line of code, every conflict resolution, every fix-up comes from a subagent.

---

## How to use

```
/parallel-orchestrate
```

Voice triggers also work: "orchestrate the plan", "ship the plan in parallel", "execute the plan in parallel".

You'll be asked to approve the task decomposition before anything dispatches. Nothing runs without your "yes."

---

## What's working (verified by dry-run)

| Area | Status |
|------|--------|
| Pre-flight (base branch, jq, freeze, dirty tree) | ✓ |
| Plan auto-discovery from gstack project plans | ✓ |
| Stack detection (Ruby/Node/Python/Go/Rust + bun/pnpm/yarn/npm) | ✓ |
| Conventional-commits prefix detection | ✓ |
| Env-var persistence across Bash tool calls (env.sh source pattern) | ✓ |
| Worktree isolation per parallel subagent | ✓ |
| Defensive result-JSON parsing (missing/malformed → treated as failed) | ✓ |
| Cherry-pick by SHA (works regardless of branch naming) | ✓ |
| Resume from checkpoint with head-match validation | ✓ |
| Bounded fix-up retries (max 2 per wave) | ✓ |
| Bounded `/review` cleanup loop (max 2 passes) | ✓ |
| Telemetry + per-wave timeline events | ✓ |

The skill survived three rounds of adversarial review and four execution dry-runs across v1.1 → v1.5. Real bugs the dry-runs caught:

- v1.4: `git rev-parse` without `--verify` echoed the input ref name to stdout, corrupting `_BASE_SHA`. Static review missed it. Execution caught it.
- v1.4 (review pass): Bash shell state doesn't persist across Claude Code Bash tool calls. Without an env.sh source pattern, every variable set in Phase 0 was empty by Phase 1.

---

## What's NOT working yet

- **Worktree branches accumulate.** The Agent tool's `isolation: "worktree"` mode leaves auto-managed branches behind. The skill prunes worktree records but does NOT auto-delete branches (deleting them is unsafe — we can't reliably tell harness branches apart from user branches). Run `git branch --list` and clean manually if they pile up.
- **Resume divergence is detected, not auto-recovered.** If you `git reset --hard` between runs, the skill correctly refuses to resume but won't try to rebuild missing commits.
- **No `/ship` integration test.** Phase 4 calls `Skill({skill: "ship"})` but the handoff has only been validated as a code path, not a real shipping flow.

---

## Architecture in 5 bullets

- **Orchestrator (this skill):** plans, dispatches, integrates. Writes `TASKS.md`, `state.jsonl`, the final report. Never writes feature code.
- **Subagents (`Agent` tool):** one per task, each in its own isolated git worktree. Reads CLAUDE.md, implements scope, commits, writes a result JSON to a shared dir.
- **Shared state directory:** `~/.gstack/projects/<slug>/orchestrate/<branch-safe>/` holds `TASKS.md`, `env.sh`, `state.jsonl`, `results/<TASK_ID>.json`.
- **Cherry-pick integration:** after each wave, the orchestrator reads each subagent's commit SHA from its result JSON and cherry-picks onto the working branch in dependency order.
- **REQUIRED SUB-SKILLS:** `superpowers:using-git-worktrees`, `superpowers:dispatching-parallel-agents`.

---

## Where the data lives

- **Skill-level analytics:** `~/.gstack/analytics/skill-usage.jsonl` — one start row + one completion row per orchestrate run, with `outcome` (success/abort/error) and `duration_s`.
- **Per-wave timeline:** `~/.gstack/projects/<slug>/timeline.jsonl` — `wave_dispatched` (wave + task count) and `wave_completed` (duration + success/failed/fixup counts) events per wave, plus the standard `started` / `completed` skill events.
- **Per-task results:** `~/.gstack/projects/<slug>/orchestrate/<branch>/results/*.json` — what each subagent did.
- **Resume state with per-wave duration:** `~/.gstack/projects/<slug>/orchestrate/<branch>/state.jsonl` — head, wave, duration, counts. Older entries (pre-1.6) lack the count/duration fields; resume logic only reads `head`/`wave`/`status` so it stays compatible.

Query with `gstack-analytics` (skill-usage), `gstack-timeline-read` (timeline), or `jq` directly.

---

## Where to read more

- Full skill definition: `~/.claude/skills/parallel-orchestrate/SKILL.md`
- Sibling skills it composes with: `/autoplan`, `/plan-eng-review`, `/review`, `/qa`, `/ship`
- The Agent tool's `isolation: "worktree"` mode is what makes parallel commits safe
