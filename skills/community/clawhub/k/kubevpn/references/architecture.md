# KubeVPN Architecture

## Three Operating Modes

### Connect Mode (VPN Tunnel)

Creates a TUN virtual interface (`tun0`) on the local machine. Traffic destined for cluster
CIDRs (pod network, service network) is routed through this interface into the cluster via
a port-forward tunnel to a `traffic-manager` pod.

```
Local machine
  └─ tun0 (virtual interface)
       └─ port-forward tunnel
            └─ traffic-manager pod (cluster)
                  └─ cluster network (pods, services)
```

DNS resolution for cluster service names also works through this tunnel.

### Proxy / Reverse Mode (Traffic Interception)

Builds on connect mode. A sidecar container is injected into the target workload's pod.
The sidecar uses iptables to intercept **all** inbound traffic and forward it back through
the tunnel to the local machine.

```
Cluster traffic → target pod (sidecar injected)
                      └─ iptables redirect → tunnel → local machine
```

The original container in the pod still exists but receives no traffic while the proxy is active.
`kubevpn leave` removes the sidecar and restores iptables rules.

### Mesh Mode (Header-Based Routing)

Builds on proxy mode. Instead of intercepting all traffic, an **Envoy proxy** is injected
alongside the sidecar. Envoy performs header-based routing:

```
Cluster traffic → Envoy proxy (injected)
                      ├─ header matches? → tunnel → local machine
                      └─ no match?       → original pod container
```

This allows selective traffic routing: only requests with matching headers (e.g., `foo: bar`)
go to the local machine, while all other traffic continues to the cluster pod normally.
Ideal for shared/staging environments where you don't want to break other users.

## Server Component (traffic-manager)

On first `kubevpn connect`, kubevpn auto-deploys a `traffic-manager` deployment in the target
namespace. This pod:
- Terminates the TUN tunnel from the local machine
- Acts as a gateway for routing traffic between local and cluster networks
- Manages sidecar injection and iptables rules for proxy/mesh modes

Can be pre-installed via Helm:
```bash
helm repo add kubevpn https://kubevpn.dev/helm
helm install kubevpn kubevpn/kubevpn -n <namespace>
```

## Protocol Support

| Protocol | Support |
|----------|---------|
| TCP | Full (all OSI L3+) |
| UDP | Full |
| ICMP | Full (ping works) |
| HTTP | Full (including mesh header routing) |
| gRPC | Full |
| WebSocket | Full |

## Multiple Cluster Connections

KubeVPN supports simultaneous connections to multiple clusters. Each connection gets its own
TUN interface and routing table entries. Use `kubevpn status` to see all active connections
and their IDs. Use `kubevpn disconnect <id>` to disconnect a specific cluster.

## Local Run Mode (Docker)

`kubevpn run` queries the Kubernetes API to retrieve the workload's pod spec, then:
1. Pulls the same container image
2. Creates a Docker container with the same env vars and volume mounts
3. Attaches the container to the kubevpn TUN network so it has full cluster access
4. Optionally injects a traffic sidecar (same as proxy mode) so cluster traffic routes to it

This lets you run and debug the exact production container image locally with full cluster
connectivity. Use `--no-proxy` to skip traffic interception (no cluster resources are modified);
without `--no-proxy`, a sidecar is injected to route cluster traffic to the local container.
