---
name: native-install
description: Install the Mobazha native binary on Linux, macOS, or Windows. Use when the user wants to run a store without Docker.
---

# Native Binary Installation

Install Mobazha as a single native binary — no Docker, no runtime dependencies. Works on Linux (x86_64 & ARM64), macOS (Apple Silicon & Intel), and Windows.

**Official guide**: <https://mobazha.org/self-host> (Native Binary tab) and <https://mobazha.org/download>

## Quick Install

> **Security note**: The install commands below download and execute a shell script from `get.mobazha.org`. Before running, you can review the script with `curl -sSL https://get.mobazha.org/install | less`. Only proceed if the user confirms they trust the source.

### Linux & macOS

```bash
curl -sSL https://get.mobazha.org/install | bash
```

This downloads the `mobazha` binary (and the `mobazha-launcher` for auto-update) to `~/.local/bin/` and starts the store as a background service.

### Windows

1. Go to <https://mobazha.org/download>
2. Download the `.zip` file for Windows
3. Extract the archive
4. Double-click `mobazha-tray.exe` to start

The Windows desktop app includes a system tray icon and auto-opens your browser to the store admin.

## What the Installer Does

1. Detects your OS and architecture (linux/darwin, amd64/arm64)
2. Downloads the matching binary from GitHub Releases
3. Verifies the SHA-256 checksum
4. Places binaries in `~/.local/bin/` (or custom `--dir`)
5. Downloads the launcher binary (crash recovery + auto-update) if available
6. Registers and starts as a background service (unless `--no-start` is passed)

After install, the store is accessible at `http://localhost:5102` (or `http://<public-ip>:5102` for VPS).

## Running Your Store

### Foreground mode

```bash
mobazha start
```

The store API and Web UI are served on port **5102** by default: `http://localhost:5102`.

### Background service (recommended)

The installer registers a service automatically. Manage it with:

```bash
mobazha service status     # Check if running
mobazha service stop       # Stop the service
mobazha service start      # Start the service
mobazha service install    # Re-install / re-register the service
mobazha service uninstall  # Remove the service
```

On Linux this uses systemd (user-mode when possible), on macOS it uses launchd.

### With a custom domain

The native binary itself does not include a reverse proxy. To use a custom domain with HTTPS, deploy via the **standalone Docker** setup instead (see `standalone-setup` skill), or manually configure a reverse proxy (Caddy, Nginx) in front of port 5102.

## Install Options

| Flag | Description |
|------|-------------|
| `--version <tag>` | Install a specific version (e.g., `v0.3.0-beta.15`) |
| `--dir <path>` | Custom install directory (default: `~/.local/bin`) |
| `--no-start` | Download only, don't register or start the service |

## Backup

```bash
mobazha backup -o ~/mobazha-backup.tar.gz
```

## Uninstall

Remove the binary and service (keeps your store data):

```bash
curl -sSL https://get.mobazha.org/install | bash -s -- --uninstall
```

Remove everything including data:

```bash
curl -sSL https://get.mobazha.org/install | bash -s -- --uninstall --purge
```

## Platform Notes

### macOS

- Installs via `curl | bash`, which bypasses Gatekeeper (no Apple Developer signing required)
- The launcher registers as a launchd LaunchAgent for auto-start on login
- Supports both Apple Silicon (arm64) and Intel (amd64)

### Linux ARM64

- Works on Raspberry Pi 4+ and ARM VPS instances
- Same install command — the script auto-detects architecture

### Running Behind NAT

- No port forwarding needed for basic operation
- Your store stays reachable via the Mobazha P2P network
- For a direct public URL, use the **standalone Docker** setup with a domain, or enable Tor overlay

## After Installation

1. Open `http://localhost:5102/admin` (or `http://<your-ip>:5102/admin` for VPS)
2. Complete the **Setup Wizard** — set admin password, store name, visibility, region/currency (see `store-onboarding` skill for the full walkthrough)
3. Add products and start selling
4. (Optional) Connect your AI agent to the store via MCP — see `store-mcp-connect` skill

## Troubleshooting

### Binary not found after install

Ensure `~/.local/bin` is in your PATH:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc
```

### Permission denied

The installer needs write access to the install directory. Use `--dir` to specify a writable location, or run with appropriate permissions.

### macOS "unverified developer" warning

This shouldn't happen with `curl | bash` install. If running a downloaded binary directly, use:

```bash
xattr -d com.apple.quarantine ./mobazha
```

### Check service logs

```bash
# Linux
journalctl --user -u mobazha -f

# macOS
tail -f ~/Library/Logs/Mobazha/mobazha.log
```
