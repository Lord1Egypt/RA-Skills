# Memory And OOM — Reading Usage Honestly, Surviving The Killer

Almost every "the server is out of memory" report is one of four different things: cache doing its job, a cgroup limit, swap thrash, or an actual leak. They have different signatures and opposite fixes.

## Read `free` Correctly

```
              total   used    free   shared  buff/cache   available
Mem:            15Gi  4.0Gi   180Mi   320Mi        11Gi        10Gi
```

- **`available` is the only number that answers "can I start something?"** It estimates reclaimable cache plus free. Low `free` with high `available` is a healthy, warm system.
- `buff/cache` is page cache the kernel will drop the instant anything needs the memory. Nobody should be alarmed by it, and nobody should try to reclaim it.
- `echo 3 > /proc/sys/vm/drop_caches` is a benchmarking tool, not a fix. It throws away warm cache, makes the next minutes slower, and changes no real memory pressure.
- `shared` includes tmpfs and `/dev/shm` — those DO count as memory and are not reclaimable while files sit in them. `/dev/shm` defaults to half of RAM; a process writing there can OOM the box while `du` on the disk shows nothing (→ `disk-space.md`).

## Who Is Actually Using It

- Summing RSS across processes overcounts shared pages: every worker counts the same copy-on-write parent memory. `ps aux` %MEM summing past 100% is this, not a bug.
- PSS divides shared pages by the number of sharers and is the number to quote: `grep Pss /proc/<pid>/smaps_rollup`, or `smem -k -s pss -r | head`.
- Kernel memory does not appear in any process: `slabtop -s c` (sorted by cache size). Growing `dentry`/`inode_cache` is usually a workload creating millions of files; a genuinely leaking module shows as an unbounded slab with no matching workload.
- Per-cgroup truth on modern hosts: `systemd-cgtop -m` for the live view, `cat /sys/fs/cgroup/<path>/memory.current` for one service. This is what the OOM killer actually accounts against.

## The OOM Killer

- Forensics: `dmesg -T | grep -iE 'out of memory|oom_kill'` or `journalctl -k -g oom`. The log names the killed process, its RSS, and the constraint (`oom-kill:...constraint=CONSTRAINT_MEMCG` = a cgroup limit, not the host).
- Selection: the kernel scores every candidate roughly by fraction of available memory consumed, on a 0-1000 scale, then adds `oom_score_adj` (range -1000..1000, applied on the same scale). So `oom_score_adj=-900` makes a process effectively unkillable until it alone uses ~90% of memory. Read live values with `cat /proc/<pid>/oom_score`.
- It frequently kills the biggest process, not the one that caused the shortage — the leaking 200 MB script survives, the 8 GB database dies.
- Protect the daemons that let you recover: `OOMScoreAdjust=-900` in the unit for the database or the agent you need alive. Reserve full exemption (-1000) for sshd only; an exempt memory hog forces the kernel to kill everything else on the host instead.
- Prefer bounded failure to random victims: `MemoryMax=2G` in the unit kills only that service's cgroup, and `MemoryHigh=1.5G` throttles it (reclaim pressure) before anything dies. `memory.events` in the cgroup counts `oom_kill` — a non-zero, climbing counter is your alert.
- Exit code 137 with plenty of free host memory = the process hit a cgroup/container limit, not the host ceiling (→ `SKILL.md` Signals And Exit Codes).

## Swap

