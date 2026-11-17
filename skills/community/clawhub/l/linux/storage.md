# Storage — Devices, Filesystems, LVM, and Mounts That Survive A Reboot

Order of work for anything involving a block device: identify → back up or snapshot → change → verify → persist. Skipping "identify" is how `sdb` becomes `sda`.

## Identify First, Always

```bash
lsblk -f                      # tree of devices, filesystems, UUIDs, mount points — the single best view
blkid                         # UUID/TYPE per device
findmnt -A                    # what is mounted where, with options and source
ls -l /dev/disk/by-id/        # stable names: model+serial, immune to boot-order reordering
```

Device names (`/dev/sda`, `/dev/nvme0n1`) are assigned in discovery order and **reorder across reboots and hotplug**. Every persistent reference — fstab, scripts, `mkfs`, `dd` — uses `UUID=` or `/dev/disk/by-id/`. The one keystroke between `sda` and `sdb` is the most expensive typo in this domain.

## Partitions

- GPT for anything over 2 TiB or booting UEFI; MBR only for legacy BIOS compatibility. `parted -s /dev/sdb mklabel gpt`.
- `sgdisk`/`parted` for scripted work, `fdisk` interactively. After changing a table on a disk with mounted partitions: `partprobe /dev/sdb` or `partx -u /dev/sdb` — otherwise the kernel keeps the old map and your new partition does not exist yet.
- Cloud volume grown in the console? The disk is bigger, the partition is not: `growpart /dev/nvme0n1 1`, then grow the filesystem (below). Two steps, and forgetting the first makes the second a no-op.
- Alignment matters on SSD/NVMe; modern tools default to 1 MiB alignment — do not hand-craft sector offsets.

## Filesystems: Choose, Grow, Never Assume Shrink

| Filesystem | Grow | Shrink | Use it for |
|---|---|---|---|
| ext4 | `resize2fs` online | Yes, but **offline only** (unmount + `resize2fs` smaller, then shrink the LV) | Default, boring, well understood |
| XFS | `xfs_growfs` online | **Never** — no shrink support exists | Large volumes, parallel I/O, RHEL default |
| btrfs | `btrfs filesystem resize` online | Online | Snapshots and checksums when you want them in the filesystem |
| ZFS | Pool expansion | Pool-level | Storage hosts where you own the whole stack |

- Grow sequence, LVM + ext4/XFS: `lvextend -r -l +100%FREE /dev/vg0/data` — `-r` resizes the filesystem in the same command and picks the right tool for you.
- `resize2fs` on a mounted ext4 grows fine; `xfs_growfs` REQUIRES the filesystem to be mounted (it takes the mount point, not the device).
- Shrinking is the operation that eats data. Back up first, and treat "we need to shrink" as a sign the volume layout was wrong.

## LVM

```bash
pvs; vgs; lvs -o +devices        # the three-line status of any LVM host
vgextend vg0 /dev/sdc            # add a new disk to the pool
lvextend -r -L +50G /dev/vg0/data
lvcreate -s -L 10G -n data-snap /dev/vg0/data    # snapshot before a risky migration
```

- An LVM snapshot is copy-on-write and **fills up**: when its allocated space is exhausted the snapshot is dropped and becomes invalid — size it for the write volume during its lifetime and delete it when done (`lvremove`). Watch with `lvs -o +snap_percent`.
- Snapshots are a rollback window, not a backup: they live on the same disks as the origin.
- Thin pools over-provision by design; monitor `Data%` and `Meta%` on the pool. A thin pool at 100% metadata is far harder to recover than one at 100% data.
- `lvs -o +devices` is what tells you whether a logical volume spans the disk you are about to remove.

## Mounts And fstab (the file that decides whether the host boots)

```
UUID=1a2b-...  /data  ext4  defaults,nofail,x-systemd.device-timeout=10  0 2
```

