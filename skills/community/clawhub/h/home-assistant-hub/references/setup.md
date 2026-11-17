# Home Assistant Hub — Setup Guide

## ⚠️ Security Warning

You are about to create a **long-lived bearer token** with broad API access to your Home Assistant instance. Treat this token like a password:

- Never share it publicly or commit it to version control
- The file `config/hub.json` is gitignored — verify `.gitignore` includes it
- Rotate the token in HA if you suspect compromise (Profile → Long-Lived Access Tokens → Revoke)

## 1. Get a Long-Lived Access Token

1. Open Home Assistant → Profile (bottom-left)
2. Scroll to **Long-Lived Access Tokens**
3. Click **CREATE TOKEN**
4. Name it `openclaw-hub`
5. **Copy the token** (shown only once!)

## 2. Configure the Hub

```bash
cd ~/.openclaw/workspace/skills/home-assistant-hub
node scripts/ha-hub.js setup
```

Enter your HA URL and token when prompted.

## 3. Test Connection

```bash
node scripts/ha-hub.js test
```

Should show your HA version.

## 4. Add Alert Rules

### Interactive:
```bash
node scripts/ha-hub.js add-rule
```

### Via JSON (recommended for bulk):
```bash
node scripts/ha-hub.js add-rules << 'EOF'
[
  {
    "name": "Garage aperto",
    "entity_id": "binary_sensor.garage_door",
    "condition": "state",
    "value": "on",
    "cooldown": 300,
    "title": "Garage",
    "template": "Il garage è aperto!"
  },
  {
    "name": "Temperatura bassa",
    "entity_id": "sensor.temperatura_interna",
    "condition": "below",
    "value": "15",
    "cooldown": 600,
    "title": "🌡️ Temperatura",
    "template": "Temperatura bassa: {{state}}°C"
  },
  {
    "name": "Persone via",
    "entities": ["person.vincenzo", "person.maria"],
    "condition": "not_state",
    "value": "home",
    "cooldown": 900,
    "title": "🏠 Tutti fuori",
    "template": "Nessuno è in casa"
  }
]
EOF
```

## 5. Start the Hub

```bash
node scripts/ha-hub.js start
```

Verify:
```bash
node scripts/ha-hub.js status
```

## 6. Stop the Hub

```bash
node scripts/ha-hub.js stop
```

## Alert Rules Reference

### Conditions

| Condition | Meaning | Example value |
|-----------|---------|---------------|
| `state` | State equals value | `on`, `home`, `open` |
| `not_state` | State not equals value | `away` |
| `above` | State (numeric) above value | `25` |
| `below` | State (numeric) below value | `10` |
| `changed` | Always trigger on change | — |

### Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Rule identifier |
| `entity_id` | Yes* | Single entity ID |
| `entities` | Yes* | Array of entity IDs |
| `condition` | Yes | See table above |
| `value` | Condition-dependent | Value to compare |
| `cooldown` | No | Seconds between alerts (default 300) |
| `title` | No | Alert title (default "HA Alert") |
| `template` | No | Custom message (default: entity: old → new) |
| `channel` | No | Notification channel (default: config value) |
| `priority` | No | `normal` or `urgent` |

*Either `entity_id` or `entities` required.

## Quiet Hours

Disable alerts during sleep in `config/hub.json`:

```json
"quiet_hours": {
  "enabled": true,
  "start": "23:00",
  "end": "07:00"
}
```

Rules during quiet hours are silently suppressed.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Connection failed | Check HA URL and token |
| Hub won't start | Check token is valid in HA |
| No alerts firing | Verify entity IDs with `node scripts/ha-cmd.js state` |
| Duplicate alerts | Increase `cooldown` in rule config |
| WS fails, polling works | Normal — polling is the fallback |
