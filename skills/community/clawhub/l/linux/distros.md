# Distributions — What Changes When The Host Is Not The One You Expected

Identify before typing: `cat /etc/os-release` (`ID`, `VERSION_ID`, `ID_LIKE`) is the one file present on every modern distribution. `hostnamectl` prints it plus the kernel and virtualization type. Set `distro_family` from it and every command below follows.

## The Mapping Table

| Concern | Debian / Ubuntu | RHEL / Fedora / Rocky | Arch | Alpine | SUSE |
|---|---|---|---|---|---|
| Packages | `apt`, `dpkg` | `dnf`, `rpm` | `pacman` | `apk` | `zypper` |
| Admin group | `sudo` | `wheel` | `wheel` | `wheel` | `wheel` |
| Web server package | `apache2` | `httpd` | `httpd` | `apache2` | `apache2` |
| SSH unit name | `ssh.service` | `sshd.service` | `sshd.service` | OpenRC `sshd` | `sshd.service` |
| Syslog file | `/var/log/syslog` | `/var/log/messages` | journal only by default | `/var/log/messages` | `/var/log/messages` |
| Service defaults | `/etc/default/<name>` | `/etc/sysconfig/<name>` | `/etc/conf.d/` | `/etc/conf.d/` | `/etc/sysconfig/` |
| Firewall front end | ufw (or nftables) | firewalld | nftables/iptables | awall/iptables | firewalld |
| MAC | AppArmor | SELinux enforcing | none by default | none by default | AppArmor |
| Init | systemd | systemd | systemd | **OpenRC** | systemd |
| Network config | netplan (Ubuntu), NetworkManager, `/etc/network/interfaces` | NetworkManager | systemd-networkd / NM | `/etc/network/interfaces` | wicked / NM |
| Core utils | GNU | GNU | GNU | **BusyBox** | GNU |

`ID_LIKE` in `/etc/os-release` is what makes a script portable across derivatives: Rocky/Alma report `ID_LIKE=rhel`, Ubuntu/Mint report `debian`. Branch on `ID_LIKE` first, `ID` second.

## Where The Differences Actually Bite

- **Package names, not just managers**: `python3-dev` vs `python3-devel`, `libssl-dev` vs `openssl-devel`, `netcat-openbsd` vs `nmap-ncat`. A script that maps managers but hardcodes Debian names fails on RHEL at the install step.
- **Unit names**: `systemctl restart ssh` works on Debian and fails on RHEL, where it is `sshd`. Same for `mariadb` vs `mysql`, `apache2` vs `httpd`. Use `systemctl list-units --type=service | grep -i <name>` when unsure.
- **SELinux enforcing by default on RHEL-family**: identical file permissions, opposite outcome. Any RHEL guidance that ignores labels is incomplete (→ `permissions.md`).
- **Firewall front end**: a `ufw allow` on RHEL usually means ufw is not installed; `firewall-cmd --permanent` on Debian usually means firewalld is not the active front end (→ `networking.md`).
- **Config file paths for the same daemon**: RHEL splits more into `/etc/sysconfig`, Debian into `/etc/default` — the same tunable, a different file.

## Alpine And BusyBox

- Alpine uses OpenRC, not systemd: `rc-service <name> start`, `rc-update add <name> default`, and none of `systemctl`/`journalctl` exists. There is no journal — logs go to files.
- BusyBox applets accept a SUBSET of GNU flags. `ps aux` prints different columns, `find` lacks `-printf`, `sed -i` behaves differently, `date` lacks some formats. Scripts written against GNU coreutils fail in ways that look like bugs in your logic.
- musl, not glibc: binaries and prebuilt wheels compiled for glibc segfault or refuse to run. This is the same tax the `docker` skill describes for Alpine base images.
- `bash` is not installed by default; `/bin/sh` is BusyBox ash. A `#!/bin/bash` script fails with "not found", which reads like the script is missing (→ the `bash` skill).

## Arch

- Rolling release: there are no point versions to pin, and partial upgrades are unsupported (→ `packages.md`).
- Configuration is minimal by default and left to the admin — expect fewer sane defaults and more explicit setup than on a server distribution.
- `/etc/pacman.d/` mirrorlist quality determines upgrade speed and, occasionally, upgrade correctness.

## WSL2

- It is a real Linux kernel in a VM, but the boundaries are unusual: systemd is opt-in (`systemd=true` in `/etc/wsl.conf`) and off by default in older builds, so `systemctl` may not work at all.
- The clock can drift after the host sleeps, breaking TLS and package signatures — `hwclock -s` or a resync fixes it (→ `scheduling.md`).
- Filesystem performance across `/mnt/c` is an order of magnitude slower than the Linux filesystem; keep working trees in the Linux side.
- `dmesg`, hardware tools, and most `smartctl`/device work are meaningless: there is no direct hardware.

## Containers Are Not Hosts

- No init unless you provide one, so no systemd, no journal, and PID 1 semantics apply (the `docker` skill owns this).
- `/proc/meminfo` and `nproc` may report the HOST's resources while the cgroup limits are much lower — every capacity rule in this skill must be read against the cgroup, not the host (→ `oom.md`, `performance.md`).
- `dmesg` inside a container shows the host kernel's buffer (or nothing) and cannot be trusted for attribution.

## Immutable And Minimal Server Images

- rpm-ostree systems (Fedora CoreOS, Silverblue) and image-based hosts (Bottlerocket, Flatcar) keep `/usr` read-only: package installs become image layers or overlays, and configuration lives in `/etc` plus a declarative provisioning file. Debugging is done from a toolbox container.
- The habit to unlearn: editing files in place and expecting them to persist. On these systems the change belongs in the image or the provisioning config, or it disappears at the next update.

## Writing Portable Procedures

```sh
. /etc/os-release
case "$ID_LIKE$ID" in
  *debian*) PKG="apt-get -y install";  SSHD=ssh   ;;
  *rhel*|*fedora*) PKG="dnf -y install"; SSHD=sshd ;;
  *) echo "unsupported: $ID" >&2; exit 1 ;;      # fail loudly, never guess
esac
```

- Detect, branch, and fail loudly on the unknown case. A script that silently assumes Debian on an unrecognized host is worse than one that stops.
- Set `LC_ALL=C` in automation. Locale changes `sort` order (byte order vs collation), decimal separators, and the output format of `date` and `ls` — a script that parses tool output works on your host and produces silently wrong results on one with a different `LANG`.
- Prefer distro-agnostic interfaces where they exist: `systemctl`, `ip`, `ss`, `journalctl`, `getent`, `findmnt`. They behave identically wherever they exist, which is most places.
- Write the host's family down once (Record It below) and let it drive every subsequent command, rather than re-detecting it at each step.

## Record It

Two different destinations, and mixing them is the common error. A per-host fact — this box is Rocky 9 with firewalld and SELinux enforcing — goes to that host's row in `## Hosts` in `~/Clawic/data/linux/memory.md`, alongside its init, filesystem layout and quirks. A user statement that their estate is standardized on something ("we are a Debian shop", "we always use nftables") is a declaration and goes to `distro_family` / `firewall_tool` / `init_system` in `config.yaml`. One Alpine box in a Debian shop must not rewrite the default (`memory-template.md`).

Related: package operations per family → `packages.md` · firewall front ends → `networking.md` · MAC systems → `permissions.md` · first configuration of a new host → `new-host.md`.
