# Processes And Signals — Killing, Keeping Alive, and Reading /proc

Signals are advisory except SIGKILL and SIGSTOP, and even those cannot touch a task in uninterruptible sleep. Diagnose the STATE first; the state names the fix.

## Read The State Before Sending Anything

```bash
ps -o pid,ppid,stat,wchan:20,etime,rss,args -p <pid>
```

| STAT | Meaning | What works |
|---|---|---|
| `R` | Running/runnable | Any signal |
| `S` | Interruptible sleep (normal idle) | Any signal |
| `D` | Uninterruptible sleep — waiting on I/O | **No signal, including -9.** Fix the I/O (`wchan` names it): dead NFS mount, failing disk, stuck device |
| `Z` | Zombie — already dead, waiting to be reaped | Nothing. Kill or fix the PARENT; init adopts and reaps the child |
| `T` | Stopped (SIGSTOP/Ctrl-Z) | `kill -CONT`; a `-TERM` to a stopped process only queues |
| `t` | Traced (a debugger or strace is attached) | Detach the tracer first |
| `I` | Idle kernel thread | Leave it alone; it does not consume CPU |

Suffixes worth reading: `s` session leader, `+` foreground group, `<`/`N` raised/lowered nice, `l` multithreaded.

- D-state cure for a dead NFS server: `umount -l /mnt/dead` (lazy) detaches the tree; the blocked tasks return errors and exit on their own. Rebooting is the fallback, not the first move.
- Zombies cost one process-table slot and zero memory. A few are noise; thousands mean a parent that never calls `wait()` — that is the bug to file.

## Killing Precisely

- Preview every pattern match: `pgrep -af <pattern>` before `pkill -f <pattern>`. `-f` matches the FULL command line, so `pkill -f python` also kills editors, agents, and any daemon whose argv mentions python.
- Signal ladder: `kill -TERM` → wait the app's real shutdown time → `kill -KILL` only if it ignored you. `kill -9` skips cleanup handlers; on a database that buys you crash recovery on the next start.
- Kill a whole process group instead of chasing children: `kill -TERM -<PGID>` (note the minus). Get the PGID with `ps -o pgid= -p <pid>`.
- Managed services: `systemctl stop <unit>` beats `kill`, because it signals the unit's whole cgroup and honours the unit's `KillMode` and timeout (→ `systemd.md`).
- `kill -0 <pid>` sends nothing and tests existence + permission — the correct liveness check in a wait loop.
- PID reuse is real on busy hosts: a pid file written minutes ago can name a different process. Verify with `ps -o lstart= -p <pid>` or use the cgroup/unit instead.
- `timeout 30s <cmd>` bounds anything that can hang; `timeout -k 5s 30s` escalates to KILL 5s after TERM.

## Keeping Work Alive

- Closing a terminal SIGHUPs its jobs. Already running: `disown -h %1`. About to start: `setsid <cmd>` or `nohup <cmd> &`.
- The durable answer on a remote host is a multiplexer (`tmux new -s work`, reattach with `tmux attach -t work`) — it also survives your laptop sleeping and the Wi-Fi dying mid-upgrade.
- Fire-and-forget under systemd, with logs and resource limits for free: `systemd-run --unit=migrate --collect -p MemoryMax=2G /usr/local/bin/migrate.sh`, then `journalctl -u migrate -f`.
- Any job launched from a login session dies with the session if `KillUserProcesses=yes` in `logind.conf` (default on some distros) — `systemd-run --scope` or a real unit avoids that whole class of surprise.

## Limits (the "too many open files" family)

