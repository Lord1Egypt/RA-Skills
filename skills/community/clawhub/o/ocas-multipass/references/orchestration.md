# Orchestration

Sub-agent architecture, adaptive complexity, checkpoint contracts, and failure recovery.

## Config check

Run during `multipass.init` and at the start of every `multipass.run`.

```bash
# Check spawn depth
# maxSpawnDepth >= 2: parallel mode
# maxSpawnDepth == 1: single-threaded (orchestrator does everything)
# maxSpawnDepth == 0: Multipass runs inline, no sub-agents

# Check mcporter
# which mcporter or npx -y mcporter --version
# Available: use mcporter call for MCP servers
# Not available: fall back to direct HTTP JSON-RPC (see resilience.md §mcporter)
```

Log the result to `manifest.json`:

```json
{
  "runtime": {
    "max_spawn_depth": 2,
    "parallel_mode": true,
    "max_children": 5,
    "max_concurrent": 8,
    "mcporter_available": true,
    "mcp_access_mode": "mcporter"
  }
}
```

If `maxSpawnDepth < 2`, proceed single-threaded. If `maxSpawnDepth == 0`, Multipass runs entirely inline -- no sub-agents, slower, still works.

## Adaptive complexity

Not every task needs four parallel workers. Match effort to complexity.

| Complexity | Gaps | Example | Workers |
|-----------|------|---------|---------|
| Simple | 1, obvious | "Get weather data" → Open-Meteo | 0 (inline search) |
| Moderate | 1-2, unclear | "Convert PDF to searchable text" | 1-2 targeted workers |
| Complex | 3+, broad | "Build a pipeline: scrape, parse, enrich, export" | Full parallel set (4) |

**Simple tasks**: the orchestrator searches 1-2 surfaces inline (no workers spawned). Check `references/scoring.md` §Known zero-auth free APIs first -- the answer may already be there.

**Moderate tasks**: spawn only the workers for the surfaces most likely to help. If the gap is "PDF parsing," searching the MCP registry and ClawHub is useful; searching public API directories probably isn't.

**Complex tasks**: spawn the full set.

This avoids paying 5x token cost for a task one inline search could answer.

## Worker definitions

| Worker ID | Surfaces | Timeout | Spawn for |
|-----------|----------|---------|-----------|
| `clawhub` | ClawHub API, Skills.sh, h4gen FTS index | 300s | moderate, complex |
| `mcp-registry` | MCP Registry, Glama, Smithery, PulseMCP | 300s | moderate, complex |
| `github` | GitHub Code Search, Agnxi sitemap | 300s | complex |
| `apis` | public-apis, RapidAPI, general web | 300s | moderate, complex |
| `execute` | n/a (uses resolved tools) | 0 | always (after resolution) |

## Spawn calls

Discovery worker:

```
sessions_spawn({
  task: "Search {surfaces} for capabilities: {gap descriptions}. Write results to {session_dir}/checkpoints/{worker_id}.json. Append progress to {session_dir}/log.jsonl. Read references/surfaces.md sections {N-M} for endpoints.",
  label: "multipass-{worker_id}-{session_id}",
  runTimeoutSeconds: 300
})
```

Execute worker:

```
sessions_spawn({
  task: "Execute task: {description}. Tools: {resolved tools with methods}. Throwaway email: {email or 'not needed'}. Write output to {session_dir}/output/. Log steps to {session_dir}/log.jsonl. Update checkpoint at {session_dir}/checkpoints/execute.json after each step. If a tool fails, try the alternative approach: {fallback}.",
  label: "multipass-execute-{session_id}",
  runTimeoutSeconds: 0
})
```

Note: the execute worker receives the fallback approach in its task description so it can pivot without returning to the orchestrator.

## Checkpoint contract

Every worker overwrites `checkpoints/{worker_id}.json` after each meaningful step.

**Discovery worker checkpoint:**

