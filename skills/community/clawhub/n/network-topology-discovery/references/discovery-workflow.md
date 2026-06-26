# Network Topology Discovery Workflow

Layer-by-layer methodology for building a complete network topology map. This
reference describes the data model, expansion algorithm, deduplication
patterns, and scope control mechanisms used by the discovery procedure.

## Layer-by-Layer Discovery Methodology

Discovery proceeds through three logical layers, each building on the prior:

### Layer 1: L2 Adjacency (CDP/LLDP + MAC)

**Goal:** Map all directly connected network devices and their physical
interconnections.

**Process:**
1. Collect CDP/LLDP neighbors from the current device
2. Collect the MAC address table to identify ports with connected hosts
3. For each neighbor, record the link (local port → remote port → remote device)
4. Mark trunk ports (many MACs) vs access ports (few MACs)

**Output:** A list of L2 links with device names, port names, and link type
(trunk/access/routed). This forms the physical topology skeleton.

### Layer 2: L3 Mapping (ARP + Subnets)

**Goal:** Assign IP addresses to L2-discovered devices and identify subnet
boundaries.

**Process:**
1. Collect the ARP table — maps IP addresses to MAC addresses
2. Cross-reference MACs from the MAC table to assign IPs to ports
3. Identify SVI/IRB interfaces — these define VLAN-to-subnet mappings
4. Record connected subnets from the routing table

**Output:** Each discovered device now has IP address(es) associated with it.
Subnet boundaries are known.

### Layer 3: Routing Domain (Routes + Protocols)

**Goal:** Discover remote subnets, routing protocol adjacencies, and routing
domain boundaries.

**Process:**
1. Collect the routing table — reveals all reachable subnets and their next-hops
2. Identify routing protocol neighbors (OSPF, BGP, IS-IS, EIGRP)
3. Cross-reference next-hop IPs against ARP to find the physical path
4. Identify VRFs — each VRF is a separate routing domain requiring independent
   discovery

**Output:** Full L3 reachability map overlaid on the L2 physical topology.
Routing protocol adjacencies supplement CDP/LLDP where those protocols are
disabled.

## Topology Data Model

### Per-Device Record

Collect and store these attributes for every discovered device:

```
Device:
  hostname: string            # From CDP/LLDP system name or show version
  management_ip: string       # Primary management IP address
  platform: string            # Hardware model (e.g., "C9300-48P", "QFX5100")
  software_version: string    # OS version string
  vendor: string              # Cisco | Juniper | Arista
  role: string                # core | distribution | access | firewall | AP | endpoint
  serial_number: string       # From show inventory / show chassis hardware
  discovery_method: string    # cdp | lldp | arp | routing | manual
  discovery_time: timestamp   # When this device was first discovered
  status: string              # discovered | pending | unreachable | out-of-scope
  vrfs: list[string]          # VRFs configured on this device
```

### Per-Link Record

Collect and store these attributes for every discovered link:

```
Link:
  device_a: string            # Hostname of first endpoint
  port_a: string              # Interface name on device_a
  device_b: string            # Hostname of second endpoint
  port_b: string              # Interface name on device_b
  link_type: string           # trunk | access | routed | port-channel
  speed: string               # Negotiated speed (1G, 10G, 25G, 100G)
  vlans: list[int]            # VLANs carried (trunk) or assigned (access)
  discovery_source: string    # cdp | lldp | mac-correlation | manual
  confirmed_bilateral: bool   # True if seen from both endpoints
  status: string              # active | stale | one-sided
```

### Per-Subnet Record

Collect and store these attributes for every discovered subnet:

```
Subnet:
  prefix: string              # CIDR notation (e.g., 10.1.1.0/24)
  vlan_id: int                # Associated VLAN (if L2/L3 boundary)
  vrf: string                 # VRF name (or "global")
  gateway_device: string      # Device hosting the SVI/IRB for this subnet
  gateway_ip: string          # Gateway IP address (SVI/IRB address)
  arp_entries: int             # Number of ARP entries in this subnet
  connected_devices: list     # Devices with interfaces in this subnet
```

## Seed Expansion Algorithm

The discovery process expands outward from a seed device. Each iteration
discovers new devices that become seeds for the next iteration.

### Algorithm

