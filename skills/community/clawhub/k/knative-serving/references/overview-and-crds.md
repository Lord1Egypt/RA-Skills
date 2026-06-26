# Overview and CRDs

## Contents

- [Serving resources](#serving-resources)
- [Control plane and data path](#control-plane-and-data-path)
- [Inspecting CRDs and schemas](#inspecting-crds-and-schemas)
- [Minimal Service](#minimal-service)
- [Common important annotations](#common-important-annotations)

## Serving resources

Knative Serving is a set of Kubernetes CRDs for serverless HTTP workloads. The normal entry point is `Service` (`ksvc`), which manages:

- `Service` / `service.serving.knative.dev`: lifecycle wrapper that creates and updates the underlying Route, Configuration, and Revisions.
- `Route` / `route.serving.knative.dev`: maps network endpoints to one or more Revisions and handles traffic split/tag URLs.
- `Configuration` / `configuration.serving.knative.dev`: desired state for code/config; changes create Revisions.
- `Revision` / `revision.serving.knative.dev`: immutable snapshot of code and configuration, autoscaled by traffic.

Useful supporting resources:

- `PodAutoscaler` (`pa.autoscaling.internal.knative.dev`): Knative autoscaler state.
- `ServerlessService` (`sks.networking.internal.knative.dev`): networking state for active/proxy modes.
- Kubernetes `Deployment`, `ReplicaSet`, `Pod`, and `Service`: generated lower-level runtime objects.

## Control plane and data path

- Controller watches Serving resources, reconciles dependent resources, and updates status conditions.
- Webhooks default and validate Serving resources before they are persisted.
- Autoscaler scales Revisions from metrics, incoming requests, and autoscaling config.
- Activator queues requests for scaled-to-zero Revisions and can buffer bursts before routing to Pods.
- Queue-proxy is injected into each Revision Pod. It collects metrics, enforces hard concurrency, performs readiness aggregation, and forwards requests to the user container.

Use this model when debugging: a Service can look fine at the Pod layer while the Route, ServerlessService, ingress, or queue-proxy still prevents traffic.

## Inspecting CRDs and schemas

Do not paste full CRD schemas into answers. Use these commands to inspect the live installed version:

```bash
kubectl api-resources --api-group=serving.knative.dev
kubectl get crd services.serving.knative.dev -o yaml
kubectl explain kservice.spec
kubectl explain kservice.spec.template.spec
kubectl explain kservice.spec.traffic
kubectl explain revision.status.conditions
```

For exact OpenAPI schema snippets:

```bash
kubectl get crd services.serving.knative.dev \
  -o jsonpath='{.spec.versions[?(@.served==true)].schema.openAPIV3Schema}' | jq
```

For a specific field:

```bash
kubectl explain kservice.spec.template.metadata.annotations
kubectl explain kservice.spec.template.spec.containerConcurrency
kubectl explain kservice.spec.template.spec.timeoutSeconds
kubectl explain kservice.spec.template.spec.responseStartTimeoutSeconds
kubectl explain kservice.spec.template.spec.idleTimeoutSeconds
kubectl explain kservice.spec.template.spec.containers
```

## Minimal Service

```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: hello
  namespace: default
spec:
  template:
    spec:
      containers:
        - image: ghcr.io/knative/helloworld-go:latest
          ports:
            - containerPort: 8080
          env:
            - name: TARGET
              value: "World"
```

Apply and inspect:

```bash
kubectl apply -f service.yaml
kubectl get ksvc hello -n default
kn service describe hello -n default
```

## Common important annotations

Put per-Revision autoscaling annotations at `spec.template.metadata.annotations`.

Autoscaling:

- `autoscaling.knative.dev/class`: `kpa.autoscaling.knative.dev` or `hpa.autoscaling.knative.dev`.
- `autoscaling.knative.dev/metric`: `concurrency`, `rps`, `cpu`, `memory`, or custom metric depending on autoscaler.
- `autoscaling.knative.dev/target`: concurrency/RPS/CPU/memory/custom target value.
- `autoscaling.knative.dev/target-utilization-percentage`: percentage target utilization, default commonly 70.
- `autoscaling.knative.dev/min-scale`: lower bound for replicas.
- `autoscaling.knative.dev/max-scale`: upper bound for replicas.
- `autoscaling.knative.dev/initial-scale`: starting scale for a new Revision.
- `autoscaling.knative.dev/activation-scale`: scale used when activating from zero.
- `autoscaling.knative.dev/scale-down-delay`: delay before scaling down.
- `autoscaling.knative.dev/scale-to-zero-pod-retention-period`: keep the last pod for a minimum duration after scale-to-zero decision.

Networking:

- `networking.knative.dev/visibility: cluster-local`: label a Service, Route, or Kubernetes Service to keep it cluster-local.
- `networking.knative.dev/ingress-class`: Service-level override for the installed ingress implementation when supported by cluster config.
- `networking.knative.dev/certificate-class`: Service-level certificate provider override when automatic TLS is configured.

Revision naming:

- `serving.knative.dev/rollout-duration`: gradual rollout duration if enabled/configured.
- `serving.knative.dev/creator` and `serving.knative.dev/lastModifier`: system/user metadata, inspect only.

Check available annotation support against the live CRD and installed Knative version; feature gates and operator configuration can change behavior.
