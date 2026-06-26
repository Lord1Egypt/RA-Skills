# Detailed Installation Guide

## Prerequisites

- Docker Desktop 4.x+
- Xiaomi account with Mi Home app and linked devices
- (Optional) Xiaomi Central Hub Gateway for local control

## Step 1: Install Docker Desktop

Download from: https://docs.docker.com/desktop/setup/install/mac-install/

After installation, ensure Docker is running (whale icon in menu bar).

## Step 2: Clone and Setup the Skill

```bash
git clone https://github.com/YOUR_USERNAME/openclaw-xiaomi-home.git
cd openclaw-xiaomi-home
```

## Step 3: Configure mcporter

Add the MCP server to your mcporter config:

```bash
mcporter config add ha-mcp \
  --stdio "cd /path/to/openclaw-xiaomi-home/scripts/ha-mcp-server && npm start"
```

Or add it manually to `~/.openclaw/config/mcporter.json`:

```json
{
  "servers": {
    "ha-mcp": {
      "command": "node",
      "args": ["/path/to/openclaw-xiaomi-home/scripts/ha-mcp-server/dist/index.js"],
      "env": {
        "HA_URL": "http://localhost:8123",
        "HA_TOKEN": "your_long_lived_token"
      }
    }
  }
}
```

## Step 4: Get Home Assistant Token

1. Open Home Assistant: http://localhost:8123
2. Create account / Login
3. Profile (your username) → Security
4. Create Long-Lived Access Token
5. Copy the token

## Step 5: Update .env

Edit `scripts/ha-mcp-server/.env`:

```
HA_URL=http://localhost:8123
HA_TOKEN=your_copied_token_here
PORT=3002
```

## Step 6: Install ha_xiaomi_home Integration

1. Home Assistant → Settings → Devices & Services
2. Add Integration → Search "Xiaomi Home"
3. Click "Xiaomi Home" → Continue
4. Login with Xiaomi account
5. Select your home and devices to import

## Step 7: Test

After HA restarts and devices are imported, test:

```bash
mcporter call ha-mcp.list_all_devices
mcporter call ha-mcp.ping_ha
```

## Troubleshooting

### HA Container Won't Start

Check logs:
```bash
docker logs homeassistant
```

### Can't Login to Xiaomi

The Xiaomi Cloud API may be blocked in your region. Use a VPN or enable LAN control in the integration settings.

### Devices Not Showing

- Ensure devices are added to Mi Home app first
- Check if device type is supported (no BLE/IR devices)
- Try re-authorizing the Xiaomi account in integration settings

## Updating

```bash
cd openclaw-xiaomi-home
git pull
cd scripts/ha-mcp-server
npm install && npm run build
docker compose restart homeassistant
```