```
1. Initialize:
   - discovered = {}           # Set of visited devices
   - pending = {seed_device}   # Queue of devices to visit
   - topology = empty_graph    # Adjacency model

2. While pending is not empty:
   a. Pop next device from pending
   b. If device is in discovered → skip
   c. Mark device as discovered
   d. Connect to device (SSH/console)
      - If connection fails → mark as "unreachable", continue
   e. Collect: CDP/LLDP neighbors, MAC table, ARP table, routing table
   f. For each discovered neighbor:
      - If neighbor not in discovered AND within scope → add to pending
   g. Add device record and link records to topology

3. Output: Complete topology graph
```

### Expansion Order

Process pending devices in this priority order for most efficient discovery:

1. **Core/distribution devices first** — they have the most neighbors, giving
   the broadest view early
2. **Routers before switches** — routing tables reveal remote subnets that
   switches cannot see
3. **Management subnet devices** — devices on the management VLAN are most
   likely reachable via SSH
4. **Access-layer devices last** — they typically connect to endpoints only,
   adding leaves to the tree

### Depth and Hop Limits

To prevent unbounded expansion:
- Set a maximum hop count from the seed (e.g., 5 hops)
- Define a management subnet or IP range as the boundary
- Stop expansion when a device's role is "edge" or "perimeter"
- Exclude devices with hostnames matching a site-code pattern outside the
  target site

## Deduplication and Reconciliation

### Link Deduplication

The same physical link appears in two neighbor tables — once from each end.
Reconciliation rules:

1. **Match on port pair:** Link (A:Gi0/1 → B:Gi0/2) and Link (B:Gi0/2 → A:Gi0/1)
   are the same link. Merge into a single record with `confirmed_bilateral: true`.
2. **Hostname normalization:** CDP may report FQDN while LLDP reports short
   hostname. Normalize to short hostname before matching.
3. **Port name normalization:** Cisco may report "GigabitEthernet0/1" in CDP
   but "Gi0/1" elsewhere. Normalize interface names to their abbreviated form.

### Device Deduplication

A device may be discovered via multiple methods:
- CDP/LLDP neighbor entry → provides hostname, platform, management IP
- ARP entry → provides IP and MAC
- Routing protocol neighbor → provides router-ID and peer IP

Merge these records by matching on management IP or hostname. If a device
appears in CDP with hostname "switch-1" and in ARP with IP 10.1.1.1, verify
they are the same device by checking the ARP MAC against the CDP-reported
platform.

### Conflict Resolution

When two sources disagree:
- **Hostname conflict:** CDP/LLDP system name is authoritative over DNS reverse
  lookup
- **IP conflict:** ARP entry is authoritative over CDP management IP (CDP
  management address may be a loopback, not the interface IP)
- **Port conflict:** If CDP shows Gi0/1 but LLDP shows Gi0/2 for the same
  remote device, the entries are likely from different physical links — do not
  merge

## Scope Control

### By Management Subnet

Restrict discovery to devices with management IPs in a defined range (e.g.,
10.0.0.0/16). When a neighbor's management IP falls outside this range, record
it as "out-of-scope" but do not expand into it.

### By VRF

Discover only within a specific VRF. Collect ARP and routing tables for that
VRF only. Devices visible via that VRF's routing table are in scope; devices
in other VRFs are boundary markers.

### By Site Code or Hostname Pattern

Use hostname naming conventions to limit scope. If the site uses prefixes
like "NYC-" for New York devices, only expand into neighbors whose hostnames
start with the target prefix. Neighbors with different prefixes are edge
devices — record the link but do not discover their further neighbors.

### By Administrative Domain

Stop expansion at firewalls, WAN routers, or provider edge devices. These
are identified by:
- CDP/LLDP capabilities showing "Router" at the perimeter
- Routing table showing a default route or summary route toward them
- Hostname patterns indicating WAN or edge role

### By Hop Count

Set a maximum hop count from the seed device. Each expansion increments the
hop counter. When a device is at the maximum hop count, record its neighbors
but do not add them to the pending queue.

## Output Formats

After discovery completes, the topology data can be rendered as:

- **Adjacency list** — text format listing each device and its neighbors
- **Edge list** — one line per link with both endpoints and attributes
- **Mermaid diagram** — flowchart or graph syntax for visual rendering
- **CSV/JSON export** — structured data for import into CMDB or monitoring tools
- **Audit report** — using the Report Template in SKILL.md to document findings
