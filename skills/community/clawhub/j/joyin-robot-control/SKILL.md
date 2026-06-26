---
name: joyin-robot-control
description: Control JoyIn AI robots (W-1 Walle / M-1 Mini) — movement, follow, photo, video, live stream, TTS, agent config, and device status via OpenAPI.
metadata: {"openclaw": {"requires": {"bins": ["python3"], "env": ["JOYIN_API_BASE", "JOYIN_AUTH_KEY", "JOYIN_DEVICE_SN"]}, "primaryEnv": "JOYIN_AUTH_KEY"}}
---

# JoyIn Robot Control

Control JoyIn AI robots through the official OpenAPI. Supports **W-1 (Walle)** and **M-1 (Mini)** robots.

## Setup

### OpenClaw Configuration

Add the following to `~/.openclaw/openclaw.json`:

```json5
{
  "skills": {
    "entries": {
      "joyin-robot-control": {
        "enabled": true,
        "apiKey": "YOUR_AUTH_KEY",
        "env": {
          "JOYIN_API_BASE": "https://api-open-test.joyin-ai.com",
          "JOYIN_AUTH_KEY": "YOUR_AUTH_KEY",
          "JOYIN_DEVICE_SN": "YOUR_DEVICE_SN",
          "JOYIN_DEVICE_TYPE_ID": "3"
        }
      }
    }
  }
}
```

See `{baseDir}/openclaw.config.example.json5` for a full template.

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `JOYIN_API_BASE` | Yes | API base URL (test: `https://api-open-test.joyin-ai.com`) |
| `JOYIN_AUTH_KEY` | Yes | Authorization key (contact JoyIn staff to obtain) |
| `JOYIN_DEVICE_SN` | Yes | Target device serial number |
| `JOYIN_DEVICE_TYPE_ID` | No | `3` for Walle (default), `2` for Mini |

OpenClaw injects these via `skills.entries.*.env` at agent run time. They are scoped to the run and do not leak into the global shell environment.

## Tool

```
python3 {baseDir}/scripts/robot_cmd.py <command> [options]
```

## Agent Workflow Rules (IMPORTANT)

**ALWAYS run `preflight` before sending any robot command.** This checks whether the device is online, its battery level, and current work mode.

### Decision flow:

```
1. Run: python3 {baseDir}/scripts/robot_cmd.py preflight
2. Check the result:
   - "ready": false  → Tell the user why (offline / OTA / low battery). Do NOT send commands.
   - "ready": true, with "note" about current mode → Inform the user, then proceed.
   - "ready": true, idle → Proceed with the command.
3. Execute the requested command.
4. Report the result to the user.
```

### State-aware behavior:

| current_status | Meaning | What to do |
|----------------|---------|------------|
| `offline` | Device not connected | Tell user. Do not send commands. |
| `idle` | Ready | Proceed normally. |
| `follow` | Following a person | Warn before sending conflicting commands (e.g. remote_control). Use `stop` first. |
| `remote_control` | Joystick active | Already in RC mode. Can send move commands directly. |
| `patrol` | Patrolling | Warn before interrupting. Use `stop` first. |
| `go_charge` | Returning to charger | Warn before interrupting. |
| `guard` | Monitoring | Warn before interrupting. |
| `ota` | Firmware updating | Do NOT send any commands. Wait. |
| `build_map` | Building SLAM map | Do NOT interrupt. |
| `active_action` | Performing action | Conflicts with follow. Use `stop` first if needed. |

### Battery rules:

- **< 10%** and not charging → Suggest `charge` command before any movement.
- **< 5%** → Refuse movement commands, only allow `charge` and `status`.

## Quick Examples

```bash
# ALWAYS run preflight check first
python3 {baseDir}/scripts/robot_cmd.py preflight

# Move robot forward
python3 {baseDir}/scripts/robot_cmd.py move --direction forward

# Stop all movement
python3 {baseDir}/scripts/robot_cmd.py stop

# Make robot say something
python3 {baseDir}/scripts/robot_cmd.py tts --text "你好，我是你的机器人助手"

# Check device status (battery, online, charging)
python3 {baseDir}/scripts/robot_cmd.py status

# Get live video stream URL
python3 {baseDir}/scripts/robot_cmd.py live_pull_url
```

