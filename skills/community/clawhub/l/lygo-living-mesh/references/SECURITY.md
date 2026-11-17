# Security — Living Mesh (Layer D)

## Protect the user

| Threat | Control |
|--------|---------|
| Egg exfil via gossip | Summaries only — roots + status; no payloads |
| Remote force-merge | Local authority; FORK_VISIBLE never auto-merges |
| Join without consent | `--i-consent` / `LYGO_MESH_JOIN_CONSENT` required |
| Quarantine ignored | Sentinel exit 3; join refused on local QUARANTINE |
| Wide-area exposure | Operator TLS + pin; no auto open ports |
| Skill supply chain | Install from deepseekoracle; LYGO Sovereign License v2.0 |

## Network

`gossip_tick`, `compare`, and optional public C checks **may** use HTTP.  
No credentials. No cookie steal. POST body is badge JSON summary only.

## Consent env

`LYGO_MESH_JOIN_CONSENT=yes` only for explicit peer join.  
Join still refuses when local status is QUARANTINE.
