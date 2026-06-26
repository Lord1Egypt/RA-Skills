# Network Topology Discovery CLI Reference — Cisco / JunOS / EOS

Commands organized by discovery layer with all three vendors side by side.
All commands are read-only (show/display only). Cisco commands validated against
IOS-XE 17.3+ and NX-OS 10.2+; JunOS 21.x+; EOS 4.28+.

## Neighbor Discovery Protocols

### CDP (Cisco Discovery Protocol)

CDP is Cisco-proprietary. Available on Cisco IOS-XE/NX-OS and Arista EOS.
**Not available on JunOS** — use LLDP instead for Juniper devices.

| Function | Cisco | EOS |
|----------|-------|-----|
| Neighbor summary | `show cdp neighbors` | `show cdp neighbors` |
| Neighbor detail | `show cdp neighbors detail` | `show cdp neighbors detail` |
| CDP on interface | `show cdp interface [intf]` | `show cdp interface [intf]` |
| CDP timers | `show cdp` | `show cdp` |
| CDP traffic stats | `show cdp traffic` | `show cdp counters` |
| CDP entry for device | `show cdp entry [name]` | `show cdp neighbors [intf] detail` |

### LLDP (Link Layer Discovery Protocol — IEEE 802.1AB)

LLDP is standards-based and supported on all three vendors. Preferred for
multi-vendor environments.

| Function | Cisco | JunOS | EOS |
|----------|-------|-------|-----|
| Neighbor summary | `show lldp neighbors` | `show lldp neighbors` | `show lldp neighbors` |
| Neighbor detail | `show lldp neighbors detail` | `show lldp neighbors detail` | `show lldp neighbors detail` |
| LLDP on interface | `show lldp interface [intf]` | `show lldp detail \| match [intf]` | `show lldp local-info interface [intf]` |
| LLDP timers | `show lldp` | `show lldp` | `show lldp` |
| LLDP traffic stats | `show lldp traffic` | `show lldp statistics` | `show lldp counters` |
| LLDP local info | `show lldp local-info` | `show lldp local-information` | `show lldp local-info` |
| Neighbor count | `show lldp neighbors \| count` | `show lldp neighbors \| count` | `show lldp neighbors \| count` |

### Neighbor Protocol Notes

- **CDP vs LLDP:** In Cisco/EOS environments, both can run simultaneously. CDP provides Cisco-specific TLVs (VTP domain, native VLAN, power). LLDP provides standard TLVs (system name, capabilities, management address).
- **JunOS:** Only LLDP is available. Enable with `set protocols lldp interface all`.
- **EOS:** Both CDP and LLDP are supported. LLDP is enabled by default; CDP must be explicitly enabled with `lldp run`.
- **Cisco:** Both protocols run by default on most platforms. Disable individually per interface if needed.
- **Capabilities field:** LLDP advertises device capabilities (Router, Bridge, Station, etc.). Use this to classify devices without logging in.

## MAC Address Tables

| Function | Cisco | JunOS | EOS |
|----------|-------|-------|-----|
| Full MAC table | `show mac address-table` | `show ethernet-switching table` | `show mac address-table` |
| MAC table count | `show mac address-table count` | `show ethernet-switching table summary` | `show mac address-table count` |
| MAC on interface | `show mac address-table interface [intf]` | `show ethernet-switching table interface [intf]` | `show mac address-table interface [intf]` |
| MAC in VLAN | `show mac address-table vlan [id]` | `show ethernet-switching table vlan [name]` | `show mac address-table vlan [id]` |
| Specific MAC lookup | `show mac address-table address [mac]` | `show ethernet-switching table \| match [mac]` | `show mac address-table address [mac]` |
| MAC aging time | `show mac address-table aging-time` | `show ethernet-switching aging-time` | `show mac address-table aging-time` |

### MAC Table Notes

- **Cisco (IOS-XE vs NX-OS):** IOS-XE uses `show mac address-table`; older IOS uses `show mac-address-table` (hyphenated). NX-OS uses `show mac address-table`.
- **JunOS:** The ethernet-switching table is only available on EX/QFX series. MX routers use bridge domains: `show bridge mac-table`.
- **Format:** Cisco/EOS show VLAN + MAC + Type (dynamic/static) + Port. JunOS shows MAC + Flags + Logical interface + Routing instance.
- **Trunk identification:** A port with many dynamic MACs is almost certainly a trunk or uplink. An access port should have 1–5 MACs.

## ARP Tables

