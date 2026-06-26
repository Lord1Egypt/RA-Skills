# Debugging

## Contents

- [Fast triage](#fast-triage)
- [Deployment rejected or not created](#deployment-rejected-or-not-created)
- [Route not ready](#route-not-ready)
- [Revision not ready](#revision-not-ready)
- [Scale-to-zero or cold start issues](#scale-to-zero-or-cold-start-issues)
- [System components](#system-components)
- [Domain and TLS issues](#domain-and-tls-issues)
- [Useful jsonpath snippets](#useful-jsonpath-snippets)
- [Fix discipline](#fix-discipline)

## Fast triage

Start with high-level conditions:

```bash
kn service describe <service> -n <namespace>
kubectl get ksvc <service> -n <namespace> -o wide
kubectl get ksvc <service> -n <namespace> -o yaml
```

Then walk the object chain:

```bash
kubectl get route,configuration,revision -n <namespace>
kubectl get podautoscaler,serverlessservice -n <namespace>
kubectl get ingress -n <namespace>
kubectl get deploy,rs,pod,svc -n <namespace>
kubectl get events -n <namespace> --sort-by=.lastTimestamp
```

## Deployment rejected or not created

Check terminal output first. Admission webhook messages usually identify invalid fields, traffic sums, unsupported features, or bad annotation values.

```bash
kubectl apply -f service.yaml --dry-run=server
kubectl explain kservice.spec.template.spec
```

## Route not ready

```bash
kubectl get route <service> -n <namespace> -o yaml
kubectl describe route <service> -n <namespace>
```

Check:

- traffic targets exist
- traffic percentages sum to 100
- target Revisions are ready
- ingress provider is healthy
- external IP/DNS is available

## Revision not ready

```bash
kubectl get revision <revision> -n <namespace> -o yaml
kubectl describe revision <revision> -n <namespace>
```

A healthy Revision has `Ready=True`. If not, inspect:

```bash
kubectl get pod -n <namespace>
kubectl describe pod <pod> -n <namespace>
kubectl logs <pod> -n <namespace> -c user-container
kubectl logs <pod> -n <namespace> -c queue-proxy
```

Container names vary. Use `kubectl get pod <pod> -o jsonpath='{.spec.containers[*].name}'`.

If Kubernetes says the Pod is ready but Knative does not, inspect queue-proxy readiness, rewritten readiness probes, ServerlessService mode, and ingress status before changing the user container.

## Scale-to-zero or cold start issues

```bash
kubectl get podautoscaler -n <namespace>
kubectl describe podautoscaler <revision> -n <namespace>
kubectl logs -n knative-serving deploy/autoscaler
kubectl logs -n knative-serving deploy/activator
```

Check min-scale, activation-scale, metric/target, and whether requests reach the ingress/Activator.

## System components

```bash
kubectl get pods -n knative-serving
kubectl logs -n knative-serving deploy/controller
kubectl logs -n knative-serving deploy/webhook
kubectl logs -n knative-serving deploy/autoscaler
kubectl logs -n knative-serving deploy/activator
```

Also inspect ingress namespace logs for Kourier, Istio, or Contour.

## Domain and TLS issues

```bash
kubectl get configmap config-domain -n knative-serving -o yaml
kubectl get configmap config-network -n knative-serving -o yaml
kubectl get domainmapping -A
kubectl describe domainmapping <domain> -n <namespace>
kubectl get certificates,challenges -A
```

Check DNS, ingress external IP, ClusterDomainClaim policy, TLS secret name, and whether the target Service is cluster-local.

## Useful jsonpath snippets

```bash
kubectl get ksvc <service> -n <namespace> \
  -o jsonpath='{range .status.conditions[*]}{.type}={.status} {.reason}{"\n"}{end}'

kubectl get route <service> -n <namespace> \
  -o jsonpath='{range .status.traffic[*]}{.revisionName} {.percent} {.url}{"\n"}{end}'

kubectl get revision <revision> -n <namespace> \
  -o jsonpath='{range .status.conditions[*]}{.type}={.status} {.reason}{"\n"}{end}'
```

## Fix discipline

- Fix the first failing condition closest to the Service top-level, then re-check.
- Avoid changing autoscaling, networking, and container config in one patch unless the root cause requires it.
- Prefer `--dry-run=server` before applying uncertain CRD fields.
