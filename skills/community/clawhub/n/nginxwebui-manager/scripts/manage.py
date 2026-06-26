#!/usr/bin/env python3
"""
NginxWebUI Manager — manage reverse proxies via NginxWebUI API.
All calls are made via docker exec into the nginxwebui container.
Features: auto-login on token expiry, unified auth check.
"""
import json, os, re, subprocess, sys, urllib.parse
from datetime import datetime, timezone, timedelta

# Auto-load .env from workspace root
_env_path = '/home/node/.openclaw/workspace/liyj/.env'
if os.path.isfile(_env_path):
    with open(_env_path) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and '=' in _line and not _line.startswith('#'):
                _k, _v = _line.split('=', 1)
                os.environ.setdefault(_k.strip(), _v.strip())

USER = os.environ.get("NGINXWEBUI_USER")
if not USER:
    print("❌ NGINXWEBUI_USER environment variable required")
    sys.exit(1)
PASS = os.environ.get("NGINXWEBUI_PASS")
if not PASS:
    print("❌ NGINXWEBUI_PASS environment variable required")
    sys.exit(1)

API_BASE = "http://127.0.0.1:8081"
cst = timezone(timedelta(hours=8))

def log(msg):
    t = datetime.now().astimezone(cst).strftime("%H:%M:%S")
    print(f"  [{t}] {msg}")

# ── Auth ──────────────────────────────────────────────────────

def login():
    """Get and save API token."""
    log("Logging in...")
    token, _ = raw_api("POST", "/token/getToken", data=f"name={USER}&pass={PASS}")
    if token:
        os.environ["NGINXWEBUI_TOKEN"] = token
        # Persist to .env
        env_file = "/home/node/.openclaw/workspace/liyj/.env"
        with open(env_file) as f:
            content = f.read()
        if "NGINXWEBUI_TOKEN=" in content:
            content = re.sub(r"NGINXWEBUI_TOKEN=.*",
                             f"NGINXWEBUI_TOKEN={token}", content)
        else:
            content += f"\nNGINXWEBUI_TOKEN={token}\n"
        with open(env_file, "w") as f:
            f.write(content)
        log(f"✅ Token saved ({token[:12]}...)")
        return True
    log(f"❌ Login failed")
    return False

# ── API call with auto-retry on 401 ───────────────────────────

def raw_api(method, path, data=None):
    """Low-level API call returning (response_dict_or_None, is_unauthorized)."""
    cmd = ["docker", "exec", "nginxwebui", "curl", "-s", "-X", method,
           f"{API_BASE}{path}"]

    token = os.environ.get("NGINXWEBUI_TOKEN")
    if token:
        cmd.extend(["-H", f"token: {token}"])

    if data is not None:
        cmd.extend(["-d", data])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        output = result.stdout.strip()
        if not output:
            return None, False
        resp = json.loads(output)
        # Detect expired token
        is_401 = isinstance(resp, dict) and resp.get("status") == "401"
        return resp, is_401
    except subprocess.TimeoutExpired:
        return None, False
    except json.JSONDecodeError:
        return None, False
    except Exception:
        return None, False

def api(method, path, data=None):
    """API call with auto-retry on token expiry."""
    resp, is_401 = raw_api(method, path, data)
    if is_401:
        log("Token expired, re-logging in...")
        if login():
            resp, _ = raw_api(method, path, data)
    return resp

def extract_token(resp):
    """Extract token string from login response."""
    if resp and resp.get("success"):
        return resp.get("obj", {}).get("token", "")
    return None

def login():
    """Get and save API token."""
    log("Logging in...")
    resp, _ = raw_api("POST", "/token/getToken", data=f"name={USER}&pass={PASS}")
    token = extract_token(resp)
    if token:
        os.environ["NGINXWEBUI_TOKEN"] = token
        env_file = "/home/node/.openclaw/workspace/liyj/.env"
        with open(env_file) as f:
            content = f.read()
        if "NGINXWEBUI_TOKEN=" in content:
            content = re.sub(r"NGINXWEBUI_TOKEN=.*",
                             f"NGINXWEBUI_TOKEN={token}", content)
        else:
            content += f"\nNGINXWEBUI_TOKEN={token}\n"
        with open(env_file, "w") as f:
            f.write(content)
        log(f"✅ Token saved ({token[:12]}...)")
        return True
    log(f"❌ Login failed")
    return False

