# Observability

Use this reference when the user asks about metrics, logs, tracing, dashboards, autoscaling signals, queue depth, cold starts, or why Knative scaled a Revision.

## Metrics model

Knative Serving uses OpenTelemetry-oriented metrics. Export may be disabled by default, so first inspect configuration and installed monitoring:

```bash
kubectl get configmap config-observability -n knative-serving -o yaml
kubectl get pods -A | grep -E 'prometheus|otel|grafana|jaeger|tempo'
kubectl get servicemonitor,podmonitor -A
```

Common export settings live in `config-observability`:

- `metrics-protocol`: `none`, `prometheus`, `http/protobuf`, or `grpc`.
- `request-metrics-protocol`: request metrics export protocol.
- `request-metrics-endpoint`: destination for request metrics.
- `tracing-protocol`, `tracing-endpoint`, `tracing-sampling-rate`: tracing export.

Do not assume Prometheus Operator CRDs exist before using `ServiceMonitor` or `PodMonitor`.

## Workload and queue-proxy metrics

Every Serving workload Pod includes queue-proxy. It enforces concurrency and emits workload metrics with attributes such as namespace, pod, service, configuration, and revision.

Useful signals:

- `kn.serving.queue.depth`: current queue-proxy queued requests.
- `kn.serving.invocation.duration`: user-container invocation duration.
- HTTP server/client metrics from queue-proxy, useful for status code and latency analysis.

Use these to distinguish app latency from queueing caused by hard concurrency, insufficient scale, or activator buffering.

## Autoscaler metrics

Autoscaler metrics explain scale decisions:

- `kn.revision.concurrency.stable` and `kn.revision.concurrency.panic`
- `kn.revision.rps.stable` and `kn.revision.rps.panic`
- `kn.revision.concurrency.target`
- `kn.revision.pods.desired`, `kn.revision.pods.requested`, and `kn.revision.pods.count`
- `kn.revision.pods.not_ready.count`, `pending.count`, and `terminating.count`

Compare these with Revision annotations and PodAutoscaler status:

```bash
kubectl get revision <revision> -n <namespace> -o yaml
kubectl describe podautoscaler <revision> -n <namespace>
```

## Control plane metrics

Control plane components expose metrics for the controller, autoscaler, webhook, activator, workqueues, and Go runtime. For reconciliation delays, admission latency, or controller saturation, inspect component metrics and logs together:

```bash
kubectl logs -n knative-serving deploy/controller
kubectl logs -n knative-serving deploy/webhook
kubectl logs -n knative-serving deploy/autoscaler
kubectl logs -n knative-serving deploy/activator
```

## Logging

Serving component logging is configured through `config-logging` in `knative-serving`:

```bash
kubectl get configmap config-logging -n knative-serving -o yaml
```

For workload logs, remember that scale-to-zero and revision rollout can delete Pods and their logs. Capture logs early:

```bash
kubectl logs -n <namespace> -l serving.knative.dev/service=<service> -c user-container --tail=200
kubectl logs -n <namespace> -l serving.knative.dev/service=<service> -c queue-proxy --tail=200
kubectl get events -n <namespace> --sort-by=.lastTimestamp
```

If logs disappear before diagnosis, recommend installing or checking a cluster log collector instead of disabling scale-to-zero as the first response.

## Tracing

If request path analysis needs traces, inspect tracing configuration and collector availability:

```bash
kubectl get configmap config-observability -n knative-serving -o yaml
kubectl get pods -A | grep -E 'otel|jaeger|tempo|zipkin'
```

Use traces to identify where latency occurs across ingress, activator, queue-proxy, and user code. Keep trace enablement proportional to the environment because sampling and exporters can add operational cost.
