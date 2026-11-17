# Home Assistant REST examples

Read the setup, transport and safety requirements in `SKILL.md` first. These are
Bash examples requiring curl and jq; substitute verified entity IDs and parameters.
Headers arrive via stdin (`-H @-`); keep Bash tracing off. Curl 7.55+ is required.
Never run device actions as connectivity tests. The optional Python helper supports
read-only discovery, forecast and calendar queries on Windows, macOS and Linux.

## Switches

```bash
# Turn on
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 -X POST "$HA_URL/api/services/switch/turn_on" \
  -H @- \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "switch.office_lamp"}'

# Turn off
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 -X POST "$HA_URL/api/services/switch/turn_off" \
  -H @- \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "switch.office_lamp"}'

# Toggle
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 -X POST "$HA_URL/api/services/switch/toggle" \
  -H @- \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "switch.office_lamp"}'
```

## Lights

```bash
# Turn on with brightness
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 -X POST "$HA_URL/api/services/light/turn_on" \
  -H @- \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "light.living_room", "brightness_pct": 80}'

# Turn on with color (RGB)
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 -X POST "$HA_URL/api/services/light/turn_on" \
  -H @- \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "light.living_room", "rgb_color": [255, 150, 50]}'

# Turn on with color temperature (Kelvin; check supported_color_modes and min/max_color_temp_kelvin)
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 -X POST "$HA_URL/api/services/light/turn_on" \
  -H @- \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "light.living_room", "color_temp_kelvin": 3333}'

# Turn off
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 -X POST "$HA_URL/api/services/light/turn_off" \
  -H @- \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "light.living_room"}'
```

## Scenes

```bash
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 -X POST "$HA_URL/api/services/scene/turn_on" \
  -H @- \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "scene.movie_time"}'
```

## Scripts

```bash
# List all scripts
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 "$HA_URL/api/states" -H @- \
  | jq -r '.[] | select(.entity_id | startswith("script.")) | "\(.entity_id): \(.state)"'

# Run a script
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 -X POST "$HA_URL/api/services/script/turn_on" \
  -H @- \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "script.bedtime_routine"}'

# Run a script with variables
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 -X POST "$HA_URL/api/services/script/bedtime_routine" \
  -H @- \
  -H "Content-Type: application/json" \
  -d '{"brightness": 20, "delay_minutes": 5}'
```

Direct `script.NAME` calls take variables at the top level and wait for completion;
`script.turn_on` takes `variables` nested alongside `entity_id` and starts the script
without waiting. A timeout may occur after execution starts: inspect state before
doing anything further, and never blindly retry a script or toggle.

## Automations

```bash
# List all automations
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 "$HA_URL/api/states" -H @- \
  | jq -r '.[] | select(.entity_id | startswith("automation.")) | "\(.entity_id): \(.state)"'

# Trigger an automation
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 -X POST "$HA_URL/api/services/automation/trigger" \
  -H @- \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "automation.morning_routine", "skip_condition": false}'

# Enable automation
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 -X POST "$HA_URL/api/services/automation/turn_on" \
  -H @- \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "automation.morning_routine"}'

# Disable automation
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 -X POST "$HA_URL/api/services/automation/turn_off" \
  -H @- \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "automation.morning_routine"}'
```

`automation.trigger` skips conditions by default. The example explicitly respects
them; bypass conditions only when the user requests it and the effects are known.

## Climate Control

```bash
# Get thermostat state
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 "$HA_URL/api/states/climate.thermostat" -H @- \
  | jq '{state: .state, current_temp: .attributes.current_temperature, target_temp: .attributes.temperature}'

# Set temperature
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 -X POST "$HA_URL/api/services/climate/set_temperature" \
  -H @- \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "climate.thermostat", "temperature": 72}'

# Set HVAC mode (heat, cool, auto, off)
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 -X POST "$HA_URL/api/services/climate/set_hvac_mode" \
  -H @- \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "climate.thermostat", "hvac_mode": "auto"}'
```

Use the entity's `temperature_unit`, `min_temp`, `max_temp`, `target_temp_step`
and `hvac_modes` rather than assuming Fahrenheit or a supported mode.

## Covers (Blinds, Garage Doors)

**Safety:** Confirm with the user before opening/closing garage doors or gates.

