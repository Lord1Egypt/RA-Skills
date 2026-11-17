# AI Monitoring

Use the New Relic CLI to find applications reporting AI/LLM telemetry and query the
underlying AI Monitoring NRDB events.

These commands are read-only, but their results can contain sensitive prompts,
responses, tool inputs, or customer data. Query only the fields needed for the task,
keep the time range narrow, and do not paste message content into tickets, chat, logs,
or third-party systems without explicit authorization.

---

## Prerequisites

Use a New Relic User Key and an account ID with access to the target account:

```bash
export NEW_RELIC_API_KEY="NRAK-..."
export NEW_RELIC_ACCOUNT_ID="1234567"
```

Prefer an existing profile when one is configured. Never print the API key or include
it in command output.

---

## Find AI-enabled Applications

Start broad. Use a name or shorter time window to reduce the discovery query, then
optionally filter the resolved entities by tags:

```bash
# Applications that reported AI Monitoring telemetry in the last seven days
newrelic aimonitoring application search --since "7 days ago"

# Require all supplied entity tags to match
newrelic aimonitoring application search \
  --tags aiEnabledApp:true,environment:production \
  --since "24 hours ago"

# Narrow the underlying event query to one application name
newrelic aimonitoring application search \
  --name "checkout-service" \
  --since "24 hours ago"
```

The result contains only each matching application's `name` and `entityGuid`. `--name`
filters the AI Monitoring events by `appName`; `--tags` filters the resolved New Relic
entities, and multiple tags use AND semantics.

Application discovery requests at most 500 unique entity GUIDs from NRDB, but then passes
the entire set to one unbatched entity lookup whose client API supports at most 25 GUIDs.
A search that finds more than 25 GUIDs can therefore fail before printing results. If the
CLI reports an entity lookup error or warns that the 500-GUID NRDB result was truncated,
shorten `--since` or add `--name`; `--tags` is applied only after entity resolution and
cannot reduce either limit or recover entities omitted by truncation. Do not treat a
partial result as a complete inventory.

Application discovery does not include `LlmVectorSearchResult` in its NRDB event set.
The `events` command below can query that event type, but an application reporting only
`LlmVectorSearchResult` will not be found by `application search`.

---

## Query AI Monitoring Events

`aimonitoring events` maps short aliases to the underlying NRDB event types:

| `--type` | NRDB event |
|---|---|
| `summary` (default) | `LlmChatCompletionSummary` |
| `message` | `LlmChatCompletionMessage` |
| `embedding` | `LlmEmbedding` |
| `feedback` | `LlmFeedbackMessage` |
| `tool` | `LlmTool` |
| `agent` | `LlmAgent` |
| `vectorsearch` | `LlmVectorSearch` |
| `vectorsearchresult` | `LlmVectorSearchResult` |

### Token and Request Summary

```bash
newrelic aimonitoring events \
  --type summary \
  --select "count(*), sum(response.usage.total_tokens)" \
  --since "1 day ago"
```

### Errors

```bash
newrelic aimonitoring events \
  --type summary \
  --select "count(*)" \
  --where "error is true" \
  --since "1 day ago"
```

### Message Content

Only query prompt or response content when the task explicitly requires it:

```bash
newrelic aimonitoring events \
  --type message \
  --select "timestamp, appName, content" \
  --where "appName = 'checkout-service'" \
  --since "30 minutes ago" \
  --limit 20
```

Empty `content` can be expected when the reporting agent has content recording disabled.
Do not recommend enabling content recording without first assessing privacy, security,
and retention requirements.

---

## Query Construction Safety

The `events` command inserts `--select`, `--where`, and `--since` directly into the
generated NRQL query. `application search` also inserts `--since` directly. Treat these
flags as executable query fragments:

- Do not interpolate untrusted user or external-system text into them.
- Prefer fixed, reviewed clauses and allowlisted field names.
- Keep `--since` and `--limit` bounded before selecting high-cardinality or sensitive data.
- Use `application search --name` for application-name discovery when possible; only
  that flag's value is escaped for backslashes and single quotes before the command
  constructs its NRQL filter.
- If a dynamic NRQL value is unavoidable, validate and escape it before invoking the CLI.

---

## Interpret Instrumentation-specific Fields

Do not combine these values blindly across instrumentation paths:

- `duration` is seconds when `ingest_source = 'otel'`, but milliseconds for APM-agent events.
- The trace identifier is `trace.id` for OpenTelemetry and `trace_id` for APM-agent events.

Segment by `ingest_source` or normalize units before comparing or aggregating duration.
Select both trace fields when the query must correlate events from mixed instrumentation.

---

## Troubleshooting

- **No applications found:** widen `--since`, remove tag filters, and confirm the selected
  profile/account is the one receiving AI Monitoring events.
- **No message content:** content recording may be disabled by design; use summary events
  unless message bodies are explicitly required and authorized.
- **Invalid event type:** use one of the aliases in the table above; arbitrary NRDB event
  names are not accepted by `--type`.
- **Unexpected duration values:** separate OpenTelemetry and APM-agent events before
  interpreting duration.
- **Application entity lookup fails:** the CLI sends all discovered GUIDs through one
  entity lookup that supports at most 25 GUIDs, and it returns `NotFound` when none of the
  GUIDs resolve (for example, after entities were deleted). Narrow with `--name` or a
  shorter `--since`; `--tags` cannot prevent these failures because it is applied later.
- **Incomplete application inventory:** treat the 500-GUID warning as truncation, narrow
  with `--name` or a shorter `--since`, and do not rely on `--tags` to restore omitted
  entities.
