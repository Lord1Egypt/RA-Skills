---
name: local-inference-context
description: >
  Context management for self-hosted LLM backends (llama.cpp, Ollama).
  Prevents mid-task 503 errors and context overflows caused by VRAM-limited
  KV caches. Use instead of generic context skills when running a local
  inference server. Complements context-recovery for post-compaction scenarios.
metadata:
  openclaw:
    emoji: 🦙
    os: ["linux", "darwin"]
---

# Local Inference Context

Generic context skills assume a reliable, large-context cloud provider.
Local backends (llama.cpp, Ollama) have a different failure profile:
the **KV cache is bounded by VRAM**, the server can return 503 before
OpenClaw's compaction logic triggers, and the compaction model is the
*same* overloaded local model. This skill addresses that reality.

---

## Why local backends fail differently

| Cloud provider | Local llama.cpp / Ollama |
|---|---|
| Context limit is a soft API error, OpenClaw retries after compaction | KV-cache fills up, server returns 503 or `context length exceeded` mid-request |
| Compaction uses same model, which is always available | Compaction uses same overloaded local model — may also fail |
| Context window is exactly what the API reports | Effective context = min(configured `--ctx-size`, available VRAM for KV cache) |
| No idle slot eviction | Idle slots can be evicted; server returns "Loading model" 503 on next request |

**The practical consequence:** on a GPU-constrained setup (e.g. a 24 GB card
running a 27B Q5 model), the usable KV-cache budget is roughly 5–8 GB.
At 32k tokens configured context, that fills up faster than the configured
limit suggests. Treat 50 % fill as amber and 70 % as red — not 60/80 %.

---

## Calibrating your effective context budget

Before a long session, run this once to understand your actual headroom:

```bash
# Check VRAM headroom
nvidia-smi --query-gpu=memory.used,memory.free,memory.total \
  --format=csv,noheader,nounits

# Check llama.cpp slot state
curl -s http://localhost:8081/slots | python3 -m json.tool
```

If `memory.free` is less than 4 GB, treat the session as already amber
regardless of what `/status` reports. Log the result to memory:

```
VRAM free: X MB — effective context budget: reduced
```

---

## Thresholds for local backends

| Fill level | State | Action |
|---|---|---|
| < 50 % | Green | Proceed normally |
| 50–69 % | Amber | Trim tool outputs, flush key facts to memory |
| 70–84 % | Red | Checkpoint, offer `/compact` before continuing |
| ≥ 85 % | Critical | Stop expanding. Compact or `/new` before next tool call |

Check `/status` at session start and after any tool call that returns
more than ~200 lines of output.

---

## Recognising a local backend failure

These are **server-side errors**, not OpenClaw compaction events.
They require a different response than a normal context overflow:

| Signal | Meaning |
|---|---|
| HTTP 503 with body `"loading model"` | Idle slot was evicted; model is reloading. Wait 10–30 s, then retry once. |
| HTTP 503 with body `"no slot available"` | All slots busy or KV cache full. Do NOT retry immediately — compact first. |
| `context length exceeded` in error | Hard KV-cache overflow. Compact or start `/new` before any retry. |
| Sudden very slow response then timeout | KV cache thrashing — reduce context before next request. |

**Never retry a 503 "no slot available" or context overflow without first
reducing context.** Retrying makes the problem worse by sending the same
oversized payload again.

---

## Pre-task checklist for long operations

Before any task you expect to span more than 4 turns (file edits, debugging
sessions, multi-step setups):

1. Run `/status` — note current fill %.
2. Check `nvidia-smi` if fill is already above 40 %.
3. Estimate token cost of the task:
   - Each file read ≈ 500–3000 tokens depending on file size
   - Each `exec` result ≈ 200–1500 tokens
   - Each `web_fetch` ≈ 1000–4000 tokens
4. If estimated total would push past 70 %, split into phases and tell
   the user upfront.

---

## Amber state (50–69 %): lean tool hygiene

Apply these habits to every tool call in amber state:

```bash
# Instead of reading entire files:
sed -n '1,50p' /path/to/file          # first 50 lines
grep -n "error\|warn\|fail" logfile   # targeted grep
tail -100 /var/log/syslog             # recent entries only

# Instead of verbose exec output:
some-command 2>&1 | tail -30
systemctl status service --no-pager --lines=20

# Summarise large outputs in one sentence, then discard them:
# "Command succeeded. Key values: port=8081, pid=12345"
```

