#!/usr/bin/env python3
"""杰峰连锁门店精准客流部署技能"""

import os, sys, json, time, shutil, argparse, uuid as uuid_mod, base64
from datetime import datetime, timedelta
from typing import Dict, Any
import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from crypto import get_time_millis, generate_signature

JF_ENDPOINT = os.getenv("JF_ENDPOINT", "api-cn.jftechws.com")
JF_BASE_URL = f"https://{JF_ENDPOINT}/gwp/v3"
SESSION_FILE = "session.json"
SESSION_BACKUP = "session.json.bak"
REQUIRED_ENV_VARS = ["JF_UUID", "JF_APP_KEY", "JF_APP_SECRET"]


# ---------------------------------------------------------------------------
# Session Management
# ---------------------------------------------------------------------------

def get_session_path(session_dir: str) -> str:
    """Return the full path to session.json inside session_dir."""
    return os.path.join(session_dir, SESSION_FILE)


def load_session(session_dir: str) -> Dict[str, Any]:
    """Load session from disk. Exits with error if missing or corrupt."""
    path = get_session_path(session_dir)
    if not os.path.exists(path):
        print(f"[error] Session not found: {path}", file=sys.stderr)
        print("Run 'init' first to create a session.", file=sys.stderr)
        sys.exit(1)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as exc:
        print(f"[error] Failed to load session: {exc}", file=sys.stderr)
        sys.exit(1)


def save_session(session_dir: str, session: Dict[str, Any]) -> None:
    """Backup existing session then write the updated one."""
    path = get_session_path(session_dir)
    backup_path = os.path.join(session_dir, SESSION_BACKUP)
    if os.path.exists(path):
        shutil.copy2(path, backup_path)
    session["updatedAt"] = datetime.now().isoformat()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(session, f, indent=2, ensure_ascii=False)


def new_session() -> Dict[str, Any]:
    """Return a blank session dict."""
    now = datetime.now().isoformat()
    return {
        "sessionId": str(uuid_mod.uuid4()),
        "createdAt": now,
        "updatedAt": now,
        "steps": {
            "store":      {"completed": False, "data": None},
            "device":     {"completed": False, "data": None},
            "flowConfig": {"completed": False, "data": None},
        },
    }


