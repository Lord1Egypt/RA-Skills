# Kubernetes Investigation Reference

Load this when the incident involves pods, nodes, namespaces, deployments, or any Kubernetes resource.

## Key Signals to Surface

- Pod status: `CrashLoopBackOff`, `OOMKilled`, `ImagePullBackOff`, `Pending`, `Evicted`
- Node conditions: `MemoryPressure`, `DiskPressure`, `NotReady`
- Resource exhaustion: CPU throttling, memory limits hit, PVC full
- Networking: service unreachable, DNS resolution failures, NetworkPolicy blocking traffic
- Control plane: API server latency, etcd compaction, scheduler backlog

## Suggested `neubird investigate` Prompts

```
"Pods in namespace <ns> are CrashLoopBackOffing — investigate root cause"
"Node <name> went NotReady 10 minutes ago — what happened?"
"Deployment <name> rollout is stuck — why?"
"HPA is not scaling up despite high CPU — investigate"
"Persistent volume claim <name> is stuck in Pending"
```

## Interpreting Exit Codes from Containers

| Exit Code | Likely Cause |
|-----------|-------------|
| 0 | Clean exit — app bug (crash on startup) or misconfiguration |
| 1 | Application error — check app logs |
| 137 | OOMKilled — increase memory limits or find leak |
| 139 | Segfault — application or dependency bug |
| 143 | SIGTERM not handled — graceful shutdown issue |
