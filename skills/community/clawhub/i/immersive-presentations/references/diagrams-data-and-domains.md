# Diagrams, Data, And Domains

Use this reference when the presentation explains technical, educational, business, science, or data-heavy material.

## Technical Diagrams

Good technical scenes reveal systems progressively:

- Architecture maps.
- Request flows.
- State machines.
- Sequence diagrams.
- Dependency graphs.
- Data pipelines.
- Control loops.
- Failure paths.
- Human-in-the-loop review paths.

Avoid dumping a full architecture diagram at once. Build it in layers:

```text
user intent -> interface -> orchestration -> tools/data -> evaluation -> feedback
```

## Data Storytelling

Data scenes should guide interpretation:

- Start with the question, not the chart type.
- Reveal baselines before outliers.
- Animate change only when time, ranking, accumulation, or causality matters.
- Annotate the few important marks.
- Let interaction test assumptions or scenarios.
- Preserve uncertainty and source limitations.

Use:

- Small multiples for comparison.
- Slope charts for change.
- Maps for geography when location matters.
- Flow diagrams for movement.
- Sankey/alluvial charts only when flows are the concept.
- Simulations for systems with feedback.

Avoid:

- Decorative 3D charts.
- Unlabeled animated numbers.
- Overloaded dashboards.
- Chart grids that require the audience to silently analyze everything.

## Business Strategy

Business presentations should show decisions and tradeoffs:

- Market map.
- Constraint landscape.
- Operating model.
- Decision tree.
- Investment frontier.
- Customer journey transformation.
- Risk propagation.
- Before/after system state.

Avoid defaulting to SaaS dashboard panels unless the story is about an actual interface or operating console.

## Education

Educational presentations should make invisible processes visible:

- Chemistry: particles, bonds, energy states.
- Biology: flows, membranes, organs, populations.
- Physics: forces, vectors, fields, frames of reference.
- Mathematics: transformation, geometry, constraints, mappings.
- History: timelines, maps, actors, causality chains.

Give learners a way to manipulate variables and see consequences.

## Science

Science scenes should distinguish observation, model, uncertainty, and inference:

- Show raw phenomenon.
- Reveal measurement.
- Build model.
- Test prediction.
- Show uncertainty.
- State what remains unknown.

## AI And Software

For AI/software topics, avoid abstract magic. Show concrete flows:

- Inputs.
- Context.
- Retrieval.
- Planning.
- Tool calls.
- Evaluation.
- Human oversight.
- Logs/traces.
- Failure modes.

Make autonomy, risk, cost, latency, and control visible.

