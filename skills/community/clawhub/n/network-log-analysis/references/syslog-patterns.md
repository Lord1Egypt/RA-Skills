# Syslog Patterns Reference — Network Log Analysis

Vendor-specific syslog message format tables, RFC 5424 facility/severity
matrix, and common network event pattern catalogs for raw log analysis.

## RFC 5424 Facility Codes

| Code | Facility | Typical Network Use |
|------|----------|-------------------|
| 0 | kern | Not used by network devices |
| 1 | user | General device messages |
| 2 | mail | Not used by network devices |
| 3 | daemon | SNMP, NTP, routing daemons |
| 4 | auth | Login, AAA, TACACS+/RADIUS |
| 5 | syslog | Syslog infrastructure messages |
| 6 | lpr | Not used by network devices |
| 7 | news | Not used by network devices |
| 8 | uucp | Not used by network devices |
| 9 | cron | Scheduled tasks on Linux-based devices |
| 10 | authpriv | Privileged authentication events |
| 11 | ftp | Not used by network devices |
| 16 | local0 | Commonly assigned: routers |
| 17 | local1 | Commonly assigned: switches |
| 18 | local2 | Commonly assigned: firewalls |
| 19 | local3 | Commonly assigned: wireless controllers |
| 20 | local4 | Commonly assigned: load balancers |
| 21 | local5 | Available for custom assignment |
| 22 | local6 | Available for custom assignment |
| 23 | local7 | Commonly assigned: network management |

## RFC 5424 Severity Levels

| Value | Severity | Keyword | Description |
|-------|----------|---------|-------------|
| 0 | Emergency | emerg | System is unusable |
| 1 | Alert | alert | Immediate action required |
| 2 | Critical | crit | Critical conditions |
| 3 | Error | err | Error conditions |
| 4 | Warning | warning | Warning conditions |
| 5 | Notice | notice | Normal but significant |
| 6 | Informational | info | Informational messages |
| 7 | Debug | debug | Debug-level messages |

**Priority (PRI) calculation:** `PRI = (Facility × 8) + Severity`

Example: local0.warning = (16 × 8) + 4 = 132. In raw syslog: `<132>`.

## Cisco IOS-XE Message Format

**Format:** `*timestamp: %FACILITY-SEVERITY-MNEMONIC: description`

### Common Facility Codes

| Facility | Subsystem | Example Mnemonic |
|----------|-----------|-----------------|
| LINK | Layer 1/2 interface | LINK-3-UPDOWN |
| LINEPROTO | Line protocol | LINEPROTO-5-UPDOWN |
| OSPF | OSPF routing | OSPF-5-ADJCHG |
| BGP | BGP routing | BGP-5-ADJCHANGE, BGP-3-NOTIFICATION |
| SYS | System events | SYS-5-CONFIG_I, SYS-5-RESTART |
| SEC | Security | SEC-6-IPACCESSLOGP |
| SEC_LOGIN | Login security | SEC_LOGIN-4-LOGIN_FAILED |
| AUTHMGR | Auth manager | AUTHMGR-5-START, AUTHMGR-5-SUCCESS |
| SNMP | SNMP subsystem | SNMP-3-AUTHFAIL |
| HSRP | First-hop redundancy | HSRP-5-STATECHANGE |
| VLAN | VLAN manager | VLAN-3-NATIVE_VLAN_MISMATCH |
| SPANNING | Spanning tree | SPANTREE-2-BLOCK_PVID_LOCAL |
| CRYPTO | IPsec/IKE | CRYPTO-4-IKMP_NO_SA |
| DHCP | DHCP snooping | DHCP_SNOOPING-5-DHCP_SNOOPING_MATCH |

### Critical Cisco Mnemonics to Monitor