| Function | Cisco | JunOS | EOS |
|----------|-------|-------|-----|
| Full ARP table | `show ip arp` | `show arp no-resolve` | `show ip arp` |
| ARP in VRF | `show ip arp vrf [name]` | `show arp routing-instance [name]` | `show ip arp vrf [name]` |
| ARP on interface | `show ip arp [intf]` | `show arp interface [intf]` | `show ip arp interface [intf]` |
| ARP count | `show ip arp summary` | `show arp no-resolve \| count` | `show ip arp summary` |
| ARP timeout | `show interfaces [intf] \| include arp` | `show arp parameters` | `show ip arp \| include timeout` |
| IPv6 neighbors | `show ipv6 neighbors` | `show ipv6 neighbors` | `show ipv6 neighbors` |

### ARP Table Notes

- **Entry age:** Cisco default ARP timeout is 14400s (4 hours). JunOS default is 1200s (20 minutes). EOS default is 14400s. Shorter timeouts produce more current data but increase ARP traffic.
- **Incomplete entries:** An ARP entry with "Incomplete" MAC means the host did not respond to ARP requests. The IP exists in the local subnet configuration but the host is unreachable at L2.
- **`no-resolve`:** JunOS `show arp no-resolve` skips DNS resolution, producing faster output. Always use `no-resolve` for discovery to avoid DNS timeouts.
- **VRF awareness:** In multi-VRF environments, each VRF has its own ARP table. Always collect ARP per VRF to get complete L3-to-L2 mappings.

## Routing Tables

| Function | Cisco | JunOS | EOS |
|----------|-------|-------|-----|
| Route summary | `show ip route summary` | `show route summary` | `show ip route summary` |
| Full routing table | `show ip route` | `show route` | `show ip route` |
| Routes by protocol | `show ip route [ospf\|bgp\|static]` | `show route protocol [ospf\|bgp\|static]` | `show ip route [ospf\|bgp\|static]` |
| Specific route | `show ip route [prefix]` | `show route [prefix] detail` | `show ip route [prefix]` |
| Routes in VRF | `show ip route vrf [name]` | `show route table [instance].inet.0` | `show ip route vrf [name]` |
| Connected routes | `show ip route connected` | `show route protocol direct` | `show ip route connected` |
| VRF list | `show vrf` | `show route instance` | `show vrf` |
| Next-hop detail | `show ip cef [prefix]` | `show route forwarding-table destination [prefix]` | `show ip route [prefix] detail` |

### Routing Table Notes

- **Connected routes:** These define the L3 boundaries of the device. Each connected route represents a directly attached subnet.
- **Next-hops:** Every non-connected route has a next-hop IP. Cross-reference each next-hop against the ARP table to find the MAC, then against the MAC table to find the physical port.
- **Routing protocol peers:** `show ip ospf neighbor` (Cisco/EOS), `show ospf neighbor` (JunOS), `show ip bgp summary` reveal L3 adjacencies that may not appear in CDP/LLDP (e.g., routed L3 links without discovery protocols enabled).
- **VRF:** Each VRF has its own routing table. Use `show vrf` (Cisco/EOS) or `show route instance` (JunOS) to enumerate all VRFs before collecting routes.

## Routing Protocol Neighbors

| Function | Cisco | JunOS | EOS |
|----------|-------|-------|-----|
| OSPF neighbors | `show ip ospf neighbor` | `show ospf neighbor` | `show ip ospf neighbor` |
| EIGRP neighbors | `show ip eigrp neighbors` | *(not available)* | *(not available)* |
| BGP peers | `show bgp ipv4 unicast summary` | `show bgp summary` | `show ip bgp summary` |
| IS-IS adjacencies | `show isis neighbors` | `show isis adjacency` | `show isis neighbors` |

### Routing Protocol Notes

- **EIGRP:** Cisco-proprietary. Not available on JunOS or EOS.
- **Routing protocol neighbors supplement CDP/LLDP:** On routed point-to-point links where CDP/LLDP may be disabled, routing protocol neighbor tables reveal L3 adjacency and provide the peer's router-ID and interface address.

## Device Identification

| Function | Cisco | JunOS | EOS |
|----------|-------|-------|-----|
| Hostname/model | `show version \| include hostname\|uptime\|model` | `show version \| match "Hostname\|Model"` | `show version \| include hostname\|model` |
| Serial number | `show inventory` | `show chassis hardware` | `show inventory` |
| Management IP | `show ip interface brief \| include Mgmt\|manage` | `show interfaces terse \| match me0\|fxp0` | `show ip interface brief \| include Management` |
| Running config | `show running-config \| include hostname\|interface\|vrf` | `show configuration \| match hostname\|interface\|routing-instances` | `show running-config \| include hostname\|interface\|vrf` |
