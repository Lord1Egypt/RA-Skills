# Backups On A Host — Designed Backwards From The Restore

A backup is a hypothesis until a restore proves it. Design from the restore: what has to be running again, how fast, and who does it at 3am. Read `## Hosts` in `~/Clawic/data/linux/memory.md` for this host's backup target and the date its last restore was verified before touching anything; read `## Due` to see whether the drill is overdue. Commands follow `backup_tool` (default: restic for file-level, the platform's snapshot for volume-level, stated as an assumption).

Scope here is the host mechanics and the drill. Cross-system retention policy, offsite strategy and compliance retention belong to the `backups` skill.

## The Four Numbers Before Any Tool

| Number | Question it answers | Where it bites |
|---|---|---|
| RPO | How much data may be lost | A nightly job means up to 24h lost; a database needs WAL/binlog shipping, not a nightly dump |
| RTO | How long a restore may take | Measured, never estimated — see the drill below |
| Restore bandwidth | How long the bytes take to arrive | 500 GB over a 100 Mbit link is ~11 hours of pure transfer (`500×8 ÷ 0.1 Gbit/s`) before anything is usable |
| Retention | How far back a mistake can be undone | Ransomware and a bad migration are both discovered days later; 7 daily copies of a corrupted file is one corrupted file |

If RTO is hours and the data is hundreds of gigabytes offsite, the plan is wrong regardless of how good the backup is — that is a local snapshot plus an offsite copy, not one tier.

## Snapshot Is Not Backup

- An LVM, ZFS, btrfs or cloud volume snapshot lives on (or next to) the same storage as the origin. It survives `rm -rf` and a bad upgrade; it does not survive the volume, the array, the account, or the region (→ `storage.md`).
- LVM snapshots additionally **fill up and get dropped** when their allocated space runs out, silently invalidating themselves. Size for the write volume during their lifetime and delete them when done.
- RAID is not backup either: it replicates the `DROP TABLE` in real time.
- The useful shape is layered: snapshot for the five-minute mistake, an on-host or LAN copy for speed, an offsite copy for the disaster, and one copy the host cannot delete.

## Consistency: Copying A Running System Copies A Torn State

- **A file-level copy of a live database is corrupt more often than not.** Use the engine's own path: `pg_dump`/`pg_basebackup` + WAL archiving, `mysqldump --single-transaction` (InnoDB only) or Percona XtraBackup, `sqlite3 .backup`, `redis-cli --rdb`, `etcdctl snapshot save`.
- Application state that spans files (a mail spool, a git server, an index) needs the application stopped or quiesced, or a snapshot taken with `fsfreeze -f /data` … `fsfreeze -u /data` around it (seconds, and every write blocks meanwhile).
- Filesystem snapshots are crash-consistent, which is what a well-behaved database recovers from. "Crash-consistent" is a promise about journal replay, not about an application that writes two files and expects both.
- `rsync` of a tree that changes during the copy produces a mix of two points in time. Snapshot first, then copy the snapshot.

## What Actually Needs Backing Up

- **Data the host produced**: databases, uploads, mail, git repositories, container volumes.
- **The configuration that makes it a server**: `/etc`, unit drop-ins, crontabs and timers, package selections (`dpkg --get-selections`, `dnf repoquery --userinstalled`), firewall rules, the LUKS header (`cryptsetup luksHeaderBackup` — a corrupted header is unrecoverable even with the passphrase).
- **The metadata a restore needs**: partition table (`sfdisk -d`), fstab with UUIDs, LVM layout (`vgcfgbackup`), and which packages a bare-metal rebuild requires. Config management replaces most of this — if and only if the repo itself is backed up somewhere else.
- Not the OS tree. Reinstalling a distribution is minutes; hunting a subtle inconsistency in a restored `/usr` is a day.
- Credentials are NOT backed up into `~/Clawic/data/` in any form. What goes in the host's row in `## Hosts` is the pointer to where they live (`vault:`, `keychain:`, `1password:`); the secret store is backed up on its own terms.

