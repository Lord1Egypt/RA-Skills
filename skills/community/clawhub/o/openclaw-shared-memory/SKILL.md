---
name: "openclaw-memory"
description: "Reuse, inspect, search, or append shared OpenClaw memory on the current machine. Use when a request depends on remembered local servers, deploy hosts, internal services, script paths, runbooks, workspace conventions, or prior user preferences that may already exist in OpenClaw memory."
---

# OpenClaw Memory

Resolve the skill directory from this `SKILL.md` file, then use the bundled script at `scripts/openclaw_memory.py`.

## Data sources

- Long-term memory: `~/.openclaw/workspace/MEMORY.md`
- Daily memory: `~/.openclaw/workspace/memory/YYYY-MM-DD.md`
- Indexed chunk fallback: `~/.openclaw/memory/main.sqlite`

If `OPENCLAW_HOME` is set, use that as the root instead of `~/.openclaw`.

## Workflow

1. If the request names a known machine, service, workflow, or environment-specific noun, search memory before any live checks.
2. Prefer markdown files as the source of truth when inspecting or updating memory.
3. If markdown results are sparse, query SQLite chunk text as a fallback.
4. Extract concrete facts such as hostnames, IPs, ports, file paths, runbook steps, and user preferences.
5. When the user wants to persist something:
   - Write durable rules and preferences to `MEMORY.md`.
   - Write day-specific progress to `memory/YYYY-MM-DD.md`.
6. After writing, report the exact file that was updated.

## Constraints

- Do not claim semantic or vector retrieval is active unless you actually verified the runtime supports it.
- For Chinese queries, direct markdown scanning is often more reliable than SQLite tokenization.
- If the OpenClaw paths are missing, say so plainly and stop instead of inventing state.

## Commands

Replace `<skill-dir>` with the directory that contains this `SKILL.md`.

```bash
python3 <skill-dir>/scripts/openclaw_memory.py doctor
python3 <skill-dir>/scripts/openclaw_memory.py recent --limit 5
python3 <skill-dir>/scripts/openclaw_memory.py search --query "deploy host" --limit 8
python3 <skill-dir>/scripts/openclaw_memory.py append --scope daily --text "Confirmed the deploy host is healthy." --dry-run
python3 <skill-dir>/scripts/openclaw_memory.py append --scope long --text "- Always search both the workspace project tree and the main project tree."
```

## Output expectations

- For search, return compact results with path, source, score, and a short snippet.
- For append, print the destination path.
- For doctor, print which OpenClaw paths exist.
