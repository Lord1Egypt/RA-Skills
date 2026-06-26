---
name: langfuse-trace-logger
version: 1.0.0
description: "Log subagent task completions as Langfuse traces for replay, evaluation, and cost analysis. Called during session-wrap Phase 4. Supports backfill, tag-based filtering, and replay-judge integration. Requires Python 3.11 via chatterbox-venv due to pydantic v1 compatibility."
metadata:
  {
    "openclaw": {
      "emoji": "📈",
      "requires": {
        "bins": ["python3"],
        "env": ["LANGFUSE_PUBLIC_KEY", "LANGFUSE_SECRET_KEY"]
      },
      "primaryEnv": "LANGFUSE_PUBLIC_KEY",
      "network": {
        "outbound": true,
        "reason": "Writes trace records to the user's Langfuse instance (self-hosted at localhost:3100 or cloud). No data leaves the user's infrastructure when using the self-hosted instance."
      },
      "security_notes": "Writes traces to the user's own Langfuse instance (self-hosted Docker container at localhost:3100 by default). When using self-hosted Langfuse, all trace data stays on the user's machine. Cloud Langfuse users send data only to their own Langfuse account."
    }
  }
---

# Skill: langfuse-trace-logger

**Purpose:** Log subagent task completions as Langfuse traces for replay, evaluation, and cost analysis.
**Scope:** Called by Loki at the end of every session wrap (Phase 4) for each significant subagent completion.
**Script:** `/Users/loki/.openclaw/workspace/scripts/langfuse-trace-logger.py`

---

## ⚠️ CRITICAL: Python Version

**Always use `~/.chatterbox-venv/bin/python3` (Python 3.11.15)**

The langfuse SDK uses pydantic v1, which is incompatible with Python 3.14. Running with system Python (`python3`) or pyenv Python (3.14.x) causes **silent failure** — no import error, no exception, trace just doesn't appear in Langfuse UI. This will waste 30+ minutes of debugging.

```bash
# ✅ Correct
~/.chatterbox-venv/bin/python3 scripts/langfuse-trace-logger.py ...

# ❌ Wrong — silent failure on Python 3.14
python3 scripts/langfuse-trace-logger.py ...
/Users/loki/.pyenv/versions/3.14.3/bin/python3 scripts/langfuse-trace-logger.py ...
```

---

## Basic Invocation

```bash
~/.chatterbox-venv/bin/python3 /Users/loki/.openclaw/workspace/scripts/langfuse-trace-logger.py \
  --session-id "$SESSION_ID" \
  --parent-id "agent:main" \
  --agent "kit" \
  --task "task-label-kebab-case" \
  --model "anthropic/claude-sonnet-4-6" \
  --status "completed" \
  --input "full task prompt given to agent (first 4000 chars)..." \
  --output "what the agent returned or accomplished..." \
  --duration 278 \
  --tokens 16900 \
  --project "reddi-agent-protocol" \
  --skills "product-tour-capture"
```

---

## Trace Schema

| Field | Type | Purpose | Notes |
|---|---|---|---|
| `--session-id` | string | Subagent session key | Use actual subagent session key — enables lineage tracing |
| `--parent-id` | string | Parent session reference | Always `"agent:main"` unless nested subagent |
| `--agent` | string | Agent name | Lowercase: kit, archie, sara, finn, quill, etc. |
| `--task` | string | Task label (kebab-case) | Used for replay grouping: `replay-judge.py --tag "task:kit-setup-rebuild"` |
| `--model` | string | Model used | e.g. `anthropic/claude-sonnet-4-6`, `anthropic/claude-haiku-4-5` |
| `--status` | string | Outcome | `completed` / `partial` / `failed` |
| `--input` | string | Full task prompt | First 4000 chars — this is what gets replayed against other models in judge runs |
| `--output` | string | Result summary | Agent's output/result — this is what the judge scores |
| `--duration` | int | Time in seconds | Used for efficiency analysis and agent routing decisions |
| `--tokens` | int | Total tokens used | Used for cost analysis and budget governance |
| `--project` | string | Project slug | Must match `projects/<slug>/STATUS.md` — enables project-level filtering |
| `--skills` | string | Comma-separated skills | e.g. `"product-tour-capture,ffmpeg-studio"` — enables skill effectiveness filtering |

### Tag Taxonomy

