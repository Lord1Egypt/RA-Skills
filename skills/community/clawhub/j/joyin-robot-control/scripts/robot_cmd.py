#!/usr/bin/env python3
"""
JoyIn Robot Control CLI — send commands to W-1 (Walle) / M-1 (Mini) robots.

Based on the official mini_OpenAPI specification.

Environment variables:
    JOYIN_API_BASE          API base URL (e.g. https://api-open-test.joyin-ai.com)
    JOYIN_AUTH_KEY          Authorization key
    JOYIN_DEVICE_SN         Device serial number
    JOYIN_DEVICE_TYPE_ID    Device type: 3=Walle (default), 2=Mini
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.request
import urllib.error


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

def _env(key: str, default: str = "") -> str:
    return os.environ.get(key, default)


def get_config() -> dict:
    return {
        "base_url": _env("JOYIN_API_BASE", "https://api-open-test.joyin-ai.com").rstrip("/"),
        "auth_key": _env("JOYIN_AUTH_KEY"),
        "device_sn": _env("JOYIN_DEVICE_SN"),
        "device_type_id": _env("JOYIN_DEVICE_TYPE_ID", "3"),
    }


# ---------------------------------------------------------------------------
# HTTP helpers (stdlib only — zero external deps)
# ---------------------------------------------------------------------------

def _headers(cfg: dict) -> dict:
    return {
        "Content-Type": "application/json",
        "Authorization": cfg["auth_key"],
        "Device-Sn": cfg["device_sn"],
        "Device-Type-Id": str(cfg["device_type_id"]),
    }


def _request(method: str, url: str, headers: dict, body: dict | None = None) -> dict:
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        err_body = e.read().decode() if e.fp else ""
        return {"code": e.code, "msg": f"HTTP {e.code}: {err_body}"}
    except urllib.error.URLError as e:
        return {"code": -1, "msg": f"Connection error: {e.reason}"}


def post_cmd(cfg: dict, body: dict) -> dict:
    """POST /v1/device/interaction/cmd — the core robot command endpoint."""
    url = f"{cfg['base_url']}/v1/device/interaction/cmd"
    return _request("POST", url, _headers(cfg), body)


def api_get(cfg: dict, path: str) -> dict:
    return _request("GET", f"{cfg['base_url']}{path}", _headers(cfg))


def api_post(cfg: dict, path: str, body: dict) -> dict:
    return _request("POST", f"{cfg['base_url']}{path}", _headers(cfg), body)


def api_put(cfg: dict, path: str, body: dict) -> dict:
    return _request("PUT", f"{cfg['base_url']}{path}", _headers(cfg), body)


# ---------------------------------------------------------------------------
# 1. Movement — Remote Control
# ---------------------------------------------------------------------------

def cmd_rc_enter(cfg, _args):
    """Enter remote control mode."""
    return post_cmd(cfg, {"cmd_type": "remote_control", "name": "enter", "data": {}})


def cmd_rc_exit(cfg, _args):
    """Exit remote control mode."""
    return post_cmd(cfg, {"cmd_type": "remote_control", "name": "exit", "data": {}})


VALID_DIRECTIONS = ["left", "left_up", "up", "right_up", "right", "right_down", "down", "left_down"]


def cmd_move(cfg, args):
    """Chassis joystick movement — 8 directions. Send at ~100ms intervals."""
    d = args.direction
    if d not in VALID_DIRECTIONS:
        return {"code": 400, "msg": f"Invalid direction '{d}'. Valid: {VALID_DIRECTIONS}"}
    return post_cmd(cfg, {
        "cmd_type": "remote_control",
        "status": "on",
        "data": {"type": "1", "command": d},
    })


def cmd_move_stop(cfg, _args):
    """Stop chassis movement."""
    return post_cmd(cfg, {"cmd_type": "remote_control", "status": "off"})


def cmd_head(cfg, args):
    """Walle head control — up/down/left/right/stop. Send at ~100ms intervals."""
    return post_cmd(cfg, {
        "cmd_type": "remote_control",
        "status": "on",
        "data": {"command": args.direction, "control_target": "head"},
    })


def cmd_arm(cfg, args):
    """Walle arm control — left_arm/right_arm, up/down/left/right/stop."""
    target = f"{args.side}_arm"
    return post_cmd(cfg, {
        "cmd_type": "remote_control",
        "status": "on",
        "data": {"command": args.direction, "control_target": target},
    })


def cmd_reset(cfg, args):
    """Walle position reset — all/head/arm."""
    return post_cmd(cfg, {
        "cmd_type": "remote_control",
        "status": "on",
        "data": {"command": "reset", "control_target": args.target},
    })


# ---------------------------------------------------------------------------
# 2. Fixed Actions (Mini)
# ---------------------------------------------------------------------------

def cmd_car_on(cfg, _args):
    """Mini: get on car (上车)."""
    return post_cmd(cfg, {"cmd_type": "car_control", "status": "on"})


def cmd_car_off(cfg, _args):
    """Mini: get off car (下车)."""
    return post_cmd(cfg, {"cmd_type": "car_control", "status": "off"})


def cmd_standup(cfg, _args):
    """Mini: stand up (站立)."""
    return post_cmd(cfg, {"cmd_type": "standup"})


def cmd_boot_off(cfg, _args):
    """Mini: retract feet (收脚)."""
    return post_cmd(cfg, {"cmd_type": "boot_control", "status": "off"})


def cmd_boot_on(cfg, _args):
    """Mini: lock feet (卡脚)."""
    return post_cmd(cfg, {"cmd_type": "boot_control", "status": "on"})


def cmd_hello(cfg, _args):
    """Mini: wave hello (打招呼)."""
    return post_cmd(cfg, {"cmd_type": "say_hello", "status": "on"})


def cmd_hello_off(cfg, _args):
    """Mini: retract hands (收手)."""
    return post_cmd(cfg, {"cmd_type": "say_hello", "status": "off"})


def cmd_head_up(cfg, _args):
    """Mini: raise head (抬头)."""
    return post_cmd(cfg, {"cmd_type": "head_control", "status": "on"})


def cmd_head_down(cfg, _args):
    """Mini: lower head (回头)."""
    return post_cmd(cfg, {"cmd_type": "head_control", "status": "off"})


def cmd_charge(cfg, _args):
    """Go to charging station (回充)."""
    return post_cmd(cfg, {"cmd_type": "go-charge", "status": "start"})


def cmd_charge_stop(cfg, _args):
    """Stop going to charging station."""
    return post_cmd(cfg, {"cmd_type": "go-charge", "status": "stop"})


# ---------------------------------------------------------------------------
# 3. Emergency Stop
# ---------------------------------------------------------------------------

def cmd_stop(cfg, _args):
    """Emergency stop — halt all movement and functions."""
    return post_cmd(cfg, {"cmd_type": "stop"})


# ---------------------------------------------------------------------------
# 4. Voice — TTS
# ---------------------------------------------------------------------------

def cmd_tts(cfg, args):
    """Play TTS text on the robot speaker."""
    keep_silent = 1 if args.keep_silent else 0
    return post_cmd(cfg, {
        "cmd_type": "play_tts",
        "data": {"text": args.text, "keep_silent": keep_silent},
    })


# ---------------------------------------------------------------------------
# 5. Device Status & Preflight Check
# ---------------------------------------------------------------------------

WORK_MODE_NAMES = {
    "offline": "离线", "idle": "空闲", "build_map": "建图",
    "patrol": "巡逻", "ota": "OTA更新", "remote_control": "遥控中",
    "follow": "跟随中", "avtalk": "语音对话", "go_charge": "回充中",
    "guard": "监控中", "active_action": "主动动作模式",
}


def cmd_status(cfg, _args):
    """Get device status: battery, online state, charging."""
    return api_get(cfg, "/v1/device/status")


def cmd_preflight(cfg, _args):
    """Pre-flight check: verify device is online and ready. Run this BEFORE sending any command."""
    result = api_get(cfg, "/v1/device/status")
    if result.get("code") != 200:
        return {
            "ready": False,
            "reason": f"Failed to reach device API: {result.get('msg', 'unknown error')}",
            "raw": result,
        }

    data = result.get("data", {})
    current_status = data.get("current_status", "offline")
    battery = data.get("battery", -1)
    is_charging = data.get("is_charging", False)

    issues = []
    if current_status == "offline":
        issues.append("Device is OFFLINE — cannot accept commands")
    if current_status == "ota":
        issues.append("Device is updating firmware (OTA) — wait until complete")
    if isinstance(battery, (int, float)) and battery != -1 and battery < 10 and not is_charging:
        issues.append(f"Battery critically low ({battery}%) — send 'charge' command first")

    mode_name = WORK_MODE_NAMES.get(current_status, current_status)

    report = {
        "ready": len(issues) == 0,
        "current_status": current_status,
        "current_status_name": mode_name,
        "battery": battery,
        "is_charging": is_charging,
        "is_bluetooth_connected": data.get("is_bluetooth_connected", False),
    }

    if issues:
        report["issues"] = issues
        report["suggestion"] = issues[0]
    else:
        if current_status in ("follow", "remote_control", "patrol", "guard", "active_action"):
            report["note"] = f"Device is currently in '{mode_name}' mode. Some commands may conflict — use 'stop' first if needed."
        else:
            report["note"] = "Device is online and idle. Ready to accept commands."

    return report


# ---------------------------------------------------------------------------
# 6. Live Video
# ---------------------------------------------------------------------------

def cmd_live_push(cfg, args):
    """Start (1) or stop (0) live video push stream."""
    return api_get(cfg, f"/v1/live_video/stream/push?status={args.status}")


def cmd_live_pull_url(cfg, _args):
    """Get live video pull URL (HLS / RTMP)."""
    return api_get(cfg, "/v1/live_video/stream/pull_url")


def cmd_live_push_url(cfg, _args):
    """Get live video push URL."""
    return api_get(cfg, "/v1/live_video/stream/push_url")


# ---------------------------------------------------------------------------
# 7. ASR Result
# ---------------------------------------------------------------------------

def cmd_asr_result(cfg, _args):
    """Get the robot's latest ASR (speech recognition) result."""
    return api_get(cfg, "/v1/device/asr/result")


