import os, sys, json, requests, re
from dotenv import load_dotenv

# Load environment variables
# 1. Load from current directory (e.g. for LG_DEVICE_ID in sub-skills)
script_dir = os.path.dirname(os.path.abspath(__file__))
current_env = os.path.join(os.getcwd(), ".env")
if os.path.exists(current_env):
    load_dotenv(current_env, override=False)

# 2. Load from parent directory (e.g. for LG_PAT in the universal root)
project_root = os.path.dirname(script_dir) 
root_env = os.path.join(project_root, ".env")
if os.path.exists(root_env):
    load_dotenv(root_env, override=False)

# Cache file for API server (always in the universal root for consistency)
CACHE_DIR = project_root
API_SERVER_CACHE = os.path.join(CACHE_DIR, ".api_server_cache")


def get_defaults():
    """Load standard API defaults from bundled reference file"""
    # Try current folder references/ first (for sub-skills)
    local_path = os.path.join(script_dir, "references", "public_api_constants.json")
    # Try parent root references/ second (for universal root)
    parent_path = os.path.join(project_root, "references", "public_api_constants.json")
    
    for p in [local_path, parent_path]:
        if os.path.exists(p):
            try:
                with open(p, "r") as f:
                    return json.load(f)
            except Exception:
                continue
    return {}


DEFAULTS = get_defaults()

# Environment Variables with Documentation Defaults
PAT = os.getenv("LG_PAT")
COUNTRY = os.getenv("LG_COUNTRY")
API_KEY = os.getenv("LG_API_KEY", DEFAULTS.get("LG_API_KEY"))
CLIENT_ID = os.getenv("LG_CLIENT_ID", DEFAULTS.get("LG_CLIENT_ID"))
MESSAGE_ID = os.getenv("LG_MESSAGE_ID", DEFAULTS.get("LG_MESSAGE_ID"))
SERVICE_PHASE = os.getenv("LG_SERVICE_PHASE", DEFAULTS.get("LG_SERVICE_PHASE"))
DEVICE_ID = os.getenv("LG_DEVICE_ID")
API_SERVER = os.getenv("LG_API_SERVER")  # Cached route - set via `save-route` command

# Check for debug flag in sys.argv
DEBUG = "--debug" in sys.argv


def log_debug(msg):
    if DEBUG:
        sys.stderr.write(f"DEBUG: {msg}\n")


def get_route_entry_point(country):
    """Select the correct initial route URL based on region."""
    americas = ["US", "CA", "MX", "BR", "AR", "CL", "CO"]
    emea = ["GB", "FR", "DE", "IT", "ES", "RU", "ZA", "AE", "SA", "TR"]
    if country in americas:
        return "https://api-aic.lgthinq.com/route"
    elif country in emea:
        return "https://api-eic.lgthinq.com/route"
    return "https://api-kic.lgthinq.com/route"


def _fetch_route_api():
    """Internal: Call route API and return the apiServer URL."""
    entry_point = get_route_entry_point(COUNTRY)
    headers = {
        "x-api-key": API_KEY,
        "x-country": COUNTRY,
        "x-service-phase": SERVICE_PHASE,
        "x-message-id": MESSAGE_ID,
    }
    log_debug(f"Calling Route API: {entry_point}")
    log_debug(f"Route Headers: {json.dumps(headers)}")

    res = requests.get(entry_point, headers=headers, timeout=10)
    data = res.json()
    log_debug(f"Route Response: {json.dumps(data)}")
    return data["response"]["apiServer"]


def get_base_url():
    """Get the regional API base URL. Priority: env var > cache file > route API."""
    if API_SERVER:
        return API_SERVER

    if os.path.exists(API_SERVER_CACHE):
        with open(API_SERVER_CACHE, "r") as f:
            server = f.read().strip()
            if server:
                return server

    try:
        server = _fetch_route_api()
        # AUTO-CACHE: Save discovered route for next time
        try:
            with open(API_SERVER_CACHE, "w") as f:
                f.write(server)
        except Exception:
            pass # Ignore write errors during auto-cache
        return server
    except Exception as e:
        log_debug(f"Route discovery failed: {str(e)}")
        # Fallback to KIC if route API fails
        return "https://api-kic.lgthinq.com"


def save_route():
    """Call route API and save result to cache file for future use."""
    try:
        server = _fetch_route_api()

        with open(API_SERVER_CACHE, "w") as f:
            f.write(server)

        return {"success": True, "apiServer": server, "cacheFile": API_SERVER_CACHE}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_device_headers(snapshot=None):
    """Headers required for Device APIs (List, Profile, State, Control)"""
    if not PAT or not COUNTRY:
        print(json.dumps({"success": False, "error": "Missing LG_PAT or LG_COUNTRY"}))
        sys.exit(1)

    headers = {
        "Authorization": f"Bearer {PAT}",
        "x-api-key": API_KEY,
        "x-client-id": CLIENT_ID,
        "x-country": COUNTRY,
        "x-message-id": MESSAGE_ID,
        # x-service-phase IS NOT used here as per documentation
        "Content-Type": "application/json",
    }
    if snapshot:
        headers["x-conditional-control"] = json.dumps({"snapshot": snapshot})
    return headers