---

## Command Reference

### 1. Movement — Remote Control

**Enter / Exit remote control mode:**

```bash
python3 {baseDir}/scripts/robot_cmd.py rc_enter
python3 {baseDir}/scripts/robot_cmd.py rc_exit
```

**Chassis movement** (8 directions, send continuously at ~100ms interval, robot stops when commands stop):

```bash
python3 {baseDir}/scripts/robot_cmd.py move --direction forward
python3 {baseDir}/scripts/robot_cmd.py move --direction backward
python3 {baseDir}/scripts/robot_cmd.py move --direction left
python3 {baseDir}/scripts/robot_cmd.py move --direction right
python3 {baseDir}/scripts/robot_cmd.py move --direction left_up
python3 {baseDir}/scripts/robot_cmd.py move --direction right_up
python3 {baseDir}/scripts/robot_cmd.py move --direction left_down
python3 {baseDir}/scripts/robot_cmd.py move --direction right_down

# Stop chassis movement
python3 {baseDir}/scripts/robot_cmd.py move_stop
```

**Head control (Walle only)** — up/down/left/right, send continuously at ~100ms:

```bash
python3 {baseDir}/scripts/robot_cmd.py head --direction up
python3 {baseDir}/scripts/robot_cmd.py head --direction down
python3 {baseDir}/scripts/robot_cmd.py head --direction left
python3 {baseDir}/scripts/robot_cmd.py head --direction right
python3 {baseDir}/scripts/robot_cmd.py head --direction stop
```

**Arm control (Walle only)** — left_arm or right_arm:

```bash
python3 {baseDir}/scripts/robot_cmd.py arm --side left --direction up
python3 {baseDir}/scripts/robot_cmd.py arm --side left --direction down
python3 {baseDir}/scripts/robot_cmd.py arm --side left --direction stop
python3 {baseDir}/scripts/robot_cmd.py arm --side right --direction up
python3 {baseDir}/scripts/robot_cmd.py arm --side right --direction stop
```

**Reset position (Walle only):**

```bash
python3 {baseDir}/scripts/robot_cmd.py reset --target all     # reset all
python3 {baseDir}/scripts/robot_cmd.py reset --target head    # reset head only
python3 {baseDir}/scripts/robot_cmd.py reset --target arm     # reset arms only
```

### 2. Fixed Actions (Mini only)

```bash
python3 {baseDir}/scripts/robot_cmd.py car_on          # 上车
python3 {baseDir}/scripts/robot_cmd.py car_off         # 下车
python3 {baseDir}/scripts/robot_cmd.py standup          # 站立
python3 {baseDir}/scripts/robot_cmd.py boot_off         # 收脚
python3 {baseDir}/scripts/robot_cmd.py boot_on          # 卡脚
python3 {baseDir}/scripts/robot_cmd.py hello            # 打招呼
python3 {baseDir}/scripts/robot_cmd.py hello_off        # 收手
python3 {baseDir}/scripts/robot_cmd.py head_up          # 抬头
python3 {baseDir}/scripts/robot_cmd.py head_down        # 回头 (低头)
python3 {baseDir}/scripts/robot_cmd.py charge           # 回充电桩
python3 {baseDir}/scripts/robot_cmd.py charge_stop      # 停止回充
```

### 3. Emergency Stop

```bash
python3 {baseDir}/scripts/robot_cmd.py stop             # 急停，停止所有移动和功能
```

### 4. Voice — TTS

```bash
# Play text on device speaker
python3 {baseDir}/scripts/robot_cmd.py tts --text "你好世界"

# Play text then close microphone (keep_silent=1)
python3 {baseDir}/scripts/robot_cmd.py tts --text "请安静" --keep-silent
```

