# Kernel — sysctl, Modules, dmesg, and Tuning That Survives

Three rules govern everything here: a runtime change is gone at reboot unless written to a file; a tunable you cannot explain is a liability; and the kernel already told you what happened — in `dmesg`.

## sysctl

```bash
sysctl net.ipv4.ip_forward              # read one
sysctl -a | grep -i somaxconn           # search
sysctl -w vm.swappiness=10              # runtime only — gone at reboot
echo 'vm.swappiness = 10' > /etc/sysctl.d/90-tuning.conf   # persistent
sysctl --system                          # reload every file, printing what applied
```

- Files in `/etc/sysctl.d/` are applied in lexical order, so `99-*.conf` wins over `10-*.conf`; on many distros `/etc/sysctl.conf` is read as part of the same set. When a setting refuses to stick, `grep -r <key> /etc/sysctl.d /etc/sysctl.conf /usr/lib/sysctl.d` finds the file that overrides yours.
- Settings applied before their subsystem exists silently fail: a `net.ipv4.conf.eth0.*` key written for an interface that appears later needs a network hook, not sysctl.d.
- Pair every `sysctl -w` you make during an incident with the file that persists it, in the same change (→ `SKILL.md` rule 5).
- Verify after reboot, once, for anything load-bearing. A tunable that only exists in one incident's shell history is a future outage.

## The Tunables Worth Knowing

| Key | Default | When to change it |
|---|---|---|
| `vm.swappiness` | 60 | 1-10 for databases and latency-sensitive services (→ `oom.md`) |
| `vm.overcommit_memory` | 0 | 1 for fork-heavy processes that reserve large address spaces; 2 only with a calculated ratio (→ `oom.md`) |
| `vm.dirty_background_ratio` / `vm.dirty_ratio` | 10 / 20 | Lower both on hosts where large write bursts cause multi-second stalls |
| `fs.inotify.max_user_watches` | distro-dependent, often 8192-65536 | Raise for editors, hot reloaders, and log shippers — the ENOSPC that is not a disk problem |
| `fs.file-max` | Sized from RAM | Rarely; the per-process limit is what you hit first (→ `processes.md`) |
| `net.core.somaxconn` | 4096 on current kernels | Raise only if the app also requests a larger listen backlog (→ `networking.md`) |
| `net.ipv4.tcp_tw_reuse` | 2 (loopback only) | 1 for outbound-heavy clients hitting ephemeral-port limits |
| `net.netfilter.nf_conntrack_max` | Sized from RAM | Raise when `nf_conntrack_count` approaches it — the alternative is silent packet drops |
| `kernel.panic` / `kernel.panic_on_oops` | 0 | Set to a number of seconds so a panicked host reboots instead of sitting dead |
| else | — | Do not copy tuning blogs wholesale; each key needs a measured reason (→ `performance.md`) |

## Transparent Huge Pages

- Enabled (`always`) by default on most distros. Databases with many small random accesses — Redis, MongoDB, PostgreSQL under some workloads, several JVM setups — document latency spikes from THP compaction and recommend `madvise` or `never`.
- Read the state: `cat /sys/kernel/mm/transparent_hugepage/enabled`. Change at runtime: `echo never > /sys/kernel/mm/transparent_hugepage/enabled`. Persist via the kernel command line (`transparent_hugepage=never`) or a `oneshot` unit that runs before the database — a sysctl file cannot set it.
- Change it because the vendor documents it for your workload, not preventively.

## Modules

```bash
lsmod                                    # loaded modules and their users
modinfo <mod>                            # parameters, dependencies, signature
modprobe <mod>                           # load with dependencies
modprobe -r <mod>                        # unload (fails while in use)
cat /sys/module/<mod>/parameters/<param> # the value actually in effect
```

- Parameters persist in `/etc/modprobe.d/<name>.conf` as `options <mod> param=value`; the loaded value only changes on reload.
- Blacklisting: `blacklist <mod>` in `/etc/modprobe.d/` prevents automatic loading, but **a module already in the initramfs still loads at boot** — regenerate afterwards (`update-initramfs -u` on Debian, `dracut -f` on RHEL) or the blacklist appears ignored (→ `boot.md`).
- Load at boot deliberately with a file in `/etc/modules-load.d/`.
- Out-of-tree modules (NVIDIA, VirtualBox, ZFS) are rebuilt per kernel by DKMS. A kernel upgrade that outruns DKMS leaves the module missing after reboot — check `dkms status` before rebooting a host that depends on one.
- Secure Boot rejects unsigned modules; the symptom is "Required key not available" and the fix is enrolling a MOK, not disabling the module.

## dmesg And The Ring Buffer

- `dmesg -T` for human timestamps, `dmesg -w` to follow, `journalctl -k -b` for the journal's copy with reliable timestamps.
- What only the kernel log tells you: OOM kills (→ `oom.md`), I/O errors and device resets (→ `storage.md`), conntrack table exhaustion and interface flaps (→ `networking.md`), segfaults with the faulting address, filesystem remounts to read-only, and hardware corrected/uncorrected errors.
- The buffer is finite and wraps; on a chatty host the message you want may already be gone unless the journal persisted it (→ `logs.md`).
- Taint flags: `cat /proc/sys/kernel/tainted` non-zero means proprietary modules, a forced module load, or a previous oops. Non-zero taint is context for a bug report, not a fault by itself.

## Kernel Command Line

- Current: `cat /proc/cmdline`. Persistent: `GRUB_CMDLINE_LINUX` in `/etc/default/grub`, then `update-grub` / `grub2-mkconfig` (→ `boot.md`).
- Parameters that belong there rather than in sysctl: `transparent_hugepage=`, `elevator=`/`scsi_mod.use_blk_mq`, `intel_iommu=on`, `isolcpus=`, `nomodeset`, `systemd.unit=`.
- Test a risky parameter as a one-time GRUB edit before committing it to the config — a bad line in `/etc/default/grub` makes every boot fail identically.

## Versions And Upgrades

- `uname -r` is the RUNNING kernel; the newest installed one only takes effect after a reboot (→ `packages.md`).
- Keep the previous kernel installed. The most common recovery from a bad kernel is choosing the older entry in the GRUB menu, and that entry has to exist.
- Vendor-specific tuning guides (database, storage, network appliance) are the legitimate source for kernel settings. Apply them as a documented set with a rollback file, not as accumulated one-liners.

## Record It

Before reading this file's tables, check `artifacts/` for an existing tuning set for this host — re-deriving one is how two contradictory sysctl files end up in `/etc/sysctl.d/`. After applying: a single tunable goes to `~/Clawic/data/linux/changes/<year>.md` (key, value, persistence file, rollback, why); a coherent SET of them goes to `artifacts/tuning-<host>-<workload>.md` with the measurement that justified it and the exact rollback, plus its `## Boxes` line in `memory.md`. A tunable that exists only in one incident's shell history is a future outage (`memory-template.md`).

Related: memory tunables in context → `oom.md` · network limits → `networking.md` · boot parameters and initramfs → `boot.md` · measuring before and after → `performance.md`.
