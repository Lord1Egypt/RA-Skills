# Container Settings

## Contents

- [Image, port, and env](#image-port-and-env)
- [ConfigMaps and Secrets](#configmaps-and-secrets)
- [Resources](#resources)
- [Probes](#probes)
- [Concurrency and queue-proxy](#concurrency-and-queue-proxy)
- [Timeouts](#timeouts)
- [Multi-container](#multi-container)
- [Security and runtime settings](#security-and-runtime-settings)

Knative Service `spec.template.spec` resembles a Kubernetes Pod template, but Knative adds defaulting, validation, queue-proxy behavior, and Revision immutability.

## Image, port, and env

```yaml
spec:
  template:
    spec:
      containers:
        - image: ghcr.io/example/app:v1
          ports:
            - containerPort: 8080
          env:
            - name: LOG_LEVEL
              value: info
```

Notes:

- Exactly one user container should receive traffic. In multi-container Services, exactly one container has the serving port.
- The app must listen on the configured port and interface reachable in the container.
- Prefer immutable image tags or digests in production.

## ConfigMaps and Secrets

Use standard Kubernetes `env`, `envFrom`, and volumes:

```yaml
envFrom:
  - configMapRef:
      name: app-config
  - secretRef:
      name: app-secret
```

Changing referenced ConfigMaps or Secrets may affect running Pods depending on mount style, but it does not create a new Revision unless the Service template changes.

## Resources

```yaml
resources:
  requests:
    cpu: "250m"
    memory: "256Mi"
  limits:
    cpu: "1"
    memory: "512Mi"
```

Resource requests influence scheduling and HPA metrics. Missing requests can make autoscaling behavior or scheduling harder to reason about.

## Probes

Knative can default readiness probing on the traffic port. Define explicit probes for real health semantics:

```yaml
readinessProbe:
  httpGet:
    path: /ready
    port: 8080
livenessProbe:
  httpGet:
    path: /healthz
    port: 8080
```

Guidance:

- Readiness decides whether traffic should be sent.
- Knative rewrites readiness probes through queue-proxy and also performs aggressive probing through the Serving network path.
- Liveness restarts the container; do not make it depend on external systems unless restart is the correct recovery.
- Startup probes are useful for slow-starting applications so liveness does not restart them too early.
- For multiple containers, ensure the cluster feature flags support multi-container probing.
- Pod status alone can be misleading; also inspect Knative Service, Revision, Route, PodAutoscaler, ServerlessService, and ingress conditions.

Supported probe types usually include `httpGet`, `tcpSocket`, `exec`, and `grpc`; verify exact support with the live CRD for older clusters.

## Concurrency and queue-proxy

Knative injects a queue-proxy sidecar. `containerConcurrency` and autoscaling targets affect how the queue-proxy admits, buffers, and reports traffic:

```yaml
spec:
  template:
    spec:
      containerConcurrency: 50
```

Low hard concurrency can protect single-threaded apps, but it can also increase waiting, tail latency, and scale-out pressure.

## Timeouts

Revision spec timeout fields are request-path behavior, not Kubernetes probes:

```yaml
spec:
  template:
    spec:
      timeoutSeconds: 300
      responseStartTimeoutSeconds: 30
      idleTimeoutSeconds: 60
```

- `timeoutSeconds`: total time allowed for a request instance to respond.
- `responseStartTimeoutSeconds`: time the routing layer waits for the app to begin sending response traffic.
- `idleTimeoutSeconds`: time an open request may stay idle without bytes.

Check installed support before applying these fields:

```bash
kubectl explain kservice.spec.template.spec.timeoutSeconds
kubectl explain kservice.spec.template.spec.responseStartTimeoutSeconds
kubectl explain kservice.spec.template.spec.idleTimeoutSeconds
```

## Multi-container

Multi-container support depends on feature flags in the installed Knative version/config:

```yaml
spec:
  template:
    spec:
      containers:
        - name: app
          image: ghcr.io/example/app:v1
          ports:
            - containerPort: 8080
        - name: sidecar
          image: ghcr.io/example/sidecar:v1
```

Use sidecars for supporting behavior, not for multiple independent HTTP entrypoints in one Service.

## Security and runtime settings

Use standard Pod spec fields where supported:

- `serviceAccountName`
- `securityContext`
- `imagePullSecrets`
- `nodeSelector`, affinity, tolerations
- volumes and mounts

Knative commonly supports `emptyDir`, `secret`, `configMap`, and `projected` volumes. PersistentVolumeClaim support requires feature flags such as `kubernetes.podspec-persistent-volume-claim` and write support when needed. Avoid large mounted volumes for latency-sensitive scale-from-zero paths because mount time can dominate cold start.

For private registries, use Kubernetes image pull credentials and verify ServiceAccount/imagePullSecrets behavior in the target namespace. If a cluster has cluster-wide private registry support, prefer the local platform convention.

Verify exact support with:

```bash
kubectl explain kservice.spec.template.spec
kubectl explain kservice.spec.template.spec.containers
```
