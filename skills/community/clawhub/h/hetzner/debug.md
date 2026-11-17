# Debugging — Symptom to Cause on Hetzner

Use this when the cause is not obvious. Everything here is provider-shaped: for a fault inside the operating system, this file ends at "it is the host" and `linux` continues.

**Before starting**, read `## Current Infrastructure` in `~/Clawic/data/hetzner/memory.md` and the last entries of `~/Clawic/data/hetzner/incidents/<year>.md` — a symptom that already happened once has its cause written down.

**Contents:** [Split the Problem in One Step](#split-the-problem-in-one-step) · [Unreachable Server](#unreachable-server) · [Slow or Hanging Traffic](#slow-or-hanging-traffic) · [Load Balancer Errors](#load-balancer-errors) · [API and Automation Errors](#api-and-automation-errors) · [Storage Symptoms](#storage-symptoms) · [Cost Symptoms](#cost-symptoms) · [Symptoms That Are Not Your Fault](#symptoms-that-are-not-your-fault) · [Writing It Down](#writing-it-down)

## Split the Problem in One Step

Before any deep dive, decide which side of the boundary the fault is on. One test does it: **reach the server from a second server in the same private network.**

| Private works, public does not | The public path: cloud firewall, primary IP, rDNS-dependent service, or a null-route |
| Neither works, console works | The host: host firewall, interface config, service not listening |
| Neither works, console does not respond | The machine or the platform: check the panel status, then rescue (`servers.md`) |
| Both work, users complain | The path beyond the server: DNS, load balancer, TLS, or MTU on a specific route |

This single test saves the most time of anything in this file, because provider faults and host faults have identical symptoms from outside.

## Unreachable Server

| Signature | Cause | Fix |
|---|---|---|
| Died the instant a firewall was applied | Cloud firewall default-denies inbound; 22 missing or scoped to the wrong source | Console in, detach or fix the firewall from the panel — no server access needed (`firewall.md`) |
| SSH refused, HTTP fine | Host firewall or `sshd` not running | Console; check the service, then the host rules |
| Everything refused, console fine | Host firewall applied all-interface rules, or the interface config broke after a reboot | Console; roll back the rules; verify persistence before leaving |
| Nothing at all, console black | Boot failure | Rescue mode, check the boot log and the filesystem (`servers.md`) |
| New server unreachable and it has no IPv4 | No default route from the private network | NAT gateway, IPv6, or attach an IPv4 (`network.md`) |
| Was reachable, now nothing, panel shows a notice | Abuse lock or null-route | Read the account email; do not debug the host (`security.md`) |
| Dedicated machine, no ping, no console | Hardware | Robot: hardware reset, then rescue, then a ticket (`dedicated.md`) |

## Slow or Hanging Traffic

| Signature | Cause | Fix |
|---|---|---|
| Small requests fine, large ones hang forever | MTU above the 1450 ceiling on a private network or an overlay | `ping -M do -s 1422`; set the interface and every encapsulation layer below the ceiling (`network.md`) |
| Latency spikes with application CPU idle | Steal time on a shared vCPU type | `%st` in `top` over a week; sustained >5% means CCX (`servers.md`) |
| Everything slower after a data growth | Disk pressure or memory pressure causing swap | Check free memory and disk; swapping on a shared type costs twice |
| Only some clients affected | Path MTU or an IPv6 route; the affected clients share a network | Test from a client on the same network as a complainant, over both protocols |
| Slow only across locations | Cross-location traffic goes over the public internet | Co-locate the chatty pair, or accept the latency deliberately (`network.md`) |
| Intermittent, correlates with backups | The backup window competing for disk and network | Move the window; throttle the backup client (`storage.md`) |

## Load Balancer Errors

| Signature | Cause | Fix |
|---|---|---|
| `503`, all backends up | No target is *healthy*: wrong check path, port, or matcher | Fix the health check before touching anything else (`network.md`) |
| `502` bursts during deploys | Targets killed while still in rotation | Drain, wait, then stop (`production.md`) |
| Requests arrive garbled or with the wrong client IP | PROXY protocol enabled on one side only | Enable on both, or neither |
| Target never becomes healthy, and it is new | Target in a different location or not in the LB's network | Same location, same network |
| Managed certificate stuck pending | The zone is not hosted in Hetzner DNS, or nameservers have not switched | Move the zone or terminate TLS yourself (`dns.md`) |
| Works over IPv4, fails over IPv6 | The service or backend is not listening on IPv6, or AAAA points somewhere stale | Test both protocols explicitly; most monitoring only tests one |

## API and Automation Errors

| Signature | Cause | Fix |
|---|---|---|
| `429` mid-apply | 3,600 requests/hour per project, shared by every tool | Lower parallelism, split state, back off (`automation.md`) |
| `401`/`403` on a call that worked | Token deleted, rotated, or the context switched to another project | Check which context is active before assuming the token is broken |
| "Resource limit exceeded" on create | Per-account cap, not capacity | Support request for an increase (SKILL.md Rule 9) |
| "Resource unavailable" for a server type | That type is out of stock in that location | Second-choice type or another location (`servers.md`) |
| `terraform destroy` fails on one resource | Delete protection is on — working as designed | Decide deliberately, then disable the flag in code (`automation.md`) |
| A plan wants to replace a stateful server | An immutable attribute changed: `user_data`, image, location, architecture, placement group | Read the plan before applying; that is data loss, not a reboot |
| Automation created a server nobody expected | A loop with no guard, or a leaked token | Check the project's resource list against inventory; treat as a leak until proven otherwise (`security.md`) |

## Storage Symptoms

| Signature | Cause | Fix |
|---|---|---|
| Volume missing after reboot | No `fstab` entry, or one by a device name that moved | Mount by `/dev/disk/by-id/`, add `nofail` (`storage.md`) |
| Boot hangs waiting for a filesystem | An `fstab` entry for a detached volume without `nofail` | Rescue mode, fix `fstab` |
| Disk full and nothing large is visible | Deleted files still held open, or a filesystem full of inodes rather than bytes | Host-level diagnosis (`linux`) |
| Restored snapshot will not boot | Architecture mismatch, or a target disk smaller than the source | Same arch, disk at least as large (`servers.md`) |
| Restore is missing recent data | Crash-consistent snapshot of a running database | Stop the database or dump logically before snapshotting |
| Storage Box refuses a delete | Append-only restriction on that key — working as designed | Prune from the maintenance credential, not from the server (`storage.md`) |

## Cost Symptoms

| Signature | Cause | Fix |
|---|---|---|
| Invoice higher than the server list | Orphans: primary IPs, volumes, snapshots, load balancers | The waste sweep (`costs.md`) |
| Powered-off servers still billed | Existence is billed, not usage | Snapshot and delete, or accept the cost |
| Traffic overage in a US location | ~1 TB included there instead of ~20 TB | Move the traffic-heavy tier to the EU, or budget for it |
| The number the user was quoted is 19% off | Net versus gross | Follow `price_mode` and say which one every figure is |
| Dedicated billed after it was "cancelled" | The request missed the period boundary | Deadlines live in `## Due` (`dedicated.md`) |

## Symptoms That Are Not Your Fault

Check these before debugging anything on the host — each one presents as an application bug:

- **Null-route under attack.** Server healthy, nothing arrives, panel or email says so (`firewall.md`).
- **Abuse lock.** Server disabled by the provider; the notice is in the account email and has a deadline (`security.md`).
- **Scheduled maintenance** in a location, announced by email in advance.
- **Type out of stock**, which fails a scale-up at exactly the wrong moment.
- **Blocked outbound port 25** on a new account, which is not a network fault (`mail.md`).
- **A blocklisted sending IP** with someone else's history (`mail.md`).

## Writing It Down

Any incident that took more than a few minutes gets an entry in `~/Clawic/data/hetzner/incidents/<year>.md`: date, kind, what happened, any reply deadline, the response, and the outcome. Anything with a deadline also gets a `## Due` line until it is closed. If the diagnosis produced a repeatable procedure, it becomes `~/Clawic/data/hetzner/artifacts/runbook-<symptom>.md` with a `## Boxes` line saying exactly when to read it — the value of this file is that the second occurrence takes minutes.
