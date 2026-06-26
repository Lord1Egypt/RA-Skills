# openclaw-plugin-dg-lab

[![npm version](https://img.shields.io/npm/v/openclaw-plugin-dg-lab.svg)](https://www.npmjs.com/package/openclaw-plugin-dg-lab)
![License](https://img.shields.io/npm/l/openclaw-plugin-dg-lab)
<br>
![Visitor Count](https://count.getloli.com/get/@openclaw-plugin-dg-lab?theme=rule34)

[中文](README.md) | [English](README_EN.md)

An [OpenClaw](https://github.com/openclaw/openclaw) plugin for connecting and controlling **DG-Lab (Coyote) V3** e-stim devices via WebSocket.

## ⚠️ Safety Disclaimer

**This plugin controls an electrical stimulation device. Misuse can cause physical harm.**

- **Never use near the chest, heart, head, or throat.** Follow all DG-Lab official safety guidelines.
- **Always start at the lowest intensity** and increase gradually.
- **Do not use** if you have a pacemaker, heart condition, epilepsy, or are pregnant.
- **Keep the device away from children.** This is an adult product.
- **You are solely responsible** for how you use this plugin. The author assumes no liability for injury, damage, or misuse.
- **The AI emotion engine can trigger stimulation automatically.** Understand this before enabling `/dg_emotion on`.
- **The software intensity limiter is a convenience feature, not a safety guarantee.** Always set safe hardware limits in the DG-Lab App.

**By using this plugin, you acknowledge these risks and agree to use it responsibly.**

## Features

- **Native integration** — runs in-process with the OpenClaw Gateway, no external services needed
- **QR code pairing** — `/dg_qr` generates a scannable QR code for the DG-Lab App to connect
- **AI agent tools** — `dg_shock` and `dg_pulse_list` let the AI directly control stimulation
- **Emotion engine** — `/dg_emotion on` enables automatic stimulation based on keyword analysis of AI replies
- **Intensity limiter** — `/dg_limit` sets a soft cap; also respects device-side hardware limits from the App
- **Safety timer** — auto-shutdown after 1 hour continuous use, 10-minute forced rest
- **Device feedback sync** — real-time strength and limit tracking from the App
- **WebSocket heartbeat** — keeps connections alive
- **Waveform continuity** — long waveforms (>7s) are automatically chunked and sent seamlessly
- **Custom waveform library** — import `.pulses` / `.json5` / `.json` files, compatible with Coyote-Game-Hub format
- **V3 protocol compliant** — uses official frequency compression algorithm and message length limits

## Requirements

- [OpenClaw](https://github.com/openclaw/openclaw) (2026.1+)
- A DG-Lab Coyote V3 device with the official app
- A server with a public IP (or port-forwarded) for WebSocket connections

## Installation


**One-click install (Recommended):**

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/FengYing1314/openclaw-plugin-dg-lab/main/install.sh)"
```

**NPM install:**

```bash
openclaw plugins install openclaw-plugin-dg-lab
```
Or:
```bash
npm install -g openclaw-plugin-dg-lab
```

**Developer / Source Installation:**

```bash
cd ~/.openclaw/workspace/plugins
git clone https://github.com/FengYing1314/openclaw-plugin-dg-lab.git
cd openclaw-plugin-dg-lab
npm install
npm run build

# Link-install the plugin
cd ~/.openclaw/workspace
openclaw plugins install -l ./plugins/openclaw-plugin-dg-lab
```

## Configuration

Add plugin config to `~/.openclaw/openclaw.json`:

```json
{
  "plugins": {
    "entries": {
      "openclaw-plugin-dg-lab": {
        "enabled": true,
        "config": {
          "serverIp": "YOUR_PUBLIC_IP",
          "port": 18888,
          "limitIntensity": 40
        }
      }
    }
  }
}
```

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `serverIp` | string | `127.0.0.1` | Public IP or domain for QR code generation |
| `port` | number | `18888` | WebSocket server port |
| `limitIntensity` | number | `40` | Default intensity soft limit (0-200) |

**Important:** Open TCP port `18888` in your server's firewall!

Then restart:

```bash
openclaw gateway restart
```

## Chat Commands

| Command | Description |
|---------|-------------|
| `/dg_qr` | Generate a QR code for the DG-Lab App to scan and connect |
| `/dg_emotion on/off` | Enable/disable emotion-driven stimulation mode |
| `/dg_limit <0-200>` | Set the intensity soft limit |
| `/dg_test +5` | Manually test a strength adjustment |
| `/dg_status` | Show current plugin state (connections, strength, device limits, queues) |
| `/dg_pulse list` | List all loaded waveform presets |
| `/dg_pulse load <file>` | Import a `.pulses` / `.json5` / `.json` waveform file |
| `/dg_pulse play <name>` | Play a custom waveform preset on channel A |
| `/dg_pulse delete <id>` | Remove a waveform from the library |

## AI Agent Tools

### `dg_shock`

Send stimulation to the connected device.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `strength` | number | ✓ | Intensity delta (+increase, -decrease, 0=reset) |
| `duration` | number | | Waveform duration in ms (default: 1000) |
| `waveform` | string | | `punish` / `tease` / `test` or custom preset name (default: punish) |
| `channel` | string | | `A` / `B` (default: A) |

### `dg_pulse_list`

List all available waveform presets (built-in + custom).

### `dg_qr_generate`

Generate a pairing QR code and return the file path.

## Built-in Waveforms

| Name | Frequency | Intensity | Description |
|------|-----------|-----------|-------------|
| `punish` | ~66Hz (15ms) | 100% constant | High frequency sustained stimulation |
| `tease` | ~5Hz (200ms) | 20-80% sine wave | Low frequency breathing pattern |
| `test` | ~10Hz (100ms) | 50→90→50% ramp | Medium frequency short test |

## Custom Waveforms (Pulse Library)

Place `.pulses`, `.json5`, or `.json` files in the `data/` directory. They are auto-loaded on startup.

**Supported formats:**

1. **Coyote-Game-Hub format** (array of presets):
```json5
[
  { id: 'abc123', name: 'Breathing', pulseData: ['0A0A0A0A00000000', ...] }
]
```

2. **Single preset**: `{ name: "My Wave", pulseData: [...] }`

3. **Raw hex array**: `["0A0A0A0A64646464", ...]`

Each hex string is 16 characters (8 bytes): 4 frequency bytes (compressed, 10-240) + 4 intensity bytes (0-100). Each entry represents 100ms (4 × 25ms windows).

## Emotion Engine

When enabled via `/dg_emotion on`, the plugin analyzes AI reply text for keywords:

| Type | Keywords (examples) | Delta | Waveform |
|------|-------------------|-------|----------|
| Punishing | 罚, 教训, 电击, punish, maximum | +15 | punish (3s) |
| Angry | 生气, 哼, 不听话, angry, warning | +8 | punish (2s) |
| Teasing | 乖, 奖励, 摸摸, good girl, reward | -3 | tease (5s) |

## Architecture

```
DG-Lab App ←── WebSocket ──→ Plugin WS Server ←── OpenClaw Gateway
                                    ↑
                           AI agent calls dg_shock
                          or emotion engine hook
```

1. Plugin starts a WebSocket server on the configured port
2. `/dg_qr` generates a QR code with `https://www.dungeon-lab.com/app-download.php#DGLAB-SOCKET#ws://IP:PORT/CONTROL_ID`
3. DG-Lab App scans the QR code and connects
4. Plugin sends strength (`strength-CH+MODE+VALUE`) and waveform (`pulse-CH:[hex...]`)
5. App reports back real-time strength and limits (`strength-A+B+limitA+limitB`)

## Safety Mechanisms

| Mechanism | Description |
|-----------|-------------|
| **Software intensity limit** | All strength changes clamped to `min(pluginLimit, deviceLimit)` |
| **Device limit sync** | Respects hardware limits set in the DG-Lab App |
| **1-hour auto-rest** | Emotion mode forces 10-minute cooldown after 60 minutes |
| **Graceful shutdown** | All channels reset to 0 on plugin stop |
| **Message length check** | Commands exceeding 1950 chars (protocol limit) are dropped |
| **Max 7s per chunk** | Waveforms auto-split into ≤70 frames per send |
| **Heartbeat** | 20s WebSocket keepalive |
| **Disconnect cleanup** | Intensity tracking resets on device disconnect |

## Protocol Reference

This plugin implements the [DG-Lab V3 Socket Control Protocol](https://github.com/DG-LAB-OPENSOURCE/DG-LAB-OPENSOURCE/blob/main/socket/README.md) and uses the [V3 frequency compression algorithm](https://github.com/DG-LAB-OPENSOURCE/DG-LAB-OPENSOURCE/blob/main/coyote/extra/README.md).

## License

MIT © [FengYing](https://github.com/FengYing1314)
