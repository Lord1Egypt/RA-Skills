# KoKonna Frame Control for OpenClaw

Control your KoKonna AI e-ink art frames from OpenClaw.

## Installation

```bash
openclaw skill install kokonna-frame
```

Or install from source:

```bash
git clone https://github.com/kokonna/openclaw-skill-kokonna-frame.git
cp -r openclaw-skill-kokonna-frame ~/.openclaw/skills/kokonna-frame
```

## Configuration

1. Create config file:
```bash
mkdir -p ~/.openclaw/skills/kokonna-frame
cp config.yaml.example ~/.openclaw/skills/kokonna-frame/config.yaml
```

2. Edit `config.yaml` and add your API keys:
```yaml
api_base_url: "https://api.galaxyguide.cn/openapi"
devices:
  living_room: "your-api-key-here"
```

Get your API key from [kokonna.art](https://kokonna.art).

## Usage

Once installed, tell your OpenClaw agent:

- "Send this image to my living room frame"
- "Push a sunset to the bedroom frame"
- "What's the battery level on my frame?"
- "Show this on KoKonna"

## Features

- 🖼️ **Automatic Resizing**: Images auto-fit your frame's display
- 📝 **Custom Names**: Give images meaningful names
- 🔋 **Device Status**: Check battery, online status, firmware
- 🏠 **Multi-Frame**: Control multiple KoKonna frames

## Requirements

```bash
pip install requests Pillow
```

## About KoKonna

KoKonna is an AI-powered e-ink art frame that blends into your home as both art and intelligent display.

- **E-ink Display**: Paper-like, low power consumption
- **AI Art**: Generates artwork based on your preferences
- **OpenClaw Integration**: Full AI assistant control

Visit [kokonna.art](https://kokonna.art) to learn more.

## License

MIT License

## Support

- Email: support@kokonna.art
- Website: https://kokonna.art
