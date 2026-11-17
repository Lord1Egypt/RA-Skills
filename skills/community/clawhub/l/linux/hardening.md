# Hardening — A Baseline For A Host Exposed To The Internet

Order matters more than completeness: the first four items remove most of the real risk, and everything after them is depth. Apply each through the lockout-proof procedure in `ssh.md`.

## The Baseline, In Order

1. **Close the network.** Default-deny inbound, allow only what serves a purpose (SSH, plus the ports the workload needs). Bind everything else to `127.0.0.1` — a service that does not listen publicly cannot be attacked publicly (→ `networking.md`).
2. **Key-only SSH.** `PasswordAuthentication no`, `KbdInteractiveAuthentication no`, `PermitRootLogin no` (or `prohibit-password` where automation needs it), `AllowGroups ssh-users`. This single change eliminates credential-stuffing as a category.
3. **Automatic security updates**, with the reboot decision made explicitly (→ `packages.md`).
4. **No shared accounts.** Named users, sudo for privilege, and offboarding that actually revokes (→ `users.md`).
5. Then: MAC enforcing, service sandboxing, auditing, integrity checking, and log shipping — the sections below.

## Firewall

- Default policy DROP inbound, ACCEPT outbound (restrict outbound only where you can enumerate what the host legitimately talks to — a broken outbound policy is a self-inflicted outage that is hard to diagnose).
- Allow SSH before enabling the policy, and keep a scheduled rollback running while you do it (→ `ssh.md`).
- Cloud security groups and the host firewall are complementary, not redundant: the security group protects against misconfiguration inside the host, the host firewall against a misconfigured security group. Run both.
- Container runtimes insert rules ahead of your front end — verify exposure from OUTSIDE the host with a port scan after any container deployment.
- Rate-limit SSH at the firewall (nftables `limit rate`, or ufw's `limit`) rather than adding a ban daemon as the first line.

## SSH Beyond The Basics

- `MaxAuthTries 3`, `LoginGraceTime 30`, `AllowTcpForwarding no` and `X11Forwarding no` unless used.
- Restrict automation keys in `authorized_keys`: `restrict,command="...",from="10.0.0.0/8"` turns a shell credential into a single-purpose one (→ `ssh.md`).
- fail2ban or sshguard reduces log noise and blocks brute force; with password auth already disabled it is defence in depth, not the defence. Watch its own rules — a misconfigured jail can ban your office range.

## Mandatory Access Control

- Leave SELinux `enforcing` on RHEL-family hosts and AppArmor enabled on Debian-family. Disabling it to make an application work trades a permanent, systemic protection for one afternoon of convenience.
- The correct workflow for a denial is: read the AVC, add the label or boolean, re-test (→ `permissions.md`).
- `getenforce` should read `Enforcing`; `aa-status` should list your service's profile in enforce mode. Both belong in whatever check runs against your fleet.

## Service Sandboxing

Every service you run is a blast radius. In the unit (→ `systemd.md`):

```ini
NoNewPrivileges=yes
ProtectSystem=strict
ReadWritePaths=/var/lib/app
ProtectHome=yes
PrivateTmp=yes
CapabilityBoundingSet=CAP_NET_BIND_SERVICE
RestrictAddressFamilies=AF_INET AF_INET6 AF_UNIX
SystemCallFilter=@system-service
```

- Run as a dedicated system user, never root, and never a user with a login shell.
- `systemd-analyze security <unit>` scores the result; work down the highest-impact findings rather than chasing a perfect number.

## Audit Surface

```bash
find / -xdev -perm -4000 -type f 2>/dev/null      # setuid binaries — know every one
find / -xdev -perm -0002 -type f 2>/dev/null      # world-writable files
find / -xdev -nouser -o -xdev -nogroup            # orphaned files from deleted accounts
ss -tlnp                                           # everything listening, and its owner
systemctl list-unit-files --state=enabled          # what starts at boot, and why
```

- Run these once on a new host and write the output to `~/Clawic/data/linux/baselines/<host>.md` under `## Audit Surface` and `## Listening`, with its `## Boxes` line in `memory.md`. The value is entirely in the DIFF at the next review, not in the first listing — and the review cadence belongs in `## Due` (`memory-template.md`).
- Remove packages you do not use rather than configuring them off — an uninstalled service has no CVEs and no misconfiguration.
- Secrets on disk: mode 600, owned by the service user, never in a world-readable `/etc` file, never in a unit's `Environment=` (which `systemctl show` exposes to any user). Use `EnvironmentFile=` with a 600 file or a credential store.

## Auditing And Integrity

- auditd answers "who changed this file" after the fact: `auditctl -w /etc/sudoers -p wa -k sudoers`, `ausearch -k sudoers`. Persist rules in `/etc/audit/rules.d/`.
- Watch the short list that matters: `/etc/passwd`, `/etc/shadow`, `/etc/sudoers` and `/etc/sudoers.d/`, `/etc/ssh/sshd_config*`, and the crontab/timer paths. Auditing everything produces a full disk and no reader.
- File integrity (AIDE, Tripwire): initialize the database on a host you trust, and **store the database off-host** — a checker whose baseline the attacker can rewrite proves nothing.
- Ship logs off-box. Local logs are deletable by whoever compromises the host; remote copies are what make an incident reconstructable (→ `logs.md`).

## Kernel And Network Posture

- `net.ipv4.conf.all.rp_filter=1` (reverse-path filtering), `net.ipv4.conf.all.accept_redirects=0`, `net.ipv4.conf.all.send_redirects=0`, `net.ipv4.tcp_syncookies=1`. Persist in `/etc/sysctl.d/` (→ `kernel.md`).
- `kernel.dmesg_restrict=1` and `kernel.kptr_restrict=1` reduce what an unprivileged local process can read.
- Mount `/tmp`, `/var/tmp`, and `/dev/shm` with `noexec,nosuid,nodev` where the workload allows it — some package managers and build tools legitimately need exec in `/tmp`, so test before enforcing.

## Compliance Regimes

- CIS Benchmarks and DISA STIGs are checklists with automated scanners (`oscap`, `lynis` for an informal pass). Treat a scanner's score as a to-do list to triage, not a target to maximize — several controls break real workloads and need documented exceptions.
- Every exception is written with its reason in `artifacts/exceptions-<host>.md`, and next to the configuration itself; an undocumented deviation is indistinguishable from a mistake at the next audit.
- Compliance is a floor. A host that passes every control and runs an unpatched application is compromised on schedule.

## What This Skill Does Not Cover

Application-level security (input validation, authentication design, dependency CVEs) is a different discipline. This file is about the host: who can reach it, who can log in, what a compromised service can touch, and what evidence survives.

**After hardening a host**, write each applied control to `changes/<year>.md` with its persistence file and its rollback, and record any documented compliance exception in `artifacts/exceptions-<host>.md`. An undocumented deviation is indistinguishable from a mistake at the next audit, and a hardening pass nobody recorded gets re-done from scratch (`memory-template.md`).

Related: accounts and offboarding → `users.md` · SSH configuration → `ssh.md` · MAC denials → `permissions.md` · log shipping → `logs.md` · what to alert on afterwards → `monitoring.md` · a host that is already compromised → `compromise.md`.
