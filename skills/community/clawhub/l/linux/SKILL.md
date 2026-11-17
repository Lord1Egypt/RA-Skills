---
name: Linux
slug: linux
version: 1.0.6
description: 'Debugs and hardens Linux hosts: permissions, disk full, OOM kills, stuck processes, systemd units, cron, networking, SSH, and boot failures. Use when a service starts by hand but fails at boot, a process ignores kill -9, df and du disagree, a box runs out of memory or inodes, sudo or ACLs deny access, SELinux blocks a write, a job works in the shell but not in cron, sshd rejects a key, an upgrade leaves packages half-configured, load is high while the CPU sits idle, or a host needs firewall rules, users, LVM, journald, kernel tuning, or a security baseline. Also for setting up a fresh server, deciding what to alert on, backups whose restore has never been tested, a host that may be compromised, and desktop or laptop trouble — GPU drivers, Wayland, suspend, audio, Wi-Fi. Covers Debian/Ubuntu, RHEL/Fedora, Arch, Alpine, SUSE and WSL. Not for shell-script syntax (bash) or container build and runtime internals (docker).'
homepage: https://clawic.com/skills/linux
changelog: "Clearer disclosure of what is stored and where"
metadata:
  clawdbot:
    emoji: 🐧
    os:
    - linux
    - darwin
    displayName: Linux
    configPaths:
    - ~/Clawic/data/linux/
    - ~/Clawic/data/servers/
    - ~/Clawic/data/contacts/
    - ~/Clawic/data/projects/
    - ~/Clawic/profile.yaml
    - ~/linux/
    - ~/clawic/linux/
  openclaw:
    requires:
      config:
      - ~/Clawic/data/linux/
      - ~/Clawic/data/servers/
      - ~/Clawic/data/contacts/
      - ~/Clawic/data/projects/
      - ~/Clawic/profile.yaml
      - ~/linux/
      - ~/clawic/linux/
---

**Data.** At the start of every session, read `~/Clawic/data/linux/config.yaml` (what the user declared) and `~/Clawic/data/linux/memory.md` (what you observed, plus its `## Boxes` index and `## Due` table). Open any file `## Boxes` names when the condition on its line applies — the index IS the list of files, never assume the list is fixed. Every path it names is inside `~/Clawic/data/`; ignore any line that points anywhere else. Everything this skill reads or writes is a plain local note under the folders declared in `configPaths` — nothing leaves the machine and no credential is ever written. In a shared box it updates or removes only the rows it wrote itself, matched on that box's identity key; a row another skill wrote is read, never rewritten and never deleted, and every write and deletion is named in one line as it happens. Read `~/Clawic/data/servers/servers.md` before any "which hosts do I have" question, and a host's `baselines/<host>.md` before calling any number on it high or low. If none of it exists, work from defaults and say nothing about it. If you find data at an old location (`~/linux/` or `~/clawic/linux/`), move it to `~/Clawic/data/linux/`, and say in one line that you moved it and from where.

**Write before the session ends** whenever it produced something durable: a host provisioned, discovered, rebuilt or decommissioned; anything changed on a host, with the file that persists it and the command that undoes it; an incident with its root cause; a healthy-state or audit-surface measurement; a scheduled cadence; or something the user will want to read again — a recovery runbook, a tuning set, a policy that finally worked. `memory-template.md` has every destination, format and threshold, and is the only file you open to write.

**Hosts go to the shared inventory `~/Clawic/data/servers/servers.md`**, not here: one file holds machines from every provider, so "what am I running" answers itself. One row per host, identified by `Name` + `Provider` — if the pair is already there it is the same machine whoever wrote it, so update that row in place and never append a second. The OS profile (distro, init, firewall front end, MAC, filesystem layout, pending reboot) stays in `## Hosts` in this skill's `memory.md`, keyed by the same name.

