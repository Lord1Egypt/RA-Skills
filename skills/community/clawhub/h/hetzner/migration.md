# Migration — Coming From a Hyperscaler, and Leaving Again

Scope: moving a workload in or out. Provider-agnostic comparison of hosts is a separate skill (`vps`).

**Before planning a cutover**, read `## Current Infrastructure` and `## Cloud Projects` in `~/Clawic/data/hetzner/memory.md`, and `~/Clawic/data/domains/domains.md` for TTLs and where each zone lives. A cutover plan that assumes a 300-second TTL on a record that is set to a day is a plan for a day of split traffic.

**Contents:** [Why People Move Here](#why-people-move-here) · [The Translation Table](#the-translation-table) · [The Four Things With No Equivalent](#the-four-things-with-no-equivalent) · [Sizing the Comparison Honestly](#sizing-the-comparison-honestly) · [The Cutover](#the-cutover) · [Data Migration](#data-migration) · [Egress Costs of Leaving](#egress-costs-of-leaving) · [Hybrid Patterns](#hybrid-patterns) · [Leaving Hetzner](#leaving-hetzner)

## Why People Move Here

Two reasons hold up, and one does not:

- **Egress.** 20 TB included per server in EU locations against ~$0.09/GB at hyperscaler list prices: the same 20 TB is ~$1,800 there and inside a ~€5 server here. For media, downloads, backups or any traffic-heavy workload this is the whole argument, and it is not close.
- **Price per core and per GB of RAM**, especially with ARM and with dedicated hardware. A steady workload typically lands somewhere between a third and a fifth of the compute bill.
- **"Simpler"** — this one does not hold. The bill is simpler; the operations are not. You gain a database to operate, a control plane to run, and a monitoring stack to build (`production.md`).

Data residency in the EU is a fourth, legitimate reason where it applies (`security.md`).

## The Translation Table

| Elsewhere | Here | Honest difference |
|---|---|---|
| EC2 / Compute Engine / Droplet | Cloud server (CX/CPX/CAX/CCX) | Fewer families, no burst-credit model, no spot market |
| Availability zone | Nothing — a placement group is the finest granularity | Rewrite any multi-AZ assumption (`production.md`) |
| EBS | Volume | Location-bound, 16 per server, no provisioned-IOPS tier to buy |
| S3 | Object Storage | S3 API, but no CDN, no lifecycle ecosystem, fewer storage classes |
| RDS / Cloud SQL | Nothing — self-hosted Postgres or MySQL | Backups, PITR, failover and upgrades become yours (`storage.md`) |
| ElastiCache | Self-hosted Redis or Valkey | Same, smaller: persistence and failover are yours |
| SQS / Pub/Sub | Self-hosted broker, or an external SaaS | Nothing managed here |
| ALB / Cloud Load Balancing | Load Balancer | Layer 4/7, health checks, PROXY protocol, managed certs only with Hetzner DNS (`dns.md`) |
| CloudFront / Cloud CDN | Nothing | External CDN, or serve directly and rely on the traffic allowance |
| Route 53 | Hetzner DNS | Free and API-driven; no geo-routing, no health-checked failover records |
| IAM | Projects and tokens | No roles, no policies, no conditions (SKILL.md Rule 2) |
| Security groups | Cloud firewall | Public interface only — private networks are unfiltered (`firewall.md`) |
| NAT gateway | A server you run | Yours to make highly available (`network.md`) |
| Secrets Manager / KMS | Nothing | Bring your own secret store; disk encryption is LUKS in-guest (`storage.md`) |
| CloudWatch | Nothing | Your own metrics, logs and alerting stack |
| EKS / GKE | Self-run k3s or kubeadm, with CCM and CSI | Control plane is yours (`kubernetes.md`) |
| Spot instances | Nothing equivalent | The Server Auction is cheap *dedicated*, not preemptible capacity (`dedicated.md`) |
| Reserved instances / committed use | Nothing to buy | Prices are already low; there is no commitment discount to model |
| Tags for cost allocation | Labels, with no cost report | Attribution is projects plus a manual reconciliation (`costs.md`) |
| Windows AMIs | Not available on Cloud | Plan for Linux, or dedicated hardware with your own licence |

## The Four Things With No Equivalent

Say these out loud before anyone commits to a migration, because each is a project, not a setting:

1. **Managed databases.** Whoever owns the migration now owns failover and point-in-time recovery. Budget the drill, not just the setup (`storage.md`).
2. **IAM.** Any design that relies on fine-grained permissions, cross-account roles, or per-resource conditions has to be re-expressed as project boundaries. There is no partial version of this.
3. **A CDN.** Traffic-heavy assets either go through an external CDN or are served directly, which is affordable here but changes latency for distant users.
4. **Managed observability.** The monitoring stack becomes infrastructure you run, back up and upgrade.

## Sizing the Comparison Honestly

The comparison that survives review:

| Line | How to get it right |
|---|---|
| Compute | Match on real utilisation, not on instance names. A hyperscaler instance at 15% CPU maps to a much smaller server here |
| Egress | Take the actual GB/month from the current bill; this is usually where the saving is |
| Storage | Per-GB volumes here against per-GB there, plus the per-TB Storage Box for anything cold |
| Managed services | The line that disappears from the invoice and reappears as engineering time — estimate hours per month and price them |
| Migration itself | One-off engineering plus the egress to get the data out (below) |
| Risk | The cost of the first self-inflicted database outage, times its probability |

State the total as monthly EUR net (or gross per `price_mode`) alongside the current bill, and say which parts are estimates. A comparison that shows a 70% saving and omits the operations line is the reason some migrations get reversed a year later.

**Write it down.** A comparison this size is an artifact: `~/Clawic/data/hetzner/artifacts/comparison-<from>-to-hetzner.md` with its `## Boxes` line, including the assumptions, because the first question in three months will be "where did that number come from".

## The Cutover

1. **Build the target and let it run empty.** Provisioning, firewall, monitoring, backups — the whole production gate (`production.md`) before any traffic.
2. **Replicate the data continuously** so the final switch moves minutes, not hours (below).
3. **Lower DNS TTLs to 300 seconds** and wait out the old TTL, days before the switch (`dns.md`).
4. **Dry run**: point a staging hostname at the new stack and exercise it with real traffic patterns. Every integration with an IP allowlist elsewhere surfaces here — payment processors, partner APIs, SMTP relays all need the new addresses added *before* cutover.
5. **Freeze writes** for the shortest possible window, do the final sync, verify row counts and a recent record.
6. **Switch DNS or the load balancer**, watch error rates, keep the old stack running and reachable.
7. **Keep the rollback open** for at least one full business cycle: the old stack stays until a week of clean metrics, because the failure you did not think of appears on a weekday morning, not at 2am.
8. Only then tear down the source, and delete both sides' orphans.

Items that are forgotten in most cutovers: rDNS on the new addresses (`mail.md`), cron jobs that only existed on the old machine, TLS certificate renewal on the new path, IP allowlists at third parties, and log retention that started over.

## Data Migration

- **Databases**: logical replication or a replica of the source, promoted at cutover. Dump-and-restore only works when the freeze window can absorb the restore time — measure it on real data first, not on staging's 2 GB.
- **Object storage**: an S3-compatible sync tool between the source bucket and Hetzner Object Storage, run repeatedly until the delta is small, then once more inside the freeze.
- **Files**: `rsync` in repeated passes; the last pass inside the freeze. Preserve ownership, permissions and extended attributes deliberately.
- Transfer over encrypted channels, and check integrity by count and checksum, not by eyeball.
- Run the transfer from the *destination* where possible: pulling means the new environment's networking is proven before it matters.

## Egress Costs of Leaving

Moving data *out* of a hyperscaler is billed by the source at its egress rate. 5 TB at ~$0.09/GB is ~$450 — a one-off that belongs in the migration budget and surprises people who priced only the destination. Some providers waive egress for a documented exit; it is worth asking before starting.

The reverse also holds and is worth saying: leaving Hetzner later is cheap in egress terms, which is a genuine argument against lock-in fears.

## Hybrid Patterns

Not everything has to move:

- **Compute here, managed state elsewhere.** Works when the latency between them is tolerable, and fails when the application makes many small round trips to the database. Measure the round-trip count before assuming.
- **Bulk and batch here, latency-critical tier elsewhere.** CI, builds, media processing and backups move first and account for most of the saving with almost none of the risk.
- **DNS and CDN elsewhere, origin here.** Common and stable, at the price of managed load-balancer certificates (`dns.md`).
- **Dedicated here for steady load, cloud elsewhere for spikes.** The complexity of two providers is real; do it when the saving is a salary, not a lunch.

Start with the hybrid that carries the least risk — usually CI and backups. It builds the operational habits before production depends on them.

## Leaving Hetzner

The exit is short, which is the point of writing it down:

- Infrastructure in code means the target's equivalent is a rewrite of the provider blocks, not of the design.
- Data leaves cheaply: the traffic allowance covers most exits.
- The order is the cutover above, in reverse, with the same rollback discipline.
- Before deleting anything here: confirm the new stack has survived a business cycle, then delete servers, then the orphans (volumes, IPs, snapshots, load balancers), then close the projects, and finally file any dedicated cancellation before its period boundary (`dedicated.md`).
- **Write it down**: delete the rows in `~/Clawic/data/servers/servers.md`, update `~/Clawic/data/domains/domains.md` for any zone that moved, and note the exit date in `memory.md`. An inventory that still lists a provider you left is worse than no inventory.
