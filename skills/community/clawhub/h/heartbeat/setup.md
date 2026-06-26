# Setup - Heartbeat

Use this setup flow at first activation.

## Goal

Collect only the minimum information needed to produce a high-quality `HEARTBEAT.md`:
- local timezone
- active hours
- strict schedule needs
- tolerance for noisy alerts and API cost

## Step 1: Baseline Questions

Ask concise questions:
1. What timezone should heartbeat use?
2. What hours should proactive checks run?
3. Which tasks must happen at exact times?
4. Which checks are expensive and should be gated?

## Step 2: Capture Current State

If the user already has a heartbeat file, capture:
- current interval policy
- no-op output behavior
- escalation rules
- known pain points (spam, misses, cost)

## Step 3: Build First Draft

Generate one safe baseline draft before suggesting advanced tuning:
- explicit scope
- active hours and timezone
- `HEARTBEAT_OK` no-op contract
- escalation and cooldown
- cron handoff list for exact-time jobs

## Step 4: Confirm Operating Mode

Offer one of three modes:
- conservative: fewer checks, lower cost
- balanced: default for most users
- aggressive: faster checks with higher cost

Persist chosen mode in `~/heartbeat/memory.md`.

## Step 5: Verification Prompt

Before finalizing, ask for confirmation:
- "Do you want strict-time tasks moved to cron and heartbeat used only for adaptive checks?"
- "Do you want cooldowns enabled for every alert path by default?"
