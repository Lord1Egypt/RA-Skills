# Home Assistant Integration

Kiwi Voice integrates bidirectionally with [Home Assistant](https://www.home-assistant.io/):

- **HA → Kiwi:** Control Kiwi from the HA dashboard (switches, buttons, sensors)
- **Kiwi → HA:** Control your smart home by voice through Kiwi via the Conversation API

## Installation

1. Copy the custom component to your HA installation:

    ```bash
    cp -r custom_components/kiwi_voice/ /path/to/homeassistant/custom_components/kiwi_voice/
    ```

2. Restart Home Assistant

3. Add the integration via UI: **Settings → Integrations → Add Integration → Kiwi Voice**

4. Enter the Kiwi Voice API URL (e.g., `http://192.168.1.100:7789`)

The integration auto-discovers Kiwi Voice on your network.

## Entities

| Entity | Type | Description |
|--------|------|-------------|
| State | Sensor | Current Kiwi state (idle, listening, thinking, speaking) |
| Language | Sensor | Active language code |
| HA Connected | Binary Sensor | Whether Kiwi is connected to HA |
| Speakers | Sensor | Number of known speaker profiles |
| Uptime | Sensor | Service uptime |
| Listening | Switch | Enable/disable microphone listening |
| Stop | Button | Stop current TTS playback |
| Reset Context | Button | Clear conversation context |
| TTS Test | Button | Speak a test phrase |
| TTS | Platform | Use Kiwi as a TTS platform in HA |

## Voice Control

Say a Home Assistant command through Kiwi:

> **"Kiwi, turn on the lights in the bedroom"**

The command is routed to the Home Assistant Conversation API and the response is spoken back by Kiwi.

## Configuration

### Kiwi Side

```yaml
# config.yaml
homeassistant:
  enabled: true
  url: "http://homeassistant.local:8123"
  token: ""    # Long-Lived Access Token from HA
```

To create a Long-Lived Access Token:

1. Go to your HA profile page
2. Scroll to **Long-Lived Access Tokens**
3. Click **Create Token**
4. Copy the token to `config.yaml`

### HA Side

The custom component connects to Kiwi's REST API and WebSocket for real-time state updates. No additional HA configuration is needed beyond adding the integration.

## REST API

Kiwi also exposes a Home Assistant endpoint:

```bash
# Check HA connection status
curl http://localhost:7789/api/homeassistant/status

# Send a voice command to HA
curl -X POST http://localhost:7789/api/homeassistant/command \
  -H "Content-Type: application/json" \
  -d '{"text": "turn on bedroom lights", "language": "en"}'
```