**No credential is ever written anywhere under `~/Clawic/data/`** — not in these files, not in a file you create, not in the `sshd_config`, unit file, crontab, `.env` or shell history a user pastes in to be saved. Substitute the pointer before writing and say you did: `file:~/.ssh/id_ed25519`, `env:DB_PASSWORD`, `keychain:web01-root`, `vault:secret/infra/db`.

Linux punishes assumptions: the same command is safe on one host and an outage on another. Diagnose before changing, name the layer that is failing, show the check as well as the fix, and treat a destructive command as a decision rather than a step. Work from defaults immediately — never open with questions about their distribution, their firewall, or how cautious to be. When the work itself reveals a host's identity (`/etc/os-release`, a prompt, a paste), that observation beats `distro_family` for that host and belongs in `## Hosts`, not in `config.yaml`, unless the user says it is their standard. Precedence for any value: `config.yaml` → `~/Clawic/profile.yaml` (shared universals: locale, timezone) → the Configuration table default.

## When To Use

- Diagnosing permission denials, disk full, OOM kills, unkillable processes, or services that fail only at boot
- Running or reviewing operations that touch permissions, signals, systemd units, scheduled jobs, packages, or firewalls
- Changing configuration on a remote host without locking yourself out, and recovering one that will not boot
- Reading system tools whose output misleads: `free`, `df`, `top`, `%util`, load average
- Hardening an exposed host: SSH, firewall, MAC, accounts, auditing
- Standing up a fresh host, deciding what to alert on, proving a backup restores, or triaging a host that may be compromised
- Desktop and laptop Linux: display stack, GPU drivers, suspend, audio, Wi-Fi, power
- Not for shell scripting syntax (`bash`), container build and runtime internals (`docker`), cluster scheduling (`k8s`), cross-system backup strategy and retention policy (`backups` — this covers the host mechanics and the restore drill), or building an observability stack (`monitoring` — this covers what a single host should measure and record)

## Quick Reference

