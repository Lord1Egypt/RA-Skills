# network-aiops Capabilities

33 MCP tools (28 read / 5 write). Every tool is wrapped with `@governed_tool`
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
| `interface_health_rca` | worst-first findings: down / error / discard / flap, each cited | low | ~80–600 |
| `bgp_neighbor_rca` | worst-first findings: down / shut / reset / route-less, each cited | low | ~60–500 |
| `config_backup` | running config, credential values masked (`include_secrets=True` for raw) | low | ~500–8000 |
| `config_diff` | candidate diff, credential values masked (dry-run, never committed) | low | ~30–1500 |
| `netbox_list_devices` | `{devices, returned, limit, truncated}` — name, role, site, status, primary IP | low | ~40–500 |
| `netbox_get_device` | + device_type, serial | low | ~80 |
| `netbox_device_interfaces` | `{interfaces, returned, limit, truncated}` — name, type, enabled, description | low | ~40–600 |
| `undo_list` | recorded, not-yet-applied reversible writes (undoId, original/inverse tool, note) | low | ~40–400 |

> **Optional fields are `null`, not `""`.** Any value the driver or NetBox did
> not return (`serial_number`, `model`, an interface `description`, an LLDP
> `remote_host`, a NetBox `site`) comes back as JSON `null`. An empty string
> means the field genuinely is empty. Never infer a value from `null`.

> **Truncation is measured.** The two NetBox listings return an envelope with
> `truncated`; one extra record is fetched to determine it. When `truncated` is
> true, re-run with a higher `limit` before drawing any conclusion about
> coverage or drift.

## Write tools

| Tool | Effect | Risk | Undo |
|------|--------|:----:|------|
| `config_merge` | merge snippet + commit under a revert timer | medium | `config_replace` back to captured running config |
| `config_replace` | replace full config + commit under a revert timer | **high** | `config_replace` back to captured running config |
| `confirm_commit` | confirm a pending commit-confirm, cancelling its revert timer | medium | none (doing nothing lets the device revert) |
| `config_rollback` | revert last commit | medium | none (already a revert) |
| `undo_apply` | execute a recorded inverse descriptor — itself governed, single-use, supports `dry_run` | medium | none (is the undo) |

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

## Commit-confirm (the guard for a change that can lock you out)

`config_merge` / `config_replace` call NAPALM's `commit_config(revert_in=N)`
(default 300s). The **device** reverts the change on its own unless
`confirm_commit` arrives first. This matters because the recorded undo is a
`config_replace` that must open a NEW session to the same device — a commit that
shuts the management interface, tightens the VTY ACL or breaks AAA kills exactly
that path, so an undo token is not a guard against lockout. A device-enforced
timer is.

Workflow: **commit (timer armed) → verify reachability from a NEW session →
`confirm_commit`**. Doing nothing is the safe branch.

The result's `commit` block reports what actually happened:

| `commit.safetyNet` | Meaning |
|---|---|
| `commit-confirm` | timer armed; the change reverts in `commit.revertInSeconds` unless confirmed |
| `undo-only` | **no timer** — the driver refused one or `revert_in=0` was passed. The change is permanent on landing; `commit.warning` says so. Arrange out-of-band access before making lockout-capable changes on such a device. |

A write with **neither** a timer nor a usable captured backup is refused
outright (`UnreversibleCommit`) before anything is committed.

### Backups are digested, not echoed

`config_merge` / `config_replace` return `backup` as `{bytes, sha256,
retainedForUndo}` — not the config body. A running config carries credential
hashes, SNMP communities, PSKs and RADIUS keys, and a tool result lands in the
agent transcript. The byte-exact raw text is kept only in `undo.db` (0600) for
the rollback. Use `config_backup` when you deliberately want the text.

### Credential values are masked, and the masking is reported

`config_backup` cannot withhold the config — returning it IS the tool's
contract — so it masks credential VALUES instead: password/secret hashes, SNMP
communities, SNMPv3 auth/priv material, IKE pre-shared keys, RADIUS/TACACS and
keychain keys become `<redacted>`. Every other line is byte-for-byte what the
device said. The same applies to every `diff`, because a diff that adds
`snmp-server community X` contains X.

Each result carries a `redaction` block (`applied`, `linesRedacted`, `note`) so
the transformation is never silent. `include_secrets=True` returns the verbatim
text, and the CLI's `-o <path>` writes raw to a file the operator named.

**Limit**: this is pattern matching over five vendor syntaxes. It REDUCES
exposure; it does not guarantee the text is credential-free. Line-oriented
rules cannot see multi-line PKI key blocks. Do not describe redacted output as
"safe to share".

### `dry_run` does not bypass the guard

`config_merge(dry_run=True)` / `config_replace(dry_run=True)` (and the CLI's
`--dry-run`) stage the candidate, return the diff, discard it, and run the SAME
`UnreversibleCommit` refusal the real commit would — a green preview is never
followed by a refusal a model would read as transient and retry.

The CLI's `--dry-run` on `config merge` / `config replace` routes through the
same governed twin, so it reaches the same guard **and** records the same audit
row. The line's invariant is: **a dry_run MAY read; it must never write.** A
preview that cannot read cannot answer "would this be refused?", so reads are
expected; the mutating call is the thing that must never happen.

(`config rollback` and `config confirm` have no `dry_run` parameter — there is no
governed preview to route through, so their `--dry-run` short-circuits
client-side and records nothing.)

One asymmetry is deliberate and safe in the right direction: the preview can only
*predict* commit-confirm support from the driver's `commit_config` signature,
whereas the real write also learns from a `NotImplementedError` raised at commit
time. So the preview's refusal condition is a strict **subset** of the write's —
it never refuses something the write would allow. The preview reports its
prediction as `commit.wouldArmTimer` / `commit.safetyNet`.
