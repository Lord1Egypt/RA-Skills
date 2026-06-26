# Autoscaling

## Contents

- [Decision points](#decision-points)
- [Autoscaler class](#autoscaler-class)
- [Metrics](#metrics)
- [Concurrency](#concurrency)
- [RPS target](#rps-target)
- [CPU and memory targets](#cpu-and-memory-targets)
- [Scale bounds](#scale-bounds)
- [Scale to zero](#scale-to-zero)
- [Verification](#verification)
- [Tuning guardrails](#tuning-guardrails)

## Decision points

1. Choose autoscaler class.
2. Choose metric.
3. Set per-replica target.
4. Set scale bounds and scale-to-zero behavior.
5. Verify status using Revision, PodAutoscaler, and Pods.

Per-Revision settings override global autoscaler config where both exist.

## Autoscaler class

Per-Revision annotation:

```yaml
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/class: "kpa.autoscaling.knative.dev"
```

Values:

- `kpa.autoscaling.knative.dev`: default Knative Pod Autoscaler, supports scale to zero and KPA metrics.
- `hpa.autoscaling.knative.dev`: Kubernetes HPA-backed autoscaling, used for CPU, memory, or custom metrics; scale-to-zero semantics differ and require cluster support.

Global config lives in `config-autoscaler` in `knative-serving`, or in `KnativeServing.spec.config.autoscaler` when installed with the Operator.

## Metrics

Per-Revision metric:

```yaml
autoscaling.knative.dev/metric: "concurrency"
```

Common values:

- `concurrency`: default KPA metric.
- `rps`: KPA requests per second.
- `cpu`: HPA CPU target.
- `memory`: HPA memory target.
- custom metric name: HPA custom metric setup.

Do not set `cpu`, `memory`, or custom metrics on the KPA class.

## Concurrency

Soft target:

```yaml
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/metric: "concurrency"
        autoscaling.knative.dev/target: "100"
        autoscaling.knative.dev/target-utilization-percentage: "70"
```

Hard limit:

```yaml
spec:
  template:
    spec:
      containerConcurrency: 50
```

Important behavior:

- Soft target drives autoscaling; it can be exceeded during bursts.
- Hard limit is enforced by queueing and can reduce throughput if set too low.
- If both soft and hard limits are set, the smaller effective value wins.
- `containerConcurrency: 0` means unlimited.

## RPS target

RPS requires the `rps` metric and uses `autoscaling.knative.dev/target` as requests per second per replica:

```yaml
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/metric: "rps"
        autoscaling.knative.dev/target: "150"
```

Use RPS when request rate is the natural capacity unit. Use concurrency when latency/blocking time makes simultaneous in-flight requests more meaningful.

## CPU and memory targets

HPA examples:

```yaml
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/class: "hpa.autoscaling.knative.dev"
        autoscaling.knative.dev/metric: "cpu"
        autoscaling.knative.dev/target: "500"
```

CPU target is millicores. Memory target is Mi.

## Scale bounds

```yaml
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/min-scale: "0"
        autoscaling.knative.dev/max-scale: "20"
        autoscaling.knative.dev/initial-scale: "1"
        autoscaling.knative.dev/activation-scale: "2"
```

Guidance:

- Set `min-scale: "1"` for latency-sensitive services that cannot tolerate cold starts.
- Set `max-scale` to protect dependencies and budgets.
- `initial-scale` controls readiness expectations for new Revisions.
- `activation-scale` controls how much capacity appears when scaling from zero.

## Scale to zero

Global `enable-scale-to-zero` controls whether Knative may scale Revisions to zero. There is no per-Revision setting for enabling scale to zero itself.

Useful related settings:

- `scale-to-zero-grace-period`: global upper bound for internal network programming before the last replica is removed; not a "keep warm" timer.
- `autoscaling.knative.dev/scale-to-zero-pod-retention-period`: per-Revision minimum time to keep the last pod after the autoscaler decides to scale to zero.
- `autoscaling.knative.dev/scale-down-delay`: KPA-only delay before applying scale-down decisions. Use it to reduce cold starts without permanently pinning replicas.
- `autoscaling.knative.dev/window`: stable window for metric averaging. Use it when the default window reacts too quickly or too slowly for the workload.

Per-Revision retention:

```yaml
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/scale-to-zero-pod-retention-period: "1m"
```

## Verification

```bash
kubectl get ksvc <service> -n <namespace>
kubectl get revision -n <namespace>
kubectl get podautoscaler -n <namespace>
kubectl get pods -n <namespace>
kubectl describe podautoscaler <revision> -n <namespace>
kubectl get configmap config-autoscaler -n knative-serving -o yaml
```

When behavior differs from config, check the actual Revision annotations because changing Service-level fields outside `spec.template` may not affect existing Revisions.

## Tuning guardrails

- Prefer `min-scale: "1"` only when latency needs justify the steady cost.
- Prefer `scale-down-delay` when short idle gaps cause cold starts but eventual scale-to-zero is still desired.
- Do not use `initial-scale` as a warm pool. It affects readiness of a newly created Revision, then normal autoscaling takes over.
- Do not use `activation-scale` as a permanent lower bound. It controls how many replicas appear when scaling from zero.
- If HPA metrics are used, verify resource requests and metrics pipeline before blaming Knative.