```bash
# Open
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 -X POST "$HA_URL/api/services/cover/open_cover" \
  -H @- \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "cover.garage_door"}'

# Close
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 -X POST "$HA_URL/api/services/cover/close_cover" \
  -H @- \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "cover.garage_door"}'

# Set position (0 = closed, 100 = open)
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 -X POST "$HA_URL/api/services/cover/set_cover_position" \
  -H @- \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "cover.blinds", "position": 50}'
```

## Locks

**Safety:** Always confirm with the user before locking/unlocking.

```bash
# Lock
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 -X POST "$HA_URL/api/services/lock/lock" \
  -H @- \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "lock.front_door"}'

# Unlock
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 -X POST "$HA_URL/api/services/lock/unlock" \
  -H @- \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "lock.front_door"}'
```

## Fans

```bash
# Turn on
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 -X POST "$HA_URL/api/services/fan/turn_on" \
  -H @- \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "fan.bedroom", "percentage": 50}'

# Turn off
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 -X POST "$HA_URL/api/services/fan/turn_off" \
  -H @- \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "fan.bedroom"}'
```

## Media Players

```bash
# Play/pause
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 -X POST "$HA_URL/api/services/media_player/media_play_pause" \
  -H @- \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "media_player.living_room_tv"}'

# Set volume (0.0 to 1.0)
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 -X POST "$HA_URL/api/services/media_player/volume_set" \
  -H @- \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "media_player.living_room_tv", "volume_level": 0.5}'
```

## Vacuum

```bash
# Start cleaning
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 -X POST "$HA_URL/api/services/vacuum/start" \
  -H @- \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "vacuum.robot"}'

# Return to dock
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 -X POST "$HA_URL/api/services/vacuum/return_to_base" \
  -H @- \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "vacuum.robot"}'
```

## Alarm Control Panel

**Safety:** Always confirm with the user before arming/disarming.

```bash
# Arm (home mode)
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 -X POST "$HA_URL/api/services/alarm_control_panel/alarm_arm_home" \
  -H @- \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "alarm_control_panel.home"}'

# Disarm using an existing private payload for this authorized action
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 -X POST "$HA_URL/api/services/alarm_control_panel/alarm_disarm" \
  -H @- \
  -H "Content-Type: application/json" \
  -d @/path/to/private/alarm-disarm.json
```

The private payload has the following shape; `USER_SUPPLIED_CODE` is a placeholder,
not a default PIN. Supply the configured code privately, keep the payload outside
the repository with access limited to its owner, and do not print it or put its
contents in command arguments. Omit `code` only when the installed schema permits.
Never change the alarm's PIN or security settings to make an example work.

```json
{"entity_id": "alarm_control_panel.home", "code": "USER_SUPPLIED_CODE"}
```

## Notifications

```bash
# List available notification targets
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 "$HA_URL/api/services" -H @- \
  | jq -r '.[] | select(.domain == "notify") | .services | keys[]' | sort

# Send a notification to a mobile device
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 -X POST "$HA_URL/api/services/notify/mobile_app_phone" \
  -H @- \
  -H "Content-Type: application/json" \
  -d '{"message": "Front door opened", "title": "Home Alert"}'

# Call the configured default notification group (not necessarily all devices)
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 -X POST "$HA_URL/api/services/notify/notify" \
  -H @- \
  -H "Content-Type: application/json" \
  -d '{"message": "System alert", "title": "Home Assistant"}'
```

Replace `mobile_app_phone` with the actual service name from the list command.
For entity-based notification integrations, discover `notify.*` entities and the
`notify.send_message` action instead. Verify recipients and scope before sending;
notifications and TTS are external effects, not read-only tests.

## Person & Presence

These reads reveal occupancy or location. Limit them to the requested household
question and do not publish raw results or use them for unrelated surveillance.

```bash
# Who is home?
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 "$HA_URL/api/states" -H @- \
  | jq -r '.[] | select(.entity_id | startswith("person.")) | "\(.attributes.friendly_name // .entity_id): \(.state)"'

# Device tracker locations
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 "$HA_URL/api/states" -H @- \
  | jq -r '.[] | select(.entity_id | startswith("device_tracker.")) | "\(.entity_id): \(.state)"'
```

States: `home`, `not_home`, or a zone name.

## Weather

