# New Host — The First Hour, And What cloud-init Owns

Everything here is cheaper now than later: an unlogged host loses the evidence of its own first crash, and a hostname changed after the certificates were issued is a second outage. Read `## Hosts` in `~/Clawic/data/linux/memory.md` first — a host the user already described does not get re-interrogated.

## The Order That Matters

1. **Identify the host before configuring it.** `cat /etc/os-release`, `hostnamectl`, `nproc`, `free -h`, `lsblk -f`, `systemd-detect-virt`. This is also the row you will write to the inventory, so collect it once (→ `distros.md`).
2. **Get a second way in before you touch access.** Provider console, serial console, or a second key. Every step below can lock you out, and the lockout-proof procedure assumes a fallback exists (→ `ssh.md`).
3. **Named account with sudo, then key-only SSH.** `useradd -m -s /bin/bash -G sudo|wheel alice`, `ssh-copy-id`, verify from a NEW session, then `PasswordAuthentication no` and `PermitRootLogin no` in a drop-in (→ `hardening.md`, `users.md`).
4. **Persistent journal, immediately.** `mkdir -p /var/log/journal && systemctl restart systemd-journald`. Skip it and the logs of the first crash die with the first reboot (→ `logs.md`).
5. **Time sync verified, not assumed.** `timedatectl` — "System clock synchronized: yes" and the timezone set to UTC on servers (→ `scheduling.md`).
6. **Automatic security updates**, with the reboot decision made explicitly by `reboot_policy` (→ `packages.md`).
7. **Firewall default-deny inbound**, allowing SSH before enabling it (→ `networking.md`).
8. **Swap decided deliberately**, not inherited from the image (below).
9. **Alarms and a baseline**: `disk_alert_pct` on every filesystem, and a healthy-period measurement recorded before the workload arrives (→ `monitoring.md`).
10. **Write the host down** — inventory row and OS profile — before the session ends. A host nobody recorded is a host nobody patches.

## Hostname And Identity

- `hostnamectl set-hostname web01` writes `/etc/hostname` and applies it live. On Debian/Ubuntu, also fix the `127.0.1.1 web01` line in `/etc/hosts`: without it `sudo` and some daemons pause on every start trying to resolve their own name.
- Set the FQDN the way the workload expects it (`web01.example.com` in `/etc/hosts`, short name in `/etc/hostname` is the common convention). Certificates, mail, and monitoring all key off this — changing it later means reissuing.
- **A cloned VM keeps the golden image's identity.** Duplicate `/etc/machine-id` makes DHCP hand two machines the same lease, and duplicate SSH host keys make every clone indistinguishable to clients. Before templating: `truncate -s 0 /etc/machine-id`, remove `/var/lib/dbus/machine-id` (or symlink it), delete `/etc/ssh/ssh_host_*`, clear logs and shell history, and remove the seeded `authorized_keys`. On first boot systemd regenerates the machine-id and sshd regenerates host keys.
- `systemd-detect-virt` tells you whether you are on KVM, a container, WSL, or bare metal — which decides whether half of `storage.md` and `kernel.md` even applies.

## cloud-init: The Files You Do Not Own

On a cloud image, cloud-init runs before you log in and again at every boot. Editing a file it manages produces the signature complaint: *"my change reverted after a reboot"*.

| It manages | Where your change belongs |
|---|---|
| Hostname | `preserve_hostname: true` in `/etc/cloud/cloud.cfg`, or set it in the instance's user-data |
| Network config (`/etc/netplan/50-cloud-init.yaml`, `/etc/sysconfig/network-scripts/*`) | A higher-numbered netplan file, or disable the module with `/etc/cloud/cloud.cfg.d/99-disable-network-config.cfg` containing `network: {config: disabled}` |
| `/etc/resolv.conf` on some images | The network config layer above, never the file |
| Users and `authorized_keys` for the default account | user-data, or `ssh_deletekeys`/`users:` in the config |
| `/etc/hosts` (some images regenerate it from a template) | `manage_etc_hosts: false`, or the template under `/etc/cloud/templates/` |
| else | Check `cloud-init query --all` and `/var/lib/cloud/instance/` before assuming a file is yours |

