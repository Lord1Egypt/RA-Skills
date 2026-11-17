# masterplan-executor

The execution counterpart to `masterplan-builder`. Where that skill plans a project to production-ready detail, this skill actually builds it — phase by phase, strictly from the masterplan, to the same overkill standard, with automatic web research whenever the plan is unclear instead of guessing.

## What it does

1. Finds and fully reads `docs/masterplan/masterplan.md` (and any linked files) in the project directory. Refuses to start from an assumed plan if none exists.
2. Checks the actual codebase and any existing `docs/masterplan/execution-log.md` to figure out real current state — never assumes a clean slate, and resumes correctly across sessions.
3. Executes the masterplan's Build Roadmap one phase at a time: implements to production standard, **automatically searches the web whenever something is ambiguous, outdated, or contradictory instead of guessing**, actually runs/tests what it builds, self-audits the code before moving on, and logs everything.
4. Runs a final whole-system integration check against the masterplan's own definition of done before calling the project complete.

## Files in this skill

```
SKILL.md                                -- the workflow Claude follows
references/execution-standards.md       -- production-readiness bar, phrased as things to
                                            verify by actually running/testing code, not just
                                            writing it (mirrors masterplan-builder's standards)
references/phase-execution-checklist.md -- the mechanical step-by-step loop for one phase
references/resource-safety.md           -- RAM-aware subagent concurrency: auto-detects
                                            available memory before any surgical/parallel
                                            subagent execution so it never risks an OOM
references/progress-log-template.md     -- template for docs/masterplan/execution-log.md,
                                            the persistent record that makes execution safely
                                            resumable across sessions
```

## How to use it

Have a masterplan ready (from `masterplan-builder`), then ask Claude to build it — e.g. "build this", "start executing phase 1", "lanjutkan pembangunan sesuai masterplan". Claude will read the plan, check what's already there, and start executing from the right point, phase by phase, asking only when a deviation is user-facing or architecturally significant.

## Core guarantee

Never guesses when a search could resolve the ambiguity. Never marks a phase done with a known Blocker/Major gap. Never leaves dead code or silent failure paths behind. Never silently deviates from the plan — every deviation is researched, implemented correctly, and logged with its reason. Never spawns subagents at a guessed or fixed concurrency — always detects actual available RAM first and falls back to sequential execution when memory is constrained or undetectable, so surgical/parallel execution never risks an OOM.

## Known limitation

Like masterplan-builder, this skill hasn't yet been run end-to-end on a real project — it's designed and internally consistent, but not battle-tested. Treat the first real run as a trial.
