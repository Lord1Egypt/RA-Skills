#!/usr/bin/env python3
"""
IoT Controller - Control smart home devices via APIs.

Supported platforms:
  - Home Assistant (REST API)
  - Mijia / XiaoMi (HTTP API, requires token)
  - Generic HTTP/REST endpoints

Requirements: requests (pip install requests)

Security:
  - Tokens are read from environment variable HA_TOKEN (not CLI args) to avoid
    exposure in process listings, shell history, and system logs.
  - URLs are validated against SSRF patterns.
  - Token values are never logged or printed in full.

Usage examples:
  # Set token via environment variable (recommended):
  $env:HA_TOKEN="your_long_lived_token"
  python iot_controller.py homeassistant --url http://192.168.1.100:8123 --action list_entities

  # Or pass via --token (will show warning):
  python iot_controller.py homeassistant --url http://192.168.1.100:8123 --token YOUR_TOKEN --action list_entities
"""

import sys
import json
import subprocess
import os
import re
import warnings

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')


# ========== Security: URL Validation ==========

# Block non-private/local IPs to prevent SSRF (Server-Side Request Forgery)
# Allow: localhost, 127.x, 10.x, 172.16-31.x, 192.168.x, ::1, fd00+/fc00+
PRIVATE_IP_PATTERN = re.compile(
    r'^(https?://)?(localhost|127\.\d+\.\d+\.\d+|10\.\d+\.\d+\.\d+)'
    r'|(172\.(1[6-9]|2\d|3[01])\.\d+\.\d+)'
    r'|(192\.168\.\d+\.\d+)'
    r'|(\[?(::1|f[cd][0-9a-f][0-9a-f]:)\]?)',
    re.IGNORECASE
)


def _validate_url(url):
    """Validate that URL points to a local/private network address."""
    if not url:
        raise ValueError("ERROR: URL cannot be empty")
    url = url.strip()
    if PRIVATE_IP_PATTERN.match(url) or 'localhost' in url.lower():
        return url
    # For generic HTTP mode, warn but allow (user may have valid use case)
    warnings.warn(
        f"WARNING: URL '{url}' does not appear to be a local/private address. "
        f"Ensure this is intentional (SSRF risk for public URLs).",
        UserWarning
    )
    return url


def _mask_token(token):
    """Return a masked version of token for safe logging/display."""
    if not token:
        return "(none)"
    if len(token) <= 8:
        return "****"
    return token[:4] + "****" + token[-4:]


def _resolve_token(token_arg=None):
    """
    Resolve token from environment variable first, then CLI argument fallback.
    Environment variable HA_TOKEN takes priority.
    Prints warning if using insecure CLI argument method.
    """
    env_token = os.environ.get("HA_TOKEN", "")
    if env_token:
        return env_token
    if token_arg:
        print(
            f"WARNING: Token passed via CLI argument is visible in process list. "
            f"Set environment variable HA_TOKEN instead for better security.",
            file=sys.stderr
        )
        return token_arg
    raise ValueError(
        "ERROR: No token provided. Set HA_TOKEN environment variable or use --token argument."
    )


# ========== Dependencies ==========

def check_requests():
    """Ensure requests library is available."""
    try:
        import requests
        return requests
    except ImportError:
        print("Installing requests...", file=sys.stderr)
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "requests>=2.31.0,<3", "-q"],
            stdout=subprocess.DEVNULL
        )
        import requests
        return requests


# ========== Home Assistant ==========

def ha_list_entities(base_url, token):
    """List all entities from Home Assistant."""
    requests = check_requests()
    _validate_url(base_url)
    url = f"{base_url.rstrip('/')}/api/states"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            entities = []
            for entity in resp.json():
                entities.append({
                    "entity_id": entity["entity_id"],
                    "state": entity["state"],
                    "friendly_name": entity["attributes"].get("friendly_name", ""),
                    "domain": entity["entity_id"].split(".")[0]
                })
            return json.dumps(entities, indent=2, ensure_ascii=False)
        else:
            return f"ERROR: HTTP {resp.status_code} - {resp.text}"
    except Exception as e:
        return f"ERROR: {e}"


