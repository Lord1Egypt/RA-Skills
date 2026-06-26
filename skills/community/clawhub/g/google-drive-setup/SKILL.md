---
name: google-drive-setup
description: Configure Google Drive mount on Linux via rclone + gog OAuth. Use when user wants to mount Google Drive as local filesystem, set up auto-mount on boot, or configure rclone with Google OAuth. Covers OAuth setup with gog, rclone configuration, and systemd auto-mount.
---

# Google Drive Setup

Mount Google Drive as a local filesystem using rclone, with OAuth via gog CLI.

## Prerequisites

- `gog` CLI installed and authenticated (see gog skill)
- `rclone` installed
- `fuse` / `fusermount` available

## Step 1: Get OAuth Credentials from gog

gog already has a valid refresh token. Export it:

```bash
export GOG_KEYRING_PASSWORD=<your-password>
gog auth tokens export <email@gmail.com> --out /tmp/gog_token.json --overwrite
```

Extract the refresh_token, client_id, and client_secret from:
- `/tmp/gog_token.json` → refresh_token
- `~/.config/gogcli/credentials.json` → client_id, client_secret

## Step 2: Configure rclone

Write `~/.config/rclone/rclone.conf`:

```ini
[GoogleDrive]
type = drive
client_id = <client_id>
client_secret = <client_secret>
scope = drive
token = {"access_token":"","token_type":"Bearer","refresh_token":"<refresh_token>","expiry":"2026-01-01T00:00:00Z"}
team_drive =
```

Manually refresh the access token (rclone will auto-refresh thereafter):

```bash
curl -s -X POST https://oauth2.googleapis.com/token \
  -d client_id=<client_id> \
  -d client_secret=<client_secret> \
  -d refresh_token=<refresh_token> \
  -d grant_type=refresh_token
```

Update rclone.conf with the returned access_token and real expiry time.

Verify: `rclone lsd GoogleDrive:`

## Step 3: Mount to Filesystem

```bash
mkdir -p /mnt/gdrive
rclone mount GoogleDrive: /mnt/gdrive \
  --daemon \
  --vfs-cache-mode full \
  --vfs-cache-max-size 2G \
  --dir-cache-time 72h \
  --allow-other
```

## Step 4: Auto-mount on Boot (systemd)

Create `/etc/systemd/system/rclone-gdrive.service`:

```ini
[Unit]
Description=rclone mount Google Drive
After=network-online.target
Wants=network-online.target

[Service]
Type=notify
ExecStart=/usr/bin/rclone mount GoogleDrive: /mnt/gdrive --vfs-cache-mode full --vfs-cache-max-size 2G --dir-cache-time 72h --allow-other
ExecStop=/bin/fusermount -u /mnt/gdrive
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable:

```bash
systemctl daemon-reload
systemctl enable rclone-gdrive
systemctl start rclone-gdrive
```

## Troubleshooting

- **"empty token found"**: rclone config has no valid token. Re-do Step 2.
- **"token expired and no refresh token"**: refresh_token missing from rclone.conf.
- **"Object does not exist at path /"**: gog keyring backend issue. Switch to file: `gog auth keyring file` and set `GOG_KEYRING_PASSWORD`.
- **"access_denied" / "developer hasn't given you access"**: Add user as test user in Google Cloud Console → OAuth consent screen.
- **OAuth app type must be "Desktop app"**: Web-type credentials redirect_uri won't work for remote servers. Use Desktop type.
