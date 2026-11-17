# 🔥 hearth

> *the heartbeat of your homelab*

**One command. 14 seconds. Every device in your lab. Same format, one screen.** No agent to install on remote hosts, no database, no SaaS, no telemetry — just read-only SSH probes from a single bridgehead. Read-only by design, host-key verification on by default, honest about what it can't see, and small enough to read top-to-bottom in 15 minutes before installing.

```
=== HOMELAB — ESTATE HEALTH SWEEP ===
Timestamp: 2026-05-02T13:24:19+01:00

=== 192.0.2.10 main-server (OpenClaw / agent) === [OK]
  L1 ping:    OK
  L2 uptime:  1 day, 2 hours, load: 0.15 0.18 0.15
  L3 mem:     used 1.6Gi / 7.7Gi, 6.0Gi avail | disk: / 6% used, 814G free
  L4 svc:     openclaw=active nginx=active ollama=active cron=active
  L5 app:     gateway={"ok":true,"status":"live"} | https-front=HTTP 200

=== 192.0.2.20 fileserver (Samba + NFS file server) === [DEGRADED]
  L1 ping:    OK
  L2 uptime:  10 weeks, 3 days, load: 0.22 0.12 0.04
  L3 mem:     used 364M / 2.7G, 2.1G avail | disk: / 92% used ⚠, 11G free
  L4 svc:     ssh=active nginx=active smbd=active nmbd=active nfs-mountd=active
  L5 app:     nginx=HTTP 200 | fileserver-manager=HTTP 302 | ts=connected
  reason:     disk 92% >= 90%

=== 1/2 healthy, 1 degraded — 14s ===
```

Every device resolves to **`[OK]` / `[DEGRADED]` / `[DOWN]`**, the run ends with a one-line summary, and the exit code (`0`/`1`/`2`) means you can drop `sweep.sh` straight into cron or CI. Add `--json` for a machine-readable version an agent or script can reason over.

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

There's no shortage of monitoring tools. hearth is different in four ways that matter:

- **Read-only — guaranteed.** hearth never modifies remote state: no service restarts, no package installs, no writes to remote hosts at all. The only local writes are a per-run temp file and hearth's own `~/.hearth/known_hosts`. You can run it from an LLM agent, from cron, from a colleague's shell — it can't change anything on the hosts it probes. Most monitoring tools can't make that promise.
- **Secure by default.** SSH host-key verification is on out of the box (`StrictHostKeyChecking=accept-new`), pinning each host's key to a dedicated known_hosts file so a changed key aborts the probe rather than leaking a password to an impostor. SSH keys are preferred over passwords. See [Security & privacy](#security--privacy).
- **Honest about what it can't see.** When a layer can't be probed (Windows host with no SSH, chroot with no systemd), hearth says so explicitly — `unmanaged-host (no SSH)`, `no-systemd (chroot — N/A)`. It doesn't fake a green result. You always know whether a green is real or just unmeasured.
- **Zero install on remote hosts.** No agent on every box. No node_exporter. No daemon. Just read-only SSH out from one bridgehead. If you can SSH to a host, hearth can probe it — there's nothing else to maintain.

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

Without hearth, the agent has to either improvise SSH commands (slow, inconsistent, sometimes wrong) or you have to type them yourself (which defeats the point of having an agent in the first place). hearth gives the agent a structured, fast, consistent, **read-only** tool — so it can answer in seconds, in the same shape every time, with no risk of accidentally restarting your production database.

The skill ships with frontmatter tuned for LLM trigger-matching, so homelab phrases like *"homelab status"*, *"check all my servers"*, *"how is the lab"*, *"homelab health check"*, *"is \<device\> up"* route to hearth automatically.

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
- **Read-only** — never modifies anything, never restarts services, never writes to remote hosts

## Quick start

```bash
# 1. Install
git clone https://github.com/nj070574-gif/hearth.git
cd hearth

# 2. Copy the example config and customise it for your devices
mkdir -p ~/.hearth
cp examples/devices.example.yaml ~/.hearth/devices.yaml
$EDITOR ~/.hearth/devices.yaml

# 3. Set credentials via env vars (NEVER in the YAML)
export HEARTH_PASS_HOSTNAME="your-ssh-password"

# 4. Run a sweep
./scripts/sweep.sh
```

