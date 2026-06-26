#!/usr/bin/env python3
"""IoT Controller - cross-platform."""
import json, sys, os, argparse

def send_http_request(url, method='GET', data=None, headers=None):
    """Send HTTP request to IoT platform."""
    try:
        import requests
        if method == 'GET':
            r = requests.get(url, headers=headers)
        elif method == 'POST':
            r = requests.post(url, json=data, headers=headers)
        elif method == 'PUT':
            r = requests.put(url, json=data, headers=headers)
        return json.dumps({"status": r.status_code, "response": r.text}, indent=2)
    except ImportError:
        return json.dumps({"error": "Install requests"}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

def homeassistant_action(url, token, action, entity_id, data=None):
    """Control Home Assistant entity."""
    if action == 'on':
        endpoint = f"{url}/api/services/homeassistant/turn_on"
    elif action == 'off':
        endpoint = f"{url}/api/services/homeassistant/turn_off"
    else:
        endpoint = f"{url}/api/services/homeassistant/{action}"

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"entity_id": entity_id}
    if data:
        payload.update(data)

    return send_http_request(endpoint, 'POST', payload, headers)

def main():
    parser = argparse.ArgumentParser(description='IoT Controller')
    subparsers = parser.add_subparsers(dest='command')

    # http command
    http_parser = subparsers.add_parser('http')
    http_parser.add_argument('--url', required=True)
    http_parser.add_argument('--method', default='GET', choices=['GET', 'POST', 'PUT'])
    http_parser.add_argument('--data', help='JSON data')

    # homeassistant command
    ha_parser = subparsers.add_parser('homeassistant')
    ha_parser.add_argument('--url', required=True)
    ha_parser.add_argument('--token', required=True)
    ha_parser.add_argument('action', choices=['on', 'off', 'toggle'])
    ha_parser.add_argument('--entity-id', required=True)

    args = parser.parse_args()

    if args.command == 'http':
        data = json.loads(args.data) if args.data else None
        print(send_http_request(args.url, args.method, data))
    elif args.command == 'homeassistant':
        print(homeassistant_action(args.url, args.token, args.action, args.entity_id))

if __name__ == '__main__':
    main()