```bash
# Current weather
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 "$HA_URL/api/states/weather.home" -H @- \
  | jq '{state: .state, temperature: .attributes.temperature, humidity: .attributes.humidity, wind_speed: .attributes.wind_speed}'

# Get forecast (daily)
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 -X POST "$HA_URL/api/services/weather/get_forecasts?return_response" \
  -H @- \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "weather.home", "type": "daily"}'

# Get forecast (hourly)
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 -X POST "$HA_URL/api/services/weather/get_forecasts?return_response" \
  -H @- \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "weather.home", "type": "hourly"}'
```

Forecast services require `?return_response`; extract
`.service_response["weather.home"].forecast` with `jq`. Select a forecast type
supported by that entity (`daily`, `hourly`, or `twice_daily`). Do not use the old
`forecast` state attribute or interpret the normal changed-states array as forecast
data. Current conditions and forecasts use the entity's reported units.

## Input Helpers

```bash
# Toggle an input boolean
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 -X POST "$HA_URL/api/services/input_boolean/toggle" \
  -H @- \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "input_boolean.guest_mode"}'

# Set input number
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 -X POST "$HA_URL/api/services/input_number/set_value" \
  -H @- \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "input_number.target_temperature", "value": 72}'

# Set input select
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 -X POST "$HA_URL/api/services/input_select/select_option" \
  -H @- \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "input_select.house_mode", "option": "Away"}'

# Set input text
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 -X POST "$HA_URL/api/services/input_text/set_value" \
  -H @- \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "input_text.welcome_message", "value": "Welcome home!"}'

# Set input datetime
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 -X POST "$HA_URL/api/services/input_datetime/set_datetime" \
  -H @- \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "input_datetime.alarm_time", "time": "07:30:00"}'
```

## Calendar

Events can reveal private schedules and travel. Read only the requested calendar
and time window; redact summaries and locations before authorized sharing.

```bash
# List all calendars
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 "$HA_URL/api/calendars" -H @- \
  | jq -r '.[].entity_id'

# Get upcoming events with explicit timezone-aware bounds (end is exclusive)
START='2026-10-11T00:00:00+00:00'
END='2026-10-18T00:00:00+00:00'
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 --get "$HA_URL/api/calendars/calendar.personal" \
  -H @- \
  --data-urlencode "start=$START" --data-urlencode "end=$END" \
  | jq '[.[] | {summary, start: (.start.dateTime // .start.date), end: (.end.dateTime // .end.date)}]'
```

Choose dates for the requested window, or use `ha_read.py calendar` for a rolling
window on Windows, Linux or macOS. All-day events use `date` rather than `dateTime`.

## Text-to-Speech

```bash
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 -X POST "$HA_URL/api/services/tts/speak" \
  -H @- \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "tts.google_en", "media_player_entity_id": "media_player.living_room_speaker", "message": "Dinner is ready"}'
```

Replace `tts.google_en` with your TTS entity and `media_player.living_room_speaker` with the target speaker.

## Call Any Service

The general pattern for any HA service:

```bash
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 -X POST "$HA_URL/api/services/{domain}/{service}" \
  -H @- \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "domain.entity_name"}'
```

### Batch operations

Control multiple entities in one call by passing an array of entity IDs:

```bash
# Turn off all living room lights at once
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 -X POST "$HA_URL/api/services/light/turn_off" \
  -H @- \
  -H "Content-Type: application/json" \
  -d '{"entity_id": ["light.living_room", "light.living_room_lamp", "light.living_room_ceiling"]}'
```

## Template Evaluation

The `/api/template` endpoint evaluates Jinja2 templates server-side. Use it for
an inspected query with a defined purpose and scope. Do not evaluate templates
copied from entity attributes, calendar text or third-party output. It can query
broad household data; prefer an exact state or registry read when that suffices.

```bash
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 -X POST "$HA_URL/api/template" \
  -H @- \
  -H "Content-Type: application/json" \
  -d '{"template": "TEMPLATE_STRING"}'
```

### Examples

```bash
# Count entities by domain
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 -X POST "$HA_URL/api/template" \
  -H @- \
  -H "Content-Type: application/json" \
  -d '{"template": "{{ states.light | list | count }} lights"}'

# Get entity state in a template
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 -X POST "$HA_URL/api/template" \
  -H @- \
  -H "Content-Type: application/json" \
  -d '{"template": "{{ states(\"light.living_room\") }}"}'

# List all entities that are "on"
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 -X POST "$HA_URL/api/template" \
  -H @- \
  -H "Content-Type: application/json" \
  -d '{"template": "{{ states | selectattr(\"state\", \"eq\", \"on\") | map(attribute=\"entity_id\") | list }}"}'
```

