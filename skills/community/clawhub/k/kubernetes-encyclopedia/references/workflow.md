# Kubernetes Encyclopedia Workflow

## Core stance

Use official Kubernetes docs plus local observed state together.

Default order:
1. check `.Kubernetes-Encyclopedia/` cache/notes
2. check official docs when needed
3. inspect live environment state
4. answer or act
5. record durable learnings

## When docs lookup is mandatory

Do a docs lookup before answering or acting when any of these are true:
- the user asks about Kubernetes command syntax, resource semantics, feature behavior, or configuration behavior
- the task involves workloads, services, ingress, volumes, scheduling, RBAC, policies, nodes, controllers, or API object behavior
- the task involves a version-sensitive feature or a behavior you are not highly confident about
- the task involves live CLI/manifest work and the resource path or safety boundaries matter

## Cache-first rule

Before fetching docs, check whether the needed material already exists under:
- `.Kubernetes-Encyclopedia/docs/kubernetes.io/docs/...`
- `.Kubernetes-Encyclopedia/notes/components/...`
- `.Kubernetes-Encyclopedia/notes/patterns/...`
- `.Kubernetes-Encyclopedia/inventory/...`

If the local cache is good enough, use it.
If not, fetch/check the official docs and then cache what you used.

## How to cache docs

Use `scripts/cache_doc.py`.

Typical usage:

```bash
python3 scripts/cache_doc.py \
  --url 'https://kubernetes.io/docs/concepts/workloads/controllers/deployment/' \
  --root '<workspace>/.Kubernetes-Encyclopedia'
```

The script will:
- fetch the page
- convert it into a normalized markdown-ish cache file
- place it under `.Kubernetes-Encyclopedia/docs/kubernetes.io/docs/...`
- add metadata such as source URL and fetch timestamp

## How to store local knowledge

### Component notes

Use `.Kubernetes-Encyclopedia/notes/components/<component-name>.md` for:
- component purpose
- access path
- role in deployment
- sensitive boundaries
- discovered quirks

### Pattern notes

Use `.Kubernetes-Encyclopedia/notes/patterns/<topic>.md` for:
- recurring workload/operations patterns
- repeated gotchas
- safe operational sequences
- environment-specific design conventions

### Inventory files

Use `.Kubernetes-Encyclopedia/inventory/` for:
- deployment/access inventory
- topology/runtime layout
- documentation index

## Distinguish evidence types

When writing notes, label information mentally as one of:
- **Official docs** — from Kubernetes documentation
- **Observed local state** — from live environment inspection
- **Inference/recommendation** — your judgment based on docs + local state

Do not blur these together.

## Recommended answer style

When it helps, mention whether your answer is based on:
- cached official docs
- freshly checked official docs
- live environment inspection
- best-practice inference

## High-sensitivity areas

Treat these as high-sensitivity even when you have live access:
- namespace-wide or cluster-wide manifest changes
- RBAC, policy, or credential exposure changes
- ingress/service exposure changes
- volume/storage class or stateful workload changes
- node, control-plane, or networking changes
- changes that could break workload availability, traffic, storage, or cluster access

For these, prefer docs lookup even if you think you remember the resource shape or command path.
