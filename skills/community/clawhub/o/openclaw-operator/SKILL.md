---
name: openclaw-ops
description: "Diagnose and prevent OpenClaw agent failures — session bloat, lane deadlocks, bootstrap truncation, auth errors, compaction timeouts, and more. Use this skill whenever an OpenClaw agent stops responding, runs slowly, fails to process messages, throws gateway errors, or needs operational health checks. Also use when setting up cron jobs, configuring multi-model failover, or planning AGENTS.md changes. Trigger on: 'agent not responding', 'openclaw health', 'gateway errors', 'session stuck', 'cron not working', 'bootstrap too big', 'compaction timeout', 'auth failed', 'rate limited', or any OpenClaw troubleshooting request."
---

# OpenClaw Ops

Operational health diagnostics and design patterns for OpenClaw agents. This skill helps you diagnose why an agent stopped responding, fix the root cause, and install preventive guardrails so it doesn't happen again.

It covers two complementary areas: **ops diagnostics** (find and fix failures now) and **design patterns** (prevent failures structurally). It is opinionated toward the safest reliable path first, with break-glass recovery reserved for true gateway lockups.

## Quick Start: Agent Not Responding?

Run through this triage in order. Most outages are caused by the top 3.

1. **Lane deadlock** — A cron job on `agent:main:main` blocks all interactive messages. Check `~/.openclaw/cron/jobs.json` for any job with `"sessionKey": "agent:main:main"`. Fix: change to `agent:main:cron:<job-name>` or `agent:main:isolated`.
2. **Session bloat** — A session file over 5MB causes compaction timeouts (600s limit). Check `~/.openclaw/agents/main/sessions/` for large `.jsonl` files. Fix: archive the session and remove from `sessions.json`.
3. **Bootstrap truncation** — `AGENTS.md` exceeds the 20,000 char limit, causing compaction to timeout on the bloated bootstrap. Check: `wc -c < ~/.openclaw/workspace/AGENTS.md`. Fix: move verbose sections to `AGENTS-REFERENCE.md`.
4. **Auth failure** — Missing provider key in agent-level `auth-profiles.json`. Check gateway.err.log for `FailoverError: No API key found`. Fix: add the profile to `~/.openclaw/agents/main/agent/auth-profiles.json`.
5. **Gateway heap OOM** — Node.js runs out of memory processing oversized sessions. Check gateway.err.log for `FATAL ERROR: Reached heap limit`. Fix: clear the bloated session first, then restart gateway.

If none of these match, read `references/failure-patterns.md` for the full catalog of 10 failure categories extracted from real gateway logs.
## Bundled Scripts

Two battle-tested bash scripts are included in `scripts/`. They can be run standalone or registered as OpenClaw cron jobs.

### session-health-watchdog.sh

Comprehensive health check that monitors five areas in a single pass:
- Session file sizes (warn at 5MB, critical at 10MB)
- Stale session locks (warn at 10min, critical at 30min)
- Cron jobs routing to `agent:main:main` (always critical)
- AGENTS.md bootstrap budget utilization
- Recent stuck-session warnings in gateway.err.log (last 15 min)

**Run standalone:** `bash scripts/session-health-watchdog.sh`

**Register as cron (recommended every 30 min):**
```bash
openclaw cron add \
  --name "Session Health Watchdog" \
  --prompt "Run the session health watchdog and report results" \
  --cron "*/30 * * * *" \
  --session-key "agent:main:cron:health-watchdog" \
  --model openai-codex/gpt-5.4
```

The watchdog outputs either "all clear" with stats, or an alert summary with severity levels. It exits non-zero when problems are found, making it suitable for monitoring pipelines.
### bootstrap-budget-check.sh

Detailed AGENTS.md size analysis with section-by-section breakdown showing which sections consume the most budget. Uses visual bars and threshold alerts.

**Thresholds:**
- Green: below 75% — plenty of headroom
- Yellow: 75-85% — watch growth
- Orange: 85-95% — consolidate soon
- Red: 95%+ — will truncate, trim immediately

**Run standalone:** `bash scripts/bootstrap-budget-check.sh`

## Session Lane Architecture

Understanding session lanes is the single most important concept for OpenClaw reliability. Every message, cron job, and subagent runs in a "session lane" — a keyed slot that can only process one task at a time.

**The golden rule:** `agent:main:main` is the interactive lane. Never put cron jobs on it.

When a cron job runs on the main lane, every interactive message (Telegram, Discord, CLI) queues behind it. If the cron runs for 2+ minutes or gets stuck, the agent appears dead.

### Lane naming conventions

| Use case | Session key pattern | Example |
|----------|-------------------|---------|
| Interactive (Telegram, CLI) | `agent:main:main` | Reserved — never use for crons |
| Cron jobs | `agent:main:cron:<job-name>` | `agent:main:cron:recall-archiver` |
| Isolated one-shots | `agent:main:isolated` | Disposable tasks |
| Channel-specific | `agent:main:telegram:group:<id>` | Per-chat sessions |
### Validating cron lanes

