# Resource-Safe Subagent Execution

This applies whenever the execution environment supports spawning subagents/parallel workers for surgical execution (e.g. Claude Code's Task/subagent tool, or any environment that lets this skill fan out independent pieces of a phase concurrently). If the environment has no such capability, this file doesn't apply — skip it and execute sequentially as normal.

The rule: **never spawn subagents at a fixed or assumed concurrency number.** Concurrency is always derived from the actual detected memory of the machine this is running on, checked fresh before each batch — not assumed from the plan, not copied from a prior session, not guessed from the project's apparent size.

## Step 1 — Detect available RAM before spawning anything

Before the first subagent is spawned in a session, detect actual system memory. Use whichever of these fits the OS/environment (try in order, use the first that works):

- Linux: `free -h` (or parse `/proc/meminfo` — `MemAvailable` is the figure that matters, not `MemTotal`, since it already accounts for reclaimable cache)
- macOS: `vm_stat` combined with `sysctl hw.memsize` for total, or `top -l 1 -s 0 | grep PhysMem`
- Windows: `Get-CimInstance Win32_OperatingSystem | Select FreePhysicalMemory,TotalVisibleMemorySize` (PowerShell) or `wmic OS get FreePhysicalMemory,TotalVisibleMemorySize`
- Container/sandboxed environments: check for a cgroup memory limit (`/sys/fs/cgroup/memory.max` or `memory.limit_in_bytes`) in addition to host RAM — a container's effective ceiling is often lower than the host's, and that lower number is the one that matters.

If detection fails outright (permission denied, command unavailable, running somewhere none of the above applies): **do not assume a generous default.** Fall back to sequential execution (no subagents) and note in the execution log that resource detection was unavailable, so the constraint is visible rather than silently skipped.

## Step 2 — Compute a safe subagent budget, not a guess

1. Take detected *available* memory (not total) as the starting budget.
2. Reserve a floor for the OS, the main agent process, and anything else already running — don't plan to use memory that's already spoken for. A reasonable default reservation is the greater of 20% of total RAM or 1–2 GB, whichever is larger, adjusted down only if you have concrete evidence the baseline footprint is smaller.
3. Estimate the per-subagent memory footprint for the actual work about to run (a subagent compiling a large project needs far more than one editing a config file — don't use one flat number for every task type; base the estimate on what this specific batch of subagents will actually do).
4. Max concurrent subagents = floor((available − reserved) / per-subagent estimate), with a hard ceiling of never exceeding available memory even in the best case — round down, never up, when the division isn't clean.
5. If that number comes out at 1 or below, don't spawn subagents at all for this batch — execute sequentially instead. Sequential-but-safe beats parallel-but-risks-OOM every time; this skill's non-negotiables (no known gaps, no silent failures) already assume execution completes correctly, and an OOM kill mid-task is exactly the kind of silent, unrecoverable failure this skill exists to prevent.

## Step 3 — Re-check before every batch, not just once per session

Available memory changes as the session runs — other processes start, caches grow, prior subagents may not have fully released memory. Re-run Step 1's detection before spawning each new batch of subagents, not just at the start of Phase 1. Treat a stale memory reading the same way you'd treat a stale masterplan assumption: don't trust it past the point where reality could have changed.

## Step 4 — Monitor and back off during execution, don't just gate at the start

Where the environment allows checking memory usage mid-run, poll periodically while subagents are active. If usage approaches the safety margin from Step 2 (e.g. crosses ~85% of the available budget), stop spawning new subagents for the current batch and let in-flight ones finish before continuing — don't wait for an actual OOM to react. If a subagent is killed or fails in a way consistent with an OOM despite this, treat it as a Blocker for this phase: reduce the concurrency budget, retry that unit of work alone if needed, and log what happened in `docs/masterplan/execution-log.md` so the constraint is visible for future phases/sessions on this same machine.

## Step 5 — Log the resource profile, not just the outcome

Record in the execution log, per phase that used subagents: detected available RAM, the concurrency budget computed from it, and how many subagents actually ran. This is what lets a future session on the same or a different machine make a correct decision immediately instead of rediscovering the constraint the hard way.

## Non-negotiables

- Never hardcode a subagent concurrency number into the plan or the code — it must always be derived from a fresh detection.
- Never treat "it worked on my machine" as proof it's safe — the whole point is this adapts per machine, per session.
- When in doubt or detection is unavailable, default to sequential. An unnecessarily slow but correct execution is always preferable to a fast one that risks an OOM mid-phase.
