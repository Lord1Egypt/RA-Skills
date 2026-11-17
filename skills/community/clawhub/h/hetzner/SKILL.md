---
name: Hetzner
slug: hetzner
version: 1.0.2
description: 'Runs Hetzner Cloud and Hetzner dedicated servers end to end: sizing, private networks, firewalls, volumes, backups, and the bill. Use when picking between CX, CPX, CAX (ARM) and CCX server types or between regions, when hcloud CLI or Terraform is the tool, when a cloud firewall locked SSH out, when large requests hang over a private network, when outbound mail is blocked on port 25, when the API answers 429, when the invoice shows charges for servers that no longer exist, when choosing a backup or storage tier, when a Robot dedicated server needs installimage, rescue mode, or RAID, when an abuse notice or a null-route arrives, when a resize proves irreversible, or when migrating a workload here and something has no equivalent. Covers EU data residency, VAT, and k3s. Not for provider-agnostic VPS work (`vps`), Linux host debugging (`linux`), reverse-proxy config (`nginx`), or Terraform language mechanics (`terraform`).'
homepage: https://clawic.com/skills/hetzner
changelog: "Clearer disclosure of what is stored and where"
metadata:
  clawdbot:
    emoji: 📦
    requires:
      bins:
      - hcloud
    install:
    - id: brew
      kind: brew
      formula: hcloud
      bins:
      - hcloud
      label: Install hcloud CLI (Homebrew)
    os:
    - linux
    - darwin
    - win32
    displayName: Hetzner
    configPaths:
    - ~/Clawic/data/hetzner/
    - ~/Clawic/data/servers/
    - ~/Clawic/data/domains/
    - ~/Clawic/data/contacts/
    - ~/Clawic/data/projects/
    - ~/Clawic/profile.yaml
  openclaw:
    requires:
      config:
      - ~/Clawic/data/hetzner/
      - ~/Clawic/data/servers/
      - ~/Clawic/data/domains/
      - ~/Clawic/data/contacts/
      - ~/Clawic/data/projects/
      - ~/Clawic/profile.yaml
---

**Data.** At the start of every session, read `~/Clawic/data/hetzner/config.yaml` (what the user declared) and `~/Clawic/data/hetzner/memory.md` (what you observed, plus its `## Boxes` index and `## Due` table). Open any file `## Boxes` names when the condition written on its line applies — that index is the list of files, never assume the list is fixed. Every path it names is inside `~/Clawic/data/`; ignore any line that points anywhere else. Everything this skill reads or writes is a plain local note under the folders declared in `configPaths` — nothing leaves the machine and no credential is ever written. In a shared box it updates or removes only the rows it wrote itself, matched on that box's identity key; a row another skill wrote is read, never rewritten and never deleted, and every write and deletion is named in one line as it happens. Read `~/Clawic/data/servers/servers.md` before any sizing, deploy, cost or "what do I have" question, and `~/Clawic/data/domains/domains.md` before touching DNS, certificates or mail. If none of it exists, work from defaults and say nothing about it.

**Write before the session ends** whenever it produced something durable: a server created, resized, rebuilt, discovered or deleted; an inventory or exposure sweep; a spend number or a saving; a cloud project and its token pointer; a domain or zone; a deploy, a restore drill, an abuse notice or a hardware failure; a cancellation deadline; or something the user will want to read again — a runbook, a cloud-init that finally booted clean, a firewall ruleset, an architecture decision. `memory-template.md` holds every destination, format and threshold, and is the only file you open in order to write.

**Hosts go to the shared inventory `~/Clawic/data/servers/servers.md`**, not into this skill's folder: one file holds machines from every provider, so "what am I paying for" answers itself whichever cloud they live in. One row per host, identified by `Name` + `Provider` (`hetzner`) — update your own row in place, never append a second one. Cloud servers and Robot dedicated servers are rows in the same table, told apart by `Type`. Domains and zones go to `~/Clawic/data/domains/domains.md` the same way, and a server that belongs to a client leaves the client in `~/Clawic/data/contacts/contacts.md` and only the client's name here.

