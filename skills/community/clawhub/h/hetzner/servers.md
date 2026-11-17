# Cloud Servers — Choosing, Sizing, and the Changes You Cannot Undo

Scope: Hetzner Cloud instances. Dedicated hardware is a different system with different rules (`dedicated.md`).

**Before sizing anything**, read `~/Clawic/data/servers/servers.md` and `## Current Infrastructure` in `~/Clawic/data/hetzner/memory.md`. Recommending a type for a workload that already has one is how a fleet ends up with four families nobody can compare.

**Contents:** [The Four Families](#the-four-families) · [Locations](#locations) · [Sizing From Evidence](#sizing-from-evidence) · [Steal Time](#steal-time) · [Images and First Boot](#images-and-first-boot) · [Resize: The One-Way Door](#resize-the-one-way-door) · [Changing Architecture](#changing-architecture) · [Rebuild, Rescue, and Console](#rebuild-rescue-and-console) · [Snapshots as a Lifecycle Tool](#snapshots-as-a-lifecycle-tool) · [Deleting a Server](#deleting-a-server) · [Protection Flags](#protection-flags)

## The Four Families

Names and prices move; the ordering does not. Figures are EU locations, net of VAT, recorded 2026-07 — verify before committing money.

| Family | CPU | Costs | Take it when |
|---|---|---|---|
| CAX | Shared Ampere ARM (arm64) | Cheapest per core of the four | Default for anything with an arm64 build: web tiers, workers, k3s nodes, build agents |
| CX | Shared Intel | ~10-25% above CAX for a comparable shape | An x86-only dependency, a licence tied to x86, or a binary nobody will rebuild |
| CPX | Shared AMD | Above CX, more vCPU per step | Single-thread-heavy workloads that still tolerate sharing |
| CCX | Dedicated vCPU | Roughly 3× shared, per core | Databases, latency-sensitive tiers, sustained CPU, anything where p99 matters |

Two consequences worth stating out loud in a recommendation:

- **arm64 is the default, not the exotic choice.** Debian, Ubuntu, Docker official images, Postgres, nginx, Node, Go, Python and the JVM all ship arm64. The exceptions are old vendor binaries, some observability agents, and anything with a native x86 licence check. Check the dependency list, not the reputation.
- **Dedicated vCPU is a database decision, not a whole-fleet decision.** Moving one Postgres to CCX and leaving the app tier on CAX usually costs less than upsizing shared instances until the noise stops.

## Locations

| Location | Where | Notes |
|---|---|---|
| `fsn1` | Falkenstein, Germany | Largest inventory; EU jurisdiction |
| `nbg1` | Nuremberg, Germany | EU jurisdiction |
| `hel1` | Helsinki, Finland | EU jurisdiction |
| `ash` | Ashburn, Virginia, US | Lower included traffic than EU locations |
| `hil` | Hillsboro, Oregon, US | Lower included traffic than EU locations |
| `sin` | Singapore | Highest latency to Europe; smallest inventory |

Rules that follow from the table:

- **Type availability is per location.** ARM (CAX) has historically been EU-only, and inventory for a given type runs out in a location without warning. Check availability in the target location before designing around a family, and have a second choice ready.
- **Private networks are per location.** Two servers in `fsn1` and `hel1` cannot share one; crossing locations means WireGuard or public endpoints (`network.md`).
- **Volumes are per location** and cannot be attached across them (`storage.md`).
- **`data_residency: eu`** removes `ash`, `hil` and `sin` from the options entirely — say so rather than quoting a US price the user cannot use.
- Latency, not price, decides between EU locations: they are priced the same, and the difference to the user base is measurable in a single `ping` test.

## Sizing From Evidence

Start at the smallest type that can hold the working set in RAM, then correct with 14 days of data:

| Observation over 14 days | Move |
|---|---|
| Sustained CPU <20% | One step down — each step down roughly halves the compute price |
| Sustained CPU >70% | One step up, or out to a second server behind a load balancer |
| Steal time >~5% sustained | Across to CCX, not up within the shared family |
| Memory consistently >80% with swap in use | Up, immediately: swapping on a shared vCPU costs both memory *and* steal |
| Disk >80% | Attach a volume (`storage.md`) — never grow the root disk (see below) |

Worked example: an app server at 12% average CPU and 45% memory on a `cax31` moves to `cax21`, halving the compute line; a Postgres at 65% CPU with 4% steal on a `cpx31` moves to `ccx13`, roughly doubling the line and removing the p99 tail. Both are recorded in `## Spend`'s optimization log with the euro delta.

CPU alone under-diagnoses memory-bound workloads. Check RSS before downsizing a JVM, Elasticsearch, or any database.

## Steal Time

Steal is the percentage of time the vCPU was ready to run and the hypervisor gave the physical core to someone else. On shared types it is normal at 0-2%. It is the single number that decides "shared is fine" versus "pay for CCX", and it is invisible in application metrics: the app just gets slower with no resource looking busy.

- Read `%st` in `top`, or `st` in `vmstat 1`.
- Judge it over a week, not an afternoon: neighbours change.
- Sustained >5% on a latency-sensitive tier → CCX. Bursts to 10% on a batch worker → ignore it.

## Images and First Boot

- `os_image` decides the base; when unset, the latest Debian stable. Image names are per-distribution and versioned (`debian-13`, `ubuntu-24.04`) — pin the version in code, because "latest" changes under you and a rebuild then produces a different machine.
- **Always create the server with an SSH key attached.** A server created without one gets a root password sent by email in plain text, which is now a credential in a mailbox forever. If it already happened: log in, set key-only authentication, rotate, and note the rotation in `## Current Infrastructure` in `~/Clawic/data/hetzner/memory.md` — never store that password anywhere.
- Snapshots taken from a running server are crash-consistent, not application-consistent. For a database, stop it or use its own dump/backup tool before snapshotting.
- First-boot configuration belongs in cloud-init `user_data` (`automation.md`), which can only be set at creation: changing it later means a new server.

## Resize: The One-Way Door

Hetzner offers two resize paths, and only one is reversible:

| Path | Reversible | Use it for |
|---|---|---|
| Change type, keep the disk | Yes — you can go back down later | Every CPU and RAM change |
| Change type and grow the disk | **No, permanently** | Only when a bigger root disk is genuinely the requirement |

Once the disk has grown, the server can never be moved to a smaller type again, and it bills at the larger type from then on. Practical rule: treat root-disk growth as creating a new server, because that is its cost profile. When the need is space rather than power, attach a volume — volumes grow, detach, and are priced per GB (`storage.md`).

Both paths need a power-off, so a resize is a scheduled maintenance, not a live operation. Plan for a reboot window and check that everything comes back with the disk mounted (`nofail` in `/etc/fstab`).

## Changing Architecture

x86 (CX/CPX/CCX) ↔ ARM (CAX) is **not** a resize. The disk image is built for one architecture and will not boot on the other. The procedure is:

1. Confirm every dependency has an arm64 build (containers: check the manifest is multi-arch, not just that it pulls on your laptop).
2. Provision the new server from a clean image of the target arch, with the same cloud-init.
3. Move data over the private network, not the public one.
4. Cut over DNS or the load balancer target, keep the old server for one rollback window, then delete it.
5. Record the move in `servers.md` (row updated in place, `Type` changed) and delete the old row if the name changed.

## Rebuild, Rescue, and Console

Three different tools that people reach for in the wrong order:

| Tool | What it does | Reach for it when |
|---|---|---|
| Console (VNC from the panel) | Keyboard on the machine, no network needed | Locked out by a firewall or a broken interface config — this is almost always the right first move |
| Rescue mode | Boots a rescue OS with the disk unmounted | The system will not boot, or the filesystem needs repair, or you need to reset something on disk |
| Rebuild from image | Wipes the disk and reinstalls | The server is disposable and the data is elsewhere |

Rebuild is irreversible and does not warn about volumes: the root disk is wiped, attached volumes are untouched. Enable rebuild protection on anything stateful (below).

## Snapshots as a Lifecycle Tool

Beyond backups, snapshots are how you move things on Hetzner:

- **Clone a server**: snapshot → create from snapshot. The clone keeps the arch and needs a disk at least as large.
- **Move to another location**: snapshot, create in the target location, re-point, delete the old. Volumes cannot move this way — copy their data over the network.
- **Cheap "off"**: snapshot and delete beats powering off, because a powered-off server bills in full (`costs.md`).
- **Move between projects**: a snapshot can be transferred to another project, which is the supported way to hand a machine from `staging` to `prod` without rebuilding it.

Snapshots bill on used space and have no lifecycle policy: whatever you create, you sweep (`## Due`).

## Deleting a Server

What goes, what stays, what keeps billing:

| Resource | On server deletion |
|---|---|
| Root disk | Destroyed |
| Backups | **Deleted with the server** — snapshot first if the data matters |
| Snapshots | Survive, keep billing |
| Attached volumes | Survive, detached, keep billing |
| Primary IP created with the server | Deleted only if auto-delete was set; otherwise it survives and keeps billing |
| Floating IPs | Survive, keep billing |
| Firewall, network, load balancer | Survive; the server just leaves them |

So the teardown order is: snapshot → verify → list volumes, primary IPs and floating IPs → delete the server → delete the orphans → delete the row in `servers.md`.

## Protection Flags

Delete protection and rebuild protection are per-resource booleans, free, and the only guard rail the platform offers. Turn both on for every server holding state and every volume, in code so a fresh `apply` restores them. They block the destructive API call outright, which means a `terraform destroy` fails loudly instead of succeeding quietly — that is the point.

**Write it down.** A server created, resized, rebuilt, moved between locations or architectures, or deleted updates its row in `~/Clawic/data/servers/servers.md` in the same turn (`Type`, `Region`, `Monthly`), and a deletion removes the row and gets its date noted in `memory.md`. A resize that grew the disk, or an architecture migration, is an irreversible fact: record it in `## Current Infrastructure` so the next session does not propose walking it back.