- `cloud-init status --long` says whether it finished and whether it errored; `/var/log/cloud-init-output.log` holds what the scripts printed. A host that boots "empty" usually has a failed module logged there.
- **user-data runs once per instance, not once per boot** — re-running requires `cloud-init clean --logs` plus a reboot, which also wipes the instance-id state. `bootcmd` and `#cloud-config` modules with `per-always` frequency are how you get per-boot behaviour.
- Validate before launching a fleet: `cloud-init schema --config-file user-data.yaml`. A YAML typo produces a host that boots with no users and no keys, which is unrecoverable without a console.
- Disable it entirely on a host that has become pet rather than cattle: `touch /etc/cloud/cloud-init.disabled`. Do it deliberately and record it, because the next admin will expect cloud-init to be in charge.

## Swap, Sized On Purpose

- The decision, not a rule: swapless makes failures fast and obvious; a few gigabytes lets cold pages leave RAM before the OOM killer picks a victim (→ `oom.md` and Where Experts Disagree in `SKILL.md`).
- Cloud images arrive both ways. Check `swapon --show` rather than assuming; an image with zero swap and 1 GiB of RAM will OOM during its first `apt full-upgrade`.
- A swap FILE is the portable answer and can be resized later: `fallocate -l 2G /swapfile`, `chmod 600`, `mkswap`, `swapon`, then the fstab line (full recipe in `oom.md`).
- Hibernation is the only case that needs swap sized against RAM, and it is a laptop concern (→ `desktop.md`).

## Filesystem Layout Decisions That Cannot Be Undone Later

- Separate `/var` (or at least `/var/log`) on anything that logs seriously: a runaway log then fills its own volume instead of stopping the whole host (→ `disk-space.md`).
- LVM on a physical or resizable volume costs nothing and buys online growth and snapshots. Growing a partition that is not on LVM means downtime or a rebuild (→ `storage.md`).
- XFS cannot shrink, ever. Choose ext4 where the size is a guess and the guess may be high.
- `nofail` plus `x-systemd.device-timeout=10` on every non-root mount, from the very first fstab line — this is the single most common cause of a cloud host that never comes back (→ `boot.md`).
- Reserve on data volumes: `tune2fs -m 1` recovers most of ext4's default 5% on a big data disk; keep the 5% on root.

## Before You Call It Ready

| Check | Command |
|---|---|
| Reboot survived, everything came back | `reboot`, then `systemctl --failed`, `journalctl -b -p err` |
| SSH works from a fresh session with the key only | New terminal, `ssh -o PasswordAuthentication=no` |
| Firewall is what you think it is, from outside | Port scan from another host, not `nft list ruleset` |
| Journal persisted across that reboot | `journalctl --list-boots` shows more than one |
| Time is synchronized | `timedatectl` |
| Unattended security updates are actually enabled | `systemctl status unattended-upgrades` / `dnf-automatic.timer` |
| Nothing unexpected is listening | `ss -tlnp` compared against what the host is for |

Rebooting on purpose now is how you find out the host boots; the alternative is finding out during an incident (→ `boot.md`).

## Record It

Write the machine to the shared inventory `~/Clawic/data/servers/servers.md` (one row, `Name` + `Provider`, update in place if it is already there) and the OS profile — distro, init, firewall front end, MAC, filesystem layout, backup target — to `## Hosts` in `~/Clawic/data/linux/memory.md`. Take the first baseline into `baselines/<host>.md` while the host is quiet, and put the patch window and any drill into `## Due`. Formats and thresholds: `memory-template.md`. A provisioning session that writes nothing means the next session starts by rediscovering this host.

Related: hardening baseline → `hardening.md` · accounts and sudo → `users.md` · lockout-proof changes → `ssh.md` · what to measure first → `monitoring.md` · distro differences → `distros.md`.
