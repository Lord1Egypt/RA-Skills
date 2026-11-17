# Dedicated Servers — Robot, Auction, installimage, and Hardware That Fails

Scope: physical machines ordered through Robot. Cloud instances are a different system with different rules (`servers.md`).

**Before ordering or cancelling**, read `~/Clawic/data/servers/servers.md` for what is already rented and `## Due` in `memory.md` for cancellation deadlines already recorded. A dedicated server ordered on top of an idle one is a month of double spend nobody notices until the invoice.

**Contents:** [Robot Is Not the Cloud](#robot-is-not-the-cloud) · [Product Lines](#product-lines) · [The Server Auction](#the-server-auction) · [Setup Fees and Billing](#setup-fees-and-billing) · [installimage](#installimage) · [RAID Choices](#raid-choices) · [Rescue and IPMI](#rescue-and-ipmi) · [Hardware Failure](#hardware-failure) · [Networking: Additional IPs, Failover, vSwitch](#networking-additional-ips-failover-vswitch) · [Cancellation](#cancellation) · [When Dedicated Is the Wrong Answer](#when-dedicated-is-the-wrong-answer)

## Robot Is Not the Cloud

| | Cloud | Robot / dedicated |
|---|---|---|
| Provisioning | Seconds, API-first | Minutes to days depending on stock; auction is usually fast |
| Billing | Hourly, capped monthly | Monthly, plus a one-time setup fee on most new orders |
| Delete | Instant, stops billing | Cancellation at a period boundary |
| Resize | Change type, reboot | Order a different machine and migrate |
| Failure | Rebuild in two minutes | A disk, a PSU, or a board that a technician replaces |
| Credentials | Cloud API tokens | Robot login plus separate web-service credentials (`security.md`) |
| Networking | Private networks, cloud firewall | vSwitch, additional and failover IPs, no cloud firewall |

The consequences that matter for design: dedicated hardware has **no live migration and no automatic rebuild**. Everything on it must either be rebuildable from code or replicated somewhere else, because a hardware fault is an outage measured in hours.

## Product Lines

Names change, shapes do not:

| Line | Shape | Fits |
|---|---|---|
| AX | AMD consumer-grade high-clock CPUs, large RAM, NVMe | Best price per core; CI runners, application servers, databases that fit in RAM |
| EX | Intel, mixed generations | Similar role, different price/perf curve; compare per workload |
| SX | Many large spinning disks | Bulk storage, archives, media libraries |
| Enterprise / dedicated-grade | Server CPUs, ECC as standard, redundant components | Workloads where ECC and enterprise support are a requirement, not a preference |

Two selection rules that survive the naming churn:

- **ECC or not is a real decision.** Consumer-grade lines may not offer it. For a database or anything long-running with large memory, silent bit flips are a genuine class of corruption; for a stateless CI runner they are noise. Check the specific machine, not the line.
- **Disks are the spec that bites.** Two NVMe drives means RAID1 and half the raw capacity; four drives open RAID10. Decide the RAID layout before ordering, because changing it later means a reinstall (below).

## The Server Auction

Used hardware from returned contracts, at a discount, usually with no setup fee and immediate availability.

- **Each machine is a one-off.** The exact CPU, disk set and RAM configuration will not be available again. Building a fleet where nodes must be identical on auction inventory is a design that cannot be repaired.
- Read the listing carefully: disk count and type, ECC or not, RAM total, and whether the price is promotional.
- Age is a fact, not a defect: a five-year-old machine with new disks is fine for a CI runner and wrong for the only copy of a database.
- Good uses: CI and build runners, batch processing, bulk storage, staging, a second site for replication. Bad uses: anything that must be replaced identically within an hour.

## Setup Fees and Billing

- Most new orders carry a one-time setup fee; auction machines usually do not. Include it in any comparison against cloud, amortised over the expected life: a €69 setup on a machine kept 12 months is ~€6/month.
- Billing is monthly with no hourly option. A dedicated server used for three days costs a month — which makes "just try it" an expensive experiment compared to a cloud instance.
- The break-even against cloud is utilisation: dedicated wins on price per core and per GB of RAM once the machine is genuinely busy most of the time, and loses everywhere else (`costs.md`).

## installimage

The provisioning tool in the rescue system: it partitions, builds the RAID, installs a distribution, and writes the bootloader from a config file.

- The config is a text file: distribution image, hostname, RAID level, partition layout, filesystem, and optional post-install steps.
- **The config is worth keeping.** Rebuilding a machine from memory at 2am is how partition layouts drift between supposedly identical servers. Save the working config to `~/Clawic/data/hetzner/artifacts/installimage-<role>.md` with its `## Boxes` line, with any password replaced by its pointer.
- Partition decisions that are painful to change afterwards: swap size, whether `/` is LVM, and whether the data directory is a separate filesystem. Decide once, encode it in the config, reuse it.
- installimage wipes the machine. Anything not backed up is gone, including the VLAN interface configuration for a vSwitch — put that in the post-install steps or you will lose private connectivity on every reinstall.
- After install: key-only SSH, host firewall, monitoring agent, and the row in `servers.md`. Automate it with the same configuration management as the cloud fleet (`automation.md`).

## RAID Choices

| Layout | Capacity | Survives | Take it when |
|---|---|---|---|
| RAID0 | All | Nothing — one disk failure loses everything | Never for anything with state; acceptable for a scratch CI runner rebuilt from code |
| RAID1 (2 disks) | Half | One disk | The default for a two-disk machine |
| RAID10 (4+ disks) | Half | One per mirror pair | Databases on a four-disk machine |
| RAID5/6 | More | One / two disks | Bulk storage on SX machines; rebuild times on large spinning disks are long and risky |
| No RAID | All | Nothing | Only when the data is replicated at the application layer across machines |

Software RAID via installimage is standard here. Two operational obligations follow: **monitor the array** (a degraded array that nobody notices is a single disk away from total loss) and **route the monitoring alert to a human** — the provider's alert about a failed disk goes to the account email, and that address must be read.

## Rescue and IPMI

- **Rescue system**: a network-booted Linux with the machine's disks unmounted. Activated from Robot, generates a one-time root password (a credential — pointer only), and requires a reboot to enter. This is where installimage runs, where filesystems get repaired, and where a broken bootloader gets fixed.
- **IPMI / KVM console**: remote console and power control for a machine that will not even network-boot. Availability and access mechanism vary by line; request it through Robot when the rescue system itself is unreachable.
- Order of escalation for an unreachable dedicated server: ping and port check from outside → Robot's status for the machine → hardware reset from Robot → rescue system → IPMI → support ticket. Skipping to the ticket wastes the hour where the reset would have worked; skipping the reset on a machine with a degraded array can make things worse — read the mail first.

## Hardware Failure

The thing cloud users forget exists:

- A failed disk in a RAID1 is not an outage but is an emergency: a second failure during the rebuild loses everything, and rebuild on large disks takes hours.
- Replacement is a support ticket with a hardware technician on the other end, scheduled, not instant. A machine that must be back in 15 minutes cannot be a single dedicated server.
- After a disk swap, the array rebuild is yours to trigger and verify. Confirm the new disk is in the array and the bootloader is installed on **both** disks, or the next reboot boots nothing.
- **Write it down**: the failure, the ticket, the resync time and the outcome go into `~/Clawic/data/hetzner/incidents/<year>.md`. Two failures on one machine in a year is a signal to move the workload.

## Networking: Additional IPs, Failover, vSwitch

- Additional single IPs and subnets are ordered per machine and may carry a monthly charge; they are configured inside the OS, not automatically.
- **Failover IPs** can be switched between dedicated servers through Robot for active/passive setups, and like cloud floating IPs they must be configured on the target host to do anything (`network.md`).
- **vSwitch** provides a VLAN between dedicated servers, and can be attached to a Cloud Network — the supported private link between dedicated and cloud. The VLAN interface is OS configuration and does not survive a reinstall unless it is in the installimage post-install steps.
- There is no cloud firewall for dedicated machines: filtering is the host firewall, plus whatever the vSwitch topology gives you (`firewall.md`).

## Cancellation

- Cancellation takes effect at a **period boundary**, and the request has to land before that period's cut-off. A day late buys another full month.
- The deadline is knowable the day the server is ordered. Record it in `## Due` immediately, as a one-off line with the date — this is the single most avoidable recurring waste in this domain.
- Before cancelling: confirm the data is off the machine and restorable, that no DNS record or failover IP still points at it, and that no vSwitch member depends on it. A cancelled dedicated server is wiped, not archived.
- **Write it down**: on cancellation, delete the row in `~/Clawic/data/servers/servers.md`, note the effective date in `memory.md`, and remove the deadline from `## Due`.

## When Dedicated Is the Wrong Answer

- The workload is spiky, and half the month it is idle — hourly cloud billing wins.
- It must survive a hardware failure without human involvement — that needs two machines or a cloud tier.
- Nobody will monitor the RAID or read the hardware mail — an unmonitored array is worse than no redundancy, because it feels safe.
- The requirement is "cheaper", and the comparison omitted the setup fee, the migration effort, and the hour a technician takes (`costs.md`).