| Mnemonic | Severity | Meaning | Action |
|----------|----------|---------|--------|
| LINK-3-UPDOWN | Error | Physical interface state change | Correlate with LINEPROTO, check cabling |
| LINEPROTO-5-UPDOWN | Notice | Line protocol state change | Correlate with LINK, check L2 negotiation |
| OSPF-5-ADJCHG | Notice | OSPF neighbor adjacency change | Check both neighbors, verify network stability |
| BGP-5-ADJCHANGE | Notice | BGP neighbor state change | Check peering config, route impact |
| BGP-3-NOTIFICATION | Error | BGP notification received/sent | Decode notification code for root cause |
| SYS-5-CONFIG_I | Notice | Configuration changed | Verify authorized change, identify user |
| SYS-5-RESTART | Notice | System restart | Check for crash, power event, or planned reload |
| SEC_LOGIN-4-LOGIN_FAILED | Warning | Authentication failure | Track source IP, count frequency |
| SNMP-3-AUTHFAIL | Error | SNMP auth failure | Verify community string, check source |
| HSRP-5-STATECHANGE | Notice | HSRP role change | Check for active/standby flip, verify primary |

## Juniper JunOS Message Format

**Standard format:** `timestamp hostname process[pid]: EVENT_ID: message`

**Structured format (when enabled):**
`timestamp hostname process[pid]: [junos@2636 tag="value" ...] message`

### Common JunOS Event Categories

| Process | Event Prefix | Subsystem |
|---------|-------------|-----------|
| rpd | RPD_OSPF_*, RPD_BGP_* | Routing protocol daemon |
| mgd | UI_*, MGMT_* | Management daemon |
| chassisd | CHASSISD_* | Chassis/hardware management |
| dcd | DCD_* | Device configuration daemon |
| snmpd | SNMPD_*, SNMP_TRAP_* | SNMP agent |
| sshd | SSHD_* | SSH daemon |
| eventd | EVENTD_* | Event processing |
| pfed | PFE_* | Packet forwarding engine |
| alarmd | ALARM_* | Alarm management |

### Critical JunOS Events to Monitor

| Event ID | Meaning | Action |
|----------|---------|--------|
| RPD_OSPF_NBRDOWN | OSPF neighbor went down | Check link state, peer config |
| RPD_OSPF_NBRUP | OSPF neighbor came up | Verify adjacency health |
| RPD_BGP_NEIGHBOR_STATE_CHANGED | BGP peer state transition | Check peering session, route impact |
| UI_COMMIT | Configuration committed | Verify authorized user and change |
| UI_COMMIT_COMPLETED | Commit finished successfully | Correlate with UI_COMMIT for timing |
| CHASSISD_FPC_OFFLINE | Line card offline | Hardware failure investigation |
| SNMPD_AUTH_FAILURE | SNMP authentication failure | Check community/credentials, source |
| SSHD_LOGIN_FAILED | SSH login failure | Track source, count frequency |
| ALARM_MANAGEMENT_ALARM_SET | Alarm raised | Check alarm type and severity |
| PFE_FW_SYSLOG_ETH | Firewall filter match | Evaluate filter hit, check policy |

## Arista EOS Message Format

**Format:** `timestamp hostname AgentName: %FACILITY-SEVERITY-message`

### Common EOS Agent Names

| Agent | Subsystem |
|-------|-----------|
| Ebra | Ethernet interface management |
| Stp | Spanning tree protocol |
| Bgp | BGP routing |
| Ospf | OSPF routing |
| Acl | Access control lists |
| Aaa | Authentication/authorization |
| ConfigAgent | Configuration management |
| Lldp | Link layer discovery |
| Mlag | Multi-chassis link aggregation |
| PimBidir | PIM multicast routing |

### Critical EOS Events to Monitor

