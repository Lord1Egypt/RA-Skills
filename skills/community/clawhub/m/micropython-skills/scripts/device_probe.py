#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Device auto-discovery and diagnostics for MicroPython and raw ESP devices.

Cross-platform (Windows/Linux/macOS) three-level probe chain:
  1. Scan serial ports (COM*, /dev/ttyUSB*, /dev/cu.usbserial-*)
  2. Try mpremote (MicroPython firmware present)
  3. Fall back to esptool (raw chip without firmware)

Usage:
    python3 device_probe.py [--port /dev/ttyUSB0]   # Linux
    python3 device_probe.py [--port COM3]            # Windows
    python3 device_probe.py [--port /dev/cu.usbmodem14101]  # macOS
"""

import subprocess
import json
import sys
import os
import glob
import re
import argparse


def run_cmd(cmd, timeout=10):
    """Run a shell command and return (stdout, stderr, returncode)."""
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout,
            encoding="utf-8", errors="replace"
        )
        return result.stdout, result.stderr, result.returncode
    except FileNotFoundError:
        return "", f"{cmd[0]} not found", 1
    except subprocess.TimeoutExpired:
        return "", f"Command timed out after {timeout}s", 1


def is_wsl2():
    """Detect if running under WSL2."""
    try:
        with open("/proc/version", "r") as f:
            return "microsoft" in f.read().lower()
    except OSError:
        return False


# ---------------------------------------------------------------------------
# Level 1: Serial port scanning
# ---------------------------------------------------------------------------

def _scan_windows_com_ports():
    """Fallback COM port detection on Windows using 'mode' command."""
    try:
        result = subprocess.run(
            ["mode"], capture_output=True, text=True, timeout=5
        )
        ports = re.findall(r"(COM\d+)", result.stdout)
        return [{"port": p, "readable": True} for p in sorted(set(ports))]
    except Exception:
        return []


def scan_serial_ports():
    """Scan for serial devices across platforms (Windows/Linux/macOS)."""
    # Prefer pyserial's cross-platform enumeration
    try:
        from serial.tools import list_ports
        devices = []
        for p in list_ports.comports():
            devices.append({
                "port": p.device,
                "readable": os.access(p.device, os.R_OK | os.W_OK) if sys.platform != "win32" else True,
                "description": p.description or "",
                "vid": hex(p.vid) if p.vid else None,
                "pid": hex(p.pid) if p.pid else None,
            })
        return devices
    except ImportError:
        if sys.platform == "win32":
            print("WARNING: pyserial not installed. Install with: pip install pyserial", file=sys.stderr)
            print("WARNING: Falling back to 'mode' command for COM port detection.", file=sys.stderr)

    # Fallback: platform-specific detection
    if sys.platform == "win32":
        return _scan_windows_com_ports()
    elif sys.platform == "darwin":
        paths = sorted(glob.glob("/dev/cu.usbserial-*") + glob.glob("/dev/cu.usbmodem*"))
    else:
        paths = sorted(glob.glob("/dev/ttyUSB*") + glob.glob("/dev/ttyACM*"))
    return [{"port": p, "readable": os.access(p, os.R_OK | os.W_OK)} for p in paths]


def get_usb_info():
    """Get Espressif USB device info (cross-platform)."""
    esp_keywords = ["303a:", "espressif", "cp210", "ch340", "1a86:", "10c4:", "ftdi"]

    if sys.platform == "win32":
        # On Windows, pyserial provides USB info in scan_serial_ports.
        # Without pyserial, no USB info is available.
        return []  # USB info is included in scan_serial_ports via pyserial VID/PID
    elif sys.platform == "darwin":
        stdout, _, rc = run_cmd(["system_profiler", "SPUSBDataType"], timeout=10)
        if rc != 0:
            return []
        # Extract lines near Espressif/serial chip mentions
        lines = stdout.splitlines()
        results = []
        for i, line in enumerate(lines):
            if any(kw in line.lower() for kw in esp_keywords):
                # Grab context: the device name is usually a few lines above
                context = " ".join(lines[max(0, i-3):i+1]).strip()
                results.append(context)
        return results
    else:
        # Linux: use lsusb
        stdout, _, rc = run_cmd(["lsusb"], timeout=5)
        if rc != 0:
            return []
        return [
            line.strip() for line in stdout.splitlines()
            if any(kw in line.lower() for kw in esp_keywords)
        ]


# ---------------------------------------------------------------------------
# Level 2: mpremote probe (requires MicroPython firmware)
# ---------------------------------------------------------------------------

def list_mpremote_devices():
    """List connected MicroPython devices via mpremote devs."""
    stdout, stderr, rc = run_cmd(["mpremote", "devs"])
    if rc != 0:
        return [], stderr

    devices = []
    for line in stdout.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("no "):
            continue
        parts = line.split()
        if parts:
            devices.append({"port": parts[0], "info": " ".join(parts[1:])})
    return devices, ""


def probe_micropython(port=None):
    """Connect to a device via mpremote and gather MicroPython system info."""
    connect_args = ["connect", port] if port else []

    probe_code = """
