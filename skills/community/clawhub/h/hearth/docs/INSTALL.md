# Installation

hearth is a bash + standard-tooling skill. There is nothing to compile, no daemon to install. You clone the repo, set credentials in env vars, and run.

## Prerequisites

All platforms need:

| Tool | Used for | Notes |
|------|----------|-------|
| `bash` 4+ | runs the skill | macOS ships bash 3 — install bash 4+ via Homebrew |
| `ssh` (OpenSSH client) | remote probes | every platform has a way to install this |
| `sshpass` | password-based SSH | optional, only needed if any device uses `auth: ssh-pass` |
| `curl` | HTTP probes | universally available |
| `awk`, `sed`, `grep` | output parsing | GNU coreutils on Linux/WSL, BSD on macOS — both work |
| `python3` | JSON parsing in L5 | 3.6+ |
| `jq` | optional, makes JSON parsing simpler | recommended but not required |
| GNU `timeout` | per-device timeout wrapper | macOS: `brew install coreutils`, alias `gtimeout` to `timeout` |

## Linux (Debian/Ubuntu)

```bash
sudo apt-get install -y bash openssh-client sshpass curl python3 jq
git clone https://github.com/nj070574-gif/hearth.git ~/hearth
cd ~/hearth
cp examples/devices.example.yaml ~/.hearth/devices.yaml
$EDITOR ~/.hearth/devices.yaml
# set env vars for your devices (see CONFIG.md)
./scripts/sweep.sh
```

## Linux (Arch / Manjaro)

```bash
sudo pacman -S bash openssh sshpass curl python jq
# rest as above
```

## Linux (Fedora / RHEL)

```bash
sudo dnf install bash openssh-clients sshpass curl python3 jq
# rest as above
```

`sshpass` may not be in the default repos on RHEL/Rocky/Alma. Either enable EPEL (`sudo dnf install epel-release`) or use SSH keys instead and skip `sshpass` entirely.

## macOS

```bash
# Install dependencies via Homebrew
brew install bash openssh hudochenkov/sshpass/sshpass curl python jq coreutils

# Make sure Homebrew bash is in PATH (Apple's bash is too old)
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Verify
bash --version  # should be 5+

# Install hearth
git clone https://github.com/nj070574-gif/hearth.git ~/hearth
cd ~/hearth
mkdir -p ~/.hearth
cp examples/devices.example.yaml ~/.hearth/devices.yaml
$EDITOR ~/.hearth/devices.yaml
./scripts/sweep.sh
```

**Note on macOS `timeout`:** the GNU `timeout` command is provided by `coreutils` as `gtimeout`. hearth detects this automatically.

**Note on macOS `sshpass`:** Homebrew core dropped `sshpass` for licence reasons. Install from a third-party tap as shown above, OR use SSH keys (recommended).

## Windows (via WSL2)

hearth does not run natively on Windows PowerShell. Use WSL2:

```powershell
# In an admin PowerShell:
wsl --install -d Ubuntu

# After reboot and Ubuntu first-run setup, drop into Ubuntu and follow the Linux instructions above.
```

This is the only supported Windows path. Native PowerShell support is unlikely — too many incompatibilities with bash idioms.

## Android (via Termux)

Termux is the recommended way to run hearth on Android.

```bash
# Install Termux from F-Droid (NOT the Play Store version — it is unmaintained)
# https://f-droid.org/packages/com.termux/

# Inside Termux:
pkg update
pkg install bash git openssh sshpass curl python jq

git clone https://github.com/nj070574-gif/hearth.git ~/hearth
cd ~/hearth
mkdir -p ~/.hearth
cp examples/devices.example.yaml ~/.hearth/devices.yaml
nano ~/.hearth/devices.yaml
./scripts/sweep.sh
```

**Caveats on Termux:**
- No systemd in Termux — Termux is itself best probed as `auth: local` with `no_systemd: true`
- Mobile networking adds latency — bump `ssh_connect_timeout: 8` in your config
- Phone may sleep — first SSH out from Termux may time out, retry succeeds (similar to chroot quirks)

## Configuration after install

See [CONFIG.md](CONFIG.md) for a full reference of the `devices.yaml` schema.

In short:
1. Copy `examples/devices.example.yaml` to `~/.hearth/devices.yaml`
2. Replace the placeholder devices with your real homelab
3. For each device using `auth: ssh-pass`, set the corresponding env var:
   ```bash
   export HEARTH_PASS_FILESERVER='your-password'
   ```
4. For HTTP probes that need bearer tokens, set those too:
   ```bash
   export HEARTH_HA_TOKEN='your-home-assistant-long-lived-token'
   ```
5. Add the env-var exports to your shell profile (`~/.bashrc`, `~/.zshrc`) so they persist.

## Verifying the install

```bash
./scripts/sweep.sh --version    # should print the hearth version
./scripts/sweep.sh --dry-run    # validates your devices.yaml without probing
./scripts/sweep.sh --device main-server  # probes only one device for a smoke test
./scripts/sweep.sh              # full sweep
```

## OpenClaw skill installation

If you run OpenClaw (an LLM-agent skill runtime — see your OpenClaw documentation for canonical install path), drop `SKILL.md` from this repo into your skills directory:

```bash
mkdir -p ~/.openclaw/workspace/skills/hearth/
cp SKILL.md ~/.openclaw/workspace/skills/hearth/
# Plus any helper scripts referenced by SKILL.md
cp -r scripts/ ~/.openclaw/workspace/skills/hearth/
```

Then trigger from your OpenClaw agent with phrases like *"server status"*, *"check all servers"*, *"how is the lab"*.

## Updating

```bash
cd ~/hearth
git pull
# review CHANGELOG.md for any breaking changes
```

Your `~/.hearth/devices.yaml` is outside the repo so `git pull` will not touch it.

## Uninstalling

```bash
rm -rf ~/hearth
rm -rf ~/.hearth   # this removes your local config — back it up first if you want to reinstall later
```