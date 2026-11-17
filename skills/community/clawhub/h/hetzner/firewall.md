# Firewalls — What the Cloud Layer Filters, and What It Never Sees

Scope: keeping the wrong packets out. Identity, tokens, abuse and the leak runbook are a separate route (`security.md`).

**Before an exposure sweep or a rule change**, read `## Current Infrastructure` in `~/Clawic/data/hetzner/memory.md`, whatever `## Boxes` points at for an existing ruleset (`artifacts/firewall-<role>.md`), and `conventions.labels` in `~/Clawic/data/hetzner/config.yaml`. A rule written against the wrong label selector protects nothing and looks correct.

**Contents:** [Two Layers, Not One](#two-layers-not-one) · [How Cloud Firewalls Behave](#how-cloud-firewalls-behave) · [Label Selectors: The Scaling Pattern](#label-selectors-the-scaling-pattern) · [A Baseline Rule Set](#a-baseline-rule-set) · [Locked Out](#locked-out) · [Host Firewall](#host-firewall) · [Exposure Sweep](#exposure-sweep) · [DDoS and Null-Routes](#ddos-and-null-routes)

## Two Layers, Not One

| Layer | Covers | Blind to |
|---|---|---|
| Cloud firewall | The server's **public** interface, filtered before the packet reaches the host | Everything on a private network, and anything the host itself opens locally |
| Host firewall (nftables/ufw/firewalld) | Every interface the server has, including the private one | Nothing — but it costs the server's own CPU and can lock you out just as hard |

The trap that keeps recurring: a careful cloud rule set on the public side, and a Postgres bound to `0.0.0.0` reachable at `10.x.x.x` by every server in the network, including a compromised build agent. **Private networks are a flat trust zone** (`network.md`). Two layers, always:

- Cloud firewall: default deny inbound, attached by label selector.
- Host: services bound to the private address only where possible, plus host rules for anything that must not be reachable network-wide.

## How Cloud Firewalls Behave

- **Stateful**: allow the inbound rule and the return traffic flows. No matching outbound rule is needed for replies.
- **Default deny inbound, default allow outbound** once a firewall is attached. Attaching an empty firewall to a running server therefore cuts every inbound connection, including your SSH session, immediately.
- **Applied at the network edge**, so blocked traffic never reaches the server and costs it nothing — this is the correct place for wide blocks.
- **Rules are IP-based**: source CIDRs and ports. No hostnames, no application awareness, no rate limiting, no WAF.
- Changes take effect in seconds and apply to existing connections. Test from a second session before closing the first.
- A server can have several firewalls attached; the effective policy is the union of their allow rules.
- Outbound rules exist and are worth using on machines that should never initiate connections (a database, an internal worker) — it turns a compromised host into a much quieter one.

## Label Selectors: The Scaling Pattern

A firewall can be applied to a label selector rather than to a list of servers. Every new server carrying `role=app` gets the policy at creation, with no step for anyone to forget. This is what makes labels operationally load-bearing on Hetzner, not just cosmetic — the same labels also drive filtering in the CLI and cost attribution, which the provider does not do for you (SKILL.md Rule 1).

Convention worth adopting, recorded under `conventions.labels` in `config.yaml`:

```
env=prod|staging       role=app|data|edge|ci       owner=<team>
```

Then: one firewall per `role`, selected by label, plus one `env`-wide firewall for the SSH policy. A new app server is protected the moment it exists.

## A Baseline Rule Set

Inbound, for a typical web tier:

| Port | Source | Why |
|---|---|---|
| 22 | The operator's fixed addresses, a bastion, or a VPN range — never `0.0.0.0/0` | SSH is the credential-guessing target; scoping it removes almost all of the noise |
| 80, 443 | `0.0.0.0/0` and `::/0` | Public web traffic; keep 80 open for ACME renewals even if it only redirects |
| ICMP | `0.0.0.0/0` | Dropping ping breaks path-MTU discovery and your own debugging (`network.md`) |
| Database, cache, admin ports | Never from the internet | These belong on the private interface, with a host rule (see above) |

If SSH cannot be scoped to fixed addresses, do not widen the rule — put SSH behind a WireGuard tunnel and leave 22 closed publicly. That is the same amount of work as maintaining an allowlist of dynamic home addresses, and it fails closed.

## Locked Out

The recovery order matters, and most people get it wrong:

1. **Open a console session from the panel.** It works with no network at all and is almost always the fix. Reach for this first.
2. From the console, decide which layer bit you: if the cloud firewall is attached, detach it or fix the rule from the panel/API — that needs no access to the server. If the cloud side is clean, it is the host firewall or the interface config.
3. **Rescue mode is for a system that will not boot**, not for a bad rule. Rebooting into rescue to fix a firewall costs a full downtime for something the console solves live.
4. Never "fix" a lockout by opening 22 to the world with the intention of narrowing it later.

Prevention that costs nothing: apply firewall changes from a second, already-open session, and keep a scheduled rollback (a timer that detaches the firewall after N minutes unless cancelled) for changes made on a machine you cannot physically reach.

## Host Firewall

- Pick one manager and stay with it. `ufw` on top of `firewalld` on top of hand-written nftables rules is how a rule that looks correct is silently ignored.
- Rules must persist across reboot — verify by rebooting once, in a maintenance window, rather than discovering it during an incident.
- Docker publishes ports by writing its own rules and **bypasses `ufw`**: a container published with `-p 5432:5432` is reachable from the internet even though `ufw` says the port is denied. Publish to the loopback or the private address (`-p 127.0.0.1:5432:5432`), or keep the port unpublished and reach it over the container network (`kubernetes.md` for the cluster case).
- The host firewall is the only layer that sees private-network traffic. If the design depends on isolating servers from each other inside one network, it depends on this file.

## Exposure Sweep

Run this on any inherited or unaudited project, and on the `## Due` cadence:

| Check | Passing looks like |
|---|---|
| Every server has a firewall attached | No server relying on "nothing is listening" |
| No inbound `0.0.0.0/0` except 80, 443, and ICMP | SSH and admin ports scoped |
| Database, cache, message broker ports | Not present in any cloud rule at all |
| Listening sockets on each host (`ss -tulpn`) | Nothing bound to `0.0.0.0` that should be private |
| Docker-published ports | Bound to loopback or the private address |
| Load balancer targets | Backends reachable only from the LB, not from the internet |
| Outbound rules on data-tier servers | Restricted to what they genuinely call |

**Write it down.** The sweep result goes into `## Current Infrastructure` in `~/Clawic/data/hetzner/memory.md`, and any server it turns up goes into `~/Clawic/data/servers/servers.md`. A rule set that took real work to get right — a bastion policy, a label-selector layout, the exceptions with their reasons — becomes `~/Clawic/data/hetzner/artifacts/firewall-<role>.md` with its `## Boxes` line, so the next person does not rediscover why port 8080 is open to one CIDR.

## DDoS and Null-Routes

- Hetzner applies automatic DDoS mitigation at the network edge. You do not configure it, and you do not get a control.
- Under a large attack, the target address can be null-routed to protect the platform: the server is up, the panel is fine, and nothing reaches it. Check the panel and the account email before debugging the host.
- Reduce the surface that invites it: no open UDP services (DNS, NTP, memcached amplification), no open admin panels, rate limiting at the reverse proxy.
- An attack that recurs is a candidate for putting a CDN or a scrubbing proxy in front, since Hetzner does not sell one.
- Record the event, the address, the duration and the outcome in `~/Clawic/data/hetzner/incidents/<year>.md` — a second null-route on the same address is a pattern, not bad luck.