def api_request(method, path, payload=None, snapshot=None):
    base_url = get_base_url()
    url = f"{base_url}{path}"
    headers = get_device_headers(snapshot)

    log_debug(f"API Request: {method} {url}")
    # Mask PAT in debug logs
    debug_headers = {
        k: (v if k != "Authorization" else "Bearer ***") for k, v in headers.items()
    }
    log_debug(f"Headers: {json.dumps(debug_headers)}")

    try:
        res = requests.request(method, url, headers=headers, json=payload, timeout=15)
        log_debug(f"API Response Status: {res.status_code}")
        return res.json()
    except Exception as e:
        return {"success": False, "error": str(e)}


def list_devices():
    return api_request("GET", "/devices")


def get_profile(device_id):
    return api_request("GET", f"/devices/{device_id}/profile")


def get_state(device_id):
    return api_request("GET", f"/devices/{device_id}/state")


def control(device_id, category, property_name, value):
    state_res = get_state(device_id)
    current_val = state_res.get("response", {}).get(category, {}).get(property_name)
    snapshot = {f"{category}.{property_name}": current_val}
    payload = {category: {property_name: value}}
    return api_request("POST", f"/devices/{device_id}/control", payload, snapshot)


def validate_config():
    """Verify all required environment variables and constants are present and valid."""
    errors = []
    if not PAT:
        errors.append("LG_PAT is missing.")
    if not COUNTRY:
        errors.append("LG_COUNTRY is missing.")
    elif not re.match(r"^[A-Z]{2}$", COUNTRY or ""):
        errors.append(f"LG_COUNTRY '{COUNTRY}' is not a valid 2-letter ISO code.")
    if not DEFAULTS:
        errors.append("Could not load public_api_constants.json.")
    return {"success": len(errors) == 0, "errors": errors}


def check_config():
    """Friendly config check for humans. Returns structured output for machines."""
    results = []
    issues = []

    pat = os.getenv("LG_PAT")
    country = os.getenv("LG_COUNTRY")
    api_server = os.getenv("LG_API_SERVER")

    if pat:
        results.append(f"✅ LG_PAT: set ({len(pat)} chars)")
    else:
        issues.append("❌ LG_PAT: missing")

    if country:
        if re.match(r"^[A-Z]{2}$", country):
            results.append(f"✅ LG_COUNTRY: {country}")
        else:
            issues.append(
                f"❌ LG_COUNTRY: invalid ('{country}' - must be 2-letter ISO)"
            )
    else:
        issues.append("❌ LG_COUNTRY: missing")

    if api_server:
        results.append(f"✅ LG_API_SERVER: {api_server}")
    else:
        results.append("⚠️  LG_API_SERVER: not set (will auto-discover via route API)")

    return {"success": len(issues) == 0, "summary": results + issues, "issues": issues}


HELP_TEXT = """LG ThinQ API Tool - Device discovery and control

Usage: python3 lg_api_tool.py <command> [args] [--debug]

Commands:
  validate       Check required env vars (LG_PAT, LG_COUNTRY, defaults)
  check-config   Human-friendly config status (recommended before first run)
  get-route     Get current API server URL
  save-route    Discover and cache API server to .api_server_cache
  list-devices  List all connected LG ThinQ devices
  get-profile   Get device profile (requires device_id)
  get-state     Get device current state (requires device_id)
  control       Control device (requires: device_id category property value)

Options:
  --debug       Enable debug output (shows API calls, headers)

Examples:
  python3 lg_api_tool.py check-config
  python3 lg_api_tool.py save-route
  python3 lg_api_tool.py list-devices
  python3 lg_api_tool.py get-profile <device_id>
  python3 lg_api_tool.py get-state <device_id>
  python3 lg_api_tool.py control <device_id> <category> <property> <value>
"""


def main():
    filtered_args = [arg for arg in sys.argv if arg != "--debug"]

    if len(filtered_args) < 2 or filtered_args[1] in ("-h", "--help"):
        print(HELP_TEXT)
        sys.exit(0)

    cmd = filtered_args[1]

    if cmd == "validate":
        print(json.dumps(validate_config()))
    elif cmd == "check-config":
        config = check_config()
        print("\n".join(config["summary"]))
        print()
        sys.exit(0 if config["success"] else 1)
    elif cmd == "get-route":
        print(json.dumps({"success": True, "apiServer": get_base_url()}))
    elif cmd == "save-route":
        result = save_route()
        if result["success"]:
            log_debug(f"Route saved to {result['cacheFile']}")
        print(json.dumps(result))
    elif cmd == "list-devices":
        print(json.dumps(list_devices()))
    elif cmd == "get-profile":
        d_id = filtered_args[2] if len(filtered_args) > 2 else DEVICE_ID
        if not d_id:
            print(json.dumps({"error": "Missing device_id"}))
            sys.exit(1)
        print(json.dumps(get_profile(d_id)))
    elif cmd == "get-state":
        d_id = filtered_args[2] if len(filtered_args) > 2 else DEVICE_ID
        if not d_id:
            print(json.dumps({"error": "Missing device_id"}))
            sys.exit(1)
        print(json.dumps(get_state(d_id)))
    elif cmd == "control":
        if len(filtered_args) < 6:
            print(
                json.dumps(
                    {
                        "error": "Usage: control <device_id> <category> <property> <value>"
                    }
                )
            )
            sys.exit(1)
        print(
            json.dumps(
                control(
                    filtered_args[2],
                    filtered_args[3],
                    filtered_args[4],
                    filtered_args[5],
                )
            )
        )
    else:
        print(json.dumps({"error": f"Unknown command: {cmd}"}))


if __name__ == "__main__":
    main()
