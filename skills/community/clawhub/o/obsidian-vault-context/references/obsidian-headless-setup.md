# Obsidian Headless Sync Setup

Connect your Obsidian vault to a server for bidirectional sync with your AI agent.

## What This Does

[Obsidian Headless](https://obsidian.md/help/sync/headless) is Obsidian's official headless sync client (open beta). It syncs your vault bidirectionally without the desktop app:

- You edit on Mac/iPhone/iPad -> change appears on server within seconds
- Agent writes on server -> change appears in your Obsidian app on all devices

Uses the same encryption and privacy protections as the desktop app, including end-to-end encryption.

## Prerequisites

- Linux server (Ubuntu 22+ recommended), macOS, or Windows
- Node.js 18+ (N-API v3 stable)
- [Obsidian Sync subscription](https://obsidian.md/sync) ($4/month for Standard, $8/month for Plus)
- Your Obsidian account credentials

## Installation

```bash
npm install -g obsidian-headless
```

## Setup

```bash
# Login to your Obsidian account
ob login

# List your remote vaults
ob sync-list-remote

# Navigate to (or create) the local vault directory
mkdir -p ~/.openclaw/vault
cd ~/.openclaw/vault

# Connect to your remote vault
ob sync-setup --vault "Your Vault Name" --device-name "openclaw-server"

# Test a one-time sync
ob sync

# Run continuous sync (watches for changes)
ob sync --continuous
```

### Sync Modes

Configure how sync behaves:

```bash
# Default: bidirectional (both sides read and write)
ob sync-config --mode bidirectional

# Pull-only: server only downloads, ignores local changes
ob sync-config --mode pull-only

# Mirror remote: server downloads and reverts any local changes
ob sync-config --mode mirror-remote
```

For agent collaboration, use `bidirectional` (the default) so the agent can write output that syncs back to your devices.

### Selective Sync

Exclude folders or limit what syncs:

```bash
# Exclude large folders the agent doesn't need
ob sync-config --excluded-folders ".obsidian/plugins,.trash"

# Only sync markdown and images (skip audio, video, PDF)
ob sync-config --file-types "image"
```

## Running as a systemd Service

For continuous sync on a Linux server:

```bash
sudo tee /etc/systemd/system/obsidian-sync.service << 'EOF'
[Unit]
Description=Obsidian Headless Sync
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/.openclaw/vault
ExecStart=/usr/local/bin/ob sync --continuous --path /home/ubuntu/.openclaw/vault
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable obsidian-sync
sudo systemctl start obsidian-sync
```

Verify:
```bash
sudo systemctl status obsidian-sync
# Should show "active (running)"
```

## Verifying the Loop

Test bidirectional sync:

1. **You -> Agent**: Edit a file in Obsidian on your phone. SSH into the server and check:
   ```bash
   cat /home/ubuntu/.openclaw/vault/path/to/file.md
   ```

2. **Agent -> You**: Create a test file on the server:
   ```bash
   echo "# Sync Test" > /home/ubuntu/.openclaw/vault/work/sync-test.md
   ```
   Open Obsidian on your phone. The file should appear within seconds.

3. **Check status**:
   ```bash
   ob sync-status --path /home/ubuntu/.openclaw/vault
   ```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `ob login` fails | Verify your Obsidian account credentials. Check Sync subscription is active. |
| `ob sync-list-remote` shows nothing | You need at least one remote vault created from the Obsidian desktop app first. |
| Files not appearing | Check vault path. Ensure the service user has write permissions. Run `ob sync-status`. |
| Conflicts on same file | Obsidian Sync creates a `conflict-TIMESTAMP` copy. Avoid editing the same file simultaneously. |
| Service crashes | Check `journalctl -u obsidian-sync -f` for errors. |
| Large vault slow initial sync | First sync of a large vault (400+ files) can take 2-5 minutes. Subsequent syncs are incremental. |
| E2E encryption password prompt | Pass `--password` to `ob sync-setup` or it will prompt interactively (won't work in systemd). |

## Security Notes

- **Isolate the vault from agent code.** The synced vault directory should contain only content files (notes, orchestration files, output). Agent skills, SOUL.md, and workflow definitions should live in a separate directory that the agent cannot write to via sync. Do not point your agent's workspace/repoRoot at the vault.
- **Run the sync service as a dedicated, unprivileged user.** Avoid storing other secrets or credentials in the same home directory.
- `ob login` stores credentials locally. Secure the server accordingly.
- End-to-end encryption is supported — use `--encryption e2ee` when creating vaults.
- Use selective sync to exclude sensitive folders (e.g., `company/legal/`, `.obsidian/`).
- If using Cloudflare Tunnel, the vault is not exposed to the internet directly.
- Consider encrypting the server's disk if the vault contains sensitive data.

## Useful Commands

```bash
# Check sync status
ob sync-status --path /home/ubuntu/.openclaw/vault

# Disconnect vault from sync
ob sync-unlink --path /home/ubuntu/.openclaw/vault

# List locally configured vaults
ob sync-list-local

# Create a new remote vault with E2E encryption
ob sync-create-remote --name "Agent Vault" --encryption e2ee
```