# ---------------------------------------------------------------------------
# 8. WiFi Configuration
# ---------------------------------------------------------------------------

def cmd_wifi(cfg, args):
    """Set robot WiFi (SSID and password are base64-encoded automatically)."""
    body = {
        "wifi": base64.b64encode(args.ssid.encode()).decode(),
        "passwd": base64.b64encode(args.password.encode()).decode(),
        "device_sn": cfg["device_sn"],
        "device_type_id": cfg["device_type_id"],
    }
    return api_post(cfg, "/v1/device/wifi/set", body)


# ---------------------------------------------------------------------------
# 9. LLM Configuration
# ---------------------------------------------------------------------------

def cmd_llm_register(cfg, args):
    """Register a custom LLM (OpenAI-compatible endpoint)."""
    body = {
        "llm_model_name": args.name,
        "base_url": args.base_url,
        "api_key": args.api_key,
    }
    if args.model:
        body["model"] = args.model
    return api_post(cfg, "/v1/llm/config", body)


def cmd_llm_list(cfg, _args):
    """List registered LLM models."""
    return api_get(cfg, "/v1/llm/configs")


def cmd_llm_update(cfg, args):
    """Update a registered LLM model."""
    body = {"llm_model_id": args.id}
    if args.name:
        body["model_name"] = args.name
    if args.base_url:
        body["base_url"] = args.base_url
    if args.api_key:
        body["api_key"] = args.api_key
    if args.model:
        body["model"] = args.model
    return api_put(cfg, "/v1/llm/config", body)


