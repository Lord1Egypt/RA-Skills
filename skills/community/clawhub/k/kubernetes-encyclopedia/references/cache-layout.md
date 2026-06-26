# `.Kubernetes-Encyclopedia/` Cache Layout

Use this directory as the workspace-local data root for the skill.

## Directory tree

```text
.Kubernetes-Encyclopedia/
  docs/
    kubernetes.io/
      docs/
        ... cached official docs pages ...
  notes/
    components/
      ... per-component notes ...
    patterns/
      ... reusable Kubernetes notes ...
  inventory/
    access.md
    topology.md
    doc-index.md
```

## Placement rules

### `docs/`
Store cached copies of official Kubernetes docs here.

Mirror the official docs path as much as practical.
Example:

```text
https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
->
.Kubernetes-Encyclopedia/docs/kubernetes.io/docs/concepts/workloads/controllers/deployment/index.md
```

### `notes/components/`
Store environment-specific component notes here.

Suggested filenames:
- `control-plane.md`
- `nodes.md`
- `ingress.md`
- `storage.md`
- `rbac.md`

### `notes/patterns/`
Store reusable operational notes here.

Examples:
- `rollout-debugging.md`
- `service-vs-ingress.md`
- `rbac-review-gotchas.md`
- `stateful-workload-ops.md`

### `inventory/`
Store environment-wide inventories here.

Suggested files:
- `access.md`
- `topology.md`
- `doc-index.md`

## Cache philosophy

Do not mirror the whole docs site eagerly.
Cache only the pages you actually consulted and expect to be useful later.
