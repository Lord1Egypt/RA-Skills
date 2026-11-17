---
name: pscale-traffic-control
description: Inventory and safely manage PlanetScale Postgres Database Traffic Control budgets and fingerprint, keyspace, or tag rules. Use when listing budgets, discovering budget/rule IDs, filtering budgets by query fingerprint, planning warn-mode guardrails, changing capacity/rate/burst/concurrency thresholds, or creating/deleting matching rules. Triggers on pscale traffic-control, traffic budget, traffic rule, Database Traffic Control, query budget, fingerprint budget, tag rule, capacity, burst, concurrency, warning threshold.
---

# pscale traffic-control

Manage Database Traffic Control budgets and rules for PlanetScale Postgres branches. Start with read-only inventory and Insights evidence; never create, update, delete, or enforce a budget without explicit approval.

## Destructive-operation safety

These gates apply to every destructive example here, including deletion, demotion, protection removal, connection/transaction termination, deploy-request closure/revert, and cleanup. Command examples and CLI confirmation prompts are not authorization.

1. Inspect fresh state and confirm support for the target engine and installed CLI. Obtain explicit approval for the exact organization and, where applicable, database, branch, and resource ID/name, plus the operation and flags; use an explicit `--org` on every operation. Stop on unsupported operations or uncertain identity.
2. Check dependencies and availability: applications, active users, child resources, routing, pending changes, and the maintenance window. Do not infer that a stale, merged, or unused-looking resource is disposable.
3. Require a verified recovery path that survives the operation: confirm backup/export usability and retention, or tested replacement/recreation instructions, ownership, and recovery time. A backup name alone is not verification; stop if recovery cannot be established.
4. Execute only the approved action. Force flags, descendant deletion, demotion, and disabling protection require separate explicit approval; never add them to work around a refusal. For a known headless session, obtain approval for the required force flag up front, before attempting the operation; stop if that approval is absent or any attempt is refused.
5. Perform read-back verification of the exact target and dependent service health. Inspect pending/asynchronous outcomes before claiming completion. Authentication/network errors are not proof of absence; an ambiguous result requires investigation, not an automatic retry.

## Inventory

```bash
# List budgets and embedded rule metadata for the branch
pscale traffic-control budget list <database> <branch> --org <org> --format json

# Find budgets containing a rule for one exact Insights fingerprint
pscale traffic-control budget list <database> <branch> --org <org> \
  --fingerprint <fingerprint> --format json

# Show one budget and its rules
pscale traffic-control budget show <database> <branch> <budget-id> \
  --org <org> --format json
```

This command family is Postgres-only. Prefer JSON so IDs, nullable limits, modes, and nested rules are not truncated. An empty filtered list means no budget currently has a rule for that exact fingerprint; it does not mean the query is harmless or that no tag/keyspace rule could affect it.

## Recommendation workflow

1. Confirm organization, Postgres database, branch, and current application impact.
2. List all budgets and inspect each relevant budget by ID.
3. Gather Insights queries, full error fingerprints, tags, anomalies, and application ownership for the intended traffic slice.
4. Prefer stable, bounded tags for a traffic class; use an exact fingerprint when one known query shape needs containment. Avoid unbounded values such as request IDs, user IDs, emails, UUIDs, or raw URLs.
5. Propose one focused budget with exact mode, capacity, rate, burst, concurrency, warning threshold, and rules. Explain application rejection risk and rollback.
6. Start in `warn` for normal rollout, observe warnings/false positives, and move to `enforce` only after explicit approval. Use `enforce` immediately only for an explicitly authorized incident response.
7. After any write, re-run `budget show` and `budget list` and compare every returned field/rule.

Traffic Control is a database resource guardrail. It does not replace query tuning, application rate limits, workload isolation, or incident diagnosis. `enforce` can reject matching queries and change application behavior.

## Budget writes

```bash
# Create in warn mode after approval; omitted numeric limits remain unlimited
pscale traffic-control budget create <database> <branch> --org <org> \
  --name <name> \
  --mode warn \
  --capacity <0-6000> \
  --rate <0-100> \
  --burst <0-6000> \
  --concurrency <0-100> \
  --warning-threshold <0-100> \
  --format json

# Update sends only flags explicitly supplied
pscale traffic-control budget update <database> <branch> <budget-id> \
  --org <org> --mode warn --format json

# Delete only after inspecting rules and approving their removal
pscale traffic-control budget delete <database> <branch> <budget-id> --org <org>
```

`--name` is required on create and the default mode is `warn`. On create and update, omitted numeric flags are not sent; distinguish omission from an explicit zero. Before changing limits or mode, save the current JSON and verify that the application has a tested rollback path. Use `--force` on delete only for an already-approved non-interactive action.

## Rule writes

```bash
# Exact query fingerprint
pscale traffic-control rule create <database> <branch> <budget-id> --org <org> \
  --fingerprint <fingerprint> --format json

# Stable tag; source defaults to sql when omitted
pscale traffic-control rule create <database> <branch> <budget-id> --org <org> \
  --tag 'key=feature,value=export,source=sql' --format json

# Delete one reviewed rule
pscale traffic-control rule delete <database> <branch> <budget-id> <rule-id> \
  --org <org>
```

Rule create also accepts `--keyspace` and repeatable `--tag`; `--kind` defaults to `match`. Each tag must contain non-empty `key` and `value`; `source` defaults to `sql`. Confirm the complete matching scope before creation. A broad or incorrect rule can affect unrelated traffic, especially under an enforced budget. Use `budget show` to verify the created/deleted rule and never infer a rule ID from a truncated display.

## Related Skills

- **pscale-insights** — gather query fingerprints, tags, errors, and anomaly evidence
- **pscale-metrics** — compare branch resource behavior before and after a rollout
- **pscale-branch** — inspect the exact Postgres branch and infrastructure target

## References

See [references/commands.md](references/commands.md) for the checksum-verified command help.