# ---------------------------------------------------------------------------
# 10. Agent Configuration
# ---------------------------------------------------------------------------

def cmd_agent_create(cfg, args):
    """Create an agent with a registered LLM."""
    body = {"agent_name": args.name, "llm_model_id": args.llm_id}
    if args.description:
        body["agent_description"] = args.description
    return api_post(cfg, "/v1/agent/config", body)


def cmd_agent_list(cfg, _args):
    """List agents."""
    return api_get(cfg, "/v1/agent/configs")


def cmd_agent_update(cfg, args):
    """Update an agent."""
    body = {"agent_id": args.id}
    if args.name:
        body["agent_name"] = args.name
    if args.description:
        body["agent_description"] = args.description
    if args.llm_id:
        body["llm_model_id"] = args.llm_id
    return api_put(cfg, "/v1/agent/config", body)


def cmd_agent_bind(cfg, args):
    """Bind an agent to the current device."""
    return api_post(cfg, "/v1/device/agent/bind", {
        "agent_id": args.agent_id,
        "device_sn": cfg["device_sn"],
    })


def cmd_agent_query(cfg, _args):
    """Query which agent is bound to the current device."""
    return api_get(cfg, f"/v1/device/agent/bind?device_sn={cfg['device_sn']}")


def cmd_agent_reset(cfg, _args):
    """Reset device to default JoyIn agent."""
    return api_post(cfg, "/v1/device/agent/reset", {"device_sn": cfg["device_sn"]})


