#!/usr/bin/env python3
"""
Imou Device Config Skill – CLI entry.

Commands: plan, sensitivity, privacy (PaaS); iot model, property get/set, service (IoT thing-model).
All descriptions and output in English. Requires IMOU_APP_ID, IMOU_APP_SECRET; optional IMOU_BASE_URL.
"""

import argparse
import json
import os
import sys

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

from imou_client import (
    get_access_token,
    get_device_camera_status,
    set_device_camera_status,
    device_alarm_plan,
    modify_device_alarm_plan,
    set_device_alarm_sensitivity,
    get_product_model,
    get_iot_device_properties,
    set_iot_device_properties,
    iot_device_control,
)

APP_ID = os.environ.get("IMOU_APP_ID", "")
APP_SECRET = os.environ.get("IMOU_APP_SECRET", "")
BASE_URL = os.environ.get("IMOU_BASE_URL", "").strip() or "https://openapi.lechange.cn"

PRIVACY_ENABLE_TYPE = "closeCamera"


def _ensure_token():
    if not APP_ID or not APP_SECRET:
        print("[ERROR] Set IMOU_APP_ID and IMOU_APP_SECRET.", file=sys.stderr)
        sys.exit(1)
    r = get_access_token(APP_ID, APP_SECRET, BASE_URL or None)
    if not r.get("success"):
        print(f"[ERROR] Get token failed: {r.get('error', 'Unknown')}", file=sys.stderr)
        sys.exit(1)
    return r["access_token"]


def cmd_plan_get(args):
    token = _ensure_token()
    r = device_alarm_plan(
        token, args.serial, args.channel_id, base_url=BASE_URL or None
    )
    if not r.get("success"):
        print(f"[ERROR] Get plan failed: {r.get('error', 'Unknown')}", file=sys.stderr)
        sys.exit(1)
    rules = r.get("rules", [])
    print(f"[INFO] deviceId={args.serial} channelId={args.channel_id} plan rules: {len(rules)}")
    for rule in rules:
        print(f"  period={rule.get('period')} enable={rule.get('enable')} "
              f"beginTime={rule.get('beginTime')} endTime={rule.get('endTime')}")
    if args.json:
        print(json.dumps({"channelId": r.get("channel_id"), "rules": rules}, ensure_ascii=False, indent=2))


def cmd_plan_set(args):
    token = _ensure_token()
    try:
        rules = json.loads(args.rules) if isinstance(args.rules, str) else args.rules
    except (json.JSONDecodeError, TypeError) as e:
        print(f"[ERROR] Invalid rules JSON: {e}", file=sys.stderr)
        sys.exit(1)
    if not isinstance(rules, list) or not rules:
        print("[ERROR] rules must be a non-empty JSON array of {period, beginTime, endTime}.", file=sys.stderr)
        sys.exit(1)
    r = modify_device_alarm_plan(
        token, args.serial, args.channel_id, rules, base_url=BASE_URL or None
    )
    if not r.get("success"):
        print(f"[ERROR] Set plan failed: {r.get('error', 'Unknown')}", file=sys.stderr)
        sys.exit(1)
    print(f"[SUCCESS] Motion detection plan updated for {args.serial} channel {args.channel_id}")


def cmd_sensitivity_set(args):
    token = _ensure_token()
    level = max(1, min(5, args.level))
    r = set_device_alarm_sensitivity(
        token, args.serial, args.channel_id, level, base_url=BASE_URL or None
    )
    if not r.get("success"):
        print(f"[ERROR] Set sensitivity failed: {r.get('error', 'Unknown')}", file=sys.stderr)
        sys.exit(1)
    print(f"[SUCCESS] Motion detection sensitivity set to {level} (1=lowest, 5=highest) for {args.serial} channel {args.channel_id}")


def cmd_privacy_get(args):
    token = _ensure_token()
    r = get_device_camera_status(
        token, args.serial, args.channel_id, PRIVACY_ENABLE_TYPE, base_url=BASE_URL or None
    )
    if not r.get("success"):
        print(f"[ERROR] Get privacy status failed: {r.get('error', 'Unknown')}", file=sys.stderr)
        sys.exit(1)
    status = r.get("status", "off")
    print(f"[INFO] Privacy mode (closeCamera) for {args.serial} channel {args.channel_id}: {status}")
    if args.json:
        print(json.dumps({"enableType": PRIVACY_ENABLE_TYPE, "status": status}, ensure_ascii=False, indent=2))