- Test before you trust: `mount -a` applies the file to the running system without a reboot. A typo caught here is a nuisance; the same typo found at boot is an emergency shell (→ `boot.md`).
- `nofail` on every non-essential mount. Without it, a missing or renamed device stops the boot dead — the single most common cause of unreachable cloud VMs after a resize or attach.
- Add `x-systemd.device-timeout=10` for network-attached or removable devices so a missing device delays boot by ten seconds instead of the default 90.
- The last field: `0` = no fsck (correct for network mounts and most cloud volumes), `1` for root, `2` for other local filesystems.
- Useful options: `noexec,nosuid,nodev` on data and `/tmp`; `ro` for anything that must not change; `noatime` removes a write per read on read-heavy volumes (`relatime` is the modern default and is usually enough).
- systemd generates a `.mount` unit per fstab entry — `systemctl daemon-reload` after editing fstab, and `systemctl status data.mount` to see why one failed.

## Network Mounts

- NFS `hard` (default) blocks I/O forever when the server disappears — that is the origin of most D-state processes (→ `processes.md`). `soft,timeo=,retrans=` returns errors instead, at the cost of corrupting writers that do not check them; databases stay `hard`.
- Recover a dead NFS mount without rebooting: `umount -l /mnt/dead` (lazy unmount), then fix the server side.
- Mount at first use rather than at boot: `x-systemd.automount,noauto` — the boot no longer depends on a remote server being up.
- SMB/CIFS credentials belong in a `credentials=/root/.smbcred` file with mode 600, never inline in fstab where every user can read them.

## Health And Failing Disks

- `dmesg -T | grep -iE 'i/o error|ata|nvme|reset'` — the kernel names a failing device long before the application does.
- `smartctl -a /dev/sda`: `Reallocated_Sector_Ct` and `Current_Pending_Sector` rising over time predict failure; on NVMe read `Percentage Used` and `Media and Data Integrity Errors`. Run `smartctl -t short /dev/sda` on suspicion.
- A filesystem remounted read-only mid-operation is the kernel protecting you: read `dmesg`, replace the device, restore from backup. Clearing space will not help.
- `fsck` only on an UNMOUNTED filesystem (`fsck -f /dev/sdb1`). Running it on a mounted one corrupts what was still healthy. For root, force it at the next boot with `fsck.mode=force` on the kernel command line (→ `boot.md`).
- RAID: `cat /proc/mdstat` shows arrays and rebuild progress; `mdadm --detail /dev/md0` names the failed member. A degraded array is an emergency with a deadline, not a warning — the second failure during rebuild is the classic total loss.

## Encryption

- LUKS: `cryptsetup luksOpen /dev/sdb1 data` → `/dev/mapper/data`; persist through `/etc/crypttab` plus fstab on the mapper device.
- Headless hosts need an unlock path at boot: a keyfile on the root disk (protects against disk theft only), TPM binding, or `dropbear-initramfs` for SSH-based unlock. Deciding this AFTER enabling encryption is how servers become unbootable remotely.
- Back up the LUKS header (`cryptsetup luksHeaderBackup`) — a corrupted header is unrecoverable data loss even with the correct passphrase.

## Durability

- A write is not on disk until `fsync` returns; `sync` flushes globally. Databases do this themselves — respect their settings rather than tuning them away for benchmark numbers.
- Atomic replace requires a rename within the SAME filesystem: write `dest/.tmp.file`, then `mv` it over the target. Across filesystems `mv` degrades to copy+delete and readers can catch a half-written file (→ `files.md`).
- Write caching on consumer SSDs can lie about flushes under power loss; on hardware you own, that is what a battery-backed controller or an enterprise drive buys.

## Record It

The storage layout is a host fact the next session must not rediscover: volume group, logical volumes and their sizes, filesystem types, which mounts are separate, and where the encrypted volumes are. Write it to the host's row in `## Hosts` in `~/Clawic/data/linux/memory.md` (and to `## Storage Layout` in `baselines/<host>.md` when a baseline exists). Every fstab edit, resize, `tune2fs -m`, or new mount goes to `changes/<year>.md` with its rollback — the fstab line you added is the one that will strand the host at the next reboot (`memory-template.md`).

Related: reclaiming space → `disk-space.md` · boot failures caused by fstab → `boot.md` · copying and syncing data → `files.md` · snapshots versus backups → `backups.md`.
