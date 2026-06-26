# Platform notes

hearth has two roles for any host:

- **Bridgehead** — the host that runs hearth and SSHes out to probe other devices
- **Probed device** — any host hearth checks the health of

Bridgehead requirements are stricter (needs bash, ssh, curl, python3+yaml). Probed device requirements are looser (often just "responds to ping" + "has SSH" + standard Linux tools).

## Compatibility matrix

| Role | Linux | macOS | Windows | Android | iOS |
|------|-------|-------|---------|---------|-----|
| **Bridgehead** | ✅ Tier 1 | ✅ Tier 1 | WSL2 only | Termux (Tier 2) | ❌ |
| **Probed (full L1-L5)** | ✅ | ✅ | HTTP-only | chroot/Termux | ❌ |
| **Probed (L1 only)** | ✅ | ✅ | ✅ | ✅ | ✅ |

## Linux specifics

Just works. No special notes for any modern distro (Debian 11+, Ubuntu 20.04+, Arch, Fedora 35+, RHEL/Rocky/Alma 8+).

`sshpass` is in the default repo on Debian/Ubuntu/Arch. On RHEL/Rocky/Alma you may need EPEL (`sudo dnf install epel-release && sudo dnf install sshpass`) or to use SSH keys instead.

## macOS specifics

- **Default bash is 3.2** (too old). Install bash 5+ via Homebrew: `brew install bash`. Then either alias `bash` to the Homebrew one or invoke scripts with `/opt/homebrew/bin/bash ./scripts/sweep.sh`.
- **`timeout` command is `gtimeout`** after `brew install coreutils`. hearth detects and adapts — no config needed from you.
- **`sshpass`** was removed from Homebrew core for licence reasons. Either install from a third-party tap (`brew install hudochenkov/sshpass/sshpass`), use SSH keys (recommended), or use `auth: ssh-key` everywhere.

## Windows specifics

**Native PowerShell is NOT supported.** No bash, no sshpass, no GNU coreutils. Trying to maintain a Windows-native port is more work than the value justifies.

**Use WSL2 instead.** All hearth features work in WSL2 Ubuntu.

```powershell
# In an admin PowerShell:
wsl --install -d Ubuntu
# Reboot, do first-run setup, then drop into Ubuntu.
# Inside Ubuntu, follow the Linux install steps.
```

When **probing** Windows hosts (not running hearth ON them), use `auth: http-only` and probe via the host's HTTP services (e.g. nginx, IIS, custom apps on local ports). hearth cannot do `systemctl is-active` over WMI/WinRM — that's out of scope.

## Android specifics (Termux)

Termux is the recommended way to run hearth on Android.

**Critical:** install Termux from **F-Droid** (https://f-droid.org/packages/com.termux/) — NOT the Play Store version, which is unmaintained.

```bash
pkg update
pkg install bash git openssh sshpass curl python jq yq
```

**Caveats specific to Android+Termux:**

- **No systemd in Termux** — Termux is itself best probed as `auth: local` with `no_systemd: true`. Or as `auth: ssh-pass` from another host (Termux's sshd is `pkg install openssh`).
- **Mobile networking adds latency** — bump `ssh_connect_timeout: 8` per-device when probing FROM Termux.
- **Phone sleeps aggressively** — first SSH out from Termux often times out, second succeeds. Set `ssh_warmup: true` on devices probed from a phone bridgehead.
- **Battery optimisations** — Android may kill Termux when in background. Add Termux to your battery-optimisation whitelist.
- **Storage permissions** — `~/.hearth/` lives in Termux's private storage (`~/.hearth/`, not `/sdcard/.hearth/`). Don't put your devices.yaml on shared storage.

## iOS

Not supported. iOS doesn't allow arbitrary local shell scripts in any maintained app store app. iOS users should:

- Run hearth on a Linux/macOS bridgehead at home
- Use Tailscale to reach the bridgehead from outside
- SSH to the bridgehead from iOS (Termius, Blink Shell, Prompt 3, etc.) and run sweeps there

## Chroot environments (Kali NetHunter, Linux Deploy, etc.)

- No systemd inside the chroot — `no_systemd: true`
- TUN devices not available — Tailscale must run in userspace networking mode (see `examples/archetypes/linux-nosystemd-chroot.md`)
- First SSH after chroot starts up is slow — `ssh_warmup: true`
- Use the chroot's user/password, not the host Android's credentials

## Container environments (Docker, Podman)

You CAN run hearth inside a Docker container. Mount your `devices.yaml` as a volume:

```bash
docker run --rm -it \
  -v ~/.hearth:/root/.hearth \
  -v ~/.ssh:/root/.ssh:ro \
  -e HEARTH_PASS_X="$HEARTH_PASS_X" \
  hearth:latest \
  /opt/hearth/scripts/sweep.sh
```

A Dockerfile is not yet provided. Contributions welcome.

## Probing FROM a Docker container

If your bridgehead is itself running in a container, all the above caveats apply, plus:

- Container needs network access to the LAN (host networking, or bridge networking with the LAN exposed)
- Container needs DNS pointed at your LAN's resolver if you use hostnames in `address:`
- Tailscale-in-Docker requires `--cap-add=NET_ADMIN --device=/dev/net/tun` for kernel-mode, or userspace networking otherwise

## Distribution-specific notes

### Debian 13 (trixie) and Ubuntu 24.04+

Both ship `iptables-nft` by default. Tailscale's apt package will swap `iptables` to `nft` mode via `update-alternatives`. This is **fine in normal cases** but has caused failures on hosts with unusual NIC configurations (USB NICs, certain Realtek drivers). If you're installing Tailscale on a Linux host that hearth will probe, do it from the physical console, not from the only SSH session you have, with a recovery plan.

### Alpine Linux

Alpine uses OpenRC, not systemd. hearth will report `no-systemd` for L4 unless you set `no_systemd: false` AND have `openrc-systemctl` (a compatibility shim) installed. Easier path: leave `no_systemd: true` and use `command` probes for L4-equivalents like `rc-status -s`.

### NixOS

systemd-based, hearth works as expected. Service names are sometimes non-obvious (e.g. `nginx.service` may be `nixos.nginx.service` depending on your config). Check with `systemctl list-units --type=service`.

### TrueNAS / FreeBSD

Not yet tested. The `linux-systemd` archetype won't apply because BSD doesn't use systemd. A FreeBSD archetype would be a good contribution if anyone wants to add it.