On the first sweep, hearth pins each host's SSH key to `~/.hearth/known_hosts` (trust-on-first-use). From then on, a changed key aborts that host's probe — see [Security & privacy](#security--privacy).

### Command-line options

```bash
./scripts/sweep.sh                 # full sweep — devices probed in parallel
./scripts/sweep.sh --device web    # just one device
./scripts/sweep.sh --group cluster # a named group from your config
./scripts/sweep.sh --problems-only # only the devices that are DOWN or DEGRADED
./scripts/sweep.sh --json          # machine-readable JSON (agents / scripts / jq)
./scripts/sweep.sh --watch 30      # live view, re-run every 30s
./scripts/sweep.sh --dry-run       # validate config without probing anything
```

Exit code is `0` (all healthy), `1` (something degraded) or `2` (something down), so this works as a drop-in cron/CI health check:

```bash
./scripts/sweep.sh --problems-only || notify-send "homelab needs attention"
```

For the OpenClaw skill version, point your OpenClaw agent at `SKILL.md` and trigger with homelab phrases like *"homelab status"*, *"check all my servers"*, *"how is the lab"*.

## Platforms

| Platform | Status | Notes |
|----------|--------|-------|
| **Linux** (Debian/Ubuntu/Arch/Fedora) | ✅ Tier 1 | Primary target. All features work. |
| **macOS** | ✅ Tier 1 | All features work. Uses `gtimeout` from `coreutils` if present, otherwise a built-in perl fallback — no hard dependency. Needs bash 4+ (`brew install bash`). |
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

hearth is built to be safe to run from an agent, from cron, or from a shared shell.

- **Read-only probes.** hearth runs only non-mutating queries — `uptime`, `free`, `df`, `systemctl is-active`, `curl` (GET). It never restarts a service, installs a package, or writes to a remote host.
- **Host-key verification on by default.** SSH probes use `StrictHostKeyChecking=accept-new`: each host's key is pinned on first contact to a dedicated `~/.hearth/known_hosts`, and a later key change aborts that host's probe — the guard that stops a man-in-the-middle from intercepting a password login. Tune with `HEARTH_SSH_STRICT`:
  - `accept-new` *(default)* — trust-on-first-use, reject changed keys
  - `yes` — strictest; the key must already be in `known_hosts` (pre-populate it for the hardest posture)
  - `no` — disabled (MITM risk); only for throwaway labs, and hearth warns on every run

  Move the known_hosts file with `HEARTH_KNOWN_HOSTS`. hearth never touches your personal `~/.ssh/known_hosts`.
- **SSH keys preferred.** Use `auth: ssh-key` with a dedicated, unprivileged key where you can; `ssh-pass` is supported for devices that only take passwords and `sshpass` is invoked only for those.
- **No credentials in config files.** Passwords live in env vars (`HEARTH_PASS_<NAME>`), tokens in `HEARTH_<APP>_TOKEN`, SSH keys in `~/.ssh/`. The repo's `.gitignore` blocks accidental commits, and hearth never echoes a credential.
- **Least privilege.** hearth never needs `sudo` or root — every probe runs as an ordinary user. A dedicated read-only SSH account is ideal.
- **No telemetry, no third parties.** hearth talks only to the hosts in your `devices.yaml`. It doesn't phone home; your sweep results stay on your machine.

## Registry moderation badge

Some skill registries auto-flag any skill that shells out to `ssh`/`curl` across multiple hosts, because a static scanner can't tell a read-only health probe from a malicious one. hearth is deliberately small (~960 lines of bash in `scripts/`) so you can verify it yourself: every command it runs is read-only and visible in the source. If a scan flags it, read `scripts/` and `SKILL.md` — the frontmatter declares the exact binaries, scope, and credential handling — then decide. Security concerns that reading the source doesn't resolve are welcome as issues.

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
