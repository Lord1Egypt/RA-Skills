# Boot Failures And Recovery — Getting A Host Back

Boot problems have a fixed shape: the further the host got before stopping, the more tools you have. Identify the stage first, because it decides which recovery path is even available.

## Which Stage Failed

| Symptom on the console | Stage | Recovery entry point |
|---|---|---|
| No firmware/vendor screen, no POST | Hardware or firmware | Out-of-band console, BIOS/UEFI settings, boot order |
| Firmware screen, then "no bootable device" | Bootloader missing or the disk moved | Live/rescue media, reinstall GRUB |
| GRUB menu appears, kernel does not load | Kernel or initramfs | Pick an older kernel from the menu (Advanced options) |
| "Cannot open root device" / kernel panic on boot | initramfs missing a driver, or wrong root UUID | Older kernel, then rebuild initramfs |
| Drops to `(initramfs)` prompt | Root filesystem unavailable or dirty | `fsck` from that prompt, check the root UUID |
| "You are in emergency mode" | A mount in `/etc/fstab` failed | Comment out the mount, `mount -a`, then fix it |
| Boots, no network, no SSH | Network config or a failed unit | Console: `systemctl --failed`, `journalctl -b -p err` |
| Boots slowly, eventually works | A unit waiting for a timeout | `systemd-analyze blame`, `critical-chain` |
| else | Read the previous boot's log after recovery: `journalctl -b -1 -p err` | Requires a persistent journal (→ `logs.md`) |

## The fstab Rule (the top cause of unreachable cloud VMs)

A device named in `/etc/fstab` that does not exist stops the boot and drops you to emergency mode — where a cloud host with no console is simply gone.

- Every non-essential mount gets `nofail`, plus `x-systemd.device-timeout=10` so a missing device costs ten seconds instead of the default 90.
- `mount -a` after every fstab edit, in the same session, before you reboot. It applies and validates the file against the running system (→ `storage.md`).
- Reference devices by `UUID=`; names like `/dev/sdb1` reorder between boots.
- In emergency mode you get a root shell with `/` mounted read-only: `mount -o remount,rw /`, edit fstab, `systemctl default` to continue booting.

## GRUB: Editing A Single Boot

At the menu, press `e` to edit the selected entry (nothing is written to disk; Ctrl-X or F10 boots it once):

- `systemd.unit=rescue.target` — single-user with the root filesystem mounted and most services stopped; asks for the root password.
- `systemd.unit=emergency.target` — the minimum: root shell, almost nothing mounted.
- `init=/bin/bash` — the last resort, bypassing systemd entirely. The root filesystem is read-only: `mount -o remount,rw /` before changing anything, and `exec /sbin/init` or a forced reboot (`echo b > /proc/sysrq-trigger`) to leave, since a normal reboot command will not work.
- `fsck.mode=force fsck.repair=yes` — force a check of the root filesystem at boot.
- `nomodeset` — boots past a graphics driver that hangs the console.
- Remove `quiet splash` to see what the kernel is actually printing; that alone answers many "it just hangs" reports.

Persistent changes go in `/etc/default/grub` (`GRUB_CMDLINE_LINUX`), then `update-grub` (Debian/Ubuntu) or `grub2-mkconfig -o /boot/grub2/grub.cfg` (RHEL). Never edit the generated `grub.cfg` directly — the next kernel update overwrites it.

If the menu never appears, hold Shift (BIOS) or press Esc (UEFI) during boot, or set `GRUB_TIMEOUT=5` and `GRUB_TIMEOUT_STYLE=menu` while the host still boots.

## Rescue From External Media (chroot)

When the installed system cannot start at all, boot a live image or the provider's rescue mode and enter the installation:

```bash
mount /dev/sda2 /mnt                       # root filesystem (lsblk -f to identify)
mount /dev/sda1 /mnt/boot                  # and /boot, /boot/efi, /var if separate
for d in dev proc sys run; do mount --rbind /$d /mnt/$d; done
chroot /mnt /bin/bash
# now: grub-install /dev/sda && update-grub, or dpkg --configure -a, or fix fstab
```

- LVM first: `vgchange -ay` before mounting. LUKS first: `cryptsetup luksOpen /dev/sda3 root`.
- Mount `/boot` and `/boot/efi` before reinstalling a bootloader, or GRUB writes to the wrong place and reports success.
- Undo the binds (`umount -R /mnt`) before rebooting so nothing is left half-mounted.

## Initramfs

- After a kernel upgrade with a half-full `/boot`, the initramfs can be truncated — the new kernel then panics while the previous one still boots. Free space in `/boot` and regenerate: `update-initramfs -u -k all` (Debian) or `dracut -f --regenerate-all` (RHEL) (→ `disk-space.md`, `packages.md`).
- A module needed to reach the root device (storage controller, RAID, multipath, network for iSCSI/NFS root) must be IN the initramfs. Blacklisting a module without regenerating the initramfs leaves it loaded at boot and looks like the blacklist was ignored (→ `kernel.md`).
- Encrypted root on a headless host needs an unlock path inside the initramfs (keyfile, TPM, or `dropbear-initramfs` for SSH unlock) — plan it before enabling encryption, not after (→ `storage.md`).

## After The Host Is Up Again

- `systemctl --failed` — the short list of what did not start.
- `journalctl -b -1 -p err --no-pager` — errors from the boot that failed, which only exists if the journal is persistent (`mkdir -p /var/log/journal`). Do this once on every host you care about, before the incident.
- `systemd-analyze blame` (per-unit time) and `systemd-analyze critical-chain` (the actual serial path) — a 90-second boot is almost always one unit waiting for a timeout, usually a network wait or a missing mount.
- SELinux hosts restored from backup or repaired from a live image often have wrong labels everywhere: `touch /.autorelabel && reboot` relabels the whole filesystem once (→ `permissions.md`).
- **Write the recovery down while it is fresh**: the sequence that worked goes to `~/Clawic/data/linux/artifacts/runbook-<host>-boot.md` with its `## Boxes` line in `memory.md`, and the incident (symptom, root cause, fix, time to resolve) to `incidents/<year>.md`. Boot recovery is the work most likely to be repeated by someone with no context at 3am (`memory-template.md`).

## Prevention That Costs Nothing

- Keep at least two kernels installed; never let a cleanup script leave exactly one.
- `mount -a` after every fstab change; `nofail` on every optional mount.
- Persistent journal enabled on day one.
- Know the out-of-band console for every host before you need it (serial console, provider web console, IPMI/iDRAC/iLO). A host you can only reach over SSH is a host you can lose permanently with one config change (→ `ssh.md`).
- Reboot on purpose, on a schedule you choose. A host with 400 days of uptime has never proven it can start.

Related: fstab and devices → `storage.md` · kernel command line and modules → `kernel.md` · unit failures → `systemd.md`.