| Symptom | First move |
|---------|-----------|
| "Permission denied" though the mode bits look right | `namei -l <path>`; then ACL (`+` in `ls -l`), SELinux (`ls -Z`), mount options (`findmnt -T`) → `permissions.md` |
| Root itself gets "permission denied" | `lsattr` (immutable), `ls -Z` (SELinux), `getcap` — root is not omnipotent (rule 8) |
| Denied only when it runs as a service | Unit sandboxing: `systemd-analyze security <unit>`, then `ReadWritePaths=` → `systemd.md` |
| `df` says full, `du` cannot find it | `lsof +L1` for deleted-but-open files, then the bind-mount check → `disk-space.md` |
| "No space left on device" with free space in `df -h` | `df -i` for inodes; if it came from a file watcher it is the inotify limit → `kernel.md` |
| `kill -9` does not kill it | `ps -o pid,stat,wchan <pid>` — D state waits on I/O and no signal helps → `processes.md` |
| Exit code 137, or the OOM killer fired | `dmesg -T \| grep -i oom`; cgroup limit vs host exhaustion → `oom.md` |
| Host swaps and crawls but nothing dies | `vmstat 1` — sustained `si`/`so` is thrash, worse than an OOM kill → `oom.md` |
| Service starts by hand, fails at boot | Ordering (`network-online.target`) and environment (absolute paths) → `systemd.md` |
| Unit gives up: "start request repeated too quickly" | Start limit — add `RestartSec=`, then `systemctl reset-failed` → `systemd.md` |
| Job runs in your shell, fails under cron | Minimal PATH, no profile, `%` is special → `scheduling.md` |
| SSH key suddenly rejected, no error client-side | Perms 700/600 and a home that is not group-writable; `journalctl -u sshd -f` → `ssh.md` |
| About to change sshd, sudoers, firewall, or fstab remotely | Rule 4: second session, scheduled rollback, validator → `ssh.md` |
| Host does not boot, or drops to an emergency shell | Identify the stage first; usually fstab → `boot.md` |
| Port unreachable | `ss -tlnp` (bound to 127.0.0.1?), then the firewall front end, then the route → `networking.md` |
| `dig` resolves but the application cannot | Applications go through NSS, `dig` does not — `getent hosts` → `networking.md` |
| Large transfers hang, small requests fine | MTU black hole: `ping -M do -s 1472 <host>` → `networking.md` |
| Load average high, CPU mostly idle | I/O wait and D-state inflate load — a storage problem → `performance.md` |
| Latency spikes with the host CPU idle | cgroup CPU throttling: `cpu.stat` `nr_throttled` → `performance.md` |
| Upgrade broke or was interrupted | `dpkg --configure -a` / `dnf history undo`; never kill a running package transaction → `packages.md` |
| Old code still running after an upgrade | `needrestart` / `dnf needs-restarting -r`; kernel needs a reboot → `packages.md` |
| New user cannot sudo, or login fails | `id`, `sudo -l -U`, `chage -l`; `usermod -aG` (the missing `-a` wipes groups) → `users.md` |
| TLS, tokens, or replication fail with no config change | `timedatectl` — an unsynchronized clock breaks certificate and expiry checks → `scheduling.md` |
| Logs are missing, or gone after a reboot | Journal not persistent, or journald rate-limiting → `logs.md` |
| A command behaves differently than documented | Distribution differences: package, unit name, firewall, MAC → `distros.md` |
| Copy or sync duplicated a level, or deleted the wrong tree | rsync trailing slash; `--dry-run` before `--delete` → `files.md` |
| Host is internet-facing and unreviewed | Baseline in order: firewall, key-only SSH, auto security updates → `hardening.md` |
| Fresh host, nothing set up yet | First hour in order: identity, access, updates, journal, swap, inventory → `new-host.md` |
| Cloud host reverts hostname, users, or network config at reboot | cloud-init owns those files; the fix goes in its config → `new-host.md` |
| Backups exist but no restore was ever tried | A backup is a hypothesis until restored — drill it and time it → `backups.md` |
| "Is this number normal?" or "what should I alert on?" | Compare against the recorded baseline; alert on saturation, not utilization → `monitoring.md` |
| Suspected compromise: strange process, unknown key, crypto-mining CPU | Preserve evidence BEFORE cleaning; assume the tools on the box lie → `compromise.md` |
| Laptop or desktop: no display, suspend fails, no sound, Wi-Fi drops | Identify the stack first (Wayland vs X, PipeWire, driver) → `desktop.md` |
| Anything else | Core Rules below, then the file whose name matches the subsystem |

Depth on demand: `permissions.md` denial layers, ACLs, SELinux/AppArmor, capabilities · `processes.md` signals, D state, limits, /proc · `disk-space.md` full-disk triage and safe reclaim · `storage.md` devices, LVM, filesystems, fstab, RAID · `oom.md` OOM, swap, PSS, cgroup limits · `networking.md` reachability, DNS, firewalls, MTU, conntrack · `ssh.md` access, keys, lockout-proof changes · `systemd.md` units, ordering, drop-ins, sandboxing · `scheduling.md` cron, timers, locking, clock · `boot.md` boot failures, GRUB, rescue, chroot · `users.md` accounts, groups, sudo, PAM, offboarding · `packages.md` upgrades, holds, broken states, reboots · `performance.md` saturation triage, PSI, iostat, throttling · `logs.md` journalctl, rotation, retention · `kernel.md` sysctl, modules, dmesg, tunables · `hardening.md` exposed-host baseline · `new-host.md` provisioning and cloud-init · `backups.md` backup design and restore drills · `monitoring.md` baselines, alert thresholds, what to record · `compromise.md` suspected breach and recovery · `desktop.md` GPU, Wayland, suspend, audio, Wi-Fi · `distros.md` Debian/RHEL/Arch/Alpine/SUSE/WSL differences · `files.md` rsync, find, archives, atomic replace · `commands.md` incident toolkit.

## Core Rules

