---
name: h-ear
description: "H-ear.world transforms sound into an actionable, meaningful translation layer of the world around you. Describe, share and act upon environmental audio as a machine sensor that empowers you, your business and your AI flow."
version: 1.1.5
author: H-ear World
homepage: https://h-ear.world
metadata: {"openclaw": {"requires": {"env": ["HEAR_API_KEY", "HEAR_ENV"], "bins": []}, "primaryEnv": "HEAR_API_KEY"}}
---

<!-- Version: keep in sync with package.json. Runtime code reads from package.json
     via createRequire — this header is the static manifest the OpenClaw gateway
     parses at install/registration time. Bump both together. -->

# H-ear — Sound Intelligence for AI Agents

H-ear.world transforms sound into an actionable, meaningful translation layer of the world around you. Describe, share and act upon environmental audio as a machine sensor that empowers you, your business and your AI flow.

## Commands

<!-- @doc-sync-ref gen:#openclaw-commands -->
| Command | Description |
|---------|-------------|
| `h-ear health` | Check H-ear API health and liveness (no auth required). |
| `h-ear usage` | Show API usage statistics (minutes, calls, quota). |
| `h-ear sounds <search>` | List supported sound classes (521+ across 3 taxonomies). |
| `h-ear jobs` | List recent classification jobs (paginated). |
| `h-ear job <jobId>` | Get detail for one job: status, fileName, eventCount, timestamps. |
| `h-ear job events <jobId>` | Get noise events for a completed job (timeline order, filterable). |
| `h-ear job audio <jobId>` | Get a 1-hour SAS URL to stream the source audio of a job. |
| `h-ear job waveform <jobId>` | Get pre-computed peaks.js waveform + audio URL. |
| `h-ear job report <jobId>` | Get a 7-day SAS URL to download the Excel analysis report. |
| `h-ear classify <fileOrUrl>` | Classify audio (URL or local file). Polls until complete. |
| `h-ear classify batch` | Submit a batch of audio URLs for asynchronous classification (callback delivery). |
| `h-ear webhook list` | List enterprise webhook registrations. |
| `h-ear webhook get <webhookId>` | Show one webhook (URL, events, filter config, delivery stats). |
| `h-ear webhook create <url>` | Create an enterprise webhook (returns signing secret ONCE). |
| `h-ear webhook update <webhookId>` | Update webhook URL, status (active/paused), or filters. |
| `h-ear webhook delete <webhookId>` | Permanently delete a webhook (cannot be undone). |
| `h-ear webhook ping <webhookId>` | Send a test ping to a webhook (verify connectivity + signing). |
| `h-ear webhook deliveries <webhookId>` | Audit trail: recent delivery attempts for a webhook. |
<!-- @end-doc-ref -->

For per-command help with all flags and examples, run `h-ear <command> --help`. For machine-readable schemas (LLM-friendly introspection): `h-ear --list-tools --json`.

## Setup

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `HEAR_API_KEY` | Yes* | | H-ear Enterprise API key (`ncm_sk_...`). Required unless `HEAR_BEARER_TOKEN` is set. Get one at [h-ear.world](https://h-ear.world). |
| `HEAR_BEARER_TOKEN` | Yes* | | OAuth bearer token. Alternative to `HEAR_API_KEY` — one of the two must be set. |
| `HEAR_ENV` | Yes | | Target environment: `dev`, `staging`, or `prod`. |
| `HEAR_BASE_URL` | No | Per-environment default | Override API base URL (advanced). |

*One of `HEAR_API_KEY` or `HEAR_BEARER_TOKEN` is required.

## Webhook Delivery

Batch classification (`classify batch`) and sound alerts (`alerts on`) use webhook callbacks for asynchronous result delivery. The OpenClaw gateway manages webhook endpoints automatically -- the skill registers callbacks against the gateway's own webhook receiver, which routes results back to your connected messaging channel. No external endpoint configuration is required by the user.

Webhook events: `job.completed`, `job.failed`, `batch.completed`, `quota.warning`.
