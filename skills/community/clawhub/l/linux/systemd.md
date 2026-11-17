# systemd — Units, Ordering, Drop-Ins, and Why It Only Fails At Boot

systemd starts everything in parallel unless you tell it otherwise. Most "works by hand, fails at boot" bugs are a missing ordering or environment assumption that only shows up when nothing else is warm.

## Editing Units Without Losing The Change

- **Never edit files under `/usr/lib/systemd/system/`** — a package upgrade overwrites them without a word.
- `systemctl edit <unit>` writes `/etc/systemd/system/<unit>.d/override.conf` (a drop-in) and reloads for you. Drop-ins win over the vendor file and survive upgrades.
- `systemctl edit --full <unit>` copies the whole unit into `/etc/` when you need to change something a drop-in cannot express (like removing an `ExecStart` — for that, an empty `ExecStart=` line must precede the new one, because list directives accumulate).
- Hand-edited files need `systemctl daemon-reload`; without it `systemctl restart` runs the OLD definition and you debug a file the system is not using. `systemctl show <unit> -p ExecStart` prints what is actually loaded.
- `systemctl cat <unit>` shows the vendor file plus every drop-in, in order — the first thing to run when a unit does not behave like its file says.

## Ordering And Dependencies

- `After=` orders, `Wants=`/`Requires=` pull in. **Ordering without a dependency does nothing if the other unit is never started**; pair them: `Wants=network-online.target` AND `After=network-online.target`.
- `After=network.target` means "the networking stack is configured", NOT "an address is up and routable". A service that binds a specific IP or dials out at startup needs `network-online.target` (which itself requires the distro's wait-online service to be enabled).
- `Requires=` propagates failure and restarts: if the required unit stops, yours stops too. `Wants=` is the weaker, usually correct choice.
- `BindsTo=` plus `After=` is the pattern for a service tied to a device or a mount (it stops when the device disappears).
- Waiting on a database that is up but not accepting connections is not an ordering problem — add a readiness check to `ExecStartPre` (`until pg_isready; do sleep 1; done` with a bounded timeout), or use `Type=notify` in the dependency.
- `systemd-analyze verify /etc/systemd/system/my.service` catches typos and bad references offline; `systemd-analyze critical-chain <unit>` shows what actually delayed it at boot.

## Service Types And Restarts

| `Type=` | Ready when | Use for |
|---|---|---|
| `simple` (default) | Immediately after fork/exec — dependents may start too early | Foreground processes with no readiness signal |
| `exec` | After the binary is executed successfully | Catches "binary not found" as a start failure |
| `notify` | The service calls `sd_notify(READY=1)` | Anything whose dependents must wait for real readiness |
| `forking` | The parent exits; needs `PIDFile=` | Legacy daemons that background themselves |
| `oneshot` | The command exits (add `RemainAfterExit=yes` to stay "active") | Migrations, one-time setup, timer targets |

- `Restart=on-failure` alone hits the start limit: the defaults are 5 starts within a 10-second window (`DefaultStartLimitBurst=5`, `DefaultStartLimitIntervalSec=10s`), after which systemd gives up with "start request repeated too quickly" and stops trying. Add `RestartSec=5`: five retries then span at least 20 seconds, which never exhausts the window.
- Reset a unit stuck in that state: `systemctl reset-failed <unit>`, then start it.
- `Restart=always` restarts even after a clean exit — right for a daemon, wrong for a `oneshot`.
- Stop timing: systemd sends SIGTERM, waits `TimeoutStopSec` (90s by default), then SIGKILLs. A service that needs longer to flush must raise it explicitly; a service that hangs every stop is ignoring SIGTERM (→ `processes.md`).
- `KillMode=control-group` (default) signals every process in the unit's cgroup — which is why `systemctl stop` beats `kill` for anything that spawns children.

## Environment: The Boot-Only Failure

- Units get a nearly empty environment. No shell profile, no `.bashrc`, and `PATH` is a small system default — the same class of failure as cron (→ `scheduling.md`).
- Use absolute paths in `ExecStart`. `ExecStart=/usr/local/bin/app` is a contract; `ExecStart=app` is a coin flip.
- `Environment="KEY=value"` for a few values, `EnvironmentFile=-/etc/default/app` for a file (the leading `-` makes a missing file non-fatal). The file is parsed by systemd, NOT by a shell: no `export`, no command substitution, no variable expansion between lines.
- `ExecStart` is not a shell either — pipes, `&&`, globs, and redirections do not work. Wrap them: `ExecStart=/bin/sh -c 'a | b'`, or better, put the logic in a script.
- Check what a running service actually received: `systemctl show <unit> -p Environment` and `tr '\0' '\n' < /proc/<pid>/environ`.
- `WorkingDirectory=` matters for any relative path the application resolves itself.

## Sandboxing (and the EACCES it causes)

Hardening directives are the reason a service gets "permission denied" on a path root can write by hand:

- `ProtectSystem=strict` mounts the whole filesystem read-only except `/dev`, `/proc`, `/sys` — add `ReadWritePaths=/var/lib/app`.
- `ProtectHome=yes` hides `/home`, `/root`, `/run/user`; `PrivateTmp=yes` gives the service its own `/tmp`, so files it writes there are invisible to you (they live under `/tmp/systemd-private-*`).
- `NoNewPrivileges=yes`, `CapabilityBoundingSet=`, `RestrictAddressFamilies=`, `SystemCallFilter=@system-service` cut the blast radius of a compromise.
- Score and tune with `systemd-analyze security <unit>` (0 = locked down, 10 = wide open). Treat it as a checklist, not a target — some services legitimately need what it flags.
- Diagnostic when a hardened service fails: comment the directive out temporarily via a drop-in, confirm it was the cause, then add the narrow `ReadWritePaths=`/capability instead of leaving it off.

## Resource Control

- `MemoryMax=`, `MemoryHigh=`, `CPUQuota=`, `TasksMax=`, `IOWeight=` apply cgroup limits per unit; live usage with `systemctl status <unit>` (it prints Memory and Tasks) or `systemd-cgtop`.
- `OOMScoreAdjust=` protects or sacrifices a unit under host memory pressure (→ `oom.md`).
- Limits set in a unit override PAM's `limits.conf`, which services never see — `LimitNOFILE=` is the only file-descriptor setting that applies to a service (→ `processes.md`).

## Journal, Targets, Sockets, User Units

- Per-unit logs: `journalctl -u <unit> -e`, add `-f` to follow, `-b` for this boot, `-p err` for severity. Full journal usage and retention → `logs.md`.
- `StandardOutput=journal` is the default; a service writing its own logfile bypasses the journal entirely, which is worth knowing before you conclude it logged nothing.
- Targets replace runlevels: `multi-user.target` (console), `graphical.target`, `rescue.target`, `emergency.target`. `systemctl get-default` / `set-default`.
- Socket activation: a `.socket` unit holds the port and starts the `.service` on first connection — the reason a "stopped" service still answers, and a clean way to survive restarts without dropping connections.
- User units (`systemctl --user`) run only while the user has a session unless `loginctl enable-linger <user>` is set. This trips every "my user timer does not run when I am logged out".
- `systemctl mask <unit>` symlinks it to `/dev/null` and blocks EVERY activation path, including socket and dependency activation; `disable` only removes the boot hookup. Mask is the tool when something keeps starting itself.

## Fast Triage

| Symptom | Move |
|---|---|
| Starts by hand, fails at boot | Ordering (`network-online.target`) and environment (absolute paths, `EnvironmentFile`) |
| "start request repeated too quickly" | Start limit — add `RestartSec=5`, then `reset-failed` |
| Change to the unit file did nothing | `daemon-reload`; verify with `systemctl cat` and `systemctl show -p ExecStart` |
| Permission denied only as a service | Sandboxing directives — `systemd-analyze security`, then `ReadWritePaths=` |
| Stops take exactly 90 seconds | The process ignores SIGTERM; fix signal handling or set `KillSignal=`/`TimeoutStopSec=` |
| Service is "inactive" but the port answers | Socket activation, or a second copy started outside systemd |
| Disabled unit keeps coming back | Another unit `Wants=` it — `systemctl list-dependencies --reverse <unit>`, then `mask` |
| else | `systemctl status <unit> -l`, then `journalctl -u <unit> -b --no-pager` |

## Record It

A drop-in is invisible to anyone reading the vendor unit file, so it goes to `~/Clawic/data/linux/changes/<year>.md` the moment you create one: unit, directive, the drop-in path, and the rollback (delete the file, `daemon-reload`, restart). The same for a unit you masked — a masked unit is the hardest "why does this not start" to diagnose six months later. Sandboxing directives that took work to get right (the exact `ReadWritePaths=` set for a service) belong in `artifacts/` as a reusable unit fragment, with its `## Boxes` line (`memory-template.md`).

Related: timers and cron → `scheduling.md` · boot-time failures and rescue targets → `boot.md` · journald retention → `logs.md` · units as a persistence mechanism for attackers → `compromise.md`.