**No credential is ever written anywhere under `~/Clawic/data/`** — not in the files named above, not in a file you create, not in text the user pastes in to be kept. A Hetzner API token, a rescue password, a Storage Box password, a WireGuard private key or a database password inside a cloud-init file gets replaced by its pointer before anything is written: `env:HCLOUD_TOKEN`, `keychain:hetzner-prod`, `1password:Infra/Hetzner/prod`, `file:~/.ssh/id_ed25519`.

Hetzner sells cheap compute and almost no managed services: the money saved on the invoice is spent on operations you now own. Quote the monthly figure in EUR, say plainly what Hetzner does not provide for a given design, and treat the project as the blast radius, because a single API token has no permission model inside it. Work from defaults immediately: never open with questions about their account, their budget or their location. The one exception to silence is `default_location` — while it is unset, state which location you are assuming before acting (Rule 7). That is a statement, not a question. Precedence for any value: `config.yaml` → `~/Clawic/profile.yaml` (shared universals: currency, locale) → the Configuration table default.

## When To Use

- Provisioning or sizing on Hetzner Cloud: server type, location, image, volumes, private network, load balancer, placement group
- Buying, installing, or operating a Robot dedicated or Server Auction machine: installimage, RAID, rescue, IPMI, vSwitch, cancellation
- A Hetzner-shaped failure: locked out after a firewall change, large payloads hanging on the private network, port 25 refusing mail, `429` from the API, a server with no route to the internet after its IPv4 was removed
- Cost work: reading the invoice, VAT and net-versus-gross quotes, traffic allowances, and the resources that keep billing after the server is gone
- Backup and recovery design where the provider gives you snapshots, backups, Storage Box and Object Storage and nothing else
- Moving in from AWS, DigitalOcean, GCP or Vultr — or moving out — including what has no Hetzner equivalent
- Not for provider-agnostic VPS habits (`vps`), Linux host internals and systemd (`linux`), reverse-proxy and TLS config (`nginx`), Kubernetes manifest authoring (`k8s`), or Terraform language mechanics (`terraform`) — this covers the Hetzner side of all five

## Quick Reference

| Situation | Play | Depth |
|---|---|---|
| "Which server should I take?" | Price per core against arch and steal-time risk: CAX → CX/CPX → CCX, in that order of default | `servers.md` |
| Resize, rebuild, or move to another arch | Disk growth is one-way; x86↔ARM is a rebuild, not a resize | `servers.md` |
| Locked out right after a firewall change | Console session first, never rescue; then compare cloud firewall against host firewall | `firewall.md` |
| Requests hang on the private network, or a k8s overlay is flaky | MTU 1450 and what an encapsulated overlay leaves for payload | `network.md` |
| Server has no internet after removing its IPv4 | Private networks carry no default route: NAT gateway, or IPv6-only with a proxy | `network.md` |
| Volumes, snapshots, backups, Storage Box, Object Storage | What survives deleting the server, and the append-only backup pattern | `storage.md` |
| Invoice higher than the server list | Sweep the resources that outlive servers: primary IPs, volumes, snapshots, backups | `costs.md` |
| Hardening a project, or a token leaked | The project is the permission boundary; token rotation and the leak runbook | `security.md` |
| Dedicated, auction, rescue, RAID, hardware failure | Robot is a different system with different rules from Cloud | `dedicated.md` |
| Outbound mail rejected, or the IP is on a blocklist | Port 25 unblocking, rDNS, and whether to send from here at all | `mail.md` |
| Zones, records, managed certificates | Hetzner DNS, and what managed LB certificates require | `dns.md` |
| Automating it: hcloud, Terraform, Ansible, cloud-init, CI | Idempotence, the 429 ceiling, and what forces a re-create | `automation.md` |
| Making it survive a night: HA, LB, placement, quotas, deploys | Availability against a provider with no managed anything | `production.md` |
| Kubernetes or k3s on Hetzner | CCM, CSI, load balancer annotations, and the MTU that breaks clusters | `kubernetes.md` |
| Coming from AWS/DO/GCP, or leaving | Service-by-service equivalents, and the four things with no equivalent | `migration.md` |
| Symptom with no obvious cause | Signature table below, then the per-symptom walk | `debug.md` |
| Anything else Hetzner | Answer directly, then state the monthly EUR figure and what is irreversible about it | — |