## Repository Mechanics (restic, borg, and rsync trees)

- Deduplicating tools (restic, borg) store one copy of repeated blocks: the second daily backup of a 200 GB tree that changed 2 GB costs about 2 GB. That is what makes daily retention affordable.
- **Pruning is the dangerous operation**: `forget` marks, `prune` deletes. Run `forget --dry-run` with the exact keep policy first, and keep policies expressed as `--keep-daily 7 --keep-weekly 4 --keep-monthly 6` rather than a raw count.
- **Verify, do not trust the exit code**: `restic check --read-data-subset=5%` (or `borg check --verify-data` periodically) reads real blocks. A repository that lists snapshots fine can still have unreadable data.
- **Append-only credentials are the ransomware answer.** A host that can delete its own backups will, once compromised. restic's `--append-only` server mode, borg's `append-only` repo flag, S3 object lock, or a pull-based model where the backup server reaches in — never the other way.
- A stale lock after a killed job blocks the next run (`restic unlock`, `borg break-lock`) — check it before assuming the repository is broken.
- **The encryption key or passphrase is not stored on the host it protects.** Losing it loses every backup; leaving it on the machine hands both to the same attacker. Store it in the user's secret manager and reference it as a pointer.
- Plain-rsync snapshot trees still work: `rsync -a --delete --link-dest=../previous src/ 2026-07-26/` gives hardlinked, browsable, per-day trees at the cost of one copy plus changes. No dedup within a file, no encryption, and a restore is just `cp` — which is exactly why some people keep it.

## The Restore Drill (the only thing that proves any of this)

Quarterly, timed, into scratch — never into production:

1. Pick a real target: last night's snapshot of the actual data set, not a test file you planted.
2. Restore to a scratch host, VM, or directory. `restic restore latest --target /scratch --include /var/lib/app`.
3. Start the application against it and check that it opens, authenticates, and shows recent data — not that the files exist.
4. **Time it end to end** and note what was missing. What breaks is never the bytes: it is the UIDs (`--numeric-owner` on tar, root on the rsync receiver), the xattrs and file capabilities (`-A -X` on rsync, `--xattrs --acls` on tar), SELinux labels (`restorecon -R`), the fstab UUIDs, the LUKS header, the bootloader, and the one credential nobody wrote down (→ `files.md`, `permissions.md`).
5. Write the measured RTO and every gap where Record It below says they go, then fix the gaps before the next drill.

Bare-metal restore adds bootloader and identity: partition, restore, fix fstab UUIDs, `grub-install` from a chroot, regenerate initramfs, then handle the machine-id and host keys (→ `boot.md`, `new-host.md`).

## Making Failure Loud

- Alert on the ABSENCE of a success, not on failure: a job that dies before it can report an error reports nothing. Have the job write a heartbeat (a timestamp file, a monitoring ping) only on success, and alert when the heartbeat ages past one interval plus a margin (→ `monitoring.md`, `scheduling.md`).
- Log the size and duration of every run; a backup that suddenly takes 10% of its usual time backed up 10% of the data.
- Put the job in a systemd timer with `Persistent=true` so a host that was down at 03:00 still runs it, and `OnFailure=` so a failed unit becomes an alert with no extra tooling (→ `scheduling.md`).
- `flock` the job: a slow night must not start a second copy against the same repository.

## Record It

After designing or changing backups, write the target and retention into the host's row in `## Hosts` (`memory.md`), and put the restore drill in `## Due` with its cadence. After a drill, update `## Due` with the run date and write the measured RTO plus what was missing into `incidents/<year>.md` if it failed, or into the host row (`verified <date>`) if it passed. A restore procedure worth repeating goes to `artifacts/runbook-restore-<host>.md` with its `## Boxes` line — pointers instead of passphrases. Formats: `memory-template.md`.

Related: snapshots and volumes → `storage.md` · copying, xattrs and archives → `files.md` · timers and locking → `scheduling.md` · rebuild after a breach → `compromise.md` · booting the restored host → `boot.md`.