### 5. Device Status & Preflight

```bash
# Pre-flight check (ALWAYS run this before any command)
python3 {baseDir}/scripts/robot_cmd.py preflight
# Returns: ready (bool), current_status, battery, is_charging, issues[], suggestion

# Get raw device status
python3 {baseDir}/scripts/robot_cmd.py status
```

**Preflight response example (ready):**
```json
{
  "ready": true,
  "current_status": "idle",
  "current_status_name": "空闲",
  "battery": 85,
  "is_charging": false,
  "note": "Device is online and idle. Ready to accept commands."
}
```

**Preflight response example (not ready):**
```json
{
  "ready": false,
  "current_status": "offline",
  "battery": -1,
  "issues": ["Device is OFFLINE — cannot accept commands"],
  "suggestion": "Device is OFFLINE — cannot accept commands"
}
```

### 6. Live Video

```bash
# Start push stream from device camera
python3 {baseDir}/scripts/robot_cmd.py live_push --status 1

# Stop push stream
python3 {baseDir}/scripts/robot_cmd.py live_push --status 0

# Get pull stream URL (HLS/RTMP)
python3 {baseDir}/scripts/robot_cmd.py live_pull_url

# Get push URL
python3 {baseDir}/scripts/robot_cmd.py live_push_url
```

### 7. ASR Result

```bash
# Get the robot's latest speech recognition result
python3 {baseDir}/scripts/robot_cmd.py asr_result
```

### 8. WiFi Configuration

```bash
# Configure robot WiFi (base64-encoded SSID and password)
python3 {baseDir}/scripts/robot_cmd.py wifi --ssid "MyWiFi" --password "12345678"
```

### 9. LLM Configuration (register your own model)

```bash
# Register a custom LLM
python3 {baseDir}/scripts/robot_cmd.py llm_register --name "My GPT" --base-url "https://api.openai.com/v1" --api-key "sk-xxx" --model "gpt-4"

# List registered LLMs
python3 {baseDir}/scripts/robot_cmd.py llm_list

# Update a registered LLM
python3 {baseDir}/scripts/robot_cmd.py llm_update --id 123 --model "gpt-4o"
```

### 10. Agent Configuration

```bash
# Create an agent with a registered LLM
python3 {baseDir}/scripts/robot_cmd.py agent_create --name "My Agent" --llm-id 123

# List agents
python3 {baseDir}/scripts/robot_cmd.py agent_list

# Update agent
python3 {baseDir}/scripts/robot_cmd.py agent_update --id 123 --name "New Name"

# Bind agent to a device
python3 {baseDir}/scripts/robot_cmd.py agent_bind --agent-id 123

# Query device's bound agent
python3 {baseDir}/scripts/robot_cmd.py agent_query

# Reset device to default JoyIn agent
python3 {baseDir}/scripts/robot_cmd.py agent_reset
```

---

## Device Types

| Type ID | Model | Codename | Key Capabilities |
|---------|-------|----------|-----------------|
| 3 | W-1 (Walle) | walle | Chassis + head + arm control, 8-direction joystick, position reset |
| 2 | M-1 (Mini) | mini | Chassis control, fixed body actions (standup/car/hello/head), charging |

## API Protocol

- **Base URL**: `https://api-open-test.joyin-ai.com` (test)
- **Auth**: All requests carry 3 headers — `Authorization`, `Device-Sn`, `Device-Type-Id`
- **Robot commands**: `POST /v1/device/interaction/cmd` with body `{"cmd_type":"...","status":"...","name":"...","data":{...}}`
- **Response format**: `{"code": 200, "msg": "success", "data": {...}}`

## Important Notes

- The device must be **online** for commands to work.
- Joystick commands (move/head/arm) need to be sent **continuously at ~100ms intervals**. The robot stops automatically when commands stop arriving.
- `keep_silent=1` on TTS means the microphone will be closed after playback.
- Some APIs (LLM config, Agent config) are marked as **"开发中"** and may not be fully available.
