# Suspected Compromise — Evidence First, Then Containment, Then Rebuild

Two instincts make this worse: rebooting (destroys volatile evidence and often the persistence mechanism you needed to find) and cleaning (removes the attacker's tooling and leaves their access). Work in this order — preserve, contain, understand, rebuild — and treat every tool on the box as untrustworthy until proven otherwise.

Read `baselines/<host>.md` before anything else: the whole method below is a diff against a known-good state, and without it "this process looks unfamiliar" is an opinion. This file covers the host. Org-level process — who is notified, disclosure, coordination — belongs to the `incident-response` skill.

## Do Not

| Action | Why it hurts |
|---|---|
| Reboot | Loses running processes, open sockets, memory-resident payloads, and deleted-but-open binaries — often the only copy of the malware |
| Delete the suspicious file first | You lose the sample and the timestamps, and the persistence mechanism reinstalls it |
| Run the box's own `ps`, `ls`, `netstat` and believe them | A userland rootkit replaces exactly those; cross-check against `/proc` |
| Change the root password and call it done | Keys, cron jobs, systemd units, and a second account survive a password change |
| Patch and keep running | Patching closes the door the attacker no longer needs |
| Restore last night's backup onto the same host | The backup is probably already compromised, and the host still is |

## Preserve, In Volatility Order

Capture from most to least volatile, to a location OFF the host (an SSH pipe or a mounted read-only share), and write down the time of each step:

```bash
date -u; uptime                                   # when you started, and how long it has been up
ss -tunap                                          # every socket with its process — the loudest signal
ps auxwwf                                          # full tree, full argv
ls -l /proc/*/exe 2>/dev/null | grep -i deleted    # running binaries whose file is gone
lsof -n -P                                          # open files, including deleted ones
cat /proc/net/tcp /proc/net/tcp6                    # the kernel's own socket list, not ss's view
last -F; lastb -F; who -a                           # logins, failures, current sessions
crontab -l; ls -la /etc/cron.*/ /var/spool/cron/    # scheduled persistence
systemctl list-units --type=service --state=running
journalctl -b --no-pager                            # ship the output off-box before anything rotates
```

- A **volume snapshot or disk image** taken from the hypervisor or the provider console is the highest-value artifact and costs nothing to keep. Take it before touching anything if the platform allows it.
- Copy a suspicious binary out via `/proc/<pid>/exe` (`cp /proc/1234/exe /mnt/eviction/sample`) — that works even after the file is deleted from disk.
- Ship the journal off-box now: local logs are deletable by whoever owns the host (→ `logs.md`).

## Contain Without Killing The Evidence

- **Isolate at the network layer above the host**: cloud security group, switch port, or hypervisor. A firewall rule inside a compromised host is subject to the compromise.
- If the host firewall is the only lever, keep your own session: allow your source address first, then default-deny, with a scheduled rollback (→ `ssh.md`).
- Keep the machine running while you collect. Stop the affected service rather than the host when you must stop the bleeding.
- Rotate the credentials the host could read, starting now and not after the analysis: SSH keys it held or authorized, API tokens in its `EnvironmentFile`s and `.env`s, database passwords, cloud instance-role sessions, agent tokens, and any shared secret its users could read (→ `users.md`).

## Where Persistence Hides

Walk all of them; attackers use two or three, so finding one is not finishing.

| Place | What to look for |
|---|---|
| `~/.ssh/authorized_keys` for EVERY account, plus `/root/.ssh/` | A key nobody recognizes; `AuthorizedKeysFile` pointed somewhere unusual in `sshd_config` |
| Cron: user crontabs, `/etc/cron.*`, `/etc/cron.d`, `at` jobs | Base64 blobs and download-then-execute one-liners; a file whose name hides among the defaults |
| systemd: `/etc/systemd/system`, `/usr/local/lib/systemd`, `~/.config/systemd/user`, timers | A unit with a plausible name and an implausible `ExecStart`; `enable-linger` on a service account |
| Accounts | A second UID 0 in `/etc/passwd`, a new account with a shell, a service account that gained one (`awk -F: '$3==0' /etc/passwd`) |
| Shell init | `~/.bashrc`, `~/.profile`, `/etc/profile.d/*`, `~/.ssh/rc` |
| Preload and modules | `/etc/ld.so.preload` (should not exist on most systems), unexpected entries in `lsmod`, `/etc/modules-load.d/` |
| Setuid and capabilities | New setuid binaries, `getcap -r /` results outside the baseline |
| Package integrity | `rpm -Va` (RHEL) or `debsums -c` (Debian) — replaced system binaries show up here |
| Web and app paths | New files under document roots, a webshell in an upload directory |
| else | Diff against `baselines/<host>.md`: listeners, enabled units, setuid list, and the file `mtime` sweep below |

```bash
find / -xdev -newermt '2026-07-01' -type f 2>/dev/null | grep -vE '^/(proc|sys|run|var/log|var/lib)' | head -50
find /tmp /var/tmp /dev/shm -type f -executable 2>/dev/null   # the classic staging directories
```

Timestamps lie: `touch -r` copies another file's mtime, so a plausible date is weak evidence. `ctime` (`stat`) is harder to forge from userland, and the package database is the strongest local witness.

## The Cryptominer Pattern (by far the most common)

Sustained 100% CPU on all cores, a process with a random-looking name in `/tmp`, `/dev/shm` or `~/.cache`, outbound connections to a mining pool on 3333/4444/14444 or over TLS to a pool domain, a cron entry that re-downloads it, and often a killer script that removes competing miners and cloud security agents. Entry point is nearly always an exposed service with a default credential or an unpatched application, not SSH brute force against keys.

Finding a miner is not the finding: the same access that ran it could run anything. It is a full compromise with a noisy symptom.

## The Rebuild Rule

**The only recovery you can defend is: rebuild from a known-good image, restore DATA (not binaries, not `/etc` wholesale), rotate every credential the host could read, then close the entry point.** Cleaning a host means proving a negative on a system whose tools the attacker controlled.

- Restore data, review configuration by diff rather than restoring it blindly, and reinstall packages from repositories rather than from the old tree (→ `backups.md`).
- Choose a restore point from BEFORE the earliest evidence, not before the discovery. The gap between intrusion and detection is usually the surprise.
- Close the entry point before the new host is exposed: the unpatched application, the credentialed service, the open management port (→ `hardening.md`, `networking.md`).
- Exceptions to the rebuild rule are business decisions, not technical ones. If the host stays, say plainly what the residual risk is and monitor it as untrusted.

## After: The Part That Prevents The Repeat

- Write the timeline: first evidence, entry point, what the attacker reached, what was rotated, what was rebuilt, and how long each step took.
- Ship logs off-box and set up file integrity checking with the database stored elsewhere — a baseline the attacker can rewrite proves nothing (→ `hardening.md`).
- Re-take the baseline on the rebuilt host so the next diff has a clean reference (→ `monitoring.md`).

## Record It

Write the incident to `incidents/<year>.md` (date, host, symptom, root cause, fix, time to resolve) and the full timeline plus the rotation list to `artifacts/postmortem-<host>-<what>.md` with its `## Boxes` line — evidence paths and pointers only, never a credential, not even a rotated one. Log every rotation and every hardening change in `changes/<year>.md` with its rollback. If the host was rebuilt, update its rows in `~/Clawic/data/servers/servers.md` and `## Hosts`, and put the file-integrity and audit-diff cadences in `## Due`. Formats: `memory-template.md`.

Related: exposure baseline and auditing → `hardening.md` · accounts and offboarding → `users.md` · restoring data → `backups.md` · shipping logs → `logs.md` · baselines to diff against → `monitoring.md`.
