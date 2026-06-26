#!/usr/bin/env python3
"""
Home Assistant Bridge for OpenClaw
Provides programmatic access to HA devices, sensors, and automations.

Features:
  - Device control (on/off/toggle)
  - Light control (brightness, color_temp, rgb)
  - Climate control (set temperature, HVAC mode)
  - Scene activation
  - Entity search by name or domain
  - Alias system for friendly device names
  - State verification after commands
  - History queries
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from typing import Optional, Dict, Any, List

try:
    import requests
except ImportError:
    print("Error: requests module not installed")
    print("Install with: pip3 install requests")
    sys.exit(1)

ALIASES_FILE = Path(__file__).parent / "aliases.json"


def load_aliases() -> Dict[str, str]:
    """Load alias mappings from aliases.json"""
    if ALIASES_FILE.exists():
        try:
            with open(ALIASES_FILE) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def resolve_alias(entity_or_alias: str) -> str:
    """Resolve an alias to an entity_id, or return as-is if not an alias."""
    aliases = load_aliases()
    lower = entity_or_alias.lower()
    if lower in aliases:
        return aliases[lower]
    # Also check if the value matches a friendly name fragment
    for alias, entity_id in aliases.items():
        if alias in lower:
            return entity_id
    return entity_or_alias


class HomeAssistantClient:
    """Client for Home Assistant REST API"""

    def __init__(self, url: Optional[str] = None, token: Optional[str] = None):
        self.url = (url or os.environ.get('HA_URL', '')).rstrip('/')
        self.token = token or os.environ.get('HA_TOKEN')

        if not self.url or not self.token:
            raise ValueError(
                "HA_URL and HA_TOKEN required. "
                "Set environment variables or run ha-setup.sh"
            )

        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Any:
        """Make API request"""
        url = f"{self.url}/api/{endpoint}"
        try:
            response = requests.request(
                method, url, headers=self.headers,
                json=data, timeout=30
            )
            response.raise_for_status()
            return response.json() if response.text else None
        except requests.exceptions.ConnectionError:
            print(f"Error: Cannot connect to {self.url}")
            return None
        except requests.exceptions.Timeout:
            print("Error: Request timed out (30s)")
            return None
        except requests.exceptions.HTTPError as e:
            print(f"Error: {e.response.status_code} - {e.response.text[:200]}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

    # ── States ──────────────────────────────────────────────

    def get_states(self) -> list:
        """Get all entity states"""
        return self._request('GET', 'states') or []

    def get_state(self, entity_id: str) -> Optional[Dict]:
        """Get specific entity state"""
        return self._request('GET', f'states/{entity_id}')

    # ── Services ────────────────────────────────────────────

    def call_service(self, domain: str, service: str, entity_id: str,
                     service_data: Optional[Dict] = None) -> bool:
        """Call a Home Assistant service"""
        data = dict(service_data or {})
        data['entity_id'] = entity_id
        result = self._request('POST', f'services/{domain}/{service}', data)
        return result is not None

    def turn_on(self, entity_id: str, **kwargs) -> bool:
        """Turn on an entity with optional parameters"""
        domain = entity_id.split('.')[0]
        return self.call_service(domain, 'turn_on', entity_id, kwargs if kwargs else None)

    def turn_off(self, entity_id: str) -> bool:
        """Turn off an entity"""
        domain = entity_id.split('.')[0]
        return self.call_service(domain, 'turn_off', entity_id)

    def toggle(self, entity_id: str) -> bool:
        """Toggle an entity"""
        domain = entity_id.split('.')[0]
        return self.call_service(domain, 'toggle', entity_id)

    # ── Lights ──────────────────────────────────────────────

    def set_light(self, entity_id: str, brightness: Optional[int] = None,
                  color_temp: Optional[int] = None, rgb: Optional[List[int]] = None) -> bool:
        """Set light attributes"""
        data = {}
        if brightness is not None:
            data['brightness'] = max(0, min(255, brightness))
        if color_temp is not None:
            data['color_temp'] = color_temp
        if rgb is not None and len(rgb) == 3:
            data['rgb_color'] = rgb
        return self.call_service('light', 'turn_on', entity_id, data)

    # ── Climate ─────────────────────────────────────────────

    def set_climate(self, entity_id: str, temperature: Optional[float] = None,
                    hvac_mode: Optional[str] = None) -> bool:
        """Set climate device parameters"""
        if hvac_mode:
            self.call_service('climate', 'set_hvac_mode', entity_id,
                              {'hvac_mode': hvac_mode})
        if temperature is not None:
            return self.call_service('climate', 'set_temperature', entity_id,
                                     {'temperature': temperature})
        return True

    # ── Scenes ──────────────────────────────────────────────

    def activate_scene(self, entity_id: str) -> bool:
        """Activate a scene"""
        return self.call_service('scene', 'turn_on', entity_id)

    # ── History ─────────────────────────────────────────────

    def get_history(self, entity_id: str, hours: int = 24) -> Optional[list]:
        """Get entity history for the last N hours"""
        from datetime import datetime, timedelta, timezone
        start = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()
        result = self._request('GET',
                               f'history/period/{start}?filter_entity_id={entity_id}&minimal_response')
        if result and len(result) > 0:
            return result[0]
        return None

    # ── Services list ───────────────────────────────────────

    def get_services(self) -> list:
        """Get available services"""
        return self._request('GET', 'services') or []

    # ── Search ──────────────────────────────────────────────

    def search_entities(self, query: str, domain: Optional[str] = None) -> List[Dict]:
        """Search entities by name or entity_id fragment"""
        states = self.get_states()
        query_lower = query.lower()
        results = []
        for entity in states:
            eid = entity.get('entity_id', '')
            fname = (entity.get('attributes', {}).get('friendly_name') or '').lower()
            if domain and not eid.startswith(f"{domain}."):
                continue
            if query_lower in eid.lower() or query_lower in fname:
                results.append({
                    'entity_id': eid,
                    'friendly_name': entity.get('attributes', {}).get('friendly_name', 'N/A'),
                    'state': entity.get('state'),
                    'domain': eid.split('.')[0]
                })
        return results


# ── CLI ─────────────────────────────────────────────────────

def cmd_on(client, args):
    entity = resolve_alias(args.entity)
    extra = {}
    if args.brightness is not None:
        extra['brightness'] = args.brightness
    if client.turn_on(entity, **extra):
        print(f"✓ Turned on {entity}")
        if args.verify:
            _verify(client, entity, 'on')
    else:
        print(f"✗ Failed to turn on {entity}")
        sys.exit(1)


def cmd_off(client, args):
    entity = resolve_alias(args.entity)
    if client.turn_off(entity):
        print(f"✓ Turned off {entity}")
        if args.verify:
            _verify(client, entity, 'off')
    else:
        print(f"✗ Failed to turn off {entity}")
        sys.exit(1)


def cmd_toggle(client, args):
    entity = resolve_alias(args.entity)
    if client.toggle(entity):
        print(f"✓ Toggled {entity}")
        if args.verify:
            time.sleep(3)
            state = client.get_state(entity)
            if state:
                print(f"  State: {state.get('state')}")
    else:
        print(f"✗ Failed to toggle {entity}")
        sys.exit(1)


def cmd_state(client, args):
    entity = resolve_alias(args.entity)
    state = client.get_state(entity)
    if state:
        print(json.dumps(state, indent=2))
    else:
        print(f"✗ Entity not found: {entity}")
        sys.exit(1)


def cmd_states(client, args):
    states = client.get_states()
    print(json.dumps(states, indent=2))


def cmd_search(client, args):
    results = client.search_entities(args.query, args.domain)
    if not results:
        print(f"No entities found matching '{args.query}'")
        return
    # Formatted output
    max_id = max(len(r['entity_id']) for r in results)
    max_name = max(len(r['friendly_name']) for r in results)
    for r in sorted(results, key=lambda x: x['entity_id']):
        print(f"  {r['entity_id']:<{max_id}}  {r['friendly_name']:<{max_name}}  [{r['state']}]")
    print(f"\n  {len(results)} result(s)")


def cmd_light(client, args):
    entity = resolve_alias(args.entity)
    rgb = None
    if args.rgb:
        parts = args.rgb.split(',')
        if len(parts) == 3:
            rgb = [int(p.strip()) for p in parts]
    if client.set_light(entity, brightness=args.brightness,
                        color_temp=args.color_temp, rgb=rgb):
        print(f"✓ Light updated: {entity}")
    else:
        print(f"✗ Failed to update light: {entity}")
        sys.exit(1)


def cmd_climate(client, args):
    entity = resolve_alias(args.entity)
    if client.set_climate(entity, temperature=args.temperature, hvac_mode=args.mode):
        print(f"✓ Climate updated: {entity}")
    else:
        print(f"✗ Failed to update climate: {entity}")
        sys.exit(1)


def cmd_scene(client, args):
    entity = resolve_alias(args.entity)
    if not entity.startswith('scene.'):
        entity = f"scene.{entity}"
    if client.activate_scene(entity):
        print(f"✓ Scene activated: {entity}")
    else:
        print(f"✗ Failed to activate scene: {entity}")
        sys.exit(1)


def cmd_history(client, args):
    entity = resolve_alias(args.entity)
    history = client.get_history(entity, hours=args.hours)
    if history:
        print(f"History for {entity} (last {args.hours}h):\n")
        for entry in history:
            ts = entry.get('last_changed', entry.get('last_updated', '?'))
            state = entry.get('state', '?')
            print(f"  {ts}  →  {state}")
        print(f"\n  {len(history)} entries")
    else:
        print(f"No history found for {entity}")


def cmd_aliases(client, args):
    aliases = load_aliases()
    if not aliases:
        print("No aliases configured.")
        print(f"Add them to: {ALIASES_FILE}")
        return
    max_alias = max(len(a) for a in aliases)
    print("Configured aliases:\n")
    for alias, entity_id in sorted(aliases.items()):
        print(f"  {alias:<{max_alias}}  →  {entity_id}")
    print(f"\n  {len(aliases)} alias(es)")


def cmd_services(client, args):
    services = client.get_services()
    print(json.dumps(services, indent=2))


def _verify(client, entity_id: str, expected: str):
    """Verify state after a command"""
    time.sleep(3)
    state = client.get_state(entity_id)
    if state:
        actual = state.get('state', '?')
        if actual == expected:
            print(f"  ✓ Verified: {actual}")
        else:
            print(f"  ⚠ State is '{actual}' (expected '{expected}')")


def main():
    parser = argparse.ArgumentParser(
        description='Home Assistant Bridge for OpenClaw',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s on kitchen                # Turn on using alias
  %(prog)s off tv --verify           # Turn off and verify state
  %(prog)s search light              # Search entities by name
  %(prog)s light bedroom --brightness 128
  %(prog)s history kitchen --hours 48
  %(prog)s aliases                   # Show all aliases
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command')

    # on
    p_on = subparsers.add_parser('on', help='Turn on entity')
    p_on.add_argument('entity', help='Entity ID or alias')
    p_on.add_argument('--brightness', type=int, help='Brightness 0-255 (lights)')
    p_on.add_argument('--verify', action='store_true', help='Verify state after command')

    # off
    p_off = subparsers.add_parser('off', help='Turn off entity')
    p_off.add_argument('entity', help='Entity ID or alias')
    p_off.add_argument('--verify', action='store_true', help='Verify state after command')

    # toggle
    p_toggle = subparsers.add_parser('toggle', help='Toggle entity')
    p_toggle.add_argument('entity', help='Entity ID or alias')
    p_toggle.add_argument('--verify', action='store_true', help='Verify state after command')

    # state
    p_state = subparsers.add_parser('state', help='Get entity state')
    p_state.add_argument('entity', help='Entity ID or alias')

    # states
    subparsers.add_parser('states', help='Get all entity states')

    # search
    p_search = subparsers.add_parser('search', help='Search entities by name')
    p_search.add_argument('query', help='Search term')
    p_search.add_argument('--domain', help='Filter by domain (switch, light, sensor...)')

    # light
    p_light = subparsers.add_parser('light', help='Control light attributes')
    p_light.add_argument('entity', help='Entity ID or alias')
    p_light.add_argument('--brightness', type=int, help='Brightness 0-255')
    p_light.add_argument('--color-temp', type=int, help='Color temperature in mireds')
    p_light.add_argument('--rgb', help='RGB color as "R,G,B" (e.g. "255,0,0")')

    # climate
    p_climate = subparsers.add_parser('climate', help='Control climate device')
    p_climate.add_argument('entity', help='Entity ID or alias')
    p_climate.add_argument('--temperature', type=float, help='Target temperature')
    p_climate.add_argument('--mode', help='HVAC mode (heat, cool, auto, off)')

    # scene
    p_scene = subparsers.add_parser('scene', help='Activate a scene')
    p_scene.add_argument('entity', help='Scene entity ID or alias')

    # history
    p_history = subparsers.add_parser('history', help='Get entity history')
    p_history.add_argument('entity', help='Entity ID or alias')
    p_history.add_argument('--hours', type=int, default=24, help='Hours to look back (default: 24)')

    # aliases
    subparsers.add_parser('aliases', help='Show configured aliases')

    # services
    subparsers.add_parser('services', help='List available HA services')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        client = HomeAssistantClient()
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    commands = {
        'on': cmd_on,
        'off': cmd_off,
        'toggle': cmd_toggle,
        'state': cmd_state,
        'states': cmd_states,
        'search': cmd_search,
        'light': cmd_light,
        'climate': cmd_climate,
        'scene': cmd_scene,
        'history': cmd_history,
        'aliases': cmd_aliases,
        'services': cmd_services,
    }

    commands[args.command](client, args)


if __name__ == '__main__':
    main()
