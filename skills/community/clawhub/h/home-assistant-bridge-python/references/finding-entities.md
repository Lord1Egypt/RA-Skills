# Entity IDs herausfinden

Diese Referenz zeigt, wie man die korrekten Entity IDs für Home Assistant Geräte findet.

## Methode 1: Alle Geräte auflisten

```bash
python3 ha-bridge.py states | jq -r '.[] | "\(.entity_id): \(.attributes.friendly_name // "N/A")"'
```

## Methode 2: Nach Name suchen

```bash
# Search for "kitchen"
python3 ha-bridge.py search kitchen

# Search for "light"
python3 ha-bridge.py search light
```

## Methode 3: Nach Domain filtern

```bash
# Nur Switches
python3 ha-bridge.py states | jq -r '.[] | select(.entity_id | startswith("switch.")) | "\(.entity_id): \(.attributes.friendly_name // "N/A")"'

# Nur Lights
python3 ha-bridge.py states | jq -r '.[] | select(.entity_id | startswith("light.")) | "\(.entity_id): \(.attributes.friendly_name // "N/A")"'

# Nur Sensoren
python3 ha-bridge.py states | jq -r '.[] | select(.entity_id | startswith("sensor.")) | "\(.entity_id): \(.attributes.friendly_name // "N/A")"'
```

## Example: Find a device

```bash
# Step 1: Search
python3 ha-bridge.py search kitchen

# Step 2: Use the entity ID
python3 ha-bridge.py on switch.kitchen_light_relay
python3 ha-bridge.py off switch.kitchen_light_relay
```

## Discovered Entity IDs

Add your own entity IDs here as you discover them:

| Device | Entity ID | Type |
|--------|-----------|------|
| *use `search` to find yours* | | |

## Tipps

1. **Friendly Names** können sich ändern, Entity IDs bleiben stabil
2. **Immer Entity ID verwenden** für Automationen und Skripte
3. **Dokumentieren** welche Entity IDs zu welchen Geräten gehören
4. **jq installieren** für bessere Filterung: `sudo apt install jq`