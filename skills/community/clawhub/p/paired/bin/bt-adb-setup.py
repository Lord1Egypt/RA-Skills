#!/usr/bin/env python3
"""bt-adb-setup — first-run helper.

Walks through the steps to get an Android phone working with the bluetooth
skill via ADB on .86. After this completes, the other bt-adb-* tools work.

  bt-adb-setup            # interactive
  bt-adb-setup --check    # just verify current state, no changes
"""
from __future__ import annotations
import argparse, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import bt_adb


def main() -> int:
    ap = argparse.ArgumentParser(description="ADB-companion first-run setup")
    ap.add_argument("--check", action="store_true",
                    help="Just verify, don't prompt for next steps")
    args = ap.parse_args()

    print("=== ADB binary ===")
    try:
        v = bt_adb._adb("version", timeout=5)
        print("  " + v.splitlines()[0])
    except Exception as e:
        print(f"  ADB not working: {e}")
        return 1

    print("\n=== Devices ===")
    devs = bt_adb.list_devices()
    if not devs:
        print("  No devices.")
        if not args.check:
            print("  Plug phone in via USB to .86 directly.")
            print("  On phone: enable Developer options + USB debugging, accept the prompt.")
        return 1

    ok_devs = [d for d in devs if d.get("state") == "device"]
    bad_devs = [d for d in devs if d.get("state") != "device"]
    for d in ok_devs:
        print(f"  OK   {d['serial']}  model={d.get('model', '?')}")
    for d in bad_devs:
        print(f"  --   {d['serial']}  state={d.get('state')}  "
              f"(if 'unauthorized', accept the prompt on the phone)")

    if not ok_devs:
        return 1

    print("\n=== Phone identity ===")
    info = bt_adb.device_info()
    for k, v in info.items():
        print(f"  {k:<18}  {v}")

    print("\n=== Battery ===")
    b = bt_adb.battery()
    print(f"  level:    {b['level_pct']}%")
    print(f"  voltage:  {b['voltage_mv']} mV")
    print(f"  temp:     {b['temperature_c']}°C")
    print(f"  charging: USB={b['usb_powered']} AC={b['ac_powered']}")

    print("\n=== Quick capability check ===")
    capabilities = []
    # SMS read
    try:
        sms = bt_adb.sms_inbox(limit=1)
        capabilities.append(("SMS read (inbox)", "OK" if sms else "no messages",
                              "bt-adb-sms-list"))
    except Exception as e:
        capabilities.append(("SMS read (inbox)", f"FAIL: {e}", "bt-adb-sms-list"))
    # File push (use empty in-memory file)
    try:
        import tempfile
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("hello")
            tmp = f.name
        bt_adb.push(tmp, "/sdcard/Download/.paired-probe.txt")
        bt_adb.shell("rm /sdcard/Download/.paired-probe.txt")
        Path(tmp).unlink(missing_ok=True)
        capabilities.append(("File push", "OK", "bt-adb-push"))
    except Exception as e:
        capabilities.append(("File push", f"FAIL: {e}", "bt-adb-push"))
    # Notifications dumpsys
    try:
        bt_adb.shell("dumpsys notification | head -1", timeout=5)
        capabilities.append(("Notifications (dumpsys)", "OK", "bt-adb-notif"))
    except Exception as e:
        capabilities.append(("Notifications (dumpsys)", f"FAIL: {e}", "bt-adb-notif"))

    for name, status, tool in capabilities:
        sym = "OK  " if status == "OK" else "WARN"
        print(f"  [{sym}]  {name:<28}  {status:<22}  → {tool}")

    print("\nSetup complete. Try:  bt-adb-sms-list   bt-adb-battery   bt-adb-screenshot")
    return 0


if __name__ == "__main__":
    sys.exit(main())
