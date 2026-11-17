# Costs — Reading the Invoice, Finding the Waste, Quoting Honestly

Prices: EU locations, net of VAT, recorded 2026-07. The **ratios and break-evens are stable**; verify the absolute figure on the current price list before committing money. Every threshold below scales with `monthly_budget_eur`.

**Before answering any spend question**, read `## Spend` in `~/Clawic/data/hetzner/memory.md` — or `spend-log.md` if the `## Boxes` index points there. A current-month number with no prior months is not an answer, and Hetzner gives no cost-allocation report to reconstruct one from.

**Contents:** [How Hetzner Bills](#how-hetzner-bills) · [VAT and Quoting](#vat-and-quoting) · [Traffic](#traffic) · [The Waste Sweep](#the-waste-sweep) · [What "Off" Costs](#what-off-costs) · [Cost Attribution Without a Cost Report](#cost-attribution-without-a-cost-report) · [Break-Evens Worth Knowing](#break-evens-worth-knowing) · [Monthly Review Checklist](#monthly-review-checklist)

## How Hetzner Bills

- **Hourly, capped at the monthly price.** A cloud server that exists for 10 days costs 10 days; one that exists all month costs the monthly cap and no more. Deleting stops the meter immediately.
- **Existence, not usage.** A powered-off server bills in full: the vCPU, RAM and disk stay reserved for it. There is no "stopped" state that saves money (see below).
- **Dedicated servers bill monthly**, with a one-time setup fee on most new orders, and no hourly option. A dedicated machine used for three days costs a month.
- **One invoice per month per account**, covering Cloud, Robot, Storage Box, Object Storage and domains. There is no per-project invoice and no tag-based breakdown.
- There is no provider-side budget alarm to configure. Budget control here is a cadence in `## Due` plus a sweep, not a feature.

## VAT and Quoting

Hetzner lists prices net. What the user actually pays depends on their situation:

| Situation | What is added |
|---|---|
| Business with a valid EU VAT ID outside Germany | Nothing — reverse charge, the net price is the price |
| German business or private customer | German VAT on top |
| Private customer elsewhere in the EU | The customer's local VAT rate |
| Outside the EU | Generally no EU VAT |

Follow `price_mode`: `net` quotes the list price and says so; `gross` adds the user's rate and says which one. A net figure compared against a gross figure is a ~19% error, which is larger than most of the savings this file will find — that is why `## Spend` rows record which one they are.

## Traffic

- Included per cloud server per month: roughly **20 TB in EU locations, ~1 TB in US locations**. Inbound is free.
- Overage is billed per TB (~€1/TB in the EU) — cheap by hyperscaler standards, but the US allowance is 20× smaller and that is where the surprise comes from.
- Allowances are per server and are pooled across the project's servers in practice; a single high-traffic server is the one to watch.
- Private-network traffic between servers in one location does not consume the allowance. This is a real reason to bind internal services to private addresses (`network.md`).
- Load balancers and Object Storage have their own traffic terms — check them separately rather than assuming the server allowance covers them.

Comparison worth making explicitly when someone is arriving from AWS: 20 TB of egress at hyperscaler list prices (~$0.09/GB) is ~$1,800; here it is inside a ~€5 server. Egress is the single biggest structural price difference, and it is the reason a media or download workload belongs here even when the compute is a wash.

## The Waste Sweep

Everything on this list bills without a server attached, and nothing on it appears in a server listing:

| Sweep | Why it accumulates |
|---|---|
| Primary IPv4 addresses with no server | Server deletion does not delete a standalone IP; each is ~€0.60/mo forever |
| Floating IPs unassigned | Created for a failover experiment, never released |
| Volumes with no server | Volumes survive their server by design |
| Snapshots older than the retention anyone agreed to | No lifecycle policy exists; nothing expires them |
| Backups enabled on stateless servers | +20% of the server price for something a rebuild recreates |
| Load balancers with zero or one target | ~€6/mo to route to nothing, or to one backend that could do its own TLS |
| Servers with no DNS record and no traffic | The staging box from a project that ended |
| Storage Box space far above what the retention policy needs | Prune is not automatic |
| Dedicated servers past their usefulness | Cancellation only lands at a period boundary, so late costs a full month |

Run it monthly, and always after a teardown. The euro delta of each sweep goes into `### Optimization Log` — without it, the same orphans get rediscovered every quarter and nobody can say what the last cleanup was worth.

## What "Off" Costs

The most common wrong reflex on this provider, worth stating with arithmetic:

- Powering off a `cax21` for 20 days saves **€0**.
- Snapshotting it (say 8 GB used, ~€0.10/month) and deleting the server saves the full 20 days of the server price, and the snapshot rebuilds it in minutes.
- The cost of that pattern is the rebuild: a server created from a snapshot gets a new IP unless a floating IP or DNS update handles it, and anything not in the snapshot is gone.

So: for staging fleets and anything used in office hours, the play is snapshot-and-delete, automated, not power scheduling. For a machine that must keep its address and be up in seconds, pay for it and stop pretending it is off.

## Cost Attribution Without a Cost Report

Hetzner does not attribute spend to tags, roles or clients. Two mechanisms substitute for it:

1. **One project per environment or client** (SKILL.md Rule 2). Resource lists are per project, so a project boundary is the only clean cost boundary the platform gives.
2. **Labels** on every resource (`env`, `role`, `owner`), applied at creation. They do not appear on the invoice, but they let you list the resources of one role and price them yourself.

The reconciliation that makes this work: once a month, list every resource in every project, price it from the current list, and compare the total against the invoice. The difference is always something nobody remembers creating — that is the sweep above, found for you.

## Break-Evens Worth Knowing

| Decision | The number that decides it |
|---|---|
| Shared versus dedicated vCPU | CCX is ~3× shared per core: worth it when steal time is costing more than 3× the shared price in lost capacity, i.e. essentially only for databases and latency-critical tiers |
| Cloud versus dedicated hardware | Dedicated wins on price per core and per GB of RAM at steady utilisation; it loses the hourly billing, the elasticity and the two-minute rebuild. Compare a month of the cloud fleet against the dedicated monthly plus amortised setup fee, then ask whether anyone will operate the hardware |
| Load balancer versus TLS on the box | ~€6/mo. Worth it at ≥2 backends or when health-based removal matters; not for a single server |
| Extra IPv4s versus a NAT gateway | 10 × ~€0.60 = ~€6/mo of addresses against a CAX11 plus the on-call surface of a single egress point (`network.md`) |
| Volume versus Storage Box for backups | Per-GB block storage against per-TB external storage — the Storage Box wins by roughly an order of magnitude for cold data |
| Backups (+20%) versus rebuild from code | If cloud-init plus a data restore is under an hour and the data is backed up elsewhere, the 20% buys convenience, not safety |

## Monthly Review Checklist

| Check | Action |
|---|---|
| Invoice total against `monthly_budget_eur` | Over budget is a finding, not a fact — name the line that grew |
| Invoice against a live resource listing per project | Anything on the invoice that is not in a listing is an orphan |
| The waste sweep above | Delete, and record the euro delta in `### Optimization Log` |
| Traffic against the allowance, per server | A server near the allowance in a US location is next month's overage |
| Servers under 20% CPU over 14 days | Downsize one step (SKILL.md Rule 3) |
| Snapshots and Storage Box usage against the retention policy | Prune |
| Dedicated servers: still needed? | If not, the cancellation deadline is the deadline (`dedicated.md`) |
| Domain renewals in the next 60 days | Confirm auto-renew, or budget for it (`dns.md`) |

**Write it down.** The month's figure, `As of` date, top items and `net`/`gross` go into `## Spend` in `~/Clawic/data/hetzner/memory.md` — overwriting the current month's row, never adding a second one. Each saving goes into `### Optimization Log` with its euro delta, the run date into `## Due`, and any host whose real cost moved more than ~20% gets its `Monthly` refreshed in `~/Clawic/data/servers/servers.md`. A checklist with no last-run date gets skipped for a quarter and nobody notices.
