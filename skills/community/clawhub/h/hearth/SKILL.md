---
name: hearth
description: A fast, read-only health-check sweep across every device in a homelab — ping, uptime/load, memory/disk, services, and app health, in 14 seconds with output you can scan in 30. Configuration-driven (~/.hearth/devices.yaml describes the lab; the skill is generic). Use when the user asks "how is the lab?", "server status", "check all servers", "is X up?", "health check", "what's down?", "anything broken?". Supports Linux, macOS, Raspberry Pi, Android (Termux/chroot), and Windows hosts (HTTP-only probe). Honest reporting — devices that can't be probed at L4 (Windows, chroots) are reported as such, never faked green. Read-only — never restarts services, never writes to remote hosts.
---

## What hearth gets you

**Before hearth:** six SSH terminals open on a Friday afternoon. Type `uptime; free -h; df -h; systemctl is-active <svc1> <svc2> ...` on each box. Eight minutes in, you've forgotten what server 1 said.

**With hearth:** one command, 14 seconds, every device, same format, one screen. Done.

```
=== HOMELAB — ESTATE HEALTH SWEEP ===
=== 192.0.2.10 main-server ===
  L1 ping:    OK
  L2 uptime:  1 day, 2 hours, load: 0.15 0.18 0.15
  L3 mem:     used 1.6Gi / 7.7Gi, 6.0Gi avail | disk: / 6% used, 814G free
  L4 svc:     openclaw=active nginx=active ollama=active cron=active
  L5 app:     gateway={"ok":true} | https-front=HTTP 200
=== 192.0.2.20 fileserver ===
  L1 ping:    OK   ...
=== sweep complete in 14 seconds ===
```

## Why someone uses this skill

Three things make hearth different from "just SSH and check yourself" or "set up Prometheus":

- **Read-only by design.** Never modifies remote state. No `systemctl restart`, no `apt-get install`, no writes beyond `/tmp/.hearth_*`. Safe to run from cron, from an LLM agent, from a colleague's shell. Most monitoring tools can't make that promise.
- **Honest about what it can't see.** When a layer can't be probed (Windows host with no SSH, chroot with no systemd), hearth says so explicitly — `unmanaged-host (no SSH)`, `no-systemd (chroot — N/A)`. It doesn't fake a green result. You always know whether a green is real or just unmeasured.
- **Zero install on remote hosts.** No agent on every box. No `node_exporter`. No daemon. Just SSH from one bridgehead. If you can SSH to a host, hearth can probe it.

The 5-layer pattern catches the failure classes that actually hit homelabs in production:

| Layer | Catches |
|-------|---------|
| L1 ping | Network drop, host off, ICMP blocked |
| L2 uptime+load | Reboots, runaway load |
| L3 mem+disk | Disk filling up before journald truncates logs, OOM-precursor leaks |
| L4 services | Service crashed, unit name drift after distro upgrade, fail2ban banning your bridgehead |
| L5 app | The "service is up but returns HTTP 500 for three days" silent-failure class |

## How hearth works

hearth is **configuration-driven** — the skill itself contains zero knowledge of any specific lab. The user describes their devices in `~/.hearth/devices.yaml` (or wherever `HEARTH_CONFIG` points), and hearth reads that config to drive its probes. Six device archetypes ship as worked examples (Linux+systemd, chroot/no-systemd, Raspberry Pi, Windows HTTP-only, SLURM cluster, multi-app web stack).

## Triggering

Invoke hearth when the user asks anything in this family:

- "server status", "lab status", "homelab status"
- "check all servers", "check the lab", "check my hosts"
- "is X up?" (where X is a device name from their config)
- "how is the lab?", "how is X?"
- "health check", "health sweep", "device health"
- "what's running?", "what's down?"

If the user names a single device, run `hearth check-device <name>` (or scope the sweep to one device with `--device <name>`).

## Operation

hearth is implemented as a thin wrapper around two scripts that ship with the project:

- `scripts/sweep.sh` — runs the full estate sweep, or a subset
- `scripts/check-device.sh` — runs the 5-layer probe on one device

Run from the user's hearth installation directory (typically `~/hearth/`):

```bash
./scripts/sweep.sh                    # full sweep
./scripts/sweep.sh --device <name>    # one device
./scripts/sweep.sh --group <name>     # named group of devices
./scripts/sweep.sh --dry-run          # validate config, no probes
```

Show the user the raw output. The output is already designed to be human-readable; do not re-summarise unless the user explicitly asks for analysis.

## Output format

Each device's status is printed in this exact format:

```
=== <ip-or-hostname> <name> [(<role>)] ===
  L1 ping:    OK | UNREACHABLE
  L2 uptime:  <duration>, load: <1m> <5m> <15m>
  L3 mem:     used <X> / <Y>, <Z> avail | disk: / <pct>% used, <free> free
  L4 svc:     <service1>=active <service2>=active ...
  L5 app:     <app1>=<status> | <app2>=<status> ...
```

Special cases:

- **`UNREACHABLE` at L1** — device fails ping. L2-L5 are skipped, sweep continues.
- **`SSH FAILED` at L2-L4** — device pings but SSH is unresponsive. L5 may still be attempted for HTTP probes.
- **`unmanaged-host (no SSH)` at L2-L4** — device is configured `auth: http-only` (e.g. Windows host without SSH). L5 carries the health signal.
- **`no-systemd (chroot — N/A)` at L4** — device is a chroot or has no systemd. L2/L3 still apply, L5 carries app-health.

## Triggers requiring extra care

- **"restart X" / "kill X" / "deploy X"** — hearth is read-only. If the user asks for write actions, do NOT use hearth — explain that hearth doesn't modify remote state and ask if they want to do that another way.
- **"add a new device"** — direct the user to edit `~/.hearth/devices.yaml`. Reference `examples/devices.example.yaml` and `docs/CONFIG.md` in the project for schema.
- **"why is X down?"** — first run `./scripts/sweep.sh --device <X>` to confirm the failure mode, then suggest investigation paths based on which layer failed (L1 = network, L4 = services, L5 = app).

## What hearth never does

- **Never modify remote hosts.** No `systemctl restart`, no `apt-get install`, no file writes beyond `/tmp/.hearth_*` ephemera.
- **Never reveal credentials.** Passwords and tokens live in env vars and SSH keys; hearth does not echo them.
- **Never make claims it can't verify.** If L4 can't be probed (chroot, Windows), hearth says so explicitly rather than reporting a fake green.
- **Never fabricate device data.** Every line of output comes from a real probe of a real device. If a probe times out, the output says so.

## Adding hearth to a new lab

If the user has not yet set up hearth:

1. Direct them to clone the repo and copy `examples/devices.example.yaml` to `~/.hearth/devices.yaml`
2. They edit the YAML with their real devices
3. They set credential env vars (`HEARTH_PASS_<DEVICE>`, etc.)
4. They run `./scripts/sweep.sh --dry-run` to validate
5. They run `./scripts/sweep.sh` for the first sweep

See `docs/INSTALL.md` for platform-specific install steps.

## Adding a new device archetype

If the user has a device type not covered by the 6 ship-included archetypes (linux-systemd, linux-nosystemd-chroot, raspberry-pi, windows-http-only, slurm-cluster, magento-server), help them craft a new entry by:

1. Reading `examples/archetypes/` for the closest existing match
2. Probing the device manually with `ssh user@host 'uname -srm; uptime; systemctl list-units --type=service --state=running --no-pager | head -20'` to discover its services
3. Adding a new device entry to their `devices.yaml`
4. Running `./scripts/sweep.sh --device <new-name>` to test

Encourage them to contribute the new archetype back upstream if it's broadly useful.

## Failure modes and what to tell the user

| Symptom | Likely cause | Suggested action |
|---------|-------------|------------------|
| L1 UNREACHABLE on a normally-reachable device | Network drop, host powered off | Check physical/UPS, check switch, ping the gateway |
| SSH FAILED but L1 OK | SSH daemon down, firewall, fail2ban ban | SSH manually from another host to confirm |
| L4 service shows `inactive` for a service the user expects active | Service crashed, unit name wrong | `journalctl -u <unit>` on the device |
| L5 HTTP probe shows `HTTP 000` | App is down or port closed | `curl -v <url>` from the bridgehead |
| L5 HTTP probe shows `HTTP 502/503` | App is up but failing | Check app's own logs |
| Sweep takes >30s for 10 devices | One device is timing out | Re-run with `--device <name>` to isolate |

## Privacy

hearth is designed to be safe to run in a public/agentic context:

- Reads only the user's own config file (no broader filesystem snooping)
- Writes only to `/tmp/.hearth_*` (cleaned up immediately)
- Does NOT log device IPs, hostnames, or output to any remote service
- Does NOT include telemetry of any kind

If asked about specific configuration values (passwords, tokens), hearth does NOT have access to those — they're in the user's env vars, only readable by the running process when invoking SSH/curl.

## Version

0.1.4 — schema-only example.yaml; app probes documented per-archetype. OpenClaw skill mode.