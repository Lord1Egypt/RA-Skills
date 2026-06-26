#!/usr/bin/env python3
"""bt-test — Self-test the bluetooth skill stack.

Runs a series of read-only checks across BlueZ, the agent, PipeWire,
OBEX and ofono, prints a clean pass/fail report, and exits non-zero if
anything looks wrong. Safe to run any time — does not pair, connect,
write, transfer or send.

Use this when:
  - troubleshooting a flaky pair/connect
  - confirming after a reboot that the stack came back up
  - in a healthcheck cron
"""
from __future__ import annotations
import json, os, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))


CHECKS = []


def check(name: str):
    def deco(fn):
        CHECKS.append((name, fn))
        return fn
    return deco


@check("BlueZ system bus reachable")
def chk_bluez():
    import bt_lib
    adapters = bt_lib.list_adapters()
    if not adapters:
        return False, "no adapters present"
    return True, f"{len(adapters)} adapter(s): {', '.join(a['name'] for a in adapters)}"


@check("All adapters healthy")
def chk_adapter_health():
    import bt_lib
    bad = []
    for a in bt_lib.list_adapters():
        h = bt_lib.adapter_health(a["name"])
        if not h["ok"]:
            bad.append(f"{a['name']}: {h['reason']}")
    if bad:
        return False, "; ".join(bad)
    return True, "all powered, BD addresses non-zero"


@check("Pairing agent (bt-agent.service) active")
def chk_agent():
    p = subprocess.run(["systemctl", "--user", "is-active", "bt-agent.service"],
                       capture_output=True, text=True)
    if p.stdout.strip() == "active":
        return True, "active"
    return False, p.stdout.strip() or "not active"


@check("PipeWire/WirePlumber active")
def chk_pipewire():
    units = ["pipewire.service", "pipewire-pulse.service", "wireplumber.service"]
    bad = []
    for u in units:
        p = subprocess.run(["systemctl", "--user", "is-active", u],
                           capture_output=True, text=True)
        if p.stdout.strip() != "active":
            bad.append(f"{u}: {p.stdout.strip()}")
    if bad:
        return False, "; ".join(bad)
    return True, "pipewire + pipewire-pulse + wireplumber all active"


@check("PipeWire BT codec plug-in present")
def chk_libspa():
    p = "/usr/lib/x86_64-linux-gnu/spa-0.2/bluez5/libspa-bluez5.so"
    if Path(p).exists():
        return True, "libspa-bluez5.so present"
    return False, "libspa-0.2-bluetooth not installed"


@check("OBEX (org.bluez.obex) on session bus")
def chk_obex():
    p = subprocess.run(["busctl", "--user", "list"], capture_output=True, text=True)
    if "org.bluez.obex" in p.stdout:
        return True, "registered (or activatable)"
    return False, "not registered/activatable"


@check("ofono active and accessible to current user")
def chk_ofono():
    p = subprocess.run(["systemctl", "is-active", "ofono"], capture_output=True, text=True)
    if p.stdout.strip() != "active":
        return False, f"ofono.service: {p.stdout.strip()}"
    # Make sure we can actually call it as user (not root)
    try:
        import bt_telephony
        modems = bt_telephony.list_modems()
        return True, f"{len(modems)} modem(s) currently registered"
    except Exception as e:
        return False, f"D-Bus access denied? {e}"


@check("All bt-* commands on PATH")
def chk_path():
    expected = [
        "bt-adapters", "bt-list", "bt-info", "bt-pair", "bt-connect",
        "bt-disconnect", "bt-trust", "bt-untrust", "bt-forget",
        "bt-gatt-read", "bt-gatt-write", "bt-gatt-tree", "bt-recover",
        "bt-audio", "bt-play", "bt-volume", "bt-send", "bt-receive",
        "bt-browse", "bt-modems", "bt-call", "bt-sms-send", "bt-sms-list",
        "bt-contacts", "bt-media", "bt-pan", "bt-battery",
        "bt-adb-setup", "bt-adb-sms-list", "bt-adb-sms-send",
        "bt-adb-push", "bt-adb-pull", "bt-adb-battery", "bt-adb-notif",
        "bt-adb-screenshot", "bt-adb-launch", "bt-adb-type", "bt-adb-media",
    ]
    bin_dir = Path.home() / "bin"
    missing = [c for c in expected if not (bin_dir / c).exists()]
    if missing:
        return False, f"missing: {', '.join(missing)}"
    return True, f"all {len(expected)} present"


@check("Shared libraries importable")
def chk_libs():
    try:
        import bt_lib, bt_audio, bt_obex, bt_telephony, bt_obex_msg, bt_adb, bt_media
        return True, "all 7 libraries import"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"



@check("ADB available + at least one device (optional)")
def chk_adb():
    import subprocess
    try:
        p = subprocess.run(["/usr/bin/adb", "devices"],
                            capture_output=True, text=True, timeout=5)
    except FileNotFoundError:
        return True, "adb not installed (skip — only needed for bt-adb-* tools)"
    except subprocess.TimeoutExpired:
        return False, "adb hung"
    devs = [l.split()[0] for l in p.stdout.splitlines()
            if l.strip() and not l.startswith("List of") and "device" in l]
    if not devs:
        return True, "adb installed but no devices (only needed for bt-adb-* tools)"
    return True, f"{len(devs)} device(s): {', '.join(devs)}"


def main() -> int:
    json_out = "--json" in sys.argv
    results = []
    pass_count = 0
    fail_count = 0
    for name, fn in CHECKS:
        try:
            ok, detail = fn()
        except Exception as e:
            ok, detail = False, f"{type(e).__name__}: {e}"
        results.append({"check": name, "ok": ok, "detail": detail})
        if ok:
            pass_count += 1
        else:
            fail_count += 1

    if json_out:
        print(json.dumps({"pass": pass_count, "fail": fail_count, "results": results}, indent=2))
        return 1 if fail_count else 0

    width = max(len(r["check"]) for r in results) + 2
    for r in results:
        sym = "OK  " if r["ok"] else "FAIL"
        print(f"  [{sym}]  {r['check']:<{width}}  {r['detail']}")
    print()
    print(f"{pass_count} passed, {fail_count} failed")
    return 1 if fail_count else 0


if __name__ == "__main__":
    sys.exit(main())
