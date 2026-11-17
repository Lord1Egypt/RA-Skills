---
name: "home-infra-stewardship"
description: "Routine NetBox, Zabbix, and homelab maintenance with responsible change authority."
---

# Home Infrastructure Stewardship

Use this procedure when doing recurring or proactive maintenance on Ryan's internal homelab services, especially NetBox, Zabbix, and nearby OpenClaw automation.

## Standing Authorization

Ryan wants Kevin to regularly and routinely improve NetBox, Zabbix, and other internal cleanup/maintenance areas. Treat this as standing approval to make responsible internal changes when, in Kevin's engineering judgment, they are a good idea.

This includes ordinary internal changes such as:

- Updating package/plugin/configuration state for NetBox, Zabbix, and supporting automation.
- Adding or refining monitoring, discovery, dashboards, data quality checks, templates, tags, maps, alerts, and sync jobs.
- Cleaning stale automation artifacts, logs, temporary files, documentation drift, and obviously broken local configuration.
- Fixing low-risk service issues, redirects, permissions, health checks, and scheduled jobs.
- Creating backups or snapshots before material service changes when practical.
- Documenting what changed in daily memory and, when appropriate, long-term memory or local READMEs.

## Guardrails

Even with this standing permission, pause or ask Ryan before:

- Destructive deletion of important data, backups, VM/container disks, databases, or historical monitoring data.
- Public/external actions: sending emails/posts, changing public DNS, exposing services, opening firewall ports to the internet, or sharing private data.
- High-risk production-affecting operations: major OS upgrades, database migrations without rollback, storage layout changes, cluster/firewall/security-policy changes, or restarting many critical services at once.
- Any action where secrets would be printed into chat or stored in inappropriate files.

Prefer recoverable choices: backup, snapshot, export, disable, or move-to-trash over hard delete.

## Recurring Maintenance Shape

On each recurring run:

1. Review durable memory and local docs for the current NetBox/Zabbix state.
2. Inspect the existing NetBox automation before adding new sync paths.
3. Check Zabbix health, monitored hosts, templates, triggers, maps/dashboards, discovery, and alert noise.
4. Look for obvious homelab cleanup opportunities around OpenClaw automation, cron jobs, logs, and docs.
5. Make small-to-medium responsible improvements directly.
6. For high-risk improvements, prepare a clear plan and notify Ryan instead of guessing.
7. Verify the change with command output, service health checks, or UI/API checks.
8. Record what changed in `memory/YYYY-MM-DD.md`; promote enduring lessons into `MEMORY.md` when appropriate.
9. Notify Ryan only when something changed materially, failed, or genuinely needs attention.

## Style

Be practical and proactive. Do not invent ceremony. Do not ask for routine permission that Ryan has already granted. Do keep a clean paper trail and a rollback path for meaningful infrastructure changes.
