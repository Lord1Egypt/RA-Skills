# Automation Templates

## Home Assistant Automation Examples

These automations can be configured in Home Assistant's UI or via YAML.

### Temperature-Based Climate Control

```yaml
automation:
  - alias: "Auto AC when hot"
    trigger:
      - platform: numeric_state
        entity_id: sensor.living_room_temperature
        above: 28
    condition:
      - condition: time
        after: "08:00:00"
        before: "22:00:00"
    action:
      - service: climate.set_temperature
        target:
          entity_id: climate.living_room_ac
        data:
          temperature: 26
      - service: notify.openclaw
        data:
          message: "🌡️ Living room temp above 28°C, AC turned on to 26°C"
```

### Motion-Activated Light

```yaml
automation:
  - alias: "Hallway light on motion"
    trigger:
      - platform: state
        entity_id: binary_sensor.hallway_motion
        to: "on"
    condition:
      - condition: sun
        after: sunset
        before: sunrise
    action:
      - service: light.turn_on
        target:
          entity_id: light.hallway
        data:
          brightness: 128
```

### Door Lock Reminder

```yaml
automation:
  - alias: "Front door auto-lock"
    trigger:
      - platform: state
        entity_id: binary_sensor.front_door
        to: "closed"
        for:
          minutes: 2
    condition:
      - condition: state
        entity_id: lock.front_door
        state: "unlocked"
    action:
      - service: lock.lock
        target:
          entity_id: lock.front_door
```

### Goodnight Routine

```yaml
automation:
  - alias: "Goodnight scene"
    trigger:
      - platform: time
        at: "22:30:00"
    action:
      - service: light.turn_off
        target:
          entity_id: group.all_lights
      - service: climate.set_temperature
        target:
          entity_id: climate.bedroom_ac
        data:
          temperature: 25
      - service: lock.lock
        target:
          entity_id: lock.front_door
```

### Leave Home

```yaml
automation:
  - alias: "Turn off when leaving"
    trigger:
      - platform: state
        entity_id: binary_sensor.front_door
        to: "closed"
        for:
          minutes: 5
    condition:
      - condition: state
        entity_id: person.jun
        state: "not_home"
    action:
      - service: switch.turn_off
        target:
          entity_id: group.all_switches
      - service: notify.openclaw
        data:
          message: "🔒 Home secured. All devices off."
```

## OpenClaw Webhook Integration

To receive alerts in OpenClaw, set up a webhook in Home Assistant.

### Configuration

Add to `configuration.yaml`:

```yaml
rest_command:
  notify_openclaw:
    url: "http://localhost:8123/api/webhook/openclaw_notify"
    method: POST
    content_type: "application/json"
    payload: '{"message": "{{ message }}"}'
```

### Enable Webhook in UI

Settings → Devices & Services → Helpers → Add Helper → Webhook

### Notify OpenClaw from Automation

```yaml
action:
  - service: rest_command.notify_openclaw
    data:
      message: "⚠️ Smoke detected in living room!"
```

## Natural Language Commands from OpenClaw

OpenClaw can execute these automations via the MCP tools:

```
User: "Turn on the fan when temperature exceeds 30°C"
→ OpenClaw: Creates automation in HA or triggers manual command

User: "Lock all doors at 10 PM"  
→ OpenClaw: Creates time-based automation

User: "Turn off everything when I leave"
→ OpenClaw: Creates device-based automation
```