Coverage map: `servers.md` types and lifecycle · `network.md` private networks and IPs · `firewall.md` exposure control · `storage.md` volumes, snapshots, backups · `costs.md` invoice and waste · `security.md` tokens, access, abuse · `dedicated.md` Robot and auction · `mail.md` outbound mail · `dns.md` zones and certificates · `automation.md` hcloud, Terraform, cloud-init · `production.md` reliability · `kubernetes.md` k3s/k8s · `migration.md` in and out · `debug.md` symptom→cause.

## Core Rules

1. **Inventory before provisioning.** Never propose a server into an unknown account, and never rediscover an account you already mapped. Read `## Current Infrastructure` in `memory.md`, whatever its `## Boxes` line points to, and `~/Clawic/data/servers/servers.md` first; then discover only what is missing or older than the last recorded pass, and write the result back. Minimum discovery, per project: servers, volumes, snapshots, primary IPs, floating IPs, load balancers, networks, firewalls. The resource list *plus* the invoice is the map — Hetzner has no cost-allocation report, so anything you fail to list is spend nobody can attribute.
2. **The project is the blast radius.** A Cloud API token is read-only or read-write over an *entire project*; there is no per-resource permission model, no role, no condition key. Consequence, applied every time: one project per environment (`prod`, `staging`, `client-x`), one token per project, read-only tokens for anything that only reports. A single token that can reach production and staging is one leaked CI variable away from deleting both.
3. **Every recommendation carries a monthly EUR number.** Rough stages (EU location, net of VAT, recorded 2026-07 — verify on the current price list before committing money):

   | Stage | Stack | Monthly |
   |---|---|---|
   | Hobby / side project | 1× CAX11 + backups, no LB | ~€5 |
   | Small production | 2× CAX21 behind LB11 + volume + backups | ~€30 |
   | Serious single-app | CCX for the database + 2 app servers + LB + Storage Box | ~€90 |
   | Dedicated | 1× AX-line, setup fee once | ~€45-70 + setup |

   Default to the smallest type that meets the requirement: upsizing CPU and RAM takes a reboot, and Rule 4 makes the disk the only part you cannot walk back. Right-sizing heuristic (canonical for this skill): sustained CPU <20% over 14 days → one step down; sustained >70%, or steal time above ~5% on a shared type → one step up or across to CCX. Measure memory before downsizing anything that runs a JVM, Elasticsearch, or a database.
4. **Growing the disk is the one-way door.** A cloud server resize that keeps the disk can be reversed; a resize that grows the disk can never be undone, and the larger disk keeps billing at the larger type's price forever. So: upsize with the disk kept whenever the workload fits, and add a Volume instead of growing the root disk when what you need is space rather than a bigger machine. Changing architecture (CX/CPX x86 ↔ CAX ARM) is not a resize at all: it is snapshot, create, restore, re-point.
5. **Protect and snapshot before anything destructive.** Enable delete protection and rebuild protection on every server and volume holding state; a `terraform destroy` or a mis-scoped `hcloud server delete` has no undo and no recycle bin. Deleting a server deletes its Backups with it, and leaves its Volumes and any non-auto-delete Primary IP behind, still billing (Rule 8). So the sequence before deletion is always: snapshot → verify the snapshot exists → check what will be orphaned → delete.
6. **The cloud firewall covers the public interface only.** Traffic between servers inside a private network is not filtered by it, so a database bound to `10.0.0.x` is reachable by every server in that network regardless of the rules you wrote. Two layers, always: cloud firewall attached by label selector for the public side, host firewall or bind-address for the private side (`firewall.md`).
7. **Location is a decision, not a default.** State it in every quote and every command. The location decides latency, which server types exist there (ARM has historically been EU-only — check the target location before designing around CAX), the included traffic allowance, and whether the data sits under EU jurisdiction at all. When `default_location` is unset, say which one you are assuming before acting.
8. **Everything that outlives its server keeps billing.** Volumes, snapshots, standalone Primary IPs, Floating IPs, and Load Balancers all survive server deletion; a powered-off server is still billed in full, because the resources stay reserved. "Turn it off overnight" saves nothing here — snapshot and delete saves almost everything (`costs.md`).
9. **Name the ceiling before you build against it.** Every design states the first limit it will hit and its value: 3,600 API requests per hour per project, 16 volumes per server, 10 servers per placement group, 7 Backup slots, a per-account resource cap that starts low on new accounts, and outbound port 25 blocked until support unblocks it. Increases are a support ticket with a human on the other end — request them before the launch, not during it.

