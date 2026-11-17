# Disk Space — When The Disk Says Full And Nothing Adds Up

The triage ladder (space → inodes → deleted-open → shadowed → reserve → snapshots) lives in `SKILL.md`. This file is what to do at each rung, plus the reclaim work that is safe to run on a live host.

## Finding The Space

```bash
df -hT                                   # per filesystem, with type — start here, note WHICH fs is full
du -xh --max-depth=1 / 2>/dev/null | sort -h | tail   # -x stays on one filesystem
du -xh --max-depth=1 /var | sort -h | tail            # then descend into the winner
find / -xdev -type f -size +500M -printf '%s\t%p\n' 2>/dev/null | sort -n | tail
ncdu -x /var                             # interactive, if installed
```

- `-x`/`-xdev` is what makes the sweep meaningful: without it you descend into network mounts and other volumes and blame the wrong disk.
- `du -sh *` skips dotfiles; `du -sh .` gives the true directory total.
- `du` counts allocated blocks, `ls -l` reports apparent size. Sparse files diverge wildly — compare with `du --apparent-size -sh`.
- Directories that are large because of file COUNT, not size, show up as slow `du` and normal totals — that is the inode case below.

## Inodes

- `df -i` reports them. Exhaustion looks exactly like a full disk ("No space left on device") while `df -h` shows free space.
- Usual sources: mail queues, PHP/session files, per-request temp files, `node_modules` trees, unrotated per-minute logs.
- Locate the offender by count, not size: `find /var -xdev -type d -printf '%h\n' | sort | uniq -c | sort -n | tail`.
- ext4 fixes the inode count at `mkfs` time — you cannot add inodes to a live ext4 filesystem; you reformat with `mkfs.ext4 -i 8192` or move the workload. XFS allocates inodes dynamically, so this class of failure is mostly an ext4 story.

## Deleted But Open

- `lsof +L1` lists files with zero links still held open — the classic "I deleted the log and nothing was freed".
- Free it without a restart: `: > /proc/<pid>/fd/<n>` truncates through the descriptor. For a file you can still name, `: > /var/log/app.log` truncates in place.
- Truncation is safe for append-mode writers (every normal logger). A writer that keeps its own offset resumes at byte 4 GB and leaves a sparse file — restart that process instead.
- If `lsof` is not installed: `find /proc/*/fd -ls 2>/dev/null | grep '(deleted)'`.

## Shadowed Mounts

Files written to a directory BEFORE a filesystem was mounted over it stay on the underlying volume, invisible to every `du` you run afterwards:

```bash
mount --bind / /mnt/root && du -xh --max-depth=2 /mnt/root | sort -h | tail && umount /mnt/root
```

Signature: `df` on `/` reports 40 GB used, `du -x /` totals 12 GB, and the gap never resolves. Check `/var/log`, `/data`, and any path a mount unit owns.

## The Reserve

- ext4 reserves 5% of the volume for root by default — 50 GB on a 1 TB disk, which users experience as "full" while `df` still shows space.
- `tune2fs -m 1 /dev/sdb1` on data volumes recovers most of it (no unmount needed). Keep the 5% on the root filesystem: it is what lets root log in and clean up after users fill the disk.
- Read the current value: `tune2fs -l /dev/sdb1 | grep -i 'reserved block'`.

## Snapshots And Other Invisible Holders

- LVM, ZFS, btrfs, and cloud volume snapshots keep deleted data alive. `lvs -o +snap_percent`, `zfs list -t snapshot -o name,used -s used`, `btrfs subvolume list /`.
- A btrfs filesystem can report ENOSPC with free space in `df` — metadata chunks are exhausted; `btrfs filesystem usage /` is the honest view and `btrfs balance start -dusage=50 /` reclaims.
- Thin-provisioned or overlay-backed volumes can run out UNDER a filesystem that looks half empty; the errors surface as I/O errors, not ENOSPC (→ `storage.md`).
- A container runtime's data directory is a frequent hidden consumer on shared hosts — the `docker` skill owns the prune matrix.

## Reclaim, In Safe Order

1. **Journal**: `journalctl --disk-usage` then `journalctl --vacuum-size=500M` (or `--vacuum-time=7d`). Instant, no restart, and it is the single most common win on systemd hosts (→ `logs.md`).
2. **Rotated logs**: delete `*.gz`/`*.1` older than your retention; then fix the rotation policy that let them accumulate rather than repeating the cleanup.
3. **Package caches**: `apt-get clean` (Debian) or `dnf clean all` (RHEL); `/var/cache/*` generally.
4. **Old kernels** — a frequent `/boot` filler: `apt autoremove --purge` on Debian, `dnf remove --oldinstallonly` on RHEL. `/boot` full also blocks the next kernel upgrade mid-transaction (→ `packages.md`).
5. **Crash dumps and cores**: `/var/crash`, `/var/lib/systemd/coredump`, `coredumpctl` retention.
6. **Temp**: `/tmp` clears at reboot (often tmpfs, so it eats RAM instead — → `oom.md`); `/var/tmp` survives reboots and is the one that quietly grows for years.
7. **User caches on build hosts**: `~/.cache`, language package caches, container build caches. Big, safe, and back the next day — schedule instead of doing it by hand.

Everything above is reversible. Anything that deletes application data goes through the owner of that data, not through a disk-space incident.

## Do Not Wait For 100%

- Alarm at `disk_alert_pct` (default 80%) on every filesystem, not just `/`. A root filesystem at 100% blocks logging, breaks `sudo` on some configurations, prevents package operations, and can leave a database read-only — the incident starts before the disk is actually full.
- Watch the derivative, not the level: a 60% filesystem growing 5 points a day is a worse alert than a stable 85%.
- Free space that fluctuates by gigabytes every few minutes is usually a job writing and deleting temp files; catch it with `lsof +L1` during the dip, not after.

## Not Actually Disk

- `ENOSPC` from a file-watching tool (editors, hot reloaders, log shippers) is the inotify watch limit, not the disk: `sysctl fs.inotify.max_user_watches` (→ `kernel.md`).
- "Read-only file system" after a burst of I/O errors means the kernel remounted it read-only to protect data — check `dmesg -T` and the device's SMART data before clearing space (→ `storage.md`).
- A full `/boot` (a separate, small partition on most Debian/Ubuntu installs) fails upgrades while `/` has hundreds of free gigabytes. Always read the `df` line for the specific mount point named in the error.

## Record It

A disk that filled once will fill again: write the incident (host, what consumed the space, what reclaimed it, time to resolve) to `~/Clawic/data/linux/incidents/<year>.md`, and the second time the same cause appears, promote it to `## Recurring Incidents` in `memory.md` with the fix that holds. Any retention or reserve change (`journalctl --vacuum-*` policy, logrotate rule, `tune2fs -m`) goes to `changes/<year>.md`, and a cleanup that has to repeat goes to `## Due` rather than into someone's memory (`memory-template.md`).

Related: block devices, LVM, resizing → `storage.md` · journald and rotation policy → `logs.md` · package caches and kernels → `packages.md` · alerting before it fills → `monitoring.md`.