def ensure_token():
    """Ensure we have a token, login if missing."""
    if not os.environ.get("NGINXWEBUI_TOKEN"):
        return login()
    return True

# ── Server operations ─────────────────────────────────────────

def list_servers(keywords=""):
    log("Fetching servers...")
    resp = api("POST", "/api/server/getPage?current=1&limit=100",
               data=f"keywords={keywords}")
    if not resp or not resp.get("success"):
        log(f"❌ Failed: {resp}")
        return

    records = resp.get("obj", {}).get("records", [])
    log(f"Found {len(records)} server(s):")
    for s in records:
        sid = s.get("id", "?")[:12]
        name = s.get("serverName", "?")
        listen = s.get("listen", "?")
        ssl = "🔒" if s.get("ssl") else " "
        enable = "✅" if s.get("enable") else "⛔"
        desc = s.get("descr", "") or ""
        proxy = {0: "http", 1: "tcp", 2: "udp"}.get(s.get("proxyType", 0), "?")
        print(f"  [{sid}] {enable}{ssl} {name:40} {proxy}:{listen}  {desc}")
    return records

def get_server(server_id):
    resp = api("POST", "/api/server/getPage?current=1&limit=200")
    if not resp or not resp.get("success"):
        log(f"❌ Failed: {resp}")
        return None

    for s in resp.get("obj", {}).get("records", []):
        if s.get("id", "").startswith(server_id):
            print(f"  ID:       {s['id']}")
            print(f"  Name:     {s.get('serverName', '?')}")
            print(f"  Listen:   {s.get('listen', '?')}")
            print(f"  Proxy:    {['http','tcp','udp'][s.get('proxyType',0)]}")
            print(f"  SSL:      {'Yes' if s.get('ssl') else 'No'}")
            print(f"  HTTP/2:   {s.get('http2', 0)}")
            print(f"  Enable:   {s.get('enable', True)}")
            print(f"  Descr:    {s.get('descr', '') or '-'}")
            print(f"  Redirect: {'Yes' if s.get('rewrite') else 'No'}")
            print(f"  PEM:      {s.get('pem', '') or '-'}")
            print(f"  KEY:      {s.get('key', '') or '-'}")
            print(f"  Created:  {s.get('createTime', '?')}")
            print(f"  Updated:  {s.get('updateTime', '?')}")
            return s
    log("❌ Server not found")
    return None

def add_server(name, listen, ssl=False, pem="", key="", descr="", enable=True):
    data = urllib.parse.urlencode({
        "serverName": name,
        "listen": str(listen),
        "def": 0,
        "ipv6": 1,
        "rewrite": 0,
        "ssl": 1 if ssl else 0,
        "http2": 2 if ssl else 0,
        "enable": 1 if enable else 0,
        "descr": descr or "",
        "proxyType": 0,
        "protocols": "TLSv1 TLSv1.1 TLSv1.2 TLSv1.3",
    })
    if ssl:
        data += f"&pem={urllib.parse.quote(pem or '')}&key={urllib.parse.quote(key or '')}"

    log(f"Creating server: {name} on :{listen} {'🔒' if ssl else ''}")
    resp = api("POST", "/api/server/insertOrUpdate", data=data)
    if resp and resp.get("success"):
        sid = resp.get("obj", {}).get("id", "")[:12]
        log(f"✅ Server created: [{sid}] {name}")
        return resp.get("obj")
    log(f"❌ Failed: {resp}")
    return None

def delete_server(server_id):
    log(f"Deleting server {server_id[:12]}...")
    resp = api("POST", "/api/server/delete", data=f"id={server_id}")
    if resp and resp.get("success"):
        log("✅ Deleted")
        return True
    log(f"❌ Failed: {resp}")
    return False

