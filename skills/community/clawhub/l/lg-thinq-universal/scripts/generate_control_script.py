import json
import sys
import os
import re


# Security: Strict Sanitization (Allowlist approach)
def sanitize(name):
    """Only allow alphanumeric and underscore to prevent injection."""
    return re.sub(r"[^a-zA-Z0-9_]", "", str(name))


def get_cli_value_expression(meta):
    """Convert CLI input into the expected Python type for the property."""
    prop_type = meta.get("type")
    if prop_type == "range":
        step = meta.get("value", {}).get("w", {}).get("step")
        return "int(filtered_args[1])" if step == 1 else "float(filtered_args[1])"
    if prop_type == "number":
        return "parse_number(filtered_args[1])"
    if prop_type == "boolean":
        return "filtered_args[1].lower() in ('1', 'true', 'yes', 'on')"
    return "filtered_args[1]"


def get_power_values(meta):
    """Return the writable/readable power values from the profile metadata."""
    value_meta = meta.get("value", {})
    writable = value_meta.get("w", []) if isinstance(value_meta, dict) else []
    readable = value_meta.get("r", []) if isinstance(value_meta, dict) else []
    combined = []
    for source in (writable, readable):
        if isinstance(source, list):
            combined.extend(source)
    return combined


def get_defaults():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(script_dir) # Go up one level from scripts/
        defaults_path = os.path.join(
            base_dir, "references", "public_api_constants.json"
        )
        with open(defaults_path, "r") as f:
            return json.load(f)
    except Exception:
        return {}


DEFAULTS = get_defaults()

TEMPLATE = """import os, sys, json, time, requests, re
from dotenv import load_dotenv

# Security Note: This script uses load_dotenv(override=False).
# Your LG_PAT and LG_COUNTRY should be managed in your shell environment.
# Local .env in the skill directory is only for LG_DEVICE_ID.
script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, ".env")
if os.path.exists(env_path):
    load_dotenv(env_path, override=False)

# Configuration from .env with fallbacks
# API Server Priority: env var > .api_server_cache > default
API_SERVER_CACHE = os.path.join(script_dir, ".api_server_cache")
if os.getenv("LG_API_SERVER"):
    BASE_URL = os.getenv("LG_API_SERVER")
elif os.path.exists(API_SERVER_CACHE):
    with open(API_SERVER_CACHE, "r") as f:
        BASE_URL = f.read().strip()
else:
    BASE_URL = "https://api-kic.lgthinq.com"

PAT = os.getenv("LG_PAT")
DEVICE_ID = os.getenv("LG_DEVICE_ID")

# Standard API Defaults (from references/defaults.json)
API_KEY = os.getenv("LG_API_KEY", "{api_key}")
CLIENT_ID = os.getenv("LG_CLIENT_ID", "{client_id}")
COUNTRY = os.getenv("LG_COUNTRY", "IN")
MESSAGE_ID = os.getenv("LG_MESSAGE_ID", "{message_id}")
SERVICE_PHASE = os.getenv("LG_SERVICE_PHASE", "{service_phase}")

def get_headers(snapshot=None):
    if not PAT:
        return None # Handled in request_with_retry
        
    headers = {{
        "Authorization": f"Bearer {{PAT}}",
        "x-api-key": API_KEY,
        "x-client-id": CLIENT_ID,
        "x-country": COUNTRY,
        "x-message-id": MESSAGE_ID,
        "Content-Type": "application/json",
    }}
    if snapshot:
        headers["x-conditional-control"] = json.dumps({{"snapshot": snapshot}})
    return headers

def request_with_retry(method, path, payload=None, snapshot=None):
    if not DEVICE_ID:
        return {{"success": False, "error": "Missing LG_DEVICE_ID. Ensure it is set in your .env file."}}
    if not PAT:
        return {{"success": False, "error": "Missing LG_PAT. Ensure it is exported in your shell."}}

    url = f"{{BASE_URL}}{{path}}"
    headers = get_headers(snapshot)
    try:
        res = requests.request(method=method, url=url, headers=headers, json=payload, timeout=15)
        
        # Structured Error Handling
        if res.status_code == 401:
            return {{"success": False, "status": 401, "error": "Unauthorized. Your LG_PAT may be expired. Refresh it at connect-pat.lgthinq.com"}}
        if res.status_code == 404:
            return {{"success": False, "status": 404, "error": f"Device {{DEVICE_ID}} not found. Check your LG_DEVICE_ID."}}
        
        return {{"success": res.status_code == 200, "data": res.json(), "status": res.status_code}}
    except Exception as e:
        return {{"success": False, "error": str(e)}}

def get_current_snapshot(category, property_name):
    \"\"\"Fetch current state using the LITERAL property name\"\"\"
    res = request_with_retry("GET", f"/devices/{{DEVICE_ID}}/state")
    if res["success"]:
        val = res["data"].get("response", {{}}).get(category, {{}}).get(property_name)
        return {{f"{{category}}.{{property_name}}": val}}
    return None

def control_property(category, property_name, value):
    snapshot = get_current_snapshot(category, property_name)
    payload = {{category: {{property_name: value}}}}
    return request_with_retry("POST", f"/devices/{{DEVICE_ID}}/control", payload, snapshot)

def get_status():
    return request_with_retry("GET", f"/devices/{{DEVICE_ID}}/state")

def parse_number(value):
    try:
        return int(value)
    except ValueError:
        return float(value)

# ============ GENERATED COMMANDS ============

{commands_logic}

# ============ CLI ============

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        commands_help = \"\"\"{commands_help}\"\"\"
        print(f"LG Device Control Script - {{DEVICE_ID or 'NOT_SET'}}\\n")
        print("Usage: python3 lg_control.py <command> [value]\\n")
        print("Commands:")
        print("  status              Get current device state")
        print("  on                  Turn device on (POWER_ON)")
        print("  off                 Turn device off (POWER_OFF)")
        print(commands_help)
        print("\\nExamples:")
        print("  python3 lg_control.py status")
        print("  python3 lg_control.py on")
        print("  python3 lg_control.py <property> <value>")
        return

    filtered_args = sys.argv[1:]
    if not filtered_args:
        print(json.dumps({{"success": False, "error": "Missing command"}}))
        return
    cmd = filtered_args[0].lower()
    
{cli_logic}
    elif cmd == "status":
        print(json.dumps(get_status()))
    else:
        print(json.dumps({{"success": False, "error": f"Unknown command: {{cmd}}"}}))

if __name__ == "__main__":
    main()
"""


