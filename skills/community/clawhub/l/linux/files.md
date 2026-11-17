# Files At Scale — Copying, Syncing, Finding, Archiving

The operations that destroy data are boring ones: a trailing slash, a `--delete` against the wrong target, a `find -delete` whose pattern was broader than it looked. Every rule here has a dry-run in front of it.

## rsync

**The trailing slash is the whole interface.** `src/` means "the CONTENTS of src"; `src` means "the directory src itself":

```bash
rsync -a /data/app/  /backup/app/     # /backup/app/file      ← usually what you want
rsync -a /data/app   /backup/app/     # /backup/app/app/file  ← the classic duplicated level
```

- Always `-n` (`--dry-run`) first when `--delete` is involved, and read the output rather than the exit code. `--delete` plus a mistyped source that resolves to an empty directory erases the destination.
- Flags worth knowing: `-a` (archive: recursive, symlinks, perms, times, group, owner) but **not** hardlinks (`-H`), ACLs (`-A`), or xattrs (`-X`) — add them explicitly when the tree relies on them (file capabilities live in xattrs, → `permissions.md`).
- `--partial --append-verify` resumes a large interrupted transfer; `--bwlimit=50m` keeps a sync from saturating the link; `--info=progress2` gives a real overall progress line.
- `-z` compresses in transit — a win on slow links, wasted CPU on a LAN, and counterproductive on already-compressed data.
- `--checksum` compares content instead of size+mtime: correct when timestamps are unreliable, expensive because it reads both sides in full.
- Over a jump host: `rsync -e 'ssh -J bastion' -a src/ host:/dst/` (→ `ssh.md`).
- Preserving ownership requires root on the receiving side; without it everything lands owned by the transfer user and "the permissions are wrong after restore" follows.

## find

```bash
find /var/log -xdev -type f -name '*.log' -mtime +30 -print      # LOOK first
find /var/log -xdev -type f -name '*.log' -mtime +30 -delete     # then act
find /data -type f -print0 | xargs -0 -P4 -n100 sha256sum        # safe with spaces, parallel
find /srv -xdev -newermt '2026-07-01' -type f                    # changed since a date
```

- `-print` before `-delete`, every time. `-delete` is applied depth-first as `find` walks; there is no confirmation and no undo.
- `-xdev` keeps the walk on one filesystem — without it a sweep of `/` descends into network mounts and other volumes.
- `-mtime +30` means "more than 30 full 24-hour periods ago", i.e. 31 days and older, because the fractional part is truncated. `-newermt '30 days ago'` expresses date thresholds without that trap.
- Order matters: `find . -name '*.tmp' -type f` tests the name first; putting cheap tests before expensive ones (`-size`, `-newer`) matters on trees with millions of entries.
- `-exec cmd {} +` batches arguments like `xargs` and is far faster than `-exec cmd {} \;`, which forks once per file.
- Filenames can contain spaces and newlines: `-print0 | xargs -0` or `-exec … +`. Parsing `ls` output is the bug this prevents.

## Copying

- `cp -a` = `-dR --preserve=all`: recursive, keeps symlinks, permissions, timestamps, and (as root) ownership. `cp -r` alone loses times and modes, which is how a restored tree gets the wrong mtimes.
- `cp` does not preserve xattrs or ACLs by default (`--preserve=xattr,mode`), and never preserves file capabilities.
- `install -D -m 0640 -o app -g app src /etc/app/config` sets mode and ownership in the same operation and creates the parent directory — better than `cp` followed by `chmod`/`chown`, because there is no window where the file exists with the wrong mode.
- Sparse files: `cp --sparse=always` avoids materializing gigabytes of zeros; a naive copy of a sparse image can fill the destination (→ `disk-space.md`).
- Big local copies should yield to production I/O: `ionice -c3 nice -n19 rsync -a …` (→ `performance.md`).

## Atomic Replacement

- `mv` within the SAME filesystem is an atomic rename: readers see either the old file or the new one, never a partial write.
- Across filesystems, `mv` degrades to copy-then-delete, which is not atomic and loses hardlinks. Write the temp file INTO the destination directory (`/etc/app/.config.tmp`), then rename.
- Ordering for durability: write, `fsync` the file, rename, then `fsync` the directory. Skipping the directory sync can lose the rename on a power cut (→ `storage.md`).
- Never edit a config in place on a live system without a backup copy you can restore in one command. `cp config config.bak.$(date +%F)` costs nothing.

## Archives

- `tar -czf out.tgz -C /src .` — `-C` changes directory so the archive contains relative paths, not `/src/...`. Absolute paths in an archive are a restore hazard.
- **`tar -tzf out.tgz | head` before extracting anything you did not create**: an archive can contain absolute paths or `../` and write outside the target directory.
- `--strip-components=1` drops the wrapping top-level directory that most release tarballs add.
- Ownership on extract: only root restores original ownership; otherwise files land owned by the extracting user (`--same-owner` is the default for root, `--no-same-owner` to force otherwise). Add `--xattrs --acls` when the tree relies on them.
- `zstd` (`tar --zstd`) compresses faster and decompresses much faster than gzip at similar ratios; gzip remains the compatibility default.

## Integrity And Deletion

- Verify what you moved: `sha256sum -c manifest.txt` (generate with `find … -exec sha256sum {} +`). Size comparison alone does not catch silent corruption.
- A copy you have never restored is a hypothesis. Restore a sample into a scratch directory, check ownership, permissions, and that the application actually opens it — the failures that matter (missing xattrs, wrong UIDs, a truncated archive) are invisible until then.
- `shred` assumes overwriting in place actually replaces the data — false on SSDs (wear levelling), on copy-on-write filesystems (btrfs, ZFS), and on any snapshotted volume. Real erasure is full-disk encryption plus discarding the key, or the device's secure-erase command.
- Deleting a file with a process holding it open frees nothing (→ `disk-space.md`).
- Guard every scripted deletion against an empty variable: `rm -rf "${DIR:?}/"` aborts if `DIR` is unset or empty (→ `SKILL.md` rule 9).

## Large Directories And Watches

- A directory with hundreds of thousands of entries makes `ls` slow because it sorts; `ls -U` or `find . -maxdepth 1 -printf '.'` avoids the sort. The real fix is sharding into subdirectories.
- Deleting millions of small files is I/O-bound, not CPU-bound: `find … -delete` under `ionice -c3`, or recreate the parent directory and remove the old one if the whole tree goes.
- Sync tools and editors that watch trees hit the inotify watch limit and fail with ENOSPC — a kernel limit, not a disk problem (→ `kernel.md`).

## Record It

A migration or sync procedure that worked — the exact rsync flag set for a tree that relies on hardlinks, ACLs or capabilities, the order of steps, the verification command — goes to `~/Clawic/data/linux/artifacts/procedure-<what>.md` with its `## Boxes` line in `memory.md`. It is the kind of thing that is rebuilt from scratch, slightly wrong, every time it is needed (`memory-template.md`).

Related: filesystem behaviour and durability → `storage.md` · reclaiming space → `disk-space.md` · transfer over SSH → `ssh.md` · restoring what you copied → `backups.md`.