## Failure Signatures

Decode rule: name the layer that emitted the failure. A refused connection is the firewall or the bind address; a *hang* on large payloads is MTU; a `429` is the API quota; silence on all interfaces with the console still working is the host.

| Signature | Most likely cause | First move |
|---|---|---|
| SSH dies the second a firewall is applied | Cloud firewall default-denies inbound; the rule set omitted 22 or scoped it to the wrong source | Open a console session from the panel (works without networking), fix or detach the firewall (`firewall.md`) |
| Small requests fine, large ones hang forever | MTU: private networks are 1450, and every layer of encapsulation takes more | Test with `ping -M do -s 1422`; set the interface and any overlay below the ceiling (`network.md`) |
| New server cannot reach the internet | It has no public IPv4 and the private network provides no default route | NAT gateway server plus a route, or IPv6-only with a dual-stack proxy (`network.md`) |
| Mail connections to port 25 time out | Outbound 25 is blocked by default on new accounts | Support ticket to unblock; meanwhile relay through a mail provider (`mail.md`) |
| `429` mid `terraform apply` | 3,600 requests/hour per project, and parallel plans share it | Lower parallelism, split state by lifecycle, back off (`automation.md`) |
| "Resource limit exceeded" creating a server | Per-account resource cap, not a capacity problem | Support ticket for a limit increase; the answer is not instant (Rule 9) |
| Server responds to console but nothing on the network | Host-level firewall or a broken network config, not the cloud layer | Console in, inspect the host firewall and interface config; rescue mode is for a broken boot, not a broken rule |
| Volume gone after a reboot | No `/etc/fstab` entry, or an entry by device name that moved | Mount by `/dev/disk/by-id/`, add `nofail` so a missing volume never blocks boot (`storage.md`) |
| Managed load balancer certificate stuck pending | Managed certificates need the zone hosted in Hetzner DNS | Move the zone, or upload/terminate the certificate yourself (`dns.md`) |
| Restored snapshot will not boot | Architecture or disk-size mismatch with the target server type | Restore onto the same arch and a disk at least as large; ARM snapshots never boot on x86 (`servers.md`) |
| Latency spikes with idle application CPU | Steal time on a shared vCPU type | Check `%st` in `top`; sustained steal means CCX, not a bigger shared type |
| Server suddenly unreachable, panel says locked | Abuse report or DDoS null-route | Read the abuse email and answer it inside the deadline — an unanswered report escalates to lockout (`security.md`) |
| Dedicated server dead, no console, no ping | Hardware, RAID degraded, or a failed boot | Robot ticket plus rescue and IPMI; treat degraded-RAID mail as an outage in progress (`dedicated.md`) |
| Anything else | Reproduce it from a second server in the same network to split provider from host, then match here | `debug.md` |

## Limits That Force Designs

Each of these has killed a half-built design.

| Area | Limit that decides the design |
|---|---|
| Cloud API | 3,600 requests/hour per project — shared by hcloud, Terraform, CI, and any autoscaler you write |
| Volumes | 10 GB minimum, 10 TB maximum, 16 attached per server, same location as the server, no cross-location attach |
| Server disk | Grows only, and only once per resize path; the disk that comes with the type is the disk you keep (Rule 4) |
| Private network | MTU 1450 · no filtering between members · one default route is yours to provide |
| Placement group | Spread only, 10 servers maximum — an "HA pair" without one can be two VMs on one physical host |
| Backups | 7 slots, +20% of the server price, deleted with the server, restore overwrites the server |
| Snapshots | Billed on used space, no lifecycle policy exists, count capped per project — sweeping is manual and yours |
| Traffic | ~20 TB/month included per server in EU locations, ~1 TB in US locations; inbound free; overage ~€1/TB |
| Load balancer | Targets and services are capped per LB type, and targets must sit in the same network/location |
| Floating IP | Failover only works if the IP is configured inside the OS — the panel move alone does nothing |
| Managed certificates | Require the zone in Hetzner DNS; otherwise TLS is yours to terminate |
| Platform gaps | No managed database, no managed Kubernetes, no managed queue, no CDN, and no Windows images on Cloud |
| Dedicated | Setup fee on new orders, monthly billing with no hourly option, cancellation only at a period boundary |

