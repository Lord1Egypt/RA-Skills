import json
import os
import random
import socket
import time
import urllib.error
import urllib.request
from pathlib import Path

BASE_URL = "https://lkk.mosobleirc.ru"
USER_AGENT = "OpenClaw-MosOblEIRC/1.0"
INVENTORY_PATH = Path(__file__).with_name("inventory.json")
READ_ATTEMPTS = 2
BUILD = "1.0.1"

class NetworkError(Exception):
    pass

class ApiError(Exception):
    def __init__(self, status: int, payload=None):
        super().__init__(f"upstream status {status}")
        self.status = status
        self.payload = payload or {}

def _json_response(status: int, payload: dict) -> dict:
    return {"statusCode": status, "headers": {"Content-Type": "application/json; charset=utf-8"},
            "body": json.dumps(payload, ensure_ascii=False, separators=(",", ":"))}

def _decode_json(raw: bytes):
    if not raw:
        return {}
    text = raw.decode("utf-8", errors="replace")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"raw": text[:500]}

def _request_once(path: str, token: str, timeout: int = 8):
    headers = {"User-Agent": USER_AGENT, "X-Auth-Tenant-Token": token, "Accept": "application/json"}
    req = urllib.request.Request(BASE_URL + path, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.status, _decode_json(response.read())
    except urllib.error.HTTPError as exc:
        return exc.code, _decode_json(exc.read())
    except (urllib.error.URLError, TimeoutError, socket.timeout) as exc:
        raise NetworkError(str(exc)) from exc


def _write_once(path: str, token: str, payload: dict, timeout: int = 10):
    headers={"User-Agent":USER_AGENT,"X-Auth-Tenant-Token":token,"Accept":"application/json",
             "Content-Type":"application/json; charset=utf-8"}
    body=json.dumps(payload,ensure_ascii=False,separators=(",",":")).encode("utf-8")
    req=urllib.request.Request(BASE_URL+path,data=body,headers=headers,method="POST")
    try:
        with urllib.request.urlopen(req,timeout=timeout) as response:
            return response.status,_decode_json(response.read())
    except urllib.error.HTTPError as exc:
        return exc.code,_decode_json(exc.read())
    except (urllib.error.URLError,TimeoutError,socket.timeout) as exc:
        raise NetworkError(str(exc)) from exc


def _meter_entry(entries, meter_id: int):
    if not isinstance(entries,list):
        return None
    for item in entries:
        meter=item.get("meter") if isinstance(item,dict) else None
        if isinstance(meter,dict) and int(meter.get("id") or -1)==int(meter_id):
            return item
    return None

def _token() -> str:
    token = os.environ.get("MOSOBLEIRC_TOKEN", "").strip()
    if not token:
        raise ApiError(503, {"errorCode": "TOKEN_NOT_CONFIGURED"})
    return token

def _live_get(path: str):
    token = _token()
    last_error = None
    for attempt in range(READ_ATTEMPTS):
        try:
            status, data = _request_once(path, token)
        except NetworkError as exc:
            last_error = exc
            if attempt + 1 >= READ_ATTEMPTS:
                raise
            time.sleep(2.0 + random.uniform(0.0, 0.7))
            continue
        if status in (401, 403):
            raise ApiError(status, {"errorCode": "AUTH_REQUIRED"})
        if 500 <= status <= 599 and attempt + 1 < READ_ATTEMPTS:
            time.sleep(2.0 + random.uniform(0.0, 0.7))
            continue
        if 200 <= status < 300:
            return data
        raise ApiError(status, data)
    raise NetworkError(str(last_error or "unknown network error"))

def _load_inventory(*, strict: bool = False):
    try:
        data = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise ValueError("inventory must be a list")
        return data
    except Exception as exc:
        if strict:
            raise ApiError(503, {"errorCode": "INVENTORY_NOT_CONFIGURED"}) from exc
        return []


def _inventory_allows(inventory, item_id: int, meter_id: int) -> bool:
    for item in inventory:
        if not isinstance(item, dict):
            continue
        try:
            same_item = int(item.get("item_id")) == int(item_id)
        except (TypeError, ValueError):
            continue
        if not same_item:
            continue
        for meter in item.get("meters") or []:
            if not isinstance(meter, dict):
                continue
            try:
                if int(meter.get("meter_id")) == int(meter_id):
                    return True
            except (TypeError, ValueError):
                continue
    return False


def _entry_verifies_current_period(entry, meter_id: int, value: int) -> bool:
    if not isinstance(entry, dict):
        return False
    meter = entry.get("meter")
    if not isinstance(meter, dict):
        return False
    try:
        if int(meter.get("id")) != int(meter_id):
            return False
    except (TypeError, ValueError):
        return False
    last = meter.get("lastValue") or {}
    total = last.get("total") or {}
    try:
        same_value = int(float(total.get("value"))) == int(value)
    except (TypeError, ValueError):
        return False
    info = entry.get("valueSendInfo") or {}
    return (
        same_value
        and str(last.get("status") or "").upper() == "PROCESSED"
        and info.get("isValueSentForCurrentPeriod") is True
    )


def _readback_after_write(read_path: str, meter_id: int, value: int):
    try:
        readback = _live_get(read_path)
    except (NetworkError, ApiError):
        return None, False
    entry = _meter_entry(readback, meter_id)
    return entry, _entry_verifies_current_period(entry, meter_id, value)

def _numeric_id(value, error_code: str):
    text = str(value or "")
    if not text.isdigit():
        raise ValueError(error_code)
    return text

def _api_error_payload(exc: ApiError):
    data = exc.payload if isinstance(exc.payload, dict) else {}
    code = data.get("errorCode") or "MOSOBLEIRC_API_ERROR"
    if exc.status in (401, 403):
        return 401, {"ok": False, "error": "AUTH_REQUIRED", "upstream_status": exc.status}
    if exc.status == 503 and code == "TOKEN_NOT_CONFIGURED":
        return 503, {"ok": False, "error": code}
    message = data.get("message") or data.get("techMessage") or "Upstream API error"
    return 502, {"ok": False, "error": code, "upstream_status": exc.status, "message": str(message)[:300]}

def _local_status():
    inventory = _load_inventory()
    meter_count = sum(len(x.get("meters") or []) for x in inventory if isinstance(x, dict))
    return {"ok": True, "service": "mosobleirc-relay", "build": BUILD,
            "provider_contacted": False, "token_configured": bool(os.environ.get("MOSOBLEIRC_TOKEN")),
            "writes_enabled": os.environ.get("ALLOW_WRITES", "false").lower() == "true",
            "inventory_items": len(inventory), "inventory_meters": meter_count}

def dispatch(payload: dict):
    action = payload.get("action")
    if action in {"ping", "status"}:
        return 200, _local_status()
    if action == "inventory":
        return 200, {"ok": True, "provider_contacted": False, "data": _load_inventory()}
    if action == "write-status":
        return 200, {"ok": True, "provider_contacted": False,
                     "writes_enabled": os.environ.get("ALLOW_WRITES", "false").lower() == "true"}
    if action == "submit":
        if os.environ.get("ALLOW_WRITES", "false").lower() != "true":
            return 403, {"ok": False, "error": "WRITES_DISABLED"}
        operation_id=str(payload.get("operation_id") or "").strip()
        if not operation_id:
            return 400, {"ok": False, "error": "OPERATION_ID_REQUIRED"}
        try:
            item_id=int(_numeric_id(payload.get("item_id"), "INVALID_ITEM_ID"))
            meter_id=int(_numeric_id(payload.get("meter_id"), "INVALID_METER_ID"))
        except ValueError as exc:
            return 400, {"ok": False, "error": str(exc)}
        value=payload.get("value")
        if isinstance(value,bool) or not isinstance(value,int) or value < 0:
            return 400, {"ok": False, "error": "INVALID_VALUE"}
        write_path=f"/api/api/clients/meters/{meter_id}/values?withOptionalCheck=true"
        read_path=f"/api/api/clients/meters/for-item/{item_id}"
        try:
            inventory=_load_inventory(strict=True)
        except ApiError:
            return 503,{"ok":False,"error":"INVENTORY_NOT_CONFIGURED","provider_contacted":False,
                        "operation_id":operation_id}
        if not _inventory_allows(inventory,item_id,meter_id):
            return 400,{"ok":False,"error":"METER_BINDING_MISMATCH","provider_contacted":False,
                        "operation_id":operation_id}
        try:
            token=_token()
            try:
                upstream_status, upstream=_write_once(write_path,token,{"value1":value})
            except NetworkError:
                entry,verified=_readback_after_write(read_path,meter_id,value)
                if verified:
                    return 200,{"ok":True,"provider_contacted":True,"operation_id":operation_id,
                                "status":"VERIFIED_AFTER_UNCERTAIN_RESPONSE","value":value,"readback_meter":entry}
                return 202,{"ok":False,"provider_contacted":True,"operation_id":operation_id,
                            "status":"UNCERTAIN_NO_RETRY","value":value}
            if upstream_status in (401,403):
                raise ApiError(upstream_status,{"errorCode":"AUTH_REQUIRED"})
            if upstream_status in {408,409,425,429} or 500 <= upstream_status <= 599:
                entry,verified=_readback_after_write(read_path,meter_id,value)
                if verified:
                    return 200,{"ok":True,"provider_contacted":True,"operation_id":operation_id,
                                "status":"VERIFIED_AFTER_UNCERTAIN_RESPONSE","value":value,
                                "readback_meter":entry,"upstream_status":upstream_status}
                return 202,{"ok":False,"provider_contacted":True,"operation_id":operation_id,
                            "status":"UNCERTAIN_NO_RETRY","value":value,"upstream_status":upstream_status}
            if not 200 <= upstream_status < 300:
                raise ApiError(upstream_status,upstream)
            entry,verified=_readback_after_write(read_path,meter_id,value)
            if verified:
                return 200,{"ok":True,"provider_contacted":True,"operation_id":operation_id,
                            "status":"VERIFIED","value":value,"readback_meter":entry}
            return 202,{"ok":False,"provider_contacted":True,"operation_id":operation_id,
                        "status":"UNCERTAIN_NO_RETRY","value":value}
        except ApiError as exc:
            status,result=_api_error_payload(exc); result["provider_contacted"]=True; result["operation_id"]=operation_id
            return status,result
    if action not in {"accounts", "items", "meters"}:
        return 400, {"ok": False, "error": "UNKNOWN_ACTION"}
    if action == "meters" and not payload.get("item_id"):
        return 400, {"ok": False, "error": "ITEM_ID_REQUIRED"}
    try:
        if action == "accounts":
            data = _live_get("/api/api/clients")
        elif action == "items":
            data = _live_get("/api/api/clients/configuration-items")
        else:
            try:
                item_id = _numeric_id(payload.get("item_id"), "INVALID_ITEM_ID")
            except ValueError as exc:
                return 400, {"ok": False, "error": str(exc)}
            data = _live_get(f"/api/api/clients/meters/for-item/{item_id}")
        return 200, {"ok": True, "provider_contacted": True, "data": data}
    except NetworkError:
        return 503, {"ok": False, "error": "RETRYABLE_EGRESS", "provider_contacted": True}
    except ApiError as exc:
        status, result = _api_error_payload(exc)
        result["provider_contacted"] = True
        return status, result

def handler(event, context):
    event = event or {}
    if not isinstance(event, dict):
        return _json_response(400, {"ok": False, "error": "BAD_EVENT"})

    # Direct yc invoke is already protected by Yandex IAM, so HMAC is not required there.
    if "body" not in event and "action" in event:
        try:
            status, result = dispatch(event)
        except Exception:
            return _json_response(500, {"ok": False, "error": "INTERNAL_ERROR"})
        return _json_response(status, result)

    # HTTPS invocation is protected by Yandex IAM at the platform level.
    body = event.get("body") or "{}"
    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        return _json_response(400, {"ok": False, "error": "BAD_JSON"})
    if not isinstance(payload, dict):
        return _json_response(400, {"ok": False, "error": "BAD_JSON"})
    try:
        status, result = dispatch(payload)
    except Exception:
        return _json_response(500, {"ok": False, "error": "INTERNAL_ERROR"})
    return _json_response(status, result)