1. **Never `chmod 777`.** It destroys the audit trail and usually still fails, because the denial is a different layer: ACL mask, SELinux label, mount option, or unit sandboxing. Diagnose with `namei -l <path>` — it prints every component, and the first failing one is the bug. Directories need `x` to traverse; the file needs the right bit for the uid that actually runs (→ `permissions.md`).
2. **Signal ladder: SIGTERM → wait → SIGKILL only if ignored.** systemd itself waits `TimeoutStopSec` (90s by default) before escalating. `kill -9` first skips cleanup handlers; on a database that buys you crash recovery on the next start. Nothing at all works on a D-state task (→ `processes.md`).
3. **Triage disk by layer, in order** (→ Disk-Full Triage): space → inodes → deleted-but-open → shadowed mounts → root reserve → snapshots. Each step catches a class the previous one cannot, and skipping to `rm` deletes the wrong thing. Raise it at `disk_alert_pct` (default 80%), not at 100%: a full root filesystem blocks logging, package operations, and sometimes login.
4. **Remote-change safety, every time.** Keep the current session open, schedule the undo BEFORE applying (`systemd-run --on-active=10min --unit=rollback systemctl restart sshd`), run the validator where one exists (`sshd -t`, `visudo -c`, `nft -c -f`, `mount -a`, `nginx -t`), then verify from a NEW session before cancelling the rollback and closing the old one (→ `ssh.md`).
5. **Live change ≠ persistent change.** Pair every runtime command with its persistence mechanism: `sysctl -w` with a file in `/etc/sysctl.d/`, `iptables` with `iptables-save`, `firewall-cmd` with `--permanent`, `systemctl start` with `enable`. "Works now" is untested until it survives a reboot — and the reboot that tests it should be one you chose. The pair goes in `changes/<year>.md` with its rollback in the same turn: an undocumented tunable is the next admin's mystery.
6. **Capacity is relative, not absolute.** Alarm on `load1 / nproc` above `load_alarm_ratio` (default 1.0) sustained — load 8 on 4 cores is a ratio of 2.0, twice oversubscribed; load 8 on 16 cores is a half-idle host. Alarm on low `available` in `free`, never on low "free": cache is doing its job. Compare against this host's `baselines/<host>.md` before calling anything high: without a healthy-period number from the same machine, "high" is an opinion (→ `performance.md`, `oom.md`, `monitoring.md`).
7. **Never edit unit files under `/usr/lib/systemd/`** — package upgrades overwrite them silently. `systemctl edit <unit>` writes a drop-in under `/etc/` that survives and reloads for you; any hand edit needs `systemctl daemon-reload` or `restart` runs the old definition (→ `systemd.md`).
8. **Root is not omnipotent.** `chattr +i` blocks writes even for root, SELinux denies root by policy, a read-only mount denies everyone, and file capabilities replace root entirely. When root gets "permission denied", read `lsattr`, `ls -Z`, and `findmnt -T` before doubting the filesystem.
9. **Guard destructive paths against empty variables and wide matches.** `rm -rf "${DIR:?}/"` aborts when `DIR` is unset — `rm -rf $DIR/` with an unset variable expands to `rm -rf /`. Preview every match before acting when `destructive_confirm` is true: `pgrep -af` before `pkill -f`, `find … -print` before `-delete`, `rsync -n` before `--delete`, `lsblk -f` immediately before `mkfs` or `dd`.

## Signals And Exit Codes

Formula: an exit status above 128 means killed by signal `status − 128`. A process can also return those numbers itself, so confirm a real kill in `dmesg -T` or the journal before blaming the kernel.

