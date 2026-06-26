# 🔥 hearth

> *the heartbeat of your homelab*

**One command. 14 seconds. Every device in your lab. Same format, one screen.** No agent to install on remote hosts, no database, no SaaS, no telemetry — just SSH probes from a single bridgehead. Read-only by design, honest about what it can't see, and small enough to read top-to-bottom in 15 minutes before installing.

```
=== HOMELAB — ESTATE HEALTH SWEEP ===
Timestamp: 2026-05-02T13:24:19+01:00

=== 192.0.2.10 main-server (OpenClaw / agent) ===
  L1 ping:    OK
  L2 uptime:  1 day, 2 hours, load: 0.15 0.18 0.15
  L3 mem:     used 1.6Gi / 7.7Gi, 6.0Gi avail | disk: / 6% used, 814G free
  L4 svc:     openclaw=active nginx=active ollama=active cron=active
  L5 app:     gateway={"ok":true,"status":"live"} | https-front=HTTP 200

=== 192.0.2.20 fileserver (Samba + NFS file server) ===
  L1 ping:    OK
  L2 uptime:  10 weeks, 3 days, load: 0.22 0.12 0.04
  L3 mem:     used 364M / 2.7G, 2.1G avail | disk: / 6% used, 131G free
  L4 svc:     ssh=active nginx=active smbd=active nmbd=active nfs-mountd=active
  L5 app:     nginx=HTTP 200 | fileserver-manager=HTTP 302 | ts=connected

=== sweep complete in 14 seconds ===
```

## What this gets you

**Before hearth:**
```
$ ssh server-1
$ uptime; free -h; df -h; systemctl is-active nginx postgres redis
$ exit
$ ssh server-2
... (repeat 8 more times)
```
Eight minutes of typing. By server 5 you've forgotten what server 1 said. By server 10 you've missed the disk filling up on server 3.

**With hearth:**
```
$ ./scripts/sweep.sh
```
14 seconds. Every device. Same format. One screen. Done.

## Why hearth, specifically

There's no shortage of monitoring tools. hearth is different in three ways that matter:

- **Read-only — guaranteed.** hearth never modifies remote state. No `systemctl restart`, no `apt-get install`, no rm, no writes beyond `/tmp/.hearth_*`. You can run it from an LLM agent, from cron, from a colleague's shell — it can't break anything. Most monitoring tools can't make that promise.
- **Honest about what it can't see.** When a layer can't be probed (Windows host with no SSH, chroot with no systemd), hearth says so explicitly — `unmanaged-host (no SSH)`, `no-systemd (chroot — N/A)`. It doesn't fake a green result. You always know whether a green is real or just unmeasured.
- **Zero install on remote hosts.** No agent on every box. No node_exporter. No daemon. Just SSH out from one bridgehead. If you can SSH to a host, hearth can probe it — there's nothing else to maintain.

## Who this is for

### 🏠 Homelab admins

If you've ever:
- Opened six SSH terminals on a Friday afternoon to check what broke
- Lost track of which box has Tailscale running and which doesn't
- Forgotten which of your hosts run Docker and which run podman
- Been bitten by a service that was "running" but actually returning 500s for three days
- Found out the fileserver's disk was 98% full only when it stopped accepting writes

…hearth catches all of those, in one command, in 14 seconds, with output you can scan in 30.

Most homelab monitoring is heavy: Prometheus + Grafana + node_exporter on every host, alerts you don't read, dashboards you don't open. That's overkill for a 5-15 device personal lab. hearth is the opposite — a single command, one bridgehead, no databases, no SaaS, no accounts. The bridgehead can be your main server, your laptop, or anything that can SSH out.

### 🛠 Sysadmins and network engineers

If you've ever inherited a server estate with a wiki of stale runbooks, hearth gives you a single source of truth for "what's actually running, where, right now." The YAML config IS the inventory. New starter? Hand them the YAML and the troubleshooting guide and they're 80% there.

The 5-layer pattern catches the failure classes that actually hit you in production:

| Layer | Catches |
|-------|---------|
| L1 | Network drop, host off, ICMP blocked |
| L2 | Reboots, runaway load, missing reboot windows |
| L3 | Disk filling up before journald starts truncating logs, OOM-precursor memory leaks |
| L4 | Service crashed, unit name drift after a distro upgrade, fail2ban banning you off your own host |
| L5 | The "service is up but returns HTTP 500 for three days" silent-failure class |