def require_step(session: Dict[str, Any], step: str, hint: str = "") -> None:
    """Exit if the given step has not been completed yet."""
    step_info = session.get("steps", {}).get(step)
    if not step_info or not step_info.get("completed"):
        msg = f"[error] Step '{step}' has not been completed yet."
        if hint:
            msg += f" Hint: {hint}"
        print(msg, file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# API Helpers
# ---------------------------------------------------------------------------

def get_headers() -> Dict[str, str]:
    """Generate JF OpenAPI auth headers. Exits if env vars are missing."""
    missing = [v for v in REQUIRED_ENV_VARS if not os.getenv(v)]
    if missing:
        print(f"[error] Missing required env vars: {', '.join(missing)}", file=sys.stderr)
        sys.exit(1)

    jf_uuid     = os.getenv("JF_UUID")
    app_key     = os.getenv("JF_APP_KEY")
    app_secret  = os.getenv("JF_APP_SECRET")
    move_card   = int(os.getenv("JF_MOVE_CARD", "2"))
    time_millis = get_time_millis()
    signature   = generate_signature(jf_uuid, app_key, app_secret, time_millis, move_card)

    return {
        "uuid":          jf_uuid,
        "appKey":        app_key,
        "timeMillis":    time_millis,
        "signature":     signature,
        "X-Request-Id":  str(uuid_mod.uuid4()),
        "Content-Type":  "application/json",
    }


def api_post(path: str, body: Dict[str, Any], retries: int = 1) -> Dict[str, Any]:
    """POST to JF API with retry on network error."""
    url = f"{JF_BASE_URL}{path}"
    headers = get_headers()

    for attempt in range(retries + 1):
        try:
            resp = requests.post(url, json=body, headers=headers, timeout=30)
            result = resp.json()
        except requests.RequestException as exc:
            if attempt < retries:
                print(f"[warn] Network error, retrying ({attempt + 1}/{retries}): {exc}", file=sys.stderr)
                continue
            print(f"[error] Network error after {retries + 1} attempts: {exc}", file=sys.stderr)
            sys.exit(1)

        if result.get("code") != 2000:
            code = result.get("code")
            msg  = result.get("msg", result.get("message", "unknown error"))
            print(f"[error] API error code={code}: {msg}", file=sys.stderr)
            if code in (4007, 28005, 28006, 28007):
                print("[hint] Auth/signature related error. Check JF_UUID, JF_APP_KEY, "
                      "JF_APP_SECRET, JF_MOVE_CARD, and system clock "
                      "(timeMillis is validated in real time and expires quickly).",
                      file=sys.stderr)
            sys.exit(1)

        return result

    # Should not reach here, but guard just in case
    print("[error] Unexpected: all retries exhausted.", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Action: init
# ---------------------------------------------------------------------------

def action_init(args) -> None:
    session_dir = args.session
    os.makedirs(session_dir, exist_ok=True)

    # Warn (not exit) if env vars are missing
    missing = [v for v in REQUIRED_ENV_VARS if not os.getenv(v)]
    if missing:
        print(f"[warn] Env vars not set: {', '.join(missing)}. "
              "API calls will fail until they are configured.", file=sys.stderr)

    session = new_session()
    save_session(session_dir, session)
    print(f"[ok] Session initialized: {session['sessionId']}")
    print(f"     Session dir: {os.path.abspath(session_dir)}")
    print(f"     Next step: create-store")


# ---------------------------------------------------------------------------
# Action: status
# ---------------------------------------------------------------------------

def action_status(args) -> None:
    session = load_session(args.session)
    fmt = getattr(args, "fmt", None) or getattr(args, "format", "table")

    if fmt == "json":
        print(json.dumps(session, indent=2, ensure_ascii=False))
        return

    print(f"Session: {session['sessionId']}")
    print(f"Created: {session['createdAt']}")
    print(f"Updated: {session['updatedAt']}")
    print()

    steps = session.get("steps", {})
    step_order = [
        ("store",      "Store"),
        ("device",     "Device"),
        ("flowConfig", "Flow Config"),
    ]
    for key, label in step_order:
        info = steps.get(key, {})
        done = info.get("completed", False)
        icon = "\u2713" if done else "\u25cb"
        line = f"  {icon} {label}"
        if done and info.get("data"):
            data = info["data"]
            extras = []
            if "id" in data:
                extras.append(f"id={data['id']}")
            if "storeName" in data:
                extras.append(f"name={data['storeName']}")
            if "deviceSN" in data:
                extras.append(f"sn={data['deviceSN']}")
            if extras:
                line += f"  ({', '.join(extras)})"
        print(line)


# ---------------------------------------------------------------------------
# Action: reset
# ---------------------------------------------------------------------------

def action_reset(args) -> None:
    session_dir = args.session
    removed = []
    for name in (SESSION_FILE, SESSION_BACKUP):
        path = os.path.join(session_dir, name)
        if os.path.exists(path):
            os.remove(path)
            removed.append(name)
    if removed:
        print(f"[ok] Removed: {', '.join(removed)}")
    else:
        print("[ok] Nothing to reset (no session files found).")


# ---------------------------------------------------------------------------
# Action: create-store
# ---------------------------------------------------------------------------

def action_create_store(args) -> None:
    session = load_session(args.session)

    body = {"storeName": args.store_name}
    if args.address:
        body["storeAddress"] = args.address
    if args.longitude is not None:
        body["longitude"] = args.longitude
    if args.latitude is not None:
        body["latitude"] = args.latitude

    result = api_post("/rtc/store/create", body)
    data = result.get("data", {})
    model = data.get("model", {}) if isinstance(data, dict) else {}

    store_data = {
        "id":           model.get("id"),
        "nodeId":       model.get("nodeId"),
        "storeName":    args.store_name,
        "storeAddress": args.address,
    }
    session["steps"]["store"] = {"completed": True, "data": store_data}
    save_session(args.session, session)

    print(f"[ok] Store created")
    print(f"     id:     {store_data['id']}")
    print(f"     nodeId: {store_data['nodeId']}")
    print(f"     Next step: add-device")


# ---------------------------------------------------------------------------
# Action: edit-store
# ---------------------------------------------------------------------------

def action_edit_store(args) -> None:
    session = load_session(args.session)
    require_step(session, "store", "Run 'create-store' first.")

    store_data = session["steps"]["store"]["data"]
    body = {"id": store_data["id"], "storeName": args.store_name}
    if args.address:
        body["storeAddress"] = args.address
    if args.longitude is not None:
        body["longitude"] = args.longitude
    if args.latitude is not None:
        body["latitude"] = args.latitude

    result = api_post("/rtc/store/edit", body)
    data = result.get("data", {})

    store_data.update({
        "storeName":    args.store_name,
        "storeAddress": args.address or store_data.get("storeAddress"),
    })
    session["steps"]["store"]["data"] = store_data
    save_session(args.session, session)

    print(f"[ok] Store updated: {store_data['id']}")


# ---------------------------------------------------------------------------
# Action: delete-store
# ---------------------------------------------------------------------------

def action_delete_store(args) -> None:
    session = load_session(args.session)
    require_step(session, "store", "No store to delete.")

    store_id = session["steps"]["store"]["data"]["id"]
    api_post("/rtc/store/delete", {"id": store_id})

    session["steps"]["store"]      = {"completed": False, "data": None}
    session["steps"]["device"]     = {"completed": False, "data": None}
    session["steps"]["flowConfig"] = {"completed": False, "data": None}
    save_session(args.session, session)

    print(f"[ok] Store deleted: {store_id}")


# ---------------------------------------------------------------------------
# Action: bind-device / device-status (optional diagnostics, NOT add-device prerequisites)
# ---------------------------------------------------------------------------

def action_bind_device(args) -> None:
    """Bind a device SN to the current account (optional; official docs do not
    require binding before add-device -- 4116 is caused by an offline device)."""
    result = api_post("/rtc/device/bind", {"sn": args.sn})
    data  = result.get("data", {})
    model = data.get("model", {}) if isinstance(data, dict) else {}
    print(f"[ok] Device bound to account")
    print(f"     sn: {args.sn}")
    if isinstance(model, dict) and model.get("id"):
        print(f"     bind id: {model['id']}")
    print("     Tip: use device-status to confirm the device is online before add-device")


def action_device_status(args) -> None:
    """Query online/registration status for one or more device SNs."""
    sns = [s.strip() for s in args.sn.split(",") if s.strip()]
    token_result = api_post("/rtc/device/token", {"sns": sns})
    token_data = token_result.get("data")
    items = token_data if isinstance(token_data, list) else (
        token_data.get("model") if isinstance(token_data, dict) else [])
    tokens = [it.get("token") for it in items
              if isinstance(it, dict) and it.get("token")]
    if not tokens:
        print("[error] No device tokens returned; device may be offline or not "
              "registered on JF cloud.", file=sys.stderr)
        sys.exit(1)

    status_result = api_post("/rtc/device/status", {"deviceTokenList": tokens})
    status_data = status_result.get("data")
    statuses = status_data if isinstance(status_data, list) else []

    offline = []
    for entry in statuses:
        sn     = entry.get("uuid", "?")
        status = entry.get("status", "unknown")
        mark   = "online" if status not in ("notfound", "offline") else status
        print(f"     {sn}: {mark}")
        if status == "notfound":
            offline.append(sn)
    if offline:
        print("[warn] Device(s) not registered on JF cloud (offline). "
              "Power on and connect to network, then retry. add-device will "
              "return 4116 until the device is online.", file=sys.stderr)
        sys.exit(1)
    print("[ok] All queried device(s) online")


# ---------------------------------------------------------------------------
# Action: snapshot (livestream frame grab)
# HA-5P-GM does NOT support OPSNAP cloud capture (Ret=101), so this is the
# ONE AND ONLY snapshot path: token -> login -> livestream URL -> PyAV frame.
# ---------------------------------------------------------------------------

def action_snapshot(args) -> None:
    session = load_session(args.session)
    require_step(session, "device", "Run 'add-device' first.")
    device_sn = session["steps"]["device"]["data"]["deviceSN"]

    # 1. fresh device token (valid 24h; always re-fetch to avoid expiry)
    token_result = api_post("/rtc/device/token", {"sns": [device_sn]})
    token_data = token_result.get("data")
    items = token_data if isinstance(token_data, list) else (
        token_data.get("model") if isinstance(token_data, dict) else [])
    token = next((it.get("token") for it in items
                  if isinstance(it, dict) and it.get("sn") == device_sn), None)
    if not token:
        print("[error] No device token returned; device offline or not bound "
              "to this account.", file=sys.stderr)
        sys.exit(1)

    # 2. login device session (KeepaliveTime keeps it alive during decode)
    api_post(f"/rtc/device/login/{token}", {
        "UserName": args.username, "PassWord": args.password,
        "KeepaliveTime": 60,
    })

    # 3. livestream URL (FLV); username/password required in body
    stream = api_post(f"/rtc/device/livestream/{token}", {
        "channel": args.channel, "stream": args.stream, "protocol": "flv",
        "username": args.username, "password": args.password,
    })
    data = stream.get("data") or {}
    url = data.get("url") or data.get("URL")
    if not url:
        print("[error] No livestream url in response.", file=sys.stderr)
        sys.exit(1)

    # 4. decode with PyAV and save a stable (non-first) frame
    try:
        import av
    except ImportError:
        print("[error] PyAV not installed. Run: pip install av", file=sys.stderr)
        sys.exit(1)

    container = av.open(url)
    frame_out = None
    for i, frame in enumerate(container.decode(video=0)):
        if i >= args.frames:
            frame_out = frame
            break
    container.close()
    if frame_out is None:
        print("[error] No video frames decoded from livestream.", file=sys.stderr)
        sys.exit(1)

    out = args.output or os.path.join(args.session, "snapshot.jpg")
    img = frame_out.to_image()
    img.save(out)
    print(f"[ok] Snapshot saved: {os.path.abspath(out)} ({img.size[0]}x{img.size[1]})")
    print("     Next step: generate-config-page --snapshot <this file>")


# ---------------------------------------------------------------------------
# Action: add-device
# ---------------------------------------------------------------------------

def action_add_device(args) -> None:
    session = load_session(args.session)
    require_step(session, "store", "Run 'create-store' first.")

    node_id = session["steps"]["store"]["data"]["nodeId"]

    body = {
        "nodeId":             node_id,
        "deviceNetworkType":  args.network_type,
        "sn":                 args.sn,
        "deviceUsername":     args.device_username or "admin",
    }
    if args.device_name:
        body["deviceName"]     = args.device_name
    if args.device_password:
        body["devicePassword"] = args.device_password

    result = api_post("/rtc/device/addJfIpc", body)
    data = result.get("data", {})
    model = data.get("model", {}) if isinstance(data, dict) else {}

    device_data = {
        "id":           model.get("id"),
        "name":         model.get("name", args.device_name),
        "deviceSN":     model.get("deviceSN", args.sn),
        "status":       model.get("status"),
        "accessStatus": model.get("accessStatus"),
    }
    session["steps"]["device"] = {"completed": True, "data": device_data}
    save_session(args.session, session)

    print(f"[ok] Device added")
    print(f"     id:   {device_data['id']}")
    print(f"     sn:   {device_data['deviceSN']}")
    print(f"     Next step: config-flow")


# ---------------------------------------------------------------------------
# Action: delete-device
# ---------------------------------------------------------------------------

def action_delete_device(args) -> None:
    session = load_session(args.session)
    require_step(session, "device", "No device to delete.")

    device_id = session["steps"]["device"]["data"]["id"]
    api_post("/rtc/device/delete", {"id": device_id})

    session["steps"]["device"]     = {"completed": False, "data": None}
    session["steps"]["flowConfig"] = {"completed": False, "data": None}
    save_session(args.session, session)

    print(f"[ok] Device deleted: {device_id}")


# ---------------------------------------------------------------------------
# Action: config-flow
# ---------------------------------------------------------------------------

def action_config_flow(args) -> None:
    session = load_session(args.session)
    require_step(session, "device", "Run 'add-device' first.")

    device_id = session["steps"]["device"]["data"]["id"]

    if args.from_file:
        # Build body from JSON file
        if not os.path.exists(args.from_file):
            print(f"[error] File not found: {args.from_file}", file=sys.stderr)
            sys.exit(1)
        with open(args.from_file, "r", encoding="utf-8") as f:
            file_data = json.load(f)
        body = {"id": device_id}
        # Merge file contents into body, converting all values to strings
        for key, value in file_data.items():
            body[key] = str(value) if not isinstance(value, (dict, list)) else value
    else:
        # Build body from CLI args
        body = {"id": device_id}
        if args.flow_type is not None:
            body["flowType"] = str(args.flow_type)
        if args.open_status is not None:
            body["openStatus"] = str(args.open_status)
        if args.areas is not None:
            body["includeAreas"] = args.areas
        if args.osd is not None:
            body["showOsdStatus"] = str(args.osd)
        if args.filter_delivery is not None:
            body["deliveryDriversStatus"] = str(args.filter_delivery)
        if args.task_time is not None:
            body["taskTime"] = args.task_time

    # Real API validates switch fields as int (doc says string, but sending
    # strings returns 4000 "xxx is illegal"). includeAreas/taskTime stay JSON strings.
    for key in ("flowType", "openStatus", "showOsdStatus", "deliveryDriversStatus"):
        if body.get(key) is not None:
            body[key] = int(body[key])

    result = api_post("/rtc/device/aiCrowdFlowConfig", body)

    flow_data = {
        "configuredAt": datetime.now().isoformat(),
        "params":       body,
    }
    session["steps"]["flowConfig"] = {"completed": True, "data": flow_data}
    save_session(args.session, session)

    print(f"[ok] Flow config applied to device {device_id}")
    print(f"     Next step: flow-stats / flow-report")


# ---------------------------------------------------------------------------
# Action: flow-stats
# ---------------------------------------------------------------------------

FLOW_STATS_LABELS = [
    ("sumFlowCount",                       "\u603b\u5ba2\u6d41"),
    ("sumInboundCount",                    "\u8fdb\u5e97\u5ba2\u6d41"),
    ("sumOutboundCount",                   "\u51fa\u5e97\u5ba2\u6d41"),
    ("sumPassCount",                       "\u8fc7\u5e97\u5ba2\u6d41"),
    ("inboundRate",                        "\u8fdb\u5e97\u7387(%)"),
    ("sumDedInboundCount",                 "\u8fdb\u5e97\u53bb\u91cd\u6570"),
    ("sumDedOutboundCount",                "\u51fa\u5e97\u53bb\u91cd\u6570"),
    ("sumDedPassCount",                    "\u8fc7\u5e97\u53bb\u91cd\u6570"),
    ("sumRemoveDuplicateFlowCount",        "\u53bb\u91cd\u603b\u5ba2\u6d41"),
    ("sumRemoveDuplicateInboundCount",     "\u53bb\u91cd\u8fdb\u5e97\u5ba2\u6d41"),
    ("sumRemoveDuplicateOutboundCount",    "\u53bb\u91cd\u51fa\u5e97\u5ba2\u6d41"),
    ("sumRemoveDuplicatePassCount",        "\u53bb\u91cd\u8fc7\u5e97\u5ba2\u6d41"),
    ("sumSingleBatchCount",                "\u5355\u4eba\u6279\u6b21\u6570\u91cf"),
    ("sumDoubleBatchCount",                "\u53cc\u4eba\u6279\u6b21\u6570\u91cf"),
    ("sumThreeBatchCount",                 "\u4e09\u4eba\u6279\u6b21\u6570\u91cf"),
    ("sumManyBatchCount",                  "\u591a\u4eba\u6279\u6b21\u6570\u91cf"),
    ("sumChildrenCount",                   "\u5b69\u7ae5\u6570"),
    ("sumYoungCount",                      "\u9752\u5e74\u6570"),
    ("sumMiddleCount",                     "\u4e2d\u5e74\u6570"),
    ("sumOldCount",                        "\u8001\u5e74\u6570"),
    ("sumManCount",                        "\u7537\u6570\u91cf"),
    ("sumWomanCount",                      "\u5973\u6570\u91cf"),
    ("sumAgeUnknownCount",                 "\u5e74\u9f84\u672a\u77e5\u6570\u91cf"),
    ("sumGenderUnknownCount",              "\u6027\u522b\u672a\u77e5\u6570\u91cf"),
]


def action_flow_stats(args) -> None:
    body = {"startTime": args.start, "endTime": args.end}

    store_id = None
    if args.store_id:
        store_id = args.store_id
    elif not args.all_stores:
        # Fall back to the store id recorded in the session, if any
        path = get_session_path(args.session)
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    session = json.load(f)
                step = session.get("steps", {}).get("store", {})
                if step.get("completed") and step.get("data"):
                    store_id = step["data"].get("id")
            except (json.JSONDecodeError, IOError):
                pass
        if not store_id:
            print("[info] No store id available; querying all stores.", file=sys.stderr)

    if store_id:
        body["storeId"] = str(store_id)
    if args.device_sn:
        body["deviceSn"] = args.device_sn

    result = api_post("/rtc/store/flowStatistics", body)
    data = result.get("data", {})
    model = data.get("model", {}) if isinstance(data, dict) else {}

    fmt = getattr(args, "fmt", None) or getattr(args, "format", "table")
    if fmt == "json":
        print(json.dumps(model, indent=2, ensure_ascii=False))
        return

    scope = f"store={store_id}" if store_id else "all stores"
    if args.device_sn:
        scope += f", deviceSn={args.device_sn}"
    print(f"[ok] Flow statistics ({scope})")
    print(f"     Range: {args.start} ~ {args.end}")
    for key, label in FLOW_STATS_LABELS:
        if key in model:
            print(f"     {label}: {model[key]}")


# ---------------------------------------------------------------------------
# Action: flow-report
# ---------------------------------------------------------------------------

MAX_REPORT_DAYS = 62

# Fields carried into the per-day trend array
DAILY_KEYS = [
    "sumFlowCount", "sumInboundCount", "sumOutboundCount", "sumPassCount",
    "inboundRate", "sumDedInboundCount", "sumRemoveDuplicateInboundCount",
]


def _to_num(value, default=0):
    """Coerce an API field (may be str/int/float/None) to a number."""
    if value is None:
        return default
    try:
        num = float(value)
    except (TypeError, ValueError):
        return default
    return int(num) if num.is_integer() else num


def _resolve_store_id(args) -> Any:
    """Resolve store id: --store-id > session > None (all stores)."""
    if getattr(args, "store_id", None):
        return args.store_id
    if getattr(args, "all_stores", False):
        return None
    path = get_session_path(args.session)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                session = json.load(f)
            step = session.get("steps", {}).get("store", {})
            if step.get("completed") and step.get("data"):
                return step["data"].get("id")
        except (json.JSONDecodeError, IOError):
            pass
    return None


def _session_store_name(args) -> Any:
    path = get_session_path(args.session)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                session = json.load(f)
            step = session.get("steps", {}).get("store", {})
            if step.get("completed") and step.get("data"):
                return step["data"].get("storeName")
        except (json.JSONDecodeError, IOError):
            pass
    return None


def _query_flow_stats(start: str, end: str, store_id=None, device_sn=None) -> Dict[str, Any]:
    """Single flowStatistics call; returns the model dict."""
    body = {"startTime": start, "endTime": end}
    if store_id:
        body["storeId"] = str(store_id)
    if device_sn:
        body["deviceSn"] = device_sn
    result = api_post("/rtc/store/flowStatistics", body)
    data = result.get("data", {})
    model = data.get("model", {}) if isinstance(data, dict) else {}
    return model if isinstance(model, dict) else {}


def _normalize_rate(model: Dict[str, Any]) -> float:
    """Return inbound rate in percent; fall back to computing from counts."""
    rate = _to_num(model.get("inboundRate"), -1)
    if rate < 0:
        total = _to_num(model.get("sumFlowCount"))
        inbound = _to_num(model.get("sumInboundCount"))
        rate = round(inbound / total * 100, 2) if total else 0
    return round(rate, 2)


def action_flow_report(args) -> None:
    store_id = _resolve_store_id(args)

    # Parse range and build the list of days
    try:
        start_dt = datetime.strptime(args.start, "%Y-%m-%d %H:%M:%S")
        end_dt   = datetime.strptime(args.end,   "%Y-%m-%d %H:%M:%S")
    except ValueError:
        print("[error] Invalid time format, expected 'yyyy-MM-dd HH:mm:ss'.", file=sys.stderr)
        sys.exit(1)
    if end_dt < start_dt:
        print("[error] --end must not be earlier than --start.", file=sys.stderr)
        sys.exit(1)

    days = []
    cur = datetime(start_dt.year, start_dt.month, start_dt.day)
    last = datetime(end_dt.year, end_dt.month, end_dt.day)
    while cur <= last:
        days.append(cur)
        cur += timedelta(days=1)
    if len(days) > MAX_REPORT_DAYS:
        print(f"[error] Range spans {len(days)} days; the report supports at most "
              f"{MAX_REPORT_DAYS} days.", file=sys.stderr)
        sys.exit(1)

    scope = f"store={store_id}" if store_id else "all stores"
    if args.device_sn:
        scope += f", deviceSn={args.device_sn}"

    # 1) Overview for the whole range
    print(f"[info] Querying overview ({scope}, {args.start} ~ {args.end}) ...")
    raw_overview = _query_flow_stats(args.start, args.end, store_id, args.device_sn)
    overview = {key: _to_num(raw_overview.get(key)) for key, _ in FLOW_STATS_LABELS}
    overview["inboundRate"] = _normalize_rate(raw_overview)

    # 2) Per-day statistics for the trend chart
    daily = []
    for idx, day in enumerate(days):
        d_start = day.strftime("%Y-%m-%d 00:00:00")
        d_end   = day.strftime("%Y-%m-%d 23:59:59")
        print(f"[info] Querying day {idx + 1}/{len(days)}: {day.strftime('%Y-%m-%d')}")
        model = _query_flow_stats(d_start, d_end, store_id, args.device_sn)
        entry = {"date": day.strftime("%Y-%m-%d")}
        for key in DAILY_KEYS:
            entry[key] = _to_num(model.get(key))
        entry["inboundRate"] = _normalize_rate(model)
        daily.append(entry)
        if idx < len(days) - 1:
            time.sleep(0.5)  # be gentle with rate limits

    store_name = args.title or _session_store_name(args) or (
        f"store {store_id}" if store_id else "all stores")

    report = {
        "meta": {
            "title":      store_name,
            "storeId":    store_id,
            "deviceSn":   args.device_sn,
            "rangeStart": args.start,
            "rangeEnd":   args.end,
            "generatedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "days":       len(days),
        },
        "overview": overview,
        "daily":    daily,
    }

    # Load template and inject data
    script_dir    = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.normpath(
        os.path.join(script_dir, "..", "assets", "flow_report_template.html"))
    if not os.path.exists(template_path):
        print(f"[error] Template not found: {template_path}", file=sys.stderr)
        sys.exit(1)
    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()

    payload = json.dumps(report, ensure_ascii=False).replace("</", "<\\/")
    marker = "window.__REPORT__ = null;"
    if marker not in html:
        print("[error] Template is missing the data marker.", file=sys.stderr)
        sys.exit(1)
    html = html.replace(marker, f"window.__REPORT__ = {payload};")

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[ok] Flow report generated: {os.path.abspath(args.output)}")
    print(f"     Scope: {scope}")
    print(f"     Range: {args.start} ~ {args.end} ({len(days)} day(s))")
    print(f"     Overview: total={_to_num(overview.get('sumFlowCount'))}, "
          f"in={_to_num(overview.get('sumInboundCount'))}, "
          f"rate={overview.get('inboundRate')}%")


# ---------------------------------------------------------------------------
# Action: generate-config-page
# ---------------------------------------------------------------------------

def action_generate_config_page(args) -> None:
    session = load_session(args.session)
    require_step(session, "device", "Run 'add-device' first.")

    device_data = session["steps"]["device"]["data"]
    device_id   = device_data.get("id", "")
    device_sn   = device_data.get("deviceSN", "")

    # Read snapshot image and encode as base64
    snapshot_path = args.snapshot
    if not os.path.exists(snapshot_path):
        print(f"[error] Snapshot file not found: {snapshot_path}", file=sys.stderr)
        sys.exit(1)

    with open(snapshot_path, "rb") as f:
        snapshot_b64 = base64.b64encode(f.read()).decode("ascii")

    # Determine file extension for data-URI mime type
    ext = os.path.splitext(snapshot_path)[1].lower()
    mime_map = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                ".gif": "image/gif", ".bmp": "image/bmp", ".webp": "image/webp"}
    mime = mime_map.get(ext, "image/png")

    # Read HTML template
    script_dir   = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(script_dir, "..", "assets", "config_tool.html")
    template_path = os.path.normpath(template_path)
    if not os.path.exists(template_path):
        print(f"[error] Template not found: {template_path}", file=sys.stderr)
        sys.exit(1)

    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Inject data before </head>
    inject_script = (
        f"<script>\n"
        f"  window.__SNAPSHOT_BASE64__ = \"data:{mime};base64,{snapshot_b64}\";\n"
        f"  window.__DEVICE_ID__ = {json.dumps(device_id)};\n"
        f"  window.__DEVICE_SN__ = {json.dumps(device_sn)};\n"
        f"</script>\n"
    )
    html = html.replace("</head>", inject_script + "</head>")

    # Write output
    output_path = args.output
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[ok] Config page generated: {os.path.abspath(output_path)}")
    print(f"     Device: {device_id} (SN: {device_sn})")


# ---------------------------------------------------------------------------
# Main / argparse
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="\u6770\u5cf0\u8fde\u9501\u95e8\u5e97\u7cbe\u51c6\u5ba2\u6d41\u90e8\u7f72\u6280\u80fd (JF Store Traffic Deployment)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--session", default="./session",
                        help="Session directory (default: ./session)")
    parser.add_argument("--format", choices=["table", "json"], default="table",
                        help="Output format (default: table)")

    sub = parser.add_subparsers(dest="action", help="Available actions")

    # --- init ---
    sub.add_parser("init", help="Initialize a new deployment session")

    # --- status ---
    p_st = sub.add_parser("status", help="Show current session status")
    p_st.add_argument("--format", dest="fmt", choices=["table", "json"], default=None,
                       help="Output format (overrides global --format)")

    # --- reset ---
    sub.add_parser("reset", help="Reset (delete) the current session")

    # --- create-store ---
    p_cs = sub.add_parser("create-store", help="Create a new store")
    p_cs.add_argument("--store-name", required=True, help="Store name")
    p_cs.add_argument("--address",    default=None,  help="Store address")
    p_cs.add_argument("--longitude",  type=float, default=None, help="Longitude")
    p_cs.add_argument("--latitude",   type=float, default=None, help="Latitude")

    # --- edit-store ---
    p_es = sub.add_parser("edit-store", help="Edit an existing store")
    p_es.add_argument("--store-name", required=True, help="New store name")
    p_es.add_argument("--address",    default=None,  help="New store address")
    p_es.add_argument("--longitude",  type=float, default=None, help="New longitude")
    p_es.add_argument("--latitude",   type=float, default=None, help="New latitude")

    # --- delete-store ---
    sub.add_parser("delete-store", help="Delete the current store")

    # --- bind-device / device-status (optional diagnostics) ---
    p_bd = sub.add_parser("bind-device",
                          help="Bind a device SN to the account (optional; not required before add-device)")
    p_bd.add_argument("--sn", required=True, help="Device serial number")

    p_ds = sub.add_parser("device-status",
                          help="Query device online/registration status")
    p_ds.add_argument("--sn", required=True,
                      help="Device serial number(s), comma-separated for batch")

    # --- snapshot (livestream frame grab; OPSNAP unsupported on HA-5P-GM) ---
    p_snap = sub.add_parser("snapshot",
                            help="Grab a live frame via livestream (HA-5P-GM has no OPSNAP)")
    p_snap.add_argument("--output",   default=None,
                        help="Output image path (default: <session>/snapshot.jpg)")
    p_snap.add_argument("--username", default="admin",
                        help="Device login username (default: admin)")
    p_snap.add_argument("--password", default="",
                        help="Device login password (default: empty factory)")
    p_snap.add_argument("--channel",  default="0", help="Channel (default: 0)")
    p_snap.add_argument("--stream",   default="0",
                        help="Stream: 0=main, 1=sub (default: 0)")
    p_snap.add_argument("--frames",   type=int, default=15,
                        help="Decode N frames and save the Nth (default: 15)")

    # --- add-device ---
    p_ad = sub.add_parser("add-device", help="Add a device to the store")
    p_ad.add_argument("--sn",              required=True, help="Device serial number")
    p_ad.add_argument("--network-type",    required=True, type=int, choices=[0, 1],
                       help="Device network type (0=already configured, 1=not configured)")
    p_ad.add_argument("--device-name",     default=None, help="Device display name")
    p_ad.add_argument("--device-username", default=None, help="Device login username")
    p_ad.add_argument("--device-password", default=None, help="Device login password")

    # --- delete-device ---
    sub.add_parser("delete-device", help="Delete the current device")

    # --- config-flow ---
    p_cf = sub.add_parser("config-flow", help="Configure AI crowd flow on the device")
    p_cf.add_argument("--from-file",       default=None,
                       help="Load config from a JSON file instead of CLI args")
    p_cf.add_argument("--flow-type",       type=int, choices=[0, 1, 2], default=None,
                       help="Flow type (0/1/2)")
    p_cf.add_argument("--open-status",     type=int, choices=[0, 1], default=None,
                       help="Open status (0=off, 1=on)")
    p_cf.add_argument("--areas",           default=None,
                       help="Areas JSON string")
    p_cf.add_argument("--osd",             type=int, choices=[0, 1], default=None,
                       help="OSD overlay (0=off, 1=on)")
    p_cf.add_argument("--filter-delivery", type=int, choices=[0, 1], default=None,
                       help="Filter delivery (0=off, 1=on)")
    p_cf.add_argument("--task-time",       default=None,
                       help="Task time configuration")

    # --- flow-report ---
    p_fr = sub.add_parser("flow-report",
                          help="Query flow statistics and generate an HTML report")
    _today = datetime.now().date()
    _week_ago = _today - timedelta(days=6)
    p_fr.add_argument("--start", default=f"{_week_ago} 00:00:00",
                      help="Start time, yyyy-MM-dd HH:mm:ss (default: 7 days ago)")
    p_fr.add_argument("--end", default=f"{_today} 23:59:59",
                      help="End time, yyyy-MM-dd HH:mm:ss (default: today)")
    p_fr.add_argument("--store-id", default=None,
                      help="Store id (default: store id from session; "
                           "falls back to all stores)")
    p_fr.add_argument("--device-sn", default=None,
                      help="Filter by device serial number (default: all devices)")
    p_fr.add_argument("--all-stores", action="store_true",
                      help="Query all stores, ignoring the session store id")
    p_fr.add_argument("--title", default=None,
                      help="Report title (default: store name from session)")
    p_fr.add_argument("--output", default="./flow_report.html",
                      help="Output HTML file (default: ./flow_report.html)")

    # --- flow-stats ---
    p_fs = sub.add_parser("flow-stats",
                          help="Query store foot-traffic aggregated statistics")
    _today = datetime.now().strftime("%Y-%m-%d")
    p_fs.add_argument("--start", default=f"{_today} 00:00:00",
                      help="Start time, yyyy-MM-dd HH:mm:ss (default: today 00:00:00)")
    p_fs.add_argument("--end", default=f"{_today} 23:59:59",
                      help="End time, yyyy-MM-dd HH:mm:ss (default: today 23:59:59)")
    p_fs.add_argument("--store-id", default=None,
                      help="Store id (default: store id from session; "
                           "falls back to all stores)")
    p_fs.add_argument("--device-sn", default=None,
                      help="Filter by device serial number (default: all devices)")
    p_fs.add_argument("--all-stores", action="store_true",
                      help="Query all stores, ignoring the session store id")
    p_fs.add_argument("--format", dest="fmt", choices=["table", "json"], default=None,
                      help="Output format (overrides global --format)")

    # --- generate-config-page ---
    p_gcp = sub.add_parser("generate-config-page",
                           help="Generate an interactive HTML config tool page")
    p_gcp.add_argument("--snapshot", required=True,
                        help="Path to snapshot image file")
    p_gcp.add_argument("--output",   default="./config_tool.html",
                        help="Output HTML file (default: ./config_tool.html)")

    args = parser.parse_args()

    if not args.action:
        parser.print_help()
        sys.exit(1)

    # Dispatch table
    actions = {
        "init":               action_init,
        "status":             action_status,
        "reset":              action_reset,
        "create-store":       action_create_store,
        "edit-store":         action_edit_store,
        "delete-store":       action_delete_store,
        "bind-device":        action_bind_device,
        "device-status":      action_device_status,
        "snapshot":           action_snapshot,
        "add-device":         action_add_device,
        "delete-device":      action_delete_device,
        "config-flow":        action_config_flow,
        "flow-stats":         action_flow_stats,
        "flow-report":        action_flow_report,
        "generate-config-page": action_generate_config_page,
    }

    handler = actions.get(args.action)
    if handler:
        handler(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
