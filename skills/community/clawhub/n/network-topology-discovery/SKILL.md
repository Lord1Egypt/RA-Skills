---
name: network-topology-discovery
description: >-
  Iterative network topology discovery using CDP/LLDP neighbor protocols,
  ARP/MAC table correlation, and routing table analysis. Multi-vendor coverage
  for Cisco IOS-XE/NX-OS, Juniper JunOS, and Arista EOS with layer-by-layer
  map building from L2 adjacency through L3 routing boundaries.
license: Apache-2.0
metadata:
  safety: read-only
  author: network-security-skills-suite
  version: "1.0.0"
  openclaw: '{"emoji":"🔍","safetyTier":"read-only","requires":{"bins":["ssh"],"env":[]},"tags":["topology","cdp","lldp"],"mcpDependencies":[],"egressEndpoints":[]}'
---

# Network Topology Discovery

Iterative discovery skill that builds a network topology map layer by layer.
Unlike threshold-based health checks, this procedure works outward from a seed
device — discovering neighbors, correlating MAC and ARP tables, analyzing
routing boundaries, and consolidating a complete adjacency model across L2 and
L3.

Commands are labeled **[Cisco]**, **[JunOS]**, or **[EOS]** where syntax
diverges. Unlabeled statements apply to all three vendors. Detailed command
syntax is in `references/cli-reference.md`; the full discovery methodology
and data model are in `references/discovery-workflow.md`.

## When to Use

- Building or validating a network diagram for an unfamiliar environment
- Post-acquisition network inventory where documentation is missing or stale
- Pre-change impact analysis — mapping blast radius before maintenance
- Incident response — determining the L2/L3 path between two endpoints
- Auditing discovered topology against intended design documents
- Identifying rogue or undocumented devices on the network
- Capacity planning — mapping link utilization paths between sites
- Migration planning — inventorying devices and links in a domain

## Prerequisites

- SSH or console access to the seed device (read-only privilege sufficient)
- Credentials that work across devices in the discovery scope — if different
  devices use different credentials, identify credential sets in advance
- CDP and/or LLDP enabled on the network (at least one protocol required)
- Knowledge of the intended discovery scope: site boundary, VRF, management
  subnet, or administrative domain to avoid unbounded expansion
- A device inventory tracker (spreadsheet, CMDB, or text file) to record
  discovered devices and avoid revisiting them

## Procedure

Follow this procedure iteratively. Each step builds on prior data. The process
expands outward from a seed device, discovering neighbors layer by layer and
correlating L2 with L3 information to produce a consolidated topology.

### Step 1: Seed Device Identification

Select a starting device and verify connectivity. The seed is typically a core
switch, distribution switch, or router with the broadest neighbor visibility.

Confirm access and collect the device identity:

**[Cisco]**
```
show version | include hostname|uptime|Software
show cdp neighbors | count
show lldp neighbors | count
```

**[JunOS]**
```
show version | match "Hostname|Model|Junos"
show lldp neighbors | count
```

**[EOS]**
```
show version | include hostname|uptime|model
show lldp neighbors | count
```

Record: hostname, platform, software version, management IP, and neighbor
count. The neighbor count sets expectations for Step 2. Add this device as the
first entry in the discovery tracker with status "discovered."

Note: CDP is Cisco-proprietary and available only on Cisco and EOS devices.
JunOS supports LLDP only. Use LLDP as the primary protocol for multi-vendor
environments.

### Step 2: L2 Neighbor Discovery

Collect all CDP and LLDP neighbors from the current device. This reveals
directly connected switches, routers, phones, and access points.

**[Cisco]**
```
show cdp neighbors detail
show lldp neighbors detail
```

**[JunOS]**
```
show lldp neighbors detail
```

**[EOS]**
```
show lldp neighbors detail
show lldp neighbors | include System
```

For each discovered neighbor, record: remote hostname, remote platform/model,
remote management IP, local interface, remote interface, and advertised
capabilities (Router, Switch, Phone, AP). The capabilities field identifies
device role without logging in.

Cross-reference each neighbor against the discovery tracker. New entries get
status "pending" — they become the next seeds for iterative expansion. Already
discovered devices are skipped.

### Step 3: MAC Address Table Analysis

Collect the MAC address table to identify all connected endpoints and to
distinguish trunk ports (many MACs) from access ports (few MACs).

**[Cisco]**
```
show mac address-table
show mac address-table count
```

**[JunOS]**
```
show ethernet-switching table
show ethernet-switching table summary
```

**[EOS]**
```
show mac address-table
show mac address-table count
```

Analyze port-to-MAC mappings:
- **Trunk ports** — multiple MACs learned, typically connecting to other
  switches. These should already appear as CDP/LLDP neighbors.
- **Access ports** — one or a few MACs learned, typically end hosts.
- **Ports with no MACs** — either unused or connected to a device that has
  not sent traffic. Check interface admin/oper state.
- **Ports with excessive MACs** (>100 on access port) — possible hub,
  unmanaged switch, or misconfigured trunk.

Flag any MAC addresses on unexpected ports — this helps identify undocumented
devices or cabling errors.

