# openclaw-xiaomi-home

[![Version](https://img.shields.io/badge/version-v1.2.0-blue.svg)](https://github.com/canmaxfire/openclaw-xiaomi-home)
[![ClawHub](https://img.shields.io/badge/ClawHub-openclaw--xiaomi--home-green.svg)](https://clawhub.com/openclaw-xiaomi-home)

**Your OpenClaw can now control your smart home.** Connect to Xiaomi/Mijia devices through Home Assistant and control everything with plain text or voice.

## The Problem It Solves

Smart home devices are scattered across apps:
- Open Mi Home app → find device → tap button

**This skill fixes that.** Just tell your AI what you want:

```
"Turn on the living room light"
"Set bedroom AC to 26 degrees"
"Is the front door locked?"
```

Done.

## What You Can Control

| Category | Examples |
|----------|----------|
| 💡 Lights | On/off, brightness |
| ❄️ Air Conditioning | Temperature, mode, fan speed |
| 🔐 Door Locks | Lock/unlock from anywhere |
| 🌡️ Sensors | Temperature, humidity, motion |
| 💨 Fans & Humidifiers | On/off, speed |
| 🪟 Blinds & Curtains | Open/close |
| 🤖 Robot Vacuums | Start, stop, return to base |
| 🔊 **XiaoAI Speakers** | **Voice announcements (TTS)** |

Works with **1837+ Xiaomi/Mijia devices**.

## How It Works

```
You → "Turn on the light"
  ↓
OpenClaw AI
  ↓
Home Assistant (local)
  ↓
Xiaomi Device
```

All stays **on your local network** — no cloud, no subscription.

## Installation

```bash
# ClawHub
clawhub install openclaw-xiaomi-home

# Manual
git clone https://github.com/canmaxice-maker/openclaw-xiaomi-home.git
mv openclaw-xiaomi-home ~/.openclaw/skills/
```

## Setup (One Time)

### 1. Start Home Assistant

```bash
cd ~/.openclaw/skills/openclaw-xiaomi-home
docker compose up -d
```

Open http://localhost:8123 and create your account.

### 2. Add Xiaomi Devices

1. **Settings → Devices & Services → Add Integration**
2. Search **Xiaomi Home** → login with Xiaomi account
3. Wait for devices to import

### 3. Create Access Token

1. HA profile → **Long-Lived Access Tokens** → Create Token
2. Copy and save it

### 4. Install Control Server

```bash
cd ~/.openclaw/skills/openclaw-xiaomi-home/scripts/ha-mcp-server
npm install && cp .env.example .env
# Edit .env with your HA_URL and HA_TOKEN
```

### 5. Start

```bash
launchctl load ~/.openclaw/skills/openclaw-xiaomi-home/scripts/ha-mcp-server/ai.openclaw.ha-mcp.plist
```

### 6. Test

```bash
node src/call-tool.mjs ping_ha
node src/call-tool.mjs list_all_devices '{"domain":"light"}'
```

## Usage

Just talk to your AI assistant:

```
"Turn on the living room light"
"Set bedroom AC to 26 degrees"
"Is the front door locked?"
"What's the temperature?"
"Lock all doors"
"Turn off all lights"
"Open the blinds"
"Start the vacuum"
```

## XiaoAI TTS Voice Announcement

Use XiaoAI speakers as a voice announcement system — your AI can "speak" reminders and alerts through the speaker.

**⚠️ Note:** Entity IDs are device-specific. You must find your own XiaoAI speaker's `notify` entity in Home Assistant (see [Finding Your Entity IDs](#finding-your-entity-ids) below).

**Python script:** `~/.openclaw/workspace/scripts/xiaoai_announce.py`

```bash
# Find your notify entity ID first (see below), then:
python3 ~/.openclaw/workspace/scripts/xiaoai_announce.py "06:30 该起床了" "notify.YOUR_ENTITY_ID"
```

**MCP tool:** `xiaoai_announce(message, entity_id?)`

**Use cases:** Health reminders, smart home alerts, agent notifications.

### Finding Your Entity IDs

XiaoAI speaker entity IDs are unique to your account. To find them:

1. Open Home Assistant → **Developer Tools → States**
2. Filter by `notify` and look for entities containing `xiaoai`, `play_text`, or `speaker`
3. Copy the entity ID (format: `notify.xiaomi_cn_XXXXXXXXXX_xxxx`)

---

## Security & Privacy

### Required Credentials

| Credential | Purpose | Storage |
|------------|---------|---------|
| `HA_TOKEN` | Home Assistant Long-Lived Access Token | `.env` file (gitignored) |

### Security Model

| Concern | Mitigation |
|---------|------------|
| Unauthenticated access | MCP server requires `Authorization: Bearer <HA_TOKEN>` on every request |
| Cross-origin abuse | CORS restricted to `http://localhost` only |
| LAN access | Server binds to localhost, not all interfaces |
| Token exfiltration | HA_TOKEN is only sent to `localhost:8123` — never to external services |
| Credential leakage | `.env` is in `.gitignore` — never committed to git |

### What This Skill Does NOT Do

- ❌ Does NOT transmit your HA token to any external service
- ❌ Does NOT accept requests from non-localhost origins
- ❌ Does NOT collect, log, or transmit usage data
- ❌ Does NOT use any LLM or AI processing
- ❌ Does NOT expose unauthenticated endpoints

## Troubleshooting

### HA won't start
```bash
docker logs homeassistant
```

### Devices not showing
- Use **China mainland** Xiaomi server in Mi Home
- Restart the homeassistant container

### Token not working
- Re-create the Long-Lived Access Token in HA
- Update `HA_TOKEN` in `.env`

## Credits

- [Home Assistant](https://www.home-assistant.io/)
- [ha_xiaomi_home](https://github.com/nickoowen/ha-xiaomi-home)
- [OpenClaw](https://openclaw.ai/)

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| [v1.2.0](https://github.com/canmaxice-maker/openclaw-xiaomi-home/releases/tag/v1.2.0) | 2026-04-24 | Added XiaoAI TTS voice announcement via `xiaoai_announce` tool |
| [v1.1.0](https://github.com/canmaxice-maker/openclaw-xiaomi-home/releases/tag/v1.1.0) | 2026-04-21 | Plain language rewrite — user benefit focus |
| [v1.0.0](https://github.com/canmaxice-maker/openclaw-xiaomi-home/releases/tag/v1.0.0) | 2026-04-21 | Initial release |

## License

MIT
