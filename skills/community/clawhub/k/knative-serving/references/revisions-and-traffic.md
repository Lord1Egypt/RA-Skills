# Revisions and Traffic

## Contents

- [Revision model](#revision-model)
- [Inspecting Revisions](#inspecting-revisions)
- [Traffic split](#traffic-split)
- [Tags](#tags)
- [Rollback](#rollback)
- [Garbage collection](#garbage-collection)

## Revision model

A Revision is an immutable snapshot created from a Configuration/Service template change. You normally do not create or update Revisions directly.

Changes that create a new Revision include:

- image changes
- env/config changes in `spec.template`
- container resources, probes, ports, and command/args
- Revision-scoped annotations under `spec.template.metadata.annotations`
- `containerConcurrency`

Traffic-only changes do not create a new Revision.

## Inspecting Revisions

```bash
kn revisions list -n <namespace>
kubectl get revisions -n <namespace>
kubectl get revision <revision> -n <namespace> -o yaml
kubectl get configuration <service> -n <namespace> -o yaml
```

Latest names:

```bash
kubectl get configuration <service> -n <namespace> \
  -o jsonpath='{.status.latestCreatedRevisionName}{"\n"}{.status.latestReadyRevisionName}{"\n"}'
```

## Traffic split

YAML:

```yaml
spec:
  traffic:
    - latestRevision: true
      percent: 90
    - revisionName: hello-00001
      percent: 10
```

`kn`:

```bash
kn service update hello --traffic @latest=90 --traffic hello-00001=10 -n default
```

The percentages must sum to 100.

## Tags

Tags create named target URLs for Revisions:

```yaml
spec:
  traffic:
    - latestRevision: true
      percent: 0
      tag: canary
    - revisionName: hello-00001
      percent: 100
      tag: stable
```

`kn`:

```bash
kn service update hello --tag @latest=canary --tag hello-00001=stable -n default
```

Use tags for smoke tests, canary access, and stable URLs independent of traffic percent.

## Rollback

Route all traffic to a known-good Revision:

```bash
kn service update hello --traffic hello-00001=100 -n default
```

YAML:

```yaml
spec:
  traffic:
    - revisionName: hello-00001
      percent: 100
```

If you need future deploys to keep serving latest by default, restore `latestRevision: true` after the rollback plan is complete.

## Garbage collection

Old Revisions can be garbage-collected based on cluster config. Do not rely on indefinite retention unless GC policy is known. Before deleting a Revision manually, confirm it is not receiving traffic:

```bash
kubectl get route <service> -n <namespace> -o yaml
kubectl delete revision <revision> -n <namespace>
```