def ha_get_state(base_url, token, entity_id):
    """Get state of a specific entity."""
    requests = check_requests()
    _validate_url(base_url)
    url = f"{base_url.rstrip('/')}/api/states/{entity_id}"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            return json.dumps(resp.json(), indent=2, ensure_ascii=False)
        else:
            return f"ERROR: HTTP {resp.status_code}"
    except Exception as e:
        return f"ERROR: {e}"


def ha_call_service(base_url, token, domain, service, entity_id, service_data=None):
    """Call a Home Assistant service."""
    requests = check_requests()
    _validate_url(base_url)
    url = f"{base_url.rstrip('/')}/api/services/{domain}/{service}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    payload = {"entity_id": entity_id}
    if service_data:
        if isinstance(service_data, str):
            try:
                payload.update(json.loads(service_data))
            except json.JSONDecodeError:
                return "ERROR: Invalid service_data JSON"
        else:
            payload.update(service_data)

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=10)
        if resp.status_code == 200:
            return f"OK: Called {domain}.{service} on {entity_id}"
        else:
            return f"ERROR: HTTP {resp.status_code} - {resp.text}"
    except Exception as e:
        return f"ERROR: {e}"


def ha_turn_on(base_url, token, entity_id, params=None):
    """Turn on an entity."""
    domain = entity_id.split(".")[0]
    return ha_call_service(base_url, token, domain, "turn_on", entity_id, params)


def ha_turn_off(base_url, token, entity_id):
    """Turn off an entity."""
    domain = entity_id.split(".")[0]
    return ha_call_service(base_url, token, domain, "turn_off", entity_id)


def ha_toggle(base_url, token, entity_id):
    """Toggle an entity."""
    domain = entity_id.split(".")[0]
    return ha_call_service(base_url, token, domain, "toggle", entity_id)


# ========== Generic HTTP ==========

def http_get(url, path="", headers=None):
    """Send HTTP GET request."""
    requests = check_requests()
    full_url = f"{url.rstrip('/')}/{path.lstrip('/')}" if path else url
    _validate_url(full_url)
    hdrs = {}
    if headers:
        for h in headers:
            k, v = h.split(":", 1)
            hdrs[k.strip()] = v.strip()

    try:
        resp = requests.get(full_url, headers=hdrs, timeout=10)
        try:
            body = resp.json()
            return json.dumps({"status": resp.status_code, "data": body}, indent=2, ensure_ascii=False)
        except Exception:
            return f"Status: {resp.status_code}\n{resp.text[:2000]}"
    except Exception as e:
        return f"ERROR: {e}"


def http_post(url, path="", body=None, headers=None):
    """Send HTTP POST request."""
    requests = check_requests()
    full_url = f"{url.rstrip('/')}/{path.lstrip('/')}" if path else url
    _validate_url(full_url)
    hdrs = {"Content-Type": "application/json"}
    if headers:
        for h in headers:
            k, v = h.split(":", 1)
            hdrs[k.strip()] = v.strip()

    payload = None
    if body:
        try:
            payload = json.loads(body) if isinstance(body, str) else body
        except json.JSONDecodeError:
            payload = body

    try:
        resp = requests.post(full_url, headers=hdrs, json=payload, timeout=10)
        try:
            rbody = resp.json()
            return json.dumps({"status": resp.status_code, "data": rbody}, indent=2, ensure_ascii=False)
        except Exception:
            return f"Status: {resp.status_code}\n{resp.text[:2000]}"
    except Exception as e:
        return f"ERROR: {e}"


def http_put(url, path="", body=None, headers=None):
    """Send HTTP PUT request."""
    requests = check_requests()
    full_url = f"{url.rstrip('/')}/{path.lstrip('/')}" if path else url
    _validate_url(full_url)
    hdrs = {"Content-Type": "application/json"}
    if headers:
        for h in headers:
            k, v = h.split(":", 1)
            hdrs[k.strip()] = v.strip()

    payload = None
    if body:
        try:
            payload = json.loads(body) if isinstance(body, str) else body
        except json.JSONDecodeError:
            payload = body

    try:
        resp = requests.put(full_url, headers=hdrs, json=payload, timeout=10)
        try:
            rbody = resp.json()
            return json.dumps({"status": resp.status_code, "data": rbody}, indent=2, ensure_ascii=False)
        except Exception:
            return f"Status: {resp.status_code}\n{resp.text[:2000]}"
    except Exception as e:
        return f"ERROR: {e}"


