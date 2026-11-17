# Production — Reliability Without Managed Services

Scope: taking something that works into something you are on call for, on a provider that sells compute and leaves the operations to you. The gate at the bottom is the checklist; everything above it explains why each item is on it.

**Before signing off on a production design**, read `## Current Infrastructure` and `## Due` in `~/Clawic/data/hetzner/memory.md`, and the recovery-drill table in `deploys/<year>.md` — a design that claims an RTO nobody has measured is a guess.

**Contents:** [What You Own Here](#what-you-own-here) · [Availability Is a Number You Choose](#availability-is-a-number-you-choose) · [Placement Groups](#placement-groups) · [The Failure Domains That Exist](#the-failure-domains-that-exist) · [Load Balancing and Rollouts](#load-balancing-and-rollouts) · [Stateful Tiers](#stateful-tiers) · [Monitoring and Alerting](#monitoring-and-alerting) · [Capacity and Limits](#capacity-and-limits) · [Maintenance Windows](#maintenance-windows) · [On-Call Reality](#on-call-reality) · [Production Gate](#production-gate)

## What You Own Here

The provider gives compute, storage, network, a load balancer and DNS. Everything below is yours, and every one of them is a thing a hyperscaler would have sold you:

- Database availability, failover, and point-in-time recovery
- Metrics, logs, traces, and their retention
- Alerting and paging
- Certificate renewal (unless the managed LB certificate path applies, `dns.md`)
- Autoscaling, if it exists at all (`automation.md`)
- Patching, kernel upgrades, and reboots
- Secret storage and rotation

State this explicitly in any design review. The invoice is smaller and the operational surface is larger; a team that does not staff the second half gets an outage that the savings do not cover.

## Availability Is a Number You Choose

Pick the target before designing, because each step changes the architecture and the bill.

| Target | Downtime/month | What it requires here |
|---|---|---|
| ~99% | ~7 h | One server, backups, a rebuild procedure someone has followed |
| ~99.9% | ~43 min | Two app servers in a spread placement group behind a load balancer; a stateful tier with a tested restore |
| ~99.95%+ | ~22 min | The above, plus a warm standby for the stateful tier and automated failover you have actually triggered |
| Higher | — | Multiple locations, replication across them, and an operations practice — not a Hetzner question any more |

The honest framing: the jump from one server to two costs about double the compute and roughly ten times the operational thinking (session state, deploy coordination, split brain). Make it deliberately.

## Placement Groups

A spread placement group guarantees its members run on different physical hosts. Without one, two servers created for redundancy can share a host, and one hardware fault takes both.

- Spread only, up to 10 servers per group.
- **Membership is set at creation.** A running server cannot join a group — the fix is to recreate it, which is exactly the migration nobody wants to do later (`automation.md`).
- So: every server that exists for redundancy is created into a placement group from the first one, before there is a second.
- Verify membership rather than assuming it. A pair that was supposed to be spread and is not is the highest-severity finding an audit can produce here.

## The Failure Domains That Exist

| Domain | What it takes down | Mitigation available |
|---|---|---|
| One physical host | Every server on it | Spread placement group |
| One location (`fsn1`, `hel1`, …) | Every server, volume and network in it | A second location, with replication and a DNS or failover-IP switch |
| One address | Reachability of one server | Floating IP or load balancer |
| The account | Everything, including same-provider backups | Off-provider backups and code in an external repository (`security.md`) |

There are no availability zones inside a location: the placement group is the finest granularity offered. A design that says "multi-AZ" has not been translated to this provider yet (`migration.md`).

## Load Balancing and Rollouts

- Health checks are the deploy mechanism: a target that fails its check is removed, so a rolling deploy is "update one target, wait for healthy, next".
- Give the check a path that reflects real readiness — a static `200` that ignores the database means the LB happily sends traffic to a broken app.
- Drain before stopping: remove the target, let in-flight requests finish, then deploy. Killing the process while it is in rotation is a burst of 502s that looks like a load balancer bug.
- Keep the rollback artifact identified before the deploy starts: the previous image digest or the snapshot taken beforehand. "We can rebuild it" is not a rollback plan at 3am.
- Database migrations are expand-contract, always: add the column, deploy code that writes both, backfill, then drop. A migration that requires the old code to be gone cannot be rolled back.

## Stateful Tiers

The part with no managed option:

- One database server is a single point of failure with a restore time, not an availability story. Be explicit about which one you are selling.
- Replication (a streaming replica on a second server, ideally in a placement group or another location) gives a failover target, and failover is still a decision someone makes: promotion, connection re-pointing, and fencing the old primary.
- Point-in-time recovery is a configuration you set up (continuous archiving to a Storage Box or Object Storage) and verify. Daily dumps alone mean up to a day of loss.
- Connection limits are your ceiling: a database on a small server with 200 application workers each holding a connection will exhaust them long before CPU matters. A pooler in front is the standard answer.
- Put the database on dedicated vCPU (CCX) and its own volume, and give the volume room — growing a volume is live, growing a root disk is irreversible (`servers.md`).

## Monitoring and Alerting

There is no managed metrics service, so the stack is yours. What matters is not which stack:

- **Metrics that page**: saturation (CPU, memory, disk, connections), error rate, and latency at p95/p99. Steal time belongs on the dashboard on shared types (`servers.md`).
- **Metrics that do not page but must exist**: traffic against the monthly allowance, disk growth trend, certificate expiry, backup age, RAID status on dedicated hardware (`dedicated.md`).
- **Alert on symptoms, not causes.** "Checkout error rate above 2%" pages; "CPU above 80%" does not, unless it reliably precedes an outage.
- Every alert routes to a human who is awake and has a runbook. An alert with no runbook trains people to ignore alerts.
- Monitor from outside as well as inside: a null-routed server looks perfectly healthy to its own agent (`firewall.md`).

## Capacity and Limits

Name the first ceiling before launch, and its current value (SKILL.md Rule 9):

- Per-account resource caps, which start low on new accounts and are raised by a support request that is not instant.
- Server type availability in the target location — a type can be out of stock exactly when the traffic spike arrives.
- API rate ceiling, if anything scales by calling the API (`automation.md`).
- Traffic allowance, particularly in US locations (`costs.md`).
- Database connections, file descriptors, and worker counts, which are limits inside your own stack and usually bite before the provider's do.

Request headroom before the launch. A limit increase during an incident is a support ticket with a human on the other end.

## Maintenance Windows

- The provider announces network and infrastructure maintenance for a location by email. Read it: a scheduled window that nobody knew about looks exactly like an incident.
- Your own reboots (kernel updates, resizes) are maintenance too. Schedule them, drain the load balancer target, and verify the machine comes back with volumes mounted and services enabled at boot.
- Verify "starts at boot" deliberately for every service, once, in a window. Half the incidents in a young production system are a service that ran because someone started it by hand.
- **Write it down**: provider maintenance affecting your servers goes into `~/Clawic/data/hetzner/incidents/<year>.md`; your own deploys and reboots go into `deploys/<year>.md`.

## On-Call Reality

- Three runbooks minimum, written before they are needed: the top failure mode, the restore, and the rollback. Each lives in `~/Clawic/data/hetzner/artifacts/` with a `## Boxes` line saying when to read it.
- A runbook is tested by having someone else follow it. Every restore drill finds a missing step (`storage.md`).
- Know the console path (`servers.md`): the recovery for a locked-out or unbootable machine does not require SSH, and people forget that under pressure.
- Provider support is a ticket queue, not a phone call: anything that requires them is measured in hours. Design so that the common failures do not.

## Production Gate

Before something is called production:

- Two servers in a spread placement group for anything in the request path, or an explicit, written acceptance of the single-server restore time
- Backups running to the configured `backup_target`, with a restore that has been performed and **timed** this quarter, and the measured RTO in the recovery-drill table of `~/Clawic/data/hetzner/deploys/<year>.md`
- Protection flags on every stateful server and volume; state and provisioning code in a repository that is not on this account
- Monitoring on saturation, errors and latency, routed to a human, with a runbook per alert
- External monitoring that would notice a null-route
- Certificate renewal path verified, with expiry monitored (`dns.md`)
- The first limit the design will hit is named, its current value known, headroom requested
- Deploy path is health-gated with an identified rollback artifact; migrations are expand-contract
- The teardown path is known: what keeps billing, what disappears (`servers.md`)
- Runbooks for the top three failure modes saved to `~/Clawic/data/hetzner/artifacts/` with their `## Boxes` lines in `memory.md`, and the next drill date in `## Due`
