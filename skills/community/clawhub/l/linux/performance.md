# Performance — Finding The Saturated Resource, Not The Busy One

Utilization tells you something is working; saturation tells you something is waiting. Users only ever feel saturation. Every triage below is: measure saturation per resource, find the one that is queueing, then attribute it to a process.

## The 60-Second Sweep

```bash
uptime                      # load1/load5/load15 — direction matters more than value
vmstat 1 5                  # r (runnable) vs b (blocked), si/so (swap), wa (I/O wait)
iostat -xz 1 3              # per-device: aqu-sz, await, %util
pidstat -u -d 1 3           # per-process CPU and disk, the attribution step
ss -s                       # socket totals — connection churn or TIME_WAIT buildup
cat /proc/pressure/{cpu,io,memory}   # PSI: the honest saturation number
```

- Read `vmstat`'s first line as a since-boot average and ignore it; the second line onward is current.
- `r` sustained above the core count means CPU queueing. `b` non-zero means tasks blocked on I/O — that is where load average comes from on an idle-looking CPU.

## Load Average, Correctly

- Linux load counts runnable AND uninterruptible (D-state) tasks. **Load 30 with idle CPUs is a storage incident, not a compute one** (→ `processes.md`).
- Normalize before judging: `load1 / nproc`. Alarm when that ratio exceeds `load_alarm_ratio` (default 1.0) for a sustained period — load 8 on 4 cores is a ratio of 2.0, twice oversubscribed; load 8 on 16 cores is a half-idle machine.
- Compare load1 against load15 for direction: 1-minute far above 15-minute means it is getting worse right now; the reverse means you are looking at the tail of a spike that is already over.

## PSI: Better Than Load Average

`/proc/pressure/{cpu,io,memory}` reports how much time tasks spent stalled, as a percentage of the last 10, 60, and 300 seconds:

```
some avg10=23.15 avg60=18.02 avg300=9.44 total=...
full avg10=11.03 ...
```

- `some` = at least one task was stalled on this resource. `full` = every runnable task was stalled — that is the number that maps to "the box feels dead".
- It is an absolute figure, comparable across machines of different sizes, which load average is not. `io some avg10 > 20` is a real I/O problem regardless of the core count.
- Per-service pressure on cgroup v2 hosts: `/sys/fs/cgroup/<unit>/{cpu,io,memory}.pressure` attributes the stall to one service.

## CPU

- `top`/`htop` %CPU is per-core: 400% means four cores saturated, not a bug. Press `1` in `top` to see cores individually — one core at 100% with the rest idle is a single-threaded bottleneck, and adding cores will not help.
- `%st` (steal) above a few percent on a cloud VM means the hypervisor is giving your vCPU to someone else. You cannot tune it away; resize, move, or change instance family.
- `%wa` (I/O wait) is idle time WITH pending I/O — high `wa` means the CPU is waiting on storage, not that the CPU is busy.
- **cgroup CPU throttling is invisible in `top`**: a container or unit with `CPUQuota=` gets frozen at the end of each 100 ms period once it exhausts its slice, producing latency spikes with plenty of host CPU idle. Check `cpu.stat` for `nr_throttled` and `throttled_usec` climbing; the fix is a higher quota or fewer threads, not more cores.
- Attribute before optimizing: `pidstat -u 1`, then `perf top -p <pid>` for the hot functions. `perf` samples at low overhead; `strace` does not (→ `processes.md`).
- Thermal or governor limits on bare metal: compare `lscpu | grep MHz` and `cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor` — `powersave` on a server costs real throughput.

## Disk I/O

- `iostat -xz 1`: the meaningful columns are `r_await`/`w_await` (latency in ms, the number users feel), `aqu-sz` (average queue depth — the saturation signal), and `r/s`+`w/s`.
- **`%util` is a lie on SSD and NVMe.** It measures "time with at least one request in flight", and a device that serves 32 requests in parallel shows 100% while barely working. Judge by `await` and queue depth instead.
- Rough latency expectations, order of magnitude: NVMe tens of microseconds, SATA SSD a few hundred, spinning disk 5-15 ms, network storage whatever the network adds. An `await` an order of magnitude above the device's class is the finding.
- Attribute with `pidstat -d 1` or `iotop -oPa`. Sequential background work (backups, `du` sweeps, log compression) should run under `ionice -c3` so it yields to production I/O.
- Sudden latency with normal throughput on a filesystem that is nearly full is fragmentation and allocation pressure — free space is a performance parameter, not just a capacity one (→ `disk-space.md`).
- Errors first, always: `dmesg -T | grep -iE 'i/o error|reset|nvme'`. A failing disk produces retries that look exactly like a slow application (→ `storage.md`).

## Network

- Throughput problems: check errors and drops before bandwidth — `ip -s link` (rx/tx errors, dropped), `nstat -az | grep -iE 'retrans|drop|overflow'`.
- Latency and retransmits per connection: `ss -tin` shows rtt and retrans for each socket.
- Accept-queue overflow, conntrack exhaustion, and ephemeral-port limits produce failures that look like application slowness → `networking.md`.
- A saturated 1 Gbit link is ~118 MB/s of payload; measuring 950 Mbit and calling it a bug wastes a day. Check the negotiated speed with `ethtool <iface>` before assuming the link is the problem.

## Method

1. **Establish the complaint in numbers.** "Slow" is not actionable; p95 latency, throughput, or a job's wall time is.
2. **Sweep all four resources** (CPU, memory, disk, network) for saturation before drilling into any one. The obvious resource is often the victim of another.
3. **Attribute to a process or cgroup** before touching configuration.
4. **Change one thing, re-measure.** Tuning several sysctls at once produces a host nobody can reason about (→ `kernel.md`).
5. **Compare to a baseline.** Without a known-good number from the same host, "high" is an opinion. Read `~/Clawic/data/linux/baselines/<host>.md` before judging any number, and when it does not exist, measure during the next healthy period and write it there under `## Healthy Numbers` — load range, PSI, `available`, per-device `await` — with its `## Boxes` line in `memory.md`. Any tuning that came out of the investigation goes to `changes/<year>.md` with its rollback (`memory-template.md`, thresholds in `monitoring.md`).

## Fast Attribution Table

| Signature | Resource | Next step |
|---|---|---|
| High load, idle CPU, `b` > 0 in vmstat | Disk or network storage | `iostat -xz 1` await; `pidstat -d 1` |
| One core pinned, others idle | Single-threaded app | `perf top -p <pid>` |
| High `%st` | Hypervisor contention | Resize or migrate the instance |
| Latency spikes with idle host CPU | cgroup CPU throttling | `cpu.stat` `nr_throttled`, raise `CPUQuota` |
| `si`/`so` nonzero in vmstat | Memory — swap thrash | → `oom.md` |
| High `await`, low IOPS | Slow or failing device | `dmesg`, `smartctl` (→ `storage.md`) |
| Retransmits climbing, CPU idle | Network path | `ss -tin`, `nstat` (→ `networking.md`) |
| Everything looks fine, users complain | Wrong layer measured | Measure inside the application (the `debugging` skill) |

Related: memory pressure and OOM → `oom.md` · tunables and their persistence → `kernel.md` · per-process tools → `processes.md`.