def generate_script(profile_json):
    data = json.loads(profile_json)
    properties = data.get("response", {}).get("property", {})

    commands_logic = []
    cli_logic = []
    commands_help = []

    first = True
    for raw_category, props in properties.items():
        if not isinstance(props, dict):
            continue

        s_category = sanitize(raw_category)

        for raw_prop_name, meta in props.items():
            if not isinstance(meta, dict):
                continue

            s_prop_name = sanitize(raw_prop_name)

            mode = meta.get("mode", [])
            if "w" in mode:
                s_func = f"cmd_{s_category.lower()}_{s_prop_name.lower()}"
                logic = f"def {s_func}(value):\\n    return control_property({repr(raw_category)}, {repr(raw_prop_name)}, value)"
                commands_logic.append(logic.replace("\\n", "\n"))

                condition = "if" if first else "elif"
                val_conversion = get_cli_value_expression(meta)
                cli = f"    {condition} cmd == {repr(s_prop_name.lower())}:\\n        if len(filtered_args) < 2: print(json.dumps({{'error': 'Missing value'}}))\\n        else: print(json.dumps({s_func}({val_conversion})))"
                cli_logic.append(cli.replace("\\n", "\n"))

                cmd_name = s_prop_name.lower()
                val_hint = "<value>"
                if meta.get("type") == "range":
                    range_meta = meta.get("value", {}).get("w", {})
                    minimum = range_meta.get("min")
                    maximum = range_meta.get("max")
                    if minimum is not None and maximum is not None:
                        val_hint = f"<{minimum}-{maximum}>"
                commands_help.append(
                    f"  {cmd_name} {val_hint}     Set {s_prop_name} ({raw_category})"
                )
                first = False

    power_prop = None
    for raw_cat, props in properties.items():
        if not isinstance(props, dict):
            continue
        for raw_prop, meta in props.items():
            values = get_power_values(meta)
            if "POWER_ON" in values and "POWER_OFF" in values:
                power_prop = (raw_cat, raw_prop)
                break
        if power_prop:
            break

    if power_prop:
        cat, prop = power_prop
        cli_logic.append(
            f"    elif cmd == 'on':\\n        print(json.dumps(control_property({repr(cat)}, {repr(prop)}, 'POWER_ON')))".replace("\\n", "\n")
        )
        cli_logic.append(
            f"    elif cmd == 'off':\\n        print(json.dumps(control_property({repr(cat)}, {repr(prop)}, 'POWER_OFF')))".replace("\\n", "\n")
        )

    return TEMPLATE.format(
        api_key=DEFAULTS.get("LG_API_KEY", ""),
        client_id=DEFAULTS.get("LG_CLIENT_ID", ""),
        message_id=DEFAULTS.get("LG_MESSAGE_ID", ""),
        service_phase=DEFAULTS.get("LG_SERVICE_PHASE", ""),
        commands_logic="\n".join(commands_logic),
        cli_logic="\n".join(cli_logic),
        commands_help="\n".join(commands_help),
    )


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print("Usage: python3 generate_control_script.py profile.json")
        sys.exit(1)

    profile_path = sys.argv[1]
    env_device_id = os.getenv("LG_DEVICE_ID")
    
    if env_device_id:
        sys.stderr.write(f"INFO: Generating control script for specific device ID: {env_device_id}\n")
    else:
        sys.stderr.write("WARNING: No LG_DEVICE_ID found in environment. The generated script will default to 'NOT_SET'.\n")
        sys.stderr.write("         Ensure the agent writes the correct ID to the local .env file during setup.\n")

    with open(profile_path, "r") as f:
        print(generate_script(f.read()))
