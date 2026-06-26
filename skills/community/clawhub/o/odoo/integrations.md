# Odoo Integrations and Automation

Use this file when the task goes beyond manual UI work and needs repeatable data movement or automation.

## Choose the Interface

| Interface | Best for | Avoid when |
|-----------|----------|------------|
| Odoo UI | one-off review, corrections, validation | volume is high or steps repeat daily |
| CSV import/export | structured bulk updates with reviewable files | mappings are unclear or deduplication is weak |
| XML-RPC | stable scripted reads and writes across standard models | the task needs real-time webhook-style behavior |
| JSON-RPC | modern scripted access when the instance exposes it well | the team cannot support custom payload handling |
| Native automation | server actions, scheduled actions, Studio automations | the logic needs external systems or serious version control |

## Surface-Specific Notes

- Odoo Online usually means UI, imports, exports, and supported APIs only.
- Odoo.sh adds branches, logs, and a safer deploy loop for custom modules and upgrades.
- Self-hosted opens the deepest toolbox, but that does not justify skipping preview and rollback discipline.
- The more access you have, the more important it is to choose the least dangerous path anyway.

## Integration Checklist

- target model and operation
- auth lane and environment
- create vs update rules
- idempotency key or natural key
- error handling and retry story
- owner of the automation

## XML-RPC Baseline

- Authenticate first through `/xmlrpc/2/common`
- Execute model calls through `/xmlrpc/2/object`
- Keep payloads narrow: explicit fields, filtered domains, deterministic writes
- Read before write whenever the operation may merge, overwrite, or duplicate records

## Import Design

- Prefer stable identifiers: external IDs, internal references, or agreed natural keys
- Normalize dates, currencies, taxes, units of measure, and company context before upload
- Separate create and update files when that reduces ambiguity
- Run a small representative batch before the full import

## Automation Design

- Prefer native Odoo automation if the rule is simple, observable, and reversible
- Prefer external workers when logic is complex, needs version control, or touches many systems
- Every automation should define trigger, scope, side effects, and failure notification

Do not hide complexity behind the word "sync." Name the source of truth and conflict policy explicitly.