import sys, gc, json
try:
    import machine
    freq = machine.freq()
except:
    freq = 0
gc.collect()
info = {
    "platform": sys.platform,
    "version": sys.version,
    "implementation": {
        "name": sys.implementation.name,
        "version": list(sys.implementation.version),
    },
    "freq_mhz": freq // 1000000 if freq else 0,
    "mem_free_kb": gc.mem_free() // 1024,
    "mem_alloc_kb": gc.mem_alloc() // 1024,
}
try:
    import os
    u = os.uname()
    info["uname"] = {"sysname": u.sysname, "machine": u.machine, "release": u.release}
    s = os.statvfs("/")
    info["storage_total_kb"] = (s[0] * s[2]) // 1024
    info["storage_free_kb"] = (s[0] * s[3]) // 1024
except:
    pass
try:
    import network
    w = network.WLAN(network.STA_IF)
    info["wifi_available"] = True
    info["wifi_connected"] = w.isconnected()
    if w.isconnected():
        info["wifi_ip"] = w.ifconfig()[0]
except:
    info["wifi_available"] = False
print("PROBE_JSON:" + json.dumps(info))
"""
    stdout, stderr, rc = run_cmd(
        ["mpremote"] + connect_args + ["exec", probe_code], timeout=15
    )

    if rc != 0:
        return None, stderr.strip() or stdout.strip() or "Failed to connect"

    for line in stdout.splitlines():
        if line.startswith("PROBE_JSON:"):
            try:
                return json.loads(line[len("PROBE_JSON:"):]), ""
            except json.JSONDecodeError as e:
                return None, f"JSON parse error: {e}"

    return None, f"No probe data received. Output: {stdout[:200]}"


# ---------------------------------------------------------------------------
# Level 3: esptool probe (raw chip without MicroPython)
# ---------------------------------------------------------------------------

def probe_esptool(port):
    """Use esptool to detect chip type, MAC, and flash info on a raw device."""
    # Try 'esptool' first (new name), fall back to 'esptool.py' (deprecated)
    esptool_cmd = None
    for name in ["esptool", "esptool.py"]:
        for ver_arg in ["version", "--version"]:
            _, _, rc = run_cmd([name, ver_arg], timeout=5)
            if rc == 0:
                esptool_cmd = name
                break
        if esptool_cmd:
            break
    if not esptool_cmd:
        return None, "esptool not found. Install with: pip install esptool"

    # Run chip-id (esptool v5+) or chip_id (older) to get chip type and MAC
    # Try v5 command first, fall back to legacy
    for subcmd in ["chip-id", "chip_id"]:
        stdout, stderr, rc = run_cmd(
            [esptool_cmd, "--port", port, subcmd], timeout=15
        )
        combined = stdout + stderr
        if "deprecated" not in combined.lower() or "chip" in combined.lower():
            break

    # Strip ANSI escape codes for reliable parsing
    combined = re.sub(r"\x1b\[[0-9;]*[a-zA-Z]", "", combined)

    # Check for permission error
    if "not readable" in combined.lower() or "permission" in combined.lower():
        if sys.platform == "win32":
            return None, f"Permission denied on {port}. Check Device Manager for driver issues."
        return None, f"Permission denied on {port}. Run: sudo chmod 666 {port}"

    # Check for connection error
    if rc != 0 and ("failed" in combined.lower() or "error" in combined.lower()):
        return None, (
            f"esptool cannot connect to {port}. "
            "The device may need to be in bootloader mode: "
            "hold BOOT button, press RESET, then release BOOT."
        )

    info = {"port": port}

    # Parse chip type — esptool v5 uses "Chip type:", older uses "Chip is"
    chip_match = re.search(r"Chip (?:type|is)[:\s]+(ESP\S+)", combined, re.IGNORECASE)
    if chip_match:
        chip_raw = chip_match.group(1).lower()
        # Normalize: "ESP32-C6" -> "esp32c6", strip suffixes like "(QFN40)"
        chip_raw = re.sub(r"\(.*", "", chip_raw).strip()
        info["chip"] = chip_raw.replace("-", "")

    # Parse MAC address
    mac_match = re.search(r"MAC:\s*([0-9a-f:]{17})", combined, re.IGNORECASE)
    if mac_match:
        info["mac"] = mac_match.group(1).lower()

    # Parse chip ID
    id_match = re.search(r"Chip ID:\s*(0x[0-9a-f]+)", combined, re.IGNORECASE)
    if id_match:
        info["chip_id"] = id_match.group(1)

    # Get flash info (v5: flash-id, legacy: flash_id)
    for subcmd in ["flash-id", "flash_id"]:
        stdout2, stderr2, rc2 = run_cmd(
            [esptool_cmd, "--port", port, subcmd], timeout=15
        )
        combined2 = re.sub(r"\x1b\[[0-9;]*[a-zA-Z]", "", stdout2 + stderr2)
        if "flash" in combined2.lower():
            break

    flash_match = re.search(r"(?:Detected |)flash size:\s*(\d+)\s*([MK])B", combined2, re.IGNORECASE)
    if flash_match:
        size = int(flash_match.group(1))
        unit = flash_match.group(2).upper()
        info["flash_size_mb"] = size if unit == "M" else size / 1024

    # Parse crystal frequency
    crystal_match = re.search(r"Crystal is (\d+)MHz", combined)
    if crystal_match:
        info["crystal_mhz"] = int(crystal_match.group(1))

    if "chip" not in info:
        return None, f"Could not identify chip on {port}. esptool output: {combined[:300]}"

    return info, ""


# ---------------------------------------------------------------------------
# Main: Three-level probe chain
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Probe MicroPython and raw ESP devices"
    )
    parser.add_argument("--port", help="Specific serial port to connect to")
    args = parser.parse_args()

    # === Level 1: Scan serial ports ===
    serial_ports = scan_serial_ports()
    usb_info = get_usb_info()

    if not serial_ports and not args.port:
        result = {
            "status": "no_device",
            "serial_ports": [],
            "usb_devices": usb_info,
            "error": "No serial devices found on USB",
        }
        if is_wsl2():
            result["hint"] = (
                "Running under WSL2. USB devices need to be forwarded from Windows "
                "using usbipd. Run in PowerShell (admin): "
                "usbipd list; usbipd bind --busid <BUSID>; usbipd attach --wsl --busid <BUSID>"
            )
        print(json.dumps(result, indent=2))
        sys.exit(1)

    port = args.port or serial_ports[0]["port"]

    # Check if port is accessible
    if not args.port and serial_ports and not serial_ports[0]["readable"]:
        result = {
            "status": "permission_denied",
            "port": port,
            "serial_ports": serial_ports,
            "usb_devices": usb_info,
            "error": f"Serial port {port} is not accessible (permission denied)",
            "fix": (
                "Check Device Manager — the COM port driver may need reinstalling"
                if sys.platform == "win32"
                else f"Run: sudo chmod 666 {port}"
            ),
        }
        print(json.dumps(result, indent=2))
        sys.exit(1)

    # === Level 2: Try mpremote (MicroPython) ===
    mp_devices, _ = list_mpremote_devices()
    if mp_devices:
        info, err = probe_micropython(port)
        if info is not None:
            result = {
                "status": "ok",
                "firmware": "micropython",
                "port": port,
                "serial_ports": serial_ports,
                **info,
            }
            print(json.dumps(result, indent=2))
            return

    # === Level 3: Try esptool (raw chip) ===
    info, err = probe_esptool(port)
    if info is not None:
        result = {
            "status": "no_firmware",
            "firmware": None,
            "serial_ports": serial_ports,
            "usb_devices": usb_info,
            **info,
            "action_hint": (
                "ESP chip detected but no MicroPython firmware. "
                "Run firmware_flash.py to download and install MicroPython."
            ),
        }
        print(json.dumps(result, indent=2))
        sys.exit(0)

    # === All levels failed ===
    result = {
        "status": "unknown_device",
        "port": port,
        "serial_ports": serial_ports,
        "usb_devices": usb_info,
        "error": err or "Could not identify device",
    }
    if "bootloader" in (err or "").lower() or "permission" in (err or "").lower():
        result["hint"] = err
    print(json.dumps(result, indent=2))
    sys.exit(1)


if __name__ == "__main__":
    main()
