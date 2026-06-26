---
name: mijia-control
description: |
  Control Xiaomi Mi Home (米家) smart devices via Xiaomi Cloud API.
  Use when: user wants to control smart home devices (lights, AC, heater, bath heater, switches, etc.),
  check device status, or create automation scenes.
  Triggers: "开灯", "关灯", "开空调", "关空调", "开浴霸", "我要洗澡", "设备状态",
  "创建场景", "自动化", "米家", "smart home", "turn on/off", any home device control request.
  NOT for: non-Xiaomi devices, HomeKit-only devices.
---

# Mi Home (米家) Control

Control Xiaomi smart home devices and create automations via cloud API.

## Setup

**Prerequisites:** `pip3 install micloud`

**Credentials:** `~/.mijia_creds.json` (chmod 600)
```json
{"userId":"...", "serviceToken":"...", "ssecurity":"...", "cUserId":"..."}
```

If login requires 2FA (device trust verification), obtain credentials via browser:
1. Open `https://account.xiaomi.com/pass/serviceLogin?sid=xiaomiio&_json=true` in browser with existing cookies
2. POST to `serviceLoginAuth2` with hash password to get `ssecurity` + `location`
3. Follow `location` URL to get `serviceToken` from cookies

## Device Control

### List devices
```bash
python3 scripts/mijia.py devices
```

### Read property
```bash
python3 scripts/mijia.py get <did> <siid> <piid>
```

### Set property
```bash
python3 scripts/mijia.py set <did> <siid> <piid> <value>
# value: true/false for bool, integer for uint8, etc.
```

**Note:** Mesh devices (BLE switches) return code:1 on set — this is normal (async confirmation). The command still executes. Verify by reading the property after a 1-2 second delay.

### Batch control
Create a JSON file with commands:
```json
[
  {"did": "946635824", "siid": 2, "piid": 1, "value": true},
  {"did": "946633803", "siid": 2, "piid": 1, "value": false}
]
```
```bash
python3 scripts/mijia.py batch /tmp/commands.json
```

## MIoT Spec Reference

Each device has services (siid) → properties (piid). Look up specs at:
`https://home.miot-spec.com/spec/<model>`

Common patterns:
- **Switch/Light:** siid:2 piid:1 = on/off (bool)
- **3-way switch:** siid:2/3/4 piid:1 = channel 1/2/3 (bool)
- **AC:** siid:2 piid:1 = on/off, piid:2 = mode, piid:3 = target temp
- **Bath heater:** siid:2 = light, siid:3 = PTC heater, siid:10 = environment (temp sensor)
- **Water heater:** siid:2 piid:1 = on/off, piid:2 = target temp, piid:3 = current temp

## Create Automation Scenes

```bash
python3 scripts/mijia.py scene_create scene.json
```

Scene JSON format (see `references/scene_template.json`):
```json
{
  "name": "回家自动开灯",
  "identify": "homelight_1234",
  "st_id": 8,
  "setting": {"enable": 1, "enable_push": 0},
  "trigger": {
    "key": "event.<did>.<siid>.<eiid>",
    "did": "<trigger_device_did>",
    "model": "<model>",
    "extra": "{\"siid\":2,\"eiid\":1}"
  },
  "action_list": [
    {
      "did": "<target_device_did>",
      "model": "<model>",
      "extra": "{\"props\":[{\"siid\":2,\"piid\":1,\"value\":true}]}",
      "type": "device_ctrl"
    }
  ]
}
```

Key fields:
- `trigger.key`: format `event.<did>.<siid>.<eiid>` for device events
- `launch.attr_filter`: optional conditions (e.g., only if light is off)
- `action_list[].extra`: JSON string with `props` array
- `st_id`: 8 = user automation
- `home_id` and `uid` are auto-filled if omitted

## Predefined Scenes

### 🚿 Bath Mode (洗澡模式)
When user says "我要洗澡":
1. Read bathroom temp: `get 927361805 10 1`
2. If temp < 28°C → turn on bath heater: `set 927361805 3 1 1` (暖风), target 30°C
3. If temp ≥ 28°C → skip heater
4. Turn on water heater: `set 965879649 2 1 1`, set 43°C: `set 965879649 2 2 43`
5. Turn on bathroom light: `set 946635824 2 1 true`

### 🐟 Auto Fish Feeding (出门自动喂鱼)
Feeds fish once per day when BOSS leaves home.

**Architecture:**
1. **OpenClaw cron** (every 5min): polls door lock event log via `/user/get_user_device_data`
2. If today has an auto-lock event (action=1) AND not fed yet → feed fish → record state
3. After feeding, all subsequent checks skip immediately (daily dedup)
4. **State file** `~/.fish_feed_state.json`: tracks last feed date

**Components:**
- Door lock events: 智能门锁2 Pro (did: 1175215651), event key `2.1020`, action=1 = auto-lock (leaving home)
- Fish feeder: 智能鱼缸 (did: 2026943875), action siid:2 aiid:1, in:[1] (1 portion)
  - ⚠️ Action 参数格式: `"in": [1]` 而不是 `[{"piid":5,"value":1}]`
- Script: `scripts/fish_auto_feed.py`

**Manual commands:**
```bash
python3 scripts/fish_auto_feed.py              # Normal run
python3 scripts/fish_auto_feed.py --dry-run    # Check without feeding
python3 scripts/fish_auto_feed.py --force      # Feed regardless
python3 scripts/fish_auto_feed.py --status     # Show state
```

**Trigger logic:**
- Polls lock event log for auto-lock (action=1) today → feed fish
- Once fed, skips all further checks until next day
- No米家自动化 needed, pure OpenClaw polling

## 小爱音箱 TTS

Make the XiaoAI speaker say something aloud.

```bash
python3 scripts/mijia.py tts <did> "<text>"
# Example: python3 scripts/mijia.py tts 100783118 "你好"
```

Flow: unmute → play-text → wait → pause playback → re-mute.
This prevents the speaker from auto-playing music after TTS.

**Important:**
- Speaker may be muted (default state at night) — script handles unmute/re-mute automatically
- After TTS, always pause playback to prevent auto-music
- Cloud API cannot control screen UI — returning to clock display requires physical tap or voice command

## Token Refresh

Tokens expire periodically. If API returns decode errors or auth failures:
1. Re-login via browser (same flow as initial setup)
2. Update `~/.mijia_creds.json` with new `serviceToken` and `ssecurity`

The `ssecurity` changes each login. The `serviceToken` is session-bound.
