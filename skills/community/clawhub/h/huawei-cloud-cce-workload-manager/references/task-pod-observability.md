# Pod Observability

## Overview

Pod observability covers monitoring, logging, and interactive debugging of running workloads. These commands help diagnose health issues, view application output, and inspect cluster resource pressure.

> **Note**: `kubectl top pods` and `kubectl top nodes` require the metrics-server addon to be installed in the cluster. On CCE, install it via `hcloud CCE InstallAddon` or the CCE console. If metrics-server is not installed, `top` commands will return `error: Metrics API not available`.

## Operations

| Operation | Command |
|-----------|---------|
| List pods | `kubectl --kubeconfig=<kubeconfig-path> get pods -n <namespace>` (add `-o wide` for node/IP, `-w` to watch) |
| Pod logs | `kubectl --kubeconfig=<kubeconfig-path> logs <pod> -n <namespace>` (add `--follow`, `--tail=100`, `-c <container>` for streaming/tail/sidecar) |
| Describe pod | `kubectl --kubeconfig=<kubeconfig-path> describe pod <pod> -n <namespace>` |
| Events | `kubectl --kubeconfig=<kubeconfig-path> get events -n <namespace> --sort-by='.lastTimestamp'` |
| Resource usage | `kubectl --kubeconfig=<kubeconfig-path> top pods -n <namespace>` |

## Advanced Debugging

| Operation | Command |
|-----------|---------|
| Exec into pod | `kubectl --kubeconfig=<kubeconfig-path> exec -it <pod> -n <namespace> -- sh` |
| Port-forward | `kubectl --kubeconfig=<kubeconfig-path> port-forward <pod> 8080:80 -n <namespace>` |

## Common Scenarios

### Check deployment health

```bash
kubectl --kubeconfig=<kubeconfig-path> get pods -n <namespace> -o wide
kubectl --kubeconfig=<kubeconfig-path> top pods -n <namespace>
```

### Debug crash loop

```bash
kubectl --kubeconfig=<kubeconfig-path> get pods -n <namespace>
kubectl --kubeconfig=<kubeconfig-path> describe pod <pod> -n <namespace>
kubectl --kubeconfig=<kubeconfig-path> logs <pod> -n <namespace> --previous
kubectl --kubeconfig=<kubeconfig-path> get events -n <namespace> --sort-by='.lastTimestamp'
```

### View multi-container logs

```bash
kubectl --kubeconfig=<kubeconfig-path> logs <pod> -n <namespace> -c <container>
kubectl --kubeconfig=<kubeconfig-path> logs <pod> -n <namespace> --all-containers --tail=100
```

### Check resource pressure

```bash
kubectl --kubeconfig=<kubeconfig-path> top pods -n <namespace>
kubectl --kubeconfig=<kubeconfig-path> top nodes
kubectl --kubeconfig=<kubeconfig-path> describe node <node>
```

### Interactive debugging

```bash
kubectl --kubeconfig=<kubeconfig-path> exec -it <pod> -n <namespace> -- sh
kubectl --kubeconfig=<kubeconfig-path> port-forward <pod> 8080:80 -n <namespace>
```