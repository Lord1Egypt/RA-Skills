# Packages And Upgrades — Without Bricking The Host

Package operations are transactions on a live system. The failure modes are: interrupted mid-transaction, an upgrade that changes behaviour silently, and a kernel that only takes effect after a reboot nobody scheduled.

## Before Any Upgrade On A Host That Matters

1. Run it inside `tmux`/`screen`. An SSH drop during `apt full-upgrade` leaves dpkg half-configured, and the recovery is done from the console (→ `ssh.md`).
2. Check free space in `/` AND `/boot` — a kernel upgrade with a full `/boot` produces a truncated initramfs and an unbootable host (→ `disk-space.md`, `boot.md`).
3. Have a rollback: a VM snapshot, an LVM snapshot, or a rebuilt host. `apt` has no reliable undo; `dnf history undo <id>` exists but cannot un-migrate data a service already touched.
4. Read what will change: `apt list --upgradable`, `apt-get -s dist-upgrade` (simulate), `dnf check-update`. Anything that REMOVES a package needs a second look before you type yes.

## Debian / Ubuntu (apt, dpkg)

| Situation | Command |
|---|---|
| Security-only view | `apt list --upgradable \| grep -i security` |
| Upgrade without removing anything | `apt upgrade` — never removes; held-back packages stay behind |
| Full upgrade including removals | `apt full-upgrade` (the old `dist-upgrade`) |
| Freeze a package at its current version | `apt-mark hold <pkg>`; list with `apt-mark showhold` |
| Recover an interrupted transaction | `dpkg --configure -a`, then `apt -f install` |
| Lock held by another process | `fuser -v /var/lib/dpkg/lock-frontend` — wait for it |
| else | `apt policy <pkg>` shows every candidate version and its source |

- **Never kill a running dpkg to release the lock.** The holder is usually `unattended-upgrades` or a `apt-daily` timer; it finishes in minutes. A killed transaction leaves packages half-configured and turns a two-minute wait into an hour of `dpkg --configure -a`.
- Conffile prompts hang automation: `apt-get -o Dpkg::Options::="--force-confold" -o Dpkg::Options::="--force-confdef" -y upgrade` keeps your existing config files; add `DEBIAN_FRONTEND=noninteractive` so nothing tries to open a dialog. Decide `confold` (keep yours) vs `confnew` (take the package's) deliberately — silence is not the same as correct.
- Repository keys: `apt-key` is deprecated and removed. Keys go in `/etc/apt/keyrings/<name>.gpg`, referenced from the source with `signed-by=`. A repository whose key is missing fails with `NO_PUBKEY`; one whose key expired fails the same way and needs the vendor's new key, not a trust bypass.
- Third-party repositories in `/etc/apt/sources.list.d/` are the usual cause of "upgrade wants to remove half the system": pin them (`/etc/apt/preferences.d/`) or accept that they can override distro packages.
- A distro release upgrade (`do-release-upgrade`) is a rebuild-grade event: snapshot first, expect third-party repos to be disabled, and never run it over a bare SSH session.

## RHEL / Fedora (dnf, rpm)

- `dnf history` / `dnf history info <id>` / `dnf history undo <id>` — a real transaction log with a rollback for package state.
- `dnf needs-restarting -r` answers "does this host need a reboot" (exit 1 = yes); `dnf needs-restarting -s` lists services running old code.
- `dnf versionlock add <pkg>` is the equivalent of an apt hold (from `python3-dnf-plugin-versionlock`).
- `rpm -qa --last | head` shows what changed most recently — the first thing to check when a host started misbehaving "for no reason".
- `rpm -V <pkg>` verifies installed files against the package: `5` means checksum changed, `T` timestamp, `M` mode. It is the cheapest tamper and drift check available.
- Modular content (AppStreams) can pin a major version of a language runtime; `dnf module list <name>` explains why the "latest" is not what you expected.

## Arch, Alpine, SUSE

- Arch is rolling: `pacman -Syu` upgrades everything, and a **partial upgrade (`pacman -Sy <pkg>`) breaks the system** because libraries and dependents move together. There is no supported "install just this one thing from a newer sync".
- Arch keeps a package cache in `/var/cache/pacman/pkg` — the practical downgrade path (`pacman -U <cached-pkg>`). `paccache -r` trims it.
- Alpine: `apk add --no-cache <pkg>`; musl, not glibc, so binaries built elsewhere may not run. `apk info -W <file>` maps a file to its package.
- SUSE: `zypper up` (respects vendor/patch rules) vs `zypper dup` (distribution upgrade); `zypper ps` lists processes using deleted libraries.

## After Upgrading: Old Code Still Running

- Upgrading a library does NOT restart the services linked against it — they keep the deleted version mapped. `/proc/<pid>/exe -> ... (deleted)` and `lsof +c 0 | grep DEL` name the offenders (→ `processes.md`).
- Debian/Ubuntu ship `needrestart`, which prompts or reports; RHEL has `dnf needs-restarting`. Use one of them as a post-upgrade step rather than assuming.
- A kernel upgrade requires a reboot to take effect: `uname -r` (running) vs the newest installed kernel. `/var/run/reboot-required` on Debian/Ubuntu is the flag file monitoring should watch.
- Live patching (kpatch, Ubuntu Livepatch) covers a subset of CVEs and defers, but does not remove, the reboot. Track the deferral rather than forgetting it.
- Reboot policy is a variable, not a habit: honour `reboot_policy` (`allowed` reboot as part of the change, `maintenance-window` propose it for the window, `never` report the requirement and stop).

## Unattended Updates

- Security-only automatic updates are the right default for internet-facing hosts: on Debian/Ubuntu `unattended-upgrades` restricted to the security origin; on RHEL `dnf-automatic` with `upgrade_type=security`.
- Configure the reboot separately (`Unattended-Upgrade::Automatic-Reboot-WithUsers "false"` plus a fixed time) — an unattended kernel update that never reboots is a false sense of safety, and one that reboots at random is an outage.
- Exclude the packages that carry your workload (database engines, language runtimes) with holds; let the OS surface patch itself.
- The `apt-daily` timers are also why the dpkg lock is busy at odd hours — that is expected behaviour, not contention to fight.

## Installing Outside The Package Manager

- Binaries dropped in `/usr/local/bin` are invisible to the package manager: no upgrades, no CVE tracking, no dependency checks. Write each one to `changes/<year>.md` and keep a manifest on the host (`/usr/local/etc`, or config management) so the next admin knows what the package manager does not own.
- Never `curl … | sh` on a host you care about: download, read, checksum, then run.
- `update-alternatives --config <name>` (Debian) or `alternatives` (RHEL) is the supported way to have two versions of the same tool and choose one.
- Language package managers (pip, npm, gem) installing system-wide fight the distro's copies. Use a virtualenv, a user prefix, or a container. On modern Debian/Ubuntu a system-wide `pip install` is blocked by design (PEP 668) — that error is the packaging system protecting itself, not a bug to override.

## Record It

Every upgrade that changed behaviour, every hold, and every third-party repository added goes to `~/Clawic/data/linux/changes/<year>.md` with the file that persists it and the command that undoes it (`apt-mark unhold`, `dnf history undo <id>`). A reboot that became required and was NOT taken goes on the host's row in `## Hosts` as `reboot pending since <date>` — a pending reboot that only lives in one session's memory is an unpatched kernel with a false sense of safety. The patch window itself belongs in `## Due` (`memory-template.md`).

Related: reboot recovery → `boot.md` · disk space for `/boot` → `disk-space.md` · distro command mapping → `distros.md` · alerting on pending reboots → `monitoring.md`.
