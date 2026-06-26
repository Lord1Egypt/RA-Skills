# Kubernetes Topic Map

Use this as a quick orientation aid when deciding what docs to look up.

## Core areas

- Kubernetes API objects and resource semantics
- `kubectl` commands and operational workflows
- Pods / deployments / daemonsets / statefulsets / jobs
- Services / ingress / DNS / traffic exposure
- ConfigMaps / Secrets / environment injection
- Volumes / persistent storage / storage classes
- Nodes / scheduling / taints / affinity / disruption behavior
- RBAC / policy / service accounts / security context
- Controllers / CRDs / cluster operations

## Typical lookup prompts

When the task is about...

### Workloads / resource semantics
Look for docs covering:
- pods
- deployments
- daemonsets
- statefulsets
- jobs/cronjobs
- rollout behavior

### Networking / exposure
Look for docs covering:
- services
- ingress
- DNS/service discovery
- network policy
- traffic exposure behavior

### Storage / config
Look for docs covering:
- volumes
- persistent volumes / claims
- storage classes
- configmaps
- secrets

### Scheduling / nodes
Look for docs covering:
- scheduling
- affinity / anti-affinity
- taints / tolerations
- node selection
- disruption and eviction behavior

### Security / access
Look for docs covering:
- RBAC
- service accounts
- pod security context
- admission/policy when relevant

### Operations / troubleshooting
Look for docs covering:
- kubectl reference
- rollout/debugging flows
- controller behavior
- cluster administration concepts when relevant
