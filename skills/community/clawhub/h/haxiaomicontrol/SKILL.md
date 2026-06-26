---
name: ha-xiaomi-control
description: Control Xiaomi smart home devices via Home Assistant API. Use when user wants to control Xiaomi or Xiao AI devices such as air conditioner, speakers, and lights through Home Assistant. Triggers include messages containing device control commands.
---

# Home Assistant + Xiaomi Device Control

Control Xiaomi smart home devices through Home Assistant API.

## Configuration

Load configuration from `TOOLS.md` → **智能家居** section, or use these defaults:

- **HA URL:** `http://192.168.31.35:8123`
- **Access Token:** Read from user's environment or TOOLS.md
- **Xiao AI Speaker:** `media_player.xiaomi_lx06_3ff3_play_control`
- **Xiao AI Command Entity:** `text.xiaomi_lx06_3ff3_execute_text_directive`
- **Air Conditioner:** `button.miir_ir02_8112_turn_off` / `button.miir_ir02_8112_turn_on`

## Control Rules

### Xiao AI Speaker Control

When user message contains **"小爱同学"** or **"小爱"**:

1. Extract the command after the trigger word
2. Call HA API to execute text directive

**Example:**
```
User: "小爱同学 播放音乐 天后"
→ Execute: text.xiaomi_lx06_3ff3_execute_text_directive with value "播放音乐天后"
```

**API Call:**
```bash
curl -X POST \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "text.xiaomi_lx06_3ff3_execute_text_directive", "value": "${COMMAND}"}' \
  ${HA_URL}/api/services/text/set_value
```

### Air Conditioner Control

When user message contains **"空调"**:

| Command | Entity | Service |
|---------|--------|---------|
| 关闭空调 | `button.miir_ir02_8112_turn_off` | `button/press` |
| 打开空调 | `button.miir_ir02_8112_turn_on` | `button/press` |
| 空调 26 度 | `number.miir_ir02_8112_temperature_for_ir` | `number/set_value` |
| 空调制冷 | `select.miir_ir02_8112_mode_for_ir` | `select/select_option` (option: "Cool") |
| 空调制热 | `select.miir_ir02_8112_mode_for_ir` | `select/select_option` (option: "Heat") |

**Example - Turn Off:**
```bash
curl -X POST \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "button.miir_ir02_8112_turn_off"}' \
  ${HA_URL}/api/services/button/press
```

**Example - Set Temperature:**
```bash
curl -X POST \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "number.miir_ir02_8112_temperature_for_ir", "value": 26}' \
  ${HA_URL}/api/services/number/set_value
```

## Available Entities

See `references/entities.md` for complete entity list.

## Error Handling

1. **Connection Failed:** Check if HA is running and accessible
2. **401 Unauthorized:** Token expired, ask user to regenerate
3. **Entity Not Found:** Verify entity ID in TOOLS.md
4. **Device Offline:** Check device status in Mi Home app

## Security Notes

- ⚠️ Access Token is sensitive - never log or expose it
- ✅ Store token in environment variable or secure config
- ✅ Use HTTPS for remote HA access
