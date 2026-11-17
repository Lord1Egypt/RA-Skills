# Scheduling — cron, systemd Timers, and a Clock You Can Trust

A scheduled job fails differently from an interactive one: minimal environment, no terminal, output nobody reads, and a schedule that can fire twice or never. Every rule here exists because a job "worked when I tested it".

## Choosing The Mechanism

| Need | Use |
|---|---|
| Simple periodic job on any Unix | crontab |
| Must run after downtime (missed window) | systemd timer with `Persistent=true` — cron silently skips missed runs |
| Resource limits, dependencies, or real logs | systemd timer (the job is a unit: `MemoryMax=`, `After=`, journal) |
| Interval measured from BOOT or from the last finish | systemd timer (`OnBootSec=`, `OnUnitInactiveSec=`) — cron cannot express either |
| One-off at a future time | `systemd-run --on-active=`, or `at` where installed |
| Laptop/desktop that is off at night | anacron (or a timer with `Persistent=true`) |
| else | crontab, and revisit when you need any row above |

## cron: The Rules That Bite

- The environment is minimal: `PATH=/usr/bin:/bin`, no profile, no `.bashrc`, `SHELL=/bin/sh`. Reproduce a failure honestly with `env -i /bin/sh -c 'your command'` — testing in your login shell proves nothing.
- Use absolute paths for every binary and every file the job touches; a job's working directory is the user's home, not the script's directory.
- `%` in a crontab line means newline: everything after the first `%` becomes stdin to the command. `date +\%F` — escape every one.
- Files in `/etc/cron.d/` need a **user field** (`0 3 * * * root /usr/local/bin/job`); a personal `crontab -e` entry must NOT have one. Swapping the two forms is the most common silent-failure in this file.
- `run-parts` (which drives `/etc/cron.daily` and friends) **skips filenames containing a dot** — `backup.sh` never runs, `backup` does. Nothing logs the omission.
- Capture both streams or lose them: `>> /var/log/job.log 2>&1`. Default output goes to local mail, which on a server nobody reads and which often is not even installed. `MAILTO=""` at the top of the crontab makes the silence deliberate.
- `@reboot` fires when the cron daemon starts, which includes a daemon restart, not only a real boot.
- `crontab -r` wipes the crontab with no confirmation and sits next to `-e` on the keyboard. Keep `crontab -l > ~/crontab.bak` current, or manage jobs as files under `/etc/cron.d/` where they are in version control.
- Day-of-month AND day-of-week both set means **OR**, not AND: `0 0 13 * 5` runs on the 13th and on every Friday. Leave one of them as `*` unless you mean the union.

## systemd Timers

```ini
# /etc/systemd/system/backup.timer
[Unit]
Description=Nightly backup
[Timer]
OnCalendar=*-*-* 03:15:00
Persistent=true
RandomizedDelaySec=15m
[Install]
WantedBy=timers.target
```

- The timer needs a matching `backup.service` (`Type=oneshot`) and `systemctl enable --now backup.timer`. Enabling the SERVICE instead of the timer runs it once at boot and never again — a frequent first-time mistake.
- `systemctl list-timers --all` shows the next and last elapse for every timer; `systemd-analyze calendar 'Mon *-*-* 04:00'` prints the next occurrences of a spec before you install it.
- `Persistent=true` runs a missed job once after the host comes back. Without it, a machine that was down at 03:15 simply has no backup that night.
- `RandomizedDelaySec=` spreads a fleet: a hundred hosts hitting the same mirror or S3 bucket at exactly 03:00 is a self-inflicted thundering herd.
- `OnUnitInactiveSec=15m` measures from the last FINISH, so a run that takes 20 minutes cannot stack on itself — the cleanest overlap protection available.
- Timers inherit the service's environment rules: absolute paths, `EnvironmentFile`, no shell (→ `systemd.md`).
- Logs come free: `journalctl -u backup.service --since yesterday`.

## Overlap, Concurrency, And Long Runs

- Any job that can outlast its interval needs a lock: `flock -n /var/lock/job.lock /usr/local/bin/job` exits immediately if a previous run is still going. Without it, a slow night produces two instances writing the same output.
- `flock -w 300` waits instead of skipping — right for a job that must eventually run, wrong for a monitor that would queue forever.
- A lock file alone (test-then-create) is not a lock: two runs can pass the test in the same instant. `flock` is atomic; write your own only if `flock` is unavailable.
- Long jobs should be idempotent and resumable. "Runs for 6 hours, breaks at hour 5, must start over" is a design bug that the scheduler cannot fix.

## Time, Timezones, And DST

- `timedatectl` in one line tells you the timezone, whether the RTC is in local time, and whether the clock is synchronized. "System clock synchronized: no" on a server is an incident waiting to happen.
- Clock skew breaks things that look unrelated: TLS certificate validation, JWT expiry, Kerberos (which typically tolerates about five minutes), replication, and log correlation across hosts.
- Run one sync daemon, not two: chrony (RHEL default, better on intermittent connectivity) or systemd-timesyncd (a lightweight SNTP client, enough for a VM). Two competing daemons fight and neither converges. `chronyc tracking` shows the current offset and drift.
- cron uses the system timezone; a host set to UTC and a team thinking in local time schedules jobs an hour off twice a year. Set servers to UTC and write schedules in UTC.
- Jobs scheduled between 01:00 and 03:00 local time can run twice or not at all on DST transition days. Schedule outside that window, or use UTC and stop thinking about it.
- VMs and laptops resuming from suspend can jump the clock forward; a timer with `Persistent=true` fires on resume, a cron job in the skipped window does not.

## Verifying A Scheduled Job Actually Ran

1. `systemctl list-timers` or `grep CRON /var/log/syslog` (`journalctl -t CRON` / `-u crond`) — did the scheduler fire?
2. Did the command run and exit non-zero? For cron, only your own redirect proves it; for timers, `systemctl status backup.service` shows the last result and `journalctl -u backup.service` the output.
3. Make failures loud: have the job write a heartbeat (timestamp file, monitoring ping) on SUCCESS, and alert on the absence of the heartbeat. A job that silently stops running is the failure mode nobody notices for months.
4. `OnFailure=notify@%n.service` on the unit turns a failed timer job into an alert without any extra tooling.

## Record It

Every recurring thing you schedule — patch window, backup, restore drill, log vacuum, audit diff, reboot drill, certificate renewal — gets a row in the `## Due` table of `~/Clawic/data/linux/memory.md` (what / every / last run / next due), checked against today's date at the start of every session and stated in one line when overdue. The job itself (unit, timer, crontab entry, lock file) goes to `changes/<year>.md` with the command that removes it. A cadence that lives only in a crontab on one host is invisible the moment that host is not the one you are looking at (`memory-template.md`).

Related: unit files, environment, and sandboxing → `systemd.md` · log retention for job output → `logs.md` · long remote operations → `ssh.md` · alerting on a job that stopped running → `monitoring.md`.