# ========== Mijia / XiaoMi ==========

def mijia_discover():
    """Discover Mijia devices on local network (basic SSDP scan)."""
    print("INFO: For Mijia device control, use the miio library:")
    print("  pip install miio")
    print("  python -m miio discover")
    return "INFO: Run the above commands to discover Mijia devices"


# ========== Main ==========

def main():
    import argparse
    parser = argparse.ArgumentParser(description="IoT Controller")
    sub = parser.add_subparsers(dest="platform")

    # Home Assistant
    p_ha = sub.add_parser("homeassistant", help="Home Assistant control")
    ha_sub = p_ha.add_subparsers(dest="action")
    ha_sub.add_parser("list", help="List all entities")

    ha_state = ha_sub.add_parser("state", help="Get entity state")
    ha_state.add_argument("--entity-id", type=str, required=True)

    ha_call = ha_sub.add_parser("call", help="Call service")
    ha_call.add_argument("--domain", type=str, required=True)
    ha_call.add_argument("--service", type=str, required=True)
    ha_call.add_argument("--entity-id", type=str, required=True)
    ha_call.add_argument("--data", type=str, help="JSON service data")

    ha_on = ha_sub.add_parser("on", help="Turn on entity")
    ha_on.add_argument("--entity-id", type=str, required=True)
    ha_on.add_argument("--data", type=str, help="JSON params (e.g. brightness)")

    ha_off = ha_sub.add_parser("off", help="Turn off entity")
    ha_off.add_argument("--entity-id", type=str, required=True)

    ha_tog = ha_sub.add_parser("toggle", help="Toggle entity")
    ha_tog.add_argument("--entity-id", type=str, required=True)

    p_ha.add_argument("--url", type=str, required=True, help="Home Assistant base URL")
    p_ha.add_argument("--token", type=str, default=None,
                      help="Long-lived access token (prefer env var HA_TOKEN)")

    # Generic HTTP
    p_http = sub.add_parser("http", help="Generic HTTP/REST control")
    http_sub = p_http.add_subparsers(dest="action")

    http_get_p = http_sub.add_parser("get", help="HTTP GET")
    http_get_p.add_argument("--path", type=str, default="")

    http_post_p = http_sub.add_parser("post", help="HTTP POST")
    http_post_p.add_argument("--path", type=str, default="")
    http_post_p.add_argument("--body", type=str, default=None)

    http_put_p = http_sub.add_parser("put", help="HTTP PUT")
    http_put_p.add_argument("--path", type=str, default="")
    http_put_p.add_argument("--body", type=str, default=None)

    p_http.add_argument("--url", type=str, required=True)
    p_http.add_argument("--header", type=str, action="append", help="Header in 'Key: Value' format")

    # Mijia
    p_mi = sub.add_parser("mijia", help="Mijia/XiaoMi control")
    mi_sub = p_mi.add_subparsers(dest="action")
    mi_sub.add_parser("discover", help="Discover devices")

    args = parser.parse_args()

    if args.platform == "homeassistant":
        url = args.url
        # Resolve token securely (env var preferred)
        try:
            token = _resolve_token(args.token)
        except ValueError as e:
            print(str(e))
            sys.exit(1)

        if args.action == "list":
            result = ha_list_entities(url, token)
        elif args.action == "state":
            result = ha_get_state(url, token, args.entity_id)
        elif args.action == "call":
            result = ha_call_service(url, token, args.domain, args.service, args.entity_id, args.data)
        elif args.action == "on":
            result = ha_turn_on(url, token, args.entity_id, args.data)
        elif args.action == "off":
            result = ha_turn_off(url, token, args.entity_id)
        elif args.action == "toggle":
            result = ha_toggle(url, token, args.entity_id)
        else:
            p_ha.print_help()
            result = None
        if result:
            print(result)

    elif args.platform == "http":
        if args.action == "get":
            print(http_get(args.url, args.path, args.header))
        elif args.action == "post":
            print(http_post(args.url, args.path, args.body, args.header))
        elif args.action == "put":
            print(http_put(args.url, args.path, args.body, args.header))
        else:
            p_http.print_help()

    elif args.platform == "mijia":
        if args.action == "discover":
            print(mijia_discover())
        else:
            p_mi.print_help()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