The logger automatically generates these tags from the fields above:
- `agent:kit` — from `--agent`
- `model_family:claude-sonnet` — derived from `--model`
- `project:reddi-agent-protocol` — from `--project`
- `skill:product-tour-capture` — one tag per skill in `--skills`
- `task:kit-setup-rebuild` — from `--task`
- `status:completed` — from `--status`

These tags power the replay-judge filter syntax.

---

## Backfill Pattern

For retroactive logging when a session wrap was skipped or traces are missing.

**Idempotent:** Uses deterministic trace IDs based on `date+agent+task` hash. Safe to re-run — won't create duplicates.

```bash
# Preview first (dry run)
~/.chatterbox-venv/bin/python3 scripts/langfuse-backfill-historical.py \
  --from-date 2026-03-24 \
  --to-date 2026-03-24 \
  --dry-run

# Then run for real
~/.chatterbox-venv/bin/python3 scripts/langfuse-backfill-historical.py \
  --from-date 2026-03-24 \
  --to-date 2026-03-24
```

**Data source:** Backfill parses `memory/YYYY-MM-DD.md` files and extracts structured task outcome blocks. This is why the task outcome block format in memory files must be consistent — inconsistent format breaks parsing silently.

**Backfill ID format:** `backfill-YYYY-MM-DD-<agent>-<task-slug>` — deterministic, no duplicate risk.

---

## Replay and Judge

```bash
# Report on all Kit traces (past 30 days)
~/.chatterbox-venv/bin/python3 scripts/replay-judge.py \
  --tag "agent:kit" --report

# Compare all Kit traces against Haiku (cost reduction analysis)
~/.chatterbox-venv/bin/python3 scripts/replay-judge.py \
  --tag "agent:kit" --models "claude-haiku-4-5" --judge "claude-haiku-4-5" --report

# Judge a specific trace
~/.chatterbox-venv/bin/python3 scripts/replay-judge.py \
  --trace-id "backfill-2026-03-24-kit-setup-rebuild" \
  --models "claude-haiku-4-5" --judge "claude-haiku-4-5"

# Filter by project
~/.chatterbox-venv/bin/python3 scripts/replay-judge.py \
  --tag "project:reddi-agent-protocol" --report

# Filter by skill
~/.chatterbox-venv/bin/python3 scripts/replay-judge.py \
  --tag "skill:product-tour-capture" --report
```

---

## Verify Traces Appeared

After logging, verify in Langfuse UI: **http://localhost:3100**

Or check programmatically:

```bash
~/.chatterbox-venv/bin/python3 -c "
import subprocess
sk = subprocess.run(
    ['op', 'read', 'op://OpenClaw/Langfuse (Local)/credential'],
    capture_output=True, text=True
).stdout.strip()
from langfuse import Langfuse
lf = Langfuse(public_key='pk-lf-openclaw-local', secret_key=sk, host='http://localhost:3100')
traces = lf.client.trace.list(limit=5)
[print(t.name, t.id[:12]) for t in traces.data]
"
```

Expected output: last 5 trace names + truncated IDs. If blank, Python version issue (see warning above).

---

## Langfuse Connection Details

| Setting | Value |
|---|---|
| UI | http://localhost:3100 |
| Public key | `pk-lf-openclaw-local` |
| Secret key | `op://OpenClaw/Langfuse (Local)/credential` (1Password) |
| Also in 1Password | `op://OpenClaw/Langfuse (Local)/Secret Key` |
| Docker | Always running (daemon service) |

---

## When to Call This Skill

This skill is called during **Phase 4 (Traces)** of the session-wrap playbook (`playbooks/session-wrap/PLAYBOOK.md`).

**Call once per significant subagent completion.** Use data from the task outcome blocks written in Phase 1 (memory file). Don't reconstruct from memory — read what you just wrote.

**Minimum threshold for logging:** Any subagent run that produced a deliverable (file written, API called, analysis produced). Skip: simple lookups, 1-line tool calls, failed attempts with no output.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Trace doesn't appear in UI | Wrong Python version | Use `~/.chatterbox-venv/bin/python3` |
| No output, no error | Same — Python 3.14 pydantic v1 incompatibility | Same fix |
| `ImportError: langfuse not found` | Wrong venv | Same fix |
| Duplicate traces on backfill | Shouldn't happen — backfill is idempotent | Check if running logger + backfill both for same trace |
| `op: command not found` | 1Password CLI not in PATH | Run from shell with OP_SERVICE_ACCOUNT_TOKEN set, or source `~/.zshrc` first |
| Langfuse UI empty after logging | Docker daemon down | `docker ps` — restart Langfuse container if needed |