### Step 4: ARP Table Correlation

Collect the ARP table to map IP addresses to MAC addresses, establishing the
L3 identity of L2-discovered hosts.

**[Cisco]**
```
show ip arp
show ip arp vrf [name]
```

**[JunOS]**
```
show arp no-resolve
show arp interface [intf]
```

**[EOS]**
```
show ip arp
show ip arp vrf [name]
```

For each ARP entry, record: IP address, MAC address, interface, VLAN, and
entry age. Cross-reference MACs from Step 3 to assign IP addresses to
previously discovered L2 endpoints.

Unresolved MACs — entries in the MAC table with no corresponding ARP entry —
indicate L2-only devices (switches without management IPs on that VLAN) or
devices on a different subnet reachable via a trunk. Unresolved ARPs — ARP
entries with incomplete MAC — indicate reachability issues (device offline or
ARP timeout).

### Step 5: Routing Table Analysis

Collect routing table entries to discover L3 next-hops, remote subnets, and
routing domain boundaries.

**[Cisco]**
```
show ip route summary
show ip route
show ip route vrf [name]
```

**[JunOS]**
```
show route summary
show route protocol [ospf|bgp|static]
show route table [routing-instance].inet.0
```

**[EOS]**
```
show ip route summary
show ip route
show ip route vrf [name]
```

Identify:
- **Connected subnets** — directly attached networks; these define the L3
  boundaries of this device.
- **Next-hop routers** — IP addresses of adjacent L3 devices. Cross-reference
  with ARP/MAC data to identify the physical interface and MAC of each
  next-hop.
- **Routing protocol neighbors** — OSPF/BGP/EIGRP peers reveal L3 adjacency
  even when CDP/LLDP is disabled.
- **Default route** — points to the upstream gateway; follow it to discover
  the next layer.
- **VRF routes** — separate routing tables indicate VRF boundaries. Repeat
  discovery per VRF to map isolated routing domains.

Any next-hop IP without a corresponding ARP entry suggests an inactive or
unreachable peer — flag for investigation.

### Step 6: Topology Consolidation

Merge L2 and L3 discovery data into a unified topology model.

For each discovered link, confirm it from both ends where possible. A link
reported by device A to device B should also appear in device B's neighbor
table pointing to device A. Asymmetric entries (link visible from one end
only) indicate: CDP/LLDP disabled on one end, unidirectional link, or stale
neighbor entry.

Build the adjacency model:
1. **Deduplicate links** — the same physical connection appears in both
   neighbors' tables. Use the local-port/remote-port pair to match.
2. **Resolve L2/L3 overlap** — a trunk link visible in CDP/LLDP and also
   carrying multiple ARP subnets represents one physical link with multiple
   L3 paths.
3. **Classify devices** — use capabilities from CDP/LLDP and routing protocol
   participation to tag each device: core router, distribution switch, access
   switch, firewall, wireless controller, endpoint.
4. **Identify boundaries** — devices at the edge of discovery scope (no
   further neighbors, or neighbors outside the target domain) define the
   topology perimeter.
5. **Flag anomalies** — undocumented devices, asymmetric links, unexpected
   routing peers, and MAC addresses on wrong VLANs.

## Threshold Tables

Discovery completeness and data freshness metrics. Unlike health-check
thresholds, these measure how complete and current the topology data is.

**Discovery Completeness:**

| Metric | Complete | Partial | Incomplete |
|--------|----------|---------|------------|
| CDP/LLDP neighbors vs expected | 100% | 80–99% | <80% |
| MACs with ARP resolution | >90% | 70–90% | <70% |
| Next-hops with ARP entries | 100% | 80–99% | <80% |
| Links confirmed from both ends | >95% | 80–95% | <80% |
| Devices with routing table collected | 100% | >80% | <80% |

**Data Freshness:**

| Data Source | Fresh | Aging | Stale |
|-------------|-------|-------|-------|
| CDP holdtime remaining | >120s | 60–120s | <60s |
| LLDP TTL remaining | >90s | 30–90s | <30s |
| ARP entry age | <300s (5min) | 300–1200s | >1200s (20min) |
| MAC entry age | Recent activity | >300s since last seen | >900s |
| Routing table age | Converged | Reconverging | Incomplete |

## Decision Trees

### Missing Expected Neighbor

```
Expected neighbor not in CDP/LLDP table
├── Is the interface admin up and oper up?
│   ├── No → Fix interface state first
│   └── Yes → Continue
├── Is CDP/LLDP enabled on local interface?
│   ├── [Cisco] show cdp interface [intf]
│   ├── [JunOS] show lldp detail | match [intf]
│   ├── [EOS] show lldp local-info interface [intf]
│   ├── Disabled → Enable CDP/LLDP on the interface
│   └── Enabled → Continue
├── Is CDP/LLDP enabled on remote device?
│   ├── Cannot verify without access → Attempt SSH to remote
│   └── Disabled on remote → Enable or use MAC/ARP as fallback
├── VLAN mismatch?
│   ├── Access port VLAN differs between ends → Fix VLAN assignment
│   └── Trunk allowed VLANs pruned → Add VLAN to trunk
└── Physical layer issue?
    ├── Check interface errors → See interface-health skill
    └── Unidirectional link → Check fiber Tx/Rx, SFP seating
```

