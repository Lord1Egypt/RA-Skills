# Monitoring A Host — What To Measure, What To Alert On, What To Record

Two failures are equally common: no alerts, and so many alerts that nobody reads them. The cure for both is the same — alert on saturation and on symptoms, record everything else as a baseline. Read `baselines/<host>.md` before calling any number high or low; without a healthy-period number from the same machine, every threshold below is a guess.

Scope here is one host: what it should measure, what deserves a page, and what to write down. Building the stack — exporters, dashboards, alert routing, tracing — belongs to the `monitoring` skill.

## Utilization, Saturation, Errors

Brendan Gregg's USE method is the whole framing: for every resource, measure **utilization** (how busy), **saturation** (how much is queued and waiting), and **errors**. Users feel saturation and errors; utilization is the number that produces false alarms.

| Resource | Utilization (context) | Saturation (alert on this) | Errors |
|---|---|---|---|
| CPU | `%usr`+`%sys` per core | `load1/nproc`, PSI `cpu some`, cgroup `nr_throttled` | — |
| Memory | `used` (never `free`) | `available` low, PSI `memory some`, swap `si`/`so`, cgroup `memory.events` `oom_kill` | OOM kills in `dmesg` |
| Disk | `%util` (meaningless on NVMe) | `await`, `aqu-sz`, PSI `io some` | `dmesg` I/O errors, SMART |
| Filesystem | `df` percent | Days-to-full trend, inode percent | Read-only remount |
| Network | bandwidth vs negotiated speed | `retrans`, accept-queue `Recv-Q`, conntrack count | `ip -s link` errors/dropped |
| else | Whatever the workload defines | Queue depth in the application itself | Its own error rate |

## Thresholds Worth Defending

Each of these has a reason, and each is a starting point to be moved once the baseline says what normal is on this host.

| Signal | Alert when | Why that number |
|---|---|---|
| `load1 / nproc` | Above `load_alarm_ratio` (default 1.0) sustained 15 min | Normalized, so it means the same on 4 and 64 cores. A spike is not an incident; a plateau is |
| PSI `io some avg60` | Above 20% | A fifth of the time at least one task was stalled on storage — comparable across machine sizes, which load is not |
| Filesystem usage | Above `disk_alert_pct` (default 80%) on EVERY mount, not just `/` | A full root blocks logging, package operations, and sometimes login (→ `disk-space.md`) |
| Filesystem days-to-full | `free ÷ daily_growth` below 14 days | The derivative catches what the level misses: 60% growing 5 points a day is worse than a stable 85% |
| Inodes | Above 80% in `df -i` | Exhaustion presents as "No space left on device" with free space showing |
| `available` memory | Below ~10% of total, or PSI `memory some` above 10% | `available`, never `free`: cache is doing its job (→ `oom.md`) |
| Swap in/out | Sustained nonzero `si` AND `so` | Thrash, which is worse than an OOM kill because nothing ends decisively |
| conntrack | `nf_conntrack_count` above 80% of max | The overflow is silent packet drops (→ `networking.md`) |
| Failed units | `systemctl --failed` non-empty | The cheapest whole-host health check that exists |
| Reboot required | `/var/run/reboot-required`, or `dnf needs-restarting -r` | A patched kernel that never rebooted is an unpatched kernel (→ `packages.md`) |
| Certificate / key expiry | 21 days out | Renewals fail, and the second attempt needs a human awake |
| Backup heartbeat | Missing for one interval plus a margin | Absence of success, not presence of failure (→ `backups.md`) |
| Clock offset | Unsynchronized, or above a few seconds | Breaks TLS, tokens, Kerberos, and log correlation (→ `scheduling.md`) |

## What Not To Alert On

- **CPU utilization.** A batch host at 100% is working correctly; a latency service at 30% can already be failing. Alert on the queue, not the busyness.
- **`free` memory being low.** That is a healthy warm cache.
- **`%util` on SSD/NVMe.** It measures "at least one request in flight" and reads 100% on a device serving 32 requests in parallel (→ `performance.md`).
- **Any single spike.** Every threshold gets a duration. A page that fires on one scrape teaches the team to ignore pages.
- **Causes when you can alert on symptoms.** "Checkout p95 above 2s" survives every refactor; "queue depth on sdb above 8" is obsolete the day the storage changes. Keep cause-level signals as dashboards for diagnosis and page on the symptom.

## Cheap Host Monitoring That Needs No Stack

- `systemctl --failed`, `journalctl -b -p err`, `df`, and a heartbeat file cover most of a small fleet's real incidents. A timer that emails or pings when one of those trips is a Sunday afternoon of work.
- `OnFailure=notify@%n.service` on the units that matter turns every failed service and every failed timer job into an alert, using only systemd (→ `scheduling.md`).
- Kernel-only events — OOM kills, I/O errors, filesystem remounted read-only, conntrack full — never appear in an application log. Watch `journalctl -k -p err` explicitly (→ `kernel.md`).
- PSI (`/proc/pressure/*`, and `/sys/fs/cgroup/<unit>/*.pressure` per service) is the highest signal-to-noise number available on a modern kernel and costs one read.
- Where an exporter is in play, the host-level set that earns its keep is: node CPU/memory/disk/filesystem/network, systemd unit states, textfile collector for anything custom. Everything else is a dashboard, not an alert.

## Baselines: The Diff Is The Product

- Measure during a **healthy period**, name it as such, and date it. A baseline taken during an incident makes the incident look like normal.
- Record into `baselines/<host>.md`: load and PSI ranges, `available` memory, root and data filesystem usage, `await` per device, the listening-port set, the count and list of setuid binaries, enabled units, and the storage layout.
- The value is entirely in the diff at the next review: a new listener, a new setuid binary, a new enabled unit, or an `await` an order of magnitude off are all findings that no absolute threshold would have produced (→ `hardening.md`, `compromise.md`).
- Re-measure after a deliberate change of size — new workload, resize, distro upgrade — and overwrite. A stale baseline hides a real regression.

## Record It

Write every measurement into `~/Clawic/data/linux/baselines/<host>.md` (`## Healthy Numbers`, `## Listening`, `## Audit Surface`, `## Storage Layout`), created on the first measurement with its `## Boxes` line in `memory.md`. Put the review cadence — audit-surface diff, retention review — into `## Due`. Thresholds the user chooses differently from the defaults are declarations: they go to `config.yaml`, not into the baseline. Formats: `memory-template.md`.

Related: saturation triage → `performance.md` · memory pressure → `oom.md` · disk trend and reclaim → `disk-space.md` · alert plumbing with timers → `scheduling.md` · audit surface → `hardening.md`.