L5 is the one that matters most. Anyone can check `systemctl is-active`. Knowing your storefront is *actually* serving content, your search index is *actually* green, your indexer is *actually* caught up — that's the bit nobody else writes.

### 🤖 OpenClaw users — this is the skill that pays for the agent

If you run OpenClaw (or any LLM-agent runtime), hearth is the skill that turns "is everything OK?" into a one-sentence question. Ask your agent:

- *"how's the lab?"* → full sweep, 14 seconds
- *"is the file server up?"* → just that one device
- *"why did the cluster go red?"* → sweep + diagnosis hints based on which layer failed

Without hearth, the agent has to either improvise SSH commands (slow, inconsistent, sometimes wrong) or you have to type them yourself (which defeats the point of having an agent in the first place). hearth gives the agent a structured, fast, consistent tool — so it can answer in seconds, in the same shape every time, with no risk of accidentally restarting your production database.

The skill ships with a frontmatter description tuned for LLM trigger-matching, so phrases like *"server status"*, *"check all servers"*, *"how is the lab"*, *"health check"*, *"is X up"* all route to hearth automatically.

## How it works — the 5 layers

A consistent five-layer probe across every device in your homelab:

| Layer | What it checks |
|-------|----------------|
| **L1 — reachability** | ICMP ping with short timeout |
| **L2 — uptime + load** | how long it's been up, current load average |
| **L3 — memory + disk** | RAM available, root partition usage |
| **L4 — services** | per-device list of systemd units (or "N/A" if not systemd) |
| **L5 — app health** | HTTP probes, JSON parsing, custom checks — the bit that catches "service up but app broken" |

Designed for the realities of real homelabs:

- **Mixed hosts** — Linux, macOS, Raspberry Pi, Android (Termux/chroot), Windows-via-HTTP
- **Mixed auth** — SSH password, SSH key, local exec, HTTP-only
- **Mixed services** — bring-your-own list per device
- **Honest reporting** — devices that can't be probed at L4 (Windows, chroots) say so, they don't fake it
- **Read-only** — never modifies anything, never restarts services, never writes to remote hosts beyond temp files

## Quick start

```bash
# 1. Install
git clone https://github.com/nj070574-gif/hearth.git
cd hearth

# 2. Copy the example config and customise it for your devices
cp examples/devices.example.yaml ~/.hearth/devices.yaml
$EDITOR ~/.hearth/devices.yaml

# 3. Set credentials via env vars (NEVER in the YAML)
export HEARTH_PASS_HOSTNAME="your-ssh-password"

# 4. Run a sweep
./scripts/sweep.sh
```

For the OpenClaw skill version, point your OpenClaw agent at `SKILL.md` and trigger with phrases like *"server status"*, *"check all servers"*, *"how is the lab"*.

See [docs/INSTALL.md](docs/INSTALL.md) for full platform-specific instructions.

## Platforms

| Platform | Status | Notes |
|----------|--------|-------|
| **Linux** (Debian/Ubuntu/Arch/Fedora) | ✅ Tier 1 | Primary target. All features work. |
| **macOS** | ✅ Tier 1 | All features work. Requires `coreutils` for GNU `timeout` (or use bundled fallback). |
| **WSL2 on Windows** | ✅ Tier 1 | Run hearth inside WSL2 Ubuntu/Debian. Full feature set. |
| **Termux on Android** | ⚠️ Tier 2 | Works, with caveats — no systemd, mobile networking quirks. |
| **Native Windows (PowerShell)** | ❌ Not supported | No native bash/sshpass. Use WSL2 instead. |
| **Probed FROM Windows** | ✅ Supported | Windows hosts can be *probed* via HTTP-only mode. |
| **Probed FROM macOS / iOS** | ✅ Supported | Same — HTTP-only probe mode. |

See [docs/PLATFORMS.md](docs/PLATFORMS.md) for details.

## Configuration

A device config has a simple shape:

```yaml
devices:
  - name: main-server
    address: 192.0.2.10
    auth: local                # local | ssh-pass | ssh-key | http-only
    services: [ssh, nginx, cron]

  - name: fileserver
    address: 192.0.2.20
    auth: ssh-pass
    user: admin
    password_env: HEARTH_PASS_FILESERVER
    services: [ssh, nginx, smbd, nmbd, nfs-mountd]
```

