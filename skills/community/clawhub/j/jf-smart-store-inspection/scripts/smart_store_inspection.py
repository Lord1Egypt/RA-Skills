#!/usr/bin/env python3
"""杰峰智慧巡店部署与AI巡检运营技能

覆盖:
- 门店管理: create/edit/delete
- 设备接入: add-device/delete-device (addJfIpc)
- AI巡检算法目录: list-algorithms
- AI巡检计划: create-plan/edit-plan/list-plans/plan-detail/start-plan/stop-plan/delete-plan
- AI巡检记录: list-records + patrol-report (HTML 抓拍图墙+统计)
- 交互配置: snapshot + generate-config-page (includeAreas 画框)
- 会话管理: init/status/reset
"""

import os, sys, json, time, shutil, argparse, uuid as uuid_mod, base64
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
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
    return os.path.join(session_dir, SESSION_FILE)


def load_session(session_dir: str) -> Dict[str, Any]:
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
    path = get_session_path(session_dir)
    backup_path = os.path.join(session_dir, SESSION_BACKUP)
    if os.path.exists(path):
        shutil.copy2(path, backup_path)
    session["updatedAt"] = datetime.now().isoformat()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(session, f, indent=2, ensure_ascii=False)


def new_session() -> Dict[str, Any]:
    now = datetime.now().isoformat()
    return {
        "sessionId": str(uuid_mod.uuid4()),
        "createdAt": now,
        "updatedAt": now,
        "steps": {
            "store":    {"completed": False, "data": None},
            "device":   {"completed": False, "data": None},
            "patrolPlan": {"completed": False, "data": None},
        },
    }


def require_step(session: Dict[str, Any], step: str, hint: str = "") -> None:
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
        "X-Request-Id":  uuid_mod.uuid4().hex,
        "Content-Type":  "application/json",
    }


def _handle_error(result: Dict[str, Any]) -> None:
    code = result.get("code")
    msg  = result.get("msg", result.get("message", "unknown error"))
    print(f"[error] API error code={code}: {msg}", file=sys.stderr)
    if code in (4007, 28005, 28006, 28007):
        print("[hint] Auth/signature related error. Check JF_UUID, JF_APP_KEY, "
              "JF_APP_SECRET, JF_MOVE_CARD, and system clock.", file=sys.stderr)
    elif code == 4000:
        print("[hint] Parameter validation failed. Verify Body fields, types "
              "(int vs string) and enum values.", file=sys.stderr)
    elif code == 4116:
        print("[hint] Not found. For add-device: device may be offline OR "
              "the appKey has no smart-store-inspection authorization.", file=sys.stderr)
    sys.exit(1)


def api_post(path: str, body: Dict[str, Any], retries: int = 1) -> Dict[str, Any]:
    url = f"{JF_BASE_URL}{path}"
    headers = get_headers()

    for attempt in range(retries + 1):
        try:
            resp = requests.post(url, json=body, headers=headers, timeout=30)
            result = resp.json()
        except requests.RequestException as exc:
            if attempt < retries:
                print(f"[warn] Network error, retrying ({attempt + 1}/{retries}): {exc}", file=sys.stderr)
                time.sleep(1)
                continue
            print(f"[error] Network error after {retries + 1} attempts: {exc}", file=sys.stderr)
            sys.exit(1)

        if result.get("code") != 2000:
            _handle_error(result)
        return result

    print("[error] Unexpected: all retries exhausted.", file=sys.stderr)
    sys.exit(1)


