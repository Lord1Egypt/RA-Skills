# Tracing and Querying

Use this reference when integrating Langfuse observability or retrieving Langfuse data for debugging, analysis, reporting, or downstream workflows.

## Prefer modern access patterns

Current Langfuse SDK generations use these default high-performance namespaces:

- `api.observations`
- `api.scores`
- `api.metrics`

Legacy endpoints live under `api.legacy.*`.

Prefer the modern namespaces unless you are working in an older codebase that already depends on legacy behavior.

## Integration guidance

When adding tracing:

1. Define the unit of work that becomes a trace.
2. Represent meaningful internal steps as observations/spans/generations/events.
3. Attach stable metadata where available:
   - user ID
   - session ID
   - workflow name
   - environment tags
   - model/provider
   - cost or usage-relevant attributes
4. Keep names stable so grouping and dashboards stay useful.
5. Prefer OpenTelemetry-compatible instrumentation patterns over custom one-off logging.

## Querying guidance

Use entity APIs when you need raw rows. Use the Metrics API when you need aggregates.

### Entity APIs are good for

- inspect a single trace
- page through traces for a user or tag
- fetch observations for a trace
- list sessions
- inspect scores

### Metrics API is good for

- total cost by model
- counts by prompt name
- daily error/latency trends
- token usage grouped by user, environment, or workflow

## Python examples

### Initialize

```python
from langfuse import get_client
langfuse = get_client()
```

### Traces

```python
traces = langfuse.api.trace.list(
    limit=100,
    user_id="user_123",
    tags=["production"],
)

trace = langfuse.api.trace.get("traceId")
```

### Observations

```python
observations = langfuse.api.observations.get_many(
    trace_id="abcdef1234",
    type="GENERATION",
    limit=100,
    fields="core,basic,usage",
)
```

### Sessions

```python
sessions = langfuse.api.sessions.list(limit=50)
```

### Scores

```python
scores = langfuse.api.scores.get_many(score_ids="ScoreId")
```

### Metrics

```python
query = """
{
  "view": "observations",
  "metrics": [{"measure": "totalCost", "aggregation": "sum"}],
  "dimensions": [{"field": "providedModelName"}],
  "filters": [],
  "fromTimestamp": "2025-05-01T00:00:00Z",
  "toTimestamp": "2025-05-13T00:00:00Z"
}
"""

metrics = langfuse.api.metrics.get(query=query)
```

### Async variants

```python
trace = await langfuse.async_api.trace.get("traceId")
traces = await langfuse.async_api.trace.list(limit=100)
```

## JS/TS examples

```ts
import { LangfuseClient } from "@langfuse/client";

const langfuse = new LangfuseClient();

const traces = await langfuse.api.trace.list();
const trace = await langfuse.api.trace.get("traceId");

const observations = await langfuse.api.observations.getMany({
  traceId: "abcdef1234",
  type: "GENERATION",
  limit: 100,
  fields: "core,basic,usage",
});

const sessions = await langfuse.api.sessions.list();
const session = await langfuse.api.sessions.get("sessionId");

const scores = await langfuse.api.scores.getMany();
const score = await langfuse.api.scores.getById("scoreId");

const metrics = await langfuse.api.metrics.get({
  query: JSON.stringify({
    view: "observations",
    metrics: [{ measure: "totalCost", aggregation: "sum" }],
    dimensions: [{ field: "providedModelName" }],
    filters: [],
    fromTimestamp: "2025-05-01T00:00:00Z",
    toTimestamp: "2025-05-13T00:00:00Z",
  }),
});
```

## Public API reminders

Project-level API base path:

- `/api/public`
- EU cloud: `https://cloud.langfuse.com/api/public`
- US cloud: `https://us.cloud.langfuse.com/api/public`

Auth uses Basic Auth:

- username = public key
- password = secret key

Example:

```bash
curl -u public-key:secret-key https://cloud.langfuse.com/api/public/projects
```

## Practical defaults

- Paginate explicitly.
- Filter early.
- Request only needed fields for observation-heavy queries.
- Use Metrics API for dashboards and aggregates instead of downloading every row.
- Expect a small delay between ingestion and query availability.