# ---------------------------------------------------------------------------
# CLI Parser
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="robot_cmd", description="JoyIn Robot Control CLI")
    p.add_argument("--base-url", help="Override JOYIN_API_BASE")
    p.add_argument("--auth-key", help="Override JOYIN_AUTH_KEY")
    p.add_argument("--device-sn", help="Override JOYIN_DEVICE_SN")
    p.add_argument("--device-type-id", help="Override JOYIN_DEVICE_TYPE_ID (3=Walle, 2=Mini)")

    sub = p.add_subparsers(dest="command", required=True)

    # -- Remote control --
    sub.add_parser("rc_enter", help="Enter remote control mode").set_defaults(func=cmd_rc_enter)
    sub.add_parser("rc_exit", help="Exit remote control mode").set_defaults(func=cmd_rc_exit)

    s = sub.add_parser("move", help="Chassis movement (8 directions)")
    s.add_argument("--direction", "-d", required=True,
                   choices=VALID_DIRECTIONS,
                   help="Movement direction")
    s.set_defaults(func=cmd_move)

    sub.add_parser("move_stop", help="Stop chassis movement").set_defaults(func=cmd_move_stop)

    s = sub.add_parser("head", help="Head control (Walle)")
    s.add_argument("--direction", "-d", required=True, choices=["up", "down", "left", "right", "stop"])
    s.set_defaults(func=cmd_head)

    s = sub.add_parser("arm", help="Arm control (Walle)")
    s.add_argument("--side", "-s", required=True, choices=["left", "right"])
    s.add_argument("--direction", "-d", required=True, choices=["up", "down", "left", "right", "stop"])
    s.set_defaults(func=cmd_arm)

    s = sub.add_parser("reset", help="Reset position (Walle)")
    s.add_argument("--target", "-t", default="all", choices=["all", "head", "arm"])
    s.set_defaults(func=cmd_reset)

    # -- Fixed actions (Mini) --
    sub.add_parser("car_on", help="Get on car (上车)").set_defaults(func=cmd_car_on)
    sub.add_parser("car_off", help="Get off car (下车)").set_defaults(func=cmd_car_off)
    sub.add_parser("standup", help="Stand up (站立)").set_defaults(func=cmd_standup)
    sub.add_parser("boot_off", help="Retract feet (收脚)").set_defaults(func=cmd_boot_off)
    sub.add_parser("boot_on", help="Lock feet (卡脚)").set_defaults(func=cmd_boot_on)
    sub.add_parser("hello", help="Wave hello (打招呼)").set_defaults(func=cmd_hello)
    sub.add_parser("hello_off", help="Retract hands (收手)").set_defaults(func=cmd_hello_off)
    sub.add_parser("head_up", help="Raise head (抬头)").set_defaults(func=cmd_head_up)
    sub.add_parser("head_down", help="Lower head (回头)").set_defaults(func=cmd_head_down)
    sub.add_parser("charge", help="Go to charging station").set_defaults(func=cmd_charge)
    sub.add_parser("charge_stop", help="Stop charging return").set_defaults(func=cmd_charge_stop)

    # -- Emergency stop --
    sub.add_parser("stop", help="Emergency stop all").set_defaults(func=cmd_stop)

    # -- TTS --
    s = sub.add_parser("tts", help="Play TTS on robot")
    s.add_argument("--text", "-t", required=True, help="Text to speak")
    s.add_argument("--keep-silent", action="store_true", help="Close mic after playback")
    s.set_defaults(func=cmd_tts)

    # -- Device status & preflight --
    sub.add_parser("preflight", help="Pre-flight check: is device online & ready?").set_defaults(func=cmd_preflight)
    sub.add_parser("status", help="Get raw device status").set_defaults(func=cmd_status)

    # -- Live video --
    s = sub.add_parser("live_push", help="Start/stop live push stream")
    s.add_argument("--status", required=True, choices=["0", "1"], help="0=stop, 1=start")
    s.set_defaults(func=cmd_live_push)

    sub.add_parser("live_pull_url", help="Get live pull URL (HLS/RTMP)").set_defaults(func=cmd_live_pull_url)
    sub.add_parser("live_push_url", help="Get live push URL").set_defaults(func=cmd_live_push_url)

    # -- ASR --
    sub.add_parser("asr_result", help="Get latest ASR result").set_defaults(func=cmd_asr_result)

    # -- WiFi --
    s = sub.add_parser("wifi", help="Configure robot WiFi")
    s.add_argument("--ssid", required=True, help="WiFi SSID")
    s.add_argument("--password", required=True, help="WiFi password")
    s.set_defaults(func=cmd_wifi)

    # -- LLM config --
    s = sub.add_parser("llm_register", help="Register a custom LLM")
    s.add_argument("--name", required=True, help="Display name")
    s.add_argument("--base-url", required=True, help="OpenAI-compatible endpoint")
    s.add_argument("--api-key", required=True, help="API key")
    s.add_argument("--model", default=None, help="Model name (optional)")
    s.set_defaults(func=cmd_llm_register)

    sub.add_parser("llm_list", help="List registered LLMs").set_defaults(func=cmd_llm_list)

    s = sub.add_parser("llm_update", help="Update a registered LLM")
    s.add_argument("--id", type=int, required=True, help="LLM model ID")
    s.add_argument("--name", default=None)
    s.add_argument("--base-url", default=None)
    s.add_argument("--api-key", default=None)
    s.add_argument("--model", default=None)
    s.set_defaults(func=cmd_llm_update)

    # -- Agent config --
    s = sub.add_parser("agent_create", help="Create an agent")
    s.add_argument("--name", required=True, help="Agent name")
    s.add_argument("--llm-id", type=int, required=True, help="LLM model ID")
    s.add_argument("--description", default=None)
    s.set_defaults(func=cmd_agent_create)

    sub.add_parser("agent_list", help="List agents").set_defaults(func=cmd_agent_list)

    s = sub.add_parser("agent_update", help="Update an agent")
    s.add_argument("--id", type=int, required=True, help="Agent ID")
    s.add_argument("--name", default=None)
    s.add_argument("--description", default=None)
    s.add_argument("--llm-id", type=int, default=None)
    s.set_defaults(func=cmd_agent_update)

    s = sub.add_parser("agent_bind", help="Bind agent to device")
    s.add_argument("--agent-id", type=int, required=True, help="Agent ID")
    s.set_defaults(func=cmd_agent_bind)

    sub.add_parser("agent_query", help="Query device's bound agent").set_defaults(func=cmd_agent_query)
    sub.add_parser("agent_reset", help="Reset to default JoyIn agent").set_defaults(func=cmd_agent_reset)

    return p


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = build_parser()
    args = parser.parse_args()

    cfg = get_config()
    if args.base_url:
        cfg["base_url"] = args.base_url.rstrip("/")
    if args.auth_key:
        cfg["auth_key"] = args.auth_key
    if args.device_sn:
        cfg["device_sn"] = args.device_sn
    if args.device_type_id:
        cfg["device_type_id"] = args.device_type_id

    if not cfg["auth_key"]:
        print("Error: JOYIN_AUTH_KEY not set. Use --auth-key or set the env var.", file=sys.stderr)
        sys.exit(1)
    if not cfg["device_sn"]:
        print("Error: JOYIN_DEVICE_SN not set. Use --device-sn or set the env var.", file=sys.stderr)
        sys.exit(1)

    result = args.func(cfg, args)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    code = result.get("code", -1)
    sys.exit(0 if code in (0, 200) else 1)


if __name__ == "__main__":
    main()