### Unresolved MAC Address

```
MAC in table but no ARP entry
├── Is MAC on a trunk port?
│   ├── Yes → MAC is behind a downstream switch, not local
│   │   └── Discover downstream switch to find the endpoint
│   └── No → MAC is on an access port
├── Is the MAC's VLAN routed on this device?
│   ├── No → ARP is on a different L3 gateway for that VLAN
│   │   └── Check the SVI/IRB owner for ARP entry
│   └── Yes → Continue
├── Check spanning-tree state on the port
│   ├── Blocking/Discarding → Port is STP-blocked; MAC learned before
│   └── Forwarding → Continue
└── Device may not have an IP configured
    └── L2-only device (unmanaged switch, printer in DHCP timeout)
```

### Asymmetric Routing View

```
Route visible from device A but not device B (or different next-hop)
├── Are both devices in the same VRF?
│   ├── No → Separate routing domains; route leaking required
│   └── Yes → Continue
├── Check routing protocol adjacency between A and B
│   ├── No adjacency → Protocol not configured or filtered
│   └── Adjacency up → Continue
├── Check route filters / distribute-lists
│   ├── [Cisco] show ip protocols | section Routing
│   ├── [JunOS] show policy [name]
│   ├── [EOS] show ip protocols | section Routing
│   └── Filter blocking the prefix → Adjust policy
├── Route redistribution boundary?
│   └── Prefix from one protocol not redistributed into another
└── Summarization hiding the specific route?
    └── Check for area summarization or aggregate routes
```

## Report Template

```
NETWORK TOPOLOGY DISCOVERY REPORT
===================================
Seed Device: [hostname]
Discovery Scope: [site / VRF / subnet range / domain]
Discovery Time: [start] to [end]
Performed By: [operator/agent]

DISCOVERY SUMMARY:
- Total devices discovered: [n]
- Routers: [n] | Switches: [n] | Firewalls: [n] | Other: [n]
- Total links mapped: [n] (confirmed bilateral: [n], unilateral: [n])
- Subnets identified: [n]
- VRFs encountered: [list]

DEVICE INVENTORY:
| Hostname | Platform | Mgmt IP | Role | Discovery Method |
|----------|----------|---------|------|------------------|
| [name]   | [model]  | [ip]   | [role] | [CDP/LLDP/ARP/routing] |

LINK MAP:
| Device A | Port A | Device B | Port B | Type | Speed |
|----------|--------|----------|--------|------|-------|
| [name]   | [intf] | [name]  | [intf] | [trunk/access/routed] | [1G/10G/...] |

ANOMALIES:
1. [Severity] [Category] — [Description]
   Observed: [what was found]
   Expected: [what design documents show]
   Impact: [topology accuracy / security / operational]
   Action: [recommended investigation or remediation]

COMPLETENESS ASSESSMENT:
- CDP/LLDP coverage: [%] of expected neighbors
- ARP resolution: [%] of MAC entries resolved
- Bilateral link confirmation: [%]

RECOMMENDATIONS:
- [Prioritized action list]

NEXT DISCOVERY: [Recommended refresh interval based on network change rate]
```

## Troubleshooting

### CDP Neighbors Missing on JunOS Devices

CDP is Cisco-proprietary and not supported on JunOS. LLDP must be used for
Juniper neighbor discovery. Ensure LLDP is enabled globally and on relevant
interfaces: `set protocols lldp interface all`. On the Cisco/EOS side, enable
LLDP alongside CDP so both protocols can exchange neighbor data with JunOS
devices.

### LLDP Showing Stale Neighbors

LLDP entries persist for the TTL duration (default 120s) after a neighbor
disappears. If stale entries appear, check: remote device was recently powered
off or rebooted, cable was disconnected, or LLDP was disabled on the remote
interface. Wait for TTL expiry or clear LLDP table manually to refresh.

### MAC Table Showing Thousands of Entries on Access Port

An access port learning hundreds of MACs suggests: a hub or unmanaged switch
behind the port, a virtualization host with many VMs bridged to one interface,
or a misconfigured trunk. Check port configuration — if it should be an access
port, investigate what is connected. Consider enabling port security to limit
MAC learning.

### ARP Entries with Incomplete MAC

`show ip arp` showing "Incomplete" for a MAC address means the device sent an
ARP request but received no reply. The target IP is configured on the local
subnet but the host is not responding. Causes: host is offline, host firewall
is blocking ARP, duplicate IP address conflict, or host is on the wrong VLAN.
Verify the host is powered on and connected to the correct VLAN.

### Routing Table Shows Unexpected Default Route

A default route pointing to an unknown next-hop may indicate: a rogue DHCP
server providing gateway addresses, an unplanned static route, or route
redistribution pulling in a default from another domain. Trace the route
source — check `show ip route 0.0.0.0` for the protocol and source. If OSPF
or BGP, identify which peer is advertising the default.