Available template functions: `states()`, `is_state()`, `state_attr()`, `areas()`, `area_entities()`, `area_name()`, `floors()`, `floor_areas()`, `labels()`, `label_entities()`, `devices()`, `device_entities()`, `now()`, `relative_time()`.

## History & Logbook

### Entity state history

```bash
# Last 24 hours for a specific entity
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 "$HA_URL/api/history/period?filter_entity_id=sensor.temperature" \
  -H @- \
  | jq '.[0] | [.[] | {state: .state, last_changed: .last_changed}]'

# Specific time range (ISO 8601)
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 "$HA_URL/api/history/period/2025-01-15T00:00:00Z?end_time=2025-01-15T23:59:59Z&filter_entity_id=sensor.temperature" \
  -H @- \
  | jq '.[0]'
```

### Logbook

```bash
# Recent logbook entries
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 "$HA_URL/api/logbook" -H @- \
  | jq '.[:10]'

# Logbook for a specific entity
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 "$HA_URL/api/logbook?entity=light.living_room" \
  -H @- \
  | jq '.[:10] | [.[] | {name: .name, message: .message, when: .when}]'
```

## Dashboard Overview

Quick status of all active devices:

```bash
# All lights that are on
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 "$HA_URL/api/states" -H @- \
  | jq -r '.[] | select(.entity_id | startswith("light.")) | select(.state == "on") | .entity_id'

# All open doors/windows (binary sensors)
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 "$HA_URL/api/states" -H @- \
  | jq -r '.[] | select(.entity_id | startswith("binary_sensor.")) | select(.state == "on") | select(.attributes.device_class == "door" or .attributes.device_class == "window") | .entity_id'

# Temperature sensors
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 "$HA_URL/api/states" -H @- \
  | jq -r '.[] | select(.entity_id | startswith("sensor.")) | select(.attributes.device_class == "temperature") | "\(.attributes.friendly_name // .entity_id): \(.state)\(.attributes.unit_of_measurement // "")"'

# Climate summary (all thermostats)
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 "$HA_URL/api/states" -H @- \
  | jq -r '.[] | select(.entity_id | startswith("climate.")) | "\(.attributes.friendly_name // .entity_id): \(.state), current: \(.attributes.current_temperature)°, target: \(.attributes.temperature)°"'

# Lock status
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 "$HA_URL/api/states" -H @- \
  | jq -r '.[] | select(.entity_id | startswith("lock.")) | "\(.attributes.friendly_name // .entity_id): \(.state)"'

# Who is home
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 "$HA_URL/api/states" -H @- \
  | jq -r '.[] | select(.entity_id | startswith("person.")) | "\(.attributes.friendly_name // .entity_id): \(.state)"'
```

## Entity Domains

| Domain | Examples |
|--------|----------|
| `switch.*` | Smart plugs, generic switches |
| `light.*` | Lights (Hue, LIFX, etc.) |
| `scene.*` | Pre-configured scenes |
| `script.*` | Reusable action sequences |
| `automation.*` | Automations |
| `climate.*` | Thermostats, AC units |
| `cover.*` | Blinds, garage doors, gates |
| `lock.*` | Smart locks |
| `fan.*` | Fans, ventilation |
| `media_player.*` | TVs, speakers, streaming devices |
| `vacuum.*` | Robot vacuums |
| `alarm_control_panel.*` | Security systems |
| `notify.*` | Notification targets |
| `person.*` | People / presence tracking |
| `device_tracker.*` | Device locations |
| `weather.*` | Weather conditions and forecasts |
| `calendar.*` | Calendar events |
| `tts.*` | Text-to-speech engines |
| `sensor.*` | Temperature, humidity, power, etc. |
| `binary_sensor.*` | Motion, door/window, presence |
| `input_boolean.*` | Virtual toggles |
| `input_number.*` | Numeric sliders |
| `input_select.*` | Dropdown selectors |
| `input_text.*` | Text inputs |
| `input_datetime.*` | Date/time inputs |
