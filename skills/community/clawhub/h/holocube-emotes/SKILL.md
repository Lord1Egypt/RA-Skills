---
name: holocube-emotes
description: Control a GeekMagic holocube display as an AI emote system. Generate holographic sprite kits with Gemini, upload to device, and swap expressions based on agent state (idle, working, error, etc.). Use when the user has a GeekMagic holocube (HelloCubic-Lite or similar) and wants their AI assistant to have a physical face that reacts to conversation context.
---

# Holocube Emotes

Turn a GeekMagic holocube into your AI's face. Generate holographic character sprites, upload them to the device, then swap expressions in real-time based on agent/session state.

## First-Time Setup

### 0. Find the device

Auto-discover holocubes on your network:

```bash
python3 scripts/holocube.py --discover
```

Output: `FOUND: 192.168.0.245 — HelloCubic-Lite V7.0.22`

If discovery fails, find the IP on the device's screen or your router's client list.

### 1. Generate sprites

Create a full emote sprite kit (requires nano-banana-pro skill with `GEMINI_API_KEY`):

```bash
python3 scripts/generate_sprites.py --output-dir ./sprites
```

Custom character:
```bash
python3 scripts/generate_sprites.py --output-dir ./sprites \
  --character "A glowing holographic cat floating in pure black void. Neon purple wireframe style."
```

This generates 7 emotes (neutral, happy, thinking, surprised, concerned, laughing, sleeping) as both static JPG and animated GIF, sized for the 240x240 display.

### 2. Upload to device

```bash
python3 scripts/setup_device.py --sprites-dir ./sprites --clear --backup-dir ./backup
```

Flags:
- `--clear` removes existing images (recommended — device has ~3MB storage)
- `--backup-dir` saves existing files before clearing
- `--ip` auto-discovers if not provided, or specify manually

### 3. Configure TOOLS.md

Add the holocube IP and emote mappings to your workspace TOOLS.md for reference. See references/tools-example.md.

## Daily Usage

### Set emote directly

```bash
python3 scripts/holocube.py happy
python3 scripts/holocube.py thinking --static   # Use JPG instead of GIF
```

### Set by agent state

```bash
python3 scripts/holocube.py working    # → thinking
python3 scripts/holocube.py complete   # → happy
python3 scripts/holocube.py error      # → concerned
python3 scripts/holocube.py opus       # → thinking (heavy model)
python3 scripts/holocube.py haiku      # → neutral (light model)
```

### Auto-select by time of day

```bash
python3 scripts/holocube.py --auto
```

- 11pm–7am → sleeping
- 7am–9am → happy
- Rest of day → neutral

### Check status

```bash
python3 scripts/holocube.py --status
python3 scripts/holocube.py --list
```

## Heartbeat Integration

Add to HEARTBEAT.md to auto-manage the emote:

```markdown
## Holocube Emote Check
- Run `python3 scripts/holocube.py --auto` to set time-appropriate emote
```

## When to Set Emotes

Use these during normal agent operations:

| Context | Command | Emote |
|---|---|---|
| Idle, waiting for input | `neutral` | 🤖 |
| Processing, running tools | `thinking` or `working` | 🔧 |
| Task completed | `happy` or `complete` | 😊 |
| Error occurred | `error` (→ surprised) | 😮 |
| Funny moment | `laughing` or `funny` | 😂 |
| Unexpected input | `surprised` or `unexpected` | 😮 |
| Night/inactive | `sleeping` or `night` | 😴 |
| Spawning sub-agent | `spawning` (→ thinking) | 🔧 |
| On-demand custom | `custom` | ✨ |

## Custom Slot

A reserved file `adam-custom.gif` on the device can be overwritten at any time for on-demand or one-off animations. Generate a GIF, upload as `adam-custom.gif`, then `python3 holocube.py custom`. Switch back to a standard emote when done.

## Device Notes

- **Model:** GeekMagic HelloCubic-Lite (240x240px glass display)
- **Format:** GIF (animated) or JFIF JPEG. Use Pillow for JPEG (ffmpeg lacks JFIF headers).
- **Storage:** ~3MB total. 6 animated GIFs use ~1.5MB, leaving ~500KB for custom slot.
- **Art style:** Dark/black backgrounds make glass disappear. Use glowing, holographic, neon elements.
- **⚠️ NEVER send `/set?reset=1`** — that's factory reset, wipes WiFi config.

## Requirements

- GeekMagic HelloCubic-Lite (or compatible) on local network
- Python 3 with Pillow (`pip install Pillow`)
- nano-banana-pro skill with `GEMINI_API_KEY` (for sprite generation only)
- `uv` (`brew install uv`) (for sprite generation only)
