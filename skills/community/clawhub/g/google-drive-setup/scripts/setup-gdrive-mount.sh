#!/bin/bash
# Setup Google Drive mount via rclone using gog's OAuth credentials
# Usage: ./setup-gdrive-mount.sh <gmail> <mount-point>
#
# Prerequisites:
#   - gog CLI authenticated with the Gmail account
#   - GOG_KEYRING_PASSWORD set in environment
#   - rclone installed

set -euo pipefail

EMAIL="${1:?Usage: $0 <gmail> <mount-point>}"
MOUNT="${2:?Usage: $0 <gmail> <mount-point>}"

# Step 1: Export token from gog
echo "==> Exporting OAuth token from gog..."
gog auth tokens export "$EMAIL" --out /tmp/gog_token.json --overwrite

# Extract values
REFRESH_TOKEN=$(python3 -c "import json; print(json.load(open('/tmp/gog_token.json'))['refresh_token'])")
CLIENT_ID=$(python3 -c "import json; print(json.load(open('$HOME/.config/gogcli/credentials.json'))['client_id'])")
CLIENT_SECRET=$(python3 -c "import json; print(json.load(open('$HOME/.config/gogcli/credentials.json'))['client_secret'])")

# Step 2: Get access token
echo "==> Refreshing access token..."
TOKEN_JSON=$(curl -s -X POST https://oauth2.googleapis.com/token \
  -d "client_id=$CLIENT_ID" \
  -d "client_secret=$CLIENT_SECRET" \
  -d "refresh_token=$REFRESH_TOKEN" \
  -d grant_type=refresh_token)

ACCESS_TOKEN=$(echo "$TOKEN_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['access_token'])")
EXPIRY=$(date -u -d "+3600 seconds" +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || python3 -c "from datetime import datetime,timedelta; print((datetime.utcnow()+timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%SZ'))")

# Step 3: Write rclone config
echo "==> Writing rclone config..."
mkdir -p ~/.config/rclone
cat > ~/.config/rclone/rclone.conf <<EOF
[GoogleDrive]
type = drive
client_id = $CLIENT_ID
client_secret = $CLIENT_SECRET
scope = drive
token = {"access_token":"$ACCESS_TOKEN","token_type":"Bearer","refresh_token":"$REFRESH_TOKEN","expiry":"$EXPIRY"}
team_drive =
EOF

# Step 4: Verify
echo "==> Verifying connection..."
rclone lsd GoogleDrive: >/dev/null 2>&1 && echo "✅ Google Drive connected!" || { echo "❌ Connection failed"; exit 1; }

# Step 5: Setup systemd auto-mount
echo "==> Setting up systemd auto-mount at $MOUNT..."
mkdir -p "$MOUNT"

cat > /etc/systemd/system/rclone-gdrive.service <<EOF
[Unit]
Description=rclone mount Google Drive
After=network-online.target
Wants=network-online.target

[Service]
Type=notify
ExecStart=/usr/bin/rclone mount GoogleDrive: $MOUNT --vfs-cache-mode full --vfs-cache-max-size 2G --dir-cache-time 72h --allow-other
ExecStop=/bin/fusermount -u $MOUNT
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable rclone-gdrive
systemctl start rclone-gdrive

# Cleanup
rm -f /tmp/gog_token.json
echo "✅ Google Drive mounted at $MOUNT (auto-mount on boot enabled)"
