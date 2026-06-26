# OpenClaw Panel — OpenClaw Skill

Control an [OpenClaw Panel](https://github.com/joaquinckronoset/openclawpanel) LED panel (64x32 HUB75 on ESP32-S3) from OpenClaw.

Display text, numbers, shapes, graphs, dashboard panels, and play sounds — all via HTTP from any OpenClaw channel (WhatsApp, Telegram, Slack, etc.).

## Installation

### From ClawHub
```bash
clawhub install openclawpanel-skill
```

### From Git
```bash
cd ~/.openclaw/skills
git clone https://github.com/joaquinckronoset/openclawpanel-skill.git
```

## Configuration

Add the panel's IP address to your OpenClaw config (`~/.openclaw/openclaw.json`):

```json
{
  "skills": {
    "entries": {
      "openclawpanel": {
        "enabled": true,
        "env": {
          "OPENCLAW_PANEL_IP": "192.168.1.50"
        }
      }
    }
  }
}
```

Replace `192.168.1.50` with your panel's actual IP (shown on the panel during boot, or check your router's DHCP table).

## Requirements

- OpenClaw Panel with firmware v0.0.1+ (includes the full HTTP API with line, bitmap, dissolve, WAV upload)
- Panel and OpenClaw host on the same local network
- `curl` available on the host machine

## Usage examples

Talk to your OpenClaw agent:

- "Show HELLO in green on the panel"
- "Play the coin sound"
- "Play this WAV file on the panel"
- "Draw a red circle in the center of the panel"
- "Draw a diagonal line across the panel"
- "Show Bitcoin price at 64,770 with a chart"
- "Fade to a new screen with dissolve effect"
- "Set panel brightness to 30%"
- "What sounds are available?"
- "Reset the panel to normal"

## API Reference

See [SKILL.md](SKILL.md) for the complete HTTP API documentation.

## License

MIT