- Soft limit is what applies, hard limit is the ceiling you may raise to as a normal user: `ulimit -Sn` / `ulimit -Hn`. A commonly shipped soft default is 1024.
- **systemd services ignore `/etc/security/limits.conf`** — that file is PAM, so it only touches login sessions. Set `LimitNOFILE=65536` in the unit (`systemctl edit <unit>`).
- Inspect what a RUNNING process actually got: `cat /proc/<pid>/limits`. Raise it without restarting: `prlimit --pid <pid> --nofile=65536:65536`.
- `fs.file-max` is the system-wide ceiling (kernel side, → `kernel.md`); the per-process limit is what you hit first in practice.
- Fork bombs and runaway thread creation: cap with `TasksMax=` in the unit or `pids` limits; the symptom is `fork: Resource temporarily unavailable` from a healthy-looking shell.

## /proc, The Live Debugger

```bash
tr '\0' '\n' < /proc/<pid>/environ      # the env it was actually started with, not yours
tr '\0' ' '  < /proc/<pid>/cmdline      # full argv, untruncated
ls -l /proc/<pid>/cwd /proc/<pid>/exe   # where it runs, which binary (even if deleted)
ls -l /proc/<pid>/fd | tail             # open files, sockets, and the deleted ones holding disk
cat /proc/<pid>/status                  # Threads, VmRSS, voluntary/nonvoluntary ctxt switches
```

- A binary upgraded under a running process shows `/proc/<pid>/exe -> /usr/bin/app (deleted)` — the running code is the OLD version. That is why `needrestart` exists (→ `packages.md`).
- Recover a deleted-but-running file: `cp /proc/<pid>/fd/<n> /tmp/recovered` while the process still holds it.
- High `nonvoluntary_ctxt_switches` = CPU starvation (the scheduler preempted it); high voluntary = it waits on I/O or locks.

## Priority And Placement

- `nice` range is -20 (highest priority) to 19; only root lowers the number. `renice -n 10 -p <pid>` after the fact.
- Niceness does nothing for an I/O-bound job — use `ionice -c3 <cmd>` (idle class) for backups, `rsync`, and `du` sweeps so they yield to production I/O.
- `taskset -c 0-3 <cmd>` pins CPUs; useful to keep a noisy batch job off the cores serving latency-sensitive work, harmful as a default.
- cgroup v2 is the real lever on modern hosts: `systemd-run -p CPUQuota=50% -p MemoryMax=1G --scope <cmd>` bounds an ad-hoc job the same way a unit bounds a service. `systemd-cgtop` shows who is actually consuming.

## Tracing, With Its Cost Stated

- `strace -f -p <pid>` slows the target by roughly an order of magnitude — acceptable on a stuck process, dangerous on a busy one. Prefer `strace -c -f -p <pid>` for a few seconds to get a syscall histogram, then stop.
- `strace -e trace=file <cmd>` answers "which path is it failing to open" in one shot, faster than reading its config.
- For a hot production process, sample instead of trace: `perf top -p <pid>` (→ `performance.md`).
- Crash forensics: `coredumpctl list` then `coredumpctl gdb <pid>` on systemd hosts; if there is no core, `ulimit -c` is 0 or `kernel.core_pattern` sends it elsewhere.

## Exit Codes

The 128+N decoding table and the signal numbers live in `SKILL.md` (Signals And Exit Codes). Two traps that belong here:

- An application may return 137 by itself; confirm a real SIGKILL with `journalctl -k` or `dmesg -T` before blaming the OOM killer (→ `oom.md`).
- In a pipeline, `$?` is the LAST command's status. `set -o pipefail` or `${PIPESTATUS[@]}` recovers the rest (→ the `bash` skill).

## Record It

A limit you raised is a change: `LimitNOFILE=`, `TasksMax=`, a `prlimit` applied live, or a nice/ionice policy goes to `~/Clawic/data/linux/changes/<year>.md` with the drop-in path and the rollback — and note whether it was applied live only, because that one is gone at the next restart. A process that had to be killed the same way twice is an incident pattern, not a chore: `incidents/<year>.md`, then `## Recurring Incidents` on the repeat (`memory-template.md`).

Related: OOM kills and memory pressure → `oom.md` · CPU/IO saturation → `performance.md` · services and their cgroups → `systemd.md`.
