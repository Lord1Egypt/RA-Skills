#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WiFi configuration and WebREPL enablement for MicroPython devices.

Pushes WiFi + WebREPL configuration to a device via mpremote USB connection.
After successful setup, the device can be accessed wirelessly via WebREPL.

Usage:
    python3 wifi_setup.py --ssid "MyWiFi" --password "secret" [--webrepl-password "repl123"] [--port /dev/ttyUSB0]
"""

import subprocess
import json
import sys
import argparse
import re


def run_mpremote(*args, timeout=30):
    """Run an mpremote command and return (stdout, stderr, returncode)."""
    cmd = ["mpremote"] + list(args)
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout,
            encoding="utf-8", errors="replace"
        )
        return result.stdout, result.stderr, result.returncode
    except FileNotFoundError:
        return "", "mpremote not found. Install with: pip install mpremote", 1
    except subprocess.TimeoutExpired:
        return "", f"mpremote timed out after {timeout}s", 1


def setup_wifi(ssid, password, webrepl_password, port=None):
    """Push WiFi + WebREPL config to device."""
    connect_args = ["connect", port] if port else []

    # MicroPython code to execute on device
    setup_code = f"""
import network, time, json

# Connect to WiFi
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect({ssid!r}, {password!r})

# Wait for connection with timeout
timeout = 15
start = time.time()
while not sta.isconnected():
    if time.time() - start > timeout:
        print("ERROR:WiFi connection timed out after " + str(timeout) + "s")
        raise SystemExit
    time.sleep(0.5)

ip = sta.ifconfig()[0]
print("LOG:WiFi connected, IP: " + ip)

# Configure WebREPL password
try:
    with open("webrepl_cfg.py", "w") as f:
        f.write("PASS = " + repr({webrepl_password!r}) + "\\n")
    print("LOG:WebREPL password configured")
except Exception as e:
    print("ERROR:Failed to write webrepl_cfg.py: " + str(e))
    raise SystemExit

# Enable WebREPL
try:
    import webrepl
    webrepl.start()
    print("LOG:WebREPL started on port 8266")
except Exception as e:
    print("ERROR:Failed to start WebREPL: " + str(e))
    raise SystemExit

# Write boot.py for auto-connect on power-up
boot_code = '''
import network, time
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect({ssid!r}, {password!r})
for _ in range(30):
    if sta.isconnected():
        break
    time.sleep(0.5)
import webrepl
webrepl.start()
'''

try:
    # Backup existing boot.py
    try:
        with open("boot.py", "r") as f:
            backup = f.read()
        with open("boot.py.bak", "w") as f:
            f.write(backup)
        print("LOG:Existing boot.py backed up to boot.py.bak")
    except OSError:
        pass

    with open("boot.py", "w") as f:
        f.write(boot_code)
    print("LOG:boot.py updated for auto-connect")
except Exception as e:
    print("ERROR:Failed to write boot.py: " + str(e))
    raise SystemExit

print("RESULT:" + json.dumps({{"ip": ip, "webrepl_port": 8266, "webrepl_password": {webrepl_password!r}}}))
"""

    stdout, stderr, rc = run_mpremote(
        *connect_args, "exec", setup_code, timeout=30
    )

    return stdout, stderr, rc


def main():
    parser = argparse.ArgumentParser(
        description="Configure WiFi and WebREPL on MicroPython device"
    )
    parser.add_argument("--ssid", required=True, help="WiFi network name")
    parser.add_argument("--password", required=True, help="WiFi password")
    parser.add_argument(
        "--webrepl-password", default="micropython",
        help="WebREPL access password (default: micropython)"
    )
    parser.add_argument("--port", help="Specific serial port to connect to")
    args = parser.parse_args()

    stdout, stderr, rc = setup_wifi(
        args.ssid, args.password, args.webrepl_password, args.port
    )

    # Print all output for the agent to parse
    if stdout:
        print(stdout)
    if stderr:
        print(stderr, file=sys.stderr)

    # Extract RESULT line for summary
    for line in (stdout or "").splitlines():
        if line.startswith("RESULT:"):
            try:
                data = json.loads(line[len("RESULT:"):])
                print(f"\nSetup complete. Device accessible at ws://{data['ip']}:{data['webrepl_port']}", file=sys.stderr)
            except json.JSONDecodeError:
                pass
            break
    else:
        if rc != 0:
            print("\nSetup failed. Check error messages above.", file=sys.stderr)

    sys.exit(rc)


if __name__ == "__main__":
    main()