def api_get(path: str, retries: int = 1) -> Dict[str, Any]:
    """GET request for endpoints like aiPatrolDetail/{batchNumber}, aiPatrolDelete/{batchNumber}."""
    url = f"{JF_BASE_URL}{path}"
    headers = get_headers()

    for attempt in range(retries + 1):
        try:
            resp = requests.get(url, headers=headers, timeout=30)
            result = resp.json()
        except requests.RequestException as exc:
            if attempt < retries:
                print(f"[warn] Network error, retrying ({attempt + 1}/{retries}): {exc}", file=sys.stderr)
                time.sleep(1)
                continue
            print(f"[error] Network error after {retries + 1} attempts: {exc}", file=sys.stderr)
            sys.exit(1)

        if result.get("code") != 2000:
            _handle_error(result)
        return result

    print("[error] Unexpected: all retries exhausted.", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Action: init / status / reset
# ---------------------------------------------------------------------------

def action_init(args) -> None:
    session_dir = args.session
    os.makedirs(session_dir, exist_ok=True)

    missing = [v for v in REQUIRED_ENV_VARS if not os.getenv(v)]
    if missing:
        print(f"[warn] Env vars not set: {', '.join(missing)}. "
              "API calls will fail until they are configured.", file=sys.stderr)

    session = new_session()
    save_session(session_dir, session)
    print(f"[ok] Session initialized: {session['sessionId']}")
    print(f"     Session dir: {os.path.abspath(session_dir)}")
    print(f"     Next step: create-store")


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
        ("patrolPlan", "AI Patrol Plan"),
    ]
    for key, label in step_order:
        info = steps.get(key, {})
        done = info.get("completed", False)
        icon = "\u2713" if done else "\u25cb"
        line = f"  {icon} {label}"
        if done and info.get("data"):
            data = info["data"]
            extras = []
            for k in ("id", "storeName", "deviceSN", "patrolName", "batchNumber"):
                if k in data and data[k] is not None:
                    extras.append(f"{k}={data[k]}")
            if extras:
                line += f"  ({', '.join(extras)})"
        print(line)


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
# Action: store CRUD
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

    api_post("/rtc/store/edit", body)

    store_data.update({
        "storeName":    args.store_name,
        "storeAddress": args.address or store_data.get("storeAddress"),
    })
    session["steps"]["store"]["data"] = store_data
    save_session(args.session, session)

    print(f"[ok] Store updated: {store_data['id']}")


def action_delete_store(args) -> None:
    session = load_session(args.session)
    require_step(session, "store", "No store to delete.")

    store_id = session["steps"]["store"]["data"]["id"]
    api_post("/rtc/store/delete", {"id": store_id})

    session["steps"]["store"]      = {"completed": False, "data": None}
    session["steps"]["device"]     = {"completed": False, "data": None}
    session["steps"]["patrolPlan"] = {"completed": False, "data": None}
    save_session(args.session, session)

    print(f"[ok] Store deleted: {store_id}")


# ---------------------------------------------------------------------------
# Action: device CRUD
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
    print(f"     Next step: list-algorithms -> create-plan")


def action_delete_device(args) -> None:
    session = load_session(args.session)
    require_step(session, "device", "No device to delete.")

    device_id = session["steps"]["device"]["data"]["id"]
    api_post("/rtc/device/delete", {"id": device_id})

    session["steps"]["device"]     = {"completed": False, "data": None}
    session["steps"]["patrolPlan"] = {"completed": False, "data": None}
    save_session(args.session, session)

    print(f"[ok] Device deleted: {device_id}")


# ---------------------------------------------------------------------------
# Action: list-algorithms (aiPatrolAlgorithmPageQuery)
# ---------------------------------------------------------------------------

def action_list_algorithms(args) -> None:
    body = {
        "pageSize": args.page_size,
        "pageNo":   args.page_no,
        "param":    {},
    }
    if args.name:
        body["param"]["algorithmName"] = args.name

    result = api_post("/rtc/device/aiPatrolAlgorithmPageQuery", body)
    model = result.get("data", {}).get("model", {}) or {}
    datas = model.get("datas") or []

    fmt = getattr(args, "fmt", None) or getattr(args, "format", "table")
    if fmt == "json":
        print(json.dumps(model, indent=2, ensure_ascii=False))
        return

    print(f"[ok] Algorithms (page {model.get('pageNo')}/{model.get('totalPage')}, "
          f"total={model.get('totalCount')})")
    if not datas:
        print("     (no algorithms)")
        return
    for a in datas:
        flow_map = {0: "进过店", 1: "进店", 2: "过店", None: "-"}
        flow = flow_map.get(a.get("flowType"), a.get("flowType"))
        print(f"  - id={a.get('algorithmId')} | {a.get('algorithmName')} "
              f"| step={a.get('step')} | threshold={a.get('threshold')} "
              f"| flowType={flow} | durationTime={a.get('durationTime')}")


# ---------------------------------------------------------------------------
# Action: create-plan / edit-plan (aiPatrolAddOrEdit)
# ---------------------------------------------------------------------------