```json
{
  "worker_id": "clawhub",
  "status": "running|complete|failed",
  "started_at": "ISO 8601",
  "updated_at": "ISO 8601",
  "gaps_searched": ["pdf-extract"],
  "gaps_remaining": ["calendar-query"],
  "candidates": [
    {
      "name": "pdf-parse",
      "type": "skill",
      "source": "clawhub",
      "slug": "author/pdf-parse",
      "composite_score": 0.84,
      "sandboxable": true,
      "auth_gate": "none",
      "probe_status": "passed"
    }
  ],
  "error": null
}
```

**Execute worker checkpoint:**

```json
{
  "worker_id": "execute",
  "status": "running|complete|partial|failed",
  "updated_at": "ISO 8601",
  "steps_completed": [
    {"step": "fetch-data", "detail": "3 endpoints called, 12 pages received"}
  ],
  "steps_remaining": [
    {"step": "format-output"}
  ],
  "output_files": ["output/report.md"],
  "current_approach": "A",
  "approaches_tried": ["A"],
  "error": null
}
```

## Log contract

All workers append to shared `log.jsonl`. One JSON object per line.

```json
{"worker": "clawhub", "phase": "discover", "step": "search", "gap": "pdf-extract", "status": "complete", "detail": "5 candidates", "ts": "ISO 8601"}
{"worker": "execute", "phase": "execute", "step": "fetch-data", "gap": null, "status": "complete", "detail": "12 pages from Open-Meteo", "ts": "ISO 8601"}
{"worker": "execute", "phase": "execute", "step": "signup", "gap": null, "status": "skipped", "detail": "service rejected disposable email, trying next candidate", "ts": "ISO 8601"}
```

## Orchestrator polling

After spawning discovery workers:

```
every 15 seconds:
  read checkpoints/
  for each worker:
    if complete or failed → mark done
    if file not updated in 120s → mark timed out, use partial results
  update status.txt with current progress
  if all done → proceed to resolve
```

After spawning execute worker:

```
every 30 seconds:
  read checkpoints/execute.json
  update status.txt
  if complete or failed → proceed to report
```

The orchestrator reads the filesystem, not announce messages. Filesystem is reliable. Announces are not (per platform issue #17569, #33827).

## Recovery

| Scenario | Action |
|----------|--------|
| Discovery worker completes | Merge candidates |
| Discovery worker times out | Use partial candidates from checkpoint |
| Discovery worker crashes (no checkpoint) | Skip that surface group |
| All discovery fails | Report failure, suggest `multipass.search` manually |
| Execute worker times out | Read checkpoint for partial output, report what completed |
| Execute worker hits auth gate | Worker pivots to fallback approach (included in spawn task) |
| Execute worker crashes | Read checkpoint, report partial completion |
| Disposable email provider down | Try next in cascade (see `references/resilience.md`) |
| Service rejects disposable email | Skip service, try next candidate |

## Identity provisioning

When the orchestrator determines a throwaway inbox is needed (Phase 1 or Phase 2), it provisions one using the cascade in `references/resilience.md` §Identity cascade.

Store in `manifest.json`:

```json
{
  "session_identity": {
    "email": "...",
    "provider": "botemail.ai",
    "created_at": "ISO 8601",
    "auth": {"api_key": "..."}
  }
}
```

Pass the email to the execute worker in its spawn task. The worker reads it from `manifest.json` if it needs to sign up for a service.

## Session lifecycle

```
planned → filling_gaps → resolved → approved → executing → complete|partial|failed
```

Possible shortcuts:
- `planned → approved → executing` (no gaps, approach A works with installed tools + web_fetch)
- `planned → filling_gaps → resolved → approved → executing → partial` (some steps completed, some failed)

Each transition updates `manifest.json` and appends to `log.jsonl`.

## Concurrency safety

- `log.jsonl`: append-only, line-atomic. Multiple writers safe.
- `checkpoints/{id}.json`: one writer per file.
- `manifest.json`: orchestrator-only.
- `status.txt`: orchestrator-only.
- `workspace/`, `output/`: workers use unique filenames.