# ── Location operations ───────────────────────────────────────

def list_locations(server_id):
    log(f"Fetching locations for server {server_id[:12]}...")
    resp = api("POST", "/api/server/getLocationByServerId",
               data=f"serverId={server_id}")
    if not resp or not resp.get("success"):
        log(f"❌ Failed: {resp}")
        return

    locs = resp.get("obj", [])
    log(f"Found {len(locs)} location(s):")
    for loc in locs:
        lid = loc.get("id", "?")[:12]
        path = loc.get("path", "?")
        target = loc.get("value", "") or loc.get("rootPath", "") or loc.get("returnUrl", "")
        type_map = {0: "proxy", 1: "static", 2: "upstream", 3: "blank", 4: "redirect"}
        ltype = type_map.get(loc.get("type", 0), "?")
        enable = "✅" if loc.get("enable") else "⛔"
        desc = loc.get("descr", "") or ""
        print(f"  [{lid}] {enable} {path:30} → {target:50}  [{ltype}]  {desc}")
    return locs

def add_location(server_id, path, target, type=0, descr="",
                 websocket=False, header=True, enable=True):
    data = urllib.parse.urlencode({
        "serverId": server_id,
        "path": path,
        "type": type,
        "value": target,
        "header": 1 if header else 0,
        "websocket": 1 if websocket else 0,
        "enable": 1 if enable else 0,
        "descr": descr or "",
    })
    log(f"Adding location: {path} → {target}")
    resp = api("POST", "/api/server/insertOrUpdateLocation", data=data)
    if resp and resp.get("success"):
        lid = resp.get("obj", {}).get("id", "")[:12]
        log(f"✅ Location created: [{lid}] {path} → {target}")
        return resp.get("obj")
    log(f"❌ Failed: {resp}")
    return None

def delete_location(loc_id):
    log(f"Deleting location {loc_id[:12]}...")
    resp = api("POST", "/api/server/deleteLocation", data=f"id={loc_id}")
    if resp and resp.get("success"):
        log("✅ Deleted")
        return True
    log(f"❌ Failed: {resp}")
    return False

# ── Nginx operations ──────────────────────────────────────────

def nginx_status():
    resp = api("POST", "/api/nginx/nginxStatus")
    if resp and resp.get("success"):
        log(f"Nginx: {resp.get('obj', '?')}")
        return resp.get("obj")
    log(f"❌ Failed: {resp}")

def reload_nginx():
    log("Step 1: Validating nginx config...")
    resp = api("POST", "/api/nginx/check")
    if not resp or not resp.get("success"):
        msg = resp.get("msg", "validation failed") if resp else "no response"
        log(f"❌ Config validation FAILED: {msg}")
        log("   Aborted reload.")
        return False

    log("✅ Config valid")
    log("Step 2: Reloading nginx...")
    resp = api("POST", "/api/nginx/reload")
    if resp and resp.get("success"):
        log("✅ Nginx reloaded")
        return True
    log(f"❌ Reload failed: {resp}")
    return False

def check_nginx():
    log("Checking nginx config...")
    resp = api("POST", "/api/nginx/check")
    if resp and resp.get("success"):
        log("✅ Config valid")
        return True
    log(f"❌ Failed: {resp}")
    return False

# ── Upstream operations ───────────────────────────────────────

def list_upstreams():
    log("Fetching upstreams...")
    resp = api("POST", "/api/upstream/getPage?current=1&limit=100")
    if not resp or not resp.get("success"):
        log(f"❌ Failed: {resp}")
        return

    records = resp.get("obj", {}).get("records", [])
    log(f"Found {len(records)} upstream(s):")
    for u in records:
        uid = u.get("id", "?")[:12]
        name = u.get("tactics", "?")
        servers = u.get("proxyList", [])
        server_str = ", ".join([f"{s.get('ip','?')}:{s.get('port','?')}" for s in (servers or [])])
        print(f"  [{uid}] {name:30} → {server_str}")
    return records

