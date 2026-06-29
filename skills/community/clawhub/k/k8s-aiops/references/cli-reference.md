# k8s-aiops CLI Reference

All commands accept `-t/--target <name>` to select a configured target (a kube
context). Namespaced commands accept `-n/--namespace <ns>`; omit it to use the
target's default namespace (read lists fall back to all-namespaces).

## Onboarding

```bash
k8s-aiops init                    # interactive wizard: register kube contexts as targets
```

## Pods

```bash
k8s-aiops pod list [-n <ns>] [-t <target>]
k8s-aiops pod get <name> [-n <ns>]
k8s-aiops pod describe <name> [-n <ns>]              # status, container states, events
k8s-aiops pod logs <name> [-n <ns>] [--tail N] [-c <container>]
k8s-aiops pod delete <name> [-n <ns>] [--dry-run]    # destructive: double confirm
```

## Deployments & Rollouts

```bash
k8s-aiops deployment list [-n <ns>]
k8s-aiops deployment get <name> [-n <ns>]
k8s-aiops deployment scale <name> <replicas> [-n <ns>]
k8s-aiops deployment restart <name> [-n <ns>]        # rolling restart
k8s-aiops deployment delete <name> [-n <ns>] [--dry-run]   # HIGH RISK: double confirm
k8s-aiops rollout status <name> [-n <ns>]
k8s-aiops rollout history <name> [-n <ns>]
k8s-aiops rollout pause|resume <name> [-n <ns>]
k8s-aiops rollout set-image <name> <container> <image> [-n <ns>]
k8s-aiops rollout undo <name> [--to-revision N] [--dry-run]   # HIGH RISK: double confirm
```

## StatefulSets / DaemonSets / Jobs / CronJobs

```bash
k8s-aiops statefulset list|get [-n <ns>]
k8s-aiops statefulset scale <name> <replicas> [-n <ns>]
k8s-aiops daemonset list|get [-n <ns>]
k8s-aiops job list|get [-n <ns>]
k8s-aiops job delete <name> [-n <ns>] [--dry-run]    # destructive: double confirm
k8s-aiops cronjob list|get [-n <ns>]
```

## Services, Ingress, Config, Storage

```bash
k8s-aiops service list [-n <ns>]
k8s-aiops ingress list|get [-n <ns>]
k8s-aiops configmap list|get [-n <ns>]
k8s-aiops secret list [-n <ns>]                      # names + key NAMES only, never values
k8s-aiops storage pvc-list|pvc-get [-n <ns>]
k8s-aiops storage pv-list|class-list
```

## Nodes & Metrics

```bash
k8s-aiops node list
k8s-aiops node describe <name>
k8s-aiops node cordon <name> [--dry-run]             # destructive: double confirm
k8s-aiops node uncordon <name>
k8s-aiops node drain <name> [--dry-run]              # HIGH RISK: double confirm
k8s-aiops top pod|node                               # requires metrics-server
```

## Namespaces, Cluster & Events

```bash
k8s-aiops namespace list
k8s-aiops namespace create <name>
k8s-aiops namespace delete <name> [--dry-run]        # HIGH RISK: double confirm
k8s-aiops cluster-info
k8s-aiops api-resources
k8s-aiops events [-n <ns>]
```

## Diagnostics & MCP

```bash
k8s-aiops doctor [--skip-auth]    # check config + cluster reachability
k8s-aiops mcp                     # start the MCP server over stdio
```

## Flags summary

| Flag | Meaning |
|------|---------|
| `-t, --target` | Target name from `~/.k8s-aiops/config.yaml` |
| `-n, --namespace` | Namespace scope |
| `--tail` | Trailing log lines (pod logs, default 100) |
| `-c, --container` | Container name (pod logs) |
| `--dry-run` | Preview a destructive op without executing |
| `--to-revision` | Rollout revision (`rollout undo`, 0 = previous) |
| `--skip-auth` | Skip the connectivity check in `doctor` |
