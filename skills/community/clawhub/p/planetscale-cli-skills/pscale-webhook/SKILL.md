---
name: pscale-webhook
description: Manage PlanetScale database webhooks with the pscale CLI. Use when listing, inspecting, creating, updating, testing, or deleting webhooks, configuring event subscriptions, enabling or disabling delivery, or setting or clearing an Authorization header. Triggers on pscale webhook, database webhook, webhook authorization header, webhook events, webhook test.
---

# pscale webhook

Manage database webhooks and their event subscriptions.

## Destructive-operation safety

These gates apply to every destructive example here, including deletion, demotion, protection removal, connection/transaction termination, deploy-request closure/revert, and cleanup. Command examples and CLI confirmation prompts are not authorization.

1. Inspect fresh state and confirm support for the target engine and installed CLI. Obtain explicit approval for the exact organization and, where applicable, database, branch, and resource ID/name, plus the operation and flags; use an explicit `--org` on every operation. Stop on unsupported operations or uncertain identity.
2. Check dependencies and availability: applications, active users, child resources, routing, pending changes, and the maintenance window. Do not infer that a stale, merged, or unused-looking resource is disposable.
3. Require a verified recovery path that survives the operation: confirm backup/export usability and retention, or tested replacement/recreation instructions, ownership, and recovery time. A backup name alone is not verification; stop if recovery cannot be established.
4. Execute only the approved action. Force flags, descendant deletion, demotion, and disabling protection require separate explicit approval; never add them to work around a refusal. For a known headless session, obtain approval for the required force flag up front, before attempting the operation; stop if that approval is absent or any attempt is refused.
5. Perform read-back verification of the exact target and dependent service health. Inspect pending/asynchronous outcomes before claiming completion. Authentication/network errors are not proof of absence; an ambiguous result requires investigation, not an automatic retry.

## Inspect first

```bash
set -o pipefail
pscale webhook list <database> --org <org> --format json |
  jq 'map(del(.secret))'
```

Use the redacted list for routine identifiers and persisted state. Webhook resource JSON from create, show, list, or update can contain the signing `secret` because the CLI serializes the raw API model. Do not capture it unredacted in logs, chat, or agent context; only an intentional create/show flow that writes directly to an approved secret store should retain it. `pscale webhook show` deliberately returns the secret, and human output has a `secret` column. When an exact show is unavoidable for non-secret inspection, pipe JSON directly through `jq 'del(.secret)'` before capturing output. `authorization_header_configured` reveals only whether the separate Authorization header is configured, never its value.

## Create

```bash
pscale webhook create <database> \
  --url https://hooks.example.com/planetscale \
  --events branch.ready,deploy_request.opened \
  --enabled=true \
  --org <org> --format json
```

`--url` is required. Confirm the destination host, TLS endpoint, subscribed events, enabled state, and receiver ownership before creation. Successful `create` output includes the generated webhook signing `secret` in both human and JSON formats. Capture it from that response directly into an approved secret manager; do not print it into logs, paste it into tickets, or commit it. Treat the create response as the one reliable capture point.

`--events` accepts a comma-separated list. Published event names are:

```text
branch.anomaly
branch.out_of_memory
branch.primary_promoted
branch.ready
branch.schema_recommendation
branch.sleeping
branch.start_maintenance
backup.failed
backup.succeeded
cluster.storage
database.access_request
deploy_request.closed
deploy_request.errored
deploy_request.in_progress
deploy_request.opened
deploy_request.pending_cutover
deploy_request.queued
deploy_request.reverted
deploy_request.schema_applied
keyspace.storage
webhook.test
```

The CLI forwards event strings to the PlanetScale API without client-side validation. Use the [`events` enum in the webhook API reference](https://planetscale.com/docs/api/reference/create_webhook) for accepted names and the [webhook events reference](https://planetscale.com/docs/api/webhook-events) for trigger and payload details; the general events page can lag the API enum. An unknown or unsupported name is not normalized by the CLI and can fail at the API.

### Authorization header

`--authorization-header` accepts the complete HTTP `Authorization` value, such as `Bearer …`. It is a secret-bearing argument. Do not place a literal credential in documentation, shell history, logs, chat, source control, or process captures. Use an approved secret source and preserve only the variable reference in reusable command text:

```bash
pscale webhook create <database> \
  --url https://hooks.example.com/planetscale \
  --authorization-header "$PLANETSCALE_WEBHOOK_AUTHORIZATION_HEADER" \
  --org <org> --format json
```

Do not run this form until the environment variable is populated outside the agent-visible context. Verify only `authorization_header_configured: true`; never attempt to read the value back.

## Update

Pass at least one of `--url`, `--authorization-header`, `--clear-authorization-header`, `--events`, or `--enabled`. Only supplied fields change, but `--events` replaces the entire subscription list rather than appending to it. Read the current list and include every event that should remain subscribed.

```bash
# Save redacted pre-change state for rollback
set -o pipefail
pscale webhook list <database> --org <org> --format json |
  jq --arg id '<webhook-id>' '.[] | select(.id == $id) | del(.secret)'

# Disable or change subscriptions
pscale webhook update <database> <webhook-id> \
  --enabled=false \
  --events branch.ready \
  --org <org> --format json | jq 'del(.secret)'

# Remove the configured header explicitly
pscale webhook update <database> <webhook-id> \
  --clear-authorization-header \
  --org <org> --format json | jq 'del(.secret)'

# Each synchronous update response is the read-back for that change
```

Before updating, save the redacted non-secret configuration (`url`, `events`, and `enabled`) and ensure the current Authorization value is available separately if rollback may need to restore it—the API does not return that header value. To roll back, re-run `webhook update` with the previous `--url`, complete `--events` list, and explicit `--enabled=<true|false>` values, plus either the prior `--authorization-header` value or `--clear-authorization-header`. The synchronous update response verifies persisted non-secret state; use `webhook test` to verify receiver behavior.

`--authorization-header` and `--clear-authorization-header` are mutually exclusive. An empty `--authorization-header` value is rejected; use the clear flag. Changing or clearing authentication can interrupt deliveries, so coordinate the receiver update and verify `authorization_header_configured` afterward.

## Test and delete

`webhook test` sends a real event to the external receiver. Confirm the destination and downstream side effects before running it. A successful CLI response proves dispatch was accepted, not that the receiver processed it; verify receiver-side evidence when available.

```bash
set -o pipefail
pscale webhook list <database> --org <org> --format json |
  jq 'map(del(.secret))'
pscale webhook test <database> <webhook-id> --org <org> --format json
```

Deletion has no CLI confirmation flag. Treat it as destructive: inspect the exact webhook, inventory dependencies, obtain explicit approval, delete, and read back the list.

```bash
set -o pipefail
pscale webhook list <database> --org <org> --format json |
  jq 'map(del(.secret))'
pscale webhook delete <database> <webhook-id> --org <org> --format json
pscale webhook list <database> --org <org> --format json |
  jq 'map(del(.secret))'
```

When scripting against `--format json`, probe one representative response first and handle optional fields defensively. The CLI serializes the underlying API webhook model for JSON, while human and CSV output use a smaller normalized view, so fields can differ and the JSON model can gain fields as the API evolves. Do not build strict decoders from the command-reference snippets or assume table and JSON output have identical fields.

## Reference

See `references/commands.md` for checksum-verified command help surfaces.
