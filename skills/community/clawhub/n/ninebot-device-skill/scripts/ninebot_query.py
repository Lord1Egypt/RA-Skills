#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ninebot vehicle query (placeholder workflow).
- API key -> list devices
- Pick device by name or sn
- Query device info -> battery/status/location

Config is overridable via --config (JSON). See references/api-spec.md.
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.parse
from typing import Any, Dict, Optional

DEFAULT_CONFIG = {
    "base_url": "https://cn-cbu-gateway.ninebot.com",
    "auth": {
        "api_key_header": "Authorization",
        "api_key_prefix": "Bearer ",
    },
    "devices": {
        "method": "GET",
        "path": "/ai-skill/api/device/info/get-device-list",
        "payload": {},
        "list_path": "data",
        "sn_field": "sn",
        "name_field": "deviceName",
    },
    "device_info": {
        "method": "POST",
        "path": "/ai-skill/api/device/info/get-device-dynamic-info",
        "payload": {"sn": "{sn}"},
        "battery_path": "data.dumpEnergy",
        "status_path": "data.powerStatus",
        "location_path": "data.locationInfo.locationDesc",
        "extra_fields": {
            "estimateMileage": "data.estimateMileage",
            "chargingState": "data.chargingState",
            "remainChargeTime": "data.remainChargeTime",
        },
    },
}

def load_config(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def deep_get(data: Dict[str, Any], path: str) -> Any:
    """Get value by dot path (e.g., data.token)."""
    cur: Any = data
    for part in path.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return None
    return cur


def get_base_url(cfg: Dict[str, Any], section: str) -> str:
    section_url = (cfg.get(section) or {}).get("base_url")
    if section_url:
        return section_url
    return cfg.get("base_url", "")


def http_request(
    method: str,
    url: str,
    headers: Dict[str, str] = None,
    payload: Dict[str, Any] = None,
) -> Dict[str, Any]:
    headers = headers or {}
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(url, data=data, headers=headers, method=method.upper())
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as err:
        raise


def read_config_from_default() -> Optional[Dict[str, Any]]:
    path = os.path.join(os.getcwd(), "config.json")
    if os.path.exists(path):
        return load_config(path)
    return None


def resolve_api_key(cfg: Dict[str, Any], arg_api_key: Optional[str]) -> Optional[str]:
    if arg_api_key:
        return arg_api_key
    env_key = os.getenv("NINEBOT_DEVICESERVICE_KEY")
    if env_key:
        return env_key
    cfg_key = cfg.get("apiKey") if isinstance(cfg, dict) else None
    if cfg_key:
        return cfg_key
    return None


def inject_api_key_header(cfg: Dict[str, Any], headers: Dict[str, str], api_key: str):
    auth_cfg = cfg.get("auth") or {}
    header_name = auth_cfg.get("api_key_header") or "x-api-key"
    prefix = auth_cfg.get("api_key_prefix") or ""
    headers[header_name] = f"{prefix}{api_key}"


def list_devices(cfg: Dict[str, Any], api_key: str, lang: str):
    url = get_base_url(cfg, "devices").rstrip("/") + cfg["devices"]["path"]
    payload_tpl = cfg["devices"].get("payload") or {}
    payload = {
        k: (v.format(api_key=api_key, lang=lang) if isinstance(v, str) else v)
        for k, v in payload_tpl.items()
    }
    headers: Dict[str, str] = {}
    if api_key:
        inject_api_key_header(cfg, headers, api_key)
    payload_to_send = None if cfg["devices"]["method"].upper() == "GET" else payload
    res = http_request(cfg["devices"]["method"], url, headers=headers, payload=payload_to_send)
    devices = deep_get(res, cfg["devices"]["list_path"]) or []
    return devices


def get_device_info(cfg: Dict[str, Any], api_key: str, sn: str):
    path = cfg["device_info"]["path"].replace("{sn}", urllib.parse.quote(sn))
    url = get_base_url(cfg, "device_info").rstrip("/") + path
    payload_tpl = cfg["device_info"].get("payload") or {}
    payload = {
        k: (v.format(api_key=api_key, sn=sn) if isinstance(v, str) else v)
        for k, v in payload_tpl.items()
    }
    headers: Dict[str, str] = {}
    if api_key:
        inject_api_key_header(cfg, headers, api_key)
    res = http_request(cfg["device_info"]["method"], url, headers=headers, payload=payload)
    if res['code'] != 0:
        raise Exception(f"API error: {res.get('msg', 'Unknown error')} (code: {res.get('code')})")
    
    out = {
        "battery": deep_get(res, cfg["device_info"]["battery_path"]),
        "status": deep_get(res, cfg["device_info"]["status_path"]),
        "location": deep_get(res, cfg["device_info"]["location_path"]),
    }
    extra = cfg["device_info"].get("extra_fields") or {}
    for k, path in extra.items():
        out[k] = deep_get(res, path)
    return out


def main():
    parser = argparse.ArgumentParser(description="Ninebot vehicle query (placeholder).")
    parser.add_argument("--api-key", default=None, help="Ninebot device service API key")
    parser.add_argument("--device-name", default=None, help="Device name to select")
    parser.add_argument("--device-sn", default=None, help="Device SN to select")
    parser.add_argument("--lang", default="zh", help="Language: zh | zh-hant | en")
    args = parser.parse_args()

    cfg = DEFAULT_CONFIG
    cfg_from_default = read_config_from_default()
    if cfg_from_default:
        cfg.update(cfg_from_default)  # Override defaults with saved config

    api_key = resolve_api_key(cfg, args.api_key)
    if not api_key:
        print(json.dumps({"error": "Missing API key. Set NINEBOT_DEVICESERVICE_KEY or provide --api-key or config.json"}, ensure_ascii=False))
        sys.exit(2)

    devices = list_devices(cfg, api_key or "", args.lang)

    if not devices:
        print(json.dumps({"error": "No devices found"}, ensure_ascii=False))
        sys.exit(2)

    selected = None
    if args.device_sn:
        for d in devices:
            if str(d.get(cfg["devices"]["sn_field"])) == args.device_sn:
                selected = d
                break
    elif args.device_name:
        for d in devices:
            if str(d.get(cfg["devices"]["name_field"])) == args.device_name:
                selected = d
                break
    else:
        # If multiple devices, return list for caller to decide
        if len(devices) > 1:
            print(json.dumps({"choose_device": devices}, ensure_ascii=False))
            sys.exit(3)
        selected = devices[0]

    if not selected:
        print(json.dumps({"error": "Device not found", "devices": devices}, ensure_ascii=False))
        sys.exit(4)

    sn = str(selected.get(cfg["devices"]["sn_field"]))
    name = selected.get(cfg["devices"]["name_field"]) or ""
    info = get_device_info(cfg, api_key or "", sn)

    power_status = info.get("status")
    if power_status is None:
        power_status_str = "unknown"
    else:
        if str(power_status).upper() in ["0"]:
            power_status_str = "OFF"
        elif str(power_status).upper() in ["1"]:
            power_status_str = "ON"
        else:
            power_status_str = "unknown"
            
    charging_state = info.get("chargingState")
    charging_status = "not_charge"
    if charging_state is not None and str(charging_state).upper() in ["1"]:
        charging_status = "charging"

    output = {
        "device_name": name,
        "battery": info.get("battery"),
        "powerStatus": power_status_str,
        "location": info.get("location"),
        "estimateMileage": info.get("estimateMileage"),
        "chargingState": charging_status,
        "remainChargingTime": info.get("remainChargeTime")
    }
    print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()
