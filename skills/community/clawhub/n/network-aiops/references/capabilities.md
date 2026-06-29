# network-aiops Capabilities

28 MCP tools (25 read / 3 write). Every tool is wrapped with `@governed_tool`
(audit + policy + budget + risk-tier; undo where a clean inverse exists). Returns
are high-signal summaries — config blobs are sanitized and size-bounded. Secrets
are never returned (user password hashes and SNMP community strings are redacted).

## Read tools

| Tool | Returns | Risk | Typical response tokens |
|------|---------|:----:|:-----------------------:|
| `device_facts` | hostname, vendor, model, os_version, serial, uptime, interface list | low | ~80–300 |
| `get_interfaces` | per-interface up/enabled/speed/description/mac | low | ~60–800 |
| `get_interfaces_counters` | per-interface octets/packets/errors/discards | low | ~60–800 |
| `get_interfaces_ip` | per-interface IPv4/IPv6 + prefix length | low | ~40–400 |
| `get_bgp_neighbors` | per-VRF peer, remote AS, up, prefix counts | low | ~60–600 |
| `get_bgp_neighbors_detail` | + state, router id, local AS, advertised prefixes | low | ~80–900 |
| `get_lldp_neighbors` | local port, remote host, remote port | low | ~40–400 |
| `get_lldp_neighbors_detail` | + chassis id, system desc, capabilities | low | ~60–700 |
| `get_arp_table` | interface, IP, MAC, age | low | ~50–700 |
| `get_mac_address_table` | MAC, interface, VLAN, static/active | low | ~50–900 |
| `get_vlans` | id, name, member interfaces | low | ~40–500 |
| `get_route_to` | per-prefix protocol, next hop, outgoing interface | low | ~40–500 |
| `get_environment` | fans, temperature, power, CPU, memory | low | ~60–500 |
| `get_optics` | per-interface rx/tx power, laser bias | low | ~40–400 |
| `get_ntp_servers` | configured NTP servers | low | ~20–120 |
| `get_ntp_stats` | per-peer stratum, offset, jitter, reachability | low | ~40–300 |
| `get_users` | username, level, has_password (hash redacted) | low | ~30–200 |
| `get_snmp_information` | chassis id, contact, location, community_count | low | ~40 |
| `get_network_instances` | VRFs: name, type, RD, interfaces | low | ~40–400 |
| `device_health` | facts + interface up/down + environment + issues | low | ~120–400 |
| `config_backup` | running config (sanitized, size-bounded) | low | ~500–8000 |
| `config_diff` | candidate diff (dry-run, never committed) | low | ~30–1500 |
| `netbox_list_devices` | name, role, site, status, primary IP | low | ~40–500 |
| `netbox_get_device` | + device_type, serial | low | ~80 |
| `netbox_device_interfaces` | per-interface name, type, enabled, description | low | ~40–600 |

## Write tools

| Tool | Effect | Risk | Undo |
|------|--------|:----:|------|
| `config_merge` | merge snippet + commit | medium | `config_replace` back to captured running config |
| `config_replace` | replace full config + commit | **high** | `config_replace` back to captured running config |
| `config_rollback` | revert last commit | medium | none (already a revert) |

## Per-driver support notes

| Getter / op | ios | nxos / nxos_ssh | iosxr | eos | junos |
|-------------|:---:|:---------------:|:-----:|:---:|:-----:|
| `get_facts` / `get_interfaces` / `get_interfaces_ip` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `get_bgp_neighbors` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `get_lldp_neighbors` / `get_arp_table` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `get_interfaces_counters` / `get_mac_address_table` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `get_bgp_neighbors_detail` | ✓ | varies | ✓ | ✓ | ✓ |
| `get_environment` / `get_ntp_*` / `get_users` / `get_snmp_information` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `get_vlans` / `get_network_instances` | varies | ✓ | ✓ | ✓ | ✓ |
| `get_optics` | varies | varies | ✓ | ✓ | ✓ |
| `get_route_to` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `get_config` (backup) | ✓ | ✓ | ✓ | ✓ | ✓ |
| `load_merge_candidate` + `compare_config` (diff/merge) | ✓ | ✓ | ✓ | ✓ | ✓ |
| `load_replace_candidate` (replace) | ✓ | varies | ✓ | ✓ | ✓ |
| `rollback` | ✓ (archive) | varies | ✓ | ✓ | ✓ |

A getter that a given driver does not implement raises `NotImplementedError`,
which the ops layer turns into a teaching `NetworkApiError` ("not supported by
the `<driver>` driver").

## Token-budget notes

- `config_backup` can be large; prefer `config_diff` to preview a change instead
  of re-fetching the whole config repeatedly.
- The runaway guard trips on tight poll loops — wait between repeated reads.

## Design notes / NAPALM assumptions

- NAPALM connections are short-lived: each tool opens a driver, runs its
  getters/config calls, and closes it. Nothing is cached across calls.
- Device passwords and the NetBox token come from the encrypted store
  `~/.network-aiops/secrets.enc` (unlocked by `NETWORK_AIOPS_MASTER_PASSWORD`;
  legacy plaintext env vars are a deprecated fallback). Enable/secret and
  transport go in `optional_args` and are passed verbatim to NAPALM. The skill
  never logs, echoes, or returns the credential.
- Connection / command / driver errors are translated centrally at the connection
  layer into a teaching `NetworkApiError`, so agents see actionable messages.
- Only the five core drivers are validated here; community drivers are untested.