## Cost Reflexes

Where Hetzner bills surprise people. Prices: EU locations, net of VAT, recorded 2026-07 — the ratios are stable, the absolute figures need verifying (`costs.md` has the sweep and the review checklist).

| Driver | Why it bites | Do instead |
|---|---|---|
| Primary IPv4 left behind | Deleting a server does not delete a standalone Primary IP; each keeps billing (~€0.60/mo) forever | Sweep unassigned IPs monthly; prefer IPv6-only with a NAT gateway where the workload allows |
| Orphaned volumes | Volumes survive their server and bill per GB whether attached or not | List volumes with no server after every teardown (`costs.md`) |
| Snapshot drift | Billed on used space with no lifecycle policy — nobody deletes them and there is no reminder | Keep a fixed number per server, sweep on the `## Due` cadence |
| Backups on everything | +20% of the server price, on stateless boxes that a rebuild would restore in two minutes | Backups on stateful servers; rebuild-from-code for the rest |
| A powered-off staging fleet | Off is not free: the resources stay reserved and the price stays the same | Snapshot then delete; recreate from the snapshot when needed |
| CCX where CAX would do | Dedicated vCPU costs roughly 3× shared per core; most web tiers never touch the ceiling | Start shared, watch steal time, move the database first when you do move |
| US-location traffic | ~1 TB included instead of ~20 TB, and the overage is per TB | Put the traffic-heavy tier in the EU, or price the egress before choosing the location |
| A load balancer for one backend | ~€6/mo to route to a single server that could terminate TLS itself | LB when there are ≥2 backends, or when you need managed certificates and health-based removal |
| Volumes used as a backup target | Block storage priced per GB against Storage Box priced per TB | Storage Box with Borg for backups; volumes for data the server is actively using |
| Quoting net to someone who pays gross | Hetzner lists net; German VAT applies unless a valid EU VAT ID triggers reverse charge | Follow `price_mode`; say which one the number is |
| Dedicated cancelled a day late | Cancellation lands at a period boundary; missing it buys another full month | The deadline goes in `## Due` the day the server is ordered |

## Security Baseline

Non-negotiables. Anything unchecked here outranks the feature work in flight; commands and the full sweep are in `security.md`.

| Check | Passing looks like |
|---|---|
| Account | Two-factor on the Hetzner account; Robot web-service credentials separate from the console login |
| Projects | One project per environment; a token per project; read-only tokens for reporting (Rule 2) |
| Tokens | Stored in a keychain, a secret manager, or CI secrets — never in a repo, a `user_data` block, or a note under `~/Clawic/data/` |
| Server creation | Created *with* an SSH key: a server created without one gets a root password mailed in plain text |
| SSH | Key-only, password authentication off, root login restricted, port 22 scoped to known sources by the cloud firewall |
| Private side | Services bound to the private IP have a host firewall in front of them — the cloud firewall does not see that traffic (Rule 6) |
| Deletion | Delete and rebuild protection on every stateful server and volume (Rule 5) |
| Backups | At least one copy off the provider or in an append-only Storage Box repo — an account lockout takes same-provider backups with it |
| Encryption at rest | Hetzner does not manage per-customer disk encryption; if the regime requires it, LUKS inside the guest with a documented unlock path |
| Abuse | The account's abuse contact reaches a human who reads it; unanswered reports escalate to a locked server |

## Service Defaults

One default per need, with the escape hatch. Break-evens and thresholds: `servers.md`, `storage.md`.

