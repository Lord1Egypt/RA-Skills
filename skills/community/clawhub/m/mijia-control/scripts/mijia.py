#!/usr/bin/env python3
"""
Mi Home (米家) Cloud Controller
Controls Xiaomi smart home devices via Xiaomi Cloud API.

Usage:
  python3 mijia.py login                         # Login and save credentials
  python3 mijia.py devices                        # List all devices
  python3 mijia.py status <did>                   # Read device properties
  python3 mijia.py set <did> <siid> <piid> <val>  # Set a device property
  python3 mijia.py get <did> <siid> <piid>        # Get a device property
  python3 mijia.py scene_create <json_file>       # Create automation scene
  python3 mijia.py scene_list                     # List automation scenes
  python3 mijia.py batch <json_file>              # Execute batch commands

Credentials are stored in ~/.mijia_creds.json (auto-refreshed via browser cookies).
"""

import sys, os, json, hashlib, time, argparse
from pathlib import Path

# Ensure micloud is available
try:
    from micloud import MiCloud
    from micloud.miutils import get_session
except ImportError:
    print("ERROR: micloud not installed. Run: pip3 install micloud", file=sys.stderr)
    sys.exit(1)

CREDS_PATH = Path.home() / ".mijia_creds.json"
DEVICES_CACHE = Path.home() / ".mijia_devices.json"

def load_creds():
    if not CREDS_PATH.exists():
        print(f"ERROR: No credentials found at {CREDS_PATH}", file=sys.stderr)
        print("Run 'python3 mijia.py login' first, or create the file manually.", file=sys.stderr)
        sys.exit(1)
    return json.loads(CREDS_PATH.read_text())

def save_creds(creds):
    CREDS_PATH.write_text(json.dumps(creds, indent=2))
    CREDS_PATH.chmod(0o600)

def get_cloud():
    creds = load_creds()
    mc = MiCloud.__new__(MiCloud)
    mc.user_id = int(creds["userId"])
    mc.service_token = creds["serviceToken"]
    mc.ssecurity = creds["ssecurity"]
    mc.cuser_id = creds.get("cUserId", "")
    mc.session = None
    mc.locale = "zh_CN"
    mc.timezone = "GMT+08:00"
    mc.default_server = "cn"
    mc.failed_logins = 0
    return mc

def cmd_login(args):
    """Interactive login - saves credentials."""
    username = args.username or input("Xiaomi username (phone): ")
    password = args.password or input("Xiaomi password: ")
    
    mc = MiCloud(username, password)
    try:
        mc.login()
        creds = {
            "userId": str(mc.user_id),
            "serviceToken": mc.service_token,
            "ssecurity": mc.ssecurity,
            "cUserId": mc.cuser_id or ""
        }
        save_creds(creds)
        print(f"Login successful! Credentials saved to {CREDS_PATH}")
    except Exception as e:
        print(f"Login failed: {e}", file=sys.stderr)
        print("If 2FA is required, obtain credentials via browser and save manually.", file=sys.stderr)
        sys.exit(1)

def cmd_devices(args):
    """List all devices."""
    mc = get_cloud()
    devices = mc.get_devices(country="cn")
    if not devices:
        print("No devices found or API error.")
        return
    
    # Cache devices
    DEVICES_CACHE.write_text(json.dumps(devices, ensure_ascii=False, indent=2))
    
    print(f"Found {len(devices)} devices:\n")
    for d in devices:
        online = "🟢" if d.get("isOnline") else "🔴"
        print(f"{online} {d.get('name')} | model: {d.get('model')} | did: {d.get('did')} | ip: {d.get('localip','N/A')}")

def cmd_get(args):
    """Get a device property."""
    mc = get_cloud()
    params = {"data": json.dumps({"params": [
        {"did": args.did, "siid": int(args.siid), "piid": int(args.piid)}
    ]})}
    r = mc.request_country("/miotspec/prop/get", "cn", params)
    data = json.loads(r if isinstance(r, str) else r.decode())
    result = data.get("result", [{}])[0]
    if result.get("code") == 0:
        print(json.dumps({"value": result["value"]}, ensure_ascii=False))
    else:
        print(json.dumps({"error": result.get("code")}, ensure_ascii=False))