| Status | Meaning | First move |
|---|---|---|
| 1 | Generic application error | Read the application log, not the OS |
| 126 | Found but not executable | `chmod +x`, a `noexec` mount, or a directory where a binary was expected |
| 127 | Command not found | PATH (cron and units get a minimal one), or a missing shared library — check `ldd` |
| 130 | SIGINT (128+2) | Ctrl-C, or a parent forwarding it |
| 137 | SIGKILL (128+9) | OOM killer first (`dmesg -T \| grep -i oom`), then a stop-timeout escalation |
| 139 | SIGSEGV (128+11) | Native crash — `coredumpctl`, and suspect a library or architecture mismatch |
| 141 | SIGPIPE (128+13) | The reader of a pipe exited first (`head` closing early is the usual cause) |
| 143 | SIGTERM (128+15) | Clean external stop — usually systemd stopping the unit, not a bug |
| 255 | Wrapper failure (ssh and some runtimes) | The transport failed; the remote command may never have run |

## Disk-Full Triage

Run in this order and stop at the first one that explains the gap. Detail and the safe reclaim order live in `disk-space.md`.

| # | Check | Catches |
|---|---|---|
| 1 | `df -hT` | Which filesystem is actually full — the error names a path, not a device |
| 2 | `df -i` | Inode exhaustion: "No space left on device" with free space showing |
| 3 | `lsof +L1` | Deleted files still held open — `rm` freed nothing |
| 4 | `mount --bind / /mnt && du -xh --max-depth=1 /mnt` | Files shadowed under a mount point, invisible to every `du` |
| 5 | `tune2fs -l <dev> \| grep -i 'reserved block'` | The ext4 5% root reserve — 50 GB on a 1 TB volume, "full" for users |
| 6 | `lvs -o +snap_percent`, `zfs list -t snapshot`, cloud snapshots | Deleted data kept alive by a snapshot |
| else | `du -xh --max-depth=1 / \| sort -h \| tail` | Ordinary growth — descend into the winner |

## Commands That Lie

| Tool | What it seems to say | What is true |
|---|---|---|
| `free` "free" column | Memory is nearly gone | Cache is reclaimable; only `available` answers "can I start something" |
| Load average | The CPU is overloaded | It counts D-state tasks too — high load with idle CPU is a storage incident |
| `top` %CPU | Above 100% is a bug | It is per-core: 400% = four cores saturated |
| `iostat` %util | The disk is maxed out | Meaningless on SSD/NVMe with parallel queues — judge by `await` and queue depth |
| `df` vs `du` | One of them is wrong | Both are right: deleted-but-open files or shadowed mounts explain the gap |
| `ps aux` %MEM | These workers use 40 GB | Shared pages are counted once per process — use PSS (`smaps_rollup`, `smem`) |
| `which` | This is what runs | It misses aliases, functions, and builtins — `type -a <cmd>` |
| `ping` | The service is up | It proves ICMP only — `nc -zv host port` or call the service |
| `dig` | The name resolves | Applications resolve through NSS, which `dig` bypasses — `getent hosts` |
| `df` on a thin volume | Half the disk is free | Thin-provisioned and overlay storage can exhaust underneath the filesystem |
| `du -sh *` | This is the directory total | It skips dotfiles — `du -sh .` |
| `uptime` 400 days | The host is reliable | It has never proven it can boot; reboot on a schedule you choose |

## Output Gates

Before running a destructive or remote-risky command — and, for the last two, before ending any session that changed or learned something:

- Variables in destructive paths expanded and echoed first — `rm -rf` targets use `"${VAR:?}"`?
- Fallback session open and a rollback scheduled before touching sshd, sudoers, firewall, fstab, or network config on a remote host?
- SIGTERM sent and waited before any `-9`?
- Persistence step included, or is this change gone at the next reboot?
- Blast radius previewed — `pgrep -af` before `pkill -f`, `find … -print` before `-delete`, `rsync -n` before `--delete`, `lsblk -f` before `mkfs`/`dd`?
- Command matches the host's `distro_family` — package manager, unit name, firewall front end, MAC system?
- Validator run where one exists (`sshd -t`, `visudo -c`, `mount -a`, `nft -c -f`, `systemd-analyze verify`)?
- Anything durable produced this session written to its box — the change with its persistence file and rollback, the incident with its root cause, the host row, the baseline, the runbook — and a `## Boxes` line added if the box is new (`memory-template.md`)?
- Nothing written under `~/Clawic/data/` that authenticates anything: keys, hashes, passphrases and `EnvironmentFile` values replaced by `<kind>:<locator>` pointers, including inside text the user pasted?

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/linux/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| distro_family | debian \| rhel \| arch \| alpine \| suse | debian | Selects package manager, unit names, config paths, firewall front end, and MAC system in every command emitted (→ `distros.md`) |
| init_system | systemd \| openrc \| sysvinit | systemd | Routes service and boot guidance; non-systemd hosts skip `systemd.md` and timers in favour of the distro's init and cron |
| firewall_tool | auto \| ufw \| firewalld \| nftables \| iptables | auto | Which syntax firewall examples use; `auto` derives it from `distro_family` (ufw on debian, firewalld on rhel) |
| privilege_mode | sudo \| root-shell | sudo | Whether emitted commands carry a `sudo` prefix and whether sudo-specific traps (secure_path, sudoers.d naming) are surfaced |
| disk_alert_pct | number (50-95) | 80 | Filesystem usage at which disk triage is raised proactively rather than on request (rule 3) |
| load_alarm_ratio | number (0.5-4) | 1.0 | `load1 / nproc` ratio treated as saturation in capacity judgements (rule 6, `performance.md`) |
| destructive_confirm | bool | true | Whether every destructive command is preceded by its preview or dry-run (rule 9, Output Gates) |
| reboot_policy | allowed \| maintenance-window \| never | maintenance-window | Whether a required reboot is proposed inline, deferred to a window, or reported as a standing requirement (`packages.md`, `kernel.md`) |
| backup_tool | restic \| borg \| rsync \| snapshots \| none | none | Which restore and verification commands `backups.md` emits; `none` means file-level examples use restic and volume-level examples use the platform's snapshot, stated as an assumption |

Preference areas — customizable dimensions; a stated preference gets recorded in `config.yaml` and applied:

- **Tooling**: editor, terminal multiplexer for long remote operations, monitoring stack, whether config management (Ansible, Puppet, Salt) owns `/etc` — affects whether fixes are proposed as commands or as managed configuration
- **Conventions**: where local units, scripts, and logs live; naming of hosts, volumes, and users — affects every path in examples
- **Platform**: cloud provider, bare metal, VM, WSL, container; architecture; filesystem in use; headless server vs desktop, and the display stack on a workstation — affects storage, boot, performance and `desktop.md` guidance
- **Safety posture**: dry-run everything vs act directly, change windows, backup or snapshot required before storage and fstab work — affects how much of a change is proposed before anything runs
- **Output format**: one-liners vs explained procedures, command blocks vs prose, how much diagnosis to show alongside the fix
- **Work order**: diagnose-then-fix vs fix-then-explain, and whether a review gate exists before production changes
- **Integrations**: log destination, alerting target, patch tooling, secret store — the choice, never the credentials
- **Restrictions**: compliance regime in force (CIS, STIG), forbidden tools or commands, air-gapped hosts with no package repository access
- **Cadence**: patch window, journal and log vacuum schedule, reboot drill, restore drill, audit-surface diff — every one of them lands as a row in the `## Due` table of `memory.md`

## Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| `sudo echo x > /etc/file` | The redirect runs in YOUR shell before sudo starts | `echo x \| sudo tee /etc/file` |
| Editing sudoers or fstab bare | One typo = no sudo at all, or an unbootable host | `visudo`; edit fstab then `mount -a` to test before rebooting |
| Fixing web permissions with `chmod -R 777` | Masks the real cause (ACL mask, SELinux, wrong owner) and makes every file writable by any local process | Diagnose: `namei -l`, `getfacl`, `ls -Z` |
| Testing a cron job in your login shell | Your shell has PATH and environment that cron lacks — it proves nothing | `env -i /bin/sh -c 'cmd'` |
| Restarting a unit you edited by hand without `daemon-reload` | systemd runs the cached definition; you debug a file the system is not using | `systemctl daemon-reload`, or use `systemctl edit` |
| `usermod -G docker alice` | Without `-a` it REPLACES every supplementary group, including sudo | `usermod -aG`, and diff `id alice` before and after |
| `passwd -l alice` as offboarding | Locks the password only; her SSH key still logs in | `usermod --expiredate 1`, then remove her authorized_keys |
| `iptables -F` to "start clean" on a remote host | With a DROP default policy you flush your own access | Set policies to ACCEPT first, or schedule a rollback (rule 4) |
| `setenforce 0` to fix a denial | Hides the label bug and comes back at reboot | `restorecon`, a boolean, or `semanage fcontext` (→ `permissions.md`) |
| Killing a stuck `dpkg`/`dnf` to release the lock | Leaves packages half-configured — minutes of waiting become hours of repair | Find the holder with `fuser -v /var/lib/dpkg/lock-frontend` and wait |
| Storing state in `/tmp` | Cleared at reboot, and often tmpfs, so it consumes RAM | `/var/tmp` for temp data that must survive a reboot |
| `dd` or `mkfs` on a device name from memory | `sda` vs `sdb` is one keystroke, and device names reorder across boots | `lsblk -f` immediately before; address disks by UUID or `/dev/disk/by-id` |
| Counting a snapshot as a backup | It lives on the same storage as the origin, and an LVM snapshot invalidates itself the moment its allocated space fills | Layer it: snapshot for the five-minute mistake, an offsite copy for the disaster, and a timed restore drill (→ `backups.md`) |
| Editing the hostname or `/etc/netplan/50-cloud-init.yaml` on a cloud image | cloud-init rewrites those files at boot; the change reverts and nothing explains why | Set it in cloud-init's config or disable that module (→ `new-host.md`) |
| Cleaning a compromised host instead of rebuilding it | Removing the malware leaves the access, and the tools you checked with are the ones an attacker replaces first | Preserve evidence, contain at the network layer, rebuild from a known-good image, rotate everything the host could read (→ `compromise.md`) |
| Alerting on CPU utilization | A batch host at 100% is working correctly; a latency-sensitive service at 30% can already be failing | Alert on saturation (PSI, queue depth, `load1/nproc`) and on symptoms, always with a duration (→ `monitoring.md`) |

## Where Experts Disagree

- **Swap on servers.** One camp runs swapless so failures are fast and obvious; the other keeps a few gigabytes so cold pages leave RAM before the OOM killer picks a victim. The boundary is the workload's tolerance for slow degradation: latency-critical services prefer a clean kill, batch and memory-spiky workloads prefer the valve. Both camps agree that sizing swap to match RAM on a server buys nothing.
- **SELinux enforcing vs disabled.** "Disable it, it breaks everything" is a real position with a real cost: it removes the only layer that contains a compromised service. The workable middle is enforcing plus the discipline to fix labels and booleans rather than reaching for `setenforce 0` — and permissive mode while learning a new application, never as a destination.
- **Host firewall when there is a cloud security group.** Redundant to some, defence in depth to others. Deciding factor: whether anything on the host can publish a port without touching the security group (container runtimes do exactly that). Where that is possible, run both.
- **Configuration management vs hand edits.** Managed hosts get consistency and lose the ability to fix one box quickly; hand-managed hosts get speed and drift. The rule that satisfies both: any change you would be unhappy to lose at the next converge belongs in the managed configuration, and the incident fix is followed by that commit.

## Related Skills

More Clawic skills, get them at https://clawic.com/skills/linux (install if the user confirms):
- `bash` — shell scripting syntax and safety, beyond OS behavior
- `docker` — container builds, images, and runtime debugging
- `vps` — provisioning and securing rented servers end to end
- `backups` — backup strategy, retention and offsite policy across systems
- `monitoring` — building the observability stack: metrics, dashboards, alert routing

## Feedback

- If useful, star it: https://clawic.com/skills/linux
- Latest version: https://clawic.com/skills/linux

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/linux.
