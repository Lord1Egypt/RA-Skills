# Networking — Private Networks, Routes, IPs, and the MTU That Breaks Things

Scope: connectivity between servers and to the internet. Packet filtering is a separate route from the Quick Reference (`firewall.md`).

**Before designing an address plan**, read `## Current Infrastructure` in `~/Clawic/data/hetzner/memory.md` and `conventions.network_cidr` in `config.yaml` — a second, overlapping CIDR is not fixable later without renumbering.

**Contents:** [MTU 1450](#mtu-1450) · [Private Networks](#private-networks) · [No Default Route](#no-default-route) · [NAT Gateway](#nat-gateway) · [IPv4, IPv6, and Going Without](#ipv4-ipv6-and-going-without) · [Floating IPs and Failover](#floating-ips-and-failover) · [Load Balancers](#load-balancers) · [Crossing Locations and Providers](#crossing-locations-and-providers) · [vSwitch: Dedicated Meets Cloud](#vswitch-dedicated-meets-cloud) · [Address Plan](#address-plan)

## MTU 1450

Hetzner private networks use an MTU of **1450**, not 1500. This single number is behind most "it works for small requests and hangs for large ones" reports on this provider.

- The symptom is never a clean error: TLS handshakes complete, small JSON responses work, a file upload or a large query result hangs until something times out. Path MTU discovery is supposed to fix it and does not, because the ICMP messages that carry the discovery are often filtered.
- Test it: `ping -M do -s 1422 <private-ip>` (1422 payload + 28 header = 1450). If that passes and `-s 1450` fails, the ceiling is confirmed.
- Set the interface MTU to 1450 on every server attached to a private network. Cloud-init images generally do this already; a hand-configured interface or a custom netplan does not.
- **Every encapsulation layer takes more.** WireGuard over a private network: 1450 − 80 = **1370**. VXLAN (Flannel default): 1450 − 50 = **1400**. IPsec: budget 1400 or less. A Kubernetes CNI left at its 1500 default over a Hetzner private network is the classic broken cluster (`kubernetes.md`).
- Jumbo frames are not available. Designs that assume 9000 do not apply here.

## Private Networks

- One network spans one **location**. Servers in `fsn1` and `hel1` cannot share a private network.
- Ranges come from the RFC1918 space; pick one `/16` per environment and carve `/24` subnets by role. Overlap with anything the user might later peer with — an office VPN, another provider, a Kubernetes pod CIDR — is the mistake that forces a full renumber.
- **A private network is a flat trust zone.** There is no segmentation and no filtering between its members: the cloud firewall does not apply here (`firewall.md`). If a database must not be reachable by a build agent on the same network, that is a host-firewall rule or a bind address, not a cloud rule.
- Attaching a server to a network is a live operation and gives it a second interface. Bind services deliberately: a service left on `0.0.0.0` is now on both the public and the private side.
- Servers get a stable private IP for the lifetime of their attachment — use it in configuration in preference to public addresses, because private traffic does not count against the traffic allowance.

## No Default Route

Attaching a server to a private network does **not** give it internet access. The network carries no default route and no NAT. A server with no public IPv4 and no IPv6 route can reach its neighbours and nothing else — including the package mirrors it needs on first boot.

Three ways out, in order of preference:

1. **Keep IPv6 only.** The server keeps a public IPv6 address, reaches anything with an AAAA record, and costs nothing extra. Fails against IPv4-only endpoints — which still includes some package mirrors, container registries, and payment APIs.
2. **NAT gateway** (below). One server with a public IPv4 does the egress for the subnet.
3. **Keep the IPv4.** Costs roughly €0.60/month per server and is the right answer for a handful of machines. The saving only becomes interesting at fleet scale.

## NAT Gateway

Pattern: one small server (a CAX11 is enough for most egress) with a public IPv4, masquerading for a subnet, plus a route in the network that points the subnet's default at it.

Three failure modes to design against before choosing this:

- **It is a single point of failure** for every outbound connection of every server behind it. A reboot for kernel updates is an egress outage. HA means a second gateway plus a mechanism to move the route — that is real work, not a checkbox.
- **IP forwarding and masquerading must survive reboot** (persisted sysctl and firewall rules), or the subnet silently loses egress the next time the gateway restarts.
- **All egress traffic now counts against one server's allowance**, and its public IP is the reputation your outbound traffic carries (`mail.md`).

For small fleets, paying for the IPv4 addresses is usually cheaper than operating a gateway. Say the arithmetic out loud: 10 servers × ~€0.60 = ~€6/month versus a CAX11 plus the on-call surface.

## IPv4, IPv6, and Going Without

| Address type | Behaviour |
|---|---|
| Primary IPv4 | Billed per address (~€0.60/mo), attached to a server or standing alone. **Survives server deletion unless auto-delete was set** — a top source of invoice mystery (`costs.md`) |
| Primary IPv6 | Every server gets a `/64` at no extra cost; use addresses from it freely |
| Floating IP | A separate, movable address for failover (below) |

- Deleting a server does not necessarily delete its address. After every teardown, list unassigned primary IPs.
- rDNS is set per address and matters for outbound mail and for some API allowlists (`mail.md`).
- An IPv6-only fleet behind an IPv4 load balancer is a working pattern: the LB has the public IPv4, the backends do not.

## Floating IPs and Failover

A Floating IP moves between servers through the API, which is what makes active/passive failover possible — but **the panel move alone does nothing**. The target server must have the address configured on its interface, or the packets arrive and are dropped.

Checklist for a working failover pair:

1. The floating IP is configured on *both* servers (on the passive one it is idle, which is fine).
2. Failover automation calls the API to move the assignment **and** verifies the new owner answers on it.
3. Something fences the old owner, or both answer and you get a split brain.
4. The failover is tested on a schedule, and the measured time goes into `deploys/<year>.md` under recovery drills.

For most stateless web tiers, a load balancer with health checks is simpler and better than a floating IP pair.

## Load Balancers

- Targets can be servers or IPs, and must be reachable from the LB — same location, and same network for private targets. A target in another location silently never becomes healthy.
- Health checks decide traffic: wrong path, wrong port, or a matcher that does not match produces a `503` with every backend up (`debug.md`).
- **PROXY protocol** is how the backend learns the client IP. Enable it on the LB *and* configure the backend to expect it — one side alone produces garbled requests, not a clean error.
- Managed TLS certificates require the zone to be hosted in Hetzner DNS (`dns.md`). Otherwise, upload a certificate or terminate TLS on the backend.
- Targets and services are capped per LB type; check the cap before designing a fan-out.
- One backend does not need a load balancer: Caddy or nginx on the server does TLS and health for free. The LB earns its ~€6/month at two backends, or when you want the health-based removal.

## Crossing Locations and Providers

Private networks stop at the location boundary. To connect `fsn1` to `hel1`, to another provider, or to an office:

- **WireGuard** is the default: small, fast, and the only thing you have to maintain is the key material and the MTU (1370 over a private network, or 1420 over the public internet). Keys are secrets — pointer only, never in `~/Clawic/data/` (`security.md`).
- Route the tunnel, do not NAT it, so both sides keep real addresses and logs stay readable.
- Cross-location traffic between Hetzner locations goes over the public internet and counts against the traffic allowance in both directions of billing terms — treat replication across locations as a cost line, not a free win.

## vSwitch: Dedicated Meets Cloud

A Robot vSwitch attached to a Cloud Network is the supported private link between dedicated hardware and cloud servers. Everything else is a tunnel you maintain.

- The vSwitch is configured on the Robot side and attached to the cloud network; the dedicated server needs a VLAN interface configured in its OS, which does not survive a fresh installimage unless it is in the post-install steps (`dedicated.md`).
- MTU applies here too — keep the VLAN interface at or below the network ceiling.
- This is the pattern for "cheap dedicated CI runner, cloud app tier": the runner reaches the registry and the app servers privately, and never needs a public port.

## Address Plan

Write the plan once, record it in `## Current Infrastructure` in `~/Clawic/data/hetzner/memory.md`, and never improvise a second range:

```
10.<env>.0.0/16          one network per environment, per location
  10.<env>.1.0/24        app
  10.<env>.2.0/24        data
  10.<env>.10.0/24       k8s nodes      (pod and service CIDRs from a different /16)
  10.<env>.20.0/24       runners, vSwitch members
```

Keep pod and service CIDRs out of the network range entirely (`kubernetes.md`), and out of anything the user's office VPN uses.

**Write it down.** A new network, a subnet, a NAT gateway, a floating-IP pair, a load balancer or a WireGuard/vSwitch link changes `## Current Infrastructure` in `~/Clawic/data/hetzner/memory.md` in the same turn — with the CIDR and the MTU actually configured, because the next session debugging a hang will start there. The address plan itself, once it exceeds a couple of lines, becomes `~/Clawic/data/hetzner/artifacts/network-plan.md` with its `## Boxes` line.
