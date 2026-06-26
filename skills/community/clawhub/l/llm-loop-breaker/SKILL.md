---
name: LLM Stream Guard
description: >
  Two-layer defense for Openclaw gateway: kills hallucinating LLM streams via
  entropy analysis, and watchdogs host CPU/RAM/Disk to prevent resource exhaustion.
metadata:
  openclaw:
    emoji: "\U0001F6E1"
    homepage: https://github.com/openclaw/clawhub
    os:
      - linux
    requires:
      bins:
        - node
        - python3
        - bash
      env:
        - OPENCLAW_APP_DIR
    install:
      - kind: node
        name: n/a
      - kind: uv
        name: psutil
    primaryEnv: OPENCLAW_APP_DIR
    skillKey: llm-stream-guard
---

# LLM Stream Guard

Two-layer runtime defense that protects the Openclaw gateway against
hallucinating LLM streams and host resource exhaustion.

## When to activate

Activate this skill **once per fresh gateway deployment** or whenever the
gateway binary (`openclaw.mjs`) is rebuilt / updated.

## What it does

### Layer 1 -- Stream Entropy Breaker (Node.js)

Patches `global.fetch` to intercept every LLM streaming response
(`text/event-stream`, `application/x-ndjson`, `application/stream+json`).

For each active stream it:

1. Accumulates text chunks and measures compressed-vs-raw byte ratio using
   zlib deflate (compression ratio = uncompressed / compressed).
2. Every 1024 bytes, schedules an entropy check via `process.nextTick`.
3. Once 4000+ bytes have been received, evaluates kill conditions:
   - **Hard kill**: compression ratio > 10.0
   - **Soft kill**: compression ratio > 6.0 AND single-character dominance > 50%
4. On kill: fires `AbortController.abort()` with reason
   `HALLUCINATION_LOOP_DETECTED_BY_ENTROPY_BREAKER`, severing the stream.

Bounded memory: accumulated text is truncated to the last 4096 characters
when it exceeds 8192. A 30-second registry cleanup removes stale streams.

### Layer 2 -- Host Resource Watchdog (Python)

Runs as a **separate daemon** outside the gateway process. Polls every 2
seconds via `psutil`.

| Rule | Trigger | Action |
|------|---------|--------|
| Redline breach | CPU >= 90% OR RAM >= 90% OR Disk >= 90% | Log warning + audit entry |
| Poison pill | Child process CPU > 95% with 0 I/O for 15 s | Kill process tree + incident snapshot |
| Memory leak | RSS monotonically grows > 100 MB over 60 s, CPU > 30% | Kill process tree + incident snapshot |
| Crash loop | Gateway PID changes 3+ times in 120 s | Incident snapshot + 30 s cooldown |

Incident snapshots capture `journalctl` and `dmesg` excerpts into
`~/.openclaw/workspace/memory/core/incidents/`.

## Deployment

Run the deterministic deploy script. It is safe to run multiple times
(idempotent).

```bash
export OPENCLAW_APP_DIR=/app          # path to openclaw installation root
bash deploy.sh
```

The script will:

1. Verify `python3`, `psutil`, and `$OPENCLAW_APP_DIR/openclaw.mjs` exist.
2. Copy runtime files to `$OPENCLAW_APP_DIR/dist/llm_stream_guard/`.
3. Inject bootstrap code into `openclaw.mjs` (skipped if already present).
4. Create a timestamped backup of `openclaw.mjs` before any modification.

After deployment, **restart the Openclaw gateway** to activate.

## Verify

```bash
# Node.js layer tests (no network, no side effects)
node test-entropy-breaker.js

# Python layer tests (mocked psutil, no real process interaction)
python3 test-watchdog.py
```

Both test suites are deterministic and produce exit code 0 on success, 1 on
failure.

## Files

| File | Purpose |
|------|---------|
| `src/stream-entropy-breaker.cjs` | Fetch-patching + stream transform + abort logic |
| `src/entropy-engine.cjs` | Zlib compression ratio calculator + repetition detector |
| `host-resource-watchdog.py` | System resource monitor daemon |
| `deploy.sh` | Deterministic deployment script |
| `test-entropy-breaker.js` | JS test suite (16 tests) |
| `test-watchdog.py` | Python test suite (14 tests) |

## Uninstall

Remove the injected block from `openclaw.mjs` (between the
`[LLM_STREAM_GUARD_START]` and `[LLM_STREAM_GUARD_END]` markers), delete
`$OPENCLAW_APP_DIR/dist/llm_stream_guard/`, and kill any running
`host-resource-watchdog.py` process.
