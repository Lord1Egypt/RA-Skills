# Alert and Incident Inspection

Inspect alert state and incident telemetry with supported read-only New Relic CLI commands.

The CLI has no alert-management command tree. Configure policies, conditions, and notification channels through a supported New Relic API or the New Relic UI instead.

---

## View Recently Opened Incident Events

Query incident events through the supported `nrql query` command:

```bash
newrelic nrql query --accountId "$NEW_RELIC_ACCOUNT_ID" --query "
  SELECT *
  FROM NrAiIncident
  WHERE event = 'open'
  SINCE 24 hours ago
  LIMIT 20
"
```

This is read-only and reports `open` events recorded in the last 24 hours, not the current
state of every incident. It can include an incident that later closed and omit an older
incident that remains open. Incident event availability and attributes depend on the data
retained in the selected account.

## Review Recent Incident Activity

```bash
newrelic nrql query --accountId "$NEW_RELIC_ACCOUNT_ID" --query "
  SELECT count(*)
  FROM NrAiIncident
  FACET event, priority
  SINCE 1 week ago
  LIMIT MAX
"
```

Use this to summarize recent incident events without changing alert configuration or incident state.

---

## Check Entity Alert Severity

```bash
newrelic entity search --name "my-app" --type APPLICATION --domain APM | \
  jq '.[] | {name, alertSeverity}'
```

Severity values include `NOT_CONFIGURED`, `NOT_ALERTING`, `WARNING`, and `CRITICAL`. Entity search is read-only; use `newrelic apm application get --guid <GUID>` when you need details for an exact APM application returned by the search.