def cmd_privacy_set(args):
    token = _ensure_token()
    on_off = args.on_off.strip().lower()
    if on_off not in ("on", "off", "1", "0", "true", "false"):
        print("[ERROR] Use on|off for privacy state.", file=sys.stderr)
        sys.exit(1)
    enable = on_off in ("on", "1", "true")
    r = set_device_camera_status(
        token, args.serial, args.channel_id, PRIVACY_ENABLE_TYPE, enable, base_url=BASE_URL or None
    )
    if not r.get("success"):
        print(f"[ERROR] Set privacy failed: {r.get('error', 'Unknown')}", file=sys.stderr)
        sys.exit(1)
    print(f"[SUCCESS] Privacy mode set to {'on' if enable else 'off'} for {args.serial} channel {args.channel_id}")


# --- IoT thing-model commands ---


def cmd_iot_model(args):
    """Get product thing model (properties, services, events) for IoT devices."""
    token = _ensure_token()
    r = get_product_model(token, args.product_id, base_url=BASE_URL or None)
    if not r.get("success"):
        print(f"[ERROR] Get product model failed: {r.get('error', 'Unknown')}", file=sys.stderr)
        sys.exit(1)
    model = r.get("model", {})
    if args.json:
        print(json.dumps(model, ensure_ascii=False, indent=2))
        return
    profile = model.get("profile", {})
    props = model.get("properties", [])
    services = model.get("services", [])
    events = model.get("events", [])
    print(f"[INFO] productId={args.product_id} identifier={profile.get('identifier')}")
    print(f"  properties: {len(props)}, services: {len(services)}, events: {len(events)}")
    if args.verbose:
        for p in props:
            print(f"    Property ref={p.get('ref')} identifier={p.get('identifier')} name={p.get('name')}")
        for s in services:
            print(f"    Service ref={s.get('ref')} identifier={s.get('identifier')} name={s.get('name')}")
        for e in events:
            print(f"    Event ref={e.get('ref')} identifier={e.get('identifier')} name={e.get('name')}")


def cmd_property_get(args):
    """Get IoT device Property values by refs."""
    token = _ensure_token()
    try:
        props_list = json.loads(args.properties) if isinstance(args.properties, str) else args.properties
        if isinstance(props_list, dict):
            props_list = list(props_list.keys())
        if not isinstance(props_list, list):
            props_list = [str(args.properties)]
    except (json.JSONDecodeError, TypeError):
        props_list = [str(p).strip() for p in args.properties.split(",")]
    r = get_iot_device_properties(
        token, args.product_id, args.serial, props_list, base_url=BASE_URL or None
    )
    if not r.get("success"):
        print(f"[ERROR] Get properties failed: {r.get('error', 'Unknown')}", file=sys.stderr)
        sys.exit(1)
    out = r.get("properties", {})
    print(f"[INFO] deviceId={args.serial} productId={args.product_id} status={r.get('status')}")
    for ref, val in out.items():
        print(f"  {ref}: {val}")
    if args.json:
        print(json.dumps({"properties": out, "status": r.get("status")}, ensure_ascii=False, indent=2))


def cmd_property_set(args):
    """Set IoT device Property values. properties = JSON object ref -> value."""
    token = _ensure_token()
    try:
        props = json.loads(args.properties) if isinstance(args.properties, str) else args.properties
        if not isinstance(props, dict):
            print("[ERROR] properties must be a JSON object, e.g. {\"3301\":1,\"3302\":2}", file=sys.stderr)
            sys.exit(1)
    except (json.JSONDecodeError, TypeError) as e:
        print(f"[ERROR] Invalid properties JSON: {e}", file=sys.stderr)
        sys.exit(1)
    r = set_iot_device_properties(
        token, args.product_id, args.serial, props, base_url=BASE_URL or None
    )
    if not r.get("success"):
        print(f"[ERROR] Set properties failed: {r.get('error', 'Unknown')}", file=sys.stderr)
        sys.exit(1)
    print(f"[SUCCESS] Properties updated for {args.serial} productId={args.product_id}")