| Pattern | Meaning | Action |
|---------|---------|--------|
| %LINEPROTO-5-UPDOWN | Interface protocol state change | Check physical link, peer device |
| %BGP-5-ADJCHANGE | BGP adjacency change | Verify peering, assess route impact |
| %OSPF-5-ADJCHG | OSPF adjacency change | Check link and neighbor health |
| %SYS-5-CONFIG_I | Configuration change | Identify user, verify authorization |
| %SYS-5-RELOAD | System reload | Check reason code (crash vs planned) |
| %MLAG-4-INTF_INACTIVE | MLAG interface down | Check MLAG peer link, domain health |
| %SECURITY-4-LOGIN_FAILED | Authentication failure | Track source, evaluate threat |
| %STP-6-INTERFACE_STATE | STP port state change | Verify topology convergence |

## Common Network Event Patterns

### Interface Events (All Vendors)

| Event Category | Cisco Pattern | JunOS Pattern | EOS Pattern |
|---------------|---------------|---------------|-------------|
| Link down | `LINK-3-UPDOWN.*down` | `SNMP_TRAP_LINK_DOWN` | `%LINEPROTO-5-UPDOWN.*down` |
| Link up | `LINK-3-UPDOWN.*up` | `SNMP_TRAP_LINK_UP` | `%LINEPROTO-5-UPDOWN.*up` |
| Duplex mismatch | `CDP-4-DUPLEX_MISMATCH` | `CHASSISD_FPC_ERR` | `%ETH-4-DUPLEX_MISMATCH` |
| Error counters | `CONTROLLER-2-PARITY` | `PFE_FW_SYSLOG_ETH` | `%PHY-4-CRC_ERROR` |

### Authentication Events (All Vendors)

| Event Category | Cisco Pattern | JunOS Pattern | EOS Pattern |
|---------------|---------------|---------------|-------------|
| Login failure | `SEC_LOGIN-4-LOGIN_FAILED` | `SSHD_LOGIN_FAILED` | `%SECURITY-4-LOGIN_FAILED` |
| Login success | `SEC_LOGIN-5-LOGIN_SUCCESS` | `SSHD_LOGIN_ACCEPTED` | `%SECURITY-6-LOGIN_SUCCESS` |
| SNMP auth fail | `SNMP-3-AUTHFAIL` | `SNMPD_AUTH_FAILURE` | `%SNMP-4-AUTHFAIL` |
| Privilege escalation | `PRIV-5-PRIV_CHANGE` | `UI_AUTH_EVENT` | `%AAA-5-ENABLE` |

### Configuration Change Events (All Vendors)

| Event Category | Cisco Pattern | JunOS Pattern | EOS Pattern |
|---------------|---------------|---------------|-------------|
| Config saved | `SYS-5-CONFIG_I` | `UI_COMMIT` | `%SYS-5-CONFIG_I` |
| Config rollback | `ROLLBACK-5-ROLLBACK` | `UI_COMMIT_ROLLBACK` | `%SYS-5-CONFIG_ROLLBACK` |
| Archive created | `ARCHIVE-5-ARCHIVE` | `MGMT_ARCHIVE` | `%CONFIG-5-ARCHIVE` |

### Routing Adjacency Events (All Vendors)

| Event Category | Cisco Pattern | JunOS Pattern | EOS Pattern |
|---------------|---------------|---------------|-------------|
| OSPF neighbor down | `OSPF-5-ADJCHG.*down` | `RPD_OSPF_NBRDOWN` | `%OSPF-5-ADJCHG.*Down` |
| OSPF neighbor up | `OSPF-5-ADJCHG.*FULL` | `RPD_OSPF_NBRUP` | `%OSPF-5-ADJCHG.*Full` |
| BGP peer down | `BGP-5-ADJCHANGE.*down` | `RPD_BGP_NEIGHBOR_STATE_CHANGED.*Idle` | `%BGP-5-ADJCHANGE.*down` |
| BGP peer up | `BGP-5-ADJCHANGE.*Established` | `RPD_BGP_NEIGHBOR_STATE_CHANGED.*Established` | `%BGP-5-ADJCHANGE.*Established` |
| BGP notification | `BGP-3-NOTIFICATION` | `RPD_BGP_NEIGHBOR_STATE_CHANGED` | `%BGP-3-NOTIFICATION` |
