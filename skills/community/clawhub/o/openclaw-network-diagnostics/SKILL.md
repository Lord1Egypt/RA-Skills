---
name: openclaw-network-diagnostics
description: Standalone advanced network diagnostics for OpenClaw to continuously test end-to-end connectivity from OpenClaw agent to Telegram Bot API and approximate delivery to a personal Telegram client. Use when investigating latency spikes, packet loss, DPI/throttling/blocking suspicion, DNS instability, TLS/TCP issues, route changes, MTU shifts, retry/timeout behavior, or Telegram rate-limits with structured rotating JSON logs.
---

# OpenClaw Network Diagnostics

## Overview

Run a pure network diagnostic worker from CLI to continuously monitor connectivity between:
1. OpenClaw runtime host
2. Telegram Bot API (`api.telegram.org`)
3. Personal Telegram client approximation via delivery verification cycles

Keep diagnostics isolated from OpenClaw LLM flow:
- Use no LLM calls.
- Consume no AI tokens.
- Run in independent async worker loops.

## Skill Files

- `scripts/netdiag.py`: standalone CLI worker (`run/start/stop/status/validate-config`)
- `references/config.example.json`: complete example configuration
- `references/example-log-entries.jsonl`: sample structured JSON logs
- `references/openclaw-integration.md`: integration patterns with pros/cons
- `references/ai-log-analysis.md`: workflow for later AI-based log analysis

## Prerequisites

Install and verify:
1. Python `3.11+`
2. macOS networking tools: `dig`, `ping`, `traceroute`
3. Telegram bot token and personal chat id

## Install

From skill root:

```bash
cd /Users/ivanbelugin/Documents/Connection\ Monitoring\ System/openclaw-network-diagnostics
python3 scripts/netdiag.py validate-config --config references/config.example.json
```

Create a real config file from the example and set real credentials:

```bash
cp references/config.example.json config.json
```

Then edit `config.json`:
- `telegram.bot_token`
- `telegram.personal_chat_id`

## Run Model

### Foreground mode (manual stop via Ctrl+C)

```bash
python3 scripts/netdiag.py run --config config.json --pid-file ./logs/netdiag.pid
```

Behavior:
- Start manually from CLI.
- Run continuously until manual stop.
- Print JSON summary to stdout on stop.
- Save summary to `logging.summary_file_path`.

### Background mode (non-blocking service)

```bash
python3 scripts/netdiag.py start --config config.json --pid-file ./logs/netdiag.pid
python3 scripts/netdiag.py status --pid-file ./logs/netdiag.pid
python3 scripts/netdiag.py stop --pid-file ./logs/netdiag.pid
```

Use this mode to avoid blocking OpenClaw main thread.

## Monitoring Behavior

Every `intervals_sec.ping` (default `30s`) perform active cycle:
1. Resolve DNS with TTL snapshot (system + public resolvers).
2. Send Bot API probe (`getMe`) and measure round-trip latency.
3. Run delivery verification cycle (`sendMessage` + selected ack mode).
4. Run packet-loss probe (`ping`) and log packet loss indicators.
5. Update outage/recovery and anomaly counters.

Additional periodic diagnostics:
- Traceroute (`intervals_sec.traceroute`)
- MTU discovery via DF ping binary search (`intervals_sec.mtu_test`)
- DNS re-resolution (`intervals_sec.dns_reresolve`)

## Delivery Verification Modes

Set `delivery_verification.mode`:

1. `bot_api_ack` (default)
- Confirm only Bot API acceptance (`sendMessage` success).
- Lowest overhead.
- Does not prove handset render/read.

2. `user_reply_ack`
- Wait for user reply via `getUpdates`.
- Better approximation of “message reached client and user interacted”.
- Requires manual interaction.

3. `callback_ack`
- Send inline button and wait callback query.
- Structured acknowledgement event.
- Requires button tap.

Read confirmation note:
- Telegram Bot API does not expose direct read receipts for bot messages.
- `user_reply_ack`/`callback_ack` are practical approximations.

## Default Tuning (Recommended)

- `timeouts_ms.connect`: `4000`
- `timeouts_ms.request`: `10000`
- `retry.max_retries`: `2`
- `retry.backoff_base_ms`: `500`
- `diagnostics.latency_anomaly_threshold_ms`: `1200`

Rationale:
- Catch transient failures without hiding persistent outages.
- Limit retry storm risk during throttling/rate-limit events.

## Logging Model

Write JSON lines to rotating files with total budget cap.

Required fields are present in every record:
- millisecond UTC timestamp
- source/destination ip + ports
- dns result snapshot (with TTL)
- tls metadata (version, cipher, handshake duration, session reuse heuristic)
- http request/response headers and status
- payload bytes sent/received
- round-trip latency
- tcp state
- retries/timeouts/socket errors
- packet-loss indicator (when probe executed)
- connection reset flag
- rate-limit metadata
- exception stacktrace

Log rotation:
- per-file size: `logging.max_file_size_mb`
- total cap: `logging.max_total_size_mb` (set `500` for your requirement)

Sensitive data handling:
- enable/disable redaction via `logging.redact_sensitive_fields`

## OpenClaw Integration Options

### Option A: External process (recommended)

Use `start/stop/status` commands from OpenClaw task hooks.

Pros:
- Strong isolation from OpenClaw runtime
- Non-blocking by design
- Independent restart and fault boundaries

Cons:
- Requires pid-file lifecycle

### Option B: In-process task

Import and run the worker inside OpenClaw loop.

Pros:
- Single-process deployment

Cons:
- Faults can impact OpenClaw main runtime
- Weaker isolation for network-heavy diagnostics

Use Option A by default for production monitoring.

## Stop and Summary

On manual stop (`SIGINT`/`SIGTERM`) the worker:
1. Flushes final metrics
2. Prints summary JSON to stdout
3. Saves summary JSON to `logging.summary_file_path`

Summary fields:
- total runtime
- total pings
- failed pings
- average latency
- max latency
- connection drops
- dns changes detected
- mtu changes detected
- anomaly count

## Analyze Logs Later with AI Tools

Use `references/ai-log-analysis.md`.

Recommended flow:
1. Slice incident window from `logs/netdiag.jsonl`
2. Compute quick counters locally
3. Feed focused window + summary into ChatGPT Codex with structured prompts
4. Ask for timeline, root-cause segmentation, anomaly clusters, and config recommendations
