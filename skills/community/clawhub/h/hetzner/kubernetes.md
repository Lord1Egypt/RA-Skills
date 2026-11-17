# Kubernetes and k3s on Hetzner — Cluster Plumbing the Provider Does Not Give You

Scope: running a cluster on Hetzner infrastructure. Manifest authoring and general cluster debugging are a separate skill (`k8s`).

**Before proposing a cluster**, read `operations_model` in `~/Clawic/data/hetzner/config.yaml` and `## Current Infrastructure` — the honest first question is whether Compose on two servers already covers this workload (`production.md`).

**Contents:** [There Is No Managed Kubernetes](#there-is-no-managed-kubernetes) · [Is a Cluster the Right Answer](#is-a-cluster-the-right-answer) · [MTU: The Thing That Breaks Clusters Here](#mtu-the-thing-that-breaks-clusters-here) · [Address Planning](#address-planning) · [The Two Hetzner Integrations](#the-two-hetzner-integrations) · [Load Balancer Services](#load-balancer-services) · [Node Layout](#node-layout) · [k3s Specifics](#k3s-specifics) · [Cost Shape](#cost-shape) · [Cluster Failure Signatures](#cluster-failure-signatures)

## There Is No Managed Kubernetes

No control plane as a service, no managed node groups, no cluster autoscaler out of the box. You run the control plane, you upgrade it, and you are on call for etcd. Everything in this file assumes that.

What the provider does give you, and what makes a self-run cluster workable:

- A cloud controller manager that turns `Service type=LoadBalancer` into a real load balancer and manages node addresses and routes.
- A CSI driver that turns `PersistentVolumeClaim` into a Volume, attached and mounted automatically.
- Private networks and firewalls to keep the cluster's internal traffic off the public internet.

## Is a Cluster the Right Answer

| Situation | Answer |
|---|---|
| One or two services, one deployer | Docker Compose on one or two servers; the cluster is pure overhead |
| Several services, one deployer, wants rolling deploys | k3s on three nodes, or Compose plus a reverse proxy — decide by whether restarts need to be zero-downtime |
| Several deployers, or a platform other teams consume | A cluster earns its keep: the API is the interface |
| A workload that genuinely scales in and out during the day | A cluster, plus a scaling mechanism you build (`automation.md`) |
| "Because it is the standard" | Not a reason; the operational cost here is real and unshared |

The frontier is whether more than one person deploys. Below that, the cluster is a second production system to operate.

## MTU: The Thing That Breaks Clusters Here

Hetzner private networks are **MTU 1450**, and CNIs default to assumptions that do not hold (`network.md`). The result is a cluster that passes every smoke test and hangs on large payloads: image pulls stall at a percentage, large API responses never arrive, TLS to some services works and to others does not.

The arithmetic, per encapsulation:

| Path | Ceiling |
|---|---|
| Node interface on a private network | 1450 |
| VXLAN (Flannel default) over that | 1400 |
| WireGuard-backed CNI over that | 1370 |
| Nested (WireGuard inside VXLAN, or a service mesh on top) | Subtract again — compute it, do not guess |

Configure the CNI's MTU explicitly at install time. Changing it later requires restarting every pod's networking, which on a live cluster is an outage. Verify with a large-payload test between pods on different nodes, not between pods on the same node — same-node traffic never leaves the host and always passes.

## Address Planning

Three ranges must not overlap, and fixing an overlap later means rebuilding the cluster:

```
10.<env>.0.0/16     Hetzner private network (nodes)
10.42.0.0/16        pod CIDR        (k3s default — confirm it does not collide)
10.43.0.0/16        service CIDR    (k3s default)
```

Also check against anything the cluster will ever peer with: an office VPN, another provider, a partner's network. The provider's private network is where the collision shows up, because nodes get addresses from it.

## The Two Hetzner Integrations

**Cloud controller manager** — needs a read-write API token for the project (a secret in the cluster, referenced by pointer in any notes, `security.md`). It provisions load balancers for `Service type=LoadBalancer`, sets node addresses, and can manage routes for the private network. Without it, `type=LoadBalancer` services stay pending forever.

**CSI driver** — turns PVCs into Volumes. Consequences that come straight from the volume rules (`storage.md`):

- Volumes are **location-bound**: a pod with a volume can only schedule onto nodes in that location. A multi-location cluster does not get portable storage.
- Volumes are **ReadWriteOnce**: one node at a time. A Deployment with two replicas sharing one PVC does not work; use a StatefulSet with a volume per replica, or shared storage over the network.
- 10 GB minimum per volume, and up to 16 attached per node — which caps how many volume-backed pods a node can host, well before CPU does.
- Volumes are not deleted with the pod unless the reclaim policy says so. Orphaned PVs bill exactly like orphaned volumes (`costs.md`).

Both components need their versions to track the Kubernetes version. An upgrade that moves the cluster ahead of the integrations breaks load balancers or storage, usually not both at once, which makes it hard to diagnose.

## Load Balancer Services

- A `Service type=LoadBalancer` creates a real, billed load balancer (~€6/mo). Ten such services is ten load balancers — use one ingress controller with a single load balancer in front instead.
- Annotations control location, network, algorithm, health check and the PROXY protocol. PROXY protocol needs both sides configured; enabling it only on the load balancer produces malformed requests, not an error (`network.md`).
- Point the load balancer at nodes over the private network where possible: it keeps cluster traffic off public addresses and off the traffic allowance.
- Managed certificates on that load balancer require the zone in Hetzner DNS (`dns.md`); otherwise terminate TLS in the ingress controller.

## Node Layout

| Role | Type | Notes |
|---|---|---|
| Control plane | CAX/CX, small but not tiny | etcd is latency-sensitive to disk; do not put it on the cheapest thing available and expect quiet |
| Workers | CAX (arm64) | Cheapest per core; requires multi-arch images (below) |
| Storage-heavy workers | Node with attached volumes | Bound to one location by the CSI |
| Database | **Outside the cluster**, on a CCX with its own volume | Stateful workloads gain the least from the cluster and lose the most when it misbehaves |

- Mixing arm64 and x86 nodes in one cluster works, and every image then needs a multi-arch manifest. Check the manifest, not just that it runs on your laptop; a single-arch image on a mixed cluster produces `exec format error` on some nodes and works on others.
- Control-plane nodes belong in a spread placement group from creation (`production.md`) — three control-plane nodes on one physical host is not high availability.
- Firewall the cluster: node-to-node ports open only within the private network, API server restricted to known sources, nothing cluster-internal exposed publicly (`firewall.md`).

## k3s Specifics

- Single binary, small footprint, an appropriate default for this provider: three nodes of a cheap ARM type run a real cluster.
- Its bundled defaults (an ingress controller, a service load balancer, a local-path storage class) overlap with the Hetzner integrations. Decide explicitly which to disable at install — running the bundled service load balancer *and* the cloud controller manager produces two things fighting over the same service.
- The datastore choice (embedded etcd versus an external database) is made at install and is painful to change. Odd numbers of control-plane nodes for embedded etcd.
- The token that joins nodes is a credential: pointer only, never in a committed cloud-init (`automation.md`).
- Upgrades are fast and therefore easy to do carelessly. Drain, upgrade, verify, next.

## Cost Shape

A three-node cluster of small ARM servers plus one load balancer is genuinely inexpensive — usually less than a single managed control plane elsewhere. The costs that are not in that number:

- One load balancer per exposed service unless an ingress controller consolidates them.
- A volume per stateful pod, at the 10 GB minimum even when the pod needs 1 GB.
- Orphaned PVs and snapshots from deleted namespaces (`costs.md`).
- The engineering time to operate a control plane, which is the largest line and does not appear on the invoice.

## Cluster Failure Signatures

| Signature | Cause | First move |
|---|---|---|
| Image pulls stall partway, large responses hang | CNI MTU above the 1450 ceiling | Compute the ceiling for the encapsulation in use and reinstall the CNI with it |
| `Service type=LoadBalancer` stuck pending | Cloud controller manager missing, or its token lacks write | Check the CCM logs; verify the token is read-write for the project |
| Pod stuck `ContainerCreating` with a volume | CSI cannot attach: wrong location, node volume limit reached, or the volume is attached elsewhere | Check the node's location against the volume's, then the attachment count |
| Two replicas, one pod pending forever | PVC is ReadWriteOnce | StatefulSet with a volume per replica, or network storage |
| `exec format error` on some nodes only | Single-arch image on a mixed arm64/x86 cluster | Multi-arch manifest, or a node selector by architecture |
| Cluster fine, one node unreachable | Host-level: firewall, disk full, OOM — not the cluster | Console into the node (`servers.md`), then `linux` |
| Everything degrades at once, no obvious cause | Control-plane node sharing a physical host with a worker that saturated it | Verify placement group membership |

**Write it down.** The cluster's node list goes into `~/Clawic/data/servers/servers.md` like any other server (`Role: k8s-control` / `k8s-worker`). The pieces that took real work — the CNI MTU actually configured, the CIDR plan, the CCM and CSI versions matched to the Kubernetes version, the join procedure — go into `~/Clawic/data/hetzner/artifacts/cluster-<name>.md` with its `## Boxes` line. Nobody re-derives an MTU at 3am twice.