Before deploying any cron job, verify its session key:
```bash
python3 -c "
import json
with open('$HOME/.openclaw/cron/jobs.json') as f:
    jobs = json.load(f)['jobs']
bad = [j['name'] for j in jobs if j.get('enabled', True) and j.get('sessionKey') == 'agent:main:main']
if bad:
    print(f'BLOCKED: {len(bad)} crons on main lane: {bad}')
else:
    print('All crons properly isolated.')
"
```

## Auth Configuration

OpenClaw uses a two-layer auth system. Global config (`openclaw.json`) declares available providers, but the agent needs its own `auth-profiles.json` to actually authenticate.

**Common mistake:** Adding a provider to global config but forgetting the agent-level profile. The gateway silently tries and fails, logging `FailoverError: No API key found for provider "X"`.

**Fix pattern:**
```json
// ~/.openclaw/agents/main/agent/auth-profiles.json
{
  "profiles": {
    "provider-name:default": {
      "keyRef": "ENV_VAR_NAME"
    }
  },
  "lastGood": {
    "provider-name": "provider-name:default"
  }
}
```

After adding, verify: `grep "FailoverError.*API key" ~/.openclaw/logs/gateway.err.log | tail -5`
## Multi-Model Failover

OpenClaw routes through model providers in a failover chain. When the primary model rate-limits or times out, it cascades to the next. Understanding this chain prevents false alarms.

**Common failover errors (from real logs):**
- `FailoverError: LLM request timed out` — provider slow, failover kicked in (238 occurrences in 3 weeks)
- `FailoverError: API rate limit reached` — 429 from provider (68 occurrences)
- `FailoverError: The AI service is temporarily overloaded` — 503/529 from provider (106 occurrences)
- `FailoverError: Request was aborted` — client-side cancellation (58 occurrences)

These are **expected** in a multi-model setup. They only become problems when ALL providers in the chain fail simultaneously, or when cooldown windows overlap causing no provider to be available.

**Diagnostic:** Check if a specific provider is consistently failing:
```bash
grep "FailoverError" ~/.openclaw/logs/gateway.err.log | \
  grep -oE 'provider=[^ ]+' | sort | uniq -c | sort -rn | head -10
```

## AGENTS.md Management

The bootstrap file (`AGENTS.md`) loads into every new session. It has a hard 20,000 character limit. Exceeding it causes silent truncation, which breaks instructions and makes compaction unreliable.

**Budget strategy:**
1. Keep AGENTS.md lean — identity, core rules, critical workflows only
2. Move verbose details to `AGENTS-REFERENCE.md` — the agent can read this on demand
3. Use `scripts/bootstrap-budget-check.sh` to monitor section-by-section usage
4. Target 50-70% utilization to leave room for organic growth

**Red flags that AGENTS.md is too big:**
- Compaction timeouts on sessions that aren't particularly large
- Agent "forgets" instructions from later sections of AGENTS.md
- New sessions start with truncated or garbled context
## Design Patterns Applied

This skill applies six patterns from the Agentic Design Patterns framework (Gulli, 2025). Understanding why each guardrail exists helps you adapt them to your setup.

For the full pattern descriptions, read `references/design-patterns.md`.

| Pattern | Where applied | What it prevents |
|---------|--------------|-----------------|
| **Routing (P2)** | Lane architecture | Cron/interactive deadlocks |
| **Exception Handling (P12)** | Watchdog alerts | Silent failures going unnoticed |
| **Goal Monitoring (P11)** | Bootstrap budget check | Instruction truncation |
| **Resource-Aware Optimization (P16)** | Session size limits | OOM crashes and compaction timeouts |
| **Evaluation & Monitoring (P19)** | Log scanning | Pattern detection across error categories |
| **Prioritization (P20)** | Triage order | Fix highest-impact issue first |

## Runbook: Common Scenarios

For the full diagnostic runbook with step-by-step commands for each failure category, read `references/failure-patterns.md`. Here are the most frequent:

### Gateway won't accept CLI connections
The gateway is alive but locked processing a stuck task. Check for stuck sessions, then use the safest available recovery path:
```bash
# Check what's stuck
tail -50 ~/.openclaw/logs/gateway.err.log | grep "stuck session"
# Restart gateway to clear transient lockups
launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway
```

**Break-glass recovery (last resort only):** if the gateway is too wedged for normal cron commands and a bad cron on `agent:main:main` is repeatedly deadlocking the system, make a timestamped backup of `~/.openclaw/cron/jobs.json`, remove or disable only the offending job, validate the JSON with `jq`, then restart the gateway. Treat direct `jobs.json` edits as emergency recovery, not routine operations.

### Compaction keeps timing out
Usually means a session is too large OR AGENTS.md is bloated. Check both:
```bash
# Session sizes
find ~/.openclaw/agents/main/sessions -name "*.jsonl" -exec ls -lh {} \; | sort -k5 -h
# Bootstrap size
wc -c < ~/.openclaw/workspace/AGENTS.md
```

### Agent responds but ignores instructions
AGENTS.md is likely truncated. Run `bootstrap-budget-check.sh` to see utilization. If above 90%, move sections to AGENTS-REFERENCE.md immediately.

### Tool writes fail with "Path escapes sandbox"
The agent tried to write to `/tmp/` or another path outside `~/.openclaw/workspace/`. All file operations must stay within the workspace sandbox. Teach the agent to use workspace-relative paths in AGENTS.md.