# ── Utility ───────────────────────────────────────────────────

def find_server_id(search):
    """Find a server by id prefix, name pattern, or listen port."""
    resp = api("POST", "/api/server/getPage?current=1&limit=200")
    if not resp or not resp.get("success"):
        return None
    for s in resp.get("obj", {}).get("records", []):
        sid = s.get("id", "")
        sname = s.get("serverName", "")
        listen = str(s.get("listen", ""))
        if sid.startswith(search) or search in sname or search == listen:
            return sid
    return None

# ── Main ──────────────────────────────────────────────────────

def main():
    # Check docker & nginxwebui container
    ps = subprocess.run(["docker", "ps", "--format", "{{.Names}}"],
                        capture_output=True, text=True, timeout=5)
    if "nginxwebui" not in ps.stdout:
        log("❌ NginxWebUI container not found or Docker socket unavailable")
        sys.exit(1)

    # Ensure we're authenticated before any operation
    if not ensure_token():
        sys.exit(1)

    import argparse
    parser = argparse.ArgumentParser(description="Manage NginxWebUI via API")
    parser.add_argument("--mode", required=True, choices=[
        "login", "status", "reload", "check",
        "list-servers", "get-server", "add-server", "delete-server",
        "list-locations", "add-location", "delete-location",
        "list-upstreams",
    ])
    parser.add_argument("--id", help="Server/location/upstream ID (or prefix)")
    parser.add_argument("--server-id", help="Parent server ID")
    parser.add_argument("--name", help="Server name (domain names)")
    parser.add_argument("--listen", help="Listen port")
    parser.add_argument("--ssl", action="store_true", help="Enable SSL")
    parser.add_argument("--pem", help="SSL cert PEM path")
    parser.add_argument("--key", help="SSL cert KEY path")
    parser.add_argument("--path", help="Location path (e.g. / or /api/)")
    parser.add_argument("--target", help="Proxy target URL")
    parser.add_argument("--type", type=int, default=0,
                        help="Location type: 0=proxy 1=static 2=upstream 3=blank 4=redirect")
    parser.add_argument("--descr", help="Description")
    parser.add_argument("--search", help="Search keyword for find-server")
    parser.add_argument("--websocket", action="store_true", help="Enable websocket")

    args = parser.parse_args()

    print(f"\n{'='*50}")
    print(f"  NginxWebUI Manager — mode: {args.mode}")
    print(f"{'='*50}\n")

    if args.mode == "login":
        login()
    elif args.mode == "status":
        nginx_status()
    elif args.mode == "reload":
        reload_nginx()
    elif args.mode == "check":
        check_nginx()
    elif args.mode == "list-servers":
        list_servers()
    elif args.mode == "get-server":
        sid = args.id or find_server_id(args.search or "")
        if not sid:
            log("❌ Provide --id or --search to find server")
            sys.exit(1)
        get_server(sid)
    elif args.mode == "add-server":
        if not args.name or not args.listen:
            log("❌ --name (domains) and --listen (port) required")
            sys.exit(1)
        add_server(args.name, args.listen, ssl=args.ssl,
                   pem=args.pem or "", key=args.key or "",
                   descr=args.descr or "")
    elif args.mode == "delete-server":
        if not args.id:
            log("❌ --id required")
            sys.exit(1)
        delete_server(args.id)
    elif args.mode == "list-locations":
        if not args.server_id:
            log("❌ --server-id required")
            sys.exit(1)
        list_locations(args.server_id)
    elif args.mode == "add-location":
        if not args.server_id or not args.path or not args.target:
            log("❌ --server-id, --path, and --target required")
            sys.exit(1)
        add_location(args.server_id, args.path, args.target,
                     type=args.type, descr=args.descr or "",
                     websocket=args.websocket)
    elif args.mode == "delete-location":
        if not args.id:
            log("❌ --id required")
            sys.exit(1)
        delete_location(args.id)
    elif args.mode == "list-upstreams":
        list_upstreams()

if __name__ == "__main__":
    main()