def _build_plan_body(args, existing: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Merge CLI args (and optional --from-file) into aiPatrolAddOrEdit body."""
    body: Dict[str, Any] = {}
    if existing:
        body.update(existing)

    if args.from_file:
        if not os.path.exists(args.from_file):
            print(f"[error] File not found: {args.from_file}", file=sys.stderr)
            sys.exit(1)
        with open(args.from_file, "r", encoding="utf-8") as f:
            file_data = json.load(f)
        body.update(file_data)

    # CLI overrides
    if args.plan_name is not None:      body["patrolName"]  = args.plan_name
    if args.time_type is not None:      body["timeType"]    = args.time_type
    if args.time_cycle is not None:     body["timeCycle"]   = args.time_cycle
    if args.detail_time is not None:    body["detailTime"]  = args.detail_time
    if args.patrol_range is not None:   body["patrolRange"] = args.patrol_range
    if args.algorithm_id is not None:   body["algorithmId"] = args.algorithm_id
    if args.threshold is not None:      body["threshold"]   = args.threshold
    if args.step is not None:           body["step"]        = args.step
    if args.time_interval is not None:  body["timeInterval"] = args.time_interval
    if args.include_areas is not None:  body["includeAreas"] = args.include_areas
    if args.duration_time is not None:  body["durationTime"] = args.duration_time
    if args.mosaic is not None:         body["mosaic"]      = args.mosaic
    if args.special_param is not None:  body["specialParam"] = args.special_param
    if getattr(args, "id", None) is not None:  # id 仅 edit-plan 注册，create-plan 无此属性
        body["id"] = args.id

    # Type coercions (int fields the API validates strictly)
    for key in ("timeType", "step", "timeInterval", "durationTime"):
        if body.get(key) is not None and not isinstance(body[key], int):
            try:
                body[key] = int(body[key])
            except (TypeError, ValueError):
                pass

    # Required fields check for create
    if not existing:
        required = ["patrolName", "timeType", "timeCycle", "detailTime",
                    "patrolRange", "algorithmId", "threshold"]
        missing = [k for k in required if body.get(k) in (None, "")]
        if missing:
            print(f"[error] Missing required fields: {', '.join(missing)}", file=sys.stderr)
            print("[hint] Provide via CLI args or --from-file JSON.", file=sys.stderr)
            sys.exit(1)

    return body


def action_create_plan(args) -> None:
    session = load_session(args.session)
    body = _build_plan_body(args)

    # Default patrolRange to session device id if not provided
    if not body.get("patrolRange"):
        dev = session.get("steps", {}).get("device", {})
        if dev.get("completed") and dev.get("data", {}).get("id"):
            body["patrolRange"] = dev["data"]["id"]
            print(f"[info] patrolRange auto-set from session device: {body['patrolRange']}")
        else:
            print("[error] --patrol-range not given and no device in session.", file=sys.stderr)
            sys.exit(1)

    result = api_post("/rtc/device/aiPatrolAddOrEdit", body)
    model = result.get("data", {}).get("model")

    plan_data = {
        "patrolName":  body.get("patrolName"),
        "algorithmId": body.get("algorithmId"),
        "patrolRange": body.get("patrolRange"),
        "params":      body,
        "model":       model,
        "createdAt":   datetime.now().isoformat(),
    }
    # Some responses return the batchNumber in model
    if isinstance(model, str) and model:
        plan_data["batchNumber"] = model
    elif isinstance(model, dict):
        for k in ("id", "batchNumber"):
            if model.get(k):
                plan_data["batchNumber"] = model[k]
                plan_data["id"] = model[k]
                break

    session["steps"]["patrolPlan"] = {"completed": True, "data": plan_data}
    save_session(args.session, session)

    print(f"[ok] AI patrol plan created")
    print(f"     name:      {body.get('patrolName')}")
    print(f"     algorithm: {body.get('algorithmId')}")
    print(f"     device:    {body.get('patrolRange')}")
    if plan_data.get("batchNumber"):
        print(f"     batchNumber: {plan_data['batchNumber']}")
    print(f"     Next step: list-plans / plan-detail / patrol-report")


def action_edit_plan(args) -> None:
    session = load_session(args.session)

    if not args.id:
        # Try session
        plan = session.get("steps", {}).get("patrolPlan", {})
        if plan.get("completed"):
            data = plan.get("data", {}) or {}
            args.id = data.get("batchNumber") or data.get("id") or (data.get("params", {}) or {}).get("id")
        if not args.id:
            print("[error] --id required (plan id / batchNumber).", file=sys.stderr)
            sys.exit(1)

    # Fetch existing detail to merge
    detail = api_post(f"/rtc/device/aiPatrolDetail/{args.id}", {})  # 网关只注册POST,GET路径参数404
    existing = detail.get("data", {}).get("model", {}) or {}

    body = _build_plan_body(args, existing=existing)
    body["id"] = args.id

    api_post("/rtc/device/aiPatrolAddOrEdit", body)

    plan_data = session.get("steps", {}).get("patrolPlan", {}).get("data", {}) or {}
    plan_data.update({
        "id":          args.id,
        "batchNumber": args.id,
        "patrolName":  body.get("patrolName"),
        "params":      body,
        "editedAt":    datetime.now().isoformat(),
    })
    session["steps"]["patrolPlan"] = {"completed": True, "data": plan_data}
    save_session(args.session, session)

    print(f"[ok] AI patrol plan updated: id={args.id}")


# ---------------------------------------------------------------------------
# Action: list-plans / plan-detail / start-plan / stop-plan / delete-plan
# ---------------------------------------------------------------------------

def action_list_plans(args) -> None:
    body = {
        "pageSize": args.page_size,
        "pageNo":   args.page_no,
        "param":    {},
    }
    if args.name:
        body["param"]["patrolName"] = args.name
    if args.status is not None:
        body["param"]["status"] = args.status

    result = api_post("/rtc/device/aiPatrolPageQuery", body)
    model = result.get("data", {}).get("model", {}) or {}
    datas = model.get("datas") or []

    fmt = getattr(args, "fmt", None) or getattr(args, "format", "table")
    if fmt == "json":
        print(json.dumps(model, indent=2, ensure_ascii=False))
        return

    print(f"[ok] AI patrol plans (page {model.get('pageNo')}/{model.get('totalPage')}, "
          f"total={model.get('totalCount')})")
    if not datas:
        print("     (no plans)")
        return
    tt = {0: "每天", 1: "每周", 2: "每月"}
    for p in datas:
        print(f"  - id={p.get('id')} | {p.get('patrolName')} "
              f"| {tt.get(p.get('timeType'), p.get('timeType'))} {p.get('timeCycle')} "
              f"| {p.get('detailTime')} | algo={p.get('algorithmId')} "
              f"| device={p.get('deviceName')}({p.get('patrolRange')})")


def action_plan_detail(args) -> None:
    batch = args.batch_number
    if not batch:
        session = load_session(args.session)
        plan = session.get("steps", {}).get("patrolPlan", {})
        if plan.get("completed"):
            data = plan.get("data", {}) or {}
            batch = data.get("batchNumber") or data.get("id")
    if not batch:
        print("[error] --batch-number required (or session plan).", file=sys.stderr)
        sys.exit(1)

    result = api_post(f"/rtc/device/aiPatrolDetail/{batch}", {})  # 网关只注册POST,GET路径参数404
    model = result.get("data", {}).get("model", {}) or {}

    fmt = getattr(args, "fmt", None) or getattr(args, "format", "table")
    if fmt == "json":
        print(json.dumps(model, indent=2, ensure_ascii=False))
        return

    print(f"[ok] Plan detail (batchNumber={batch})")
    for k in ("id", "patrolName", "timeType", "timeCycle", "detailTime",
              "patrolRange", "deviceName", "algorithmId", "step", "timeInterval",
              "threshold", "durationTime", "includeAreas", "mosaic", "specialParam"):
        if k in model:
            v = model[k]
            if isinstance(v, str) and len(v) > 120:
                v = v[:120] + "..."
            print(f"     {k}: {v}")


def action_start_stop_plan(args, open_switch: int) -> None:
    batch = args.id
    if not batch:
        session = load_session(args.session)
        plan = session.get("steps", {}).get("patrolPlan", {})
        if plan.get("completed"):
            data = plan.get("data", {}) or {}
            batch = data.get("batchNumber") or data.get("id")
    if not batch:
        print("[error] --id required.", file=sys.stderr)
        sys.exit(1)

    api_post("/rtc/device/aiPatrolStartAndStop", {"id": batch, "openSwitch": open_switch})
    action = "started" if open_switch == 1 else "stopped"
    print(f"[ok] AI patrol plan {action}: id={batch}")


def action_start_plan(args) -> None:
    action_start_stop_plan(args, 1)


def action_stop_plan(args) -> None:
    action_start_stop_plan(args, 0)


def action_delete_plan(args) -> None:
    batch = args.batch_number
    if not batch:
        session = load_session(args.session)
        plan = session.get("steps", {}).get("patrolPlan", {})
        if plan.get("completed"):
            data = plan.get("data", {}) or {}
            batch = data.get("batchNumber") or data.get("id")
    if not batch:
        print("[error] --batch-number required.", file=sys.stderr)
        sys.exit(1)

    api_post(f"/rtc/device/aiPatrolDelete/{batch}", {})  # 网关只注册POST,GET路径参数404

    # Clear session plan if it matches
    session = load_session(args.session)
    plan = session.get("steps", {}).get("patrolPlan", {})
    if plan.get("completed"):
        data = plan.get("data", {}) or {}
        if (data.get("batchNumber") or data.get("id")) == batch:
            session["steps"]["patrolPlan"] = {"completed": False, "data": None}
            save_session(args.session, session)

    print(f"[ok] AI patrol plan deleted: batchNumber={batch}")


# ---------------------------------------------------------------------------
# Action: list-records (aiPatrolRecordPageQuery)
# ---------------------------------------------------------------------------

def _fetch_records(body: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Paginate through aiPatrolRecordPageQuery until hasNext=false or max pages."""
    all_records: List[Dict[str, Any]] = []
    page_no = body.get("pageNo", 1)
    page_size = body.get("pageSize", 20)
    max_pages = body.pop("_maxPages", 20)
    while True:
        body["pageNo"] = page_no
        body["pageSize"] = page_size
        result = api_post("/rtc/device/aiPatrolRecordPageQuery", body)
        model = result.get("data", {}).get("model", {}) or {}
        datas = model.get("datas") or []
        all_records.extend(datas)
        if not model.get("hasNext"):
            break
        page_no += 1
        if page_no > max_pages:
            print(f"[warn] Reached max pages ({max_pages}); stopping.", file=sys.stderr)
            break
        time.sleep(0.2)
    return all_records


def action_list_records(args) -> None:
    param: Dict[str, Any] = {}
    if args.begin:  param["beginTime"] = args.begin
    if args.end:    param["endTime"]   = args.end
    if args.device_id:
        param["deviceIdList"] = [d.strip() for d in args.device_id.split(",") if d.strip()]
    if args.algorithm_id:
        param["algorithmIdList"] = [a.strip() for a in args.algorithm_id.split(",") if a.strip()]

    body = {
        "pageSize": args.page_size,
        "pageNo":   1,
        "param":    param,
        "_maxPages": args.max_pages,
    }

    records = _fetch_records(body)

    fmt = getattr(args, "fmt", None) or getattr(args, "format", "table")
    if fmt == "json":
        print(json.dumps(records, indent=2, ensure_ascii=False))
        return

    print(f"[ok] AI patrol records: {len(records)}")
    if not records:
        return
    for r in records[:args.limit]:
        print(f"  - {r.get('releaseTime')} | {r.get('deviceName')}({r.get('deviceId')}) "
              f"| {r.get('algorithmName')}({r.get('algorithmId')}) "
              f"| pic={bool(r.get('cloudPictureUrl'))}")
    if len(records) > args.limit:
        print(f"     ... and {len(records) - args.limit} more (use --format json for all)")


# ---------------------------------------------------------------------------
# Action: patrol-report (HTML: image wall + statistics)
# ---------------------------------------------------------------------------

def _record_has_detection(r: Dict[str, Any]) -> bool:
    """True if the record's detailData contains at least one detected object.

    detailData is a JSON string like [{"image":..., "objects":[{"bbox":..,"label":..,"score":..}]}].
    Records without any object mean the algorithm analyzed but did not alarm.
    """
    dd = r.get("detailData")
    if not dd:
        return False
    if isinstance(dd, str):
        try:
            dd = json.loads(dd)
        except (json.JSONDecodeError, ValueError):
            return False
    if isinstance(dd, dict):
        dd = [dd]
    if not isinstance(dd, list):
        return False
    return any(isinstance(fr, dict) and (fr.get("objects") or [])
               for fr in dd)



def action_patrol_report(args) -> None:
    param: Dict[str, Any] = {}
    if args.begin:  param["beginTime"] = args.begin
    if args.end:    param["endTime"]   = args.end
    if args.device_id:
        param["deviceIdList"] = [d.strip() for d in args.device_id.split(",") if d.strip()]
    if args.algorithm_id:
        param["algorithmIdList"] = [a.strip() for a in args.algorithm_id.split(",") if a.strip()]

    body = {
        "pageSize": 50,
        "pageNo":   1,
        "param":    param,
        "_maxPages": args.max_pages,
    }

    print(f"[info] Fetching AI patrol records ({args.begin} ~ {args.end}) ...")
    records = _fetch_records(body)
    print(f"[info] Fetched {len(records)} records")

    # Aggregate statistics
    by_device: Dict[str, int] = {}
    by_algo: Dict[str, int] = {}
    algo_alarm: Dict[str, int] = {}
    by_day: Dict[str, int] = {}
    with_pic = 0
    for r in records:
        dev = r.get("deviceName") or r.get("deviceId") or "unknown"
        algo = r.get("algorithmName") or r.get("algorithmId") or "unknown"
        rt = r.get("releaseTime") or ""
        day = rt.split(" ")[0] if rt else "unknown"
        by_device[dev] = by_device.get(dev, 0) + 1
        by_algo[algo] = by_algo.get(algo, 0) + 1
        if _record_has_detection(r):
            algo_alarm[algo] = algo_alarm.get(algo, 0) + 1
        by_day[day] = by_day.get(day, 0) + 1
        if r.get("cloudPictureUrl"):
            with_pic += 1

    # Store name for title
    store_name = args.title
    if not store_name:
        path = get_session_path(args.session)
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    session = json.load(f)
                step = session.get("steps", {}).get("store", {})
                if step.get("completed") and step.get("data"):
                    store_name = step["data"].get("storeName")
            except (json.JSONDecodeError, IOError):
                pass
    store_name = store_name or "AI 巡检记录"

    report = {
        "meta": {
            "title":       store_name,
            "rangeBegin":  args.begin,
            "rangeEnd":    args.end,
            "generatedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "totalRecords": len(records),
            "withPicture":  with_pic,
        },
        "byDevice": [{"name": k, "count": v} for k, v in
                     sorted(by_device.items(), key=lambda x: -x[1])],
        "byAlgorithm": [{"name": k, "count": v, "alarmCount": algo_alarm.get(k, 0)} for k, v in
                        sorted(by_algo.items(), key=lambda x: -x[1])],
        "byDay": [{"date": k, "count": v} for k, v in sorted(by_day.items())],
        "records": records,
    }

    script_dir    = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.normpath(
        os.path.join(script_dir, "..", "assets", "patrol_report_template.html"))
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

    print(f"[ok] Patrol report generated: {os.path.abspath(args.output)}")
    print(f"     Range:   {args.begin} ~ {args.end}")
    print(f"     Records: {len(records)} (with picture: {with_pic})")
    print(f"     Devices: {len(by_device)}, Algorithms: {len(by_algo)}")


# ---------------------------------------------------------------------------
# Action: snapshot (livestream frame grab)
# ---------------------------------------------------------------------------

def action_snapshot(args) -> None:
    session = load_session(args.session)
    require_step(session, "device", "Run 'add-device' first.")
    device_sn = session["steps"]["device"]["data"]["deviceSN"]

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

    api_post(f"/rtc/device/login/{token}", {
        "UserName": args.username, "PassWord": args.password,
        "KeepaliveTime": 60,
    })

    stream = api_post(f"/rtc/device/livestream/{token}", {
        "channel": args.channel, "stream": args.stream, "protocol": "flv",
        "username": args.username, "password": args.password,
    })
    data = stream.get("data") or {}
    url = data.get("url") or data.get("URL")
    if not url:
        print("[error] No livestream url in response.", file=sys.stderr)
        sys.exit(1)

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
# Action: generate-config-page (includeAreas drawing tool)
# ---------------------------------------------------------------------------

def action_generate_config_page(args) -> None:
    session = load_session(args.session)
    require_step(session, "device", "Run 'add-device' first.")

    device_data = session["steps"]["device"]["data"]
    device_id   = device_data.get("id", "")
    device_sn   = device_data.get("deviceSN", "")

    snapshot_path = args.snapshot
    if not os.path.exists(snapshot_path):
        print(f"[error] Snapshot file not found: {snapshot_path}", file=sys.stderr)
        sys.exit(1)

    with open(snapshot_path, "rb") as f:
        snapshot_b64 = base64.b64encode(f.read()).decode("ascii")

    ext = os.path.splitext(snapshot_path)[1].lower()
    mime_map = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                ".gif": "image/gif", ".bmp": "image/bmp", ".webp": "image/webp"}
    mime = mime_map.get(ext, "image/png")

    script_dir   = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.normpath(
        os.path.join(script_dir, "..", "assets", "config_tool.html"))
    if not os.path.exists(template_path):
        print(f"[error] Template not found: {template_path}", file=sys.stderr)
        sys.exit(1)

    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()

    inject_script = (
        f"<script>\n"
        f"  window.__SNAPSHOT_BASE64__ = \"data:{mime};base64,{snapshot_b64}\";\n"
        f"  window.__DEVICE_ID__ = {json.dumps(device_id)};\n"
        f"  window.__DEVICE_SN__ = {json.dumps(device_sn)};\n"
        f"</script>\n"
    )
    html = html.replace("</head>", inject_script + "</head>")

    output_path = args.output
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[ok] Config page generated: {os.path.abspath(output_path)}")
    print(f"     Device: {device_id} (SN: {device_sn})")
    print(f"     Next: open in browser, draw includeAreas polygon, download JSON,")
    print(f"           then feed to create-plan --from-file <downloaded.json>")