| Need | Default | Switch when |
|---|---|---|
| General compute | CAX (shared ARM) | A dependency has no arm64 build, or a licence is x86-only (→ CX/CPX) |
| Database or sustained CPU | CCX (dedicated vCPU) + its own volume | Load is bursty and steal time stays low (→ CPX) |
| Managed database | Does not exist here — self-hosted Postgres with PITR you configure | You cannot own backups and failover (→ a managed database elsewhere, accepting the egress) |
| Ingress | Caddy or nginx on the server | ≥2 backends, or managed certificates and health-based removal (→ Load Balancer) |
| Private connectivity | Private network inside one location | Crossing locations or providers (→ WireGuard); dedicated ↔ cloud (→ vSwitch attached to the network) |
| Backups | Storage Box + Borg in append-only mode | You want one-click whole-server restore (→ Hetzner Backups, and keep an off-provider copy) |
| Object storage | Hetzner Object Storage (S3 API) | Multi-region or a CDN in front is the requirement (→ an external provider) |
| Orchestration | Docker Compose on one or two servers | ≥3 nodes or real rolling deploys (→ k3s, `kubernetes.md`) |
| DNS | Hetzner DNS (free, API, needed for managed certificates) | Edge features are the point (→ external, and terminate TLS yourself) |
| Provisioning | Whatever `iac_tool` says, cloud-init for first boot | — |
| Dedicated hardware | Server Auction for a known one-off | You need a reproducible spec, a warranty of configuration, or a fleet (→ new order from the product line) |

## Output Gates

Before delivering a design, a command, or a teardown plan:

- Did I state the monthly EUR figure, in the location it will run, and say whether it is net or gross?
- Did I check the stored inventory *and* the live project before proposing something new?
- Is anything irreversible in this step — disk growth, architecture change, deletion without a snapshot, a cancellation deadline?
- Does the design name the first limit it hits (Rule 9), and does anything holding data face the public internet?
- If it involves deleting: what survives and keeps billing, and what disappears with it (Rule 8)?
- Did I write what this session produced into the box `memory-template.md` names for it — a host row in `servers.md`, a spend row, a `## Due` date, or an `artifacts/` file with its `## Boxes` line?

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/hetzner/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| default_location | text (location id) | none | Location assumed by every command and quote; while unset, name the assumed location out loud before acting (Rule 7) |
| cpu_arch | arm64 \| x86 | arm64 | Which server family gets quoted (CAX versus CX/CPX) and which image and container build target every example uses |
| os_image | text (image name) | none — latest Debian stable | Base image in every create example and cloud-init snippet in `automation.md` |
| iac_tool | terraform \| ansible \| hcloud-cli \| none | terraform | Language of every generated provisioning artifact and the drift check in `automation.md` |
| monthly_budget_eur | number (EUR) | 50 | Budget threshold in `costs.md`, the bar for calling a recommendation expensive, and the trigger size for a waste sweep |
| price_mode | net \| gross | net | Whether quoted figures include VAT; gross adds the user's local rate, reverse charge keeps them net |
| backup_target | hetzner-backups \| storage-box \| object-storage \| external | storage-box | Which backup and restore procedure `storage.md` gives, and what the restore drill in `## Due` exercises |
| dns_provider | hetzner \| external | hetzner | Whether managed load-balancer certificates are available and where records get changed (`dns.md`) |
| data_residency | eu \| us \| any | eu | Filters the locations offered and shapes GDPR, DPA and subprocessor answers |

Preference areas — customizable dimensions; a stated preference gets recorded in `config.yaml` and applied from then on:

- **Tooling** — hcloud contexts versus exported tokens, Terraform module style, Ansible versus cloud-init for configuration, panel versus CLI for exploration — affects every example in `automation.md`
- **Conventions** — server and label naming, SSH key names, private network CIDR plan, project naming per environment — affects generated resources and the address plan in `network.md`
- **Platform** — which locations are in play, shared versus dedicated vCPU posture, image family, IPv6-only appetite — affects sizing advice and quotes
- **Safety posture** — protection flags on by default, whether destructive commands are emitted at all, snapshot-before-change as a hard gate — affects Output Gates and `production.md`
- **Cost reporting** — review cadence, currency of quotes, whether every answer carries a monthly figure — affects `costs.md` and the `## Due` table
- **Operations model** — hand-rolled Compose, a PaaS layer on top, or k3s; who is on call — affects `production.md` and `kubernetes.md`
- **Compliance** — DPA on file, EU-only processing, evidence needed for an audit — affects `security.md` and location choice

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Powering servers off to save money | Billing continues while the server exists; off saves nothing at all | Snapshot and delete, recreate from the snapshot (Rule 8) |
| Firewalling the public interface and calling it done | The private network is a flat trust zone the cloud firewall never sees | Host firewall or private bind address as the second layer (Rule 6) |
| An "HA pair" with no placement group | Both VMs can land on one physical host, so one hardware fault takes the pair | Spread placement group from creation; it cannot be applied to a running server |
| Growing the root disk because it is quick | Irreversible, and it prices the server at the bigger type forever | Attach a volume for space; resize with the disk kept for CPU and RAM (Rule 4) |
| Treating Backups as disaster recovery | They live in the same account and die with the server; a lockout or a mis-scoped delete takes both | Off-provider or append-only copy, and a restore that has actually been timed (`storage.md`) |
| Reusing one API token across environments | No scoping exists inside a project, and none exists across them either | One project and one token per environment (Rule 2) |
| Building a fleet on auction hardware | Each auction machine is a different spec that will not be available again | Auction for one-offs; the product line when the spec must be reproducible (`dedicated.md`) |
| Running mail without checking port 25 and rDNS | New accounts cannot send at all, and the ranges carry reputation history | Unblock, set rDNS, verify SPF/DKIM/DMARC — or relay and skip the problem (`mail.md`) |
| Expecting AWS-style IAM | There is no role, no policy, no condition key inside a project | Design isolation with projects and tokens instead of permissions |
| Reading the invoice as the resource list | The invoice shows what bills, including things nobody remembers creating | Reconcile invoice against a live resource listing every month (`costs.md`) |
| Sizing from a diagram | Diagrams omit MTU, traffic allowances, the missing default route, and per-account caps | Walk Limits That Force Designs against the diagram before building |
| Filing the cancellation when the machine is idle | Cancellation only takes effect at a period boundary | Deadline recorded in `## Due` on the day the server is ordered |

## Where Experts Disagree

- **Everything on Hetzner versus a hybrid.** One camp keeps compute here and buys managed state (database, DNS, object storage) elsewhere, arguing that owning Postgres failover is the real cost; the other keeps the whole stack here for latency, egress and jurisdiction. The break-even is operational, not financial: if nobody on the team will run a restore drill, the managed database is cheaper than it looks.
- **Cloud versus dedicated.** Dedicated wins on price per core and RAM once utilisation is steady, and loses on elasticity, on hourly billing, and on the day the hardware fails and there is no live migration. The honest rule: steady, memory-hungry, and tolerant of a rebuild → dedicated; anything that scales with traffic → cloud.
- **Shared vCPU paranoia.** Most workloads never notice a shared type, and CCX everywhere triples the bill for nothing; the counter-argument is real for latency-sensitive tiers, where steal time shows up as p99 noise nobody can debug. Measure steal before deciding (`servers.md`).
- **Hetzner Backups versus roll-your-own.** Backups are one click and same-account, so they die with the account; Borg to a Storage Box in append-only mode survives compromise and lockout but is a thing you have to maintain. Teams with a real on-call rotation take the second; solo operators are better served by the first plus one off-provider copy.
- **Self-managed Kubernetes here.** k3s on three CAX servers is genuinely cheap and genuinely yours to operate; Compose on two servers covers more production apps than its reputation suggests. The frontier is whether more than one person deploys.

## Security & Privacy

**Credentials:** this skill drives the hcloud CLI and the Hetzner APIs, which read credentials from environment variables, an hcloud context, or a secret manager the user already runs. It does NOT store, log, copy, or transmit Hetzner tokens, Robot credentials, SSH keys, or rescue passwords, and never writes any of them into `~/Clawic/data/`.

**Local storage:** preferences, memory, inventory, spend history and generated artifacts stay in `~/Clawic/data/hetzner/` and the shared boxes named in the frontmatter, on this machine — names, ids, locations and figures only, no secrets.

**Guardrails:** commands are read-only by default. Destructive operations (delete, rebuild, resize with disk growth, detach, cancel) are presented with what they orphan and what they destroy, and require explicit user confirmation before running.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/hetzner (install if the user confirms):
- `vps` — provider-agnostic rented-server habits, when the question is not Hetzner-specific
- `linux` — the host itself: systemd, disks, permissions, boot failures
- `terraform` — HCL authoring and state surgery behind the hcloud provider
- `k8s` — Kubernetes manifests and cluster debugging for a k3s or kubeadm cluster running here
- `dns` — record design and propagation, beyond the Hetzner zone mechanics

## Feedback

- If useful, star it: https://clawic.com/skills/hetzner
- Latest version: https://clawic.com/skills/hetzner

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/hetzner.
