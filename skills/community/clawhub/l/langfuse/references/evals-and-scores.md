# Evaluations and Scores

Use this reference when attaching custom evaluation results, collecting user feedback, building external eval pipelines, or creating datasets and experiment-oriented Langfuse workflows.

## Choose the right attachment level

Attach scores to the narrowest level that answers the question you care about.

- **Trace**: use for end-to-end run quality
- **Observation**: use for a specific span or generation
- **Session**: use for multi-turn conversation quality
- **Dataset run**: use for offline experiment/evaluation runs

## Score types

Use one of these score types:

- `NUMERIC`
- `CATEGORICAL`
- `BOOLEAN`

Keep score names stable over time. Example:

- `correctness`
- `overall_quality`
- `policy_compliance`
- `user_feedback`

## Common use cases

- user thumbs-up / thumbs-down
- factuality or correctness scoring
- policy or guardrail checks
- runtime validation such as valid JSON or executable SQL
- human labeling workflows
- external evaluator pipelines that read traces, score them, and push results back

## Python examples

### Numeric

```python
langfuse.create_score(
    name="correctness",
    value=0.9,
    trace_id="trace_id_here",
    observation_id="observation_id_here",  # optional
    data_type="NUMERIC",
    comment="Factually correct",
)
```

### Categorical

```python
langfuse.create_score(
    name="accuracy",
    value="partially correct",
    trace_id="trace_id_here",
    observation_id="observation_id_here",  # optional
    data_type="CATEGORICAL",
    comment="Some factual errors",
)
```

### Boolean

```python
langfuse.create_score(
    name="helpfulness",
    value=1,
    trace_id="trace_id_here",
    observation_id="observation_id_here",  # optional
    data_type="BOOLEAN",
    comment="Very helpful response",
)
```

### Score current context

```python
with langfuse.start_as_current_observation(as_type="span", name="my-operation") as span:
    span.score(
        name="correctness",
        value=0.9,
        data_type="NUMERIC",
        comment="Factually correct",
    )

    span.score_trace(
        name="overall_quality",
        value=0.95,
        data_type="NUMERIC",
    )
```

## JS/TS example

```ts
import { LangfuseClient } from "@langfuse/client";

const langfuse = new LangfuseClient();

langfuse.score.create({
  id: "unique_id",
  traceId: message.traceId,
  observationId: message.generationId,
  name: "correctness",
  value: 0.9,
  dataType: "NUMERIC",
  comment: "Factually correct",
});

await langfuse.flush();
```

## Design rules

- Use comments when a reviewer may need context.
- Do not overload one score name with changing semantics.
- Prefer idempotent identifiers where supported if the same score may be updated.
- For observation-level scores, include both observation ID and trace ID.
- For session-level workflows, make sure the application emits stable session identifiers.

## Dataset guidance

Use datasets when you need repeatable offline evaluation or experiments.

Relevant namespaces include:

- `langfuse.api.datasets.*`
- `langfuse.api.dataset_items.*`
- `langfuse.api.dataset_run_items.*`

Use datasets for:

- regression suites
- prompt comparison
- model comparison
- experiment reruns against a stable benchmark set

## External evaluation pipeline pattern

A common pattern is:

1. Query traces or observations from Langfuse.
2. Run custom evaluators externally.
3. Write scores back to Langfuse.
4. Review aggregated performance in dashboards or via metrics queries.

This pattern is a good fit for guardrails, rubric scoring, red-team checks, and post-hoc quality analysis.
