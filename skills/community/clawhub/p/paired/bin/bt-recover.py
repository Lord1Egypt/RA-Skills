#!/usr/bin/env python3
"""bt-recover — Diagnose and recover a BlueZ adapter that's stuck.

Common modes of failure on the BCM43142 (and many cheap chipsets):
  * BD address shows 00:00:00:00:00:00 — firmware lost
  * "Can't init device hciN: Connection timed out" — controller wedged

This script:
  1. Reports the current state of every BlueZ adapter
  2. Runs `rfkill unblock bluetooth` and `systemctl restart bluetooth`
  3. If that doesn't recover the adapter (BD still all-zero or DOWN), it
     finds the matching USB device by VID:PID and de/re-authorises it,
     which forces the kernel to re-attach the firmware.
  4. Re-checks and reports.

Requires sudo. Either:
  * configure passwordless sudo for the commands this script runs (recommended):
      visudo -f /etc/sudoers.d/paired-bt-recover
      <youruser> ALL=(root) NOPASSWD: /usr/sbin/rfkill, /usr/bin/systemctl, /usr/sbin/hciconfig, /usr/bin/sh
  * or set SUDO_PASS in the environment before invoking (insecure on shared hosts)
  * or run interactively and let sudo prompt
"""
from __future__ import annotations
import argparse, os, subprocess, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from bt_lib import list_adapters, adapter_health


def _sudo(*args: str) -> tuple[int, str]:
    """Run a command via sudo.

    Reads password from SUDO_PASS env if set; otherwise relies on sudo's
    own prompt or a passwordless-sudo rule. NEVER hardcodes a password.
    """
    pw = os.environ.get("SUDO_PASS")
    cmd = ["sudo", "-S" if pw else "-n", *args]
    stdin_input = (pw + "\n") if pw else None
    p = subprocess.run(cmd, input=stdin_input, capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr).strip()


def _find_usb_bt() -> list[tuple[str, str, str]]:
    """Return list of (sysfs_dir, vendor, product) for USB BT controllers."""
    out = []
    for d in Path("/sys/bus/usb/devices").iterdir():
        v = d / "idVendor"
        p = d / "idProduct"
        if not v.exists() or not p.exists():
            continue
        # Only USB BT classes have a btusb-bound interface
        # Skip hubs etc.
        try:
            vid = v.read_text().strip()
            pid = p.read_text().strip()
        except OSError:
            continue
        # Look for an interface bound to btusb
        for sub in d.iterdir():
            if sub.name.startswith(d.name + ":"):
                drv = sub / "driver"
                if drv.exists() and "btusb" in os.readlink(drv):
                    out.append((str(d), vid, pid))
                    break
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Recover a stuck BlueZ adapter")
    ap.add_argument("--adapter", default="hci0")
    ap.add_argument("--force-usb-reset", action="store_true",
                    help="Skip the soft attempts and reset the USB device immediately")
    args = ap.parse_args()

    print(f"=== Initial state ===")
    for a in list_adapters():
        print(f"  {a['name']}: {a['address']} powered={a['powered']}")

    h0 = adapter_health(args.adapter)
    if h0["ok"] and not args.force_usb_reset:
        print(f"\n{args.adapter} looks healthy — no recovery needed.")
        return 0
    print(f"\n{args.adapter} unhealthy: {h0['reason']}")

    if not args.force_usb_reset:
        print("\n=== Soft recovery: rfkill + bluetooth restart ===")
        _sudo("rfkill", "unblock", "bluetooth")
        _sudo("systemctl", "restart", "bluetooth")
        time.sleep(3)
        _sudo("hciconfig", args.adapter, "up")
        time.sleep(2)
        h1 = adapter_health(args.adapter)
        if h1["ok"]:
            print(f"  Recovered: {h1['address']}")
            return 0
        print(f"  Soft recovery insufficient: {h1['reason']}")

    print("\n=== Hard recovery: USB de/re-authorise ===")
    btusb_devs = _find_usb_bt()
    if not btusb_devs:
        print("  No USB BT device found — aborting (built-in non-USB controller?)")
        return 1
    for sysdir, vid, pid in btusb_devs:
        dev = Path(sysdir).name
        print(f"  Resetting USB device {dev} (vid={vid} pid={pid})")
        _sudo("sh", "-c", f"echo 0 > {sysdir}/authorized")
        time.sleep(1)
        _sudo("sh", "-c", f"echo 1 > {sysdir}/authorized")
        time.sleep(4)

    _sudo("systemctl", "restart", "bluetooth")
    time.sleep(3)
    _sudo("hciconfig", args.adapter, "up")
    time.sleep(2)

    h2 = adapter_health(args.adapter)
    if h2["ok"]:
        print(f"\nRecovered: {h2['address']} powered={h2['powered']}")
        return 0
    print(f"\nStill unhealthy: {h2['reason']}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
