# Simulation Rules

## Targets

Default simulation targets:

- CPU target utilization: 60%.
- Memory target utilization: 70%.
- Bottleneck threshold: 80%.
- Headroom: 15%.

These defaults prefer business safety over maximum cost reduction. For latency-sensitive or bursty systems, lower the targets or increase headroom.

## Node Simulation

For each sample:

```text
required_nodes = ceil(current_nodes * max(cpu / target_cpu, memory / target_memory) * (1 + headroom))
recommended_nodes = clamp(required_nodes, autoscaler_min_nodes, autoscaler_max_nodes)
```

Signals:

- `estimated_reducible_nodes > 0`: possible lower baseline capacity, but validate over more than one period.
- `capped_sample_count > 0`: autoscaler max is too low for the simulated demand.
- many scale events: workload may be bursty; do not shrink too aggressively.
- p95 near bottleneck: keep headroom even if average utilization looks low.

## HPA Advice

Recommend faster scale-up when:

- CPU or memory p95 is high.
- bottleneck prediction is `projected` or `at_or_above_threshold`.
- desired replicas frequently trails current demand.

Recommend faster scale-down or higher target utilization when:

- avg and p95 are low across comparable periods.
- simulation shows fewer nodes are enough with headroom.
- there are no recent bottleneck projections.

Use `autoscaling/v2` behavior when generating previews:

- scale-up stabilization window around 60 seconds for responsive workloads.
- scale-down stabilization window around 300 seconds or longer for noisy workloads.
- choose conservative max percent changes when the workload is stateful or cache-heavy.

## Node Autoscaler Advice

If autoscaling is absent:

- propose min/max bounds based on simulation.
- keep min nodes high enough for HA, daemon overhead, and critical workloads.

If autoscaling exists:

- raise max nodes if simulation is capped.
- lower min nodes only when multiple records show sustained low p95.
- shorten scale-down cooldown only if workload churn is low and pod disruption risk is controlled.

## Execution Boundary

The skill may generate HPA manifests and preview `huawei_configure_cce_hpa`. Applying `confirm=true`, changing nodepool autoscaling, or resizing node pools requires explicit customer approval and a rollback plan.