def cmd_set(args):
    """Set a device property."""
    mc = get_cloud()
    # Auto-detect value type
    val = args.value
    if val.lower() == "true": val = True
    elif val.lower() == "false": val = False
    else:
        try: val = int(val)
        except:
            try: val = float(val)
            except: pass
    
    params = {"data": json.dumps({"params": [
        {"did": args.did, "siid": int(args.siid), "piid": int(args.piid), "value": val}
    ]})}
    r = mc.request_country("/miotspec/prop/set", "cn", params)
    data = json.loads(r if isinstance(r, str) else r.decode())
    result = data.get("result", [{}])[0]
    code = result.get("code", -1)
    # code:0 = confirmed success, code:1 = sent (mesh async), both are OK
    if code in (0, 1):
        print(json.dumps({"ok": True, "code": code}, ensure_ascii=False))
    else:
        print(json.dumps({"ok": False, "code": code}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

def cmd_status(args):
    """Read common properties of a device."""
    mc = get_cloud()
    # Read siid 2-10, piid 1-5
    props = []
    for siid in range(2, 11):
        for piid in range(1, 6):
            props.append({"did": args.did, "siid": siid, "piid": piid})
    
    params = {"data": json.dumps({"params": props})}
    r = mc.request_country("/miotspec/prop/get", "cn", params)
    data = json.loads(r if isinstance(r, str) else r.decode())
    
    results = []
    for p in data.get("result", []):
        if p.get("code") == 0:
            results.append({"siid": p["siid"], "piid": p["piid"], "value": p["value"]})
    print(json.dumps(results, ensure_ascii=False, indent=2))

def cmd_batch(args):
    """Execute batch set commands from JSON file."""
    mc = get_cloud()
    commands = json.loads(Path(args.json_file).read_text())
    
    params_list = []
    for cmd in commands:
        params_list.append({
            "did": cmd["did"],
            "siid": cmd["siid"],
            "piid": cmd["piid"],
            "value": cmd["value"]
        })
    
    params = {"data": json.dumps({"params": params_list})}
    r = mc.request_country("/miotspec/prop/set", "cn", params)
    data = json.loads(r if isinstance(r, str) else r.decode())
    
    for result in data.get("result", []):
        code = result.get("code", -1)
        ok = "✅" if code in (0, 1) else "❌"
        print(f"{ok} did:{result['did']} siid:{result['siid']} piid:{result['piid']} code:{code}")

def cmd_tts(args):
    """Make a XiaoAI speaker say text aloud."""
    import time as _time
    mc = get_cloud()
    did = args.did
    text = args.text

    def _action(siid, aiid, ins):
        params = {"data": json.dumps({"params": {"did": did, "siid": siid, "aiid": aiid, "in": ins}})}
        r = mc.request_country("/miotspec/action", "cn", params)
        return json.loads(r if isinstance(r, str) else r.decode())

    def _set(props):
        params = {"data": json.dumps({"params": [{"did": did, **p} for p in props]})}
        mc.request_country("/miotspec/prop/set", "cn", params)

    # 1. Unmute + ensure volume
    _set([{"siid": 2, "piid": 2, "value": False}, {"siid": 2, "piid": 1, "value": int(args.volume)}])
    _time.sleep(0.5)

    # 2. Play text (siid:5 aiid:1, in: piid:1=text)
    result = _action(5, 1, [{"piid": 1, "value": text}])
    code = result.get("result", {}).get("code", -1)
    print(json.dumps({"ok": code == 0, "code": code}, ensure_ascii=False))

    # 3. Wait for speech to finish (~0.15s per char + 2s buffer)
    wait = max(2, len(text) * 0.15 + 2)
    _time.sleep(wait)

    # 4. Pause playback to prevent auto-music
    _action(3, 2, [])

    # 5. Re-mute if requested
    if args.remute:
        _set([{"siid": 2, "piid": 2, "value": True}])

def cmd_scene_create(args):
    """Create an automation scene from JSON definition."""
    mc = get_cloud()
    scene = json.loads(Path(args.json_file).read_text())
    
    # Ensure required fields
    if "home_id" not in scene:
        scene["home_id"] = _get_home_id(mc)
    if "uid" not in scene:
        scene["uid"] = mc.user_id
    if "st_id" not in scene:
        scene["st_id"] = 8
    if "setting" not in scene:
        scene["setting"] = {"enable": 1, "enable_push": 0}
    if "identify" not in scene:
        scene["identify"] = f"scene_{int(time.time())}"
    
    params = {"data": json.dumps(scene)}
    r = mc.request_country("/scene/edit", "cn", params)
    if isinstance(r, bytes):
        r = r.decode()
    data = json.loads(r) if isinstance(r, str) else r
    print(json.dumps(data, ensure_ascii=False, indent=2))

def cmd_scene_list(args):
    """List existing scenes."""
    mc = get_cloud()
    home_id = _get_home_id(mc)
    
    params = {"data": json.dumps({"home_id": home_id, "req_type": 1})}
    r = mc.request_country("/appgateway/miot/appsceneservice/AppSceneService/GetSceneList", "cn", params)
    data = json.loads(r if isinstance(r, str) else r.decode())
    
    if data.get("code") == 0:
        scenes = data.get("result", {}).get("scene_info_list", [])
        print(f"Found {len(scenes)} scenes:")
        for s in scenes:
            print(f"  - {s.get('name','')} | id:{s.get('scene_id','')}")
    else:
        print(f"Error: {data}")

def _get_home_id(mc):
    """Get the first home ID."""
    params = {"data": json.dumps({"fg": True, "fetch_share": True, "limit": 10, "app_ver": 7})}
    r = mc.request_country("/v2/homeroom/gethome", "cn", params)
    data = json.loads(r if isinstance(r, str) else r.decode())
    homes = data.get("result", {}).get("homelist", [])
    return homes[0]["id"] if homes else 0

def main():
    parser = argparse.ArgumentParser(description="Mi Home Cloud Controller")
    sub = parser.add_subparsers(dest="command")
    
    p_login = sub.add_parser("login", help="Login to Xiaomi Cloud")
    p_login.add_argument("--username", "-u")
    p_login.add_argument("--password", "-p")
    
    sub.add_parser("devices", help="List all devices")
    
    p_get = sub.add_parser("get", help="Get device property")
    p_get.add_argument("did")
    p_get.add_argument("siid")
    p_get.add_argument("piid")
    
    p_set = sub.add_parser("set", help="Set device property")
    p_set.add_argument("did")
    p_set.add_argument("siid")
    p_set.add_argument("piid")
    p_set.add_argument("value")
    
    p_status = sub.add_parser("status", help="Read device status")
    p_status.add_argument("did")
    
    p_batch = sub.add_parser("batch", help="Batch set from JSON")
    p_batch.add_argument("json_file")
    
    p_sc = sub.add_parser("scene_create", help="Create automation scene")
    p_sc.add_argument("json_file")
    
    p_tts = sub.add_parser("tts", help="Make speaker say text")
    p_tts.add_argument("did")
    p_tts.add_argument("text")
    p_tts.add_argument("--volume", type=int, default=50)
    p_tts.add_argument("--no-remute", dest="remute", action="store_false", default=True)

    sub.add_parser("scene_list", help="List scenes")
    
    args = parser.parse_args()
    
    commands = {
        "login": cmd_login, "devices": cmd_devices, "get": cmd_get,
        "set": cmd_set, "status": cmd_status, "batch": cmd_batch, "tts": cmd_tts,
        "scene_create": cmd_scene_create, "scene_list": cmd_scene_list
    }
    
    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
