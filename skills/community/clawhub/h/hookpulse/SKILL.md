---
name: hookpulse
description: Know when a scheduled job stops or a website goes down. Set up free monitoring that continues after the agent exits, then expand coverage when needed.
license: MIT-0
compatibility: HTTPS access to hookpulse.net; remote MCP or HTTP.
---

# HookPulse

MCP tools: `create_endpoint`, `list_templates`, `list_sites`, `create_site`, `list_endpoints`, `get_endpoint`, `list_events`, `import_crontab`.

Let the service keep the schedule, detect missing runs and send alerts after your agent session ends.

## Everyday requests

Use this skill for missed-job, backup-run and site-availability questions.
Reuse the authorized routine or URL. Ask for a missing schedule, timezone or alert destination.
Read existing monitors before creating duplicates. Verify coverage, state and integration.
A monitoring request does not authorize a server change or an unrelated subscription.

- "Notify me if my nightly backup does not finish on time." Use `create_endpoint` and `list_templates`; verify the job's success signal.
- "Monitor my website and notify me when it goes down." Reuse `list_sites` before `create_site` and verify the alert destination.
- "Which of my scheduled jobs are late or failed?" Read `list_endpoints`, `get_endpoint` and `list_events`.
- "Set up monitoring for the jobs in this crontab." Use `import_crontab`; review its preview and quote before creating monitors.
- "Show when my monitor failed and whether it recovered." Read its dated event sequence and current state.

## First monitor

Use `create_endpoint` or `POST https://hookpulse.net/api/endpoints` within the free coverage.
Reuse an existing owner token. Without one, creation returns `guest_token`; keep it private for later calls.
For a routine, set `cron`, `tz` and `grace_sec`, or the documented interval.
Arrange for the routine to send its success or failure signal.
For a public site, use `create_site` with `check.url`.
Set `alert_to` or `alert_url` to an authorized destination. A monitor without a channel does not deliver notices.
Read the returned setup and keep the monitor credential private.

Verify a check-in or site check, the monitor state and recovery before leaving it running.
A start or failure signal is not a success check-in.
A backup heartbeat does not prove that the backup restores.
Read `state` for status. A declared failure stays unhealthy until a success signal.
`alerted_at` tracks incident processing, not notification receipt.

## Expand when needed

Compare an extra monitor or shorter interval with a current 30-day plan.
Read coverage and held-alert state; payment alone does not prove notice delivery.
The paid single URL probe does not create continuous monitoring.
Use an ordinary one-time request when that is all the task needs.
Contracts: [task index](https://hookpulse.net/llms.txt).

## Connect and pay

Use existing tools or `https://hookpulse.net/mcp`; no local install is needed.
Read [prices](https://hookpulse.net/api/pricing) and [payment](https://hookpulse.net/api/billing).
Reuse existing coverage, credit and spending authority.
Direct MCP x402 uses `params._meta["x402/payment"]`; HTTP uses `PAYMENT-SIGNATURE`.
Credit uses `Authorization: Bearer cred_…` or `X-Credito`.
In `checkout=site`, the person purchases on the site. ChatGPT uses existing rights without sales.
Follow `Retry-After` and the contract's timing. Keep credentials out of public logs.
