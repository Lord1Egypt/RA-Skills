---
name: openclaw-peer-bridge
description: Design and operate communication patterns between two OpenClaw instances. Use when a user wants one OpenClaw deployment to send status, tasks, reminders, audit results, or webhook callbacks to another OpenClaw deployment, or when defining a bridge between local and remote OpenClaw agents, dashboards, or automation flows.
---

# OpenClaw Peer Bridge

Design communication between two OpenClaw instances using supported primitives only.
Prefer explicit, auditable flows: webhook delivery, cron delivery, channel routing, or user-mediated relay.
Do not invent peer-to-peer commands or claim native cross-instance session sharing unless it exists in the current deployment.

## Core patterns

### 1. Event push via webhook

Use when one OpenClaw instance needs to notify another system or service immediately.

Pattern:
1. Source OpenClaw runs an isolated cron or task.
2. Delivery mode is `webhook`.
3. Target side exposes an HTTP endpoint that accepts the event and decides what to do next.

Use for:
- health checks
- deployment notifications
- audit summaries
- workflow completion callbacks

## 2. Human-routed messaging bridge

Use when the only guaranteed common surface between two instances is a chat channel.

Pattern:
1. Instance A sends a structured message to a human-controlled channel.
2. Human or downstream automation forwards or triggers Instance B.
3. Keep payloads short, explicit, and idempotent.

Use for:
- approvals
- escalation paths
- low-frequency handoffs
- cross-org workflows where direct network trust is not available

## 3. Scheduled relay

Use when exact timing matters more than low latency.

Pattern:
1. Source instance schedules a cron job.
2. Cron produces either an announcement or webhook.
3. Target instance or receiving system processes the scheduled event.

Use for:
- daily summaries
- recurring audits
- scheduled sync checks
- heartbeat-style supervision

## 4. Local-to-remote control pattern

Use when a workstation OpenClaw needs to coordinate with a server-side OpenClaw.

Recommended split:
- local instance handles human interaction, approvals, and dashboards
- remote instance handles long-running jobs, server inspection, and isolated automation

Design rules:
- keep credentials local to the instance that needs them
- push summaries, not raw secrets
- define ownership of each task clearly
- prefer append-only logs and explicit acknowledgements

## Workflow

### Step 1: define the bridge objective

State the business outcome first:
- alerting
- task dispatch
- result return
- approval request
- periodic reporting

### Step 2: choose the transport

Choose the smallest sufficient transport:
- webhook for machine-to-machine notifications
- chat delivery for human-visible handoffs
- cron for scheduled communication
- local files only for same-machine coordination

### Step 3: define message contract

Specify:
- event name
- sender instance
- intended receiver
- timestamp
- payload fields
- retry behavior
- idempotency key if duplicate delivery is possible

Prefer JSON for machine processing and short bullet summaries for human review.

### Step 4: define trust boundary

Document:
- which side is authoritative
- where credentials live
- which actions require approval
- what happens on failure or timeout

Never assume both OpenClaw instances share memory, sessions, or auth state.

### Step 5: implement with reversible changes

Prefer:
- isolated cron jobs
- explicit webhook URLs
- local config edits with backup
- test messages before production use

### Step 6: verify end to end

Check:
- source event fired
- delivery succeeded
- receiver handled duplicate-safe logic
- failure path is visible
- no secrets leaked in logs or chat

## Output expectations

When using this skill, produce one of these deliverables:
- bridge design memo
- message schema
- cron payload definition
- webhook contract
- rollout plan with rollback
- troubleshooting checklist

## Guardrails

- Use only documented OpenClaw commands and delivery modes.
- Do not claim native OpenClaw-to-OpenClaw federation unless the environment explicitly provides it.
- Ask before publishing endpoints, changing firewall rules, or exposing dashboards.
- Prefer fewer, larger writes over chatty loops when integrating with external services.
- Keep communication auditable and easy to reason about.

## Quick examples

### Example: daily remote server audit to local operator

Design:
- remote OpenClaw runs a daily isolated cron job
- job performs audit
- delivery posts webhook to an operator-controlled endpoint or announces into a monitored channel
- local OpenClaw summarizes findings for the user

### Example: deployment completion handoff

Design:
- build instance finishes deploy pipeline
- sends webhook with environment, version, result, and log URL
- receiving side creates a human-facing summary and asks for next action if needed