For full app-health probes (HTTP, JSON parsing, custom commands), see the per-archetype guides under [examples/archetypes/](examples/archetypes/) — each one shows a complete worked example for that device type.

Full schema reference: [docs/CONFIG.md](docs/CONFIG.md)

## Device archetypes (provided as examples)

hearth ships with worked examples for common homelab device types:

- [Linux + systemd](examples/archetypes/linux-systemd.md) — the default, covers most servers
- [Linux without systemd](examples/archetypes/linux-nosystemd-chroot.md) — chroots, Termux, Alpine without systemd
- [Raspberry Pi](examples/archetypes/raspberry-pi.md) — RAM-tight devices, CPU temp via vcgencmd
- [Windows host (HTTP-only)](examples/archetypes/windows-http-only.md) — Windows machines probed via their HTTP services
- [SLURM cluster](examples/archetypes/slurm-cluster.md) — head + compute nodes with NFS health
- [Magento server](examples/archetypes/magento-server.md) — Apache + MariaDB + OpenSearch + indexer health

Mix and match for your own lab.

## Security & privacy

- **No credentials in config files.** Passwords live in env vars (`HEARTH_PASS_<NAME>`), SSH keys live in `~/.ssh/`. The repo's `.gitignore` blocks accidental commits.
- **Read-only probes.** hearth runs `uptime`, `free`, `df`, `systemctl is-active`, `curl`. It never modifies remote state.
- **No telemetry.** hearth doesn't phone home. Your sweep results stay on your machine.
- **No third-party services required.** No accounts, no API keys, no SaaS dependencies.

## About the SUSPICIOUS moderation badge on registries

Some skill registries (including ClawHub) auto-flag this skill as **"SUSPICIOUS"** with reason codes like `install_untrusted_source`, `llm_suspicious`, and `vt_suspicious`. **This rating is expected** for any skill of this kind, and here's why — so you can make an informed decision before installing.

The rating is triggered by static patterns that scanners cannot distinguish from genuinely-malicious skills:

| What scanners see | What it actually is |
|--|--|
| Bash scripts that call `ssh` and `curl` against multiple remote hosts | Read-only health probes — `uptime`, `free`, `df`, `systemctl is-active`, `curl /healthz`. Same commands you'd type by hand. |
| References to `sshpass` for password-based SSH | Optional dependency, only used if YOUR config sets `auth: ssh-pass`. Never invoked otherwise. |
| Documentation showing `apt-get install`, `pkg install`, `brew install` | Standard install instructions for standard dependencies (bash, openssh, curl). |
| User-defined `command:` probe type in YAML config | Runs YOUR commands from YOUR config, on YOUR machines. hearth does not generate, fetch, or modify these. |

What hearth **does not** do, by design, with full source transparency:

- ❌ Phone home, log to remote servers, or telemetry of any kind
- ❌ Modify any state on remote hosts (no `systemctl restart`, no `apt-get install`, no writes beyond `/tmp/.hearth_*`)
- ❌ Fetch or execute code from external sources at runtime
- ❌ Read your `~/.ssh/` or `/etc/shadow` or any host-state outside what your YAML asks for
- ❌ Send your config, hostnames, or sweep output anywhere off-host

Every single shell command hearth runs is visible in `scripts/` (490 lines of bash, ~13 KB) — small enough to read top-to-bottom in 15 minutes. We encourage you to do exactly that before installing.

If you have a security concern that isn't addressed by reading the source, please open an issue.
## Status

Pre-release. Tested against a 10-device homelab covering:
- Generic Debian/Ubuntu hosts
- Raspberry Pi Zero W (RAM-constrained, single-core ARMv6)
- Kali Linux on Android (chroot, no systemd, mobile network)
- Low-power fanless Linux mini-PCs
- Workstation-class laptops repurposed as servers
- Consumer laptops repurposed as servers
- Windows desktops probed via HTTP-only mode

## Contributing

Contributions welcome — see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT. See [LICENSE](LICENSE).

## Trademark notice

"hearth" is a generic English word. This project does not claim a trademark on the name. If you build something else and call it hearth, that's fine.

---

*Built because the lab was getting harder to keep in my head than to keep alive.*