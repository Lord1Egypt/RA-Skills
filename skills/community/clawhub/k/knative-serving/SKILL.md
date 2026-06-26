---
name: knative-serving
description: Use this skill when a task involves Knative Serving on Kubernetes, including designing or deploying serverless container workloads, converting Deployments to Knative Services, writing or reviewing serving.knative.dev manifests, using kn or kubectl for Serving resources, configuring autoscaling or scale-to-zero, managing Revisions and traffic splits, debugging Ready/Route/Configuration/Revision failures, configuring cluster-local or custom-domain networking, probes, timeouts, volumes, private registries, observability, or resolving common Serving errors even when the user only mentions ksvc, routes, revisions, canary, cold starts, or Knative autoscaling.
metadata:
  openclaw:
    emoji: 🚀
    requires:
      bins: [kubectl, kn]
---

# Knative Serving

Use this skill for Knative Serving work on Kubernetes clusters. Prefer current cluster state over assumptions: inspect resources with `kubectl` and `kn`, then make the smallest manifest or command change that matches the user's deployment model.

## Workflow

1. Identify the scope: deploy/update, Deployment conversion, autoscaling, revision/traffic, networking, container runtime, or debugging.
2. Check the cluster context before changing live resources:
   ```bash
   kubectl config current-context
   kubectl get ns
   kubectl get ksvc,route,configuration,revision -A
   ```
3. Prefer `kn` for fast operational changes and examples; prefer YAML plus `kubectl apply` when the user needs reviewable declarative config.
4. For production manifests, keep all per-revision behavior under `spec.template` so Knative creates a new Revision for behavior-changing changes.
5. Validate with status, conditions, and traffic targets, not only Pods:
   ```bash
   kn service describe <service> -n <namespace>
   kubectl get ksvc <service> -n <namespace> -o yaml
   kubectl get revision -n <namespace>
   kubectl get route <service> -n <namespace> -o yaml
   ```

## References

Read only the files needed for the task:

- `references/overview-and-crds.md`: Serving resource model, CRD schema discovery, core objects, Serving API fields, and important labels/annotations.
- `references/kn-cli.md`: `kn` CLI workflows for create, update, describe, revisions, traffic, domain, and service operations.
- `references/autoscaling.md`: KPA/HPA, metrics, concurrency, RPS target, scale-to-zero, scale bounds, scale windows/delays, and autoscaling annotations.
- `references/container-settings.md`: container image, ports, env, secrets/config, resources, probes, timeouts, volumes, private registries, multi-container, and queue-proxy implications.
- `references/revisions-and-traffic.md`: immutable Revisions, rollout, pinning, tagging, splitting, rollback, and garbage collection.
- `references/networking.md`: Route, ingress, external URL, cluster-local/private services, DomainMapping, default domains, TLS, ingress class, Kourier/Istio/Contour notes.
- `references/observability.md`: Serving metrics, queue-proxy and autoscaler signals, logs, tracing, and config-observability/config-logging.
- `references/debugging.md`: diagnosis flow, commands, condition interpretation, logs/events, and common error patterns.
- `references/common-errors.md`: quick lookup table for frequent Knative Serving failures and fixes.

## Defaults

- Use `Service` (`ksvc`) for normal workloads; reach for lower-level Route/Configuration only when the user explicitly needs them.
- Treat annotations under `spec.template.metadata.annotations` as Revision-scoped unless the reference says otherwise.
- Treat cluster-local visibility as a label on the Service/Route/Kubernetes Service unless the live installed version says otherwise.
- Do not list full CRD schemas in answers. Show how to inspect them with `kubectl explain`, `kubectl get crd`, and OpenAPI output.
- When autoscaling is involved, state whether the setting is global ConfigMap, Operator config, or per-Revision annotation/spec field.
- When debugging, follow the object chain: Service -> Route/Configuration -> Revision -> PodAutoscaler/ServerlessService -> Deployment/Pod -> ingress.

## Safety

- Do not assume `kn` can install Knative Serving or Eventing; use it for resource operations after Knative is installed.
- Do not expose a private Service with DomainMapping unless the user explicitly wants that. A DomainMapping can make a private Service reachable through the mapped domain.
- Do not assume metrics/logging/tracing export is enabled. Check `config-observability`, `config-logging`, and the cluster monitoring stack first.
- Avoid setting low `containerConcurrency` as a generic fix. It can increase queueing, latency, and cold starts.
- Do not mix KPA-only metrics with HPA-only metrics. KPA supports `concurrency` and `rps`; HPA handles CPU, memory, and custom metrics when configured.
- For traffic changes, ensure traffic percentages sum to 100 before applying manifests or commands.