# ---------------------------------------------------------------------------
# Main / argparse
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="杰峰智慧巡店部署与AI巡检运营技能 (JF Smart Store Inspection)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--session", default="./session",
                        help="Session directory (default: ./session)")
    parser.add_argument("--format", choices=["table", "json"], default="table",
                        help="Output format (default: table)")

    sub = parser.add_subparsers(dest="action", help="Available actions")

    # --- init / status / reset ---
    sub.add_parser("init", help="Initialize a new deployment session")
    p_st = sub.add_parser("status", help="Show current session status")
    p_st.add_argument("--format", dest="fmt", choices=["table", "json"], default=None)
    sub.add_parser("reset", help="Reset (delete) the current session")

    # --- store ---
    p_cs = sub.add_parser("create-store", help="Create a new store")
    p_cs.add_argument("--store-name", required=True)
    p_cs.add_argument("--address",    default=None)
    p_cs.add_argument("--longitude",  type=float, default=None)
    p_cs.add_argument("--latitude",   type=float, default=None)

    p_es = sub.add_parser("edit-store", help="Edit an existing store")
    p_es.add_argument("--store-name", required=True)
    p_es.add_argument("--address",    default=None)
    p_es.add_argument("--longitude",  type=float, default=None)
    p_es.add_argument("--latitude",   type=float, default=None)

    sub.add_parser("delete-store", help="Delete the current store")

    # --- device ---
    p_ad = sub.add_parser("add-device", help="Add a JF IPC device to the store")
    p_ad.add_argument("--sn",              required=True)
    p_ad.add_argument("--network-type",    required=True, type=int, choices=[0, 1],
                       help="0=already configured, 1=not configured")
    p_ad.add_argument("--device-name",     default=None)
    p_ad.add_argument("--device-username", default=None)
    p_ad.add_argument("--device-password", default=None)

    sub.add_parser("delete-device", help="Delete the current device")

    # --- algorithms ---
    p_la = sub.add_parser("list-algorithms", help="List available AI patrol algorithms")
    p_la.add_argument("--name", default=None, help="Filter by algorithmName (fuzzy)")
    p_la.add_argument("--page-size", type=int, default=20)
    p_la.add_argument("--page-no",   type=int, default=1)
    p_la.add_argument("--format", dest="fmt", choices=["table", "json"], default=None)

    # --- plans ---
    def _add_plan_common_args(p, is_create: bool):
        p.add_argument("--from-file", default=None,
                       help="Load plan config from JSON (e.g. downloaded from config tool)")
        p.add_argument("--plan-name", default=None, help="patrolName")
        p.add_argument("--time-type", type=int, choices=[0, 1, 2], default=None,
                       help="0=daily, 1=weekly, 2=monthly")
        p.add_argument("--time-cycle", default=None,
                       help="daily='0', weekly='1,2,3', monthly='1,15'")
        p.add_argument("--detail-time", default=None,
                       help="HH:MM-HH:MM,HH:MM-HH:MM (max 5 segments, no overlap)")
        p.add_argument("--patrol-range", default=None,
                       help="Device resource id (default: session device)")
        p.add_argument("--algorithm-id", default=None)
        p.add_argument("--threshold", default=None, help="0.01~0.99")
        p.add_argument("--step", type=int, default=None, help="Frame sampling rate")
        p.add_argument("--time-interval", type=int, default=None)
        p.add_argument("--include-areas", default=None,
                       help="JSON string of detection areas (from config tool)")
        p.add_argument("--duration-time", type=int, default=None)
        p.add_argument("--mosaic", default=None, help="face,plate,human (comma separated)")
        p.add_argument("--special-param", default=None)
        if not is_create:
            p.add_argument("--id", default=None, help="Plan id / batchNumber (edit only)")

    p_cp = sub.add_parser("create-plan", help="Create AI patrol plan (aiPatrolAddOrEdit)")
    _add_plan_common_args(p_cp, is_create=True)

    p_ep = sub.add_parser("edit-plan", help="Edit AI patrol plan (merges existing detail)")
    _add_plan_common_args(p_ep, is_create=False)

    p_lp = sub.add_parser("list-plans", help="List AI patrol plans (aiPatrolPageQuery)")
    p_lp.add_argument("--name", default=None, help="Filter by patrolName")
    p_lp.add_argument("--status", type=int, choices=[1, 2], default=None,
                      help="1=running, 2=paused")
    p_lp.add_argument("--page-size", type=int, default=20)
    p_lp.add_argument("--page-no",   type=int, default=1)
    p_lp.add_argument("--format", dest="fmt", choices=["table", "json"], default=None)

    p_pd = sub.add_parser("plan-detail", help="Get AI patrol plan detail")
    p_pd.add_argument("--batch-number", default=None,
                      help="Batch number / plan id (default: session)")
    p_pd.add_argument("--format", dest="fmt", choices=["table", "json"], default=None)

    p_sp = sub.add_parser("start-plan", help="Enable AI patrol plan")
    p_sp.add_argument("--id", default=None, help="Plan id / batchNumber")

    p_tp = sub.add_parser("stop-plan", help="Disable AI patrol plan")
    p_tp.add_argument("--id", default=None, help="Plan id / batchNumber")

    p_dp = sub.add_parser("delete-plan", help="Delete AI patrol plan")
    p_dp.add_argument("--batch-number", default=None)

    # --- records ---
    _today = datetime.now().strftime("%Y-%m-%d")
    _week_ago = (datetime.now() - timedelta(days=6)).strftime("%Y-%m-%d")

    p_lr = sub.add_parser("list-records", help="Query AI patrol records")
    p_lr.add_argument("--begin", default=_week_ago, help="yyyy-MM-dd (default: 7 days ago)")
    p_lr.add_argument("--end",   default=_today,    help="yyyy-MM-dd (default: today)")
    p_lr.add_argument("--device-id",    default=None, help="Comma separated device ids")
    p_lr.add_argument("--algorithm-id", default=None, help="Comma separated algorithm ids")
    p_lr.add_argument("--page-size", type=int, default=50)
    p_lr.add_argument("--max-pages", type=int, default=20)
    p_lr.add_argument("--limit", type=int, default=20, help="Print first N in table mode")
    p_lr.add_argument("--format", dest="fmt", choices=["table", "json"], default=None)

    p_pr = sub.add_parser("patrol-report", help="Generate HTML report (image wall + stats)")
    p_pr.add_argument("--begin", default=_week_ago)
    p_pr.add_argument("--end",   default=_today)
    p_pr.add_argument("--device-id",    default=None)
    p_pr.add_argument("--algorithm-id", default=None)
    p_pr.add_argument("--max-pages", type=int, default=20)
    p_pr.add_argument("--title",  default=None)
    p_pr.add_argument("--output", default="./patrol_report.html")

    # --- snapshot / config page ---
    p_snap = sub.add_parser("snapshot", help="Grab a live frame via livestream")
    p_snap.add_argument("--output",   default=None)
    p_snap.add_argument("--username", default="admin")
    p_snap.add_argument("--password", default="")
    p_snap.add_argument("--channel",  default="0")
    p_snap.add_argument("--stream",   default="0", help="0=main, 1=sub")
    p_snap.add_argument("--frames",   type=int, default=15)

    p_gcp = sub.add_parser("generate-config-page",
                           help="Generate interactive includeAreas drawing tool page")
    p_gcp.add_argument("--snapshot", required=True)
    p_gcp.add_argument("--output",   default="./config_tool.html")

    args = parser.parse_args()

    if not args.action:
        parser.print_help()
        sys.exit(1)

    actions = {
        "init":                 action_init,
        "status":               action_status,
        "reset":                action_reset,
        "create-store":         action_create_store,
        "edit-store":           action_edit_store,
        "delete-store":         action_delete_store,
        "add-device":           action_add_device,
        "delete-device":        action_delete_device,
        "list-algorithms":      action_list_algorithms,
        "create-plan":          action_create_plan,
        "edit-plan":            action_edit_plan,
        "list-plans":           action_list_plans,
        "plan-detail":          action_plan_detail,
        "start-plan":           action_start_plan,
        "stop-plan":            action_stop_plan,
        "delete-plan":          action_delete_plan,
        "list-records":         action_list_records,
        "patrol-report":        action_patrol_report,
        "snapshot":             action_snapshot,
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