- `vm.swappiness` defaults to 60 — the kernel's willingness to swap anonymous pages instead of dropping cache. Set 1-10 for databases and latency-sensitive services; 0 does not disable swap, it only makes the kernel avoid it until it is nearly out.
- Thrash detection: `vmstat 1` and watch `si`/`so`. Sustained nonzero swap-in AND swap-out means the working set does not fit — the machine crawls at a fraction of its speed while every check reports "healthy". This is worse than an OOM kill, which at least ends decisively.
- Sizing: swap is an overflow valve for cold pages and a place for hibernation, not extra RAM. A few gigabytes is enough for a server; sizing it to match RAM only guarantees a longer, slower death.
- `swapoff -a` requires enough free RAM to hold everything currently swapped — running it on a pressured host triggers the OOM killer immediately. Check `free` first.
- zram (compressed swap in RAM) is a real win on memory-constrained hosts: compressible pages cost ~2-3× less RAM than they occupy, with CPU as the price.
- Adding a swap file (the portable answer when there is no swap partition): `fallocate -l 2G /swapfile` (use `dd if=/dev/zero of=/swapfile bs=1M count=2048` on filesystems where `fallocate` produces an unusable extent-mapped file, notably older btrfs), then `chmod 600 /swapfile && mkswap /swapfile && swapon /swapfile`, then an fstab line `/swapfile none swap sw 0 0`. Mode 600 is not cosmetic — a world-readable swap file exposes whatever the kernel paged out.

## Overcommit

- `vm.overcommit_memory=0` (default) is a heuristic: large allocations may be refused, ordinary ones are granted optimistically and the OOM killer is the backstop.
- Mode 2 (`overcommit_memory=2`, `overcommit_ratio=N`) makes allocation fail with ENOMEM instead of killing later — deterministic, and it breaks any application that reserves large virtual regions (JVMs, Go runtimes, Redis's fork-based persistence).
- Redis logging "Background save may fail under low memory" is this: `fork()` reserves the parent's whole address space on paper. `vm.overcommit_memory=1` is the vendor-documented setting for that specific case.

## Application-Level Ceilings

- A runtime with its own heap limit must be capped BELOW the cgroup limit, or the runtime grows into a kill: JVM `-XX:MaxRAMPercentage=75` (container-aware; older JVMs sized the heap from HOST memory and OOM instantly in a small cgroup), Node `--max-old-space-size` in MB at ~75-80% of the limit.
- Growing RSS is not proof of a leak. Allocators return freed memory to the OS lazily; glibc's arenas can hold it indefinitely. Judge on a plateau: memory that never stops rising across days, under constant load, is a leak.
- Confirm with a heap profiler for the language before rewriting anything. The `debugging` skill covers isolation strategy.

## Fast Triage

| Signature | Diagnosis | Move |
|---|---|---|
| Low `free`, high `available`, no swap activity | Healthy cache | Do nothing |
| `si`/`so` sustained in `vmstat 1` | Thrash — working set exceeds RAM | Cut the workload or add RAM; swappiness is a mitigation, not a fix |
| Exit 137, `constraint=CONSTRAINT_MEMCG` in dmesg | cgroup/container limit | Raise `MemoryMax` or fix the service |
| Exit 137, host-wide OOM report | Real host exhaustion | Find the largest PSS consumer, add limits to prevent a repeat |
| RSS flat, `available` falling for days | Kernel slab or tmpfs growth | `slabtop -s c`, `df -h /dev/shm` |
| ENOMEM without any kill | Overcommit mode 2 or a per-process limit | `cat /proc/<pid>/limits`, `sysctl vm.overcommit_memory` |
| Anything else | Establish the trend before acting | Sample `available` and per-cgroup `memory.current` over an hour, against the figure in `baselines/<host>.md` |

## Record It

An OOM kill is an incident with a root cause worth one row: host, which process the kernel picked, whether the constraint was the cgroup or the host, and what fixed it, in `~/Clawic/data/linux/incidents/<year>.md`. The fix itself — `MemoryMax=`, `MemoryHigh=`, `OOMScoreAdjust=`, a swappiness change, a new swap file — goes to `changes/<year>.md` with its drop-in path and rollback, and the host's normal `available` figure belongs in `baselines/<host>.md` so the next "it is running out of memory" report can be checked against a number instead of a feeling (`memory-template.md`).

Related: cgroup limits and unit directives → `systemd.md` · CPU and I/O saturation → `performance.md` · kernel tunables and persistence → `kernel.md` · thresholds worth alerting on → `monitoring.md`.
