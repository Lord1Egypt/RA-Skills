# OpenClaw Failure Patterns Catalog

Extracted from real gateway logs (53,249 error lines across 3 weeks of production operation). Each pattern includes frequency data, detection commands, root cause, and fix procedure.

## Table of Contents

1. [Lane Deadlock](#1-lane-deadlock)
2. [Session Bloat & Compaction Timeout](#2-session-bloat--compaction-timeout)
3. [Bootstrap Truncation](#3-bootstrap-truncation)
4. [Auth Profile Missing](#4-auth-profile-missing)
5. [Multi-Model Failover Cascade](#5-multi-model-failover-cascade)
6. [Rate Limiting & Cooldown Overlap](#6-rate-limiting--cooldown-overlap)
7. [Gateway Heap OOM](#7-gateway-heap-oom)
8. [Sandbox Escape Writes](#8-sandbox-escape-writes)
9. [Tool Edit Failures](#9-tool-edit-failures)
10. [Config Reload Stalls](#10-config-reload-stalls)

---

## 1. Lane Deadlock

**Frequency:** 4,605 stuck-session warnings in 3 weeks
**Severity:** Critical — agent appears completely dead

**Detection:**
```bash
grep "stuck session.*agent:main:main" ~/.openclaw/logs/gateway.err.log | tail -10
```
**Symptoms:**
- Agent stops responding to all interactive messages (Telegram, Discord, CLI)
- Gateway is running (launchd shows healthy) but processes nothing
- `openclaw cron edit` and other CLI commands hang or timeout
- Log shows repeating `stuck session: sessionId=... sessionKey=agent:main:main state=processing age=XXXs`

**Root cause:** A cron job or long-running task occupies `agent:main:main`, blocking the queue. Every new interactive message stacks behind it. If the task runs on a short interval (e.g., every 5 min with a 5-min timeout), the lock never releases.

**Fix:**
1. First try the safe path: restart gateway and use normal OpenClaw cron commands once the CLI responds again.
2. If the gateway is fully wedged and the bad cron immediately re-locks the system, use **break-glass recovery**: make a timestamped backup of `~/.openclaw/cron/jobs.json`, disable or remove only the offending job, and validate the file with `jq` before restart.
3. After recovery, re-create or fix the job using normal OpenClaw cron commands — do not leave the system depending on hand-edited state.
4. Restart gateway: `launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway`

**Prevention:** Run the cron lane validator before deploying any new cron job. The session-health-watchdog catches this automatically.

---

## 2. Session Bloat & Compaction Timeout

**Frequency:** 34 compaction events logged, including repeated failures on same session
**Severity:** Critical — session becomes unusable, can cascade to OOM

**Detection:**
```bash
find ~/.openclaw/agents/main/sessions -name "*.jsonl" -exec ls -lh {} \; | awk '$5 ~ /M/ {print}' | sort -k5 -h
grep "compaction.*timeout\|compaction.*failed" ~/.openclaw/logs/gateway.err.log | tail -10
```
**Symptoms:**
- Specific session stops responding while others work
- Log shows compaction attempts that timeout at 600s
- Session `.jsonl` file is 5MB+ (critical at 10MB+)
- Compaction safeguard messages: "dropped N older chunk(s)"

**Root cause:** Sessions grow linearly with every message exchange. High-traffic channels (Telegram groups, automated pipelines) accumulate thousands of messages. Once a session exceeds the compaction window, it enters a death spiral — compaction tries, times out, session grows further.

**Fix:**
1. Archive the session: `cp ~/.openclaw/agents/main/sessions/<id>.jsonl ~/backups/`
2. Remove from registry: edit `~/.openclaw/agents/main/sessions/sessions.json` to remove the entry
3. The agent will create a fresh session on next message to that channel

**Prevention:** Monitor session sizes with the watchdog. For high-traffic channels, consider periodic session rotation.

---

## 3. Bootstrap Truncation

**Frequency:** Observed at 94% utilization (18,790 / 20,000 chars) causing cascading failures
**Severity:** High — agent loses instructions silently

**Detection:**
```bash
bash scripts/bootstrap-budget-check.sh
# or quick check:
wc -c < ~/.openclaw/workspace/AGENTS.md
```
**Symptoms:**
- Agent "forgets" rules from later sections of AGENTS.md
- Compaction produces garbled summaries
- New sessions start with incomplete context
- Agent behavior is inconsistent between sessions

**Root cause:** AGENTS.md has a hard 20,000 character limit. Content beyond this is silently truncated during bootstrap. Organic growth from adding new workflows, delegation rules, etc. causes gradual creep.

**Fix:**
1. Run `bootstrap-budget-check.sh` to see section-by-section breakdown
2. Move verbose sections to `AGENTS-REFERENCE.md`
3. Keep only identity, core rules, and critical workflow summaries in AGENTS.md
4. Target 50-70% utilization

**Prevention:** Include bootstrap budget check in nightly consolidation cron.

---

## 4. Auth Profile Missing

**Frequency:** 3,802 `No API key found` errors in 3 weeks
**Severity:** Medium — specific model unavailable, failover may compensate

**Detection:**
```bash
grep "FailoverError: No API key" ~/.openclaw/logs/gateway.err.log | \
  grep -oE 'provider "[^"]+"' | sort | uniq -c | sort -rn
```
**Symptoms:**
- Specific model never gets used despite being configured
- Repeated `FailoverError: No API key found for provider "X"` in logs
- Agent falls back to other models but may degrade in quality

**Root cause:** Two-layer auth system — global `openclaw.json` declares providers, but `~/.openclaw/agents/main/agent/auth-profiles.json` must have a matching entry with the actual key reference.

**Fix:**
Add to `auth-profiles.json`:
```json
{
  "profiles": {
    "<provider>:default": {
      "keyRef": "<ENV_VAR_NAME>"
    }
  },
  "lastGood": {
    "<provider>": "<provider>:default"
  }
}
```

**Prevention:** After adding any new model provider, immediately verify auth with: `openclaw models test <provider>/<model>`

---

## 5. Multi-Model Failover Cascade

**Frequency:** 238 timeouts + 106 overloaded + 68 rate limits = 412 failover events
**Severity:** Medium — usually self-healing, critical only if all providers down
**Detection:**
```bash
grep "FailoverError" ~/.openclaw/logs/gateway.err.log | \
  grep -oE 'FailoverError: [^.]+' | sort | uniq -c | sort -rn | head -10
grep "timeout next=" ~/.openclaw/logs/gateway.err.log | \
  grep -oE 'next=[^ ]+' | sort | uniq -c | sort -rn
```

**Symptoms:**
- Occasional slow responses (failover adds latency)
- Log shows cascading `timeout provider=X next=Y` entries
- In worst case, all providers in cooldown simultaneously

**Root cause:** LLM providers have rate limits, capacity limits, and occasional outages. The failover chain handles this gracefully — unless every provider is unavailable at once.

**Fix (if all providers down):**
1. Check provider status pages
2. Clear cooldowns: restart gateway
3. Consider adding more providers to the chain

**Prevention:** Maintain 3+ providers in the failover chain. Stagger rate limit windows. Monitor `rate_limit window=cooldown` log entries.

---

## 6. Rate Limiting & Cooldown Overlap

**Frequency:** 494 rate_limit events, 247 explicit 429 responses
**Severity:** Medium — causes temporary model unavailability
**Detection:**
```bash
grep "rate_limit" ~/.openclaw/logs/gateway.err.log | \
  grep -oE 'provider=[^ ]+' | sort | uniq -c | sort -rn
```

**Symptoms:**
- Bursts of 429 errors followed by cooldown periods
- Agent responses slow down during peak usage
- Specific providers cycle through available/cooldown states

**Root cause:** Cron jobs + interactive use + subagent spawning can exceed provider rate limits. Each 429 puts the provider in a cooldown window. If multiple providers hit cooldown simultaneously, no model is available.

**Fix:** Spread cron schedules to avoid clustering. Reduce cron frequency for non-critical jobs. Use cheaper models for routine tasks.

---

## 7. Gateway Heap OOM

**Frequency:** 6 OOM events, 2 FATAL heap limit crashes
**Severity:** Critical — gateway process dies, launchd respawns

**Detection:**
```bash
grep "FATAL ERROR.*heap limit\|JavaScript heap out of memory" ~/.openclaw/logs/gateway.err.log
```

**Symptoms:**
- Gateway suddenly stops, then restarts (launchd respawn)
- Brief total outage (30-60 seconds)
- Often preceded by processing a very large session
**Root cause:** Node.js default heap limit (~1.5GB) exceeded when processing oversized session files. The gateway loads entire session histories into memory for compaction.

**Fix:**
1. Clear the oversized session (see Pattern 2)
2. Increase Node.js heap: add `--max-old-space-size=4096` to the launchd plist

**Prevention:** Keep sessions under 5MB. The watchdog catches this before OOM occurs.

---

## 8. Sandbox Escape Writes

**Frequency:** 8+ `Path escapes sandbox` write failures
**Severity:** Low — write silently fails, agent retries or gives up

**Detection:**
```bash
grep "write failed: Path escapes sandbox" ~/.openclaw/logs/gateway.err.log | tail -10
```

**Symptoms:**
- Agent reports it "saved" a file but the file doesn't exist
- Writes to `/tmp/`, home directory, or other non-workspace paths fail
- Agent tries creative workarounds that also fail

**Root cause:** The agent's file sandbox restricts writes to `~/.openclaw/workspace/`. Common when the agent tries to use `/tmp/` for intermediate files, or when instructions reference absolute paths outside the workspace.

**Fix:** Update AGENTS.md to explicitly instruct workspace-relative paths for all file operations. Use `workspace/tmp/` instead of `/tmp/`.
---

## 9. Tool Edit Failures

**Frequency:** 30+ edit failures, 7 "path changed during write" errors
**Severity:** Low — individual operation fails, agent usually retries

**Detection:**
```bash
grep "edit failed" ~/.openclaw/logs/gateway.err.log | \
  grep -oE 'edit failed: [^.]+' | sort | uniq -c | sort -rn
```

**Common causes:**
- "Could not find the exact text" — file changed between read and edit (race condition with crons)
- "Found N occurrences" — edit target isn't unique, needs more context
- "path changed during write" — concurrent file modification

**Fix:** For race conditions, ensure crons that modify the same files don't overlap in schedule. For non-unique matches, use longer context strings in edit operations.

---

## 10. Config Reload Stalls

**Frequency:** 19 reload events, 10 restart failures
**Severity:** Medium — config changes don't take effect until gateway fully restarts

**Detection:**
```bash
grep "reload\|restart failed" ~/.openclaw/logs/gateway.err.log | tail -10
```
**Symptoms:**
- Config changes (editing `openclaw.json`) don't take effect
- Gateway reports "deferring until N operation(s) complete" indefinitely
- `restart failed (Bootstrap failed: 5: Input/output error)` or `(spawnSync launchctl ETIMEDOUT)`

**Root cause:** Gateway defers config reloads while operations are in progress. If operations never complete (stuck session), the reload never happens. Restart attempts can fail if launchd is also stuck.

**Fix:**
1. Wait for active operations to finish, or
2. Force restart: `launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway`
3. If launchd is stuck: `launchctl bootout gui/$(id -u)/ai.openclaw.gateway && launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist`

**Prevention:** Avoid editing config during peak cron execution windows. Batch config changes together.