Write key values to memory immediately after each tool call — do not
rely on them surviving a compaction summary intact.

---

## Red state (70–84 %): checkpoint before continuing

1. Write a checkpoint to memory now:

```markdown
## Checkpoint [timestamp]
Status: [what is done]
Pending: [what is next]
Critical values: [file paths, ports, error codes, config keys]
```

2. Tell the user:

> ⚠️ Context at ~N % (local backend — conservative threshold).
> I've saved progress to memory. Recommend `/compact Focus on [task]`
> before continuing. Or `/new` for a clean session.

3. If continuing, use `/compact Focus on <current task>` — not bare
   `/compact`. The local model needs a focused instruction to produce
   a useful summary under memory pressure.

---

## Critical state (≥ 85 %): stop and recover

Do not issue any more tool calls that expand context.

1. Write the checkpoint (see above).
2. Send the user a recovery message:

```
🛑 Context critical (~N %). Stopping to prevent a server error.

Done: [X]
Pending: [Y]
Key info: [Z]

Options:
  /compact Focus on [task]   — summarise and continue
  /new                       — fresh session (I'll reload from memory)
```

3. Wait for the user to choose. Do not attempt to continue on your own.

---

## After a 503 or context-overflow error

If the server already returned an error before you could act:

1. **Do not panic and do not retry the same request.**
2. Check the error type:
   - `"loading model"` → wait 15–30 s, then retry once with a minimal message.
   - `"no slot available"` or `context length exceeded` → compact first.
3. Run `/compact Focus on [what you were doing]`.
4. After compaction, verify the slot is ready:
   ```bash
   curl -s http://localhost:8081/health
   # expect: {"status":"ok"}
   ```
5. Re-read any file paths or config values from memory or disk —
   do not trust the compaction summary to have preserved them verbatim.
6. Resume with a short, targeted first message to re-establish the
   session before loading more context.

---

## Compaction model — required, not optional

Without a dedicated compaction model, OpenClaw uses the same local model
for summarisation — the identical model whose KV cache just caused the
overflow. This means compaction will likely fail or produce a degraded
summary. **A separate compaction model is a prerequisite for this skill
to work reliably, not an optional optimisation.**

The compaction model should run on a different machine or a second
inference instance with its own memory budget. It does not need to be
powerful — it only needs to summarise text faithfully and follow
instructions. A 7B–8B model is sufficient.

**Recommended model:** `qwen2.5:7b` via Ollama (fits in ~5 GB RAM/VRAM,
fast, excellent at summarisation and instruction-following).
Fallback if speed is critical: `llama3.2:3b` (~2 GB).

```json
{
  "agents": {
    "defaults": {
      "compaction": {
        "model": "ollama/qwen2.5:7b",
        "notifyUser": true,
        "memoryFlush": {
          "model": "ollama/qwen2.5:7b"
        }
      }
    }
  },
  "providers": {
    "ollama": {
      "baseUrl": "http://<COMPACTION-SERVER-IP>:11434"
    }
  }
}
```

**Without this configuration, the skill provides partial benefit only:**
the conservative thresholds and lean tool habits reduce overflow frequency,
but cannot recover reliably once an overflow occurs.

---

## Slash command reference

| Command | When to use |
|---|---|
| `/status` | Check fill % — use at session start and after large tool outputs |
| `/context list` | See which injected files and skills consume the most tokens |
| `/compact Focus on <topic>` | Guided compaction — always specify focus on a local backend |
| `/new` | Clean slate — fastest recovery when context is critical |
| `/usage tokens` | Per-reply token counter — useful for calibrating estimates |

---

## Relationship to other skills

| Skill | When to use instead |
|---|---|
| `context-recovery` | After compaction on any backend — recovers lost context via channel history |
| `context-budgeting` | Cloud providers or stable local setups — heartbeat-based GC at >80 % |
| `context-clean-up` | Diagnosing chronic context bloat — ranked offender audit |
| `context-anchor` | Post-compaction orientation via memory file scan |

Use `local-inference-context` **before** problems occur and `context-recovery`
**after** compaction if context was lost.
