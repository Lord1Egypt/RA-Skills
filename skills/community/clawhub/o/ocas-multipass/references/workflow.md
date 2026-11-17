# Multipass — Workflow

Four phases. Task first, tools second, execution third, report last.

## Phase 1: Plan

Understand the task. What outcome does the user need?

Generate 2-3 approaches ranked by self-sufficiency. Lead with the approach that needs the least external tooling. Many tasks have a no-signup path.

Check runtime config (see `references/orchestration.md` §Config check). If `maxSpawnDepth < 2`, run single-threaded. If mcporter is not installed, mark MCP-by-URL as unavailable and fall back to direct HTTP for MCP servers.

Write `manifest.json` with status `planned`.

## Phase 2: Fill Gaps

If the selected approach has no gaps, skip to Phase 3.

**Adaptive complexity:**
- Simple (1 gap, obvious): inline search, no workers.
- Moderate (2-3 gaps): 1-2 targeted workers.
- Complex (4+): full parallel worker set.

If `sessions_spawn` fails when spawning a worker, fall back to inline execution for that surface. Do not stop.

Discovery workers search surfaces (see `references/surfaces.md`), score candidates (see `references/scoring.md`), and write to `checkpoints/`. Orchestrator polls and merges.

**Resolution preference:**

1. Free API, no auth → `web_fetch`
2. Free API, key via signup → throwaway identity + `web_fetch`
3. MCP server → `mcporter call {url}.{tool}` or direct HTTP
4. Downloaded skill → read SKILL.md as context

**All network calls use retry logic** (see `references/resilience.md` §Retry). 3 attempts, exponential backoff, before skipping.

**Identity provisioning** (only when needed): create throwaway inbox from cascade in `references/resilience.md` §Identity. Use BotEmail first (longest-lived). If all providers fail, proceed without signup capability — restrict to no-auth candidates only.

**When a candidate fails** (signup blocked, gate hit, endpoint down):
- Skip to next candidate. If no candidates remain, try the next approach from Phase 1.
- If all approaches exhausted, apply reframing tactics from `references/resilience.md` §Reframing.
- If reframing fails, proceed to Phase 4 and produce a failure report.

**When a gate is hit** (CAPTCHA, browser login, SMS):
- Search installed skills and MCP servers for a handler (see `references/resilience.md` §Gates). Max search depth: 1 (do not search for handlers of handlers).
- If handler found, use it. If not, skip the service.

Write `manifest.json` with status `resolved`.

## Phase 3: Execute

Spawn `worker:execute` with the resolved tools and the fallback approach baked into the task description so it can pivot without returning to the orchestrator.

The worker:
- Calls APIs via `web_fetch` (with retry)
- Calls MCP servers via `mcporter call` by URL or direct HTTP
- Uses downloaded SKILL.md as context
- Uses session identity for signups
- Writes progress to `log.jsonl` and `checkpoints/execute.json` after every major step
- Writes `status.txt` one-liner for progress visibility

**If the execute worker hits a wall** (API error, rate limit, service down):
- Retry 3 times with backoff.
- If still failing, try the fallback approach.
- If fallback also fails, complete as much as possible and proceed to Phase 4.

## Phase 4: Report

Write to session directory:

**1. Task output** in `output/` — the deliverable. Even if partial.

**2. replay.md** — standalone recipe with health checks, version pins, and "what might break" section. See `references/resilience.md` §Replay health.

**3. manifest.json** — final status: `complete`, `partial`, or `failed`.
- `complete`: task fully accomplished.
- `partial`: some steps succeeded, some failed. Output contains what was accomplished. Manifest documents what remains.
- `failed`: no useful output produced. Manifest documents every approach tried, every candidate evaluated, every failure reason. This is still a useful artifact.

**4. Journal entry.**

Update `status.txt`: `[done] {one-line summary of outcome}`
