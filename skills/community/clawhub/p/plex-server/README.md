# Plex Media Server Manager

An OpenClaw skill for managing Plex Media Server via its HTTP API, with optional Nvidia Shield device management via ADB.

## Features

- **Server discovery** — auto-find all Plex servers on your account, no manual IP needed
- **Rich media search** — search your library with full metadata: resolution, codec, bitrate, audio languages, subtitles, genres, ratings
- **Active session monitoring** — see who's watching what, with progress and device info
- **Library management** — list libraries, trigger scans for new content
- **Health checks** — Plex server status + active sessions
- **Optional ADB** — if your Plex server runs on an Nvidia Shield, manage the device too (reboot, restart Plex, system health)

## Quick Start

### 1. Get your Plex token

You need your Plex authentication token. Here's how to find it:

**Method A — From any media item (easiest):**
1. Open [Plex Web](https://app.plex.tv) in your browser
2. Navigate to any movie or TV episode in your library
3. Click the **"⋯"** (three dots) menu on the media item
4. Select **"Get Info"** → **"View XML"**
5. Look at the URL in your browser's address bar — find `X-Plex-Token=`
6. Copy everything after `X-Plex-Token=` until the next `&` or end of URL

**Method B — From browser developer tools:**
1. Open [Plex Web](https://app.plex.tv) and sign in
2. Press `F12` to open Developer Tools
3. Go to **Application** tab → **Local Storage** → `https://app.plex.tv`
4. Find the key `plexToken` (or search for `myPlexAccessToken`)
5. Copy its value

**Method C — From a Plex XML response:**
1. Visit `https://app.plex.tv/desktop` in your browser
2. Open Developer Tools → **Network** tab
3. Refresh the page and look for any request to `plex.tv`
4. Check the request headers or query parameters for `X-Plex-Token`

> ⚠️ **Important:** Your Plex token grants full access to your account and all servers. Treat it like a password. The skill stores it in `~/.openclaw/shield/config.json` with `chmod 600` permissions.

### 2. Discover your servers

```bash
node scripts/shield-cli.js discover YOUR_PLEX_TOKEN
```

This lists all Plex Media Servers associated with your account, showing:
- Server name, product, version, platform
- Local and remote connection URLs
- Server index (for multi-server setups)

### 3. Configure

```bash
# Single server — auto-discovers and configures
node scripts/shield-cli.js setup YOUR_PLEX_TOKEN

# Multiple servers — pick by index
node scripts/shield-cli.js setup YOUR_PLEX_TOKEN 0   # first server
node scripts/shield-cli.js setup YOUR_PLEX_TOKEN 1   # second server
```

That's it! No username, no password — the token is the universal key for all Plex API calls.

## Usage

### Search Media

```bash
node scripts/shield-cli.js search "Indiana Jones" | node scripts/shield-cli.js format
```

Output includes:
- 🎞️ Type and library
- ⏱️ Duration · 🏷️ Genres · 🏢 Studio · 🎬 Content rating
- ⭐ Rating · 👁️ View count
- 📺 Video quality (resolution, codec, bitrate, container, file size)
- 🔊 Audio tracks (codec, channels, language)
- 💬 Subtitles (codec, language)
- 📝 Plot summary

### Active Sessions

```bash
node scripts/shield-cli.js sessions
```

Shows who's currently streaming, what they're watching, progress, device, and transcoding status.

### Library Management

```bash
# List all libraries
node scripts/shield-cli.js libraries

# Scan a library for new content
node scripts/shield-cli.js scan 1
```

### Health Check

```bash
node scripts/shield-cli.js health
```

Reports Plex server status, version, and active sessions. If ADB is configured, also shows device uptime, memory, disk, and battery.

### Recently Added

```bash
node scripts/shield-cli.js recently-added
```

### Check for Plex Updates

```bash
node scripts/shield-cli.js updater-status
```

## Optional: Nvidia Shield ADB Setup

If your Plex server runs on an Nvidia Shield TV, you can enable device management features (reboot, restart Plex, system health).

### Prerequisites

1. **Enable Developer Options** on your Shield:
   - Go to **Settings** → **Device Preferences** → **About**
   - Click **Build** 7 times until "You are now a developer!" appears

2. **Enable USB Debugging**:
   - Go to **Settings** → **Device Preferences** → **Developer options**
   - Enable **USB debugging**
   - Enable **Debugging over network** (note the IP and port shown, usually `5555`)

3. **Authorize the connection** (one-time):
   ```bash
   adb connect 192.168.70.2:5555
   ```
   A dialog will appear on your Shield TV — check **"Always allow from this computer"** and click **OK**.

### Configure with ADB

```bash
node scripts/shield-cli.js setup YOUR_PLEX_TOKEN 0 192.168.70.2
```

The last argument is your Shield's IP address. The ADB port defaults to `5555`.

### ADB Commands

| Command | Description |
|---------|-------------|
| `connect` | Connect ADB to the Shield |
| `adb-health` | Device health: uptime, memory, disk, battery |
| `reboot` | Reboot the Shield |
| `restart-plex` | Force stop and restart the Plex app |

> 💡 **Tip:** Use a DHCP reservation on your router to give your Shield a fixed IP address. Otherwise the IP may change and ADB will stop working.

## Configuration

All settings are stored in `~/.openclaw/shield/config.json`:

```json
{
  "shield_ip": "192.168.70.2",
  "adb_port": 5555,
  "plex_token": "your-token-here",
  "plex_url": "http://192.168.70.2:32400"
}
```

The file is created with `chmod 600` (owner read/write only).

## Requirements

- **Node.js** ≥ 18
- **curl** (available on macOS and most Linux distributions)
- **ADB** (optional, only for Shield device management) — install via `apt install adb` or Android SDK Platform Tools

## How It Works

### Server Discovery

The skill calls `https://plex.tv/api/resources` with your token. Plex returns an XML document listing every device and server on your account, including local IP addresses and ports. The skill parses this to find your Plex Media Server automatically — no manual IP entry needed.

### Media Search

Search uses three Plex API calls per local result:
1. `/search?query=` — basic search with title, year, type, summary
2. `/library/metadata/<id>` (JSON) — quality metadata: resolution, codec, bitrate, container, file size, duration, studio, rating, genres
3. `/library/metadata/<id>` (XML) — stream-level details: audio language, subtitle language, codec per track

The `format` command renders this into human-readable text with emoji, suitable for any chat platform (Discord, WhatsApp, Telegram, etc.).

## Troubleshooting

**"No Plex servers found"**
- Verify your token is correct (try Method A above)
- Make sure your server is online and claimed to your Plex account

**"Could not determine local IP"**
- Your server might be remote (not on the same network). Use `configure` for manual setup:
  ```bash
  node scripts/shield-cli.js configure SERVER_IP YOUR_PLEX_TOKEN http://SERVER_IP:32400
  ```

**ADB connection fails**
- Make sure USB debugging and network debugging are enabled on the Shield
- Verify the Shield's IP hasn't changed (use DHCP reservation)
- Re-authorize: `adb disconnect && adb connect 192.168.x.x:5555`

**Search returns no results**
- Verify the Plex server is running and reachable
- Check that your libraries are properly configured in Plex

## License

MIT