def cmd_service_invoke(args):
    """Invoke IoT device Service (event/command). ref = service ref, content = JSON input params."""
    token = _ensure_token()
    try:
        content = json.loads(args.content) if isinstance(args.content, str) else (args.content or {})
        if not isinstance(content, dict):
            content = {}
    except (json.JSONDecodeError, TypeError):
        content = {}
    r = iot_device_control(
        token, args.product_id, args.serial, args.ref, content, base_url=BASE_URL or None
    )
    if not r.get("success"):
        print(f"[ERROR] Service invoke failed: {r.get('error', 'Unknown')}", file=sys.stderr)
        sys.exit(1)
    out = r.get("content", {})
    print(f"[SUCCESS] Service ref={args.ref} invoked for {args.serial}")
    if out:
        print(json.dumps(out, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="Imou Device Config – motion plan, sensitivity, privacy (closeCamera)."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # plan get
    p_plan = sub.add_parser("plan", help="Motion detection plan get/set.")
    p_plan_sub = p_plan.add_subparsers(dest="plan_cmd", required=True)
    p_plan_get = p_plan_sub.add_parser("get", help="Get motion detection plan.")
    p_plan_get.add_argument("serial", help="Device serial (deviceId).")
    p_plan_get.add_argument("channel_id", help="Channel ID.")
    p_plan_get.add_argument("--json", action="store_true", help="Print full JSON.")
    p_plan_get.set_defaults(func=cmd_plan_get)

    # plan set
    p_plan_set = p_plan_sub.add_parser("set", help="Set motion detection plan.")
    p_plan_set.add_argument("serial", help="Device serial.")
    p_plan_set.add_argument("channel_id", help="Channel ID.")
    p_plan_set.add_argument("--rules", required=True, help='JSON array of {period, beginTime, endTime}.')
    p_plan_set.set_defaults(func=cmd_plan_set)

    # sensitivity set
    p_sens = sub.add_parser("sensitivity", help="Motion detection sensitivity.")
    p_sens_sub = p_sens.add_subparsers(dest="sensitivity_cmd", required=True)
    p_sens_set = p_sens_sub.add_parser("set", help="Set sensitivity 1-5.")
    p_sens_set.add_argument("serial", help="Device serial.")
    p_sens_set.add_argument("channel_id", help="Channel ID.")
    p_sens_set.add_argument("level", type=int, help="Sensitivity 1-5 (1=lowest, 5=highest).")
    p_sens_set.set_defaults(func=cmd_sensitivity_set)

    # privacy get/set
    p_priv = sub.add_parser("privacy", help="Privacy mode (closeCamera) get/set.")
    p_priv_sub = p_priv.add_subparsers(dest="privacy_cmd", required=True)
    p_priv_get = p_priv_sub.add_parser("get", help="Get privacy mode status.")
    p_priv_get.add_argument("serial", help="Device serial.")
    p_priv_get.add_argument("channel_id", help="Channel ID.")
    p_priv_get.add_argument("--json", action="store_true", help="Print full JSON.")
    p_priv_get.set_defaults(func=cmd_privacy_get)

    p_priv_set = p_priv_sub.add_parser("set", help="Set privacy mode on/off.")
    p_priv_set.add_argument("serial", help="Device serial.")
    p_priv_set.add_argument("channel_id", help="Channel ID.")
    p_priv_set.add_argument("on_off", help="on or off.")
    p_priv_set.set_defaults(func=cmd_privacy_set)

    # IoT thing-model: model, property get/set, service invoke
    p_iot = sub.add_parser("iot", help="IoT thing-model: model, property get/set, service invoke.")
    p_iot_sub = p_iot.add_subparsers(dest="iot_cmd", required=True)

    p_iot_model = p_iot_sub.add_parser("model", help="Get product thing model (properties, services, events).")
    p_iot_model.add_argument("product_id", help="Product ID (from device list).")
    p_iot_model.add_argument("--json", action="store_true", help="Print full model JSON.")
    p_iot_model.add_argument("--verbose", "-v", action="store_true", help="List property/service/event refs.")
    p_iot_model.set_defaults(func=cmd_iot_model)

    p_prop_get = p_iot_sub.add_parser("property-get", help="Get IoT device Property values by refs.")
    p_prop_get.add_argument("product_id", help="Product ID.")
    p_prop_get.add_argument("serial", help="Device serial (deviceId).")
    p_prop_get.add_argument("properties", help='Property refs: JSON array e.g. ["3301","3302"] or comma-separated.')
    p_prop_get.add_argument("--json", action="store_true", help="Print full JSON.")
    p_prop_get.set_defaults(func=cmd_property_get)

    p_prop_set = p_iot_sub.add_parser("property-set", help="Set IoT device Property values.")
    p_prop_set.add_argument("product_id", help="Product ID.")
    p_prop_set.add_argument("serial", help="Device serial.")
    p_prop_set.add_argument("properties", help='JSON object ref->value e.g. {"3301":1,"3302":2}.')
    p_prop_set.set_defaults(func=cmd_property_set)

    p_svc = p_iot_sub.add_parser("service", help="Invoke IoT device Service (event/command).")
    p_svc.add_argument("product_id", help="Product ID.")
    p_svc.add_argument("serial", help="Device serial.")
    p_svc.add_argument("ref", help="Service ref from thing model.")
    p_svc.add_argument("--content", default="{}", help='JSON input params e.g. {"40":"value"}. Default {}.')
    p_svc.set_defaults(func=cmd_service_invoke)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
