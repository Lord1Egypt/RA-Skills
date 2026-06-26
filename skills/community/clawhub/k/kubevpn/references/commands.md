# KubeVPN CLI Command Reference

## Table of Contents
- [connect](#connect)
- [disconnect](#disconnect)
- [quit](#quit)
- [proxy](#proxy)
- [leave](#leave)
- [sync](#sync)
- [unsync](#unsync)
- [run](#run)
- [status](#status)
- [alias](#alias)
- [connection](#connection)
- [route](#route)
- [ssh](#ssh)
- [image](#image)
- [logs](#logs)
- [reset](#reset)
- [uninstall](#uninstall)
- [upgrade / version](#upgrade--version)
- [Global Options](#global-options)
- [SSH Jump Flags](#ssh-jump-flags)

---

## connect

Connect to kubernetes cluster network. Enables direct access to Pod IPs, Service IPs, and cluster DNS from local machine.

```
kubevpn connect [flags] [options]
```

| Flag | Description |
|------|-------------|
| `--extra-cidr` | Extra CIDR to add to route table, repeatable. eg: `--extra-cidr 192.168.0.0/24` |
| `--extra-domain` | Extra domain whose resolved IP is added to route table, repeatable |
| `--extra-node-ip` | Add cluster node IPs to route table |
| `--foreground` | Run in foreground (don't daemonize) |
| `--image` | Image for server container (default: `ghcr.io/kubenetworks/kubevpn:v2.x.x`) |
| `--image-pull-secret-name` | Secret name for pulling image from private registry |
| `--manager-namespace` | Namespace of traffic manager (when installed via Helm) |
| `--transfer-image` | Transfer kubevpn image to a custom registry before use |
| `--debug` | Enable debug mode |
| `--remote-kubeconfig` | Path to kubeconfig on remote SSH server |
| + SSH jump flags | See [SSH Jump Flags](#ssh-jump-flags) |

**Examples:**
```bash
kubevpn connect
kubevpn connect -n staging
kubevpn connect --extra-cidr 192.168.0.159/24 --extra-cidr 192.168.1.160/32
kubevpn connect --extra-node-ip
# Via SSH bastion
kubevpn connect --ssh-addr 192.168.1.100:22 --ssh-username root --ssh-keyfile ~/.ssh/ssh.pem
kubevpn connect --ssh-alias dev
```

---

## disconnect

Disconnect from a kubernetes cluster network. Automatically leaves any proxy/sync resources that depend on the connection, and cleans up DNS and hosts entries.

```
kubevpn disconnect [connectID] [flags]
```

| Flag | Description |
|------|-------------|
| `--all` | Disconnect from all clusters |

**Examples:**
```bash
kubevpn disconnect 03dc50feb8c3   # disconnect specific connection (ID from `kubevpn status`)
kubevpn disconnect --all          # disconnect all
```

---

## quit

Disconnect from cluster, leave proxy resources, quit the kubevpn daemon gRPC server, and cleanup DNS/hosts. More thorough than `disconnect`.

```
kubevpn quit
```

---

## proxy

Proxy kubernetes workloads inbound traffic into local PC.

Without `--headers`: intercepts **all** inbound traffic (including L4/TCP/UDP).
With `--headers`: mesh mode — only traffic matching headers routes to local; other traffic hits the cluster pod normally. Supports HTTP, gRPC, Thrift, WebSocket.

Also connects to cluster network automatically (like `connect`).

```
kubevpn proxy <workload> [flags] [options]
```

Supported workload types: `deployment`, `service`, and multiple at once.

| Flag | Short | Description |
|------|-------|-------------|
| `--headers` | `-H` | `KEY=VALUE` header for mesh routing. Repeatable (AND logic). eg: `--headers foo=bar --headers env=dev` |
| `--portmap` | | Map container port to local port. Format: `[tcp/udp]/containerPort:localPort`. eg: `--portmap 9080:8080`, `--portmap udp/9080:5000` |
| `--extra-cidr` | | Extra CIDRs for route table |
| `--extra-domain` | | Extra domains for route table |
| `--extra-node-ip` | | Add node IPs to route table |
| `--foreground` | | Foreground hang up |
| `--image` | | Sidecar image override |
| `--image-pull-secret-name` | | Image pull secret |
| `--manager-namespace` | | Traffic manager namespace |
| `--debug` | | Enable debug mode |
| + SSH jump flags | | See [SSH Jump Flags](#ssh-jump-flags) |

**Examples:**
```bash
# All traffic to local
kubevpn proxy deployment/productpage

# Multiple workloads
kubevpn proxy deployment/authors deployment/productpage
kubevpn proxy deployment authors productpage

# Mesh: only header foo=bar hits local
kubevpn proxy deployment/productpage --headers foo=bar

# Port mapping
kubevpn proxy deployment/productpage --portmap 9080:8080
kubevpn proxy deployment/productpage --portmap udp/9080:5000

# Via SSH
kubevpn proxy deployment/productpage --ssh-addr 192.168.1.100:22 --ssh-username root --ssh-keyfile ~/.ssh/ssh.pem --headers foo=bar
```

---

## leave

Leave proxy resource and restore workload to its original spec.

The last person to leave triggers full cleanup of injected containers (`vpn`, `envoy-proxy`). Others just remove themselves from the mesh routing.

```
kubevpn leave <workload> [flags] [options]
```

**Examples:**
```bash
kubevpn leave deployment/authors
kubevpn leave deployment/productpage -n bookinfo
```

---

## sync

Sync local directory to a cloned workload running **inside the cluster**, with the same env/volume/network as the target. Supports mesh routing via `--headers`.

```
kubevpn sync <workload> [flags] [options]
```

| Flag | Short | Description |
|------|-------|-------------|
| `--sync` | | Local-to-remote dir mapping. Format: `LOCAL_DIR:REMOTE_DIR`. eg: `--sync ~/code:/app/code` |
| `--headers` | `-H` | Mesh routing headers (AND logic) |
| `--container` | `-c` | Container name (default: first or annotated container) |
| `--target-image` | | Image for the sync container (default: origin image) |
| `--image` | | kubevpn sidecar image override |
| `--debug` | | Enable debug mode |
| + SSH jump flags | | See [SSH Jump Flags](#ssh-jump-flags) |

**Examples:**
```bash
kubevpn sync deployment/productpage --sync ~/code:/code/app
kubevpn sync deployment/productpage --sync ~/code:/code/app --headers foo=bar
```

---

## unsync

Remove sync resources created by `kubevpn sync`.

```
kubevpn unsync <sync-resource-name> [flags] [options]
```

**Examples:**
```bash
kubevpn unsync deployment/authors-sync-645d7
```

---

## run

Run kubernetes workload in local Docker container with same volumes, env vars, and network as cluster pod.

What it does:
1. Downloads volumes (mountPath) and mounts them to Docker container
2. Connects to cluster network and attaches it to the Docker container
3. Gets all env vars from the pod and sets them on the container

```
kubevpn run TYPE/NAME [-c CONTAINER] [flags] -- [args...] [options]
```

| Flag | Short | Description |
|------|-------|-------------|
| `--headers` | `-H` | Mesh routing headers |
| `--no-proxy` | | Run locally without intercepting cluster traffic |
| `--entrypoint` | | Override container ENTRYPOINT |
| `--dev-image` | | Use a different image (eg. dev/debug image) |
| `--container` | `-c` | Container name to run |
| `--connect-mode` | | `host` or `container` network mode (default: `host`) |
| `--image` | | kubevpn sidecar image |
| `--platform` | | Platform for multi-platform images |
| `--privileged` | | Run container with extended privileges (default: `true`) |
| `--publish` | `-p` | Publish container port(s) to host |
| `--publish-all` | `-P` | Publish all exposed ports to random ports |
| `--expose` | | Expose a port or range |
| `--volume` | `-v` | Bind mount a volume |
| `--rm` | | Auto-remove container when it exits |
| `--pull` | | Pull policy: `always`, `missing`, `never` (default: `missing`) |
| `--debug` | | Enable debug mode |
| + SSH jump flags | | See [SSH Jump Flags](#ssh-jump-flags) |

**Examples:**
```bash
kubevpn run deployment/productpage
kubevpn run deployment/productpage --headers foo=bar
kubevpn run deployment/productpage --no-proxy

# Open an interactive shell
kubevpn run deployment/authors -n default --entrypoint /bin/bash

# Use a dev image
kubevpn run deployment/authors --dev-image golang:1.21 --entrypoint bash

# Via SSH alias
kubevpn run deployment/authors -n default --kubeconfig ~/.kube/config --ssh-alias dev --entrypoint /bin/bash
```

---

## status

Show connect status and list proxy/sync resources.

```
kubevpn status [flags]
```

| Flag | Short | Description |
|------|-------|-------------|
| `--output` | `-o` | Output format: `table` (default), `json`, `yaml`, `wide` |
| `--alias` | | Query by alias config name |
| `--kubevpnconfig` | `-f` | Path to kubevpn config file |
| `--remote` | `-r` | Remote config file URL |

**Examples:**
```bash
kubevpn status
kubevpn status -o json
kubevpn status --alias dev_new
```

---

## alias

Execute commands using named config aliases, defined in `~/.kubevpn/config.yaml`. Supports `Needs` dependency chains (connect to cluster A before cluster B).

```
kubevpn alias <alias-name> [flags]
```

| Flag | Short | Description |
|------|-------|-------------|
| `--kubevpnconfig` | `-f` | Path to kubevpn config file (default: `~/.kubevpn/config.yaml`) |
| `--remote` | `-r` | Remote config file URL |

**Config file format** (`~/.kubevpn/config.yaml`):

```yaml
Name: dev
Description: dev k8s environment
Needs: jumper        # connect to 'jumper' first, then 'dev'
Flags:
- connect
- --kubeconfig=~/.kube/config
- --namespace=default
---
Name: jumper
Description: jumper k8s environment
Flags:
- connect
- --kubeconfig=~/.kube/jumper_config
- --namespace=test
---
Name: all-in-one
Description: inline kubeconfig via JSON
Flags:
- connect
- --kubeconfig-json={"apiVersion":"v1","clusters":[...]}
- --namespace=test
```

**Examples:**
```bash
kubevpn alias dev       # connect to jumper first, then dev (due to Needs)
kubevpn alias jumper    # connect to jumper only
```

---

## connection

Manage active connections.

```
kubevpn connection <subcommand>
kubevpn conn <subcommand>        # alias
```

### connection list

```bash
kubevpn connection list
kubevpn conn ls         # alias
```

### connection use

Switch current active connection (affects which connection `sync`/`unsync` operate on).

```bash
kubevpn connection use 03dc50feb8c3
```

---

## route

Manage the route table of the current TUN device.

```
kubevpn route <subcommand>
```

### route add

```bash
kubevpn route add 198.19.0.1/32
```

### route delete

```bash
kubevpn route delete 198.19.0.1/32
```

### route search

```bash
kubevpn route search 198.19.0.1
```

---

## ssh

SSH into a jump server directly (without connecting to a cluster). Supports the same ProxyJump chains as other commands.

```
kubevpn ssh [flags] [options]
```

| Flag | Description |
|------|-------------|
| `--lite` | Lite mode: only connect to SSH server (no two-way tunnel). Default (full) mode also creates a tunnel for inner IP communication |
| `--platform` | SSH server platform, used if kubevpn needs to be installed (default: `linux/amd64`) |
| `--extra-cidr` | Extra CIDRs to add to route table |
| + SSH jump flags | See [SSH Jump Flags](#ssh-jump-flags) |

**Examples:**
```bash
kubevpn ssh --ssh-addr 192.168.1.100:22 --ssh-username root --ssh-keyfile ~/.ssh/ssh.pem
kubevpn ssh --ssh-alias dev
```

---

## image

Manage kubevpn images (copy between registries or re-tag).

### image copy

```
kubevpn image copy <src_image_ref> <dst_image_ref>
kubevpn image cp  <src_image_ref> <dst_image_ref>   # alias
```

Only transfers layers that don't already exist at the target. Within the same registry, attempts to mount layers between repositories.

**Examples:**
```bash
# Copy to private registry (useful when ghcr.io is not accessible)
kubevpn image copy ghcr.io/kubenetworks/kubevpn:latest registry.example.org/kubevpn/kubevpn:latest

# Re-tag
kubevpn image copy ghcr.io/kubenetworks/kubevpn:latest ghcr.io/kubenetworks/kubevpn:v2.3.4
```

---

## logs

Print logs for the kubevpn daemon gRPC server (both sudo daemon and daemon gRPC server logs).

```
kubevpn logs [flags]
```

| Flag | Short | Description |
|------|-------|-------------|
| `--follow` | `-f` | Stream logs continuously |
| `--lines` | `-l` | Number of recent log lines to display (default: `10`) |

**Examples:**
```bash
kubevpn logs
kubevpn logs -f
kubevpn logs -l 50
```

---

## reset

Force-reset a workload to its original spec, removing injected `envoy-proxy` and `vpn` containers and restoring service mesh rules. Use when `leave` doesn't work.

```
kubevpn reset <workload> [flags] [options]
```

**Examples:**
```bash
kubevpn reset deployment/productpage
kubevpn reset deployment/productpage -n test
kubevpn reset deployment/productpage --ssh-alias dev
```

---

## uninstall

Remove **all** kubevpn resources from the cluster (deployments, services, serviceAccounts, etc.). Also removes local Docker containers/networks created by kubevpn, cleans up hosts entries and DNS settings.

```
kubevpn uninstall [flags] [options]
```

**Examples:**
```bash
kubevpn uninstall
kubevpn uninstall -n test
kubevpn uninstall --ssh-addr 192.168.1.100:22 --ssh-username root --ssh-keyfile ~/.ssh/ssh.pem
```

---

## upgrade / version

```bash
kubevpn upgrade    # Upgrade client to latest version
kubevpn version    # Print client version info
```

---

## Global Options

Available on all commands (via `kubevpn options`):

| Flag | Description |
|------|-------------|
| `--kubeconfig` | Path to kubeconfig file |
| `--context` | Kubeconfig context to use |
| `-n`, `--namespace` | Namespace scope |
| `--cluster` | Kubeconfig cluster to use |
| `--user` | Kubeconfig user to use |
| `--server` / `-s` | Kubernetes API server address |
| `--token` | Bearer token for API server auth |
| `--as` | Username to impersonate |
| `--as-group` | Group to impersonate (repeatable) |
| `--insecure-skip-tls-verify` | Skip TLS certificate validation |
| `--certificate-authority` | Path to CA cert file |
| `--client-certificate` | Path to client cert file |
| `--client-key` | Path to client key file |
| `--request-timeout` | Timeout per server request (eg: `30s`, `2m`) |

---

## SSH Jump Flags

Available on `connect`, `proxy`, `run`, `sync`, `reset`, `uninstall`, `ssh`:

| Flag | Description |
|------|-------------|
| `--ssh-addr` | SSH jump server address `HOST:PORT` |
| `--ssh-username` | SSH username |
| `--ssh-password` | SSH password |
| `--ssh-keyfile` | Path to SSH private key file |
| `--ssh-alias` | SSH config alias from `~/.ssh/config` |
| `--ssh-jump` | Inline ProxyJump config string eg: `--ssh-addr jump.example.org --ssh-username user --gssapi-password xxx` |
| `--remote-kubeconfig` | Path to kubeconfig on remote SSH server |
| `--gssapi-keytab` | GSSAPI keytab file path |
| `--gssapi-cache` | GSSAPI cache file path (from `kinit -c`) |
| `--gssapi-password` | GSSAPI password |

ProxyJump chain example:
```
┌──────┐     ┌──────┐     ┌──────┐                 ┌────────────┐
│  pc  ├────►│ ssh1 ├────►│ ssh2 ├─────►... ─────► │ api-server │
└──────┘     └──────┘     └──────┘                 └────────────┘

kubevpn connect --ssh-alias <alias>
```
