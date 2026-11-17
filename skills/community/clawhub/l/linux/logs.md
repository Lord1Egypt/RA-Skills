# Logs — Finding The Line That Explains It

Two log systems coexist on most hosts: the journal (binary, indexed, structured) and text files under `/var/log` (rsyslog, plus whatever applications write themselves). Knowing which one holds the answer saves the search.

## journalctl, The Useful Subset

```bash
journalctl -u nginx -e                     # one unit, jump to the end
journalctl -u nginx --since "10 min ago" --no-pager
journalctl -b -p err                       # this boot, errors and worse
journalctl -b -1 -p err                    # the PREVIOUS boot — needs a persistent journal
journalctl -k                              # kernel ring buffer, with real timestamps
journalctl -f -u app -g 'timeout|refused'  # follow, grep-filtered (-g is a regex)
journalctl _PID=1234                       # by field; also _UID=, _COMM=, _SYSTEMD_UNIT=
journalctl -o json-pretty -n 1             # every field available for a single entry
journalctl --since "2026-07-01" --until "2026-07-02 06:00" -o short-iso
```

- Priorities are numeric: 0 emerg … 3 err, 4 warning, 6 info, 7 debug. `-p err` means "err and worse", not "err only".
- `-o short-iso` prints unambiguous timestamps; `--utc` for correlating across hosts in different zones. Do that before pasting logs into a ticket.
- `-g` is available in reasonably recent systemd and is faster than piping to grep because it filters before formatting.
- `--follow` plus a unit is the correct way to watch a service through a restart; a `tail -f` on a rotated file stops following silently.

## Persistence (do this once, on every host)

- Default `Storage=auto` keeps the journal in RAM unless `/var/log/journal` exists. On a host without it, **every log from before the last reboot is gone** — including the logs of the crash you are investigating.
- Enable: `mkdir -p /var/log/journal && systemctl restart systemd-journald`. Verify later with `journalctl --list-boots` showing more than one entry.
- Size: journald caps itself at 10% of the filesystem, never more than 4 GB by default, and keeps 15% of the filesystem free. Override with `SystemMaxUse=` and `SystemKeepFree=` in `/etc/systemd/journald.conf`.
- Reclaim now: `journalctl --disk-usage`, then `journalctl --vacuum-size=500M` or `--vacuum-time=7d` (→ `disk-space.md`).

## The Silence That Is Not Silence

- **Rate limiting drops messages.** journald defaults to roughly 10000 messages per 30 seconds per service and logs "Suppressed N messages due to rate-limiting" when it kicks in. A service in a tight error loop loses exactly the lines you want. Raise `RateLimitBurst=` for that unit, or fix the loop.
- A service that writes its own logfile does not appear in the journal at all. `systemctl cat <unit> | grep -i standard` and check the application's own config before concluding it logged nothing.
- Output produced before the process reached its logging setup goes to `StandardOutput` (journal) — check both places for startup failures.
- A container's logs belong to the container runtime, not the host journal (unless the runtime is configured to use the journald driver).

## Text Logs Under /var/log

| Path | Distro | Holds |
|---|---|---|
| `/var/log/syslog` | Debian/Ubuntu | Everything rsyslog collects |
| `/var/log/messages` | RHEL/Fedora/SUSE | Same role |
| `/var/log/auth.log` / `/var/log/secure` | Debian / RHEL | Authentication, sudo, sshd |
| `/var/log/kern.log` | Debian | Kernel messages (also `journalctl -k`) |
| `/var/log/dmesg` | Most | Boot-time ring buffer snapshot |
| `/var/log/audit/audit.log` | RHEL with auditd | SELinux AVCs and audit rules |
| else | Application-specific | `lsof -p <pid> \| grep -i log` finds where a process actually writes |

- rsyslog and journald often both run: the same message exists in two places, with different timestamps and formats. Decide which is authoritative for your investigation rather than reconciling them.
- `dmesg -T` humanizes kernel timestamps, but the conversion is computed from uptime and drifts after suspend/resume — trust `journalctl -k` timestamps on laptops and VMs that sleep.

## Rotation

- logrotate runs from a systemd timer (`logrotate.timer`) or `/etc/cron.daily` and reads `/etc/logrotate.conf` plus `/etc/logrotate.d/*`.
- The classic failure: logrotate renames the file, the running process keeps writing to the same inode, and **the new file stays empty forever while the old one keeps growing invisibly**. The fix is a `postrotate` that signals the process to reopen (`systemctl reload <unit>` or `kill -USR1`), or `copytruncate` when the application cannot be signalled — accepting that `copytruncate` can lose the lines written during the copy.
- Test a rule without waiting a day: `logrotate -d /etc/logrotate.d/app` (dry run) then `logrotate -f /etc/logrotate.d/app` (force).
- `size`/`maxsize` protect against a burst that fills the disk between daily runs; `daily` alone does not.
- Compression (`compress delaycompress`) usually pays for itself immediately on text logs.

## Reading An Incident

1. Bound the window: the first user report minus a few minutes, to now. Everything else is noise.
2. Start at the errors: `journalctl -b -p err --since "<t>" --no-pager`.
3. Find the FIRST anomaly in that window, not the loudest. Cascading failures produce thousands of downstream errors after one cause.
4. Correlate across services on the same timeline: `journalctl --since "<t>" --until "<t2>" -o short-iso` with no unit filter, once you have a suspect minute.
5. Check the kernel separately: `journalctl -k --since "<t>"` — OOM kills, I/O errors, and network resets never appear in an application's log.
6. Correlate across hosts in UTC, and only after the clocks are verified synchronized (→ `scheduling.md`).

## Shipping And Retention

- Local logs are lost with the host and can be deleted by whoever compromises it. Anything security-relevant ships off-box (`ForwardToSyslog=yes` plus a remote rsyslog target, or a collector agent) → `hardening.md`.
- Set retention deliberately: journal vacuum policy plus logrotate `rotate N`. "Keep everything" ends as a full disk during an incident, which is when logs matter most.
- Structured output (`-o json`) is what makes journal data usable by a collector without reparsing free text.

## Record It

Retention is a decision with a rollback, so it goes to `~/Clawic/data/linux/changes/<year>.md`: the journald caps you set, the logrotate rule you added, the shipping target you configured, and how to undo each. Put the retention review itself in `## Due` — "keep everything" becomes a full disk during the incident when logs matter most, and nobody notices the drift until then. What an investigation concluded goes to `incidents/<year>.md`, not into a log excerpt: the line that explained it, in one sentence, beats a thousand pasted lines. Strip tokens and passwords out of any log excerpt before it is written anywhere under `~/Clawic/data/` (`memory-template.md`).

Related: disk reclaim → `disk-space.md` · unit logging directives → `systemd.md` · audit rules and log shipping → `hardening.md` · preserving logs off-box during a breach → `compromise.md`.
