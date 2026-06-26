---
name: kubevpn
description: >
  KubeVPN is a cloud-native dev tool to connect local machine to Kubernetes cluster networks.
  Use this skill when the user mentions: kubevpn, KubeVPN, or any of the following scenarios:
  (1) Connect local machine to k8s/Kubernetes cluster network or internal services;
  (2) Access pod IPs, service IPs, or cluster DNS from local;
  (3) Intercept or proxy inbound traffic of a k8s workload/deployment/service to local PC;
  (4) Local development against a remote Kubernetes cluster;
  (5) Debug a k8s service locally while it receives real cluster traffic;
  (6) Run a Kubernetes pod/deployment locally in Docker with same env vars, volumes, network;
  (7) Sync local source code into a running cluster workload (hot-reload in cluster env);
  (8) SSH bastion/jump host to reach a private k8s API server;
  (9) 本地连接 Kubernetes 集群网络 / 本地调试 k8s 服务 / 拦截集群流量到本地 / 本地运行 k8s workload。
---

# KubeVPN

KubeVPN bridges a local machine to a remote Kubernetes cluster network. Core workflows:
**connect** (VPN tunnel), **proxy** (traffic interception), **run** (local pod simulation), **sync** (local code → cluster clone).

## Installation

```bash
brew install kubevpn                              # macOS
curl -fsSL https://kubevpn.dev/install.sh | sh   # Linux/macOS
kubectl krew install kubevpn/kubevpn              # kubectl plugin
scoop bucket add extras && scoop install kubevpn  # Windows
```

## Core Workflows

### 1. Connect — Access cluster network

```bash
kubevpn connect
kubevpn connect -n <namespace>
kubevpn connect --context <context-name>
kubevpn disconnect --all
```

After connecting, access cluster resources directly:
```bash
ping <pod-ip>
curl <service-name>:<port>
curl <service-name>.<namespace>.svc.cluster.local:<port>
```

### 2. Proxy — Intercept inbound traffic

Intercepts inbound cluster traffic for a workload and forwards to local machine.
`proxy` also auto-connects to the cluster if not already connected.

```bash
kubevpn proxy deployment/<name>
kubevpn proxy deployment/<name> -n <namespace>

# Mesh mode: only requests with matching headers go to local
kubevpn proxy deployment/<name> --headers foo=bar
kubevpn proxy deployment/<name> --headers foo=bar --headers env=dev  # AND logic

# Port mapping
kubevpn proxy deployment/<name> --portmap 9080:8080
kubevpn proxy deployment/<name> --portmap udp/9080:5000

# Multiple workloads at once
kubevpn proxy deployment/authors deployment/productpage

kubevpn leave deployment/<name>   # stop proxying, restore workload
```

### 3. Run — Simulate pod locally in Docker

Runs a workload in a local Docker container with identical env vars, volumes, and network.

```bash
kubevpn run deployment/<name>
kubevpn run deployment/<name> --entrypoint /bin/bash   # interactive shell
kubevpn run deployment/<name> --no-proxy               # no traffic interception
kubevpn run deployment/<name> --dev-image golang:1.21 --entrypoint bash
kubevpn run deployment/<name> --headers foo=bar        # mesh mode
```

### 4. Sync — Hot-reload local code in cluster

Clones the workload **inside the cluster** and syncs a local directory into the clone.
The clone has the same env/volumes/network as the original. Supports mesh routing via `--headers`.

```bash
kubevpn sync deployment/<name> --sync ~/code:/app/code
kubevpn sync deployment/<name> --sync ~/code:/app/code --headers foo=bar

kubevpn unsync deployment/<name>-sync-xxxxx   # remove sync resource
```

### 5. Alias — Named config shortcuts

Define named aliases in `~/.kubevpn/config.yaml` to avoid repeating long flags. Supports `Needs` dependency chains (connect to cluster A before cluster B).

```bash
kubevpn alias dev       # runs the flags defined under "dev" in config
kubevpn alias jumper    # connect to jumper cluster only
```

See [commands.md](references/commands.md#alias) for config file format.

### Via SSH Bastion / Jump Host

All connect/proxy/run/sync commands support SSH jump:
```bash
kubevpn connect --ssh-addr 192.168.1.100:22 --ssh-username root --ssh-keyfile ~/.ssh/id_rsa
kubevpn connect --ssh-alias dev                           # uses ~/.ssh/config alias
kubevpn proxy deployment/<name> --ssh-alias dev --headers foo=bar
```

## Reference Files

- **[commands.md](references/commands.md)** — Full flag reference for all kubevpn commands (including `alias`, `connection`, `route`, `ssh`, `image`, `logs`, `quit`)
- **[architecture.md](references/architecture.md)** — How connect/proxy/mesh modes work internally

## Common Patterns

| Goal | Command |
|------|---------|
| Access cluster IPs/services locally | `kubevpn connect` |
| Connect using a saved alias | `kubevpn alias <name>` |
| Debug a service (receive all its traffic) | `kubevpn proxy deployment/<name>` |
| Debug only my requests (don't break others) | `kubevpn proxy deployment/<name> --headers x-user=me` |
| Reproduce a pod environment locally | `kubevpn run deployment/<name> --entrypoint sh` |
| Hot-reload local code in cluster env | `kubevpn sync deployment/<name> --sync ~/code:/app` |
| Check connection status | `kubevpn status` |
| Force-restore a stuck workload | `kubevpn reset deployment/<name>` |
| Fully stop kubevpn (daemon + connections) | `kubevpn quit` |
| Remove all kubevpn from cluster | `kubevpn uninstall` |
| Copy image to private registry | `kubevpn image copy <src> <dst>` |
| Tail daemon logs | `kubevpn logs -f` |

## Notes

- `proxy`, `run`, and `sync` auto-connect to the cluster if not already connected
- Multiple clusters can be connected simultaneously; use `kubevpn status` or `kubevpn connection list` to inspect
- `disconnect` cleans up DNS/hosts; `quit` also stops the daemon gRPC server entirely
- Server components are auto-deployed on first use (or pre-install: `helm install kubevpn kubevpn/kubevpn`)
- Supports HTTP, gRPC, Thrift, WebSocket, TCP, UDP, ICMP
- Use `kubevpn reset deployment/<name>` if a workload gets stuck with injected containers
- Use `kubevpn image copy` to mirror images to a private registry when `ghcr.io` is not accessible
