#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HCT Alarm - OpenClaw Hooks Pre-Check
Checks whether OpenClaw hooks are properly configured and reachable.
Run this BEFORE any other alarm configuration steps.
"""

import sys
import os
import json
import urllib.request
import urllib.error
import argparse
from datetime import datetime

OPENCLAW_CFG = os.path.expanduser("~/.openclaw/openclaw.json")
CHECKS = []


def log(status, msg):
    symbol = {"OK": "✓", "FAIL": "✗", "SKIP": "⊘", "INFO": "ℹ"}.get(status, "?")
    print(f"  [{status}] {msg}")
    CHECKS.append({"status": status, "msg": msg})


def check_config_file():
    if not os.path.exists(OPENCLAW_CFG):
        log("FAIL", f"Config file not found: {OPENCLAW_CFG}")
        return False
    try:
        with open(OPENCLAW_CFG, "r") as f:
            json.load(f)
        log("OK", "Config file is valid JSON")
        return True
    except json.JSONDecodeError as e:
        log("FAIL", f"Config file is not valid JSON: {e}")
        return False


def check_hooks_enabled():
    with open(OPENCLAW_CFG, "r") as f:
        config = json.load(f)
    hooks = config.get("hooks", {})
    if hooks.get("enabled") is True:
        log("OK", "hooks.enabled = true")
        return True
    log("FAIL", "hooks.enabled is not true (or hooks section missing)")
    return False


def check_hooks_token():
    with open(OPENCLAW_CFG, "r") as f:
        config = json.load(f)
    hooks = config.get("hooks", {})
    token = hooks.get("token", "")
    if token and isinstance(token, str) and len(token) > 0:
        log("OK", f"hooks.token is set ({len(token)} chars)")
        return True, token
    log("FAIL", "hooks.token is missing or empty")
    return False, None


def check_token_not_same_as_gateway():
    with open(OPENCLAW_CFG, "r") as f:
        config = json.load(f)
    hooks = config.get("hooks", {})
    gateway = config.get("gateway", {})
    hooks_token = hooks.get("token", "")
    gateway_token = gateway.get("auth", {}).get("token", "")
    if hooks_token and gateway_token and hooks_token == gateway_token:
        log("FAIL", "hooks.token must be different from gateway.auth.token")
        return False
    log("OK", "hooks.token differs from gateway.auth.token")
    return True


def check_gateway_port():
    with open(OPENCLAW_CFG, "r") as f:
        config = json.load(f)
    gateway = config.get("gateway", {})
    port = gateway.get("port", "")
    if port:
        log("OK", f"gateway.port = {port}")
        return True, port
    log("FAIL", "gateway.port is not set")
    return False, None


def check_hooks_reachable(hooks_token, port):
    url = f"http://127.0.0.1:{port}/hooks/agent"
    body = json.dumps({"source": "pre_check"}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Authorization": f"Bearer {hooks_token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            code = resp.status
            data = resp.read().decode("utf-8")
            log("OK", f"Hooks endpoint reachable (HTTP {code})")
            return True
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        if e.code == 400 and "message required" in body.lower():
            log("OK", f"Hooks endpoint reachable (HTTP 400 — endpoint alive, needs message body)")
            return True
        log("FAIL", f"HTTP {e.code}: {body[:100]}")
        return False
    except urllib.error.URLError as e:
        log("FAIL", f"Cannot reach OpenClaw gateway: {e.reason}")
        return False
    except Exception as e:
        log("FAIL", f"Unexpected error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="OpenClaw Hooks Pre-Check for HCT Alarm")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] OpenClaw Hooks Pre-Check")
    print("=" * 50)

    all_passed = True

    if not check_config_file():
        all_passed = False

    if not check_hooks_enabled():
        all_passed = False

    token_ok, hooks_token = check_hooks_token()
    if not token_ok:
        all_passed = False

    if not check_token_not_same_as_gateway():
        all_passed = False

    port_ok, port = check_gateway_port()
    if not port_ok:
        all_passed = False

    if token_ok and port_ok:
        if not check_hooks_reachable(hooks_token, port):
            all_passed = False
    else:
        log("SKIP", "Skipping reachability check (config not ready)")

    print("=" * 50)
    if all_passed:
        print("[RESULT] ✓ All checks passed. OpenClaw hooks are ready.")
    else:
        print("[RESULT] ✗ Some checks failed. Fix the issues above before proceeding.")

    if args.json:
        print(json.dumps({"ok": all_passed, "checks": CHECKS}, indent=2, ensure_ascii=False))

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
