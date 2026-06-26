# Home Assistant Entity Reference

## Xiao AI Speaker Pro (小爱音箱 Pro)

| Entity ID | Type | Function |
|-----------|------|----------|
| `media_player.xiaomi_lx06_3ff3_play_control` | media_player | 播放控制 |
| `text.xiaomi_lx06_3ff3_execute_text_directive` | text | 执行文本指令 |
| `text.xiaomi_lx06_3ff3_play_text` | text | 播放文本 |
| `button.xiaomi_lx06_3ff3_play_music` | button | 播放音乐 |
| `button.xiaomi_lx06_3ff3_wake_up` | button | 唤醒 |
| `switch.xiaomi_lx06_3ff3_sleep_mode` | switch | 睡眠模式 |

## Air Conditioner (空调 - 客厅)

| Entity ID | Type | Function |
|-----------|------|----------|
| `button.miir_ir02_8112_turn_off` | button | 关闭空调 |
| `button.miir_ir02_8112_turn_on` | button | 打开空调 |
| `button.miir_ir02_8112_temperature_up` | button | 温度 + |
| `button.miir_ir02_8112_temperature_down` | button | 温度 - |
| `button.miir_ir02_8112_fan_speed_up` | button | 风速 + |
| `button.miir_ir02_8112_fan_speed_down` | button | 风速 - |
| `climate.miir_ir02_8112_ir_aircondition_control` | climate | 空调控制 (温度/模式/风速) |
| `number.miir_ir02_8112_temperature_for_ir` | number | 温度设置 (16-30°C) |
| `select.miir_ir02_8112_mode_for_ir` | select | 模式选择 (Auto/Cool/Heat/Dry/Fan) |

## Other Devices

| Entity ID | Type | Function |
|-----------|------|----------|
| `light.yeelink_lamp22_1fe0_light` | light | 米家智能显示器灯条 1S |
| `humidifier.xiaomi_4lite_097f_humidifier` | humidifier | 米家无雾加湿器 3 |
| `switch.xiaomi_my02_5d42_massager` | switch | 米家智能眼部按摩仪 |

## HA Services Reference

### button/press
```json
{"entity_id": "button.xxx"}
```

### text/set_value
```json
{"entity_id": "text.xxx", "value": "command text"}
```

### number/set_value
```json
{"entity_id": "number.xxx", "value": 26}
```

### select/select_option
```json
{"entity_id": "select.xxx", "option": "Cool"}
```

### climate/set_temperature
```json
{"entity_id": "climate.xxx", "temperature": 26}
```

### climate/turn_on
```json
{"entity_id": "climate.xxx"}
```

### climate/turn_off
```json
{"entity_id": "climate.xxx"}
```
