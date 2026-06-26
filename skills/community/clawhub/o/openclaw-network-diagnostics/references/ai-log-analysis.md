# AI Log Analysis (ChatGPT Codex)

## Step 1: Prepare a focused slice

Use a short time window around incident timestamps.

```bash
rg '"timestamp_utc":"2026-03-05T11:2' logs/netdiag.jsonl > logs/window.jsonl
```

## Step 2: Compute quick counters before AI

```bash
rg '"event":"telegram_request"' logs/window.jsonl | wc -l
rg '"level":"ERROR"' logs/window.jsonl | wc -l
rg '"rate_limit":\{"detected":true' logs/window.jsonl | wc -l
```

## Step 3: Prompt template for ChatGPT Codex

Use this prompt and attach `window.jsonl` plus `netdiag-summary.json`:

```text
Analyze these OpenClaw network diagnostic JSON logs.
Tasks:
1) Find the first root-cause segment in time order.
2) Separate DNS issues, TCP/TLS issues, Telegram API rate-limits, and client-delivery issues.
3) Quantify failure duration, retry effectiveness, and recovery time.
4) Highlight recurring destination IP or route hop anomalies.
5) Return a remediation plan with immediate, short-term, and long-term actions.
Output format:
- Executive summary
- Timeline (UTC)
- Evidence table (timestamp, event, reason)
- Recommended config changes
```

## Step 4: Prompt template for anomaly clustering

```text
Cluster anomalies by signature using fields:
- socket_error
- tcp_state
- tls.cipher/version
- packet_loss_indicator.percent
- rate_limit.retry_after_sec
Provide top 5 signatures with count and representative timestamps.
```

## Step 5: Data hygiene

If token redaction was disabled, mask token before sharing logs externally.
